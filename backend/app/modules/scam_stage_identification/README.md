# Module 4: Scam-Stage Identification

> **Category:** Scam-stage identification  
> **Function:** Tracks the 5-stage social engineering kill-chain (Stage 0 to 4) and predicts the scammer's next move  
> **Priority:** Essential · Core Engine

A state-machine and pattern classifier that tracks how a victim is being led through the **5-Stage Social Engineering Kill-Chain** of modern task and employment scams:

```
[Stage 0: Bait] ──► [Stage 1: Hook] ──► [Stage 2: Prepaid Trap] ──► [Stage 3: Lock-In] ──► [Stage 4: Exit Scam]
```

---

## Table of Contents

- [The 5 Scam Script Stages](#the-5-scam-script-stages)
- [Monotonic Progression Architecture](#monotonic-progression-architecture)
- [File Structure](#file-structure)
- [Standalone Installation & Usage](#standalone-installation--usage)
  - [1. Copy Files](#1-copy-files)
  - [2. Identify Scam Stage](#2-identify-scam-stage)
  - [3. Predictive Next Move Forecasting](#3-predictive-next-move-forecasting)
  - [4. Single-Line Convenience Function](#4-single-line-convenience-function)
- [API Reference](#api-reference)
  - [`StageClassifier`](#stageclassifier)
  - [`StageIdentificationResult`](#stageidentificationresult)
- [Stage Detection Rules & Triggers](#stage-detection-rules--triggers)

---

## The 5 Scam Script Stages

| Stage | Name | Scam Mechanism & Psychological Trigger |
|---|---|---|
| **0** | **Bait** | Unsolicited WhatsApp/SMS message, excessive daily pay (₹2,000–₹8,000/day) for trivial tasks (YouTube likes, Google Maps reviews), zero interview. |
| **1** | **Hook** | Directs victim to Telegram receptionist, pays real token payout (₹150–₹300) to build psychological trust and proof-of-work. |
| **2** | **Prepaid Trap** | Asks for initial deposit for "VIP merchant orders" or "combo tasks" with promises of 30-50% instant profit. |
| **3** | **Lock-In** | Withdrawal balance is blocked. Extortion demands for 18% GST, "unfreeze fee", or "repair score" to release trapped funds. |
| **4** | **Exit Scam** | Group deleted, victim blocked, funds stolen, or fake "cyber recovery agent" approaches demanding upfront fee. |

---

## Monotonic Progression Architecture

Unlike stateless classifiers that evaluate each message in isolation, `StageClassifier` utilizes a **monotonic state machine**:
- Once a victim enters a predatory stage (e.g., Stage 3: Lock-in), polite messages or subsequent conversational pleasantries cannot demote the conversation back to Stage 0.
- Preserves the maximum reached risk stage across multi-message logs.
- Accompanied by a **Predictive Forecaster** that anticipates the scammer's subsequent coercive demand based on current stage context.

---

## File Structure

```bash
scam_stage_identification/
├── __init__.py          # Module exports (StageClassifier, identify_scam_stage)
├── stage_classifier.py  # High-level stage classifier & wrapper
├── stage_engine.py      # 5-stage monotonic progression state machine
└── README.md            # Documentation
```

---

## Standalone Installation & Usage

### 1. Copy Files

Copy the `scam_stage_identification/` directory directly into your project root:

```bash
cp -r backend/app/modules/scam_stage_identification /path/to/your/project/
```

### 2. Identify Scam Stage

```python
from scam_stage_identification import StageClassifier

classifier = StageClassifier()

text = """
Your withdrawal of Rs 75,000 is on hold due to system tax regulations.
Please deposit Rs 13,500 (18% GST) within 30 minutes to unfreeze your merchant balance.
"""

result = classifier.classify(text)

print("Detected Stage :", result.detected_stage)      # 3
print("Stage Name     :", result.stage_name)          # "Stage 3: Lock-in"
print("Confidence     :", result.confidence)          # 0.95
print("Next Move      :", result.next_scammer_move)
# Output: "They will keep inventing new fees (tax, insurance, compliance). Eventually they will block you and disappear."

print("Advice for User:", result.what_user_should_do)
# Output: "DO NOT pay any tax or unfreeze fee. They will never release the funds..."
```

### 3. Predictive Next Move Forecasting

```python
from scam_stage_identification import StageClassifier

classifier = StageClassifier()

# User just completed first token task
res = classifier.classify("Task 1 complete. Here is screenshot of like. Receptionist sent 150 rs to my GPay.")

print("Current Stage :", res.stage_name)        # "Stage 1: Hook"
print("Predicted Next:", res.next_scammer_move)
# Output: "They will now invite you to a VIP Telegram group and demand a prepaid deposit (Rs 1,000 - 3,000) for high commission tasks."
```

### 4. Single-Line Convenience Function

```python
from scam_stage_identification import identify_scam_stage

stage_info = identify_scam_stage("Deposit Rs 2000 for combo task")
print(f"Active Stage: {stage_info.detected_stage} ({stage_info.stage_name})")
```

---

## API Reference

### `StageClassifier`

```python
StageClassifier()
```

- `classify(text: str, current_stage: int = 0) -> StageIdentificationResult`

### `StageIdentificationResult`

| Attribute | Type | Description |
|---|---|---|
| `detected_stage` | `int` | Integer stage from `0` to `4` (or `-1` if genuine). |
| `stage_name` | `str` | Formal stage title (e.g., `"Stage 2: Prepaid Trap"`). |
| `confidence` | `float` | Classification certainty from `0.0` to `1.0`. |
| `is_active` | `bool` | `True` if a scam stage was recognized. |
| `next_scammer_move` | `str` | Anticipated next manipulative tactic. |
| `what_user_should_do`| `str` | Actionable defense advice for the victim. |
| `triggers_found` | `list[str]` | Specific keyword and pattern triggers matched. |
| `to_dict()` | `method` | Returns serializable Python dictionary. |

---

## Stage Detection Rules & Triggers

- **Stage 0 (Bait)**: Matches `5000/day`, `like youtube videos`, `google map review`, `no interview needed`, `daily payout`.
- **Stage 1 (Hook)**: Matches `telegram receptionist`, `code 888`, `trial task completed`, `credited 150`, `code sent`.
- **Stage 2 (Prepaid Trap)**: Matches `prepaid task`, `deposit 1000`, `recharge wallet`, `vip merchant`, `combo order`, `crypto order`.
- **Stage 3 (Lock-In)**: Matches `withdrawal is frozen`, `withheld`, `pay 18% gst`, `tax clearance`, `credit score repair`, `account unfrozen`.
- **Stage 4 (Exit Scam)**: Matches `blocked by admin`, `group deleted`, `fund recovery expert`, `hacker will recover funds`.
