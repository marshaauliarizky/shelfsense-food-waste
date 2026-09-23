# ShelfSense MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished local Streamlit portfolio demo that imports simulated bakery operations data, calculates food-waste metrics, explains operational risks, recommends markdown or production actions, and answers a limited set of data-backed questions.

**Architecture:** Use a structured Streamlit application backed by SQLite. Keep data loading, persistence, analytics, decision rules, chatbot intent handling, charts, and UI components in separate modules so each boundary can be tested independently. Use deterministic rules and moving averages for the MVP; label all simulated data and estimated impact clearly.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, SQLite, Plotly, openpyxl, pytest.

**Spec:** `docs/superpowers/specs/2026-09-22-shelfsense-design.md`

## Global Constraints

- The application is a local portfolio demo and must label all sample data as simulated/demo data.
- No production ML forecasting, external POS integration, payment integration, or unrestricted LLM access is part of the MVP.
- Quantity values cannot be negative; `sold_qty + waste_qty` cannot exceed `production_qty` for a daily record.
- `discount_pct` must be between 0 and 100; `unit_price` and `unit_cost` must be greater than 0.
- Estimated impact must remain visually and semantically separate from actual outcomes.
- Chatbot responses must be generated from supported intents and current application data.
- New production behavior must follow TDD: write a failing test, verify the failure, implement the minimum behavior, then run the relevant and full test suites.

## Review Focus

- Invalid Excel rows must be rejected with actionable reasons without partially corrupting the database; test in Task 2.
- Zero production must not produce infinity, NaN, or a crash in KPI calculations; test in Task 3.
- A product with near expiry but no surplus must not receive a markdown recommendation; test in Task 4.
- Estimated markdown impact must never be presented as an actual result; test the output contract in Task 4 and the display in Task 6.
- Unsupported chatbot questions must receive a bounded fallback instead of invented numbers; test in Task 5.

## File Structure

Create these files:

```text
app.py
src/__init__.py
src/config.py
src/database.py
src/data_loader.py
src/analytics.py
src/decision_engine.py
src/chatbot.py
src/charts.py
src/ui.py
data/sample_food_waste.xlsx
tests/conftest.py
tests/test_config.py
tests/test_data_loader.py
tests/test_database.py
tests/test_analytics.py
tests/test_decision_engine.py
tests/test_chatbot.py
tests/test_charts.py
tests/test_integration.py
requirements.txt
README.md
```

### Task 1: Project Scaffold and Configuration

**Files:** Create `requirements.txt`, `src/__init__.py`, `src/config.py`, `tests/conftest.py`, and `tests/test_config.py`.

**Interfaces:** Produce `src.config.REQUIRED_COLUMNS`, `src.config.DEFAULT_DB_PATH`, and `src.config.SUPPORTED_WASTE_REASONS` for later modules.

- [ ] **Step 1: Write the failing test**

```python
from src.config import REQUIRED_COLUMNS, SUPPORTED_WASTE_REASONS


def test_config_exposes_schema_and_supported_waste_reasons():
    assert "transaction_id" in REQUIRED_COLUMNS
    assert "expiry_date" in REQUIRED_COLUMNS
    assert "expiry" in SUPPORTED_WASTE_REASONS
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_config.py -v`  
Expected: FAIL because `src.config` does not exist.

- [ ] **Step 3: Write minimal implementation**

