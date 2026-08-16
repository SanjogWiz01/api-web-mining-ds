"""
📘 TOPIC 26: WebSockets — Real-Time, Bidirectional
=================================================
WebSockets keep a single open connection for two-way, real-time
communication (chat, live prices, notifications).

Unlike HTTP:
  HTTP        → request → response → close
  WebSocket   → client connects once, both sides push anytime

Requires `pip install websockets` (or `websocket-client`).
"""


# ─────────────────────────────────────────────
# 1. WebSocket handshake concept
# ─────────────────────────────────────────────
def handshake():
    print("\n── WebSocket Handshake ──────────────")
    steps = [
        ("1", "Client sends GET /socket with Upgrade: websocket"),
        ("2", "Server replies 101 Switching Protocols"),
        ("3", "Connection is now open and bidirectional"),
        ("4", "Frames flow both ways until either side closes"),
    ]
    for num, step in steps:
        print(f"  Step {num}: {step}")


# ─────────────────────────────────────────────
# 2. Async echo client example (websockets lib)
# ─────────────────────────────────────────────
def async_client_example():
    print("\n── Async Echo Client ────────────────")
    code = '''
import asyncio
import websockets

async def chat():
    async with websockets.connect("wss://echo.websocket.org") as ws:
        await ws.send("hello server")
        reply = await ws.recv()
        print(f"Server echoed: {reply}")

asyncio.run(chat())
'''
    print(code)


# ─────────────────────────────────────────────
# 3. Message frames (text vs binary)
# ─────────────────────────────────────────────
def message_frames():
    print("\n── Message Frames ───────────────────")
    frames = [
        ("Text", "UTF-8 strings — JSON payloads are common"),
        ("Binary", "Raw bytes — images, protobuf, audio"),
        ("Ping/Pong", "Keepalive so proxies don't drop idle links"),
        ("Close", "Clean shutdown with a status code"),
    ]
    for kind, desc in frames:
        print(f"  {kind:<10} {desc}")


# ─────────────────────────────────────────────
# 4. Common use cases
# ─────────────────────────────────────────────
def use_cases():
    print("\n── Use Cases ────────────────────────")
    cases = [
        "Live chat & collaboration",
        "Stock tickers & streaming prices",
        "Real-time dashboards & notifications",
        "Multiplayer games",
    ]
    for c in cases:
        print(f"  • {c}")


if __name__ == "__main__":
    print("=" * 55)
    print("  WEBSOCKETS: real-time bidirectional")
    print("=" * 55)
    handshake()
    async_client_example()
    message_frames()
    use_cases()
    print("\nWebSocket demos complete.")