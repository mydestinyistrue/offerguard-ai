# Module 1: Job / Task Scam Classifier

> **Category:** Job/task scam classifier  
> **Function:** Analyzes posts, chats, and offer letters for financial scam patterns and high-yield baits  
> **Priority:** Essential · Core Engine

A standalone, plug-and-play classification engine for detecting fraudulent job postings, task-based work-from-home schemes (YouTube like/subscribe, Google review tasks, hotel rating scams), crypto merchant tasks, and fake appointment letters.

---

## Table of Contents

- [Features](#features)
- [Architecture & Dual-Engine Scoring](#architecture--dual-engine-scoring)
- [File Structure](#file-structure)
- [Standalone Installation & Usage](#standalone-installation--usage)
  - [1. Copy Files](#1-copy-files)
  - [2. Basic Offline Usage (Zero Dependencies)](#2-basic-offline-usage-zero-dependencies)
  - [3. Enabling Groq Cloud 120B AI Reasoning](#3-enabling-groq-cloud-120b-ai-reasoning)
  - [4. Single-Line Convenience Function](#4-single-line-convenience-function)
- [API Reference](#api-reference)
  - [`JobTaskClassifier`](#jobtaskclassifier)
  - [`JobClassificationResult`](#jobclassificationresult)
- [Environment Configuration](#environment-configuration)

---

## Features

- **Multi-lingual pattern detection**: Evaluates English, Hinglish, Hindi, and Punjabi scripts.
- **Financial red-flag analysis**: Identifies upfront deposits, "prepaid tasks", "combo orders", fake gate passes, and account rental/OTP requests.
- **Compensation interval awareness**: Distinguishes legitimate annual compensation (`₹5,00,000 - ₹7,00,000 a year`, `CTC`, `LPA`, `PF`, `Gratuity`) from deceptive daily cash baits (`₹5,000/day`).
- **Hybrid reasoning**: Blends deterministic regex heuristics (60%) with Groq Cloud LLM reasoning (40%, `openai/gpt-oss-120b`).
- **Safety latch override**: Automatically flags threats if high-confidence deterministic rules are violated ($score \ge 70$), preventing LLM false negatives.
- **Fully decoupled**: Operates 100% offline with zero external services when no API key is supplied.

---

## Architecture & Dual-Engine Scoring

```
[ Input Job Post / Chat Text ]
              │
       ┌──────┴──────┐
       ▼             ▼
[ Rules Engine ]  [ Groq 120B / Gemini ]
  - 18 Signals     - Structured JSON
  - Deductions     - Forensic Reasoning
       │             │
       └──────┬──────┘
              ▼
    [ Risk Score Blender ]
   (Rules * 0.60 + LLM * 0.40)
              │
              ▼
  [ JobClassificationResult ]
```

---

## File Structure

```bash
job_task_classifier/
├── __init__.py          # Module exports (JobTaskClassifier, classify_job_offer)
├── classifier.py        # Master hybrid orchestrator & score blending
├── rules_engine.py      # Standalone 18-signal deterministic heuristic engine
├── llm_service.py       # Groq Cloud 120B / Gemini API client
└── README.md            # Documentation
```

---

## Standalone Installation & Usage

### 1. Copy Files

Copy the `job_task_classifier/` directory directly into your project root:

```bash
cp -r backend/app/modules/job_task_classifier /path/to/your/project/
```

### 2. Basic Offline Usage (Zero Dependencies)

```python
from job_task_classifier import JobTaskClassifier

# Initialize without an API key (fully offline heuristic mode)
classifier = JobTaskClassifier()

result = classifier.classify("Earn Rs 5,000 daily liking YouTube videos on Telegram. Add HR @Priya")

print("Verdict      :", result.verdict)       # "SCAM"
print("Risk Score   :", result.risk_score)    # 72 (0 to 100)
print("Is Scam      :", result.is_scam)        # True
print("Confidence   :", result.confidence)     # 0.80
print("Explanation  :", result.explanation)
print("Signals Found:", len(result.signals))
for s in result.signals:
    print(f"  - [{s['id']}] Weight: {s['weight']} | Quote: '{s['evidence']}'")
```

### 3. Enabling Groq Cloud 120B AI Reasoning

Provide a Groq API key via constructor or environment variable:

```python
import os
os.environ["GROQ_API_KEY"] = "gsk_..."

classifier = JobTaskClassifier(groq_api_key="gsk_...")
result = classifier.classify(
    "Hi dear! Part-time work available. Daily 20 mins review hotel on Google maps. Pay 150 per review."
)

print(result.verdict)      # "SCAM"
print(result.explanation)  # Detailed LLM forensic reasoning
print(result.llm_assisted) # True
```

### 4. Single-Line Convenience Function

```python
from job_task_classifier import classify_job_offer

result = classify_job_offer("Deposit Rs 1000 to get Rs 1500 commission in 15 mins")
if result.is_scam:
    print(f"Danger! Flagged as {result.verdict} with risk score {result.risk_score}/100")
```

---

## API Reference

### `JobTaskClassifier`

```python
JobTaskClassifier(
    groq_api_key: str | None = None,
    gemini_api_key: str | None = None,
    rules_weight: float = 0.60,
    llm_weight: float = 0.40
)
```

- `classify(text: str, language: str = "en") -> JobClassificationResult`

### `JobClassificationResult`

| Attribute | Type | Description |
|---|---|---|
| `verdict` | `str` | Final classification: `"SCAM"`, `"SUSPICIOUS"`, `"LIKELY_GENUINE"`, or `"UNSURE"`. |
| `risk_score` | `int` | Composite forensic risk score from `0` to `100`. |
| `confidence` | `float` | Estimation certainty from `0.0` to `1.0`. |
| `signals` | `list[dict]` | Detected forensic triggers (includes `id`, `name`, `weight`, `evidence`). |
| `explanation` | `str` | Human-readable explanation of why the offer was classified. |
| `is_scam` | `bool` | Convenience flag (`True` for `SCAM` or high-risk `SUSPICIOUS`). |
| `llm_assisted` | `bool` | Whether an LLM was invoked and contributed to the verdict. |
| `rules_score` | `int` | Raw deterministic rule score before blending. |
| `llm_score` | `int | None` | Raw LLM risk score (or `None` if running offline). |
| `to_dict()` | `method` | Returns serializable Python dictionary. |

---

## Environment Configuration

```bash
GROQ_API_KEY="gsk_..."
GROQ_MODEL="openai/gpt-oss-120b"
GEMINI_API_KEY="..."
RULES_WEIGHT=0.60
LLM_WEIGHT=0.40
```
