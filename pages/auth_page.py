"""
pages/auth_page.py
Authentication page – login and sign-up tabs with form validation.
"""

import streamlit as st
from auth.auth import attempt_login, attempt_signup, is_logged_in


def show():
    if is_logged_in():
        st.success("You are already logged in!")
        if st.button("Go to My Feed"):
            st.session_state["nav"] = "My Feed"
            st.rerun()
        return

    st.title("👤 Account Access")

    # Pre-select tab if coming from pricing CTA
    default_tab = 1 if st.session_state.get("signup_role") else 0

    tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Sign Up"])

    # ── Login tab ─────────────────────────────────────────────────────────────
    with tab_login:
        st.subheader("Welcome back")
        with st.form("login_form"):
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True,
                                              type="primary")

        if submitted:
            success, msg = attempt_login(email, password)
            if success:
                st.success(msg)
                st.session_state.pop("signup_role", None)
                st.session_state["nav"] = "My Feed"
                st.rerun()
            else:
                st.error(msg)

        st.markdown("---")
        st.caption("🔒 Forgot your password? Password reset email coming soon.")

    # ── Sign-up tab ───────────────────────────────────────────────────────────
    with tab_signup:
        st.subheader("Create your account")
        preset_role = st.session_state.get("signup_role", "user")

        with st.form("signup_form"):
            full_name = st.text_input("Full name *", placeholder="Jane Smith")
            email_su = st.text_input("Email address *", placeholder="you@example.com")
            password_su = st.text_input("Password * (min 6 chars)", type="password")
            role = st.selectbox(
                "Account type *",
                options=["user", "advertiser"],
                index=0 if preset_role == "user" else 1,
                format_func=lambda r: "👤 Member ($52/yr)" if r == "user"
                                      else "📣 Advertiser ($10/mo per listing)"
            )
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            submitted_su = st.form_submit_button("Create Account",
                                                  use_container_width=True,
                                                  type="primary")

        if submitted_su:
            if not agree:
                st.warning("Please agree to the Terms of Service to continue.")
            else:
                success, msg = attempt_signup(full_name, email_su, password_su, role)
                if success:
                    st.success(msg)
                    st.session_state.pop("signup_role", None)
                    # Redirect to onboarding
                    st.session_state["nav"] = "Complete Profile"
                    st.rerun()
                else:
                    st.error(msg)
