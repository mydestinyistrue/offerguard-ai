"""PII masking service – detects and redacts Indian PII from text.

Supports:
  - Indian mobile numbers (+91 / 0-prefixed 10-digit)
  - Aadhaar numbers (12-digit with optional spaces/dashes)
  - UPI IDs (xxx@upi / xxx@ybl / etc.)
  - Bank account numbers (9-18 digit sequences)
  - Email addresses
  - PAN card numbers
  - IFSC codes
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field


# ── Patterns ──────────────────────────────────────────────────────────

# Indian mobile: +91-XXXXXXXXXX, 91XXXXXXXXXX, 0XXXXXXXXXX, or plain 10-digit
_PHONE_RE = re.compile(
    r"""
    (?<!\d)                           # no digit before
    (?:\+91[\s\-]?|91[\s\-]?|0)?      # optional country/trunk prefix
    [6-9]\d{9}                        # 10-digit Indian mobile
    (?!\d)                            # no digit after
    """,
    re.VERBOSE,
)

# Aadhaar: 12 digits, optionally grouped as 4-4-4 with spaces or dashes
_AADHAAR_RE = re.compile(
    r"""
    (?<!\d)
    [2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}
    (?!\d)
    """,
    re.VERBOSE,
)

# UPI ID: alphanumeric.dots@provider
_UPI_RE = re.compile(
    r"[a-zA-Z0-9._\-]+@(?:upi|ybl|okhdfcbank|okaxis|oksbi|okicici|paytm|apl|"
    r"ibl|axl|sbi|hdfcbank|icici|kotak|indus|federal|rbl|yes|boi|cbi|pnb|"
    r"unionbank|canara|bob|dbs|idbi|indian|jkb|karb|kvb|mahb|scb|tjsb|uco|"
    r"united|fino|airtel|jio|freecharge|slice|jupiter|cred|gpay|phonepe)",
    re.IGNORECASE,
)

# Email
_EMAIL_RE = re.compile(
    r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}",
)

# PAN: AAAAA9999A
_PAN_RE = re.compile(r"(?<![A-Z])[A-Z]{5}\d{4}[A-Z](?![A-Z])")

# IFSC: 4 letters + 0 + 6 alphanumeric
_IFSC_RE = re.compile(r"(?<![A-Z0-9])[A-Z]{4}0[A-Z0-9]{6}(?![A-Z0-9])")

# Bank account numbers: 9-18 digit sequences (after removing obvious non-account patterns)
_BANK_ACCT_RE = re.compile(r"(?<!\d)\d{9,18}(?!\d)")


@dataclass
class MaskResult:
    masked_text: str
    pii_types: list[str] = field(default_factory=list)
    original_hash: str | None = None

    @property
    def pii_found(self) -> list[str]:
        return self.pii_types


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def mask_pii(text: str, *, compute_hash: bool = False) -> MaskResult:
    """Mask all detected PII in *text* and return the result."""
    pii_types: list[str] = []
    masked = text

    # Order matters – mask more specific patterns first to avoid partial matches.

    # UPI IDs
    if _UPI_RE.search(masked):
        masked = _UPI_RE.sub("[UPI_REDACTED]", masked)
        pii_types.append("upi_id")

    # Emails (before phone, as emails contain digits)
    if _EMAIL_RE.search(masked):
        masked = _EMAIL_RE.sub("[EMAIL_REDACTED]", masked)
        pii_types.append("email")

    # PAN
    if _PAN_RE.search(masked):
        masked = _PAN_RE.sub("[PAN_REDACTED]", masked)
        pii_types.append("pan")

    # IFSC
    if _IFSC_RE.search(masked):
        masked = _IFSC_RE.sub("[IFSC_REDACTED]", masked)
        pii_types.append("ifsc")

    # Phone numbers
    if _PHONE_RE.search(masked):
        masked = _PHONE_RE.sub("[PHONE_REDACTED]", masked)
        pii_types.append("phone")

    # Aadhaar (after phone to avoid double-masking)
    if _AADHAAR_RE.search(masked):
        masked = _AADHAAR_RE.sub("[AADHAAR_REDACTED]", masked)
        pii_types.append("aadhaar")

    # Bank account numbers – only match remaining long digit sequences
    # Avoid matching things that were already redacted or are clearly not accounts
    remaining_long_digits = _BANK_ACCT_RE.findall(masked)
    for seq in remaining_long_digits:
        # Skip if it looks like a timestamp or year-like number
        if len(seq) <= 10 and seq.startswith(("19", "20")):
            continue
        masked = masked.replace(seq, "[BANK_ACCT_REDACTED]", 1)
        if "bank_account" not in pii_types:
            pii_types.append("bank_account")

    return MaskResult(
        masked_text=masked,
        pii_types=pii_types,
        original_hash=_hash_text(text) if compute_hash else None,
    )


def mask_messages(messages: list[dict]) -> tuple[list[dict], list[str]]:
    """Mask PII across a list of message dicts. Returns (masked_messages, all_pii_types)."""
    all_pii: set[str] = set()
    masked_msgs: list[dict] = []
    for msg in messages:
        result = mask_pii(msg.get("text", ""))
        all_pii.update(result.pii_types)
        masked_msgs.append({**msg, "text": result.masked_text})
    return masked_msgs, sorted(all_pii)
