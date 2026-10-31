"""FastAPI router for /api/eval evaluation harness."""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.models.schemas import (
    ConfusionEntry,
    EvalCase,
    EvalCaseResult,
    EvalRequest,
    EvalResponse,
    Verdict,
    AnalyzeRequest,
)
from app.services.analyzer import get_analyzer

router = APIRouter(prefix="/api", tags=["Evaluation"])


def evaluate_cases(cases_data: list[dict]) -> EvalResponse:
    analyzer = get_analyzer()
    results: list[EvalCaseResult] = []
    matrix_counts = defaultdict(lambda: defaultdict(int))
    
    stage_correct = 0
    stage_total = 0

    for c in cases_data:
        input_text = c.get("input", "")
        exp_verdict_str = c.get("true_verdict") or c.get("expected_verdict", "UNSURE")
        exp_verdict = Verdict(exp_verdict_str)
        exp_stage = c.get("true_stage") if c.get("true_stage") is not None else c.get("expected_stage")

        req = AnalyzeRequest(
            text=input_text,
            language=c.get("language", "en"),
            format=c.get("format", "text")
        )
        res = analyzer.analyze(req)

        pred_verdict = res.verdict
        pred_stage = res.stage

        is_correct_verdict = (pred_verdict == exp_verdict)
        matrix_counts[exp_verdict.value][pred_verdict.value] += 1

        is_correct_stage = None
        if exp_stage is not None:
            stage_total += 1
            if pred_stage == exp_stage:
                stage_correct += 1
                is_correct_stage = True
            else:
                is_correct_stage = False

        results.append(EvalCaseResult(
            label=c.get("title") or c.get("label") or c.get("id", "Case"),
            predicted_verdict=pred_verdict,
            expected_verdict=exp_verdict,
            correct_verdict=is_correct_verdict,
            predicted_stage=pred_stage,
            expected_stage=exp_stage,
            correct_stage=is_correct_stage,
            risk_score=res.risk_score,
        ))

    total = len(results)
    acc = sum(1 for r in results if r.correct_verdict) / total if total > 0 else 0.0
    stage_acc = (stage_correct / stage_total) if stage_total > 0 else None

    # Format confusion matrix
    all_labels = ["SCAM", "SUSPICIOUS", "LIKELY_GENUINE", "UNSURE"]
    confusion_entries = []
    for actual in all_labels:
        for predicted in all_labels:
            confusion_entries.append(ConfusionEntry(
                actual=actual,
                predicted=predicted,
                count=matrix_counts[actual][predicted]
            ))

    return EvalResponse(
        results=results,
        accuracy=round(acc, 4),
        stage_accuracy=round(stage_acc, 4) if stage_acc is not None else None,
        confusion_matrix=confusion_entries,
    )


@router.get("/eval", response_model=EvalResponse)
async def run_default_evaluation() -> EvalResponse:
    """Run evaluation against the standard 60-case testset."""
    settings = get_settings()
    testset_path = settings.DATA_DIR / "testset.json"
    if not testset_path.exists():
        raise HTTPException(status_code=404, detail="testset.json not found in data directory")

    try:
        with open(testset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cases = data.get("test_cases", []) if isinstance(data, dict) else data
        return evaluate_cases(cases)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eval harness failed: {str(e)}")


@router.post("/eval", response_model=EvalResponse)
async def run_custom_evaluation(req: EvalRequest) -> EvalResponse:
    """Run evaluation against user-submitted test cases."""
    cases_dicts = []
    for c in req.cases:
        text = "\n".join([f"{m.sender}: {m.text}" for m in c.messages])
        cases_dicts.append({
            "input": text,
            "true_verdict": c.expected_verdict.value,
            "true_stage": c.expected_stage,
            "label": c.label,
        })
    return evaluate_cases(cases_dicts)
