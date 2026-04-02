from __future__ import annotations

from datetime import datetime
from typing import Iterable

from db import get_conn


def rows_to_dicts(rows: Iterable):
    return [dict(r) for r in rows]


def get_user(user_id: int) -> dict | None:
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users(exclude_user_id: int | None = None):
    conn = get_conn()
    if exclude_user_id:
        rows = conn.execute("SELECT * FROM users WHERE id != ?", (exclude_user_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return rows_to_dicts(rows)


def swipe_user(liker_id: int, liked_id: int, decision: str):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO likes(liker_id, liked_id, decision) VALUES (?, ?, ?)",
        (liker_id, liked_id, decision),
    )
    if decision == "like":
        reverse = conn.execute(
            "SELECT 1 FROM likes WHERE liker_id = ? AND liked_id = ? AND decision='like'",
            (liked_id, liker_id),
        ).fetchone()
        if reverse:
            a, b = sorted([liker_id, liked_id])
            conn.execute("INSERT OR IGNORE INTO matches(user_a, user_b) VALUES (?, ?)", (a, b))
    conn.commit()
    conn.close()


def get_matches(user_id: int):
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT m.*, u.* FROM matches m
        JOIN users u ON u.id = CASE WHEN m.user_a = ? THEN m.user_b ELSE m.user_a END
        WHERE m.user_a = ? OR m.user_b = ?
        ORDER BY m.created_at DESC
        """,
        (user_id, user_id, user_id),
    ).fetchall()
    conn.close()
    return rows_to_dicts(rows)


def create_event(payload: dict):
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO events(name, host_user_id, description, date, time, city, address, category, vibe,
                           featured_image, route_link, notes_rules, capacity, focus_type, price_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["name"], payload["host_user_id"], payload.get("description"), payload.get("date"),
            payload.get("time"), payload.get("city"), payload.get("address"), payload.get("category"),
            payload.get("vibe"), payload.get("featured_image"), payload.get("route_link"),
            payload.get("notes_rules"), payload.get("capacity"), payload.get("focus_type"), payload.get("price_type"),
        ),
    )
    conn.commit()
    conn.close()


def get_events():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM events ORDER BY date, time").fetchall()
    conn.close()
    return rows_to_dicts(rows)


def swipe_event(user_id: int, event_id: int, decision: str):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO event_swipes(user_id, event_id, decision) VALUES (?, ?, ?)",
        (user_id, event_id, decision),
    )
    if decision == "like":
        conn.execute("INSERT OR IGNORE INTO rsvps(user_id, event_id) VALUES (?, ?)", (user_id, event_id))
    conn.commit()
    conn.close()


def get_user_events(user_id: int):
    conn = get_conn()
    attending = conn.execute(
        "SELECT e.* FROM rsvps r JOIN events e ON e.id = r.event_id WHERE r.user_id = ? ORDER BY e.date",
        (user_id,),
    ).fetchall()
    hosted = conn.execute("SELECT * FROM events WHERE host_user_id = ? ORDER BY date", (user_id,)).fetchall()
    conn.close()
    return rows_to_dicts(attending), rows_to_dicts(hosted)


def exchange_card(owner_user_id: int, collected_user_id: int, met_location: str, met_date: str, event_id=None, notes=""):
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO card_exchanges(owner_user_id, collected_user_id, met_location, met_date, event_id, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (owner_user_id, collected_user_id, met_location, met_date or datetime.utcnow().date().isoformat(), event_id, notes),
    )
    conn.commit()
    conn.close()


def get_collection(owner_user_id: int):
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT c.*, u.display_name, u.make, u.model, u.year, u.color, u.vehicle_photo, u.card_id,
               e.name as event_name
        FROM card_exchanges c
        JOIN users u ON u.id = c.collected_user_id
        LEFT JOIN events e ON e.id = c.event_id
        WHERE c.owner_user_id = ?
        ORDER BY c.created_at DESC
        """,
        (owner_user_id,),
    ).fetchall()
    conn.close()
    return rows_to_dicts(rows)


def dashboard_stats(user_id: int):
    conn = get_conn()
    cards = conn.execute("SELECT COUNT(*) c FROM card_exchanges WHERE owner_user_id=?", (user_id,)).fetchone()["c"]
    events = conn.execute("SELECT COUNT(*) c FROM rsvps WHERE user_id=?", (user_id,)).fetchone()["c"]
    matches = conn.execute("SELECT COUNT(*) c FROM matches WHERE user_a=? OR user_b=?", (user_id, user_id)).fetchone()["c"]
    conn.close()
    return {"cards": cards, "events": events, "matches": matches}
