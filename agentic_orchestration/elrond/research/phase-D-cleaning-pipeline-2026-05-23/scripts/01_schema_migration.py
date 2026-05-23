#!/usr/bin/env python3
"""
Phase D Step 0: Schema migration runner — idempotent.

Adds 9 new columns to `weapon_knowledge_entries` + 3 new views.
Skips columns/views that already exist (PRAGMA-guarded + sqlite_master-guarded).

Outputs:
  - logs/01_schema_migration.json — structured summary (Discipline #19 emerging pattern)

Authority: Matt 2026-05-23 whole-pipeline upfront authorization.
Math note: §1 (schema migration plan).
Backup: pre-fired by 00_backup.sh before this script runs.
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "01_schema_migration.json"

# ---------------------------------------------------------------------------
# 9 column definitions per math note §1.2
# ---------------------------------------------------------------------------

COLUMN_DEFS = [
    (
        "wieldable_humanoid",
        "TEXT DEFAULT 'unknown' CHECK (wieldable_humanoid IN "
        "('one_hand','two_hand','shoulder_supported','either','no','mount_required','unknown'))",
    ),
    (
        "weapon_kind",
        "TEXT DEFAULT 'unknown' CHECK (weapon_kind IN "
        "('category','unique','named_template','ammo_or_consumable','unknown'))",
    ),
    (
        "dedup_status",
        "TEXT DEFAULT 'unprocessed' CHECK (dedup_status IN "
        "('canonical','merged_into','unprocessed'))",
    ),
    (
        "variant_relationship",
        "TEXT DEFAULT 'independent'",
    ),
    (
        "cultural_lineage_canonical",
        "TEXT DEFAULT 'unknown' CHECK (cultural_lineage_canonical IN "
        "('european','east_asian','south_asian','southeast_asian','middle_eastern',"
        "'african','north_american_indigenous','mesoamerican','south_american_indigenous',"
        "'arctic_circumpolar','oceanic','fantasy_generic','sci_fi_generic',"
        "'cross_cultural','unknown'))",
    ),
    (
        "historical_period_canonical",
        "TEXT DEFAULT 'unknown' CHECK (historical_period_canonical IN "
        "('pre_classical','classical','medieval','early_modern','industrial',"
        "'modern','contemporary','fictional','unknown'))",
    ),
    (
        "register_canonical",
        "TEXT DEFAULT 'unknown' CHECK (register_canonical IN "
        "('historical','military_modern','fantasy','sci_fi','mythological','unknown'))",
    ),
    (
        "cultural_lineage_confidence",
        "REAL DEFAULT 0.0 CHECK (cultural_lineage_confidence >= 0.0 "
        "AND cultural_lineage_confidence <= 1.0)",
    ),
    (
        "template_quality_score",
        "REAL DEFAULT 0.0 CHECK (template_quality_score >= 0.0 "
        "AND template_quality_score <= 1.0)",
    ),
]

# ---------------------------------------------------------------------------
# 3 view definitions per math note §1.3
# ---------------------------------------------------------------------------

VIEW_DEFS = [
    (
        "v_category_sample",
        """CREATE VIEW v_category_sample AS
        SELECT * FROM weapon_knowledge_entries
        WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')
          AND weapon_kind IN ('category','named_template')
          AND dedup_status IN ('canonical','unprocessed')
          AND source_library NOT IN (
            'wikipedia-unfiltered',
            'pf2ools-pf2ools-data-quarantined',
            'souls-api-thomaslincoln-quarantined'
          )""",
    ),
    (
        "v_category_sample_humanoid_strict",
        """CREATE VIEW v_category_sample_humanoid_strict AS
        SELECT * FROM v_category_sample
        WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported')""",
    ),
    (
        "v_category_sample_humanoid_permissive",
        """CREATE VIEW v_category_sample_humanoid_permissive AS
        SELECT * FROM v_category_sample
        WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either','mount_required')""",
    ),
]


