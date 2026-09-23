# ShelfSense

ShelfSense is a portfolio project for food-waste prevention and markdown planning in bakery operations. It turns simulated production, sales, stock, expiry, and markdown records into operational views and explainable recommendations.

## Live Demo

Try the deployed Streamlit app here: [ShelfSense Live Demo](https://shelfsense-food-waste.streamlit.app/)

## Run locally

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

The optional document and presentation build scripts use `requirements-build.txt`.

The app loads `data/sample_food_waste.xlsx` into a local SQLite database on first run. The dataset is simulated and is not connected to a real business.

## What it demonstrates

- Excel validation and SQLite persistence.
- KPI calculation for production, sold-through, waste rate, revenue, and estimated loss.
- Waste monitoring by product, branch, and reason.
- Explainable markdown and production recommendations.
- A bounded chatbot that answers from current data only.
- Streamlit UI designed as a bakery operations console rather than an AI chat demo.
- Editorial bakery imagery in `assets/` for a more recognizable product experience.

## Architecture

`data_loader.py` validates incoming Excel files. `database.py` persists clean rows. `analytics.py` calculates metrics and moving-average baselines. `decision_engine.py` applies deterministic rules. `chatbot.py` maps supported questions to those analytics functions. `charts.py` and `ui.py` keep presentation concerns separate from the data logic.

See [`docs/PROJECT_MAP.md`](docs/PROJECT_MAP.md) for a guided explanation of the folder structure.

For usage instructions, see [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md). For the business explanation and interpretation of results, see [`docs/PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md).

The full Word documentation is available at [`docs/ShelfSense_Project_Documentation.docx`](docs/ShelfSense_Project_Documentation.docx).

The portfolio presentation is available at [`docs/ShelfSense_Portfolio_Deck_v2.pptx`](docs/ShelfSense_Portfolio_Deck_v2.pptx).

For publishing guidance, see [`docs/DEPLOYMENT_CHECKLIST.md`](docs/DEPLOYMENT_CHECKLIST.md).

For a complete explanation of the project, see [`docs/PROJECT_WALKTHROUGH.md`](docs/PROJECT_WALKTHROUGH.md).

## Export workbook

The project includes [`exports/ShelfSense_demo_workbook.xlsx`](exports/ShelfSense_demo_workbook.xlsx). It contains transaction data, KPI summary, waste by product, and recommendations in separate sheets so the simulated analysis can be reviewed outside the app.

## KPI definitions

- Sold-through rate = sold quantity / production quantity.
- Waste rate = waste quantity / production quantity.
- Estimated loss = waste quantity × unit cost.
- Stock gap = current stock − demand baseline.

Undefined ratios are displayed as `—`. Recommendations are estimates; actual manager decisions and outcomes are stored separately.

## References

- [UNEP Food Waste Index Report 2024](https://www.unep.org/resources/publication/food-waste-index-report-2024)
- [U.S. Food Waste Pact Data Report](https://foodwastepact.refed.org/resources/2025-data-report/)
- [Dynamic Pricing and Organic Waste Bans](https://pubsonline.informs.org/doi/10.1287/mksc.2020.0214)

## Test

```powershell
python -m pytest -q
```

The first run may create `data/shelfsense.db`; it is a local demo artifact.
