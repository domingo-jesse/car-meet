import streamlit as st

from auth import create_user, login_user
from db import init_db
from pages.discovery import render_discovery, render_matches
from pages.events import render_create_event, render_event_discovery, render_my_events
from pages.home import render_home
from pages.profile import render_collection, render_edit_profile, render_profile, signup_form
from seed_data import seed_if_empty
from services import get_user
from utils.ui import header_bar, inject_theme

st.set_page_config(page_title="MotorMatch", page_icon="🏁", layout="wide")
inject_theme()
init_db()
seed_if_empty()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_id:
    header_bar()
    tab1, tab2 = st.tabs(["🔐 Log in", "✨ Sign up"])
    with tab1:
        st.markdown("### Welcome back")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log in"):
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user["id"]
                st.success("Logged in.")
                st.rerun()
            else:
                st.error("Invalid credentials. Demo users use password: demo123")
    with tab2:
        payload = signup_form()
        if payload:
            ok, msg = create_user(payload)
            (st.success if ok else st.error)(msg)

    st.info("Try demo account usernames from seed data (e.g., `kaiboost`, password `demo123`).")
    st.stop()

user = get_user(st.session_state.user_id)
with st.sidebar:
    st.image(user["vehicle_photo"], use_container_width=True)
    st.markdown(f"### {user['display_name']}")
    st.caption(f"@{user['username']} · {user['city']}")
    if st.button("🚪 Log out"):
        st.session_state.user_id = None
        st.rerun()
    page = st.radio(
        "Navigate",
        [
            "Home Feed",
            "Discover People",
            "Matches",
            "Event Discovery",
            "Create Event",
            "My Events",
            "My Collector Card",
            "Edit Profile",
            "My Collection",
        ],
    )

header_bar(user)
if page == "Home Feed":
    render_home(user)
elif page == "Discover People":
    render_discovery(user)
elif page == "Matches":
    render_matches(user)
elif page == "Event Discovery":
    render_event_discovery(user)
elif page == "Create Event":
    render_create_event(user)
elif page == "My Events":
    render_my_events(user)
elif page == "My Collector Card":
    render_profile(user)
elif page == "Edit Profile":
    render_edit_profile(user)
elif page == "My Collection":
    render_collection(user)
