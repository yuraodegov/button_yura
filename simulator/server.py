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

        # =========================================
        # FSM STATUS
        # =========================================

        elif self.path == "/status":
            hostname = socket.gethostname()

            buttons_status = {}
            for btn_id, btn in simulator.buttons.items():
                import time
                now = time.time()
                held_ms = None
                if btn["state"] == "PRESSED" and btn["press_time"]:
                    held_ms = round((now - btn["press_time"]) * 1000)

                buttons_status[btn_id] = {
                    "state": btn["state"],
                    "held_ms": held_ms,
                    "last_release_time": btn["last_release_time"],
                }

            response = {
                "pod": hostname,
                "long_press_threshold_ms": int(simulator.long_press_threshold * 1000),
                "double_click_window_ms":  int(simulator.double_click_window * 1000),
                "buttons": buttons_status,
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

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

            result = simulator.handle_event(button, action)

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
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running on port {port}...")
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()