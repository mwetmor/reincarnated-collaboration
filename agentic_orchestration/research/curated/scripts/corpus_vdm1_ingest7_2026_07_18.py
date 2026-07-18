#!/usr/bin/env python3
"""
VDM-1 ingest wave 7 — D-5 poedb backfill FILL-ONLY merge (capstone/item enrichment).

Elrond (data steward, SINGLE WRITER of corpus.db).

The smallest, mechanically-simplest ingest of the run. The D-5 poedb sweep
backfilled the two structurally-sparse dossier families (capstone_alterations,
item_alterations) for PoE1; gandalf steward-repaired its schema deviations
(abstained rows strictly null-payload/null-conf; conf as numeric 0.9/0.75/0.5)
before handing it to this ingest. See the STEWARD AUDIT + REPAIR ADDENDUM at the
bottom of backfill-capstone-items-summary.md.

Follows the ingest-4/ingest-6 procedure exactly (load_jsonl parse-validation;
short single BEGIN IMMEDIATE..COMMIT txn; connect_with_retry index.lock wrapper
wait-30s-retry-3x; journal_mode kept DELETE for concurrent readonly crawlers).

THE FILL-ONLY LAW (binding, from the summary addendum):
  A backfill dossier row may LAND only where the existing stage-1 kit_dossier row
  for that (kit_id, family) is abstained -- or absent entirely. NEVER overwrite a
  non-abstained stage-1 row (stage-1 guide-tier fills are primary; this sweep is
  enrichment). Backfill rows that are THEMSELVES abstained (the 8) do NOT land at
  all -- the stage-1 abstention already records the silence; skip + count them as
  skipped-abstained.

Dossier landing paths (per non-abstained backfill row, keyed by (kit_id, family)):
  - existing row abstained=1  -> UPDATE IN PLACE (flip): set payload_json,
      source_url, anchor_quote, abstained=0, conf, extraction_provenance.
      GUARDED `AND abstained=1` so a non-abstained (primary) row can NEVER be
      clobbered even if the (kit,fam) key were reused -- belt+braces on the law.
  - existing row absent        -> INSERT.
  - existing row non-abstained -> SKIP + count (report). (Fill ceiling note from the
      addendum: expected 0 here for PoE1 -- verified in dry-run: all 94 kits carry
      stage-1 ABSTAINED rows for BOTH families, incl. poe1-incinerate item_alterations,
      so every one of the 86 non-abstained backfill rows is a FLIP; 0 inserts, 0 skips.)

Provenance stamp: extraction_provenance = 'd5-backfill' (the D-5 sweep is a distinct
enrichment source vs the stage-1 'fetched-vdm1' guide-tier fills; stamping it lets a
reader partition guide-tier from catalogue-backfill provenance). NOTE: this is the
FIRST use of a non-default extraction_provenance value in kit_dossier (ingests 1-6
all landed 'fetched-vdm1', the column default). No schema change -- the column
already accepts arbitrary TEXT.

CITATIONS (66 rows). Structural note: the D-5 crawl was SKILL-batched, not
kit-batched, so its citation file is URL-keyed and carries NO kit_id -- unlike the
stage-1 batch citation files (ingest-4) which carried an explicit per-row kit_id.
kit_citations requires kit_id NOT NULL with UNIQUE(kit_id, url), so each citation's
kit_id is DERIVED deterministically (no fabrication -- every derivation traces to a
dossier row or a payload-subject match, logged below):
  PRIMARY  : url == a NON-abstained backfill dossier row's source_url -> that row's
             kit_id(s). 4 URLs fan to 2 kits (shared core skill across kits); each
             fanned kit is cited (page-provenance-per-kit, matching how stage-1
             recorded the same shared pages).
  SECONDARY: 8 URLs are supporting/cross-reference pages (a unique-item page, a
             keystone page, a co-skill page) fetched WHILE building another kit's
             dossier; they are not any row's primary source_url. Mapped by
             payload-subject match to the owning kit (SECONDARY_KIT below).
Dedupe discipline (same as the UNIQUE(kit,url) contract honored across ingests):
  skip any (kit_id, url) already in kit_citations; skip within-batch dupes; count both.
  Dry-run: 16 new (kit,url) pairs land; 54 dedupe vs existing (these poedb pages were
  already cited in stage-1 under the SAME derived kits -- strong cross-validation of
  the derivation); 0 within-batch; 0 orphans (every citation resolves to a real
  canon_corpus kit).
cite_class: input carries class='communal' (all 66) -> kit_citations.cite_class
  'communal' (in the CHECK enum). rank_class: 'attested-era' (these are live poedb
  pages fetched THIS wave with a 2026-07-18 access_date -- current attestation, not a
  recovered Wayback snapshot). archive_url <- input 'snapshot' (all null). quarantined=0.

Charter laws honored (unchanged from ingest-4/6):
  - No silent transformation: every kit_id DERIVATION for a citation is logged; every
    dossier landing decision (flip/insert/skip) is logged; no raw datum dropped.
  - No-fabrication: abstained backfill rows (8) do NOT land; abstained kit_dossier
    rows keep payload NULL (DB CHECK). Fill-only law guards every write.
  - Reversible: raw JSONL inputs committed + static; reproducible against the
    pre-ingest7 backup.
  - journal_mode stays DELETE. Short write txn; index.lock retry on the write handle.

Usage:
  python3 corpus_vdm1_ingest7_2026_07_18.py           # dry-run (validate + report, no writes)
  python3 corpus_vdm1_ingest7_2026_07_18.py --apply   # execute the single write txn
"""
import argparse
import json
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/admin/Games/reincarnated-collaboration")
DB = REPO / "agentic_orchestration/research/curated/corpus.db"
S1 = REPO / "agentic_orchestration/research/vdm1/stage1/poe1"
DOSS_F = S1 / "backfill-capstone-items-dossier.jsonl"
CIT_F = S1 / "backfill-capstone-items-citations.jsonl"

