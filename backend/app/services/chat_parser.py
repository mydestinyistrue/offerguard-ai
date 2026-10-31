"""Chat conversation parser for WhatsApp, Telegram, and raw text formats.

Converts unstructured input or export logs into a structured list of MessageItem objects.
"""

from __future__ import annotations

import re
from typing import Optional
from app.models.schemas import MessageItem


# WhatsApp format 1: [30/10/2026, 10:15:00 AM] +91 98765 43210: message
_WA_P1 = re.compile(
    r"^\[?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?\s*(?:[AP]M)?)\]?\s*[-~]?\s*([^:]+?):\s*(.*)$",
    re.IGNORECASE | re.MULTILINE
)

# WhatsApp format 2: 30/10/26, 10:15 am - Sender: message
_WA_P2 = re.compile(
    r"^(\d{1,2}[/-]\d{1,2}[/-]\d{2,4},?\s+\d{1,2}:\d{2}\s*(?:[ap]m)?)\s*-\s*([^:]+?):\s*(.*)$",
    re.IGNORECASE | re.MULTILINE
)

# Telegram format: @Username: message or Name: message
_TG_P = re.compile(
    r"^(@?[A-Za-z0-9_\s+]{2,30}?):\s*(.*)$",
    re.MULTILINE
)


def parse_chat_text(raw_text: str) -> list[MessageItem]:
    """Parse raw text into an ordered list of MessageItem objects."""
    if not raw_text or not raw_text.strip():
        return []

    text = raw_text.strip()
    messages: list[MessageItem] = []

    # Try WhatsApp P1
    lines = text.split("\n")
    current_msg: Optional[MessageItem] = None

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        m1 = _WA_P1.match(line_clean)
        if m1:
            if current_msg:
                messages.append(current_msg)
            ts, sender, body = m1.groups()
            current_msg = MessageItem(sender=sender.strip(), text=body.strip(), timestamp=ts.strip())
            continue

        m2 = _WA_P2.match(line_clean)
        if m2:
            if current_msg:
                messages.append(current_msg)
            ts, sender, body = m2.groups()
            current_msg = MessageItem(sender=sender.strip(), text=body.strip(), timestamp=ts.strip())
            continue

        # Check if line starts with Sender: message
        m3 = _TG_P.match(line_clean)
        if m3 and not line_clean.lower().startswith(("http", "ref:", "subject:", "note:", "sub:", "terms:")):
            sender, body = m3.groups()
            # If sender looks like a plausible sender name
            if len(sender.split()) <= 4:
                if current_msg:
                    messages.append(current_msg)
                current_msg = MessageItem(sender=sender.strip(), text=body.strip(), timestamp=None)
                continue

        # If continuation of existing message
        if current_msg:
            current_msg.text += " " + line_clean
        else:
            # First line without explicit sender format
            current_msg = MessageItem(sender="Unknown", text=line_clean, timestamp=None)

    if current_msg:
        messages.append(current_msg)

    # If no messages were extracted or only 1 generic block, split paragraphs
    if not messages:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if paragraphs:
            for idx, p in enumerate(paragraphs):
                messages.append(MessageItem(sender=f"Speaker_{idx%2 + 1}", text=p))
        else:
            messages.append(MessageItem(sender="Sender", text=text))

    return messages
