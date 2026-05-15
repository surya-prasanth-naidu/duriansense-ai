import streamlit as st
import pandas as pd
from html import escape
from database import get_all_predictions


def format_disease_name(name):
    return str(name).replace("_", " ").title()


def risk_class(risk):
    risk = str(risk).lower()
    if risk == "medium":
        return "risk-medium"
    if risk == "high":
        return "risk-high"
    return "risk-low"


def admin_prediction_logs():
    st.markdown("""
<style>
.logs-hero {
    background: rgba(10, 15, 12, 0.72);
    padding: 28px;
    border-radius: 26px;
    border: 1px solid rgba(184,234,131,0.25);
    box-shadow: 0 0 35px rgba(132,204,22,0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
}

.logs-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.logs-subtitle {
    color: #e5e7eb;
    font-size: 16px;
    line-height: 1.6;
}

.metric-card {
    background: rgba(15, 23, 42, 0.78);
    padding: 24px;
    border-radius: 22px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 25px rgba(132,204,22,0.10);
    margin-bottom: 24px;
}

.metric-label {
    color: #d1d5db;
    font-size: 14px;
    font-weight: 700;
}

.metric-value {
    color: #b8ea83;
    font-size: 36px;
    font-weight: 900;
    margin-top: 8px;
}

.glass-card {
    background: rgba(10, 15, 12, 0.66);
    padding: 24px;
    border-radius: 24px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 35px rgba(132,204,22,0.10);
    backdrop-filter: blur(16px);
    margin-bottom: 26px;
    overflow-x: auto;
}

.section-title {
    color: #b8ea83;
    font-size: 25px;
    font-weight: 900;
    margin-bottom: 18px;
}

.logs-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
    font-size: 15px;
}

.logs-table th {
    text-align: left;
    padding: 14px;
    color: #b8ea83;
    border-bottom: 1px solid rgba(184,234,131,0.25);
    background: rgba(184,234,131,0.08);
}

.logs-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}

.logs-table tr:hover {
    background: rgba(184,234,131,0.08);
}

.risk-low {
    color: #86efac;
    font-weight: 900;
}

.risk-medium {
    color: #fde68a;
    font-weight: 900;
}

.risk-high {
    color: #fca5a5;
    font-weight: 900;
}

div[data-testid="stDownloadButton"] button {
    background: linear-gradient(90deg, #86b85d, #b9ec7d) !important;
    color: #07120c !important;
    border-radius: 14px !important;
    border: none !important;
    font-weight: 900 !important;
    padding: 12px 20px !important;
}

div[data-testid="stCodeBlock"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

    records = get_all_predictions()

    st.markdown("""
<div class="logs-hero">
    <div class="logs-title">📋 Admin Prediction Logs</div>
    <div class="logs-subtitle">
        View all prediction records created by farmers, monitor disease detections, and export logs for reporting.
    </div>
</div>
""", unsafe_allow_html=True)

    if not records:
        st.info("No prediction logs available yet.")
        return

    df = pd.DataFrame(records, columns=[
        "Log ID",
        "Full Name",
        "Username",
        "Image",
        "Disease",
        "Confidence (%)",
        "Risk Level",
        "Date & Time"
    ])

    df["Confidence (%)"] = pd.to_numeric(df["Confidence (%)"], errors="coerce").round(2)
    df["Disease"] = df["Disease"].apply(format_disease_name)

    total_logs = len(df)
    unique_users = df["Username"].nunique()
    high_risk_count = len(df[df["Risk Level"].astype(str).str.lower() == "high"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">📋 Total Logs</div>
    <div class="metric-value">{total_logs}</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">👥 Active Users</div>
    <div class="metric-value">{unique_users}</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">⚠️ High Risk</div>
    <div class="metric-value">{high_risk_count}</div>
</div>
""", unsafe_allow_html=True)

    view_option = st.selectbox(
        "Choose records to display",
        [
            "Latest 25 Records",
            "Oldest 25 Records",
            "All Records"
        ]
    )

    if view_option == "Latest 25 Records":
        display_df = df.head(25)
    elif view_option == "Oldest 25 Records":
        display_df = df.tail(25)
    else:
        display_df = df

    st.caption(f"Showing {len(display_df)} of {len(df)} total prediction logs.")

    rows_html = ""

    for _, row in display_df.iterrows():
        risk = str(row["Risk Level"])

        rows_html += (
            "<tr>"
            f"<td>{escape(str(row['Log ID']))}</td>"
            f"<td>{escape(str(row['Full Name']))}</td>"
            f"<td>{escape(str(row['Username']))}</td>"
            f"<td>{escape(str(row['Image']))}</td>"
            f"<td>{escape(str(row['Disease']))}</td>"
            f"<td>{escape(str(row['Confidence (%)']))}%</td>"
            f"<td class='{risk_class(risk)}'>{escape(risk)}</td>"
            f"<td>{escape(str(row['Date & Time']))}</td>"
            "</tr>"
        )

    table_html = (
        "<div class='glass-card'>"
        "<div class='section-title'>🌿 Prediction Log Records</div>"
        "<table class='logs-table'>"
        "<thead>"
        "<tr>"
        "<th>Log ID</th>"
        "<th>Full Name</th>"
        "<th>Username</th>"
        "<th>Image</th>"
        "<th>Disease</th>"
        "<th>Confidence</th>"
        "<th>Risk Level</th>"
        "<th>Date & Time</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        f"{rows_html}"
        "</tbody>"
        "</table>"
        "</div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download All Records as CSV",
        data=csv,
        file_name="duriasense_prediction_logs.csv",
        mime="text/csv"
    )