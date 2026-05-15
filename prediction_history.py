import streamlit as st
import pandas as pd
from html import escape
from textwrap import dedent
from database import get_user_predictions


def format_disease_name(name):
    return str(name).replace("_", " ").title()


def prediction_history_page():
    st.markdown(dedent("""
<style>
.history-hero {
    background: rgba(10, 15, 12, 0.72);
    padding: 26px;
    border-radius: 24px;
    border: 1px solid rgba(184,234,131,0.25);
    box-shadow: 0 0 35px rgba(132,204,22,0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
}

.history-title {
    font-size: 40px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.history-subtitle {
    color: #e5e7eb;
    font-size: 16px;
}

.metric-card {
    background: rgba(15, 23, 42, 0.76);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 25px rgba(132,204,22,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 32px;
    font-weight: 900;
    color: #b8ea83;
}

.metric-label {
    color: #e5e7eb;
    font-size: 14px;
    margin-top: 4px;
}

.table-card {
    background: rgba(10, 15, 12, 0.66);
    padding: 22px;
    border-radius: 24px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 35px rgba(132,204,22,0.10);
    backdrop-filter: blur(16px);
    margin-top: 18px;
    overflow-x: auto;
}

.history-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
    font-size: 15px;
}

.history-table th {
    text-align: left;
    padding: 14px;
    color: #b8ea83;
    border-bottom: 1px solid rgba(184,234,131,0.25);
    background: rgba(184,234,131,0.08);
}

.history-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}

.history-table tr:hover {
    background: rgba(184,234,131,0.08);
}

.risk-low {
    color: #86efac;
    font-weight: 800;
}

.risk-medium {
    color: #fde68a;
    font-weight: 800;
}

.risk-high {
    color: #fca5a5;
    font-weight: 800;
}

div[data-testid="stCodeBlock"] {
    display: none !important;
}
</style>
"""), unsafe_allow_html=True)

    records = get_user_predictions(st.session_state.user["id"])

    st.markdown(dedent("""
<div class="history-hero">
    <div class="history-title">🕘 My Prediction History</div>
    <div class="history-subtitle">
        View all your previous durian leaf scans, disease results, confidence levels, and risk status.
    </div>
</div>
"""), unsafe_allow_html=True)

    if not records:
        st.info("No prediction history yet.")
        return

    df = pd.DataFrame(records, columns=[
        "Image", "Disease", "Confidence (%)", "Risk Level", "Date & Time"
    ])

    df["Confidence (%)"] = pd.to_numeric(df["Confidence (%)"], errors="coerce").round(2)
    df["Disease"] = df["Disease"].apply(format_disease_name)

    total_scans = len(df)
    latest_disease = df.iloc[0]["Disease"]
    average_confidence = round(df["Confidence (%)"].mean(), 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-value">{total_scans}</div>
    <div class="metric-label">Total Scans</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-value">{average_confidence}%</div>
    <div class="metric-label">Average Confidence</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-value" style="font-size:24px;">{latest_disease}</div>
    <div class="metric-label">Latest Detection</div>
</div>
""", unsafe_allow_html=True)

    search = st.text_input(
        "🔎 Search by image, disease, risk, or date",
        placeholder="Example: anthracnose, low, 2026"
    )

    if search:
        search_lower = search.lower()
        df = df[df.apply(lambda row: search_lower in " ".join(row.astype(str)).lower(), axis=1)]

    if df.empty:
        st.warning("No matching prediction records found.")
        return

    rows_html = ""

    for _, row in df.iterrows():
        risk = str(row["Risk Level"])
        risk_class = "risk-low"

        if risk.lower() == "medium":
            risk_class = "risk-medium"
        elif risk.lower() == "high":
            risk_class = "risk-high"

        confidence_value = row["Confidence (%)"]

        rows_html += f"""
<tr>
    <td>{escape(str(row["Image"]))}</td>
    <td>{escape(str(row["Disease"]))}</td>
    <td>{escape(str(confidence_value))}%</td>
    <td class="{risk_class}">{escape(risk)}</td>
    <td>{escape(str(row["Date & Time"]))}</td>
</tr>
"""

    table_html = f"""
<div class="table-card">
<table class="history-table">
<thead>
<tr>
<th>Image</th>
<th>Disease</th>
<th>Confidence</th>
<th>Risk Level</th>
<th>Date & Time</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>
"""

    st.markdown(table_html, unsafe_allow_html=True)