PROVENANCE = "d5-backfill"
TARGET_FAMILIES = {"capstone_alterations", "item_alterations"}
DOSSIER_FAMILY = {"skill_loop", "skill_geometry", "item_alterations",
                  "capstone_alterations", "author_credit", "variants"}

# Secondary (supporting/cross-reference) citation pages -> owning kit. Derived by
# payload-subject match (each page's subject appears in exactly this kit's payload;
# HoAG's Cyclone+Herald_of_Agony pair per the crawl notes "Cyclone ... used as HoAG
# poison applier"). Minion_Instability is a keystone shared by golementalist+srs;
# attributed to poe1-srs (SRS is the Minion-Instability archetype). Deterministic,
# audited against the DB in dry-run (3 of these 8 already exist in kit_citations
# under exactly these kits -> confirms the mapping).
SECONDARY_KIT = {
    "https://poedb.tw/unique.php?n=Mjölner": "poe1-mjolner",
    "https://poedb.tw/us/Ancestral_Bond": "poe1-pizza-sticks",
    "https://poedb.tw/us/Cyclone": "poe1-hoag",
    "https://poedb.tw/us/Earthshatter_of_Prominence": "poe1-earthshatter",
    "https://poedb.tw/us/Herald_of_Agony": "poe1-hoag",
    "https://poedb.tw/us/Minion_Instability": "poe1-srs",
    "https://poedb.tw/us/Sweep": "poe1-sweep",
    "https://poedb.tw/us/Volatile_Dead": "poe1-poets-pen-vd",
}


def load_jsonl(path):
    rows = []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rows.append((ln, json.loads(line)))   # raises on malformed line (defect-repair validation)
    return rows


