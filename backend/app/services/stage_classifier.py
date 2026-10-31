"""StageClassifier: Dedicated Stage-by-Stage Forensic Classifier for Task Scams.

Deconstructs conversation flow across the 5 cybercriminal script stages:
  - Stage 0 (Bait): Initial unsolicited contact, exaggerated daily pay, no interview
  - Stage 1 (Hook): Trial task, small real payout (₹150-₹300) to build psychological trust
  - Stage 2 (Prepaid Trap): Asked to deposit money for VIP/combo tasks with promised returns
  - Stage 3 (Lock-in): Withdrawal blocked, extortion for TDS/tax/unfreeze fee or error penalty
  - Stage 4 (Exit): Blocked, group deleted, vanished, or secondary recovery agent arrives
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from app.models.schemas import Signal


@dataclass
class StageEvidence:
    stage: int
    pattern_id: str
    matched_text: str
    weight: int
    description: str


@dataclass
class StageClassificationResult:
    detected_stage: int
    stage_name: str
    confidence: float
    stage_progression: List[int]
    evidence_trail: List[StageEvidence]
    monetary_escalation: Dict[str, Any]
    next_scammer_move: str
    what_user_should_do: str


# ==============================================================================
# PATTERN DICTIONARY BY STAGE (English, Hinglish, Hindi, Punjabi)
# ==============================================================================

# Generic comma-tolerant rupee amount pattern: 150, 1,000, 5,000, 10,000, 1,50,000
_AMT = r"(?:rs\.?|₹|inr)?\s*[\d,]{2,}"


# ------------------------------------------------------------------------------
# STAGE 0: BAIT PATTERNS
# ------------------------------------------------------------------------------
STAGE_0_PATTERNS = {
    "S0_VIDEO_LIKE_OFFER": re.compile(
        r"(?:like|liking|subscribe|subscribing|watch|watching)\s*(?:youtube|videos?|channels?)",
        re.I,
    ),
    "S0_RATING_TASK_OFFER": re.compile(
        r"(?:hotel|restaurant|product|google\s*maps?|app)\s*(?:review|rating|5\s*star)",
        re.I,
    ),
    "S0_EXAGGERATED_PAY": re.compile(
        r"(?:earn|salary|daily|income)[:\s]*(?:rs\.?|₹|inr)?\s*[\d,]+\s*(?:to\s*(?:rs\.?|₹|inr)?\s*[\d,]+)?\s*(?:daily|per\s*day|per\s*hour|a\s*day|weekly)",
        re.I,
    ),
    "S0_NO_INTERVIEW": re.compile(
        r"(?:no|without)\s*(?:skill|experience|interview|test|exam|assessment|resume)",
        re.I,
    ),
    "S0_INSTANT_SELECTION": re.compile(
        r"(?:direct|instant|immediate)\s*(?:joining|selection|hiring)\s*(?:without\s*exam|on\s*merit)?",
        re.I,
    ),
    "S0_TELEGRAM_MIGRATION": re.compile(
        r"(?:contact|message|add|reach)\s*(?:our)?\s*(?:receptionist|mentor|admin|supervisor|manager)\s*(?:on)?\s*telegram",
        re.I,
    ),
    # Regional Hindi / Hinglish
    "S0_HINDI_DAILY_EARN": re.compile(
        r"(?:घर\s*बैठे|daily)\s*[\d,]+.*(?:कमाएं|kamayein|kamaye|kamao)",
        re.I,
    ),
    # Regional Punjabi
    "S0_PUNJABI_BAIT": re.compile(
        r"(?:ਰੋਜ਼ਾਨਾ\s*₹[\d,]+|ਘਰ\s*ਬੈਠੇ.*ਕਮਾਓ|ਕੋਈ\s*ਇੰਟਰਵਿਊ\s*ਨਹੀਂ)",
        re.I,
    ),
}


# ------------------------------------------------------------------------------
# STAGE 1: HOOK PATTERNS (Trust Building & Small Payouts)
# ------------------------------------------------------------------------------
STAGE_1_PATTERNS = {
    "S1_SMALL_PAYOUT_SENT": re.compile(
        r"(?:₹|rs\.?|inr)?\s*(?:100|150|200|250|300|500)\s*(?:credited|transferred|sent|received|earned|approved)",
        re.I,
    ),
    "S1_SMALL_PAYOUT_RECEIVED": re.compile(
        r"(?:got|received|credited)\s*(?:₹|rs\.?|inr)?\s*(?:100|150|200|250|300|500)",
        re.I,
    ),
    "S1_TRIAL_TASK_BONUS": re.compile(
        r"(?:trial|welcome|novice|first)\s*(?:task|bonus|incentive|order|payout).*" + _AMT,
        re.I,
    ),
    "S1_SCREENSHOT_TASK_SUBMIT": re.compile(
        r"(?:send|sent|submit|attach)\s*screenshot\s*(?:of\s*liked|proof|done)?",
        re.I,
    ),
    "S1_GROUP_SOCIAL_PROOF": re.compile(
        r"(?:all\s*\d+\s*members\s*got|received\s*payment\s*thank\s*you|fast\s*payment\s*best\s*job)",
        re.I,
    ),
    # Regional Hinglish
    "S1_HINGLISH_PAYOUT": re.compile(
        r"(?:account\s*mein|paytm\s*par|phonepe\s*par)\s*(?:₹|rs\.?)?\s*[\d,]+\s*(?:aa\s*gaye|mil\s*gaye|mil\s*gaya)",
        re.I,
    ),
    # Regional Punjabi
    "S1_PUNJABI_PAYOUT": re.compile(
        r"(?:₹[\d,]+\s*(?:ਮਿਲ\s*ਗਏ|ਖਾਤੇ\s*ਵਿੱਚ\s*ਭੇਜ|ਗੂਗਲ\s*ਪੇਅ))",
        re.I,
    ),
}


# ------------------------------------------------------------------------------
# STAGE 2: PREPAID TRAP PATTERNS (Demanding Money / Combo Orders)
# ------------------------------------------------------------------------------
STAGE_2_PATTERNS = {
    "S2_DEPOSIT_FOR_RETURN": re.compile(
        r"(?:deposit|invest|recharge)\s*" + _AMT + r".*(?:return|get|profit|refund|earn).*" + _AMT,
        re.I,
    ),
    "S2_PROMISED_PERCENT_RETURN": re.compile(
        r"(?:return|earn|get|profit)\s*" + _AMT + r".*(?:after|on|for|per).*(?:deposit|invest|recharge|task)",
        re.I,
    ),
    "S2_GUARANTEED_PROFIT_SCHEME": re.compile(
        r"(?:guaranteed|assured|fixed)\s*(?:return|income|profit|earning|gain)\s*(?:\d+[%x×]|immediate)?",
        re.I,
    ),
    "S2_PREPAID_COMBO_TASK": re.compile(
        r"(?:merchant\s*prepaid|package\s*[a-d]|order\s*simulation|(?:start|choose|select|pay\s*for|deposit\s*for)\s*(?:a\s*)?(?:vip\s*task|combo\s*task)|(?:vip\s*task|combo\s*task)\s*(?:requires|deposit|plan|package|amount|fee|\:|\₹))",
        re.I,
    ),
    "S2_UPFRONT_EQUIPMENT_FEES": re.compile(
        r"(?:registration|joining|processing|activation|laptop|uniform|gate\s*pass|proctoring|software|security|caution|token|kit|medical|id\s*card)[:\s]*(?:fee|charge|deposit|amount|bond)?[:\s]*" + _AMT + r"|(?:refundable\s*)?(?:security|caution)\s*deposit\s*(?:of)?\s*" + _AMT + r"|(?:deposit|transfer|send)\s*(?:a\s*)?(?:refundable\s*)?(?:security\s*|caution\s*)?deposit\s*(?:of)?\s*" + _AMT + r"|(?:ਸੁਰੱਖਿਆ\s*ਡਿਪਾਜ਼ਿਟ|ਡਿਪਾਜ਼ਿਟ|ਫੀਸ).*" + _AMT,
        re.I,
    ),
    "S2_PERSONAL_UPI_ROUTING": re.compile(
        r"(?:pay|transfer|send)\s*" + _AMT + r".*(?:to\s*merchant\s*upi|upi\s*id|to\s*account)",
        re.I,
    ),
    # Regional Hinglish
    "S2_HINGLISH_TRAP": re.compile(
        r"(?:deposit\s*karna\s*hoga|paisa\s*wapas\s*milega\s*with\s*commission|guaranteed\s*profit)",
        re.I,
    ),
    # Regional Punjabi
    "S2_PUNJABI_TRAP": re.compile(
        r"(?:ਡਿਪਾਜ਼ਿਟ\s*ਕਰਦੇ\s*ਹੋ\s*ਤਾਂ.*ਵਾਪਸ\s*ਮਿਲਣਗੇ|ਗਾਰੰਟੀਡ\s*ਮੁਨਾਫਾ)",
        re.I,
    ),
}


# ------------------------------------------------------------------------------
# STAGE 3: LOCK-IN PATTERNS (Withdrawal Blocked & Extortion)
# ------------------------------------------------------------------------------
STAGE_3_PATTERNS = {
    "S3_WITHDRAWAL_FROZEN": re.compile(
        r"(?:withdrawal|withdraw|payout)\s*(?:blocked|frozen|suspended|pending|failed|locked|withheld)",
        re.I,
    ),
    "S3_TAX_UNFREEZE_EXTORTION": re.compile(
        r"(?:pay|deposit|transfer|settle)\s*(?:tax|tds|gst|fee|charge|penalty|clearing|bond|fine)\s*(?:to|for|before|unless|of)\s*" + _AMT,
        re.I,
    ),
    "S3_SYSTEM_ERROR_PENALTY": re.compile(
        r"(?:data\s*fix|system\s*error|error\s*code|credit\s*score|score\s*dropped).*(?:fee|charge|recharge|deposit|" + _AMT + r")",
        re.I,
    ),
    "S3_CANNOT_DEDUCT_AUTOMATIC": re.compile(
        r"(?:cannot|can'?t)\s*(?:deduct|cut)\s*(?:from\s*balance|automatically)",
        re.I,
    ),
    "S3_LEGAL_POLICE_THREAT": re.compile(
        r"(?:report\s*(?:to|your)\s*(?:police|cyber\s*crime|aadhaar|pan)|police\s*dispatch|legal\s*team|verification\s*bond)",
        re.I,
    ),
    # Regional Hinglish
    "S3_HINGLISH_LOCKIN": re.compile(
        r"(?:error\s*repair\s*karne\s*ke\s*liye|account\s*terminate\s*ho\s*jayega|paisa\s*forfeit)",
        re.I,
    ),
    # Regional Punjabi
    "S3_PUNJABI_LOCKIN": re.compile(
        r"(?:ਨਿਕਾਸੀ.*ਰੋਕ|ਕਲੀਅਰੈਂਸ\s*ਫੀਸ|ਸਾਰਾ\s*ਖਾਤਾ\s*ਬੰਦ|ਟੈਕਸ\s*ਬਕਾਇਆ)",
        re.I,
    ),
}


# ------------------------------------------------------------------------------
# STAGE 4: EXIT PATTERNS (Vanish, Blocked & Secondary Scams)
# ------------------------------------------------------------------------------
STAGE_4_PATTERNS = {
    "S4_VICTIM_BLOCKED": re.compile(
        r"(?:blocked|removed|kicked)\s*(?:from|by|me|you)",
        re.I,
    ),
    "S4_GROUP_DELETED": re.compile(
        r"(?:group|channel|community)\s*(?:deleted|removed|disappeared|gone|terminated)",
        re.I,
    ),
    "S4_NUMBER_SWITCHED_OFF": re.compile(
        r"(?:number|phone)\s*(?:switched\s*off|not\s*reachable|disconnected|inactive)",
        re.I,
    ),
    "S4_DISAPPEARED_WITH_FUNDS": re.compile(
        r"(?:took\s*(?:my)?\s*" + _AMT + r".*disappeared|money\s*(?:gone|lost|stolen|doob\s*gaye))",
        re.I,
    ),
    "S4_SECONDARY_RECOVERY_AGENT": re.compile(
        r"(?:recovery|refund)\s*(?:agent|expert|specialist|advocate|lawyer|help)|(?:advocate.*cyber|authorized\s*recovery|server\s*unfreeze\s*charge|recover.*(?:task|scam|funds|lost))",
        re.I,
    ),
    # Regional Hinglish
    "S4_HINGLISH_EXIT": re.compile(
        r"(?:group\s*se\s*nikaal\s*diya|paise\s*doob\s*gaye|username\s*sab\s*delete)",
        re.I,
    ),
    # Regional Punjabi
    "S4_PUNJABI_EXIT": re.compile(
        r"(?:ਟੈਲੀਗ੍ਰਾਮ\s*'ਤੇ\s*ਮੈਨੂੰ\s*ਬਲਾਕ|ਗਰੁੱਪ\s*ਵੀ\s*ਡਿਲੀਟ|ਪੈਸੇ\s*ਚਲੇ\s*ਗਏ)",
        re.I,
    ),
}


# ==============================================================================
# STAGE CLASSIFIER CLASS
# ==============================================================================

class StageClassifier:
    """Stage-by-stage classifier identifying conversation stage using structured pattern banks."""

    STAGE_NAMES = {
        0: "Stage 0: Bait",
        1: "Stage 1: Hook & Small Payouts",
        2: "Stage 2: Prepaid Trap",
        3: "Stage 3: Lock-in & Extortion",
        4: "Stage 4: Exit & Secondary Scam",
    }

    STAGE_NEXT_MOVES = {
        0: "The scammer will invite you to Telegram or WhatsApp, ask you to perform a trial task (like a video or rating), and send you ₹100-₹200 to establish trust.",
        1: "The scammer will invite you to a 'VIP/Merchant' task, asking you to deposit ₹1,000 to ₹5,000 with a promise of 30-50% instant return.",
        2: "Once you transfer money, they will lock your withdrawal and claim a 'system error' or 'combo task', demanding ₹10,000+ more.",
        3: "They will threaten you with account forfeiture, taxes, or police complaints. They will NEVER release your money and will eventually block you.",
        4: "Beware of people claiming to be 'cyber recovery agents' or 'lawyers' offering to recover lost funds for an upfront fee — this is a secondary scam.",
    }

    STAGE_ADVICE = {
        0: "Do NOT share your WhatsApp number or move to private Telegram groups. Never send personal details.",
        1: "Keep the small trial payout if already credited, but immediately STOP and block them before they ask for a deposit.",
        2: "DO NOT send any deposit or recharge. Your money will NOT be refunded. Call 1930 immediately to freeze the recipient UPI account.",
        3: "STOP paying immediately. Do not pay any 'tax' or 'unfreeze fee'. Preserve all chat screenshots and file an FIR at cybercrime.gov.in.",
        4: "Report all suspect phone numbers and UPI IDs to helpline 1930. Do not pay any third-party 'recovery agent'.",
    }

    def __init__(self):
        pass

    def extract_stage_features(self, text: str) -> Dict[int, List[StageEvidence]]:
        """Run all pattern banks and return matched evidence grouped by stage."""
        features: Dict[int, List[StageEvidence]] = {0: [], 1: [], 2: [], 3: [], 4: []}

        # Check Stage 4 (Exit)
        for pid, pat in STAGE_4_PATTERNS.items():
            for m in pat.finditer(text):
                features[4].append(StageEvidence(
                    stage=4,
                    pattern_id=pid,
                    matched_text=m.group(0),
                    weight=50,
                    description="Scammer blocking victim, channel deletion, or secondary recovery approach",
                ))

        # Check Stage 3 (Lock-in)
        for pid, pat in STAGE_3_PATTERNS.items():
            for m in pat.finditer(text):
                features[3].append(StageEvidence(
                    stage=3,
                    pattern_id=pid,
                    matched_text=m.group(0),
                    weight=45,
                    description="Withdrawal blocked with fee extortion, penalty, or legal threats",
                ))

        # Check Stage 2 (Prepaid Trap)
        for pid, pat in STAGE_2_PATTERNS.items():
            for m in pat.finditer(text):
                features[2].append(StageEvidence(
                    stage=2,
                    pattern_id=pid,
                    matched_text=m.group(0),
                    weight=40,
                    description="Deposit demand for promised high return or upfront job fee",
                ))

        # Check Stage 1 (Hook)
        for pid, pat in STAGE_1_PATTERNS.items():
            for m in pat.finditer(text):
                features[1].append(StageEvidence(
                    stage=1,
                    pattern_id=pid,
                    matched_text=m.group(0),
                    weight=30,
                    description="Small trial payout credited, building psychological trust",
                ))

        # Check Stage 0 (Bait)
        for pid, pat in STAGE_0_PATTERNS.items():
            for m in pat.finditer(text):
                features[0].append(StageEvidence(
                    stage=0,
                    pattern_id=pid,
                    matched_text=m.group(0),
                    weight=20,
                    description="Unsolicited part-time job offer, video likes, high daily salary",
                ))

        return features

    def classify(self, text: str, existing_signals: Optional[List[Signal]] = None) -> StageClassificationResult:
        """Classify stage using hierarchical monotonic progression rules."""
        features = self.extract_stage_features(text)
        signal_ids = {s.id for s in (existing_signals or [])}

        progression: List[int] = []
        all_evidence: List[StageEvidence] = []

        for st in range(5):
            if features[st]:
                progression.append(st)
                all_evidence.extend(features[st])

        # Monotonic State Transition Logic:
        # Highest confirmed stage in the cybercriminal killchain takes precedence.
        has_exit = bool(features[4])
        has_blocked = bool(features[3] or "WITHDRAWAL_BLOCKED_FEE" in signal_ids)
        has_real_deposit = bool(features[2] or "UPFRONT_DEPOSIT" in signal_ids)
        has_payout = bool(features[1] or "SMALL_PAYOUT_THEN_ESCALATE" in signal_ids)

        if has_exit:
            detected_stage = 4
            confidence = 0.95
        elif has_blocked:
            detected_stage = 3
            confidence = 0.92
        elif has_real_deposit:
            # If trial payout happened (stage 1) and there was no actual deposit requested yet, stay at stage 1
            if has_payout and "UPFRONT_DEPOSIT" not in signal_ids and not any(p.pattern_id in {"S2_DEPOSIT_FOR_RETURN", "S2_UPFRONT_EQUIPMENT_FEES", "S2_PERSONAL_UPI_ROUTING"} for p in features[2]):
                detected_stage = 1
                confidence = 0.90
            else:
                detected_stage = 2
                confidence = 0.90
        elif has_payout:
            detected_stage = 1
            confidence = 0.88
        elif features[0] or any(s in signal_ids for s in ["TOO_GOOD_PAY", "MOVE_TO_PRIVATE_CHAT", "NO_INTERVIEW_INSTANT_OFFER"]):
            detected_stage = 0
            confidence = 0.85
        else:
            detected_stage = 0
            confidence = 0.50

        # Money escalation analysis
        amounts = re.findall(r"(?:₹|rs\.?|inr)?\s*([\d,]+)", text, re.I)
        cleaned_amounts = []
        for a in amounts:
            clean = a.replace(",", "")
            if clean.isdigit() and len(clean) >= 3:
                cleaned_amounts.append(int(clean))

        monetary_escalation = {
            "amounts_detected": cleaned_amounts,
            "min_amount": min(cleaned_amounts) if cleaned_amounts else 0,
            "max_amount": max(cleaned_amounts) if cleaned_amounts else 0,
            "is_escalating": len(cleaned_amounts) >= 2 and cleaned_amounts[-1] > cleaned_amounts[0],
        }

        return StageClassificationResult(
            detected_stage=detected_stage,
            stage_name=self.STAGE_NAMES[detected_stage],
            confidence=confidence,
            stage_progression=progression if progression else [0],
            evidence_trail=all_evidence,
            monetary_escalation=monetary_escalation,
            next_scammer_move=self.STAGE_NEXT_MOVES[detected_stage],
            what_user_should_do=self.STAGE_ADVICE[detected_stage],
        )


_classifier: Optional[StageClassifier] = None

def get_stage_classifier() -> StageClassifier:
    global _classifier
    if _classifier is None:
        _classifier = StageClassifier()
    return _classifier
