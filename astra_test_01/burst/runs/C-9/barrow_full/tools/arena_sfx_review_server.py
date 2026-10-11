#!/usr/bin/env python3
"""Serve only the SFX sheet and validated selection handoffs on the local LAN."""
import argparse
import hashlib
import json
import os
import socket
import tempfile
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY = 1_000_000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def lan_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
        connection.connect(("192.0.2.1", 9))  # Routing lookup only; no packets sent.
        return connection.getsockname()[0]


def validate(raw, catalogue):
    if not isinstance(raw, dict) or any(raw.get(key) != value for key, value in {
        "schema": "barrow_sfx_selections_v1",
        "catalog_sha256": catalogue["catalog_sha256"],
        "manifest_sha256": catalogue["manifest_sha256"],
    }.items()):
        raise ValueError("This selection file belongs to a different sound review.")
    choices = raw.get("choices")
    actions = {action["key"]: action for action in catalogue["actions"]}
    if not isinstance(choices, dict) or set(choices) - set(actions):
        raise ValueError("Unknown action in selections.")
    cleaned, resolved = {}, []
    for key, action in actions.items():
        row = choices.get(key, {"choice": "pending", "notes": ""})
        if not isinstance(row, dict):
            raise ValueError("Invalid choice for " + action["label"])
        options = {option["id"]: option for option in action["options"]}
        choice, notes = row.get("choice"), row.get("notes")
        if not isinstance(choice, str) or choice not in {"pending", "mute", "find_more", *options} or not isinstance(notes, str) or len(notes) > 10000:
            raise ValueError("Invalid choice for " + action["label"])
        if key in choices:
            cleaned[key] = {"choice": choice, "notes": notes}
        sources = options.get(choice, {}).get("sources", [])
        resolved.append({"cue": key, "label": action["label"], "choice": choice, "notes": notes,
                         "sources": [{"path": path, "sha256": catalogue["clips"][path]["sha256"]} for path in sources]})
    return {"schema": "barrow_sfx_selections_v1", "catalog_sha256": catalogue["catalog_sha256"],
            "manifest_sha256": catalogue["manifest_sha256"], "music": "accepted_for_now",
            "choices": cleaned, "resolved_choices": resolved}


class ReviewServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, catalogue, page, selections, allowed_hosts):
        super().__init__(address, Handler)
        self.catalogue, self.page, self.selections = catalogue, page, selections
        self.allowed_hosts, self.selection_lock = allowed_hosts, threading.Lock()

    def saved(self):
        if not self.selections.exists():
            return {"revision": None, "selection": None}
        data = self.selections.read_bytes()
        raw = json.loads(data)
        validate(raw, self.catalogue)
        return {"revision": sha(data), "selection": raw}


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body, content_type="application/json"):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def host_ok(self):
        try:
            host = urlsplit("http://" + self.headers.get("Host", "")).hostname
        except ValueError:
            host = None
        if host not in self.server.allowed_hosts:
            self.reply(403, {"error": "Use the local address printed by the server."})
            return False
        return True

    def do_GET(self):
        if not self.host_ok():
            return
        path = urlsplit(self.path).path
        if path in ("/", "/SFX_REVIEW.html"):
            self.reply(200, self.server.page, "text/html; charset=utf-8")
        elif path == "/api/selections":
            try:
                with self.server.selection_lock:
                    saved = self.server.saved()
                self.reply(200, saved)
            except (ValueError, OSError) as error:
                self.reply(500, {"error": "Saved selections could not be read: " + str(error)})
        elif path == "/favicon.ico":
            self.reply(204, b"")
        else:
            self.reply(404, {"error": "Not found"})

    do_HEAD = do_GET

    def do_POST(self):
        if not self.host_ok():
            return
        if urlsplit(self.path).path != "/api/selections":
            self.reply(404, {"error": "Not found"})
            return
        # Same-origin JSON writes only; no CORS and no arbitrary filesystem access.
        origin = self.headers.get("Origin")
        if origin and origin != "http://" + self.headers.get("Host"):
            self.reply(403, {"error": "Selections must be saved from this review page."})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.reply(415, {"error": "JSON selections required."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BODY:
                self.reply(413, {"error": "Selection file is too large or empty."})
                return
            self.connection.settimeout(10)
            raw = json.loads(self.rfile.read(size))
            if not isinstance(raw, dict) or "expected_revision" not in raw:
                raise ValueError("Load the saved selection revision before saving.")
            selection = validate(raw.get("selection"), self.server.catalogue)
            with self.server.selection_lock:
                existing = self.server.saved()
                if raw["expected_revision"] != existing["revision"]:
                    self.reply(409, {"error": "Another device saved newer choices. Export your local choices, then load the saved choices before saving again."})
                    return
                selection["saved_at"] = datetime.now(timezone.utc).isoformat()
                data = (json.dumps(selection, indent=2) + "\n").encode()
                destination = self.server.selections
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    # Keep the previous handoff too; atomic writes preserve a good file.
                    backup = destination.with_name(destination.stem + ".previous.json")
                    self.atomic_write(backup, destination.read_bytes())
                self.atomic_write(destination, data)
            self.reply(200, {"revision": sha(data), "saved_at": selection["saved_at"]})
        except (ValueError, OSError) as error:
            self.reply(400, {"error": str(error)})

    @staticmethod
    def atomic_write(destination, data):
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".sfx-save-", delete=False) as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
            temporary = output.name
        os.replace(temporary, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8767)
    parser.add_argument("--selections", type=Path, default=ROOT / "audio_review/selections/barrow-sfx-selections.json")
    args = parser.parse_args()
    catalogue = json.loads((ROOT / "audio_review/SFX_REVIEW_CATALOG.json").read_text())
    page = (ROOT / "audio_review/SFX_REVIEW.html").read_text()
    hostname, ip = socket.gethostname().lower(), lan_ip()
    page = page.replace('<script id="review-data"', '<script>window.BARROW_REVIEW_SERVER=true;</script>\n<script id="review-data"', 1)
    server = ReviewServer((args.host, args.port), catalogue, page.encode(), args.selections,
                          {"localhost", "127.0.0.1", hostname, hostname.split(".")[0], ip})
    print(json.dumps({"phone_url": f"http://{ip}:{args.port}/", "local_url": f"http://localhost:{args.port}/", "selections": str(args.selections), "pid": os.getpid()}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
