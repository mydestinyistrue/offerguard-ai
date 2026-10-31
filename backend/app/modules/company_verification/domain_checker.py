"""Domain & Email Verification Service with VirusTotal v3 Threat Intelligence.

Detects:
- VirusTotal v3 Security Vendor Analysis for job URLs and links (with fallback)
- Free-mail services used for corporate/HR recruitment
- Brand impersonation / look-alike domains (e.g. tcs-careers-global.com)
- Suspicious TLDs commonly used in task scams (.xyz, .top, .vip, .live, .cc)
"""

from __future__ import annotations

import base64
import logging
import os
import re
from pathlib import Path
from typing import Optional, Tuple
import requests

try:
    from app.core.config import get_settings
    _HAVE_SETTINGS = True
except ImportError:
    _HAVE_SETTINGS = False

try:
    from app.models.schemas import VirusTotalDetails
except ImportError:
    from dataclasses import dataclass
    @dataclass
    class VirusTotalDetails:  # type: ignore[no-redef]
        status: str
        risk_score: int = 0
        reason: str = ""
        target_url: Optional[str] = None
        malicious: int = 0
        suspicious: int = 0
        harmless: int = 0

logger = logging.getLogger(__name__)

_EMAIL_REGEX = re.compile(r"\b([a-zA-Z0-9_.+\-]+@([a-zA-Z0-9\-]+\.[a-zA-Z]{2,}))\b", re.IGNORECASE)
_URL_REGEX = re.compile(r"\b(?:https?:\/\/|www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.\/]+)\b", re.IGNORECASE)

_COMMON_FREEMAIL = {
    "gmail.com", "yahoo.com", "yahoo.co.in", "hotmail.com", "outlook.com",
    "rediffmail.com", "protonmail.com", "aol.com", "icloud.com", "mail.com",
    "zoho.com", "yandex.com", "live.com"
}

_SUSPICIOUS_TLDS = {".xyz", ".top", ".vip", ".live", ".cc", ".work", ".click", ".link", ".buzz", ".club", ".icu", ".shop"}

# Real corporate domains for major brands
_BRAND_OFFICIAL_DOMAINS = {
    "tcs": ["tcs.com"],
    "tata": ["tcs.com", "tatamotors.com", "tatasteel.com", "tata.com"],
    "infosys": ["infosys.com"],
    "wipro": ["wipro.com"],
    "hcl": ["hcl.com", "hcltech.com"],
    "tech mahindra": ["techmahindra.com"],
    "google": ["google.com", "google.co.in"],
    "microsoft": ["microsoft.com"],
    "amazon": ["amazon.com", "amazon.in", "amazon.jobs"],
    "flipkart": ["flipkart.com", "flipkartcareers.com"],
    "meesho": ["meesho.com"],
    "swiggy": ["swiggy.in", "swiggy.com"],
    "zomato": ["zomato.com"],
    "reliance": ["ril.com", "jio.com"],
    "jio": ["jio.com"],
    "sbi": ["sbi.co.in", "bank.sbi"],
    "hdfc": ["hdfcbank.com"],
    "icici": ["icicibank.com"],
    "deloitte": ["deloitte.com"],
}


def check_job_url_on_virustotal(target_url: str, vt_api_key: str) -> VirusTotalDetails:
    """
    Evaluates a job link against VirusTotal v3 API.
    Returns status, risk score, vendor counts, and reason.
    """
    norm_url = target_url.strip()
    if not norm_url.startswith(("http://", "https://")):
        norm_url = "https://" + norm_url

    # VirusTotal v3 API requires base64-encoded URL identifier (without trailing '=')
    url_id = base64.urlsafe_b64encode(norm_url.encode()).decode().strip("=")
    endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {"x-apikey": vt_api_key}

    try:
        response = requests.get(endpoint, headers=headers, timeout=4.5)

        if response.status_code == 200:
            data = response.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = data.get("malicious", 0)
            suspicious = data.get("suspicious", 0)
            harmless = data.get("harmless", 0)

            if malicious > 0:
                return VirusTotalDetails(
                    status="MALICIOUS",
                    risk_score=100,
                    reason=f"CRITICAL: Flagged as dangerous by {malicious} security vendors on VirusTotal!",
                    target_url=norm_url,
                    malicious=malicious,
                    suspicious=suspicious,
                    harmless=harmless,
                )
            elif suspicious > 0:
                return VirusTotalDetails(
                    status="SUSPICIOUS",
                    risk_score=60,
                    reason=f"WARNING: Flagged as suspicious by {suspicious} security vendors on VirusTotal.",
                    target_url=norm_url,
                    malicious=malicious,
                    suspicious=suspicious,
                    harmless=harmless,
                )
            else:
                return VirusTotalDetails(
                    status="CLEAN",
                    risk_score=0,
                    reason=f"Clean ({harmless} vendors reported no threats).",
                    target_url=norm_url,
                    malicious=malicious,
                    suspicious=suspicious,
                    harmless=harmless,
                )

        elif response.status_code == 404:
            # 404 means the domain is brand new / never scanned before (High Risk for job scams)
            return VirusTotalDetails(
                status="UNKNOWN_DOMAIN",
                risk_score=85,
                reason="URL not found in VirusTotal database. Brand new or unindexed domain — HIGH RISK for job scams!",
                target_url=norm_url,
            )

        elif response.status_code == 429:
            return VirusTotalDetails(
                status="RATE_LIMITED",
                risk_score=50,
                reason="VirusTotal API rate limit reached (max 4 req/min). Falling back to heuristic checks.",
                target_url=norm_url,
            )

        else:
            return VirusTotalDetails(
                status="ERROR",
                risk_score=0,
                reason=f"VirusTotal API Status code {response.status_code}. Falling back to heuristic checks.",
                target_url=norm_url,
            )

    except Exception as e:
        logger.warning(f"VirusTotal request error: {e}")
        return VirusTotalDetails(
            status="ERROR",
            risk_score=0,
            reason=f"VirusTotal connection timed out. Falling back to heuristic checks.",
            target_url=norm_url,
        )


