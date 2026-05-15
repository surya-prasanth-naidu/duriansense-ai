import streamlit as st
from database import add_user, login_user, reset_password_by_username
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def auth_page():
    bg_image = get_base64_image("assets/login_background.png")

    if "show_reset" not in st.session_state:
        st.session_state.show_reset = False

    if "forgot" in st.query_params:
        st.session_state.show_reset = True
        st.query_params.clear()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(0,0,0,0.45);
        background-blend-mode: darken;
    }}

    section[data-testid="stSidebar"] {{
        display: none;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 1rem;
        max-width: 100%;
    }}

    .main-login-card {{
        width: 100%;
        max-width: 560px;
        margin: auto;
        margin-top: 70px;
    }}

    .stTabs {{
        background: rgba(10, 15, 12, 0.82);
        padding: 30px;
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.14);
        backdrop-filter: blur(24px);
        box-shadow: 0 0 40px rgba(180,255,160,0.15), 0 0 120px rgba(0,0,0,0.55);
    }}

    .login-title {{
        text-align: center;
        color: white;
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 8px;
    }}

    .login-subtitle {{
        text-align: center;
        color: #e5e7eb;
        font-size: 15px;
        margin-bottom: 32px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 5px;
        border: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 28px;
    }}

    .stTabs [data-baseweb="tab"] {{
        width: 50%;
        justify-content: center;
        height: 52px;
        color: white;
        font-weight: 800;
        border-radius: 12px;
        font-size: 15px;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, #9dbd82, #b8ea83);
        color: white;
    }}

    .stTabs [data-baseweb="tab-border"] {{
        display: none;
    }}

    [data-testid="stTextInput"] label,
    [data-testid="stSelectbox"] label {{
        display: none;
    }}

    [data-testid="stTextInput"] input {{
        background: rgba(5, 8, 14, 0.92);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 14px;
        color: white;
        height: 46px;
        padding-left: 16px;
        font-size: 15px;
    }}

    [data-testid="stTextInput"] input::placeholder {{
        color: #c1c5c1;
    }}

    [data-testid="stSelectbox"] div {{
        background: rgba(5, 8, 14, 0.92);
        color: white;
        border-radius: 14px;
    }}

    [data-testid="stCheckbox"] label {{
        color: white;
        font-weight: 600;
        font-size: 14px;
    }}

    div[data-testid="stButton"] button {{
        width: 100% !important;
        height: 56px !important;
        background: linear-gradient(90deg, #97b57d, #b9ea83) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        margin-top: 18px !important;
        box-shadow: 0 0 20px rgba(184,234,131,0.25) !important;
    }}

    div[data-testid="stButton"] button:hover {{
        background: linear-gradient(90deg, #a8cf8d, #caf491) !important;
        color: white !important;
        border: none !important;
    }}

    .forgot-link-box {{
        text-align: right;
        margin-top: 2px;
        padding-top: 0px;
    }}

    .forgot-link-box a {{
        color: #d1d5db !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        text-decoration: none !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}

    .forgot-link-box a:hover {{
        color: #ffffff !important;
        text-decoration: underline !important;
    }}

    div[data-testid="stButton"]:has(#cancel_marker) button {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #b8ea83 !important;
        border: none !important;
        box-shadow: none !important;
        width: auto !important;
        height: auto !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin-top: 10px !important;
        font-size: 13px !important;
    }}

    .auth-footer {{
        margin-top: 36px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.14);
        text-align: center;
        color: #d1d5db;
        font-size: 13px;
        line-height: 1.6;
    }}

    .auth-footer span {{
        color: #b8ea83;
        font-weight: 800;
    }}

    .reset-card {{
        margin-top: 25px;
        padding: 25px;
        border-radius: 20px;
        background: rgba(10,15,12,0.80);
        border: 1px solid rgba(184,234,131,0.18);
        backdrop-filter: blur(18px);
    }}

    .reset-title {{
        font-size: 28px;
        font-weight: 900;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }}

    .reset-subtitle {{
        text-align: center;
        color: #d1d5db;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1.3, 1.4, 1.3])

    with center:
        st.markdown('<div class="main-login-card">', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.markdown("""
            <div class="login-title">🌿 Welcome Back!</div>
            <div class="login-subtitle">Login to your account</div>
            """, unsafe_allow_html=True)

            username = st.text_input("", placeholder="👤 Username", key="login_username")
            password = st.text_input("", placeholder="🔒 Password", type="password", key="login_password")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.checkbox("Remember me", key="remember_me")

            with col2:
                st.markdown("""
                <div class="forgot-link-box">
                    <a href="?forgot=1" target="_self">Forgot Password?</a>
                </div>
                """, unsafe_allow_html=True)

            btn_left, btn_center, btn_right = st.columns([1, 1.4, 1])

            with btn_center:
                login_clicked = st.button("👤 LOGIN TO ACCESS", key="login_btn")

            if login_clicked:
                user = login_user(username, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "id": user[0],
                        "full_name": user[1],
                        "username": user[2],
                        "role": user[3]
                    }
                    st.success("Login successful.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

            if st.session_state.show_reset:
                st.markdown("""
                <div class="reset-card">
                    <div class="reset-title">🔑 Reset Password</div>
                    <div class="reset-subtitle">Enter your username and new password</div>
                </div>
                """, unsafe_allow_html=True)

                reset_username = st.text_input("", placeholder="👤 Enter Username", key="reset_username")
                new_reset_password = st.text_input("", placeholder="🔒 New Password", type="password", key="reset_new_password")
                confirm_reset_password = st.text_input("", placeholder="🔒 Confirm New Password", type="password", key="reset_confirm_password")

                reset_clicked = st.button("✅ RESET PASSWORD", key="reset_password_btn")

                st.markdown('<span id="cancel_marker"></span>', unsafe_allow_html=True)
                cancel_clicked = st.button("Cancel", key="cancel_reset_btn")

                if cancel_clicked:
                    st.session_state.show_reset = False
                    st.rerun()

                if reset_clicked:
                    if not reset_username or not new_reset_password or not confirm_reset_password:
                        st.warning("Please fill in all fields.")
                    elif new_reset_password != confirm_reset_password:
                        st.error("Passwords do not match.")
                    elif len(new_reset_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        result = reset_password_by_username(reset_username, new_reset_password)

                        if result == "success":
                            st.success("Password reset successful. You can now login with your new password.")
                            st.session_state.show_reset = False
                        else:
                            st.error(result)

            st.markdown("""
            <div class="auth-footer">
                <span>DuriaSense AI</span><br>
                Secure access for durian disease detection and smart farming insights.
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <div class="login-title">🌿 Create Account</div>
            <div class="login-subtitle">Register your account</div>
            """, unsafe_allow_html=True)

            full_name = st.text_input("", placeholder="👤 Full Name", key="signup_fullname")
            new_username = st.text_input("", placeholder="👤 Username", key="signup_username")
            new_password = st.text_input("", placeholder="🔒 Password", type="password", key="signup_password")
            role = st.selectbox("", ["Farmer", "Admin"], key="signup_role")

            btn_left, btn_center, btn_right = st.columns([1, 1.4, 1])

            with btn_center:
                signup_clicked = st.button("🌿 CREATE ACCOUNT", key="signup_btn")

            if signup_clicked:
                if full_name and new_username and new_password:
                    success = add_user(full_name, new_username, new_password, role)

                    if success:
                        st.success("Account created successfully.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("""
            <div class="auth-footer">
                <span>DuriaSense AI</span><br>
                Create your account to start managing AI-powered disease detection.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)