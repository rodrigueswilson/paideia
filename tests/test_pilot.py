"""End-to-end checks of the pilot's irreversible data boundaries."""

from __future__ import annotations

from contextlib import closing
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

from http.server import ThreadingHTTPServer

from paideia_pilot.core import PilotError, Store
from paideia_pilot.server import handler_for


class PilotStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "pilot.sqlite")

    def tearDown(self):
        self.temp.cleanup()

    def _approved(self):
        self.store.import_sample()
        for item in self.store.objects():
            self.store.approve(item["id"])

    def _attempt(self, item, rating="matched"):
        return {
            "attempt_id": str(uuid4()), "event_id": str(uuid4()),
            "presentation_id": item["presentation_id"], "object_id": item["id"],
            "object_version": item["version"], "rating": rating, "used_hint": False,
        }

    def test_duplicate_import_and_changed_quote(self):
        first = self.store.import_sample()
        second = self.store.import_sample()
        self.assertEqual(first["document_id"], second["document_id"])
        self.assertEqual(self.store.summary(), {"sources": 1, "documents": 1, "objects": 3, "approved": 0, "attempts": 0})
        object_id = first["objects"][0]["id"]
        with closing(sqlite3.connect(self.store.path)) as db:
            db.execute("UPDATE objects SET quote='An altered quotation' WHERE id=?", (object_id,))
            db.commit()
        with self.assertRaisesRegex(PilotError, "Quotation does not match"):
            self.store.approve(object_id)

    def test_retry_conflict_ranking_and_restore(self):
        self._approved()
        first = self.store.next_object()
        attempt = self._attempt(first)
        self.assertFalse(self.store.record_attempt(attempt)["replayed"])
        self.assertTrue(self.store.record_attempt(attempt)["replayed"])
        conflicting = {**attempt, "rating": "partial"}
        with self.assertRaisesRegex(PilotError, "different data"):
            self.store.record_attempt(conflicting)
        duplicate_event = {**attempt, "attempt_id": str(uuid4())}
        with self.assertRaisesRegex(PilotError, "Event ID already belongs"):
            self.store.record_attempt(duplicate_event)
        self.assertEqual(self.store.summary()["attempts"], 1)
        second = self.store.next_object()
        self.assertNotEqual(first["id"], second["id"])
        self.store.record_attempt(self._attempt(second, "skip"))
        third = self.store.next_object()
        self.assertNotEqual(second["id"], third["id"])
        backup = Path(self.temp.name) / "backup.sqlite"
        self.store.backup(backup)
        restored = Store(backup)
        self.assertEqual(restored.summary(), self.store.summary())
        self.assertEqual(restored.next_object()["id"], third["id"])


class PilotHTTPTests(unittest.TestCase):
    def test_loopback_http_flow_and_origin_guard(self):
        with TemporaryDirectory() as directory:
            store = Store(Path(directory) / "pilot.sqlite")
            server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(store))
            worker = Thread(target=server.serve_forever, daemon=True)
            worker.start()
            base = f"http://127.0.0.1:{server.server_port}"
            try:
                with urlopen(base + "/") as response:
                    self.assertIn(b"Synthetic-only pilot", response.read())
                payload = json.dumps({}).encode()
                request = Request(base + "/api/import-sample", payload, {"Content-Type": "application/json"})
                with urlopen(request) as response:
                    self.assertEqual(len(json.load(response)["objects"]), 3)
                blocked = Request(
                    base + "/api/import-sample", payload,
                    {"Content-Type": "application/json", "Origin": "https://example.invalid"},
                )
                with self.assertRaises(HTTPError) as error:
                    urlopen(blocked)
                self.assertEqual(error.exception.code, 403)
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
