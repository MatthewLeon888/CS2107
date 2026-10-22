#!/usr/bin/env python3
"""Intentionally vulnerable SSRF training service (local CTF use only)."""
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import ProxyHandler, Request, build_opener

PUBLIC_PORT = int(os.environ.get("PORT", "5000"))
INTERNAL_PORT = int(os.environ.get("INTERNAL_PORT", "5001"))
FLAG_PATH = Path(os.environ.get("FLAG_PATH", Path(__file__).with_name("flag.txt")))

# No environment proxies: requests to loopback must really reach this process.
FETCHER = build_opener(ProxyHandler({}))


class QuietHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def reply(self, code, data, content_type="text/plain; charset=utf-8"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class StaffOnly(QuietHandler):
    def do_GET(self):
        if urlsplit(self.path).path != "/staff/flag":
            self.reply(404, "Not found\n")
            return
        try:
            flag = FLAG_PATH.read_text(encoding="utf-8").strip()
        except OSError:
            self.reply(500, "The staff vault is unavailable.\n")
            return
        self.reply(200, flag + "\n")


class Noticeboard(QuietHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/":
            body = """<!doctype html>
<html lang="en"><meta charset="utf-8"><title>NUT Noticeboard Preview</title>
<h1>NUT Noticeboard: Link Preview</h1>
<p>Paste a public URL to preview the page through our server.</p>
<form action="/preview" method="get">
<input name="url" size="60" placeholder="http://example.org/">
<button>Preview</button></form></html>"""
            self.reply(200, body, "text/html; charset=utf-8")
            return
        if parsed.path != "/preview":
            self.reply(404, "Not found\n")
            return
        url = parse_qs(parsed.query).get("url", [""])[0]
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            self.reply(400, "Please provide an absolute HTTP(S) URL.\n")
            return

        # VULNERABILITY: validates the URL scheme, but not its destination.
        # Requests to 127.0.0.1 (or another private network host) are allowed.
        try:
            req = Request(url, headers={"User-Agent": "NUT-LinkPreview/1.0"})
            with FETCHER.open(req, timeout=3) as response:
                body = response.read(65536)
        except (URLError, HTTPError, OSError, ValueError) as err:
            self.reply(502, "Preview failed: " + str(err) + "\n")
            return
        self.reply(200, body)


def main():
    internal = ThreadingHTTPServer(("127.0.0.1", INTERNAL_PORT), StaffOnly)
    threading.Thread(target=internal.serve_forever, daemon=True).start()
    public = ThreadingHTTPServer(("0.0.0.0", PUBLIC_PORT), Noticeboard)
    print(f"Noticeboard on :{PUBLIC_PORT}; staff service on 127.0.0.1:{INTERNAL_PORT}", flush=True)
    try:
        public.serve_forever()
    finally:
        public.server_close()
        internal.shutdown()
        internal.server_close()


if __name__ == "__main__":
    main()
