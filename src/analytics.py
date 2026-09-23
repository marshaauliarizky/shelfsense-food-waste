import pandas as pd


def _ratio(numerator, denominator):
    return None if denominator == 0 else numerator / denominator


def calculate_kpis(frame: pd.DataFrame) -> dict:
    production = float(frame["production_qty"].sum())
    sold = float(frame["sold_qty"].sum())
    waste = float(frame["waste_qty"].sum())
    return {
        "total_production": int(production), "total_sold": int(sold), "total_waste": int(waste),
        "sold_through_rate": _ratio(sold, production), "waste_rate": _ratio(waste, production),
        "estimated_loss": float((frame["waste_qty"] * frame["unit_cost"]).sum()),
        "gross_revenue": float((frame["sold_qty"] * frame["unit_price"] * (1 - frame["discount_pct"] / 100)).sum()),
        "at_risk_products": int(frame["product_id"].nunique()),
    }


def calculate_daily_trend(frame):
    result = frame.copy()
    result["transaction_date"] = pd.to_datetime(result["transaction_date"])
    return result.groupby("transaction_date", as_index=False).agg(
        sold_qty=("sold_qty", "sum"), waste_qty=("waste_qty", "sum"), production_qty=("production_qty", "sum")
    ).sort_values("transaction_date")


def moving_average_forecast(frame, periods=7):
    result = frame.copy()
    result["transaction_date"] = pd.to_datetime(result["transaction_date"])
    result = result.sort_values("transaction_date")
    result["forecast_qty"] = result.groupby(["branch", "product_id"])["sold_qty"].transform(
        lambda values: values.shift(1).rolling(periods, min_periods=1).mean().fillna(values.mean())
    )
    return result


def calculate_product_risk(frame, as_of_date):
    result = moving_average_forecast(frame)
    result["expiry_date"] = pd.to_datetime(result["expiry_date"])
    result["expiry_days"] = (result["expiry_date"] - pd.Timestamp(as_of_date)).dt.days
    result["stock_gap"] = result["stock_qty"] - result["forecast_qty"]
    result["waste_rate"] = result.apply(lambda row: _ratio(row.waste_qty, row.production_qty), axis=1)
    result["sold_through_rate"] = result.apply(lambda row: _ratio(row.sold_qty, row.production_qty), axis=1)
    return result


def compare_periods(frame, current_start, current_end, previous_start, previous_end):
    dates = pd.to_datetime(frame["transaction_date"])
    current = frame.loc[(dates >= pd.Timestamp(current_start)) & (dates <= pd.Timestamp(current_end))].copy()
    previous = frame.loc[(dates >= pd.Timestamp(previous_start)) & (dates <= pd.Timestamp(previous_end))].copy()
    return pd.DataFrame([{"period": "current", **calculate_kpis(current)}, {"period": "previous", **calculate_kpis(previous)}])
