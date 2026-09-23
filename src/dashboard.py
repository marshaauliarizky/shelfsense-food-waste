import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from .analytics import calculate_kpis, calculate_product_risk, compare_periods
from .chatbot import answer_question
from .charts import daily_sales_waste_chart, waste_by_reason_chart
from .database import fetch_transactions, insert_manager_decision, insert_transactions
from .decision_engine import recommend_actions
from .ui_components import format_currency, render_status_badge


def render_page(page, frame, selected_date, database_path):
    renderers = {
        "Today's Operations": render_operations,
        "Waste Monitor": render_waste_monitor,
        "Markdown Planner": render_markdown_planner,
        "Production Review": render_production_review,
        "Import Data": render_import_data,
        "Ask ShelfSense": render_question_panel,
        "Data Notes": render_data_notes,
    }
    renderers.get(page, render_operations)(frame, selected_date, database_path)


def render_operations(frame, selected_date, database_path):
    st.subheader("Today's Operations")
    kpi = calculate_kpis(frame)
    cards = [
        ("Production", f"{kpi['total_production']:,} units"),
        ("Sold-through", _format_rate(kpi["sold_through_rate"])),
        ("Waste rate", _format_rate(kpi["waste_rate"])),
        ("Estimated loss", format_currency(kpi["estimated_loss"])),
    ]
    for column, (label, value) in zip(st.columns(4), cards):
        column.metric(label, value)

    chart_column, comparison_column = st.columns([1.6, 1])
    with chart_column:
        st.markdown("#### Waste and sales / last 8 weeks")
        st.plotly_chart(daily_sales_waste_chart(frame), width="stretch")
    with comparison_column:
        st.markdown("#### What changed?")
        current_end = pd.Timestamp(selected_date)
        current_start = current_end - pd.Timedelta(days=6)
        previous_end = current_start - pd.Timedelta(days=1)
        comparison = compare_periods(
            frame,
            current_start,
            current_end,
            previous_end - pd.Timedelta(days=6),
            previous_end,
        )
        if len(comparison) == 2:
            change = comparison.iloc[0].waste_rate - comparison.iloc[1].waste_rate
            st.metric("Waste rate vs previous week", f"{comparison.iloc[0].waste_rate:.1%}", f"{change:+.1%}")
        st.caption("Period comparison uses the selected date and the previous 7-day window.")

    st.markdown("#### Needs attention")
    risk_frame = calculate_product_risk(frame, selected_date)
    recommendations = [item for item in recommend_actions(risk_frame) if item["priority"] != "no_action"][:6]
    if not recommendations:
        st.success("No immediate action is needed for the selected scope.")
    for recommendation in recommendations:
        with st.container(border=True):
            st.markdown(f"**{recommendation['product_name']}** · {recommendation['branch']}")
            render_status_badge(recommendation["priority"])
            st.write(recommendation["issue"] + ". " + "; ".join(recommendation["evidence"]))
            st.caption(recommendation["action"] + f" · Estimated revenue: {format_currency(recommendation['estimated_revenue'])}")


def render_waste_monitor(frame, selected_date, database_path):
    st.subheader("Waste Monitor")
    st.plotly_chart(waste_by_reason_chart(frame), width="stretch")
    product_column, branch_column = st.columns(2)
    with product_column:
        st.markdown("#### Waste by product")
        product_waste = frame.groupby(["product_name", "category"], as_index=False).agg(
            waste_qty=("waste_qty", "sum"), production_qty=("production_qty", "sum")
        )
        product_waste["waste_rate"] = product_waste.waste_qty / product_waste.production_qty
        st.dataframe(product_waste.sort_values("waste_qty", ascending=False), width="stretch", hide_index=True)
    with branch_column:
        st.markdown("#### Waste by branch")
        branch_waste = frame.groupby("branch", as_index=False).agg(
            waste_qty=("waste_qty", "sum"), production_qty=("production_qty", "sum")
        )
        branch_waste["waste_rate"] = branch_waste.waste_qty / branch_waste.production_qty
        st.dataframe(branch_waste.sort_values("waste_rate", ascending=False), width="stretch", hide_index=True)


