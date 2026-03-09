"""
pages/advertiser_dashboard.py
Advertiser dashboard – create, edit, delete and toggle listings.
"""

import streamlit as st
from auth.auth import get_current_user, is_logged_in, is_advertiser
from database.db import (
    get_listings_by_owner, create_listing, update_listing,
    delete_listing, get_listing_by_id, get_subscription,
)

CATEGORIES = [
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


def _listing_form(prefix: str, defaults: dict | None = None) -> dict | None:
    """
    Render the listing creation/edit form.
    Returns a dict of field values on submit, else None.
    """
    d = defaults or {}
    with st.form(f"{prefix}_listing_form"):
        st.markdown("#### Basic Info")
        c1, c2 = st.columns(2)
        with c1:
            listing_type = st.selectbox(
                "Listing type *",
                ["social", "business"],
                index=0 if d.get("listing_type", "social") == "social" else 1,
                format_func=lambda t: "🌐 Social Account" if t == "social" else "🏢 Business",
            )
            title = st.text_input("Title *", value=d.get("title", ""),
                                   placeholder="e.g. FitLife Austin")
            category = st.selectbox(
                "Category *", CATEGORIES,
                index=CATEGORIES.index(d["category"]) if d.get("category") in CATEGORIES else 0
            )
        with c2:
            state = st.selectbox(
                "State", US_STATES,
                index=US_STATES.index(d["state"]) if d.get("state") in US_STATES else 0
            )
            city = st.text_input("City", value=d.get("city", ""))
            tags = st.text_input("Tags (comma-separated)",
                                  value=d.get("tags", ""),
                                  placeholder="yoga, wellness, austin")

        st.markdown("#### Description")
        description = st.text_area("Short description", value=d.get("description", ""),
                                    height=100, max_chars=500)

        st.markdown("#### Contact & Links")
        l1, l2 = st.columns(2)
        with l1:
            email = st.text_input("Email", value=d.get("email", ""))
            phone = st.text_input("Phone", value=d.get("phone", ""))
            website_url = st.text_input("Website URL", value=d.get("website_url", ""))
        with l2:
            instagram_url = st.text_input("Instagram URL", value=d.get("instagram_url", ""))
            facebook_url = st.text_input("Facebook URL", value=d.get("facebook_url", ""))

        st.markdown("#### Images (URLs)")
        img1 = st.text_input("Image 1 URL", value=d.get("image_url_1", ""),
                             placeholder="https://…")
        img2 = st.text_input("Image 2 URL", value=d.get("image_url_2", ""),
                             placeholder="https://… (optional)")

        submitted = st.form_submit_button("💾 Save Listing", use_container_width=True,
                                          type="primary")

    if submitted:
        if not title.strip():
            st.error("Title is required.")
            return None
        return dict(
            listing_type=listing_type, title=title.strip(), category=category,
            tags=tags.strip(), description=description.strip(), state=state,
            city=city.strip(), email=email.strip(), phone=phone.strip(),
            website_url=website_url.strip(), instagram_url=instagram_url.strip(),
            facebook_url=facebook_url.strip(), image_url_1=img1.strip(),
            image_url_2=img2.strip(),
        )
    return None


def show():
    if not is_logged_in():
        st.warning("Please log in.")
        return
    if not is_advertiser():
        st.error("❌ This area is for advertisers only. Please upgrade your account.")
        if st.button("See Pricing"):
            st.session_state["nav"] = "Pricing"
            st.rerun()
        return

    user = get_current_user()
    st.title("📣 Advertiser Dashboard")

    # ── Subscription status widget ─────────────────────────────────────────────
    sub = get_subscription(user["id"])
    if sub:
        status_color = "#2ecc71" if sub["status"] == "active" else "#e94560"
        st.markdown(
            f"<div style='background:#16213e;border:1px solid #0f3460;border-radius:8px;"
            f"padding:0.75rem 1.2rem;margin-bottom:1rem;'>"
            f"💳 <b>Subscription:</b> {sub['subscription_type'].title()} "
            f"· <span style='color:{status_color}'>{sub['status'].upper()}</span> "
            f"· ${sub['amount']:.2f}/{sub['billing_cycle']}"
            f"<span style='float:right;color:#a8b2d8;font-size:0.8rem;'>"
            f"⚠️ Billing is mocked for MVP</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_list, tab_create = st.tabs(["📋 My Listings", "➕ Create New Listing"])

    # ── My Listings ───────────────────────────────────────────────────────────
    with tab_list:
        listings = get_listings_by_owner(user["id"])
        if not listings:
            st.info("You haven't created any listings yet. Go to **Create New Listing**.")
        else:
            for listing in listings:
                with st.container(border=True):
                    hdr, controls = st.columns([3, 2])
                    with hdr:
                        status_icon = "✅" if listing["is_active"] else "⏸️"
                        approved_str = (
                            "🟢 Approved" if listing["is_approved"]
                            else "🟡 Pending Review"
                        )
                        st.markdown(f"**{status_icon} {listing['title']}**")
                        st.caption(
                            f"📂 {listing['category']}  ·  "
                            f"{'🌐 Social' if listing['listing_type']=='social' else '🏢 Business'}  ·  "
                            f"{approved_str}"
                        )

                    with controls:
                        col_toggle, col_del = st.columns(2)
                        with col_toggle:
                            new_active = not listing["is_active"]
                            btn_label = "⏸️ Deactivate" if listing["is_active"] else "▶️ Activate"
                            if st.button(btn_label, key=f"toggle_{listing['id']}",
                                         use_container_width=True):
                                update_listing(listing["id"], is_active=int(new_active))
                                st.rerun()
                        with col_del:
                            if st.button("🗑️ Delete", key=f"del_{listing['id']}",
                                         use_container_width=True):
                                delete_listing(listing["id"])
                                st.success("Listing deleted.")
                                st.rerun()

                    # Inline edit expander
                    with st.expander("✏️ Edit listing"):
                        data = _listing_form(f"edit_{listing['id']}", defaults=listing)
                        if data:
                            update_listing(listing["id"], **data)
                            st.success("Listing updated!")
                            st.rerun()

    # ── Create Listing ────────────────────────────────────────────────────────
    with tab_create:
        st.subheader("New Listing")
        data = _listing_form("create")
        if data:
            create_listing(owner_user_id=user["id"], **data)
            st.success("🎉 Listing submitted for review!")
            st.session_state["nav"] = "Advertiser Dashboard"
            st.rerun()
