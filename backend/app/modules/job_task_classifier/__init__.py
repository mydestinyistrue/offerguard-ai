"""Module 1: Job/Task Scam Classifier.
Function: Analyse posts, chats and offer letters.

Provides both granular detection functions and a standalone, zero-dependency
`JobTaskClassifier` class that can be integrated into any other Python application.
"""

from .classifier import JobTaskClassifier, JobClassificationResult, classify_job_offer
from .rules_engine import (
    detect_signals,
    detect_all_signals,
    compute_rules_score,
    get_payment_signal_count,
    Signal,
)
from .llm_service import get_llm_service, LLMService

__all__ = [
    "JobTaskClassifier",
    "JobClassificationResult",
    "classify_job_offer",
    "detect_signals",
    "detect_all_signals",
    "compute_rules_score",
    "get_payment_signal_count",
    "get_llm_service",
    "LLMService",
    "Signal",
]
