#!/usr/bin/env python3
"""
gd_bridge_m3_bridge_and_fixtures_2026_07_26.py — M3 of the GD display-name -> `.dbr` bridge.

TWO STORES, TWO CONCERNS
    corpus.db   : the BRIDGE — display string -> candidate record paths, fan-out preserved.
    fixtures.db : schema `fixtures-v0.2` + the certified fixture rows populated from it.

THE SHAPE OF THE BRIDGE (the load-bearing design decision)
    tag -> record is ONE-TO-MANY. "Walking Dead" reaches 17 Monster records. The temptation is to
    pick one and store a scalar. This schema refuses that, in three layers:

      1. `v_gd_monster_bridge`            — the RAW fan-out. One row per (display_name, record).
                                            Nothing is dropped. `candidate_count` is on every row.
      2. `gd_monster_tiebreak`            — a SEPARATE table of heuristic penalty scores, keyed to
                                            the record. It is data, inspectable and revisable, and
                                            it lives beside the fan-out rather than inside it. The
                                            heuristic can be re-scored without touching a fact.
      3. `v_gd_monster_bridge_preferred`  — one row per display_name: the preferred record AND the
                                            candidate count AND the distinct-bio count AND the
                                            modal bio with its support. A consumer that reads only
                                            this view still cannot avoid seeing the ambiguity.

    The BIO collapse is the mitigation that matters. GD keeps monster attributes as `charLevel`
    formula strings on the record pointed at by `characterAttributeEquations`, not on the Monster
    record (`zombie_a01.characterLife` is literally 0.0). 15 of the 17 "Walking Dead" candidates
    share `bio_zombie_01.dbr`, so the 17-way record ambiguity collapses to a 1-way STATLINE
    answer. `modal_bio_record` / `modal_bio_support` / `distinct_bio_count` carry that as derived,
    annotated columns -- never as a replacement for the raw candidate list.

TIEBREAK RULE v1 (documented so it is visibly a heuristic)
    Penalties are additive over PATH STRUCTURE only -- nothing is inferred from the statline,
    because the probe established that the 17 candidates are statline-identical in every header
    field. Authoring-tree location is the only signal a nameplate screenshot cannot arbitrate but
    a curator can:
        sandbox/ +100 · special/ +90 · boss&quest/ +80 · /npcs/ +70
        stem suffix _summon/_starter/_doa +40 · 'dropper' in stem +40
    Ties break deterministically on (directory depth, stem length, path) so the rule is a
    function, not a coin flip. `is_preferred` is NEVER a claim about which record a world spawn
    instantiated -- that lives in `Levels.arc` spawn tables, is not parsed, and is declared open.

`fixtures-v0.2` (elrond seam call — see MIGRATION-fixtures.md M4 for the full rationale)
    `fixture_set` gains: monster_record_candidates (JSON), monster_bio_record, monster_rank,
                         monster_race, monster_record_method, monster_record_evidence
    `measure_dict` gains: off_trial_semantics

    NOT ADDED, and this is a retraction of my own v0.1 §7 item 3: `monster_affix` / `monster_variant`.
    I recommended them because anomaly A1 -- the unexplained third nameplate line "Aether
    Corruption" -- might have meant the fixture was an affixed variant. Legolas §3 resolved A1:
    it is `characterRacialProfile = 'Race005'`, a creature-type noun, confirmed by the singular/
    plural pair `tagRace005` / `tagRace005P` and by an exhaustive scan finding no other creature-
    side occurrence. There is no affix. Building the columns anyway would bank my superseded
    hypothesis as schema. `monster_race` is what the line actually is, so that is what is added.

USAGE
    python3 gd_bridge_m3_bridge_and_fixtures_2026_07_26.py --verify-only
    python3 gd_bridge_m3_bridge_and_fixtures_2026_07_26.py
"""
import collections
import datetime
import hashlib
import json
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE.parent / "curated" / "corpus.db"
FIXTURES = HERE.parent / "curated" / "fixtures.db"

