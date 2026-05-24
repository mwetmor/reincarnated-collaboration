#!/usr/bin/env python3
"""
Cycle 10 Stage 1.5 schema migration — additive only.

Adds 8 new columns to weapon_knowledge_entries:
  - extracted_length_value REAL
  - extracted_length_unit TEXT
  - extracted_weight_value REAL
  - extracted_weight_unit TEXT
  - extracted_materials TEXT       (comma-separated, source phrasing preserved)
  - extracted_named_bearer TEXT    (source phrasing preserved; Discipline #11)
  - extracted_provenance_richness REAL [0.0, 1.0]
  - extracted_historical_use TEXT

Idempotent: skips columns that already exist (PRAGMA-guarded).

Authority: knight-rider Cycle 10 dispatch 2026-05-24 (Matt 2026-05-23 parent authorization).
Same additive-column pattern as Phase D MIGRATION.md.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "01_schema_migration.json"

COLUMN_DEFS = [
    ("extracted_length_value", "REAL"),
    ("extracted_length_unit", "TEXT"),
    ("extracted_weight_value", "REAL"),
    ("extracted_weight_unit", "TEXT"),
    ("extracted_materials", "TEXT"),
    ("extracted_named_bearer", "TEXT"),
    ("extracted_provenance_richness", "REAL"),
    ("extracted_historical_use", "TEXT"),
]


def existing_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def main() -> int:
    started = time.time()
    log = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "db_path": DB_PATH,
        "columns_added": [],
        "columns_skipped_already_exists": [],
        "errors": [],
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        before = existing_columns(conn, "weapon_knowledge_entries")
        for col, coltype in COLUMN_DEFS:
            if col in before:
                log["columns_skipped_already_exists"].append(col)
                continue
            try:
                conn.execute(
                    f"ALTER TABLE weapon_knowledge_entries ADD COLUMN {col} {coltype}"
                )
                log["columns_added"].append(col)
            except sqlite3.OperationalError as e:
                log["errors"].append({"column": col, "error": str(e)})
        conn.commit()
        after = existing_columns(conn, "weapon_knowledge_entries")
        log["total_columns_after"] = len(after)
    finally:
        conn.close()

    log["elapsed_sec"] = round(time.time() - started, 2)
    log["status"] = "ok" if not log["errors"] else "partial"
    LOG_PATH.write_text(json.dumps(log, indent=2))
    print(json.dumps(log, indent=2))
    return 0 if log["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
