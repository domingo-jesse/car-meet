import sqlite3
from pathlib import Path

DB_PATH = Path("data/motormatch.db")


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age_range TEXT,
            city TEXT,
            bio TEXT,
            interests TEXT,
            vehicle_type TEXT,
            make TEXT,
            model TEXT,
            year TEXT,
            color TEXT,
            mods TEXT,
            meet_style TEXT,
            tags TEXT,
            vehicle_photo TEXT,
            personal_photo TEXT,
            card_id TEXT UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            liker_id INTEGER NOT NULL,
            liked_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(liker_id, liked_id)
        );

        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_a INTEGER NOT NULL,
            user_b INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_a, user_b)
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host_user_id INTEGER NOT NULL,
            description TEXT,
            date TEXT,
            time TEXT,
            city TEXT,
            address TEXT,
            category TEXT,
            vibe TEXT,
            featured_image TEXT,
            route_link TEXT,
            notes_rules TEXT,
            capacity INTEGER,
            focus_type TEXT,
            price_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS event_swipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, event_id)
        );

        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            status TEXT DEFAULT 'attending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, event_id)
        );

        CREATE TABLE IF NOT EXISTS card_exchanges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_user_id INTEGER NOT NULL,
            collected_user_id INTEGER NOT NULL,
            met_location TEXT,
            met_date TEXT,
            event_id INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()
