"""
pages/feed.py
Personalised recommendation feed for logged-in users.
"""

import json
import streamlit as st
from auth.auth import get_current_user, is_logged_in
from utils.recommendations import get_recommended_listings, score_listing


def show():
    if not is_logged_in():
        st.warning("Please log in to see your personalised feed.")
        if st.button("Log In"):
            st.session_state["nav"] = "Sign Up / Login"
            st.rerun()
        return

    user = get_current_user()
    st.title(f"✨ Your Feed, {user['full_name'].split()[0]}")

    # ── Profile completeness nudge ─────────────────────────────────────────────
    interests_raw = user.get("interests", "[]") or "[]"
    try:
        interests = json.loads(interests_raw)
    except Exception:
        interests = []

    if not interests:
        st.warning(
            "🎯 **Your feed is empty because your profile is incomplete.** "
            "Add your interests to unlock personalised recommendations."
        )
        if st.button("Complete My Profile"):
            st.session_state["nav"] = "Complete Profile"
            st.rerun()
        return

    # ── Profile summary chips ─────────────────────────────────────────────────
    interest_html = " ".join(
        f"<span style='background:#0f3460;color:#a8b2d8;padding:3px 10px;"
        f"border-radius:12px;font-size:0.82rem;margin-right:4px'>{i}</span>"
        for i in interests
    )
    location = ", ".join(filter(None, [user.get("city"), user.get("state")]))
    st.markdown(
        f"**Your interests:** {interest_html}"
        + (f"  &nbsp;·&nbsp; 📍 {location}" if location else ""),
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Recommendations ────────────────────────────────────────────────────────
    listings = get_recommended_listings(user, limit=20)
    if not listings:
        st.info("No listings match your profile yet — check back soon as more join!")
        return

    st.subheader(f"🔥 {len(listings)} listings matched for you")

    col1, col2 = st.columns(2)
    for idx, listing in enumerate(listings):
        score = score_listing(listing, user)
        ltype_badge = "🌐 Social" if listing["listing_type"] == "social" else "🏢 Business"
        location_l = ", ".join(filter(None, [listing.get("city"), listing.get("state")]))

        with (col1 if idx % 2 == 0 else col2):
            with st.container(border=True):
                hdr, badge = st.columns([3, 1])
                with hdr:
                    st.markdown(f"### {listing['title']}")
                    st.caption(
                        f"📂 {listing['category']}   📍 {location_l or 'N/A'}"
                    )
                with badge:
                    st.markdown(
                        f"<br><span style='background:#e94560;color:white;"
                        f"padding:3px 8px;border-radius:12px;font-size:0.78rem;"
                        f"'>{ltype_badge}</span><br>"
                        f"<span style='color:#a8b2d8;font-size:0.78rem;'>⭐ score {score}</span>",
                        unsafe_allow_html=True,
                    )

                imgs = [listing.get("image_url_1"), listing.get("image_url_2")]
                imgs = [i for i in imgs if i]
                if imgs:
                    ic = st.columns(len(imgs))
                    for col, url in zip(ic, imgs):
                        col.image(url, use_container_width=True)

                if listing.get("description"):
                    st.markdown(
                        listing["description"][:180]
                        + ("…" if len(listing["description"]) > 180 else "")
                    )

                # Tags
                if listing.get("tags"):
                    tag_html = " ".join(
                        f"<span style='background:#0f3460;color:#a8b2d8;"
                        f"padding:2px 7px;border-radius:10px;"
                        f"font-size:0.75rem;margin-right:3px'>{t.strip()}</span>"
                        for t in listing["tags"].split(",") if t.strip()
                    )
                    st.markdown(tag_html + "<br>", unsafe_allow_html=True)

                # Links
                links = []
                if listing.get("website_url"):
                    links.append(f"[🌐 Website]({listing['website_url']})")
                if listing.get("instagram_url"):
                    links.append(f"[📸 Instagram]({listing['instagram_url']})")
                if listing.get("facebook_url"):
                    links.append(f"[👍 Facebook]({listing['facebook_url']})")
                if links:
                    st.markdown("  ·  ".join(links))

                contact = []
                if listing.get("email"):
                    contact.append(f"✉️ {listing['email']}")
                if listing.get("phone"):
                    contact.append(f"📞 {listing['phone']}")
                if contact:
                    st.caption("  ·  ".join(contact))
