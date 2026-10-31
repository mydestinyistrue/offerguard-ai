# Module 5: Victim Protection

> **Category:** Victim protection  
> **Function:** Explains risk, extracts suspect financial artifacts, and generates pre-formatted 1930 Cybercrime Helpline FIR complaint packs  
> **Priority:** Essential · Core Engine

Generates pre-formatted criminal complaint dossiers formatted specifically for India's **National Cyber Crime Reporting Portal** (`cybercrime.gov.in`) and the **1930 Cybercrime Helpline**, along with localized trilingual emergency guidance.

---

## Table of Contents

- [Features](#features)
- [FIR Dossier Architecture](#fir-dossier-architecture)
- [File Structure](#file-structure)
- [Standalone Installation & Usage](#standalone-installation--usage)
  - [1. Copy Files](#1-copy-files)
  - [2. Generate a 1930 Complaint Pack](#2-generate-a-1930-complaint-pack)
  - [3. Extract Suspect Financial Artifacts](#3-extract-suspect-financial-artifacts)
  - [4. Trilingual Safety Guidance (EN, HI, PA)](#4-trilingual-safety-guidance-en-hi-pa)
- [API Reference](#api-reference)
  - [`generate_complaint_pack()`](#generate_complaint_pack)
  - [`extract_incident_artifacts()`](#extract_incident_artifacts)
  - [`ComplaintPack`](#complaintpack)
- [Golden Hour Reporting Protocols](#golden-hour-reporting-protocols)

---

## Features

- **1930 Cybercrime Complaint Dossier**: Automatically structures evidence into a police FIR format accepted by cyber police stations and `cybercrime.gov.in`.
- **Financial Artifact Extraction**: Parses chat logs to isolate suspect UPI handles, destination bank account numbers, phone numbers, and exact loss figures.
- **Trilingual Guidance Engine**: Generates actionable, culturally tuned instructions in **English**, **Hindi (हिन्दी)**, and **Punjabi (ਪੰਜਾਬੀ)**.
- **Golden Hour Protocol**: Steps victims through triggering immediate bank lien freezes to stop secondary fund laundering.

---

## FIR Dossier Architecture

```
[ Conversation Evidence & Loss Amount ]
                    │
                    ▼
     [ Financial Artifact Extractor ]
   - Suspect UPI VPAs (e.g. scammer@bank)
   - Suspect Phone / Telegram Handles
   - Loss Chronology & Timestamps
                    │
                    ▼
       [ Report Pack Formatter ]
   - Formatted for cybercrime.gov.in
   - Structured evidence quotes
   - Chronological incident narrative
                    │
                    ▼
  [ Trilingual Victim Defense Pack ]
   (English / Hindi / Punjabi)
```

---

## File Structure

```bash
victim_protection/
├── __init__.py          # Module exports (generate_complaint_pack, extract_incident_artifacts, etc.)
├── report_generator.py  # Formats official 1930 Cybercrime police complaint
├── language.py          # Trilingual localized guidance dictionaries
└── README.md            # Documentation
```

---

## Standalone Installation & Usage

### 1. Copy Files

Copy the `victim_protection/` directory directly into your project root:

```bash
cp -r backend/app/modules/victim_protection /path/to/your/project/
```

### 2. Generate a 1930 Complaint Pack

```python
from victim_protection import generate_complaint_pack

messages = [
    {"sender": "+91 98765 43210", "text": "Pay ₹5,000 for VIP task to scammer@okhdfcbank", "timestamp": "10:15 AM"},
    {"sender": "Victim", "text": "I sent Rs 5,000. Where is my profit?", "timestamp": "10:20 AM"},
    {"sender": "+91 98765 43210", "text": "Your account is frozen. Pay ₹10,000 tax to unfreeze.", "timestamp": "10:25 AM"},
]

pack = generate_complaint_pack(
    messages=messages,
    victim_name="Rahul Sharma",
    victim_phone="9876543210",
    amount_lost=15000.0,
    language="en",
)

print("Suggested Helpline :", pack.suggested_helpline)  # "1930"
print("Summary            :", pack.summary)
print("\n--- COMPLAINT PACK REPORT ---\n")
print(pack.report_text)
```

### 3. Extract Suspect Financial Artifacts

```python
from victim_protection import extract_incident_artifacts

raw_chat = "Send Rs 12,000 to merchant99@paytm or call +91 91234 56789 on Telegram @fast_hr"
artifacts = extract_incident_artifacts(raw_chat)

print("Suspect UPIs  :", artifacts["upi_ids"])       # ['merchant99@paytm']
print("Suspect Phones:", artifacts["phone_numbers"])  # ['+91 91234 56789']
print("Amounts Found :", artifacts["amounts"])        # [12000.0]
```

### 4. Trilingual Safety Guidance (EN, HI, PA)

```python
from victim_protection import get_localized_advice

advice_hi = get_localized_advice(language="hi", stage=3)
print("Hindi Advice:")
for step in advice_hi["action_steps"]:
    print(" -", step)
```

---

## API Reference

### `generate_complaint_pack(...)`

```python
generate_complaint_pack(
    messages: list[dict],
    victim_name: str | None = None,
    victim_phone: str | None = None,
    amount_lost: float | None = None,
    language: str = "en"
) -> ComplaintPack
```

### `ComplaintPack`

| Attribute | Type | Description |
|---|---|---|
| `report_text` | `str` | Full formatted police complaint draft ready for `cybercrime.gov.in`. |
| `suggested_helpline` | `str` | `"1930"` (India National Cybercrime Helpline). |
| `summary` | `str` | One-paragraph executive incident abstract. |
| `artifacts` | `dict` | Extracted suspect UPIs, phone numbers, and financial loss metrics. |
| `action_steps` | `list[str]` | Actionable immediate defense steps for the complainant. |
| `language` | `str` | Language code used (`"en"`, `"hi"`, or `"pa"`). |
| `to_dict()` | `method` | Returns serializable Python dictionary. |

---

## Golden Hour Reporting Protocols

1. **Immediate Freeze**: Call **1930** immediately (within 2–4 hours). The Indian Cyber Crime Coordination Centre (I4C) coordinates directly with banks to put a hold on recipient mule accounts.
2. **Preserve Digital Evidence**: Take full screenshots showing timestamps, transaction UTR numbers, UPI IDs, and WhatsApp/Telegram phone numbers.
3. **Formal Complaint**: Lodge the pre-formatted report pack generated by OfferGuard at `https://cybercrime.gov.in` to obtain an official National Cybercrime Acknowledgement Number.
