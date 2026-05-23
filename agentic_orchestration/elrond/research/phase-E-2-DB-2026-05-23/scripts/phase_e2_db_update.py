"""
Phase E-2-DB cluster-label UPDATE — elrond data steward curation pass.

Inputs:
  - gandalf canonical-label JSON at agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json
  - DB at /Users/admin/Games/reincarnated-loadout/data/telemetry.db

What this script does (single transaction):
  1. Validates JSON: 125 entries, db_cluster_id 1-125, non-null canonical_label/cluster_type
  2. Pre-state captured separately (pre-update-state-clusters.tsv)
  3. Idempotent ALTER TABLE clusters ADD COLUMN cluster_type TEXT (catches "duplicate column" error)
  4. Transactional UPDATE of clusters.label + clusters.cluster_type for all 125 rows
  5. Verification queries:
     - zero PROVISIONAL labels remain
     - count = 125 unchanged
     - spot-checks on db_cluster_ids 63, 87, 91 (the dispatch's illustrative refs;
       legolas-id 62, 86, 90)
     - round-trip smoke: 100-row sample joining weapon_knowledge_entries -> clusters

Tool script per elrond charter — not consumed by engine. Lives under
agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/scripts/.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/admin/Games/reincarnated-collaboration")
DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
JSON_PATH = REPO_ROOT / "agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json"
POST_STATE_PATH = REPO_ROOT / "agentic_orchestration/elrond/research/phase-E-2-DB-2026-05-23/post-update-state-clusters.tsv"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    # ---- 1. Load + validate JSON -----------------------------------------
    with JSON_PATH.open() as f:
        payload = json.load(f)

    clusters = payload["clusters"]
    if len(clusters) != 125:
        fail(f"expected 125 clusters; got {len(clusters)}")

    db_ids = [c["db_cluster_id"] for c in clusters]
    if sorted(db_ids) != list(range(1, 126)):
        fail("db_cluster_id range is not 1..125 (gaps or duplicates)")

    for c in clusters:
        if not c.get("canonical_label"):
            fail(f"db_cluster_id={c['db_cluster_id']}: null canonical_label")
        if not c.get("cluster_type"):
            fail(f"db_cluster_id={c['db_cluster_id']}: null cluster_type")

    print(f"JSON validates: 125 clusters; db_cluster_id 1..125; all labels + types populated.")

    # ---- 2. Connect to DB ------------------------------------------------
    if not DB_PATH.exists():
        fail(f"DB not found at {DB_PATH}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # Sanity-check pre-state
    n_pre = cur.execute("SELECT COUNT(*) FROM clusters").fetchone()[0]
    if n_pre != 125:
        fail(f"clusters row count pre-update is {n_pre}, expected 125")
    n_prov_pre = cur.execute("SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%'").fetchone()[0]
    print(f"Pre-update: clusters rows={n_pre}; PROVISIONAL labels={n_prov_pre}")

    # ---- 3. Idempotent ALTER TABLE ADD COLUMN cluster_type --------------
    try:
        cur.execute("ALTER TABLE clusters ADD COLUMN cluster_type TEXT")
        print("ALTER TABLE clusters ADD COLUMN cluster_type TEXT — applied.")
        alter_applied = True
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("ALTER TABLE clusters ADD COLUMN cluster_type — already exists; skipped (idempotent).")
            alter_applied = False
        else:
            raise

    # ---- 4. Transactional UPDATE ----------------------------------------
    update_rows = [
        (c["canonical_label"], c["cluster_type"], c["db_cluster_id"]) for c in clusters
    ]

    try:
        cur.execute("BEGIN")
        cur.executemany(
            "UPDATE clusters SET label = ?, cluster_type = ? WHERE id = ?",
            update_rows,
        )
        rowcount = cur.rowcount
        # rowcount on executemany is implementation-defined; verify via re-query below
        conn.commit()
        print(f"UPDATE executed: {len(update_rows)} parameter sets submitted; sqlite rowcount={rowcount}.")
    except Exception as e:
        conn.rollback()
        fail(f"UPDATE transaction failed and rolled back: {e}")

    # ---- 5. Verification ------------------------------------------------
    n_post = cur.execute("SELECT COUNT(*) FROM clusters").fetchone()[0]
    n_prov_post = cur.execute("SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%'").fetchone()[0]
    n_null_label = cur.execute("SELECT COUNT(*) FROM clusters WHERE label IS NULL OR label = ''").fetchone()[0]
    n_null_type = cur.execute("SELECT COUNT(*) FROM clusters WHERE cluster_type IS NULL OR cluster_type = ''").fetchone()[0]

    print()
    print("=== Verification queries ===")
    print(f"clusters row count post-update: {n_post} (expected 125)")
    print(f"PROVISIONAL labels remaining:   {n_prov_post} (expected 0)")
    print(f"NULL/empty label rows:          {n_null_label} (expected 0)")
    print(f"NULL/empty cluster_type rows:   {n_null_type} (expected 0)")

    if n_post != 125 or n_prov_post != 0 or n_null_label != 0 or n_null_type != 0:
        fail("Verification gates did not all pass; see counts above.")

    # Spot-check sample (dispatch text used legolas ids 1, 50, 62, 86, 90 ->
    # db_cluster_ids 2, 51, 63, 87, 91). Also probe db_cluster_id 1.
    print()
    print("Spot-checks (db_cluster_id, label, cluster_type):")
    for db_id in (1, 51, 63, 87, 91):
        row = cur.execute(
            "SELECT id, label, cluster_type FROM clusters WHERE id = ?", (db_id,)
        ).fetchone()
        print(f"  id={row[0]:>3}  type={row[2]:<28}  label={row[1]}")

    # ---- 6. Round-trip smoke (100-row sample) ---------------------------
    smoke_rows = cur.execute(
        """
        SELECT wke.id, wke.canonical_name, wke.cluster_id, c.label, c.cluster_type
        FROM weapon_knowledge_entries wke
        JOIN clusters c ON c.id = wke.cluster_id
        WHERE wke.cluster_id IS NOT NULL
        ORDER BY wke.id
        LIMIT 100
        """
    ).fetchall()
    if len(smoke_rows) != 100:
        fail(f"round-trip smoke expected 100 rows; got {len(smoke_rows)}")
    orphans = [r for r in smoke_rows if r[3] is None or r[3] == "" or r[3].startswith("PROVISIONAL:")]
    if orphans:
        fail(f"round-trip smoke: {len(orphans)} rows had null/empty/PROVISIONAL labels via join")
    print()
    print(f"Round-trip smoke (100 rows): PASS — all join targets carry canonical labels + cluster_type.")
    # Show first 3 + last 3 for sanity
    print("First 3 joined rows:")
    for r in smoke_rows[:3]:
        print(f"  wke.id={r[0]:>6}  '{r[1]}'  -> cluster_id={r[2]}  type={r[4]}  label='{r[3]}'")
    print("Last 3 joined rows:")
    for r in smoke_rows[-3:]:
        print(f"  wke.id={r[0]:>6}  '{r[1]}'  -> cluster_id={r[2]}  type={r[4]}  label='{r[3]}'")

    # Distribution check: cluster_type breakdown
    print()
    print("cluster_type distribution (DB-side):")
    for row in cur.execute(
        "SELECT cluster_type, COUNT(*) FROM clusters GROUP BY cluster_type ORDER BY cluster_type"
    ).fetchall():
        print(f"  {row[0]:<32} {row[1]}")

    # ---- 7. Persist post-state TSV for audit ----------------------------
    POST_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with POST_STATE_PATH.open("w") as f:
        for row in cur.execute(
            "SELECT id, cluster_type, label FROM clusters ORDER BY id"
        ).fetchall():
            f.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")
    print()
    print(f"Post-update state written to {POST_STATE_PATH}")

    conn.close()

    print()
    print("=== ACCEPTANCE GATES ===")
    print(f"  [PASS] All 125 labels updated; zero PROVISIONAL remain.")
    print(f"  [PASS] Row count unchanged at 125.")
    print(f"  [PASS] Round-trip smoke (100-row join sample).")
    print(f"  [{'PASS' if alter_applied else 'PASS (idempotent skip)'}] cluster_type column populated.")


if __name__ == "__main__":
    main()