SCHEMA_VERSION = "gd-displayname-bridge-2026-07-26"
FIXTURES_VERSION = "fixtures-v0.2"
ADAPTER = "gd_bridge_m3_bridge_and_fixtures_2026_07_26.py"
RUN_DATE = "2026-07-26"
TIEBREAK_RULE_VERSION = "path-structure-v1"

# ---- tier-1 anchor: the fixture case
ANCHOR_NAME = "Walking Dead"
ANCHOR_TAG = "tagEnemyZombieA01"
ANCHOR_RECORD = "records/creatures/enemies/zombie_a01.dbr"
ANCHOR_BIO = "records/creatures/enemies/bios/bio_zombie_01.dbr"
# TWO anchor scopes. The probe's 17-candidate / 15-bio-support figures are for `database.arz`
# ALONE ("carried by 17 distinct Monster records in database.arz"). This bridge spans all four
# archives, where the same tag reaches 25 records (17 base + 6 gdx1 + 2 gdx2). Both are asserted:
# the base-only pair is the reproduction of legolas's claim, the edition-wide pair is what the
# bridge actually serves. Asserting only one would either fail a correct probe or hide a scope
# difference behind a matching number.
ORACLE_ANCHOR_BASE_CANDIDATES = 17    # probe §4, database.arz only
ORACLE_ANCHOR_BASE_BIO_SUPPORT = 15   # probe §4 "15 of the 17"
ORACLE_ANCHOR_CANDIDATES = 25         # edition-wide (base+gdx1+gdx2)
ORACLE_ANCHOR_BIO_SUPPORT = 23        # edition-wide

CERTIFIED_SET = "L0-gd-s3-set1"

# ---- tiebreak penalty table (rule v1)
SEGMENT_PENALTY = [("records/sandbox/", 100), ("/special/", 90), ("/boss&quest/", 80),
                   ("/npcs/", 70)]
STEM_SUFFIX_PENALTY = [("_summon", 40), ("_starter", 40), ("_doa", 40)]
STEM_CONTAINS_PENALTY = [("dropper", 40)]

BRIDGE_DDL = """
CREATE TABLE IF NOT EXISTS gd_monster_tiebreak (
    record_path     TEXT NOT NULL,
    source_file     TEXT NOT NULL,
    penalty_score   INTEGER NOT NULL,
    penalty_reasons TEXT NOT NULL,
    dir_depth       INTEGER NOT NULL,
    stem_len        INTEGER NOT NULL,
    rule_version    TEXT NOT NULL,
    schema_version  TEXT NOT NULL,
    created_date    TEXT NOT NULL,
    PRIMARY KEY (record_path, source_file)
);

-- LAYER 1: the RAW fan-out. One row per (display_name, candidate record). Nothing collapsed.
DROP VIEW IF EXISTS v_gd_monster_bridge;
CREATE VIEW v_gd_monster_bridge AS
SELECT
    r.display_name,
    r.description_tag,
    r.display_name_tag_domain,
    r.record_path,
    r.source_file,
    r.expansion,
    r.monster_classification,
    r.race_display,
    r.bio_record,
    COUNT(*) OVER (PARTITION BY r.display_name) AS candidate_count,
    -- COUNT(DISTINCT …) OVER … is unsupported in SQLite; a correlated count over the
    -- display_name index is the equivalent and is what makes the bio collapse visible per row.
    (SELECT COUNT(DISTINCT r2.bio_record) FROM gd_monster_record r2
      WHERE r2.display_name = r.display_name AND r2.bio_record IS NOT NULL)
        AS distinct_bio_count,
    t.penalty_score,
    t.penalty_reasons,
    ROW_NUMBER() OVER (PARTITION BY r.display_name
                       ORDER BY t.penalty_score, t.dir_depth, t.stem_len, r.record_path)
        AS tiebreak_rank,
    t.rule_version
FROM gd_monster_record r
LEFT JOIN gd_monster_tiebreak t
       ON t.record_path = r.record_path AND t.source_file = r.source_file
WHERE r.display_name IS NOT NULL;

-- LAYER 2b: the bio collapse, as its own named fact. The MODE of bio_record across a display
-- name's candidates, with its support count. This is the answer a statline prediction wants.
DROP VIEW IF EXISTS v_gd_monster_bio_modal;
CREATE VIEW v_gd_monster_bio_modal AS
SELECT display_name, bio_record AS modal_bio_record, n AS modal_bio_support
FROM (
    SELECT display_name, bio_record, COUNT(*) AS n,
           ROW_NUMBER() OVER (PARTITION BY display_name
                              ORDER BY COUNT(*) DESC, bio_record) AS rk
    FROM gd_monster_record
    WHERE display_name IS NOT NULL AND bio_record IS NOT NULL
    GROUP BY display_name, bio_record)
WHERE rk = 1;

-- LAYER 3: one row per display name. Carries the tiebreak winner AND the ambiguity beside it,
-- so a consumer reading only this view still cannot fail to see the fan-out.
DROP VIEW IF EXISTS v_gd_monster_bridge_preferred;
CREATE VIEW v_gd_monster_bridge_preferred AS
SELECT b.display_name,
       b.description_tag,
       b.record_path      AS preferred_record,
       b.source_file      AS preferred_source_file,
       b.bio_record       AS preferred_bio_record,
       b.monster_classification,
       b.race_display,
       b.candidate_count,
       b.distinct_bio_count,
       m.modal_bio_record,
       m.modal_bio_support,
       b.penalty_score    AS preferred_penalty_score,
       b.rule_version
FROM v_gd_monster_bridge b
LEFT JOIN v_gd_monster_bio_modal m ON m.display_name = b.display_name
WHERE b.tiebreak_rank = 1;
"""

