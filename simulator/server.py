import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # fix импорта model

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

from model import ButtonSimulator

logging.basicConfig(level=logging.INFO)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        elif self.path == "/ui":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            # fix пути к ui.html
            ui_path = os.path.join(os.path.dirname(__file__), "ui.html")
            with open(ui_path, "r") as f:
                self.wfile.write(f.read().encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/event":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            logging.info(f"POST /event body: {body}")  # fix логирование

            try:
                data = json.loads(body)
            except Exception:
                self.send_response(400)
                self.end_headers()
                return

            button = data.get("button")
            action = data.get("action")

            # fix: создаём новый simulator на каждый запрос — нет, лучше сбрасывать состояние
            result = simulator.handle_event(button, action)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # отключаем стандартные логи сервера


simulator = ButtonSimulator()
server = HTTPServer(("0.0.0.0", 5000), Handler)

if __name__ == "__main__":
    print("Server running on port 5000...")
    server.serve_forever()