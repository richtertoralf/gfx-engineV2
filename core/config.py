"""
core.config
-----------
Globale Konfiguration der Multisport GFX Engine V2.
"""

from dataclasses import dataclass


@dataclass
class Settings:
    REDIS_URL: str = "redis://localhost:6379/0"
    NAMESPACE: str = "gfx:"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True


settings = Settings()

