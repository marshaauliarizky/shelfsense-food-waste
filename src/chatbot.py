from dataclasses import dataclass
import pandas as pd
from .analytics import calculate_kpis, calculate_product_risk
from .decision_engine import recommend_actions


@dataclass
class ChatResponse:
    text: str
    intent: str | None
    supported: bool


def answer_question(question, frame, as_of_date):
    text = question.lower().strip()
    if "most waste" in text or "paling banyak terbuang" in text:
        grouped = frame.groupby("product_name", as_index=False)["waste_qty"].sum().sort_values("waste_qty", ascending=False)
        row = grouped.iloc[0]
        return ChatResponse(f"{row.product_name} has the most waste: {int(row.waste_qty)} units in the available data.", "top_waste_product", True)
    if "highest waste" in text or "waste rate tertinggi" in text:
        grouped = frame.groupby("branch").apply(lambda x: x.waste_qty.sum() / x.production_qty.sum()).sort_values(ascending=False)
        return ChatResponse(f"{grouped.index[0]} has the highest waste rate at {grouped.iloc[0]:.1%}.", "highest_waste_branch", True)
    if "loss" in text or "kerugian" in text:
        kpi = calculate_kpis(frame)
        return ChatResponse(f"Estimated loss for the selected data is Rp{kpi['estimated_loss']:,.0f}.", "estimated_loss_period", True)
    if "markdown" in text or "promo" in text:
        recs = [r for r in recommend_actions(calculate_product_risk(frame, as_of_date)) if r["suggested_discount_pct"]]
        answer = "No markdown recommendation for the selected data." if not recs else "; ".join(f"{r['product_name']} {r['suggested_discount_pct']}%" for r in recs[:3])
        return ChatResponse(answer, "today_markdown_recommendations", True)
    if "compare" in text and "branch" in text:
        grouped = frame.groupby("branch").apply(lambda x: x.waste_qty.sum() / x.production_qty.sum()).sort_values()
        return ChatResponse("Branch waste-rate comparison: " + ", ".join(f"{name} {rate:.1%}" for name, rate in grouped.items()), "highest_waste_branch", True)
    if "weekday" in text or "weekend" in text:
        dates = pd.to_datetime(frame["transaction_date"])
        weekend = frame.loc[dates.dt.weekday >= 5, "sold_qty"].mean()
        weekday = frame.loc[dates.dt.weekday < 5, "sold_qty"].mean()
        return ChatResponse(f"Average units sold: weekday {weekday:.1f}, weekend {weekend:.1f}.", "weekday_weekend_comparison", True)
    if "why" in text or "kenapa" in text:
        name = next((value for value in frame["product_name"].unique() if value.lower() in text), None)
        if name:
            subset = frame[frame["product_name"] == name]
            return ChatResponse(f"{name} is flagged because its waste rate is {(subset.waste_qty.sum() / subset.production_qty.sum()):.1%} in the selected data.", "product_reason", True)
    return ChatResponse("I can answer supported questions about waste, branches, estimated loss, markdowns, and product drivers.", None, False)
