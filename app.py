"""
app.py
Simple Search – Main Streamlit entry point.

Run with:
    streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st

# ── Load environment variables ─────────────────────────────────────────────────
load_dotenv()

# ── Init DB (must happen before anything that touches the DB) ──────────────────
from database.db import init_db
init_db()

# ── Seed demo data on first run ───────────────────────────────────────────────
from database.seed_data import seed_if_empty
seed_if_empty()

# ── Page modules ──────────────────────────────────────────────────────────────
from pages import landing, browse, pricing, auth_page, onboarding, feed
from pages import advertiser_dashboard, admin_dashboard
from auth.auth import is_logged_in, is_admin, is_advertiser, logout_user, get_current_user

# ── Streamlit page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Simple Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    /* Dark theme overrides */
    .stApp { background-color: #0d1117; }
    .stSidebar { background-color: #161b22 !important; }
    .stSidebar .stMarkdown, .stSidebar label { color: #c9d1d9 !important; }
    h1, h2, h3 { color: #f0f6fc !important; }
    p, li { color: #8b949e; }
    /* Remove default streamlit branding color from buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }
    /* Container cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    /* Metric styling */
    [data-testid="stMetric"] label { color: #8b949e !important; }
    [data-testid="stMetricValue"] { color: #f0f6fc !important; }
    /* Hide Streamlit default hamburger */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────────
if "nav" not in st.session_state:
    st.session_state["nav"] = "Home"

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding:1rem 0 1.5rem;">
            <div style="font-size:2rem">🔍</div>
            <div style="font-size:1.3rem; font-weight:800; color:#f0f6fc;">Simple Search</div>
            <div style="font-size:0.8rem; color:#8b949e;">Discover. Connect. Grow.</div>
        </div>
    """, unsafe_allow_html=True)

    # Build nav options based on login state / role
    nav_public = ["Home", "Browse", "Pricing"]
    nav_auth = ["Sign Up / Login"]
    nav_user = ["My Feed", "Complete Profile"]
    nav_adv = ["Advertiser Dashboard"]
    nav_admin = ["Admin Dashboard"]
    nav_logout = ["Logout"]

    if is_logged_in():
        options = nav_public + nav_user
        if is_advertiser():
            options += nav_adv
        if is_admin():
            options += nav_admin
        options += nav_logout
    else:
        options = nav_public + nav_auth

    # Clamp nav selection to valid options
    if st.session_state["nav"] not in options:
        st.session_state["nav"] = options[0]

    selected = st.radio(
        "Navigate",
        options,
        index=options.index(st.session_state["nav"]),
        label_visibility="collapsed",
    )
    st.session_state["nav"] = selected

    # Logged-in user info
    if is_logged_in():
        user = get_current_user()
        st.markdown("---")
        st.markdown(
            f"<div style='text-align:center;color:#8b949e;font-size:0.85rem;'>"
            f"👤 {user['full_name']}<br>"
            f"<span style='background:#0f3460;color:#a8b2d8;padding:2px 8px;"
            f"border-radius:10px;font-size:0.75rem'>{user['role'].title()}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

# ── Handle logout ─────────────────────────────────────────────────────────────
if st.session_state["nav"] == "Logout":
    logout_user()
    st.session_state["nav"] = "Home"
    st.rerun()

# ── Route to page ─────────────────────────────────────────────────────────────
page = st.session_state["nav"]

if page == "Home":
    landing.show()
elif page == "Browse":
    browse.show()
elif page == "Pricing":
    pricing.show()
elif page == "Sign Up / Login":
    auth_page.show()
elif page == "Complete Profile":
    onboarding.show()
elif page == "My Feed":
    feed.show()
elif page == "Advertiser Dashboard":
    advertiser_dashboard.show()
elif page == "Admin Dashboard":
    admin_dashboard.show()
