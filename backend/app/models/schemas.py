"""Pydantic models for request / response schemas."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ─────────────────────────────────────────────────────────────
class Verdict(str, Enum):
    SCAM = "SCAM"
    SUSPICIOUS = "SUSPICIOUS"
    LIKELY_GENUINE = "LIKELY_GENUINE"
    UNSURE = "UNSURE"


class Language(str, Enum):
    EN = "en"
    HI = "hi"
    PA = "pa"


# ── Request models ────────────────────────────────────────────────────
class MessageItem(BaseModel):
    """A single chat message."""
    sender: str = Field(..., description="Who sent the message (e.g. 'recruiter', 'victim', 'unknown')")
    text: str = Field(..., description="Message body")
    timestamp: Optional[str] = Field(None, description="ISO-8601 or WhatsApp-style timestamp")


class AnalyzeRequest(BaseModel):
    """POST /api/analyze body - accepts structured messages or raw text."""
    text: Optional[str] = Field(None, description="Direct text input")
    raw_text: Optional[str] = Field(None, description="Alternative raw text input")
    messages: Optional[list[MessageItem]] = Field(
        None,
        max_length=500,
        description="Ordered chat messages",
    )
    format: Optional[str] = Field("text", description="text, whatsapp_export, telegram, offer_letter")
    language: Language = Field(Language.EN, description="Response language (en, hi, pa)")
    context: Optional[str] = Field(None, max_length=500, description="Extra user context")


class RawTextAnalyzeRequest(BaseModel):
    """Alternative: raw chat text (WhatsApp / Telegram export)."""
    raw_text: str = Field(..., min_length=1, max_length=100_000)
    language: Language = Field(Language.EN)
    context: Optional[str] = Field(None, max_length=500)


class ReportRequest(BaseModel):
    """POST /api/report body."""
    messages: Optional[list[MessageItem]] = None
    raw_text: Optional[str] = None
    text: Optional[str] = None
    victim_name: Optional[str] = Field(None, max_length=100)
    victim_phone: Optional[str] = Field(None, max_length=15)
    amount_lost: Optional[float] = Field(None, ge=0)
    language: Language = Field(Language.EN)


class EvalCase(BaseModel):
    """One labelled test case for the eval harness."""
    messages: list[MessageItem]
    expected_verdict: Verdict
    expected_stage: Optional[int] = Field(None, ge=0, le=4)
    label: str = Field("", description="Human-readable case name")


class EvalRequest(BaseModel):
    """POST /api/eval body (batch eval)."""
    cases: list[EvalCase] = Field(..., min_length=1, max_length=200)


# ── Signal / evidence models ─────────────────────────────────────────
class Signal(BaseModel):
    """A detected scam signal with evidence."""
    id: str = Field(..., description="Signal identifier, e.g. UPFRONT_DEPOSIT")
    weight: int = Field(..., description="Score contribution")
    evidence: str = Field("", description="Exact quote from input")
    message_index: Optional[int] = Field(None, description="0-based index of source message")


class VirusTotalDetails(BaseModel):
    status: str = Field(..., description="MALICIOUS | SUSPICIOUS | CLEAN | UNKNOWN_DOMAIN | RATE_LIMITED | ERROR | NOT_CONFIGURED")
    risk_score: int = Field(0, description="Risk score 0-100 from VT analysis")
    reason: str = Field("", description="Explanation of security vendor findings")
    target_url: Optional[str] = None
    malicious: int = 0
    suspicious: int = 0
    harmless: int = 0


class CompanyInfo(BaseModel):
    name: Optional[str] = None
    cin: Optional[str] = None
    domain: Optional[str] = None
    mca_match: Optional[bool] = None
    match_score: Optional[float] = None
    status: Optional[str] = None
    roc: Optional[str] = None
    state: Optional[str] = None
    verification_outcome: Optional[str] = None  # "Found and active", "Not found in snapshot", "Suspicious match"
    domain_signals: list[str] = Field(default_factory=list)
    virustotal: Optional[VirusTotalDetails] = None


class PIIMaskResult(BaseModel):
    original_hash: Optional[str] = None
    masked_text: str
    pii_found: list[str] = Field(default_factory=list, description="Types of PII detected")


# ── Response models ───────────────────────────────────────────────────
class AnalyzeResponse(BaseModel):
    """Response from POST /api/analyze."""
    verdict: Verdict
    risk_score: int = Field(..., ge=0, le=100)
    stage: int = Field(..., ge=0, le=4)
    stage_label: str = ""
    next_likely_move: str = ""
    signals: list[Signal] = Field(default_factory=list)
    company: Optional[CompanyInfo] = None
    advice: list[str] = Field(default_factory=list)
    explanation_simple: str = ""
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    language: Language = Language.EN
    pii_masked: bool = False
    pii_types_found: list[str] = Field(default_factory=list)
    rules_score: int = 0
    llm_score: Optional[int] = None
    blended_score: int = 0


class ReportResponse(BaseModel):
    """Response from POST /api/report."""
    report_text: str
    suggested_helpline: str = "1930"
    summary: str = ""
    evidence_count: int = 0


class EvalCaseResult(BaseModel):
    label: str
    predicted_verdict: Verdict
    expected_verdict: Verdict
    correct_verdict: bool
    predicted_stage: int
    expected_stage: Optional[int]
    correct_stage: Optional[bool]
    risk_score: int


class ConfusionEntry(BaseModel):
    actual: str
    predicted: str
    count: int


class EvalResponse(BaseModel):
    results: list[EvalCaseResult]
    accuracy: float
    stage_accuracy: Optional[float] = None
    confusion_matrix: list[ConfusionEntry] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    gemini_configured: bool = False
    groq_configured: bool = False
    llm_provider: str = "rules_only"


# ── LLM structured output schema ─────────────────────────────────────
class LLMSignal(BaseModel):
    id: str
    evidence: str = ""
    message_index: Optional[int] = None


class LLMCompany(BaseModel):
    name: Optional[str] = None
    cin: Optional[str] = None
    domain: Optional[str] = None


class LLMAnalysis(BaseModel):
    """Schema we ask Gemini to return."""
    verdict: str  # SCAM | SUSPICIOUS | LIKELY_GENUINE | UNSURE
    risk_score: int = Field(ge=0, le=100)
    stage: int = Field(ge=0, le=4)
    next_likely_move: str = ""
    signals: list[LLMSignal] = Field(default_factory=list)
    company: Optional[LLMCompany] = None
    advice: list[str] = Field(default_factory=list)
    explanation_simple: str = ""
    confidence: float = Field(0.5, ge=0.0, le=1.0)
