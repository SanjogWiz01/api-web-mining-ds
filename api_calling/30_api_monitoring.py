"""
📘 TOPIC 30: API Monitoring & Logging
====================================
You can't improve what you don't measure.
Track requests, latency, errors, and status codes.

Key metrics:
  request count, error rate, p50/p95 latency,
  status code distribution, rate-limit hits
"""

import requests
import time
import json
from collections import Counter

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Simple request logger with timing
# ─────────────────────────────────────────────
def timed_request(method: str, url: str, **kwargs):
    start = time.perf_counter()
    try:
        r = requests.request(method, url, timeout=10, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        entry = {
            "method": method,
            "url": url,
            "status": r.status_code,
            "ms": round(elapsed, 1),
            "bytes": len(r.content),
        }
        print(f"  [{entry['status']}] {method} {url.split('typicode.com')[-1]} "
              f"{entry['ms']:.0f}ms {entry['bytes']}B")
        return entry
    except requests.RequestException as e:
        print(f"  [ERR] {method} {url} → {type(e).__name__}")
        return {"method": method, "url": url, "status": None, "ms": 0, "bytes": 0, "error": str(e)}


def log_some_requests():
    print("\n── Timed Requests ───────────────────")
    entries = []
    for i in range(1, 6):
        entries.append(timed_request("GET", f"{BASE_URL}/posts/{i}"))
    return entries


# ─────────────────────────────────────────────
# 2. Aggregate metrics
# ─────────────────────────────────────────────
def aggregate_metrics(entries):
    print("\n── Aggregated Metrics ───────────────")
    statuses = Counter(e["status"] for e in entries)
    total_ms = sum(e["ms"] for e in entries)
    print(f"  Requests  : {len(entries)}")
    print(f"  Statuses  : {dict(statuses)}")
    print(f"  Total time: {total_ms:.0f}ms  Avg: {total_ms/len(entries):.1f}ms")


# ─────────────────────────────────────────────
# 3. Log to JSON file (rotate-friendly)
# ─────────────────────────────────────────────
def write_json_log(entries):
    print("\n── JSON Log Output ──────────────────")
    log_line = json.dumps({"timestamp": time.time(), "requests": entries})
    print(f"  Sample log: {log_line[:120]}...")
    print("  → Write each request as one JSON line to api.log")


# ─────────────────────────────────────────────
# 4. Alert thresholds
# ─────────────────────────────────────────────
def alerting():
    print("\n── Alert Thresholds ─────────────────")
    rules = [
        ("Error rate", "> 5% of requests in 5 min"),
        ("p95 latency", "> 1000ms"),
        ("429s", "> 10 in a minute"),
        ("5xx", "> 0 for 2 minutes"),
    ]
    for metric, threshold in rules:
        print(f"  • {metric:<12} alert when {threshold}")


if __name__ == "__main__":
    print("=" * 55)
    print("  MONITORING: measure & log API health")
    print("=" * 55)
    entries = log_some_requests()
    aggregate_metrics(entries)
    write_json_log(entries)
    alerting()
    print("\nMonitoring demos complete.")