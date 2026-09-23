from pathlib import Path
from uuid import uuid4
from src.database import fetch_transactions, initialize_database, insert_transactions


def test_insert_transactions_round_trips_clean_rows(valid_frame):
    db_path = Path("data") / f"test-shelfsense-{uuid4().hex}.db"
    initialize_database(db_path)
    inserted = insert_transactions(db_path, valid_frame)
    result = fetch_transactions(db_path)
    assert inserted == len(valid_frame)
    assert list(result["transaction_id"]) == ["TX-1"]