Define the required columns from the spec, supported reasons `expiry`, `overproduction`, `damage`, and `quality_issue`, and a database path defaulting to `data/shelfsense.db` while allowing a caller-provided path.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_config.py -v`  
Expected: PASS.

- [ ] **Step 5: Add dependencies and run the suite**

Write `requirements.txt` with Streamlit, Pandas, Plotly, openpyxl, and pytest. Run `python -m pytest -q`; expected result is PASS.

### Task 2: SQLite Persistence and Excel Validation

**Files:** Create `src/database.py`, `src/data_loader.py`, `tests/test_database.py`, and `tests/test_data_loader.py`.

**Interfaces:**

- `data_loader.validate_dataframe(frame) -> ValidationReport`
- `data_loader.load_excel(path) -> ValidationReport`
- `database.initialize_database(path) -> None`
- `database.insert_transactions(path, frame) -> int`
- `database.fetch_transactions(path) -> pandas.DataFrame`
- `database.insert_manager_decision(path, decision) -> int`

- [ ] **Step 1: Write failing validation tests**

Test that negative quantities, missing required columns, duplicate `transaction_id`, and `sold_qty + waste_qty > production_qty` are rejected with row-level error messages and excluded from `clean_frame`. Define a `base_row` fixture in `tests/conftest.py`.

```python
def test_validation_rejects_negative_quantity():
    frame = pd.DataFrame([base_row("TX-1", production_qty=-1)])
    report = validate_dataframe(frame)
    assert report.valid_rows == 0
    assert "quantity cannot be negative" in report.errors[0].lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_data_loader.py -v`  
Expected: FAIL because `ValidationReport` and validation functions do not exist.

- [ ] **Step 3: Implement the loader**

Create a dataclass report containing `clean_frame`, `valid_rows`, `rejected_rows`, `duplicate_count`, `missing_columns`, and `errors`. Normalize column names to lowercase snake case, coerce dates and numeric fields, validate constraints, and preserve row-level reasons.

- [ ] **Step 4: Run validation tests**

Run: `python -m pytest tests/test_data_loader.py -v`  
Expected: PASS.

- [ ] **Step 5: Write the failing database round-trip test**

```python
def test_insert_transactions_round_trips_clean_rows(tmp_path, valid_frame):
    db_path = tmp_path / "shelfsense.db"
    initialize_database(db_path)
    inserted = insert_transactions(db_path, valid_frame)
    result = fetch_transactions(db_path)
    assert inserted == len(valid_frame)
    assert list(result["transaction_id"]) == ["TX-1"]
```

- [ ] **Step 6: Run the database test to verify it fails**

Run: `python -m pytest tests/test_database.py::test_insert_transactions_round_trips_clean_rows -v`  
Expected: FAIL because the SQLite layer does not exist.

- [ ] **Step 7: Implement the SQLite layer**

Create `transactions` and `manager_decisions` tables, use parameterized SQL, enforce a unique primary key on `transaction_id`, and wrap batch inserts in one transaction. Roll back the whole batch if insertion fails.

- [ ] **Step 8: Run the data-layer suite**

Run: `python -m pytest tests/test_data_loader.py tests/test_database.py -v`  
Expected: PASS.

### Task 3: Analytics and Simulated Dataset

**Files:** Create `src/analytics.py`, `data/sample_food_waste.xlsx`, and `tests/test_analytics.py`.

**Interfaces:**

- `calculate_kpis(frame) -> dict`
- `calculate_daily_trend(frame) -> pandas.DataFrame`
- `calculate_product_risk(frame, as_of_date) -> pandas.DataFrame`
- `moving_average_forecast(frame, periods=7) -> pandas.DataFrame`
- `compare_periods(frame, current_start, current_end, previous_start, previous_end) -> pandas.DataFrame`

- [ ] **Step 1: Write failing KPI tests**

```python
def test_calculate_kpis_returns_waste_rate_and_estimated_loss(sample_frame):
    result = calculate_kpis(sample_frame)
    assert result["total_production"] == 20
    assert result["total_waste"] == 4
    assert result["waste_rate"] == 0.2
    assert result["estimated_loss"] == 32_000


