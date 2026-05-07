import sys
import os
import socket
import json
import logging
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

# Fix import path
sys.path.insert(0, os.path.dirname(__file__))

from model import ButtonSimulator

logging.basicConfig(level=logging.INFO)

simulator = ButtonSimulator()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        elif self.path == "/ui":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            ui_path = os.path.join(os.path.dirname(__file__), "ui.html")

            with open(ui_path, "r") as f:
                self.wfile.write(f.read().encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):

        # =========================================
        # BUTTON EVENTS
        # =========================================

        if self.path == "/event":

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            logging.info(f"POST /event body: {body}")

            try:
                data = json.loads(body)

            except Exception:
                self.send_response(400)
                self.end_headers()
                return

            button = data.get("button")
            action = data.get("action")

            # FSM logic
            result = simulator.handle_event(button, action)

            # add pod/container hostname
            hostname = socket.gethostname()
            result["pod"] = hostname

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())

        # =========================================
        # RUN PYTEST
        # =========================================

        elif self.path == "/run-tests":

            result = subprocess.run(
                ["pytest", "tests/", "-v"],
                capture_output=True,
                text=True
            )

            response = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":

    print("Server running on port 5000...")

    server = HTTPServer(("0.0.0.0", 5000), Handler)

    server.serve_forever()