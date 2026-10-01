#!/usr/bin/env python3
"""JOIN-1 J0 corpus.db migration (elrond, 2026-10-01): GD-SLICE freeze-not-drop, plus the docket-sweep ledger.

Charter: agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md v0.5, section 5, J0 elrond row.
Ruled:   J-L4 (Matt, 2026-09-29, KC2-PLAY KP-110) approves the additive schema change.
         J-L1 (same ruling) approves the rule "Q86 supersedes any pre-union permanent-gap-record that
         closed a kit-internal mechanism", with docket 5 re-dispositioned first.
MIGRATION entry: research/curated/MIGRATION.md, "join1-j0-2026-10-01".

M1 (GD-SLICE) on exact_skill_field. ADDITIVE ONLY: no column dropped, no existing value rewritten.
  * vocab_scope      in {neutral, game_named}. Mechanical: game_named iff canon_key starts with
                     '<g>_' for g in the corpus's own game codes (SELECT DISTINCT game FROM canon_corpus).
  * boundary_class   in {internal, boundary, out_of_arena, unresolved}. Mechanical: the FIRST rule (by
                     rule_order) of the committed rule table research/curated/gd-slice-boundary-class-rules-
                     2026-10-01.csv whose GLOB matches canon_key. The rule that fired is stored in
                     boundary_class_rule, so every row is traceable to one auditable line.
  * boundary_class_rule  the rule_id that fired.
  * mechanism_grade / magnitude_grade  constrained to the era-substrate LAW section 4 vocabulary. Mechanical:
                     both INHERIT the header's exact_skill.fidelity_grade, because every exact_skill_field row
                     is a decoded value of its header's record (mechanism and magnitude come from one source;
                     on this table the P0 section 7.3 split is structurally degenerate). PRECONDITION: the GV
                     remedy (join1_j0_gv_relabel_2026_10_01.py) has landed, so no header still says MEASURED;
                     the run aborts otherwise rather than copy the defect into two new columns.
  * is_core          FROZEN, not dropped: a BEFORE UPDATE OF is_core trigger aborts any rewrite.
  * table boundary_class_rule (the rule CSV, loaded verbatim) + view v_exact_skill_field_class_audit
    (rows whose stored derived columns disagree with a fresh derivation; expected EMPTY) + an AFTER
    INSERT trigger that derives both columns for new rows, so the derivation cannot drift.

M2 (docket sweep) on mechanic_gap_docket.
  * table docket_disposition_sweep: one row per docket swept (all 63 rows of the table are screened;
    the 17 the charter names, plus dockets 2 and 6, carry a verdict; the other 44 are screened as non-closures); the prior disposition is preserved on every row.
  * docket 5 ONLY: disposition 'permanent-gap-record' -> 'superseded-by-q86' (Matt-ruled instance), with
    the prior value written into provenance_json.q86_supersession. No other docket row is written. The
    further hits go to Matt as ONE batch (elrond/notes/2026-10-01-join1-j0-docket-sweep.md section 3)
    and are recorded here as PROPOSED, not applied.

Modes:
  --mode dry-run (default)  copies corpus.db into MEMORY (sqlite backup API), applies M1+M2 there and runs
                            every audit. ZERO bytes written to disk.
  --mode apply              refuses to run while free disk < 40 GiB (charter section 6 HALT boundary),
                            writes a file backup, applies in one transaction, then re-runs the audits.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                     # agentic_orchestration/research
DB = ROOT / "curated" / "corpus.db"
RULES_CSV = ROOT / "curated" / "gd-slice-boundary-class-rules-2026-10-01.csv"
VERSION = "join1-j0-2026-10-01"
HALT_FREE_GIB = 40.0
GRADES = ("MEASURED", "DATAMINED", "MODEL-VERIFIED", "AUTHORED")

# --------------------------------------------------------------------------------------------------
# M2 sweep verdicts. Test: (T1) is the disposition a pre-union `permanent-gap-record`? (T2) is the
# mechanism kit-internal (P0 method)? Both -> a hit. Docket 5 is the Matt-ruled instance.
# --------------------------------------------------------------------------------------------------
SWEEP = [
    # docket, q86_class, verdict, batch_item, reason
    (1, "mixed", "UNTOUCHED-NOT-CLOSED", None,
     "engine-design-intake is open, not closed (T1 no). Mixed: kit-internal consumption of entities, some world-produced (corpses, hostile fodder). Q86 consequence (info): the D-4.2 'declare permanently approximated' branch is foreclosed for the kit-internal sub-shapes when a member kit joins."),
    (2, "world_shape", "UNTOUCHED-BOUNDARY-OR-WORLD-SHAPE", "M-3 (secondary clause only)",
     "permanent-gap-record over party scope in a solo engine: world shape, named untouched by J-L1. Its SECONDARY clause (source reserves ~100% vs the LOCKED reservation_percent 0.75 cap, clamped in-map) is a kit-internal value under a LOCKED engine guard: routed to Matt as scope question M-3, not re-dispositioned."),
    (3, "kit_internal", "PROPOSED-SUPERSEDED-BY-Q86", "M-1",
     "permanent-gap-record (T1 yes) over per-hit/per-entity random element from a fixed pool: the kit decides the element; the boundary only reads the resulting family tag (B8), as for any packet (T2 yes). HIT. The docket's preserved prunable=build / unprunable=trap distinction must survive. Corrigendum: P0 7.5 listed docket 3 as engine-design-intake; it is permanent-gap-record."),
    (4, "mixed", "UNTOUCHED-NOT-CLOSED", None,
     "Compound. DECLARE half (stun magnitude as damage source) is engine-design-intake: open (T1 no). COLLISION half (the anti-stunlock floor) is working-as-intended over CC on monsters: BOUNDARY, untouched by J-L1 whatever its disposition; when a stun kit joins it is a monster-CC lever question (P0 7.1), not a docket re-disposition."),
    (5, "kit_internal", "SUPERSEDED-BY-Q86", None,
     "Matt-ruled instance (J-L1, 2026-09-29, KP-110): permanent-gap-record over self-damage cast cost redirected to a proxy life pool, a kit-internal resource law. APPLIED by this migration; prior disposition preserved."),
    (6, "ambiguous", "SCOPE-QUESTION", "M-3",
     "Outside the charter's named list; screened because the sweep covers the whole table. working-as-intended: the closed-loop self-damage trigger economy collides with MAX_CHAIN_DEPTH=1 LOCKED ('the guard IS the design'). Trigger and proc machinery is kit-internal under Q86, but a chain-depth cap applied to every kit reads as a shared (boundary) rule. Not a permanent-gap-record (T1 no), so J-L1 does not reach it literally. Routed as scope question M-3."),
    (7, "mixed", "UNTOUCHED-NOT-CLOSED", None,
     "engine-design-intake: open (T1 no). Capture-from-world reads the world roster (world shape); ability inheritance is kit-internal once captured."),
    (8, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "engine-design-intake: open (T1 no). Kit-internal (a stat counts the army). Q86 consequence (info): the D-4.2 'declare flavour-only' branch is foreclosed when the kit joins."),
    (9, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] summoner-deferral: engine-design-intake after D-5 un-deferral: open (T1 no). Consistent with Q86."),
    (10, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] stat-as-damage-substrate: engine-design-intake: open (T1 no). The 6-way DO-NOT-MERGE split stands. Its stun-substrate member is docket 4's declare half."),
    (11, "mixed", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] spatial-consumable-resource-node: engine-design-intake (sibling of docket 1): open (T1 no)."),
    (12, "world_shape", "UNTOUCHED-BOUNDARY-OR-WORLD-SHAPE", None,
     "[5.2 FAMILY] support-party-scope: permanent-gap-record over party scope: world shape, named untouched by J-L1. P0 7.4 (Battle Orders allies) is consistent with it."),
    (13, "out_of_arena", "UNTOUCHED-OUT-OF-ARENA", None,
     "[5.2 FAMILY] loot-economy-identity: permanent-out-of-scope (T1 no; not a fight mechanism, T2 no). Agrees with P0 7.2 OUT-OF-ARENA."),
    (14, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] mode-swap-identity: hold is not a closure (T1 no). GX-02 form-swap adjacents."),
    (15, "mixed", "SCOPE-QUESTION", "M-2",
     "[5.2 FAMILY] roguelite-idiom: permanent-genre-law-record, 'no engine action', is a CLOSING disposition, but not literally permanent-gap-record (T1 literal no). Members split: kit-internal (self-cost-contract, finite-ammo-burst, duo-boon-pair) vs boundary (delayed-detonation Doom and per-arrow-status are status on monsters; deflect is hit resolution). Routed as scope question M-2."),
    (16, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] minion-consumption-harvest: standing-family-record names an evidenced family; it does not close one (T1 no)."),
    (17, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] recipe-combination-determines-output: standing-family-record; not a closure (T1 no)."),
    (18, "kit_internal", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] gear-stat-as-minion-scaling: standing-family-record; not a closure (T1 no)."),
    (19, "mixed", "UNTOUCHED-NOT-CLOSED", None,
     "[5.2 FAMILY] held-singletons: hold is not a closure (T1 no). Cross-reference: member 'utility-transport teleport-sorc' is the Teleport row excluded from J-S3b (a B7 boundary item for a later kit)."),
]
NAMED = {1, 3, 4, 5, 7, 8} | set(range(9, 20))


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def free_gib(path: Path) -> float:
    st = os.statvfs(path)
    return st.f_bavail * st.f_frsize / (1024 ** 3)


def load_rules():
    with open(RULES_CSV, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        assert r["boundary_class"] in ("internal", "boundary", "out_of_arena", "unresolved"), r
    orders = [int(r["rule_order"]) for r in rows]
    assert len(set(orders)) == len(orders), "rule_order must be unique"
    return rows


def table_hash(con, sql):
    h = hashlib.sha256()
    for row in con.execute(sql):
        h.update(repr(row).encode())
    return h.hexdigest()


ESF_ORIG_COLS = ("entity_id, canon_key, rank, canon_value, canon_unit, raw_field, raw_value, field_kind, "
                 "field_family, is_core, canon_key_provenance, monotonic_class, monotonic_dir, source_file, "
                 "record_path, schema_version, created_date")
DERIVE_VOCAB = ("CASE WHEN EXISTS (SELECT 1 FROM (SELECT DISTINCT game FROM canon_corpus) g "
                "WHERE {k} GLOB g.game || '_*') THEN 'game_named' ELSE 'neutral' END")
DERIVE_CLASS = ("(SELECT r.boundary_class FROM boundary_class_rule r WHERE {k} GLOB r.glob "
                "ORDER BY r.rule_order LIMIT 1)")
DERIVE_RULE = ("(SELECT r.rule_id FROM boundary_class_rule r WHERE {k} GLOB r.glob "
               "ORDER BY r.rule_order LIMIT 1)")
DERIVE_GRADE = "(SELECT s.fidelity_grade FROM exact_skill s WHERE s.entity_id = {e})"


def migrate(con, rules, rules_sha, applied_utc):
    cur = con.cursor()
    pre = {
        "esf_rows": cur.execute("SELECT count(*) FROM exact_skill_field").fetchone()[0],
        "esf_hash": table_hash(con, f"SELECT {ESF_ORIG_COLS} FROM exact_skill_field ORDER BY entity_id, canon_key, rank"),
        "is_core_hash": table_hash(con, "SELECT entity_id, canon_key, rank, is_core FROM exact_skill_field ORDER BY 1,2,3"),
        "docket_hash_not5": table_hash(con, "SELECT * FROM mechanic_gap_docket WHERE docket_id<>5 ORDER BY docket_id"),
        "docket5": cur.execute("SELECT status, disposition, provenance_json FROM mechanic_gap_docket WHERE docket_id=5").fetchone(),
        "dockets": cur.execute("SELECT docket_id, status, disposition FROM mechanic_gap_docket ORDER BY docket_id").fetchall(),
    }
    cols = {r[1] for r in cur.execute("PRAGMA table_info(exact_skill_field)")}
    if "vocab_scope" in cols or "boundary_class" in cols:
        raise SystemExit("ABORT: exact_skill_field already carries the J0 columns (migration already applied?)")
    stale = cur.execute("SELECT count(*) FROM exact_skill WHERE fidelity_grade='MEASURED'").fetchone()[0]
    if stale:
        raise SystemExit(f"ABORT: {stale} exact_skill headers still say MEASURED; the GV remedy must land first")
    if pre["docket5"][1] != "permanent-gap-record":
        raise SystemExit(f"ABORT: docket 5 disposition is {pre['docket5'][1]!r}, expected 'permanent-gap-record'")

    cur.execute("BEGIN")
    # ---- M1 ------------------------------------------------------------------------------------
    cur.execute("""CREATE TABLE boundary_class_rule (
        rule_order     INTEGER PRIMARY KEY,
        rule_id        TEXT NOT NULL,
        glob           TEXT NOT NULL,
        boundary_class TEXT NOT NULL CHECK (boundary_class IN ('internal','boundary','out_of_arena','unresolved')),
        q86_item       TEXT,
        basis          TEXT NOT NULL,
        flag           TEXT,
        source_csv     TEXT NOT NULL,
        source_csv_sha256 TEXT NOT NULL)""")
    cur.executemany(
        "INSERT INTO boundary_class_rule VALUES (?,?,?,?,?,?,?,?,?)",
        [(int(r["rule_order"]), r["rule_id"], r["glob"], r["boundary_class"], r["q86_item"] or None,
          r["basis"], r["flag"] or None, RULES_CSV.name, rules_sha) for r in rules])
    cur.execute("ALTER TABLE exact_skill_field ADD COLUMN vocab_scope TEXT "
                "CHECK (vocab_scope IS NULL OR vocab_scope IN ('neutral','game_named'))")
    cur.execute("ALTER TABLE exact_skill_field ADD COLUMN boundary_class TEXT "
                "CHECK (boundary_class IS NULL OR boundary_class IN ('internal','boundary','out_of_arena','unresolved'))")
    cur.execute("ALTER TABLE exact_skill_field ADD COLUMN boundary_class_rule TEXT")
    glist = ",".join(f"'{g}'" for g in GRADES)
    cur.execute(f"ALTER TABLE exact_skill_field ADD COLUMN mechanism_grade TEXT "
                f"CHECK (mechanism_grade IS NULL OR mechanism_grade IN ({glist}))")
    cur.execute(f"ALTER TABLE exact_skill_field ADD COLUMN magnitude_grade TEXT "
                f"CHECK (magnitude_grade IS NULL OR magnitude_grade IN ({glist}))")
    k = "exact_skill_field.canon_key"
    e = "exact_skill_field.entity_id"
    cur.execute(f"UPDATE exact_skill_field SET vocab_scope = {DERIVE_VOCAB.format(k=k)}, "
                f"boundary_class = {DERIVE_CLASS.format(k=k)}, boundary_class_rule = {DERIVE_RULE.format(k=k)}, "
                f"mechanism_grade = {DERIVE_GRADE.format(e=e)}, magnitude_grade = {DERIVE_GRADE.format(e=e)}")
    cur.execute("""CREATE TRIGGER trg_esf_is_core_frozen BEFORE UPDATE OF is_core ON exact_skill_field
        BEGIN SELECT RAISE(ABORT, 'exact_skill_field.is_core is FROZEN (join1-j0-2026-10-01, J-L4): a pre-Q86 TSR-2 artifact, preserved not dropped. Read boundary_class / vocab_scope.'); END""")
    n = "NEW.canon_key"
    cur.execute(f"""CREATE TRIGGER trg_esf_derive_on_insert AFTER INSERT ON exact_skill_field
        BEGIN UPDATE exact_skill_field SET vocab_scope = {DERIVE_VOCAB.format(k=n)},
              boundary_class = {DERIVE_CLASS.format(k=n)}, boundary_class_rule = {DERIVE_RULE.format(k=n)},
              mechanism_grade = {DERIVE_GRADE.format(e="NEW.entity_id")},
              magnitude_grade = {DERIVE_GRADE.format(e="NEW.entity_id")}
              WHERE rowid = NEW.rowid; END""")
    f = "f.canon_key"
    cur.execute(f"""CREATE VIEW v_exact_skill_field_class_audit AS
        SELECT f.entity_id, f.canon_key, f.rank,
               f.vocab_scope, {DERIVE_VOCAB.format(k=f)} AS vocab_scope_derived,
               f.boundary_class, {DERIVE_CLASS.format(k=f)} AS boundary_class_derived,
               f.boundary_class_rule, {DERIVE_RULE.format(k=f)} AS boundary_class_rule_derived,
               f.mechanism_grade, f.magnitude_grade, {DERIVE_GRADE.format(e="f.entity_id")} AS header_grade
          FROM exact_skill_field f
         WHERE f.vocab_scope IS NOT {DERIVE_VOCAB.format(k=f)}
            OR f.boundary_class IS NOT {DERIVE_CLASS.format(k=f)}
            OR f.boundary_class_rule IS NOT {DERIVE_RULE.format(k=f)}
            OR f.mechanism_grade IS NOT {DERIVE_GRADE.format(e="f.entity_id")}
            OR f.magnitude_grade IS NOT {DERIVE_GRADE.format(e="f.entity_id")}""")
    # ---- M2 ------------------------------------------------------------------------------------
    cur.execute("""CREATE TABLE docket_disposition_sweep (
        sweep_id          TEXT NOT NULL,
        docket_id         INTEGER NOT NULL REFERENCES mechanic_gap_docket(docket_id),
        named_in_charter  INTEGER NOT NULL CHECK (named_in_charter IN (0,1)),
        prior_status      TEXT,
        prior_disposition TEXT,
        q86_class         TEXT CHECK (q86_class IN ('kit_internal','boundary','world_shape','out_of_arena','mixed','ambiguous','not_assessed')),
        verdict           TEXT NOT NULL CHECK (verdict IN ('SUPERSEDED-BY-Q86','PROPOSED-SUPERSEDED-BY-Q86','SCOPE-QUESTION',
                                   'UNTOUCHED-NOT-CLOSED','UNTOUCHED-BOUNDARY-OR-WORLD-SHAPE','UNTOUCHED-OUT-OF-ARENA','NOT-A-PRE-UNION-CLOSURE')),
        matt_batch_item   TEXT,
        applied           INTEGER NOT NULL CHECK (applied IN (0,1)),
        authority         TEXT NOT NULL,
        reason            TEXT NOT NULL,
        swept_date        TEXT NOT NULL,
        PRIMARY KEY (sweep_id, docket_id))""")
    prior = {d: (s, disp) for d, s, disp in pre["dockets"]}
    swept = {row[0] for row in SWEEP}
    rows = []
    for d, q, v, b, why in SWEEP:
        s, disp = prior[d]
        rows.append((VERSION, d, int(d in NAMED), s, disp, q, v, b, int(d == 5),
                     "J-L1 (Matt, 2026-09-29, KP-110) rule; elrond sweep" if d != 5 else
                     "J-L1 (Matt, 2026-09-29, KP-110): docket 5 ruled by name", why, "2026-10-01"))
    # Every other docket row: screened, not a pre-union closure of the rule's shape.
    for d, s, disp in pre["dockets"]:
        if d in swept:
            continue
        closing = disp in ("permanent-gap-record", "permanent-out-of-scope", "permanent-genre-law-record", "working-as-intended")
        assert not closing, f"docket {d} carries closing disposition {disp!r} but is not in SWEEP"
        rows.append((VERSION, d, 0, s, disp, "not_assessed", "NOT-A-PRE-UNION-CLOSURE", None, 0,
                     "elrond sweep (screen only)",
                     f"Screened: status {s!r}, disposition {disp!r} is not a closing disposition, so J-L1 has nothing to supersede. Mechanism class not assessed (outside the rule's reach).",
                     "2026-10-01"))
    cur.executemany("INSERT INTO docket_disposition_sweep VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    prov = json.loads(pre["docket5"][2] or "{}")
    prov["q86_supersession"] = {
        "prior_disposition": "permanent-gap-record",
        "new_disposition": "superseded-by-q86",
        "ruling": "J-L1 (Matt, 2026-09-29, KC2-PLAY ledger KP-110): Q86 supersedes any pre-union permanent-gap-record that closed a kit-internal mechanism; docket 5 first",
        "sweep": VERSION,
        "date": "2026-10-01",
        "effect": "The mechanism enters natively when a kit carrying it joins; no build is owed by this record.",
    }
    cur.execute("UPDATE mechanic_gap_docket SET disposition='superseded-by-q86', provenance_json=? WHERE docket_id=5",
                (json.dumps(prov, ensure_ascii=False),))
    cur.execute("INSERT INTO corpus_schema_meta(version, applied_utc, note) VALUES (?,?,?)", (
        VERSION, applied_utc,
        "JOIN-1 J0 (elrond; conductor gandalf; J-L4 + J-L1 ruled by Matt 2026-09-29, KP-110). ADDITIVE. "
        "M1 GD-SLICE: exact_skill_field +vocab_scope (mechanical from the key's game-code prefix), "
        "+boundary_class/+boundary_class_rule (mechanical: first GLOB match in boundary_class_rule, loaded from "
        f"{RULES_CSV.name} FILE sha256 {rules_sha}), +mechanism_grade/+magnitude_grade (mechanical: inherit the header "
        "exact_skill.fidelity_grade, post-GV DATAMINED). "
        "is_core FROZEN by trigger, not dropped. Audit view v_exact_skill_field_class_audit (expected empty). "
        "M2: docket_disposition_sweep (63 screened); docket 5 disposition permanent-gap-record -> superseded-by-q86 "
        "(prior preserved in provenance_json.q86_supersession). Further hits PROPOSED only (Matt batch)."))
    con.commit()
    return pre


def audit(con, pre, test_triggers):
    cur = con.cursor()
    out = {}
    out["esf_rows"] = cur.execute("SELECT count(*) FROM exact_skill_field").fetchone()[0]
    out["esf_rows_unchanged"] = out["esf_rows"] == pre["esf_rows"]
    out["orig_columns_byte_identical"] = table_hash(
        con, f"SELECT {ESF_ORIG_COLS} FROM exact_skill_field ORDER BY entity_id, canon_key, rank") == pre["esf_hash"]
    out["is_core_unchanged"] = table_hash(
        con, "SELECT entity_id, canon_key, rank, is_core FROM exact_skill_field ORDER BY 1,2,3") == pre["is_core_hash"]
    out["audit_view_rows"] = cur.execute("SELECT count(*) FROM v_exact_skill_field_class_audit").fetchone()[0]
    out["null_vocab"] = cur.execute("SELECT count(*) FROM exact_skill_field WHERE vocab_scope IS NULL").fetchone()[0]
    out["null_class"] = cur.execute("SELECT count(*) FROM exact_skill_field WHERE boundary_class IS NULL").fetchone()[0]
    out["grade_dist"] = cur.execute(
        "SELECT mechanism_grade, magnitude_grade, count(*) FROM exact_skill_field GROUP BY 1,2").fetchall()
    out["vocab_x_provenance"] = cur.execute(
        "SELECT vocab_scope, canon_key_provenance, count(DISTINCT canon_key), count(*) FROM exact_skill_field GROUP BY 1,2 ORDER BY 1,2").fetchall()
    out["vocab_x_is_core"] = cur.execute(
        "SELECT schema_version, is_core, vocab_scope, count(DISTINCT canon_key), count(*) FROM exact_skill_field GROUP BY 1,2,3 ORDER BY 1,2,3").fetchall()
    out["class_dist"] = cur.execute(
        "SELECT boundary_class, count(DISTINCT canon_key), count(*) FROM exact_skill_field GROUP BY 1 ORDER BY 1").fetchall()
    out["class_x_is_core"] = cur.execute(
        "SELECT boundary_class, is_core, count(DISTINCT canon_key), count(*) FROM exact_skill_field GROUP BY 1,2 ORDER BY 1,2").fetchall()
    out["rules_fired"] = cur.execute(
        "SELECT boundary_class_rule, count(DISTINCT canon_key), count(*) FROM exact_skill_field GROUP BY 1 ORDER BY 1").fetchall()
    out["rules_never_fired"] = [r[0] for r in cur.execute(
        "SELECT DISTINCT rule_id FROM boundary_class_rule WHERE rule_id NOT IN (SELECT DISTINCT boundary_class_rule FROM exact_skill_field) ORDER BY 1")]
    out["unresolved_keys"] = cur.execute(
        "SELECT canon_key, boundary_class_rule, count(*) FROM exact_skill_field WHERE boundary_class='unresolved' GROUP BY 1,2").fetchall()
    out["flagged_rule_rows"] = cur.execute(
        "SELECT r.rule_id, count(DISTINCT f.canon_key), count(*) FROM exact_skill_field f JOIN boundary_class_rule r "
        "ON r.rule_id=f.boundary_class_rule AND f.canon_key GLOB r.glob WHERE r.flag IS NOT NULL GROUP BY 1 ORDER BY 1").fetchall()
    out["docket_not5_unchanged"] = table_hash(
        con, "SELECT * FROM mechanic_gap_docket WHERE docket_id<>5 ORDER BY docket_id") == pre["docket_hash_not5"]
    out["docket5_now"] = cur.execute("SELECT status, disposition FROM mechanic_gap_docket WHERE docket_id=5").fetchone()
    out["docket5_prior_preserved"] = json.loads(cur.execute(
        "SELECT provenance_json FROM mechanic_gap_docket WHERE docket_id=5").fetchone()[0])["q86_supersession"]["prior_disposition"]
    out["sweep_rows"] = cur.execute("SELECT count(*) FROM docket_disposition_sweep").fetchone()[0]
    out["sweep_verdicts"] = cur.execute(
        "SELECT verdict, count(*), group_concat(docket_id) FROM docket_disposition_sweep GROUP BY 1 ORDER BY 1").fetchall()
    out["integrity"] = cur.execute("PRAGMA integrity_check").fetchone()[0]
    if test_triggers:   # in-memory only
        try:
            cur.execute("UPDATE exact_skill_field SET is_core = is_core WHERE rowid = (SELECT min(rowid) FROM exact_skill_field)")
            out["freeze_trigger"] = "FAILED: update was allowed"
        except sqlite3.DatabaseError as e:
            out["freeze_trigger"] = f"OK: aborted ({str(e)[:60]}...)"
        cur.execute("INSERT INTO exact_skill_field(entity_id, canon_key, rank, canon_value, raw_field, raw_value, field_kind, "
                    "source_file, record_path, schema_version) VALUES ('__probe__','gd_defensive_probe',0,1,'x',1,'static','x','x','probe')")
        cur.execute("INSERT INTO exact_skill_field(entity_id, canon_key, rank, canon_value, raw_field, raw_value, field_kind, "
                    "source_file, record_path, schema_version) VALUES ('__probe__','brand_new_key',0,1,'x',1,'static','x','x','probe')")
        out["insert_trigger"] = cur.execute(
            "SELECT canon_key, vocab_scope, boundary_class, boundary_class_rule, mechanism_grade FROM exact_skill_field WHERE entity_id='__probe__' ORDER BY 1").fetchall()
        con.rollback()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    a = ap.parse_args()
    rules = load_rules()
    rules_sha = sha256_file(RULES_CSV)
    applied_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"rules: {RULES_CSV.name} FILE sha256 {rules_sha} ({len(rules)} patterns)")
    print(f"corpus.db FILE sha256 (before): {sha256_file(DB)}")
    if a.mode == "dry-run":
        src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        con = sqlite3.connect(":memory:", isolation_level=None)
        src.backup(con)
        src.close()
        if con.execute("SELECT count(*) FROM exact_skill WHERE fidelity_grade='MEASURED'").fetchone()[0]:
            import join1_j0_gv_relabel_2026_10_01 as GV        # GV not yet on disk: land it in memory first
            gv_out, gv_ok = GV.run(con, applied_utc)
            print(f"GV remedy applied IN MEMORY first (precondition): {'PASS' if gv_ok else 'FAIL'}")
            if not gv_ok:
                sys.exit(1)
        pre = migrate(con, rules, rules_sha, applied_utc)
        res = audit(con, pre, test_triggers=True)
        print("MODE: dry-run (in memory; zero bytes written)")
    else:
        g = free_gib(DB.parent)
        print(f"free disk: {g:.2f} GiB")
        if g < HALT_FREE_GIB:
            raise SystemExit(f"REFUSED: free disk {g:.2f} GiB < {HALT_FREE_GIB} GiB (JOIN-1 charter section 6 HALT boundary)")
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        bak = DB.with_name(f"corpus.db.pre-join1-j0-{stamp}-backup")
        shutil.copy2(DB, bak)
        print(f"backup: {bak.name} FILE sha256 {sha256_file(bak)}")
        con = sqlite3.connect(DB, isolation_level=None)
        pre = migrate(con, rules, rules_sha, applied_utc)
        res = audit(con, pre, test_triggers=False)
        con.close()
        print(f"corpus.db FILE sha256 (after): {sha256_file(DB)}")
    for key, val in res.items():
        print(f"{key}: {val}")
    ok = (res["esf_rows_unchanged"] and res["orig_columns_byte_identical"] and res["is_core_unchanged"]
          and res["audit_view_rows"] == 0 and res["null_vocab"] == 0 and res["null_class"] == 0
          and res["grade_dist"] == [("DATAMINED", "DATAMINED", res["esf_rows"])]
          and res["docket_not5_unchanged"] and res["integrity"] == "ok")
    print("VERDICT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
