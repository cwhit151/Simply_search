"""
utils/recommendations.py
Scoring engine for personalised listing suggestions.

Scoring rules:
  +3  category matches any user interest
  +2  state matches user state
  +1  any listing tag appears in user likes
  -1  any listing tag appears in user dislikes
"""

import json
from database.db import get_listings


def _parse_list(raw: str, delimiter: str = ",") -> list[str]:
    """Split and strip a delimited string into a lowercased list."""
    if not raw:
        return []
    return [item.strip().lower() for item in raw.split(delimiter) if item.strip()]


def _parse_interests(raw: str) -> list[str]:
    """Interests are stored as a JSON array string."""
    if not raw:
        return []
    try:
        return [i.lower() for i in json.loads(raw)]
    except (json.JSONDecodeError, TypeError):
        # Fallback: try comma split
        return _parse_list(raw)


def score_listing(listing: dict, user: dict) -> int:
    """Compute a recommendation score for one listing given one user profile."""
    score = 0
    interests = _parse_interests(user.get("interests", "[]"))
    likes = _parse_list(user.get("likes", ""))
    dislikes = _parse_list(user.get("dislikes", ""))
    tags = _parse_list(listing.get("tags", ""))
    category = (listing.get("category") or "").lower()
    listing_state = (listing.get("state") or "").lower()
    user_state = (user.get("state") or "").lower()

    # +3 for category match
    if category and category in interests:
        score += 3

    # +2 for state match
    if listing_state and user_state and listing_state == user_state:
        score += 2

    # +1 per tag that matches a like
    for tag in tags:
        if tag in likes:
            score += 1

    # -1 per tag that matches a dislike
    for tag in tags:
        if tag in dislikes:
            score -= 1

    return score


def get_recommended_listings(user: dict, limit: int = 20) -> list[dict]:
    """
    Return up to `limit` active/approved listings ranked by score (desc).
    Listings with score <= 0 are still included but sorted last.
    """
    all_listings = get_listings()
    scored = [(listing, score_listing(listing, user)) for listing in all_listings]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [listing for listing, _ in scored[:limit]]
