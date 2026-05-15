import streamlit as st
import base64
from database import create_tables
from auth import auth_page
from farmer_dashboard import farmer_dashboard
from admin_dashboard import admin_dashboard
from prediction_history import prediction_history_page
from analytics import analytics_page
from admin_logs import admin_prediction_logs
from chatbot import chatbot_page
from model_info import model_info_page
from settings import settings_page
from admin_users import admin_users_page
from admin_analytics import admin_analytics_page


st.set_page_config(
    page_title="DurianSense AI",
    page_icon="🌿",
    layout="wide"
)


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def apply_logged_in_background():
    bg_image = get_base64_image("assets/smartpredictionbck.png")

    st.markdown(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
            url("data:image/png;base64,{bg_image}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .block-container {{
        background: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def dashboard_hero(user_name):
    hero_img = get_base64_image("assets/dashboard_hero.png.png")

    css = f"""
    <style>
    .stApp {{
        background:
            linear-gradient(90deg, rgba(4,8,6,0.92), rgba(4,8,6,0.58), rgba(4,8,6,0.20)),
            url("data:image/png;base64,{hero_img}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}

    .block-container {{
        padding-top: 0rem !important;
        padding-left: 3.5rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }}

    .hero-wrapper {{
        min-height: 100vh;
        display: flex;
        align-items: center;
        padding-left: 40px;
    }}

    .hero-content {{
        max-width: 1100px;
        color: white;
    }}

    .hero-kicker {{
        color: #c9f27b;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 18px;
        text-transform: uppercase;
    }}

    .hero-title {{
        font-size: 88px;
        font-weight: 900;
        line-height: 0.95;
        margin-bottom: 25px;
    }}

    .hero-title span {{
        color: #c9f27b;
    }}

    .hero-welcome {{
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 20px;
    }}

    .hero-text {{
        font-size: 26px;
        line-height: 1.6;
        color: #f3f4f6;
        max-width: 1000px;
        margin-bottom: 35px;
    }}

    .typing-box {{
        display: inline-block;
        padding: 20px 28px;
        border-radius: 18px;
        background: rgba(0,0,0,0.42);
        border: 1px solid rgba(201,242,123,0.25);
        margin-bottom: 40px;
        max-width: 1000px;
    }}

    .typing-main {{
        color: #c9f27b;
        font-size: 30px;
        font-weight: 900;
        margin-bottom: 10px;
        animation: glow 1.5s ease-in-out infinite alternate;
    }}

    @keyframes glow {{
        from {{ text-shadow: 0 0 5px rgba(201,242,123,0.25); }}
        to {{ text-shadow: 0 0 25px rgba(201,242,123,0.95); }}
    }}

    .typing-sub {{
        color: white;
        font-size: 21px;
        font-weight: 700;
        line-height: 1.5;
    }}

    .feature-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        max-width: 1100px;
    }}

    .feature-card {{
        background: rgba(0,0,0,0.40);
        padding: 16px 24px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 18px;
        font-weight: 800;
        color: white;
    }}
    </style>
    """

    html = f"""
    <div class="hero-wrapper">
        <div class="hero-content">
            <div class="hero-kicker">Smart Agriculture Dashboard</div>
            <div class="hero-title">AI-Powered <span>Durian Farm</span><br>Disease Monitoring</div>
            <div class="hero-welcome">Welcome, {user_name} 👋</div>
            <div class="hero-text">
                Monitor your durian farm with AI-powered disease detection, prediction history,
                heatmap analysis, and smart farming insights.
            </div>
            <div class="typing-box">
                <div class="typing-main">🌿 Early detection protects healthier durian trees.</div>
                <div class="typing-sub">
                    Upload a leaf image and let AI detect disease symptoms before they spread across your farm.
                </div>
            </div>
            <div class="feature-row">
                <div class="feature-card">📸 Leaf Disease Scan</div>
                <div class="feature-card">🔥 AI Heatmap Focus</div>
                <div class="feature-card">📊 Prediction Insights</div>
                <div class="feature-card">🌱 Smarter Farm Decisions</div>
            </div>
        </div>
    </div>
    """

    st.markdown(css + html, unsafe_allow_html=True)


create_tables()

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 20% 10%, rgba(184,234,131,0.18), transparent 28%),
        linear-gradient(180deg, #173f25 0%, #0c2719 45%, #04100b 100%);
    border-right: 1px solid rgba(184,234,131,0.28);
    box-shadow: 0 0 45px rgba(132,204,22,0.16);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

.sidebar-logo {
    padding: 24px 8px 18px 8px;
    text-align: center;
}

.sidebar-logo-icon {
    font-size: 54px;
    filter: drop-shadow(0 0 14px rgba(184,234,131,0.55));
}

.sidebar-logo-title {
    font-size: 28px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
}

.sidebar-logo-sub {
    font-size: 13px;
    color: #b8ea83;
    margin-top: 6px;
    font-weight: 700;
}

.login-card {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(184,234,131,0.30);
    padding: 18px;
    border-radius: 22px;
    margin: 10px 0 12px 0;
    box-shadow: inset 0 0 20px rgba(184,234,131,0.06);
}

.login-card strong {
    color: #b8ea83;
}

.sidebar-separator {
    height: 1px;
    background: rgba(184,234,131,0.25);
    margin: 16px 0 18px 0;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-size: 16px !important;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
    padding: 11px 14px;
    border-radius: 18px;
    margin-bottom: 10px;
    transition: 0.2s ease;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
    background: rgba(184,234,131,0.14);
    transform: translateX(3px);
}

section[data-testid="stSidebar"] input:checked + div {
    background: linear-gradient(90deg, #86b85d, #b9ec7d) !important;
    color: white !important;
    border-radius: 18px;
    box-shadow: 0 0 22px rgba(184,234,131,0.30);
}

.sidebar-bottom {
    margin-top: 35px;
    padding-bottom: 18px;
}

.sidebar-leaf {
    text-align: center;
    font-size: 85px;
    line-height: 0.9;
    filter: drop-shadow(0 0 18px rgba(184,234,131,0.45));
}

.feedback-box {
    margin-top: 12px;
    padding: 16px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(184,234,131,0.22);
    border-radius: 20px;
    text-align: center;
}

.feedback-title {
    color: #b8ea83;
    font-weight: 900;
    font-size: 14px;
}

.feedback-text {
    color: #d1d5db;
    font-size: 12px;
    margin-top: 8px;
    line-height: 1.5;
}

section[data-testid="stSidebar"] button {
    background: rgba(15,23,42,0.78) !important;
    border: 1px solid rgba(184,234,131,0.32) !important;
    color: white !important;
    border-radius: 14px !important;
    width: 100%;
    margin-top: 8px;
    margin-bottom: 6px;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(184,234,131,0.18) !important;
    border-color: rgba(184,234,131,0.55) !important;
}
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


if not st.session_state.logged_in:
    auth_page()

else:
    user = st.session_state.user

    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🌿</div>
        <div class="sidebar-logo-title">DurianSense AI</div>
        <div class="sidebar-logo-sub">Disease Detection System</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div class="login-card">
        <strong>Logged in as:</strong><br>{user['full_name']}<br><br>
        <strong>Role:</strong> {user['role']}
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown('<div class="sidebar-separator"></div>', unsafe_allow_html=True)

    if user["role"] == "Admin":
        page = st.sidebar.radio(
            "Admin Menu",
            [
                "🏠 Admin Dashboard",
                "👥 Users",
                "📋 Prediction Logs",
                "📊 Analytics",
                "⚙️ Settings"
            ]
        )
    else:
        page = st.sidebar.radio(
            "Farmer Menu",
            [
                "🏠 Dashboard",
                "📷 Smart Prediction",
                "🕘 My Prediction History",
                "📊 Analytics",
                "🤖 AI Chatbot Assistant",
                "📘 Model Information",
                "⚙️ Settings"
            ]
        )

    st.sidebar.markdown("""
    <div class="sidebar-bottom">
        <div class="sidebar-leaf">🌿</div>
        <div class="feedback-box">
            <div class="feedback-title">Help us improve!</div>
            <div class="feedback-text">Your feedback helps make the system better.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if user["role"] == "Admin":
        apply_logged_in_background()

        st.title("🌿 DurianSense AI")
        st.subheader("AI-Powered Durian Disease Detection & Farm Monitoring System")

        if page == "🏠 Admin Dashboard":
            admin_dashboard()
        elif page == "👥 Users":
            admin_users_page()
        elif page == "📋 Prediction Logs":
            admin_prediction_logs()
        elif page == "📊 Analytics":
            admin_analytics_page()
        elif page == "⚙️ Settings":
            settings_page()

    else:
        if page == "🏠 Dashboard":
            dashboard_hero(user["full_name"])

        else:
            apply_logged_in_background()

            st.title("🌿 DurianSense AI")
            st.subheader("AI-Powered Durian Disease Detection & Farm Monitoring System")

            if page == "📷 Smart Prediction":
                farmer_dashboard()
            elif page == "🕘 My Prediction History":
                prediction_history_page()
            elif page == "📊 Analytics":
                analytics_page()
            elif page == "🤖 AI Chatbot Assistant":
                chatbot_page()
            elif page == "📘 Model Information":
                model_info_page()
            elif page == "⚙️ Settings":
                settings_page()