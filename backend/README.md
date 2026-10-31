# OfferGuard AI — Backend Server & Forensic Engine

The backend for **OfferGuard AI** is a high-performance Python application built with **FastAPI**, **Pydantic v2**, and **Uvicorn**. It orchestrates a dual-engine scoring architecture blending deterministic regex heuristics with Large Language Model inference (Groq Cloud 120B / Google Gemini 2.0 Flash).

The server verifies employer legitimacy against a local Ministry of Corporate Affairs (MCA) database snapshot, scans suspicious links using VirusTotal v3, tracks a 5-stage monotonic scam progression radar, and generates pre-formatted legal complaint packages for India's 1930 Cybercrime Helpline.

---

## Table of Contents

- [Features & Capabilities](#features--capabilities)
- [Server Architecture](#server-architecture)
- [Project Structure](#project-structure)
- [The 5 Core Modules](#the-5-core-modules)
- [API Endpoints Reference](#api-endpoints-reference)
  - [1. Analyze Conversation / Job Offer (`POST /api/analyze`)](#1-analyze-conversation--job-offer-post-apianalyze)
  - [2. Generate 1930 Helpline Complaint Pack (`POST /api/report`)](#2-generate-1930-helpline-complaint-pack-post-apireport)
  - [3. Run Benchmark Evaluation Suite (`GET /api/eval`)](#3-run-benchmark-evaluation-suite-get-apieval)
- [Environment Setup](#environment-setup)
- [Installation & Running Locally](#installation--running-locally)
  - [Prerequisites](#prerequisites)
  - [Virtual Environment Setup](#virtual-environment-setup)
  - [Running the Server](#running-the-server)
- [Benchmarking & Offline Testing](#benchmarking--offline-testing)

---

## Features & Capabilities

- **Dual-Engine Scoring**: 60% deterministic rule heuristics + 40% LLM reasoning (Groq 120B / Gemini Flash) with safety latch override for high-confidence threats.
- **5-Stage Monotonic Radar**: Tracks social engineering progression from Stage 0 (Bait) to Stage 4 (Exit Scam) without backward regression.
- **Corporate Registry Verification**: Instant fuzzy matching of corporate names and CIN numbers against a local SQLite MCA snapshot using RapidFuzz.
- **Threat Intelligence**: Scans embedded URLs via VirusTotal API v3; identifies look-alike domains and disposable TLDs.
- **Indian PII Redactor**: Scrubs Aadhaar numbers, PAN cards, UPI handles, and Indian phone numbers prior to LLM submission.
- **Helpline 1930 FIR Generator**: Builds tamper-evident, chronologically ordered complaint dossiers for cybercrime authorities.

---

## Server Architecture

```
[ Incoming Request (Chat / Offer / Screenshot Text) ]
                        │
                        ▼
            [ Conversation Intelligence ]
        ├── Parse WhatsApp / Telegram turns
        └── Redact Indian PII (Aadhaar, UPI, Phone)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 [ Rules Engine (60%) ]       [ LLM Service (40%) ]
  - 18+ Forensic Signals       - Groq 120B / Gemini Flash
  - Salary Negation Filter     - Structured JSON Reasoning
         │                             │
         └──────────────┬──────────────┘
                        ▼
               [ Risk Blender ]
          (Safety Latch: Rules >= 70)
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
[ Company Verifier ]  [ Stage Radar ]  [ Victim Protection ]
 - MCA ROC SQLite     - Stages 0 to 4  - 1930 FIR Generator
 - VirusTotal v3      - Predictive Move- Trilingual Advice
                        │
                        ▼
     [ JSON Forensic Response / API Client ]
```

---

## Project Structure

```bash
backend/
├── app/
│   ├── main.py                  # FastAPI application entry, CORS & routes
│   ├── __init__.py
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   └── config.py            # Pydantic BaseSettings loading from .env
│   ├── models/                  # Pydantic schemas & DTOs
│   │   ├── __init__.py
│   │   └── schemas.py           # Request / Response schemas & validation
│   ├── routers/                 # Route controllers & API endpoints
│   │   ├── __init__.py
│   │   ├── analyze.py           # POST /api/analyze endpoint
│   │   ├── eval_router.py       # GET /api/eval benchmark test runner
│   │   └── report.py            # POST /api/report FIR dossier generator
│   ├── services/                # Business logic & orchestrators
│   │   ├── __init__.py
│   │   ├── analyzer.py          # Master forensic analysis coordinator
│   │   ├── chat_parser.py       # Multi-turn WhatsApp/Telegram parser
│   │   ├── document_parser.py   # PDF text extraction via PyMuPDF (fitz)
│   │   ├── domain_checker.py    # Typosquatting & disposable TLD auditor
│   │   ├── language.py          # Trilingual translation engine
│   │   ├── llm_service.py       # Groq 120B / Gemini Flash client
│   │   ├── mca_lookup.py        # SQLite MCA registry fuzzy matcher
│   │   ├── pii_masker.py        # Indian PII redaction engine
│   │   ├── report_generator.py  # 1930 Cybercrime complaint pack builder
│   │   ├── rules_engine.py      # Deterministic 18-signal rule engine
│   │   ├── stage_classifier.py  # Standalone stage classifier wrapper
│   │   └── stage_engine.py      # Monotonic 5-stage progression state machine
│   └── modules/                 # 5 Decoupled standalone modules (Zero-lock-in)
│       ├── README.md            # Modular architecture guide
│       ├── job_task_classifier/         # Module 1: Job / Task Scam Classifier
│       ├── company_verification/        # Module 2: Company & Domain Verification
│       ├── conversation_intelligence/   # Module 3: Conversation Intelligence
│       ├── scam_stage_identification/   # Module 4: Scam-Stage Radar
│       └── victim_protection/           # Module 5: Victim Protection & 1930 FIR
├── .env                         # Server environment variables
├── .env.example                 # Configuration template
└── requirements.txt             # Production Python dependencies
```

---

## The 5 Core Modules

The `backend/app/modules/` directory contains 5 self-contained, standalone Python packages with zero framework lock-in. Any module can be extracted and embedded into other codebases:

1. **`job_task_classifier`**: Hybrid scam and fraudulent job detection engine.
2. **`company_verification`**: MCA ROC registry lookups and VirusTotal v3 domain analysis.
3. **`conversation_intelligence`**: Multi-turn dialogue parsing, PDF extraction, and Indian PII masking.
4. **`scam_stage_identification`**: Monotonic 5-stage social engineering kill-chain state machine.
5. **`victim_protection`**: 1930 Cybercrime police complaint generator and trilingual safety advice.

---

## API Endpoints Reference

### 1. Analyze Conversation / Job Offer (`POST /api/analyze`)

Analyzes a conversation transcript, job offer letter, or single message.

- **Request Body**:
  ```json
  {
    "text": "Earn Rs 5,000 daily liking YouTube videos. Deposit Rs 1,000 for VIP task on Telegram @Priya",
    "language": "en"
  }
  ```

- **Response (200 OK)**:
  ```json
  {
    "verdict": "SCAM",
    "risk_score": 88,
    "confidence": 0.95,
    "scam_stage": {
      "stage": 2,
      "name": "Stage 2: Prepaid Trap",
      "description": "Scammer demands deposit for VIP merchant tasks.",
      "is_active": true,
      "next_move": "They will prompt you to complete higher value combo orders.",
      "what_user_should_do": "Cease all contact and do not transfer any funds."
    },
    "signals": [
      {
        "id": "PREPAID_TASK",
        "name": "Prepaid Task Deposit",
        "evidence": "Deposit Rs 1,000 for VIP task",
        "weight": 35
      }
    ],
    "company_verification": {
      "company_name": null,
      "mca_verified": false,
      "domain_risk": "CLEAN"
    }
  }
  ```

### 2. Generate 1930 Helpline Complaint Pack (`POST /api/report`)

Generates a pre-formatted cybercrime complaint dossier.

- **Request Body**:
  ```json
  {
    "messages": [
      {"sender": "+91 98765 43210", "text": "Pay Rs 5000 to fraud@okhdfcbank", "timestamp": "10:00 AM"}
    ],
    "victim_name": "Rahul Sharma",
    "victim_phone": "9876543210",
    "amount_lost": 5000.0,
    "language": "en"
  }
  ```

- **Response (200 OK)**:
  ```json
  {
    "report_text": "NATIONAL CYBER CRIME REPORTING PORTAL COMPLAINT DRAFT...",
    "suggested_helpline": "1930",
    "summary": "Task scam financial fraud via UPI transfer."
  }
  ```

### 3. Run Benchmark Evaluation Suite (`GET /api/eval`)

Executes the automated 70-case evaluation test suite and returns performance metrics.

---

## Environment Setup

Create a `.env` file in the `backend/` directory:

```bash
# Server Port & Mode
PORT=8000
ENVIRONMENT=development
RATE_LIMIT=60

# Groq Cloud API
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="openai/gpt-oss-120b"

# Google Gemini API
GEMINI_API_KEY="your_gemini_api_key_here"
GEMINI_MODEL="gemini-2.0-flash"
LLM_TIMEOUT=30

# VirusTotal Threat Intelligence API
VIRUSTOTAL_API_KEY="your_virustotal_api_key_here"

# Scoring Weights
RULES_WEIGHT=0.60
LLM_WEIGHT=0.40
MAX_INPUT_CHARS=50000
```

---

## Installation & Running Locally

### Prerequisites
- **Python**: 3.10 or higher
- **pip**: Latest version

### Virtual Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Benchmarking & Offline Testing

To test detection accuracy across the 70 benchmark cases:

```bash
cd backend
python -c "
import json
from app.services.analyzer import analyze_case
cases = json.load(open('data/testset.json', encoding='utf-8'))
correct = sum(1 for c in cases if analyze_case(c['text']).verdict == c['expected_verdict'])
print(f'Accuracy: {correct}/{len(cases)} ({correct/len(cases)*100:.2f}%)')
"
```
