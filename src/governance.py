from __future__ import annotations

from dataclasses import dataclass, asdict

from src.config import POLICY


@dataclass
class Finding:
    finding_id: str
    area: str
    severity: str
    status: str
    observation: str
    recommendation: str


def build_findings(primary: dict, challenger: dict, source_metrics: dict) -> list[Finding]:
    findings: list[Finding] = []
    if primary["auc"] < POLICY["auc_min"]:
        findings.append(Finding("MRV-001", "discrimination", "high", "open", f"Primary AUC {primary['auc']:.3f} is below the illustrative {POLICY['auc_min']:.2f} floor.", "Redevelop or materially strengthen discrimination before production use."))
    if not (POLICY["calibration_slope_low"] <= primary["calibration_slope"] <= POLICY["calibration_slope_high"]):
        findings.append(Finding("MRV-002", "calibration", "high", "open", f"Calibration slope {primary['calibration_slope']:.3f} falls outside the illustrative {POLICY['calibration_slope_low']:.2f}-{POLICY['calibration_slope_high']:.2f} range.", "Recalibrate on representative development/validation data and retest slope/intercept."))
    if abs(primary["calibration_intercept"]) > POLICY["calibration_intercept_abs_max"]:
        findings.append(Finding("MRV-003", "calibration", "medium", "open", f"Calibration intercept {primary['calibration_intercept']:.3f} exceeds the illustrative absolute tolerance.", "Review calibration-in-the-large and portfolio default-rate alignment."))
    if challenger["auc"] - primary["auc"] >= POLICY["challenger_auc_materiality"]:
        findings.append(Finding("MRV-004", "benchmarking", "medium", "open", f"Challenger AUC exceeds the primary by {challenger['auc']-primary['auc']:.3f}.", "Document the interpretability/performance trade-off and formally justify model selection."))
    psi = float(source_metrics.get("holdout_psi", 0.0))
    if psi >= POLICY["psi_high"]:
        sev = "high"
        findings.append(Finding("MRV-005", "stability", sev, "open", f"Holdout PSI {psi:.3f} indicates material population shift.", "Investigate drift drivers and consider redevelopment."))
    elif psi >= POLICY["psi_low"]:
        findings.append(Finding("MRV-005", "stability", "medium", "open", f"Holdout PSI {psi:.3f} indicates moderate population shift.", "Increase monitoring frequency and investigate drift drivers."))
    flags = source_metrics.get("methodology_flags", {})
    if not flags.get("genuine_out_of_time_validation", False):
        findings.append(Finding("MRV-006", "validation design", "high", "open", "The source model explicitly states that genuine out-of-time validation was not performed.", "Obtain a temporal cohort and perform out-of-time validation before production approval."))
    if not flags.get("empirical_lgd_model", False) or not flags.get("empirical_ead_model", False):
        findings.append(Finding("MRV-007", "scope boundary", "medium", "open", "LGD/EAD layers are not empirically estimated in the source project.", "Keep PD validation conclusions separate from any LGD/EAD or ECL production-use claim."))
    return findings


def validation_opinion(findings: list[Finding]) -> str:
    severities = [f.severity for f in findings if f.status == "open"]
    if "critical" in severities:
        return "reject"
    if "high" in severities:
        return "conditionally acceptable for research; not production-approved"
    if "medium" in severities:
        return "acceptable with remediation"
    return "acceptable within stated scope"


def finding_records(findings: list[Finding]) -> list[dict]:
    return [asdict(f) for f in findings]
