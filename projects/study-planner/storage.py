"""SQLite persistence for coursework tasks."""
import sqlite3

STATUSES = ("To do", "In progress", "Done")


def connect(path="data.sqlite3"):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def init_db(path="data.sqlite3"):
    with connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, course TEXT NOT NULL, status TEXT NOT NULL, notes TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")


def list_items(path="data.sqlite3"):
    init_db(path)
    with connect(path) as db:
        return [dict(row) for row in db.execute("SELECT * FROM tasks ORDER BY id DESC")]


def save(title, course, status, notes="", item_id=None, path="data.sqlite3"):
    title, course, notes = title.strip(), course.strip(), notes.strip()
    if not title or not course or status not in STATUSES:
        raise ValueError("Title, course and a valid status are required")
    init_db(path)
    with connect(path) as db:
        if item_id is None:
            return db.execute("INSERT INTO tasks (title, course, status, notes) VALUES (?, ?, ?, ?)", (title, course, status, notes)).lastrowid
        result = db.execute("UPDATE tasks SET title=?, course=?, status=?, notes=? WHERE id=?", (title, course, status, notes, item_id))
        if not result.rowcount:
            raise ValueError("Task not found")
        return item_id


def delete(item_id, path="data.sqlite3"):
    init_db(path)
    with connect(path) as db:
        return bool(db.execute("DELETE FROM tasks WHERE id=?", (item_id,)).rowcount)
