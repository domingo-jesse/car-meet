# MotorMatch 🏁

MotorMatch is a polished Streamlit MVP inspired by **Tinder + collector cards + car/bike meet culture**.

## Features

- Lightweight auth (sign up / log in / log out) with persistent SQLite storage.
- Rich vehicle-centered user profiles that double as digital collector cards.
- Swipe-style people discovery (pass/like), mutual match logic, and match management.
- Event discovery with swipe RSVP, filters, event creation, and personal event views.
- Card Exchange system with meet memory metadata:
  - where you met
  - when you met
  - event linkage
  - notes
- Searchable “My Collection” page.
- Social-style home feed with featured builds, upcoming events, trending tags, and quick stats.
- Seed/demo data included (20+ users, 10 events).
- Modular code structure with clear seams for swapping SQLite/auth to Supabase/Firebase/Postgres later.

## Project Structure

```text
app.py
auth.py
db.py
services.py
seed_data.py
requirements.txt
README.md
pages/
  home.py
  discovery.py
  events.py
  profile.py
utils/
  constants.py
  storage.py
  ui.py
data/
uploads/
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the printed localhost URL in your browser.

## Demo login

Seed users are auto-created on first run. Use any seeded username (e.g. `kaiboost`) with:

- password: `demo123`

## Notes on future migration

- **Auth**: `auth.py` currently hashes passwords with SHA-256 and stores local credentials in SQLite. Replace these methods with Supabase/Firebase/Auth0 calls.
- **Data Access Layer**: `services.py` centralizes app logic around users/matches/events/cards; this is the main migration surface for Postgres/Firebase.
- **Storage**: image uploads are saved under `uploads/` via `utils/storage.py`. Swap that module for S3/Supabase Storage/Firebase Storage.

## MVP caveats

- Designed as an MVP for demo/portfolio use.
- Not production hardened for security (e.g., no password reset/email verification/rate-limiting).
