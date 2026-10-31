# OfferGuard AI — Modular Architecture & Standalone Engines

This directory contains the **5 core, decoupled standalone engines** powering OfferGuard AI. Each module is intentionally engineered with **zero framework lock-in**, meaning any folder in this directory can be copied and embedded directly into external codebases (FastAPI, Flask, Django, AWS Lambda, Celery workers, or Telegram chatbots) without requiring the parent OfferGuard application.

---

## Table of Contents

- [The 5 MVP Modules](#the-5-mvp-modules)
- [Design Principles & Portability](#design-principles--portability)
- [Architecture & Data Flow](#architecture--data-flow)
- [Directory Structure](#directory-structure)
- [How to Embed a Module in Another Project](#how-to-embed-a-module-in-another-project)
  - [Example 1: Job & Task Scam Classifier](#example-1-job--task-scam-classifier)
  - [Example 2: Ministry of Corporate Affairs Verification](#example-2-ministry-of-corporate-affairs-verification)
  - [Example 3: Conversation Intelligence & Indian PII Redaction](#example-3-conversation-intelligence--indian-pii-redaction)
  - [Example 4: 5-Stage Scam Progression Radar](#example-4-5-stage-scam-progression-radar)
  - [Example 5: Victim Protection & 1930 FIR Generator](#example-5-victim-protection--1930-fir-generator)
- [Configuration & Environment Variables](#configuration--environment-variables)

---

## The 5 MVP Modules

| Directory | Official Module Name | Primary Forensic Function | Entry Point |
|---|---|---|---|
| [`job_task_classifier/`](./job_task_classifier/README.md) | **1. Job/Task Scam Classifier** | Analyzes posts, chats, and offer letters for financial scam patterns and high-yield baits. | `JobTaskClassifier` |
| [`company_verification/`](./company_verification/README.md) | **2. Company Verification** | Verifies MCA corporate registry claims, brand typosquatting, and scans URLs via VirusTotal v3. | `CompanyVerifier` |
| [`conversation_intelligence/`](./conversation_intelligence/README.md) | **3. Conversation Intelligence** | Understands multi-turn WhatsApp/Telegram dialogues, extracts PDFs, and redacts Indian PII. | `ConversationIntelligence` |
| [`scam_stage_identification/`](./scam_stage_identification/README.md) | **4. Scam-Stage Identification** | Tracks the 5-stage social engineering kill-chain (Stage 0 to 4) and predicts the scammer's next move. | `StageClassifier` |
| [`victim_protection/`](./victim_protection/README.md) | **5. Victim Protection** | Generates official 1930 Cybercrime complaint drafts and localized safety guidance (EN, HI, PA). | `generate_complaint_pack()` |

---

## Design Principles & Portability

1. **Zero Framework Lock-in**:
   - Each module utilizes native Python primitives, standard library data structures (`@dataclass`), and optional Pydantic bindings.
   - No hardcoded dependency on FastAPI, databases, or specific web frameworks.
2. **Graceful Degradation**:
   - Every module functions **100% offline** using deterministic heuristics and embedded datasets.
   - When external API keys (`GROQ_API_KEY`, `VIRUSTOTAL_API_KEY`) are present in the environment or passed via constructor, modules automatically upgrade their capabilities.
3. **Defense-in-Depth**:
   - All text inputs are treated as untrusted and screened for prompt injection attempts before LLM processing.
   - Personally Identifiable Information (PII) is masked locally before any external API calls.

---

## Architecture & Data Flow

```
Raw Input (Transcript / Offer Letter / Screenshot OCR)
                        │
                        ▼
       [ Module 3: Conversation Intelligence ]
        ├── Parse multi-turn chat turns (WhatsApp / Telegram)
        ├── PyMuPDF PDF extraction
        └── Redact Indian PII (Aadhaar, UPI, Phone, PAN)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 [ Module 1: Job/Task Classifier ] [ Module 2: Company Verification ]
  ├── 18+ Forensic Signals          ├── MCA ROC SQLite Search
  └── Groq 120B / Gemini Reasoner   └── VirusTotal v3 URL Scanner
         │                             │
         └──────────────┬──────────────┘
                        ▼
       [ Module 4: Scam-Stage Radar ]
        ├── Monotonic State Machine (Stages 0 - 4)
        └── Predictive Psychology Forecaster
                        │
                        ▼
       [ Module 5: Victim Protection ]
        ├── Pre-formatted 1930 Cybercrime FIR Pack
        └── Trilingual Emergency Advice (EN, HI, PA)
```

---

## Directory Structure

```bash
modules/
├── README.md                            # This architecture guide
├── job_task_classifier/                 # Module 1
│   ├── __init__.py
│   ├── classifier.py                    # Master hybrid classifier
│   ├── rules_engine.py                  # Standalone regex heuristic engine
│   ├── llm_service.py                   # Groq Cloud 120B client
│   └── README.md
├── company_verification/                # Module 2
│   ├── __init__.py
│   ├── verifier.py                      # Master verification manager
│   ├── mca_lookup.py                    # Local SQLite MCA lookup
│   ├── domain_checker.py                # Typosquatting & TLD auditor
│   ├── data/mca.sqlite                  # Pre-indexed MCA company snapshot
│   └── README.md
├── conversation_intelligence/           # Module 3
│   ├── __init__.py
│   ├── pipeline.py                      # Multi-turn chat & PII pipeline
│   ├── chat_parser.py                   # WhatsApp & Telegram timestamp parser
│   ├── pii_masker.py                    # Regex & checksum Indian PII scrubber
│   ├── document_parser.py               # PDF offer letter extractor (fitz)
│   └── README.md
├── scam_stage_identification/           # Module 4
│   ├── __init__.py
│   ├── stage_classifier.py             # High-level stage classifier
│   ├── stage_engine.py                  # 5-stage monotonic state machine
│   └── README.md
└── victim_protection/                   # Module 5
    ├── __init__.py
    ├── report_generator.py             # 1930 Cybercrime complaint pack builder
    ├── language.py                      # Trilingual localized guidance
    └── README.md
```

---

## How to Embed a Module in Another Project

### Example 1: Job & Task Scam Classifier

```python
from job_task_classifier import JobTaskClassifier

# 100% offline regex heuristics, or uses Groq 120B if GROQ_API_KEY is set
classifier = JobTaskClassifier()
result = classifier.classify("Earn Rs 5,000 daily liking YouTube videos. Add Telegram @Priya")

print("Verdict   :", result.verdict)       # "SCAM"
print("Risk Score:", result.risk_score)    # 72 (0 to 100)
print("Is Scam   :", result.is_scam)        # True
```

### Example 2: Ministry of Corporate Affairs Verification

```python
from company_verification import CompanyVerifier

verifier = CompanyVerifier()
result = verifier.verify(company_name="Tata Consultancy Services", text="Contact hr-tcs@gmail.com")

print("MCA Matched:", result.mca_verified)       # True
print("CIN        :", result.cin)                # "L22210MH1995PLC084781"
print("Domain Risk:", result.domain_risk)        # "SUSPICIOUS" (Free email impersonation)
```

### Example 3: Conversation Intelligence & Indian PII Redaction

```python
from conversation_intelligence import mask_pii

raw_chat = "Pay Rs 3,000 to fraud@okhdfcbank or call 9876543210. Aadhaar: 5432 1098 7654"
cleaned = mask_pii(raw_chat)

print(cleaned.masked_text)
# "Pay Rs 3,000 to [UPI_REDACTED] or call [PHONE_REDACTED]. Aadhaar: [AADHAAR_REDACTED]"
```

### Example 4: 5-Stage Scam Progression Radar

```python
from scam_stage_identification import StageClassifier

radar = StageClassifier()
result = radar.classify("Your withdrawal is frozen. Deposit Rs 5,000 tax to release your funds.")

print("Stage    :", result.detected_stage)      # 3
print("Name     :", result.stage_name)          # "Stage 3: Lock-in"
print("Next Move:", result.next_scammer_move)   # Forecaster warning
```

### Example 5: Victim Protection & 1930 FIR Generator

```python
from victim_protection import generate_complaint_pack

pack = generate_complaint_pack(
    messages=[{"sender": "Scammer", "text": "Pay 5000 to fraud@paytm", "timestamp": "10:00 AM"}],
    victim_name="Rahul Sharma",
    victim_phone="9876543210",
    amount_lost=5000.0,
    language="en",
)

print(pack.report_text)  # Pre-formatted 1930 FIR dossier
```

---

## Configuration & Environment Variables

| Variable | Type | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | `str` | `""` | Groq Cloud API Key for ultra-fast 120B model reasoning. |
| `GROQ_MODEL` | `str` | `"openai/gpt-oss-120b"` | Target Groq model identifier. |
| `GEMINI_API_KEY` | `str` | `""` | Google Gemini API Key for fallback multimodal inference. |
| `VIRUSTOTAL_API_KEY` | `str` | `""` | VirusTotal v3 REST API key for URL reputation lookups. |
| `RULES_WEIGHT` | `float` | `0.60` | Weight assigned to deterministic rule engine scores (0.0 to 1.0). |
| `LLM_WEIGHT` | `float` | `0.40` | Weight assigned to LLM model evaluation scores (0.0 to 1.0). |
