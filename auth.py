import hashlib
from typing import Optional

from db import get_conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(payload: dict) -> tuple[bool, str]:
    required = ["display_name", "username", "password", "vehicle_type", "make", "model"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (
                display_name, username, password, age_range, city, bio, interests,
                vehicle_type, make, model, year, color, mods, meet_style, tags,
                vehicle_photo, personal_photo, card_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("display_name"),
                payload.get("username"),
                hash_password(payload.get("password")),
                payload.get("age_range"),
                payload.get("city"),
                payload.get("bio"),
                payload.get("interests"),
                payload.get("vehicle_type"),
                payload.get("make"),
                payload.get("model"),
                payload.get("year"),
                payload.get("color"),
                payload.get("mods"),
                payload.get("meet_style"),
                payload.get("tags"),
                payload.get("vehicle_photo"),
                payload.get("personal_photo"),
                payload.get("card_id"),
            ),
        )
        conn.commit()
        return True, "Account created successfully."
    except Exception as ex:
        return False, f"Could not create user: {ex}"
    finally:
        conn.close()


def login_user(username: str, password: str) -> Optional[dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