def test_calculate_kpis_handles_zero_production(sample_frame):
    result = calculate_kpis(sample_frame.assign(production_qty=0))
    assert result["waste_rate"] is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_analytics.py -v`  
Expected: FAIL because analytics functions do not exist.

- [ ] **Step 3: Implement KPI and trend functions**

Aggregate numeric fields, calculate sold-through rate, waste rate, estimated loss, gross revenue, and stock gap. Return `None` for undefined ratios. Keep date handling explicit and timezone-free.

- [ ] **Step 4: Add risk and forecast tests**

Assert that risk output includes `expiry_days`, `stock_gap`, and `forecast_qty`, and that the moving average uses only available records for each product/branch combination.

- [ ] **Step 5: Implement risk and moving-average functions**

Compute `expiry_days` from `expiry_date - as_of_date`, group demand by product and branch, and use a seven-day rolling mean with a minimum of one observation.

- [ ] **Step 6: Generate the simulated Excel dataset**

Create at least 8 weeks of records for Kemang, Senopati, and BSD with 10–15 products across pastry, bread, cake, and savory. Include weekday/weekend patterns, rainy-day variation, events, expiry risk, overproduction, stockouts, slow-moving items, and records before/after markdown. Ensure every row satisfies the loader constraints.

- [ ] **Step 7: Run analytics and dataset checks**

Run `python -m pytest tests/test_analytics.py -v`. Then run `python -c "from src.data_loader import load_excel; r=load_excel('data/sample_food_waste.xlsx'); print(r.valid_rows, r.rejected_rows)"`. Expected: tests pass and rejected rows equal zero.

### Task 4: Explainable Decision Engine

**Files:** Create `src/decision_engine.py` and `tests/test_decision_engine.py`.

**Interfaces:**

- `recommend_actions(risk_frame) -> list[dict]`
- `recommend_discount(expiry_days, stock_gap) -> float | None`

- [ ] **Step 1: Write failing rule tests**

```python
def test_near_expiry_surplus_gets_high_priority_markdown():
    recommendations = recommend_actions(frame_for(expiry_days=1, stock_gap=11))
    result = recommendations[0]
    assert result["priority"] == "high"
    assert result["suggested_discount_pct"] == 20
    assert "expiry" in " ".join(result["evidence"]).lower()


def test_near_expiry_without_surplus_gets_no_markdown():
    recommendations = recommend_actions(frame_for(expiry_days=1, stock_gap=0))
    assert recommendations[0]["suggested_discount_pct"] is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_decision_engine.py -v`  
Expected: FAIL because the decision engine does not exist.

- [ ] **Step 3: Implement deterministic rules**

Apply the five rules in the spec in stable priority order. Each recommendation must include issue, evidence, action, suggested discount, estimated units saved, and estimated revenue. Never store estimated values as actual results.

- [ ] **Step 4: Add edge-case tests**

Cover three consecutive high-waste days, consistent demand above forecast, high discount with low sell-through, and a healthy product that should return `no_action`.

- [ ] **Step 5: Run the decision-engine tests**

Run: `python -m pytest tests/test_decision_engine.py -v`  
Expected: PASS.

### Task 5: Bounded Chatbot Queries

**Files:** Create `src/chatbot.py` and `tests/test_chatbot.py`.

**Interfaces:**

- `answer_question(question, frame, as_of_date) -> ChatResponse`
- `ChatResponse.text: str`
- `ChatResponse.intent: str | None`
- `ChatResponse.supported: bool`

- [ ] **Step 1: Write failing chatbot tests**

```python
def test_chatbot_answers_top_waste_question(sample_frame):
    response = answer_question("Which product has the most waste?", sample_frame, "2026-09-01")
    assert response.supported is True
    assert response.intent == "top_waste_product"
    assert "waste" in response.text.lower()


def test_chatbot_does_not_invent_answer_for_unsupported_question(sample_frame):
    response = answer_question("What will sales be next year?", sample_frame, "2026-09-01")
    assert response.supported is False
    assert "supported" in response.text.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_chatbot.py -v`  
Expected: FAIL because the chatbot module does not exist.

- [ ] **Step 3: Implement intent matching**

Normalize the question, match the six supported intents, call analytics or decision-engine functions, and format responses with the relevant period and numbers. Use explicit fallback text for unsupported questions.

- [ ] **Step 4: Add tests for all supported intents**

Cover branch comparison, estimated loss, today’s markdown recommendation, product reason, and weekday/weekend comparison. Assert returned numbers are derived from the source frame.

- [ ] **Step 5: Run chatbot and unit tests**

Run `python -m pytest tests/test_chatbot.py tests/test_analytics.py tests/test_decision_engine.py -v`. Expected: PASS.

### Task 6: Distinctive Streamlit UI and Charts

**Files:** Create `src/charts.py`, `src/ui.py`, `app.py`, and `tests/test_charts.py`.

**Interfaces:**

- `charts.daily_sales_waste_chart(frame) -> plotly.graph_objects.Figure`
- `charts.waste_by_reason_chart(frame) -> plotly.graph_objects.Figure`
- `ui.format_currency(value) -> str`
- `ui.render_status_badge(priority) -> None`

- [ ] **Step 1: Write failing pure-function UI tests**

```python
def test_format_currency_uses_indonesian_display_format():
    assert format_currency(1250000) == "Rp1,25 jt"


