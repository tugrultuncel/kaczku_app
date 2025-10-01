# Kaczku App

Kaczku is a collaborative mapping application where every registered user can pin locations on a shared map. All pins are visible to all authenticated users, making it easy to share favourite places, meet-up spots, or important locations with the whole community.

## Features

- 🔐 **Account management** – Register, log in, and log out securely with hashed passwords.
- 🗺️ **Interactive map** – Built with [Leaflet](https://leafletjs.com/) and OpenStreetMap tiles.
- 📍 **Shared pin board** – Add map pins with a title and optional description; everyone can see them instantly.
- 📨 **Real-time updates** – New pins appear immediately without reloading the page.

## Getting started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the development server

```bash
flask --app app:create_app --debug run
```

The application uses SQLite by default and creates the `kaczku.db` database file in the project root on first run.

### 3. Create an account

- Visit `http://127.0.0.1:5000/register` to sign up.
- After logging in you will be redirected to the shared map, where you can click anywhere to add a new pin.

## Configuration

Environment variables can be used to override defaults:

- `SECRET_KEY` – Flask secret key (default: `dev-secret-key`).
- `DATABASE_URL` – SQLAlchemy connection string (default: `sqlite:///kaczku.db`).

## Project structure

```
app/
├── __init__.py
├── auth.py
├── models.py
├── pins.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── map.js
└── templates/
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── base.html
    └── pins/
        └── map.html
```

`app.py` is provided for local development convenience, instantiating the Flask application using the factory pattern defined in `app/__init__.py`.
