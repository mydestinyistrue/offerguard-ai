"""CompanyVerifier: Standalone verification of corporate claims, MCA records, and domain legitimacy."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List, Dict, Any

from .mca_lookup import MCALookupService, get_mca_service
from .domain_checker import DomainCheckerService, get_domain_service, check_job_url_on_virustotal


@dataclass
class CompanyVerificationResult:
    """Consolidated result of MCA lookup and domain/URL security check."""
    company_name: Optional[str]
    cin: Optional[str]
    mca_verified: bool
    verification_outcome: str  # "Found and active", "Not found in snapshot", "Suspicious match"
    domain_risk: str          # "CLEAN", "SUSPICIOUS", "MALICIOUS", "UNKNOWN"
    domain_signals: List[str]
    virustotal_status: Optional[str]
    virustotal_risk_score: int
    is_suspicious: bool
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CompanyVerifier:
    """Unified Company & Domain Verifier.
    
    Verifies corporate claims against the MCA registry and scans domains/URLs with VirusTotal.
    """
    def __init__(self, db_path: Optional[Path] = None, vt_api_key: Optional[str] = None):
        self.mca_service = MCALookupService(db_path=db_path)
        self.domain_service = DomainCheckerService()
        self.vt_api_key = vt_api_key or os.environ.get("VIRUSTOTAL_API_KEY")

    def verify(
        self,
        company_name: Optional[str] = None,
        text: Optional[str] = None,
        url: Optional[str] = None,
    ) -> CompanyVerificationResult:
        full_text = f"{company_name or ''} {text or ''} {url or ''}".strip()
        mca_info = self.mca_service.verify_company_in_text(full_text)
        
        domain_signals, vt_result = self.domain_service.analyze_domain_signals(
            full_text,
            claimed_company=mca_info.name or company_name,
            vt_api_key=self.vt_api_key,
        )

        reasons = []
        is_suspicious = False

        if mca_info.verification_outcome == "Suspicious match":
            reasons.append("Claimed company has low fuzzy match or status irregularity in MCA registry.")
            is_suspicious = True
        elif mca_info.verification_outcome == "Not found in snapshot":
            reasons.append("Company not found in official active corporate registry snapshot.")

        for sig in domain_signals:
            if "FREE_MAIL_HR" in sig:
                reasons.append("HR recruiter is using free email (e.g. Gmail) instead of corporate domain.")
                is_suspicious = True
            elif "BRAND_IMPERSONATION" in sig:
                reasons.append(f"Domain appears to impersonate a legitimate corporate brand: {sig}")
                is_suspicious = True
            elif "SUSPICIOUS_TLD" in sig:
                reasons.append(f"URL uses high-risk disposable TLD: {sig}")
                is_suspicious = True

        vt_status = None
        vt_risk = 0
        if vt_result:
            vt_status = getattr(vt_result, "status", None)
            vt_risk = getattr(vt_result, "risk_score", 0)
            if vt_status in ("MALICIOUS", "SUSPICIOUS"):
                is_suspicious = True
                reasons.append(f"VirusTotal threat alert: {getattr(vt_result, 'reason', '')}")

        domain_risk = "MALICIOUS" if vt_status == "MALICIOUS" else ("SUSPICIOUS" if is_suspicious else "CLEAN")

        return CompanyVerificationResult(
            company_name=mca_info.name or company_name,
            cin=mca_info.cin,
            mca_verified=bool(mca_info.mca_match and mca_info.verification_outcome == "Found and active"),
            verification_outcome=mca_info.verification_outcome or "Unverified",
            domain_risk=domain_risk,
            domain_signals=domain_signals,
            virustotal_status=vt_status,
            virustotal_risk_score=vt_risk,
            is_suspicious=is_suspicious,
            reasons=reasons,
        )


def verify_company(
    company_name: Optional[str] = None,
    text: Optional[str] = None,
    url: Optional[str] = None,
    vt_api_key: Optional[str] = None,
) -> CompanyVerificationResult:
    """Convenience helper to verify company and domains in one line."""
    verifier = CompanyVerifier(vt_api_key=vt_api_key)
    return verifier.verify(company_name=company_name, text=text, url=url)
