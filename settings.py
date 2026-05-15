import streamlit as st
from database import change_password

def settings_page():
    st.header("⚙️ Settings")

    user = st.session_state.user

    st.subheader("👤 Profile Information")
    st.write(f"**Full Name:** {user['full_name']}")
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Role:** {user['role']}")

    st.divider()

    st.subheader("🔐 Change Password")

    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not old_password or not new_password or not confirm_password:
            st.warning("Please fill in all password fields.")

        elif new_password != confirm_password:
            st.error("New password and confirm password do not match.")

        elif len(new_password) < 6:
            st.error("New password must be at least 6 characters.")

        else:
            result = change_password(
                user_id=user["id"],
                old_password=old_password,
                new_password=new_password
            )

            if result == "success":
                st.success("Password updated successfully. Please use your new password next time.")
            else:
                st.error(result)

    st.divider()

    