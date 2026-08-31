from __future__ import annotations

from io import StringIO
import json
import time

import pandas as pd
import requests

from src.config import METRICS_URL, PREDICTIONS_URL


def _get(url: str) -> str:
    last_error = None
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=(10, 30), headers={"User-Agent": "independent-model-validation/1.0"})
            response.raise_for_status()
            return response.text
        except Exception as exc:
            last_error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Unable to retrieve pinned source evidence: {last_error}")


def load_source_evidence() -> tuple[pd.DataFrame, dict]:
    predictions = pd.read_csv(StringIO(_get(PREDICTIONS_URL)))
    metrics = json.loads(_get(METRICS_URL))
    required = {"observed_default", "pd_scorecard", "pd_challenger", "duration", "amount", "age"}
    missing = required.difference(predictions.columns)
    if missing:
        raise ValueError(f"Missing source prediction fields: {sorted(missing)}")
    if len(predictions) < 100:
        raise ValueError("Holdout sample is too small for this validation workflow")
    if not predictions["observed_default"].isin([0, 1]).all():
        raise ValueError("Outcome must be binary")
    for col in ["pd_scorecard", "pd_challenger"]:
        if not predictions[col].between(0, 1).all():
            raise ValueError(f"{col} contains invalid probabilities")
    return predictions, metrics
