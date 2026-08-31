import numpy as np
import pandas as pd

from src.metrics import bootstrap_auc_ci, validation_metrics


def test_metrics_perfect_ranking():
    y = pd.Series([0, 0, 1, 1])
    p = pd.Series([0.05, 0.20, 0.80, 0.95])
    m = validation_metrics(y, p)
    assert m["auc"] == 1.0
    assert m["gini"] == 1.0
    assert m["ks"] == 1.0
    assert m["brier"] < 0.05


def test_bootstrap_ci_is_ordered():
    y = pd.Series([0,1] * 30)
    p = pd.Series(np.linspace(0.05, 0.95, 60))
    lo, hi = bootstrap_auc_ci(y, p, 100, 7)
    assert 0 <= lo <= hi <= 1
