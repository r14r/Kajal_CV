import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = (ROOT / 'server.py').read_text().replace("DB = ROOT / 'data.sqlite3'", f"DB = Path({str(Path(cls.temp.name) / 'test.sqlite3')!r})").replace("('127.0.0.1', 8761)", "('127.0.0.1', 0)").replace("('127.0.0.1', 8762)", "('127.0.0.1', 0)")
        # Test a real HTTP server on an available port without touching a user's database.
        import socket
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            cls.port = sock.getsockname()[1]
        cls.server = cls.server.replace("('127.0.0.1', 0)", f"('127.0.0.1', {cls.port})")
        Path(cls.temp.name, 'server.py').write_text(cls.server)
        Path(cls.temp.name, 'index.html').write_text((ROOT / 'index.html').read_text())
        cls.process = subprocess.Popen([sys.executable, str(Path(cls.temp.name, 'server.py'))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                urlopen(f'http://127.0.0.1:{cls.port}/api/items', timeout=.2).close()
                break
            except URLError:
                time.sleep(.03)
        else:
            cls.process.kill()
            raise RuntimeError('Server did not start')

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=3)
        cls.temp.cleanup()

    def call(self, path, method='GET', data=None):
        body = json.dumps(data).encode() if data is not None else None
        request = Request(f'http://127.0.0.1:{self.port}{path}', data=body, method=method, headers={'Content-Type': 'application/json'})
        try:
            with urlopen(request) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            return error.code, json.load(error)

    def test_crud_persistence_filter_and_invalid_input(self):
        status, item = self.call('/api/items', 'POST', {'title': 'Example', 'detail': '<b>text</b>'})
        self.assertEqual(status, 201)
        key = item['id']
        self.assertEqual(self.call('/api/items')[1][0]['detail'], '<b>text</b>')
        self.assertEqual(self.call('/api/items?status=missing')[0], 400)
        self.assertEqual(self.call('/api/items', 'POST', {'title': '   '})[0], 400)
        self.assertEqual(self.call(f'/api/items/{key}', 'PUT', {'title': 'Changed', 'status': 'Done' if 'Study Planner' in self.server else 'Interview'})[0], 200)
        self.assertEqual(self.call('/api/items?status=' + ('Done' if 'Study Planner' in self.server else 'Interview'))[1][0]['title'], 'Changed')
        self.assertEqual(self.call(f'/api/items/{key}', 'DELETE')[0], 200)
        self.assertEqual(self.call(f'/api/items/{key}', 'DELETE')[0], 404)
        self.assertEqual(self.call('/api/items')[1], [])
