# Simple Search 🔍

A production-ready MVP discovery and lightweight advertising platform built with **Streamlit** and **SQLite**.

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/simple-search.git
cd simple-search
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env if needed (defaults work for local dev)
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**. The database and seed data are created automatically on first launch.

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@simplesearch.com` | `admin123` |
| Advertiser 1 | `maya@fitlife.com` | `password123` |
| Advertiser 2 | `carlos@autoworks.com` | `password123` |
| User | `jordan@example.com` | `password123` |
| User | `priya@example.com` | `password123` |

---

## 📁 Project Structure

```
simple_search/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
│
├── database/
│   ├── db.py                       # SQLite schema + CRUD helpers
│   └── seed_data.py                # Demo data loader (runs on first launch)
│
├── auth/
│   └── auth.py                     # Password hashing, login, signup, session
│
├── utils/
│   └── recommendations.py          # Personalised listing scoring engine
│
└── pages/
    ├── landing.py                  # Public landing page
    ├── browse.py                   # Searchable/filterable listing grid
    ├── pricing.py                  # Plan comparison page
    ├── auth_page.py                # Login + Sign-up tabs
    ├── onboarding.py               # User profile completion form
    ├── feed.py                     # Personalised recommendation feed
    ├── advertiser_dashboard.py     # Advertiser CRUD dashboard
    └── admin_dashboard.py          # Admin controls + metrics
```

---

## 🌐 Deploy to Streamlit Community Cloud

1. Push your project to GitHub (make sure `simple_search.db` is in `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **Deploy an app**.
3. Select your repository, set **Main file path** to `app.py`.
4. Add Secrets (equivalent to `.env`) in the Streamlit Secrets section:
   ```toml
   DATABASE_PATH = "simple_search.db"
   ```
5. Click **Deploy**.

> **Note:** For production, replace SQLite with a hosted database (PostgreSQL via Supabase) and Stripe for real payments.

---

## 💡 Roles & Permissions

| Role | Browse | My Feed | Create Listings | Admin Panel |
|------|--------|---------|-----------------|-------------|
| Guest | ✅ | ❌ | ❌ | ❌ |
| User | ✅ | ✅ | ❌ | ❌ |
| Advertiser | ✅ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ |

---

## 📊 Recommendation Engine

Listings are scored for each user using:

| Signal | Points |
|--------|--------|
| Category matches a user interest | +3 |
| Listing state matches user state | +2 |
| Tag matches a user "like" keyword | +1 |
| Tag matches a user "dislike" keyword | -1 |

Listings are sorted by score (highest first) in the **My Feed** page.

---

## 💳 Pricing (MVP – Mocked Billing)

| Plan | Price | Billed |
|------|-------|--------|
| Member | $52 | Yearly |
| Advertiser | $10 per listing | Monthly |

Payments are mocked for MVP. Integrate **Stripe** for production billing.

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python 3.11+
- **Database**: SQLite (via `database/db.py`)
- **Auth**: bcrypt password hashing + Streamlit session state
- **Images**: Unsplash URLs for demo data
- **Payments**: Mocked (Stripe-ready structure)
