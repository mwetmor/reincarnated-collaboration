#!/usr/bin/env python3
"""
corpus_j4b_d2_stamping_apply_2026_10_14.py -- JOIN-1 J4b B0-N: apply gamora's D2 stamping package v3.

Owner: elrond (corpus.db steward). Conductor: gandalf, Run JOIN-1.
Rulings: KC2 KP-442 (new kit_id d2-fire-sorc-c14; the referent's grade is the kit-level kit_mapping cell;
inputs only), KP-443 (referent grade CLOSE), KP-444 (skillProgression spent).
Package v3 (rule owner gamora, collab d2e28cbc6; generator engine ce810948), gated PASS by jack-ryan
(collab e6ce1a4a3, addendum 2):
    agentic_orchestration/gamora/analyses/2026-10-14-join1-j4b-d2-stamping/
      corpus_j4b_d2_stamping_2026_10_14.sql   sha256 f9985251f76c0c099be48e4ca28d7192d56339e4ca1a1adff20857b7f690114a
      stamping_table.json                     the 597 rows, input digests, predicted ROWSETs

WHAT IT DOES
    Executes the package file statement by statement (sqlite3.complete_statement, so a ';' inside a string
    literal does not split a statement) inside ONE enclosing transaction of this script's own. The package's
    BEGIN TRANSACTION / COMMIT lines are not executed. Package SELECT guard lines are executed and printed
    verbatim; they are NOT trusted as the gate -- independent guards are computed here. Adds one
    corpus_schema_meta row. No DDL.

GUARDS (all must hold, dry-run and apply)
    pre : free disk > 20 GiB; corpus.db FILE == 2617c0c1...; SQL sha == f9985251...; stamping_table.json input
          digests match; ROWSET J-S4b == c96d8975..., d2-fire-sorc == db01da52..., gd-eor-warlord == 1819fd0c...;
          d2-fire-sorc-c14 absent everywhere; R-D2S1 absent; referent grade IS NULL.
    post: ROWSET J-S4b == 59099b7d... AND every J-S4b row in every ROWSET table except kit_mapping unchanged
          (moved only by the grade row); referent grade CLOSE / MAPPED; ROWSET d2-fire-sorc-c14 == bbc2db89...;
          c14 counts canon_corpus 1 / kit_mapping 1 / kit_citations 3 / kit_numeric 597 (key set == the table's),
          0 rows with rdr_value IS NOT source_value, all rule R-D2S1 v1, scale counts == rows_by_scale;
          c14 has no canon_engine_key row and is absent from v_combat_kits and v_corpus_substrate;
          EVERY other kit's ROWSET unchanged (all canon_corpus kit_ids); other-kit kit_numeric full-row digest
          unchanged; normalization_rule unchanged except +R-D2S1; table row counts change only by
          canon_corpus +1, kit_mapping +1, kit_citations +3, kit_numeric +597, normalization_rule +1,
          corpus_schema_meta +1; integrity_check ok; foreign_key_check empty.

USAGE
    python3 corpus_j4b_d2_stamping_apply_2026_10_14.py --dry-run   # in-memory copy; zero bytes written
    python3 corpus_j4b_d2_stamping_apply_2026_10_14.py --apply     # backup, apply, re-verify, record digest
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
COLLAB = HERE.parents[2]
CURATED = HERE.parent / "curated"
DB = CURATED / "corpus.db"
PKG = COLLAB / "agentic_orchestration/gamora/analyses/2026-10-14-join1-j4b-d2-stamping"
SQL = PKG / "corpus_j4b_d2_stamping_2026_10_14.sql"
TABLE = PKG / "stamping_table.json"

REF = "gd-eor-warlord-referent"
NEW = "d2-fire-sorc-c14"
SIB_D2 = "d2-fire-sorc"
SIB_GD = "gd-eor-warlord"

FILE_IN = "2617c0c101d8d924cb327e50137b1b3a61b1a8cbd81a24632d2ebe3469eaa26b"
SQL_SHA = "f9985251f76c0c099be48e4ca28d7192d56339e4ca1a1adff20857b7f690114a"
ROWSET_IN = {REF: "c96d8975ca4d5e0511174c2ba5d6560329b1e049749e49137f7f45ab592ad0e9",
             SIB_D2: "db01da528164eeec5935b0d0d1836f94ec748ebbd11118e2cf2360f7a26ed618",
             SIB_GD: "1819fd0c1e277469ff81016ae5e32cafa46ba4944e30d12f35d1ec2bf108c7cc"}
ROWSET_OUT = {REF: "59099b7d779f44b5d56076058a0539af97b9497dd2e298868b8020c4fe598ac7",
              NEW: "bbc2db8943086e85bf2504ccd4f4ed77fbcd87d9c84e692cdb2bf26a069db87b",
              SIB_D2: ROWSET_IN[SIB_D2], SIB_GD: ROWSET_IN[SIB_GD]}
SCHEMA_META_VERSION = "join1-j4b-d2-stamping-2026-10-14"
ROWSET_TABLES = ["canon_corpus", "kit_mapping", "kit_numeric", "kit_composition", "kit_citations",
                 "kit_dossier", "kit_deviation", "kit_delta_t4", "kit_acceptance_assert",
                 "kit_door_arg", "skill_geometry_band", "verify_ledger"]
COUNT_DELTA = {"canon_corpus": 1, "kit_mapping": 1, "kit_citations": 3, "kit_numeric": 597,
               "normalization_rule": 1, "corpus_schema_meta": 1}


def sha_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _lines(con, t, kit):
    con.row_factory = sqlite3.Row
    out = [t + "\t" + json.dumps(dict(r), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
           for r in con.execute(f"SELECT * FROM {t} WHERE kit_id = ? ORDER BY rowid", (kit,)).fetchall()]
    con.row_factory = None
    return out


def rowset(con, kit, tables=ROWSET_TABLES):
    """The J-S4 pin's ROWSET law (corpus_js4b_referent_mint_2026_10_02.rowset)."""
    lines = []
    for t in tables:
        lines += _lines(con, t, kit)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def rows_digest(con, sql, args=()):
    con.row_factory = sqlite3.Row
    lines = [json.dumps(dict(r), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
             for r in con.execute(sql, args).fetchall()]
    con.row_factory = None
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest(), len(lines)


def table_counts(con):
    names = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return {n: con.execute(f'SELECT count(*) FROM "{n}"').fetchone()[0] for n in names}


def statements(path: pathlib.Path):
    buf = ""
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if not buf and line.lstrip().startswith("--"):
            continue
        buf += line
        if sqlite3.complete_statement(buf):
            s = buf.strip()
            buf = ""
            if s:
                yield s
    assert not buf.strip(), f"trailing incomplete statement in {path.name}: {buf[:80]!r}"


def run_file(con, path, log):
    n = {"UPDATE": 0, "INSERT": 0, "SELECT": 0}
    for s in statements(path):
        head = s.split(None, 1)[0].rstrip(";").upper()
        if head in ("BEGIN", "COMMIT", "END", "ROLLBACK"):
            log.append(f"  package '{s}' NOT executed (enclosed in this script's transaction)")
            continue
        assert head in n, f"unexpected statement kind {head!r}"
        assert con.in_transaction, "enclosing transaction lost"
        cur = con.execute(s)
        n[head] += 1
        if head == "SELECT":
            for r in cur.fetchall():
                log.append(f"  [package] {r[0]}")
        elif head == "UPDATE":
            log.append(f"  [package] UPDATE ... ({cur.rowcount} rows)")
            assert cur.rowcount == 1, "the package's one UPDATE must touch exactly one row"
    return n


def q1(con, sql, args=()):
    return con.execute(sql, args).fetchone()[0]


def all_kits(con):
    return [r[0] for r in con.execute("SELECT kit_id FROM canon_corpus ORDER BY kit_id")]


def main(mode):
    st = os.statvfs(str(CURATED))
    free = st.f_bavail * st.f_frsize / 2**30
    print(f"free disk {free:.2f} GiB")
    assert free > 20, "HALT: free disk below the charter's 20 GiB line"
    pre_sha = sha_file(DB)
    assert pre_sha == FILE_IN, f"REFUSE: corpus.db FILE is {pre_sha}, not {FILE_IN}"
    assert sha_file(SQL) == SQL_SHA, "REFUSE: package SQL digest mismatch"
    tbl = json.loads(TABLE.read_text())
    assert tbl["corpus_db_FILE_sha256_in"] == FILE_IN and tbl["sql_sha256"] == SQL_SHA
    assert tbl["ROWSET_in"] == ROWSET_IN and tbl["predicted_post_apply_ROWSET"] == ROWSET_OUT
    assert tbl["new_kit"] == NEW and tbl["rule"] == "R-D2S1" and tbl["n_kit_numeric_rows"] == 597
    want_keys = {r["numeric_key"] for r in tbl["rows"]}
    assert len(want_keys) == 597

    bak = None
    if mode == "dry-run":
        con = sqlite3.connect(":memory:", isolation_level=None)
        src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        src.backup(con)
        src.close()
    else:
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        bak = CURATED / f"corpus.db.pre-j4b-d2-stamping-{ts}-backup"
        shutil.copy2(DB, bak)
        assert sha_file(bak) == pre_sha, "backup digest mismatch"
        print(f"backup {bak.name} FILE sha256 {pre_sha}")
        con = sqlite3.connect(str(DB), isolation_level=None)
    con.execute("PRAGMA foreign_keys=ON")
    log, g = [], {}

    # ---- pre ----
    for k, d in ROWSET_IN.items():
        assert rowset(con, k) == d, f"pre ROWSET {k} drifted"
    for t in ROWSET_TABLES + ["canon_engine_key"]:
        assert q1(con, f"SELECT count(*) FROM {t} WHERE kit_id=?", (NEW,)) == 0, f"{NEW} already in {t}"
    assert q1(con, "SELECT count(*) FROM normalization_rule WHERE rule_id='R-D2S1'") == 0
    assert q1(con, "SELECT count(*) FROM kit_mapping WHERE kit_id=? AND grade IS NULL", (REF,)) == 1
    kits_pre = all_kits(con)
    rowsets_pre = {k: rowset(con, k) for k in kits_pre}
    ref_nonmapping_pre = rowset(con, REF, [t for t in ROWSET_TABLES if t != "kit_mapping"])
    other_sql = "SELECT * FROM kit_numeric WHERE kit_id <> ? ORDER BY kit_id, numeric_key"
    other_pre = rows_digest(con, other_sql, (NEW,))
    rule_sql = "SELECT * FROM normalization_rule WHERE rule_id <> 'R-D2S1' ORDER BY rule_id"
    rules_pre = rows_digest(con, rule_sql)
    counts_before = table_counts(con)
    g["pre_kits"] = len(kits_pre)
    g["pre_other_kit_numeric_rows"] = other_pre[1]

    try:
        con.execute("BEGIN IMMEDIATE")
        g["package_statements"] = run_file(con, SQL, log)
        assert g["package_statements"]["UPDATE"] == 1 and g["package_statements"]["INSERT"] == 1 + 1 + 1 + 3 + 597

        # referent: moved only by the grade row
        assert con.execute("SELECT grade, terminal_state FROM kit_mapping WHERE kit_id=?", (REF,)).fetchone() == ("CLOSE", "MAPPED")
        assert rowset(con, REF, [t for t in ROWSET_TABLES if t != "kit_mapping"]) == ref_nonmapping_pre, \
            "J-S4b moved outside its kit_mapping row"
        # new kit
        c = {t: q1(con, f"SELECT count(*) FROM {t} WHERE kit_id=?", (NEW,)) for t in ROWSET_TABLES}
        assert c == {**{t: 0 for t in ROWSET_TABLES}, "canon_corpus": 1, "kit_mapping": 1,
                     "kit_citations": 3, "kit_numeric": 597}, c
        got_keys = {r[0] for r in con.execute("SELECT numeric_key FROM kit_numeric WHERE kit_id=?", (NEW,))}
        assert got_keys == want_keys, "c14 key set differs from stamping_table.json"
        assert q1(con, "SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rdr_value IS NOT source_value", (NEW,)) == 0
        assert con.execute("SELECT group_concat(DISTINCT rule_id), group_concat(DISTINCT rule_version_applied) "
                           "FROM kit_numeric WHERE kit_id=?", (NEW,)).fetchone() == ("R-D2S1", "1")
        scales = dict(con.execute("SELECT source_scale, count(*) FROM kit_numeric WHERE kit_id=? GROUP BY 1", (NEW,)).fetchall())
        assert scales == tbl["rows_by_scale"], scales
        assert q1(con, "SELECT count(*) FROM canon_engine_key WHERE kit_id=?", (NEW,)) == 0
        assert q1(con, "SELECT count(*) FROM v_combat_kits WHERE kit_id=?", (NEW,)) == 0
        assert q1(con, "SELECT count(*) FROM v_corpus_substrate WHERE kit_id=?", (NEW,)) == 0
        # every other kit
        kits_post = all_kits(con)
        assert sorted(kits_post) == sorted(kits_pre + [NEW])
        moved = [k for k in kits_pre if rowset(con, k) != rowsets_pre[k]]
        assert moved == [REF], f"ROWSETs moved: {moved}"
        assert rows_digest(con, other_sql, (NEW,)) == other_pre, "an other-kit kit_numeric row moved"
        assert rows_digest(con, rule_sql) == rules_pre, "a normalization_rule other than R-D2S1 moved"
        g["post_rowsets"] = {k: rowset(con, k) for k in ROWSET_OUT}
        assert g["post_rowsets"] == ROWSET_OUT, g["post_rowsets"]

        note = (f"J4b D2 stamping package v3 APPLIED by elrond (corpus.db steward) from gamora (rule owner; collab d2e28cbc6, "
                f"generator engine ce810948; SQL sha {SQL_SHA[:16]}), gated PASS by jack-ryan (collab e6ce1a4a3). Rulings "
                f"KP-442/443/444. DATA-ONLY, no DDL. (1) {REF}: kit_mapping.grade NULL -> CLOSE, terminal MAPPED, corrected "
                f"deviation note; kit_numeric untouched (J-S4b moved only by the grade row). (2) normalization_rule R-D2S1 v1 "
                f"(IDENTITY over 8 d2_input_* scales; anchors applied at the adapter boundary, never in the corpus). (3) new kit "
                f"{NEW} (source c14-build-file, parked, no canon_engine_key row): canon_corpus 1, kit_mapping 1 (grade NULL, owed), "
                f"kit_citations 3, kit_numeric 597 INPUT rows (VERBATIM planner + DATAMINED 1.13; the sheet is derived by the "
                f"binder). ROWSETs: J-S4b {ROWSET_IN[REF][:16]} -> {ROWSET_OUT[REF][:16]}; {NEW} {ROWSET_OUT[NEW][:16]}; "
                f"{SIB_D2} and {SIB_GD} and every other kit unchanged (asserted). Script "
                f"research/scripts/corpus_j4b_d2_stamping_apply_2026_10_14.py.")
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (SCHEMA_META_VERSION, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), note))
        counts_after = table_counts(con)
        exp = dict(counts_before)
        for t, d in COUNT_DELTA.items():
            exp[t] += d
        assert counts_after == exp, {t: (counts_before[t], counts_after[t]) for t in counts_after if counts_after[t] != exp.get(t)}
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        g["integrity_check"] = q1(con, "PRAGMA integrity_check")
        assert g["integrity_check"] == "ok"
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        con.close()
        raise

    if mode == "apply":
        con.close()
        con = sqlite3.connect(str(DB))
    g["reverify_rowsets"] = {k: rowset(con, k) for k in ROWSET_OUT}
    assert g["reverify_rowsets"] == ROWSET_OUT
    g["reverify_unmoved_kits"] = sum(1 for k in kits_pre if k != REF and rowset(con, k) == rowsets_pre[k])
    assert g["reverify_unmoved_kits"] == len(kits_pre) - 1
    g["reverify_integrity"] = q1(con, "PRAGMA integrity_check")
    g["reverify_fk"] = con.execute("PRAGMA foreign_key_check").fetchall()
    assert g["reverify_integrity"] == "ok" and g["reverify_fk"] == []
    con.close()
    post_sha = sha_file(DB) if mode == "apply" else None
    if mode == "apply":
        assert post_sha != pre_sha
    for line in log:
        print(line)
    out = dict(mode=mode, pre_FILE=pre_sha, post_FILE=post_sha, backup=bak.name if bak else None,
               package={"sql": SQL_SHA, "table": sha_file(TABLE)}, guards=g,
               table_count_deltas=COUNT_DELTA, other_kit_numeric_digest=other_pre[0])
    print(json.dumps(out, indent=1, default=str))
    return out


if __name__ == "__main__":
    main("apply" if "--apply" in sys.argv else "dry-run")
