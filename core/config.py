"""
core.config
-----------
Globale Konfiguration der Multisport GFX Engine V2.
"""

from dataclasses import dataclass


@dataclass
class Settings:
    # Basis-Einstellung für Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Präfix für alle Keys, um Namespace sauber zu halten
    NAMESPACE: str = "gfx:"


settings = Settings()

