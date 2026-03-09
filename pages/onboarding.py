"""
pages/onboarding.py
User onboarding form – collects profile details used for recommendations.
"""

import json
import streamlit as st
from auth.auth import get_current_user, is_logged_in
from database.db import update_user, get_user_by_id

# ── Available categories (mirrors listing categories) ──────────────────────────
INTERESTS = [
    "Fitness", "Health", "Travel", "Cars", "Geography", "Art", "Sports",
    "Real Estate", "Mechanic", "Investor", "Business Services", "Food",
    "Beauty", "Tech", "Music", "Pets", "Fashion", "Education", "Finance",
    "Photography",
]

US_STATES = [
    "", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]


def show():
    if not is_logged_in():
        st.warning("Please log in first.")
        if st.button("Go to Login"):
            st.session_state["nav"] = "Sign Up / Login"
            st.rerun()
        return

    user = get_current_user()
    st.title("🎨 Complete Your Profile")
    st.markdown(
        "Help us personalise your experience. "
        "Your data is used only to surface relevant listings."
    )
    st.markdown("---")

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("📱 Phone number", value=user.get("phone") or "",
                                   placeholder="555-123-4567")
            state = st.selectbox("📍 State", options=US_STATES,
                                  index=US_STATES.index(user.get("state") or "")
                                  if user.get("state") in US_STATES else 0)
            city = st.text_input("🏙️ City (optional)", value=user.get("city") or "")

        with col2:
            instagram_handle = st.text_input(
                "📸 Instagram handle (optional)",
                value=user.get("instagram_handle") or "",
                placeholder="@yourhandle"
            )
            facebook_handle = st.text_input(
                "👍 Facebook handle (optional)",
                value=user.get("facebook_handle") or "",
                placeholder="yourpage"
            )

        st.markdown("#### 🎯 Interests")
        st.caption("Select all that apply — used to rank your discovery feed.")
        # Parse existing interests
        existing_interests = []
        try:
            existing_interests = json.loads(user.get("interests") or "[]")
        except Exception:
            pass
        selected_interests = st.multiselect(
            "Choose your interests",
            options=INTERESTS,
            default=[i for i in existing_interests if i in INTERESTS],
        )

        st.markdown("#### 💚 What do you like?")
        likes = st.text_area(
            "Keywords you love (comma-separated)",
            value=user.get("likes") or "",
            placeholder="e.g. hiking, coffee, vintage cars, Italian food",
            height=80,
        )

        st.markdown("#### 🚫 What do you dislike?")
        dislikes = st.text_area(
            "Keywords to avoid (comma-separated)",
            value=user.get("dislikes") or "",
            placeholder="e.g. fast food, loud music",
            height=80,
        )

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True,
                                           type="primary")

    if submitted:
        update_user(
            user["id"],
            phone=phone,
            state=state,
            city=city,
            interests=json.dumps(selected_interests),
            likes=likes.strip(),
            dislikes=dislikes.strip(),
            instagram_handle=instagram_handle.strip(),
            facebook_handle=facebook_handle.strip(),
        )
        # Refresh session user
        refreshed = get_user_by_id(user["id"])
        st.session_state["user"] = refreshed
        st.success("✅ Profile saved! Your feed has been updated.")
        st.balloons()
        import time; time.sleep(1)
        st.session_state["nav"] = "My Feed"
        st.rerun()
