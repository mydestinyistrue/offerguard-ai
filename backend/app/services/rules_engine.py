"""Rules engine – pattern-based scam signal detection with weighted scoring.

Optimized for Indian task scams, prepaid fraudulent schemes, fake job offers,
and multi-lingual transcripts (English, Hinglish, Hindi, Punjabi).
"""

from __future__ import annotations

import re
from app.models.schemas import Signal


# ── Comma-tolerant amount pattern ─────────────────────────────────────
_AMT = r"(?:rs\.?|₹|inr)?\s*[\d,]{3,}"

_UPFRONT_DEPOSIT_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:deposit|transfer|send|recharge|wire)[:\s]*" + _AMT,
        r"pay\s*(?:upfront|first|before|advance|fee|charge|deposit|amount|karein|kijiye|karo)[:\s]*" + _AMT,
        r"(?:cashier[\x27\s]?s?\s*check|advance\s*check).*" + _AMT,
        r"(?:registration|joining|processing|activation|laptop|uniform|gate\s*pass|proctoring|software|security|caution|token|clearing|kit|medical|id\s*card|verification|fee)[:\s]*(?:fee|charge|deposit|amount|bond|kit)?[:\s]*" + _AMT,
        r"(?:deposit|transfer|send)\s*(?:a\s*)?(?:refundable\s*)?(?:security\s*|caution\s*)?deposit\s*(?:of)?\s*" + _AMT,
        r"(?:refundable\s*)?(?:security|caution)\s*deposit\s*(?:of)?\s*" + _AMT,
        r"(?:refundable\s*)?caution\s*deposit",
        r"pay\s*(?:first|before|upfront|advance)\s*(?:rs\.?|₹|inr)?\s*[\d,]+",
        r"invest[:\s]*" + _AMT,
        r"minimum\s*(?:deposit|investment|recharge)",
        r"(?:top[\s\-]?up|recharge)\s*(?:your)?\s*(?:wallet|account|balance|portal)",
        r"security\s*franchise\s*fee",
        r"payment\s*kijiye.*(?:upi|account)",
        r"(?:fee|charge|bond)\s*(?:of)?[:\s]*" + _AMT,
        r"(?:ਸੁਰੱਖਿਆ\s*ਡਿਪਾਜ਼ਿਟ|ਡਿਪਾਜ਼ਿਟ|ਫੀਸ).*" + _AMT,
        r"(?:ਸੁਰੱਖਿਆ\s*ਡਿਪਾਜ਼ਿਟ|ਡਿਪਾਜ਼ਿਟ|ਫੀਸ)\s*(?:ਲਈ)?\s*" + _AMT + r"?\s*(?:ਜਮ੍ਹਾਂ|ਕਰਵਾਓ|ਭੇਜੋ)", # Punjabi
        r"(?:ਡਿਪਾਜ਼ਿਟ|ਫੀਸ|ਸੁਰੱਖਿਆ)\s*(?:ਜਮ੍ਹਾਂ|ਭੇਜੋ)", # Punjabi
        r"(?:डिपॉजिट|फीस|पेमेंट)\s*(?:करें|दीजिए|जमा)", # Hindi
    ]
]

_PREPAID_RETURN_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:deposit|invest|recharge)\s*" + _AMT + r".*(?:return|get|profit|refund|earn).*" + _AMT,
        r"(?:return|earn|get|profit)\s*" + _AMT + r".*(?:after|on|for|per).*(?:deposit|invest|recharge|task)",
        r"(?:guaranteed|assured|fixed)\s*(?:return|income|profit|earning|gain)",
        r"(?:\d+[%x×])\s*(?:return|profit|earning|gain)",
        r"(?:double|triple)\s*(?:your)?\s*(?:money|investment|amount)",
        r"commission\s*" + _AMT,
        r"combo\s*task",
        r"merchant\s*(?:task|order|prepaid)",
        r"ਗਾਰੰਟੀਡ\s*ਮੁਨਾਫਾ", # Punjabi
        r"गारंटीड\s*मुनाफा", # Hindi
    ]
]

