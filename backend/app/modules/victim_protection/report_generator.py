"""Report generator service for India's 1930 cybercrime helpline & portal.

Generates a structured, evidence-backed complaint pack ready to be submitted
to cybercrime.gov.in or provided during a 1930 helpline phone call.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

try:
    from app.models.schemas import MessageItem, ReportRequest, ReportResponse, Verdict, Language
except ImportError:
    from dataclasses import dataclass
    from enum import Enum
    class Language(str, Enum):  # type: ignore[no-redef]
        EN = "en"
        HI = "hi"
        PA = "pa"
    class Verdict(str, Enum):  # type: ignore[no-redef]
        SCAM = "SCAM"
        SUSPICIOUS = "SUSPICIOUS"
        LIKELY_GENUINE = "LIKELY_GENUINE"
        UNSURE = "UNSURE"
    @dataclass
    class MessageItem:  # type: ignore[no-redef]
        sender: str
        text: str
        timestamp: Optional[str] = None
        message_index: Optional[int] = None
    @dataclass
    class ReportResponse:  # type: ignore[no-redef]
        report_text: str
        suggested_helpline: str = "1930"
        summary: str = ""
        evidence_count: int = 0

        def to_dict(self):
            from dataclasses import asdict
            return asdict(self)


_UPI_PATTERN = re.compile(r"\b[a-zA-Z0-9._\-]+@(?:upi|ybl|okhdfcbank|okaxis|oksbi|okicici|paytm|apl|sbi|icici|axis|hdfcbank|kotak|axl|ibl)\b", re.I)
_PHONE_PATTERN = re.compile(r"(?:\+91[\s\-]?)?[6-9]\d{9}\b")
_TELEGRAM_HANDLE = re.compile(r"@[A-Za-z0-9_]{4,32}\b")
_AMOUNT_PATTERN = re.compile(r"(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d{2})?)", re.I)


def extract_incident_artifacts(text: str) -> dict:
    """Extract suspect UPI IDs, phone numbers, handles, and amounts from text."""
    upis = list(set(_UPI_PATTERN.findall(text)))
    phones = list(set(_PHONE_PATTERN.findall(text)))
    handles = list(set(_TELEGRAM_HANDLE.findall(text)))
    
    amounts = []
    for match in _AMOUNT_PATTERN.finditer(text):
        raw_amt = match.group(1).replace(",", "")
        try:
            val = float(raw_amt)
            if 50 <= val <= 10000000:
                amounts.append(val)
        except ValueError:
            pass

    return {
        "upis": upis,
        "phones": phones,
        "handles": handles,
        "amounts": sorted(list(set(amounts))),
    }


def generate_complaint_pack(
    messages: list[MessageItem],
    victim_name: Optional[str] = None,
    victim_phone: Optional[str] = None,
    amount_lost: Optional[float] = None,
    language: Language = Language.EN,
) -> ReportResponse:
    """Compile a complete 1930 Cybercrime complaint pack."""
    def _msg_str(m):
        sender = getattr(m, "sender", None) or (m.get("sender") if isinstance(m, dict) else "Unknown")
        text = getattr(m, "text", None) or (m.get("text") if isinstance(m, dict) else str(m))
        return f"{sender}: {text}"
    full_text = "\n".join([_msg_str(m) for m in messages])
    artifacts = extract_incident_artifacts(full_text)

    # Estimate amount if not supplied
    total_amount = amount_lost
    if total_amount is None and artifacts["amounts"]:
        total_amount = max(artifacts["amounts"])

    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format suspects section
    suspect_info = []
    if artifacts["phones"]:
        suspect_info.append(f"• Suspect Phone Number(s): {', '.join(artifacts['phones'])}")
    if artifacts["upis"]:
        suspect_info.append(f"• Suspect UPI ID(s) / Receiver Accounts: {', '.join(artifacts['upis'])}")
    if artifacts["handles"]:
        suspect_info.append(f"• Suspect Telegram / Social Handles: {', '.join(artifacts['handles'])}")
    if not suspect_info:
        suspect_info.append("• Suspect Identifiers: See enclosed conversation log")

    suspects_block = "\n".join(suspect_info)

    # Format timeline / conversation excerpt
    def _line_fmt(i, m):
        t = getattr(m, 'timestamp', None) or (m.get('timestamp') if isinstance(m, dict) else None) or f"Step {i+1}"
        s = getattr(m, 'sender', None) or (m.get('sender') if isinstance(m, dict) else "Unknown")
        txt = getattr(m, 'text', None) or (m.get('text') if isinstance(m, dict) else str(m))
        return f"[{t}] {s}: {txt}"
    chat_excerpt = "\n".join([_line_fmt(i, m) for i, m in enumerate(messages[:15])])

    report_text = f"""================================================================================
