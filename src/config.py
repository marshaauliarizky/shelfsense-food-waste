from pathlib import Path

DEFAULT_DB_PATH = Path("data") / "shelfsense.db"

REQUIRED_COLUMNS = (
    "transaction_id", "transaction_date", "transaction_time", "branch",
    "product_id", "product_name", "category", "production_qty", "sold_qty",
    "waste_qty", "stock_qty", "unit_price", "unit_cost", "discount_pct",
    "expiry_date", "shelf_life_days",
)

SUPPORTED_WASTE_REASONS = ("expiry", "overproduction", "damage", "quality_issue")

NUMERIC_COLUMNS = (
    "production_qty", "sold_qty", "waste_qty", "stock_qty", "unit_price",
    "unit_cost", "discount_pct", "shelf_life_days", "forecast_qty",
    "actual_markdown_revenue",
)
