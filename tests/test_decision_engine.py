import pandas as pd
from src.decision_engine import recommend_actions


def frame_for(expiry_days=1, stock_gap=11):
    return pd.DataFrame([{
        "product_id": "P-1", "product_name": "Croissant", "branch": "Kemang",
        "expiry_days": expiry_days, "stock_qty": max(stock_gap, 0) + 4,
        "forecast_qty": 4, "stock_gap": stock_gap, "waste_rate": 0.02,
        "sold_through_rate": 0.75, "unit_price": 20_000, "unit_cost": 8_000,
        "discount_pct": 0,
    }])


def test_near_expiry_surplus_gets_high_priority_markdown():
    result = recommend_actions(frame_for())[0]
    assert result["priority"] == "high"
    assert result["suggested_discount_pct"] == 20
    assert "expiry" in " ".join(result["evidence"]).lower()


def test_near_expiry_without_surplus_gets_no_markdown():
    result = recommend_actions(frame_for(stock_gap=0))[0]
    assert result["suggested_discount_pct"] is None
