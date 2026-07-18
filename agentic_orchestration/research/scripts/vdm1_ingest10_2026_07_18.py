#!/usr/bin/env python3
"""
VDM-1 ingest-10 — basin-1 mapping rows (48) + REVIEW-3 un-quarantine + CONFIRMED-only promotions.

Single-writer: elrond. Substrate: agentic_orchestration/research/curated/corpus.db.
Charter: agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md.

Discipline (identical to ingests 1..9):
  - Backup taken by the CALLER (pre-vdm1-ingest10-<ts> + md5 sidecar) BEFORE this runs.
  - journal_mode = DELETE preserved (asserted, never changed).
  - index.lock retry wrapper: wait 30s, retry up to 3x, on the connect.
  - Single transaction; guarded writes assert rowcount; idempotent mapping UPSERT.
  - No-silent-transformation; concurrent readonly crawlers (basin-2) unaffected.
  - integrity_check + foreign_key_check at end.

THREE WORK ITEMS:
  1. Ingest 48 basin-1 kit_mapping rows (POST-AUDIT files; UPSERT idempotent).
  2. REVIEW-3 un-quarantine flip: kit_citations id=369 (mobalytics/jungroan,
     temporalis-blink, authored-class) quarantined 1->0. Do NOT touch id=375
     (walking-calamity mmoexp — genuine junk-tail, KEEPS quarantined=1).
  3. Basin-1 probe-fact promotions, CONFIRMED-ONLY (steward ruling at basin close-out).
     Whole-kit block flip fact_provenance -> 'verified-v1.1' ONLY for kits that are
     mechanics=CONFIRMED-with-anchor AND have ZERO CONTRADICTED verdict in ANY family.
     This automatically excludes all 9 contradicted kits (4 era-contra + 5 idmech-contra),
     honoring BOTH dispatch exclusion rules (era-family excluded for era-contradicted;
     identity/mechanics excluded for ERRATA-19..23 carriers). See NARROWER-THING note below.
"""
import json
import os
import sqlite3
import sys
import time
from datetime import date

DB = "agentic_orchestration/research/curated/corpus.db"
MAP_DIR = "agentic_orchestration/research/vdm1/stage2/basin1/"
TODAY = date.today().isoformat()

MAP_FILES = [f"mapping-batch-0{i}.jsonl" for i in (1, 2, 3, 4)]

REVIEW3_CITATION_ID = 369          # mobalytics/jungroan temporalis-blink (authored) -> flip 1->0
REVIEW3_URL_SUBSTR = "blink-autobomber-jungroan"
KEEP_QUARANTINED_ID = 375          # walking-calamity mmoexp -> MUST stay quarantined=1

# --- NARROWER-THING promotion design (dispatch item 3) ---------------------------------
# canon_probe_facts has 10 CONTENT families (delivery/footprint/element/control/defense/
# economy/movement/geo_text/rank1_upgrade/sources_used). verify_ledger has 4 VERIFICATION
# claim-families (identity/mechanics/era/negative_canon). Probe families cannot be
# partitioned into era-vs-identity-vs-mechanics buckets, so a PARTIAL promotion of *some*
# probe families for a contradicted kit cannot be expressed cleanly WITHOUT laundering kb
# rows into verified-looking state (the m04 concern). Per the dispatch ("if your promotion
# machinery cannot express a partial promotion cleanly, do the narrower thing"), we promote
# the whole 10-fact block ONLY for kits with zero CONTRADICTED in ANY family AND
# mechanics=CONFIRMED-with-anchor (the PoE1 ingest-4 gate). Every contradicted kit is
# excluded whole, which strictly honors both named exclusion rules and excludes nothing more
# than the gate requires.


def load_mapping(fn):
    rows = []
    with open(MAP_DIR + fn) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception as e:
                sys.exit(f"PARSE FAIL {fn}:{i}: {e}")
            for req in ("kit_id", "mapping_json", "grade", "deviation_notes", "terminal_state"):
                if req not in o:
                    sys.exit(f"MISSING FIELD {req} in {fn}:{i}")
            if not isinstance(o["mapping_json"], dict):
                sys.exit(f"mapping_json not object {fn}:{i}")
            rows.append(o)
    return rows


