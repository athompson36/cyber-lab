#!/usr/bin/env python3
"""
Build SQLite inventory database from YAML catalog files.

Usage (from repo root):
  python inventory/scripts/build_db.py

Requires: PyYAML (pip install pyyaml)

Creates inventory/inventory.db with table 'items' and columns matching SCHEMA.md.
"""

import json
import os
import sqlite3
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INVENTORY_DIR = os.path.join(REPO_ROOT, "inventory")
ITEMS_DIR = os.path.join(INVENTORY_DIR, "items")
DB_PATH = os.path.join(INVENTORY_DIR, "inventory.db")

CATEGORY_FILES = [
    ("sbc", "sbcs.yaml"),
    ("controller", "controllers.yaml"),
    ("sensor", "sensors.yaml"),
    ("accessory", "accessories.yaml"),
    ("component", "components.yaml"),
]


def load_all_items():
    items = []
    for category, filename in CATEGORY_FILES:
        path = os.path.join(ITEMS_DIR, filename)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for it in data.get("items", []):
            it["category"] = category
            items.append(it)
    return items


def row_from_item(it):
    return (
        it.get("id", ""),
        it.get("name", ""),
        it.get("category", ""),
        it.get("manufacturer") or "",
        it.get("part_number") or "",
        it.get("model") or "",
        it.get("quantity") if it.get("quantity") is not None else 1,
        it.get("location") or "",
        json.dumps(it.get("specs") or {}, ensure_ascii=False),
        it.get("datasheet_url") or "",
        it.get("datasheet_file") or "",
        it.get("notes") or "",
        json.dumps(it.get("used_in") or [], ensure_ascii=False),
        json.dumps(it.get("tags") or [], ensure_ascii=False),
    )


def main():
    os.makedirs(INVENTORY_DIR, exist_ok=True)
    items = load_all_items()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            manufacturer TEXT,
            part_number TEXT,
            model TEXT,
            quantity INTEGER DEFAULT 1,
            location TEXT,
            specs TEXT,
            datasheet_url TEXT,
            datasheet_file TEXT,
            notes TEXT,
            used_in TEXT,
            tags TEXT
        )
    """)
    conn.execute("DELETE FROM items")
    conn.executemany(
        """
        INSERT INTO items (
            id, name, category, manufacturer, part_number, model,
            quantity, location, specs, datasheet_url, datasheet_file,
            notes, used_in, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [row_from_item(it) for it in items],
    )
    conn.commit()
    conn.close()
    print(f"Wrote {len(items)} items to {DB_PATH}")


if __name__ == "__main__":
    main()
