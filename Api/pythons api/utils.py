import hashlib
import json


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def to_json(data: dict) -> str:
    return json.dumps(data, indent=2, default=str)