_WITHDRAWAL_BLOCKED_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:withdrawal|withdraw|payout)\s*(?:is\s*)?(?:blocked|frozen|suspended|pending|failed|locked|withheld)",
        r"(?:pay|deposit|transfer|settle)\s*(?:a\s*|the\s*|\d+%\s*)?(?:tax|tds|gst|fee|charge|penalty|clearing|bond|fine|clearance)\s*(?:to|for|before|unless|of)\s*" + _AMT,
        r"unfreeze\s*(?:your\s*)?(?:fee|charge|amount|deposit|funds|account|wallet|balance)",
        r"(?:tax|tds|gst)\s*(?:clearance|deduction|charge|fee|payment).*(?:withdraw|release|unfreeze)",
        r"(?:account|wallet|balance)\s*(?:frozen|blocked|locked|suspended)",
        r"(?:data\s*fix|system\s*error|error\s*code|credit\s*score).*(?:fee|charge|recharge|deposit)",
        r"verification\s*bond\s*(?:of)?\s*" + _AMT,
        r"(?:anti[\s\-]?money\s*laundering|aml)\s*(?:audit|regulations|hold)?",
        r"(?:ਨਿਕਾਸੀ.*ਰੋਕ|ਕਲੀਅਰੈਂਸ\s*ਫੀਸ|ਟੈਕਸ\s*ਬਕਾਇਆ)", # Punjabi
        r"निकासी\s*(?:रोक|फ्रीज|ब्लॉक)", # Hindi
    ]
]

_SMALL_PAYOUT_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:trial|welcome|joining|registration)\s*(?:bonus|incentive|task|payout).*" + _AMT,
        r"(?:₹|rs\.?|inr)?\s*(?:100|150|200|250|300|500)\s*(?:credited|transferred|sent|received|earned)",
        r"(?:received|got|credited)\s*(?:₹|rs\.?|inr)?\s*(?:100|150|200|250|300|500)",
        r"(?:mil\s*gaye|a\s*gaye|mil\s*gaya)\s*(?:hain)?.*(?:₹|rs\.?)",
        r"ਮਿਲ\s*ਗਏ", # Punjabi
    ]
]

_ACCOUNT_RENTAL_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:share|send|provide)\s*(?:your)?\s*(?:otp|one[\s\-]?time[\s\-]?password)",
        r"(?:rent|lend|use)\s*(?:your)?\s*(?:bank\s*account|current\s*account|saving\s*account)",
        r"(?:atm|debit\s*card)\s*(?:pin|cvv)",
    ]
]

_MOVE_PRIVATE_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:telegram|whatsapp)\s*(?:group|channel|mentor|receptionist|manager|officer|desk)",
        r"(?<![a-zA-Z0-9._%+-])@([A-Za-z0-9_]{4,32})\b(?!\.[a-zA-Z]{2,})",
        r"(?:add|contact|message)\s*(?:our)?\s*(?:receptionist|mentor|admin|supervisor)\s*on\s*telegram",
        r"t\.me\/[A-Za-z0-9_]+",
        r"ਟੈਲੀਗ੍ਰਾਮ", # Punjabi
        r"टेलीग्राम", # Hindi
    ]
]

_TOO_GOOD_PAY_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:earn|salary|daily|income)[:\s]*(?:rs\.?|₹|inr)?\s*[\d,]+\s*(?:to\s*(?:rs\.?|₹|inr)?\s*[\d,]+)?\s*(?:daily|per\s*day|per\s*hour|a\s*day|weekly)",
        r"(?:like|liking|subscribe|subscribing|watch|watching)\s*(?:youtube|videos?|channels?)",
        r"(?:hotel|restaurant|product|google\s*maps?)\s*(?:review|rating|5\s*star)",
        r"(?:data\s*entry|typing\s*work).*(?:rs\.?|₹|inr)?\s*[\d,]+",
        r"order\s*(?:ranking|simulation|rating)",
        r"ਰੋਜ਼ਾਨਾ\s*₹[\d,]+", # Punjabi
        r"ਦੈਨਿਕ\s*₹[\d,]+", # Punjabi
        r"daily\s*[\d,]+.*(?:kamayein|kamaye|kamao)", # Hinglish
        r"ਘਰ\s*ਬੈਠੇ.*ਕਮਾਓ", # Punjabi
        r"घर\s*बैठे.*कमाएं", # Hindi
    ]
]