CRIMINAL COMPLAINT DRAFT — FINANCIAL CYBER FRAUD (TASK / JOB SCAM)
GENERATED VIA TASKGUARD · FOR SUBMISSION TO HELPLINE 1930 & CYBERCRIME.GOV.IN
================================================================================
DATE & TIME: {timestamp_str}
INCIDENT CATEGORY: Financial Fraud -> Online Task / Part-Time Job Scam
REPORTING HELPLINE: 1930 (National Cyber Crime Reporting Helpline)
PORTAL: https://cybercrime.gov.in

1. COMPLAINANT PARTICULARS
--------------------------------------------------------------------------------
Complainant Name: {victim_name or '[Enter Your Full Name]'}
Contact Phone Number: {victim_phone or '[Enter Your 10-Digit Mobile Number]'}
Total Financial Loss Claimed: ₹{f"{total_amount:,.2f}" if total_amount is not None else "[Enter Exact Rupee Amount Lost]"}

2. SUSPECT DETAILS IDENTIFIED
--------------------------------------------------------------------------------
{suspects_block}

3. INCIDENT DESCRIPTION (BRIEF SUMMARY)
--------------------------------------------------------------------------------
The complainant was approached by unknown individuals offering remote part-time employment / tasks (e.g. video liking, ratings, merchant tasks). 
After initiating basic tasks, the perpetrators induced the victim to deposit funds into specified merchant/personal accounts under the guise of 'prepaid tasks', 'security deposit', or 'VIP tier'.
Subsequently, withdrawals were withheld citing 'tax', 'unfreeze fee', or 'system error', resulting in unauthorized financial misappropriation.

4. CHAT LOG EXCERPT & EVIDENCE TRAIL
--------------------------------------------------------------------------------
{chat_excerpt}

5. REQUESTED POLICE / CYBER CELL ACTION
--------------------------------------------------------------------------------
1. Immediate lien / freeze request on suspect receiver UPI / Bank Accounts under Section 102 CrPC.
2. IP and subscriber identification data (CDR/SDR) from Telegram and telecom service providers.
3. Registration of FIR under relevant sections of the Bharatiya Nyaya Sanhita (BNS) / IPC Section 420 (Cheating) and Section 66D of the Information Technology Act.

================================================================================
Generated by TaskGuard — Keep your transaction UTR numbers and screenshots ready.
================================================================================
"""

    summary = f"Task scam complaint drafted for ₹{total_amount:,.0f} lost across {len(messages)} recorded messages." if total_amount else f"Task scam complaint drafted across {len(messages)} recorded messages."

    return ReportResponse(
        report_text=report_text,
        suggested_helpline="1930",
        summary=summary,
        evidence_count=len(artifacts["upis"]) + len(artifacts["phones"]) + len(artifacts["handles"]),
    )


class VictimProtectionService:
    """Standalone Victim Protection Service for India 1930 reporting and guidance."""

    @staticmethod
    def generate_complaint_pack(
        messages: Optional[list] = None,
        text: Optional[str] = None,
        victim_name: Optional[str] = None,
        victim_phone: Optional[str] = None,
        amount_lost: Optional[float] = None,
        language: str = "en",
    ) -> ReportResponse:
        if messages is None:
            if text:
                messages = [MessageItem(sender="Suspect", text=text)]
            else:
                messages = []
        elif messages and isinstance(messages[0], dict):
            messages = [
                MessageItem(
                    sender=m.get("sender", "Unknown"),
                    text=m.get("text", ""),
                    timestamp=m.get("timestamp"),
                    message_index=m.get("message_index"),
                )
                for m in messages
            ]
        lang_enum = Language.EN
        try:
            lang_enum = Language(language)
        except Exception:
            pass

        return generate_complaint_pack(
            messages=messages,
            victim_name=victim_name,
            victim_phone=victim_phone,
            amount_lost=amount_lost,
            language=lang_enum,
        )


ReportGenerator = VictimProtectionService

