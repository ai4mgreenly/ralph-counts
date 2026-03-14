#!/usr/bin/env python3
"""Tiny server for ralph-counts dashboard. Serves index.html and the stats file."""

import http.server
import json
import os
import sys

STATS_PATH = os.path.expanduser("~/.local/state/ralph/stats.jsonl")
HOST = os.environ.get("RALPH_COUNTS_HOST", "localhost")
PORT = int(os.environ.get("RALPH_COUNTS_PORT", "5004"))
DIR = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/stats":
            try:
                with open(STATS_PATH, "r") as f:
                    raw = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(raw.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"stats.jsonl not found")
            return
        super().do_GET()

    def log_message(self, format, *args):
        pass  # silence request logs


if __name__ == "__main__":
    server = http.server.HTTPServer((HOST, PORT), Handler)
    print(f"ralph-counts → http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