def connect_with_lock_retry():
    lock = ".git/index.lock"  # informational; the DB lock is what matters, retry on OperationalError
    last = None
    for attempt in range(1, 4 + 1):  # initial + 3 retries
        try:
            con = sqlite3.connect(DB, timeout=30.0)
            con.execute("PRAGMA foreign_keys = ON")
            return con
        except sqlite3.OperationalError as e:
            last = e
            if attempt <= 3:
                print(f"[lock-retry] attempt {attempt} failed ({e}); waiting 30s", flush=True)
                time.sleep(30)
    raise last


def main():
    con = connect_with_lock_retry()
    jm = con.execute("PRAGMA journal_mode").fetchone()[0]
    if jm.lower() != "delete":
        sys.exit(f"ABORT: journal_mode is {jm!r}, expected 'delete'")
    cur = con.cursor()

    # ---- gather all mapping rows, validate against schema enums + FK + in-file dupes ----
    all_rows = []
    for fn in MAP_FILES:
        all_rows.extend(load_mapping(fn))
    if len(all_rows) != 48:
        sys.exit(f"ABORT: expected 48 mapping rows, got {len(all_rows)}")
    ids = [r["kit_id"] for r in all_rows]
    if len(set(ids)) != 48:
        from collections import Counter
        dups = [k for k, n in Counter(ids).items() if n > 1]
        sys.exit(f"ABORT: in-file duplicate kit_ids: {dups}")
    # FK: every kit_id in canon_corpus
    have = set(r[0] for r in cur.execute("SELECT kit_id FROM canon_corpus").fetchall())
    missing = [k for k in ids if k not in have]
    if missing:
        sys.exit(f"ABORT: kit_ids missing from canon_corpus (FK would fail): {missing}")
    # grade histogram (dispatch expected 0 EXACT / 34 CLOSE / 14 APPROX / 0 GAPPED)
    from collections import Counter
    ghist = Counter(r["grade"] for r in all_rows)
    thist = Counter(r["terminal_state"] for r in all_rows)
    if dict(ghist) != {"CLOSE": 34, "APPROX": 14}:
        sys.exit(f"ABORT: grade histogram {dict(ghist)} != expected CLOSE34/APPROX14")
    if dict(thist) != {"MAPPED": 48}:
        sys.exit(f"ABORT: terminal histogram {dict(thist)} != expected MAPPED48")

    # pre-existing kit_mapping rows for these kits (insert vs replace bookkeeping)
    qm = ",".join("?" * len(ids))
    preexist = set(
        r[0] for r in cur.execute(
            f"SELECT kit_id FROM kit_mapping WHERE kit_id IN ({qm})", ids
        ).fetchall()
    )
    n_replace = len(preexist)
    n_insert = 48 - n_replace

    km_before = cur.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]

    # ---- REVIEW-3 preconditions (read BEFORE write) ----
    r3 = cur.execute(
        "SELECT id, kit_id, url, cite_class, quarantined FROM kit_citations WHERE id=?",
        (REVIEW3_CITATION_ID,),
    ).fetchone()
    if r3 is None:
        sys.exit(f"ABORT: REVIEW-3 citation id={REVIEW3_CITATION_ID} not found")
    if r3[1] != "poe2-temporalis-blink" or REVIEW3_URL_SUBSTR not in r3[2] or r3[4] != 1:
        sys.exit(f"ABORT: REVIEW-3 precondition mismatch: {r3}")
    keeprow = cur.execute(
        "SELECT id, kit_id, url, quarantined FROM kit_citations WHERE id=?",
        (KEEP_QUARANTINED_ID,),
    ).fetchone()
    if keeprow is None or "mmoexp" not in keeprow[2] or keeprow[3] != 1:
        sys.exit(f"ABORT: walking-calamity mmoexp keep-row precondition mismatch: {keeprow}")

    # ---- PROMOTION gate computation (read-only pass) ----
    from collections import defaultdict
    basin1 = ids  # the 48 basin-1 kits
    agg = defaultdict(lambda: defaultdict(lambda: {"C": 0, "X": 0, "Ca": 0}))
    for kit, fam, verdict, anchor in cur.execute(
        f"SELECT kit_id, claim_family, verdict, anchor_quote FROM verify_ledger "
        f"WHERE kit_id IN ({qm})", basin1
    ):
        if verdict == "CONFIRMED":
            agg[kit][fam]["C"] += 1
            if anchor and anchor.strip():
                agg[kit][fam]["Ca"] += 1
        elif verdict == "CONTRADICTED":
            agg[kit][fam]["X"] += 1
    pf_kits = set(
        r[0] for r in cur.execute(
            f"SELECT DISTINCT kit_id FROM canon_probe_facts WHERE kit_id IN ({qm})", basin1
        ).fetchall()
    )
    promote_kits = []
    excl_contra = []
    excl_no_mech = []
    zero_pf_clean = []
    for k in basin1:
        a = agg[k]
        any_contra = any(a[f]["X"] > 0 for f in a)
        mech_conf_anchored = a["mechanics"]["Ca"] > 0
        if any_contra:
            excl_contra.append(k)
            continue
        if not mech_conf_anchored:
            excl_no_mech.append(k)
            continue
        if k in pf_kits:
            promote_kits.append(k)
        else:
            zero_pf_clean.append(k)

    # guard: no promote kit is contradicted; every promote kit has a mechanics-CONFIRMED anchor
    for k in promote_kits:
        if any(agg[k][f]["X"] > 0 for f in agg[k]):
            raise RuntimeError(f"promote-set guard: {k} carries a CONTRADICTION")
        if agg[k]["mechanics"]["Ca"] == 0:
            raise RuntimeError(f"promote-set guard: {k} lacks mechanics-CONFIRMED anchor")
    # guard: named exclusion sets are actually excluded
    NAMED_ERA_CONTRA = {"poe2-acolyte-darkness", "poe2-concoction", "poe2-grim-feast",
                        "poe2-warbringer-totems"}
    NAMED_ERRATA_19_23 = {"poe2-walking-calamity", "tq2-whirlwind-rogue", "tq2-elementalist",
                          "tq2-stormblade-ice-shards"}
    for k in (NAMED_ERA_CONTRA | NAMED_ERRATA_19_23):
        if k in promote_kits:
            raise RuntimeError(f"EXCLUSION VIOLATION: named-excluded kit {k} is in promote-set")

    verif_before = con.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'"
    ).fetchone()[0]

    # =================== WRITE (single transaction) ===================
    try:
        cur.execute("BEGIN IMMEDIATE")

        # -- ITEM 1: kit_mapping UPSERT (idempotent; post-audit file state wins) --
        ins_map = 0
        for r in all_rows:
            mj = json.dumps(r["mapping_json"], ensure_ascii=False)
            cur.execute(
                """INSERT INTO kit_mapping
                     (kit_id, mapping_json, grade, deviation_notes, terminal_state,
                      mapping_provenance, authored_date)
                   VALUES (?,?,?,?,?, 'authored-vdm1', ?)
                   ON CONFLICT(kit_id) DO UPDATE SET
                     mapping_json=excluded.mapping_json,
                     grade=excluded.grade,
                     deviation_notes=excluded.deviation_notes,
                     terminal_state=excluded.terminal_state,
                     mapping_provenance='authored-vdm1',
                     authored_date=excluded.authored_date""",
                (r["kit_id"], mj, r["grade"], r["deviation_notes"], r["terminal_state"], TODAY),
            )
            ins_map += 1
        if ins_map != 48:
            raise RuntimeError(f"kit_mapping upsert count {ins_map} != 48")

        # -- ITEM 2: REVIEW-3 un-quarantine flip (id=369 only) --
        cur.execute(
            "UPDATE kit_citations SET quarantined=0 WHERE id=? AND quarantined=1",
            (REVIEW3_CITATION_ID,),
        )
        if cur.rowcount != 1:
            raise RuntimeError(f"REVIEW-3 flip rowcount={cur.rowcount}, expected 1")

        # -- ITEM 3: CONFIRMED-only promotions (whole-kit block, 32 kits x 10 = 320) --
        promoted_rows = 0
        for k in promote_kits:
            cur.execute(
                "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                "WHERE kit_id=? AND fact_provenance IN ('kb-legacy','named-source-unfetched')",
                (k,),
            )
            promoted_rows += cur.rowcount

        con.commit()
    except Exception:
        con.rollback()
        raise

    # =================== VERIFY (post-write) ===================
    integ = con.execute("PRAGMA integrity_check").fetchone()[0]
    fkc = con.execute("PRAGMA foreign_key_check").fetchall()
    jm2 = con.execute("PRAGMA journal_mode").fetchone()[0]

    km_after = con.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    g_after = dict(Counter(
        r[0] for r in con.execute(
            f"SELECT grade FROM kit_mapping WHERE kit_id IN ({qm})", ids
        ).fetchall()
    ))
    t_after = dict(Counter(
        r[0] for r in con.execute(
            f"SELECT terminal_state FROM kit_mapping WHERE kit_id IN ({qm})", ids
        ).fetchall()
    ))
    r3_after = con.execute(
        "SELECT quarantined FROM kit_citations WHERE id=?", (REVIEW3_CITATION_ID,)
    ).fetchone()[0]
    keep_after = con.execute(
        "SELECT quarantined FROM kit_citations WHERE id=?", (KEEP_QUARANTINED_ID,)
    ).fetchone()[0]
    verif_after = con.execute(
        "SELECT COUNT(*) FROM canon_probe_facts WHERE fact_provenance='verified-v1.1'"
    ).fetchone()[0]

    tot_v = con.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    tot_c = con.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    tot_d = con.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    tot_m = con.execute("SELECT COUNT(*) FROM kit_mapping").fetchone()[0]
    quar = con.execute("SELECT COUNT(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]
    prov = dict(con.execute(
        "SELECT fact_provenance, COUNT(*) FROM canon_probe_facts GROUP BY fact_provenance"
    ).fetchall())
    con.close()

    print("=== INGEST-10 COMPLETE ===")
    print(f"[item1] kit_mapping: {n_insert} inserted, {n_replace} replaced (UPSERT); "
          f"count {km_before} -> {km_after}")
    print(f"        grade(basin1)={g_after}  terminal(basin1)={t_after}")
    print(f"[item2] REVIEW-3 citation id={REVIEW3_CITATION_ID} quarantined 1->{r3_after} "
          f"(flip OK); walking-calamity mmoexp id={KEEP_QUARANTINED_ID} quarantined={keep_after} (KEPT)")
    print(f"[item3] promotions: {len(promote_kits)} kits x 10 = {promoted_rows} facts flipped "
          f"-> verified-v1.1")
    print(f"        EXCLUDED contra ({len(excl_contra)}): {sorted(excl_contra)}")
    print(f"        EXCLUDED mechanics-not-CONFIRMED ({len(excl_no_mech)}): {sorted(excl_no_mech)}")
    print(f"        clean+mechConf but zero-probe ({len(zero_pf_clean)}): {sorted(zero_pf_clean)}")
    print(f"        verified-v1.1: {verif_before} -> {verif_after} (Δ+{verif_after - verif_before})")
    print(f"TOTALS  verify_ledger={tot_v} kit_citations={tot_c} kit_dossier={tot_d} "
          f"kit_mapping={tot_m} quarantined={quar}")
    print(f"        provenance={prov}")
    print(f"integrity_check={integ}  foreign_key_check={'clean' if not fkc else fkc}  "
          f"journal_mode={jm2}")


if __name__ == "__main__":
    main()
