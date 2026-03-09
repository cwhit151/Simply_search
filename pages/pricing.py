"""
pages/pricing.py
Pricing page – compare user and advertiser plans.
"""

import streamlit as st


def show():
    st.title("💳 Pricing Plans")
    st.markdown("Simple, transparent pricing — no hidden fees, no contracts.")
    st.markdown("---")

    st.markdown("""
        <style>
        .plan-card {
            background: #16213e;
            border: 2px solid #0f3460;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            height: 100%;
        }
        .plan-card.featured { border-color: #e94560; }
        .plan-price { font-size: 2.5rem; font-weight: 800; color: #e94560; }
        .plan-period { color: #a8b2d8; font-size: 0.95rem; }
        .plan-title { color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.25rem; }
        .plan-sub { color: #a8b2d8; font-size: 0.9rem; margin-bottom: 1.5rem; }
        .feature-row { color: #cdd6f4; text-align: left; padding: 0.3rem 0;
                       border-bottom: 1px solid #0f3460; font-size: 0.9rem; }
        .badge-pop { background: #e94560; color: white; border-radius: 20px;
                     padding: 3px 12px; font-size: 0.8rem; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

    col_user, col_adv = st.columns(2)

    # ── User plan ─────────────────────────────────────────────────────────────
    with col_user:
        st.markdown("""
            <div class="plan-card">
                <div class="plan-title">🙋 Member Plan</div>
                <div class="plan-sub">For individuals who want to discover</div>
                <div class="plan-price">$52</div>
                <div class="plan-period">per year &nbsp;·&nbsp; ~$4.33/month</div>
                <br>
                <div class="feature-row">✅ Personalised recommendation feed</div>
                <div class="feature-row">✅ Unlimited browsing & search</div>
                <div class="feature-row">✅ Category & location filters</div>
                <div class="feature-row">✅ Direct contact with businesses</div>
                <div class="feature-row">✅ Profile with interests & lifestyle</div>
                <div class="feature-row">❌ Cannot create listings</div>
                <br>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Get Member Access", key="cta_user", use_container_width=True):
            st.session_state["nav"] = "Sign Up / Login"
            st.rerun()

    # ── Advertiser plan ───────────────────────────────────────────────────────
    with col_adv:
        st.markdown("""
            <div class="plan-card featured">
                <span class="badge-pop">⭐ Most Popular</span><br><br>
                <div class="plan-title">📣 Advertiser Plan</div>
                <div class="plan-sub">For brands and businesses ready to grow</div>
                <div class="plan-price">$10</div>
                <div class="plan-period">per month · per listing</div>
                <br>
                <div class="feature-row">✅ Create unlimited listings</div>
                <div class="feature-row">✅ Social account OR business card</div>
                <div class="feature-row">✅ Up to 2 images per listing</div>
                <div class="feature-row">✅ Full contact info & external links</div>
                <div class="feature-row">✅ Appear in personalised feeds</div>
                <div class="feature-row">✅ Toggle listings active/inactive</div>
                <div class="feature-row">✅ Dashboard to manage all listings</div>
                <br>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Advertising", key="cta_adv", use_container_width=True,
                     type="primary"):
            st.session_state["nav"] = "Sign Up / Login"
            st.session_state["signup_role"] = "advertiser"
            st.rerun()

    st.markdown("---")

    # ── Comparison table ──────────────────────────────────────────────────────
    st.subheader("Full Feature Comparison")
    features = [
        ("Feature", "Member ($52/yr)", "Advertiser ($10/mo/listing)"),
        ("Browse all listings", "✅", "✅"),
        ("Personalised recommendations", "✅", "✅"),
        ("Category & location filters", "✅", "✅"),
        ("Create listings", "❌", "✅"),
        ("Upload images", "❌", "Up to 2"),
        ("Social account listings", "❌", "✅"),
        ("Business profile cards", "❌", "✅"),
        ("Appear in discovery feed", "❌", "✅"),
        ("Advertiser dashboard", "❌", "✅"),
        ("Multiple listings", "❌", "✅"),
    ]
    header = features[0]
    rows = features[1:]
    col_a, col_b, col_c = st.columns([3, 2, 2])
    col_a.markdown(f"**{header[0]}**")
    col_b.markdown(f"**{header[1]}**")
    col_c.markdown(f"**{header[2]}**")
    st.markdown("<hr style='margin:4px 0'>", unsafe_allow_html=True)
    for feat, mem, adv in rows:
        ca, cb, cc = st.columns([3, 2, 2])
        ca.write(feat)
        cb.write(mem)
        cc.write(adv)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Payment is mocked for MVP.** In production, Stripe will handle billing.")
