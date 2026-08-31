# Illustrative validation policy

This document defines the transparent thresholds used by the repository. They are project assumptions, not a bank's or regulator's policy.

## Model tiering

The validated PD model is treated as an illustrative **Tier 1** model because credit-risk parameters can influence underwriting/risk classification and feed expected-credit-loss analytics. A real institution would apply its own materiality, complexity, usage and regulatory criteria.

## Core tests

- discrimination: ROC-AUC, Gini, KS and bootstrap uncertainty;
- calibration: Brier score, calibration intercept and calibration slope;
- stability: PSI from the source pipeline;
- benchmarking: primary-versus-challenger discrimination and calibration;
- outcomes: segment-level AUC/default rate/Brier analysis;
- sensitivity: additive-PD and multiplicative-odds perturbations;
- validation design: data representativeness, temporal validation and scope boundaries.

## Illustrative thresholds

AUC below 0.70 triggers a high-severity finding. Calibration slope outside 0.80-1.20 triggers high severity. Absolute calibration intercept above 0.25 triggers medium severity. PSI 0.10-0.25 is medium and >=0.25 is high. Challenger AUC improvement of at least 0.02 triggers a model-selection finding. Absence of genuine out-of-time validation is treated as high severity for a production-use claim.
