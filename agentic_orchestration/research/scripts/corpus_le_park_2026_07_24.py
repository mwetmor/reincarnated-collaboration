#!/usr/bin/env python3
"""
corpus_le_park_2026_07_24.py — PARK (not delete) all Last Epoch kits from the active roster.

RULING LINEAGE
    Matt 2026-07-24, TSR-7 fork (ii), gandalf true-sources grill brief
    `agentic_orchestration/gandalf/notes/2026-07-23-true-sources-grill-brief.md` §4 (rulings ledger, TSR-7 row).

TIGHTENED ROSTER RULE (verbatim, final text):
    "active-roster membership requires banked anchors OR a LANDED/agent-executable raw lane."

WHY LE FAILS BOTH DISJUNCTS
    (1) Banked anchors: LE holds 0 kit_numeric rows and 0 kit_composition rows — no deep anchor kit.
    (2) LANDED/agent-executable raw lane: NONE landed.
          - prowner/last-epoch-data (skillTrees.ts, 5,102,196 B) proves the data CLASS is extractable
            but the repo is STALE (pushed 2024-03-19, LE-1.0 era).
          - aianlinb/LELocalePatch is FRESH (2026-03-27) — tooling ecosystem alive, but not a data drop.
          - lastepochtools.com is live + maintained but BOT-GATED (403 to WebFetch and browser-UA curl) —
            not agent-fetchable.
          - official EHG Game Data API "not yet available".
          - Unity il2cpp extraction = highest-cost fallback; not executed, not landed.

WHY POE2 IS NOT AFFECTED (precedent does NOT cascade)
    PoE2 passes disjunct (1) on banked anchors alone: 105 kit_numeric rows. The tightened rule is a
    disjunction — one satisfied branch is sufficient. PoE2 stays ACTIVE.

REACTIVATION TRIGGER (stays live)
    A fresh LE datamine drop LANDING (agent-executable, current-patch) = LE re-passes the test.
    To reactivate: set roster_status='active', roster_status_note recording the landed lane, and
    restore the denominator 233 -> 270. NO rows were deleted, so reactivation is a flag flip.

MECHANISM (schema, park-not-delete — curated rows are capital, reversible)
    Additive, non-destructive. Adds three columns to canon_corpus:
      roster_status       TEXT  CHECK IN ('active','parked')  DEFAULT 'active'   (tagged, not encoded)
      roster_status_note  TEXT  (park lineage / reactivation note; NULL for active)
      roster_status_date  TEXT  (date the status was last set)
    Flags the 37 LE kits (game='le') to 'parked'. ZERO row deletions. kit_numeric / kit_composition
    untouched (LE has none anyway — re-verified as a sanity gate below).

    Design note (Discipline #14 spirit / elrond tagged-not-encoded law): park state is an EXPLICIT
    status column, not packed into kit_id, game code, or a compound flag. Every parked row still
    traces to its origin (source, source_date, provenance_tag preserved). Fully reversible.

IDEMPOTENT: re-running is safe. Columns added only if absent; flags set by game='le'; schema_meta
row inserted only if this version is not already present.

USAGE:
    python3 corpus_le_park_2026_07_24.py            # apply
    python3 corpus_le_park_2026_07_24.py --dry-run  # report, no writes
"""
import sqlite3
import sys
import datetime
import pathlib

DB = pathlib.Path(__file__).resolve().parent.parent / "curated" / "corpus.db"
SCHEMA_VERSION = "le-park-2026-07-24"
PARK_DATE = "2026-07-24"
PARK_NOTE = (
    "PARKED 2026-07-24 (Matt, TSR-7 fork ii). Roster rule tightened: "
    "'active-roster membership requires banked anchors OR a LANDED/agent-executable raw lane.' "
    "LE fails both disjuncts (0 banked kit_numeric/kit_composition; raw lane stale/bot-gated, none landed). "
    "PARK-not-DELETE: rows retained, reversible. Reactivation trigger: a fresh LE datamine drop landing."
)


def col_exists(cur, table, col):
    return any(r[1] == col for r in cur.execute(f"PRAGMA table_info({table})").fetchall())


