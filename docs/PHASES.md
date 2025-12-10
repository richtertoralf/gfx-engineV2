"""# Multisport GFX-Engine V2 – Projektchronik (bisher umgesetzte Phasen)

Dieses Dokument beschreibt **ausschließlich die Phasen, die bereits vollständig oder teilweise umgesetzt wurden**.  
Es dient als technische Nachvollziehbarkeit für Entwickler.

---

# PHASE 0 — REPO & SKELETT

**Ziel:** Projektstruktur anlegen, Repository initialisieren.

## Ergebnisse
- `/opt/gfx-engine` erstellt  
- Git-Repository initialisiert  
- Basisstruktur angelegt:
```text
input/ kes/ hora/ winlaufen/
core/ config.py redis.py model/
api/ main.py state/ start/ startlist/ biathlon/ event/
dashboard/ control.html control.js modules/
renderer/ index.html update.js modules/
static/ css/ js/
tools/ reset_redis.py
docs/ README.md PHASES.md
```

- `.gitignore` erstellt  
- Dummy-Dateien eingefügt  
- Phase 0 abgeschlossen

---

# PHASE 1 — REDIS + CORE-BASIS

**Ziel:** Redis-Anbindung und zentrale Core-Funktionen schaffen.

## Ergebnisse
- Redis installiert und aktiviert  
- Python venv eingerichtet  
- `core/config.py` (alte Version) mit statischen Variablen  
- `core/redis.py` erstellt mit:
  - `get_json`
  - `set_json`
  - `delete_pattern`
  - `exists`
- Reset-Tool: `tools/reset_redis.py`
- Funktionstests erfolgreich
- Phase 1 abgeschlossen

---

# PHASE 2 — API BASIS

**Ziel:** FastAPI-Grundgerüst + Router einbinden.

## Ergebnisse
- FastAPI & Uvicorn installiert  
- `api/main.py` erstellt  
- Router eingebunden:
  - `/state`
  - `/start`
  - `/startlist`
  - `/biathlon`
- Ping- und State-Endpunkte funktionieren  
- Manuelle API-Tests erfolgreich  
- Phase 2 abgeschlossen

---

# PHASE 3 — SYSTEMD + EVENT-ROUTER

**Ziel:** API dauerhaft betreiben, Logging & Event-System.

## Ergebnisse
- systemd-Service eingerichtet (Port 8000 → später geändert)  
- Logging in `core/logging.py` implementiert  
- Event-Router `/event/trigger` erstellt  
- Dashboard & Renderer können später Events nutzen  
- Phase 3 abgeschlossen

---

# PHASE 4 — Portwechsel, zentrale YAML-Config & Core-Refactor

**Ziel:** Engine modular, konfigurierbar und portkonfliktfrei machen.

## 4.1 Portwechsel 8000 → 8720
- Grund: MediaMTX nutzt 8000/8001 (RTP/RTCP)
- Neuer Port jetzt überall aktiv

## 4.2 Neue zentrale YAML-Konfigurationsdatei
Erstellt: `/opt/gfx-engine/config/gfx-engine.yaml`

Enthält:
- Server-Einstellungen  
- Redis  
- Pfade  
- Feature-Flags  

## 4.3 Neuer Config-Loader (core/config.py)
- Lädt YAML  
- Erzeugt Dataclasses: SERVER, REDIS, PATHS, LOGGING, FEATURES  
- Definiert globale Variablen wie API_PORT, REDIS_URL  
- Entfernt alte Hardcoded-Version vollständig

## 4.4 Fehlerbehebungen
- PyYAML installiert + in requirements ergänzt  
- Importfehler in core/redis.py behoben  
- systemd-Probleme durch fehlende YAML-Abhängigkeit korrigiert  

## 4.5 systemd aktualisiert
- Port auf 8720 geändert  
- Logging-Ordner `/var/log/gfx-engine` eingerichtet  

## 4.6 Optionaler Systemnutzer (noch nicht umgesetzt)
- Planung dokumentiert, aber noch nicht aktiv

Phase 4 abgeschlossen.

---

# STATUS ÜBERSICHT

| Phase | Zustand | Kurzbeschreibung |
|-------|---------|------------------|
| 0 | ✔️ abgeschlossen | Repo + Struktur |
| 1 | ✔️ abgeschlossen | Redis + Core |
| 2 | ✔️ abgeschlossen | Minimal-API |
| 3 | ✔️ abgeschlossen | systemd + Events |
| 4 | ✔️ abgeschlossen | YAML config + Portwechsel |
| 5 | ⏳ offen | Dashboard Modularisierung |
| 6 | ⏳ offen | Renderer WebSocket |
| 7 | ⏳ offen | Parser WinLaufen / HoRa / KES |

---

**Letzte Aktualisierung: 10.12.2025**

"""