_FREE_MAIL_HR_RE = re.compile(
    r"\b(?:[a-zA-Z0-9_.+\-]*(?:hr|careers?|recruit|talent|jobs?|apply|contact|info|hiring|infra|typist|aai|desk)[a-zA-Z0-9_.+\-]*)@(gmail\.com|yahoo\.com|yahoo\.co\.in|hotmail\.com|outlook\.com|rediffmail\.com|protonmail\.com)\b",
    re.IGNORECASE,
)

_NO_INTERVIEW_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:no|without)\s*(?:skill|experience|interview|test|exam|assessment)",
        r"no\s*written\s*exam",
        r"direct\s*(?:joining|selection|hiring)\s*(?:on\s*merit|without\s*exam)",
        r"ਕੋਈ\s*ਇੰਟਰਵਿਊ\s*ਨਹੀਂ", # Punjabi
        r"बिना\s*(?:किसी\s*)?इंटरव्यू", # Hindi
    ]
]

_URGENCY_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:hurry|urgent\s*requirement|right\s*now|last\s*chance|only\s*\d+\s*slots?\s*left|within\s*\d+\s*(?:hours?|minutes?)|failure\s*to\s*pay\s*within|immediately\s*(?:pay|deposit|transfer|send)|urgent\s*joining)",
    ]
]

_GENUINE_PROCESS_PATS = [
    re.compile(p, re.I)
    for p in [
        r"(?:does\s*not|never)\s*(?:charge|request|ask|collect)\s*(?:any)?\s*(?:fee|deposit|money)",
        r"no\s*fee\s*(?:is\s*charged|of\s*any\s*kind|charged|required)",
        r"merit[\s\-]?based",
        r"(?:technical|in[\s\-]?person|hr)\s*interview",
        r"(?:campus\s*recruitment|placement\s*cell|campus\s*drive)",
        r"(?:preliminary|main)\s*examination",
        r"valid\s*gate\s*score",
        r"company\s*laptop\s*and\s*headset\s*upon\s*selection",
        r"no\s*upfront\s*cash\s*deposit",
        r"adjusted\s*from\s*(?:your)?\s*weekly\s*delivery\s*earnings",
        r"\b(?:github|wellfound|angellist|peak\s*xv|esops|backend\s*engineer|cto)\b",
        r"\b(?:portfolio|figma\s*design|freelance\s*contract|sample\s*landing\s*page)\b",
        r"\b(?:delivery\s*partner|delivery\s*fleet|kyc\s*verification|local\s*delivery\s*hub)\b",
        r"(?:ਰੈਜ਼ਿਊਮੇ|ਇੰਟਰਵਿਊ|ਤਨਖਾਹ|ਆਫਰ\s*ਲੈਟਰ)", # Punjabi resume / interview
        r"(?:interview\s*reschedule|second\s*technical\s*round|calendar\s*invite)",
        r"(?:compensation|careers\s*page|exploratory\s*chat|internshala|devcommunity|deloitte|successfactors|fellowship|ctc|stipend|notice\s*period|easy\s*apply|teams|webex)",
        r"ਕੋਈ\s*ਰਜਿਸਟ੍ਰੇਸ਼ਨ\s*ਫੀਸ\s*ਨਹੀਂ", # Punjabi
        r"आवेदन\s*शुल्क:\s*शून्य", # Hindi
        r"\b(?:provident\s*fund|health\s*insurance|life\s*insurance|cell\s*phone\s*reimbursement|gratuity)\b",
        r"\b(?:permanent,\s*full[\s\-]?time|full[\s\-]?time|key\s*responsibilities|job\s*description|store\s*manager)\b",
        r"\b(?:indeed\.com|naukri\.com|linkedin\.com\/jobs|glassdoor\.com)\b",
    ]
]

