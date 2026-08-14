"""
📘 TOPIC 8: Security — Never Expose API Keys
=============================================
API key security is critical. Leaking credentials can lead to:
  - Unauthorized usage charges
  - Data breaches
  - Account suspension

Best practices covered here:
  1. Use environment variables (os.environ)
  2. Use .env files with python-dotenv (never commit .env to git)
  3. Validate HTTPS (TLS)
  4. Avoid logging sensitive headers
  5. Rotate keys regularly
"""

import os
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Load Key from Environment Variable
# ─────────────────────────────────────────────
def load_key_from_env():
    print("\n── Load API Key from Environment ────")
    # Set in terminal: $env:MY_API_KEY = "your_actual_key"
    # Or in a .env file loaded by python-dotenv
    api_key = os.environ.get("MY_API_KEY", "NOT_SET")

    if api_key == "NOT_SET":
        print("  WARNING: MY_API_KEY not set in environment variables")
        print("  Set it with: $env:MY_API_KEY = 'your_key' (PowerShell)")
        print("           or: export MY_API_KEY='your_key' (Bash)")
    else:
        masked = api_key[:4] + "*" * (len(api_key) - 4)
        print(f"  API Key loaded: {masked} (masked for safety)")

    return api_key


# ─────────────────────────────────────────────
# 2. .env File Pattern (dotenv)
# ─────────────────────────────────────────────
def dotenv_pattern():
    print("\n── .env File Pattern ────────────────")
    env_file_content = """# .env (ADD THIS FILE TO .gitignore!)
MY_API_KEY=your_actual_api_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_TOKEN=super_secret_jwt_signing_key
"""
    gitignore_entry = ".env\n.env.local\n*.key\nsecrets/\n"

    print("  1. Create a .env file in your project root:")
    for line in env_file_content.strip().split("\n"):
        print(f"     {line}")
    print("\n  2. Add to .gitignore:")
    for line in gitignore_entry.strip().split("\n"):
        print(f"     {line}")
    print("\n  3. In Python:")
    print("     from dotenv import load_dotenv")
    print("     load_dotenv()")
    print("     key = os.environ.get('MY_API_KEY')")


# ─────────────────────────────────────────────
# 3. Always Use HTTPS
# ─────────────────────────────────────────────
def https_verification():
    print("\n── HTTPS / TLS Verification ─────────")
    url_https = "https://jsonplaceholder.typicode.com/posts/1"

    # Default: verify=True (recommended — validates SSL certificate)
    r = requests.get(url_https, verify=True)
    print(f"  HTTPS request: {r.status_code} | SSL verified: True")

    # Never do this in production:
    # requests.get(url, verify=False)  # Disables SSL — INSECURE!
    print("  NEVER use verify=False in production — exposes to MITM attacks")


# ─────────────────────────────────────────────
# 4. Safe Logging (mask sensitive headers)
# ─────────────────────────────────────────────
def safe_logging_pattern():
    print("\n── Safe Logging Pattern ─────────────")
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.FAKE",
        "X-API-Key": "sk-prod-xyz-1234567890",
        "Content-Type": "application/json",
    }
    SENSITIVE_KEYS = {"Authorization", "X-API-Key", "Cookie", "Set-Cookie"}

    print("  Headers as logged (sensitive fields masked):")
    for key, value in headers.items():
        if key in SENSITIVE_KEYS:
            masked = value[:10] + "***REDACTED***"
            print(f"    {key}: {masked}")
        else:
            print(f"    {key}: {value}")


# ─────────────────────────────────────────────
# 5. Security Checklist
# ─────────────────────────────────────────────
def security_checklist():
    print("\n── API Security Checklist ───────────")
    checklist = [
        ("PASS", "Use environment variables for all secrets"),
        ("PASS", "Add .env to .gitignore"),
        ("PASS", "Always use HTTPS (TLS) for all API calls"),
        ("PASS", "Mask sensitive data in logs"),
        ("PASS", "Rotate API keys periodically"),
        ("PASS", "Use least-privilege API scopes"),
        ("FAIL", "Hardcode API keys in source code"),
        ("FAIL", "Commit secrets to version control"),
        ("FAIL", "Use HTTP (not HTTPS) for production"),
        ("FAIL", "Log raw Authorization headers"),
    ]
    for status, item in checklist:
        icon = "[OK]" if status == "PASS" else "[X]"
        print(f"  {icon} {item}")


if __name__ == "__main__":
    print("=" * 55)
    print("  SECURITY: Keys, HTTPS, .env, Safe Logging")
    print("=" * 55)
    load_key_from_env()
    dotenv_pattern()
    https_verification()
    safe_logging_pattern()
    security_checklist()
    print("\nSecurity demos complete.")