def connect_with_retry(path, attempts=3, wait=30):
    """Open the write connection; on a locked DB (index.lock / 'database is locked')
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

    doss = load_jsonl(DOSS_F)
    cits = load_jsonl(CIT_F)

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.execute("PRAGMA foreign_keys=ON;")

    dbkits = set(r[0] for r in con.execute("SELECT kit_id FROM canon_corpus"))
    # current (kit,family) -> abstained state
    cur_state = {}
    for k, f, a in con.execute("SELECT kit_id, family, abstained FROM kit_dossier"):
        cur_state[(k, f)] = a
    # guard: exactly one dossier row per (kit,family) in the target families for PoE1
    dup = con.execute(
        "SELECT kit_id, family, COUNT(*) c FROM kit_dossier "
        "WHERE kit_id LIKE 'poe1-%' AND family IN ('capstone_alterations','item_alterations') "
        "GROUP BY kit_id, family HAVING c > 1").fetchall()
    assert not dup, f"multi-row (kit,family) among target families -> UNIQUE risk: {dup}"
    pre_kd = con.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    pre_kc = con.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    pre_abst_cap = con.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='capstone_alterations' "
        "AND kit_id LIKE 'poe1-%' AND abstained=1").fetchone()[0]
    pre_abst_item = con.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='item_alterations' "
        "AND kit_id LIKE 'poe1-%' AND abstained=1").fetchone()[0]
    pre_tot_cap = con.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='capstone_alterations' "
        "AND kit_id LIKE 'poe1-%'").fetchone()[0]
    pre_tot_item = con.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='item_alterations' "
        "AND kit_id LIKE 'poe1-%'").fetchone()[0]

    # ---- DOSSIER: classify each backfill row under the FILL-ONLY LAW ----
    flips, inserts, skips_nonabst, skips_abst = [], [], [], []
    fam_stat = defaultdict(lambda: {"flip": 0, "insert": 0, "skip_nonabst": 0, "skip_abst": 0})
    for ln, o in doss:
        k = o.get("kit_id"); f = o.get("family"); abst = o.get("abstained")
        assert f in DOSSIER_FAMILY, f"line {ln}: family {f!r} not in enum"
        assert f in TARGET_FAMILIES, f"line {ln}: unexpected family {f!r} in a capstone/item backfill"
        assert k in dbkits, f"line {ln}: kit {k!r} absent from canon_corpus"
        assert abst in (0, 1), f"line {ln}: abstained {abst!r} not 0/1"
        if abst == 1:
            # abstained backfill row: DOES NOT LAND (no-fabrication; stage-1 silence already recorded)
            assert o.get("payload_json") is None, \
                f"line {ln}: abstained backfill row {k}/{f} carries non-null payload (steward-repair expected null)"
            assert o.get("conf") is None, \
                f"line {ln}: abstained backfill row {k}/{f} carries non-null conf (steward-repair expected null)"
            skips_abst.append((k, f)); fam_stat[f]["skip_abst"] += 1
            continue
        # non-abstained backfill row -> subject to fill-only landing
        payload = o.get("payload_json")
        assert payload is not None, f"line {ln}: non-abstained row {k}/{f} has null payload"
        conf = o.get("conf")
        assert isinstance(conf, (int, float)), \
            f"line {ln}: conf {conf!r} not numeric (steward-repair maps provenance-tags -> float)"
        payload_str = json.dumps(payload, ensure_ascii=False)
        rec = (k, f, payload_str, o.get("source_url"), o.get("anchor_quote"), conf)
        st = cur_state.get((k, f))
        if st == 1:
            flips.append(rec); fam_stat[f]["flip"] += 1
        elif st is None:
            inserts.append(rec); fam_stat[f]["insert"] += 1
        else:  # st == 0 -> existing non-abstained -> FILL-ONLY LAW: SKIP
            skips_nonabst.append((k, f)); fam_stat[f]["skip_nonabst"] += 1

    # ---- CITATIONS: derive kit_id, dedupe ----
    url2kit_primary = defaultdict(set)
    for _, o in doss:
        if o.get("abstained") == 0 and o.get("source_url"):
            url2kit_primary[o["source_url"]].add(o["kit_id"])
    existing_cit = set((k, u) for k, u in con.execute("SELECT kit_id, url FROM kit_citations"))
    con.close()

    cite_ins = []
    cit_dedup_existing = cit_dedup_within = cit_orphan = 0
    cit_derivation = []   # (url, kit, PRIMARY|SECONDARY) for the log
    seen_batch = set()
    for ln, o in cits:
        u = o.get("url")
        assert u, f"citation line {ln}: null url"
        if u in url2kit_primary:
            kits = sorted(url2kit_primary[u]); how = "PRIMARY"
        elif u in SECONDARY_KIT:
            kits = [SECONDARY_KIT[u]]; how = "SECONDARY"
        else:
            cit_orphan += 1
            print(f"   CIT ORPHAN line {ln}: {u} -> no kit (UNMAPPED)")
            continue
        for k in kits:
            if k not in dbkits:
                cit_orphan += 1; continue
            cit_derivation.append((u, k, how))
            if (k, u) in existing_cit:
                cit_dedup_existing += 1; continue
            if (k, u) in seen_batch:
                cit_dedup_within += 1; continue
            seen_batch.add((k, u))
            # class -> cite_class ; rank_class attested-era (live 2026-07-18 fetch)
            cc = o.get("class")
            assert cc == "communal", f"citation line {ln}: unexpected class {cc!r}"
            cite_ins.append((k, u, o.get("snapshot"), o.get("site"),
                             o.get("author_handle"), None, "communal", "attested-era",
                             o.get("access_date"), 0))

    # ---- report ----
    tot_flip = sum(v["flip"] for v in fam_stat.values())
    tot_ins = sum(v["insert"] for v in fam_stat.values())
    tot_sk_non = sum(v["skip_nonabst"] for v in fam_stat.values())
    tot_sk_abst = sum(v["skip_abst"] for v in fam_stat.values())
    print("=== VDM-1 ingest wave 7 (%s) — D-5 backfill fill-only merge ===" %
          ("APPLY" if args.apply else "DRY-RUN"))
    for f in ("capstone_alterations", "item_alterations"):
        s = fam_stat[f]
        print(f"  {f}: flip(abst->fill)={s['flip']}  insert-new={s['insert']}  "
              f"skip-non-abstained={s['skip_nonabst']}  skip-abstained={s['skip_abst']}")
    print(f"  TOTALS: flip={tot_flip} insert={tot_ins} skip_nonabst={tot_sk_non} skip_abstained={tot_sk_abst}")
    print(f"  kit_dossier row-count delta (inserts only) = {tot_ins}")
    print(f"  citations: input=66  new-land={len(cite_ins)}  "
          f"dedup-existing={cit_dedup_existing}  dedup-within={cit_dedup_within}  orphan={cit_orphan}")
    print(f"  citation kits touched: {len(set(k for k, _, _, _, _, _, _, _, _, _ in cite_ins))}")
    # abstention-rate before (informational; after computed post-write for APPLY)
    print(f"  capstone_alterations PoE1 abstention BEFORE: {pre_abst_cap}/{pre_tot_cap}")
    print(f"  item_alterations     PoE1 abstention BEFORE: {pre_abst_item}/{pre_tot_item}")

    # ---- pre-write asserts (dispatch file truths + THE FILL-ONLY LAW) ----
    assert tot_flip + tot_ins + tot_sk_non == 86, \
        f"flip+insert+skip_nonabst = {tot_flip+tot_ins+tot_sk_non} != 86"
    assert tot_sk_abst == 8, f"skip_abstained = {tot_sk_abst} != 8 (the 8 abstained backfill rows)"
    assert fam_stat["capstone_alterations"]["flip"] + fam_stat["capstone_alterations"]["insert"] + \
        fam_stat["capstone_alterations"]["skip_nonabst"] == 57, "capstone non-abstained backfill != 57"
    assert fam_stat["item_alterations"]["flip"] + fam_stat["item_alterations"]["insert"] + \
        fam_stat["item_alterations"]["skip_nonabst"] == 29, "item non-abstained backfill != 29"
    assert cit_orphan == 0, f"{cit_orphan} citation(s) unmapped to any kit"
    # every flip target is currently abstained (fill-only law, verified pre-write)
    for k, f, *_ in flips:
        assert cur_state.get((k, f)) == 1, f"flip target {k}/{f} not abstained pre-write"

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to write.")
        return

    # ---------- single short write txn (write handle with index.lock retry) ----------
    wcon = connect_with_retry(DB)
    try:
        wcon.execute("BEGIN IMMEDIATE;")
        # FLIP: in-place UPDATE, GUARDED to abstained=1 rows only (fill-only law).
        n_flipped = 0
        for k, f, payload_str, src, anchor, conf in flips:
            c = wcon.execute(
                "UPDATE kit_dossier SET payload_json=?, source_url=?, anchor_quote=?, "
                "abstained=0, conf=?, extraction_provenance=? "
                "WHERE kit_id=? AND family=? AND abstained=1",
                (payload_str, src, anchor, conf, PROVENANCE, k, f))
            assert c.rowcount == 1, f"flip {k}/{f} hit {c.rowcount} rows (expected 1, guarded abstained=1)"
            n_flipped += 1
        # INSERT new (kit,fam) rows (none expected for PoE1)
        if inserts:
            wcon.executemany(
                "INSERT INTO kit_dossier "
                "(kit_id, family, payload_json, source_url, anchor_quote, abstained, conf, extraction_provenance) "
                "VALUES (?,?,?,?,?,0,?,?)",
                [(k, f, p, s, a, c, PROVENANCE) for (k, f, p, s, a, c) in inserts])
        # CITATIONS
        if cite_ins:
            wcon.executemany(
                "INSERT INTO kit_citations "
                "(kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)", cite_ins)
        wcon.commit()
    except Exception:
        wcon.rollback()
        raise

    # ---------- POST-write asserts ----------
    post_kd = wcon.execute("SELECT COUNT(*) FROM kit_dossier").fetchone()[0]
    post_kc = wcon.execute("SELECT COUNT(*) FROM kit_citations").fetchone()[0]
    post_abst_cap = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='capstone_alterations' "
        "AND kit_id LIKE 'poe1-%' AND abstained=1").fetchone()[0]
    post_abst_item = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE family='item_alterations' "
        "AND kit_id LIKE 'poe1-%' AND abstained=1").fetchone()[0]
    d5_rows = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE extraction_provenance='d5-backfill'").fetchone()[0]
    abst_bad = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE abstained=1 AND payload_json IS NOT NULL").fetchone()[0]
    fill_bad = wcon.execute(
        "SELECT COUNT(*) FROM kit_dossier WHERE abstained=0 AND payload_json IS NULL").fetchone()[0]
    orph_kc = wcon.execute("SELECT COUNT(*) FROM kit_citations kc WHERE NOT EXISTS "
                           "(SELECT 1 FROM canon_corpus c WHERE c.kit_id=kc.kit_id)").fetchone()[0]
    jm = wcon.execute("PRAGMA journal_mode;").fetchone()[0]
    ic = wcon.execute("PRAGMA integrity_check;").fetchone()[0]
    fk = wcon.execute("PRAGMA foreign_key_check;").fetchall()

    # kit_dossier count changes by inserts ONLY (flips are in-place UPDATEs)
    assert post_kd == pre_kd + tot_ins, f"kit_dossier {post_kd} != {pre_kd}+{tot_ins} (inserts only)"
    assert post_kc == pre_kc + len(cite_ins), f"kit_citations {post_kc} != {pre_kc}+{len(cite_ins)}"
    assert n_flipped == tot_flip == 86, f"flipped {n_flipped} != 86"
    # abstention drops by exactly the flips per family
    assert post_abst_cap == pre_abst_cap - fam_stat["capstone_alterations"]["flip"], "capstone abstention delta"
    assert post_abst_item == pre_abst_item - fam_stat["item_alterations"]["flip"], "item abstention delta"
    assert d5_rows == 86, f"d5-backfill provenance rows {d5_rows} != 86"
    assert abst_bad == 0, "abstained row carries non-null payload"
    assert fill_bad == 0, "filled (abstained=0) row carries NULL payload"
    assert orph_kc == 0, "citation orphan (kit absent from canon_corpus)"
    assert jm == "delete", f"journal_mode {jm} != delete"
    assert ic == "ok", f"integrity_check {ic}"
    assert fk == [], f"foreign_key_check {fk}"

    print("\n=== APPLIED ===")
    print(f"kit_dossier   {pre_kd} -> {post_kd}  (+{post_kd-pre_kd}; inserts only)")
    print(f"kit_citations {pre_kc} -> {post_kc}  (+{post_kc-pre_kc})")
    print(f"flipped abstained->filled: {n_flipped}  (d5-backfill provenance rows: {d5_rows})")
    print(f"capstone_alterations PoE1 abstention: {pre_abst_cap}/{pre_tot_cap} -> {post_abst_cap}/{pre_tot_cap}")
    print(f"item_alterations     PoE1 abstention: {pre_abst_item}/{pre_tot_item} -> {post_abst_item}/{pre_tot_item}")
    print(f"journal_mode: {jm} | integrity_check: {ic} | foreign_key_check: {fk}")
    wcon.close()


if __name__ == "__main__":
    sys.exit(main())
