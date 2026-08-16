"""
📘 TOPIC 16: Webhooks — Server-to-Server Events
==============================================
A webhook is an API endpoint the API SERVER calls when an event happens.
Instead of polling, you register a callback URL and receive a POST.

Key practices:
  - Validate the payload signature (HMAC)
  - Respond quickly with 200 so the sender stops retrying
  - Make your handler idempotent (deduplicate by event id)
"""

import requests
import hmac
import hashlib
import json

WEBHOOK_SECRET = "super-secret-shared-key"


# ─────────────────────────────────────────────
# 1. Simulate receiving a webhook (server side)
# ─────────────────────────────────────────────
def handle_webhook_payload(payload: dict, signature: str) -> bool:
    """Verify HMAC signature then process the payload."""
    msg = json.dumps(payload, separators=(",", ":")).encode()
    expected = hmac.new(WEBHOOK_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    valid = hmac.compare_digest(expected, signature)
    if valid:
        print(f"  ✓ Signature valid — processing event '{payload.get('event')}'")
    else:
        print("  ✗ Signature INVALID — reject payload")
    return valid


def simulate_incoming_webhook():
    print("\n── Incoming Webhook ─────────────────")
    payload = {"event": "user.created", "id": "evt_123", "user_id": 42}
    msg = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(WEBHOOK_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    handle_webhook_payload(payload, signature)

    # tampered payload must fail
    tampered = {"event": "user.created", "id": "evt_123", "user_id": 999}
    handle_webhook_payload(tampered, signature)


# ─────────────────────────────────────────────
# 2. Register a webhook URL (client side)
# ─────────────────────────────────────────────
def register_webhook():
    print("\n── Register Webhook URL ─────────────")
    # Real APIs: POST /webhooks {"url": "...", "events": [...]}
    r = requests.post(
        "https://httpbin.org/post",
        json={"url": "https://myapp.example.com/hooks/stripe", "events": ["payment.succeeded"]},
    )
    data = r.json()
    print(f"  Status: {r.status_code}")
    print(f"  Registered URL: {data.get('json', {}).get('url')}")


# ─────────────────────────────────────────────
# 3. Polling vs webhooks comparison
# ─────────────────────────────────────────────
def polling_vs_webhooks():
    print("\n── Polling vs Webhooks ──────────────")
    comparison = [
        ("Polling", "Client asks 'anything new?' every N seconds"),
        ("         ", "Simple but wasteful and adds latency"),
        ("Webhooks", "Server pushes the event instantly"),
        ("         ", "Efficient but needs a public endpoint + security"),
    ]
    for label, text in comparison:
        print(f"  {label:<9} {text}")


if __name__ == "__main__":
    print("=" * 55)
    print("  WEBHOOKS: server-to-server events")
    print("=" * 55)
    simulate_incoming_webhook()
    register_webhook()
    polling_vs_webhooks()
    print("\nWebhook demos complete.")