# Module 2: Company Verification

> **Category:** Company verification  
> **Function:** Ministry of Corporate Affairs (MCA) registry lookups, brand typosquatting, and official domain security audits  
> **Priority:** Essential · Core Engine

A standalone verification engine for validating whether an employer or recruiter is an authentic corporate entity or a scam impersonator using:
1. **Ministry of Corporate Affairs (MCA) Registry Lookup:** Fuzzy-matches against active Indian corporate entities and verifies Corporate Identification Numbers (CIN).
2. **Domain & Brand Impersonation Audit:** Detects typosquatting, look-alike domains (e.g., `tcs-global-jobs.com`), and recruiters using free webmail (`@gmail.com`) for Fortune 500 roles.
3. **VirusTotal v3 URL Threat Intelligence:** Scans links using Base64 URL identifiers across 70+ antivirus engines, with automatic offline fallback when unconfigured.

---

## Table of Contents

- [Features](#features)
- [Verification Flow](#verification-flow)
- [File Structure](#file-structure)
- [Standalone Installation & Usage](#standalone-installation--usage)
  - [1. Copy Files](#1-copy-files)
  - [2. Verify Corporate Claims](#2-verify-corporate-claims)
  - [3. VirusTotal URL Intelligence](#3-virustotal-url-intelligence)
  - [4. Single-Line Convenience Function](#4-single-line-convenience-function)
- [API Reference](#api-reference)
  - [`CompanyVerifier`](#companyverifier)
  - [`CompanyVerificationResult`](#companyverificationresult)
- [Embedded Database Details](#embedded-database-details)
- [Environment Configuration](#environment-configuration)

---

## Features

- **MCA Master Registry**: Pre-indexed SQLite snapshot containing Corporate Identification Numbers (CIN), official company titles, ROC jurisdiction, and active business status.
- **RapidFuzz Token-Sort Matching**: Robust string distance matching resilient against deceptive spacing, abbreviations, and casing variations.
- **Webmail Impersonation Detection**: Automatically flags recruiters who contact applicants from free providers (`@gmail.com`, `@yahoo.com`, `@outlook.com`) while claiming affiliation with verified enterprises.
- **High-Risk TLD Sentinel**: Flags disposable or frequently abused top-level domains (`.top`, `.xyz`, `.club`, `.work`, `.vip`, `.cc`).
- **VirusTotal v3 Integration**: Automated SHA-256 / Base64 URL reputation queries against 70+ antivirus engines.

---

## Verification Flow

```
[ Input: Company Name / Job Text / URL ]
                    │
       ┌────────────┴────────────┐
       ▼                         ▼
[ MCA Registry Lookup ]   [ Domain & URL Audit ]
 - Fuzzy Token Sort Match  - Typosquatting Check
 - CIN Verification        - Free Webmail Audit
 - Active Status Check     - VirusTotal v3 Threat Scan
       │                         │
       └────────────┬────────────┘
                    ▼
      [ CompanyVerificationResult ]
```

---

## File Structure

```bash
company_verification/
├── __init__.py          # Module exports (CompanyVerifier, verify_company)
├── verifier.py          # Unified verification coordinator
├── mca_lookup.py        # SQLite MCA registry fuzzy matcher (RapidFuzz)
├── domain_checker.py    # Lookalike domains, free-mail & TLD auditor
├── data/
│   └── mca.sqlite       # Pre-indexed SQLite database of registered Indian companies
└── README.md            # Documentation
```

---

## Standalone Installation & Usage

### 1. Copy Files

Copy the `company_verification/` directory directly into your project:

```bash
cp -r backend/app/modules/company_verification /path/to/your/project/
```

### 2. Verify Corporate Claims

```python
from company_verification import CompanyVerifier

verifier = CompanyVerifier()

# Verify a job offer text
result = verifier.verify(text="Tata Consultancy Services hiring. Contact hr-tcs@gmail.com at tcs-careers.xyz")

print("Company Identified   :", result.company_name)          # "TATA CONSULTANCY SERVICES LIMITED"
print("CIN                  :", result.cin)                   # "L22210MH1995PLC084781"
print("MCA Verified         :", result.mca_verified)          # True
print("Verification Outcome :", result.verification_outcome)  # "Found and active"
print("Domain Risk          :", result.domain_risk)           # "SUSPICIOUS"
print("Is Suspicious        :", result.is_suspicious)         # True
print("Reasons              :", result.reasons)
# Output:
# [
#   "HR recruiter is using free email (e.g. Gmail) instead of corporate domain.",
#   "URL uses high-risk disposable TLD: .xyz"
# ]
```

### 3. VirusTotal URL Intelligence

Pass your VirusTotal API key (or set `VIRUSTOTAL_API_KEY` in environment):

```python
from company_verification import CompanyVerifier

verifier = CompanyVerifier(vt_api_key="your_virustotal_api_key")
result = verifier.verify(url="https://suspicious-prepaid-task.top")

print("VirusTotal Status:", result.virustotal_status)      # "MALICIOUS" | "CLEAN" | "UNKNOWN_DOMAIN"
print("VT Risk Score    :", result.virustotal_risk_score)  # 100
```

### 4. Single-Line Convenience Function

```python
from company_verification import verify_company

res = verify_company(company_name="Infosys", text="Apply at careers@infosys.com")
print(res.mca_verified)  # True
print(res.domain_risk)   # "CLEAN"
```

---

## API Reference

### `CompanyVerifier`

```python
CompanyVerifier(
    db_path: str | Path | None = None,
    vt_api_key: str | None = None
)
```

- `verify(company_name: str | None = None, text: str | None = None, url: str | None = None) -> CompanyVerificationResult`

### `CompanyVerificationResult`

| Attribute | Type | Description |
|---|---|---|
| `company_name` | `str \| None` | Matched official corporate title. |
| `cin` | `str \| None` | Corporate Identification Number (CIN). |
| `mca_verified` | `bool` | `True` if company was matched in the MCA database. |
| `verification_outcome` | `str` | `"Found and active"`, `"Not found"`, etc. |
| `domain_risk` | `str` | Risk rating: `"CLEAN"`, `"SUSPICIOUS"`, or `"MALICIOUS"`. |
| `is_suspicious` | `bool` | Overall verdict boolean on company/domain credibility. |
| `reasons` | `list[str]` | List of identified forensic anomalies or red flags. |
| `virustotal_status` | `str \| None` | VirusTotal threat status (`"MALICIOUS"`, `"CLEAN"`, etc.). |
| `virustotal_risk_score`| `int` | Threat score from `0` to `100`. |
| `to_dict()` | `method` | Returns serializable Python dictionary. |

---

## Embedded Database Details

The embedded database `data/mca.sqlite` contains:
- Official corporate name index with uppercase token normalization.
- 21-character Corporate Identification Numbers (CIN).
- Registered ROC state and office address.
- Active / Inactive / Struck-off company status.

---

## Environment Configuration

```bash
# VirusTotal v3 REST API Key
VIRUSTOTAL_API_KEY="your_api_key_here"
```
