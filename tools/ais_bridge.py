#!/usr/bin/env python3
"""Bridge raw AIS-Catcher JSON into a normalized local snapshot/API."""

from __future__ import annotations

import argparse
import json
import socket
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-host", default="192.168.86.26")
    parser.add_argument("--source-port", type=int, default=5010)
    parser.add_argument("--write-json")
    parser.add_argument("--duration", type=float, default=15.0)
    parser.add_argument("--max-messages", type=int, default=250)
    parser.add_argument("--serve-port", type=int)
    parser.add_argument("--serve-host", default="127.0.0.1")
    parser.add_argument("--limit", type=int, default=50)
    return parser.parse_args()


class SnapshotState:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.lock = threading.Lock()
        self.started_at = time.time()
        self.messages_seen = 0
        self.last_event_at: float | None = None
        self.targets: dict[str, dict[str, Any]] = {}

    def ingest(self, payload: dict[str, Any]) -> None:
        mmsi = payload.get("mmsi")
        if not mmsi:
            return
        now = time.time()
        item = {
            "mmsi": mmsi,
            "class": payload.get("class"),
            "name": payload.get("name") or payload.get("shipname"),
            "lat": payload.get("lat"),
            "lon": payload.get("lon"),
            "speed": payload.get("speed"),
            "course": payload.get("course"),
            "heading": payload.get("heading"),
            "type": payload.get("type"),
            "aid_type_text": payload.get("aid_type_text"),
            "callsign": payload.get("callsign"),
            "timestamp": payload.get("timestamp"),
            "rxtime": payload.get("rxtime"),
            "country": payload.get("country"),
            "channel": payload.get("channel"),
            "raw": payload,
            "last_seen_unix": now,
        }
        with self.lock:
            self.messages_seen += 1
            self.last_event_at = now
            self.targets[str(mmsi)] = item
            if len(self.targets) > self.limit * 3:
                ordered = sorted(
                    self.targets.values(),
                    key=lambda row: row["last_seen_unix"],
                    reverse=True,
                )[: self.limit * 2]
                self.targets = {str(row["mmsi"]): row for row in ordered}

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            ordered = sorted(
                self.targets.values(),
                key=lambda row: row["last_seen_unix"],
                reverse=True,
            )[: self.limit]
            return {
                "ok": True,
                "source": {"host": args.source_host, "port": args.source_port},
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "messages_seen": self.messages_seen,
                "targets_seen": len(self.targets),
                "last_event_at": self.last_event_at,
                "targets": [
                    {
                        key: value
                        for key, value in row.items()
                        if key != "raw"
                    }
                    for row in ordered
                ],
            }


class SnapshotHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        if self.path in ("/", "/snapshot"):
            self._send_json(HTTPStatus.OK, self.server.state.snapshot())
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not found"})

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        blob = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def write_snapshot(path: str, state: SnapshotState) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(state.snapshot(), indent=2) + "\n", encoding="utf-8")


def collect(state: SnapshotState, duration: float, max_messages: int, write_json: str | None) -> None:
    deadline = time.time() + duration if duration > 0 else None
    with socket.create_connection((args.source_host, args.source_port), timeout=5) as sock:
        sock.settimeout(5)
        buffer = b""
        while True:
            if deadline is not None and time.time() >= deadline:
                break
            if state.messages_seen >= max_messages:
                break
            chunk = sock.recv(8192)
            if not chunk:
                break
            buffer += chunk
            while b"\n" in buffer:
                raw_line, buffer = buffer.split(b"\n", 1)
                line = raw_line.decode("utf-8", "replace").strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                state.ingest(payload)
                if write_json:
                    write_snapshot(write_json, state)


def run_server(state: SnapshotState) -> None:
    httpd = ThreadingHTTPServer((args.serve_host, args.serve_port), SnapshotHandler)
    httpd.state = state
    print(f"serving snapshot on http://{args.serve_host}:{args.serve_port}", flush=True)
    httpd.serve_forever()


def main() -> int:
    state = SnapshotState(limit=args.limit)
    server_thread = None
    if args.serve_port:
        server_thread = threading.Thread(target=run_server, args=(state,), daemon=True)
        server_thread.start()

    try:
        collect(state, args.duration, args.max_messages, args.write_json)
    finally:
        if args.write_json:
            write_snapshot(args.write_json, state)

    print(json.dumps(state.snapshot(), indent=2))
    if server_thread:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return 0
    return 0


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(main())
