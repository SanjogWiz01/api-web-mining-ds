"""
🚀 API Calling — Master Runner
================================
Runs all 10 API concept demonstrations in sequence.
Each module covers one fundamental API concept.

Topics covered:
  01  HTTP Basics        — GET, POST, PUT, DELETE
  02  Authentication     — API Keys, Bearer Tokens, OAuth
  03  Endpoints          — Base URL, Paths, Query Params
  04  Request Headers    — Content-Type, Authorization
  05  Error Handling     — Status codes, raise_for_status, exceptions
  06  Rate Limits        — Backoff, throttling, header inspection
  07  Data Format        — JSON encoding, decoding, validation
  08  Security           — .env, HTTPS, safe logging
  09  Documentation      — Reading API docs, schema validation
  10  Testing Tools      — curl commands, automated test suite, Postman

Usage:
  python main.py           → Run all topics
  python main.py 1         → Run only topic 1
  python main.py 5 7 10    → Run topics 5, 7, and 10
"""

import sys
import importlib
import traceback


MODULES = {
    1:  ("01_http_basics",      "HTTP Basics: GET, POST, PUT, DELETE"),
    2:  ("02_authentication",   "Authentication: API Keys, Tokens, OAuth"),
    3:  ("03_endpoints",        "Endpoints: Base URL, Paths, Params"),
    4:  ("04_request_headers",  "Request Headers: Content-Type, Authorization"),
    5:  ("05_error_handling",   "Error Handling: Status Codes & Exceptions"),
    6:  ("06_rate_limits",      "Rate Limits: Backoff & Throttling"),
    7:  ("07_data_format_json", "Data Format: JSON Parsing & Validation"),
    8:  ("08_security",         "Security: Keys, HTTPS, .env Pattern"),
    9:  ("09_documentation",    "Documentation: Reading & Using API Docs"),
    10: ("10_testing_tools",    "Testing Tools: curl, Postman, Auto Tests"),
}


def separator(topic_num: int, title: str):
    print("\n")
    print("━" * 60)
    print(f"  📘 TOPIC {topic_num:>2} │ {title}")
    print("━" * 60)


def run_topic(topic_num: int):
    if topic_num not in MODULES:
        print(f"  [ERROR] Topic {topic_num} not found. Choose 1-10.")
        return

    module_name, title = MODULES[topic_num]
    separator(topic_num, title)

    try:
        mod = importlib.import_module(module_name)
        # Each module has a main block — re-run its primary demo function
        # by importing and calling based on module naming conventions
        func_map = {
            1:  getattr(mod, "demo_get", None),
            2:  getattr(mod, "api_key_in_header", None),
            3:  getattr(mod, "demonstrate_endpoints", None),
            4:  getattr(mod, "show_request_headers", None),
            5:  getattr(mod, "demo_error_handling", None),
            6:  getattr(mod, "demo_rate_limits", None),
            7:  getattr(mod, "parse_and_validate", None),
            8:  getattr(mod, "security_checklist", None),
            9:  getattr(mod, "print_api_reference", None),
            10: getattr(mod, "run_api_test_suite", None),
        }
        fn = func_map.get(topic_num)
        if fn:
            fn()
        else:
            print(f"  Module loaded: {module_name}")
    except Exception as e:
        print(f"  [ERROR] Failed to run topic {topic_num}: {e}")
        traceback.print_exc()


def main():
    print("=" * 60)
    print("   API CALLING — 10 FUNDAMENTAL CONCEPTS")
    print("   Using: requests | jsonplaceholder.typicode.com")
    print("=" * 60)

    if len(sys.argv) > 1:
        topics = []
        for arg in sys.argv[1:]:
            try:
                topics.append(int(arg))
            except ValueError:
                print(f"  Invalid topic number: {arg}")
    else:
        topics = list(MODULES.keys())  # Run all

    for topic in topics:
        run_topic(topic)

    print("\n")
    print("=" * 60)
    print("  All selected topics complete!")
    print("  Run individual files: python 01_http_basics.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
