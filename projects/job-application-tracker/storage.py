"""SQLite persistence for a single user's job applications."""
import sqlite3
from pathlib import Path

STATUSES = ("Interested", "Applied", "Interview", "Offer", "Closed")


def connect(path="data.sqlite3"):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(path="data.sqlite3"):
    with connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, company TEXT NOT NULL, role TEXT NOT NULL, status TEXT NOT NULL, notes TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")


def list_items(path="data.sqlite3"):
    init_db(path)
    with connect(path) as db:
        return [dict(row) for row in db.execute("SELECT * FROM applications ORDER BY id DESC")]


def save(company, role, status, notes="", item_id=None, path="data.sqlite3"):
    company, role, notes = company.strip(), role.strip(), notes.strip()
    if not company or not role or status not in STATUSES:
        raise ValueError("Company, role and a valid status are required")
    init_db(path)
    with connect(path) as db:
        if item_id is None:
            return db.execute("INSERT INTO applications (company, role, status, notes) VALUES (?, ?, ?, ?)", (company, role, status, notes)).lastrowid
        result = db.execute("UPDATE applications SET company=?, role=?, status=?, notes=? WHERE id=?", (company, role, status, notes, item_id))
        if not result.rowcount:
            raise ValueError("Application not found")
        return item_id


def delete(item_id, path="data.sqlite3"):
    init_db(path)
    with connect(path) as db:
        return bool(db.execute("DELETE FROM applications WHERE id=?", (item_id,)).rowcount)
