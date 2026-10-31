"""Module 5: Victim Protection.
Function: Explain risk and provide 1930 reporting guidance.
Generates pre-formatted National Cyber Crime Portal (1930) complaint packs, speed-dial links, and trilingual guidance.
"""

from .report_generator import (
    generate_complaint_pack,
    extract_incident_artifacts,
    VictimProtectionService,
    ReportGenerator,
)
from .language import (
    get_localized_stage_label,
    get_localized_next_move,
    get_localized_advice,
    get_localized_pack,
)

__all__ = [
    "VictimProtectionService",
    "ReportGenerator",
    "generate_complaint_pack",
    "extract_incident_artifacts",
    "get_localized_stage_label",
    "get_localized_next_move",
    "get_localized_advice",
    "get_localized_pack",
]
