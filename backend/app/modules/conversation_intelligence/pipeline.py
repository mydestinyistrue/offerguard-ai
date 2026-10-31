"""Standalone pipeline for Conversation Intelligence.

Provides unified chat parsing, Indian PII redaction, and PDF/document extraction.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

from .chat_parser import parse_chat_text, MessageItem
from .pii_masker import mask_pii, MaskResult
from .document_parser import extract_text_from_pdf, extract_text_from_upload


@dataclass
class ConversationPayload:
    """Structured representation of parsed conversation and redacted PII."""
    raw_text: str
    masked_text: str
    messages: List[Dict[str, Any]]
    pii_found: List[str]
    message_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConversationIntelligence:
    """Unified Conversation Intelligence interface."""

    @staticmethod
    def parse_chat(text: str) -> List[MessageItem]:
        """Parse raw multi-turn WhatsApp, Telegram, or plaintext exports."""
        return parse_chat_text(text)

    @staticmethod
    def mask_pii(text: str) -> MaskResult:
        """Mask Indian PII (mobile numbers, Aadhaar, PAN, UPI IDs, emails, bank accounts)."""
        return mask_pii(text)

    @staticmethod
    def extract_pdf(pdf_bytes: bytes) -> str:
        """Extract plain text from PDF documents using PyMuPDF."""
        return extract_text_from_pdf(pdf_bytes)

    def process(self, raw_text: str) -> ConversationPayload:
        """Parse conversation, extract turns, and mask sensitive PII in one call."""
        messages = parse_chat_text(raw_text)
        pii = mask_pii(raw_text)
        
        msg_list = [
            {
                "sender": getattr(m, "sender", "Unknown"),
                "text": getattr(m, "text", ""),
                "timestamp": getattr(m, "timestamp", None),
                "message_index": getattr(m, "message_index", None),
            }
            for m in messages
        ]

        return ConversationPayload(
            raw_text=raw_text,
            masked_text=pii.masked_text,
            messages=msg_list,
            pii_found=pii.pii_found,
            message_count=len(msg_list),
        )
