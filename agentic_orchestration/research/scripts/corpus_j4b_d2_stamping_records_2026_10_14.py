#!/usr/bin/env python3
"""
corpus_j4b_d2_stamping_records_2026_10_14.py -- the export/manifest records for the J4b D2 stamping apply.

Run ONCE, after corpus_j4b_d2_stamping_apply_2026_10_14.py --apply. Reads corpus.db READ-ONLY.
  (1) kits-export/gd-eor-warlord-referent.json: mapping.grade/terminal_state/deviation_notes from the DB;
      the grade unknown marked RESOLVED; corpus_rowset digest + history.
  (2) kits-export/gd-eor-warlord-referent.manifest.json: rowset digest, current FILE, a revision.
  (3) NEW kits-export/d2-fire-sorc-c14.json: a verbatim dump of the kit's ROWSET rows (no transformation).
  (4) NEW kits-export/d2-fire-sorc-c14.manifest.json: ROWSET digest + counts, sources, package, corpus FILE.
Refuses unless the live DB FILE and the four ROWSETs are exactly the post-apply values.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import corpus_j4b_d2_stamping_apply_2026_10_14 as A  # noqa: E402

EXP = A.CURATED / "kits-export"
REF_EXPORT = EXP / f"{A.REF}.json"
REF_MANIFEST = EXP / f"{A.REF}.manifest.json"
NEW_EXPORT = EXP / f"{A.NEW}.json"
NEW_MANIFEST = EXP / f"{A.NEW}.manifest.json"
POST_FILE = "c7012de3134a1e646031f9bfff23ec33df3656e84aa3ee8224582e9854c203e8"
BACKUP = "corpus.db.pre-j4b-d2-stamping-20261015T035301Z-backup"
C14_DIR = A.COLLAB / "agentic_orchestration/legolas/research/2026-10-14-join1-c14-sorc-build-file"
GATE = A.COLLAB / "agentic_orchestration/qa/findings/2026-10-14-join1-j4b-d2-stamping-gate.md"
DATE = "2026-10-15"


def fe(p):
    return {"path": str(p), "sha256": A.sha_file(p), "kind": "FILE"}


def main():
    assert A.sha_file(A.DB) == POST_FILE, "REFUSE: corpus.db is not the post-apply FILE"
    con = sqlite3.connect(f"file:{A.DB}?mode=ro", uri=True)
    rs = {k: A.rowset(con, k) for k in A.ROWSET_OUT}
    assert rs == A.ROWSET_OUT, rs
    con.row_factory = sqlite3.Row
    km = dict(con.execute("SELECT * FROM kit_mapping WHERE kit_id=?", (A.REF,)).fetchone())
    assert (km["grade"], km["terminal_state"]) == ("CLOSE", "MAPPED")

    # (1) referent export
    ex = json.loads(REF_EXPORT.read_text())
    export_pre = A.sha_file(REF_EXPORT)
    assert ex["mapping"]["grade"] is None
    ex["mapping"]["grade"] = km["grade"]
    ex["mapping"]["terminal_state"] = km["terminal_state"]
    ex["mapping"]["deviation_notes"] = km["deviation_notes"]
    hit = 0
    for u in ex["unknowns"]:
        if u["what"].startswith("EoR mapping grade"):
            u["what"] = "EoR mapping grade (EXACT/CLOSE/APPROX/GAPPED) -- RESOLVED: CLOSE"
            u["settle"] = ("RESOLVED 2026-10-15: graded CLOSE / MAPPED (jack-ryan BLOCK on EXACT, collab bb83a9eeb + "
                           "f658a08b0; conductor KP-443), applied by elrond from gamora's stamping package v3 "
                           "(collab d2e28cbc6). The deviation note is in mapping.deviation_notes.")
            hit += 1
    assert hit == 1
    ex["corpus_rowset"]["digest"] = rs[A.REF]
    ex["corpus_rowset"]["history"].append({"date": DATE, "digest": rs[A.REF],
                                           "event": "J4b mapping grade CLOSE (kit_mapping row only; KP-442/443)"})
    REF_EXPORT.write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
    export_post = A.sha_file(REF_EXPORT)

    # (2) referent manifest
    man = json.loads(REF_MANIFEST.read_text())
    assert man["files"]["export"]["sha256"] == export_pre
    assert man["rowsets"][A.REF]["digest"] == A.ROWSET_IN[A.REF]
    man["files"]["export"]["sha256"] = export_post
    man["rowsets"][A.REF]["digest"] = rs[A.REF]
    man["corpus_db"]["current_FILE_sha256"] = POST_FILE
    man["revisions"].append({
        "date": DATE, "by": "elrond",
        "event": "J4b D2 stamping package v3 applied: referent mapping grade CLOSE / MAPPED (kit_mapping row only); "
                 "new sibling kit d2-fire-sorc-c14 (its own ROWSET); rulings KP-442/443/444",
        "corpus_db": {"pre_FILE_sha256": A.FILE_IN, "post_FILE_sha256": POST_FILE, "backup": BACKUP},
        "rowset": {"pre": A.ROWSET_IN[A.REF], "post": rs[A.REF], "moved_only_by": "kit_mapping row"},
        "files": {"package_sql": fe(A.SQL), "stamping_table": fe(A.TABLE), "gate": fe(GATE),
                  "apply_script": fe(HERE / "corpus_j4b_d2_stamping_apply_2026_10_14.py"),
                  "records_script": fe(pathlib.Path(__file__).resolve()),
                  "export": {"path": str(REF_EXPORT), "sha256": export_post, "kind": "FILE"}}})
    REF_MANIFEST.write_text(json.dumps(man, indent=2) + "\n")

    # (3) new kit export: verbatim ROWSET dump
    blocks = {}
    for t in A.ROWSET_TABLES:
        blocks[t] = [dict(r) for r in con.execute(f"SELECT * FROM {t} WHERE kit_id=? ORDER BY rowid", (A.NEW,))]
    counts = {t: len(v) for t, v in blocks.items()}
    nex = {
        "kit_id": A.NEW,
        "export_shape": "kits-export/rowset-dump-v1: every ROWSET-table row WHERE kit_id = d2-fire-sorc-c14, verbatim "
                        "(ordered by rowid), no transformation. INPUTS ONLY (KP-442 S3): the sheet is derived by the binder.",
        "provenance": {"build_file": "legolas C-14 (collab 0ac88e6ef), Maxroll S14 Meteor guide, Standard variant",
                       "package": "gamora stamping package v3 (collab d2e28cbc6, generator engine ce810948)",
                       "gate": "jack-ryan PASS (collab e6ce1a4a3)", "rulings": ["KP-442", "KP-443", "KP-444"],
                       "applied_by": "elrond", "applied": DATE},
        "sibling_not_modified": {"kit_id": A.SIB_D2, "rowset": rs[A.SIB_D2],
                                 "note": "D2R web values (rankedboost); nothing reads them as the 1.13 kit; c14 inherits nothing (KP-442 F4)"},
        "corpus_rowset": {"law": "J-S4 pin ROWSET law (see gd-eor-warlord-referent.manifest.json rowset_law)",
                          "tables": A.ROWSET_TABLES, "counts": counts, "digest": rs[A.NEW],
                          "history": [{"date": DATE, "digest": rs[A.NEW], "event": "mint (stamping package v3)"}]},
        "rows": blocks,
    }
    NEW_EXPORT.write_text(json.dumps(nex, indent=2, ensure_ascii=False) + "\n")

    # (4) new kit manifest
    tbl = json.loads(A.TABLE.read_text())
    files = {"export": fe(NEW_EXPORT), "package_sql": fe(A.SQL), "stamping_table": fe(A.TABLE), "gate": fe(GATE),
             "build_file_verbatim": fe(C14_DIR / "build_file_standard_verbatim.json"),
             "build_sheet": fe(C14_DIR / "sorc_build_sheet.json"),
             "apply_script": fe(HERE / "corpus_j4b_d2_stamping_apply_2026_10_14.py"),
             "records_script": fe(pathlib.Path(__file__).resolve())}
    assert files["build_file_verbatim"]["sha256"] == tbl["build_file_sha256"], "build file drifted from the package's input"
    nman = {"kit_id": A.NEW, "minted": DATE, "by": "elrond", "schema_meta_version": A.SCHEMA_META_VERSION,
            "files": files,
            "raw_1_13_tables_sha256": tbl["raw_files_sha256"],
            "rowsets": {A.NEW: {"digest": rs[A.NEW], "counts": counts, "kind": "ROWSET"},
                        A.SIB_D2: {"digest": rs[A.SIB_D2], "kind": "ROWSET", "note": "unchanged (guarded)"},
                        A.SIB_GD: {"digest": rs[A.SIB_GD], "kind": "ROWSET", "note": "unchanged (guarded)"},
                        A.REF: {"digest": rs[A.REF], "kind": "ROWSET", "note": "moved only by its kit_mapping grade row"}},
            "rowset_law": json.loads(REF_MANIFEST.read_text())["rowset_law"],
            "corpus_db": {"pre_FILE_sha256": A.FILE_IN, "post_FILE_sha256": POST_FILE, "backup": BACKUP},
            "rows_by_scale": tbl["rows_by_scale"]}
    NEW_MANIFEST.write_text(json.dumps(nman, indent=2) + "\n")
    con.close()
    assert A.sha_file(A.DB) == POST_FILE, "corpus.db changed during the records pass"
    print(json.dumps({"ref_export": export_post, "ref_manifest": A.sha_file(REF_MANIFEST),
                      "new_export": A.sha_file(NEW_EXPORT), "new_manifest": A.sha_file(NEW_MANIFEST),
                      "counts": counts, "rowsets": rs}, indent=1))


if __name__ == "__main__":
    main()
