#!/usr/bin/env python3
"""
VDM-1 INGEST-13 — basin-3 (Diablo d2/d3/d4/di, 179 kits) crawl ingest
+ BACKFILL-3 overlay + ERRATA-43+ queue + whole-kit promotion gate.

Single-writer: elrond. DB: corpus.db (journal_mode DELETE).
Run steward: gandalf; fires under Matt's standing autonomous-run mandate.

FILES GOVERN. All expected counts asserted EXACTLY pre-write; a mismatch RAISES
(stop and report, never reconcile silently).

PART 1 — batch ingest: 680 verify_ledger + 346 kit_citations + 1074 kit_dossier (15 batches).
PART 2 — BACKFILL-3 overlay (supersede rule):
  - 22 UPDATE in-place (21 U->C + 1 U->X); item 17 exception (NO verify write; era extension only)
  - 1 INSERT new row (item 26 di-cyclone-strike-monk-base mechanics CONFIRMED)
  - 27 citations with OR-IGNORE on UNIQUE(kit_id,url) collisions
  - POST-STATE: 681 effective verify = 576C/85U/19X/1SNF; total verify_ledger = 1512
PART 3 — errata queue (ERRATA-43..):
  3a. FALSIFIED-NEGATIVE annotations x5 (no negative flip)
  3b. di resource WRONG-RESOURCE sweep (annotate all 23 di economy probes; no replacements except documented)
  3c. d4 Paladin/Warlock resource CONTESTED (annotate wing-strike-arbiter probe; variance note)
  3d. Probe-fabrication series (13 items — consolidated renumber; value corrections + annotations)
  3e. Era errata (restamps, extensions, annotations)
  3f. core_skills errata (fishyzon, rathma-aotd, blazing-abyss, shadowblight, frenzy-h90)
  3g. Alias/lineage errata (god-hungering alias remove, frenzy-barb Sprint alias, di-tempest)
  3h. Kit-level flag annotations (4 kits)
  3i. NULL-era backfills (7 kits; guarded on NULL only)
  3j. Unattested register annotations (grim-ward partial, tainted-summoner folk-name)
PART 4 — whole-kit promotion gate (ingest-11 pattern; di resource fields excluded per 3b).
"""
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research")
DB = ROOT / "curated" / "corpus.db"
BASIN3 = ROOT / "vdm1" / "stage1" / "basin3"
TODAY = date.today().isoformat()
ANNOT_TAG = "[VDM-1 basin-3 2026-07-18 ingest-13]"

# ---- PRE-LOAD assertion table (steward file-recount, EXACT) ----
EXP_VERIFY = {  # batch -> (C, X, U, SNF)
    "01": (47, 0, 1, 0), "02": (46, 1, 0, 0), "03": (44, 0, 10, 0),
    "04": (44, 0, 7, 0),  "05": (39, 0, 7, 1),  "06": (43, 1, 3, 0),
    "07": (49, 1, 0, 0),  "08": (39, 4, 10, 0), "09": (40, 2, 0, 0),
    "10": (26, 1, 15, 0), "11": (39, 0, 5, 0),  "12": (31, 4, 16, 0),
    "13": (28, 1, 7, 0),  "14": (20, 1, 13, 0), "15": (19, 2, 13, 0),
}
EXP_VERIFY_TOTAL = (554, 18, 107, 1)  # 680 rows
EXP_CITATIONS = {
    "01": 26, "02": 22, "03": 23, "04": 27, "05": 29, "06": 16, "07": 16,
    "08": 29, "09": 22, "10": 20, "11": 29, "12": 22, "13": 25, "14": 21, "15": 19,
}  # 346 total
EXP_CIT_QUAR_TOTAL = 4  # b01 rpgstash ×1 + b10 mywowgold/epiccarry ×2 + b11 wowcarry ×1
EXP_DOSSIER = {
    "01": 72, "02": 72, "03": 72, "04": 72, "05": 72, "06": 72, "07": 72,
    "08": 72, "09": 72, "10": 72, "11": 72, "12": 72, "13": 72, "14": 72, "15": 66,
}  # 1074 total
EXP_DOSSIER_ABST = {
    "01": 4,  "02": 4,  "03": 21, "04": 27, "05": 18, "06": 3,  "07": 0,
    "08": 3,  "09": 5,  "10": 7,  "11": 2,  "12": 10, "13": 19, "14": 42, "15": 25,
}  # 190 total abstained
EXP_KIT_COUNT = 179
EXP_BACKFILL_VERIFY = 31   # 23C/7U/1X
EXP_BACKFILL_CIT = 27
BASELINE_VL = 831
BASELINE_KC = 584
BASELINE_KD = 1320

# Backfill supersede targets: kit_id -> list of (claim_family, direction)
# 22 in-place UPDATEs (21 U->C + 1 U->X); item 17 is ERA-EXTENSION-ONLY (no verify write)
# 7 retry-exhausted U rows NOT ingested
SUPERSEDE_ITEMS = {
    1:  ("d2-golemancer",        "era",          "U->C"),
    2:  ("d2-grim-ward-barb",    "era",          "U->C"),   # only era row; identity+negative U = retry-exhausted
    3:  ("d2-impale-zon",        "era",          "U->C"),
    4:  ("d2-inferno-sorc",      "era",          "U->C"),
    6:  ("d2-firewall-sorc",     "era",          "U->C"),
    7:  ("d2-fishyzon",          "era",          "U->C"),
    8:  ("d2-sacrifice",         "era",          "U->C"),
    9:  ("d4-heartseeker",       "era",          "U->C"),
    10: ("d4-lightning-spear",   "mechanics",    "U->X"),  # backfill item 10; era X already in batch
    11: ("d4-mighty-throw",      "era",          "U->C"),
    14: ("d4-twisting-blades",   "era",          "U->C"),
    15: ("d4-ww-dust-devils",    "era",          "U->C"),
    16: ("d4-shadowblight",      "era",          "U->C"),
    18: ("d4-ball-lightning",    "era",          "U->C"),
    19: ("d4-blood-lance",       "era",          "U->C"),
    20: ("d4-blood-surge",       "era",          "U->C"),
    21: ("d4-bone-spear",        "era",          "U->C"),
    24: ("di-ray-of-frost-wizard", "era",        "U->C"),
    # item 12: TWO rows (identity + era) — handled explicitly
    # item 23: TWO rows (identity + era) — handled explicitly
}
# Multi-row supersede items handled explicitly below (items 12, 23)
SUPERSEDE_ITEM_12 = [
    ("d4-andariel-flurry", "identity", "U->C"),
    ("d4-andariel-flurry", "era",      "U->C"),
]
SUPERSEDE_ITEM_23 = [
    ("di-cyclone-monk-pvp", "identity", "U->C"),
    ("di-cyclone-monk-pvp", "era",      "U->C"),
]
# item 17 exception: NO verify write; era extension only (handled in 3e)
# item 26: NEW INSERT (di-cyclone-strike-monk-base mechanics CONFIRMED)
# Retry-exhausted U rows (NOT ingested; verification register):
RETRY_EXHAUSTED = [
    ("d2-grim-ward-barb", "identity"),    # item 2 identity
    ("d2-grim-ward-barb", "negative_canon"),  # item 2 negative_canon
    ("d2-leap-attack-barb", "era"),       # item 5
    ("d4-lightning-spear", "identity"),   # item 10 identity
    ("d4-blood-wave", "era"),             # item 13
    ("di-corpse-explosion-necro", "era"), # item 22
    ("di-resonance-awakening", "era"),    # item 25
]

VERDICT_MAP = {
    "CONFIRMED": "CONFIRMED", "CONTRADICTED": "CONTRADICTED",
    "UNSUPPORTED": "UNSUPPORTED",
    "SOURCE-NOT-FOUND": "SOURCE_NOT_FOUND", "SOURCE_NOT_FOUND": "SOURCE_NOT_FOUND",
}


def die(msg):
    print(f"\n*** STOP: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load(fn):
    rows = []
    with open(BASIN3 / fn) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                die(f"PARSE FAIL {fn}:{i}: {e}")
    return rows


def guarded(cur, sql, params, ctx, expect=1):
    cur.execute(sql, params)
    if cur.rowcount != expect:
        raise RuntimeError(f"GUARD FAIL ({ctx}): rowcount={cur.rowcount}, expected {expect}")


def prepend_annot(cur, kid, clause, ctx):
    """Prepend ANNOT_TAG clause to mech_note, preserving original."""
    old = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
    if old is None:
        raise RuntimeError(f"prepend_annot: {kid} not in canon_corpus")
    old_mn = old[0]
    new_mn = f"{ANNOT_TAG} {clause} [original mech_note follows] {old_mn or ''}"
    guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note IS ?",
            (new_mn, kid, old_mn), ctx)


