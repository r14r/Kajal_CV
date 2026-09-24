import os
import tempfile
import unittest

from fastapi.testclient import TestClient
from retrieval import chunks, retrieve


class RetrievalTests(unittest.TestCase):
    def test_chunk_and_rank(self):
        self.assertTrue(all(len(x) <= 650 for x in chunks('a ' * 900)))
        documents = [{'id': 1, 'title': 'Database', 'content': 'SQLite stores data in a local file.'},
                     {'id': 2, 'title': 'Design', 'content': 'Animation makes a web page move.'}]
        self.assertEqual(retrieve('Where does SQLite store data?', documents)[0]['id'], 1)
        self.assertEqual(retrieve('zebra', documents), [])


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        os.environ['RAG_DATA_DIR'] = self.temp.name
        # `DATA` and `DB` are module constants; change them only within this isolated test process.
        import app
        from pathlib import Path
        app.DATA = Path(self.temp.name)
        app.DB = app.DATA / 'chat.sqlite3'
        self.client = TestClient(app.app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.temp.cleanup()

    def test_chat_retrieves_sources_and_persists(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertGreaterEqual(len(self.client.get('/api/documents').json()), 3)
        response = self.client.post('/api/chat', json={'question': 'How does SQLite store data?'})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['mode'], 'extracts')
        self.assertTrue(any('sqlite' in c['document'] for c in result['citations']))
        saved = self.client.get(f"/api/conversations/{result['conversation_id']}").json()
        self.assertEqual([m['role'] for m in saved['messages']], ['user', 'assistant'])
        self.assertEqual(self.client.post('/api/chat', json={'question': 'More about SQLite', 'conversation_id':999999}).status_code, 404)
        self.assertEqual(self.client.delete(f"/api/conversations/{result['conversation_id']}").status_code, 200)

    def test_add_delete_document_and_validation(self):
        self.assertEqual(self.client.post('/api/documents', json={'title':'x','content':'short'}).status_code, 422)
        created = self.client.post('/api/documents', json={'title':'Custom','content':'A custom database note about indexing and queries.'})
        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.delete('/api/documents/' + str(created.json()['id'])).status_code, 200)
        self.assertEqual(self.client.delete('/api/documents/999999').status_code, 404)