def existing_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def existing_views(conn: sqlite3.Connection) -> set[str]:
    return {
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='view'"
        ).fetchall()
    }


def add_column_if_absent(
    conn: sqlite3.Connection, table: str, col_name: str, col_def: str
) -> dict:
    cols = existing_columns(conn, table)
    if col_name in cols:
        return {"column": col_name, "action": "SKIP_EXISTS"}
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}")
    return {"column": col_name, "action": "ADDED"}


def create_view_if_absent(
    conn: sqlite3.Connection, view_name: str, view_sql: str
) -> dict:
    views = existing_views(conn)
    if view_name in views:
        return {"view": view_name, "action": "SKIP_EXISTS"}
    conn.execute(view_sql)
    return {"view": view_name, "action": "CREATED"}


def smoke_test(conn: sqlite3.Connection) -> dict:
    """Per math note §1.4 smoke test."""
    info = conn.execute(
        "PRAGMA table_info(weapon_knowledge_entries)"
    ).fetchall()
    column_count = len(info)
    column_names = [r[1] for r in info]

    views = sorted(existing_views(conn))
    target_views = [
        "v_category_sample",
        "v_category_sample_humanoid_strict",
        "v_category_sample_humanoid_permissive",
    ]
    missing_views = [v for v in target_views if v not in views]

    null_weapon_kind = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE weapon_kind IS NULL"
    ).fetchone()[0]

    v_category_sample_count = conn.execute(
        "SELECT COUNT(*) FROM v_category_sample"
    ).fetchone()[0]

    total_rows = conn.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries"
    ).fetchone()[0]

    return {
        "column_count": column_count,
        "column_count_expected": 26,  # 17 original + 9 new
        "column_count_ok": column_count == 26,
        "column_names": column_names,
        "target_views_present": missing_views == [],
        "all_views": views,
        "weapon_kind_null_count": null_weapon_kind,
        "weapon_kind_null_ok": null_weapon_kind == 0,
        "v_category_sample_count": v_category_sample_count,
        "v_category_sample_count_pre_classification_ok": v_category_sample_count == 0,
        "total_rows": total_rows,
        "total_rows_expected": 89839,
        "total_rows_ok": total_rows == 89839,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()

    summary: dict = {
        "script": "01_schema_migration.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "column_ops": [],
        "view_ops": [],
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")

        # Columns
        for col_name, col_def in COLUMN_DEFS:
            try:
                result = add_column_if_absent(
                    conn, "weapon_knowledge_entries", col_name, col_def
                )
            except sqlite3.OperationalError as e:
                result = {"column": col_name, "action": "ERROR", "error": str(e)}
            summary["column_ops"].append(result)
            print(f"  [column] {result}")

        conn.commit()

        # Views
        for view_name, view_sql in VIEW_DEFS:
            try:
                result = create_view_if_absent(conn, view_name, view_sql)
            except sqlite3.OperationalError as e:
                result = {"view": view_name, "action": "ERROR", "error": str(e)}
            summary["view_ops"].append(result)
            print(f"  [view] {result}")

        conn.commit()

        # Smoke test
        summary["smoke_test"] = smoke_test(conn)
        print(f"  [smoke] {json.dumps(summary['smoke_test'], indent=2)}")

    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Overall pass/fail
    smoke = summary["smoke_test"]
    summary["passed"] = (
        smoke["column_count_ok"]
        and smoke["target_views_present"]
        and smoke["weapon_kind_null_ok"]
        and smoke["v_category_sample_count_pre_classification_ok"]
        and smoke["total_rows_ok"]
        and all(op.get("action") in ("ADDED", "SKIP_EXISTS") for op in summary["column_ops"])
        and all(op.get("action") in ("CREATED", "SKIP_EXISTS") for op in summary["view_ops"])
    )

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n  ==> PASSED: {summary['passed']}")
    print(f"  ==> Summary written to {LOG_PATH}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