_BRAND_IMPERSONATION_PATS = [
    re.compile(p, re.I)
    for p in [
        r"\b(?:amaz0n|amzon|amaazon|amazn)\b",
        r"\b(?:fl1pkart|flipkrt|flpkart|filpkart)\b",
        r"\b(?:g00gle|googel|gogle)\b",
        r"\b(?:micr0soft|microsft|mircosoft)\b",
        r"\b(?:tcs[\s\-]?official|tcs[\s\-]?career|careers\.tcs@gmail\.com)\b",
        r"\b(?:inf0sys|infoys|infosyss)\b",
        r"\b(?:paytmm|paytm[\s\-]?task)\b",
        r"\b(?:z0mat0|zomto|zomatoo)\b",
        r"tata\s*consultancy\s*services\s*\(impersonated\)",
    ]
]

_NEGATION_BEFORE_PATS = [
    re.compile(r"\b(?:does\s*not|doesn't|do\s*not|don't|never|without\s*any|zero\s*fee|free\s*of\s*cost|beware\s*of|not\s*charge|free\s*joining|koi\s*bhi|koi)\b|(?:ਕੋਈ|ਬਿਨਾਂ|ਬਿਨਾ|ਨਹੀਂ)", re.I),
    re.compile(r"\bno\s+(?:upfront\s*)?(?:cash\s*)?(?:fee|charge|deposit|investment|money|exam|interview|registration)\b", re.I),
]

_NEGATION_AFTER_PATS = [
    re.compile(r"\b(?:toh\s*nahi|to\s*nahi|nahi\s*hai|nahi\s*lagegi|not\s*required|not\s*charged|is\s*free|zero|exempt|not\s*collected)\b", re.I),
    re.compile(r"\b(?:adjusted\s*from\s*(?:your)?\s*(?:weekly|monthly)?\s*(?:delivery\s*)?(?:earnings|payouts|salary)|ਨਹੀਂ)\b", re.I),
    re.compile(r"\b(?:per\s*(?:year|annum|month|week|day|hour)|a\s*(?:year|annum|month|week|day)|p\.a\.?|p\.m\.?|lpa|ctc|annually|monthly|yearly)\b", re.I),
]


def _is_negated(text: str, start_idx: int, end_idx: int = -1) -> bool:
    window_before = text[max(0, start_idx - 60):start_idx]
    if any(p.search(window_before) for p in _NEGATION_BEFORE_PATS):
        return True
    if end_idx != -1:
        window_after = text[end_idx:min(len(text), end_idx + 100)]
        if any(p.search(window_after) for p in _NEGATION_AFTER_PATS):
            return True
    return False


def _find_first_match(
    patterns: list[re.Pattern],
    messages: list[dict],
    check_negation: bool = False,
) -> tuple[str, int | None]:
    for idx, msg in enumerate(messages):
        text = msg.get("text", "")
        for pat in patterns:
            for m in pat.finditer(text):
                if check_negation and _is_negated(text, m.start(), m.end()):
                    continue
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                return text[start:end].strip(), idx
    return "", None


def _find_all_matches(
    patterns: list[re.Pattern],
    messages: list[dict],
    check_negation: bool = False,
) -> list[tuple[str, int]]:
    results = []
    for idx, msg in enumerate(messages):
        text = msg.get("text", "")
        for pat in patterns:
            for m in pat.finditer(text):
                if check_negation and _is_negated(text, m.start(), m.end()):
                    continue
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                results.append((text[start:end].strip(), idx))
                break
    return results


