"""
core.redis
----------
Abstraktion für Redis-Zugriffe in der GFX Engine V2.

Zentrale Funktionen:
- get_json(key)
- set_json(key, data)
- delete_pattern(pattern)
- exists(key)
"""

import json
import redis
from .config import settings


# ---------------------------------------------
# Redis-Client – Singleton
# ---------------------------------------------
def _get_client():
    return redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True  # damit Strings automatisch UTF-8 sind
    )


client = _get_client()


# ---------------------------------------------
# JSON holen
# ---------------------------------------------
def get_json(key: str):
    key = settings.NAMESPACE + key
    raw = client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


# ---------------------------------------------
# JSON setzen
# ---------------------------------------------
def set_json(key: str, data):
    key = settings.NAMESPACE + key
    client.set(key, json.dumps(data))


# ---------------------------------------------
# Key existiert?
# ---------------------------------------------
def exists(key: str) -> bool:
    key = settings.NAMESPACE + key
    return client.exists(key) == 1


# ---------------------------------------------
# Keys nach Pattern löschen
# ---------------------------------------------
def delete_pattern(pattern: str):
    pattern = settings.NAMESPACE + pattern
    keys = client.keys(pattern)
    for k in keys:
        client.delete(k)
    return len(keys)


