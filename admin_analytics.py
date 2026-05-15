import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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


def admin_analytics_page():
    st.markdown("""
<style>
.analytics-hero {
    background: rgba(10, 15, 12, 0.72);
    padding: 28px;
    border-radius: 26px;
    border: 1px solid rgba(184,234,131,0.25);
    box-shadow: 0 0 35px rgba(132,204,22,0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
}

.analytics-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.analytics-subtitle {
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
    font-size: 34px;
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

.analytics-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
    font-size: 15px;
}

.analytics-table th {
    text-align: left;
    padding: 14px;
    color: #b8ea83;
    border-bottom: 1px solid rgba(184,234,131,0.25);
    background: rgba(184,234,131,0.08);
}

.analytics-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}

.analytics-table tr:hover {
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

.chart-card {
    background: rgba(10, 15, 12, 0.66);
    padding: 22px;
    border-radius: 24px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 35px rgba(132,204,22,0.10);
    backdrop-filter: blur(16px);
    margin-bottom: 26px;
}

div[data-testid="stCodeBlock"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

    records = get_all_predictions()

    st.markdown("""
<div class="analytics-hero">
    <div class="analytics-title">📊 Admin Analytics Dashboard</div>
    <div class="analytics-subtitle">
        Review overall AI prediction performance, disease distribution, user activity, and system confidence trends.
    </div>
</div>
""", unsafe_allow_html=True)

    if not records:
        st.info("No prediction data available yet.")
        return

    df = pd.DataFrame(records, columns=[
        "Log ID",
        "Full Name",
        "Username",
        "Image",
        "Disease",
        "Confidence",
        "Risk",
        "Date & Time"
    ])

    df["Confidence"] = pd.to_numeric(df["Confidence"], errors="coerce").round(2)
    df = df.dropna(subset=["Confidence"])
    df["Disease"] = df["Disease"].apply(format_disease_name)

    if df.empty:
        st.warning("Prediction records exist, but confidence values are invalid.")
        return

    most_common_disease = df["Disease"].mode()[0]
    avg_confidence = round(df["Confidence"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">📸 Total Scans</div>
    <div class="metric-value">{len(df)}</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">👥 Unique Users</div>
    <div class="metric-value">{df["Username"].nunique()}</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">🎯 Avg Confidence</div>
    <div class="metric-value">{avg_confidence}%</div>
</div>
""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">🦠 Most Common</div>
    <div class="metric-value" style="font-size:22px;">{most_common_disease}</div>
</div>
""", unsafe_allow_html=True)

    view_option = st.selectbox(
        "Choose prediction records to display",
        ["Latest 25 Records", "Oldest 25 Records", "All Records"]
    )

    if view_option == "Latest 25 Records":
        display_df = df.head(25)
    elif view_option == "Oldest 25 Records":
        display_df = df.tail(25)
    else:
        display_df = df

    st.caption(f"Showing {len(display_df)} of {len(df)} total prediction records.")

    rows_html = ""

    for _, row in display_df.iterrows():
        risk = str(row["Risk"])

        rows_html += (
            "<tr>"
            f"<td>{escape(str(row['Log ID']))}</td>"
            f"<td>{escape(str(row['Full Name']))}</td>"
            f"<td>{escape(str(row['Username']))}</td>"
            f"<td>{escape(str(row['Image']))}</td>"
            f"<td>{escape(str(row['Disease']))}</td>"
            f"<td>{escape(str(row['Confidence']))}%</td>"
            f"<td class='{risk_class(risk)}'>{escape(risk)}</td>"
            f"<td>{escape(str(row['Date & Time']))}</td>"
            "</tr>"
        )

    table_html = (
        "<div class='glass-card'>"
        "<div class='section-title'>📋 Prediction Records</div>"
        "<table class='analytics-table'>"
        "<thead>"
        "<tr>"
        "<th>Log ID</th>"
        "<th>Full Name</th>"
        "<th>Username</th>"
        "<th>Image</th>"
        "<th>Disease</th>"
        "<th>Confidence</th>"
        "<th>Risk</th>"
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

    st.markdown("<div class='section-title'>🦠 Disease Distribution</div>", unsafe_allow_html=True)

    disease_counts = df["Disease"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(3.8, 2.5))
    ax1.bar(disease_counts.index, disease_counts.values)
    ax1.set_title("Disease Distribution", fontsize=9)
    ax1.set_xlabel("Disease", fontsize=7)
    ax1.set_ylabel("Count", fontsize=7)
    ax1.tick_params(axis="x", labelrotation=25, labelsize=6)
    ax1.tick_params(axis="y", labelsize=7)
    plt.tight_layout()

    col_left, col_mid, col_right = st.columns([1, 1.6, 1])
    with col_mid:
        st.pyplot(fig1)

    st.markdown("<div class='section-title'>📈 Confidence Trend</div>", unsafe_allow_html=True)

    df = df.reset_index(drop=True)
    df["Scan Number"] = range(1, len(df) + 1)

    fig2, ax2 = plt.subplots(figsize=(3.8, 2.5))
    ax2.plot(df["Scan Number"], df["Confidence"], marker="o", linewidth=1.5, markersize=4)
    ax2.set_title("Overall Confidence Trend", fontsize=9)
    ax2.set_xlabel("Scan Number", fontsize=7)
    ax2.set_ylabel("Confidence (%)", fontsize=7)
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis="both", labelsize=7)
    plt.tight_layout()

    col_left, col_mid, col_right = st.columns([1, 1.6, 1])
    with col_mid:
        st.pyplot(fig2)