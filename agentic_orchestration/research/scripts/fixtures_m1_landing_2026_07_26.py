#!/usr/bin/env python3
"""
fixtures.db landing — MILESTONE 1
=================================
Creates `research/curated/fixtures.db` on schema `fixtures-v0.1`, applies the
reviewed DDL (`research/scripts/fixtures_v0_1_ddl.sql`), and seeds the
`measure_dict` controlled vocabulary.

Agent: elrond (data steward).  Commissioner: gandalf (GD program, gap 5).
Governing artifacts:
  elrond/notes/2026-07-25-l0-fixture-schema-draft.md    (v0.1 draft, sec 6.1 seed)
  gandalf/notes/2026-07-25-l0-fixture-schema-review.md  (ACCEPT + rulings O-1..O-10)

Idempotent: rebuilds fixtures.db from scratch every run. The DB file is
gitignored (curated/.gitignore `*.db`); this script IS the durable record.

DDL verification performed at this landing (against draft sec 10 + the rulings):
  - O-1 separate store                       -> honoured (own file, own MIGRATION doc)
  - O-2 measure_subkey column                -> present, in the PK
  - O-6 dps_field oracle-side colour only    -> CORRECTED HERE. The draft sec 6.1 table
        listed dps_field lane_availability='both'; gandalf ruled it OUT of the G3
        comparable set. Seeded as 'oracle-only'. (DDL itself needed no change.)
  - O-7 disagreeing readings both stand      -> no reconciliation logic anywhere
  - O-8 NULL monster_record admitted; v_fixture_bank_certified filters -> present
  - O-9 'expired' in fixture_set_constraint.held CHECK -> present
  - table creation order (capture before fixture_character, which FKs it) -> correct
  - `PRAGMA foreign_key_check` clean on an empty apply
"""

import hashlib
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone

REPO = "/Users/admin/Games/reincarnated-collaboration"
CURATED = os.path.join(REPO, "agentic_orchestration/research/curated")
SCRIPTS = os.path.join(REPO, "agentic_orchestration/research/scripts")
DDL_PATH = os.path.join(SCRIPTS, "fixtures_v0_1_ddl.sql")
DB_PATH = os.path.join(CURATED, "fixtures.db")
SCHEMA_VERSION = "fixtures-v0.1"

