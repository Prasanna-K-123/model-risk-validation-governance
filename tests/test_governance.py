from src.governance import build_findings, validation_opinion


def test_findings_capture_calibration_and_oot_gap():
    primary = {"auc":0.73,"brier":0.18,"calibration_slope":0.64,"calibration_intercept":-0.31}
    challenger = {"auc":0.753,"brier":0.196,"calibration_slope":1.0,"calibration_intercept":0.0}
    source = {"holdout_psi":0.04,"methodology_flags":{"genuine_out_of_time_validation":False,"empirical_lgd_model":False,"empirical_ead_model":False}}
    findings = build_findings(primary, challenger, source)
    ids = {f.finding_id for f in findings}
    assert "MRV-002" in ids
    assert "MRV-006" in ids
    assert validation_opinion(findings) == "conditionally acceptable for research; not production-approved"
