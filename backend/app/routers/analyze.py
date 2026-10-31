"""FastAPI router for /api/analyze endpoints."""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, RawTextAnalyzeRequest, Language
from app.services.analyzer import get_analyzer
from app.modules.conversation_intelligence import extract_text_from_upload

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_offer(req: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze chat messages or raw text for task scam patterns, stages, and company claims."""
    analyzer = get_analyzer()
    try:
        return analyzer.analyze(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")


@router.post("/analyze/raw", response_model=AnalyzeResponse)
async def analyze_raw_text(req: RawTextAnalyzeRequest) -> AnalyzeResponse:
    """Direct raw text analysis (WhatsApp exports, SMS, job posts)."""
    analyzer = get_analyzer()
    norm_req = AnalyzeRequest(
        raw_text=req.raw_text,
        language=req.language,
        context=req.context,
    )
    return analyzer.analyze(norm_req)


@router.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_uploaded_document(
    file: UploadFile = File(...),
    language: Language = Form(Language.EN),
    context: Optional[str] = Form(None),
) -> AnalyzeResponse:
    """Analyze an uploaded document (PDF offer letter, text log, or chat export)."""
    try:
        content_bytes = await file.read()
        extracted_text = extract_text_from_upload(file.filename or "upload.txt", content_bytes)
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400, 
                detail="No readable text found in document. If this PDF contains scanned images or screenshots, please use the OfferGuard AI web interface which performs in-browser OCR on PDF images."
            )
        
        analyzer = get_analyzer()
        req = AnalyzeRequest(
            raw_text=extracted_text,
            language=language,
            context=context or f"Uploaded file: {file.filename}",
        )
        return analyzer.analyze(req)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document extraction error: {str(e)}")
