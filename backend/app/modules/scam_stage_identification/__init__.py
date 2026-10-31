"""Module 4: Scam-Stage Identification.
Function: Recognize the progression of known scam scripts.

Tracks the 5-stage social engineering kill-chain (Stage 0 to Stage 4), monetary escalation,
and next-move foresight. Can be imported standalone in any Python application.
"""

from .stage_classifier import (
    get_stage_classifier,
    StageClassifier,
    StageClassificationResult,
    StageEvidence,
    identify_scam_stage,
)
from .stage_engine import detect_stage, STAGE_LABELS, STAGE_DESCRIPTIONS, NEXT_LIKELY_MOVES

ScamStageClassifier = StageClassifier
ScamStageEngine = detect_stage

__all__ = [
    "ScamStageClassifier",
    "ScamStageEngine",
    "get_stage_classifier",
    "StageClassifier",
    "StageClassificationResult",
    "StageEvidence",
    "identify_scam_stage",
    "detect_stage",
    "STAGE_LABELS",
    "STAGE_DESCRIPTIONS",
    "NEXT_LIKELY_MOVES",
]
