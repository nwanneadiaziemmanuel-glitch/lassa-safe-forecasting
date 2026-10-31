from src.preprocessing import load_weekly_data, audit_weekly_data


def test_weekly_audit():
    df = load_weekly_data("data/lassa_fever_timeseries_full.csv")
    a = audit_weekly_data(df)
    assert a["rows"] == 307
    assert a["missing_total"] == 0
    assert a["duplicate_week_starts"] == 0
    assert a["date_gaps_not_7d"] == 0
