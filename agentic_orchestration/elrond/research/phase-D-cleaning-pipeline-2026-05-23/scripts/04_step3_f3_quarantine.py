#!/usr/bin/env python3
"""
Phase D Step 3: F3 quarantine (pf2ools + souls-api items.js).

Per gandalf cleaning-policy-design §F3 + math note §2.3 + Open Question Q4:

Two whole-source quarantines via the wikipedia-unfiltered Discipline #11 pattern:
  - pf2ools-pf2ools-data (688 rows; 100% non-weapons; Pathfinder 2e backgrounds)
  - souls-api-thomaslincoln items.js subset (56 rows of 58; 96.6% FP non-weapons)
    EXCEPT 2 weapons.js rows preserved (per Q4 — zero-cost TP preservation)

For each quarantine:
  1. Dump rows to gzipped JSONL archive
  2. Rename source_library to '<original>-quarantined'
  3. NO DELETE (Discipline #11 audit-preservation)

Outputs:
  - DB mutations: 688 + 56 = 744 source_library renames
  - quarantine-archives/pf2ools-quarantine-2026-05-23.jsonl.gz
  - quarantine-archives/souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz
  - quarantine-archives/README.md amendment (this script appends a section)
  - logs/04_step3_f3_quarantine.json

Idempotency: WHERE source_library matches the un-quarantined slug; re-runs are no-op.
Archive files: write only if absent.

Authority: Matt 2026-05-23 whole-pipeline upfront authorization.
Math note: §2.3 + §6.4 (Q4 souls-api preservation).
"""

from __future__ import annotations

import gzip
import json
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "04_step3_f3_quarantine.json"
ARCHIVE_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
    "research/weapon-library-import-2026-05-22/quarantine-archives"
)
PF2OOLS_ARCHIVE = ARCHIVE_DIR / "pf2ools-quarantine-2026-05-23.jsonl.gz"
SOULS_ARCHIVE = ARCHIVE_DIR / "souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz"

DATE_STAMP = "2026-05-23"


def archive_rows(
    conn: sqlite3.Connection,
    where_clause: str,
    where_args: tuple,
    archive_path: Path,
) -> int:
    """Dump matching rows to gzipped JSONL. Idempotent: skip if archive already exists."""
    if archive_path.exists():
        print(f"  [archive] {archive_path.name} already exists — skip (idempotent)")
        return 0

    cur = conn.execute(
        f"""SELECT id, canonical_name, source_library, source_url, source_id,
                   description_text, structured_properties, cultural_lineage_tags,
                   historical_period, genre_appearances, related_entries,
                   license_class, imported_at,
                   weapon_kind, dedup_status, variant_relationship,
                   cultural_lineage_canonical, historical_period_canonical,
                   register_canonical, cultural_lineage_confidence,
                   template_quality_score, wieldable_humanoid, cluster_id
            FROM weapon_knowledge_entries
            WHERE {where_clause}""",
        where_args,
    )
    cols = [d[0] for d in cur.description]
    count = 0
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(archive_path, "wt", encoding="utf-8") as f:
        for row in cur:
            record = dict(zip(cols, row))
            f.write(json.dumps(record, default=str) + "\n")
            count += 1
    print(f"  [archive] wrote {count} rows to {archive_path}")
    return count


def quarantine_rename(
    conn: sqlite3.Connection,
    where_clause: str,
    where_args: tuple,
    new_source_library: str,
) -> int:
    cur = conn.execute(
        f"""UPDATE weapon_knowledge_entries
            SET source_library = ?
            WHERE {where_clause}""",
        (new_source_library, *where_args),
    )
    rowcount = cur.rowcount
    conn.commit()
    return rowcount


def quarantine_pf2ools(conn: sqlite3.Connection) -> dict:
    """All 688 pf2ools rows → -quarantined."""
    # Idempotency: only operate on rows still under un-quarantined slug
    archived = archive_rows(
        conn,
        "source_library = ?",
        ("pf2ools-pf2ools-data",),
        PF2OOLS_ARCHIVE,
    )
    renamed = quarantine_rename(
        conn,
        "source_library = ?",
        ("pf2ools-pf2ools-data",),
        "pf2ools-pf2ools-data-quarantined",
    )
    return {"archived": archived, "renamed": renamed}


def quarantine_souls_api(conn: sqlite3.Connection) -> dict:
    """Souls-api items.js subset only (per Q4 — preserve 2 weapons.js rows)."""
    archived = archive_rows(
        conn,
        "source_library = ? AND source_url LIKE ?",
        ("souls-api-thomaslincoln", "%items.js%"),
        SOULS_ARCHIVE,
    )
    renamed = quarantine_rename(
        conn,
        "source_library = ? AND source_url LIKE ?",
        ("souls-api-thomaslincoln", "%items.js%"),
        "souls-api-thomaslincoln-quarantined",
    )
    return {"archived": archived, "renamed": renamed}


