#!/usr/bin/env python3
"""
corpus_js4b_agreement_tolerance_rerun_2026_10_06.py -- JOIN-1 B0-N finding: re-run the J-S4b pack agreement
check under a DECLARED tolerance policy, and refresh the referent export + manifest after the rule stamping.

Owner: elrond. Conductor: gandalf (KP-304 finding routed to elrond; KP-305 routing).

THE FINDING (KP-304). The 2026-10-02 mint (corpus_js4b_referent_mint_2026_10_02.py) marked S13-SF-PERIOD
"agree" for soulfire_period_s at 0.2 against the pack's 0.20000000298023224 with no declared tolerance. Two
undeclared mechanisms were at work, not one:
    (M1) close() compared with math.isclose(rel_tol=1e-6, abs_tol=1e-6) -- a tolerance named nowhere on the face;
    (M2) the PACK value of S13-SF-PERIOD was passed through f32() (7-significant-digit presentation) BEFORE the
         comparison, so the export and the corpus source_anchor print the pack value as 0.2 -- a silent
         transformation of the comparand, not just a loose comparison.

THE POLICY (declared here, named on the face of every check as `tolerance_policy`):
    AGREE-TOL-v1
      EXACT           record == pack as IEEE-754 binary64 values, as read. No rounding of either side.
      F32-SAME-DATUM  not EXACT, but (a) at least one side is EXACTLY a binary32 value widened to binary64
                      (struct '<f' round-trip is bit-identical), and (b) both sides round to the IDENTICAL
                      binary32 bit pattern. I.e. the two numbers are two representations of ONE float32 datum
                      (the store's widened form vs its shortest decimal). This is not a numeric tolerance: it
                      admits at most half a float32 ulp, and only where one side is provably float32-origin.
      DISAGREE        anything else. There is no other tolerance.
    Pack values are read RAW (no f32 presentation): the mint's build() is run a second time with f32 = identity
    and the pack side is taken from that run; the record side is the corpus source_value (asserted bit-equal
    to the first run's record value for all 104 rows).

READ-ONLY on corpus.db. Writes kits-export/gd-eor-warlord-referent.json and its manifest.

USAGE
    python3 corpus_js4b_agreement_tolerance_rerun_2026_10_06.py            # report only
    python3 corpus_js4b_agreement_tolerance_rerun_2026_10_06.py --write    # report + rewrite export + manifest
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sqlite3
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import corpus_js4b_referent_mint_2026_10_02 as MINT  # noqa: E402  (read-only: load_sources / build / anchor / rowset)

DB = MINT.DB
KIT = MINT.KIT
EXPORT = MINT.EXPORT_DIR / f"{KIT}.json"
MANIFEST = MINT.EXPORT_DIR / f"{KIT}.manifest.json"
APPLY_SCRIPT = HERE / "corpus_js4b_rule_stamping_apply_2026_10_06.py"
PKG = MINT.COLLAB / "agentic_orchestration/gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin/stamping"
FILE_EXPECT = "639acb2033e09b522793e1138a36c9144dc23af05be0ebe6944955fd4a9432ea"
FILE_PRE = "0d73475aea0f5f290a754a501e58d83af06958259fae4621317320f0fb285d07"
BACKUP = "corpus.db.pre-js4b-stamping-20261006T231654Z-backup"
ROWSET_EXPECT = "c3e0f121d2a7f44cc17c72107bd31db1bdf489f146a68898b3971b69b6c01597"
PROVISIONAL = "PROVISIONAL: R-CTX-GEO scope amendment ACCEPTED PROVISIONALLY (conductor KP-304), pending jack-ryan JOIN-1 B0-N Gate-2; revert sets rdr_value/rule_id/rule_version_applied to NULL"

POLICY = {
    "id": "AGREE-TOL-v1",
    "declared": "2026-10-06 (elrond; occasioned by gamora KP-304 finding, conductor routing KP-305)",
    "classes": {
        "EXACT": "record == pack as IEEE-754 binary64 values, as read; no rounding of either side",
        "F32-SAME-DATUM": "not EXACT; at least one side is exactly a binary32 value widened to binary64, and both sides round "
                          "to the identical binary32 bit pattern -- two representations of ONE float32 datum (widened vs "
                          "shortest-decimal). Admits at most half a float32 ulp, only where one side is provably float32-origin.",
        "DISAGREE": "anything else; no other tolerance exists",
    },
    "agree_means": "class in {EXACT, F32-SAME-DATUM}",
    "pack_values": "read raw (no f32 presentation rounding of the comparand)",
    "supersedes": "the 2026-10-02 mint check: math.isclose(rel_tol=1e-6, abs_tol=1e-6) (undeclared) + f32() applied to the "
                  "S13-SF-PERIOD pack value before comparison (undeclared transformation of the comparand)",
}


def f32_bits(x: float) -> int:
    return struct.unpack("<I", struct.pack("<f", x))[0]


def is_f32_exact(x: float) -> bool:
    return struct.unpack("<f", struct.pack("<f", x))[0] == x


def classify(rec: float, pack: float) -> str:
    a, b = float(rec), float(pack)
    if a == b:
        return "EXACT"
    try:
        if (is_f32_exact(a) or is_f32_exact(b)) and f32_bits(a) == f32_bits(b):
            return "F32-SAME-DATUM"
    except (OverflowError, struct.error):
        pass
    return "DISAGREE"


def sha_file(p):
    return MINT.sha_file(pathlib.Path(p))


def main(write: bool):
    assert sha_file(DB) == FILE_EXPECT, "corpus.db is not the post-stamping FILE"
    src = MINT.load_sources()                       # asserts pack digest of record + save digest
    rows_a = MINT.build(src)                        # as minted (record side)
    real_f32 = MINT.f32
    MINT.f32 = lambda x: float(x)                   # raw run: pack side without presentation rounding
    try:
        rows_b = MINT.build(src)
    finally:
        MINT.f32 = real_f32
    old, _ = MINT.agreement(copy.deepcopy(rows_a))  # the 2026-10-02 classification, reproduced

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    corpus = {r["numeric_key"]: dict(r) for r in con.execute("SELECT * FROM kit_numeric WHERE kit_id=?", (KIT,))}
    rs = MINT.rowset(con, KIT)
    con.close()
    assert rs[0] == ROWSET_EXPECT, rs[0]
    assert [r["numeric_key"] for r in rows_a] == [r["numeric_key"] for r in rows_b] and set(corpus) == {r["numeric_key"] for r in rows_a}
    # the re-run reads the same inputs as the mint: record values AND anchors reproduce the corpus bit-for-bit
    for r in old:
        c = corpus[r["numeric_key"]]
        assert struct.pack("<d", r["value"]) == struct.pack("<d", c["source_value"]), r["numeric_key"]
        assert MINT.anchor(r) == c["source_anchor"], f"anchor drift {r['numeric_key']}"

    by_b = {r["numeric_key"]: r for r in rows_b}
    new_rows, reclass, comparand_fixes, dis = [], [], [], []
    tally = {"EXACT": 0, "F32-SAME-DATUM": 0, "DISAGREE": 0}
    for r in old:
        b = by_b[r["numeric_key"]]
        raw_checks = ([b["pack"]] if b["pack"] else []) + b["pack_alt"]
        assert len(raw_checks) == len(r["checks"])
        checks = []
        for oc, (rid, pv_raw) in zip(r["checks"], raw_checks):
            assert oc["pack_row"] == rid
            cls = classify(r["value"], pv_raw)
            tally[cls] += 1
            agree = cls != "DISAGREE"
            ch = {"pack_row": rid, "pack_value": pv_raw, "class": cls, "agree": agree,
                  "tolerance_policy": POLICY["id"], "agree_2026_10_02": oc["agree"]}
            if struct.pack("<d", float(oc["pack_value"])) != struct.pack("<d", float(pv_raw)):
                ch["pack_value_as_printed_2026_10_02"] = oc["pack_value"]
                comparand_fixes.append({"numeric_key": r["numeric_key"], "pack_row": rid,
                                        "printed_2026_10_02": oc["pack_value"], "raw_pack_value": pv_raw})
            if (oc["agree"] and cls != "EXACT") or (agree != oc["agree"]):
                reclass.append({"numeric_key": r["numeric_key"], "record_value": r["value"], "pack_row": rid,
                                "pack_value_raw": pv_raw, "was": "agree" if oc["agree"] else "disagree",
                                "was_basis": "math.isclose rel/abs 1e-6 (undeclared)" +
                                             (" on an f32-presented comparand" if "pack_value_as_printed_2026_10_02" in ch else ""),
                                "now": cls, "now_agree": agree,
                                "record_f32_exact": is_f32_exact(r["value"]), "pack_f32_exact": is_f32_exact(float(pv_raw)),
                                "f32_bits_record": f"0x{f32_bits(r['value']):08X}", "f32_bits_pack": f"0x{f32_bits(float(pv_raw)):08X}"})
            if not agree:
                dis.append({"numeric_key": r["numeric_key"], "record_value": r["value"], "pack_row": rid,
                            "pack_value": pv_raw, "class": cls, "note": r.get("note")})
            checks.append(ch)
        new_rows.append({"numeric_key": r["numeric_key"], "checks": checks})

    n_cmp = sum(1 for r in new_rows if r["checks"])
    n_ok = sum(1 for r in new_rows if r["checks"] and all(c["agree"] for c in r["checks"]))
    n_exact_rows = sum(1 for r in new_rows if r["checks"] and all(c["class"] == "EXACT" for c in r["checks"]))
    n_old_ok = sum(1 for r in old if r["checks"] and all(c["agree"] for c in r["checks"]))
    n_old_dis = sum(1 for r in old for c in r["checks"] if not c["agree"])
    report = {"policy": POLICY["id"], "checks_by_class": tally, "rows_compared": n_cmp, "rows_all_agree": n_ok,
              "rows_all_exact": n_exact_rows, "rows_all_agree_2026_10_02": n_old_ok,
              "disagreeing_checks": len(dis), "disagreeing_checks_2026_10_02": n_old_dis,
              "reclassified_checks": reclass, "comparand_fixes": comparand_fixes}
    print(json.dumps(report, indent=1))
    if not write:
        return report

    # ------------------------------------------------------------------ export
    ex = json.loads(EXPORT.read_text())
    export_sha_at_mint = sha_file(EXPORT)
    nc = {r["numeric_key"]: r for r in new_rows}
    for n in ex["numeric"]:
        c = corpus[n["numeric_key"]]
        n["pack_checks"] = nc[n["numeric_key"]]["checks"]
        n["rdr_value"] = c["rdr_value"]
        n["rule_id"] = c["rule_id"]
        n["rule_version_applied"] = c["rule_version_applied"]
        if c["rule_id"] == "R-CTX-GEO":
            n["rule_stamp_status"] = PROVISIONAL
        elif c["rule_id"] == "R-T2":
            n["rule_stamp_status"] = "STAMPED (R-T2 v1, IDENTITY; covers gd_seconds by its own Covers enumeration)"
        else:
            n["rule_stamp_status"] = "UNSTAMPED (NO-RULE; reason in gamora stamping_table.json)"
    ac = ex["agreement_check"]
    hist = {k: ac[k] for k in ("n_rows_all_checks_agree", "disagreements") if k in ac}
    hist["basis"] = POLICY["supersedes"]
    ac.update({"tolerance_policy": POLICY, "n_rows_compared_to_pack": n_cmp, "n_rows_all_checks_agree": n_ok,
               "n_rows_all_checks_exact": n_exact_rows, "checks_by_class": tally, "disagreements": dis,
               "reclassified_2026_10_06": reclass, "comparand_fixes_2026_10_06": comparand_fixes,
               "as_of_2026_10_02": hist,
               "corpus_source_anchor_note": "kit_numeric.source_anchor still carries the 2026-10-02 'AGREES/DISAGREES' text "
                                            "(and prints S13-SF-PERIOD's pack value as 0.2). It was NOT edited: any edit moves "
                                            "the J-S4b ROWSET off the pinned c3e0f121. This block is the classification of "
                                            "record; an anchor refresh awaits a conductor ruling."})
    ex["rule_stamping"] = {
        "applied": "2026-10-06", "by": "elrond (corpus.db steward)", "rule_owner": "gamora",
        "package": "agentic_orchestration/gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin/stamping/ (collab 9a90660f8)",
        "R-T2": sorted(k for k, c in corpus.items() if c["rule_id"] == "R-T2"),
        "R-CTX-GEO_provisional": sorted(k for k, c in corpus.items() if c["rule_id"] == "R-CTX-GEO"),
        "R-CTX-GEO_status": PROVISIONAL,
        "unstamped": sum(1 for c in corpus.values() if c["rule_id"] is None),
        "rdr_equals_source_on_every_stamped_row": all(c["rdr_value"] == c["source_value"] for c in corpus.values() if c["rule_id"]),
    }
    ex["unknowns"] = [u for u in ex["unknowns"] if not u["what"].startswith("rdr_value for every kit_numeric row")]
    ex["unknowns"].insert(0, {"what": "rdr_value for the 85 unstamped kit_numeric rows",
                              "settle": "the normalization-rule owner (gamora): no active rule covers their scales (gd_energy, "
                                        "gd_rank, gd_pct_sheet, gd_pct, gd_flat_damage, ...); per-row reasons in stamping_table.json"})
    ex["corpus_rowset"]["digest"] = rs[0]
    ex["corpus_rowset"]["row_counts"] = rs[1]
    ex["corpus_rowset"]["history"] = [{"date": "2026-10-02", "digest": MINT_ROWSET, "event": "mint"},
                                      {"date": "2026-10-06", "digest": rs[0], "event": "rule stamping (14 R-T2 + 5 R-CTX-GEO provisional)"}]
    EXPORT.write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
    export_sha = sha_file(EXPORT)

    # ------------------------------------------------------------------ manifest
    man = json.loads(MANIFEST.read_text())
    man["files"]["export"]["sha256_at_mint_2026_10_02"] = man["files"]["export"]["sha256"]
    assert man["files"]["export"]["sha256_at_mint_2026_10_02"] == export_sha_at_mint, "export changed since the mint manifest"
    man["files"]["export"]["sha256"] = export_sha
    man["rowsets"][KIT]["digest_at_mint_2026_10_02"] = man["rowsets"][KIT]["digest"]
    man["rowsets"][KIT]["digest"] = rs[0]
    man["corpus_db"]["current_FILE_sha256"] = FILE_EXPECT
    rev = {
        "date": "2026-10-06", "by": "elrond", "event": "J-S4b rule stamping applied + agreement check re-run under AGREE-TOL-v1",
        "corpus_db": {"pre_FILE_sha256": FILE_PRE, "post_FILE_sha256": FILE_EXPECT, "backup": BACKUP},
        "rowset": {"pre": MINT_ROWSET, "after_R-T2_only": "e53ff212ead3f130333115e9743000c41a8cdcd3223c5f24c7af5aa89b8d319f",
                   "post": rs[0]},
        "provisional_rows": sorted(k for k, c in corpus.items() if c["rule_id"] == "R-CTX-GEO"),
        "provisional_status": PROVISIONAL,
        "files": {
            "stamping_sql_R-T2": {"path": str(PKG / "corpus_js4b_rule_stamping_2026_10_06.sql"),
                                  "sha256": sha_file(PKG / "corpus_js4b_rule_stamping_2026_10_06.sql"), "kind": "FILE"},
            "stamping_sql_R-CTX-GEO_amendment": {"path": str(PKG / "corpus_js4b_rctxgeo_gd_metres_amendment_2026_10_06.sql"),
                                                 "sha256": sha_file(PKG / "corpus_js4b_rctxgeo_gd_metres_amendment_2026_10_06.sql"), "kind": "FILE"},
            "stamping_table": {"path": str(PKG / "stamping_table.json"), "sha256": sha_file(PKG / "stamping_table.json"), "kind": "FILE"},
            "apply_script": {"path": str(APPLY_SCRIPT), "sha256": sha_file(APPLY_SCRIPT), "kind": "FILE"},
            "tolerance_rerun_script": {"path": str(pathlib.Path(__file__).resolve()), "sha256": sha_file(__file__), "kind": "FILE"},
            "export": {"path": str(EXPORT), "sha256": export_sha, "kind": "FILE"},
        },
        "tolerance_policy": POLICY["id"],
        "reclassified_checks": len(reclass),
    }
    man.setdefault("revisions", []).append(rev)
    MANIFEST.write_text(json.dumps(man, indent=2) + "\n")
    print("export", EXPORT, export_sha)
    print("manifest", MANIFEST, sha_file(MANIFEST))
    return report


MINT_ROWSET = "66250f2d138be8b13e780c2f3ab6d35f637998ef7faa3f45f2ed31a8f69665b7"

if __name__ == "__main__":
    main("--write" in sys.argv)