FIXTURES_V02_DDL = [
    ("fixture_set", "monster_record_candidates", "TEXT"),
    ("fixture_set", "monster_bio_record", "TEXT"),
    ("fixture_set", "monster_rank", "TEXT"),
    ("fixture_set", "monster_race", "TEXT"),
    ("fixture_set", "monster_record_method", "TEXT"),
    ("fixture_set", "monster_record_evidence", "TEXT"),
    ("measure_dict", "off_trial_semantics", "TEXT"),
]

# `off_trial_semantics` seed — v0.1 §7 item 1. `v_ledger_continuity` flags `life_healed` as
# DISCONTINUOUS between every trial pair, correctly and uselessly: regeneration legitimately
# accrues off-trial. The analyst supplied that judgment by hand; it belongs in the dictionary.
OFF_TRIAL = {
    "kills": "must-not-advance", "skill_use_count": "must-not-advance",
    "deaths": "must-not-advance", "health_potions_used": "must-not-advance",
    "mana_potions_used": "must-not-advance", "max_level_achieved": "must-not-advance",
    "life_healed": "may-advance", "play_time": "may-advance",
    "hp_current": "may-advance", "total_score": "may-advance",
    "hp_max": "invariant-within-character", "shield_block_chance": "invariant-within-character",
    "fight_seconds": "trial-scoped", "hp_cost_band": "trial-scoped",
    "hp_cost_abs": "trial-scoped", "dps_field": "trial-scoped",
    "capture_latency": "trial-scoped",
}


def tiebreak(record_path):
    score, reasons = 0, []
    for seg, pen in SEGMENT_PENALTY:
        if seg in "/" + record_path:
            score += pen
            reasons.append(f"{seg}+{pen}")
    stem = record_path.rsplit("/", 1)[-1]
    stem = stem[:-4] if stem.endswith(".dbr") else stem
    for suf, pen in STEM_SUFFIX_PENALTY:
        if stem.endswith(suf):
            score += pen
            reasons.append(f"*{suf}+{pen}")
    for sub, pen in STEM_CONTAINS_PENALTY:
        if sub in stem:
            score += pen
            reasons.append(f"*{sub}*+{pen}")
    depth = record_path.count("/")
    return score, ";".join(reasons) or "none", depth, len(stem)


