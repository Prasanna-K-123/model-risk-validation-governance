from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score, roc_curve


def ks_statistic(y: pd.Series, p: pd.Series) -> float:
    fpr, tpr, _ = roc_curve(y, p)
    return float(np.max(tpr - fpr))


def calibration_parameters(y: pd.Series, p: pd.Series) -> tuple[float, float]:
    eps = 1e-6
    clipped = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    logit = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=2000)
    model.fit(logit, np.asarray(y, dtype=int))
    return float(model.intercept_[0]), float(model.coef_[0][0])


def validation_metrics(y: pd.Series, p: pd.Series) -> dict:
    auc = float(roc_auc_score(y, p))
    intercept, slope = calibration_parameters(y, p)
    return {
        "auc": auc,
        "gini": 2 * auc - 1,
        "ks": ks_statistic(y, p),
        "brier": float(brier_score_loss(y, p)),
        "calibration_intercept": intercept,
        "calibration_slope": slope,
    }


def bootstrap_auc_ci(y: pd.Series, p: pd.Series, n_boot: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    yv = np.asarray(y)
    pv = np.asarray(p)
    aucs: list[float] = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(yv), len(yv))
        ys = yv[idx]
        if len(np.unique(ys)) < 2:
            continue
        aucs.append(float(roc_auc_score(ys, pv[idx])))
    if not aucs:
        raise ValueError("Unable to bootstrap AUC")
    return float(np.quantile(aucs, 0.025)), float(np.quantile(aucs, 0.975))


def segment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["age_segment"] = pd.cut(work["age"], [-np.inf, 29, 44, np.inf], labels=["<=29", "30-44", "45+"])
    work["amount_segment"] = pd.qcut(work["amount"], 3, labels=["low", "mid", "high"], duplicates="drop")
    rows = []
    for dimension in ["age_segment", "amount_segment"]:
        for segment, sample in work.groupby(dimension, observed=True):
            if sample["observed_default"].nunique() < 2:
                continue
            m = validation_metrics(sample["observed_default"], sample["pd_scorecard"])
            rows.append({"dimension": dimension, "segment": str(segment), "n": len(sample), "default_rate": sample["observed_default"].mean(), "auc": m["auc"], "brier": m["brier"]})
    return pd.DataFrame(rows)


def sensitivity_analysis(y: pd.Series, p: pd.Series) -> pd.DataFrame:
    eps = 1e-6
    base = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    odds = base / (1 - base)
    scenarios = {
        "base": base,
        "pd_plus_5pp": np.clip(base + 0.05, eps, 1 - eps),
        "pd_minus_5pp": np.clip(base - 0.05, eps, 1 - eps),
        "odds_up_10pct": np.clip((odds * 1.10) / (1 + odds * 1.10), eps, 1 - eps),
        "odds_down_10pct": np.clip((odds * 0.90) / (1 + odds * 0.90), eps, 1 - eps),
    }
    rows = []
    for name, probs in scenarios.items():
        m = validation_metrics(y, pd.Series(probs))
        rows.append({"scenario": name, **m})
    return pd.DataFrame(rows)
