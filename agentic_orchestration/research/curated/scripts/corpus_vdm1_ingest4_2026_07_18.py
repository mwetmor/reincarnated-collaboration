#!/usr/bin/env python3
"""
VDM-1 ingest wave 4 — PoE1 batches 07-08 (22 kits) into landing-zone tables
+ ERRATA-10..13 (four b08-era era corrections) + Vaal-Blade-Vortex era backfill
+ Unattested-Register + floor-based bucket-audit register annotations
+ fact_provenance promotions
+ FIRST kit_mapping ingest wave (48 rows, stage2 mapping-batch-01..04).

Elrond (data steward, SINGLE WRITER of corpus.db).

Follows the ingest-3 procedure (corpus_vdm1_ingest3_2026_07_18.py) exactly. Five
parts (dispatch scope):

  (1) STAGE-1 batches 07-08 -> verify_ledger / kit_citations / kit_dossier.
      b07 verify=53 (44 CONFIRMED / 9 UNSUPPORTED / 0 CONTRA), citations=38,
      dossier=72 (25 abstained). b08 verify=46 (37 C / 4 CONTRADICTED / 5 U),
      citations=34, dossier=60 (4 abstained). Kit coverage 12+10. Negative kits:
      poe1-sweep (b07) + poe1-wild-strike (b08), both negative=1, negative_canon
      CONFIRMED -> substantive, 0 filler dropped.
      NOTE: batch-07-dossier line 2 (poe1-spectral-throw/skill_geometry) had a
      premature close-brace repaired by the steward via parse-and-merge; file now
      parses clean (validated in-script by load_jsonl -> json.loads).
      Boolean-drift: b07/b08 emit INTEGER 0/1 for abstained + quarantined (NO JSON
      booleans this wave), so coerce_bin fires 0 bool-coercions (guard retained for
      parity/safety, same as ingest-3's dossier.abstained path).

  (2) ERRATA-10..13 — all four b08-era era corrections. Each is a CONTRADICTED
      verify row carrying its anchor; each canon_corpus.eras UPDATE is guarded to
      hit EXACTLY 1 row against the exact current DB value; errata_applied=1 set on
      the single CONTRADICTED era verify row per kit.
        ERRATA-10 poe1-venom-gyre   "3.7-3.13;3.20+"    -> "3.8-3.13;3.20+"
                  debut-inside-bucket: Venom Gyre introduced 3.8.0; the 3.7-3.13
                  band floor 3.7 predates it -> floor 3.7->3.8.
        ERRATA-11 poe1-viper-poison "3.0-3.6;3.7-3.13"  -> "3.7-3.13"
                  RESTAMP (not blanket DROP) under the ERRATA-8 seismic-trap
                  precedent. The ENTIRE 3.0-3.6 bucket is a combined-kit
                  impossibility: co-skill Pestilent Strike debuts 3.8.0, so the
                  dual-skill Assassin archetype as stamped cannot exist pre-3.8.
                  ADJUDICATION: the b08 anchors DO attest a specific later window --
                  a CONFIRMED positive era row on 3.7-3.13 ("[3.8] Pestilent Strike
                  & Viper Strike Poison Assassin" thread by tylam6746, patch 3.8).
                  Per ERRATA-8's rule ("restamp only if b08 anchors attest a
                  specific later window; DROP only if no in-bucket attestation"),
                  since a later band IS attested we DROP only the unattested 3.0-3.6
                  bucket and KEEP the attested 3.7-3.13 -> "3.7-3.13".
        ERRATA-12 poe1-ward-loop    "3.14-3.19;3.20+"   -> "3.15-3.19;3.20+"
                  debut-inside-bucket: Ward mechanic debut 3.15 (Expedition); the
                  3.14-3.19 band floor 3.14 predates Ward -> floor 3.14->3.15.
        ERRATA-13 poe1-winter-orb   "3.0-3.6"           -> "3.5-3.6"
                  debut-inside-bucket: Winter Orb debut 3.5.0 (Betrayal;
                  poe.ninja 9% at 3.5); the 3.0-3.6 band floor 3.0 predates it by
                  five patches -> floor 3.0->3.5.

  (3) ERA FILLS + REGISTER ANNOTATIONS (NOT errata):
        - poe1-vaal-blade-vortex: DB eras EMPTY (DB-only census kit). b07 era
          verdict CONFIRMED; anchor attests "added 3.3.0 ... 3.7-3.13 era presence".
          BACKFILL eras -> "3.0-3.6;3.7-3.13" (3.3.0 debut lands in the 3.0-3.6
          bucket; the 3.8 guide confirms 3.7-3.13). Guarded UPDATE eras='' -> value,
          rowcount==1. This is a fill of an EMPTY column from a CONFIRMED crawl, NOT
          an errata (no prior value contradicted) -> NO errata_applied flag; recorded
          here + migration doc as a fill-from-verified-crawl provenance note.
        - poe1-totem-hierophant: era UNSUPPORTED ("Era stamps absent from DB --
          cannot verify era claims"); eras unrecoverable from search -> UNATTESTED
          REGISTER entry. NO data write (eras stays EMPTY). Charter stream-1:
          UNSUPPORTED/SOURCE-NOT-FOUND on an unrecoverable axis -> Unattested
          Register (the landing-zone verify row is the record).
        - poe1-tectonic-slam (intro 3.2.0) + poe1-toxic-rain (intro 3.4.0): b07
          graded their 3.0-3.6 floor stamps CONFIRMED (genuine back-half presence),
          so NO errata basis. Their attested introduction patches are attached to
          their floor-based bucket-audit register rows (annotation only) for the
          stage-3 systematic sweep. NO data write.

  (4) PROMOTIONS per the standing gate (mechanics=CONFIRMED AND zero CONTRADICTED
      anywhere on the kit) for b07/08 kits -> verified-v1.1. The four ERRATA-10..13
      kits carry a CONTRADICTED era -> EXCLUDED (their probe facts stay legacy).
      poe1-wormblaster FAILS the gate directly: mechanics=UNSUPPORTED (pobarchives
      403'd; the 3.3 forum thread shows a Flameblast / Herald of Ash Slayer variant,
      NOT the claimed CoC+Barrage+Pathfinder). It has 0 CONTRADICTED but is NOT in
      the promote set (mechanics!=CONFIRMED) -> stays legacy, flagged for stage-4
      residue. Asserted NOT in promote_kits.

  (5) kit_mapping FIRST WAVE -- 48 rows from stage2/poe1/mapping-batch-01..04.jsonl
      (provenance authored-vdm1). Steward-audited ACCEPTED (post-audit file state is
      truth). ASSERTS: grade histogram EXACT 2 / CLOSE 32 / APPROX 10 / GAPPED 4;
      terminal MAPPED_DOCKET rows == exactly the 4 GAPPED rows (R-M7 1:1 law);
      48 distinct kit_ids all present in canon_corpus. The mint-candidates /
      docket-candidates / *-summary side files are NOT ingested (await steward
      ratification at stage-3).

Charter laws honored (unchanged):
  - No silent transformation: every deviation from raw input is logged (this doc +
    errata ledger). Every era write is guarded rowcount==1 against the exact old
    value.
  - No-fabrication: abstained dossier rows keep payload NULL (DB CHECK). This wave
    29 abstained rows (b07=25, b08=4), ALL already payload-NULL (0 stripped).
  - Reversible: raw JSONL inputs are committed + static; reproducible against the
    pre-ingest4 backup.
  - journal_mode stays DELETE (readonly crawlers + mapping agents run concurrently).
  - Short write txn: all validation before the single BEGIN..COMMIT; index.lock
    retry on the write handle (wait 30s, retry 3x) per dispatch LAW.

Usage:
  python3 corpus_vdm1_ingest4_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest4_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
S1 = REPO / "agentic_orchestration/research/vdm1/stage1/poe1"
S2 = REPO / "agentic_orchestration/research/vdm1/stage2/poe1"
BATCHES = ["07", "08"]
MAP_BATCHES = ["01", "02", "03", "04"]

# ---- CHECK enums mirrored from schema (validate before insert) ----
VERIFY_FAMILY = {"identity", "mechanics", "era", "negative_canon"}
VERIFY_VERDICT = {"CONFIRMED", "CONTRADICTED", "UNSUPPORTED", "SOURCE_NOT_FOUND"}
CITE_CLASS = {"authored", "communal", "official", "dataset", None}
RANK_CLASS = {"recovered", "attested-era", None}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}
MAP_GRADE = {"EXACT", "CLOSE", "APPROX", "GAPPED"}
MAP_TERMINAL = {"MAPPED", "MAPPED_DOCKET"}
BINARY = {0, 1}

# ---- ERRATA-10..13 (eras): kit -> (old_eras, new_eras). Guard requires exact old match. ----
# Each is a CONTRADICTED b08 era row carrying its anchor; errata_applied=1 set on
# the single CONTRADICTED era verify row per kit.
ERRATA = {
    "poe1-venom-gyre":  ("3.7-3.13;3.20+",    "3.8-3.13;3.20+"),  # ERRATA-10 debut 3.8.0 floor 3.7->3.8
    "poe1-viper-poison": ("3.0-3.6;3.7-3.13", "3.7-3.13"),        # ERRATA-11 RESTAMP: drop unattested 3.0-3.6, keep attested 3.7-3.13
    "poe1-ward-loop":   ("3.14-3.19;3.20+",   "3.15-3.19;3.20+"), # ERRATA-12 Ward debut 3.15 floor 3.14->3.15
    "poe1-winter-orb":  ("3.0-3.6",           "3.5-3.6"),         # ERRATA-13 debut 3.5.0 floor 3.0->3.5
}
ERRATA_KITS = set(ERRATA)

# ---- ERA BACKFILL (fill NULL eras from a CONFIRMED crawl; NOT errata; no errata_applied) ----
# poe1-vaal-blade-vortex: eras NULL -> value. DB-only census kits carry SQL NULL
# (not '') in eras; guard requires the current value IS NULL and the UPDATE matches
# `eras IS NULL` (rowcount==1). old sentinel is Python None.
ERA_BACKFILL = {
    "poe1-vaal-blade-vortex": (None, "3.0-3.6;3.7-3.13"),
}

# Kits that get register annotations only (NO data write) -- documented, not written.
UNATTESTED_REGISTER = {"poe1-totem-hierophant"}       # era unrecoverable -> Unattested Register
REGISTER_INTRO_ANNOT = {                               # CONFIRMED floors; attach intro patch to register row
    "poe1-tectonic-slam": "3.2.0",
    "poe1-toxic-rain":    "3.4.0",
}

# Wide-bucket floors for the floor-based stage-3 bucket-audit register selector.
WIDE_BUCKETS = ("3.0-3.6", "3.7-3.13", "3.14-3.19")


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))   # raises on any malformed line (defect-repair validation)
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


def era_floor(eras):
    """Leftmost band of a ';'-joined eras string ('' -> '')."""
    if not eras:
        return ""
    return eras.split(";")[0]


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute writes (default: dry-run)")
    args = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    # ground truth snapshots
    negflag = dict(con.execute("SELECT kit_id, negative FROM canon_corpus"))
    curera = dict(con.execute("SELECT kit_id, eras FROM canon_corpus"))
    dbkits = set(negflag)
    pre_km = con.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    pre_vl = con.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    pre_kc = con.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    pre_kd = con.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    pre_v11 = con.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'").fetchone()[0]
    pre_corpus = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]

    # pre-flight ERRATA / BACKFILL guards: current DB value must match expected old
    for k, (old, _new) in ERRATA.items():
        assert curera.get(k) == old, \
            f"ERRATA guard: {k} current eras {curera.get(k)!r} != expected old {old!r}"
    for k, (old, _new) in ERA_BACKFILL.items():
        assert old is None and curera.get(k) is None, \
            f"BACKFILL guard: {k} current eras {curera.get(k)!r} != expected NULL"

    log = {"verify": {}, "dropped_filler": {}, "citations": {}, "dossier": {},
           "mapping": 0, "rejects": [], "abstain_payload_stripped": [],
           "bool_coerced": [], "promotions": {}}

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
            # errata: mark the single CONTRADICTED era row for each errata kit
            errata = 0
            if kit in ERRATA_KITS and fam == "era" and verd == "CONTRADICTED":
                errata = 1; errata_marks[kit] += 1
            verify_ins.append((kit, fam, r.get("claim_text"), verd,
                               r.get("anchor_quote"), r.get("source_url"), errata))
            log["verify"][b] += 1

    cite_ins = []
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
            payload_str = None if payload is None else json.dumps(payload, ensure_ascii=False)
            doss_ins.append((kit, fam, payload_str, r.get("source_url"),
                             r.get("anchor_quote"), abst, r.get("conf")))
            log["dossier"][b] += 1

    # ---------- VALIDATE + STAGE kit_mapping inserts (first wave) ----------
    map_ins = []
    grade_hist = {g: 0 for g in MAP_GRADE}
    term_hist = {t: 0 for t in MAP_TERMINAL}
    gapped_kits, docket_kits, map_kits = [], [], []
    for b in MAP_BATCHES:
        rows = load_jsonl(S2 / f"mapping-batch-{b}.jsonl")
        for ln, r in rows:
            kit = r.get("kit_id"); grade = r.get("grade"); term = r.get("terminal_state")
            if kit not in dbkits or grade not in MAP_GRADE or term not in MAP_TERMINAL:
                log["rejects"].append(("mapping", b, ln, "enum/FK", r)); continue
            mj = r.get("mapping_json")
            mj_str = None if mj is None else json.dumps(mj, ensure_ascii=False)
            map_ins.append((kit, mj_str, grade, r.get("deviation_notes"), term))
            grade_hist[grade] += 1
            term_hist[term] += 1
            map_kits.append(kit)
            if grade == "GAPPED":
                gapped_kits.append(kit)
            if term == "MAPPED_DOCKET":
                docket_kits.append(kit)
    log["mapping"] = len(map_ins)

    # ---------- promotion set: mechanics CONFIRMED & no CONTRADICTED anywhere ----------
    mech_conf, has_contra, allkits = {}, {}, set()
    for b in BATCHES:
        for _, r in load_jsonl(S1 / f"batch-{b}-verify.jsonl"):
            k = r["kit_id"]; allkits.add(k)
            if r["claim_family"] == "mechanics" and r["verdict"] == "CONFIRMED":
                mech_conf[k] = True
            if r["verdict"] == "CONTRADICTED":
                has_contra[k] = True
    promote_kits = sorted(k for k in allkits if mech_conf.get(k) and not has_contra.get(k))
    for k in ERRATA_KITS:
        assert k not in promote_kits, f"{k} must NOT promote (carried CONTRADICTED era)"
    # wormblaster FAILS the gate (mechanics UNSUPPORTED) -> must NOT be in promote set
    assert "poe1-wormblaster" not in promote_kits, \
        "wormblaster must NOT promote (mechanics=UNSUPPORTED: pobarchives 403; wrong-variant forum evidence)"

    # ---------- compute post-wave-4 floor-based bucket-audit register (annotation) ----------
    # A kit qualifies iff its era FLOOR (leftmost band) equals a wide bucket AND it
    # has NOT been individually verified/errata'd across waves 1-4. State reflects
    # post-wave-4 errata + backfill applied in-memory.
    proj_era = dict(curera)
    for k, (_old, new) in ERRATA.items():
        proj_era[k] = new
    for k, (_old, new) in ERA_BACKFILL.items():
        proj_era[k] = new
    verified_kits = set(r[0] for r in con.execute("SELECT DISTINCT kit_id FROM verify_ledger"))
    verified_kits |= allkits   # + this wave's crawled kits (not yet committed)
    register = []
    for k, e in sorted(proj_era.items()):
        if era_floor(e) in WIDE_BUCKETS and k not in verified_kits:
            register.append((k, e, era_floor(e)))

    # ---------- report ----------
    tot_v = sum(log["verify"].values()); tot_drop = sum(log["dropped_filler"].values())
    tot_c = sum(log["citations"].values()); tot_d = sum(log["dossier"].values())
    print("=== VDM-1 ingest wave 4 (%s) ===" % ("APPLY" if args.apply else "DRY-RUN"))
    print("verify   ingested per batch:", log["verify"], "TOTAL", tot_v)
    print("dropped-filler   per batch:", log["dropped_filler"], "TOTAL", tot_drop)
    print("citations ingested per batch:", log["citations"], "TOTAL", tot_c)
    print("dossier   ingested per batch:", log["dossier"], "TOTAL", tot_d)
    print("kit_mapping ingested:", log["mapping"])
    print("  grade histogram:", grade_hist)
    print("  terminal histogram:", term_hist)
    print("  GAPPED kits:", sorted(gapped_kits))
    print("  MAPPED_DOCKET kits:", sorted(docket_kits))
    print("  distinct mapping kit_ids:", len(set(map_kits)))
    print("errata marks (per kit CONTRADICTED era row):", errata_marks)
    print("bool->int coercions (drift-transparency):", len(log["bool_coerced"]))
    print("rejects (malformed enum/FK):", len(log["rejects"]))
    for rj in log["rejects"]:
        print("   REJECT", rj[:4])
    print("abstain payload-stripped:", len(log["abstain_payload_stripped"]))
    print("promote kits (%d):" % len(promote_kits), promote_kits)
    print("post-wave-4 floor-based bucket-audit register (%d):" % len(register))
    for k, e, fl in register:
        annot = ""
        if k in UNATTESTED_REGISTER:
            annot = "  [UNATTESTED-REGISTER: era unrecoverable]"
        elif k in REGISTER_INTRO_ANNOT:
            annot = f"  [intro {REGISTER_INTRO_ANNOT[k]}; CONFIRMED floor]"
        print(f"    {k:32} {e:36} floor={fl}{annot}")

    # ---------- pre-write asserts ----------
    # verify tallies match dispatch file truths
    assert tot_v == 53 + 46 == 99, f"verify total {tot_v} != 99"
    assert log["citations"]["07"] == 38 and log["citations"]["08"] == 34, "citation batch counts"
    assert log["dossier"]["07"] == 72 and log["dossier"]["08"] == 60, "dossier batch counts"
    # each errata (10..13) marked exactly one CONTRADICTED era verify row
    for k, n in errata_marks.items():
        assert n == 1, f"errata mark for {k} hit {n} verify rows (expected 1)"
    # kit_mapping histogram asserts (dispatch file truths)
    assert grade_hist == {"EXACT": 2, "CLOSE": 32, "APPROX": 10, "GAPPED": 4}, \
        f"grade histogram {grade_hist} != EXACT2/CLOSE32/APPROX10/GAPPED4"
    assert term_hist == {"MAPPED": 44, "MAPPED_DOCKET": 4}, f"terminal histogram {term_hist}"
    assert sorted(docket_kits) == sorted(gapped_kits), \
        "R-M7 1:1 law: MAPPED_DOCKET rows must equal the GAPPED rows exactly"
    assert len(set(map_kits)) == 48 and len(map_kits) == 48, \
        f"expected 48 distinct mapping kits, got {len(set(map_kits))}/{len(map_kits)}"
    assert len(map_ins) == 48, f"map_ins {len(map_ins)} != 48"

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
        wcon.executemany(
            "INSERT INTO kit_mapping "
            "(kit_id, mapping_json, grade, deviation_notes, terminal_state) "
            "VALUES (?,?,?,?,?)", map_ins)
        # ERRATA-10..13: correct canon_corpus eras (each guarded to exactly 1 row)
        for k, (old, new) in ERRATA.items():
            cur = wcon.execute(
                "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras=?", (new, k, old))
            assert cur.rowcount == 1, f"errata UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # ERA BACKFILL (VBV): fill NULL eras (guarded to exactly 1 row on `eras IS NULL`)
        for k, (old, new) in ERA_BACKFILL.items():
            assert old is None
            cur = wcon.execute(
                "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND eras IS NULL", (new, k))
            assert cur.rowcount == 1, f"backfill UPDATE {k} hit {cur.rowcount} rows (expected 1)"
        # fact_provenance promotion for clean kits
        prom_rows = 0
        for k in promote_kits:
            c = wcon.execute(
                "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                "WHERE kit_id=? AND fact_provenance IN ('named-source-unfetched','kb-legacy')", (k,))
            log["promotions"][k] = c.rowcount
            prom_rows += c.rowcount
        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    # ---------- POST-write asserts ----------
    post_vl = wcon.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    post_kc = wcon.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    post_kd = wcon.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    post_km = wcon.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    post_v11 = wcon.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'").fetchone()[0]
    post_corpus = wcon.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    jm = wcon.execute("PRAGMA journal_mode;").fetchone()[0]
    ic = wcon.execute("PRAGMA integrity_check;").fetchone()[0]
    fk = wcon.execute("PRAGMA foreign_key_check;").fetchall()
    # errata_applied audit: all flagged rows are era/CONTRADICTED
    bad_flag = wcon.execute(
        "SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1 "
        "AND NOT (claim_family='era' AND verdict='CONTRADICTED')").fetchone()[0]
    tot_flag = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    # landing-zone orphans (FK back to canon_corpus)
    orph_vl = wcon.execute("SELECT COUNT(*) FROM verify_ledger v WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=v.kit_id)").fetchone()[0]
    orph_km = wcon.execute("SELECT COUNT(*) FROM kit_mapping m WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=m.kit_id)").fetchone()[0]
    na_leak = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE claim_text LIKE 'N/A%'").fetchone()[0]
    abst_bad = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE abstained=1 AND payload_json IS NOT NULL").fetchone()[0]
    docket_map = wcon.execute(
        "SELECT COUNT(*) FROM kit_mapping WHERE terminal_state='MAPPED_DOCKET'").fetchone()[0]
    worm_v11 = wcon.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE kit_id='poe1-wormblaster' "
        "AND fact_provenance='verified-v1.1'").fetchone()[0]

    assert post_vl == pre_vl + 99, f"verify_ledger {post_vl} != {pre_vl}+99"
    assert post_kc == pre_kc + 72, f"kit_citations {post_kc} != {pre_kc}+72"
    assert post_kd == pre_kd + 132, f"kit_dossier {post_kd} != {pre_kd}+132"
    assert post_km == pre_km + 48 == 48, f"kit_mapping {post_km} != {pre_km}+48"
    assert post_corpus == pre_corpus == 585, f"canon_corpus changed {pre_corpus}->{post_corpus}"
    assert bad_flag == 0, f"{bad_flag} errata_applied rows are not era/CONTRADICTED"
    assert tot_flag == 8 + 4, f"errata_applied total {tot_flag} != 12 (8 prior + 4 this wave)"
    assert orph_vl == 0 and orph_km == 0, "landing-zone orphans"
    assert na_leak == 0, "N/A-filler leaked into ledger"
    assert abst_bad == 0, "abstained dossier row carries non-NULL payload"
    assert docket_map == 4, f"kit_mapping MAPPED_DOCKET rows {docket_map} != 4"
    assert worm_v11 == 0, f"wormblaster must stay legacy, has {worm_v11} verified-v1.1"
    assert jm == "delete", f"journal_mode {jm} != delete"
    assert ic == "ok", f"integrity_check {ic}"
    assert fk == [], f"foreign_key_check {fk}"
    # per-errata-kit: exactly 1 errata_applied row; VBV: 0 (backfill is not errata)
    for k in ERRATA_KITS:
        n = wcon.execute("SELECT COUNT(*) FROM verify_ledger WHERE kit_id=? AND errata_applied=1",
                         (k,)).fetchone()[0]
        assert n == 1, f"{k} errata_applied rows {n} != 1"
    vbv_flag = wcon.execute(
        "SELECT COUNT(*) FROM verify_ledger WHERE kit_id='poe1-vaal-blade-vortex' AND errata_applied=1"
    ).fetchone()[0]
    assert vbv_flag == 0, f"VBV backfill must NOT set errata_applied ({vbv_flag} rows flagged)"
    # eras values landed exactly
    for k, (_old, new) in {**ERRATA, **ERA_BACKFILL}.items():
        got = wcon.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()[0]
        assert got == new, f"{k} eras {got!r} != {new!r}"

    print("\n=== APPLIED ===")
    print(f"verify_ledger  {pre_vl} -> {post_vl}  (+{post_vl-pre_vl})")
    print(f"kit_citations  {pre_kc} -> {post_kc}  (+{post_kc-pre_kc})")
    print(f"kit_dossier    {pre_kd} -> {post_kd}  (+{post_kd-pre_kd})")
    print(f"kit_mapping    {pre_km} -> {post_km}  (+{post_km-pre_km})")
    print(f"verified-v1.1  {pre_v11} -> {post_v11}  (+{post_v11-pre_v11})")
    print("promotion rowcounts per kit:", log["promotions"])
    print("total probe-fact rows promoted:", prom_rows)
    print("errata_applied total (must be 12):", tot_flag)
    print("wormblaster verified-v1.1 facts (must be 0):", worm_v11)
    print("journal_mode:", jm, "| integrity_check:", ic, "| foreign_key_check:", fk)
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
