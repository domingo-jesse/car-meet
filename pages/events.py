from datetime import date
import streamlit as st

from services import create_event, get_events, get_user_events, swipe_event
from utils.constants import MEET_STYLES


def filter_events(events, filters):
    out = []
    for e in events:
        if filters["city"] and filters["city"].lower() not in (e["city"] or "").lower():
            continue
        if filters["focus"] != "Any" and e["focus_type"] != filters["focus"]:
            continue
        if filters["price"] != "Any" and e["price_type"] != filters["price"]:
            continue
        if filters["vibe"] != "Any" and filters["vibe"] not in (e["category"] or ""):
            continue
        if filters["date"] and e["date"] < filters["date"].isoformat():
            continue
        out.append(e)
    return out


def render_event_discovery(user):
    st.subheader("🗓️ Swipe Events")
    all_events = get_events()
    f1, f2, f3, f4, f5 = st.columns(5)
    filters = {
        "date": f1.date_input("From date", value=date.today()),
        "city": f2.text_input("City"),
        "focus": f3.selectbox("Focus", ["Any", "Car", "Motorcycle", "Mixed"]),
        "vibe": f4.selectbox("Style/Vibe", ["Any"] + MEET_STYLES),
        "price": f5.selectbox("Price", ["Any", "Free", "Paid"]),
    }
    events = filter_events(all_events, filters)
    if "event_idx" not in st.session_state:
        st.session_state.event_idx = 0

    if not events:
        st.info("No events found with current filters.")
        return

    e = events[st.session_state.event_idx % len(events)]
    with st.container(border=True):
        st.image(e["featured_image"], use_container_width=True)
        st.markdown(f"### {e['name']}")
        st.write(f"📍 {e['city']} • {e['address']}")
        st.caption(f"{e['date']} {e['time']} · {e['category']} · {e['vibe']} · {e['price_type']}")
        st.write(e["description"])

    b1, b2 = st.columns(2)
    if b1.button("⬅️ Not Interested", use_container_width=True):
        swipe_event(user["id"], e["id"], "pass")
        st.session_state.event_idx += 1
        st.rerun()
    if b2.button("➡️ RSVP", use_container_width=True):
        swipe_event(user["id"], e["id"], "like")
        st.success("You're attending! Directions placeholder added.")
        st.info(f"Route Link: {e['route_link']}")
        st.session_state.event_idx += 1
        st.rerun()


def render_create_event(user):
    st.subheader("➕ Create Event")
    with st.form("create_event"):
        name = st.text_input("Event Name *")
        description = st.text_area("Description")
        dcol1, dcol2 = st.columns(2)
        dt = dcol1.date_input("Date", value=date.today())
        tm = dcol2.text_input("Time", value="19:00")
        city = st.text_input("City")
        address = st.text_input("Address")
        category = st.selectbox("Meet Category", MEET_STYLES)
        vibe = st.text_input("Expected vibe")
        route_link = st.text_input("Route/Map link placeholder", value="https://maps.example.com")
        notes = st.text_area("Event notes / rules")
        focus = st.selectbox("Car vs bike focus", ["Car", "Motorcycle", "Mixed"])
        price = st.selectbox("Free/Paid", ["Free", "Paid"])
        capacity = st.number_input("Capacity (optional)", min_value=0, value=0)
        image = st.text_input("Featured image URL", value="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?q=80&w=1400&auto=format&fit=crop")
        submitted = st.form_submit_button("Create Event")

    if submitted:
        if not name:
            st.error("Event name is required.")
            return
        create_event(
            {
                "name": name,
                "host_user_id": user["id"],
                "description": description,
                "date": dt.isoformat(),
                "time": tm,
                "city": city,
                "address": address,
                "category": category,
                "vibe": vibe,
                "route_link": route_link,
                "notes_rules": notes,
                "capacity": capacity if capacity > 0 else None,
                "featured_image": image,
                "focus_type": focus,
                "price_type": price,
            }
        )
        st.success("Event created!")


def render_my_events(user):
    st.subheader("🎟️ My Events")
    attending, hosted = get_user_events(user["id"])
    t1, t2, t3 = st.tabs(["Attending", "Hosted", "Past"])
    with t1:
        for e in attending:
            st.markdown(f"- **{e['name']}** · {e['date']} · {e['city']}")
    with t2:
        for e in hosted:
            st.markdown(f"- **{e['name']}** · {e['date']} · {e['city']}")
    with t3:
        today = date.today().isoformat()
        for e in attending:
            if e["date"] < today:
                st.markdown(f"- **{e['name']}** · attended on {e['date']}")
