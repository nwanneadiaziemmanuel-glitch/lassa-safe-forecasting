"""Reproduce the leakage-controlled core forecasting analysis.

Usage from the repository root:
    python -m src.run_analysis --data data/lassa_fever_timeseries_full.csv
"""
from pathlib import Path
import argparse
import json

import pandas as pd

from .preprocessing import load_weekly_data, audit_weekly_data
from .features import make_features
from .forecasting import rolling_year_evaluation


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/lassa_fever_timeseries_full.csv")
    ap.add_argument("--out", default="results/v1_1_core")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = load_weekly_data(args.data)
    audit = audit_weekly_data(df)
    (out / "audit_summary.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    feat, _ = make_features(df)
    feat.to_csv(out / "feature_matrix.csv", index=False)

    frames = [rolling_year_evaluation(df, horizon=h) for h in (1, 2, 3, 4)]
    forecast = pd.concat(frames, ignore_index=True)
    forecast.to_csv(out / "forecast_reproduction.csv", index=False)
    print(json.dumps(audit, indent=2))
    print("Wrote:", out)


if __name__ == "__main__":
    main()
