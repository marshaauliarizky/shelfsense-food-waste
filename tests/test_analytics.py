from src.analytics import calculate_kpis, calculate_product_risk


def test_calculate_kpis_returns_waste_rate_and_estimated_loss(sample_frame):
    result = calculate_kpis(sample_frame)
    assert result["total_production"] == 20
    assert result["total_waste"] == 4
    assert result["waste_rate"] == 0.2
    assert result["estimated_loss"] == 32_000


def test_calculate_kpis_handles_zero_production(sample_frame):
    result = calculate_kpis(sample_frame.assign(production_qty=0))
    assert result["waste_rate"] is None


def test_product_risk_includes_expiry_days(sample_frame):
    result = calculate_product_risk(sample_frame, "2026-09-01")
    assert result.iloc[0]["expiry_days"] == 1
    assert "forecast_qty" in result.columns