# ---------------------------------------------------------------------------
# measure_dict seed — draft sec 6.1, with the O-6 correction applied.
# (key, label, unit, value_kind, panel_field, lane_availability, rung, definition, confounds)
# ---------------------------------------------------------------------------
MEASURE_DICT = [
    ("play_time", "Play Time", "s", "counter", "Play Time", "both", "L0",
     "In-game play-time counter. THE trial clock (draft sec 8.5) — file mtimes are "
     "transfer times, not capture times.",
     "Session-cumulative; advances during menus and panel-reading, so a before/after "
     "delta over-states engagement time by the capture overhead."),
    ("total_score", "Total Score", "pts", "counter", "Total Score", "oracle-only", "L0",
     "GD's own composite score counter.", "Opaque formula; no sim analogue."),
    ("deaths", "Number of deaths", "count", "counter", "Number of deaths", "both", "L0",
     "Session-cumulative player deaths.", None),
    ("kills", "Number of kills", "count", "counter", "Number of kills", "both", "L0",
     "Session-cumulative monster kills.",
     "Counts EVERY kill including off-trial ones — the ledger-continuity detector "
     "(draft sec 8.1) exists because of this."),
    ("health_potions_used", "Health potions used", "count", "counter",
     "Health potions used", "both", "L0",
     "Session-cumulative health-potion consumptions. Attests the no-potions constraint.", None),
    ("mana_potions_used", "Mana potions used", "count", "counter",
     "Mana potions used", "both", "L0",
     "Session-cumulative mana-potion consumptions.", None),
    ("max_level_achieved", "Max. level achieved", "level", "gauge", "Max. level achieved",
     "both", "L0",
     "Highest character level reached this session. The mid-set level-up detector "
     "(draft sec 8.2).",
     "It is a session MAX, not the level in force — equal only because these sittings "
     "never de-levelled."),
    ("dps_field", "Damage per second", "dmg/s", "gauge", "Damage per second",
     "oracle-only", "L0",
     "GD's recent-window DPS meter. O-6 RULING: dropped from the G3-B comparable set; "
     "kept as oracle-side colour only. fight_seconds + kills already bracket TTK.",
     "Window semantics undocumented; the window EXPIRES. A 0.00 reading after a real "
     "fight means the window lapsed before capture (draft sec 8.4), not zero damage. "
     "Always pair with validity_flag."),
    ("skill_use_count", "Skills Used (per record)", "count", "counter",
     "Skills Used", "both", "L0",
     "Per-skill session-cumulative use counter. Uses measure_subkey to carry the "
     "skill .dbr record path (O-2), joinable to corpus.db exact_skill.record_path.", None),
    ("life_healed", "Life healed", "HP", "counter", "Life healed", "both", "L0",
     "Session-cumulative HP restored by any source. Used as a damage-taken PROXY.",
     "THREE named confounds (draft sec 8.6): (1) a level-up raises max HP and triggers "
     "regen, accruing life_healed with zero damage taken; (2) it does not accrue at "
     "full HP, so short full-HP fights read 0.00; (3) over a long capture window it "
     "measures post-fight regen too, not damage taken IN the fight."),
    ("shield_block_chance", "Shield block chance", "pct", "gauge", "Shield block chance",
     "both", "L0", "Panel-reported shield block chance.", None),
    ("fight_seconds", "Fight duration (hand-noted)", "s", "band", None, "both", "L0",
     "Matt's hand-timed engagement duration. Oracle emits a band; sim emits exact.",
     "Round-3 addendum (matt-addendum-timing-uncertainty.md): hand-noted seconds "
     "INCLUDE ~1 s per screenshot of capture overhead — systematic bias UPWARD. Bank "
     "with uncertainty_abs >= 2 s. Panel play_time deltas are the stronger instrument."),
    ("hp_cost_band", "HP cost (categorical)", None, "categorical", None, "both", "L0",
     "Categorical HP-cost note ('none' / 'sliver' / ...) when no number was taken.", None),
    ("hp_cost_abs", "HP cost (absolute)", "HP", "band", None, "both", "L0",
     "HP lost across the fight, hand-noted or globe-derived.",
     "Disagrees with the life_healed panel delta (draft sec 8.6). O-7: both stand, "
     "unreconciled."),
    ("hp_current", "Current HP (globe)", "HP", "gauge", None, "both", "L0",
     "HP globe current value.",
     "Read at capture time, not at the killing blow — regen may have run."),
    ("hp_max", "Max HP (globe)", "HP", "gauge", None, "both", "L0",
     "HP globe maximum value.", None),
    ("capture_latency", "Capture latency", "s", "gauge", None, "oracle-only", "L0",
     "Seconds between the fight ending and the after-shot being taken. The condition "
     "on which dps_field validity depends (draft sec 8.4).", None),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.exists(DDL_PATH):
        sys.exit("FATAL: DDL not found at %s" % DDL_PATH)

    if os.path.exists(DB_PATH):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        bak = DB_PATH + ".pre-m1-" + stamp
        shutil.copy2(DB_PATH, bak)
        print("backed up existing DB -> %s" % os.path.basename(bak))
        os.remove(DB_PATH)

    ddl = open(DDL_PATH).read()
    ddl_sha = sha256_file(DDL_PATH)

    con = sqlite3.connect(DB_PATH)
    con.executescript(ddl)

    con.executemany(
        "INSERT INTO measure_dict (measure_key,label,unit,value_kind,panel_field,"
        "lane_availability,ladder_rung_introduced,definition,confounds) "
        "VALUES (?,?,?,?,?,?,?,?,?)", MEASURE_DICT)

    con.execute(
        "INSERT INTO schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        (SCHEMA_VERSION,
         datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "M1 landing. DDL sha256=%s. measure_dict seeded with %d keys "
         "(draft sec 6.1 + O-6 correction: dps_field is oracle-only). "
         "Applied by fixtures_m1_landing_2026_07_26.py."
         % (ddl_sha, len(MEASURE_DICT))))

    con.commit()

    # --- verification -------------------------------------------------------
    print("\nDDL sha256: %s" % ddl_sha)
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    views = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")]
    print("tables (%d): %s" % (len(tables), ", ".join(tables)))
    print("views  (%d): %s" % (len(views), ", ".join(views)))
    print("measure_dict rows: %d" % con.execute(
        "SELECT COUNT(*) FROM measure_dict").fetchone()[0])
    print("  oracle-only keys: %s" % ", ".join(
        r[0] for r in con.execute(
            "SELECT measure_key FROM measure_dict WHERE lane_availability='oracle-only' "
            "ORDER BY measure_key")))
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    print("foreign_key_check: %s" % ("CLEAN" if not fk else fk))
    # every view must be selectable on an empty DB
    for v in views:
        con.execute("SELECT * FROM %s LIMIT 1" % v).fetchall()
    print("all %d views selectable on empty DB: OK" % len(views))
    con.close()
    print("\nfixtures.db landed at %s" % DB_PATH)


if __name__ == "__main__":
    main()
