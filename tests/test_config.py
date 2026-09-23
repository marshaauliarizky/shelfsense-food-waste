from src.config import REQUIRED_COLUMNS, SUPPORTED_WASTE_REASONS


def test_config_exposes_schema_and_supported_waste_reasons():
    assert "transaction_id" in REQUIRED_COLUMNS
    assert "expiry_date" in REQUIRED_COLUMNS
    assert "expiry" in SUPPORTED_WASTE_REASONS