def main(dry_run=False):
    if not DB.exists():
        sys.exit(f"FATAL: corpus.db not found at {DB}")
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON;")
    cur = con.cursor()

    # ---- SANITY GATE (pre-write): confirm the premise numbers before touching anything ----
    le_total = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE game='le'").fetchone()[0]
    le_numeric = cur.execute(
        "SELECT COUNT(*) FROM kit_numeric kn JOIN canon_corpus c ON c.kit_id=kn.kit_id WHERE c.game='le'"
    ).fetchone()[0]
    le_comp = cur.execute(
        "SELECT COUNT(*) FROM kit_composition kc JOIN canon_corpus c ON c.kit_id=kc.kit_id WHERE c.game='le'"
    ).fetchone()[0]
    poe2_numeric = cur.execute(
        "SELECT COUNT(*) FROM kit_numeric kn JOIN canon_corpus c ON c.kit_id=kn.kit_id WHERE c.game='poe2'"
    ).fetchone()[0]

    print(f"SANITY GATE  LE kits={le_total}  LE kit_numeric={le_numeric}  LE kit_composition={le_comp}  PoE2 kit_numeric={poe2_numeric}")
    assert le_total == 37, f"expected 37 LE kits, found {le_total} — HALT (premise changed)"
    assert le_numeric == 0, f"expected 0 LE kit_numeric, found {le_numeric} — HALT (would touch numeric data)"
    assert le_comp == 0, f"expected 0 LE kit_composition, found {le_comp} — HALT (would touch composition data)"
    assert poe2_numeric == 105, f"expected 105 PoE2 kit_numeric, found {poe2_numeric} — HALT (PoE2 premise changed)"
    print("SANITY GATE PASS — LE has zero exact-number rows; PoE2 anchors intact.")

    # ---- denominator accounting (record-BUCKET = the 5 active-roster games) ----
    active_games = ("poe1", "d2", "gd", "le", "poe2")
    denom_before = cur.execute(
        f"SELECT COUNT(*) FROM canon_corpus WHERE game IN {active_games}"
    ).fetchone()[0]
    denom_after = denom_before - le_total
    print(f"DENOMINATOR  record-bucket before={denom_before}  after park={denom_after}  (LE removed={le_total})")
    assert denom_before == 270, f"expected 270 record-bucket before, found {denom_before} — HALT"
    assert denom_after == 233, f"expected 233 after park, computed {denom_after} — HALT"

    if dry_run:
        print("DRY-RUN — no writes. Would add 3 columns, flag 37 LE kits parked, insert schema_meta row.")
        con.close()
        return

    # ---- ADDITIVE DDL (idempotent) ----
    if not col_exists(cur, "canon_corpus", "roster_status"):
        cur.execute(
            "ALTER TABLE canon_corpus ADD COLUMN roster_status TEXT "
            "CHECK (roster_status IN ('active','parked')) NOT NULL DEFAULT 'active'"
        )
        print("DDL  added canon_corpus.roster_status (default 'active')")
    else:
        print("DDL  canon_corpus.roster_status already present — skipped")

    if not col_exists(cur, "canon_corpus", "roster_status_note"):
        cur.execute("ALTER TABLE canon_corpus ADD COLUMN roster_status_note TEXT")
        print("DDL  added canon_corpus.roster_status_note")
    else:
        print("DDL  canon_corpus.roster_status_note already present — skipped")

    if not col_exists(cur, "canon_corpus", "roster_status_date"):
        cur.execute("ALTER TABLE canon_corpus ADD COLUMN roster_status_date TEXT")
        print("DDL  added canon_corpus.roster_status_date")
    else:
        print("DDL  canon_corpus.roster_status_date already present — skipped")

    # ---- FLAG the 37 LE kits parked (ZERO deletions) ----
    cur.execute(
        "UPDATE canon_corpus SET roster_status='parked', roster_status_note=?, roster_status_date=? "
        "WHERE game='le'",
        (PARK_NOTE, PARK_DATE),
    )
    flagged = cur.rowcount
    print(f"FLAG  set roster_status='parked' on {flagged} LE kits")
    assert flagged == 37, f"expected to flag 37, flagged {flagged} — HALT (rolling back)"

    # ---- schema_meta record (idempotent) ----
    exists = cur.execute(
        "SELECT COUNT(*) FROM corpus_schema_meta WHERE version=?", (SCHEMA_VERSION,)
    ).fetchone()[0]
    if not exists:
        cur.execute(
            "INSERT INTO corpus_schema_meta(version, applied_utc, note) VALUES (?,?,?)",
            (
                SCHEMA_VERSION,
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "LE PARK-not-DELETE (elrond, TSR-7 fork ii, Matt 2026-07-24). Additive: roster_status "
                "{active,parked} + roster_status_note + roster_status_date on canon_corpus. 37 LE kits "
                "flagged parked; 0 deletions; kit_numeric/kit_composition untouched (LE has none). "
                "Active record-bucket denominator 270 -> 233. Reactivation: fresh LE datamine drop landing.",
            ),
        )
        print(f"SCHEMA_META  inserted version '{SCHEMA_VERSION}'")
    else:
        print(f"SCHEMA_META  version '{SCHEMA_VERSION}' already present — skipped")

    con.commit()

    # ---- POST-write verification ----
    parked = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE roster_status='parked'").fetchone()[0]
    active = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE roster_status='active'").fetchone()[0]
    total = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    active_bucket = cur.execute(
        f"SELECT COUNT(*) FROM canon_corpus WHERE game IN {active_games} AND roster_status='active'"
    ).fetchone()[0]
    le_still_present = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE game='le'").fetchone()[0]
    fk = cur.execute("PRAGMA foreign_key_check").fetchall()
    integ = cur.execute("PRAGMA integrity_check").fetchone()[0]

    print("---- POST-APPLY VERIFICATION ----")
    print(f"  canon_corpus total rows      : {total}   (unchanged — no deletions)")
    print(f"  roster_status='parked'       : {parked}")
    print(f"  roster_status='active'       : {active}")
    print(f"  LE rows still present        : {le_still_present}  (retained, reversible)")
    print(f"  active record-bucket (denom) : {active_bucket}")
    print(f"  foreign_key_check            : {'clean' if not fk else fk}")
    print(f"  integrity_check              : {integ}")
    assert le_still_present == 37, "LE rows must remain present (park-not-delete)"
    assert active_bucket == 233, f"active record-bucket must be 233, got {active_bucket}"
    assert parked >= 37, "at least 37 parked"
    assert not fk, "foreign_key_check must be clean"
    assert integ == "ok", "integrity_check must be ok"
    print("POST-APPLY VERIFICATION PASS.")
    con.close()


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
