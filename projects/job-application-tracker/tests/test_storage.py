import tempfile
import unittest
from pathlib import Path

from storage import STATUSES, delete, list_items, save


class StorageTests(unittest.TestCase):
    def test_create_edit_delete_and_validation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = str(Path(temp) / "app.sqlite3")
            ident = save("  Example  ", "Developer", STATUSES[0], " note ", path=path)
            self.assertEqual(list_items(path)[0]["id"], ident)
            self.assertEqual(list_items(path)[0]["notes"], "note")
            save("Example", "Engineer", STATUSES[-1], item_id=ident, path=path)
            self.assertEqual(list_items(path)[0]["role"] if "role" in list_items(path)[0] else list_items(path)[0]["title"], "Engineer")
            self.assertTrue(delete(ident, path))
            self.assertEqual(list_items(path), [])
            with self.assertRaises(ValueError):
                save("", "Engineer", STATUSES[0], path=path)