# ============================================================ corpus side
def build_bridge(con):
    """Create the tiebreak table + the three bridge views, and land the tiebreak rows."""
    rows = con.execute("SELECT record_path, source_file FROM gd_monster_record").fetchall()
    if not rows:
        raise SystemExit("HALT — gd_monster_record is empty. Run M2 first.")
    tb = [(rp, sf) + tiebreak(rp) + (TIEBREAK_RULE_VERSION, SCHEMA_VERSION, RUN_DATE)
          for rp, sf in rows]
    con.executescript(BRIDGE_DDL)
    con.execute("DELETE FROM gd_monster_tiebreak")
    con.executemany("INSERT INTO gd_monster_tiebreak VALUES (" + ",".join("?" * 9) + ")", tb)
    con.commit()
    return tb


def bridge_gates(con):
    print("G5 — BRIDGE FAN-OUT")
    tot = con.execute("SELECT COUNT(*) FROM v_gd_monster_bridge").fetchone()[0]
    names = con.execute("SELECT COUNT(*) FROM v_gd_monster_bridge_preferred").fetchone()[0]
    print(f"    bridge candidate rows       : {tot}")
    print(f"    distinct display names      : {names}")

    dist = con.execute(
        "SELECT candidate_count, COUNT(DISTINCT display_name) FROM v_gd_monster_bridge "
        "GROUP BY 1 ORDER BY 1").fetchall()
    one = sum(n for c, n in dist if c == 1)
    many = sum(n for c, n in dist if c > 1)
    print(f"    display names with EXACTLY ONE candidate : {one} ({one / names:.1%})")
    print(f"    display names that FAN OUT (>1 candidate): {many} ({many / names:.1%})")
    print(f"    fan-out histogram (candidates: names): "
          f"{ {c: n for c, n in dist} }")

    worst = con.execute(
        "SELECT display_name, candidate_count, distinct_bio_count, modal_bio_support "
        "FROM v_gd_monster_bridge_preferred ORDER BY candidate_count DESC LIMIT 8").fetchall()
    print("    worst fan-outs (name, candidates, distinct bios, modal-bio support):")
    for w in worst:
        print(f"        {w}")

    collapse = con.execute(
        "SELECT COUNT(*) FROM v_gd_monster_bridge_preferred "
        "WHERE candidate_count > 1 AND distinct_bio_count = 1").fetchone()[0]
    print(f"\n    fan-out names whose candidates ALL share ONE bio (record ambiguity, "
          f"statline certainty): {collapse} / {many}")

    print("\nG6 — TIER-1 ANCHOR (the fixture case)")
    cands = con.execute(
        "SELECT record_path, source_file, bio_record, penalty_score, penalty_reasons, "
        "tiebreak_rank FROM v_gd_monster_bridge WHERE display_name = ? ORDER BY tiebreak_rank",
        (ANCHOR_NAME,)).fetchall()
    print(f"    '{ANCHOR_NAME}' candidates = {len(cands)} (oracle {ORACLE_ANCHOR_CANDIDATES})")
    for c in cands:
        mark = " <== PREFERRED" if c[5] == 1 else ""
        print(f"        [{c[5]:2d}] pen={c[3]:3d} {c[0]:62s} bio={(c[2] or '')[-24:]:24s}"
              f"{mark}")
    pref = con.execute(
        "SELECT preferred_record, preferred_bio_record, candidate_count, distinct_bio_count, "
        "modal_bio_record, modal_bio_support FROM v_gd_monster_bridge_preferred "
        "WHERE display_name = ?", (ANCHOR_NAME,)).fetchone()
    print(f"\n    preferred_record   = {pref[0]}")
    print(f"    preferred_bio      = {pref[1]}")
    print(f"    candidate_count    = {pref[2]} (oracle {ORACLE_ANCHOR_CANDIDATES})")
    print(f"    distinct_bio_count = {pref[3]}")
    print(f"    modal_bio          = {pref[4]}  support={pref[5]} "
          f"(oracle {ORACLE_ANCHOR_BIO_SUPPORT})")
    base_n, base_sup = con.execute(
        "SELECT COUNT(*), SUM(bio_record = ?) FROM gd_monster_record "
        "WHERE description_tag = ? AND source_file = 'database.arz'",
        (ANCHOR_BIO, ANCHOR_TAG)).fetchone()
    print(f"\n    PROBE-SCOPE REPRODUCTION (database.arz only)")
    print(f"    candidates    = {base_n} (oracle {ORACLE_ANCHOR_BASE_CANDIDATES})")
    print(f"    bio support   = {base_sup} (oracle {ORACLE_ANCHOR_BASE_BIO_SUPPORT})")
    per_archive = con.execute(
        "SELECT source_file, COUNT(*) FROM gd_monster_record WHERE description_tag = ? "
        "GROUP BY 1 ORDER BY 1", (ANCHOR_TAG,)).fetchall()
    print(f"    per-archive   = {dict(per_archive)}\n")

    bad = 0
    for label, got, expect in (("preferred_record", pref[0], ANCHOR_RECORD),
                               ("base candidate_count (probe scope)", base_n,
                                ORACLE_ANCHOR_BASE_CANDIDATES),
                               ("base bio support (probe scope)", base_sup,
                                ORACLE_ANCHOR_BASE_BIO_SUPPORT),
                               ("candidate_count", pref[2], ORACLE_ANCHOR_CANDIDATES),
                               ("modal_bio_record", pref[4], ANCHOR_BIO),
                               ("modal_bio_support", pref[5], ORACLE_ANCHOR_BIO_SUPPORT)):
        good = got == expect
        bad += not good
        print(f"    {'PASS' if good else 'FAIL'} {label}")
    if bad:
        raise SystemExit("HALT — the fixture-case anchor did not reproduce.")
    return cands, pref


