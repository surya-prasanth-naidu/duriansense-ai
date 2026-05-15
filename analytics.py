import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from html import escape
from textwrap import dedent
from database import get_user_predictions_with_id, delete_prediction


def format_disease_name(name):
    return str(name).replace("_", " ").title()


def analytics_page():
    st.markdown(dedent("""
<style>
.analytics-table-card {
    background: rgba(10, 15, 12, 0.66);
    padding: 22px;
    border-radius: 24px;
    border: 1px solid rgba(184,234,131,0.20);
    box-shadow: 0 0 35px rgba(132,204,22,0.10);
    backdrop-filter: blur(16px);
    margin-top: 18px;
    margin-bottom: 28px;
    overflow-x: auto;
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
</style>
"""), unsafe_allow_html=True)

    st.header("📊 Analytics Dashboard")

    records = get_user_predictions_with_id(st.session_state.user["id"])

    if not records:
        st.info("No prediction data available yet. Please scan some images first.")
        return

    df = pd.DataFrame(records, columns=[
        "id", "image", "disease", "confidence", "risk", "datetime"
    ])

    df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").round(2)
    df["datetime"] = df["datetime"].astype(str)
    df = df.dropna(subset=["confidence"])

    if df.empty:
        st.warning("Prediction records exist, but confidence values are invalid.")
        return

    st.metric("Total Scans", len(df))

    st.subheader("📋 Live Prediction Records")

    rows_html = ""

    for _, row in df.iterrows():
        risk = str(row["risk"])
        risk_class = "risk-low"

        if risk.lower() == "medium":
            risk_class = "risk-medium"
        elif risk.lower() == "high":
            risk_class = "risk-high"

        rows_html += f"""
<tr>
    <td>{escape(str(row["image"]))}</td>
    <td>{escape(format_disease_name(row["disease"]))}</td>
    <td>{escape(str(row["confidence"]))}%</td>
    <td class="{risk_class}">{escape(risk)}</td>
    <td>{escape(str(row["datetime"]))}</td>
</tr>
"""

    table_html = f"""
<div class="analytics-table-card">
<table class="analytics-table">
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

    st.subheader("🗑️ Delete Prediction Record")

    delete_options = {
        f"{row['image']} | {format_disease_name(row['disease'])} | {row['datetime']}": row["id"]
        for _, row in df.iterrows()
    }

    selected_record = st.selectbox(
        "Select a prediction record to delete",
        list(delete_options.keys())
    )

    if st.button("Delete Selected Record"):
        delete_prediction(
            prediction_id=delete_options[selected_record],
            user_id=st.session_state.user["id"]
        )
        st.success("Prediction record deleted successfully.")
        st.rerun()

    st.subheader("🦠 Disease Distribution")

    disease_counts = df["disease"].apply(format_disease_name).value_counts()

    fig1, ax1 = plt.subplots(figsize=(3.6, 2.4))
    ax1.bar(disease_counts.index, disease_counts.values)
    ax1.set_title("Disease Distribution", fontsize=9)
    ax1.set_xlabel("Disease", fontsize=7)
    ax1.set_ylabel("Count", fontsize=7)
    ax1.tick_params(axis="x", labelrotation=25, labelsize=6)
    ax1.tick_params(axis="y", labelsize=7)
    plt.tight_layout()

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.pyplot(fig1)

    st.subheader("📈 Confidence Trend")

    df = df.reset_index(drop=True)
    df["scan_no"] = range(1, len(df) + 1)

    fig2, ax2 = plt.subplots(figsize=(3.6, 2.4))
    ax2.plot(df["scan_no"], df["confidence"], marker="o", linewidth=1.5, markersize=4)
    ax2.set_title("Confidence Trend", fontsize=9)
    ax2.set_xlabel("Scan Number", fontsize=7)
    ax2.set_ylabel("Confidence (%)", fontsize=7)
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis="both", labelsize=7)
    plt.tight_layout()

    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.pyplot(fig2)

    st.caption("Charts update automatically based on the latest prediction records stored in SQLite.")