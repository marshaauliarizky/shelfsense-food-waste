from src.charts import daily_sales_waste_chart
from src.ui_components import format_currency


def test_format_currency_uses_indonesian_display_format():
    assert format_currency(1_250_000) == "Rp1,25 jt"


def test_chart_function_returns_plotly_figure(sample_frame):
    figure = daily_sales_waste_chart(sample_frame)
    assert len(figure.data) >= 2
