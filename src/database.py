import sqlite3
from pathlib import Path
import pandas as pd


def initialize_database(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY, transaction_date TEXT NOT NULL,
            transaction_time TEXT NOT NULL, branch TEXT NOT NULL, product_id TEXT NOT NULL,
            product_name TEXT NOT NULL, category TEXT NOT NULL, production_qty INTEGER NOT NULL,
            sold_qty INTEGER NOT NULL, waste_qty INTEGER NOT NULL, stock_qty INTEGER NOT NULL,
            unit_price REAL NOT NULL, unit_cost REAL NOT NULL, discount_pct REAL NOT NULL,
            expiry_date TEXT NOT NULL, shelf_life_days INTEGER NOT NULL, forecast_qty REAL,
            weather TEXT, event_flag INTEGER NOT NULL DEFAULT 0, waste_reason TEXT,
            actual_markdown_revenue REAL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS manager_decisions (
            decision_id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id TEXT NOT NULL,
            decision_type TEXT NOT NULL, decision_status TEXT NOT NULL,
            recommended_discount REAL, actual_discount REAL, manager_note TEXT,
            actual_sold_qty INTEGER, actual_waste_qty INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)


def insert_transactions(path: str | Path, frame: pd.DataFrame) -> int:
    initialize_database(path)
    columns = [c for c in frame.columns if c not in {"created_at"}]
    rows = frame[columns].copy()
    for column in ("transaction_date", "expiry_date"):
        if column in rows:
            rows[column] = rows[column].astype(str)
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO transactions ({','.join(columns)}) VALUES ({placeholders})"
    with sqlite3.connect(path) as connection:
        connection.executemany(sql, rows.where(pd.notna(rows), None).itertuples(index=False, name=None))
    return len(rows)


def fetch_transactions(path: str | Path) -> pd.DataFrame:
    initialize_database(path)
    with sqlite3.connect(path) as connection:
        return pd.read_sql_query("SELECT * FROM transactions ORDER BY transaction_date, transaction_time", connection)


def insert_manager_decision(path: str | Path, decision: dict) -> int:
    initialize_database(path)
    fields = ["transaction_id", "decision_type", "decision_status", "recommended_discount", "actual_discount", "manager_note", "actual_sold_qty", "actual_waste_qty"]
    values = [decision.get(field) for field in fields]
    with sqlite3.connect(path) as connection:
        cursor = connection.execute(f"INSERT INTO manager_decisions ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})", values)
        return int(cursor.lastrowid)
