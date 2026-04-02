import streamlit as st


def inject_theme():
    st.markdown(
        """
        <style>
        .stApp {background: linear-gradient(180deg,#0b0f16 0%, #111827 45%, #0b1220 100%); color: #e5e7eb;}
        .mm-title {font-size: 2.3rem; font-weight: 800; letter-spacing: .5px; margin-bottom: .2rem;}
        .mm-sub {color:#9ca3af; margin-bottom: 1rem;}
        .mm-card {background: rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12); padding: 1rem; border-radius: 20px;}
        .tag {display:inline-block; margin:0 6px 6px 0; padding:5px 10px; border-radius:999px; background:#1f2937; color:#93c5fd; font-size:.78rem;}
        .stat-pill {background:#111827;padding:.35rem .7rem;border-radius:999px;border:1px solid #374151;}
        .stButton>button {border-radius: 12px; font-weight: 700; width:100%;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def header_bar(user=None):
    st.markdown('<div class="mm-title">🏁 MotorMatch</div>', unsafe_allow_html=True)
    if user:
        st.markdown(f"<div class='mm-sub'>Welcome back, <b>{user['display_name']}</b> • Card ID {user['card_id']}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='mm-sub'>Swipe builds, find your tribe, collect community cards.</div>", unsafe_allow_html=True)


def render_tags(tags: str):
    if not tags:
        return
    html = "".join([f"<span class='tag'>{t.strip()}</span>" for t in tags.split(",") if t.strip()])
    st.markdown(html, unsafe_allow_html=True)