def detect_signals(messages: list[dict]) -> list[Signal]:
    signals: list[Signal] = []
    full_text = " ".join(m.get("text", "") for m in messages)

    # 1. UPFRONT_DEPOSIT (+40)
    ev, idx = _find_first_match(_UPFRONT_DEPOSIT_PATS, messages, check_negation=True)
    if ev:
        signals.append(Signal(id="UPFRONT_DEPOSIT", weight=40, evidence=ev, message_index=idx))

    # 2. PREPAID_RETURN (+40)
    ev, idx = _find_first_match(_PREPAID_RETURN_PATS, messages, check_negation=True)
    if ev:
        signals.append(Signal(id="PREPAID_RETURN", weight=40, evidence=ev, message_index=idx))

    # 3. WITHDRAWAL_BLOCKED_FEE (+40)
    ev, idx = _find_first_match(_WITHDRAWAL_BLOCKED_PATS, messages)
    if ev:
        signals.append(Signal(id="WITHDRAWAL_BLOCKED_FEE", weight=40, evidence=ev, message_index=idx))

    # 4. SMALL_PAYOUT_THEN_ESCALATE (+25)
    ev, idx = _find_first_match(_SMALL_PAYOUT_PATS, messages)
    if ev:
        signals.append(Signal(id="SMALL_PAYOUT_THEN_ESCALATE", weight=25, evidence=ev, message_index=idx))

    # 5. ACCOUNT_RENTAL_OR_OTP (+30)
    ev, idx = _find_first_match(_ACCOUNT_RENTAL_PATS, messages)
    if ev:
        signals.append(Signal(id="ACCOUNT_RENTAL_OR_OTP", weight=30, evidence=ev, message_index=idx))

    # 6. MOVE_TO_PRIVATE_CHAT (+15)
    ev, idx = _find_first_match(_MOVE_PRIVATE_PATS, messages)
    if ev:
        signals.append(Signal(id="MOVE_TO_PRIVATE_CHAT", weight=15, evidence=ev, message_index=idx))

    # 7. TOO_GOOD_PAY (+15)
    ev, idx = _find_first_match(_TOO_GOOD_PAY_PATS, messages)
    if ev:
        signals.append(Signal(id="TOO_GOOD_PAY", weight=15, evidence=ev, message_index=idx))

    # 8. FREE_MAIL_HR (+15)
    m = _FREE_MAIL_HR_RE.search(full_text)
    if m:
        signals.append(Signal(id="FREE_MAIL_HR", weight=15, evidence=m.group(0), message_index=None))

    # 9. NO_INTERVIEW_INSTANT_OFFER (+10)
    ev, idx = _find_first_match(_NO_INTERVIEW_PATS, messages)
    if ev:
        signals.append(Signal(id="NO_INTERVIEW_INSTANT_OFFER", weight=10, evidence=ev, message_index=idx))

    # 10. URGENCY_PRESSURE (+10)
    ev, idx = _find_first_match(_URGENCY_PATS, messages)
    if ev:
        signals.append(Signal(id="URGENCY_PRESSURE", weight=10, evidence=ev, message_index=idx))

    # 11. BRAND_IMPERSONATION (+25)
    ev, idx = _find_first_match(_BRAND_IMPERSONATION_PATS, messages)
    if ev:
        signals.append(Signal(id="BRAND_IMPERSONATION", weight=25, evidence=ev, message_index=idx))

    # 12. GENUINE_SIGNALS (negative weights)
    genuine_matches = _find_all_matches(_GENUINE_PROCESS_PATS, messages, check_negation=True)
    if genuine_matches:
        signals.append(Signal(
            id="GENUINE_SIGNALS",
            weight=-30 if len(genuine_matches) >= 2 else -20,
            evidence="; ".join(e for e, _ in genuine_matches[:3]),
            message_index=genuine_matches[0][1],
        ))

    return signals


def compute_rules_score(signals: list[Signal]) -> int:
    raw = sum(s.weight for s in signals)
    return max(0, min(100, raw))


def get_payment_signal_count(signals: list[Signal]) -> int:
    payment_ids = {
        "UPFRONT_DEPOSIT",
        "PREPAID_RETURN",
        "WITHDRAWAL_BLOCKED_FEE",
        "ACCOUNT_RENTAL_OR_OTP",
    }
    return sum(1 for s in signals if s.id in payment_ids)


def detect_all_signals(data) -> list[Signal]:
    if isinstance(data, str):
        lines = [line.strip() for line in data.split("\n") if line.strip()]
        msgs = [{"text": l, "sender": "Unknown"} for l in lines] if lines else [{"text": data, "sender": "Unknown"}]
        return detect_signals(msgs)
    elif isinstance(data, list):
        msgs = []
        for item in data:
            if hasattr(item, "text"):
                msgs.append({"text": item.text, "sender": getattr(item, "sender", "Unknown")})
            elif isinstance(item, dict):
                msgs.append(item)
            else:
                msgs.append({"text": str(item), "sender": "Unknown"})
        return detect_signals(msgs)
    return []
