"""
core.config
-----------
Modulare zentrale Konfiguration der Multisport GFX Engine V2.

- Lädt config/gfx-engine.yaml
- Stellt klar getrennte Bereiche bereit:
  SERVER, REDIS, PATHS, LOGGING, FEATURES
- Features sind gruppiert in: core / sports / imports
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field

CONFIG_PATH = Path("/opt/gfx-engine/config/gfx-engine.yaml")


def load_yaml():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file missing: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


raw = load_yaml()


# ============================================================
# Dataclasses
# ============================================================

@dataclass
class ServerConfig:
    host: str
    port: int
    debug: bool


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    namespace: str

    @property
    def url(self):
        return f"redis://{self.host}:{self.port}/{self.db}"


@dataclass
class PathsConfig:
    dashboard: str
    renderer: str
    static: str


@dataclass
class LoggingConfig:
    level: str


@dataclass
class FeatureTree:
    core: dict = field(default_factory=dict)
    sports: dict = field(default_factory=dict)
    imports: dict = field(default_factory=dict)

    def enabled(self, group: str, feature: str) -> bool:
        """General: FEATURES.enabled('sports', 'biathlon')"""
        return self.__dict__.get(group, {}).get(feature, False)


# ============================================================
# Instanzen
# ============================================================

SERVER = ServerConfig(**raw["server"])
REDIS = RedisConfig(**raw["redis"])
PATHS = PathsConfig(**raw["paths"])
LOGGING = LoggingConfig(**raw["logging"])
FEATURES = FeatureTree(**raw["features"])


# ============================================================
# Debug-Ausgabe (falls aktiviert)
# ============================================================

if SERVER.debug:
    print(f"[CONFIG] Server läuft auf {SERVER.host}:{SERVER.port}")
    print(f"[CONFIG] Redis: {REDIS.url}")
    print(f"[CONFIG] Websocket: {FEATURES.enabled('core', 'websocket_updates')}")
    print(f"[CONFIG] Biathlon aktiviert: {FEATURES.enabled('sports', 'biathlon')}")
