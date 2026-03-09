"""
database/db.py
SQLite database setup, schema creation, and helper query functions.
Handles all direct DB interactions for Simple Search.
"""

import sqlite3
import os
from datetime import datetime

# ── Database path (override via env var) ──────────────────────────────────────
DB_PATH = os.getenv("DATABASE_PATH", "simple_search.db")


def get_connection():
    """Return a SQLite connection with row_factory for dict-like rows."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create all tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── Users ─────────────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            role            TEXT    NOT NULL DEFAULT 'user',   -- user | advertiser | admin
            full_name       TEXT    NOT NULL,
            email           TEXT    NOT NULL UNIQUE,
            password_hash   TEXT    NOT NULL,
            phone           TEXT,
            state           TEXT,
            city            TEXT,
            interests       TEXT,   -- JSON array stored as string
            likes           TEXT,   -- comma-separated keywords
            dislikes        TEXT,   -- comma-separated keywords
            instagram_handle TEXT,
            facebook_handle  TEXT,
            created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # ── Listings ──────────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_user_id   INTEGER NOT NULL REFERENCES users(id),
            listing_type    TEXT    NOT NULL,  -- 'social' | 'business'
            title           TEXT    NOT NULL,
            category        TEXT    NOT NULL,
            tags            TEXT,              -- comma-separated
            description     TEXT,
            state           TEXT,
            city            TEXT,
            email           TEXT,
            phone           TEXT,
            website_url     TEXT,
            instagram_url   TEXT,
            facebook_url    TEXT,
            image_url_1     TEXT,
            image_url_2     TEXT,
            is_active       INTEGER NOT NULL DEFAULT 1,   -- 0 | 1
            is_approved     INTEGER NOT NULL DEFAULT 0,   -- 0 | 1
            created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # ── Subscriptions ─────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id             INTEGER NOT NULL REFERENCES users(id),
            subscription_type   TEXT    NOT NULL,  -- 'user' | 'advertiser'
            status              TEXT    NOT NULL DEFAULT 'active',  -- active | cancelled | pending
            billing_cycle       TEXT    NOT NULL,  -- 'monthly' | 'yearly'
            amount              REAL    NOT NULL,
            created_at          TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


# ── User helpers ───────────────────────────────────────────────────────────────

def create_user(full_name, email, password_hash, role="user", phone="",
                state="", city="", interests="[]", likes="", dislikes="",
                instagram_handle="", facebook_handle=""):
    """Insert a new user and return their id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (role, full_name, email, password_hash, phone,
                           state, city, interests, likes, dislikes,
                           instagram_handle, facebook_handle)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (role, full_name, email, password_hash, phone, state, city,
          interests, likes, dislikes, instagram_handle, facebook_handle))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_user_by_email(email):
    """Return a user row dict or None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Return a user row dict or None."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_user(user_id, **kwargs):
    """Update arbitrary user fields."""
    if not kwargs:
        return
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    conn = get_connection()
    conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?",
                 (*kwargs.values(), user_id))
    conn.commit()
    conn.close()


def get_all_users():
    """Admin: return all users."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Listing helpers ────────────────────────────────────────────────────────────

def create_listing(owner_user_id, listing_type, title, category, tags="",
                   description="", state="", city="", email="", phone="",
                   website_url="", instagram_url="", facebook_url="",
                   image_url_1="", image_url_2=""):
    """Insert a new listing and return its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO listings (owner_user_id, listing_type, title, category,
                              tags, description, state, city, email, phone,
                              website_url, instagram_url, facebook_url,
                              image_url_1, image_url_2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (owner_user_id, listing_type, title, category, tags, description,
          state, city, email, phone, website_url, instagram_url, facebook_url,
          image_url_1, image_url_2))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_listing_by_id(listing_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM listings WHERE id = ?", (listing_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_listings(filters=None):
    """
    Return approved + active listings, with optional filters dict:
        listing_type, category, state, search (keyword in title/tags/description)
    """
    query = "SELECT * FROM listings WHERE is_approved = 1 AND is_active = 1"
    params = []

    if filters:
        if filters.get("listing_type"):
            query += " AND listing_type = ?"
            params.append(filters["listing_type"])
        if filters.get("category"):
            query += " AND category = ?"
            params.append(filters["category"])
        if filters.get("state"):
            query += " AND state = ?"
            params.append(filters["state"])
        if filters.get("search"):
            kw = f"%{filters['search']}%"
            query += " AND (title LIKE ? OR tags LIKE ? OR description LIKE ?)"
            params.extend([kw, kw, kw])

    query += " ORDER BY created_at DESC"
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_listings_by_owner(owner_user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM listings WHERE owner_user_id = ? ORDER BY created_at DESC",
        (owner_user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_listing(listing_id, **kwargs):
    if not kwargs:
        return
    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    conn = get_connection()
    conn.execute(f"UPDATE listings SET {set_clause} WHERE id = ?",
                 (*kwargs.values(), listing_id))
    conn.commit()
    conn.close()


def delete_listing(listing_id):
    conn = get_connection()
    conn.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
    conn.commit()
    conn.close()


def get_all_listings_admin():
    """Admin: return ALL listings regardless of status."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM listings ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Subscription helpers ───────────────────────────────────────────────────────

def create_subscription(user_id, subscription_type, billing_cycle, amount):
    conn = get_connection()
    conn.execute("""
        INSERT INTO subscriptions (user_id, subscription_type, status,
                                   billing_cycle, amount)
        VALUES (?, ?, 'active', ?, ?)
    """, (user_id, subscription_type, billing_cycle, amount))
    conn.commit()
    conn.close()


def get_subscription(user_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_subscription_status(sub_id, status):
    conn = get_connection()
    conn.execute("UPDATE subscriptions SET status = ? WHERE id = ?", (status, sub_id))
    conn.commit()
    conn.close()


def get_all_subscriptions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM subscriptions ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Metrics ───────────────────────────────────────────────────────────────────

def get_metrics():
    """Return simple platform metrics dict."""
    conn = get_connection()
    total_users = conn.execute(
        "SELECT COUNT(*) FROM users WHERE role != 'admin'"
    ).fetchone()[0]
    total_advertisers = conn.execute(
        "SELECT COUNT(*) FROM users WHERE role = 'advertiser'"
    ).fetchone()[0]
    total_listings = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    active_listings = conn.execute(
        "SELECT COUNT(*) FROM listings WHERE is_active = 1 AND is_approved = 1"
    ).fetchone()[0]
    pending_listings = conn.execute(
        "SELECT COUNT(*) FROM listings WHERE is_approved = 0"
    ).fetchone()[0]
    conn.close()
    return {
        "total_users": total_users,
        "total_advertisers": total_advertisers,
        "total_listings": total_listings,
        "active_listings": active_listings,
        "pending_listings": pending_listings,
    }
