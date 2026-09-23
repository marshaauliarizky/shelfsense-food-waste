from datetime import date

import streamlit as st


def inject_styles():
    st.markdown(
        """
<style>
:root { --ink: #243029; --muted: #68746c; --paper: #f7f4ed; --line: #e4e0d6; --green: #587568; --amber: #c48638; }
@keyframes shelfFade { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes shelfRise { from { opacity: 0; transform: translateY(18px) scale(.985); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes softGlow { 0%, 100% { box-shadow: 0 10px 28px rgba(88, 117, 104, .08); } 50% { box-shadow: 0 16px 34px rgba(88, 117, 104, .17); } }
html, body, [class*="css"], .stApp { font-family: "Aptos", "Segoe UI", sans-serif; }
.stApp { background: radial-gradient(circle at 82% 4%, rgba(207, 222, 211, .42), transparent 26rem), radial-gradient(circle at 4% 70%, rgba(231, 214, 182, .26), transparent 24rem), var(--paper); color: var(--ink); }
[data-testid="stAppViewContainer"] { background: var(--paper); }
[data-testid="stSidebar"] { background: #25332c; border-right: 1px solid #34483d; }
[data-testid="stSidebar"] * { font-family: "Aptos", "Segoe UI", sans-serif; }
[data-testid="stSidebar"] h2 { color: #f7f4ed !important; font-size: 1.35rem; letter-spacing: -.02em; }
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small { color: #bac8be !important; }
[data-testid="stSidebar"] label p { color: #eef2ed !important; font-size: .78rem; font-weight: 650; letter-spacing: .01em; }
[data-testid="stSidebar"] [data-testid="stRadio"] label p { color: #dbe6dd !important; font-size: .9rem; font-weight: 500; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p { color: #ffffff !important; font-weight: 700; }
[data-testid="stSidebar"] div[data-baseweb="select"] > div { background: #f8f6f0 !important; border: 1px solid #d7ddd5 !important; border-radius: 8px !important; min-height: 42px; }
[data-testid="stSidebar"] div[data-baseweb="select"] span, [data-testid="stSidebar"] div[data-baseweb="select"] input { color: #243029 !important; -webkit-text-fill-color: #243029 !important; font-weight: 600 !important; }
[data-testid="stSidebar"] [data-testid="stDateInput"] input { background: #f8f6f0 !important; color: #243029 !important; -webkit-text-fill-color: #243029 !important; border: 1px solid #d7ddd5 !important; border-radius: 8px !important; font-weight: 600 !important; }
[data-baseweb="popover"] { background: #fffdf8 !important; border: 1px solid #d7ddd5 !important; }
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] [role="option"] { background: #fffdf8 !important; color: #243029 !important; }
[data-baseweb="popover"] [role="option"]:hover { background: #e8efe9 !important; color: #243029 !important; }
.block-container { padding-top: 2.8rem; padding-bottom: 3rem; max-width: 1420px; }
.hero { padding: 1rem 0 1.15rem; border-bottom: 1px solid var(--line); margin-bottom: 1.15rem; animation: shelfFade .65s ease both; }
.eyebrow { color: var(--amber); text-transform: uppercase; letter-spacing: .16em; font-size: .68rem; font-weight: 800; }
.hero h1 { font-family: "Aptos Display", "Segoe UI", sans-serif; font-size: clamp(2rem, 4vw, 3.6rem); line-height: 1.02; letter-spacing: -.055em; font-weight: 720; margin: .35rem 0 .7rem; color: var(--ink); max-width: 820px; }
.hero p { color: var(--muted); font-size: 1rem; max-width: 650px; margin: 0; }
.stSubheader { color: var(--ink); letter-spacing: -.025em; font-weight: 720; }
[data-testid="stMetric"] { background: #fffdf8; border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.05rem; box-shadow: 0 5px 18px rgba(45, 55, 47, .045); animation: shelfRise .65s ease both, softGlow 5s ease-in-out 1s infinite; transition: transform .22s ease, border-color .22s ease; }
[data-testid="stMetric"]:hover { transform: translateY(-4px); border-color: #b9cbbd; }
[data-testid="stMetricLabel"] p { color: var(--muted) !important; font-size: .76rem; font-weight: 700; }
[data-testid="stMetricValue"] { color: var(--ink) !important; font-size: 1.65rem; letter-spacing: -.04em; }
.note { background: #e7efe8; color: #365243; border: 1px solid #cbdccc; border-left: 4px solid var(--green); padding: .8rem 1rem; border-radius: 9px; margin-bottom: 1.25rem; }
.risk { background: #fffaf0; border: 1px solid #e7d8bc; border-left: 4px solid var(--amber); padding: 1rem 1.1rem; border-radius: 10px; margin-bottom: .7rem; color: var(--ink); animation: shelfRise .55s ease both; transition: transform .22s ease, box-shadow .22s ease; }
.risk:hover { transform: translateX(4px); box-shadow: 0 10px 22px rgba(91, 70, 36, .09); }
[data-testid="stImage"] img { border-radius: 14px; animation: shelfFade .85s ease both; box-shadow: 0 14px 30px rgba(45, 55, 47, .10); }
[data-testid="stAlert"] { animation: shelfFade .45s ease both; }
.stDataFrame { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
button[kind="secondary"] { border-radius: 8px; }
</style>
        """,
        unsafe_allow_html=True,
    )


