# Webhooks: letting the API call you back

Webhooks flip the model: instead of polling an API for changes, you register a
URL and the API *pushes* events to it over HTTP.

## Polling vs Webhooks

```
POLLING (you ask every N seconds)        WEBHOOKS (API pushes when it changes)
[client] --GET /events?since=X--> [api]  [api] --POST /you/webhook--> [server]
[client] <--empty--               [api]  [api] --POST /you/webhook--> [server]
[client] --GET /events?since=X--> [api]  ...
```

Polling wastes requests; webhooks are event-driven and near real-time.

## How a webhook works

1. You register a URL (e.g. `https://myapp.com/api/orders/events`).
2. The API signs and POSTs a JSON payload to it on each event.
3. You respond fast with `2xx`; anything else makes the API retry.
4. Handle the event asynchronously (queue) if processing is slow.

## Typical webhook payload

```json
{
  "id": "evt_123",
  "type": "order.created",
  "created": 1720000000,
  "data": { "order_id": 456, "amount": 99.5 }
}
```

## Receiving webhooks in Python (Flask)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/api/orders/events")
def handle_event():
    payload = request.get_json(force=True)
    event_type = payload.get("type")
    print(f"received {event_type}: {payload['data']}")
    return jsonify({"ok": True}), 200   # acknowledge fast
```

## Webhook security

- **Signatures**: verify a signature header (HMAC with a shared secret).
- **Replay protection**: check the `event id` against processed ids.
- **HTTPS only**: never send webhooks over plain HTTP.

```python
import hashlib, hmac

def verify_signature(secret: bytes, payload: bytes, signature: str) -> bool:
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## Webhook delivery best practices

- Acknowledge with `200` as soon as received; do heavy work in a worker/queue.
- Retry with backoff on non-2xx (most providers retry up to N times over days).
- Make handlers **idempotent** (processing the same event twice is harmless).
- Log everything; webhook debugging is hard otherwise.

## When to use which

| Need                          | Use          |
|-------------------------------|--------------|
| Receive immediate updates      | Webhooks     |
| Simple client, no server       | Polling      |
| Need guaranteed delivery      | Webhooks + queue |
| Data that changes rarely      | Polling      |
