from pathlib import Path
import sys
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.database import fetch_transactions

frame = fetch_transactions(ROOT / "data" / "shelfsense.db")
frame["transaction_date"] = pd.to_datetime(frame["transaction_date"])
output = ROOT / "assets"
output.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.facecolor": "#fffdf8", "figure.facecolor": "#f7f4ed"})

trend = frame.groupby("transaction_date", as_index=False).agg(sold=("sold_qty", "sum"), waste=("waste_qty", "sum"))
fig, ax = plt.subplots(figsize=(12, 5), dpi=160)
ax.plot(trend.transaction_date, trend.sold, color="#587568", linewidth=2.5, label="Sold")
ax.plot(trend.transaction_date, trend.waste, color="#c48638", linewidth=2.5, label="Waste")
ax.set_title("Sales and waste trend", loc="left", color="#243029", weight="bold")
ax.set_ylabel("Units")
ax.grid(axis="y", color="#e4e0d6", linewidth=.8)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, ncol=2, loc="upper left")
fig.tight_layout()
fig.savefig(output / "chart-sales-waste.png", bbox_inches="tight")
plt.close(fig)

reasons = frame.groupby("waste_reason", dropna=False)["waste_qty"].sum().sort_values(ascending=False)
reasons.index = reasons.index.fillna("Unspecified")
fig, ax = plt.subplots(figsize=(8, 5), dpi=160)
ax.bar(reasons.index, reasons.values, color="#c48638", width=.58)
ax.set_title("Waste by recorded reason", loc="left", color="#243029", weight="bold")
ax.set_ylabel("Units")
ax.tick_params(axis="x", rotation=18)
ax.grid(axis="y", color="#e4e0d6", linewidth=.8)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(output / "chart-waste-reasons.png", bbox_inches="tight")
plt.close(fig)

print("Chart images exported to", output)
