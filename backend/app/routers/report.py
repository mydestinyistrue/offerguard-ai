"""FastAPI router for /api/report endpoints."""

from __future__ import annotations

from fastapi import APIRouter
from app.models.schemas import ReportRequest, ReportResponse, MessageItem
from app.modules.conversation_intelligence import parse_chat_text
from app.modules.victim_protection import generate_complaint_pack

router = APIRouter(prefix="/api", tags=["Reporting"])


@router.post("/report", response_model=ReportResponse)
async def create_complaint_report(req: ReportRequest) -> ReportResponse:
    """Generate a formal 1930 Cybercrime complaint pack from conversation evidence."""
    messages = req.messages or []
    raw = req.text or req.raw_text or ""
    if not messages and raw:
        messages = parse_chat_text(raw)
    if not messages:
        messages = [MessageItem(sender="Victim", text=raw or "No chat log supplied.")]

    return generate_complaint_pack(
        messages=messages,
        victim_name=req.victim_name,
        victim_phone=req.victim_phone,
        amount_lost=req.amount_lost,
        language=req.language,
    )
