"""Stage state machine – determines the scam stage (0-4) from conversation signals.

Stages:
  0 – Bait:    Unknown number, "part-time job", high daily pay, no interview
  1 – Hook:    Telegram group, "mentor", small tasks, small payouts
  2 – Prepaid Trap: Deposit money for promised return, unknown UPI, fake dashboard
  3 – Lock-in: Withdrawal blocked, tax/unfreeze fee, urgency/threats
  4 – Exit:    Blocked, group deleted, recovery agent appears
"""

from __future__ import annotations

import re
from app.models.schemas import Signal


STAGE_LABELS = {
    0: "Bait",
    1: "Hook",
    2: "Prepaid Trap",
    3: "Lock-in",
    4: "Exit",
}

STAGE_DESCRIPTIONS = {
    0: "Initial contact — too-good-to-be-true job offers with no interview required.",
    1: "Building trust — small tasks and small payouts to create confidence.",
    2: "The trap — asking for deposits/payments with promises of higher returns.",
    3: "Locked in — withdrawal blocked, demanding more fees to release money.",
    4: "Exit — scammer disappears, blocks victim, or sends fake recovery agents.",
}

NEXT_LIKELY_MOVES = {
    0: "They will likely invite you to a Telegram/WhatsApp group and assign simple 'trial tasks' with small payouts to build trust.",
    1: "They will likely ask you to 'upgrade' or deposit money for higher-paying tasks, showing fake dashboards with growing balances.",
    2: "They will likely show a large balance on a fake dashboard but block your withdrawal, demanding 'tax' or 'verification fees'.",
    3: "They will keep inventing new fees (tax, insurance, compliance). Eventually they will block you and disappear.",
    4: "The scam is complete. A 'recovery agent' may contact you — this is also a scam. File a report with cybercrime helpline 1930.",
}


# ── Stage exit patterns ───────────────────────────────────────────────

_EXIT_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:blocked|removed|kicked)\s*(?:from|by|me|you)",
        r"(?:group|channel)\s*(?:deleted|removed|disappeared|gone)",
        r"(?:recovery|refund)\s*(?:agent|expert|specialist|manager|help)",
        r"(?:can'?t|cannot|unable)\s*(?:reach|contact|find)\s*(?:them|him|her|the\s*person)",
        r"(?:stopped|not)\s*(?:replying|responding|answering)",
        r"(?:money|amount)\s*(?:gone|lost|stolen|disappeared)",
        r"number\s*(?:switched\s*off|not\s*reachable|disconnected)",
        r"(?:group\s*se\s*nikaal|nikaal\s*diya|paise\s*doob\s*gaye|delete\s*kar\s*diya)", # Hinglish
        r"(?:ਬਲਾਕ\s*ਕਰ\s*ਦਿੱਤਾ|ਗਰੁੱਪ\s*(?:ਵੀ\s*)?ਡਿਲੀਟ|ਪੈਸੇ\s*ਚਲੇ\s*ਗਏ|ਫੋਨ\s*(?:ਕਿਉਂ\s*)?ਬੰਦ)", # Punjabi
    ]
]

_LOCK_IN_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:withdrawal|withdraw)\s*(?:blocked|frozen|suspended|failed|locked|pending)",
        r"(?:pay|deposit|settle).*(?:tax|fee|charge|penalty|bond|fine).*(?:unfreeze|unlock|release|withdraw|avoid|police)",
        r"(?:account|wallet|balance)\s*(?:frozen|blocked|locked|suspended)",
        r"(?:unfreeze|unlock|release)\s*(?:fee|charge|amount|deposit)",
        r"(?:verification\s*bond|police\s*dispatch|report\s*your\s*aadhaar)",
        r"(?:ਨਿਕਾਸੀ\s*(?:ਰੋਕ|ਬੰਦ)|ਕਲੀਅਰੈਂਸ\s*ਫੀਸ)", # Punjabi
        r"(?:निकासी\s*(?:रोक|फ्रीज)|सिस्टम\s*एरर|पैसे\s*फंस)", # Hindi
    ]
]


def detect_stage(arg1, arg2=None) -> int:
    """Determine the scam stage from signals and message content or text.
    
    Accepts (signals, messages), (text, signals), or (signals, text).
    """
    signals: list[Signal] = []
    full_text = ""

    if isinstance(arg1, str):
        full_text = arg1
        if isinstance(arg2, list):
            signals = arg2
    elif isinstance(arg1, list):
        if arg1 and isinstance(arg1[0], Signal):
            signals = arg1
            if isinstance(arg2, str):
                full_text = arg2
            elif isinstance(arg2, list):
                full_text = " ".join(m.get("text", "") if isinstance(m, dict) else str(m) for m in arg2)
        elif isinstance(arg2, list) and arg2 and isinstance(arg2[0], Signal):
            signals = arg2
            full_text = " ".join(m.get("text", "") if isinstance(m, dict) else str(m) for m in arg1)
        else:
            full_text = " ".join(m.get("text", "") if isinstance(m, dict) else str(m) for m in arg1)
            if isinstance(arg2, list):
                signals = arg2

    signal_ids = {s.id for s in signals}

    # Stage 4: Exit
    for pat in _EXIT_PATS:
        if pat.search(full_text):
            return 4

    # Stage 3: Lock-in
    if "WITHDRAWAL_BLOCKED_FEE" in signal_ids:
        return 3
    for pat in _LOCK_IN_PATS:
        if pat.search(full_text):
            return 3

    # Stage 2: Prepaid Trap
    if "UPFRONT_DEPOSIT" in signal_ids or "PREPAID_RETURN" in signal_ids:
        return 2

    # Stage 1: Hook (trust building with trial tasks or small payouts)
    if "SMALL_PAYOUT_THEN_ESCALATE" in signal_ids:
        return 1
    if re.search(r"(?:trial\s*task|task\s*1|mentor|supervisor|vip\s*task\s*channel).*(?:credited|bonus|incentive|completed|approve|sent|transferred|mil\s*gaye|ਮਿਲ\s*ਗਏ)", full_text, re.I):
        return 1

    # Stage 0: Bait (initial unsolicited pitch)
    bait_signals = {
        "TOO_GOOD_PAY", "FREE_MAIL_HR", "NO_INTERVIEW_INSTANT_OFFER",
        "URGENCY_PRESSURE", "BRAND_IMPERSONATION", "ACCOUNT_RENTAL_OR_OTP",
        "MOVE_TO_PRIVATE_CHAT",
    }
    if signal_ids & bait_signals:
        return 0

    # No clear stage detected — default to 0 if there are any scam signals
    if any(s.weight > 0 for s in signals):
        return 0

    return 0  # Lowest stage if nothing detected


def get_stage_label(stage: int) -> str:
    return STAGE_LABELS.get(stage, "Unknown")


def get_next_likely_move(stage: int) -> str:
    return NEXT_LIKELY_MOVES.get(stage, "")
