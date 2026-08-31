from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from src.config import BOOTSTRAPS, RANDOM_STATE, SOURCE_COMMIT
from src.data import load_source_evidence
from src.governance import build_findings, finding_records, validation_opinion
from src.metrics import bootstrap_auc_ci, segment_analysis, sensitivity_analysis, validation_metrics
from src.reporting import build_report, write_json

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
REPORT = ROOT / "reports" / "generated" / "independent_validation_report.md"


def main() -> None:
    predictions, source = load_source_evidence()
    y = predictions["observed_default"]
    primary = validation_metrics(y, predictions["pd_scorecard"])
    challenger = validation_metrics(y, predictions["pd_challenger"])
    primary["auc_ci_95"] = list(bootstrap_auc_ci(y, predictions["pd_scorecard"], BOOTSTRAPS, RANDOM_STATE))
    challenger["auc_ci_95"] = list(bootstrap_auc_ci(y, predictions["pd_challenger"], BOOTSTRAPS, RANDOM_STATE + 1))

    findings = build_findings(primary, challenger, source)
    findings_df = pd.DataFrame(finding_records(findings))
    segments = segment_analysis(predictions)
    sensitivity = sensitivity_analysis(y, predictions["pd_scorecard"])

    metrics = {
        "source_commit": SOURCE_COMMIT,
        "holdout_rows": int(len(predictions)),
        "default_rate": float(y.mean()),
        "primary": primary,
        "challenger": challenger,
        "challenger_auc_delta": float(challenger["auc"] - primary["auc"]),
        "holdout_psi": float(source["holdout_psi"]),
        "open_findings": int(len(findings)),
        "high_findings": int(sum(f.severity == "high" for f in findings)),
        "validation_opinion": validation_opinion(findings),
        "methodology_flags": {
            "source_predictions": "empirical saved holdout outputs from separate credit-risk repository",
            "governance_thresholds": "illustrative",
            "institutional_policy_claim": False,
        },
    }
    OUTPUTS.mkdir(exist_ok=True)
    write_json(metrics, OUTPUTS / "validation_metrics.json")
    findings_df.to_csv(OUTPUTS / "findings.csv", index=False)
    segments.to_csv(OUTPUTS / "segment_analysis.csv", index=False)
    sensitivity.to_csv(OUTPUTS / "sensitivity.csv", index=False)
    build_report(metrics, findings_df, segments, sensitivity, REPORT)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
