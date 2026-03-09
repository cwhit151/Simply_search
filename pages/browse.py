"""
pages/browse.py
Public browse page – searchable, filterable grid of all approved listings.
"""

import streamlit as st
from database.db import get_listings

# ── Constants ─────────────────────────────────────────────────────────────────
CATEGORIES = [
    "All", "Fitness", "Health", "Travel", "Cars", "Geography", "Art",
    "Sports", "Real Estate", "Mechanic", "Investor", "Business Services",
    "Food", "Beauty", "Tech", "Music", "Pets", "Fashion", "Education",
    "Finance", "Photography",
]

US_STATES_FILTER = ["All States"] + [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
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


def _listing_card(listing: dict):
    """Render a single listing card in a styled container."""
    ltype_badge = "🌐 Social" if listing["listing_type"] == "social" else "🏢 Business"
    location = ", ".join(filter(None, [listing.get("city"), listing.get("state")]))

    with st.container(border=True):
        # Header row
        col_info, col_type = st.columns([3, 1])
        with col_info:
            st.markdown(f"### {listing['title']}")
            st.caption(f"📂 {listing['category']}   📍 {location or 'Location N/A'}")
        with col_type:
            st.markdown(f"<br><span style='background:#e94560;color:white;"
                        f"padding:3px 10px;border-radius:12px;font-size:0.8rem;"
                        f"'>{ltype_badge}</span>", unsafe_allow_html=True)

        # Images
        img_cols = []
        imgs = [listing.get("image_url_1"), listing.get("image_url_2")]
        imgs = [i for i in imgs if i]
        if imgs:
            img_cols = st.columns(len(imgs))
            for col, url in zip(img_cols, imgs):
                with col:
                    st.image(url, use_container_width=True)

        # Description
        if listing.get("description"):
            st.markdown(listing["description"][:200] +
                        ("…" if len(listing.get("description", "")) > 200 else ""))

        # Tags
        if listing.get("tags"):
            tag_html = " ".join(
                f"<span style='background:#0f3460;color:#a8b2d8;padding:2px 8px;"
                f"border-radius:10px;font-size:0.78rem;margin-right:4px'>{t.strip()}</span>"
                for t in listing["tags"].split(",") if t.strip()
            )
            st.markdown(tag_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # Links & contact
        link_parts = []
        if listing.get("website_url"):
            link_parts.append(f"[🌐 Website]({listing['website_url']})")
        if listing.get("instagram_url"):
            link_parts.append(f"[📸 Instagram]({listing['instagram_url']})")
        if listing.get("facebook_url"):
            link_parts.append(f"[👍 Facebook]({listing['facebook_url']})")
        if link_parts:
            st.markdown("  ·  ".join(link_parts))

        # Contact
        contact_parts = []
        if listing.get("email"):
            contact_parts.append(f"✉️ {listing['email']}")
        if listing.get("phone"):
            contact_parts.append(f"📞 {listing['phone']}")
        if contact_parts:
            st.caption("  ·  ".join(contact_parts))


def show():
    st.title("🔍 Browse Listings")
    st.markdown("Discover social accounts and businesses curated for you.")

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🎛️ Filters", expanded=True):
        fc1, fc2, fc3 = st.columns([2, 2, 3])
        with fc1:
            selected_type = st.selectbox(
                "Listing type", ["All", "Social Accounts", "Businesses"]
            )
        with fc2:
            selected_category = st.selectbox("Category", CATEGORIES)
        with fc3:
            search_term = st.text_input("🔍 Search keyword",
                                         placeholder="e.g. yoga, vintage, Austin")

        state_col, _ = st.columns([2, 3])
        with state_col:
            selected_state = st.selectbox("State", US_STATES_FILTER)

    # ── Category chips ────────────────────────────────────────────────────────
    st.markdown("**Quick categories:**")
    chip_cols = st.columns(len(CATEGORIES[:8]))
    for i, cat in enumerate(CATEGORIES[1:8]):
        with chip_cols[i]:
            if st.button(cat, key=f"chip_{cat}", use_container_width=True):
                selected_category = cat  # noqa — visual only; actual filter above

    st.markdown("---")

    # ── Build filters dict ────────────────────────────────────────────────────
    filters = {}
    if selected_type == "Social Accounts":
        filters["listing_type"] = "social"
    elif selected_type == "Businesses":
        filters["listing_type"] = "business"
    if selected_category != "All":
        filters["category"] = selected_category
    if selected_state != "All States":
        filters["state"] = selected_state
    if search_term.strip():
        filters["search"] = search_term.strip()

    listings = get_listings(filters)

    # ── Tabs: Social / Business ───────────────────────────────────────────────
    tab_all, tab_social, tab_biz = st.tabs(
        [f"All ({len(listings)})", "🌐 Social Accounts", "🏢 Businesses"]
    )

    social = [l for l in listings if l["listing_type"] == "social"]
    biz = [l for l in listings if l["listing_type"] == "business"]

    def render_grid(items):
        if not items:
            st.info("No listings found. Try adjusting your filters.")
            return
        # 2-column grid
        cols = st.columns(2)
        for idx, listing in enumerate(items):
            with cols[idx % 2]:
                _listing_card(listing)

    with tab_all:
        render_grid(listings)
    with tab_social:
        render_grid(social)
    with tab_biz:
        render_grid(biz)
