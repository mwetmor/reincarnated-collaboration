#!/usr/bin/env python3
"""
corpus_js4b_rule_stamping_apply_2026_10_06.py -- JOIN-1 B0-N: apply gamora's J-S4b rule-stamping package.

Owner: elrond (corpus.db steward). Conductor: gandalf, Run JOIN-1 (KC2 ledger KP-304 / KP-305).
Package (rule owner gamora, collab 9a90660f8):
    agentic_orchestration/gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin/stamping/
      corpus_js4b_rule_stamping_2026_10_06.sql                 14 gd_seconds rows under R-T2
      corpus_js4b_rctxgeo_gd_metres_amendment_2026_10_06.sql   5 gd_metres radii under R-CTX-GEO,
                                                               amendment ACCEPTED PROVISIONALLY (KP-304),
                                                               pending jack-ryan JOIN-1 B0-N Gate-2
      stamping_table.json                                      the per-row verdicts (14 / 5 / 85)
    (…_PROPOSED_2026_10_06.sql is superseded and is NOT read.)

WHAT IT DOES
    Executes the two package files, in order, statement by statement (sqlite3.complete_statement, so a ';'
    inside a string literal does not split a statement), inside ONE enclosing transaction of this script's
    own. The package's own BEGIN TRANSACTION / COMMIT lines are not executed: the enclosing transaction makes
    both files atomic together, and nothing commits unless every guard below holds. Package SELECT guard lines
    are executed and printed verbatim; they are NOT trusted as the gate -- independent guards are computed here.
    Adds one corpus_schema_meta row naming the 5 provisional rows and their revert statement. No DDL.

GUARDS (all must hold, dry-run and apply)
    pre : corpus.db FILE == 0d73475a…; J-S4b ROWSET == 66250f2d…; 104 J-S4b rows unstamped;
          other kits 456 stamped rows / TOTAL(rdr) recorded
    mid : (after file 1) 14 rows R-T2, all gd_seconds; J-S4b ROWSET == e53ff212…
    post: 5 rows R-CTX-GEO, all gd_metres; 19 stamped / 85 unstamped; 0 rows with rdr_value IS NOT source_value;
          the stamped/unstamped key sets == stamping_table.json's STAMP / STAMP-UNDER-AMENDMENT / NO-RULE sets;
          other kits: 456 rows, same TOTAL(rdr), and a full digest of every other-kit kit_numeric row unchanged;
          sibling gd-eor-warlord ROWSET unchanged; normalization_rule unchanged except R-CTX-GEO.description;
          every table's row count unchanged except corpus_schema_meta +1; J-S4b ROWSET == c3e0f121…;
          integrity_check ok; foreign_key_check empty.

USAGE
    python3 corpus_js4b_rule_stamping_apply_2026_10_06.py --dry-run   # in-memory copy; zero bytes written
    python3 corpus_js4b_rule_stamping_apply_2026_10_06.py --apply     # backup, apply, re-verify, record digest
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
PKG = COLLAB / "agentic_orchestration/gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin/stamping"
SQL1 = PKG / "corpus_js4b_rule_stamping_2026_10_06.sql"
SQL2 = PKG / "corpus_js4b_rctxgeo_gd_metres_amendment_2026_10_06.sql"
TABLE = PKG / "stamping_table.json"
KIT = "gd-eor-warlord-referent"
SIBLING = "gd-eor-warlord"

FILE_IN = "0d73475aea0f5f290a754a501e58d83af06958259fae4621317320f0fb285d07"
ROWSET_IN = "66250f2d138be8b13e780c2f3ab6d35f637998ef7faa3f45f2ed31a8f69665b7"
ROWSET_MID = "e53ff212ead3f130333115e9743000c41a8cdcd3223c5f24c7af5aa89b8d319f"
ROWSET_OUT = "c3e0f121d2a7f44cc17c72107bd31db1bdf489f146a68898b3971b69b6c01597"
SIBLING_ROWSET = "1819fd0c1e277469ff81016ae5e32cafa46ba4944e30d12f35d1ec2bf108c7cc"
SCHEMA_META_VERSION = "join1-js4b-rule-stamping-2026-10-06"
PROVISIONAL_KEYS = ["eor_radius_m", "soulfire_explosion_radius_m", "vires_might_target_radius_m",
                    "war_cry_radius_m_r16", "violent_delights_target_radius_m"]
REVERT_SQL = ("UPDATE kit_numeric SET rdr_value=NULL, rule_id=NULL, rule_version_applied=NULL "
              "WHERE kit_id='gd-eor-warlord-referent' AND source_scale='gd_metres' AND rule_id='R-CTX-GEO'; "
              "and strip the ' ⚑ SCOPE AMENDMENT 2026-10-06 …' suffix from normalization_rule R-CTX-GEO.description")
ROWSET_TABLES = ["canon_corpus", "kit_mapping", "kit_numeric", "kit_composition", "kit_citations",
                 "kit_dossier", "kit_deviation", "kit_delta_t4", "kit_acceptance_assert",
                 "kit_door_arg", "skill_geometry_band", "verify_ledger"]


def sha_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rowset(con, kit):
    """Same law as corpus_js4b_referent_mint_2026_10_02.rowset (the J-S4 pin)."""
    con.row_factory = sqlite3.Row
    lines = []
    for t in ROWSET_TABLES:
        for r in con.execute(f"SELECT * FROM {t} WHERE kit_id = ? ORDER BY rowid", (kit,)).fetchall():
            lines.append(t + "\t" + json.dumps(dict(r), sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    con.row_factory = None
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
    n_upd = 0
    for s in statements(path):
        head = [w.rstrip(";").upper() for w in s.split(None, 2)[:2]]
        if head[0] in ("BEGIN", "COMMIT", "END", "ROLLBACK"):
            log.append(f"  [{path.name}] package '{s}' NOT executed (enclosed in this script's transaction)")
            continue
        assert con.in_transaction, "enclosing transaction lost"
        cur = con.execute(s)
        if head[0] == "SELECT":
            for r in cur.fetchall():
                log.append(f"  [{path.name}] {r[0]}")
        elif head[0] == "UPDATE":
            n_upd += 1
            log.append(f"  [{path.name}] UPDATE … ({cur.rowcount} rows)")
    return n_upd


def q1(con, sql, args=()):
    return con.execute(sql, args).fetchone()[0]


def main(mode):
    st = os.statvfs(str(CURATED))
    free = st.f_bavail * st.f_frsize / 2**30
    print(f"free disk {free:.2f} GiB")
    assert free > 20, "HALT: free disk below the charter's 20 GiB line"
    pre_sha = sha_file(DB)
    assert pre_sha == FILE_IN, f"REFUSE: corpus.db FILE is {pre_sha}, not {FILE_IN}"
    pkg_sha = {p.name: sha_file(p) for p in (SQL1, SQL2, TABLE)}
    tbl = json.loads(TABLE.read_text())
    assert tbl["corpus_db_FILE_sha256_in"] == FILE_IN and tbl["js4b_ROWSET_in"] == ROWSET_IN
    want = {"STAMP": set(), "STAMP-UNDER-AMENDMENT": set(), "NO-RULE": set()}
    for r in tbl["rows"]:
        want[r["verdict"]].add(r["numeric_key"])
    assert {k: len(v) for k, v in want.items()} == {"STAMP": 14, "STAMP-UNDER-AMENDMENT": 5, "NO-RULE": 85}
    assert want["STAMP-UNDER-AMENDMENT"] == set(PROVISIONAL_KEYS)

    bak = None
    if mode == "dry-run":
        con = sqlite3.connect(":memory:", isolation_level=None)
        src = sqlite3.connect(str(DB))
        src.backup(con)
        src.close()
    else:
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        bak = CURATED / f"corpus.db.pre-js4b-stamping-{ts}-backup"
        shutil.copy2(DB, bak)
        assert sha_file(bak) == pre_sha, "backup digest mismatch"
        print(f"backup {bak.name} FILE sha256 {pre_sha}")
        con = sqlite3.connect(str(DB), isolation_level=None)
    con.execute("PRAGMA foreign_keys=ON")
    log, g = [], {}

    other_sql = ("SELECT * FROM kit_numeric WHERE kit_id <> ? ORDER BY kit_id, numeric_key")
    rule_sql = "SELECT * FROM normalization_rule WHERE rule_id <> 'R-CTX-GEO' ORDER BY rule_id"
    counts_before = table_counts(con)
    g["pre_rowset"] = rowset(con, KIT)
    assert g["pre_rowset"] == ROWSET_IN, g["pre_rowset"]
    g["pre_unstamped"] = q1(con, "SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rdr_value IS NULL AND rule_id IS NULL", (KIT,))
    assert g["pre_unstamped"] == 104
    g["pre_other"] = con.execute("SELECT count(*), TOTAL(rdr_value) FROM kit_numeric WHERE kit_id<>? AND rule_id IS NOT NULL", (KIT,)).fetchone()
    assert g["pre_other"][0] == 456, g["pre_other"]
    other_digest_pre = rows_digest(con, other_sql, (KIT,))
    rules_digest_pre = rows_digest(con, rule_sql)
    sib_pre = rowset(con, SIBLING)
    assert sib_pre == SIBLING_ROWSET
    ctx_desc_pre = q1(con, "SELECT description FROM normalization_rule WHERE rule_id='R-CTX-GEO'")

    try:
        con.execute("BEGIN IMMEDIATE")
        run_file(con, SQL1, log)
        g["mid_stamped"] = con.execute("SELECT count(*), group_concat(DISTINCT rule_id), group_concat(DISTINCT source_scale) "
                                       "FROM kit_numeric WHERE kit_id=? AND rule_id IS NOT NULL", (KIT,)).fetchone()
        assert g["mid_stamped"] == (14, "R-T2", "gd_seconds"), g["mid_stamped"]
        g["mid_rowset"] = rowset(con, KIT)
        assert g["mid_rowset"] == ROWSET_MID, g["mid_rowset"]
        run_file(con, SQL2, log)
        g["post_ctxgeo"] = con.execute("SELECT count(*), group_concat(DISTINCT source_scale) FROM kit_numeric "
                                       "WHERE kit_id=? AND rule_id='R-CTX-GEO'", (KIT,)).fetchone()
        assert g["post_ctxgeo"] == (5, "gd_metres"), g["post_ctxgeo"]
        stamped = {r[0]: r[1] for r in con.execute("SELECT numeric_key, rule_id FROM kit_numeric WHERE kit_id=? AND rule_id IS NOT NULL", (KIT,))}
        unst = {r[0] for r in con.execute("SELECT numeric_key FROM kit_numeric WHERE kit_id=? AND rule_id IS NULL AND rdr_value IS NULL", (KIT,))}
        assert {k for k, v in stamped.items() if v == "R-T2"} == want["STAMP"]
        assert {k for k, v in stamped.items() if v == "R-CTX-GEO"} == want["STAMP-UNDER-AMENDMENT"]
        assert unst == want["NO-RULE"]
        g["post_stamped_unstamped"] = (len(stamped), len(unst))
        assert g["post_stamped_unstamped"] == (19, 85)
        g["post_rdr_ne_source"] = q1(con, "SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rule_id IS NOT NULL "
                                          "AND rdr_value IS NOT source_value", (KIT,))
        assert g["post_rdr_ne_source"] == 0
        g["post_version_applied"] = q1(con, "SELECT group_concat(DISTINCT rule_version_applied) FROM kit_numeric WHERE kit_id=? AND rule_id IS NOT NULL", (KIT,))
        assert str(g["post_version_applied"]) == "1"
        g["post_other"] = con.execute("SELECT count(*), TOTAL(rdr_value) FROM kit_numeric WHERE kit_id<>? AND rule_id IS NOT NULL", (KIT,)).fetchone()
        assert g["post_other"] == g["pre_other"], g["post_other"]
        assert rows_digest(con, other_sql, (KIT,)) == other_digest_pre, "an other-kit kit_numeric row moved"
        assert rows_digest(con, rule_sql) == rules_digest_pre, "a normalization_rule other than R-CTX-GEO moved"
        ctx_desc_post = q1(con, "SELECT description FROM normalization_rule WHERE rule_id='R-CTX-GEO'")
        assert ctx_desc_post.startswith(ctx_desc_pre) and "SCOPE AMENDMENT 2026-10-06" in ctx_desc_post[len(ctx_desc_pre):]
        assert rowset(con, SIBLING) == sib_pre, "sibling ROWSET moved"
        g["post_rowset"] = rowset(con, KIT)
        assert g["post_rowset"] == ROWSET_OUT, g["post_rowset"]
        note = (f"J-S4b rule stamping APPLIED by elrond (corpus.db steward) from gamora's package (rule owner; collab 9a90660f8; "
                f"KP-304/KP-305; conductor gandalf). DATA-ONLY, no DDL. {KIT}: 14 gd_seconds rows -> R-T2 v1 (IDENTITY); "
                f"⚑ 5 gd_metres rows -> R-CTX-GEO v1 (IDENTITY) STAMPED UNDER THE PROVISIONAL SCOPE AMENDMENT (KP-304), "
                f"pending jack-ryan JOIN-1 B0-N Gate-2: {', '.join(PROVISIONAL_KEYS)}. If the gate rejects it, revert = "
                f"{REVERT_SQL}. 85 rows remain unstamped (NO-RULE, reasons in stamping_table.json). J-S4b ROWSET "
                f"{ROWSET_IN[:16]} -> {ROWSET_OUT[:16]}; other kits unchanged (456 stamped rows, full-row digest asserted). "
                f"Script research/scripts/corpus_js4b_rule_stamping_apply_2026_10_06.py.")
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (SCHEMA_META_VERSION, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), note))
        counts_after = table_counts(con)
        exp = dict(counts_before)
        exp["corpus_schema_meta"] += 1
        assert counts_after == exp, "a table row count moved other than corpus_schema_meta +1"
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        g["integrity_check"] = q1(con, "PRAGMA integrity_check")
        assert g["integrity_check"] == "ok"
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        con.close()
        raise

    # re-verify on the committed state (re-opened for apply)
    if mode == "apply":
        con.close()
        con = sqlite3.connect(str(DB))
    g["reverify_rowset"] = rowset(con, KIT)
    assert g["reverify_rowset"] == ROWSET_OUT
    g["reverify_integrity"] = q1(con, "PRAGMA integrity_check")
    g["reverify_fk"] = con.execute("PRAGMA foreign_key_check").fetchall()
    assert g["reverify_integrity"] == "ok" and g["reverify_fk"] == []
    g["reverify_other"] = con.execute("SELECT count(*), TOTAL(rdr_value) FROM kit_numeric WHERE kit_id<>? AND rule_id IS NOT NULL", (KIT,)).fetchone()
    assert g["reverify_other"] == g["pre_other"]
    assert rowset(con, SIBLING) == SIBLING_ROWSET
    con.close()
    post_sha = sha_file(DB) if mode == "apply" else None
    if mode == "apply":
        assert post_sha != pre_sha
    for line in log:
        print(line)
    out = dict(mode=mode, pre_FILE=pre_sha, post_FILE=post_sha, backup=str(bak.name) if bak else None,
               package_FILE_sha256=pkg_sha, guards={k: (list(v) if isinstance(v, tuple) else v) for k, v in g.items()},
               other_kits_digest=other_digest_pre[0], counts_after_changed={"corpus_schema_meta": exp["corpus_schema_meta"]})
    print(json.dumps(out, indent=1, default=str))
    return out


if __name__ == "__main__":
    main("apply" if "--apply" in sys.argv else "dry-run")
