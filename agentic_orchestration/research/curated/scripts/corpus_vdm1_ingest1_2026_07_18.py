#!/usr/bin/env python3
"""
VDM-1 ingest wave 1 — PoE1 batches 01-02 into landing-zone tables.

Elrond (data steward, SINGLE WRITER of corpus.db).

Loads three JSONL streams per batch (verify / citations / dossier) into
verify_ledger / kit_citations / kit_dossier, and applies the run's first errata.

Charter laws honored:
  - No silent transformation: every deviation from raw input is logged and,
    where content is altered (the 2 payload-carrying abstain rows), the raw
    value is preserved verbatim in the migration doc.
  - No-fabrication: abstained rows keep payload NULL (DB CHECK); the abstain
    note is metadata, moved to the log, never injected into anchor_quote.
  - Reversible: raw JSONL inputs are committed and static; this run is
    reproducible from them.
  - journal_mode stays DELETE (readonly crawlers run concurrently).
  - Short write txn: all validation happens BEFORE the single BEGIN..COMMIT.

Filler-row rule:
  negative_canon UNSUPPORTED rows on canon_corpus.negative=0 kits are
  N/A-filler (not honest silence) and are DROPPED at ingest, per batch.
  negative_canon rows on negative=1 kits ingest normally.

ERRATA-1 (batch-02, CONTRADICTED):
  poe1-crackling-lance eras "3.7-3.13" -> "3.12-3.13" (debut patch 3.12.0,
  Heist, 2020-09). errata_applied=1 set on the ingested crackling-lance era row.

fact_provenance promotion:
  kits with mechanics=CONFIRMED and ZERO CONTRADICTED verdicts anywhere flip
  canon_probe_facts.fact_provenance -> 'verified-v1.1'. crackling-lance is
  excluded (carried a CONTRADICTED era).

Usage:
  python3 corpus_vdm1_ingest1_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest1_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
IN = REPO / "agentic_orchestration/research/vdm1/stage1/poe1"
BATCHES = ["01", "02"]

# ---- CHECK enums mirrored from schema (validate before insert) ----
VERIFY_FAMILY = {"identity", "mechanics", "era", "negative_canon"}
VERIFY_VERDICT = {"CONFIRMED", "CONTRADICTED", "UNSUPPORTED", "SOURCE_NOT_FOUND"}
CITE_CLASS = {"authored", "communal", "official", "dataset", None}
RANK_CLASS = {"recovered", "attested-era", None}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}
BINARY = {0, 1}

# ERRATA-1
CL_KIT = "poe1-crackling-lance"
CL_OLD_ERAS = "3.7-3.13"
CL_NEW_ERAS = "3.12-3.13"


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys=ON;")

    # ground truth: negative flag + probe-fact provenance snapshot
    negflag = dict(con.execute("SELECT kit_id, negative FROM canon_corpus"))
    dbkits = set(negflag)

    log = {"verify": {}, "dropped_filler": {}, "citations": {}, "dossier": {},
           "rejects": [], "abstain_payload_stripped": [], "promotions": {}}

    # ---------- VALIDATE + STAGE all inserts (no DB writes yet) ----------
    verify_ins = []   # tuples for insert
    errata_marks = 0
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-verify.jsonl")
        log["verify"][b] = 0
        log["dropped_filler"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("claim_family"); verd = r.get("verdict")
            # enum + FK validation
            if fam not in VERIFY_FAMILY or verd not in VERIFY_VERDICT or kit not in dbkits:
                log["rejects"].append(("verify", b, ln, "enum/FK", r))
                continue
            # filler-row rule: negative_canon UNSUPPORTED on negative=0 kit -> DROP
            if fam == "negative_canon" and verd == "UNSUPPORTED" and negflag.get(kit, 0) == 0:
                log["dropped_filler"][b] += 1
                continue
            # ERRATA-1: mark the crackling-lance era row
            errata = 0
            if kit == CL_KIT and fam == "era":
                errata = 1
                errata_marks += 1
            verify_ins.append((kit, fam, r.get("claim_text"), verd,
                               r.get("anchor_quote"), r.get("source_url"), errata))
            log["verify"][b] += 1

    cite_ins = []
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-citations.jsonl")
        log["citations"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); url = r.get("url")
            cc = r.get("cite_class"); rc = r.get("rank_class"); q = r.get("quarantined", 0)
            if (kit not in dbkits or not url or cc not in CITE_CLASS
                    or rc not in RANK_CLASS or q not in BINARY):
                log["rejects"].append(("citations", b, ln, "enum/FK", r))
                continue
            cite_ins.append((kit, url, r.get("archive_url"), r.get("site"),
                             r.get("author_handle"), r.get("title"), cc, rc,
                             r.get("accessed_date"), q))
            log["citations"][b] += 1

    doss_ins = []
    for b in BATCHES:
        rows = load_jsonl(IN / f"batch-{b}-dossier.jsonl")
        log["dossier"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("family"); abst = r.get("abstained", 0)
            if kit not in dbkits or fam not in DOSSIER_FAMILY or abst not in BINARY:
                log["rejects"].append(("dossier", b, ln, "enum/FK", r))
                continue
            payload = r.get("payload_json")
            # CHECK: abstained=1 => payload NULL. Two rows carry an explanatory
            # {"note":...}; strip to NULL to satisfy the constraint, preserve the
            # note verbatim in the log (documented, not silent).
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
    assert CL_KIT not in promote_kits, "crackling-lance must NOT promote (CONTRADICTED era)"

    # ---------- report ----------
    tot_v = sum(log["verify"].values())
    tot_drop = sum(log["dropped_filler"].values())
    tot_c = sum(log["citations"].values())
    tot_d = sum(log["dossier"].values())
    print("=== VDM-1 ingest wave 1 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("verify   ingested per batch:", log["verify"], "TOTAL", tot_v)
    print("dropped-filler   per batch:", log["dropped_filler"], "TOTAL", tot_drop)
    print("citations ingested per batch:", log["citations"], "TOTAL", tot_c)
    print("dossier   ingested per batch:", log["dossier"], "TOTAL", tot_d)
    print("errata marks (crackling-lance era rows):", errata_marks)
    print("rejects (malformed enum/FK):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:4])
    print("abstain payload-stripped (note preserved in log):",
          len(log["abstain_payload_stripped"]))
    for a in log["abstain_payload_stripped"]:
        print("   STRIP b%s ln%s %s/%s note=%s" % a)
    print("promote kits (%d):" % len(promote_kits), promote_kits)

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to write.")
        con.close()
        return

    # ---------- single short write txn ----------
    try:
        con.execute("BEGIN IMMEDIATE;")
        con.executemany(
            "INSERT INTO verify_ledger "
            "(kit_id, claim_family, claim_text, verdict, anchor_quote, source_url, errata_applied) "
            "VALUES (?,?,?,?,?,?,?)", verify_ins)
        con.executemany(
            "INSERT INTO kit_citations "
            "(kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)", cite_ins)
        con.executemany(
            "INSERT INTO kit_dossier "
            "(kit_id, family, payload_json, source_url, anchor_quote, abstained, conf) "
            "VALUES (?,?,?,?,?,?,?)", doss_ins)
        # ERRATA-1: correct canon_corpus eras for crackling-lance
        cur = con.execute(
            "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?",
            (CL_NEW_ERAS, CL_KIT, CL_OLD_ERAS))
        assert cur.rowcount == 1, f"errata UPDATE hit {cur.rowcount} rows (expected 1)"
        # fact_provenance promotion for clean kits
        prom_rows = 0
        for k in promote_kits:
            c = con.execute(
                "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                "WHERE kit_id=? AND fact_provenance IN ('named-source-unfetched','kb-legacy')",
                (k,))
            log["promotions"][k] = c.rowcount
            prom_rows += c.rowcount
        con.commit()
    except Exception:
        con.rollback()
        raise

    print("\n=== APPLIED ===")
    print("promotion rowcounts per kit:", log["promotions"])
    print("total probe-fact rows promoted:", prom_rows)
    print("journal_mode:", con.execute("PRAGMA journal_mode;").fetchone()[0])
    print("integrity_check:", con.execute("PRAGMA integrity_check;").fetchone()[0])
    con.close()


if __name__ == "__main__":
    sys.exit(main())
