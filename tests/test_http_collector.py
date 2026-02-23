import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from mvp_bot.collectors.http_json_collector import HttpJsonCollector


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "items": [
                {
                    "text": "crypto cat narrative",
                    "author": "alice",
                    "likes": 9,
                    "shares": 2,
                    "comments": 1,
                    "created_at": "2026-01-01T00:00:00Z",
                    "source": "x",
                }
            ]
        }
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


class HttpCollectorTest(unittest.TestCase):
    def test_fetch_recent(self):
        server = HTTPServer(("127.0.0.1", 0), _Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            endpoint = f"http://127.0.0.1:{server.server_port}/feed"
            collector = HttpJsonCollector(endpoint=endpoint)
            events = collector.fetch_recent()
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].author, "alice")
            self.assertEqual(events[0].source, "x")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
