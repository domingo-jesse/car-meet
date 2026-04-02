import random
import streamlit as st

from services import dashboard_stats, get_all_users, get_collection, get_events
from utils.ui import render_tags


def render_home(user):
    st.subheader("🔥 Community Feed")
    stats = dashboard_stats(user["id"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Cards Collected", stats["cards"])
    c2.metric("Events Attending", stats["events"])
    c3.metric("Matches", stats["matches"])

    users = get_all_users(exclude_user_id=user["id"])
    events = get_events()
    collection = get_collection(user["id"])

    left, right = st.columns([2, 1])
    with left:
        st.markdown("### Featured Builds")
        for u in random.sample(users, k=min(3, len(users))):
            with st.container(border=True):
                st.image(u["vehicle_photo"], use_container_width=True)
                st.markdown(f"**{u['display_name']}** · {u['year']} {u['make']} {u['model']} · {u['city']}")
                st.caption(u["bio"])
                render_tags(u["tags"])

        st.markdown("### Upcoming Events")
        for e in events[:4]:
            with st.container(border=True):
                st.image(e["featured_image"], use_container_width=True)
                st.markdown(f"**{e['name']}** · {e['date']} {e['time']}")
                st.caption(f"{e['city']} • {e['category']} • {e['vibe']}")

    with right:
        st.markdown("### Trending Tags")
        for t in ["#JDM", "#Track", "#Sportbike", "#Stance", "#Classics", "#NightCruise"]:
            st.markdown(f"- {t}")

        st.markdown("### Recent Card Exchanges")
        for card in collection[:5]:
            st.markdown(f"- {card['display_name']} at {card['met_location'] or 'Local meet'}")
