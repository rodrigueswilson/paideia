"""Loopback-only HTTP interface for the synthetic technical pilot."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit

from .core import PilotError, Store

STATIC = Path(__file__).parent / "static"
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}


def handler_for(store: Store):
    class Handler(BaseHTTPRequestHandler):
        server_version = "PaideiaPilot/0.1"

        def _json(self, status: int, payload: dict | list | None):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'")
            self.end_headers()
            self.wfile.write(body)

        def _allowed_host(self) -> bool:
            host = self.headers.get("Host", "")
            return host in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}

        def do_GET(self):
            if not self._allowed_host():
                self._json(403, {"error": "Loopback host required"})
                return
            path = urlsplit(self.path).path
            if path in FILES:
                filename, mime = FILES[path]
                body = (STATIC / filename).read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'")
                self.end_headers()
                self.wfile.write(body)
            elif path == "/api/state":
                self._json(200, {"summary": store.summary(), "objects": store.objects(), "mode": "synthetic-only"})
            elif path == "/api/next":
                self._json(200, {"next": store.next_object()})
            else:
                self._json(404, {"error": "Not found"})

        def do_POST(self):
            if not self._allowed_host():
                self._json(403, {"error": "Loopback host required"})
                return
            origin = self.headers.get("Origin")
            if origin not in (None, f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}"):
                self._json(403, {"error": "Cross-origin request refused"})
                return
            if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                self._json(415, {"error": "JSON required"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = 0
            if length < 0 or length > 16384:
                self._json(413, {"error": "Request too large"})
                return
            try:
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError
            except (ValueError, UnicodeDecodeError):
                self._json(400, {"error": "Invalid JSON object"})
                return
            path = urlsplit(self.path).path
            try:
                if path == "/api/import-sample":
                    result = store.import_sample()
                    self._json(200, result)
                elif path.startswith("/api/objects/") and path.endswith("/approve"):
                    object_id = path[len("/api/objects/") : -len("/approve")]
                    self._json(200, store.approve(object_id))
                elif path == "/api/attempts":
                    result = store.record_attempt(body)
                    self._json(200 if result["replayed"] else 201, result)
                else:
                    self._json(404, {"error": "Not found"})
            except PilotError as exc:
                self._json(409, {"error": str(exc)})

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Paideia synthetic technical pilot")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--db", type=Path, default=Path("data/pilot.sqlite"))
    args = parser.parse_args()
    store = Store(args.db)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(store))
    print(f"Synthetic-only Paideia pilot: http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
