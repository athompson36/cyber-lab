# Lab Inventory — SBCs, Controllers, Sensors, Accessories & Components

Catalog of hardware on hand: boards, sensors, accessories, and electrical components with **specs and datasheet links** (or local PDFs in `datasheets/`).

---

## Purpose

- **Single source of truth** for what you own: part numbers, specs, quantities, locations.
- **Datasheets** — link URLs or store PDFs under `datasheets/` for offline use.
- **Traceability** — link items to lab devices (`devices/`) or projects (`current_project.md`) via `used_in` and `tags`.

---

## Quick start

1. **Browse or edit** the YAML files under `items/` (one file per category).
2. **Schema:** See [SCHEMA.md](SCHEMA.md) for field reference and suggested `specs` keys.
3. **Add items:** Copy an existing entry, set `id`, `name`, `specs`, `datasheet_url` (or `datasheet_file`).
4. **Optional:** Run `scripts/build_db.py` to generate `inventory.db` (SQLite) for querying.

---

## Categories

| File | Contents |
|------|----------|
| [items/sbcs.yaml](items/sbcs.yaml) | Single-board computers (Raspberry Pi, Pine64, etc.) |
| [items/controllers.yaml](items/controllers.yaml) | MCU boards (ESP32, Arduino, Teensy, T-Beam) |
| [items/sensors.yaml](items/sensors.yaml) | Sensors and sensor modules |
| [items/accessories.yaml](items/accessories.yaml) | Antennas, cases, cables, expansion boards, displays |
| [items/components.yaml](items/components.yaml) | Discrete parts and ICs |

---

## Datasheets

- **URLs:** Store in `datasheet_url` per item (preferred for single source of truth).
- **Local PDFs:** Put files in `datasheets/` and set `datasheet_file` (e.g. `datasheets/bme280.pdf`). Add large PDFs to `.gitignore` if you don’t want them in git.

---

## Web app (AI-backed management UI)

A Flask web app provides search, category filter, **AI natural-language query**, firmware **update checks**, and item details. See **[app/README.md](app/README.md)** for run instructions.

**Local:** From repo root, after building the DB:
```bash
pip install -r inventory/app/requirements.txt
python inventory/app/app.py
# Open http://127.0.0.1:5050
```

**Docker:** From repo root (build DB first: `python inventory/scripts/build_db.py`):
```bash
docker compose -f inventory/app/docker-compose.yml up --build
# Open http://127.0.0.1:5050
```

---

## Database (optional)

From the repo root:

```bash
# Option A: use a venv (recommended on macOS with system Python)
python3 -m venv .venv && source .venv/bin/activate
pip install pyyaml
python inventory/scripts/build_db.py

# Option B: if PyYAML is already installed for your Python
python3 inventory/scripts/build_db.py
```

Creates `inventory/inventory.db` (SQLite) with one table `items` and all fields. You can query with `sqlite3 inventory/inventory.db` or any SQL tool.

---

## Relation to the rest of the lab

- **devices/** — Target *types* for firmware (pinmaps, configs, firmware repos). Inventory can list *instances* of those boards and link via `used_in` (e.g. `t_beam_1w`).
- **current_project.md** — Project ideas; inventory `used_in` can reference project shorthand (e.g. `digital_mixer`, `lora_mesh`).
