"""
database/seed_data.py
Demo seed data loader.

Inserts:
  - 1 admin account
  - 2 advertiser accounts
  - 3 regular user accounts
  - 10 listings (mix of social and business) – all pre-approved
  - Subscriptions for all accounts

Only runs when the DB is empty (idempotent via seed_if_empty()).
"""

import json
from auth.auth import hash_password
from database.db import (
    get_connection, create_user, create_listing,
    create_subscription, get_user_by_email, update_listing,
)


def seed_if_empty():
    """Run seeding only if no users exist yet."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    if count > 0:
        return  # Already seeded

    _seed()


def _seed():
    # ── Admin ──────────────────────────────────────────────────────────────────
    admin_id = create_user(
        full_name="Admin User",
        email="admin@simplesearch.com",
        password_hash=hash_password("admin123"),
        role="admin",
        state="Texas",
        city="Austin",
        interests=json.dumps(["Tech", "Business Services"]),
    )

    # ── Advertisers ────────────────────────────────────────────────────────────
    adv1_id = create_user(
        full_name="Maya Fitness",
        email="maya@fitlife.com",
        password_hash=hash_password("password123"),
        role="advertiser",
        phone="512-555-0101",
        state="Texas",
        city="Austin",
        interests=json.dumps(["Fitness", "Health"]),
        likes="yoga, wellness, organic",
        instagram_handle="@mayafitlife",
    )
    create_subscription(adv1_id, "advertiser", "monthly", 10.00)

    adv2_id = create_user(
        full_name="Carlos Auto Works",
        email="carlos@autoworks.com",
        password_hash=hash_password("password123"),
        role="advertiser",
        phone="303-555-0202",
        state="Colorado",
        city="Denver",
        interests=json.dumps(["Cars", "Mechanic"]),
        likes="cars, trucks, engine, repair",
    )
    create_subscription(adv2_id, "advertiser", "monthly", 10.00)

    # ── Regular users ──────────────────────────────────────────────────────────
    u1_id = create_user(
        full_name="Jordan Lee",
        email="jordan@example.com",
        password_hash=hash_password("password123"),
        role="user",
        state="Texas",
        city="Houston",
        interests=json.dumps(["Fitness", "Food", "Travel"]),
        likes="tacos, hiking, yoga",
        dislikes="fast food, loud",
        instagram_handle="@jordanlee",
    )
    create_subscription(u1_id, "user", "yearly", 52.00)

    u2_id = create_user(
        full_name="Priya Sharma",
        email="priya@example.com",
        password_hash=hash_password("password123"),
        role="user",
        state="California",
        city="Los Angeles",
        interests=json.dumps(["Beauty", "Fashion", "Photography"]),
        likes="skincare, art, portraits",
        dislikes="spam",
    )
    create_subscription(u2_id, "user", "yearly", 52.00)

    u3_id = create_user(
        full_name="Derek Nguyen",
        email="derek@example.com",
        password_hash=hash_password("password123"),
        role="user",
        state="Colorado",
        city="Boulder",
        interests=json.dumps(["Cars", "Sports", "Tech"]),
        likes="cars, motorsport, gadgets",
        dislikes="country music",
    )
    create_subscription(u3_id, "user", "yearly", 52.00)

    # ── Listings ───────────────────────────────────────────────────────────────
    PLACEHOLDER_FITNESS = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80"
    PLACEHOLDER_YOGA = "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&q=80"
    PLACEHOLDER_CAR = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=80"
    PLACEHOLDER_FOOD = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=80"
    PLACEHOLDER_TRAVEL = "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600&q=80"
    PLACEHOLDER_BEAUTY = "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80"
    PLACEHOLDER_TECH = "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80"
    PLACEHOLDER_SPORT = "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&q=80"

    listings_seed = [
        # Social accounts
        dict(
            owner_user_id=adv1_id, listing_type="social",
            title="FitLife Austin 🏋️", category="Fitness",
            tags="yoga, wellness, austin, fitness",
            description="Daily workout tips, healthy recipes, and Austin gym culture. "
                        "Follow for motivation and local fitness events.",
            state="Texas", city="Austin",
            email="maya@fitlife.com", phone="512-555-0101",
            instagram_url="https://instagram.com/fitlifeaustin",
            image_url_1=PLACEHOLDER_FITNESS, image_url_2=PLACEHOLDER_YOGA,
        ),
        dict(
            owner_user_id=adv1_id, listing_type="social",
            title="Mindful Maya 🧘", category="Health",
            tags="mindfulness, meditation, health, wellness",
            description="Guided meditations, breathwork sessions, and mental wellness "
                        "content for busy professionals.",
            state="Texas", city="Austin",
            email="maya@fitlife.com",
            instagram_url="https://instagram.com/mindfulmaya",
            facebook_url="https://facebook.com/mindfulmaya",
            image_url_1=PLACEHOLDER_YOGA,
        ),
        # Businesses
        dict(
            owner_user_id=adv2_id, listing_type="business",
            title="Carlos Auto Works 🔧", category="Mechanic",
            tags="cars, repair, mechanic, denver, truck",
            description="Full-service auto repair in Denver. Specializing in "
                        "European and domestic vehicles. Family-owned since 2008.",
            state="Colorado", city="Denver",
            email="carlos@autoworks.com", phone="303-555-0202",
            website_url="https://carlosautoworks.example.com",
            image_url_1=PLACEHOLDER_CAR,
        ),
        dict(
            owner_user_id=adv2_id, listing_type="social",
            title="Denver Gearheads 🚗", category="Cars",
            tags="cars, meet, motorsport, colorado, gearhead",
            description="Colorado's biggest car enthusiast community. Weekly meets, "
                        "track days, and car culture content.",
            state="Colorado", city="Denver",
            instagram_url="https://instagram.com/denvergearheads",
            image_url_1=PLACEHOLDER_CAR,
        ),
        dict(
            owner_user_id=adv1_id, listing_type="business",
            title="Green Plate Kitchen 🥗", category="Food",
            tags="food, vegan, healthy, austin, meal prep",
            description="Plant-based meal prep service in Austin. Weekly boxes "
                        "crafted by nutritionists. Delivery across Travis County.",
            state="Texas", city="Austin",
            email="hello@greenplate.example.com", phone="512-555-0303",
            website_url="https://greenplate.example.com",
            image_url_1=PLACEHOLDER_FOOD,
        ),
        dict(
            owner_user_id=adv2_id, listing_type="business",
            title="Wanderlust Travel Co. ✈️", category="Travel",
            tags="travel, adventure, tours, colorado, hiking",
            description="Boutique travel agency specialising in outdoor adventures "
                        "and off-the-beaten-path destinations. Colorado HQ.",
            state="Colorado", city="Boulder",
            email="info@wanderlust.example.com", phone="720-555-0404",
            website_url="https://wanderlust.example.com",
            instagram_url="https://instagram.com/wanderlusttravel",
            image_url_1=PLACEHOLDER_TRAVEL,
        ),
        dict(
            owner_user_id=adv1_id, listing_type="social",
            title="Glow Up Beauty 💄", category="Beauty",
            tags="beauty, skincare, makeup, tutorials",
            description="Honest product reviews, skincare routines, and makeup "
                        "tutorials for every skin tone. Based in LA.",
            state="California", city="Los Angeles",
            instagram_url="https://instagram.com/glowupbeauty",
            image_url_1=PLACEHOLDER_BEAUTY, image_url_2=PLACEHOLDER_BEAUTY,
        ),
        dict(
            owner_user_id=adv2_id, listing_type="business",
            title="Byte Forward Tech 💻", category="Tech",
            tags="tech, software, startup, consulting, saas",
            description="Boutique software consultancy helping small businesses "
                        "automate workflows and build MVPs fast.",
            state="Texas", city="Austin",
            email="hello@byteforward.example.com", phone="512-555-0505",
            website_url="https://byteforward.example.com",
            image_url_1=PLACEHOLDER_TECH,
        ),
        dict(
            owner_user_id=adv1_id, listing_type="social",
            title="High Altitude Sports 🏔️", category="Sports",
            tags="sports, skiing, climbing, colorado, outdoors",
            description="Adventure sports content from Colorado's front range. "
                        "Skiing, rock climbing, and trail running.",
            state="Colorado", city="Boulder",
            instagram_url="https://instagram.com/highaltitudesports",
            image_url_1=PLACEHOLDER_SPORT,
        ),
        dict(
            owner_user_id=adv2_id, listing_type="business",
            title="Lux Real Estate Group 🏠", category="Real Estate",
            tags="real estate, homes, investment, texas, property",
            description="Top-rated real estate brokerage in Texas. Residential, "
                        "commercial, and investment properties.",
            state="Texas", city="Dallas",
            email="listings@luxre.example.com", phone="214-555-0606",
            website_url="https://luxre.example.com",
            facebook_url="https://facebook.com/luxrealestate",
        ),
    ]

    for data in listings_seed:
        listing_id = create_listing(**data)
        # Auto-approve all seed listings
        update_listing(listing_id, is_approved=1, is_active=1)

    print("✅ Seed data loaded successfully.")
