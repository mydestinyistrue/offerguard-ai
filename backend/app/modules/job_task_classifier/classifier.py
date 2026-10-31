"""Standalone, plug-and-play Job/Task Scam Classifier.

Can be extracted and integrated into ANY Python application, FastAPI/Django service,
worker, or CLI tool with ZERO internal dependencies.

Example Usage:
--------------
    from job_task_classifier import JobTaskClassifier

    classifier = JobTaskClassifier() # auto-reads GROQ_API_KEY from env if available
    result = classifier.classify("Earn Rs 5000 daily liking YouTube videos on Telegram")

    print(result.verdict)      # "SCAM"
    print(result.risk_score)   # 85
    print(result.signals)      # [{'id': 'TOO_GOOD_PAY', 'weight': 20, ...}, ...]
    print(result.explanation)  # "Detected high daily pay bait with push to Telegram..."
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

from .rules_engine import detect_all_signals, compute_rules_score, Signal
from .llm_service import LLMService


@dataclass
class JobClassificationResult:
    """Clean, self-contained result format for external apps."""
    verdict: str              # "SCAM" | "SUSPICIOUS" | "LIKELY_GENUINE" | "UNSURE"
    risk_score: int           # 0 to 100
    confidence: float         # 0.0 to 1.0
    signals: List[Dict[str, Any]]  # List of triggered forensic signals
    explanation: str          # Concise human explanation
    is_scam: bool             # Convenience boolean flag
    llm_assisted: bool        # Whether LLM reasoning contributed
    rules_score: int          # Raw score from deterministic patterns
    llm_score: Optional[int] = None  # Raw score from LLM if active

    def to_dict(self) -> Dict[str, Any]:
        """Convert result directly to dictionary for JSON APIs."""
        return asdict(self)


class JobTaskClassifier:
    """Self-contained Job & Task Scam Classifier.

    Blends deterministic regex heuristics with optional Groq / Gemini reasoning.
    Works fully offline if no API keys are provided.
    """

    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        rules_weight: float = 0.5,
        llm_weight: float = 0.5,
    ):
        self.rules_weight = rules_weight
        self.llm_weight = llm_weight
        self.llm_service = LLMService(
            groq_api_key=groq_api_key,
            gemini_api_key=gemini_api_key,
        )

    def classify(self, text: str, language: str = "en") -> JobClassificationResult:
        """Classify a job offer, post, or chat message.

        Parameters
        ----------
        text : str
            The raw text of the job description, WhatsApp/Telegram message, or email.
        language : str, optional
            'en', 'hi', or 'pa' (default is 'en').

        Returns
        -------
        JobClassificationResult
            Self-contained classification with verdict, risk score, and signal evidence.
        """
        if not text or not text.strip():
            return JobClassificationResult(
                verdict="UNSURE",
                risk_score=0,
                confidence=0.0,
                signals=[],
                explanation="No text provided for classification.",
                is_scam=False,
                llm_assisted=False,
                rules_score=0,
            )

        # 1. Run deterministic pattern rules
        rule_signals = detect_all_signals(text)
        rules_score = compute_rules_score(rule_signals)

        # 2. Check for signature scam triggers
        has_deposit = any(s.id == "UPFRONT_DEPOSIT" for s in rule_signals)
        has_prepaid_return = any(s.id == "PREPAID_RETURN" for s in rule_signals)
        has_blocked_fee = any(s.id == "WITHDRAWAL_BLOCKED_FEE" for s in rule_signals)
        has_small_payout = any(s.id == "SMALL_PAYOUT_THEN_ESCALATE" for s in rule_signals)
        has_too_good_pay = any(s.id == "TOO_GOOD_PAY" for s in rule_signals)
        has_private_chat = any(s.id == "MOVE_TO_PRIVATE_CHAT" for s in rule_signals)
        has_no_interview = any(s.id == "NO_INTERVIEW_INSTANT_OFFER" for s in rule_signals)
        has_genuine = any(s.id == "GENUINE_SIGNALS" for s in rule_signals)

        payment_signal_count = sum(1 for s in rule_signals if s.id in {
            "UPFRONT_DEPOSIT", "PREPAID_RETURN", "WITHDRAWAL_BLOCKED_FEE", "ACCOUNT_RENTAL_OR_OTP"
        })

        # 3. Optional LLM reasoning if configured
        llm_score: Optional[int] = None
        llm_explanation: Optional[str] = None
        llm_verdict: Optional[str] = None
        llm_assisted = False

        if self.llm_service.is_configured:
            try:
                llm_res = self.llm_service.analyze_conversation(text, language=language)
                if llm_res:
                    llm_score = llm_res.risk_score
                    llm_explanation = llm_res.explanation
                    llm_verdict = llm_res.verdict
                    llm_assisted = True
            except Exception:
                llm_assisted = False

        # 4. Blend scores
        if llm_score is not None:
            blended_score = int(round(self.rules_weight * rules_score + self.llm_weight * llm_score))
        else:
            blended_score = rules_score

        # 5. Overrides & Final Verdict Assignment
        if "escrow" in text.lower() or "bank guarantee" in text.lower():
            blended_score = 45
            verdict = "SUSPICIOUS"
        elif has_genuine and not (has_deposit or has_prepaid_return or has_blocked_fee):
            blended_score = min(blended_score, 10)
            verdict = "LIKELY_GENUINE"
        elif has_blocked_fee or payment_signal_count >= 2:
            blended_score = max(blended_score, 88)
            verdict = "SCAM"
        elif has_deposit or has_prepaid_return:
            blended_score = max(blended_score, 75)
            verdict = "SCAM"
        elif (has_too_good_pay and has_private_chat) or (has_too_good_pay and has_no_interview):
            blended_score = max(blended_score, 72)
            verdict = "SCAM"
        elif has_small_payout and (has_private_chat or has_too_good_pay):
            blended_score = max(blended_score, 70)
            verdict = "SCAM"
        elif blended_score >= 70:
            verdict = "SCAM"
        elif blended_score >= 30 or rule_signals:
            verdict = "SUSPICIOUS"
        elif has_genuine or len(text.strip().split()) > 20:
            verdict = "LIKELY_GENUINE"
        else:
            verdict = "UNSURE"

        # 6. Build explanation
        if llm_explanation:
            explanation = llm_explanation
        elif verdict == "SCAM":
            top_sigs = [s.id.replace("_", " ").title() for s in rule_signals[:3]]
            explanation = f"High probability scam detected. Red flags found: {', '.join(top_sigs)}."
        elif verdict == "SUSPICIOUS":
            explanation = "Suspicious job offer or task pattern detected. Exercise caution and verify employer credentials."
        elif verdict == "LIKELY_GENUINE":
            explanation = "Standard corporate recruitment patterns detected without upfront payment demands."
        else:
            explanation = "Insufficient signal information to conclusively classify."

        # Format signal list
        signals_data = [
            {
                "id": s.id,
                "weight": s.weight,
                "evidence": getattr(s, "evidence", ""),
            }
            for s in rule_signals
        ]

        # Confidence calculation
        if verdict in ("SCAM", "LIKELY_GENUINE"):
            confidence = min(0.95, 0.70 + (len(rule_signals) * 0.05))
        else:
            confidence = 0.60

        return JobClassificationResult(
            verdict=verdict,
            risk_score=blended_score,
            confidence=round(confidence, 2),
            signals=signals_data,
            explanation=explanation,
            is_scam=(verdict == "SCAM" or (verdict == "SUSPICIOUS" and blended_score >= 60)),
            llm_assisted=llm_assisted,
            rules_score=rules_score,
            llm_score=llm_score,
        )


def classify_job_offer(
    text: str,
    groq_api_key: Optional[str] = None,
    language: str = "en",
) -> JobClassificationResult:
    """Convenience helper to classify text in a single line."""
    classifier = JobTaskClassifier(groq_api_key=groq_api_key)
    return classifier.classify(text, language=language)
