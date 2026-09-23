import pandas as pd
import streamlit as st

from src.config import DEFAULT_DB_PATH
from src.dashboard import render_page
from src.data_loader import load_excel
from src.database import fetch_transactions, initialize_database, insert_transactions
from src.ui_components import inject_styles, render_hero, render_sidebar, show_intro_dialog


st.set_page_config(page_title="ShelfSense", layout="wide", initial_sidebar_state="expanded")
inject_styles()


def load_demo_data():
    """Open the local database and seed it from the bundled workbook when needed."""
    initialize_database(DEFAULT_DB_PATH)
    frame = fetch_transactions(DEFAULT_DB_PATH)
    if frame.empty:
        report = load_excel("data/sample_food_waste.xlsx")
        insert_transactions(DEFAULT_DB_PATH, report.clean_frame)
        frame = fetch_transactions(DEFAULT_DB_PATH)
    return frame


if "frame" not in st.session_state:
    st.session_state.frame = load_demo_data()

frame = st.session_state.frame.copy()
frame["transaction_date"] = pd.to_datetime(frame["transaction_date"])
show_intro_dialog()

page, selected_branch, selected_date = render_sidebar(frame)
if selected_branch != "All branches":
    frame = frame.loc[frame["branch"] == selected_branch].copy()

render_hero()
render_page(page, frame, selected_date, DEFAULT_DB_PATH)
