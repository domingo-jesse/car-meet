from datetime import date
import streamlit as st

from services import exchange_card, get_all_users, get_matches, swipe_user
from utils.constants import STYLE_TAGS
from utils.ui import render_tags


def user_pool(current_user, filters):
    users = get_all_users(exclude_user_id=current_user["id"])
    pool = []
    for u in users:
        if filters["vehicle_type"] != "Any" and u["vehicle_type"] != filters["vehicle_type"]:
            continue
        if filters["city"] and filters["city"].lower() not in (u["city"] or "").lower():
            continue
        if filters["make_model"] and filters["make_model"].lower() not in f"{u['make']} {u['model']}".lower():
            continue
        if filters["style"] != "Any" and filters["style"] not in (u["tags"] or ""):
            continue
        pool.append(u)
    return pool


def render_discovery(user):
    st.subheader("💘 Discover People")
    fc1, fc2, fc3, fc4 = st.columns(4)
    filters = {
        "vehicle_type": fc1.selectbox("Type", ["Any", "Car", "Motorcycle"]),
        "city": fc2.text_input("City contains"),
        "style": fc3.selectbox("Style Tag", ["Any"] + STYLE_TAGS),
        "make_model": fc4.text_input("Make / Model"),
    }
    pool = user_pool(user, filters)
    if "discovery_idx" not in st.session_state:
        st.session_state.discovery_idx = 0

    if not pool:
        st.info("No profiles match your filters.")
        return

    idx = st.session_state.discovery_idx % len(pool)
    candidate = pool[idx]
    with st.container(border=True):
        st.image(candidate["vehicle_photo"], use_container_width=True)
        st.markdown(f"### {candidate['display_name']} · {candidate['age_range'] or 'N/A'}")
        st.markdown(f"**{candidate['year']} {candidate['make']} {candidate['model']}** • {candidate['color']}")
        st.caption(f"📍 {candidate['city']} | Meet Style: {candidate['meet_style']}")
        st.write(candidate["bio"])
        render_tags(candidate["tags"])

    b1, b2, b3 = st.columns([1, 1, 1])
    if b1.button("⬅️ Pass", use_container_width=True):
        swipe_user(user["id"], candidate["id"], "pass")
        st.session_state.discovery_idx += 1
        st.rerun()
    if b3.button("➡️ Like", use_container_width=True):
        swipe_user(user["id"], candidate["id"], "like")
        st.success("Liked! If they like you back, it's a match.")
        st.session_state.discovery_idx += 1
        st.rerun()
    b2.button("🎮 Next", use_container_width=True, on_click=lambda: st.session_state.update(discovery_idx=st.session_state.discovery_idx + 1))


def render_matches(user):
    st.subheader("🤝 Matches")
    matches = get_matches(user["id"])
    if not matches:
        st.info("No matches yet. Keep swiping!")
        return

    for m in matches:
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            c1.image(m["vehicle_photo"], use_container_width=True)
            with c2:
                st.markdown(f"### {m['display_name']}")
                st.write(f"{m['year']} {m['make']} {m['model']} · {m['city']}")
                render_tags(m["tags"])
                with st.expander("Exchange collector card / mark met"):
                    loc = st.text_input("Where did you meet?", key=f"loc_{m['id']}")
                    met_date = st.date_input("Date met", value=date.today(), key=f"date_{m['id']}")
                    notes = st.text_area("Notes", key=f"notes_{m['id']}")
                    if st.button("💳 Save to My Collection", key=f"save_{m['id']}"):
                        exchange_card(user["id"], m["id"], loc, met_date.isoformat(), None, notes)
                        st.success("Card exchanged and saved!")
