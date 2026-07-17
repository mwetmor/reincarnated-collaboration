#!/usr/bin/env python3
"""
corpus_curation_la_mcd_2026_07_16.py — LA + MCD §9.19 re-harvest curation into corpus.db

Charge: agentic_orchestration/gandalf/briefs/2026-07-16-elrond-la-mcd-curation-brief.md
        (execute pass, post-HALT, per gandalf's RECONCILIATION RULING = Option A).

WHAT THIS DOES (catalogue-only — the HARD BOUNDARY):
  Inserts the 58 §9.19-successor records (the spec-valid replacements for the deleted 182) as
  CATALOGUE CITIZENS into corpus.db:
    - 57 at grain='kit'  (LA 46 positive + LA 6 negative twins + MCD 5 positive)  -> row_class='combat-kit'
    -  1 system-record   `la-monetization-confound`  grain=NULL, row_class='system-record'
      (precedent: the 18 existing system-records, e.g. tli-sage-elixir — all is_system-family,
       grain=NULL, cell_key=NULL, excluded from every fit by row_class).

  NO FIT INPUTS. Every new engine_key row carries cell_key = NULL. The fit-membership predicate is
  `row_class='combat-kit' AND cell_key IS NOT NULL AND negative=0` (verified in
  atlas_refit_candidate_2026_07_16.py L161/167/202/282); cell_key IS NOT NULL is the fit gate, so
  NULL-cell_key rows are catalogued-but-fit-excluded. The E4 refit derives cell_keys behind its
  pre-registered gates (grain='kit' + source-exclusion + congruence-to-E3-camera) — a SEPARATE,
  LATER charge (WAVE 4 ruling). This script writes NO atlas-coordinates, runs NO leiden/affinity,
  touches NO served artifact. corpus.db is the ONLY mutation surface.

WHY engine_key rows at all (0-orphan discipline): the corpus<->engine_key 1:1 (every corpus row has
  exactly one engine_key child; zero orphans) is the ratified never-orphan invariant (dual-hard-delete
  MIGRATION entry; 527/527 pre-state). To preserve it we write 58 engine_key rows (57 combat-kit + 1
  system-record) — but with cell_key=NULL so none enter a fit. Corpus rows are marked unresolved=1
  (fit-input derivation owed to E4), mirroring the pre-existing "no-key" mechanism.

SOURCE OF TRUTH (source-anchored + reversible): the two §9.19 five-stage JSONL corpora, parsed
  directly. The verbatim JSONL row is preserved in canon_engine_key.raw_json — NO destructive
  transform. Every curation value is a stated rule over the record's own fields.

GRAIN LAW (ratified): corpus grain = emission grain. LA = la-{identity} community build identities;
  MCD = mcd-{archetype} item-defined loops — both loop-identity grain -> grain='kit'. The system
  archetype (la-monetization-confound) emits NO kit -> grain=NULL (honest NULL, not a lie; the E4
  grain='kit' predicate auto-excludes it — GRAIN LAW filtering at consumption, exactly as designed).

PROVENANCE: source='canon'; provenance_tag='canon-harvest-9.19-{la|mcd}-2026-07-16';
  source_date='2026-07-16'; prov='legolas-mode-b-9.19;elrond-curated'; run commits da003065 (LA) /
  14abd361 (MCD) recorded in provenance_json + flags. These are the spec-valid successors of the
  deleted 182 (dual-hard-delete-2026-07-16); the provenance chain makes that legible.

NEGATIVES: the 6 LA negative twins carry the corpus negative=1 convention (same as the 38-negative
  trap-skill treatment). Not dropped; not counted as positives.

PREFIX COORDS (canon_corpus attr/range/tempo/amp/proxy/commit): taken from proj.<axis>.v IFF the
  axis does not abstain; abstain (v='n/a') -> NULL (never write 'n/a' — it violates the CHECK enum).
  Surveyed: ZERO non-abstain proj values are out-of-enum, so the rule reduces to write-v-or-NULL.

FAIL-LOUD POST-CURATION ASSERTS (gandalf ruling-corrected; HALT + rollback on any failure):
  total=585 · kit=566 · NULL=19 · gear=0 · class=0 · engine_key 1:1 (0 orphans both directions).

IDEMPOTENT: additive upsert keyed on kit_id; re-running re-derives identical rows. Backup taken by
  this script BEFORE any write (corpus.db.pre-la-mcd-curation-2026-07-16-backup); transactional —
  a single BEGIN/COMMIT, rolled back on any assert failure (no partial writes).
"""

