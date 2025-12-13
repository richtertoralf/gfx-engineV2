## Architektur – Kurzfassung (gfx-engineV2)

Die **Multisport GFX Engine V2** ist ein modulares Grafik- und Steuerungssystem für
Live-Sportproduktionen (Biathlon, Skispringen, Langlauf, MTB u. a.).

Das System trennt **Bedienung**, **Logik**, **Datenhaltung** und **Rendering** strikt
voneinander und ist auf Stabilität, Nachvollziehbarkeit und einfache Erweiterung ausgelegt.

---

### Architekturprinzipien

- **Single Source of Truth:**  
  Der komplette Live-Zustand liegt zentral in **Redis**.

- **Zustandslose Frontends:**  
  Dashboard und Renderer können jederzeit neu geladen werden.

- **Klare Schichten:**  
  Keine direkte Kommunikation zwischen UI und Renderer.

- **Multisportfähig:**  
  Gemeinsamer Kern, disziplinspezifische Erweiterungen.

---

### Systemübersicht

```text
Operator
│
▼
[ Dashboard ]
(HTML / CSS / JS)
│ REST / WebSocket
▼
[ API ]
(FastAPI)
│
▼
[ Redis ]
(Core Data Layer)
│
▼
[ Renderer ]
(OBS / Browser / Videowall)
```


---

### Schichten im Überblick

**Dashboard (Control Layer)**  
- Bedienoberfläche für Operatoren  
- Keine Logik, kein Redis-Zugriff  
- Sendet nur semantische Befehle (SHOW / HIDE / UPDATE)

**API (FastAPI)**  
- Validiert Befehle  
- Schreibt Zustandsänderungen nach Redis  
- Liefert Daten für Dashboard und Renderer

**Core Data Layer (Redis)**  
- Zentrale Datenhaltung  
- Einheitliche, lesbare Keys  
- Ermöglicht parallele Ausgaben

**Renderer**  
- Reines Rendering (keine Steuerlogik)  
- Läuft als OBS Browser Source, Videowall oder Monitor  
- Mehrere Renderer gleichzeitig möglich

---

### Datenmodell (Beispiele)

```text
event.title
overlay.start.visible
overlay.weather.temperature
athlete.current.bib
biathlon.lane.3.status
```

Alle Module lesen und schreiben ausschließlich über dieses Modell.

## Disziplinmodell

### Generischer Kern (immer aktiv):

Event Info

Start / Startliste

Wetter

Uhr / Timer

Name Caption

Branding

Texte / Schedule

Ergebnisse (generisch)

### Disziplinspezifisch (abhängig von event.discipline):

Biathlon: Schießbahnen, Strafen, KES und HoRa Parser

Skispringen: Weite, Wind, Gate

## Ausfallsicherheit

Reload von Dashboard oder Renderer → Zustand bleibt erhalten

API-Restart → Redis unverändert

Netzunterbrechungen → saubere Wiederaufnahme

Geeignet für Outdoor-Events, mobile Netze und temporäre Setups.

## Ziel

Ein einfaches, robustes und erweiterbares Grafiksystem,
optimiert für reale Live-Sportproduktionen – nicht für Overengineering.

