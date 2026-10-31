"""TaskGuard (ScamShield AI) Core Modular Architecture.

Derived directly from the official Problem Statement CTBF-AI-11 MVP Specification:
  1. job_task_classifier       -> Analyse posts, chats and offer letters
  2. company_verification       -> MCA registry and official domain checks
  3. conversation_intelligence  -> Understand multiple messages together
  4. scam_stage_identification  -> Recognize the progression of known scam scripts
  5. victim_protection          -> Explain risk and provide 1930 reporting guidance
"""

from . import (
    job_task_classifier,
    company_verification,
    conversation_intelligence,
    scam_stage_identification,
    victim_protection,
)

__all__ = [
    "job_task_classifier",
    "company_verification",
    "conversation_intelligence",
    "scam_stage_identification",
    "victim_protection",
]
