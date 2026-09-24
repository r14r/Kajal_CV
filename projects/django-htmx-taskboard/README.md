# Momentum - Django + HTMX task board

A complete local task board with a Django/SQLite backend and server-rendered HTMX interactions. The HTMX JavaScript file is bundled in `board/static/board/`, so the app needs no CDN at runtime.

## Run (Python 3.10+)

```bash
cd projects/django-htmx-taskboard
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/>. The app stores tasks in `db.sqlite3`. For tests, run `python manage.py test`. The test suite checks creation, validation, filtering, completion, deletion and CSRF protection.

## How it works

- Django models and migrations own the SQLite database.
- The form validates task names and notes.
- HTMX requests return a server-rendered task-list fragment, replacing only `#task-list`.
- Django escapes user-supplied task text and checks CSRF for mutations.

This is a single-user development demonstration. `DEBUG` defaults to enabled, and the development secret key is not suitable for public deployment. Before deploying, configure a new `DJANGO_SECRET_KEY`, disable debug, set approved hosts, add authentication and use a production server.

HTMX copyright Big Sky Software, licensed under the Zero-Clause BSD licence; see `board/static/board/htmx.LICENSE`.
