from dataclasses import dataclass
from pathlib import Path
import re
import pandas as pd

from .config import NUMERIC_COLUMNS, REQUIRED_COLUMNS


@dataclass
class ValidationReport:
    clean_frame: pd.DataFrame
    valid_rows: int
    rejected_rows: int
    duplicate_count: int
    missing_columns: list[str]
    errors: list[str]


def _normalize_column(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def validate_dataframe(frame: pd.DataFrame) -> ValidationReport:
    data = frame.copy()
    data.columns = [_normalize_column(c) for c in data.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        return ValidationReport(data.iloc[0:0], 0, len(data), 0, missing, [f"Missing required columns: {', '.join(missing)}"])

    for column in ("forecast_qty", "weather", "event_flag", "waste_reason", "actual_markdown_revenue"):
        if column not in data.columns:
            data[column] = None
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data["transaction_date"] = pd.to_datetime(data["transaction_date"], errors="coerce").dt.date
    data["expiry_date"] = pd.to_datetime(data["expiry_date"], errors="coerce").dt.date
    errors = []
    invalid = pd.Series(False, index=data.index)
    for column in NUMERIC_COLUMNS:
        if column in {"forecast_qty", "actual_markdown_revenue"} and data[column].isna().all():
            continue
        bad = data[column].isna()
        if bad.any():
            invalid |= bad
            errors.append(f"Invalid numeric value in {column}")
    quantity_cols = ["production_qty", "sold_qty", "waste_qty", "stock_qty"]
    negative = data[quantity_cols].lt(0).any(axis=1)
    if negative.any():
        invalid |= negative
        errors.append("Quantity cannot be negative")
    over = data["sold_qty"] + data["waste_qty"] > data["production_qty"]
    if over.any():
        invalid |= over
        errors.append("Sold and waste quantities cannot exceed production")
    if data["discount_pct"].lt(0).any() or data["discount_pct"].gt(100).any():
        invalid |= data["discount_pct"].lt(0) | data["discount_pct"].gt(100)
        errors.append("Discount percentage must be between 0 and 100")
    if data["unit_price"].le(0).any() or data["unit_cost"].le(0).any():
        invalid |= data["unit_price"].le(0) | data["unit_cost"].le(0)
        errors.append("Unit price and unit cost must be greater than zero")
    duplicate_mask = data["transaction_id"].duplicated(keep=False)
    duplicate_count = int(data["transaction_id"].duplicated().sum())
    if duplicate_mask.any():
        invalid |= duplicate_mask
        errors.append("Duplicate transaction_id detected")
    blank = data[["transaction_id", "branch", "product_id", "product_name"]].isna().any(axis=1)
    if blank.any():
        invalid |= blank
        errors.append("Required text fields cannot be blank")
    clean = data.loc[~invalid].reset_index(drop=True)
    return ValidationReport(clean, len(clean), int(invalid.sum()), duplicate_count, [], errors)


def load_excel(path: str | Path) -> ValidationReport:
    return validate_dataframe(pd.read_excel(path))
