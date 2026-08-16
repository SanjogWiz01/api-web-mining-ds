"""
📘 TOPIC 27: Server-Sent Events (SSE) — One-Way Streams
======================================================
SSE lets a server push updates to the client over a single HTTP
connection. Unlike WebSockets it is one-way and uses plain HTTP.

Format (text/event-stream):
    data: {"message": "hello"}

    (each event separated by a blank line)

Use case: live feeds, progress updates, notification streams.
"""

import requests
import json


# ─────────────────────────────────────────────
# 1. Show SSE format
# ─────────────────────────────────────────────
def sse_format():
    print("\n── SSE Format ───────────────────────")
    events = [
        'data: {"id": 1, "msg": "tick"}',
        "",
        'data: {"id": 2, "msg": "tock"}',
        "",
        'id: 3',
        'event: done',
        'data: {"finished": true}',
        "",
    ]
    print("  text/event-stream body:")
    print("  " + "\n  ".join(events))


# ─────────────────────────────────────────────
# 2. Parse an SSE stream
# ─────────────────────────────────────────────
def parse_sse(stream_text: str):
    print("\n── Parse SSE Stream ────────────────")
    events = []
    current = {}
    for line in stream_text.splitlines():
        if not line.strip():
            if current:
                events.append(current)
                current = {}
            continue
        if line.startswith("data:"):
            current["data"] = line[5:].strip()
        elif line.startswith("id:"):
            current["id"] = line[3:].strip()
        elif line.startswith("event:"):
            current["event"] = line[6:].strip()
    if current:
        events.append(current)
    for ev in events:
        print(f"  event={ev.get('event', 'message')} id={ev.get('id')} → {ev.get('data')}")


def demo_parse():
    raw = 'data: {"n":1}\n\nid: 5\nevent: update\ndata: {"n":2}\n\n'
    parse_sse(raw)


# ─────────────────────────────────────────────
# 3. Live connection with requests (stream=True)
# ─────────────────────────────────────────────
def live_stream():
    print("\n── Live SSE Connection ──────────────")
    print("  With `requests`, stream=True + iter_lines():")
    code = '''
with requests.get(url, stream=True) as r:
    for line in r.iter_lines():
        if line.startswith(b"data:"):
            payload = json.loads(line[5:])
            print(payload)
'''
    print(code)


# ─────────────────────────────────────────────
# 4. SSE vs WebSocket
# ─────────────────────────────────────────────
def sse_vs_ws():
    print("\n── SSE vs WebSocket ────────────────")
    comparison = [
        ("SSE", "Server → client only, plain HTTP, auto-reconnect"),
        ("WebSocket", "Bidirectional, binary + text, full duplex"),
    ]
    for label, text in comparison:
        print(f"  {label:<10} {text}")


if __name__ == "__main__":
    print("=" * 55)
    print("  SERVER-SENT EVENTS: one-way push")
    print("=" * 55)
    sse_format()
    demo_parse()
    live_stream()
    sse_vs_ws()
    print("\nSSE demos complete.")