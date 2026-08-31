from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


def write_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def build_report(metrics: dict, findings: pd.DataFrame, segments: pd.DataFrame, sensitivity: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    p = metrics["primary"]
    c = metrics["challenger"]
    lines = [
        "# Independent Model Validation Report",
        "",
        f"**Validation opinion:** {metrics['validation_opinion']}",
        "",
        "## Scope and independence",
        "",
        "This report independently recomputes holdout diagnostics from the source model's saved predictions. It does not rely only on the source model's headline metrics. The source evidence is pinned to an immutable Git commit. Governance thresholds and severity definitions are illustrative internal-policy assumptions.",
        "",
        "## Primary model diagnostics",
        "",
        f"- AUC: {p['auc']:.4f} (95% bootstrap CI {p['auc_ci_95'][0]:.4f}-{p['auc_ci_95'][1]:.4f})",
        f"- Gini: {p['gini']:.4f}",
        f"- KS: {p['ks']:.4f}",
        f"- Brier score: {p['brier']:.4f}",
        f"- Calibration intercept: {p['calibration_intercept']:.4f}",
        f"- Calibration slope: {p['calibration_slope']:.4f}",
        f"- Holdout PSI from source pipeline: {metrics['holdout_psi']:.4f}",
        "",
        "## Challenger benchmark",
        "",
        f"Challenger AUC is {c['auc']:.4f} versus {p['auc']:.4f} for the primary scorecard; challenger Brier is {c['brier']:.4f} versus {p['brier']:.4f}.",
        "",
        "## Findings register",
        "",
        findings.to_markdown(index=False) if not findings.empty else "No open findings.",
        "",
        "## Segment outcome analysis",
        "",
        segments.to_markdown(index=False) if not segments.empty else "No eligible segments.",
        "",
        "## Sensitivity analysis",
        "",
        sensitivity.to_markdown(index=False),
        "",
        "## Limitations and production conditions",
        "",
        "The source project uses a research credit dataset and a random holdout rather than genuine temporal validation. The source project also explicitly labels LGD/EAD as non-empirical. This validation therefore supports demonstration of validation methodology, not production approval, regulatory compliance, or institution-specific model governance.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
