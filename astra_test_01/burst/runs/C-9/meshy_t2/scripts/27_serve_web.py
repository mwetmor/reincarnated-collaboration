#!/usr/bin/env python3
"""Serve reincarnated-loadout/public locally so /playtest/cliffside/ can be driven.

    python3 scripts/27_serve_web.py [public_dir] [port]

python3 -m http.server is NOT good enough here. Godot's loader calls
WebAssembly.instantiateStreaming, which REFUSES a response whose Content-Type is
not application/wasm rather than falling back -- and http.server's mimetypes table
does not know .wasm on every macOS Python. The page would then fail for a reason
that has nothing to do with the build under test, which is the worst kind of
verification failure: one that looks like a finding.

The route's shell carries <base href="/playtest/cliffside/">, so the server root
must be public/, not the route directory.
"""
import functools
import http.server
import socketserver
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/admin/Games/reincarnated-loadout/public"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8731


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
        ".pck": "application/octet-stream",
        ".js": "text/javascript",
        ".json": "application/json",
    }

    def log_message(self, fmt, *a):
        sys.stderr.write("%s\n" % (fmt % a))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), functools.partial(Handler, directory=ROOT)) as s:
        print("serving %s on http://127.0.0.1:%d/" % (ROOT, PORT), flush=True)
        s.serve_forever()
