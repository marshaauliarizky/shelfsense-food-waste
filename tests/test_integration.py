from pathlib import Path
from uuid import uuid4
from src.analytics import calculate_kpis, calculate_product_risk
from src.chatbot import answer_question
from src.data_loader import load_excel
from src.database import fetch_transactions, initialize_database, insert_transactions
from src.decision_engine import recommend_actions


def test_demo_pipeline_from_excel_to_recommendation_and_answer():
    report = load_excel("data/sample_food_waste.xlsx")
    assert report.rejected_rows == 0
    db_path = Path("data") / f"integration-demo-{uuid4().hex}.db"
    initialize_database(db_path)
    insert_transactions(db_path, report.clean_frame)
    frame = fetch_transactions(db_path)
    assert calculate_kpis(frame)["total_production"] > 0
    assert recommend_actions(calculate_product_risk(frame, "2026-09-22"))
    assert answer_question("Which product has the most waste?", frame, "2026-09-22").supported
