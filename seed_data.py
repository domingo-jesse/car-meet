from __future__ import annotations

import random
from datetime import date, timedelta
from uuid import uuid4

from auth import hash_password
from db import get_conn
from utils.constants import CITIES, MEET_STYLES

USERS = [
    ("Kai", "kaiboost", "Car", "Nissan", "370Z", "2016", "Blue", "Coilovers, Tomei exhaust", "JDM,Drift,Track"),
    ("Mina", "minarides", "Motorcycle", "Yamaha", "MT-07", "2022", "Matte Black", "Frame sliders, clip-ons", "Motorcycle,Sportbike,Cruiser"),
    ("Rico", "ricoturbo", "Car", "Subaru", "WRX STI", "2019", "White", "Big turbo, tune", "JDM,Track,Tuner"),
    ("Lex", "lexstance", "Car", "Lexus", "IS300", "2004", "Silver", "Air suspension, wheels", "Stance,JDM,Classic"),
    ("Noah", "musclenoh", "Car", "Ford", "Mustang GT", "2018", "Red", "Cat-back, intake", "Muscle,Cruise"),
    ("Ari", "aricafe", "Motorcycle", "Honda", "CB650R", "2021", "Gray", "Bar-end mirrors", "Cafe Racer,Motorcycle"),
    ("Ivy", "ivyeuro", "Car", "BMW", "M3", "2017", "Black", "Carbon lip, tune", "Euro,Track"),
    ("Troy", "troydrift", "Car", "Mazda", "MX-5", "2015", "Orange", "Angle kit, bucket seats", "Drift,JDM"),
    ("June", "junebike", "Motorcycle", "Kawasaki", "Ninja 650", "2020", "Green", "Slip-on, tail tidy", "Sportbike,Motorcycle"),
    ("Dani", "daniclassic", "Car", "Chevrolet", "Camaro", "1969", "Yellow", "Restomod V8", "Classic,Muscle"),
    ("Omar", "omarrally", "Car", "Toyota", "GR Corolla", "2024", "White", "Rally wheels", "JDM,Off-road,Track"),
    ("Rae", "raecruise", "Motorcycle", "Harley", "Iron 883", "2019", "Burgundy", "Mini apes, custom seat", "Cruiser,Motorcycle"),
    ("Ben", "benturbo", "Car", "Audi", "S4", "2018", "Gray", "Stage 2 tune", "Euro,Tuner"),
    ("Sia", "siatrack", "Car", "Porsche", "Cayman", "2016", "Blue", "Track pads, harness", "Track,Euro"),
    ("Moe", "moeoffroad", "Car", "Jeep", "Wrangler", "2020", "Tan", "Lift kit, 35s", "Off-road,Cruise"),
    ("Tess", "tessjdm", "Car", "Honda", "Civic Type R", "2021", "Championship White", "Exhaust, splitter", "JDM,Track"),
    ("Gio", "giobikes", "Motorcycle", "Ducati", "Monster", "2023", "Red", "SC Project exhaust", "Sportbike,Motorcycle"),
    ("Paz", "pazstance", "Car", "Volkswagen", "GTI", "2017", "White", "Air ride, wheels", "Stance,Euro"),
    ("Elle", "elleclassic", "Car", "Datsun", "240Z", "1973", "Orange", "L28 swap", "Classic,JDM"),
    ("Vic", "vicnight", "Motorcycle", "Suzuki", "GSX-R750", "2019", "Blue", "Quickshifter", "Sportbike,Track,Motorcycle"),
]

EVENTS = [
    "Friday Night Cruise", "Eastside Bikes & Coffee", "JDM Sunset Meet", "Canyon Ride Meetup",
    "Classics on Main", "Turbo Night", "Stance & Shine", "Track Prep Social", "Off-road Dawn Run", "Euro Night Meetup",
]


def seed_if_empty():
    conn = get_conn()
    user_count = conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
    if user_count == 0:
        for idx, row in enumerate(USERS, start=1):
            display_name, username, vehicle_type, make, model, year, color, mods, tags = row
            conn.execute(
                """
                INSERT INTO users(display_name, username, password, age_range, city, bio, interests,
                                  vehicle_type, make, model, year, color, mods, meet_style, tags,
                                  vehicle_photo, personal_photo, card_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    display_name,
                    username,
                    hash_password("demo123"),
                    random.choice(["18-24", "25-34", "35-44"]),
                    random.choice(CITIES),
                    f"{display_name} lives for clean builds, chill meets, and weekend runs.",
                    "Night drives, detailing, photo shoots",
                    vehicle_type,
                    make,
                    model,
                    year,
                    color,
                    mods,
                    random.choice(MEET_STYLES),
                    tags,
                    "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=1400&auto=format&fit=crop",
                    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=800&auto=format&fit=crop",
                    f"MM-{uuid4().hex[:8].upper()}",
                ),
            )

    event_count = conn.execute("SELECT COUNT(*) c FROM events").fetchone()["c"]
    if event_count == 0:
        users = [r[0] for r in conn.execute("SELECT id FROM users LIMIT 8").fetchall()]
        for i, name in enumerate(EVENTS):
            dt = date.today() + timedelta(days=i + 1)
            conn.execute(
                """
                INSERT INTO events(name, host_user_id, description, date, time, city, address, category, vibe,
                                   featured_image, route_link, notes_rules, capacity, focus_type, price_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    random.choice(users),
                    f"{name} brings out passionate riders and drivers for a social, photogenic community night.",
                    dt.isoformat(),
                    random.choice(["18:00", "19:00", "20:00", "08:00"]),
                    random.choice(CITIES),
                    f"{100+i} Main St",
                    random.choice(MEET_STYLES),
                    random.choice(["Chill", "High Energy", "Family-friendly", "Photo-heavy"]),
                    "https://images.unsplash.com/photo-1469285994282-454ceb49e63f?q=80&w=1400&auto=format&fit=crop",
                    "https://maps.example.com/route-placeholder",
                    "Respect locals. No burnouts in lot. Keep it safe.",
                    random.choice([None, 50, 80, 120]),
                    random.choice(["Car", "Motorcycle", "Mixed"]),
                    random.choice(["Free", "Paid"]),
                ),
            )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_if_empty()
