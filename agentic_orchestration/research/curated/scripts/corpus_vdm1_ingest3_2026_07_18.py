#!/usr/bin/env python3
"""
VDM-1 ingest wave 3 — PoE1 batches 05-06 (24 kits) into landing-zone tables.

Elrond (data steward, SINGLE WRITER of corpus.db).

Loads three JSONL streams per batch (verify / citations / dossier) into
verify_ledger / kit_citations / kit_dossier, applies FIVE errata (ERRATA-5..8 era
corrections + ERRATA-9 era_year rekey), and promotes fact_provenance for clean
kits. Follows the ingest-2 procedure exactly (corpus_vdm1_ingest2_2026_07_18.py)
with three wave-3 additions:

  (1) BOOLEAN-DRIFT NORMALIZATION. batch-06 emits JSON booleans for `quarantined`
      (false) where batch-05 emits integers (0). Python maps False==0, so the
      BINARY membership check passes, but to avoid silent type drift into an
      INTEGER column we coerce bool->int explicitly at stage time (no-silent-
      transformation: the coercion is logged in the migration doc, and int(False)
      == the value SQLite would store anyway).
  (2) ERRATA-9 era_year rekey (poe1-kinetic-fusillade 2013 -> 2024). This is a
      NON-eras canon_corpus column; it does NOT set verify_ledger.errata_applied
      (that flag is reserved for the CONTRADICTED-era-row convention). The era
      verdict for kinetic-fusillade is CONFIRMED (3.20+ correct); only the
      bulk-fill era_year artifact is corrected. Anchored by batch-05 citations
      ([3.27]/(3.28) guide titles => 2024) + the verify era anchor (3.27.0).
  (3) index.lock RETRY on the write connection (wait 30s, retry 3x) per dispatch
      LAW (concurrent readonly crawlers + mapping agents running).

Format drift (batch-06 GRANULAR verify rows) is INGESTED AS-IS: identity split
folk-name/aliases (14 identity rows) and era split one-row-per-band (28 era rows)
=> 55 verify rows for 12 kits vs the ~36 of earlier batches. Rows are additive and
more checkable; the per-kit granularity is recorded in the migration doc so
partition analysis can normalize per-kit later. Each errata kit still carries
EXACTLY ONE CONTRADICTED era row (verified pre-flight), so the errata-mark guard
is unaffected by the split.

Charter laws honored (unchanged):
  - No silent transformation: every deviation from raw input is logged. The
    poets-pen-vd class red flag CANNOT be corrected here (no class column exists
    in corpus.db; the value lives in roster_atlas.class_v4r2, and poets-pen-vd is
    ABSENT from roster_atlas) -> logged as REVIEW-2 in the errata ledger, routed
    to the roster_atlas owner via knight-rider. Nothing about class is written.
  - No-fabrication: abstained rows keep payload NULL (DB CHECK). This wave has 63
    abstained dossier rows (B05=36, B06=27), ALL already payload-NULL.
  - Reversible: raw JSONL inputs are committed and static; reproducible.
  - journal_mode stays DELETE (readonly crawlers + mapping agents run concurrently).
  - Short write txn: all validation happens BEFORE the single BEGIN..COMMIT.

Filler-row rule (unchanged): negative_canon UNSUPPORTED on canon_corpus.negative=0
kits are N/A-filler -> DROP. This wave: batch-05 has ZERO negative_canon rows;
batch-06 has exactly ONE (poe1-reaper, CONFIRMED, on negative=1) which ingests
normally. => 0 filler dropped this wave.

ERRATA this wave (ERRATA-5..8 are CONTRADICTED era rows carrying their anchor; each
UPDATE is guarded to hit exactly 1 canon_corpus row against the exact current DB
value; errata_applied=1 set on the single CONTRADICTED era verify row):
  ERRATA-5  poe1-icicle-mines       eras floor 3.7 -> 3.8  (skill introduced 3.8.0)
            "3.7-3.13"           -> "3.8-3.13"
  ERRATA-6  poe1-lightning-conduit  eras floor 3.14 -> 3.19 (introduced 3.19.0 LoK)
            "3.14-3.19;3.20+"    -> "3.19;3.20+"
  ERRATA-7  poe1-pconc              eras floor 3.14 -> 3.16 (introduced 3.16.0 Scourge)
            "3.14-3.19;3.20+"    -> "3.16-3.19;3.20+"
  ERRATA-8  poe1-seismic-trap       DROP unattested 3.7-3.13 bucket; attested meta
            begins 3.16 (positive CONFIRMED row: 3.16/3.18 forum guides). Distinct
            root-cause class: "patch-buff-seeded stamp, no adoption evidence"
            (skill existed 3.3.0 but the 3.7-3.13 stamp has NO meta attestation; a
            3.13-era patch-buff likely seeded the stamp without adoption).
            "3.7-3.13;3.14-3.19" -> "3.14-3.19"
  ERRATA-9  poe1-kinetic-fusillade  era_year 2013 -> 2024 (bulk-fill artifact;
            actual introduction 3.27.0 = 2024, per batch-05 [3.27]/(3.28) titles).
            NON-eras column; does NOT set errata_applied (era verdict is CONFIRMED).

fact_provenance promotion (unchanged rule): kits with mechanics=CONFIRMED and ZERO
CONTRADICTED verdicts anywhere flip canon_probe_facts.fact_provenance ->
'verified-v1.1'. The four era-errata kits (icicle-mines, lightning-conduit, pconc,
seismic-trap) are EXCLUDED (each carried a CONTRADICTED era). kinetic-fusillade
PROMOTES (its era is CONFIRMED; only era_year was rekeyed). minion-pact-bv PROMOTES
despite identity=UNSUPPORTED (RULING: identity-UNSUPPORTED is honest silence on the
folk-name, NOT a contradiction; the promotion gate is mechanics=CONFIRMED & no
CONTRADICTED; verified-v1.1 certifies the probe-fact substrate, not the nickname).

Usage:
  python3 corpus_vdm1_ingest3_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest3_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
IN = REPO / "agentic_orchestration/research/vdm1/stage1/poe1"
BATCHES = ["05", "06"]

# ---- CHECK enums mirrored from schema (validate before insert) ----
VERIFY_FAMILY = {"identity", "mechanics", "era", "negative_canon"}
VERIFY_VERDICT = {"CONFIRMED", "CONTRADICTED", "UNSUPPORTED", "SOURCE_NOT_FOUND"}
CITE_CLASS = {"authored", "communal", "official", "dataset", None}
RANK_CLASS = {"recovered", "attested-era", None}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}
BINARY = {0, 1}

# ---- ERRATA table (eras): kit -> (old_eras, new_eras). Guard requires exact old match. ----
ERRATA = {
    "poe1-icicle-mines":      ("3.7-3.13",            "3.8-3.13"),          # ERRATA-5
    "poe1-lightning-conduit": ("3.14-3.19;3.20+",     "3.19;3.20+"),        # ERRATA-6
    "poe1-pconc":             ("3.14-3.19;3.20+",     "3.16-3.19;3.20+"),   # ERRATA-7
    "poe1-seismic-trap":      ("3.7-3.13;3.14-3.19",  "3.14-3.19"),         # ERRATA-8
}
ERRATA_KITS = set(ERRATA)

# ---- ERRATA-9 (era_year rekey; NON-eras column; no errata_applied flag) ----
ERAYEAR_ERRATA = {
    "poe1-kinetic-fusillade": (2013, 2024),   # bulk-fill artifact -> 3.27.0 = 2024
}


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))
    return rows


def coerce_bin(v):
    """Normalize JSON booleans/ints to 0/1 explicitly (boolean-drift guard).
    Returns None if the value is not a clean binary (caller rejects)."""
    if v is True:
        return 1
    if v is False:
        return 0
    if v in (0, 1):
        return int(v)
    return None


def connect_with_retry(path, attempts=3, wait=30):
    """Open the write connection; on a locked DB (index.lock / database is locked)
    wait `wait`s and retry up to `attempts` times per dispatch LAW."""
    last = None
    for i in range(1, attempts + 1):
        try:
            con = sqlite3.connect(str(path), timeout=wait)
            con.execute("PRAGMA foreign_keys=ON;")
            # probe the lock early with a no-op immediate txn, then release
            con.execute("BEGIN IMMEDIATE;")
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    # ground truth: negative flag + current eras + current era_year snapshots
    negflag = dict(con.execute("SELECT kit_id, negative FROM canon_corpus"))
    curera = dict(con.execute("SELECT kit_id, eras FROM canon_corpus"))
    curyr = dict(con.execute("SELECT kit_id, era_year FROM canon_corpus"))
    dbkits = set(negflag)

    # pre-flight: assert each errata's current DB value matches the expected old value
    for k, (old, _new) in ERRATA.items():
        assert curera.get(k) == old, \
            f"ERRATA guard: {k} current eras {curera.get(k)!r} != expected old {old!r}"
    for k, (old, _new) in ERAYEAR_ERRATA.items():
        assert curyr.get(k) == old, \
            f"ERRATA-9 guard: {k} current era_year {curyr.get(k)!r} != expected old {old!r}"

    log = {"verify": {}, "dropped_filler": {}, "citations": {}, "dossier": {},
           "rejects": [], "abstain_payload_stripped": [], "bool_coerced": [],
           "promotions": {}}

    # ---------- VALIDATE + STAGE all inserts (no DB writes yet) ----------
    verify_ins = []
    errata_marks = {k: 0 for k in ERRATA}
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-verify.jsonl")
        log["verify"][b] = 0
        log["dropped_filler"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("claim_family"); verd = r.get("verdict")
            if fam not in VERIFY_FAMILY or verd not in VERIFY_VERDICT or kit not in dbkits:
                log["rejects"].append(("verify", b, ln, "enum/FK", r))
                continue
            # filler-row rule: negative_canon UNSUPPORTED on negative=0 kit -> DROP
            if fam == "negative_canon" and verd == "UNSUPPORTED" and negflag.get(kit, 0) == 0:
                log["dropped_filler"][b] += 1
                continue
            # errata: mark the single CONTRADICTED era row for each of the four kits
            errata = 0
            if kit in ERRATA_KITS and fam == "era" and verd == "CONTRADICTED":
                errata = 1
                errata_marks[kit] += 1
            verify_ins.append((kit, fam, r.get("claim_text"), verd,
                               r.get("anchor_quote"), r.get("source_url"), errata))
            log["verify"][b] += 1

    cite_ins = []
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-citations.jsonl")
        log["citations"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); url = r.get("url")
            cc = r.get("cite_class"); rc = r.get("rank_class")
            q_raw = r.get("quarantined", 0)
            q = coerce_bin(q_raw)
            if (kit not in dbkits or not url or cc not in CITE_CLASS
                    or rc not in RANK_CLASS or q is None):
                log["rejects"].append(("citations", b, ln, "enum/FK", r))
                continue
            # log any bool->int coercion (drift transparency; value is unchanged)
            if isinstance(q_raw, bool):
                log["bool_coerced"].append(("citations.quarantined", b, ln, kit, repr(q_raw), q))
            cite_ins.append((kit, url, r.get("archive_url"), r.get("site"),
                             r.get("author_handle"), r.get("title"), cc, rc,
                             r.get("accessed_date"), q))
            log["citations"][b] += 1

    doss_ins = []
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-dossier.jsonl")
        log["dossier"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("family")
            abst_raw = r.get("abstained", 0)
            abst = coerce_bin(abst_raw)
            if kit not in dbkits or fam not in DOSSIER_FAMILY or abst is None:
                log["rejects"].append(("dossier", b, ln, "enum/FK", r))
                continue
            if isinstance(abst_raw, bool):
                log["bool_coerced"].append(("dossier.abstained", b, ln, kit, repr(abst_raw), abst))
            payload = r.get("payload_json")
            # CHECK: abstained=1 => payload NULL. This wave every abstain row is
            # already payload-NULL; keep the strip guard for parity + safety.
            if abst == 1 and payload is not None:
                log["abstain_payload_stripped"].append(
                    (b, ln, kit, fam, json.dumps(payload, ensure_ascii=False)))
                payload = None
            payload_str = None if payload is None else json.dumps(payload, ensure_ascii=False)
            doss_ins.append((kit, fam, payload_str, r.get("source_url"),
                             r.get("anchor_quote"), abst, r.get("conf")))
            log["dossier"][b] += 1

    # ---------- promotion set: mechanics CONFIRMED & no CONTRADICTED anywhere ----------
    mech_conf, has_contra, allkits = {}, {}, set()
    for b in BATCHES:
        for _, r in load_jsonl(IN / f"batch-{b}-verify.jsonl"):
            k = r["kit_id"]; allkits.add(k)
            if r["claim_family"] == "mechanics" and r["verdict"] == "CONFIRMED":
                mech_conf[k] = True
            if r["verdict"] == "CONTRADICTED":
                has_contra[k] = True
    promote_kits = sorted(k for k in allkits
                          if mech_conf.get(k) and not has_contra.get(k))
    for k in ERRATA_KITS:
        assert k not in promote_kits, f"{k} must NOT promote (carried CONTRADICTED era)"
    # RULING check: minion-pact-bv (identity UNSUPPORTED) MUST be in the promote set
    assert "poe1-minion-pact-bv" in promote_kits, \
        "minion-pact-bv should promote (identity-UNSUPPORTED is honest silence, not a contradiction)"
    # kinetic-fusillade (era_year rekey, era CONFIRMED) MUST promote
    assert "poe1-kinetic-fusillade" in promote_kits, \
        "kinetic-fusillade should promote (era CONFIRMED; only era_year rekeyed)"

    # ---------- report ----------
    tot_v = sum(log["verify"].values())
    tot_drop = sum(log["dropped_filler"].values())
    tot_c = sum(log["citations"].values())
    tot_d = sum(log["dossier"].values())
    print("=== VDM-1 ingest wave 3 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("verify   ingested per batch:", log["verify"], "TOTAL", tot_v)
    print("dropped-filler   per batch:", log["dropped_filler"], "TOTAL", tot_drop)
    print("citations ingested per batch:", log["citations"], "TOTAL", tot_c)
    print("dossier   ingested per batch:", log["dossier"], "TOTAL", tot_d)
    print("errata marks (per kit CONTRADICTED era row):", errata_marks)
    print("bool->int coercions (drift-transparency):", len(log["bool_coerced"]))
    print("rejects (malformed enum/FK):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:4])
    print("abstain payload-stripped (note preserved in log):",
          len(log["abstain_payload_stripped"]))
    print("promote kits (%d):" % len(promote_kits), promote_kits)

    # each errata (5..8) must have marked exactly one CONTRADICTED era verify row
    for k, n in errata_marks.items():
        assert n == 1, f"errata mark for {k} hit {n} verify rows (expected 1)"

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to write.")
        con.close()
        return

    con.close()  # close the readonly handle before opening the write handle

    # ---------- single short write txn (write handle with index.lock retry) ----------
    wcon = connect_with_retry(DB)
    try:
        wcon.execute("BEGIN IMMEDIATE;")
        wcon.executemany(
            "INSERT INTO verify_ledger "
            "(kit_id, claim_family, claim_text, verdict, anchor_quote, source_url, errata_applied) "
            "VALUES (?,?,?,?,?,?,?)", verify_ins)
        wcon.executemany(
            "INSERT INTO kit_citations "
            "(kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)", cite_ins)
        wcon.executemany(
            "INSERT INTO kit_dossier "
            "(kit_id, family, payload_json, source_url, anchor_quote, abstained, conf) "
            "VALUES (?,?,?,?,?,?,?)", doss_ins)
        # ERRATA-5..8: correct canon_corpus eras (each guarded to exactly 1 row)
        for k, (old, new) in ERRATA.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?",
                (new, k, old))
            assert cur.rowcount == 1, f"errata UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # ERRATA-9: era_year rekey (NON-eras column; guarded to exactly 1 row)
        for k, (old, new) in ERAYEAR_ERRATA.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET era_year=? WHERE kit_id=? AND era_year=?",
                (new, k, old))
            assert cur.rowcount == 1, f"era_year UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # fact_provenance promotion for clean kits
        prom_rows = 0
        for k in promote_kits:
            c = wcon.execute(
                "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                "WHERE kit_id=? AND fact_provenance IN ('named-source-unfetched','kb-legacy')",
                (k,))
            log["promotions"][k] = c.rowcount
            prom_rows += c.rowcount
        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    print("\n=== APPLIED ===")
    print("promotion rowcounts per kit:", log["promotions"])
    print("total probe-fact rows promoted:", prom_rows)
    print("journal_mode:", wcon.execute("PRAGMA journal_mode;").fetchone()[0])
    print("integrity_check:", wcon.execute("PRAGMA integrity_check;").fetchone()[0])
    print("foreign_key_check:", wcon.execute("PRAGMA foreign_key_check;").fetchall())
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
