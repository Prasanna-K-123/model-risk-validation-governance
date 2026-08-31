# Independent Model Risk Validation & Governance

An independent-style validation framework applied to the credit-risk PD model built in `credit-risk-ifrs9-stress-testing`. The framework pins the source model to a specific Git commit, independently recomputes holdout performance from saved predictions, compares the primary scorecard with its challenger, tests calibration and stability, applies governance thresholds, creates a findings register, and produces a validation opinion.

## Verified validation outcome

GitHub Actions successfully ran the unit tests, independent validation pipeline and evidence-persistence step. The validation independently recomputed metrics from **200 saved holdout observations** pinned to source commit `98bbae43d8c711e98021539b184fc8f672a6273c`.

| Diagnostic | Primary scorecard | Challenger |
|---|---:|---:|
| ROC-AUC | 0.7295 | 0.7529 |
| 95% bootstrap AUC CI | 0.6531–0.7994 | 0.6793–0.8268 |
| Gini | 0.4590 | 0.5057 |
| KS | 0.3738 | 0.3857 |
| Brier score | 0.1838 | 0.1958 |
| Calibration intercept | -0.3122 | -0.6569 |
| Calibration slope | 0.6411 | 1.4287 |

The challenger improves AUC by **0.0233**, but has a worse Brier score and also materially imperfect calibration. The source holdout PSI is **0.0392**, below the illustrative drift trigger.

The framework produces **5 open validation findings, including 2 high-severity findings**, and therefore issues the opinion:

> **Conditionally acceptable for research; not production-approved.**

High-severity findings are (1) primary-model calibration slope outside the illustrative 0.80–1.20 range and (2) absence of genuine out-of-time validation. Medium findings cover calibration-in-the-large, challenger/model-selection trade-offs, and the source project's non-empirical LGD/EAD scope. The point of the project is to demonstrate independent challenge, including adverse conclusions, rather than manufacture a clean approval.

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

This repository does **not** claim production approval. Its purpose is to demonstrate how an independent validation function challenges a model rather than merely rebuilding it. The immutable source pin prevents silent changes in the validated evidence set.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_validation.py
```

The pipeline writes `outputs/validation_metrics.json`, `outputs/findings.csv`, `outputs/segment_analysis.csv`, `outputs/sensitivity.csv` and `reports/generated/independent_validation_report.md`.
