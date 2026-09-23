import plotly.graph_objects as go
from .analytics import calculate_daily_trend


def daily_sales_waste_chart(frame):
    trend = calculate_daily_trend(frame)
    fig = go.Figure()
    fig.add_bar(x=trend["transaction_date"], y=trend["sold_qty"], name="Sold", marker_color="#5f8066")
    fig.add_bar(x=trend["transaction_date"], y=trend["waste_qty"], name="Waste", marker_color="#d39b45")
    fig.update_layout(barmode="group", template="simple_white", margin=dict(l=20, r=20, t=30, b=20), legend_orientation="h")
    return fig


def waste_by_reason_chart(frame):
    grouped = frame.groupby("waste_reason", dropna=False)["waste_qty"].sum().reset_index()
    fig = go.Figure(go.Bar(x=grouped["waste_reason"].fillna("Unspecified"), y=grouped["waste_qty"], marker_color="#d39b45"))
    fig.update_layout(template="simple_white", margin=dict(l=20, r=20, t=30, b=20))
    return fig
