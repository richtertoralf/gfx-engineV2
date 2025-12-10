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
from .config import REDIS  # neue V2-Konfiguration


# -------------------------------------------------------
# Redis-Client – Singleton / Lazy Initialization
# -------------------------------------------------------
_redis_client = None


def _get_client():
    """Erzeugt den Redis-Client nur einmal (Lazy Loading)."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=REDIS.host,
            port=REDIS.port,
            db=REDIS.db,
            decode_responses=True
        )
    return _redis_client


# -------------------------------------------------------
# Namespacing
# -------------------------------------------------------
def _ns(key: str) -> str:
    """Fügt automatisch das Namespace-Präfix hinzu."""
    return f"{REDIS.namespace}{key}"


# -------------------------------------------------------
# JSON lesen
# -------------------------------------------------------
def get_json(key: str):
    """Liest JSON-Daten aus Redis und wandelt sie in Python-Objekte um."""
    raw = _get_client().get(_ns(key))
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


# -------------------------------------------------------
# JSON schreiben
# -------------------------------------------------------
def set_json(key: str, data):
    """Speichert Python-Objekte als JSON in Redis."""
    raw = json.dumps(data)
    return _get_client().set(_ns(key), raw)


# -------------------------------------------------------
# Key existiert?
# -------------------------------------------------------
def exists(key: str) -> bool:
    return _get_client().exists(_ns(key)) > 0


# -------------------------------------------------------
# Keys nach Pattern löschen
# -------------------------------------------------------
def delete_pattern(pattern: str):
    """
    Löscht alle Keys, die auf das Pattern passen.
    Beispiel: delete_pattern("startlist:*")
    """
    client = _get_client()
    full_pattern = _ns(pattern)
    keys = client.keys(full_pattern)
    if keys:
        client.delete(*keys)
    return len(keys)
