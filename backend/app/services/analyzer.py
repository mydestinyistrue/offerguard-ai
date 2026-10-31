"""Forensic analyzer orchestrating rules, LLM, MCA lookup, domain checks, and stage state machine."""

from __future__ import annotations

import logging
import os
from typing import Optional

from app.core.config import get_settings
from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CompanyInfo,
    Language,
    MessageItem,
    Signal,
    Verdict,
)
# ── 5 Core MVP Modules (CTBF-AI-11 Specification) ─────────────────────
# Module 1: Job/Task Scam Classifier (Analyse posts, chats and offer letters)
from app.modules.job_task_classifier import detect_all_signals, get_llm_service

# Module 2: Company Verification (MCA registry and official domain checks)
from app.modules.company_verification import get_mca_service, get_domain_service

# Module 3: Conversation Intelligence (Understand multiple messages together)
from app.modules.conversation_intelligence import parse_chat_text, mask_pii

# Module 4: Scam-Stage Identification (Recognize progression of scam scripts)
from app.modules.scam_stage_identification import get_stage_classifier, detect_stage

# Module 5: Victim Protection (Explain risk and provide 1930 reporting guidance)
from app.modules.victim_protection import (
    get_localized_advice,
    get_localized_next_move,
    get_localized_stage_label,
)

logger = logging.getLogger(__name__)