def test_chart_function_returns_plotly_figure(sample_frame):
    figure = daily_sales_waste_chart(sample_frame)
    assert len(figure.data) >= 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_charts.py -v`  
Expected: FAIL because UI and chart modules do not exist.

- [ ] **Step 3: Implement the visual system**

Configure Streamlit page settings, CSS, color constants, KPI cards, status badges, tables, and restrained Plotly layouts using charcoal, cream, muted green, and amber. Use operational copy and no AI branding, neon gradients, or generic robot imagery.

- [ ] **Step 4: Implement all pages in `app.py`**

Build Today’s Operations, Waste Monitor, Markdown Planner, Production Review, Ask ShelfSense, and Data Notes. Initialize SQLite and load the sample Excel file on first run. Use session state for the active frame and selected date/branch. Add manual transaction and manager-decision forms with inline validation.

- [ ] **Step 5: Run UI tests and startup check**

Run `python -m pytest tests/test_charts.py -v`. Then run `streamlit run app.py --server.headless true`. Expected: tests pass and Streamlit starts without traceback. Manually verify every page, simulated-data labels, estimated-versus-actual distinction, filters, and import summary.

### Task 7: README, Integration Verification, and Portfolio Polish

**Files:** Create `README.md` and `tests/test_integration.py`; modify `app.py` and `src/ui.py` as needed.

- [ ] **Step 1: Write the failing integration test**

```python
def test_demo_pipeline_from_excel_to_recommendation_and_answer(tmp_path):
    report = load_excel("data/sample_food_waste.xlsx")
    assert report.rejected_rows == 0
    db_path = tmp_path / "demo.db"
    initialize_database(db_path)
    insert_transactions(db_path, report.clean_frame)
    frame = fetch_transactions(db_path)
    assert calculate_kpis(frame)["total_production"] > 0
    assert recommend_actions(calculate_product_risk(frame, "2026-09-22"))
    assert answer_question("Which product has the most waste?", frame, "2026-09-22").supported
```

- [ ] **Step 2: Run the integration test to verify it fails**

Run: `python -m pytest tests/test_integration.py -v`. Expected: FAIL until all pipeline modules and sample data are connected.

- [ ] **Step 3: Complete README documentation**

Document the problem, UI overview, features, architecture, setup commands, simulated-data disclaimer, KPI definitions, rule-engine examples, chatbot scope, testing command, limitations, and research references.

- [ ] **Step 4: Polish copy and empty states**

Ensure missing data, empty recommendation lists, unsupported questions, invalid uploads, and no-selected-branch states have human-readable messages. Ensure every estimate says `estimated` and every sample-data page says `Simulated demo data`.

- [ ] **Step 5: Run complete verification**

Run `python -m pytest -q`. Then run `python -c "from src.data_loader import load_excel; r=load_excel('data/sample_food_waste.xlsx'); assert r.rejected_rows == 0; print('sample data valid')"` and `streamlit run app.py --server.headless true`. Expected: all tests pass, sample data validates with zero rejected rows, and Streamlit starts without traceback.

- [ ] **Step 6: Confirm portfolio handoff**

Verify the README contains exact run commands and the UI demonstrates the full path: sample data → KPI → risk → recommendation → manager decision → bounded chatbot answer.

## Execution Notes

This workspace is not currently a Git repository, so normal per-task commit steps cannot be performed until Git is initialized or the project is moved into a repository. Keep each task’s changes isolated and run the stated tests before moving to the next task.
