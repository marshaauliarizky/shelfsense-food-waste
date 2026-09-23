import pandas as pd
import pytest


def base_row(transaction_id="TX-1", **overrides):
    row = {
        "transaction_id": transaction_id, "transaction_date": "2026-09-01",
        "transaction_time": "09:00", "branch": "Kemang", "product_id": "P-1",
        "product_name": "Croissant", "category": "pastry", "production_qty": 20,
        "sold_qty": 12, "waste_qty": 4, "stock_qty": 4, "unit_price": 20_000,
        "unit_cost": 8_000, "discount_pct": 0, "expiry_date": "2026-09-02",
        "shelf_life_days": 2, "forecast_qty": 14, "weather": "clear",
        "event_flag": 0, "waste_reason": "expiry",
    }
    row.update(overrides)
    return row


@pytest.fixture
def valid_frame():
    return pd.DataFrame([base_row()])


@pytest.fixture
def sample_frame():
    return pd.DataFrame([base_row()])