import json
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # -> reincarnated-collaboration
DB = ROOT / "agentic_orchestration/research/curated/corpus.db"
BACKUP = ROOT / "agentic_orchestration/research/curated/corpus.db.pre-la-mcd-curation-2026-07-16-backup"
SRC_DIR = ROOT / "claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3"
LA_JSONL = SRC_DIR / "canon-corpus-la.jsonl"
MCD_JSONL = SRC_DIR / "canon-corpus-mcd.jsonl"

SOURCE_DATE = "2026-07-16"
RUN_COMMIT = {"la": "da003065", "mcd": "14abd361"}
PROV_TAG = {"la": "canon-harvest-9.19-la-2026-07-16", "mcd": "canon-harvest-9.19-mcd-2026-07-16"}
PROV = "legolas-mode-b-9.19;elrond-curated"

# corpus CHECK-constrained prefix-coord enums (survey-proven: all non-abstain proj values fit these)
PREFIX_ENUMS = {
    "attr": {"STR", "DEX", "INT", "WIS"},
    "range": {"melee", "mid", "ranged", "dual"},
    "tempo": {"low", "med", "high"},
    "amp": {"flat", "spiky", "var"},
    "proxy": {"solo", "light", "heavy"},
    "commit": {"instant", "wind-up", "channel"},
}

SYSTEM_RECORD_ID = "la-monetization-confound"
SYSTEM_RECORD_CLASS = "system archetype"

# Ruling-corrected census (the fail-loud arithmetic target)
EXPECT = {"total": 585, "kit": 566, "null": 19, "gear": 0, "class": 0}
EXPECT_INSERT_KIT = 57       # LA 46 pos + LA 6 neg + MCD 5 pos
EXPECT_INSERT_SYSTEM = 1     # la-monetization-confound
EXPECT_INSERT_TOTAL = 58


# --------------------------------------------------------------------------------------
# PARSE (source-anchored ground truth)
# --------------------------------------------------------------------------------------
def load(jsonl_path):
    recs = []
    for line in jsonl_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        recs.append((line, json.loads(line)))  # (verbatim_line, parsed) — verbatim preserved
    return recs


def classify(rec):
    """Return 'system' | 'negative-kit' | 'positive-kit'. system = class=='system archetype'."""
    if rec.get("class") == SYSTEM_RECORD_CLASS:
        return "system"
    return "negative-kit" if rec.get("negative") is True else "positive-kit"


def prefix_coord(rec, axis):
    """proj.<axis>.v IFF not abstain and in-enum; else None. Never writes 'n/a'."""
    cell = (rec.get("proj", {}) or {}).get(axis, {}) or {}
    v = cell.get("v")
    if cell.get("abstain") or v is None:
        return None
    return v if v in PREFIX_ENUMS[axis] else None  # defensive: out-of-enum -> NULL (survey: never fires)


def system_route(rec):
    """Route for the system-record, from its dominant (non-abstain) econ axis."""
    econ = (rec.get("proj", {}) or {}).get("econ", {}) or {}
    v = econ.get("v")
    return v if v and v != "n/a" else "system-archetype"


