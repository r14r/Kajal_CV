"""Local, single-user portfolio demonstration. Data stays in data.sqlite3."""
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'data.sqlite3'
TITLE = 'Job Application Tracker'
STATES = ['Applied', 'Interview', 'Offer', 'Rejected']


def init_db():
    with sqlite3.connect(DB) as db:
        db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, title TEXT NOT NULL, detail TEXT NOT NULL DEFAULT "", status TEXT NOT NULL, created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)')


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        encoded = json.dumps(body).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def read_body(self):
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size < 1 or size > 16384:
                raise ValueError('Body must be between 1 and 16384 bytes')
            value = json.loads(self.rfile.read(size))
            if not isinstance(value, dict):
                raise ValueError('Expected a JSON object')
            title = value.get('title', '')
            detail = value.get('detail', '')
            state = value.get('status', STATES[0])
            if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
                raise ValueError('Title must contain 1-120 characters')
            if not isinstance(detail, str) or len(detail) > 1000:
                raise ValueError('Detail must contain at most 1000 characters')
            if state not in STATES:
                raise ValueError('Invalid status')
            return title.strip(), detail.strip(), state
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError, TypeError) as error:
            self.reply(400, {'error': str(error)})
            return None

    def item_id(self):
        path = urlparse(self.path).path
        if not path.startswith('/api/items/'):
            return None
        try:
            value = int(path.removeprefix('/api/items/'))
            return value if value > 0 else None
        except ValueError:
            return None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            data = (ROOT / 'index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path == '/api/items':
            query = parse_qs(urlparse(self.path).query)
            status = query.get('status', [''])[0]
            if status and status not in STATES:
                return self.reply(400, {'error': 'Invalid status filter'})
            with sqlite3.connect(DB) as db:
                db.row_factory = sqlite3.Row
                rows = db.execute('SELECT * FROM items WHERE (? = "" OR status = ?) ORDER BY id DESC', (status, status)).fetchall()
            return self.reply(200, [dict(row) for row in rows])
        self.reply(404, {'error': 'Not found'})

    def do_POST(self):
        if urlparse(self.path).path != '/api/items':
            return self.reply(404, {'error': 'Not found'})
        item = self.read_body()
        if item is None:
            return
        with sqlite3.connect(DB) as db:
            cursor = db.execute('INSERT INTO items(title, detail, status) VALUES (?, ?, ?)', item)
            row = db.execute('SELECT * FROM items WHERE id = ?', (cursor.lastrowid,)).fetchone()
        self.reply(201, dict(zip(('id', 'title', 'detail', 'status', 'created'), row)))

    def do_PUT(self):
        key = self.item_id()
        if key is None:
            return self.reply(404, {'error': 'Not found'})
        item = self.read_body()
        if item is None:
            return
        with sqlite3.connect(DB) as db:
            cursor = db.execute('UPDATE items SET title = ?, detail = ?, status = ? WHERE id = ?', (*item, key))
        self.reply(200, {'updated': True}) if cursor.rowcount else self.reply(404, {'error': 'Not found'})

    def do_DELETE(self):
        key = self.item_id()
        if key is None:
            return self.reply(404, {'error': 'Not found'})
        with sqlite3.connect(DB) as db:
            cursor = db.execute('DELETE FROM items WHERE id = ?', (key,))
        self.reply(200, {'deleted': True}) if cursor.rowcount else self.reply(404, {'error': 'Not found'})


if __name__ == '__main__':
    init_db()
    print('Open http://127.0.0.1:8761 (Ctrl+C to stop)')
    ThreadingHTTPServer(('127.0.0.1', 8761), Handler).serve_forever()
