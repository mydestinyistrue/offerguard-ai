"""Module 3: Conversation Intelligence.
Function: Understand multiple messages together.

Parses multi-turn WhatsApp/Telegram dialogues, extracts text from PDFs/documents,
and redacts sensitive Indian PII. Fully self-contained for external use.
"""

from .pipeline import ConversationIntelligence, ConversationPayload
ConversationPipeline = ConversationIntelligence
from .chat_parser import parse_chat_text, MessageItem
from .document_parser import extract_text_from_upload, extract_text_from_pdf
from .pii_masker import mask_pii, MaskResult

__all__ = [
    "ConversationIntelligence",
    "ConversationPipeline",
    "ConversationPayload",
    "parse_chat_text",
    "MessageItem",
    "extract_text_from_upload",
    "extract_text_from_pdf",
    "mask_pii",
    "MaskResult",
]
