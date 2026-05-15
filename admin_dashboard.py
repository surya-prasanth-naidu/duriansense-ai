import streamlit as st
import pandas as pd
from html import escape
from database import get_connection


def format_disease_name(name):
    return str(name).replace("_", " ").title()


def risk_class(risk):
    risk = str(risk).lower()
    if risk == "medium":
        return "risk-medium"
    if risk == "high":
        return "risk-high"
    return "risk-low"


def role_class(role):
    return "role-admin" if str(role) == "Admin" else "role-farmer"


def render_table(headers, rows):
    header_html = "".join([f"<th>{escape(str(h))}</th>" for h in headers])
    body_html = ""

    for row in rows:
        body_html += "<tr>"
        for cell, css_class in row:
            body_html += f'<td class="{css_class}">{cell}</td>'
        body_html += "</tr>"

    return (
        '<table class="admin-table">'
        '<thead><tr>'
        f'{header_html}'
        '</tr></thead>'
        '<tbody>'
        f'{body_html}'
        '</tbody>'
        '</table>'
    )


def admin_dashboard():
    st.markdown("""
<style>
.admin-hero {
    background: rgba(10, 15, 12, 0.72);
    padding: 28px;
    border-radius: 26px;
    border: 1px solid rgba(184,234,131,0.25);
    box-shadow: 0 0 35px rgba(132,204,22,0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
}

.admin-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.admin-subtitle {
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
    margin-bottom: 18px;
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

.admin-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
    font-size: 15px;
}

.admin-table th {
    text-align: left;
    padding: 14px;
    color: #b8ea83;
    border-bottom: 1px solid rgba(184,234,131,0.25);
    background: rgba(184,234,131,0.08);
}

.admin-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}

.admin-table tr:hover {
    background: rgba(184,234,131,0.08);
}

.role-admin {
    color: #93c5fd;
    font-weight: 800;
}

.role-farmer {
    color: #86efac;
    font-weight: 800;
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
""", unsafe_allow_html=True)

    conn = get_connection()

    users_df = pd.read_sql_query(
        "SELECT id, full_name, username, role FROM users ORDER BY id DESC",
        conn
    )

    predictions_df = pd.read_sql_query(
        """
        SELECT 
            predictions.id,
            users.full_name,
            users.username,
            predictions.image_name,
            predictions.disease_result,
            predictions.confidence,
            predictions.risk_level,
            predictions.created_at
        FROM predictions
        JOIN users ON predictions.user_id = users.id
        ORDER BY predictions.id DESC
        """,
        conn
    )

    conn.close()

    total_users = len(users_df)
    total_predictions = len(predictions_df)
    total_farmers = len(users_df[users_df["role"] == "Farmer"])
    total_admins = len(users_df[users_df["role"] == "Admin"])

    st.markdown("""
<div class="admin-hero">
    <div class="admin-title">🧑‍💼 Admin Control Center</div>
    <div class="admin-subtitle">
        Manage DuriaSense AI users, monitor prediction activities, and review system usage from one premium dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">👥 Total Users</div>
    <div class="metric-value">{total_users}</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">🌱 Farmers</div>
    <div class="metric-value">{total_farmers}</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">🛡️ Admins</div>
    <div class="metric-value">{total_admins}</div>
</div>
""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">📸 Predictions</div>
    <div class="metric-value">{total_predictions}</div>
</div>
""", unsafe_allow_html=True)

    user_rows = []

    for _, row in users_df.iterrows():
        user_rows.append([
            (escape(str(row["id"])), ""),
            (escape(str(row["full_name"])), ""),
            (escape(str(row["username"])), ""),
            (escape(str(row["role"])), role_class(row["role"]))
        ])

    user_table = render_table(
        ["User ID", "Full Name", "Username", "Role"],
        user_rows
    )

    st.markdown(
        f'<div class="glass-card"><div class="section-title">👥 Registered Users</div>{user_table}</div>',
        unsafe_allow_html=True
    )

    if not predictions_df.empty:
        prediction_rows = []

        for _, row in predictions_df.head(8).iterrows():
            risk = str(row["risk_level"])

            prediction_rows.append([
                (escape(str(row["full_name"])), ""),
                (escape(str(row["username"])), ""),
                (escape(str(row["image_name"])), ""),
                (escape(format_disease_name(row["disease_result"])), ""),
                (f'{round(float(row["confidence"]), 2)}%', ""),
                (escape(risk), risk_class(risk)),
                (escape(str(row["created_at"])), "")
            ])

        prediction_table = render_table(
            ["Full Name", "Username", "Image", "Disease", "Confidence", "Risk", "Date & Time"],
            prediction_rows
        )

        st.markdown(
            f'<div class="glass-card"><div class="section-title">📋 Recent Prediction Activities</div>{prediction_table}</div>',
            unsafe_allow_html=True
        )

    else:
        st.info("No prediction activities recorded yet.")