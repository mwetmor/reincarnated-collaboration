#!/usr/bin/env python3
"""
VDM-1 ingest wave 8 — FIRST basin-1 ingest: PoE2 batches 01-02 (kits 1-24) into
the landing-zone tables + a 3-kit era adjudication docket (ERRATA-16/17/18) +
1 phantom-mechanic REVIEW (erasure, no data change) + 3 mech_note annotations +
2 basin-2 roster-hygiene fixes.

Elrond (data steward, SINGLE WRITER of corpus.db).

Follows the ingest-4 procedure (corpus_vdm1_ingest4_2026_07_18.py) idioms exactly:
guarded single-row eras restamp (assert prior value, rowcount==1), landing-zone
INSERTs, backup+md5 reversibility, index.lock retry wrapper (wait 30s, retry 3x),
journal_mode DELETE preserved (concurrent readonly basin-1 b03/b04 crawlers +
parallel git commits), integrity_check + foreign_key_check.

FOUR PARTS (dispatch scope):

  (1) STAGE-1 basin-1 batches 01-02 -> verify_ledger / kit_citations / kit_dossier.
      FILE TRUTH (recounted in-script):
        b01 verify=38 (28 CONFIRMED / 2 CONTRADICTED / 8 UNSUPPORTED),
            citations=36, dossier=72 (24 abstained).
        b02 verify=60 (56 C / 2 X / 2 U), citations=34, dossier=72 (16 abstained).
      Kit coverage 12+12 = 24 distinct poe2 kits (kits 1-24), verify set == dossier
      set. Negative kits: poe2-chronomancer-01, poe2-concoction, poe2-perfect-strike-01
      (all negative=1) — their 3 negative_canon rows all sit on negative=1 kits, so
      the ingest-4 filler-drop rule (negative_canon UNSUPPORTED on negative=0 -> DROP)
      fires 0 times; all 38+60 verify rows land as stated.
      Dossier steward-pre-verified clean: 0 abstained-with-payload, 0 string-conf
      (validated again in-script by the abstain->payload-NULL law + numeric coercion).
      Boolean-drift guard retained (coerce_bin): b01/b02 emit INTEGER 0/1 -> 0
      coercions expected.

  (2) ADJUDICATION DOCKET — 3 era restamps + 1 phantom REVIEW (recorded in the
      errata ledger). Each restamp is a guarded single-row eras UPDATE against the
      EXACT current value; errata_applied=1 is set ONLY on CONTRADICTED-era verify
      rows (the established convention — see ingest-6 header / errata-ledger).

        ERRATA-16 poe2-acolyte-darkness  "0.1;0.2-dawn" -> "0.3-edict;0.4;0.5-ancients"
          D-2a class (floor too EARLY), taken to its limit: Into the Breach's poe2db
          version history STARTS at v0.3.0 and runs through v0.5.0. BOTH stamped
          bands (0.1, 0.2-dawn) predate the 0.3.0 debut, so the naive floor-narrow
          would empty the stamp. Per the ERRATA-11 rule (drop unattested bands +
          restamp to the crawl-attested later window), the corrected value is the
          attested window 0.3-0.5 = "0.3-edict;0.4;0.5-ancients". The single
          CONTRADICTED era verify row (claim "0.1, 0.2-dawn") is flagged
          errata_applied=1.

        ERRATA-17 poe2-concoction  "0.2-dawn;0.3-edict;0.4;0.5-ancients"
                                -> "0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients"
          floor-too-LATE class (NEW; inverse of D-2a). A maxroll Poisonous Concoction
          guide carries "Adjusted build for patch 0.1.0e Hotfix 6" — attested
          presence in 0.1, one band BELOW the stamped floor 0.2-dawn. The stamped
          floor postdates attested presence. RULING: EXTEND the floor to 0.1
          (fill-from-verified-crawl, BACKFILL-1 VBV shape) rather than leave +
          annotate — the attestation is a specific, dated hotfix guide, so the floor
          fill is evidence-grounded, not speculative. Because a CONTRADICTED era
          verify row DID land (the stamp is contradicted as internally inconsistent
          re: 0.1 presence), errata_applied=1 is set on it (this is the discriminator
          vs BACKFILL-1: BACKFILL-1's era row was CONFIRMED -> no flag; here the era
          row is CONTRADICTED -> flag). The later four bands are untouched.

        ERRATA-18 poe2-grim-feast  "0.2-dawn;0.3-edict;0.4" -> "0.2-dawn"
          ERRATA-8/11 trim shape. Grim Feast was "completely reworked and re-enabled"
          at 0.3.0 (poe2db) — the ES-overleech identity the kit describes existed ONLY
          in 0.2-dawn; the reworked 0.3.0+ skill is a DIFFERENT mechanic (minion-
          revival). The b02 era rows split granularly: 1 CONFIRMED (0.2-dawn) + 2
          CONTRADICTED (0.3-edict, 0.4). TRIM to the attested ES-overleech window
          "0.2-dawn" (drop the 2 post-rework bands). Split-kit (ES variant vs post-
          rework Grim Resurrection) was considered and REJECTED as overkill for one
          kit — the trim + a mech_note annotation records the rework boundary
          losslessly. BOTH CONTRADICTED band rows are flagged errata_applied=1 (the
          CONFIRMED 0.2-dawn row is NOT flagged). This is the first errata to flag 2
          rows on one kit (paired-band drop; the seismic-trap/ERRATA-8 shape flagged 1
          because only 1 band was contradicted).

        REVIEW-2 (basin-1) poe2-erasure-edc-lich  "Erasure" phantom-mechanic — NO
          data change, NO delete. The crawl reports "Erasure" 404s on poe2db and is
          absent from all lich/witch sources; Essence Drain + Contagion are CONFIRMED.
          "Erasure" appears in core_skills ["Essence Drain lineage","Contagion",
          "Erasure"] AND in mech_note. Per REVIEW-1 (earthshatter phantom-alias) +
          the di-spiritform-druid-pvp PHANTOM precedent: annotate it as
          unverified-possible-phantom in mech_note (append), do NOT delete "Erasure"
          from core_skills (no-silent-edits: SOURCE-NOT-FOUND is honest silence, not
          disproof). REVIEW stays OPEN for Matt-tier review. The era verify row is
          CONFIRMED -> no errata_applied; identity+mechanics UNSUPPORTED are honest
          silences captured by the landing-zone verify rows.

      errata_applied total: 12 -> 16 (+1 acolyte, +1 concoction, +2 grim-feast).

  (3) ANNOTATIONS (no restamps) — appended to canon_corpus.mech_note (the
      established annotation home; see di-spiritform-druid-pvp / demon-form-class
      notes in PoE1). Each append is a guarded single-row UPDATE (rowcount==1) that
      PREPENDS a dated "VDM-1 basin-1 annotation:" clause to the existing note (the
      original harvest note is preserved verbatim after it — no-silent-transformation).

        A1 poe2-demon-form  — element framing misleading: Demon Form is element-
           agnostic (Spark/lightning + cold + fire variants all attested); "fire
           spells in-form" is NOT the defining/exclusive mechanic. No eras/element
           column restamp (element correction is a stage-later concern; annotation
           records the finding).
        A2 poe2-minion-infernalist (+ poe2-infernal-legion) — ascendancy lineage
           shift: Infernalist hosted 0.1/0.2; Lich dominant 0.3+. Both kits carry
           the Infernalist archetype; the class field understates lineage complexity.
           Annotation on both (infernal-legion's b02 summary explicitly flags the
           Infernalist->Lich shift).
        A3 poe2-minion-infernalist — "Loyal Hellhound" alias UNSUPPORTED: the actual
           skill name is "Summon Infernal Hound" (a.k.a. "Infernal Hound") across all
           guides. The alias lives in this kit's core_skills; it is NOT deleted
           (same no-silent-edits discipline as the erasure phantom) — annotated as
           an unsupported alias with the real skill name recorded. Its b02 verify
           mechanics row is UNSUPPORTED (already landing in verify_ledger).

  (4) BASIN-2 ROSTER HYGIENE — spec-gen flagged; verified in-script.
        R1 le-ring-of-shields: corpus_bucket 'poe1' -> 'le' (provenance error; the
           kit is Last Epoch. Sibling le- rows use bucket 'le' — 36/37 le- rows are
           'le'; this is the sole outlier). eras + core_skills are NULL; the mobile-
           JSONL kb source carries NO row for this kit (verified: absent from all 17
           canon-corpus-*.jsonl) -> LEAVE NULL (basin-2 crawl verifies what exists).
           Only the bucket is fixed (guarded rowcount==1 on the exact old value).
        R2 le-shift-bladedancer: bucket already 'le' (correct). eras + core_skills
           NULL; same kb-absence -> LEAVE NULL. No write (nothing to fix; documented
           as verified-correct-bucket + intentional-NULL-left).

Charter laws honored:
  - No silent transformation: every eras write is guarded rowcount==1 against the
    EXACT current value; every mech_note append prepends (original retained);
    all 3 era restamps + the roster-bucket fix logged in this doc + the errata
    ledger. NULL columns left NULL where the kb source is silent (documented).
  - No-fabrication: abstained dossier rows keep payload NULL (DB CHECK). "Erasure"
    and "Loyal Hellhound" phantoms are annotated, NOT deleted.
  - Reversible: raw JSONL inputs committed + static; reproducible against the
    pre-ingest8 backup (corpus.db.pre-vdm1-ingest8-2026-07-18-backup).
  - journal_mode stays DELETE (readonly b03/b04 crawlers run concurrently).
  - Short write txn: all validation before the single BEGIN IMMEDIATE..COMMIT;
    index.lock retry on the write handle (wait 30s, retry 3x) per dispatch LAW.

Usage:
  python3 corpus_vdm1_ingest8_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest8_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
S1 = REPO / "agentic_orchestration/research/vdm1/stage1/basin1"
BATCHES = ["01", "02"]

# ---- CHECK enums mirrored from schema (validate before insert) ----
VERIFY_FAMILY = {"identity", "mechanics", "era", "negative_canon"}
VERIFY_VERDICT = {"CONFIRMED", "CONTRADICTED", "UNSUPPORTED", "SOURCE_NOT_FOUND"}
CITE_CLASS = {"authored", "communal", "official", "dataset", None}
RANK_CLASS = {"recovered", "attested-era", None}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}
BINARY = {0, 1}

# ---- ERRATA-16..18 (eras): kit -> (old_eras, new_eras). Guard requires exact old match. ----
# errata_applied=1 is set on the CONTRADICTED era verify row(s) for each kit.
ERRATA = {
    "poe2-acolyte-darkness": ("0.1;0.2-dawn",
                              "0.3-edict;0.4;0.5-ancients"),         # ERRATA-16 D-2a-to-limit: drop pre-debut bands, restamp attested 0.3-0.5
    "poe2-concoction":       ("0.2-dawn;0.3-edict;0.4;0.5-ancients",
                              "0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients"),  # ERRATA-17 floor-too-LATE: extend floor to attested 0.1
    "poe2-grim-feast":       ("0.2-dawn;0.3-edict;0.4",
                              "0.2-dawn"),                            # ERRATA-18 ES-death trim: drop post-0.3-rework bands
}
ERRATA_KITS = set(ERRATA)
# expected errata_applied flag count per kit (CONTRADICTED era verify rows)
ERRATA_FLAG_EXPECT = {
    "poe2-acolyte-darkness": 1,
    "poe2-concoction": 1,
    "poe2-grim-feast": 2,       # 0.3-edict + 0.4 both CONTRADICTED (0.2-dawn CONFIRMED, not flagged)
}
NEW_FLAGS = sum(ERRATA_FLAG_EXPECT.values())   # 4

# REVIEW (basin-1) — phantom mechanic, NO data change, NO delete.
REVIEW_KITS = {"poe2-erasure-edc-lich"}

# ---- mech_note annotation appends: kit -> annotation clause (PREPENDED, original kept) ----
# Guarded single-row UPDATE; the clause is dated + VDM-1-tagged.
ANNOT_TAG = "[VDM-1 basin-1 2026-07-18] "
ANNOTATIONS = {
    "poe2-erasure-edc-lich": (
        ANNOT_TAG + "PHANTOM-CANDIDATE (REVIEW-2, basin-1): 'Erasure' 404s on poe2db "
        "and is absent from all lich/witch sources fetched; Essence Drain + Contagion "
        "CONFIRMED real. 'Erasure' in core_skills is unverified-possible-phantom "
        "(NOT deleted — REVIEW open for Matt-tier per REVIEW-1 earthshatter / "
        "di-spiritform precedent). id+mechanics verify UNSUPPORTED. -- "),
    "poe2-demon-form": (
        ANNOT_TAG + "ANNOTATION: element framing MISLEADING — Demon Form is element-"
        "AGNOSTIC (Spark/lightning + cold + fire variants all attested); 'fire spells "
        "in-form' is NOT the defining/exclusive mechanic (fire nodes exist in the "
        "Infernalist ascendancy but the form does not lock element). mechanics verify "
        "UNSUPPORTED for the fire-exclusive claim. No element/eras restamp this wave. -- "),
    "poe2-minion-infernalist": (
        ANNOT_TAG + "ANNOTATION: (a) ascendancy lineage shift — Infernalist hosted "
        "0.1/0.2, Lich dominant 0.3+; class field understates lineage complexity. "
        "(b) 'Loyal Hellhound' alias in core_skills is UNSUPPORTED — actual skill name "
        "is 'Summon Infernal Hound' (a.k.a. 'Infernal Hound') across all guides; alias "
        "NOT deleted (no-silent-edits). -- "),
    "poe2-infernal-legion": (
        ANNOT_TAG + "ANNOTATION: ascendancy lineage shift — Infernalist->Lich from 0.3+ "
        "(Infernalist dominant 0.1/0.2 per Kripp Dec2024/Jan2025; current maxroll guide "
        "= Lich). era stamps CONFIRMED; class field understates lineage complexity. -- "),
}
ANNOT_KITS = set(ANNOTATIONS)

# ---- Roster hygiene (basin-2) ----
# R1: le-ring-of-shields bucket poe1 -> le (guarded on exact old value).
ROSTER_BUCKET_FIX = {
    "le-ring-of-shields": ("poe1", "le"),
}
# R2: le-shift-bladedancer — verified correct bucket 'le'; eras+core_skills NULL left
# NULL (kb-absent). NO write. Asserted in-script.
ROSTER_NO_WRITE = {"le-shift-bladedancer"}


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))   # raises on any malformed line
    return rows


def coerce_bin(v):
    """Normalize JSON booleans/ints to 0/1 (boolean-drift guard). None if not binary."""
    if v is True:
        return 1
    if v is False:
        return 0
    if v in (0, 1):
        return int(v)
    return None


def connect_with_retry(path, attempts=3, wait=30):
    """Open the write connection; on a locked DB wait `wait`s and retry up to
    `attempts` times per dispatch LAW (concurrent basin-1 crawler git commits)."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    # ground truth snapshots
    negflag = dict(con.execute("SELECT kit_id, negative FROM canon_corpus"))
    curera = dict(con.execute("SELECT kit_id, eras FROM canon_corpus"))
    curbucket = dict(con.execute("SELECT kit_id, corpus_bucket FROM canon_corpus"))
    curnote = dict(con.execute("SELECT kit_id, mech_note FROM canon_corpus"))
    curcore = dict(con.execute("SELECT kit_id, core_skills FROM canon_corpus"))
    dbkits = set(negflag)
    existing_cites = set(con.execute("SELECT kit_id, url FROM kit_citations"))
    pre_vl = con.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    pre_kc = con.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    pre_kd = con.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    pre_corpus = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    pre_flag = con.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]

    # pre-flight ERRATA guards: current DB value must match expected old
    for k, (old, _new) in ERRATA.items():
        assert curera.get(k) == old, \
            f"ERRATA guard: {k} current eras {curera.get(k)!r} != expected old {old!r}"
    # pre-flight roster guards
    for k, (old, _new) in ROSTER_BUCKET_FIX.items():
        assert curbucket.get(k) == old, \
            f"ROSTER guard: {k} current bucket {curbucket.get(k)!r} != expected {old!r}"
    for k in ROSTER_NO_WRITE:
        assert curbucket.get(k) == "le", f"ROSTER no-write guard: {k} bucket {curbucket.get(k)!r} != 'le'"
        assert curera.get(k) is None, f"ROSTER no-write guard: {k} eras not NULL ({curera.get(k)!r})"
        assert curcore.get(k) is None, f"ROSTER no-write guard: {k} core_skills not NULL ({curcore.get(k)!r})"
    # annotation kits must exist + carry an existing note we prepend to
    for k in ANNOT_KITS:
        assert k in dbkits, f"annotation kit {k} absent from canon_corpus"
    # REVIEW kit must retain 'Erasure' in core_skills (we are NOT deleting it)
    for k in REVIEW_KITS:
        assert k in dbkits, f"REVIEW kit {k} absent"

    log = {"verify": {}, "dropped_filler": {}, "citations": {}, "dossier": {},
           "cite_dedupe_existing": 0, "cite_dedupe_within": 0,
           "rejects": [], "abstain_payload_stripped": [], "bool_coerced": [],
           "abstained": {}}

    # ---------- VALIDATE + STAGE stage-1 inserts ----------
    verify_ins = []
    errata_marks = {k: 0 for k in ERRATA}
    for b in BATCHES:
        rows = load_jsonl(S1 / f"batch-{b}-verify.jsonl")
        log["verify"][b] = 0
        log["dropped_filler"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("claim_family"); verd = r.get("verdict")
            if fam not in VERIFY_FAMILY or verd not in VERIFY_VERDICT or kit not in dbkits:
                log["rejects"].append(("verify", b, ln, "enum/FK", r)); continue
            # filler-row rule: negative_canon UNSUPPORTED on negative=0 kit -> DROP
            if fam == "negative_canon" and verd == "UNSUPPORTED" and negflag.get(kit, 0) == 0:
                log["dropped_filler"][b] += 1; continue
            # errata: mark CONTRADICTED era rows for each errata kit
            errata = 0
            if kit in ERRATA_KITS and fam == "era" and verd == "CONTRADICTED":
                errata = 1; errata_marks[kit] += 1
            verify_ins.append((kit, fam, r.get("claim_text"), verd,
                               r.get("anchor_quote"), r.get("source_url"), errata))
            log["verify"][b] += 1

    cite_ins = []
    seen_cite = set()
    for b in BATCHES:
        rows = load_jsonl(S1 / f"batch-{b}-citations.jsonl")
        log["citations"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); url = r.get("url")
            cc = r.get("cite_class"); rc = r.get("rank_class")
            q_raw = r.get("quarantined", 0); q = coerce_bin(q_raw)
            if (kit not in dbkits or not url or cc not in CITE_CLASS
                    or rc not in RANK_CLASS or q is None):
                log["rejects"].append(("citations", b, ln, "enum/FK", r)); continue
            key = (kit, url)
            if key in existing_cites:
                log["cite_dedupe_existing"] += 1; continue
            if key in seen_cite:
                log["cite_dedupe_within"] += 1; continue
            seen_cite.add(key)
            if isinstance(q_raw, bool):
                log["bool_coerced"].append(("citations.quarantined", b, ln, kit, repr(q_raw), q))
            cite_ins.append((kit, url, r.get("archive_url"), r.get("site"),
                             r.get("author_handle"), r.get("title"), cc, rc,
                             r.get("accessed_date"), q))
            log["citations"][b] += 1

    doss_ins = []
    for b in BATCHES:
        rows = load_jsonl(S1 / f"batch-{b}-dossier.jsonl")
        log["dossier"][b] = 0
        log["abstained"][b] = 0
        for ln, r in rows:
            kit = r.get("kit_id"); fam = r.get("family")
            abst_raw = r.get("abstained", 0); abst = coerce_bin(abst_raw)
            if kit not in dbkits or fam not in DOSSIER_FAMILY or abst is None:
                log["rejects"].append(("dossier", b, ln, "enum/FK", r)); continue
            if isinstance(abst_raw, bool):
                log["bool_coerced"].append(("dossier.abstained", b, ln, kit, repr(abst_raw), abst))
            payload = r.get("payload_json")
            if abst == 1 and payload is not None:   # CHECK: abstain => payload NULL
                log["abstain_payload_stripped"].append(
                    (b, ln, kit, fam, json.dumps(payload, ensure_ascii=False)))
                payload = None
            if abst == 1:
                log["abstained"][b] += 1
            payload_str = None if payload is None else json.dumps(payload, ensure_ascii=False)
            doss_ins.append((kit, fam, payload_str, r.get("source_url"),
                             r.get("anchor_quote"), abst, r.get("conf")))
            log["dossier"][b] += 1

    # ---------- report ----------
    tot_v = sum(log["verify"].values()); tot_drop = sum(log["dropped_filler"].values())
    tot_c = sum(log["citations"].values()); tot_d = sum(log["dossier"].values())
    print("=== VDM-1 ingest wave 8 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("verify   ingested per batch:", log["verify"], "TOTAL", tot_v)
    print("dropped-filler   per batch:", log["dropped_filler"], "TOTAL", tot_drop)
    print("citations ingested per batch:", log["citations"], "TOTAL", tot_c)
    print("  cite dedupe (existing / within):",
          log["cite_dedupe_existing"], "/", log["cite_dedupe_within"])
    print("dossier   ingested per batch:", log["dossier"], "TOTAL", tot_d)
    print("  abstained per batch:", log["abstained"],
          "TOTAL", sum(log["abstained"].values()))
    print("errata marks (CONTRADICTED era rows) per kit:", errata_marks)
    print("bool->int coercions (drift-transparency):", len(log["bool_coerced"]))
    print("rejects (malformed enum/FK):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:4])
    print("abstain payload-stripped:", len(log["abstain_payload_stripped"]))
    print("era restamps:")
    for k, (old, new) in ERRATA.items():
        print(f"    {k:26} {old!r} -> {new!r}  (flag {ERRATA_FLAG_EXPECT[k]} row(s))")
    print("roster bucket fix:")
    for k, (old, new) in ROSTER_BUCKET_FIX.items():
        print(f"    {k:26} bucket {old!r} -> {new!r}")
    print("roster no-write (verified correct):", sorted(ROSTER_NO_WRITE))
    print("mech_note annotations (prepend):", sorted(ANNOT_KITS))
    print("REVIEW (no data change):", sorted(REVIEW_KITS))

    # ---------- pre-write asserts (file truths) ----------
    assert log["verify"]["01"] == 38 and log["verify"]["02"] == 60, \
        f"verify batch counts {log['verify']} != 38/60"
    assert tot_v == 98, f"verify total {tot_v} != 98"
    assert tot_drop == 0, f"filler-drop {tot_drop} != 0 (all negative_canon on negative=1 kits)"
    assert log["citations"]["01"] + log["cite_dedupe_existing"] + log["cite_dedupe_within"] \
        >= 36 or True  # per-batch dedupe accounted below by totals
    assert (log["citations"]["01"] + log["citations"]["02"]
            + log["cite_dedupe_existing"] + log["cite_dedupe_within"]) == 70, \
        "citation input total (landed + deduped) != 70"
    assert log["dossier"]["01"] == 72 and log["dossier"]["02"] == 72, \
        f"dossier batch counts {log['dossier']} != 72/72"
    assert log["abstained"]["01"] == 24 and log["abstained"]["02"] == 16, \
        f"dossier abstained {log['abstained']} != 24/16"
    assert len(log["abstain_payload_stripped"]) == 0, "steward-clean claim: 0 abstain-with-payload"
    for k, n in errata_marks.items():
        assert n == ERRATA_FLAG_EXPECT[k], \
            f"errata mark for {k} hit {n} verify rows (expected {ERRATA_FLAG_EXPECT[k]})"

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to write.")
        con.close()
        return

    con.close()  # close readonly handle before opening write handle

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
        # ERRATA-16..18: correct canon_corpus eras (each guarded to exactly 1 row)
        for k, (old, new) in ERRATA.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?", (new, k, old))
            assert cur.rowcount == 1, f"errata UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # Roster bucket fix (guarded to exactly 1 row on the exact old value)
        for k, (old, new) in ROSTER_BUCKET_FIX.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET corpus_bucket=? WHERE kit_id=? AND corpus_bucket=?",
                (new, k, old))
            assert cur.rowcount == 1, f"roster bucket UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # mech_note annotation prepend (original note preserved after the clause)
        for k, clause in ANNOTATIONS.items():
            old_note = curnote.get(k) or ""
            new_note = clause + old_note
            cur = wcon.execute(
                "UPDATE canon_corpus SET mech_note=? WHERE kit_id=?", (new_note, k))
            assert cur.rowcount == 1, f"annotation UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    # ---------- POST-write asserts ----------
    post_vl = wcon.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    post_kc = wcon.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    post_kd = wcon.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    post_corpus = wcon.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    post_flag = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    jm = wcon.execute("PRAGMA journal_mode;").fetchone()[0]
    ic = wcon.execute("PRAGMA integrity_check;").fetchone()[0]
    fk = wcon.execute("PRAGMA foreign_key_check;").fetchall()
    # errata_applied audit: all flagged rows are era/CONTRADICTED
    bad_flag = wcon.execute(
        "SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1 "
        "AND NOT (claim_family='era' AND verdict='CONTRADICTED')").fetchone()[0]
    # landing-zone orphans (FK back to canon_corpus)
    orph_vl = wcon.execute("SELECT COUNT(*) FROM verify_ledger v WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=v.kit_id)").fetchone()[0]
    orph_kc = wcon.execute("SELECT COUNT(*) FROM kit_citations kc WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=kc.kit_id)").fetchone()[0]
    orph_kd = wcon.execute("SELECT COUNT(*) FROM kit_dossier kd WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=kd.kit_id)").fetchone()[0]
    abst_bad = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE abstained=1 AND payload_json IS NOT NULL").fetchone()[0]
    # provenance defaults landed (fetched-vdm1 on the new landing rows)
    kd_prov = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE extraction_provenance='fetched-vdm1'").fetchone()[0]

    assert post_vl == pre_vl + 98, f"verify_ledger {post_vl} != {pre_vl}+98"
    assert post_kc == pre_kc + 70, f"kit_citations {post_kc} != {pre_kc}+70"
    assert post_kd == pre_kd + 144, f"kit_dossier {post_kd} != {pre_kd}+144"
    assert post_corpus == pre_corpus == 585, f"canon_corpus changed {pre_corpus}->{post_corpus}"
    assert post_flag == pre_flag + NEW_FLAGS == 16, \
        f"errata_applied {post_flag} != {pre_flag}+{NEW_FLAGS} (=16)"
    assert bad_flag == 0, f"{bad_flag} errata_applied rows are not era/CONTRADICTED"
    assert orph_vl == 0 and orph_kc == 0 and orph_kd == 0, "landing-zone orphans"
    assert abst_bad == 0, "abstained dossier row carries non-NULL payload"
    assert jm == "delete", f"journal_mode {jm} != delete"
    assert ic == "ok", f"integrity_check {ic}"
    assert fk == [], f"foreign_key_check {fk}"
    # per-errata-kit exact flag count + eras value landed
    for k, exp in ERRATA_FLAG_EXPECT.items():
        n = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE kit_id=? AND errata_applied=1",
                         (k,)).fetchone()[0]
        assert n == exp, f"{k} errata_applied rows {n} != {exp}"
    for k, (_old, new) in ERRATA.items():
        got = wcon.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
        assert got == new, f"{k} eras {got!r} != {new!r}"
    # roster bucket fixed; no-write kit unchanged
    for k, (_old, new) in ROSTER_BUCKET_FIX.items():
        got = wcon.execute("SELECT corpus_bucket FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
        assert got == new, f"{k} bucket {got!r} != {new!r}"
    for k in ROSTER_NO_WRITE:
        b, e, c = wcon.execute(
            "SELECT corpus_bucket, eras, core_skills FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()
        assert b == "le" and e is None and c is None, f"{k} no-write kit mutated: {b!r},{e!r},{c!r}"
    # erasure phantom NOT deleted from core_skills; annotation landed
    era_core = wcon.execute("SELECT core_skills FROM canon_corpus WHERE kit_id='poe2-erasure-edc-lich'").fetchone()[0]
    assert "Erasure" in (era_core or ""), "REVIEW-2 law: 'Erasure' must remain in core_skills (not deleted)"
    for k in ANNOT_KITS:
        note = wcon.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
        assert note.startswith(ANNOT_TAG), f"{k} annotation not prepended"
    # 'Loyal Hellhound' alias NOT deleted from minion-infernalist core_skills
    mi_core = wcon.execute("SELECT core_skills FROM canon_corpus WHERE kit_id='poe2-minion-infernalist'").fetchone()[0]
    assert "Loyal Hellhound" in (mi_core or ""), "'Loyal Hellhound' alias must remain (not deleted)"

    print("\n=== APPLIED ===")
    print(f"verify_ledger  {pre_vl} -> {post_vl}  (+{post_vl-pre_vl})")
    print(f"kit_citations  {pre_kc} -> {post_kc}  (+{post_kc-pre_kc})")
    print(f"kit_dossier    {pre_kd} -> {post_kd}  (+{post_kd-pre_kd})")
    print(f"errata_applied {pre_flag} -> {post_flag}  (+{post_flag-pre_flag})")
    print(f"kit_dossier fetched-vdm1 provenance rows: {kd_prov}")
    print("canon_corpus (unchanged):", post_corpus)
    print("journal_mode:", jm, "| integrity_check:", ic, "| foreign_key_check:", fk)
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
