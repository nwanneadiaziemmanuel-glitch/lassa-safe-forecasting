
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "week_start_date","week_end_date","epi_year","epi_week",
    "suspected_cases","confirmed_cases","probable_cases","deaths"
]

def load_weekly_data(path):
    df = pd.read_csv(path, parse_dates=["week_start_date","week_end_date"])
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df.sort_values("week_start_date").reset_index(drop=True)

def audit_weekly_data(df):
    out = {
        "rows": len(df),
        "columns": len(df.columns),
        "date_min": str(df["week_start_date"].min().date()),
        "date_max": str(df["week_start_date"].max().date()),
        "missing_total": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_week_starts": int(df["week_start_date"].duplicated().sum()),
        "negative_counts": int((df[["suspected_cases","confirmed_cases","probable_cases","deaths"]] < 0).sum().sum()),
        "confirmed_gt_suspected": int((df["confirmed_cases"] > df["suspected_cases"]).sum()),
        "probable_gt_suspected": int((df["probable_cases"] > df["suspected_cases"]).sum()),
        "deaths_gt_confirmed_plus_probable": int((df["deaths"] > df["confirmed_cases"] + df["probable_cases"]).sum()),
        "date_gaps_not_7d": int((df["week_start_date"].diff().dt.days.dropna() != 7).sum()),
        "week_end_mismatch": int(((df["week_end_date"] - df["week_start_date"]).dt.days != 6).sum()),
    }
    if "extraction_method" in df:
        out["extraction_counts"] = df["extraction_method"].value_counts().to_dict()
    return out

def save_audit(df, output_json):
    import json
    Path(output_json).write_text(json.dumps(audit_weekly_data(df), indent=2), encoding="utf-8")
