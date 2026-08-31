# Independent Model Validation Report

**Validation opinion:** conditionally acceptable for research; not production-approved

## Scope and independence

This report independently recomputes holdout diagnostics from the source model's saved predictions. It does not rely only on the source model's headline metrics. The source evidence is pinned to an immutable Git commit. Governance thresholds and severity definitions are illustrative internal-policy assumptions.

## Primary model diagnostics

- AUC: 0.7295 (95% bootstrap CI 0.6531-0.7994)
- Gini: 0.4590
- KS: 0.3738
- Brier score: 0.1838
- Calibration intercept: -0.3122
- Calibration slope: 0.6411
- Holdout PSI from source pipeline: 0.0392

## Challenger benchmark

Challenger AUC is 0.7529 versus 0.7295 for the primary scorecard; challenger Brier is 0.1958 versus 0.1838.

## Findings register

| finding_id   | area              | severity   | status   | observation                                                                               | recommendation                                                                            |
|:-------------|:------------------|:-----------|:---------|:------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------|
| MRV-002      | calibration       | high       | open     | Calibration slope 0.641 falls outside the illustrative 0.80-1.20 range.                   | Recalibrate on representative development/validation data and retest slope/intercept.     |
| MRV-003      | calibration       | medium     | open     | Calibration intercept -0.312 exceeds the illustrative absolute tolerance.                 | Review calibration-in-the-large and portfolio default-rate alignment.                     |
| MRV-004      | benchmarking      | medium     | open     | Challenger AUC exceeds the primary by 0.023.                                              | Document the interpretability/performance trade-off and formally justify model selection. |
| MRV-006      | validation design | high       | open     | The source model explicitly states that genuine out-of-time validation was not performed. | Obtain a temporal cohort and perform out-of-time validation before production approval.   |
| MRV-007      | scope boundary    | medium     | open     | LGD/EAD layers are not empirically estimated in the source project.                       | Keep PD validation conclusions separate from any LGD/EAD or ECL production-use claim.     |

## Segment outcome analysis

| dimension      | segment   |   n |   default_rate |      auc |    brier |
|:---------------|:----------|----:|---------------:|---------:|---------:|
| age_segment    | <=29      |  88 |       0.352273 | 0.801924 | 0.166807 |
| age_segment    | 30-44     |  72 |       0.291667 | 0.654528 | 0.213499 |
| age_segment    | 45+       |  40 |       0.2      | 0.703125 | 0.167494 |
| amount_segment | low       |  67 |       0.283582 | 0.751096 | 0.161366 |
| amount_segment | mid       |  66 |       0.272727 | 0.69213  | 0.190911 |
| amount_segment | high      |  67 |       0.343284 | 0.742095 | 0.199091 |

## Sensitivity analysis

| scenario        |      auc |     gini |      ks |    brier |   calibration_intercept |   calibration_slope |
|:----------------|---------:|---------:|--------:|---------:|------------------------:|--------------------:|
| base            | 0.729524 | 0.459048 | 0.37381 | 0.183753 |               -0.312157 |            0.64115  |
| pd_plus_5pp     | 0.729524 | 0.459048 | 0.37381 | 0.187894 |               -0.515507 |            0.690037 |
| pd_minus_5pp    | 0.727857 | 0.455714 | 0.37381 | 0.184378 |               -0.381066 |            0.265844 |
| odds_up_10pct   | 0.729524 | 0.459048 | 0.37381 | 0.185292 |               -0.373332 |            0.641168 |
| odds_down_10pct | 0.729524 | 0.459048 | 0.37381 | 0.182602 |               -0.244388 |            0.641141 |

## Limitations and production conditions

The source project uses a research credit dataset and a random holdout rather than genuine temporal validation. The source project also explicitly labels LGD/EAD as non-empirical. This validation therefore supports demonstration of validation methodology, not production approval, regulatory compliance, or institution-specific model governance.
