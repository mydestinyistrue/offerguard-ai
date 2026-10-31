# Module 3: Conversation Intelligence

> **Category:** Conversation intelligence  
> **Function:** Understands multi-turn WhatsApp/Telegram conversations, parses PDF offer letters, and redacts Indian Personally Identifiable Information (PII)  
> **Priority:** Essential · Core Engine

Provides multi-turn dialogue extraction, Indian personal data scrubbing, and multi-format document text extraction with zero external server dependencies.

---

## Table of Contents

- [Features](#features)
- [Pipeline Architecture](#pipeline-architecture)
- [File Structure](#file-structure)
- [Standalone Installation & Usage](#standalone-installation--usage)
  - [1. Copy Files](#1-copy-files)
  - [2. Multi-Turn Chat Parsing](#2-multi-turn-chat-parsing)
  - [3. Indian PII Redaction](#3-indian-pii-redaction)
  - [4. PDF Offer Letter Extraction](#4-pdf-offer-letter-extraction)
  - [5. Full Integrated Pipeline](#5-full-integrated-pipeline)
- [API Reference](#api-reference)
  - [`ConversationIntelligence`](#conversationintelligence)
  - [`mask_pii()`](#mask_pii)
  - [`parse_chat_log()`](#parse_chat_log)
  - [`extract_text_from_pdf()`](#extract_text_from_pdf)
- [PII Redaction Specifications](#pii-redaction-specifications)

---

## Features

- **Multi-Turn Chat Parsing**: Parses export logs from WhatsApp (Android & iOS standard 12h/24h timestamps) and Telegram channels into structured message turns (`sender`, `timestamp`, `text`).
- **Sender Attribution**: Classifies participants into `Recruiter`, `Victim`, or `System` to map chronological psychological coercion.
- **Indian PII Redaction**: Scrubs sensitive personal identification data:
  - 10-digit Indian Mobile Numbers (`+91`, `0`, or bare `9/8/7/6` prefixes)
  - UPI Virtual Payment Addresses (VPAs, e.g., `user@okaxis`, `user@paytm`)
  - 12-digit Aadhaar Numbers (with space/hyphen separators)
  - Permanent Account Numbers (PAN: `[A-Z]{5}[0-9]{4}[A-Z]`)
  - Bank Account Numbers (9–18 digits) and Email addresses
- **High-Throughput PDF Extraction**: PyMuPDF (`fitz`) engine extracting structured text from appointment letters and PDF contracts in milliseconds.

---

## Pipeline Architecture

```
[ Raw Chat Transcript / PDF Offer Letter ]
                    │
                    ▼
          [ Document Parser ]
         (Extract text from PDF)
                    │
                    ▼
            [ Chat Parser ]
   (Decompose into structured turns)
                    │
                    ▼
             [ PII Masker ]
   (Redact Aadhaar, UPI, Phone, PAN)
                    │
                    ▼
       [ Cleaned Forensic Text ]
```

---

## File Structure

```bash
conversation_intelligence/
├── __init__.py          # Module exports (ConversationIntelligence, mask_pii, parse_chat_log, etc.)
├── pipeline.py          # Unified multi-turn chat & PII pipeline coordinator
├── chat_parser.py       # WhatsApp & Telegram regex timestamp parser
├── pii_masker.py        # Indian PII redactor (regex + checksums)
├── document_parser.py   # PDF text extractor via PyMuPDF (fitz)
└── README.md            # Documentation
```

---

## Standalone Installation & Usage

### 1. Copy Files

Copy the `conversation_intelligence/` directory directly into your project root:

```bash
cp -r backend/app/modules/conversation_intelligence /path/to/your/project/
```

### 2. Multi-Turn Chat Parsing

```python
from conversation_intelligence import ConversationIntelligence

ci = ConversationIntelligence()

chat_log = """
[30/10/2026, 10:15:00 AM] +91 98765 43210: Hello dear! Are you looking for part-time work?
[30/10/2026, 10:16:00 AM] Candidate: Yes, what is the work?
[30/10/2026, 10:17:00 AM] +91 98765 43210: Earn Rs 3,000 daily. Just like YouTube videos.
"""

messages = ci.parse_chat(chat_log)
print(f"Total turns: {len(messages)}")
for m in messages:
    print(f"[{m.timestamp}] {m.sender}: {m.text}")
```

### 3. Indian PII Redaction

```python
from conversation_intelligence import mask_pii

raw = "My phone is 9876543210. Pay Rs 2000 to fraud-agent@okhdfcbank or send Aadhaar 5432 1098 7654."
result = mask_pii(raw)

print("Masked Text:", result.masked_text)
# Output:
# "My phone is [PHONE_REDACTED]. Pay Rs 2000 to [UPI_REDACTED] or send Aadhaar [AADHAAR_REDACTED]."

print("Entities Found:", result.entities_found)
```

### 4. PDF Offer Letter Extraction

```python
from conversation_intelligence import extract_text_from_pdf

with open("offer_letter.pdf", "rb") as f:
    pdf_bytes = f.read()

text = extract_text_from_pdf(pdf_bytes)
print("Extracted Length:", len(text))
```

### 5. Full Integrated Pipeline

```python
from conversation_intelligence import ConversationIntelligence

ci = ConversationIntelligence()
pipeline_res = ci.process(chat_log)

print("Cleaned Text for AI :", pipeline_res.cleaned_text)
print("Detected Participants:", pipeline_res.participants)
print("Turn Count          :", pipeline_res.turn_count)
```

---

## API Reference

### `ConversationIntelligence`

- `parse_chat(text: str) -> list[ChatMessage]`
- `mask_pii(text: str) -> MaskedResult`
- `extract_pdf(pdf_bytes: bytes) -> str`
- `process(raw_input: str) -> ProcessedConversation`

### `mask_pii(text: str)`

Returns a `MaskedResult` with:
- `masked_text` (`str`): Sanitized string with PII replaced by placeholders (`[PHONE_REDACTED]`, `[UPI_REDACTED]`, `[AADHAAR_REDACTED]`, `[PAN_REDACTED]`).
- `entities_found` (`list[dict]`): List of redacted entity types and locations.

---

## PII Redaction Specifications

| Entity | Pattern / Standard | Replacement Token |
|---|---|---|
| **Indian Phone** | `(\+91[\-\s]?)?[6-9]\d{9}` | `[PHONE_REDACTED]` |
| **UPI ID / VPA** | `[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}` | `[UPI_REDACTED]` |
| **Aadhaar Number** | `\b[2-9]{1}[0-9]{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b` | `[AADHAAR_REDACTED]` |
| **PAN Card** | `\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b` | `[PAN_REDACTED]` |
| **Email Address** | `[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+` | `[EMAIL_REDACTED]` |