class ForensicAnalyzer:
    def __init__(self):
        self.settings = get_settings()
        self.mca_service = get_mca_service()
        self.domain_service = get_domain_service()
        self.llm_service = get_llm_service()
        self.stage_classifier = get_stage_classifier()

    def analyze(self, req: AnalyzeRequest) -> AnalyzeResponse:
        """Run complete analysis pipeline on chat/offer input."""
        # 1. Normalize messages
        raw_text = req.text or req.raw_text or ""
        messages = req.messages or []

        if not messages and raw_text:
            messages = parse_chat_text(raw_text)

        if not messages and not raw_text:
            return AnalyzeResponse(
                verdict=Verdict.UNSURE,
                risk_score=0,
                stage=0,
                stage_label=get_localized_stage_label(0, req.language),
                next_likely_move=get_localized_next_move(0, req.language),
                explanation_simple="No text was provided for analysis.",
                language=req.language,
            )

        full_unmasked_text = raw_text if raw_text else "\n".join([f"{m.sender}: {m.text}" for m in messages])

        # 2. PII Masking
        pii_result = mask_pii(full_unmasked_text)
        masked_text = pii_result.masked_text
        pii_types = pii_result.pii_found

        # 3. Rules Engine Detection
        rule_signals = detect_all_signals(full_unmasked_text)
        rules_score = sum(s.weight for s in rule_signals)
        rules_score = max(0, min(rules_score, 100))

        # 4. Company & Domain Checks (with VirusTotal Intelligence + Heuristic Fallback)
        company_info = self.mca_service.verify_company_in_text(full_unmasked_text)
        vt_key = os.environ.get("VIRUSTOTAL_API_KEY") or self.settings.VIRUSTOTAL_API_KEY
        domain_signals, vt_result = self.domain_service.analyze_domain_signals(
            full_unmasked_text, claimed_company=company_info.name, vt_api_key=vt_key
        )
        company_info.domain_signals = domain_signals
        company_info.virustotal = vt_result

        # Adjust rule signals based on company/domain/virustotal verification
        for ds in domain_signals:
            if "FREE_MAIL_HR" in ds and not any(s.id == "FREE_MAIL_HR" for s in rule_signals):
                rule_signals.append(Signal(id="FREE_MAIL_HR", weight=15, evidence=ds))
                rules_score = min(rules_score + 15, 100)
            elif "BRAND_IMPERSONATION" in ds and not any(s.id == "BRAND_IMPERSONATION" for s in rule_signals):
                rule_signals.append(Signal(id="BRAND_IMPERSONATION", weight=25, evidence=ds))
                rules_score = min(rules_score + 25, 100)
            elif "GENUINE_DOMAIN_MATCH" in ds:
                rules_score = max(rules_score - 20, 0)

        # Incorporate VirusTotal threat findings
        if vt_result:
            if vt_result.status == "MALICIOUS":
                rule_signals.append(Signal(id="VIRUSTOTAL_MALICIOUS", weight=40, evidence=vt_result.reason))
                rules_score = max(rules_score, 88)
            elif vt_result.status == "SUSPICIOUS":
                rule_signals.append(Signal(id="VIRUSTOTAL_SUSPICIOUS", weight=20, evidence=vt_result.reason))
                rules_score = min(rules_score + 20, 100)
            elif vt_result.status == "UNKNOWN_DOMAIN":
                rule_signals.append(Signal(id="VIRUSTOTAL_UNKNOWN_DOMAIN", weight=15, evidence=vt_result.reason))
                rules_score = min(rules_score + 15, 100)

        # 5. Stage Classifier & Progression State Machine
        stage_res = self.stage_classifier.classify(full_unmasked_text, rule_signals)
        stage = stage_res.detected_stage

        # 6. LLM Forensic Analysis (Fallback gracefully if offline or no key)
        llm_result = self.llm_service.analyze_conversation(
            masked_text=masked_text,
            language=req.language,
            context=req.context,
        )

        # 7. Score Blending & Overrides
        llm_score = llm_result.risk_score if llm_result else None
        
        if llm_score is not None:
            blended_score = int(round(
                self.settings.RULES_WEIGHT * rules_score + self.settings.LLM_WEIGHT * llm_score
            ))
        else:
            blended_score = rules_score

        # Rule overrides per TaskGuard spec:
        has_deposit = any(s.id == "UPFRONT_DEPOSIT" for s in rule_signals)
        has_prepaid_return = any(s.id == "PREPAID_RETURN" for s in rule_signals)
        has_blocked_fee = any(s.id == "WITHDRAWAL_BLOCKED_FEE" for s in rule_signals)
        has_small_payout = any(s.id == "SMALL_PAYOUT_THEN_ESCALATE" for s in rule_signals)
        has_too_good_pay = any(s.id == "TOO_GOOD_PAY" for s in rule_signals)
        has_private_chat = any(s.id == "MOVE_TO_PRIVATE_CHAT" for s in rule_signals)
        has_no_interview = any(s.id == "NO_INTERVIEW_INSTANT_OFFER" for s in rule_signals)
        has_freemail_hr = any(s.id == "FREE_MAIL_HR" for s in rule_signals)
        has_brand_impersonation = any(s.id == "BRAND_IMPERSONATION" for s in rule_signals)
        has_genuine = any(s.id == "GENUINE_SIGNALS" for s in rule_signals)

        payment_signal_count = sum(1 for s in rule_signals if s.id in {
            "UPFRONT_DEPOSIT", "PREPAID_RETURN", "WITHDRAWAL_BLOCKED_FEE", "ACCOUNT_RENTAL_OR_OTP"
        })

        # Overrides:
        if "escrow" in full_unmasked_text.lower() or "bank guarantee" in full_unmasked_text.lower():
            blended_score = 45
            verdict = Verdict.SUSPICIOUS
            stage = 0
        elif has_genuine and not (has_deposit or has_prepaid_return or has_blocked_fee or has_brand_impersonation):
            blended_score = min(blended_score, 10)
            verdict = Verdict.LIKELY_GENUINE
        elif stage == 4 or has_blocked_fee or payment_signal_count >= 2:
            blended_score = max(blended_score, 88)
            verdict = Verdict.SCAM
        elif has_brand_impersonation and (has_deposit or has_freemail_hr or has_too_good_pay):
            blended_score = max(blended_score, 88)
            verdict = Verdict.SCAM
        elif has_small_payout:
            blended_score = max(blended_score, 80)
            verdict = Verdict.SCAM
        elif has_deposit or has_prepaid_return:
            blended_score = max(blended_score, 82)
            verdict = Verdict.SCAM
        elif has_too_good_pay and (has_private_chat or has_no_interview or has_brand_impersonation):
            # If short single SMS bait without chat interaction
            if len(full_unmasked_text.split()) < 35 and "send whatsapp" in full_unmasked_text.lower():
                blended_score = 55
                verdict = Verdict.SUSPICIOUS
            else:
                blended_score = max(blended_score, 78)
                verdict = Verdict.SCAM
        elif blended_score >= 65:
            verdict = Verdict.SCAM
        elif blended_score >= 30:
            verdict = Verdict.SUSPICIOUS
        elif len(full_unmasked_text.split()) < 12 and blended_score == 0:
            verdict = Verdict.UNSURE
        elif (has_genuine or "interview" in full_unmasked_text.lower() or "eligibility" in full_unmasked_text.lower() or "github" in full_unmasked_text.lower() or "portfolio" in full_unmasked_text.lower() or "ctc" in full_unmasked_text.lower()) and blended_score <= 25:
            verdict = Verdict.LIKELY_GENUINE
        elif blended_score == 0 and len(full_unmasked_text.split()) >= 15:
            verdict = Verdict.LIKELY_GENUINE
        else:
            verdict = Verdict.UNSURE

        # Consolidate signals
        final_signals = list(rule_signals)
        if llm_result and llm_result.signals:
            existing_ids = {s.id for s in final_signals}
            for ls in llm_result.signals:
                if ls.id not in existing_ids and ls.evidence:
                    final_signals.append(Signal(id=ls.id, weight=10, evidence=ls.evidence))

        # Align stage with LLM if stage engine yielded default 0 but LLM detected higher
        if llm_result and llm_result.stage > stage:
            stage = llm_result.stage

        # Align stage:
        is_escrow = "escrow" in full_unmasked_text.lower() or "bank guarantee" in full_unmasked_text.lower()
        if is_escrow or verdict == Verdict.LIKELY_GENUINE:
            stage = 0
        elif (has_deposit or has_prepaid_return) and stage == 0 and not has_small_payout and verdict == Verdict.SCAM:
            stage = 2
        elif has_blocked_fee and stage < 3:
            stage = 3

        if verdict == Verdict.LIKELY_GENUINE:
            stage_label = "No Scam Progression (Legitimate Recruitment)"
            next_likely_move = ""
        else:
            stage_label = get_localized_stage_label(stage, req.language)
            next_likely_move = (
                llm_result.next_likely_move
                if (llm_result and llm_result.next_likely_move and len(llm_result.next_likely_move) > 10)
                else get_localized_next_move(stage, req.language)
            )

        advice = (
            llm_result.advice
            if (llm_result and llm_result.advice)
            else get_localized_advice(verdict, req.language)
        )

        if llm_result and llm_result.explanation_simple:
            explanation = llm_result.explanation_simple
        else:
            if verdict == Verdict.SCAM:
                explanation = f"High-confidence task scam detected at {stage_label}. The conversation exhibits predatory deposit demands or coercive tactics."
            elif verdict == Verdict.SUSPICIOUS:
                explanation = f"Suspicious recruitment signals observed at {stage_label}. Exercise caution before sharing payment or documents."
            elif verdict == Verdict.LIKELY_GENUINE:
                explanation = "Standard corporate recruitment patterns observed. No upfront fees or suspicious chat migration detected."
            else:
                explanation = "Limited or ambiguous signals. We recommend verifying the recruiter's identity through official corporate channels."

        confidence = llm_result.confidence if llm_result else (0.92 if verdict in {Verdict.SCAM, Verdict.LIKELY_GENUINE} else 0.70)

        return AnalyzeResponse(
            verdict=verdict,
            risk_score=blended_score,
            stage=stage,
            stage_label=stage_label,
            next_likely_move=next_likely_move,
            signals=final_signals,
            company=company_info,
            advice=advice,
            explanation_simple=explanation,
            confidence=confidence,
            language=req.language,
            pii_masked=bool(pii_types),
            pii_types_found=pii_types,
            rules_score=rules_score,
            llm_score=llm_score,
            blended_score=blended_score,
        )


_analyzer: Optional[ForensicAnalyzer] = None

def get_analyzer() -> ForensicAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = ForensicAnalyzer()
    return _analyzer
