"""
TaskGuard Evaluation Script
Loads testset.json, calls /api/analyze for each case, and computes metrics.
Usage: python evaluate.py [--api-url http://localhost:3000] [--output eval_results.json]
"""

import json
import argparse
import time
import sys
import os
from collections import defaultdict, Counter
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


def load_testset(path: str) -> list[dict]:
    """Load test cases from testset.json."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "test_cases" in data:
        return data["test_cases"]
    if isinstance(data, list):
        return data
    raise ValueError(f"Unexpected testset format in {path}")


def call_api(api_url: str, test_case: dict, timeout: int = 30) -> dict | None:
    """Call /api/analyze with a test case and return the response."""
    endpoint = f"{api_url.rstrip('/')}/api/analyze"
    payload = {
        "text": test_case["input"],
        "format": test_case.get("format", "text"),
        "language": test_case.get("language", "en"),
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Connection refused for {test_case['id']} — is the server running?")
        return None
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout for {test_case['id']}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  ✗ HTTP error for {test_case['id']}: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Unexpected error for {test_case['id']}: {e}")
        return None


def compute_confusion_matrix(
    true_labels: list[str], pred_labels: list[str], labels: list[str]
) -> dict:
    """Compute confusion matrix as a nested dict."""
    matrix = {t: {p: 0 for p in labels} for t in labels}
    for t, p in zip(true_labels, pred_labels):
        if t in matrix and p in matrix[t]:
            matrix[t][p] += 1
    return matrix


def compute_metrics_per_class(
    true_labels: list[str], pred_labels: list[str], labels: list[str]
) -> dict:
    """Compute precision, recall, F1, and support for each class."""
    metrics = {}
    for label in labels:
        tp = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p == label)
        fp = sum(1 for t, p in zip(true_labels, pred_labels) if t != label and p == label)
        fn = sum(1 for t, p in zip(true_labels, pred_labels) if t == label and p != label)
        support = sum(1 for t in true_labels if t == label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        metrics[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }
    return metrics


def compute_stage_accuracy(
    true_stages: list[int], pred_stages: list[int]
) -> dict:
    """Compute stage-level accuracy metrics."""
    if not true_stages:
        return {"accuracy": 0.0, "total": 0, "correct": 0, "mae": 0.0}

    correct = sum(1 for t, p in zip(true_stages, pred_stages) if t == p)
    total = len(true_stages)
    mae = sum(abs(t - p) for t, p in zip(true_stages, pred_stages)) / total

    # Per-stage accuracy
    per_stage = {}
    for stage in sorted(set(true_stages)):
        stage_pairs = [(t, p) for t, p in zip(true_stages, pred_stages) if t == stage]
        stage_correct = sum(1 for t, p in stage_pairs if t == p)
        per_stage[str(stage)] = {
            "accuracy": round(stage_correct / len(stage_pairs), 4) if stage_pairs else 0.0,
            "total": len(stage_pairs),
            "correct": stage_correct,
        }

    return {
        "accuracy": round(correct / total, 4),
        "total": total,
        "correct": correct,
        "mae": round(mae, 4),
        "per_stage": per_stage,
    }


def compute_signal_metrics(
    true_signals_list: list[list[str]], pred_signals_list: list[list[str]]
) -> dict:
    """Compute signal detection metrics (set-based precision/recall)."""
    total_precision_sum = 0.0
    total_recall_sum = 0.0
    n = 0
    all_signal_counts = Counter()
    detected_signal_counts = Counter()

    for true_sigs, pred_sigs in zip(true_signals_list, pred_signals_list):
        true_set = set(true_sigs)
        pred_set = set(pred_sigs)
        if not true_set and not pred_set:
            continue
        n += 1
        for s in true_set:
            all_signal_counts[s] += 1
        for s in true_set & pred_set:
            detected_signal_counts[s] += 1

        if pred_set:
            total_precision_sum += len(true_set & pred_set) / len(pred_set)
        if true_set:
            total_recall_sum += len(true_set & pred_set) / len(true_set)

    avg_precision = round(total_precision_sum / n, 4) if n > 0 else 0.0
    avg_recall = round(total_recall_sum / n, 4) if n > 0 else 0.0
    avg_f1 = (
        round(2 * avg_precision * avg_recall / (avg_precision + avg_recall), 4)
        if (avg_precision + avg_recall) > 0
        else 0.0
    )

    # Per-signal recall
    per_signal = {}
    for sig, total in all_signal_counts.most_common():
        detected = detected_signal_counts.get(sig, 0)
        per_signal[sig] = {
            "recall": round(detected / total, 4),
            "total": total,
            "detected": detected,
        }

    return {
        "avg_precision": avg_precision,
        "avg_recall": avg_recall,
        "avg_f1": avg_f1,
        "cases_evaluated": n,
        "per_signal": per_signal,
    }


def print_confusion_matrix(matrix: dict, labels: list[str]):
    """Pretty-print a confusion matrix to stdout."""
    col_width = max(len(l) for l in labels) + 2
    header = "True \\ Pred".ljust(col_width) + "".join(l.ljust(col_width) for l in labels)
    print(header)
    print("-" * len(header))
    for true_label in labels:
        row = true_label.ljust(col_width)
        for pred_label in labels:
            row += str(matrix[true_label][pred_label]).ljust(col_width)
        print(row)


def print_metrics_table(metrics: dict):
    """Pretty-print per-class metrics."""
    print(f"\n{'Class':<18} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Support':>10}")
    print("-" * 60)
    for label, m in metrics.items():
        print(
            f"{label:<18} {m['precision']:>10.4f} {m['recall']:>10.4f} "
            f"{m['f1']:>10.4f} {m['support']:>10}"
        )


def main():
    parser = argparse.ArgumentParser(description="TaskGuard Evaluation Script")
    parser.add_argument(
        "--api-url",
        default="http://localhost:3000",
        help="Base URL of the TaskGuard API (default: http://localhost:3000)",
    )
    parser.add_argument(
        "--testset",
        default=os.path.join(os.path.dirname(__file__), "testset.json"),
        help="Path to testset.json",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(os.path.dirname(__file__), "eval_results.json"),
        help="Path to save evaluation results",
    )
    parser.add_argument(
        "--timeout", type=int, default=30, help="API request timeout in seconds"
    )
    parser.add_argument(
        "--delay", type=float, default=0.5, help="Delay between API calls in seconds"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print per-case results"
    )
    args = parser.parse_args()

    # Load test cases
    print(f"Loading test set from {args.testset}...")
    test_cases = load_testset(args.testset)
    print(f"Loaded {len(test_cases)} test cases.\n")

    # Distribution summary
    verdict_dist = Counter(tc["true_verdict"] for tc in test_cases)
    stage_dist = Counter(tc.get("true_stage", -1) for tc in test_cases)
    format_dist = Counter(tc.get("format", "text") for tc in test_cases)
    lang_dist = Counter(tc.get("language", "en") for tc in test_cases)
    print("Test set distribution:")
    print(f"  Verdicts: {dict(verdict_dist)}")
    print(f"  Stages:   {dict(stage_dist)}")
    print(f"  Formats:  {dict(format_dist)}")
    print(f"  Languages:{dict(lang_dist)}")
    print()

    # Run evaluation
    results = []
    true_verdicts = []
    pred_verdicts = []
    true_stages = []
    pred_stages = []
    true_signals_list = []
    pred_signals_list = []
    errors = []
    skipped = 0

    print(f"Evaluating against {args.api_url}...")
    print("=" * 60)

    for i, tc in enumerate(test_cases):
        tc_id = tc["id"]
        print(f"[{i+1}/{len(test_cases)}] {tc_id}: {tc['title'][:50]}...", end=" ")

        response = call_api(args.api_url, tc, timeout=args.timeout)

        if response is None:
            print("SKIPPED")
            skipped += 1
            errors.append({"id": tc_id, "error": "API call failed"})
            if args.delay > 0:
                time.sleep(args.delay)
            continue

        # Extract predictions (adapt field names to your API response schema)
        pred_verdict = response.get("verdict", response.get("classification", "UNSURE"))
        pred_stage = response.get("stage", response.get("scam_stage", -1))
        pred_signals = response.get("signals", response.get("detected_signals", []))

        # Normalize signal format
        if isinstance(pred_signals, list) and pred_signals and isinstance(pred_signals[0], dict):
            pred_signals = [s.get("id", s.get("signal_id", "")) for s in pred_signals]

        true_verdict = tc["true_verdict"]
        true_stage = tc.get("true_stage", -1)
        true_sigs = tc.get("true_signals", [])

        # Record
        true_verdicts.append(true_verdict)
        pred_verdicts.append(pred_verdict)
        true_signals_list.append(true_sigs)
        pred_signals_list.append(pred_signals)

        if true_stage >= 0 and pred_stage >= 0:
            true_stages.append(true_stage)
            pred_stages.append(pred_stage)

        verdict_match = "✓" if true_verdict == pred_verdict else "✗"
        stage_match = ""
        if true_stage >= 0:
            stage_match = f" | Stage: {pred_stage} {'✓' if true_stage == pred_stage else '✗'}"

        print(f"{verdict_match} (pred={pred_verdict}, true={true_verdict}){stage_match}")

        case_result = {
            "id": tc_id,
            "title": tc["title"],
            "true_verdict": true_verdict,
            "pred_verdict": pred_verdict,
            "verdict_correct": true_verdict == pred_verdict,
            "true_stage": true_stage,
            "pred_stage": pred_stage,
            "stage_correct": true_stage == pred_stage if true_stage >= 0 else None,
            "true_signals": true_sigs,
            "pred_signals": pred_signals,
            "response": response if args.verbose else None,
        }
        results.append(case_result)

        if args.delay > 0:
            time.sleep(args.delay)

    print("=" * 60)
    print(f"\nCompleted: {len(results)} evaluated, {skipped} skipped, {len(errors)} errors\n")

    if not results:
        print("No results to evaluate. Ensure the API server is running.")
        sys.exit(1)

    # ── Verdict Metrics ──
    verdict_labels = ["SCAM", "SUSPICIOUS", "LIKELY_GENUINE", "UNSURE"]
    # Include any labels that appear in predictions but not in our standard set
    all_labels = sorted(set(verdict_labels) | set(pred_verdicts) | set(true_verdicts))
    # But keep canonical order first
    ordered_labels = [l for l in verdict_labels if l in all_labels]
    ordered_labels += [l for l in all_labels if l not in ordered_labels]

    confusion = compute_confusion_matrix(true_verdicts, pred_verdicts, ordered_labels)
    verdict_metrics = compute_metrics_per_class(true_verdicts, pred_verdicts, ordered_labels)

    overall_accuracy = round(
        sum(1 for t, p in zip(true_verdicts, pred_verdicts) if t == p) / len(true_verdicts), 4
    )

    # Macro averages
    active_classes = [l for l in ordered_labels if verdict_metrics[l]["support"] > 0]
    macro_precision = round(
        sum(verdict_metrics[l]["precision"] for l in active_classes) / len(active_classes), 4
    ) if active_classes else 0.0
    macro_recall = round(
        sum(verdict_metrics[l]["recall"] for l in active_classes) / len(active_classes), 4
    ) if active_classes else 0.0
    macro_f1 = round(
        sum(verdict_metrics[l]["f1"] for l in active_classes) / len(active_classes), 4
    ) if active_classes else 0.0

    print("\n══════════════════════════════════════════════════════")
    print("                 VERDICT METRICS")
    print("══════════════════════════════════════════════════════")
    print(f"\nOverall Accuracy: {overall_accuracy:.4f} ({sum(1 for t, p in zip(true_verdicts, pred_verdicts) if t == p)}/{len(true_verdicts)})")
    print(f"Macro Precision:  {macro_precision:.4f}")
    print(f"Macro Recall:     {macro_recall:.4f}")
    print(f"Macro F1:         {macro_f1:.4f}")

    print_metrics_table(verdict_metrics)

    print("\nConfusion Matrix:")
    print_confusion_matrix(confusion, ordered_labels)

    # ── Stage Metrics ──
    stage_metrics = compute_stage_accuracy(true_stages, pred_stages)

    if true_stages:
        print("\n\n══════════════════════════════════════════════════════")
        print("                  STAGE METRICS")
        print("══════════════════════════════════════════════════════")
        print(f"\nStage Accuracy: {stage_metrics['accuracy']:.4f} ({stage_metrics['correct']}/{stage_metrics['total']})")
        print(f"Mean Absolute Error: {stage_metrics['mae']:.4f}")
        if "per_stage" in stage_metrics:
            print("\nPer-Stage Breakdown:")
            for stage, sm in sorted(stage_metrics["per_stage"].items(), key=lambda x: int(x[0])):
                print(f"  Stage {stage}: {sm['accuracy']:.4f} ({sm['correct']}/{sm['total']})")

    # ── Signal Metrics ──
    signal_metrics = compute_signal_metrics(true_signals_list, pred_signals_list)

    print("\n\n══════════════════════════════════════════════════════")
    print("                 SIGNAL METRICS")
    print("══════════════════════════════════════════════════════")
    print(f"\nAvg Signal Precision: {signal_metrics['avg_precision']:.4f}")
    print(f"Avg Signal Recall:    {signal_metrics['avg_recall']:.4f}")
    print(f"Avg Signal F1:        {signal_metrics['avg_f1']:.4f}")

    if signal_metrics.get("per_signal"):
        print("\nPer-Signal Recall (top 15):")
        for sig, sm in list(signal_metrics["per_signal"].items())[:15]:
            print(f"  {sig:<30} {sm['recall']:.4f} ({sm['detected']}/{sm['total']})")

    # ── Save Results ──
    eval_output = {
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "api_url": args.api_url,
            "testset_path": args.testset,
            "total_cases": len(test_cases),
            "evaluated": len(results),
            "skipped": skipped,
            "errors": len(errors),
        },
        "verdict_metrics": {
            "overall_accuracy": overall_accuracy,
            "macro_precision": macro_precision,
            "macro_recall": macro_recall,
            "macro_f1": macro_f1,
            "per_class": verdict_metrics,
            "confusion_matrix": confusion,
        },
        "stage_metrics": stage_metrics,
        "signal_metrics": signal_metrics,
        "per_case_results": results,
        "errors": errors,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(eval_output, f, indent=2, ensure_ascii=False)

    print(f"\n\nResults saved to {args.output}")
    print("Done.")


if __name__ == "__main__":
    main()
