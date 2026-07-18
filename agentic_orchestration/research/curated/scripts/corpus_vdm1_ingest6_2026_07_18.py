#!/usr/bin/env python3
"""
VDM-1 ingest wave 6 — ERRATA-14/15 (stage-3 D-2a uniform-law retro) +
ratified CANDIDATE ingestion (stage-3 D-4): 8 docket rows + 6 mint rows.

Elrond (data steward, SINGLE WRITER of corpus.db).

Follows the ingest-4 procedure (corpus_vdm1_ingest4_2026_07_18.py) idioms exactly:
guarded single-row eras restamp (assert prior value, rowcount==1), INSERT-only
candidate landing, backup+md5 reversibility, index.lock retry wrapper (wait 30s,
retry 3x), journal_mode DELETE preserved, integrity_check + foreign_key_check.

TWO JOBS:

  (1) ERRATA-14/15 — stage-3 D-2a uniform-law retro-application.
      The now-RETIRED policy split let an era floor stand if the skill had
      "genuine back-half presence" inside the bucket (b07 graded these two
      CONFIRMED-with-note under that split; see errata-ledger REGISTER-ANNOT
      wave 4). The stage-3 D-2a UNIFORM LAW is: an era floor that PREDATES the
      skill's introduction patch is CONTRADICTED, regardless of back-half meta
      presence. Both kits' floor bucket 3.0-3.6 has floor 3.0, but the skills
      debuted mid-bucket, so the floor is narrowed to the debut patch.

        ERRATA-14 poe1-tectonic-slam  "3.0-3.6"  -> "3.2-3.6"
                  Tectonic Slam introduced 3.2.0 (attested in the b07 era
                  CONFIRMED verify row anchor: "Tectonic Slam was introduced in
                  patch 3.2.0 as a new Strength Skill Gem"). Floor 3.0 predates
                  the 3.2.0 debut by two patches -> floor 3.0->3.2.
        ERRATA-15 poe1-toxic-rain
                  "3.0-3.6;3.7-3.13;3.14-3.19;3.20+" ->
                  "3.4-3.6;3.7-3.13;3.14-3.19;3.20+"
                  Toxic Rain introduced 3.4.0 Delve (attested in the b07 era
                  CONFIRMED verify row anchor: "Toxic Rain was introduced in
                  version 3.4.0 (Delve league)"). Floor 3.0 predates the 3.4.0
                  debut by four patches -> floor 3.0->3.4. Only the leftmost
                  bucket's floor moves; the three later buckets are UNTOUCHED
                  (3.7-3.13 stays as-is — its b07 UNSUPPORTED grade is a
                  partition-analysis input, not an errata basis, per the wave-4
                  REGISTER-ANNOT note; the 3.14-3.19 and 3.20+ buckets are
                  CONFIRMED and untouched).

      DISPATCH LAW: do NOT retro-edit the b07 verify_ledger verdict rows — they
      KEEP their historical CONFIRMED grades. No `errata_applied` flag is set on
      any row this wave (that convention is reserved for CONTRADICTED-era verify
      rows; these kits carry no CONTRADICTED era row). The data restamp + the
      errata-ledger ERRATA-14/15 entries are the sole audit trail, exactly the
      ERRATA-9 / BACKFILL-1 provenance shape (data change, no flag). Post-wave
      errata_applied total therefore STAYS 12 (unchanged from ingest-4).

  (2) RATIFIED CANDIDATE INGESTION (stage-3 D-4). The two ratified files are the
      consolidation of record (16 docket filings -> 8; 8 mint filings -> 6); the
      24 per-batch candidate side-files are NOT ingested.

        docket: ratified-docket-rows.jsonl (8) -> mechanic_gap_docket
        mint:   ratified-mint-candidates.jsonl (6) -> mint_ledger

      Every row carries status 'steward-ratified-candidate' (one mint row is
      'steward-ratified-candidate-GRADUATED'). These are CANDIDATE records: NO
      engine change is authorized; Matt-tier approval happens at THE REVIEW BOOK.

      SCHEMA MAPPING (seam judgment; no-fabrication + reversibility):
        mechanic_gap_docket already HAS a `status` column (default 'open') ->
          set per-row from the file. `mechanism_class`, `evidence_kits`
          (JSON array, serialized 1:1), `destination`, `spec_text`
          (-> spec_text_or_path column) map directly. The extra file fields
          `consolidated_from` + `notes` have NO column -> carried LOSSLESSLY in
          a NEW guarded `provenance_json` TEXT column (added via guarded
          ADD COLUMN if absent). No datum is dropped.
        mint_ledger LACKS a `status` column -> a NEW guarded `status` TEXT
          column is added (the GRADUATED distinction is query-load-bearing and
          deserves a first-class home; parallels the docket table). `mint_class`
          (CHECK quantitative|qualitative), `description`, `forced_by_kits`
          (JSON array) map directly. The file's `consolidated_from` + `notes`
          are carried in the existing `ladder_step_audit` column packed as a
          small JSON object (that column is exactly the "which ladder step /
          provenance" slot) — no new column needed for those; `status` is the
          only structural add.

      These are INSERT-only into currently-empty tables (both asserted 0 pre).

  ASSERTS to report (dispatch): mechanic_gap_docket = 8 rows; mint_ledger = 6
  rows; the entity-as-consumable-resource-pool docket row carries 7 evidence
  kits; the GRADUATED mint carries 3 forcing kits; both ERRATA restamps applied
  with prior-value asserts held; journal DELETE; integrity_check ok.

Charter laws honored:
  - No silent transformation: every eras write is guarded rowcount==1 against
    the EXACT current value; both restamps logged in the errata ledger + this
    doc. Candidate rows are ingested 1:1 (JSON serialized ensure_ascii=False);
    no field dropped (extras carried in provenance_json / ladder_step_audit).
  - No-fabrication: no CANDIDATE is promoted to any engine-authoritative state;
    status column preserves 'steward-ratified-candidate[-GRADUATED]' verbatim.
  - Reversible: raw JSONL inputs are committed + static; reproducible against
    the pre-ingest6 backup. The two ADD COLUMN migrations are additive
    (nullable, no default rewrite) and non-destructive.
  - journal_mode stays DELETE (readonly crawlers run concurrently).
  - Short write txn: all validation before the single BEGIN..COMMIT; index.lock
    retry on the write handle (wait 30s, retry 3x) per dispatch LAW.

Usage:
  python3 corpus_vdm1_ingest6_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest6_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
S2 = REPO / "agentic_orchestration/research/vdm1/stage2/poe1"
DOCKET_FILE = S2 / "ratified-docket-rows.jsonl"
MINT_FILE = S2 / "ratified-mint-candidates.jsonl"

# ---- CHECK enums mirrored from schema (validate before insert) ----
MINT_CLASS = {"quantitative", "qualitative"}
RATIFIED_STATUS = {"steward-ratified-candidate", "steward-ratified-candidate-GRADUATED"}

# ---- ERRATA-14/15 (eras): kit -> (old_eras, new_eras). Guard requires exact old match. ----
# stage-3 D-2a uniform-law retro: era floor predating skill introduction = CONTRADICTED.
# b07 verdict rows are NOT retro-edited (keep CONFIRMED); NO errata_applied flag is set.
ERRATA = {
    "poe1-tectonic-slam": ("3.0-3.6",
                           "3.2-3.6"),                                   # ERRATA-14 debut 3.2.0, floor 3.0->3.2
    "poe1-toxic-rain":    ("3.0-3.6;3.7-3.13;3.14-3.19;3.20+",
                           "3.4-3.6;3.7-3.13;3.14-3.19;3.20+"),          # ERRATA-15 debut 3.4.0, floor 3.0->3.4
}
ERRATA_KITS = set(ERRATA)


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))   # raises on any malformed line
    return rows


def connect_with_retry(path, attempts=3, wait=30):
    """Open the write connection; on a locked DB (index.lock / database is locked)
    wait `wait`s and retry up to `attempts` times per dispatch LAW."""
    last = None
    for i in range(1, attempts + 1):
        try:
            con = sqlite3.connect(str(path), timeout=wait)
            con.execute("PRAGMA foreign_keys=ON;")
            con.execute("BEGIN IMMEDIATE;")   # probe the lock early, then release
            con.execute("COMMIT;")
            return con
        except sqlite3.OperationalError as e:
            last = e
            if "lock" in str(e).lower() and i < attempts:
                print(f"   [lock] attempt {i}/{attempts}: {e} -> wait {wait}s, retry")
                time.sleep(wait)
                continue
            raise
    raise last


def table_columns(con, table):
    return {r[1] for r in con.execute(f"PRAGMA table_info({table})")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    # ground-truth snapshots
    curera = dict(con.execute("SELECT kit_id, eras FROM canon_corpus"))
    dbkits = set(curera)
    pre_docket = con.execute("SELECT COUNT(*) FROM mechanic_gap_docket").fetchone()[0]
    pre_mint = con.execute("SELECT COUNT(*) FROM mint_ledger").fetchone()[0]
    pre_flag = con.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    pre_corpus = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    docket_cols = table_columns(con, "mechanic_gap_docket")
    mint_cols = table_columns(con, "mint_ledger")

    # ---- pre-flight ERRATA guards: current DB value must match expected old ----
    for k, (old, _new) in ERRATA.items():
        assert curera.get(k) == old, \
            f"ERRATA guard: {k} current eras {curera.get(k)!r} != expected old {old!r}"

    # ---- pre-flight: both candidate tables MUST be empty (INSERT-only into fresh tables) ----
    assert pre_docket == 0, f"mechanic_gap_docket not empty pre-ingest ({pre_docket})"
    assert pre_mint == 0, f"mint_ledger not empty pre-ingest ({pre_mint})"
    # errata_applied baseline unchanged this wave (no CONTRADICTED rows minted)
    assert pre_flag == 12, f"errata_applied baseline {pre_flag} != 12 (ingest-4 state)"

    log = {"rejects": []}

    # ---------- VALIDATE + STAGE docket rows ----------
    docket_ins = []
    docket_kit_counts = {}
    for ln, r in load_jsonl(DOCKET_FILE):
        mech = r.get("mechanism_class")
        ev = r.get("evidence_kits")
        status = r.get("status")
        dest = r.get("destination")
        if status not in RATIFIED_STATUS or not isinstance(ev, list) or not mech:
            log["rejects"].append(("docket", ln, "status/shape", r)); continue
        # FK sanity: every evidence kit_id should exist in canon_corpus (report, don't drop)
        missing = [k for k in ev if k not in dbkits]
        if missing:
            log["rejects"].append(("docket-evidence-fk", ln, f"missing:{missing}", r)); continue
        prov = {"consolidated_from": r.get("consolidated_from"), "notes": r.get("notes")}
        docket_ins.append({
            "mechanism_class": mech,
            "spec_text_or_path": r.get("spec_text"),
            "evidence_kits": json.dumps(ev, ensure_ascii=False),
            "destination": dest,
            "status": status,
            "provenance_json": json.dumps(prov, ensure_ascii=False),
        })
        docket_kit_counts[mech] = len(ev)

    # ---------- VALIDATE + STAGE mint rows ----------
    mint_ins = []
    mint_kit_counts = {}
    graduated = []
    for ln, r in load_jsonl(MINT_FILE):
        mc = r.get("mint_class")
        fb = r.get("forced_by_kits")
        status = r.get("status")
        if mc not in MINT_CLASS or status not in RATIFIED_STATUS or not isinstance(fb, list):
            log["rejects"].append(("mint", ln, "enum/shape", r)); continue
        missing = [k for k in fb if k not in dbkits]
        if missing:
            log["rejects"].append(("mint-forced-fk", ln, f"missing:{missing}", r)); continue
        ladder = {"consolidated_from": r.get("consolidated_from"), "notes": r.get("notes")}
        mint_ins.append({
            "mint_class": mc,
            "description": r.get("description"),
            "forced_by_kits": json.dumps(fb, ensure_ascii=False),
            "ladder_step_audit": json.dumps(ladder, ensure_ascii=False),
            "status": status,
        })
        key = (mc, r.get("description", "")[:40])
        mint_kit_counts[key] = len(fb)
        if status == "steward-ratified-candidate-GRADUATED":
            graduated.append((len(fb), r.get("forced_by_kits")))

    # ---------- named asserts (dispatch truths) computed on staged data ----------
    entity_pool_ct = docket_kit_counts.get("entity-as-consumable-resource-pool")
    grad_ct = graduated[0][0] if graduated else None

    # ---------- report ----------
    print("=== VDM-1 ingest wave 6 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("docket rows staged:", len(docket_ins))
    print("mint rows staged:", len(mint_ins))
    print("entity-as-consumable-resource-pool evidence_kits:", entity_pool_ct)
    print("GRADUATED mint(s):", len(graduated), "forcing-kit count:", grad_ct)
    print("ERRATA restamps (guarded, prior-value asserts HELD):")
    for k, (old, new) in ERRATA.items():
        print(f"    {k:22} {old!r} -> {new!r}")
    print("rejects (malformed enum/FK/shape):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:3])
    print("docket schema add-column needed (provenance_json):",
          "provenance_json" not in docket_cols)
    print("mint schema add-column needed (status):", "status" not in mint_cols)

    # ---------- pre-write asserts ----------
    assert len(log["rejects"]) == 0, f"{len(log['rejects'])} rejected rows — HALT"
    assert len(docket_ins) == 8, f"docket rows {len(docket_ins)} != 8"
    assert len(mint_ins) == 6, f"mint rows {len(mint_ins)} != 6"
    assert entity_pool_ct == 7, \
        f"entity-as-consumable-resource-pool evidence_kits {entity_pool_ct} != 7"
    assert len(graduated) == 1, f"expected exactly 1 GRADUATED mint, got {len(graduated)}"
    assert grad_ct == 3, f"GRADUATED mint forcing kits {grad_ct} != 3"

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to write.")
        con.close()
        return

    con.close()  # close readonly handle before opening write handle

    # ---------- single short write txn (write handle with index.lock retry) ----------
    wcon = connect_with_retry(DB)
    try:
        wcon.execute("BEGIN IMMEDIATE;")

        # guarded additive migrations (idempotent — only if absent)
        if "provenance_json" not in docket_cols:
            wcon.execute("ALTER TABLE mechanic_gap_docket ADD COLUMN provenance_json TEXT")
        if "status" not in mint_cols:
            wcon.execute("ALTER TABLE mint_ledger ADD COLUMN status TEXT")

        # ERRATA-14/15: correct canon_corpus eras (each guarded to exactly 1 row on exact old)
        for k, (old, new) in ERRATA.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?", (new, k, old))
            assert cur.rowcount == 1, f"errata UPDATE {k} hit {cur.rowcount} rows (expected 1)"

        # docket candidate rows (INSERT-only)
        wcon.executemany(
            "INSERT INTO mechanic_gap_docket "
            "(mechanism_class, spec_text_or_path, evidence_kits, destination, status, provenance_json) "
            "VALUES (:mechanism_class, :spec_text_or_path, :evidence_kits, :destination, :status, :provenance_json)",
            docket_ins)

        # mint candidate rows (INSERT-only)
        wcon.executemany(
            "INSERT INTO mint_ledger "
            "(mint_class, description, forced_by_kits, ladder_step_audit, status) "
            "VALUES (:mint_class, :description, :forced_by_kits, :ladder_step_audit, :status)",
            mint_ins)

        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    # ---------- POST-write asserts ----------
    post_docket = wcon.execute("SELECT COUNT(*) FROM mechanic_gap_docket").fetchone()[0]
    post_mint = wcon.execute("SELECT COUNT(*) FROM mint_ledger").fetchone()[0]
    post_flag = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    post_corpus = wcon.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    jm = wcon.execute("PRAGMA journal_mode;").fetchone()[0]
    ic = wcon.execute("PRAGMA integrity_check;").fetchone()[0]
    fk = wcon.execute("PRAGMA foreign_key_check;").fetchall()

    # named-assert re-checks read back from the DB
    entity_row = wcon.execute(
        "SELECT evidence_kits FROM mechanic_gap_docket WHERE mechanism_class=?",
        ("entity-as-consumable-resource-pool",)).fetchone()
    entity_pool_db = len(json.loads(entity_row[0])) if entity_row else None
    grad_row = wcon.execute(
        "SELECT forced_by_kits FROM mint_ledger WHERE status='steward-ratified-candidate-GRADUATED'"
    ).fetchall()
    grad_db = len(json.loads(grad_row[0][0])) if len(grad_row) == 1 else None
    # every candidate row carries a ratified status
    bad_docket_status = wcon.execute(
        "SELECT COUNT(*) FROM mechanic_gap_docket WHERE status NOT IN "
        "('steward-ratified-candidate','steward-ratified-candidate-GRADUATED')").fetchone()[0]
    bad_mint_status = wcon.execute(
        "SELECT COUNT(*) FROM mint_ledger WHERE status NOT IN "
        "('steward-ratified-candidate','steward-ratified-candidate-GRADUATED')").fetchone()[0]

    assert post_docket == pre_docket + 8 == 8, f"mechanic_gap_docket {post_docket} != 8"
    assert post_mint == pre_mint + 6 == 6, f"mint_ledger {post_mint} != 6"
    assert post_corpus == pre_corpus, f"canon_corpus row count changed {pre_corpus}->{post_corpus}"
    assert post_flag == 12, f"errata_applied total {post_flag} != 12 (must be UNCHANGED this wave)"
    assert entity_pool_db == 7, f"DB entity-pool evidence_kits {entity_pool_db} != 7"
    assert len(grad_row) == 1 and grad_db == 3, \
        f"DB GRADUATED mint rows {len(grad_row)} / forcing kits {grad_db} (expected 1 / 3)"
    assert bad_docket_status == 0 and bad_mint_status == 0, "non-ratified status leaked"
    assert jm == "delete", f"journal_mode {jm} != delete"
    assert ic == "ok", f"integrity_check {ic}"
    assert fk == [], f"foreign_key_check {fk}"
    # eras landed exactly + b07 verdict rows untouched (still CONFIRMED, unflagged)
    for k, (_old, new) in ERRATA.items():
        got = wcon.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
        assert got == new, f"{k} eras {got!r} != {new!r}"
        flagged = wcon.execute(
            "SELECT COUNT(*) FROM verify_ledger WHERE kit_id=? AND errata_applied=1", (k,)).fetchone()[0]
        assert flagged == 0, f"{k} must have 0 errata_applied rows (b07 rows keep CONFIRMED), has {flagged}"
        conf = wcon.execute(
            "SELECT COUNT(*) FROM verify_ledger WHERE kit_id=? AND claim_family='era' AND verdict='CONFIRMED'",
            (k,)).fetchone()[0]
        assert conf >= 1, f"{k} lost its historical CONFIRMED era verdict row"

    print("\n=== APPLIED ===")
    print(f"mechanic_gap_docket  {pre_docket} -> {post_docket}  (+{post_docket-pre_docket})")
    print(f"mint_ledger          {pre_mint} -> {post_mint}  (+{post_mint-pre_mint})")
    print(f"errata_applied total (UNCHANGED, must be 12): {post_flag}")
    print(f"canon_corpus rows (unchanged): {post_corpus}")
    print("entity-as-consumable-resource-pool evidence_kits (DB):", entity_pool_db)
    print("GRADUATED mint forcing kits (DB):", grad_db)
    for k, (old, new) in ERRATA.items():
        print(f"eras restamp {k}: {old!r} -> {new!r}  (b07 verdict rows UNTOUCHED: CONFIRMED)")
    print("journal_mode:", jm, "| integrity_check:", ic, "| foreign_key_check:", fk)
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
