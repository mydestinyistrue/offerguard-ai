"""MCA (Ministry of Corporate Affairs) Company Lookup Service.

Queries the local SQLite snapshot of data.gov.in company master data using
RapidFuzz for fuzzy matching and returns one of three honest outcomes:
1. Found and active
2. Not found in snapshot
3. Suspicious match
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Optional
from rapidfuzz import fuzz

try:
    from app.core.config import get_settings
    _HAVE_SETTINGS = True
except ImportError:
    _HAVE_SETTINGS = False

try:
    from app.models.schemas import CompanyInfo
except ImportError:
    from dataclasses import dataclass, field
    @dataclass
    class CompanyInfo:  # type: ignore[no-redef]
        name: Optional[str] = None
        cin: Optional[str] = None
        domain: Optional[str] = None
        mca_match: Optional[bool] = None
        match_score: Optional[float] = None
        status: Optional[str] = None
        roc: Optional[str] = None
        state: Optional[str] = None
        verification_outcome: Optional[str] = None
        domain_signals: list = field(default_factory=list)
        virustotal: Optional[Any] = None


_CIN_REGEX = re.compile(r"\b([LU]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6})\b", re.IGNORECASE)

# Common company name suffixes/noise words
_STOPWORDS = {"pvt", "private", "ltd", "limited", "llp", "corp", "corporation", "inc", "co", "company", "india", "services", "solutions", "technologies", "tech"}


def normalize_company_name(name: str) -> str:
    """Normalize company name for comparison."""
    clean = re.sub(r"[^\w\s]", " ", name.lower())
    tokens = [w for w in clean.split() if w not in _STOPWORDS and len(w) > 1]
    return " ".join(tokens)


def extract_cin_from_text(text: str) -> Optional[str]:
    """Extract a valid format Indian CIN from text if present."""
    match = _CIN_REGEX.search(text)
    if match:
        return match.group(1).upper()
    return None


def extract_potential_company_names(text: str) -> list[str]:
    """Extract potential company names mentioned in the text."""
    candidates = []
    # Known big companies to look for
    known_brands = [
        "Tata Consultancy Services", "TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra",
        "Google India", "Google", "Microsoft", "Amazon", "Flipkart", "Meesho", "Swiggy",
        "Zomato", "Reliance", "Jio", "State Bank of India", "SBI", "HDFC", "ICICI",
        "Taskforce", "Global Rating", "Deloitte", "Internshala", "Naukri",
        "Digital Task", "Telegram Online Task", "YouTube Promotion Agency"
    ]
    for brand in known_brands:
        if re.search(r"\b" + re.escape(brand) + r"\b", text, re.I):
            candidates.append(brand)

    # Patterns like "company: X", "at X Limited", "welcome to X"
    patterns = [
        r"(?:welcome to|working with|joined|representing|from)\s+([A-Z][A-Za-z0-9\s&]{2,30}(?:Pvt|Private|Ltd|Limited|LLP|Technologies|Services|Digital))",
        r"(?:company|organization|firm|agency):\s*([A-Za-z0-9\s&]{3,40})",
        r"([A-Z][A-Za-z0-9\s&]{2,25})\s+(?:Pvt\s*Ltd|Private\s*Limited|Limited|LLP)",
    ]
    for pat in patterns:
        for match in re.finditer(pat, text, re.I):
            extracted = match.group(1).strip()
            if extracted and len(extracted) > 3 and extracted not in candidates:
                candidates.append(extracted)

    return candidates


class MCALookupService:
    def __init__(self, db_path: Optional[Path] = None):
        settings = get_settings() if _HAVE_SETTINGS else None
        possible_paths = [
            db_path,
            (settings.DATA_DIR / "mca.sqlite") if settings and hasattr(settings, "DATA_DIR") else None,
            Path(__file__).parent / "mca.sqlite",
            Path(__file__).parent / "data" / "mca.sqlite",
            Path(__file__).resolve().parent.parent.parent / "data" / "mca.sqlite",
            Path.cwd() / "data" / "mca.sqlite",
            Path.cwd() / "backend" / "data" / "mca.sqlite",
        ]
        self.db_path = next((p for p in possible_paths if p and p.exists()), db_path or Path("data/mca.sqlite"))
        self._cached_companies: list[dict] = []
        self._load_cache()

    def _load_cache(self):
        """Pre-load company records in memory for fast fuzzy matching."""
        if not self.db_path.exists():
            return
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT cin, company_name, company_name_normalized, status, roc, state, email FROM companies")
            self._cached_companies = [dict(row) for row in cur.fetchall()]
            conn.close()
        except Exception:
            self._cached_companies = []

    def lookup_by_cin(self, cin: str) -> Optional[dict]:
        """Direct lookup by Corporate Identification Number."""
        cin_clean = cin.strip().upper()
        for comp in self._cached_companies:
            if comp["cin"].upper() == cin_clean:
                return comp
        return None

    def search_company(self, query: str, threshold: float = 65.0) -> Optional[dict]:
        """Fuzzy search company by name."""
        if not query or not self._cached_companies:
            return None

        norm_query = normalize_company_name(query)
        if not norm_query:
            norm_query = query.lower().strip()

        best_match = None
        best_score = 0.0

        for comp in self._cached_companies:
            norm_target = comp["company_name_normalized"] or normalize_company_name(comp["company_name"])
            
            # Compute multiple fuzzy metrics
            score_sort = fuzz.token_sort_ratio(norm_query, norm_target)
            score_set = fuzz.token_set_ratio(norm_query, norm_target)
            score_partial = fuzz.partial_ratio(norm_query, norm_target)
            
            score = max(score_sort, score_set, score_partial * 0.9)
            if score > best_score:
                best_score = score
                best_match = comp

        if best_match and best_score >= threshold:
            res = dict(best_match)
            res["match_score"] = round(best_score, 1)
            return res

        return None

    def verify_company_in_text(self, text: str) -> CompanyInfo:
        """Scan text for company claims or CIN and return verified CompanyInfo."""
        extracted_cin = extract_cin_from_text(text)
        candidates = extract_potential_company_names(text)

        # 1. If CIN found
        if extracted_cin:
            rec = self.lookup_by_cin(extracted_cin)
            if rec:
                status = rec.get("status", "Active")
                is_active = "active" in status.lower()
                outcome = "Found and active" if is_active else "Suspicious match (Status: " + status + ")"
                return CompanyInfo(
                    name=rec["company_name"],
                    cin=rec["cin"],
                    status=status,
                    roc=rec.get("roc"),
                    state=rec.get("state"),
                    mca_match=True,
                    match_score=100.0,
                    verification_outcome=outcome,
                )
            else:
                return CompanyInfo(
                    cin=extracted_cin,
                    mca_match=False,
                    match_score=0.0,
                    verification_outcome="Not found in snapshot (CIN claimed but not in ROC master)",
                )

        # 2. If company names extracted
        if candidates:
            best_info = None
            highest_score = 0.0
            
            for candidate in candidates:
                match = self.search_company(candidate)
                if match and match["match_score"] > highest_score:
                    highest_score = match["match_score"]
                    status = match.get("status", "Active")
                    is_active = "active" in status.lower()
                    
                    if not is_active:
                        outcome = f"Suspicious match — Status is {status}"
                    elif highest_score >= 85:
                        outcome = "Found and active (Registration verified; recruiter authenticity must still be verified)"
                    else:
                        outcome = f"Partial match with {match['company_name']}"

                    best_info = CompanyInfo(
                        name=match["company_name"],
                        cin=match["cin"],
                        status=status,
                        roc=match.get("roc"),
                        state=match.get("state"),
                        mca_match=True,
                        match_score=highest_score,
                        verification_outcome=outcome,
                    )

            if best_info:
                return best_info
            
            # If candidate found but no MCA match
            return CompanyInfo(
                name=candidates[0],
                mca_match=False,
                match_score=0.0,
                verification_outcome="Not found in MCA snapshot. Please verify credentials on mca.gov.in before sharing details.",
            )

        return CompanyInfo(
            verification_outcome="No specific company name or CIN identified in input text."
        )


_mca_service: Optional[MCALookupService] = None

def get_mca_service() -> MCALookupService:
    global _mca_service
    if _mca_service is None:
        _mca_service = MCALookupService()
    return _mca_service