README_AMENDMENT_MARKER = "## Phase D F3 quarantines — 2026-05-23"
README_AMENDMENT = """

---

## Phase D F3 quarantines — 2026-05-23

**Date archived:** 2026-05-23
**Authority:** Matt direction 2026-05-23 (whole-pipeline upfront authorization for Phase D)
**Pattern:** Discipline #11 audit-preservation (compressed JSONL dump; source_library renamed; NO DELETE)

Two whole-source quarantines added by Phase D Step 3 per gandalf F3 framework:

### pf2ools-pf2ools-data → pf2ools-pf2ools-data-quarantined

- **Rows quarantined:** 688
- **TP rate:** 0% (legolas Phase A Deliverable 3 §1 confirmed)
- **Content:** Pathfinder 2e character backgrounds; ALL non-weapons.
- **Evidence:** Source URLs all point to `data/AV0/`, `data/APG/`, `data/CRB/` background data files. Descriptions are background text (ability boosts, trained skills, skill feats). Examples: "Bibliophile", "Eldritch Anatomist", "Bandit", "Cook", "Courier".
- **Archive:** `pf2ools-quarantine-2026-05-23.jsonl.gz`

### souls-api-thomaslincoln (items.js subset) → souls-api-thomaslincoln-quarantined

- **Rows quarantined:** 56 of 58 total souls-api rows (96.6% FP per legolas)
- **2 preserved:** weapons.js rows (DRAGON GREATSWORD + 1 other) stay `source_library='souls-api-thomaslincoln'` per math note Q4 (zero-cost TP preservation).
- **Content:** Dark Souls 1 items.js entries — keys, embers, spells, consumables, quest items (AFFIDAVIT, ALLURING SKULL, ANNEX KEY, BINOCULARS, etc.). NOT weapons.
- **Archive:** `souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz`

## Cumulative quarantine archive state

| Source | Archive file | Rows | Date |
|---|---|---|---|
| wikipedia-unfiltered (entries) | wikipedia-unfiltered-entries-2026-05-22.jsonl.gz | 130,334 | 2026-05-22 |
| wikipedia-unfiltered (images) | wikipedia-unfiltered-images-2026-05-22.jsonl.gz | 38,589 | 2026-05-22 |
| pf2ools-pf2ools-data | pf2ools-quarantine-2026-05-23.jsonl.gz | 688 | 2026-05-23 |
| souls-api-thomaslincoln (items.js) | souls-api-thomaslincoln-quarantine-2026-05-23.jsonl.gz | 56 | 2026-05-23 |

Restoration via Python round-trip (JSONL → INSERT; reverse the source_library rename for in-DB quarantines).
"""


def amend_readme(readme_path: Path) -> dict:
    """Append Phase D quarantine section to README.md if not already present."""
    if not readme_path.exists():
        readme_path.write_text(README_AMENDMENT.lstrip())
        return {"action": "CREATED"}
    content = readme_path.read_text()
    if README_AMENDMENT_MARKER in content:
        return {"action": "SKIP_EXISTS"}
    with readme_path.open("a") as f:
        f.write(README_AMENDMENT)
    return {"action": "AMENDED"}


def acceptance_check(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()
    # Pre/post counts
    pf2ools_remaining = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='pf2ools-pf2ools-data'"
    ).fetchone()[0]
    pf2ools_quarantined = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='pf2ools-pf2ools-data-quarantined'"
    ).fetchone()[0]
    souls_remaining = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='souls-api-thomaslincoln'"
    ).fetchone()[0]
    souls_quarantined = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE source_library='souls-api-thomaslincoln-quarantined'"
    ).fetchone()[0]
    total_active = cur.execute(
        """SELECT COUNT(*) FROM weapon_knowledge_entries
           WHERE source_library NOT IN (
             'wikipedia-unfiltered',
             'pf2ools-pf2ools-data-quarantined',
             'souls-api-thomaslincoln-quarantined'
           )"""
    ).fetchone()[0]
    # Total all (including quarantined)
    total_all = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries"
    ).fetchone()[0]
    return {
        "pf2ools_unquarantined_remaining": pf2ools_remaining,
        "pf2ools_quarantined": pf2ools_quarantined,
        "souls_api_remaining": souls_remaining,
        "souls_api_quarantined": souls_quarantined,
        "total_all_rows": total_all,
        "total_active_rows": total_active,
        # Acceptance per math note §2.3: post-quarantine active substrate ~89,095
        "active_in_expected_band": 89000 <= total_active <= 89200,
        # Idempotency: 0 un-quarantined pf2ools/souls-items-js rows remain
        "quarantine_clean": pf2ools_remaining == 0 and souls_quarantined > 0,
        "souls_preserved_two_weapons": souls_remaining == 2,
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "04_step3_f3_quarantine.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        summary["pf2ools_result"] = quarantine_pf2ools(conn)
        summary["souls_api_result"] = quarantine_souls_api(conn)
        summary["readme_result"] = amend_readme(ARCHIVE_DIR / "README.md")
        summary["acceptance"] = acceptance_check(conn)
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    acc = summary["acceptance"]
    summary["passed"] = (
        acc["active_in_expected_band"]
        and acc["quarantine_clean"]
        and acc["souls_preserved_two_weapons"]
    )

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n  ==> pf2ools quarantined: {acc['pf2ools_quarantined']} (expected 688)")
    print(f"  ==> souls-api quarantined: {acc['souls_api_quarantined']} (expected 56)")
    print(f"  ==> souls-api preserved (weapons.js): {acc['souls_api_remaining']} (expected 2)")
    print(f"  ==> total active: {acc['total_active_rows']} (band 89,000-89,200)")
    print(f"  ==> PASSED: {summary['passed']}")
    print(f"  ==> Summary: {LOG_PATH}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
