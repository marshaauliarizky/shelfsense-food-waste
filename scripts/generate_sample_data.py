from datetime import date, timedelta
from pathlib import Path
import random
import pandas as pd

random.seed(42)
products = [
    ("P01", "Butter Croissant", "pastry", 2, 24000, 9000),
    ("P02", "Chocolate Croissant", "pastry", 2, 26000, 10000),
    ("P03", "Sourdough Loaf", "bread", 3, 42000, 17000),
    ("P04", "Milk Bun", "bread", 2, 18000, 7000),
    ("P05", "Banana Bread", "bread", 4, 30000, 12000),
    ("P06", "Tiramisu Cup", "cake", 2, 38000, 16000),
    ("P07", "Carrot Cake Slice", "cake", 3, 32000, 13000),
    ("P08", "Chicken Puff", "savory", 1, 28000, 11000),
    ("P09", "Mushroom Quiche", "savory", 2, 34000, 14000),
    ("P10", "Cinnamon Roll", "pastry", 2, 25000, 9500),
    ("P11", "Matcha Financier", "pastry", 3, 22000, 8500),
    ("P12", "Cheese Danish", "pastry", 2, 27000, 10500),
]
branches = {"Kemang": 1.0, "Senopati": 1.18, "BSD": 0.82}
rows = []
start = date(2026, 7, 28)
for day_offset in range(57):
    current = start + timedelta(days=day_offset)
    weekend = current.weekday() >= 5
    for branch, branch_factor in branches.items():
        for product_id, name, category, shelf_life, price, cost in products:
            base = {"pastry": 28, "bread": 20, "cake": 12, "savory": 18}[category]
            demand = base * branch_factor * (1.22 if weekend else 1.0)
            if name == "Sourdough Loaf" and weekend:
                demand *= 1.18
            if name == "Chicken Puff" and current.weekday() == 2:
                demand *= 0.72
            if current.day in (5, 15, 25):
                demand *= 1.12
            rain = random.random() < 0.25
            if rain:
                demand *= 0.86
            production = max(1, round(demand * random.uniform(1.02, 1.25)))
            if name in ("Chocolate Croissant", "Mushroom Quiche") and current.weekday() == 1:
                production += 8
            sold = min(production, max(0, round(random.gauss(demand, max(2, demand * 0.12)))))
            waste = max(0, production - sold - random.randint(0, min(2, max(0, production - sold))))
            stock = production - sold - waste
            markdown = 20 if stock > demand * 0.35 and shelf_life <= 2 else (10 if stock > demand * 0.25 else 0)
            expiry = current + timedelta(days=shelf_life)
            rows.append({
                "transaction_id": f"TX-{day_offset:03d}-{branch[:2]}-{product_id}",
                "transaction_date": current.isoformat(), "transaction_time": "09:00",
                "branch": branch, "product_id": product_id, "product_name": name,
                "category": category, "production_qty": production, "sold_qty": sold,
                "waste_qty": waste, "stock_qty": stock, "unit_price": price,
                "unit_cost": cost, "discount_pct": markdown, "expiry_date": expiry.isoformat(),
                "shelf_life_days": shelf_life, "forecast_qty": round(demand, 2),
                "weather": "rain" if rain else "clear", "event_flag": int(current.day in (5, 15, 25)),
                "waste_reason": "expiry" if waste and shelf_life <= 2 else ("overproduction" if waste else None),
                "actual_markdown_revenue": round(sold * price * (1 - markdown / 100), 2),
            })
Path("data").mkdir(exist_ok=True)
pd.DataFrame(rows).to_excel("data/sample_food_waste.xlsx", index=False)
print(f"wrote {len(rows)} rows")
