"""
auth/auth.py
Authentication helpers: password hashing, sign-up, login, session management.
"""

import bcrypt
import streamlit as st
from database.db import create_user, get_user_by_email, create_subscription, get_subscription


# ── Password helpers ──────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Return a bcrypt hash of the plain-text password."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True when plain matches the stored hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ── Session helpers ───────────────────────────────────────────────────────────

def login_user(user: dict):
    """Store user info in Streamlit session state."""
    st.session_state["user"] = user
    st.session_state["logged_in"] = True


def logout_user():
    """Clear session state."""
    for key in ["user", "logged_in"]:
        st.session_state.pop(key, None)


def get_current_user() -> dict | None:
    """Return the logged-in user dict or None."""
    return st.session_state.get("user")


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def is_admin() -> bool:
    user = get_current_user()
    return bool(user and user.get("role") == "admin")


def is_advertiser() -> bool:
    user = get_current_user()
    return bool(user and user.get("role") in ("advertiser", "admin"))


# ── Auth actions ──────────────────────────────────────────────────────────────

def attempt_login(email: str, password: str) -> tuple[bool, str]:
    """
    Try to log in with email + password.
    Returns (success: bool, message: str).
    """
    if not email or not password:
        return False, "Please enter email and password."
    user = get_user_by_email(email.strip().lower())
    if not user:
        return False, "No account found with that email."
    if not verify_password(password, user["password_hash"]):
        return False, "Incorrect password."
    login_user(user)
    return True, f"Welcome back, {user['full_name']}!"


def attempt_signup(full_name: str, email: str, password: str,
                   role: str = "user") -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str).
    """
    if not full_name or not email or not password:
        return False, "All fields are required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    email = email.strip().lower()
    if get_user_by_email(email):
        return False, "An account with this email already exists."
    hashed = hash_password(password)
    new_id = create_user(full_name=full_name, email=email,
                         password_hash=hashed, role=role)
    # Auto-create a pending subscription for new users
    if role == "user":
        create_subscription(new_id, "user", "yearly", 52.00)
    elif role == "advertiser":
        create_subscription(new_id, "advertiser", "monthly", 10.00)
    user = get_user_by_email(email)
    login_user(user)
    return True, f"Account created! Welcome, {full_name}."
