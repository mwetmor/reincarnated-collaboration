#!/usr/bin/env python3
"""
corpus_rctxgeo_confirm_2026_10_06.py -- record jack-ryan's JOIN-1 B0-N Gate-2 CONFIRMATION of the R-CTX-GEO
gd_metres scope amendment (qa/findings/2026-10-06-join1-b0n-gate2.md s5; collab 6371fe6cc; conductor KP-307).

Owner: elrond (corpus.db steward). DATA-ONLY, no DDL.

WHAT IT DOES
    * normalization_rule R-CTX-GEO.description: APPENDS a CONFIRMED clause (corrigenda-forward, per the Gate-2's
      condition 1: the 'ACCEPTED PROVISIONALLY ... pending' text stays as history; the new clause states that it
      supersedes it). Records the two scope limits (condition 2: skill radii only; condition 3: unit identity,
      not values). rule_version stays 1 (transform unchanged).
    * corpus_schema_meta +1 row.
    * kit_numeric is NOT touched -> the J-S4b ROWSET must stay c3e0f121... (asserted; abort if it would move).
    * --apply also lifts the provisional label on the 5 rows in the referent export and adds a manifest revision.

USAGE
    python3 corpus_rctxgeo_confirm_2026_10_06.py --dry-run
    python3 corpus_rctxgeo_confirm_2026_10_06.py --apply
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import corpus_js4b_rule_stamping_apply_2026_10_06 as A  # noqa: E402  (rowset / sha_file / table_counts / rows_digest)

DB, CURATED, KIT = A.DB, A.CURATED, A.KIT
EXPORT = CURATED / "kits-export" / f"{KIT}.json"
MANIFEST = CURATED / "kits-export" / f"{KIT}.manifest.json"
FILE_IN = "639acb2033e09b522793e1138a36c9144dc23af05be0ebe6944955fd4a9432ea"
ROWSET = A.ROWSET_OUT
GATE = "collab 6371fe6cc"
FINDING = "agentic_orchestration/qa/findings/2026-10-06-join1-b0n-gate2.md s5"
SCHEMA_META_VERSION = "join1-rctxgeo-gd-metres-confirmed-2026-10-06"
CLAUSE = (" ⚑ CONFIRMED jack-ryan JOIN-1 B0-N Gate-2 (collab 6371fe6cc), 2026-10-06; conductor KP-307: the gd_metres scope "
          "amendment above is CONFIRMED and supersedes its 'ACCEPTED PROVISIONALLY, pending jack-ryan JOIN-1 B0-N Gate-2' "
          "wording (kept as history). SCOPE LIMITS: skill radii only -- gd_metres_per_second (e.g. player_v_ref_m_per_s) and "
          "any other gd_metres quantity that is not a skill radius need their own amendment. The confirmation certifies the "
          "UNIT IDENTITY, not the values: war_cry_radius_m_r16 16.8 vs the oracle's 16.0 (r12; KP-241 (4)) remains an open "
          "value disagreement. rule_version stays 1 (transform unchanged).")
KEYS = ["eor_radius_m", "soulfire_explosion_radius_m", "vires_might_target_radius_m", "war_cry_radius_m_r16",
        "violent_delights_target_radius_m"]
STATUS = ("CONFIRMED: R-CTX-GEO v1 (IDENTITY), gd_metres scope amendment confirmed by jack-ryan JOIN-1 B0-N Gate-2 "
          "(collab 6371fe6cc; conductor KP-307). Scope: skill radii only. Certifies the unit identity, not the value.")


def main(mode):
    st = os.statvfs(str(CURATED))
    free = st.f_bavail * st.f_frsize / 2**30
    print(f"free disk {free:.2f} GiB")
    assert free > 20, "HALT: free disk below 20 GiB"
    pre = A.sha_file(DB)
    assert pre == FILE_IN, f"REFUSE: corpus.db FILE is {pre}"
    bak = None
    if mode == "dry-run":
        con = sqlite3.connect(":memory:", isolation_level=None)
        s = sqlite3.connect(str(DB)); s.backup(con); s.close()
    else:
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        bak = CURATED / f"corpus.db.pre-rctxgeo-confirm-{ts}-backup"
        shutil.copy2(DB, bak)
        assert A.sha_file(bak) == pre
        print(f"backup {bak.name} FILE sha256 {pre}")
        con = sqlite3.connect(str(DB), isolation_level=None)
    con.execute("PRAGMA foreign_keys=ON")
    rs_pre = A.rowset(con, KIT)
    assert rs_pre == ROWSET, rs_pre
    sib_pre = A.rowset(con, A.SIBLING)
    counts_pre = A.table_counts(con)
    knum_pre = A.rows_digest(con, "SELECT * FROM kit_numeric ORDER BY kit_id, numeric_key")
    rules_pre = A.rows_digest(con, "SELECT * FROM normalization_rule WHERE rule_id <> 'R-CTX-GEO' ORDER BY rule_id")
    row_pre = con.execute("SELECT rule_version, source_scale, status, description FROM normalization_rule WHERE rule_id='R-CTX-GEO'").fetchone()
    assert "pending jack-ryan JOIN-1 B0-N Gate-2" in row_pre[3] and "CONFIRMED jack-ryan" not in row_pre[3]
    try:
        con.execute("BEGIN IMMEDIATE")
        cur = con.execute("UPDATE normalization_rule SET description = description || ? WHERE rule_id='R-CTX-GEO' "
                          "AND instr(description, 'CONFIRMED jack-ryan JOIN-1 B0-N Gate-2') = 0", (CLAUSE,))
        assert cur.rowcount == 1
        row_post = con.execute("SELECT rule_version, source_scale, status, description FROM normalization_rule WHERE rule_id='R-CTX-GEO'").fetchone()
        assert row_post[:3] == row_pre[:3] and row_post[3] == row_pre[3] + CLAUSE
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (SCHEMA_META_VERSION, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     f"R-CTX-GEO gd_metres scope amendment CONFIRMED by jack-ryan JOIN-1 B0-N Gate-2 ({GATE}; {FINDING}); "
                     f"conductor KP-307. Description clause appended corrigenda-forward (provisional wording kept as history). "
                     f"The PROVISIONAL label of join1-js4b-rule-stamping-2026-10-06 on {', '.join(KEYS)} is LIFTED; nothing reverts. "
                     f"Scope limits: skill radii only (gd_metres_per_second needs its own amendment); unit identity confirmed, "
                     f"not values (war_cry_radius_m_r16 16.8 vs oracle 16.0 open). kit_numeric untouched; J-S4b ROWSET "
                     f"{ROWSET[:16]} unchanged. elrond, script research/scripts/corpus_rctxgeo_confirm_2026_10_06.py."))
        assert A.rowset(con, KIT) == ROWSET, "ROWSET would move -- STOP"
        assert A.rowset(con, A.SIBLING) == sib_pre
        assert A.rows_digest(con, "SELECT * FROM kit_numeric ORDER BY kit_id, numeric_key") == knum_pre
        assert A.rows_digest(con, "SELECT * FROM normalization_rule WHERE rule_id <> 'R-CTX-GEO' ORDER BY rule_id") == rules_pre
        exp = dict(counts_pre); exp["corpus_schema_meta"] += 1
        assert A.table_counts(con) == exp
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        con.execute("COMMIT")
    except Exception:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise
    if mode == "apply":
        con.close()
        con = sqlite3.connect(str(DB))
    rs_post = A.rowset(con, KIT)
    integ = con.execute("PRAGMA integrity_check").fetchone()[0]
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    assert rs_post == ROWSET and integ == "ok" and fk == []
    con.close()
    post = A.sha_file(DB) if mode == "apply" else None
    print(json.dumps({"mode": mode, "pre_FILE": pre, "post_FILE": post, "backup": bak.name if bak else None,
                      "rowset_pre": rs_pre, "rowset_post": rs_post, "kit_numeric_all_rows_unchanged": True,
                      "integrity_check": integ, "foreign_key_check": fk,
                      "schema_meta_rows": exp["corpus_schema_meta"]}, indent=1))
    if mode != "apply":
        return
    # export + manifest
    ex = json.loads(EXPORT.read_text())
    export_pre = A.sha_file(EXPORT)
    for n in ex["numeric"]:
        if n["numeric_key"] in KEYS:
            assert n["rule_id"] == "R-CTX-GEO" and n["rule_stamp_status"].startswith("PROVISIONAL")
            n["rule_stamp_status"] = STATUS
    rsb = ex["rule_stamping"]
    rsb["R-CTX-GEO_confirmed"] = rsb.pop("R-CTX-GEO_provisional")
    rsb["R-CTX-GEO_status_history"] = [{"date": "2026-10-06", "status": rsb.pop("R-CTX-GEO_status")},
                                       {"date": "2026-10-06", "status": STATUS, "by": f"jack-ryan JOIN-1 B0-N Gate-2 ({GATE}; {FINDING})"}]
    rsb["R-CTX-GEO_status"] = STATUS
    rsb["R-CTX-GEO_scope_limits"] = [
        "skill radii only: gd_metres_per_second (player_v_ref_m_per_s) and any other non-radius gd_metres quantity need their own amendment",
        "certifies the unit identity, not the values: war_cry_radius_m_r16 16.8 vs the oracle's 16.0 (r12; KP-241 (4)) remains an open value disagreement"]
    EXPORT.write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
    export_post = A.sha_file(EXPORT)
    man = json.loads(MANIFEST.read_text())
    assert man["files"]["export"]["sha256"] == export_pre
    man["files"]["export"]["sha256"] = export_post
    man["corpus_db"]["current_FILE_sha256"] = post
    man["revisions"].append({
        "date": "2026-10-06", "by": "elrond", "event": "R-CTX-GEO gd_metres amendment CONFIRMED (jack-ryan B0-N Gate-2); provisional label lifted",
        "corpus_db": {"pre_FILE_sha256": pre, "post_FILE_sha256": post, "backup": bak.name},
        "rowset": {"pre": rs_pre, "post": rs_post, "unchanged": rs_pre == rs_post},
        "confirmed_rows": KEYS, "gate": f"{GATE}; {FINDING}",
        "files": {"confirm_script": {"path": str(pathlib.Path(__file__).resolve()), "sha256": A.sha_file(pathlib.Path(__file__)), "kind": "FILE"},
                  "export": {"path": str(EXPORT), "sha256": export_post, "kind": "FILE"}}})
    MANIFEST.write_text(json.dumps(man, indent=2) + "\n")
    print("export", export_post)
    print("manifest", A.sha_file(MANIFEST))


if __name__ == "__main__":
    main("apply" if "--apply" in sys.argv else "dry-run")
