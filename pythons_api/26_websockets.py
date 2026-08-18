"""Real implementation: WebSockets with FastAPI.

WebSockets give you a persistent, bidirectional, full-duplex channel between
client and server - ideal for live feeds, notifications, dashboards, chat.

Run:
    pip install fastapi "uvicorn[standard]" websockets
    python 26_websockets.py

Test with a WebSocket client:
    pip install websockets
    python -m websockets ws://127.0.0.1:8000/ws
"""

import asyncio
import json
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="WebSocket Demo", version="1.0.0")


class ConnectionManager:
    """Track live connections and broadcast messages to all of them."""

    def __init__(self) -> None:
        self.active: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active.discard(websocket)

    async def send_personal(self, websocket: WebSocket, message: dict[str, Any]) -> None:
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict[str, Any]) -> None:
        text = json.dumps(message)
        for ws in list(self.active):
            try:
                await ws.send_text(text)
            except Exception:
                self.disconnect(ws)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.send_personal(websocket, {"type": "connected", "data": "welcome"})
        while True:
            raw = await websocket.receive_text()
            message = json.loads(raw)
            await manager.broadcast({"type": "chat", "sender": message.get("name", "anon"),
                                     "data": message.get("text", "")})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "disconnected"})


@app.websocket("/ws/echo")
async def echo_endpoint(websocket: WebSocket):
    """Echo server - the simplest possible WebSocket handler."""
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            await websocket.send_text(f"echo: {raw}")
    except WebSocketDisconnect:
        pass


@app.get("/")
def root():
    return {"websockets": ["/ws", "/ws/echo"]}


# ------------------------------------------------------------------ client
async def demo_client() -> None:
    """Minimal WebSocket client using the `websockets` library."""
    import websockets

    uri = "ws://127.0.0.1:8000/ws/echo"
    async with websockets.connect(uri) as ws:
        await ws.send("hello over the wire")
        reply = await ws.recv()
        print(f"  received: {reply}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)