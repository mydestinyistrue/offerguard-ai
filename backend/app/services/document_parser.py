"""Document & Image text extraction service (OCR and PDF parsing).

Supports:
- PDF Offer Letters (via PyMuPDF / fitz)
- Plain text / chat logs (.txt, .log, .json)
"""

from __future__ import annotations

import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Check PyMuPDF
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    try:
        import pymupdf as fitz
        HAS_PYMUPDF = True
    except ImportError:
        HAS_PYMUPDF = False


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text content from all pages of a PDF document."""
    if not HAS_PYMUPDF:
        raise RuntimeError("PyMuPDF (fitz) is not installed for PDF parsing.")
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_parts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        t = page.get_text("text")
        if t.strip():
            text_parts.append(t.strip())
    
    return "\n\n".join(text_parts)


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    """Extract plain text from uploaded file based on its extension."""
    fn_lower = filename.lower()
    
    # 1. Plain text / chat logs
    if fn_lower.endswith((".txt", ".log", ".json", ".chat")):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1", errors="replace")

    # 2. PDF documents
    if fn_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    # 3. Default fallback: try utf-8 text
    try:
        return file_bytes.decode("utf-8")
    except Exception:
        raise ValueError(
            f"File format for '{filename}' requires client-side OCR. Please upload screenshots through the web interface."
        )