# --------------------------------------------------------------------------------------
# INSERT (transactional; both tables; cell_key ALWAYS NULL — catalogue-only, no fit input)
# --------------------------------------------------------------------------------------
def insert_row(cur, verbatim, rec, game, kind):
    kit_id = rec["id"]
    negative = 1 if kind == "negative-kit" else 0
    is_system = 1 if kind == "system" else 0
    grain = None if kind == "system" else "kit"
    row_class = "system-record" if kind == "system" else "combat-kit"
    # unresolved=1: fit-input (cell_key) derivation is owed to the E4 refit (catalogue-only landing)
    unresolved = 1

    if kind == "system":
        grain_note = (
            "system-record: not kit/gear/class emittable; excluded from fits by row_class; "
            "§9.19 monetization-confound rider anchor (all emission axes abstain, econ-only). "
            "Precedent: the 18 existing system-records (e.g. tli-sage-elixir)."
        )
    else:
        grain_note = (
            "loop-identity grain (GRAIN LAW: corpus grain = emission grain); "
            f"{'LA la-{identity} community build identity' if game == 'la' else 'MCD mcd-{archetype} item-defined loop'}. "
            "cell_key deferred to E4 refit (fit input owed)."
        )

    eras = ";".join(rec.get("eras", []) or [])
    lineage = rec.get("lineage") or None
    canon_tier = rec.get("canon_tier")
    mech_note = rec.get("mech_summary", "")
    prov_list = rec.get("prov", []) or []

    # ---- canon_corpus ----
    cur.execute(
        """
        INSERT INTO canon_corpus
          (kit_id, folk_name, game, corpus_bucket, canon_tier, eras, negative, lineage,
           source, is_system, unresolved, mint, dossier_owed,
           provenance_tag, source_date,
           attr_val, range_val, tempo_val, amp_val, proxy_val, commit_val,
           prefix_conf_provenance,
           mech_note, flags, prov, grain, grain_note)
        VALUES (?,?,?,?,?,?,?,?, ?,?,?,?,?, ?,?, ?,?,?,?,?,?, ?, ?,?,?,?,?)
        ON CONFLICT(kit_id) DO UPDATE SET
          folk_name=excluded.folk_name, game=excluded.game, corpus_bucket=excluded.corpus_bucket,
          canon_tier=excluded.canon_tier, eras=excluded.eras, negative=excluded.negative,
          lineage=excluded.lineage, source=excluded.source, is_system=excluded.is_system,
          unresolved=excluded.unresolved, provenance_tag=excluded.provenance_tag,
          source_date=excluded.source_date, attr_val=excluded.attr_val, range_val=excluded.range_val,
          tempo_val=excluded.tempo_val, amp_val=excluded.amp_val, proxy_val=excluded.proxy_val,
          commit_val=excluded.commit_val, prefix_conf_provenance=excluded.prefix_conf_provenance,
          mech_note=excluded.mech_note, flags=excluded.flags, prov=excluded.prov,
          grain=excluded.grain, grain_note=excluded.grain_note
        """,
        (
            kit_id, rec.get("folk_name", kit_id), game, game, canon_tier, eras, negative, lineage,
            "canon", is_system, unresolved, 0, 1 if rec.get("dossier_owed") else 0,
            PROV_TAG[game], SOURCE_DATE,
            prefix_coord(rec, "attr"), prefix_coord(rec, "range"), prefix_coord(rec, "tempo"),
            prefix_coord(rec, "amp"), prefix_coord(rec, "proxy"), prefix_coord(rec, "commit"),
            "9.19-proj-abstain-aware",
            mech_note,
            json.dumps({
                "class": rec.get("class"), "eras": rec.get("eras", []),
                "gap_refs": rec.get("gap_refs", []), "flags": rec.get("flags", []),
                "neg_twin": rec.get("neg_twin"), "run_commit": RUN_COMMIT[game],
                "spec": "§9.19 five-stage (pipeline-spec v2.13)", "kind": kind,
            }),
            json.dumps(prov_list), grain, grain_note,
        ),
    )

    # ---- canon_engine_key (cell_key=NULL — NO fit input; raw_json = verbatim JSONL line) ----
    provenance_json = json.dumps({
        "source": f"canon-harvest-9.19-{game}", "curator": "elrond", "date": SOURCE_DATE,
        "spec": "§9.19 five-stage (pipeline-spec v2.13)", "run_commit": RUN_COMMIT[game],
        "grain": grain, "kind": kind,
        "cell_key": "NULL — catalogue-only landing; fit-input derivation owed to E4 refit "
                    "(WAVE 4 pre-registered gates). Successor of the deleted 182 "
                    "(dual-hard-delete-2026-07-16).",
    })
    flags = ["canon-harvest-9.19", f"run-commit:{RUN_COMMIT[game]}", "catalogue-only",
             "cell_key:NULL;fit-input-owed-to-E4"]
    if kind == "negative-kit":
        flags.append("negative:1;trap-identity-twin")
    if kind == "system":
        flags.append("system-record;monetization-confound-rider-anchor")

    cur.execute(
        """
        INSERT INTO canon_engine_key
          (kit_id, row_class, route, cell_key, flags, provenance_json, raw_json)
        VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(kit_id) DO UPDATE SET
          row_class=excluded.row_class, route=excluded.route, cell_key=excluded.cell_key,
          flags=excluded.flags, provenance_json=excluded.provenance_json, raw_json=excluded.raw_json
        """,
        (
            kit_id, row_class, (system_route(rec) if kind == "system" else None), None,
            json.dumps(flags), provenance_json, verbatim,
        ),
    )


