"""Module 2: Company Verification.
Function: MCA registry and official domain checks.

Validates legal entity registration, corporate domains, and VirusTotal v3 URL intelligence.
Can be used standalone in any Python application.
"""

from .verifier import CompanyVerifier, CompanyVerificationResult, verify_company
from .mca_lookup import get_mca_service, MCALookupService, extract_cin_from_text, normalize_company_name
from .domain_checker import (
    get_domain_service,
    DomainCheckerService,
    check_job_url_on_virustotal,
)

__all__ = [
    "CompanyVerifier",
    "CompanyVerificationResult",
    "verify_company",
    "get_mca_service",
    "MCALookupService",
    "extract_cin_from_text",
    "normalize_company_name",
    "get_domain_service",
    "DomainCheckerService",
    "check_job_url_on_virustotal",
]
