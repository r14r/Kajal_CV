# Job Application Tracker

A complete, local single-user web app. Uses Python 3.10+ standard library, SQLite, HTML, CSS, and JavaScript. No installation, account, network connection, or API key is needed.

## Run

```bash
cd projects/job-application-tracker
python3 server.py
```

Open <http://127.0.0.1:8761>. Press Ctrl+C to stop. The app creates `data.sqlite3` beside `server.py`; it persists between restarts and is ignored by Git. Do not publish private data from that file.

## Capabilities

- Add, edit, delete, search, and filter applications.
- Data validation in both the browser and server; server responses for invalid requests and missing items.
- Responsive layout; readable on phones.
- Local HTTP JSON API: `GET /api/items`, `GET /api/items?status=...`, `POST /api/items`, `PUT /api/items/ID`, `DELETE /api/items/ID`.

## Verification

Run `python3 -m unittest discover -s tests -v` in this folder. Then add an item in the browser, reload, edit it, filter it, and delete it.

## Design notes

This app binds to `127.0.0.1` and has no login. It is a portfolio demonstration, not a multi-user production service. HTML is built with DOM `textContent` so entered notes are displayed as text. To deploy publicly, add authentication, access control, HTTPS, and a production server.
