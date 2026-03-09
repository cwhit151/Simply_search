"""
pages/admin_dashboard.py
Admin dashboard – view users, approve/reject listings, manage subscriptions, metrics.
"""

import streamlit as st
from auth.auth import get_current_user, is_logged_in, is_admin
from database.db import (
    get_all_users, get_all_listings_admin, update_listing,
    get_all_subscriptions, update_subscription_status,
    get_metrics, update_user,
)


def show():
    if not is_logged_in():
        st.warning("Please log in.")
        return
    if not is_admin():
        st.error("❌ Admin access only.")
        return

    st.title("🛡️ Admin Dashboard")

    # ── Metrics ───────────────────────────────────────────────────────────────
    metrics = get_metrics()
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, (label, val) in zip(
        [m1, m2, m3, m4, m5],
        [
            ("👥 Users", metrics["total_users"]),
            ("📣 Advertisers", metrics["total_advertisers"]),
            ("📋 Listings", metrics["total_listings"]),
            ("✅ Active", metrics["active_listings"]),
            ("🟡 Pending", metrics["pending_listings"]),
        ],
    ):
        with col:
            st.metric(label, val)

    st.markdown("---")

    tab_listings, tab_users, tab_subs = st.tabs(
        ["📋 Listings", "👥 Users", "💳 Subscriptions"]
    )

    # ── Listings tab ──────────────────────────────────────────────────────────
    with tab_listings:
        listings = get_all_listings_admin()
        if not listings:
            st.info("No listings yet.")
        else:
            for listing in listings:
                with st.container(border=True):
                    row1, row2 = st.columns([4, 2])
                    with row1:
                        approved_str = "🟢 Approved" if listing["is_approved"] else "🟡 Pending"
                        active_str = "✅ Active" if listing["is_active"] else "⏸️ Inactive"
                        st.markdown(
                            f"**{listing['title']}** "
                            f"<span style='color:#a8b2d8;font-size:0.85rem'>"
                            f"({listing['listing_type'].title()}) · "
                            f"{listing['category']} · {listing.get('state','N/A')}"
                            f"</span>",
                            unsafe_allow_html=True,
                        )
                        st.caption(f"{approved_str}  ·  {active_str}  ·  owner_id={listing['owner_user_id']}")
                        if listing.get("description"):
                            st.caption(listing["description"][:120] + "…")

                    with row2:
                        col_a, col_r = st.columns(2)
                        with col_a:
                            if not listing["is_approved"]:
                                if st.button("✅ Approve", key=f"appr_{listing['id']}",
                                             use_container_width=True):
                                    update_listing(listing["id"], is_approved=1)
                                    st.rerun()
                            else:
                                if st.button("🚫 Revoke", key=f"revk_{listing['id']}",
                                             use_container_width=True):
                                    update_listing(listing["id"], is_approved=0)
                                    st.rerun()
                        with col_r:
                            toggle_lbl = "⏸️ Deactivate" if listing["is_active"] else "▶️ Activate"
                            if st.button(toggle_lbl, key=f"adm_tog_{listing['id']}",
                                         use_container_width=True):
                                update_listing(listing["id"],
                                               is_active=int(not listing["is_active"]))
                                st.rerun()

    # ── Users tab ─────────────────────────────────────────────────────────────
    with tab_users:
        users = get_all_users()
        if not users:
            st.info("No users yet.")
        else:
            # Build a display table
            import pandas as pd
            df = pd.DataFrame([
                {
                    "ID": u["id"],
                    "Name": u["full_name"],
                    "Email": u["email"],
                    "Role": u["role"],
                    "State": u.get("state") or "",
                    "Joined": u["created_at"][:10],
                }
                for u in users
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("Change user role")
            user_emails = [u["email"] for u in users]
            sel_email = st.selectbox("Select user", user_emails)
            sel_user = next((u for u in users if u["email"] == sel_email), None)
            if sel_user:
                new_role = st.selectbox("New role", ["user", "advertiser", "admin"],
                                         index=["user", "advertiser", "admin"].index(
                                             sel_user["role"]))
                if st.button("Update Role"):
                    update_user(sel_user["id"], role=new_role)
                    st.success(f"Role updated to {new_role} for {sel_email}.")
                    st.rerun()

    # ── Subscriptions tab ─────────────────────────────────────────────────────
    with tab_subs:
        subs = get_all_subscriptions()
        if not subs:
            st.info("No subscriptions yet.")
        else:
            import pandas as pd
            df_s = pd.DataFrame([
                {
                    "Sub ID": s["id"],
                    "User ID": s["user_id"],
                    "Type": s["subscription_type"],
                    "Status": s["status"],
                    "Cycle": s["billing_cycle"],
                    "Amount": f"${s['amount']:.2f}",
                    "Created": s["created_at"][:10],
                }
                for s in subs
            ])
            st.dataframe(df_s, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("Toggle subscription status")
            sub_ids = [s["id"] for s in subs]
            sel_sub_id = st.selectbox("Select subscription ID", sub_ids)
            sel_sub = next((s for s in subs if s["id"] == sel_sub_id), None)
            if sel_sub:
                new_status = st.selectbox(
                    "New status", ["active", "cancelled", "pending"],
                    index=["active", "cancelled", "pending"].index(sel_sub["status"])
                )
                if st.button("Update Status"):
                    update_subscription_status(sel_sub_id, new_status)
                    st.success(f"Subscription {sel_sub_id} → {new_status}")
                    st.rerun()
