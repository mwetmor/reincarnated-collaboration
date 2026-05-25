#!/usr/bin/env python3
"""
Cycle 10 Sidecar B — Step 1: schema extension (weapon_kind enum expansion).

Authority:
  - Dispatch § 3.1: extend weapon_kind enum to include 'shield', 'tome', 'banner',
    'focus', 'horn', 'talisman' (in addition to existing 'category', 'unique',
    'named_template', 'ammo_or_consumable', 'unknown').
  - Off-hand-items canonical doc § 1 (the 6 categories).
  - ADR-004 + Phase D + Phase 0a MIGRATION pattern precedent (additive change).

SQLite implementation note:
  SQLite does not support `ALTER TABLE DROP CONSTRAINT`. We use the
  PRAGMA writable_schema pattern to surgically edit the CHECK clause in
  sqlite_master, then PRAGMA integrity_check verifies. This is the
  recommended pattern per SQLite docs for column-level CHECK constraint
  modification on a pre-existing table.

Idempotency:
  Script is idempotent. If the CHECK already contains 'shield', exits noop.

Run from anywhere:
  python3 scripts/01_schema_extension.py
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")

OLD_CHECK = "weapon_kind TEXT DEFAULT 'unknown' CHECK (weapon_kind IN ('category','unique','named_template','ammo_or_consumable','unknown'))"
NEW_CHECK = "weapon_kind TEXT DEFAULT 'unknown' CHECK (weapon_kind IN ('category','unique','named_template','ammo_or_consumable','shield','tome','banner','focus','horn','talisman','unknown'))"

NEW_VALUES = ("shield", "tome", "banner", "focus", "horn", "talisman")


def main() -> int:
    if not DB_PATH.exists():
        print(f"FATAL: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Fetch current schema text from sqlite_master
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='weapon_knowledge_entries'")
    row = cur.fetchone()
    if row is None:
        print("FATAL: weapon_knowledge_entries table not found", file=sys.stderr)
        return 1
    current_sql = row[0]

    # Idempotency check
    if all(f"'{v}'" in current_sql for v in NEW_VALUES):
        # All new enum values already present in CHECK clause
        print("[idempotent] weapon_kind CHECK already includes off-hand values; no-op")
        conn.close()
        return 0

    if OLD_CHECK not in current_sql:
        # Surface a clear failure if the old CHECK string we expected isn't present.
        # This indicates a schema drift from expected baseline (Phase 0a + Stage 1.5 + Stage 3 state).
        print("FATAL: expected old CHECK clause not found verbatim. Aborting to avoid bad edit.", file=sys.stderr)
        print(f"  expected substring: {OLD_CHECK[:120]}...", file=sys.stderr)
        print("  inspect current schema with: sqlite3 telemetry.db \".schema weapon_knowledge_entries\"", file=sys.stderr)
        conn.close()
        return 2

    new_sql = current_sql.replace(OLD_CHECK, NEW_CHECK)
    if new_sql == current_sql:
        print("FATAL: REPLACE produced no change (string-match failure).", file=sys.stderr)
        conn.close()
        return 3

    # Apply writable_schema edit pattern.
    cur.execute("BEGIN")
    try:
        cur.execute("PRAGMA writable_schema=1")
        cur.execute(
            "UPDATE sqlite_master SET sql=? WHERE type='table' AND name='weapon_knowledge_entries'",
            (new_sql,),
        )
        cur.execute("PRAGMA writable_schema=0")
        # Verify integrity before commit
        cur.execute("PRAGMA integrity_check")
        ic = cur.fetchall()
        if ic != [("ok",)]:
            cur.execute("ROLLBACK")
            print(f"FATAL: integrity_check returned {ic}; rolled back.", file=sys.stderr)
            conn.close()
            return 4
        conn.commit()
    except Exception as e:
        cur.execute("ROLLBACK")
        print(f"FATAL: schema edit failed; rolled back. error={e}", file=sys.stderr)
        conn.close()
        return 5

    # Verification round-trip
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='weapon_knowledge_entries'")
    final_sql = cur.fetchone()[0]
    for v in NEW_VALUES:
        if f"'{v}'" not in final_sql:
            print(f"FATAL: post-write verification missing enum value '{v}'", file=sys.stderr)
            conn.close()
            return 6

    # SQLite caches compiled schema per-connection. After a writable_schema edit
    # we must reopen the connection so subsequent CHECK enforcement reflects the
    # new constraint clause.
    conn.close()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # CHECK enforcement smoke-test: insert+rollback a row with a new enum value
    # to verify the new constraint actually accepts it.
    cur.execute("BEGIN")
    try:
        cur.execute(
            """INSERT INTO weapon_knowledge_entries (canonical_name, source_library, source_url, weapon_kind)
               VALUES (?, ?, ?, ?)""",
            ("__sidecar_b_smoke__", "__test__", "__sidecar_b_smoke__", "shield"),
        )
        cur.execute("ROLLBACK")
    except sqlite3.IntegrityError as e:
        cur.execute("ROLLBACK")
        print(f"FATAL: smoke-test INSERT with weapon_kind='shield' rejected: {e}", file=sys.stderr)
        conn.close()
        return 7

    # Negative smoke-test: ensure invalid enum value is still rejected
    cur.execute("BEGIN")
    rejected_ok = False
    try:
        cur.execute(
            """INSERT INTO weapon_knowledge_entries (canonical_name, source_library, source_url, weapon_kind)
               VALUES (?, ?, ?, ?)""",
            ("__sidecar_b_smoke_neg__", "__test__", "__sidecar_b_smoke_neg__", "totally_invalid_value"),
        )
    except sqlite3.IntegrityError:
        rejected_ok = True
    cur.execute("ROLLBACK")
    if not rejected_ok:
        print("FATAL: invalid weapon_kind was accepted by CHECK; constraint broken", file=sys.stderr)
        conn.close()
        return 8

    print("[ok] schema extension landed:")
    print(f"     weapon_kind enum now: ('category','unique','named_template','ammo_or_consumable','shield','tome','banner','focus','horn','talisman','unknown')")
    print(f"     positive smoke (shield accepted): ok")
    print(f"     negative smoke (invalid rejected): ok")
    print(f"     integrity_check: ok")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
