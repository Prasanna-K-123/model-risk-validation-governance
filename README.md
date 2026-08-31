# Independent Model Risk Validation & Governance

An independent-style validation framework applied to the credit-risk PD model built in `credit-risk-ifrs9-stress-testing`. The framework pins the source model to a specific Git commit, independently recomputes holdout performance from saved predictions, compares the primary scorecard with its challenger, tests calibration and stability, applies governance thresholds, creates a findings register, and produces a validation opinion.

## Validation scope

- independent recomputation of ROC-AUC, Gini, KS and Brier score
- calibration intercept/slope and calibration error diagnostics
- bootstrap uncertainty for discrimination
- challenger benchmarking and materiality assessment
- population-stability / PSI review using the source model's documented output
- segment-level outcome analysis
- sensitivity tests under probability shifts and odds scaling
- model inventory, tiering, validation status and issue-severity rules
- explicit review of source-model limitations, including the absence of genuine out-of-time validation
- machine-generated validation report and findings register
- unit tests and GitHub Actions reproducibility

## Evidence boundary

The underlying holdout predictions and source metrics are real outputs from this account's separate credit-risk project and are pinned to commit `98bbae43d8c711e98021539b184fc8f672a6273c`. The underlying German-credit sample is public research data. Governance thresholds, model tiering and issue severities in this repository are **illustrative internal-policy assumptions**, not the policies of any bank, regulator or employer.

This repository does **not** claim production approval. Its purpose is to demonstrate how an independent validation function challenges a model rather than merely rebuilding it.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_validation.py
```

The pipeline writes `outputs/validation_metrics.json`, `outputs/findings.csv`, `outputs/segment_analysis.csv`, `outputs/sensitivity.csv` and `reports/generated/independent_validation_report.md`.