def show_intro_dialog():
    if "intro_seen" in st.session_state or st.query_params.get("capture") == "1":
        return

    @st.dialog("Welcome to ShelfSense")
    def intro():
        st.markdown("#### A practical view of bakery operations")
        st.write("ShelfSense connects production, sales, stock, expiry, and waste into a single decision view.")
        st.info("Start with Today's Operations. Use Branch and As of in the sidebar to change the scope.")
        st.write("Every recommendation is explainable and based on simulated demo data.")
        if st.button("Open dashboard", width="stretch"):
            st.rerun()

    st.session_state.intro_seen = True
    intro()


def render_sidebar(frame):
    pages = ["Today's Operations", "Waste Monitor", "Markdown Planner", "Production Review", "Import Data", "Ask ShelfSense", "Data Notes"]
    requested_page = st.query_params.get("page")
    default_page = requested_page if requested_page in pages else pages[0]
    with st.sidebar:
        st.markdown("## ShelfSense")
        st.caption("Operations console for perishable inventory")
        page = st.radio(
            "Navigate",
            pages,
            index=pages.index(default_page),
            label_visibility="collapsed",
        )
        st.divider()
        selected_branch = st.selectbox("Branch", ["All branches"] + sorted(frame["branch"].unique().tolist()))
        selected_date = st.date_input(
            "As of",
            value=date(2026, 9, 22),
            min_value=frame["transaction_date"].dt.date.min(),
            max_value=date(2026, 12, 31),
        )
        st.caption("SIMULATED DEMO DATA")
    return page, selected_branch, selected_date


def render_hero():
    hero_copy, hero_image = st.columns([1.05, 1.35], gap="large")
    with hero_copy:
        st.markdown(
            '<div class="hero"><div class="eyebrow">ShelfSense / Operations</div><h1>What should sell, what may spoil, and what to do next.</h1><p>A quieter view of inventory decisions for bakery teams.</p></div>',
            unsafe_allow_html=True,
        )
    with hero_image:
        st.image("assets/shelfsense-hero.png", width="stretch")
    st.markdown('<div class="note">This workspace uses simulated demo data. Recommendations are estimates, not actual business outcomes.</div>', unsafe_allow_html=True)
    with st.popover("How to read this dashboard"):
        st.markdown("**Waste rate** shows the share of production that was not sold. **Estimated loss** uses unit cost, not retail price. **High priority** means expiry and surplus need attention soon.")
        st.caption("Use Markdown Planner to record the manager decision and compare it with the eventual outcome.")


def format_currency(value):
    value = float(value or 0)
    if abs(value) >= 1_000_000:
        return f"Rp{value / 1_000_000:.2f}".replace(".", ",") + " jt"
    if abs(value) >= 1_000:
        return f"Rp{value / 1_000:.0f} rb"
    return f"Rp{value:,.0f}".replace(",", ".")


def render_status_badge(priority):
    labels = {"high": "High priority", "watch": "Watch", "no_action": "No action"}
    st.markdown(f"`{labels.get(priority, priority)}`")
