import pandas as pd


def recommend_discount(expiry_days, stock_gap):
    if stock_gap <= 0:
        return None
    if expiry_days <= 1:
        return 20
    if expiry_days == 2:
        return 10
    return None


def recommend_actions(risk_frame: pd.DataFrame) -> list[dict]:
    recommendations = []
    for _, row in risk_frame.iterrows():
        discount = recommend_discount(row.get("expiry_days", 99), row.get("stock_gap", 0))
        evidence = []
        issue = "No immediate action"
        action = "Keep current production and pricing"
        priority = "no_action"
        if discount:
            priority = "high" if row.expiry_days <= 1 else "watch"
            issue = "Inventory may remain unsold before expiry"
            action = f"Apply a {discount}% markdown during the markdown window"
            evidence = [f"{int(row.stock_gap)} units above forecast", f"{int(row.expiry_days)} expiry days remaining"]
        elif row.get("waste_rate", 0) > 0.10:
            priority, issue, action = "watch", "Waste rate is persistently high", "Review production quantity for the next cycle"
            evidence = [f"Waste rate {row.waste_rate:.0%}"]
        elif row.get("sold_through_rate", 1) < 0.50 and row.get("discount_pct", 0) >= 20:
            priority, issue, action = "watch", "Product remains slow-moving after discount", "Review assortment and baseline demand"
            evidence = [f"Sold-through {row.sold_through_rate:.0%}", f"Discount {row.discount_pct:.0f}%"]
        estimated_units = max(float(row.get("stock_gap", 0)), 0) * (0.65 if discount else 0)
        estimated_revenue = estimated_units * float(row.get("unit_price", 0)) * (1 - (discount or 0) / 100)
        recommendations.append({
            "product_id": row.product_id, "product_name": row.product_name, "branch": row.branch,
            "priority": priority, "issue": issue, "evidence": evidence, "action": action,
            "suggested_discount_pct": discount, "estimated_units_saved": estimated_units,
            "estimated_revenue": estimated_revenue,
        })
    order = {"high": 0, "watch": 1, "no_action": 2}
    return sorted(recommendations, key=lambda item: order[item["priority"]])
