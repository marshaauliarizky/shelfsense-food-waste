from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analytics import calculate_kpis, calculate_product_risk
from src.database import fetch_transactions
from src.decision_engine import recommend_actions


DATABASE = ROOT / "data" / "shelfsense.db"
OUTPUT = ROOT / "exports" / "ShelfSense_demo_workbook.xlsx"


def export_workbook():
    frame = fetch_transactions(DATABASE)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    kpis = calculate_kpis(frame)
    kpi_frame = pd.DataFrame([{"metric": key, "value": value} for key, value in kpis.items()])
    waste = frame.groupby(["product_name", "category"], as_index=False).agg(
        production_qty=("production_qty", "sum"), sold_qty=("sold_qty", "sum"),
        waste_qty=("waste_qty", "sum"), estimated_loss=("unit_cost", lambda costs: 0),
    )
    loss = frame.assign(estimated_loss=frame["waste_qty"] * frame["unit_cost"]).groupby("product_name", as_index=False)["estimated_loss"].sum()
    waste = waste.drop(columns="estimated_loss").merge(loss, on="product_name", how="left")
    risk = calculate_product_risk(frame, "2026-09-22")
    recommendations = pd.DataFrame(recommend_actions(risk))
    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        frame.to_excel(writer, sheet_name="Transactions", index=False)
        kpi_frame.to_excel(writer, sheet_name="KPI Summary", index=False)
        waste.to_excel(writer, sheet_name="Waste by Product", index=False)
        recommendations.to_excel(writer, sheet_name="Recommendations", index=False)
    return OUTPUT


if __name__ == "__main__":
    print(export_workbook())
