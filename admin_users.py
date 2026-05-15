import streamlit as st
import pandas as pd
from html import escape
from database import get_connection


def role_class(role):
    return "role-admin" if str(role) == "Admin" else "role-farmer"


def admin_users_page():
    st.markdown("""
<style>
.users-hero {
    background: rgba(10, 15, 12, 0.72);
    padding: 28px;
    border-radius: 26px;
    border: 1px solid rgba(184,234,131,0.25);
    box-shadow: 0 0 35px rgba(132,204,22,0.12);
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
}

.users-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    margin-bottom: 8px;
}

.users-subtitle {
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

.user-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
    font-size: 15px;
}

.user-table th {
    text-align: left;
    padding: 14px;
    color: #b8ea83;
    border-bottom: 1px solid rgba(184,234,131,0.25);
    background: rgba(184,234,131,0.08);
}

.user-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}

.user-table tr:hover {
    background: rgba(184,234,131,0.08);
}

.role-admin {
    color: #93c5fd;
    font-weight: 900;
}

.role-farmer {
    color: #86efac;
    font-weight: 900;
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
    conn.close()

    st.markdown("""
<div class="users-hero">
    <div class="users-title">👥 User Management</div>
    <div class="users-subtitle">
        View all registered DuriaSense AI users, monitor farmer accounts, and manage system access overview.
    </div>
</div>
""", unsafe_allow_html=True)

    if users_df.empty:
        st.info("No registered users found.")
        return

    total_users = len(users_df)
    total_farmers = len(users_df[users_df["role"] == "Farmer"])
    total_admins = len(users_df[users_df["role"] == "Admin"])

    col1, col2, col3 = st.columns(3)

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

    rows_html = ""

    for _, row in users_df.iterrows():
        role = str(row["role"])

        rows_html += (
            "<tr>"
            f"<td>{escape(str(row['id']))}</td>"
            f"<td>{escape(str(row['full_name']))}</td>"
            f"<td>{escape(str(row['username']))}</td>"
            f"<td class='{role_class(role)}'>{escape(role)}</td>"
            "</tr>"
        )

    table_html = (
        "<div class='glass-card'>"
        "<div class='section-title'>📋 Registered Users</div>"
        "<table class='user-table'>"
        "<thead>"
        "<tr>"
        "<th>User ID</th>"
        "<th>Full Name</th>"
        "<th>Username</th>"
        "<th>Role</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        f"{rows_html}"
        "</tbody>"
        "</table>"
        "</div>"
    )

    st.markdown(table_html, unsafe_allow_html=True)