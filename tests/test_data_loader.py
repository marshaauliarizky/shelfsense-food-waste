import pandas as pd
from src.data_loader import validate_dataframe
from tests.conftest import base_row


def test_validation_rejects_negative_quantity():
    report = validate_dataframe(pd.DataFrame([base_row(production_qty=-1)]))
    assert report.valid_rows == 0
    assert "quantity cannot be negative" in report.errors[0].lower()


def test_validation_rejects_duplicate_transaction_id():
    report = validate_dataframe(pd.DataFrame([base_row(), base_row()]))
    assert report.valid_rows == 0
    assert report.duplicate_count == 1


def test_validation_rejects_missing_column():
    row = base_row()
    row.pop("expiry_date")
    report = validate_dataframe(pd.DataFrame([row]))
    assert "expiry_date" in report.missing_columns


def test_validation_rejects_sold_and_waste_above_production():
    report = validate_dataframe(pd.DataFrame([base_row(sold_qty=18, waste_qty=5)]))
    assert report.valid_rows == 0
    assert "cannot exceed production" in report.errors[0].lower()