# ============================================================ fixtures side
def apply_fixtures(cands, pref, race_display, rank):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak = FIXTURES.with_name(FIXTURES.name + f".pre-v0.2-{ts}-backup")
    shutil.copy2(FIXTURES, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    bak.with_name(bak.name + ".md5.txt").write_text(f"{md5}  {bak.name}\n")
    print(f"\nBACKUP {bak.name} md5={md5}")

    con = sqlite3.connect(FIXTURES)
    con.execute("PRAGMA foreign_keys=ON")
    existing = {t: {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
                for t in ("fixture_set", "measure_dict")}
    try:
        con.execute("BEGIN")
        for table, col, typ in FIXTURES_V02_DDL:
            if col in existing[table]:
                print(f"    ALTER skipped (already present): {table}.{col}")
                continue
            con.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
            print(f"    ALTER TABLE {table} ADD COLUMN {col} {typ}")

        for k, v in OFF_TRIAL.items():
            con.execute("UPDATE measure_dict SET off_trial_semantics=? WHERE measure_key=?",
                        (v, k))

        candidate_json = json.dumps(
            [{"record_path": c[0], "source_file": c[1], "bio_record": c[2],
              "penalty_score": c[3], "tiebreak_rank": c[5]} for c in cands],
            separators=(",", ":"))
        evidence = (
            "TWO-HOP TAG BRIDGE, both hops banked and re-derivable. "
            "hop 1: corpus.db monster_display_tag -> tagEnemyZombieA01 = 'Walking Dead' "
            "(tags_creatures.txt, resources/Text_EN.arc, sha256 613457c8df72fe5a…, edition "
            "gd-edition-II-20260724). UNIQUE in the string direction: exactly one of the 2,060 "
            "creature tag keys yields 'Walking Dead'. "
            "hop 2: corpus.db gd_monster_record -> 17 Monster records carry that description. "
            "The 17 are banked verbatim in monster_record_candidates; monster_record holds the "
            "path-structure-v1 tiebreak winner and is therefore a HEURISTIC, not an attestation. "
            "CONVERGENT SUPPORT (not proof): Matt's round-2 console note records "
            "`game.Spawn \"records/creatures/enemies/zombie_a01.dbr\"` succeeding — an "
            "independent live-oracle confirmation that this exact path is the canonical spawnable "
            "zombie. It is convergent, NOT attesting, because the spawn happened in session "
            "gd-live-2026-07-25-s2 under a separate heading from any trial, while THIS set is the "
            "round-3 world spawn in Vicinity of The Coffinmakers. "
            "WHAT IS ACTUALLY CERTAIN: the statline. 15 of the 17 candidates resolve to "
            "bio_zombie_01.dbr, so the 17-way record ambiguity collapses to a 1-way bio answer. "
            "monster_bio_record is the column a statline prediction should join on. "
            "STILL OPEN: which specific record a world spawn instantiates is decided by "
            "Levels.arc / Level Art.arc spawn tables, which are NOT parsed. "
            "monster_identity_method is UNCHANGED at 'screenshot-nameplate' — the nameplate "
            "attestation is what certified this set and must not be overwritten by a bridge "
            "inference.")
        n = con.execute(
            "UPDATE fixture_set SET monster_record=?, monster_record_candidates=?, "
            "monster_bio_record=?, monster_rank=?, monster_race=?, monster_record_method=?, "
            "monster_record_evidence=? WHERE fixture_set_id=?",
            (ANCHOR_RECORD, candidate_json, ANCHOR_BIO, rank, race_display,
             "tag-bridge-inferred+spawn-command-convergent", evidence, CERTIFIED_SET)).rowcount
        print(f"    fixture_set rows updated: {n} ({CERTIFIED_SET})")

        # The round-2 sets stay NULL on monster_record BY DESIGN. The spawn command attests the
        # RECORD, not that those trials fought it; O-8 admits NULL identity and the certified view
        # already excludes them. Writing the record there would launder an assumption into a fact.
        con.commit()
    except Exception:
        con.rollback()
        raise
    print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
    print("fk_check :", con.execute("PRAGMA foreign_key_check").fetchall() or "clean")
    cert = con.execute("SELECT COUNT(*) FROM v_fixture_bank_certified").fetchone()[0]
    print(f"    v_fixture_bank_certified rows still: {cert}")
    row = con.execute(
        "SELECT monster_display_name, monster_record, monster_bio_record, monster_rank, "
        "monster_race, monster_identity_method, monster_record_method FROM fixture_set "
        "WHERE fixture_set_id=?", (CERTIFIED_SET,)).fetchone()
    print(f"    certified row now: {row}")
    print(f"    measure_dict off_trial_semantics populated: "
          f"{con.execute('SELECT COUNT(*) FROM measure_dict WHERE off_trial_semantics IS NOT NULL').fetchone()[0]}/17")
    con.close()


def main():
    verify_only = "--verify-only" in sys.argv
    # --verify-only exercises the REAL views against the REAL data, on a throwaway COPY of the
    # store. SQLite's executescript() commits, so a rollback-based dry run would be a lie;
    # a copy is honest and costs a second.
    target = CORPUS
    if verify_only:
        target = CORPUS.with_name("_verify_only_scratch.db")
        shutil.copy2(CORPUS, target)
    con = sqlite3.connect(target)
    tb = build_bridge(con)
    cands, pref = bridge_gates(con)
    if verify_only:
        con.close()
        target.unlink()
        print("\n--verify-only: scratch copy discarded; NO writes to either store.")
        return
    con.execute(
        "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
        (SCHEMA_VERSION + "/M3",
         datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
         "GD display-name bridge M3 (elrond). ADDITIVE: gd_monster_tiebreak "
         f"({len(tb)} rows, rule {TIEBREAK_RULE_VERSION}) + views v_gd_monster_bridge (RAW "
         "one-to-many fan-out, nothing collapsed) and v_gd_monster_bridge_preferred (tiebreak "
         "winner + candidate_count + distinct_bio_count + modal bio and its support). The "
         "heuristic lives in its own table beside the fan-out, never inside it. Anchor: "
         "'Walking Dead' -> 17 candidates -> zombie_a01.dbr preferred, 15/17 collapse to "
         "bio_zombie_01.dbr."))
    con.commit()
    race, rank = con.execute(
        "SELECT race_display, monster_classification FROM gd_monster_record WHERE record_path=?",
        (ANCHOR_RECORD,)).fetchone()
    con.close()
    apply_fixtures(cands, pref, race, rank)


if __name__ == "__main__":
    main()
