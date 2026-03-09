"""
pages/landing.py
Public landing page – headline, value props, and CTAs.
"""

import streamlit as st


def show():
    # ── Hero section ──────────────────────────────────────────────────────────
    st.markdown("""
        <style>
        .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .hero h1 { color: #e94560; font-size: 2.8rem; margin-bottom: 0.5rem; }
        .hero p  { color: #a8b2d8; font-size: 1.2rem; max-width: 600px; margin: 0 auto 1.5rem; }
        .badge {
            display: inline-block;
            background: #e94560;
            color: white;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .card {
            background: #16213e;
            border: 1px solid #0f3460;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
        }
        .card h3 { color: #e94560; margin-top: 0; }
        .card p  { color: #a8b2d8; }
        .stat-num { font-size: 2rem; font-weight: 700; color: #e94560; }
        .stat-lbl { color: #a8b2d8; font-size: 0.9rem; }
        </style>

        <div class="hero">
            <div class="badge">🚀 Simple Search</div>
            <h1>Discover. Connect. Grow.</h1>
            <p>
                A searchable discovery platform where real people find niche accounts,
                small businesses, and local services — without algorithm noise.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── CTAs ──────────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔍  Browse Listings", use_container_width=True, type="primary"):
            st.session_state["nav"] = "Browse"
            st.rerun()
    with col2:
        if st.button("✨  Sign Up Free", use_container_width=True):
            st.session_state["nav"] = "Sign Up / Login"
            st.rerun()
    with col3:
        if st.button("💼  Advertise Here", use_container_width=True):
            st.session_state["nav"] = "Pricing"
            st.rerun()

    st.markdown("---")

    # ── Value props ───────────────────────────────────────────────────────────
    st.subheader("Why Simple Search?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="card">
                <h3>🔎 Curated Discovery</h3>
                <p>Browse handpicked social accounts and local businesses filtered by
                   your interests, location, and lifestyle.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="card">
                <h3>💰 Affordable Ads</h3>
                <p>List your social page or business for just <strong style="color:#e94560">$10/month</strong>.
                   No middlemen, no bidding wars — just results.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="card">
                <h3>🎯 Personalised Feed</h3>
                <p>Create your profile once. Our matching engine surfaces the most
                   relevant listings based on your interests and location.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats bar ─────────────────────────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("$52", "/ year for members"),
        ("$10", "/ month per listing"),
        ("15+", "discovery categories"),
        ("100%", "human-curated"),
    ]
    for col, (num, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
                <div style="text-align:center; padding:1rem 0;">
                    <div class="stat-num">{num}</div>
                    <div class="stat-lbl">{lbl}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── How it works ──────────────────────────────────────────────────────────
    st.subheader("How It Works")
    h1, h2, h3 = st.columns(3)
    steps = [
        ("1️⃣", "Create Your Profile",
         "Tell us your interests, location, and what you love. Takes 2 minutes."),
        ("2️⃣", "Get Matched",
         "Our algorithm instantly ranks listings by relevance — no doomscrolling required."),
        ("3️⃣", "Discover & Connect",
         "Reach out directly via listings. No DM spam, no gatekeeping."),
    ]
    for col, (icon, title, desc) in zip([h1, h2, h3], steps):
        with col:
            st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Footer CTA ────────────────────────────────────────────────────────────
    st.info("🌟 Ready to explore? **Sign up free** and discover what's out there.")