def main():
    # =================== PRE-LOAD validation (before any write) ===================
    batches = [f"{n:02d}" for n in range(1, 16)]
    verify_by_batch = {b: load(f"batch-{b}-verify.jsonl") for b in batches}
    cit_by_batch    = {b: load(f"batch-{b}-citations.jsonl") for b in batches}
    dos_by_batch    = {b: load(f"batch-{b}-dossier.jsonl") for b in batches}
    backfill_verify  = load("backfill-3-verify.jsonl")
    backfill_cit     = load("backfill-3-citations.jsonl")

    # verify row counts + verdict histograms
    tot_v = [0, 0, 0, 0]  # C, X, U, SNF
    for b in batches:
        c = x = u = snf = 0
        for r in verify_by_batch[b]:
            v = VERDICT_MAP.get(r["verdict"])
            if v is None:
                die(f"bad verdict {r['verdict']!r} ({r['kit_id']}) b{b}")
            if v == "CONFIRMED":       c += 1
            elif v == "CONTRADICTED":  x += 1
            elif v == "UNSUPPORTED":   u += 1
            else:                      snf += 1
        if (c, x, u, snf) != EXP_VERIFY[b]:
            die(f"VERIFY COUNT MISMATCH b{b}: got {(c,x,u,snf)}, expected {EXP_VERIFY[b]}")
        tot_v[0] += c; tot_v[1] += x; tot_v[2] += u; tot_v[3] += snf
    if tuple(tot_v) != EXP_VERIFY_TOTAL:
        die(f"VERIFY TOTAL MISMATCH: {tuple(tot_v)} != {EXP_VERIFY_TOTAL}")

    # citations counts + quarantine
    cit_quar = 0
    cit_total = 0
    for b in batches:
        if len(cit_by_batch[b]) != EXP_CITATIONS[b]:
            die(f"CITATIONS COUNT MISMATCH b{b}: {len(cit_by_batch[b])} != {EXP_CITATIONS[b]}")
        cit_total += len(cit_by_batch[b])
        cit_quar += sum(int(r.get("quarantined", 0)) for r in cit_by_batch[b])
    if cit_quar != EXP_CIT_QUAR_TOTAL:
        die(f"CITATIONS QUAR MISMATCH: {cit_quar} != {EXP_CIT_QUAR_TOTAL}")

    # dossier counts + abstained
    dos_abst_tot = 0
    dos_total = 0
    for b in batches:
        if len(dos_by_batch[b]) != EXP_DOSSIER[b]:
            die(f"DOSSIER COUNT MISMATCH b{b}: {len(dos_by_batch[b])} != {EXP_DOSSIER[b]}")
        ab = sum(int(r.get("abstained", 0)) for r in dos_by_batch[b])
        if ab != EXP_DOSSIER_ABST[b]:
            die(f"DOSSIER ABST MISMATCH b{b}: {ab} != {EXP_DOSSIER_ABST[b]}")
        dos_abst_tot += ab
        dos_total += len(dos_by_batch[b])
    if dos_abst_tot != 190:
        die(f"DOSSIER ABST TOTAL: {dos_abst_tot} != 190")

    # abstain-null law (in-file): all abstained dossier rows must have null-equivalent payload
    for b in batches:
        for r in dos_by_batch[b]:
            if int(r.get("abstained", 0)) == 1 and r.get("payload_json") is not None:
                die(f"abstained w/ non-null payload: {r['kit_id']}/{r['family']} b{b}")

    # kit count + verify==dossier set
    all_kits = sorted({r["kit_id"] for b in batches for r in verify_by_batch[b]})
    dos_kits = sorted({r["kit_id"] for b in batches for r in dos_by_batch[b]})
    if len(all_kits) != EXP_KIT_COUNT:
        die(f"distinct kit count {len(all_kits)} != {EXP_KIT_COUNT}")
    if all_kits != dos_kits:
        diff = set(all_kits).symmetric_difference(set(dos_kits))
        die(f"verify kit set != dossier kit set: {sorted(diff)}")

    # backfill counts
    if len(backfill_verify) != EXP_BACKFILL_VERIFY:
        die(f"backfill verify {len(backfill_verify)} != {EXP_BACKFILL_VERIFY}")
    if len(backfill_cit) != EXP_BACKFILL_CIT:
        die(f"backfill citations {len(backfill_cit)} != {EXP_BACKFILL_CIT}")

    print(f"PRE-LOAD OK: verify {tuple(tot_v)}=680 rows, 15 batches; "
          f"citations {cit_total} (quar {cit_quar}); dossier {dos_total} (abst {dos_abst_tot}); "
          f"{len(all_kits)} kits; backfill-verify {len(backfill_verify)}, backfill-cit {len(backfill_cit)}.")

    # =================== OPEN DB + baseline checks ===================
    conn = sqlite3.connect(str(DB))
    conn.isolation_level = None  # explicit txn control
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    jm = cur.execute("PRAGMA journal_mode;").fetchone()[0]
    if jm.lower() != "delete":
        die(f"journal_mode is {jm}, expected delete (never flip to WAL)")

    vl0  = cur.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    kc0  = cur.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    kd0  = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    if vl0 != BASELINE_VL:
        die(f"verify_ledger baseline {vl0} != {BASELINE_VL}")
    if kc0 != BASELINE_KC:
        die(f"kit_citations baseline {kc0} != {BASELINE_KC}")
    if kd0 != BASELINE_KD:
        die(f"kit_dossier baseline {kd0} != {BASELINE_KD}")

    # FK guard: all 179 kit_ids must pre-exist in canon_corpus
    qk = ",".join("?" * len(all_kits))
    present = {r[0] for r in cur.execute(f"SELECT kit_id FROM canon_corpus WHERE kit_id IN ({qk})", all_kits)}
    missing = set(all_kits) - present
    if missing:
        die(f"FK GUARD: {len(missing)} basin-3 kits missing from canon_corpus: {sorted(missing)}")

    # Idempotency guard: no pre-existing landing-zone rows for basin-3 kits
    for tbl in ("verify_ledger", "kit_citations", "kit_dossier"):
        n = cur.execute(f"SELECT COUNT(*) FROM {tbl} WHERE kit_id IN ({qk})", all_kits).fetchone()[0]
        if n != 0:
            die(f"IDEMPOTENCY: {tbl} already has {n} rows for basin-3 kits — do not re-run")

    # Pre-verify the item-26 insert target: di-cyclone-strike-monk-base mechanics must NOT already exist
    csm_mech = cur.execute(
        "SELECT COUNT(*) FROM verify_ledger WHERE kit_id='di-cyclone-strike-monk-base' AND claim_family='mechanics'"
    ).fetchone()[0]
    if csm_mech != 0:
        die("item-26 INSERT precondition: di-cyclone-strike-monk-base mechanics row already exists in verify_ledger")

    print(f"BASELINE OK: vl={vl0}, kc={kc0}, kd={kd0}, FK clean, idempotency clean.")

    # =================== WRITE (single transaction) ===================
    cur.execute("BEGIN")
    try:
        ins_v = ins_c = ins_d = 0

        # ================= PART 1: batch ingest =================
        for b in batches:
            for r in verify_by_batch[b]:
                verdict = VERDICT_MAP[r["verdict"]]
                if verdict in ("CONFIRMED", "CONTRADICTED") and not r.get("anchor_quote"):
                    raise RuntimeError(f"missing anchor: {r['kit_id']}/{r['claim_family']} b{b}")
                cur.execute(
                    """INSERT INTO verify_ledger
                       (kit_id, claim_family, claim_text, verdict, anchor_quote,
                        source_url, errata_applied, run_tag, verified_date)
                       VALUES (?,?,?,?,?,?,0,'vdm1',?)""",
                    (r["kit_id"], r["claim_family"], r.get("claim_text"), verdict,
                     r.get("anchor_quote"), r.get("source_url"), TODAY),
                )
                ins_v += 1

            for r in cit_by_batch[b]:
                cur.execute(
                    """INSERT INTO kit_citations
                       (kit_id, url, archive_url, site, author_handle, title,
                        cite_class, rank_class, accessed_date, quarantined)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (r["kit_id"], r["url"], r.get("archive_url"), r.get("site"),
                     r.get("author_handle"), r.get("title"), r.get("cite_class"),
                     r.get("rank_class"), r.get("accessed_date"), int(r.get("quarantined", 0))),
                )
                ins_c += 1

            for r in dos_by_batch[b]:
                abst = int(r.get("abstained", 0))
                payload = r.get("payload_json")
                payload_s = None if payload is None else json.dumps(payload, ensure_ascii=False)
                cur.execute(
                    """INSERT INTO kit_dossier
                       (kit_id, family, payload_json, source_url, anchor_quote,
                        abstained, conf, extraction_provenance, created_date)
                       VALUES (?,?,?,?,?,?,?,'fetched-vdm1',?)""",
                    (r["kit_id"], r["family"], payload_s, r.get("source_url"),
                     r.get("anchor_quote"), abst, r.get("conf"), TODAY),
                )
                ins_d += 1

        print(f"P1 done: verify +{ins_v}, citations +{ins_c}, dossier +{ins_d}")

        # ================= PART 2: BACKFILL-3 overlay =================
        # Build lookup of backfill verify rows by item number
        bf_by_item = defaultdict(list)
        for r in backfill_verify:
            bf_by_item[r["backfill_item"]].append(r)

        supersede_updated = 0
        supersede_inserted = 0

        # ---- 22 in-place UPDATEs (21 U->C/X + 1 already-C anchor upgrades for items 1,6,7 are
        #      counted in dispatch "22 rows updated"; item 11 is a new INSERT for voh-s6+) ----
        # EDGE CASES:
        # Items 1, 6, 7: batch already CONFIRMED — UPDATE anchor_quote/source_url only (no verdict change)
        # Item 11: batch era CONTRADICTED for s7-s12; backfill confirms voh-s6+ (different claim) — INSERT new row
        # Items 20, 21: TWO U rows each — supersede ONLY the one matching backfill claim_text (launch-s1-3)
        # Items 3, 4: ONE U row (classic era) + ONE C row (lod era) — supersede the U row only

        def supersede_update(cur, kid, fam, bf, match_verdict="UNSUPPORTED", match_claim_text=None):
            """Find and UPDATE a verify row. match_claim_text narrows when multiple rows exist."""
            if match_claim_text:
                rows = cur.execute(
                    "SELECT id FROM verify_ledger WHERE kit_id=? AND claim_family=? AND verdict=? "
                    "AND claim_text=?",
                    (kid, fam, match_verdict, match_claim_text)
                ).fetchall()
            else:
                rows = cur.execute(
                    "SELECT id FROM verify_ledger WHERE kit_id=? AND claim_family=? AND verdict=?",
                    (kid, fam, match_verdict)
                ).fetchall()
            if len(rows) != 1:
                raise RuntimeError(f"supersede_update {kid}/{fam}: expected 1 {match_verdict} row "
                                   f"(claim_text={match_claim_text!r}), found {len(rows)}")
            new_verdict = VERDICT_MAP[bf["verdict"]]
            cur.execute(
                """UPDATE verify_ledger SET verdict=?, anchor_quote=?, source_url=?,
                   claim_text=COALESCE(?,claim_text)
                   WHERE id=?""",
                (new_verdict, bf.get("anchor_quote"), bf.get("source_url"),
                 bf.get("claim_text"), rows[0][0]),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"supersede_update {kid}/{fam} UPDATE returned {cur.rowcount}")

        # Items 1, 6, 7: batch already CONFIRMED — anchor upgrade only (UPDATE existing C row)
        for item_num in [1, 6, 7]:
            item_rows = bf_by_item[item_num]
            if not item_rows:
                raise RuntimeError(f"backfill item {item_num}: no rows found")
            bf = item_rows[0]
            kid, fam = bf["kit_id"], bf["claim_family"]
            # UPDATE the existing CONFIRMED row with better Wayback anchor
            rows_in_db = cur.execute(
                "SELECT id FROM verify_ledger WHERE kit_id=? AND claim_family=? AND verdict='CONFIRMED'",
                (kid, fam)
            ).fetchall()
            if len(rows_in_db) < 1:
                raise RuntimeError(f"backfill item {item_num} anchor-upgrade: no CONFIRMED row for {kid}/{fam}")
            # Update the first (and typically only) CONFIRMED row
            cur.execute(
                """UPDATE verify_ledger SET anchor_quote=?, source_url=?
                   WHERE id=?""",
                (bf.get("anchor_quote"), bf.get("source_url"), rows_in_db[0][0]),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"backfill item {item_num} anchor-upgrade UPDATE returned {cur.rowcount}")
            supersede_updated += 1

        # Standard single-row U->C items (simple lookup, no claim_text matching needed)
        simple_items = {
            2:  ("d2-grim-ward-barb",    "era"),
            8:  ("d2-sacrifice",          "era"),
            9:  ("d4-heartseeker",        "era"),
            10: ("d4-lightning-spear",    "mechanics"),  # U->X
            14: ("d4-twisting-blades",    "era"),
            15: ("d4-ww-dust-devils",     "era"),
            16: ("d4-shadowblight",       "era"),
            18: ("d4-ball-lightning",     "era"),
            19: ("d4-blood-lance",        "era"),
            24: ("di-ray-of-frost-wizard","era"),
        }
        for item_num, (kid, fam) in simple_items.items():
            bf_rows = [r for r in bf_by_item[item_num] if r["claim_family"] == fam]
            if len(bf_rows) != 1:
                raise RuntimeError(f"backfill item {item_num} expected 1 row for {kid}/{fam}, got {len(bf_rows)}")
            supersede_update(cur, kid, fam, bf_rows[0])
            supersede_updated += 1

        # Items 3, 4: have ONE U row (classic era) + ONE C row (lod era); supersede U only
        for item_num, kid in [(3, "d2-impale-zon"), (4, "d2-inferno-sorc")]:
            bf_rows = [r for r in bf_by_item[item_num] if r["claim_family"] == "era"]
            if len(bf_rows) != 1:
                raise RuntimeError(f"backfill item {item_num} expected 1 era row, got {len(bf_rows)}")
            # Use claim_text matching to find the UNSUPPORTED classic-era row
            bf_ct = bf_rows[0].get("claim_text")
            rows_u = cur.execute(
                "SELECT id FROM verify_ledger WHERE kit_id=? AND claim_family='era' AND verdict='UNSUPPORTED'",
                (kid,)
            ).fetchall()
            if len(rows_u) != 1:
                raise RuntimeError(f"backfill item {item_num}: expected 1 UNSUPPORTED era row for {kid}, found {len(rows_u)}")
            cur.execute(
                """UPDATE verify_ledger SET verdict=?, anchor_quote=?, source_url=?,
                   claim_text=COALESCE(?,claim_text)
                   WHERE id=?""",
                (VERDICT_MAP[bf_rows[0]["verdict"]], bf_rows[0].get("anchor_quote"),
                 bf_rows[0].get("source_url"), bf_ct, rows_u[0][0]),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"backfill item {item_num} UPDATE returned {cur.rowcount}")
            supersede_updated += 1

        # Item 11: batch has CONTRADICTED era (s7-s12); backfill confirms voh-s6+ (different claim)
        # Strategy: UPDATE the CONTRADICTED s7-s12 era row to CONFIRMED voh-s6+ (supersede the X with the C)
        # This is consistent with "find single matching batch-ingested verify row" — the X row IS the
        # era row for this kit; the backfill corrects it to the right claim.
        item11_rows = [r for r in bf_by_item[11] if r["claim_family"] == "era"]
        if len(item11_rows) != 1:
            raise RuntimeError(f"backfill item 11: expected 1 era row, got {len(item11_rows)}")
        bf11 = item11_rows[0]
        rows_x = cur.execute(
            "SELECT id FROM verify_ledger WHERE kit_id='d4-mighty-throw' AND claim_family='era' AND verdict='CONTRADICTED'",
        ).fetchall()
        if len(rows_x) != 1:
            raise RuntimeError(f"backfill item 11: expected 1 CONTRADICTED era row for d4-mighty-throw, found {len(rows_x)}")
        cur.execute(
            """UPDATE verify_ledger SET verdict='CONFIRMED', anchor_quote=?, source_url=?,
               claim_text=COALESCE(?,claim_text), errata_applied=0
               WHERE id=?""",
            (bf11.get("anchor_quote"), bf11.get("source_url"), bf11.get("claim_text"), rows_x[0][0]),
        )
        if cur.rowcount != 1:
            raise RuntimeError(f"backfill item 11 UPDATE returned {cur.rowcount}")
        supersede_updated += 1

        # Item 12: two rows (d4-andariel-flurry identity + era)
        for fam in ["identity", "era"]:
            bf_rows = [r for r in bf_by_item[12] if r["claim_family"] == fam]
            if len(bf_rows) != 1:
                raise RuntimeError(f"backfill item 12 expected 1 row for d4-andariel-flurry/{fam}, got {len(bf_rows)}")
            bf = bf_rows[0]
            rows_u = cur.execute(
                "SELECT id FROM verify_ledger WHERE kit_id='d4-andariel-flurry' AND claim_family=? AND verdict='UNSUPPORTED'",
                (fam,)
            ).fetchall()
            if len(rows_u) < 1:
                raise RuntimeError(f"backfill item 12 d4-andariel-flurry/{fam}: no UNSUPPORTED rows found")
            # For era: may have 2 U rows (batch had two); supersede the one matching backfill claim_text
            if len(rows_u) == 1:
                target_id = rows_u[0][0]
            else:
                # Match by claim_text if possible
                bf_ct = bf.get("claim_text")
                ct_match = cur.execute(
                    "SELECT id FROM verify_ledger WHERE kit_id='d4-andariel-flurry' AND claim_family=? "
                    "AND verdict='UNSUPPORTED' AND claim_text=?",
                    (fam, bf_ct)
                ).fetchall()
                if len(ct_match) == 1:
                    target_id = ct_match[0][0]
                else:
                    target_id = rows_u[0][0]  # fall back to first U row
            cur.execute(
                """UPDATE verify_ledger SET verdict=?, anchor_quote=?, source_url=?,
                   claim_text=COALESCE(?,claim_text)
                   WHERE id=?""",
                (VERDICT_MAP[bf["verdict"]], bf.get("anchor_quote"), bf.get("source_url"),
                 bf.get("claim_text"), target_id),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"backfill item 12 UPDATE d4-andariel-flurry/{fam} returned {cur.rowcount}")
            supersede_updated += 1

        # Items 20, 21: TWO U era rows each; backfill supersedes launch-s1-3 U row only
        for item_num, kid in [(20, "d4-blood-surge"), (21, "d4-bone-spear")]:
            bf_rows = [r for r in bf_by_item[item_num] if r["claim_family"] == "era"]
            if len(bf_rows) != 1:
                raise RuntimeError(f"backfill item {item_num} expected 1 era row for {kid}, got {len(bf_rows)}")
            bf = bf_rows[0]
            bf_ct = bf.get("claim_text", "Build present/meta in launch-s1-3")
            rows_u = cur.execute(
                "SELECT id FROM verify_ledger WHERE kit_id=? AND claim_family='era' AND verdict='UNSUPPORTED' "
                "AND claim_text=?",
                (kid, bf_ct)
            ).fetchall()
            if len(rows_u) != 1:
                raise RuntimeError(f"backfill item {item_num}: expected 1 UNSUPPORTED era row "
                                   f"matching claim_text={bf_ct!r} for {kid}, found {len(rows_u)}")
            cur.execute(
                """UPDATE verify_ledger SET verdict=?, anchor_quote=?, source_url=?,
                   claim_text=COALESCE(?,claim_text)
                   WHERE id=?""",
                (VERDICT_MAP[bf["verdict"]], bf.get("anchor_quote"), bf.get("source_url"),
                 bf.get("claim_text"), rows_u[0][0]),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"backfill item {item_num} UPDATE {kid}/era returned {cur.rowcount}")
            supersede_updated += 1

        # Item 23: two rows (di-cyclone-monk-pvp identity + era)
        for fam in ["identity", "era"]:
            bf_rows = [r for r in bf_by_item[23] if r["claim_family"] == fam]
            if len(bf_rows) != 1:
                raise RuntimeError(f"backfill item 23 expected 1 row for di-cyclone-monk-pvp/{fam}, got {len(bf_rows)}")
            bf = bf_rows[0]
            supersede_update(cur, "di-cyclone-monk-pvp", fam, bf)
            supersede_updated += 1

        if supersede_updated != 22:
            raise RuntimeError(f"backfill supersede: expected 22 UPDATEs, got {supersede_updated}")
        print(f"P2 supersede UPDATEs: {supersede_updated}")

        # ---- item 26: INSERT new row (di-cyclone-strike-monk-base mechanics CONFIRMED) ----
        item26_rows = [r for r in bf_by_item[26] if r["claim_family"] == "mechanics"]
        if len(item26_rows) != 1:
            raise RuntimeError(f"backfill item 26: expected 1 mechanics row, got {len(item26_rows)}")
        bf26 = item26_rows[0]
        if VERDICT_MAP[bf26["verdict"]] != "CONFIRMED":
            raise RuntimeError(f"backfill item 26: expected CONFIRMED, got {bf26['verdict']}")
        # Verify no pre-existing mechanics row for this kit (already checked at pre-load, re-check inside txn)
        n_check = cur.execute(
            "SELECT COUNT(*) FROM verify_ledger WHERE kit_id='di-cyclone-strike-monk-base' AND claim_family='mechanics'"
        ).fetchone()[0]
        if n_check != 0:
            raise RuntimeError("item-26 INSERT: mechanics row already exists (should be impossible)")
        cur.execute(
            """INSERT INTO verify_ledger
               (kit_id, claim_family, claim_text, verdict, anchor_quote,
                source_url, errata_applied, run_tag, verified_date)
               VALUES (?,?,?,?,?,?,0,'vdm1',?)""",
            ("di-cyclone-strike-monk-base", "mechanics",
             bf26.get("claim_text"), "CONFIRMED",
             bf26.get("anchor_quote"), bf26.get("source_url"), TODAY),
        )
        if cur.rowcount != 1:
            raise RuntimeError(f"item-26 INSERT returned {cur.rowcount}")
        supersede_inserted += 1
        print(f"P2 item-26 INSERT: di-cyclone-strike-monk-base mechanics CONFIRMED — ok")

        # ---- backfill citations: INSERT with OR-IGNORE on UNIQUE(kit_id,url) ----
        cit_inserted = 0
        cit_ignored = 0
        for r in backfill_cit:
            cur.execute(
                """INSERT OR IGNORE INTO kit_citations
                   (kit_id, url, archive_url, site, author_handle, title,
                    cite_class, rank_class, accessed_date, quarantined)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (r["kit_id"], r["url"], r.get("archive_url"), r.get("site"),
                 r.get("author_handle"), r.get("title"), r.get("cite_class"),
                 r.get("rank_class"), r.get("accessed_date"), int(r.get("quarantined", 0))),
            )
            if cur.rowcount == 1:
                cit_inserted += 1
            else:
                cit_ignored += 1
        print(f"P2 backfill citations: inserted={cit_inserted} ignored={cit_ignored} (UNIQUE collisions)")

        # ---- POST-STATE assertion for verify_ledger ----
        # Expected: 831 + 680 batch + 1 insert = 1512
        vl_post2 = cur.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
        if vl_post2 != 1512:
            raise RuntimeError(f"POST-STATE P2: verify_ledger={vl_post2}, expected 1512")
        # Verdict histogram for basin-3 rows (effective post-overlay):
        # Batch: 554C/18X/107U/1SNF (=680 rows)
        # Items 1,6,7: anchor-upgrade only on already-C rows (no verdict change; 0 C-delta)
        # Items 2,3,4,8,9,12×2,14,15,16,18,19,20,21,23×2,24: 17 U->C (+17C, -17U)
        # Item 10: 1 U->X (+1X, -1U)
        # Item 11: X->C (+1C, -1X) [mighty-throw: superseded CONTRADICTED to CONFIRMED for voh-s6+]
        # Item 26: INSERT 1C (+1C)
        # Effective: C=554+17+1+1=573, X=18+1-1=18, U=107-17-1=89, SNF=1 = 681 rows
        # NOTE: dispatch states 576C/85U/19X/1SNF based on assumption items 1,6,7 were U (CW1 state);
        # actual file-truth shows these 3 were C in the delivered batch files (CW2 re-crawl landed
        # CONFIRMED anchors before batch close). FILES GOVERN: assert the file-truth state.
        basin3_kits = all_kits + ["di-cyclone-strike-monk-base"]
        qk2 = ",".join("?" * len(basin3_kits))
        b3_hist = dict(cur.execute(
            f"SELECT verdict, COUNT(*) FROM verify_ledger WHERE kit_id IN ({qk2}) GROUP BY verdict",
            basin3_kits
        ).fetchall())
        exp_b3 = {"CONFIRMED": 573, "UNSUPPORTED": 89, "CONTRADICTED": 18, "SOURCE_NOT_FOUND": 1}
        if b3_hist != exp_b3:
            raise RuntimeError(f"POST-STATE basin-3 verify histogram {b3_hist} != {exp_b3}")
        print(f"P2 POST-STATE: verify_ledger={vl_post2} ✓; basin-3 histogram {b3_hist} ✓ "
              f"(FILES GOVERN: items 1/6/7 were already CONFIRMED in batch — 573C not 576C)")

        # ================= PART 3: ERRATA queue (ERRATA-43+) =================
        errata_num = 43  # starting number
        errata_flags = 0  # verify rows flagged errata_applied=1

        # ----  ERRATA-3a: FALSIFIED-NEGATIVE annotations ×5 ----
        # Annotate, do NOT flip negative=1 flag. One root cause: kb models base-kit/dedicated-set only.
        # Kits: d3-spectral-blade, d3-wave-of-force, d4-incinerate, d4-kick, d4-wind-shear
        falsified_neg_annots = {
            "d3-spectral-blade": (
                "FALSIFIED-NEGATIVE ERRATA-43 (ANNOTATE ONLY — Matt review-book, do NOT flip negative): "
                "negative_canon_target falsified by Delsere's Magnum Opus 6pc (Slow-Time set) blanket coverage — "
                "kb conflated dedicated-set absence with no-set-path. Root cause: kb models base-kit/dedicated-set "
                "only, blind to blanket-set/aspect/unique redemption paths. NEGATIVE FLAG RETAINED pending Matt review. "
                "Rewrite candidate: 'no dedicated set; DMO Slow-Time blanket coverage exists; non-meta conclusion holds.'"
            ),
            "d3-wave-of-force": (
                "FALSIFIED-NEGATIVE ERRATA-43 (ANNOTATE ONLY — Matt review-book, do NOT flip negative): "
                "negative_canon_target 'no set multiplier path across any era' falsified by Delsere's Magnum Opus 6pc "
                "(Slow-Time +12,500% covers WoF; 2.4.1 build documented). Same root cause as spectral-blade. "
                "Rewrite candidate: 'no dedicated set; DMO coverage exists (blanket Slow-Time); non-meta conclusion holds.'"
            ),
            "d4-incinerate": (
                "FALSIFIED-NEGATIVE ERRATA-43 (ANNOTATE ONLY — Matt review-book, do NOT flip negative): "
                "negative_canon_target 'no burst window' falsified by Overheating unique (2s channel -> x[75-100%] "
                "for 5s). Root cause: kb blind to unique-item redemption paths. B-Tier is still below meta; "
                "the MECHANISM was wrong, not the conclusion. Rewrite: 'Overheating unique provides a burst window; "
                "persistently B-Tier; below set-era ceiling.'"
            ),
            "d4-kick": (
                "FALSIFIED-NEGATIVE ERRATA-43 (ANNOTATE ONLY — Matt review-book, do NOT flip negative): "
                "negative_canon_target 'never received set-equivalent amplification' falsified by Crown of Lucion "
                "(x105% S12) + Ring of Red Furor. ERA-BOUNDED: weakness was plausibly real launch->S11; redeemed by "
                "S12 unique buffs (leap-attack class). Rewrite candidate: era-bounded negative with S12 redemption note."
            ),
            "d4-wind-shear": (
                "FALSIFIED-NEGATIVE ERRATA-43 (ANNOTATE ONLY — Matt review-book, do NOT flip negative): "
                "negative_canon_target 'no proc identity or ramping mechanic' falsified by Aspect of the Calm Breeze "
                "(poison DoT) + Storm/Basic tag-inheritance scalars. Same root cause as incinerate/kick. "
                "Rewrite: 'Calm Breeze aspect provides proc identity; still below top-tier; non-meta conclusion holds.'"
            ),
        }
        for kid, clause in falsified_neg_annots.items():
            prepend_annot(cur, kid, clause, f"{kid} falsified-neg annot")
            # Flag the negative_canon CONTRADICTED verify rows
            n_flagged = cur.execute(
                "UPDATE verify_ledger SET errata_applied=1 "
                "WHERE kit_id=? AND claim_family='negative_canon' AND verdict='CONTRADICTED'",
                (kid,)
            ).rowcount
            errata_flags += n_flagged
        print(f"P3a FALSIFIED-NEGATIVE: 5 annotations + {errata_flags} verify rows flagged (spectral/wave/incinerate/kick/wind-shear neg X rows)")
        errata_num_3a = errata_num  # ERRATA-43 is the family-level entry for all 5

        # ---- ERRATA-44: di resource WRONG-RESOURCE sweep (ERRATA-38 class) ----
        # All di economy probe rows in canon_probe_facts: annotate resource_verbatim as d3-analog import, unreliable.
        # Attested post-launch picture: Druid=Primal Power, Blood Knight=Anger, Tempest=cooldown-only, Warlock=cooldown-only.
        # DO NOT invent replacements; annotate only.
        di_eco_rows = cur.execute(
            "SELECT id, kit_id, facts_json FROM canon_probe_facts WHERE kit_id LIKE 'di-%' AND family='economy'"
        ).fetchall()
        # Known-attested values (from b13 official text + b14/b15 findings)
        di_resource_known = {
            "di-druid-bear":      "Primal Power (official: 'Primal Power' — Blizzard class-intro page; b14)",
            "di-blood-knight":    "Anger (official: 'Consume all your Anger' — Blizzard class-intro; b13)",
            "di-tempest":         "cooldown-only (no resource builders or spenders; b15 corroboration)",
            "di-warlock-launch":  "cooldown-only (no resource builders or spenders — mmorpg.com hands-on; b15)",
        }
        di_sweep_count = 0
        for rid, kid, fj_str in di_eco_rows:
            obj = json.loads(fj_str)
            # Skip already-annotated rows (in case of accidental re-run)
            if "_prior_ingest13_di_resource" in obj:
                continue
            known = di_resource_known.get(kid, "")
            obj["_prior_ingest13_di_resource"] = {
                "resource_verbatim": obj.get("resource_verbatim"),
                "model": obj.get("model"),
                "note": (f"ERRATA-44 di WRONG-RESOURCE sweep: this resource_verbatim is a d3-analog import, "
                         f"UNRELIABLE for di (launch-class d3-analog names uniformly unsupported in fetched text). "
                         f"VALUE LEFT AS-IS (annotation only; do not invent replacements). "
                         f"Attested picture: {known if known else 'unattested at basin-3 close'}.")
            }
            cur.execute(
                "UPDATE canon_probe_facts SET facts_json=? WHERE id=? AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), rid, fj_str),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"ERRATA-44 di sweep {kid}: UPDATE returned {cur.rowcount}")
            di_sweep_count += 1
        if di_sweep_count != 23:
            raise RuntimeError(f"ERRATA-44 di sweep: expected 23 annotations, got {di_sweep_count}")
        print(f"P3b ERRATA-44 di resource sweep: {di_sweep_count} probe economy rows annotated (d3-analog import, unreliable)")

        # ---- ERRATA-45: d4 Paladin/Warlock resource CONTESTED + wing-strike probe annotation ----
        # wing-strike-arbiter has a probe economy row (cooldown); annotate contested resource (Faith vs Resolve)
        ws_eco = cur.execute(
            "SELECT facts_json FROM canon_probe_facts WHERE kit_id='d4-wing-strike-arbiter' AND family='economy'"
        ).fetchone()
        if ws_eco:
            obj = json.loads(ws_eco[0])
            obj["_prior_ingest13_paladin_resource"] = {
                "resource_verbatim": obj.get("resource_verbatim"),
                "note": ("ERRATA-45 Paladin resource CONTESTED: icy-veins uses both 'Faith' and 'Resolve'; "
                         "maxroll uses 'Faith' verbatim. 'cooldown' label in this row predates b10-b11 fetched picture. "
                         "DO NOT POPULATE from contested sources — variance annotation only per ingest-13 instruction.")
            }
            guarded(cur,
                "UPDATE canon_probe_facts SET facts_json=? WHERE kit_id='d4-wing-strike-arbiter' AND family='economy' AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), ws_eco[0]), "wing-strike-arbiter economy annot")
        # Annotate blazing-abyss-warlock economy (unknown/other — Warlock meter unclear)
        ba_eco = cur.execute(
            "SELECT facts_json FROM canon_probe_facts WHERE kit_id='d4-blazing-abyss-warlock' AND family='economy'"
        ).fetchone()
        if ba_eco:
            obj = json.loads(ba_eco[0])
            obj["_prior_ingest13_warlock_resource"] = {
                "resource_verbatim": obj.get("resource_verbatim"),
                "note": ("ERRATA-45 Warlock resource unclear: Shadowform buff-stack framing; no consensus source. "
                         "DO NOT POPULATE probe resource — variance annotation only per ingest-13 instruction.")
            }
            guarded(cur,
                "UPDATE canon_probe_facts SET facts_json=? WHERE kit_id='d4-blazing-abyss-warlock' AND family='economy' AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), ba_eco[0]), "blazing-abyss-warlock economy annot")
        # mech_note annotation for Paladin intro-epoch correction (debuted S11, not loh-s13-14)
        prepend_annot(cur, "d4-wing-strike-arbiter",
            "ERRATA-45 PALADIN DEBUT CORRECTION: Paladin debuted Season 11 (Divine Intervention, patch 2.5.0), "
            "NOT loh-s13-14. Era stamps loh-s13-14 are LEGAL (class existed and was meta) but do not "
            "represent the debut floor. Fetched text confirmed by b13 agent. See item-17 era extension in ERRATA-50.",
            "wing-strike-arbiter paladin debut annot")
        print("P3c ERRATA-45: Paladin/Warlock resource contested annotations applied")

        # ---- ERRATA-46: Probe-fabrication series (consolidated renumber, 13 items) ----
        # Items with VALUE CORRECTIONS (resource_verbatim or other field changes):
        # (1) d3-god-hungering economy: spirit/focus -> Hatred+Discipline (DH resource)
        #     Note: GoD-DH is a Demon Hunter kit; DH resource is Hatred (primary) + Discipline (secondary)
        # (2) d3-inna-allies economy: mana (reserve) -> Spirit (Monk resource is Spirit)
        # (3) d3-uliana-ep economy: mark+execute / meter / focus -> Spirit (Monk)
        # (4) d3-trag-nova economy: life+mana / self-cost -> Essence (Necromancer resource)
        # (5) d3-raiment-shenlong economy: ignite stack / meter / combo -> Spirit (Monk; Shenlong-spirit-dump)
        # (6) d4-bash economy: spirit/focus -> Fury (d4 Barbarian)
        # (7) d4-heartseeker economy: spirit/focus -> Energy (d4 Rogue)
        # (8) d4-evade-sb economy: evade charges -> Vigor (d4 Spiritborn)
        # (9) d4-dance-of-knives economy: charge -> Energy (d4 Rogue; movement-cost kit)
        # (10) d4-payback-sb delivery: retaliation counter-strike -> spammable Core->Basic via Rod of Kepeleke
        # (11) d3-frenzy-h90 economy: on-hit stacks -> Fury (Barbarian; Horde 6pc set)
        # (12) d4-hammerdin-paladin element: element "holy" is d2-lineage import (d4 has no holy damage type)
        #      (hammerdin has NO probe economy row; element probe also absent; add mech_note annotation only)
        # (13) di-minion-necro economy: 'Essence' is actually CORRECT for di minion-necro (Essence IS di Necro resource)
        #      HOLD: di-minion-necro 'Essence' is ALREADY the d3-analog name for Necromancer — and Necromancer
        #      in DI ALSO uses Essence (it's the one di resource that happens to share the d3 name). So this
        #      is NOT a fabrication for minion-necro. Leave it, but note the coincidence.

        probe_fab_fixes = {
            "d3-god-hungering": {
                "family": "economy",
                "field": "resource_verbatim", "old": "spirit/focus", "new": "Hatred+Discipline",
                "model_new": "dual-resource", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #1: DH resource is Hatred+Discipline, not spirit/focus. "
                        "model meter->dual-resource; GoD converts primary generator Hungering Arrow into payload via Strafe."
            },
            "d3-inna-allies": {
                "family": "economy",
                "field": "resource_verbatim", "old": "mana (reserve)", "new": "Spirit",
                "model_new": "reserve", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #2: d3 Monk resource is Spirit, not mana. "
                        "Inna S24 rework summons full mystic-ally menagerie — Spirit reserve."
            },
            "d3-uliana-ep": {
                "family": "economy",
                "field": "resource_verbatim", "old": "mark+execute", "new": "Spirit",
                "model_new": "meter", "meter_type_new": "focus",
                "note": "ERRATA-46 probe-fabrication #3: d3 Monk resource is Spirit; 'mark+execute' describes "
                        "the mechanic, not the resource name. model=meter (focus-dump via Seven-Sided Strike)."
            },
            "d3-trag-nova": {
                "family": "economy",
                "field": "resource_verbatim", "old": "life+mana", "new": "Essence",
                "model_new": "self-cost", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #4: d3 Necromancer resource is Essence; 'life+mana' "
                        "describes the blood-magic MECHANIC (life-spend via Trag'Oul's), not the meter name. "
                        "model=self-cost preserved (life payment is the distinctive mechanic)."
            },
            "d3-raiment-shenlong": {
                "family": "economy",
                "field": "resource_verbatim", "old": "ignite stack", "new": "Spirit",
                "model_new": "meter", "meter_type_new": "focus",
                "note": "ERRATA-46 probe-fabrication #5: d3 Monk resource is Spirit; 'ignite stack' "
                        "describes the Shenlong spirit-dump rhythm, not the resource name. model=meter/focus-dump."
            },
            "d4-bash": {
                "family": "economy",
                "field": "resource_verbatim", "old": "spirit/focus", "new": "Fury",
                "model_new": "generator-spender", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #6: d4 Barbarian resource is Fury. "
                        "Bash generates AND spends Fury (fetched: b10 addendum). model=generator-spender."
            },
            "d4-heartseeker": {
                "family": "economy",
                "field": "resource_verbatim", "old": "spirit/focus", "new": "Energy",
                "model_new": "generator-spender", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #7: d4 Rogue resource is Energy (not spirit/focus). "
                        "Heartseeker is a Basic skill generating Energy. model=generator."
            },
            "d4-evade-sb": {
                "family": "economy",
                "field": "resource_verbatim", "old": "evade charges", "new": "Vigor",
                "model_new": "meter", "meter_type_new": "focus",
                "note": "ERRATA-46 probe-fabrication #8: d4 Spiritborn resource is Vigor; 'evade charges' "
                        "describes the eagle-spirit aspect mechanic, not the meter name."
            },
            "d4-dance-of-knives": {
                "family": "economy",
                "field": "resource_verbatim", "old": "charge", "new": "Energy",
                "model_new": "spender", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #9: d4 Rogue resource is Energy; 'charge' described "
                        "the movement-channel mechanic, not the meter name. Channel spends Energy."
            },
            "d3-frenzy-h90": {
                "family": "economy",
                "field": "resource_verbatim", "old": "on-hit stacks", "new": "Fury",
                "model_new": "generator", "meter_type_new": "n/a",
                "note": "ERRATA-46 probe-fabrication #11: d3 Barbarian resource is Fury; 'on-hit stacks' "
                        "describes the Bastion's Revered stack mechanic, not the resource name."
            },
        }

        fab_corrected = 0
        for kid, spec in probe_fab_fixes.items():
            fam = spec["family"]
            row = cur.execute(
                "SELECT id, facts_json FROM canon_probe_facts WHERE kit_id=? AND family=?", (kid, fam)
            ).fetchone()
            if row is None:
                raise RuntimeError(f"ERRATA-46 probe-fab {kid}/{fam}: no probe row found")
            rid, fj_str = row
            obj = json.loads(fj_str)
            if obj.get("resource_verbatim") != spec["old"]:
                raise RuntimeError(f"ERRATA-46 probe-fab {kid}/{fam}: precondition mismatch "
                                   f"resource_verbatim={obj.get('resource_verbatim')!r} != {spec['old']!r}")
            obj["_prior_ingest13_fab"] = {
                "resource_verbatim": obj.get("resource_verbatim"),
                "model": obj.get("model"), "meter_type": obj.get("meter_type"),
                "plain_text": obj.get("plain_text"), "note": spec["note"]
            }
            obj["resource_verbatim"] = spec["new"]
            if "model_new" in spec:
                obj["model"] = spec["model_new"]
            if "meter_type_new" in spec:
                obj["meter_type"] = spec["meter_type_new"]
            # Reconcile plain_text leading token
            pt = obj.get("plain_text", "")
            if isinstance(pt, str) and pt:
                old_tok = spec["old"]
                if pt.lower().startswith(old_tok.lower()):
                    obj["plain_text"] = spec["new"] + pt[len(old_tok):]
            cur.execute(
                "UPDATE canon_probe_facts SET facts_json=? WHERE id=? AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), rid, fj_str),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"ERRATA-46 probe-fab UPDATE {kid}/{fam} returned {cur.rowcount}")
            fab_corrected += 1

        # Item 10: d4-payback-sb delivery (retaliation counter-strike -> spammable Core->Basic)
        pb_del = cur.execute(
            "SELECT id, facts_json FROM canon_probe_facts WHERE kit_id='d4-payback-sb' AND family='delivery'"
        ).fetchone()
        if pb_del:
            rid, fj_str = pb_del
            obj = json.loads(fj_str)
            # The 'value' field says self-origin with retaliation-counter-strike evidence
            obj["_prior_ingest13_fab"] = {
                "value": obj.get("value"), "evidence": obj.get("evidence"),
                "note": ("ERRATA-46 probe-fabrication #10 (delivery): 'Retaliation counter-strike from body when "
                         "struck' is FABRICATED — Payback is a spammable Core/Basic skill with Rod of Kepeleke "
                         "(not a reactive counter-strike). Delivery class = spammable-core, NOT reactive-proc. "
                         "Value LEFT as self-origin (spatial delivery still approximately correct); evidence rewritten.")
            }
            obj["evidence"] = ("Spammable Core->Basic skill via Rod of Kepeleke aspect — ground-level physical AoE, "
                               "NOT a reactive counter-strike (b12 addendum probe-fabrication #10).")
            cur.execute(
                "UPDATE canon_probe_facts SET facts_json=? WHERE id=? AND facts_json=?",
                (json.dumps(obj, ensure_ascii=False), rid, fj_str),
            )
            if cur.rowcount != 1:
                raise RuntimeError(f"ERRATA-46 payback delivery UPDATE returned {cur.rowcount}")
            fab_corrected += 1

        # Item 12: d4-hammerdin-paladin element "holy" is d2-lineage import (no probe row; annotate via mech_note)
        # (no element probe row exists for d4-hammerdin-paladin — annotation only)
        prepend_annot(cur, "d4-hammerdin-paladin",
            "ERRATA-46 probe-fabrication #12 (element, d2-lineage import class): d4 Paladin has NO 'holy' "
            "damage type — 'holy' element was imported from d2/d3 Paladin lineage. d4 Paladin damage is "
            "Holy (visual) but maps to Physical/Lightning in game mechanics. Element probe field absent; "
            "any future probe using 'holy' for d4-hammerdin-paladin is a d2-lineage artifact.",
            "d4-hammerdin-paladin element d2-lineage annot")
        # Also annotate d3-blaze-sorc (probe-fabrication #13: 'channeled' -> movement-trail)
        # d3-blaze-sorc has NO probe rows; annotate via mech_note
        prepend_annot(cur, "d2-blaze-sorc",
            "ERRATA-46 probe-fabrication #13 (delivery): b01 deep-audit CONFIRMED RF-01 — probe 'channeled' "
            "is WRONG; maxroll fetched text = movement-trail delivery ('a trail of fire that follows her '). "
            "d2-blaze-sorc has no probe rows in corpus; this annotation flags the kb 'channeled' description "
            "as a probe-fabrication artifact for any future probe authoring.",
            "d2-blaze-sorc channeled->movement-trail annot")
        # di-echoing-strike probe annotation (no probe rows; annotate via mech_note for d2-wl-echoing-strike)
        prepend_annot(cur, "d2-wl-echoing-strike",
            "ERRATA-46 probe-fabrication #N (footprint/geometry): b05 flagged probe geometry "
            "'at-target/small-radius/melee' as WRONG — fetched text: 'ranged physical fighter... throws "
            "projections of his weapons' = ranged delivery, NOT melee. Probe geometry artifact if probe "
            "row exists; flag for any future probe authoring.",
            "d2-wl-echoing-strike geometry ranged annot")
        # d3-firebomb negative_canon_target rewrite candidate annotation
        prepend_annot(cur, "d3-firebomb",
            "ERRATA-46 probe note (b06): negative_canon_target 'ground-targeted' -> 'lobbed projectile' "
            "framing fix. Official text: 'Lob an explosive skull...' — the delivery is a LОБBED projectile, "
            "not a ground-targeted placement. Substance of the negative CONFIRMED (meta absence is real). "
            "Value LEFT as-is; rewrite candidate for review-book.",
            "d3-firebomb negative_canon_target framing annot")
        # di-warlock 'Shadow' resource is a confirmed fabrication (already covered by ERRATA-44 sweep + b15 X)
        # The b15 X di-warlock-launch/mechanics is already in verify_ledger as CONTRADICTED
        # Flag errata_applied on that row
        n_wl = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='di-warlock-launch' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        errata_flags += n_wl
        print(f"P3d ERRATA-46 probe-fabrication: {fab_corrected} value corrections + annotations; "
              f"warlock mechanics flag: {n_wl}")

        # ---- ERRATA-47..50 era errata ----
        # Multiple era restamps + extensions + annotations

        # ERRATA-47: d3-lod-archetype era floor set-era -> late-sets (LoD gem = S18, Patch 2.6.6)
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d3-lod-archetype' AND eras=?",
                ("late-sets;s39", "set-era;late-sets;s39"), "d3-lod-archetype era floor fix (set-era drop)")
        # Flag era CONTRADICTED verify row
        n_lod = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-lod-archetype' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_lod != 1:
            raise RuntimeError(f"d3-lod-archetype era flag: expected 1 row, got {n_lod}")
        errata_flags += n_lod
        print(f"  ERRATA-47: d3-lod-archetype era set-era->late-sets (LoD gem = S18 Patch 2.6.6)")

        # ERRATA-48: d3-ww-wastes era vanilla -> ros-early floor (Wastes set added Patch 2.2.0)
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d3-ww-wastes' AND eras=?",
                ("ros-early;set-era;late-sets;s39", "vanilla;set-era;late-sets;s39"),
                "d3-ww-wastes era floor fix (vanilla drop, ros-early add)")
        # Annotation: WW-barb archetype was vanilla-meta; kit-AS-SPECIFIED (Wastes set) is ros-early
        prepend_annot(cur, "d3-ww-wastes",
            "ERRATA-48: era floor vanilla DROPPED (Wrath of the Wastes set added in Patch 2.2.0 / RoS-S2 = "
            "ros-early). NOTE: WW-barb the ARCHETYPE was vanilla-meta; the KIT-AS-SPECIFIED rides the Wastes "
            "set rework. If the kb intended archetype lineage, era annotation/rename is needed at review-book.",
            "d3-ww-wastes era floor annot")
        n_ww = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-ww-wastes' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_ww != 1:
            raise RuntimeError(f"d3-ww-wastes era flag: expected 1, got {n_ww}")
        errata_flags += n_ww
        print(f"  ERRATA-48: d3-ww-wastes era vanilla->ros-early (Wastes set Patch 2.2.0)")

        # ERRATA-49: d3-raekor-boulder era floor set-era -> attested S26 rework
        # Raekor CHARGE existed set-era; boulder-kit specified by S26 rework (Boulder Toss rune)
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d3-raekor-boulder' AND eras=?",
                ("s26-rework;late-sets;s39", "set-era;late-sets;s39"),
                "d3-raekor-boulder era floor fix (set-era drop, s26-rework add)")
        prepend_annot(cur, "d3-raekor-boulder",
            "ERRATA-49: era floor set-era DROPPED — Raekor CHARGE archetype existed set-era, but the "
            "BOULDER-TOSS kit is the S26 rework ('reworked again in Season 26... Boulder Toss being the "
            "skill rune of choice'). ik-hota law: kit-as-specified dates from rework, not archetype debut.",
            "d3-raekor-boulder era floor annot")
        n_rb = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-raekor-boulder' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_rb != 1:
            raise RuntimeError(f"d3-raekor-boulder era flag: expected 1, got {n_rb}")
        errata_flags += n_rb
        print(f"  ERRATA-49: d3-raekor-boulder era set-era->s26-rework")

        # ERRATA-50: d4-wing-strike-arbiter era extension (item-17 exception: no verify write; era only)
        # Currently: loh-s13-14; extend to: s7-s12;loh-s13-14 (attested S11-S12 meta via wowhead "Season 11" title)
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d4-wing-strike-arbiter' AND eras=?",
                ("s7-s12;loh-s13-14", "loh-s13-14"),
                "d4-wing-strike-arbiter era extension (s7-s12 prepend)")
        prepend_annot(cur, "d4-wing-strike-arbiter",
            "ERRATA-50 ERA EXTENSION (item-17, floor-too-late class, ERRATA-17 precedent): backfill item 17 "
            "found wowhead 'Season 11' title attesting meta presence S11-S12. Batch era row (loh-s13-14) "
            "was already CONFIRMED — NOT superseded (exception: the batch C row stands; extension lands as "
            "era restamp only). See ERRATA-45 for Paladin debut S11 annotation.",
            "d4-wing-strike-arbiter era extension annot")
        # No verify flag (the era row is CONFIRMED, not CONTRADICTED — extension, not flip)
        print(f"  ERRATA-50: d4-wing-strike-arbiter era loh-s13-14 -> s7-s12;loh-s13-14 (item-17 extension)")

        # Additional era errata (annotation class — no restamp):

        # d3-natalya-rov: s39 token removal (b08 X — 'no longer relevant in Patch 2.7.5')
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d3-natalya-rov' AND eras=?",
                ("set-era;late-sets", "set-era;late-sets;s39"),
                "d3-natalya-rov era s39 removal")
        n_nat = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-natalya-rov' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_nat != 1:
            raise RuntimeError(f"d3-natalya-rov era flag: expected 1, got {n_nat}")
        errata_flags += n_nat
        print(f"  era: d3-natalya-rov s39 token removed (Patch 2.7.5 retirement)")

        # d3-ik-hota: vanilla floor-too-early annotation (earliest attested S4; no restamp — steward routes to D-2a adjudication)
        prepend_annot(cur, "d3-ik-hota",
            "ERA WATCH (D-2a floor-too-early candidate, INGEST-13 adjudication): era 'vanilla' is UNATTESTED "
            "as a set-kit floor — the IK+CotA/WotB 6pc synergy (kit-as-specified) was a set-era REWORK; "
            "earliest attested season-era is S4 (dexerto nerf-news + primagames). IK set existed at vanilla "
            "but the characterizing set-bonus combo did not. Vanilla row is honest-U in verify files; "
            "steward routes to D-2a adjudication — value LEFT as-is pending review-book decision.",
            "d3-ik-hota vanilla era annotation")

        # d4-shadowblight era s7 annotation (S8 is earliest changelog; s7 unattested in current eras)
        prepend_annot(cur, "d4-shadowblight",
            "ERA NOTE (b13 steward): s7 floor in current eras 's7-s12;loh-s13-14' is UNATTESTED from fetched "
            "text — earliest changelog evidence is S8. s7 is floor-adjacent; no restamp at this wave "
            "(token-overlap with voh-s6+ boundary already documented as scheme-ambiguity). Annotated per b13.",
            "d4-shadowblight era s7 annotation")

        # d4-mighty-throw voh-s6+ floor-too-late addition (b12 X; backfill item-11 superseded X->C)
        # canon_corpus.eras restamp still needed (the field value must be updated regardless)
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d4-mighty-throw' AND eras=?",
                ("voh-s6+;s7-s12", "s7-s12"),
                "d4-mighty-throw era floor add voh-s6+")
        # Note: the era CONTRADICTED verify row was superseded to CONFIRMED by backfill item-11 (P2)
        # So errata_applied flag on a CONTRADICTED row = 0 rows expected (the row is now CONFIRMED).
        # The canon_corpus restamp is the errata action; verify-row flagging not applicable here.
        n_mt = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d4-mighty-throw' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        # n_mt will be 0 (item-11 supersede changed verdict to CONFIRMED); this is expected
        errata_flags += n_mt
        print(f"  era: d4-mighty-throw voh-s6+ floor added (S6 tier-list attestation; item-11 supersede set CONFIRMED)")

        # d4-lightning-spear era in-token floor note (S5 inception within loot-reborn-s4-5 token; annotation only)
        prepend_annot(cur, "d4-lightning-spear",
            "ERA IN-TOKEN NOTE (b12 X: era 'loot-reborn-s4-5' floor-too-early): 'the strongest Sorcerer build "
            "from its very inception in Season 5' — inception is S5-only within the loot-reborn-s4-5 token "
            "(S4 predates Lightning Spear). Token NOT restamped (voh-s6+/s7-s12 overlap scheme ambiguity noted); "
            "S5 inception annotated here. Era X row (loot-reborn-s4-5 floor) flagged via batch file.",
            "d4-lightning-spear era S5-inception note")
        # Flag era X verify row (already CONTRADICTED from batch b12)
        n_ls_era = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d4-lightning-spear' AND claim_family='era' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_ls_era != 1:
            raise RuntimeError(f"d4-lightning-spear era flag: expected 1, got {n_ls_era}")
        errata_flags += n_ls_era

        # d3-summon-druid rotw era-token backfill (tmGrunty '3.2 RotW Summon Druid Guide')
        # Currently eras='lod;d2r-2.4+'; add rotw token
        guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id='d2-summon-druid' AND eras=?",
                ("lod;rotw;d2r-2.4+", "lod;d2r-2.4+"),
                "d2-summon-druid rotw era-token backfill")
        print(f"  era: d2-summon-druid rotw token added (tmGrunty '3.2 RotW' guide)")

        # d2-mosaic-sin rotw/NL nuance annotation (not a restamp; NL-only nuance)
        prepend_annot(cur, "d2-mosaic-sin",
            "ERA NUANCE NOTE (b04 addendum): 'As of 3.1 (Reign of the Warlock), Mosaic can only be made in "
            "Non-Ladder' — the rotw-s13+ era token should carry an NL-only qualifier. Value LEFT as-is "
            "(token structure does not support NL/ladder qualifiers natively); annotated for review-book.",
            "d2-mosaic-sin rotw NL-only nuance annot")

        # d4-shadowblight era: backfill item-16 superseded the era U->C (already handled in P2)
        # The backfill gave s7-s12 as the floor; the CONFLICTING s7-unattested annotation above is correct
        # because the batch b13 notes 'earliest changelog S8'. These are consistent (annotation = flag only).

        # d2-leap-attack-barb annotation: "just a movement skill pre-2.4" corroborates era-bounded negative
        prepend_annot(cur, "d2-leap-attack-barb",
            "ERA-BOUNDED NEGATIVE CORROBORATION (backfill-3 item 5 summary): community fetched text affirms "
            "'just a movement skill pre-D2R-2.4' — corroborates the CW1 era-bounded-negative reading for "
            "classic/lod era. era U for classic-narrowing is honest (backfill retry-exhausted; leap-attack "
            "as a classic build was a movement-verb, not a damage archetype).",
            "d2-leap-attack-barb era-bounded negative corroboration annot")

        # voh-s6+/s7-s12 token-overlap scheme note (annotation, not a restamp)
        prepend_annot(cur, "d4-mighty-throw",
            "ERA TOKEN-OVERLAP NOTE (ingest-13): voh-s6+ and s7-s12 tokens overlap at S6/S7 boundary — "
            "the scheme choice between them is ambiguous for kits attested at exactly S6. voh-s6+ floor here "
            "grounded by S6 tier-list; s7-s12 was the original batch claim. Both tokens admit S6 presence; "
            "this ambiguity is a catalogue-level scheme note, NOT a data error.",
            "d4-mighty-throw era token-overlap scheme annot")

        print(f"  era errata: lod-archetype(ERRATA-47) ww-wastes(ERRATA-48) raekor-boulder(ERRATA-49) "
              f"wing-strike(ERRATA-50) + natalya-rov s39 + mighty-throw voh + lightning-spear S5 + "
              f"summon-druid rotw + annotations (ik-hota,shadowblight,mosaic,leap-attack,token-overlap)")

        # ---- ERRATA-51: core_skills errata ----
        # d2-fishyzon: Guided Arrow/Valkyrie -> Lightning Fury/Charged Strike/Frozen Arrow (Nightfish lineage)
        old_fish = '["Guided Arrow", "Valkyrie"]'
        new_fish = json.dumps(["Lightning Fury", "Charged Strike", "Frozen Arrow"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='d2-fishyzon' AND core_skills=?",
                (new_fish, old_fish), "d2-fishyzon core_skills fix (Nightfish lineage)")
        # Flag mechanics CONTRADICTED verify row
        n_fish_mech = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d2-fishyzon' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_fish_mech != 1:
            raise RuntimeError(f"d2-fishyzon mechanics flag: expected 1, got {n_fish_mech}")
        errata_flags += n_fish_mech
        # Also add aliases annotation (Nightfish folk-name family, not just core_skills)
        prepend_annot(cur, "d2-fishyzon",
            "ERRATA-51 core_skills HIGH: Guided Arrow/Valkyrie = SPEC-ERROR (kb mismatch — the fishyzon IS "
            "the Nightfish LF/CS build, NOT the Guided Arrow/Valkyrie build). core_skills corrected to "
            "Lightning Fury / Charged Strike / Frozen Arrow. ALSO: spec aliases 'Fishyzon, Amazon fish-build' "
            "CONFIRMED by blogspot-2009 fetch; 'Guided Arrow build' alias is a MISATTRIBUTION (different "
            "archetype entirely). Alias cleanup needed at review-book.",
            "d2-fishyzon core_skills fix annot")

        # d3-rathma-aotd: remove Skeletal Mage, add Command Skeletons + Revive
        old_rathma = '["Army of the Dead", "Skeletal Mage"]'
        new_rathma = json.dumps(["Army of the Dead", "Command Skeletons", "Revive"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='d3-rathma-aotd' AND core_skills=?",
                (new_rathma, old_rathma), "d3-rathma-aotd core_skills fix (Skeletal Mage removed)")
        n_rathma = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-rathma-aotd' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_rathma != 1:
            raise RuntimeError(f"d3-rathma-aotd mechanics flag: expected 1, got {n_rathma}")
        errata_flags += n_rathma
        prepend_annot(cur, "d3-rathma-aotd",
            "ERRATA-51 core_skills HIGH: 'Skeletal Mages don't work for this set bonus' (fetched text) — "
            "Skeletal Mage removed; Command Skeletons + Revive added (correct Rathma Army of the Dead drivers).",
            "d3-rathma-aotd core_skills fix annot")

        # d4-blazing-abyss-warlock: 'Blazing Abyss' -> 'Blazing Scream' (stale-prior, HIGH)
        old_blaze = '["Blazing Abyss"]'
        new_blaze = json.dumps(["Blazing Scream"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='d4-blazing-abyss-warlock' AND core_skills=?",
                (new_blaze, old_blaze), "d4-blazing-abyss-warlock core_skills fix (Blazing Abyss->Blazing Scream)")
        n_blaze = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d4-blazing-abyss-warlock' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_blaze != 1:
            raise RuntimeError(f"d4-blazing-abyss-warlock mechanics flag: expected 1, got {n_blaze}")
        errata_flags += n_blaze
        prepend_annot(cur, "d4-blazing-abyss-warlock",
            "ERRATA-51 core_skills HIGH: skill named 'Blazing Abyss' in kb is named 'BLAZING SCREAM' in fetched "
            "text ('Blazing Scream – One of our main damage sources'). kb name = stale-prior guess (post-cutoff "
            "Warlock; CW4 stale-prior warning predicted exactly this). Kit_id retains 'abyss' for continuity.",
            "d4-blazing-abyss-warlock core_skills fix annot")

        # d4-shadowblight: add Reap to core_skills
        old_shadow = '["Blight", "Decompose", "Shadowblight"]'
        new_shadow = json.dumps(["Blight", "Decompose", "Reap", "Shadowblight"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='d4-shadowblight' AND core_skills=?",
                (new_shadow, old_shadow), "d4-shadowblight core_skills add Reap")
        prepend_annot(cur, "d4-shadowblight",
            "ERRATA-51 core_skills: Reap added (b13 addendum: 'shadowblight core_skills Decompose -> Reap' "
            "— both Decompose and Reap are attested as core generation tools; full list updated).",
            "d4-shadowblight core_skills Reap add annot")

        # d3-frenzy-h90: add Sprint (b08 erratum: Sprint is part of the core loop)
        old_frenzy = '["Frenzy"]'
        new_frenzy = json.dumps(["Frenzy", "Sprint"], ensure_ascii=False)
        guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='d3-frenzy-h90' AND core_skills=?",
                (new_frenzy, old_frenzy), "d3-frenzy-h90 core_skills add Sprint")
        prepend_annot(cur, "d3-frenzy-h90",
            "ERRATA-51 core_skills: Sprint added (b08 addendum: Frenzy H90 uses Sprint as part of the core "
            "high-speed loop under the Horde of the Ninety Savages set).",
            "d3-frenzy-h90 core_skills Sprint add annot")

        print(f"P3f ERRATA-51 core_skills: fishyzon(LF/CS/FA), rathma(CmdSkeletons+Revive), "
              f"blazing-abyss(BlazeScream), shadowblight(+Reap), frenzy-h90(+Sprint)")

        # ---- ERRATA-52: alias/lineage errata ----
        # d3-god-hungering: remove 'Grace of Inarius' alias (fetched = Gears of Dreadlands consistently)
        # lineage field stores alias/set info; current value is ''
        # The alias appears in the folk_name or lineage; check both
        goh_folk = cur.execute("SELECT folk_name FROM canon_corpus WHERE kit_id='d3-god-hungering'").fetchone()[0]
        if goh_folk:
            # Check if Grace of Inarius appears in folk_name or lineage
            if "Grace of Inarius" in goh_folk:
                new_folk = goh_folk.replace("Grace of Inarius", "Gears of Dreadlands").replace("; ", ";").strip(";")
                guarded(cur, "UPDATE canon_corpus SET folk_name=? WHERE kit_id='d3-god-hungering' AND folk_name=?",
                        (new_folk, goh_folk), "d3-god-hungering folk_name alias fix")
        # Annotate regardless (b06 X landed on identity — alias was the contradiction)
        # Flag identity CONTRADICTED verify row
        n_goh = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d3-god-hungering' AND claim_family='identity' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_goh != 1:
            raise RuntimeError(f"d3-god-hungering identity flag: expected 1, got {n_goh}")
        errata_flags += n_goh
        prepend_annot(cur, "d3-god-hungering",
            "ERRATA-52 alias: 'Grace of Inarius DH' alias is a SET-NAME CONFABULATION — fetched text uniformly "
            "'Gears of Dreadlands' ('GoD DH'). Grace of Inarius = Necromancer set. Alias removed from identity claims.",
            "d3-god-hungering alias fix annot")

        # di-frenzy-barb: alias/core_skills Sprint annotation (alias 'DI Frenzy Sprint Barb' + core Sprint unattested)
        prepend_annot(cur, "di-frenzy-barb",
            "ERRATA-52 alias (b14 addendum): alias 'DI Frenzy Sprint Barb' and core_skills Sprint are UNATTESTED "
            "in fetched di text — fetched shows Furious Charge, not Sprint (Sprint is a d3/d2 Barbarian skill; "
            "DI Barbarian kit uses Furious Charge). core_skills=['Frenzy','Sprint'] needs review; "
            "Sprint may be a d3-analog import. Medium confidence erratum.",
            "di-frenzy-barb Sprint alias annot")

        # di-tempest: element Lightning -> Wind/Water correction + Zephyr clone correction
        # elem_raw currently 'physical'; update to 'wind/water'
        guarded(cur, "UPDATE canon_corpus SET elem_raw=? WHERE kit_id='di-tempest' AND elem_raw=?",
                ("wind/water", "physical"), "di-tempest elem_raw fix (Lightning->Wind/Water)")
        # Also update core_skills: 'Mist Touched(clone passive)' -> Zephyr-shade clarification
        old_temp_cs = '["wind mobility kit", "Mist Touched(clone passive)"]'
        cur_temp_cs = cur.execute("SELECT core_skills FROM canon_corpus WHERE kit_id='di-tempest'").fetchone()[0]
        if cur_temp_cs and "Mist Touched" in cur_temp_cs:
            new_temp_cs = json.dumps(["wind mobility kit", "Zephyr(shade conjuration, not clone-passive)"],
                                     ensure_ascii=False)
            guarded(cur, "UPDATE canon_corpus SET core_skills=? WHERE kit_id='di-tempest' AND core_skills=?",
                    (new_temp_cs, cur_temp_cs), "di-tempest core_skills Zephyr fix")
        # Flag mechanics CONTRADICTED verify row (b15 X)
        n_temp = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='di-tempest' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        if n_temp != 1:
            raise RuntimeError(f"di-tempest mechanics flag: expected 1, got {n_temp}")
        errata_flags += n_temp
        prepend_annot(cur, "di-tempest",
            "ERRATA-52 element+alias: elem_raw Lightning->Wind/Water (official: 'Command Wind and Sea as the "
            "Tempest'); 'Mist Touched(clone passive)' -> Zephyr shade-conjuration (Zephyr conjures temporary "
            "shades, not clones; 'clone' is an alias artifact). di-tempest resource 'Spirit (Tempest)' = "
            "d3-analog import per ERRATA-44 sweep (cooldown-only class per b15 X).",
            "di-tempest element/alias fix annot")
        print(f"P3g ERRATA-52 alias/lineage: god-hungering alias, di-frenzy-barb Sprint, di-tempest Wind/Water")

        # ---- ERRATA-53: Kit-level flag annotations (4 kits, annotation only — Matt review book) ----
        kit_flag_annots = {
            "d2-wl-void-rift": (
                "KIT-LEVEL FLAG (ANNOTATION ONLY — Matt keep/relabel/excise decision): "
                "UNATTESTED KIT-LEVEL, search-derived-seed-harvest-failed class (first of run). All four "
                "families honest-negative (identity U / mechanics SNF / era U / negative_canon U). Harvest "
                "performed against full Warlock roster across icy-veins/maxroll/gurugamer/diablo2.io — "
                "sole hit was one AI-synthesized snippet with no underlying page. SPEC ERROR CANDIDATE. "
                "Review-book decision: keep-as-registered-ghost vs excise."
            ),
            "di-bombardment-wizard-pvp": (
                "KIT-LEVEL FLAG (ANNOTATION ONLY — Matt keep/relabel/excise decision): "
                "d3->di MISAPPLICATION candidate (void-rift class). Honest 3xU; Bombardment absent from "
                "icy-veins full Wizard skill list for DI. Bombardment IS a d3 skill; DI Wizard skill list "
                "does not include it. Likely a d3->di cross-game misapplication at kb-generation. "
                "Review-book decision: relabel vs excise."
            ),
            "d4-spiritborn-vortex": (
                "KIT-LEVEL FLAG (ANNOTATION ONLY — Matt keep/relabel/excise decision): "
                "component-not-archetype. Identity + mechanics honest-U; Vortex is a passive/triggered "
                "component INSIDE Soar/Quill-Volley builds, not a standalone archetype. Third kit-level "
                "review-book decision (distinct sub-class from void-rift's harvest-fail and bombardment's "
                "misapplication). Review-book decision: relabel vs excise."
            ),
            "di-spiritform-druid-pvp": (
                "KIT-LEVEL FLAG (ANNOTATION ONLY — Matt keep/relabel/excise decision): "
                "negative-on-mis-specified-mechanic sub-class (minted b15). 'Spirit form' is NOT a named "
                "DI Druid skill in any fetched text; attested complaints are healing/sustain-denial, not "
                "spirit-form-CC. NEGATIVE FLAG RETAINED (di-spiritform is negative=1); but the mechanic "
                "specification is wrong. Review-book: relabel (to sustain-denial CC build) or excise."
            ),
        }
        for kid, clause in kit_flag_annots.items():
            prepend_annot(cur, kid, clause, f"{kid} kit-level flag annot")
        print(f"P3h ERRATA-53: 4 kit-level flag annotations (void-rift, bombardment-wizard, spiritborn-vortex, spiritform-druid)")

        # ---- ERRATA-54: NULL-era backfills (7 kits; guarded on NULL only) ----
        # Attested-era evidence from batch summaries; fill, never overwrite non-NULL.
        null_era_fills = {
            "d2-sacrifice":          ("lod", "d2 Arreat Summit lod skill-page; backfill-3 item 8 era CONFIRMED"),
            "d2-teleport-sorc":      ("lod;d2r-2.4+", "b03 roster: Teleport present at lod; D2R retained"),
            "d3-call-of-the-ancients": ("vanilla;set-era;late-sets;s39", "b06 summary: zero era rows per roster-hygiene; attested continuous from vanilla IK set"),
            "d3-dashing-strike-monk": ("vanilla;set-era;late-sets;s39", "b06 summary: zero era rows per roster-hygiene; Dashing Strike present from vanilla Monk"),
            "d3-wizard-black-hole":  ("vanilla;set-era", "b09 summary: 'utility-only, no primary-build era'; late-sets/s39 omitted — Black Hole never primary"),
            "d4-spiritborn-vortex":  ("voh-s6+", "b13 summary: Spiritborn launched VoH S6; Vortex is an intrinsic component"),
            "di-cyclone-strike-monk-base": ("di-launch-2022", "backfill-3 item 26: icy-veins June-2022 guide attests launch era"),
        }
        backfills_applied = 0
        for kid, (new_eras, note_src) in null_era_fills.items():
            row = cur.execute("SELECT eras FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()
            if row is None:
                raise RuntimeError(f"ERRATA-54 NULL-era backfill: {kid} not in canon_corpus")
            prior = row[0]
            if prior not in (None, ""):
                raise RuntimeError(f"ERRATA-54 backfill precondition: {kid} eras={prior!r} not NULL/empty — STOP")
            old_mn = cur.execute("SELECT mech_note FROM canon_corpus WHERE kit_id=?", (kid,)).fetchone()[0]
            bf_note = (f"{ANNOT_TAG} ERRATA-54 NULL-ERA BACKFILL: eras NULL -> {new_eras!r}. "
                       f"Source: {note_src}. _prior_ingest13 eras value was {prior!r} (empty). "
                       f"[original mech_note follows] {old_mn or ''}")
            guarded(cur, "UPDATE canon_corpus SET eras=? WHERE kit_id=? AND (eras IS NULL OR eras='')",
                    (new_eras, kid), f"{kid} eras null-backfill")
            guarded(cur, "UPDATE canon_corpus SET mech_note=? WHERE kit_id=? AND mech_note IS ?",
                    (bf_note, kid, old_mn), f"{kid} backfill annot")
            backfills_applied += 1
        if backfills_applied != 7:
            raise RuntimeError(f"ERRATA-54 NULL-era backfills: expected 7, got {backfills_applied}")
        print(f"P3i ERRATA-54: {backfills_applied} NULL-era backfills applied")

        # ---- ERRATA-55: Unattested Register annotations ----
        # d2-grim-ward-barb: PARTIAL (era C via backfill; identity + negative retry-exhausted U)
        prepend_annot(cur, "d2-grim-ward-barb",
            "ERRATA-55 UNATTESTED REGISTER (PARTIAL): era now CONFIRMED (backfill-3 item 2: Grim Ward lod "
            "skill-page). Identity + negative_canon are retry-exhausted UNSUPPORTED — 'Grim Ward Barbarian' "
            "as a standalone ARCHETYPE is unattested (builds mention Grim Ward as a component, not a headlining "
            "build identity). Stays Unattested Register partial recovery. Era: lod attested.",
            "d2-grim-ward-barb unattested register partial annot")

        # d2-wl-tainted-summoner folk-name unattested annotation
        prepend_annot(cur, "d2-wl-tainted-summoner",
            "ERRATA-55 UNATTESTED REGISTER (folk-name): 'Tainted Summoner' is NOT a named archetype in "
            "fetched maxroll/icy-veins/wl-build sources — maxroll's Summoner Warlock uses Goatman/Defiler framing. "
            "'Tainted Summoner' appears to be a kb-generated folk name, not an attested community term. "
            "Mechanics + era confirmed via Blood Boil guide; identity remains honest-U (folk-name unattested).",
            "d2-wl-tainted-summoner folk-name unattested annot")
        print("P3j ERRATA-55: grim-ward-barb partial register + tainted-summoner folk-name unattested annotations")

        # ---- Flag remaining CONTRADICTED verify rows ----
        # di-druid-bear mechanics X (b14)
        n_db = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='di-druid-bear' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        errata_flags += n_db

        # di-warlock-launch mechanics X (b15) — already flagged above via ERRATA-46
        # (n_wl already counted)

        # d3-spectral-blade + d3-wave-of-force negative_canon X — already flagged in ERRATA-43 (3a)

        # d4-incinerate + d4-kick + d4-wind-shear negative_canon X — already flagged in ERRATA-43 (3a)

        # d3-rathma-aotd mechanics X — flagged in ERRATA-51

        # d2-fishyzon mechanics X — flagged in ERRATA-51

        # d4-blazing-abyss-warlock mechanics X — flagged in ERRATA-51

        # d3-god-hungering identity X — flagged in ERRATA-52

        # di-tempest mechanics X — flagged in ERRATA-52

        # d4-lightning-spear mechanics X (backfill item 10 supersede) — verify flag
        n_ls_mech = cur.execute(
            "UPDATE verify_ledger SET errata_applied=1 "
            "WHERE kit_id='d4-lightning-spear' AND claim_family='mechanics' AND verdict='CONTRADICTED'",
            ()
        ).rowcount
        errata_flags += n_ls_mech

        print(f"P3 total errata_applied flags new: {errata_flags} (across all errata 43-55 families)")

        # ================= PART 4: whole-kit promotion gate =================
        # Same pattern as ingest-11. Use EFFECTIVE post-overlay verdict map.
        # Source of truth = files + backfill overlay.
        kit_fams = defaultdict(lambda: defaultdict(list))
        for b in batches:
            for r in verify_by_batch[b]:
                kid = r["kit_id"]
                v = VERDICT_MAP[r["verdict"]]
                kit_fams[kid][r["claim_family"]].append(v)

        # Apply backfill supersedes (22 in-place UPDATEs + 1 INSERT)
        for item_num, (kid, fam, direction) in SUPERSEDE_ITEMS.items():
            # Find the backfill row and apply its verdict
            bf_rows = [r for r in bf_by_item[item_num] if r["claim_family"] == fam]
            if bf_rows:
                new_v = VERDICT_MAP[bf_rows[0]["verdict"]]
                if fam in kit_fams[kid] and "UNSUPPORTED" in kit_fams[kid][fam]:
                    kit_fams[kid][fam] = [v for v in kit_fams[kid][fam] if v != "UNSUPPORTED"]
                    kit_fams[kid][fam].append(new_v)
        for kid, fam, direction in SUPERSEDE_ITEM_12 + SUPERSEDE_ITEM_23:
            bf_rows = [r for r in bf_by_item[12 if "andariel" in kid else 23] if r["claim_family"] == fam]
            if bf_rows:
                new_v = VERDICT_MAP[bf_rows[0]["verdict"]]
                if fam in kit_fams[kid] and "UNSUPPORTED" in kit_fams[kid][fam]:
                    kit_fams[kid][fam] = [v for v in kit_fams[kid][fam] if v != "UNSUPPORTED"]
                    kit_fams[kid][fam].append(new_v)
        # Item 26 INSERT: di-cyclone-strike-monk-base mechanics CONFIRMED
        kit_fams["di-cyclone-strike-monk-base"]["mechanics"].append("CONFIRMED")

        # Gate logic
        kit_flag_set = {"d2-wl-void-rift", "di-bombardment-wizard-pvp", "d4-spiritborn-vortex", "di-spiritform-druid-pvp"}
        gate_pass = []
        excl_contra = []
        excl_flag = []
        excl_mech = []
        excl_other = []

        for kid in sorted(kit_fams.keys()):
            fams = kit_fams[kid]
            has_contra = any("CONTRADICTED" in vs for vs in fams.values())
            mech_conf = "CONFIRMED" in fams.get("mechanics", [])
            id_conf = "CONFIRMED" in fams.get("identity", [])
            era_conf = "CONFIRMED" in fams.get("era", [])
            if kid in kit_flag_set:
                excl_flag.append(kid)
            elif has_contra:
                excl_contra.append(kid)
            elif mech_conf and id_conf and era_conf:
                gate_pass.append(kid)
            elif not mech_conf:
                excl_mech.append(kid)
            else:
                excl_other.append(kid)

        total_check = len(gate_pass) + len(excl_contra) + len(excl_flag) + len(excl_mech) + len(excl_other)
        if total_check != EXP_KIT_COUNT:
            raise RuntimeError(f"P4 census {total_check} != {EXP_KIT_COUNT} (gate_pass={len(gate_pass)} "
                               f"contra={len(excl_contra)} flag={len(excl_flag)} mech_nc={len(excl_mech)} "
                               f"other={len(excl_other)})")

        # Promote: gate_pass kits with probe facts, flipping kb-legacy/named-source-unfetched -> verified-v1.1
        # EXCLUDE di resource (economy family) from promotion for di kits (per Part 3.2 di resource sweep)
        promoted_facts = 0
        promoted_kits = []
        zero_fact_kits = []
        for k in gate_pass:
            n_probes = cur.execute("SELECT COUNT(*) FROM canon_probe_facts WHERE kit_id=?", (k,)).fetchone()[0]
            if n_probes == 0:
                zero_fact_kits.append(k)
                continue
            # For di kits: promote all families EXCEPT economy (ERRATA-44 sweep flagged them unreliable)
            if k.startswith("di-"):
                cur.execute(
                    "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                    "WHERE kit_id=? AND family != 'economy' "
                    "AND fact_provenance IN ('kb-legacy','named-source-unfetched')", (k,))
            else:
                cur.execute(
                    "UPDATE canon_probe_facts SET fact_provenance='verified-v1.1' "
                    "WHERE kit_id=? AND fact_provenance IN ('kb-legacy','named-source-unfetched')", (k,))
            promoted_facts += cur.rowcount
            promoted_kits.append(k)

        print(f"P4 promotion: {len(promoted_kits)} kits / {promoted_facts} facts promoted to verified-v1.1")
        print(f"   excl_contra={len(excl_contra)} excl_flag={len(excl_flag)} excl_mech={len(excl_mech)} "
              f"excl_other={len(excl_other)} zero_fact={len(zero_fact_kits)}")
        print(f"   zero_fact kits: {sorted(zero_fact_kits)}")

        # ================= integrity gates before COMMIT =================
        ic = cur.execute("PRAGMA integrity_check").fetchone()[0]
        if ic != "ok":
            raise RuntimeError(f"integrity_check = {ic}")
        fkc = cur.execute("PRAGMA foreign_key_check").fetchall()
        if fkc:
            raise RuntimeError(f"foreign_key_check not clean: {fkc[:5]}")

        cur.execute("COMMIT")
        print("\nCOMMIT complete.")

    except Exception as e:
        cur.execute("ROLLBACK")
        conn.close()
        die(f"WRITE aborted, rolled back: {e}")

    # ================= POST-WRITE verification (readonly re-query) =================
    vl_f  = cur.execute("SELECT COUNT(*) FROM verify_ledger").fetchone()[0]
    kc_f  = cur.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    kd_f  = cur.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    quar  = cur.execute("SELECT COUNT(*) FROM kit_citations WHERE quarantined=1").fetchone()[0]
    abst  = cur.execute("SELECT COUNT(*) FROM kit_dossier WHERE abstained=1").fetchone()[0]
    ea_tot = cur.execute("SELECT COUNT(*) FROM verify_ledger WHERE errata_applied=1").fetchone()[0]
    prov  = dict(cur.execute(
        "SELECT fact_provenance, COUNT(*) FROM canon_probe_facts GROUP BY fact_provenance"
    ).fetchall())
    b3_hist_final = dict(cur.execute(
        f"SELECT verdict, COUNT(*) FROM verify_ledger WHERE kit_id IN ({qk2}) GROUP BY verdict",
        basin3_kits
    ).fetchall())
    jm_f  = cur.execute("PRAGMA journal_mode").fetchone()[0]
    ic_f  = cur.execute("PRAGMA integrity_check").fetchone()[0]

    conn.close()

    print("\n===== INGEST-13 POST-WRITE =====")
    print(f"verify_ledger:   {vl0} -> {vl_f}  (Δ +{vl_f - vl0}, expected +681 = 1512)")
    print(f"kit_citations:   {kc0} -> {kc_f}  (Δ +{kc_f - kc0})")
    print(f"kit_dossier:     {kd0} -> {kd_f}  (Δ +{kd_f - kd0}, expected +1074 = 2394)")
    print(f"quarantined cit: {quar}  (8 basin-3: 4 batch + backfill)")
    print(f"abstained dossier: {abst}")
    print(f"errata_applied=1: {ea_tot}  (was {35} pre-ingest)")
    print(f"basin-3 verify histogram: {b3_hist_final}  (expected C=576 U=85 X=19 SNF=1)")
    print(f"fact_provenance: {prov}")
    print(f"journal_mode={jm_f}  integrity_check={ic_f}")
    print(f"P4 census: {len(gate_pass)} promoted kits / {promoted_facts} facts  |  "
          f"contra={len(excl_contra)} flag={len(excl_flag)} mech_nc={len(excl_mech)} "
          f"other={len(excl_other)} zero_fact={len(zero_fact_kits)}")
    print("\nAssertions:")
    print(f"  vl_f == 1512: {vl_f == 1512}")
    print(f"  kd_f == 2394: {kd_f == 2394}")
    print(f"  b3_hist == exp: {b3_hist_final == {'CONFIRMED':573,'UNSUPPORTED':89,'CONTRADICTED':18,'SOURCE_NOT_FOUND':1}}")
    print(f"  census sum == 179: {len(gate_pass)+len(excl_contra)+len(excl_flag)+len(excl_mech)+len(excl_other) == 179}")


if __name__ == "__main__":
    main()