class DomainCheckerService:
    def __init__(self, freemail_path: Optional[Path] = None):
        settings = get_settings() if _HAVE_SETTINGS else None
        default_path = (settings.DATA_DIR / "freemail_domains.txt") if settings and hasattr(settings, "DATA_DIR") else Path("data/freemail_domains.txt")
        self.freemail_path = freemail_path or default_path
        self.freemail_domains = set(_COMMON_FREEMAIL)
        self._load_freemail_file()

    def _load_freemail_file(self):
        if self.freemail_path and self.freemail_path.exists():
            try:
                with open(self.freemail_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip().lower()
                        if line and not line.startswith("#"):
                            self.freemail_domains.add(line)
            except Exception:
                pass

    def extract_emails(self, text: str) -> list[tuple[str, str]]:
        """Return list of (full_email, domain)."""
        results = []
        for match in _EMAIL_REGEX.finditer(text):
            full_email = match.group(1).lower()
            domain = match.group(2).lower()
            results.append((full_email, domain))
        return results

    def extract_domains(self, text: str) -> list[str]:
        """Extract web domains mentioned in text."""
        domains = []
        for match in _URL_REGEX.finditer(text):
            raw = match.group(1).lower().split("/")[0]
            if "." in raw and not raw.endswith("."):
                domains.append(raw)
        return list(set(domains))

    def extract_urls(self, text: str) -> list[str]:
        """Extract full URLs or domains suitable for scanning."""
        urls = []
        for match in _URL_REGEX.finditer(text):
            val = match.group(0).strip()
            if "." in val and not val.endswith("@"):
                urls.append(val)
        return urls

    def analyze_domain_signals(
        self, 
        text: str, 
        claimed_company: Optional[str] = None,
        vt_api_key: Optional[str] = None,
    ) -> Tuple[list[str], Optional[VirusTotalDetails]]:
        """
        Analyze text for domain and email signals.
        Evaluates URLs against VirusTotal if API key is provided, falling back to heuristic checks.
        """
        signals = []
        emails = self.extract_emails(text)
        domains = self.extract_domains(text)
        urls = self.extract_urls(text)
        vt_result: Optional[VirusTotalDetails] = None

        # ── 1. VirusTotal URL Security Scan (if API key and URLs are available) ──
        if vt_api_key and urls:
            primary_url = urls[0]
            vt_result = check_job_url_on_virustotal(primary_url, vt_api_key)
            if vt_result.status == "MALICIOUS":
                signals.append(f"VIRUSTOTAL_MALICIOUS: [VirusTotal] {vt_result.reason} (Target: {vt_result.target_url})")
            elif vt_result.status == "SUSPICIOUS":
                signals.append(f"VIRUSTOTAL_SUSPICIOUS: [VirusTotal] {vt_result.reason} (Target: {vt_result.target_url})")
            elif vt_result.status == "UNKNOWN_DOMAIN":
                signals.append(f"VIRUSTOTAL_UNKNOWN: [VirusTotal] {vt_result.reason}")
            elif vt_result.status == "CLEAN":
                signals.append(f"VIRUSTOTAL_CLEAN: [VirusTotal] {vt_result.reason}")

        # ── 2. Heuristic Check: Free-mail HR addresses ───────────────────────
        has_corp_email = any(d not in self.freemail_domains for _, d in emails)
        for email, domain in emails:
            if domain in self.freemail_domains:
                if any(hr_word in email for hr_word in ["hr", "career", "recruit", "job", "hiring", "apply", "talent"]):
                    signals.append(f"FREE_MAIL_HR: Official recruitment contact is using free email provider '{domain}' ({email}). Legit enterprises use corporate domains.")
                elif claimed_company and not has_corp_email:
                    signals.append(f"FREE_MAIL_HR: Free email '{email}' used while claiming to represent '{claimed_company}'.")

        # ── 3. Heuristic Check: Brand impersonation in domain ─────────────────
        text_lower = text.lower()
        for brand, official_domains in _BRAND_OFFICIAL_DOMAINS.items():
            if brand in text_lower:
                for domain in domains:
                    if brand in domain and not any(domain == off or domain.endswith("." + off) for off in official_domains):
                        signals.append(f"BRAND_IMPERSONATION: Domain '{domain}' contains brand '{brand}', but official domains are: {', '.join(official_domains)}.")

        # ── 4. Heuristic Check: Suspicious disposable scam TLDs ──────────────
        for domain in domains:
            for tld in _SUSPICIOUS_TLDS:
                if domain.endswith(tld):
                    signals.append(f"SUSPICIOUS_DOMAIN_TLD: Domain '{domain}' uses high-risk extension '{tld}' frequently associated with disposable scam landing pages.")

        # ── 5. Heuristic Check: Official corporate domain match (Green Flag) ──
        if claimed_company:
            comp_lower = claimed_company.lower()
            for brand, official_domains in _BRAND_OFFICIAL_DOMAINS.items():
                if brand in comp_lower:
                    for domain in domains:
                        if any(domain == off or domain.endswith("." + off) for off in official_domains):
                            signals.append(f"GENUINE_DOMAIN_MATCH: Domain '{domain}' matches the verified corporate domain of {brand.upper()}.")

        return signals, vt_result


_domain_service: Optional[DomainCheckerService] = None

def get_domain_service() -> DomainCheckerService:
    global _domain_service
    if _domain_service is None:
        _domain_service = DomainCheckerService()
    return _domain_service
