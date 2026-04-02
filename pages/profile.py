from datetime import date
from uuid import uuid4

import streamlit as st

from db import get_conn
from services import get_collection
from utils.constants import MEET_STYLES, STYLE_TAGS, VEHICLE_TYPES
from utils.storage import save_uploaded_file
from utils.ui import render_tags


def render_profile(user):
    st.subheader("🪪 My Collector Card")
    left, right = st.columns([1, 1])
    with left:
        st.image(user["vehicle_photo"], use_container_width=True)
    with right:
        st.markdown(f"### {user['display_name']}  ")
        st.markdown(f"**{user['year']} {user['make']} {user['model']}** • {user['color']}")
        st.write(user["bio"])
        st.caption(f"📍 {user['city']} · Meet style: {user['meet_style']}")
        render_tags(user["tags"])
        st.code(f"Collector Card ID: {user['card_id']}")
        st.button("🔗 Share Card")
        st.caption("QR-style share placeholder for future release.")


def render_edit_profile(user):
    st.subheader("✍️ Edit Profile")
    with st.form("edit_profile"):
        display_name = st.text_input("Display name", value=user["display_name"])
        age = st.text_input("Age range", value=user["age_range"] or "")
        city = st.text_input("City", value=user["city"] or "")
        bio = st.text_area("Short bio", value=user["bio"] or "")
        interests = st.text_input("Interests", value=user["interests"] or "")

        vehicle_type = st.selectbox("Vehicle type", VEHICLE_TYPES, index=VEHICLE_TYPES.index(user["vehicle_type"]) if user["vehicle_type"] in VEHICLE_TYPES else 0)
        make = st.text_input("Make", value=user["make"] or "")
        model = st.text_input("Model", value=user["model"] or "")
        year = st.text_input("Year", value=user["year"] or "")
        color = st.text_input("Vehicle color", value=user["color"] or "")
        mods = st.text_area("Mods/customizations", value=user["mods"] or "")
        meet_style = st.selectbox("Favorite meet style", MEET_STYLES, index=MEET_STYLES.index(user["meet_style"]) if user["meet_style"] in MEET_STYLES else 0)
        tags = st.multiselect("Badges/tags", STYLE_TAGS, default=[t.strip() for t in (user["tags"] or "").split(",") if t.strip()])
        v_img = st.file_uploader("Vehicle photo", type=["png", "jpg", "jpeg"])
        p_img = st.file_uploader("Personal photo (optional)", type=["png", "jpg", "jpeg"])
        submit = st.form_submit_button("Save Changes")

    if submit:
        v_path = save_uploaded_file(v_img, "vehicle") or user["vehicle_photo"]
        p_path = save_uploaded_file(p_img, "person") or user["personal_photo"]
        conn = get_conn()
        conn.execute(
            """
            UPDATE users
            SET display_name=?, age_range=?, city=?, bio=?, interests=?, vehicle_type=?, make=?, model=?,
                year=?, color=?, mods=?, meet_style=?, tags=?, vehicle_photo=?, personal_photo=?
            WHERE id=?
            """,
            (display_name, age, city, bio, interests, vehicle_type, make, model, year, color, mods, meet_style, ",".join(tags), v_path, p_path, user["id"]),
        )
        conn.commit()
        conn.close()
        st.success("Profile updated. Refresh to see latest card.")


def render_collection(user):
    st.subheader("📚 My Collection")
    cards = get_collection(user["id"])
    q = st.text_input("Search by name, make/model, event, location")
    if q:
        ql = q.lower()
        cards = [
            c for c in cards
            if ql in (c["display_name"] or "").lower()
            or ql in f"{c['make']} {c['model']}".lower()
            or ql in (c["event_name"] or "").lower()
            or ql in (c["met_location"] or "").lower()
        ]

    if not cards:
        st.info("No cards saved yet.")
        return

    for c in cards:
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            c1.image(c["vehicle_photo"], use_container_width=True)
            with c2:
                st.markdown(f"### {c['display_name']} · {c['card_id']}")
                st.write(f"{c['year']} {c['make']} {c['model']} ({c['color']})")
                st.caption(f"Met: {c['met_date'] or date.today().isoformat()} @ {c['met_location'] or 'Unknown'}")
                if c["event_name"]:
                    st.write(f"Event: {c['event_name']}")
                st.write(f"Notes: {c['notes'] or 'No notes'}")


def signup_form():
    st.subheader("Create your MotorMatch account")
    with st.form("signup"):
        display_name = st.text_input("Display name *")
        username = st.text_input("Username *")
        password = st.text_input("Password *", type="password")
        age = st.text_input("Age range")
        city = st.text_input("City/region")
        bio = st.text_area("Short bio")
        interests = st.text_input("Driving/riding interests")
        vehicle_type = st.selectbox("Vehicle type *", VEHICLE_TYPES)
        make = st.text_input("Make *")
        model = st.text_input("Model *")
        year = st.text_input("Year")
        color = st.text_input("Vehicle color")
        mods = st.text_area("Mods/customizations")
        meet_style = st.selectbox("Favorite meet style", MEET_STYLES)
        tags = st.multiselect("Badges/tags", STYLE_TAGS)
        vehicle_photo = st.file_uploader("Vehicle photo *", type=["png", "jpg", "jpeg"], key="signup_vehicle")
        personal_photo = st.file_uploader("Personal photo (optional)", type=["png", "jpg", "jpeg"], key="signup_person")
        submit = st.form_submit_button("Sign up")

    if not submit:
        return None

    return {
        "display_name": display_name,
        "username": username,
        "password": password,
        "age_range": age,
        "city": city,
        "bio": bio,
        "interests": interests,
        "vehicle_type": vehicle_type,
        "make": make,
        "model": model,
        "year": year,
        "color": color,
        "mods": mods,
        "meet_style": meet_style,
        "tags": ",".join(tags),
        "vehicle_photo": save_uploaded_file(vehicle_photo, "vehicle") if vehicle_photo else "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=1400&auto=format&fit=crop",
        "personal_photo": save_uploaded_file(personal_photo, "person") if personal_photo else None,
        "card_id": f"MM-{uuid4().hex[:8].upper()}",
    }
