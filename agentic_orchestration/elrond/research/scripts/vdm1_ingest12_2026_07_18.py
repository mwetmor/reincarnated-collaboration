#!/usr/bin/env python3
"""
VDM-1 INGEST-12 — basin-2 mapping ingest + three riders.
Single-writer: elrond. DB: corpus.db (journal_mode DELETE).

Payloads (one transaction, all-or-nothing):
  P1: kit_mapping ingestion — 76 basin-2 rows (INSERT only; STOP on any kit_id collision).
  P2: b05 author-credit backfill — UPDATE-in-place 10 abstained author_credit rows (abstained 1->0).
  P3: canon_engine_key WRONG-RESOURCE third-store sweep — 16 gd resource_verbatim rows -> energy
      (extends ERRATA-38; mirrors the probe-store split 14 mana + 2 spirit/focus).
  P4: le-umbral-blades mech_note circular-clause reword (ERRATA-42 annotation-class).

Execution-integrity (ingest-11 lesson banked): clean backup taken + md5 recorded BEFORE this run;
live md5 verified == baseline pre-run (external, in the dispatch shell); NO dry-run harness against
the live path — this script's DB constant points at live corpus.db and it is invoked directly.
Every UPDATE guards affected-rowcount == expected and RAISES (rolls back) on mismatch. All expected
counts asserted; FILES GOVERN — a mismatch stops the run pre/at-write, does not reconcile silently.

FILE-TRUTH NOTE (P1 grade histogram): the 76 files carry the post-audit per-batch histograms
(W1 8E/19C/3A/6G from the b01..b03 audit addenda: forcewave APPROX->CLOSE, blade-trap/eor/stormbox
APPROX) => full-corpus 9E/43C/13A/11G, 65 MAPPED / 11 MAPPED_DOCKET. The WAVE-PLAN W1-CLOSED rollup
line (and the brief's derived D-2c target 9E/44C/12A/11G) undercount APPROX by 1 / overcount CLOSE by
1 -- an arithmetic slip in the rollup, not a data error. This script asserts the FILE truth
(43C/13A) and reports the divergence; it does NOT edit any grade to match the stale rollup.
"""

import json
import sqlite3
import hashlib
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research")
DB = ROOT / "curated" / "corpus.db"
MAPPING_DIR = ROOT / "vdm1" / "stage2" / "basin2"
BACKFILL_FILE = ROOT / "vdm1" / "stage1" / "basin2" / "batch-05-dossier-authorcredit-backfill.jsonl"

# ---- expected contracts (FILES GOVERN; asserted PRE-LOAD) ----
EXP_MAPPING_TOTAL = 76
EXP_PER_FILE = {1: 12, 2: 12, 3: 12, 4: 11, 5: 11, 6: 12, 7: 6}
# FILE-TRUTH grade/terminal histogram (post-audit per-batch sums; see FILE-TRUTH NOTE):
EXP_GRADE_HIST = {"EXACT": 9, "CLOSE": 43, "APPROX": 13, "GAPPED": 11}
EXP_TERMINAL_HIST = {"MAPPED": 65, "MAPPED_DOCKET": 11}
EXP_BACKFILL_ROWS = 10
EXP_P3_SWEEP = 16
BASELINE_KM = 142
BASELINE_KD = 1320

BACKFILL_KIDS = [
    "le-fire-aura-spellblade", "le-flame-reave-spellblade", "le-ghostflame-warlock",
    "le-hammer-throw-paladin", "le-harvest-lich", "le-healing-hands-paladin",
    "le-judgement-paladin", "le-lightning-blast", "le-low-life-ward", "le-manifest-armor",
]

# P4 exact strings (verified against current DB value at measure-time)
UMBRAL_KID = "le-umbral-blades"
UMBRAL_OLD_CLAUSE = ("fetched text attests Umbral Blades as physical/cold (probe element already "
                     "reads 'Physical / Cold'), NOT void")
UMBRAL_NEW_CLAUSE = ("probe element reads Physical/Cold; fetched text is element-silent, NOT void")


