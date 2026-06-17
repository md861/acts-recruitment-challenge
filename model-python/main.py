import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from population_model.config import ModelConfig
from population_model.model import PopulationModel


class ModelRuntime:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = PopulationModel(config)
        self.lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def snapshot(self) -> dict:
        with self.lock:
            return self.model.snapshot()

    def step(self) -> dict:
        with self.lock:
            self.model.step()
            return self.model.snapshot()

    def reset(self) -> dict:
        with self.lock:
            self.model.reset()
            return self.model.snapshot()

    def _run_loop(self) -> None:
        while not self._stop.is_set():
            time.sleep(self.config.tick_interval_seconds)
            with self.lock:
                self.model.step()


def make_handler(runtime: ModelRuntime):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path == "/health":
                self._send_json({"status": "ok"})
                return
            if path == "/snapshot":
                self._send_json(runtime.snapshot())
                return
            self._send_json({"error": "not found"}, status=404)

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            if path == "/step":
                self._send_json(runtime.step())
                return
            if path == "/reset":
                self._send_json(runtime.reset())
                return
            self._send_json({"error": "not found"}, status=404)

        def log_message(self, fmt: str, *args) -> None:
            print(f"[model] {self.address_string()} - {fmt % args}")

        def _send_json(self, payload: dict, status: int = 200) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def main() -> None:
    config = ModelConfig.from_env()
    host = os.getenv("MODEL_HOST", "127.0.0.1")
    port = int(os.getenv("MODEL_PORT", "8001"))
    runtime = ModelRuntime(config)
    runtime.start()

    server = ThreadingHTTPServer((host, port), make_handler(runtime))
    print(f"[model] listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        runtime.stop()
        server.server_close()


if __name__ == "__main__":
    main()