# --------------------------------------------------------------------------------------
# MAIN (backup-first, transactional, fail-loud)
# --------------------------------------------------------------------------------------
def main():
    if not DB.exists():
        sys.exit(f"corpus.db not found at {DB}")

    la = load(LA_JSONL)
    mcd = load(MCD_JSONL)
    assert len(la) == 53, f"expected 53 LA records, got {len(la)}"
    assert len(mcd) == 5, f"expected 5 MCD records, got {len(mcd)}"

    # census the source partition (fail-loud vs the ruling)
    la_kinds = [classify(r) for _, r in la]
    mcd_kinds = [classify(r) for _, r in mcd]
    n_sys = la_kinds.count("system") + mcd_kinds.count("system")
    n_neg = la_kinds.count("negative-kit") + mcd_kinds.count("negative-kit")
    n_pos = la_kinds.count("positive-kit") + mcd_kinds.count("positive-kit")
    print("== LA + MCD §9.19 curation (catalogue-only, grain='kit' + 1 system-record) ==")
    print(f"  source partition: positive-kit={n_pos}  negative-kit={n_neg}  system={n_sys}")
    assert n_sys == EXPECT_INSERT_SYSTEM, f"expected 1 system-record, got {n_sys}"
    assert n_neg == 6, f"expected 6 negative twins, got {n_neg}"
    assert (n_pos + n_neg) == EXPECT_INSERT_KIT, (
        f"expected {EXPECT_INSERT_KIT} kit-grain rows, got {n_pos + n_neg}")
    # the sole system-record is la-monetization-confound
    sys_ids = [r["id"] for _, r in la + mcd if classify(r) == "system"]
    assert sys_ids == [SYSTEM_RECORD_ID], f"system-record id mismatch: {sys_ids}"

    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys=ON")
    cur = con.cursor()

    # ---- pre-state ----
    pre_total = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    pre_kit = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0]
    pre_null = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL").fetchone()[0]
    pre_ek = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
    print(f"  pre-state: corpus total={pre_total} kit={pre_kit} NULL={pre_null} | engine_key={pre_ek}")
    assert (pre_total, pre_kit, pre_null, pre_ek) == (527, 509, 18, 527), (
        f"PRE-STATE mismatch vs brief precondition (527/509/18/527): got "
        f"{(pre_total, pre_kit, pre_null, pre_ek)}")

    # ---- PRE-INSERT COLLISION CHECK (fail-loud; brief iron law 5) ----
    incoming = [rec["id"] for _, rec in la + mcd]
    assert len(set(incoming)) == 58, f"incoming ids not unique: {len(set(incoming))} distinct of 58"
    coll_corpus = cur.execute(
        "SELECT kit_id FROM canon_corpus WHERE kit_id IN (%s)" % ",".join("?" * len(incoming)),
        incoming).fetchall()
    coll_ek = cur.execute(
        "SELECT kit_id FROM canon_engine_key WHERE kit_id IN (%s)" % ",".join("?" * len(incoming)),
        incoming).fetchall()
    residue_corpus = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE kit_id LIKE 'la-%' OR kit_id LIKE 'mcd-%'").fetchone()[0]
    residue_ek = cur.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE 'la-%' OR kit_id LIKE 'mcd-%'").fetchone()[0]
    print(f"  collision check: incoming-id collisions corpus={len(coll_corpus)} engine_key={len(coll_ek)} "
          f"| la-/mcd- residue corpus={residue_corpus} engine_key={residue_ek}")
    if coll_corpus or coll_ek or residue_corpus or residue_ek:
        con.close()
        sys.exit(f"HALT: collision/residue detected (delete should have left 0). "
                 f"corpus_coll={[c[0] for c in coll_corpus]} ek_coll={[c[0] for c in coll_ek]} "
                 f"residue={residue_corpus}/{residue_ek}")

    # ---- BACKUP-FIRST (before any write) ----
    con.commit()  # ensure clean checkpoint
    shutil.copyfile(str(DB), str(BACKUP))
    integ_bak = sqlite3.connect(str(BACKUP)).execute("PRAGMA integrity_check").fetchone()[0]
    print(f"  backup: {BACKUP.name}  (integrity_check={integ_bak})")
    assert integ_bak == "ok", f"backup integrity failed: {integ_bak}"

    # ---- capture survivor digest (the 527 pre-rows must be byte-untouched — additive) ----
    surv_pre = cur.execute(
        "SELECT kit_id||'|'||grain||'|'||negative FROM canon_corpus ORDER BY kit_id").fetchall()
    surv_pre_set = {r[0] for r in surv_pre}

    # ---- TRANSACTIONAL INSERT ----
    try:
        cur.execute("BEGIN")
        for verbatim, rec in la:
            insert_row(cur, verbatim, rec, "la", classify(rec))
        for verbatim, rec in mcd:
            insert_row(cur, verbatim, rec, "mcd", classify(rec))

        # schema_meta marker (inside txn)
        cur.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            ("la-mcd-curation-9.19-2026-07-16", "2026-07-16T00:00:00Z",
             "LA+MCD §9.19 re-harvest curation (elrond, execute pass post-HALT per gandalf Option-A "
             "ruling). 58 records: 57 grain='kit' (LA 46 pos + 6 neg twins + MCD 5 pos) row_class="
             "'combat-kit'; 1 system-record la-monetization-confound grain=NULL row_class="
             "'system-record' (tli-sage-elixir precedent). Catalogue-only: every engine_key cell_key"
             "=NULL (NO fit input; fit gate is cell_key IS NOT NULL); unresolved=1 (E4 owes cell_key "
             "derivation). Provenance: canon-harvest-9.19 five-stage (spec v2.13), run commits "
             "da003065 LA / 14abd361 MCD, source_date 2026-07-16. Spec-valid successors of the "
             "deleted 182 (dual-hard-delete-2026-07-16). NO refit/leiden/affinity/atlas-coordinate/"
             "served-artifact touch — E4 refit admits behind WAVE-4 pre-registered gates. Additive; "
             "527 survivors byte-untouched; raw JSONL preserved verbatim in raw_json (reversible)."))

        # ---- POST-CURATION ASSERTS (fail-loud; ruling-corrected) ----
        total = cur.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
        kit = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0]
        null = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL").fetchone()[0]
        gear = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='gear'").fetchone()[0]
        clazz = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='class'").fetchone()[0]
        got = {"total": total, "kit": kit, "null": null, "gear": gear, "class": clazz}
        assert got == EXPECT, f"POST-CURATION GRAIN CENSUS mismatch: got {got}, expected {EXPECT}"

        # engine_key 1:1 (0 orphans both directions)
        ek_total = cur.execute("SELECT COUNT(*) FROM canon_engine_key").fetchone()[0]
        fwd_orphan = cur.execute(
            "SELECT COUNT(*) FROM canon_engine_key ek LEFT JOIN canon_corpus cc ON ek.kit_id=cc.kit_id "
            "WHERE cc.kit_id IS NULL").fetchone()[0]
        rev_orphan = cur.execute(
            "SELECT COUNT(*) FROM canon_corpus cc LEFT JOIN canon_engine_key ek ON cc.kit_id=ek.kit_id "
            "WHERE ek.kit_id IS NULL").fetchone()[0]
        assert ek_total == EXPECT["total"], f"engine_key count {ek_total} != {EXPECT['total']}"
        assert fwd_orphan == 0 and rev_orphan == 0, (
            f"engine_key orphans: forward={fwd_orphan} reverse={rev_orphan} (must be 0/0)")

        # NO fit inputs: all 58 new engine_key rows have cell_key NULL
        new_with_cellkey = cur.execute(
            "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id IN (%s) AND cell_key IS NOT NULL"
            % ",".join("?" * len(incoming)), incoming).fetchone()[0]
        assert new_with_cellkey == 0, f"{new_with_cellkey} new rows carry a cell_key (must be 0 — no fit input)"

        # grain<->row_class partition intact (kit<->combat-kit, NULL<->system-record)
        bad_partition = cur.execute(
            "SELECT COUNT(*) FROM canon_corpus cc JOIN canon_engine_key ek ON cc.kit_id=ek.kit_id "
            "WHERE (cc.grain='kit' AND ek.row_class<>'combat-kit') "
            "   OR (cc.grain IS NULL AND ek.row_class<>'system-record')").fetchone()[0]
        assert bad_partition == 0, f"grain<->row_class partition broken on {bad_partition} rows"

        # the 6 negatives are negative=1 and NOT counted as positives
        neg_now = cur.execute(
            "SELECT COUNT(*) FROM canon_corpus WHERE negative=1 AND provenance_tag LIKE 'canon-harvest-9.19-%'"
        ).fetchone()[0]
        assert neg_now == 6, f"expected 6 new negatives, got {neg_now}"

        # additive: 527 survivors byte-untouched (same kit_id|grain|negative signature)
        surv_post_set = {
            r[0] for r in cur.execute(
                "SELECT kit_id||'|'||grain||'|'||negative FROM canon_corpus "
                "WHERE kit_id NOT IN (%s) ORDER BY kit_id" % ",".join("?" * len(incoming)),
                incoming).fetchall()}
        assert surv_post_set == surv_pre_set, "SURVIVOR SIGNATURE CHANGED — not additive (abort)"

        integ = cur.execute("PRAGMA integrity_check").fetchone()[0]
        assert integ == "ok", f"integrity_check failed post-insert: {integ}"

        con.commit()
    except Exception as e:
        con.rollback()
        con.close()
        # restore from backup to guarantee no partial writes survive
        shutil.copyfile(str(BACKUP), str(DB))
        sys.exit(f"HALT (rolled back + restored from backup, NO partial writes): {e}")

    # ---- report ----
    print("\n  POST-CURATION (committed):")
    print(f"    corpus total={total}  kit={kit}  NULL={null}  gear={gear}  class={clazz}   [expect 585/566/19/0/0]")
    print(f"    engine_key={ek_total}  orphans fwd={fwd_orphan} rev={rev_orphan}  new-rows-with-cellkey={new_with_cellkey}")
    print(f"    inserted: {n_pos} positive-kit + {n_neg} negative-kit + {n_sys} system-record = {n_pos + n_neg + n_sys}")
    print(f"    LA: {la_kinds.count('positive-kit')} pos + {la_kinds.count('negative-kit')} neg + "
          f"{la_kinds.count('system')} system   MCD: {mcd_kinds.count('positive-kit')} pos")
    con.close()
    print("CURATION COMPLETE.")


if __name__ == "__main__":
    main()