def die(msg):
    print(f"\n*** STOP: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_mapping_rows():
    rows = []
    per_file = {}
    for i in range(1, 8):
        fn = MAPPING_DIR / f"mapping-batch-{i:02d}.jsonl"
        c = 0
        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                rows.append(d)
                c += 1
        per_file[i] = c
    return rows, per_file


def load_backfill_rows():
    rows = []
    with open(BACKFILL_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main():
    # ---------- PRE-LOAD validation (before opening a write cursor) ----------
    map_rows, per_file = load_mapping_rows()
    if per_file != EXP_PER_FILE:
        die(f"per-file count mismatch: {per_file} != {EXP_PER_FILE}")
    if len(map_rows) != EXP_MAPPING_TOTAL:
        die(f"mapping total {len(map_rows)} != {EXP_MAPPING_TOTAL}")

    req = {"kit_id", "mapping_json", "grade", "deviation_notes", "terminal_state"}
    for d in map_rows:
        miss = req - set(d.keys())
        if miss:
            die(f"row {d.get('kit_id')} missing fields {miss}")
        if not isinstance(d["mapping_json"], dict):
            die(f"row {d['kit_id']} mapping_json not an object")
        if d["grade"] not in ("EXACT", "CLOSE", "APPROX", "GAPPED"):
            die(f"row {d['kit_id']} bad grade {d['grade']}")
        if d["terminal_state"] not in ("MAPPED", "MAPPED_DOCKET"):
            die(f"row {d['kit_id']} bad terminal {d['terminal_state']}")

    gh = Counter(d["grade"] for d in map_rows)
    th = Counter(d["terminal_state"] for d in map_rows)
    if dict(gh) != EXP_GRADE_HIST:
        die(f"grade histogram {dict(gh)} != FILE-TRUTH {EXP_GRADE_HIST}")
    if dict(th) != EXP_TERMINAL_HIST:
        die(f"terminal histogram {dict(th)} != {EXP_TERMINAL_HIST}")

    kids = [d["kit_id"] for d in map_rows]
    if len(set(kids)) != EXP_MAPPING_TOTAL:
        die(f"duplicate kit_ids in mapping files: {[k for k in set(kids) if kids.count(k) > 1]}")

    bf_rows = load_backfill_rows()
    if len(bf_rows) != EXP_BACKFILL_ROWS:
        die(f"backfill rows {len(bf_rows)} != {EXP_BACKFILL_ROWS}")
    for d in bf_rows:
        if d.get("family") != "author_credit":
            die(f"backfill row {d.get('kit_id')} family != author_credit")
        if d.get("abstained") != 0:
            die(f"backfill row {d.get('kit_id')} abstained != 0 (must populate)")
        if d.get("payload_json") is None:
            die(f"backfill row {d.get('kit_id')} payload_json is null (must populate)")
    bf_kids = [d["kit_id"] for d in bf_rows]
    if sorted(bf_kids) != sorted(BACKFILL_KIDS):
        die(f"backfill kit set {sorted(bf_kids)} != expected {sorted(BACKFILL_KIDS)}")

    print("PRE-LOAD OK: 76 mapping rows (9E/43C/13A/11G · 65 MAPPED / 11 DOCKET), 10 backfill rows.")

    # ---------- open DB, verify baseline, single transaction ----------
    conn = sqlite3.connect(str(DB))
    conn.isolation_level = None  # explicit txn control
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    jm = cur.execute("PRAGMA journal_mode;").fetchone()[0]
    if jm.lower() != "delete":
        die(f"journal_mode is {jm}, expected delete (never flip to WAL)")

    km0 = cur.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    kd0 = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    if km0 != BASELINE_KM:
        die(f"kit_mapping baseline {km0} != {BASELINE_KM}")
    if kd0 != BASELINE_KD:
        die(f"kit_dossier baseline {kd0} != {BASELINE_KD}")

    existing_km = set(r[0] for r in cur.execute("SELECT kit_id FROM kit_mapping"))
    canon = set(r[0] for r in cur.execute("SELECT kit_id FROM canon_corpus"))
    overlap = [k for k in kids if k in existing_km]
    if overlap:
        die(f"kit_mapping COLLISION (INSERT-only law) — do not upsert: {overlap}")
    fkfail = [k for k in kids if k not in canon]
    if fkfail:
        die(f"kit_mapping FK-fail (not in canon_corpus): {fkfail}")

    # P3 measure-first (already reported externally; re-assert here inside txn scope)
    p3_targets = [r[0] for r in cur.execute(
        "SELECT kit_id FROM canon_engine_key WHERE kit_id LIKE 'gd-%' AND "
        "(resource_verbatim LIKE '%spirit%' OR resource_verbatim LIKE '%focus%' "
        " OR resource_verbatim GLOB '*mana*')"
    )]
    if len(p3_targets) != EXP_P3_SWEEP:
        die(f"P3 measured {len(p3_targets)} gd resource_verbatim residue rows != {EXP_P3_SWEEP} "
            f"-- steward re-authorizes; do not improvise scope. kits={sorted(p3_targets)}")

    # P4 measure-first: confirm the circular clause is present exactly once
    umbral_note = cur.execute(
        "SELECT mech_note FROM canon_corpus WHERE kit_id=?", (UMBRAL_KID,)
    ).fetchone()
    if umbral_note is None:
        die(f"P4 kit {UMBRAL_KID} not found")
    umbral_note = umbral_note[0]
    if UMBRAL_OLD_CLAUSE not in umbral_note:
        die(f"P4 old clause not found verbatim in umbral mech_note (annotation drift)")

    print(f"BASELINE OK: kit_mapping={km0}, kit_dossier={kd0}, 0 overlap, 0 FK-fail, "
          f"P3 residue={len(p3_targets)}, P4 clause present.")

    # ================= WRITE (single txn) =================
    cur.execute("BEGIN")
    try:
        # ---- P1: INSERT 76 kit_mapping rows ----
        for d in map_rows:
            cur.execute(
                "INSERT INTO kit_mapping (kit_id, mapping_json, grade, deviation_notes, "
                "terminal_state) VALUES (?,?,?,?,?)",
                (d["kit_id"], json.dumps(d["mapping_json"], ensure_ascii=False),
                 d["grade"], d.get("deviation_notes"), d["terminal_state"]),
            )
        # mapping_provenance default 'authored-vdm1' and authored_date default now() stand.
        km_after = cur.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
        if km_after != BASELINE_KM + EXP_MAPPING_TOTAL:
            raise RuntimeError(f"P1 post-insert count {km_after} != {BASELINE_KM + EXP_MAPPING_TOTAL}")

        # ---- P2: UPDATE-in-place 10 abstained author_credit rows ----
        p2_affected = 0
        for d in bf_rows:
            cur.execute(
                "UPDATE kit_dossier SET abstained=0, payload_json=?, source_url=?, "
                "anchor_quote=?, conf=? "
                "WHERE kit_id=? AND family='author_credit' AND abstained=1",
                (json.dumps(d["payload_json"], ensure_ascii=False), d.get("source_url"),
                 d.get("anchor_quote"), d.get("conf"), d["kit_id"]),
            )
            n = cur.rowcount
            if n != 1:
                raise RuntimeError(f"P2 {d['kit_id']} affected {n} rows, expected 1 "
                                   f"(guarded rollback)")
            p2_affected += n
        if p2_affected != EXP_BACKFILL_ROWS:
            raise RuntimeError(f"P2 total affected {p2_affected} != {EXP_BACKFILL_ROWS}")
        kd_after = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
        if kd_after != BASELINE_KD:
            raise RuntimeError(f"P2 kit_dossier total changed to {kd_after}; UPDATE must not INSERT "
                               f"(expected {BASELINE_KD})")

        # ---- P3: sweep canon_engine_key.resource_verbatim (16 gd rows) -> energy ----
        # spirit/focus -> energy ; lowercase 'mana' -> 'energy' (preserve '(reserve)' qualifier)
        p3_affected = 0
        p3_detail = {}
        for kid in sorted(p3_targets):
            old = cur.execute(
                "SELECT resource_verbatim FROM canon_engine_key WHERE kit_id=?", (kid,)
            ).fetchone()[0]
            if "spirit" in old or "focus" in old:
                new = "energy"
            elif "reserve" in old:
                new = "energy (reserve)"
            elif "mana" in old and "Mana" not in old:
                # substring replace lowercase mana -> energy (compounds like 'mana-...')
                new = old.replace("mana", "energy")
            else:
                raise RuntimeError(f"P3 {kid} unexpected resource_verbatim '{old}' — no rule")
            cur.execute(
                "UPDATE canon_engine_key SET resource_verbatim=? WHERE kit_id=? "
                "AND resource_verbatim=?",
                (new, kid, old),
            )
            n = cur.rowcount
            if n != 1:
                raise RuntimeError(f"P3 {kid} affected {n} rows, expected 1 (guarded rollback)")
            p3_affected += n
            p3_detail[kid] = (old, new)
        if p3_affected != EXP_P3_SWEEP:
            raise RuntimeError(f"P3 total affected {p3_affected} != {EXP_P3_SWEEP}")
        # safety: 0 gd resource_verbatim residue remaining; 0 LE rows touched
        resid = cur.execute(
            "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE 'gd-%' AND "
            "(resource_verbatim LIKE '%spirit%' OR resource_verbatim LIKE '%focus%' "
            " OR resource_verbatim GLOB '*mana*')"
        ).fetchone()[0]
        if resid != 0:
            raise RuntimeError(f"P3 residual gd resource_verbatim residue {resid} != 0")

        # ---- P4: reword umbral-blades circular clause (guarded rowcount==1) ----
        new_note = umbral_note.replace(UMBRAL_OLD_CLAUSE, UMBRAL_NEW_CLAUSE)
        if new_note == umbral_note:
            raise RuntimeError("P4 reword produced no change (clause match failure)")
        cur.execute(
            "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note=?",
            (new_note, UMBRAL_KID, umbral_note),
        )
        if cur.rowcount != 1:
            raise RuntimeError(f"P4 affected {cur.rowcount} rows, expected 1 (guarded rollback)")

        # ---- integrity gates before COMMIT ----
        ic = cur.execute("PRAGMA integrity_check").fetchone()[0]
        if ic != "ok":
            raise RuntimeError(f"integrity_check = {ic}")
        fkc = cur.execute("PRAGMA foreign_key_check").fetchall()
        if fkc:
            raise RuntimeError(f"foreign_key_check not clean: {fkc[:5]}")

        cur.execute("COMMIT")
    except Exception as e:
        cur.execute("ROLLBACK")
        conn.close()
        die(f"WRITE aborted, rolled back: {e}")

    # ================= POST-WRITE verification (readonly re-query) =================
    km_f = cur.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    kd_f = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    gh_db = dict(cur.execute(
        "SELECT grade, COUNT(*) FROM kit_mapping WHERE kit_id IN ({}) GROUP BY grade".format(
            ",".join("?" * len(kids))), kids).fetchall())
    th_db = dict(cur.execute(
        "SELECT terminal_state, COUNT(*) FROM kit_mapping WHERE kit_id IN ({}) GROUP BY "
        "terminal_state".format(",".join("?" * len(kids))), kids).fetchall())
    bf_nonabst = cur.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='author_credit' AND abstained=0 "
        "AND kit_id IN ({})".format(",".join("?" * len(BACKFILL_KIDS))), BACKFILL_KIDS
    ).fetchone()[0]
    p3_gd_energy = cur.execute(
        "SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE 'gd-%' "
        "AND resource_verbatim='energy'"
    ).fetchone()[0]
    umbral_now = cur.execute(
        "SELECT mech_note FROM canon_corpus WHERE kit_id=?", (UMBRAL_KID,)).fetchone()[0]

    conn.close()

    print("\n===== POST-WRITE VERIFICATION =====")
    print(f"kit_mapping final: {km_f}  (expected {BASELINE_KM + EXP_MAPPING_TOTAL})")
    print(f"kit_dossier total: {kd_f}  (expected {BASELINE_KD}, unchanged)")
    print(f"grade hist (76 new): {gh_db}")
    print(f"terminal hist (76 new): {th_db}")
    print(f"backfill non-abstained author_credit rows: {bf_nonabst}/10")
    print(f"P3 gd resource_verbatim='energy' rows: {p3_gd_energy}")
    print(f"P4 new clause present: {UMBRAL_NEW_CLAUSE in umbral_now}")
    print(f"P4 old clause gone: {UMBRAL_OLD_CLAUSE not in umbral_now}")
    print("\nP3 sweep detail (old -> new):")
    for kid in sorted(p3_detail):
        print(f"  {kid}: {p3_detail[kid][0]} -> {p3_detail[kid][1]}")


if __name__ == "__main__":
    main()