def render_markdown_planner(frame, selected_date, database_path):
    st.subheader("Markdown Planner")
    st.caption("A markdown window is suggested only when remaining stock is above the demand baseline.")
    image_column, planner_column = st.columns([0.85, 1.15], gap="large")
    with image_column:
        st.image("assets/bakery-product-board.png", width="stretch")
        st.caption("Product board · visual reference for the simulated bakery assortment")
    with planner_column:
        st.markdown("#### Today's markdown window")
        st.caption("Prioritized by expiry risk, stock gap, and demand baseline.")

    risk_frame = calculate_product_risk(frame, selected_date)
    for recommendation in [item for item in recommend_actions(risk_frame) if item["priority"] != "no_action"]:
        evidence = " · ".join(recommendation["evidence"])
        st.markdown(
            f'<div class="risk"><b>{recommendation["product_name"]}</b> · {recommendation["branch"]}<br>'
            f'{recommendation["issue"]}<br><small>{evidence}</small><br>'
            f'<b>Manager action:</b> {recommendation["action"]}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("Record a manager decision"):
        transaction_id = st.selectbox("Transaction", frame["transaction_id"].tolist())
        decision_type = st.selectbox("Decision", ["markdown", "reduce_production", "no_action"])
        status = st.selectbox("Status", ["planned", "completed", "skipped"])
        note = st.text_input("Manager note")
        if st.button("Save decision"):
            insert_manager_decision(
                database_path,
                {
                    "transaction_id": transaction_id,
                    "decision_type": decision_type,
                    "decision_status": status,
                    "manager_note": note,
                },
            )
            st.toast("Manager decision saved")
            st.success("Decision saved.")


def render_production_review(frame, selected_date, database_path):
    st.subheader("Production Review")
    review = frame.groupby(["product_name", "category"], as_index=False).agg(
        planned=("production_qty", "sum"),
        sold=("sold_qty", "sum"),
        waste=("waste_qty", "sum"),
        forecast=("forecast_qty", "sum"),
    )
    review["production_gap"] = review.planned - review.forecast
    st.dataframe(review.sort_values("production_gap", ascending=False), width="stretch", hide_index=True)
    st.caption("Forecast is a simple moving-average baseline for demonstration, not a production forecast model.")


def render_import_data(frame, selected_date, database_path):
    st.subheader("Import Data")
    st.caption("Upload an Excel file with the required transaction columns. Invalid rows are not inserted.")
    upload = st.file_uploader("Excel file", type=["xlsx", "xls"])
    if upload is None:
        return

    from .data_loader import load_excel

    report = load_excel(upload)
    st.write({"valid rows": report.valid_rows, "rejected rows": report.rejected_rows, "duplicates": report.duplicate_count})
    if report.errors:
        st.error("; ".join(report.errors))
    if report.valid_rows and st.button("Insert valid rows"):
        try:
            insert_transactions(database_path, report.clean_frame)
            st.session_state.frame = fetch_transactions(database_path)
            st.toast(f"Inserted {report.valid_rows} valid rows")
            st.success(f"Inserted {report.valid_rows} rows. Reload the page to refresh the dashboard.")
        except sqlite3.IntegrityError:
            st.error("Some transaction IDs already exist in the database. No duplicate rows were inserted.")
    if report.rejected_rows:
        st.dataframe(report.clean_frame.head(5), width="stretch", hide_index=True)


def render_question_panel(frame, selected_date, database_path):
    st.subheader("Ask ShelfSense")
    st.caption("Try: Which product has the most waste? · Which product should get a markdown? · What is the estimated loss?")
    question = st.text_input("Question", placeholder="Which product has the most waste?")
    if question:
        response = answer_question(question, frame, selected_date)
        st.markdown(f"#### {response.text}")
        if not response.supported:
            st.info("Supported topics: waste, branches, estimated loss, markdowns, and product drivers.")


def render_data_notes(frame, selected_date, database_path):
    st.subheader("Data Notes")
    st.markdown(
        """
        **Simulated demo data** covers 8 weeks, 3 bakery branches, and 12 products. It intentionally includes demand variation, weather, events, stockouts, overproduction, and markdown records.

        **Waste rate** = waste quantity / production quantity. **Estimated loss** = waste quantity × unit cost. Estimated impact is illustrative and must not be read as an actual saving.

        The recommendation engine is deterministic and explainable. It uses expiry days, stock gap, waste rate, sell-through, and markdown level. The chatbot is limited to supported intents and does not generate unrestricted database queries.
        """
    )
    export_path = Path("exports/ShelfSense_demo_workbook.xlsx")
    if export_path.exists():
        st.download_button(
            "Download data workbook",
            data=export_path.read_bytes(),
            file_name=export_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


def _format_rate(value):
    return f"{value:.1%}" if value is not None else "—"
