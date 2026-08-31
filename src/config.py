from __future__ import annotations

SOURCE_COMMIT = "98bbae43d8c711e98021539b184fc8f672a6273c"
PREDICTIONS_URL = f"https://raw.githubusercontent.com/Prasanna-K-123/credit-risk-ifrs9-stress-testing/{SOURCE_COMMIT}/outputs/holdout_predictions.csv"
METRICS_URL = f"https://raw.githubusercontent.com/Prasanna-K-123/credit-risk-ifrs9-stress-testing/{SOURCE_COMMIT}/outputs/metrics.json"
RANDOM_STATE = 20260831
BOOTSTRAPS = 1000

# Illustrative validation policy, not an institutional policy.
POLICY = {
    "auc_min": 0.70,
    "brier_max": 0.20,
    "calibration_slope_low": 0.80,
    "calibration_slope_high": 1.20,
    "calibration_intercept_abs_max": 0.25,
    "psi_low": 0.10,
    "psi_high": 0.25,
    "challenger_auc_materiality": 0.02,
}
