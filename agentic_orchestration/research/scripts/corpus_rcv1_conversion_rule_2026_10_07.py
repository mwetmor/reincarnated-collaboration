#!/usr/bin/env python3
"""
corpus_rcv1_conversion_rule_2026_10_07.py -- JOIN-1 J2 (KP-324): PROPOSED normalization rule R-CV1 for damage-type
conversion percentages, and the stamp of the referent's three conversion rows under it.

Owner: elrond (corpus.db steward). Conductor: gandalf (KP-324 commission; KP-326 CONFIRMED with the rule owner's
amendment). Rule owner: gamora -- objection on the predicate only, converts to SIGN-OFF with the amendment
(agentic_orchestration/gamora/notes/2026-10-07-rcv1-rule-owner-objection.md, collab 16f23ca88).

WHY A NEW RULE (survey, 2026-10-07, corpus.db FILE 37635bad...):
    No active rule covers a damage-type conversion percentage.
      * gd_pct is named by NO rule's source_scale or Covers enumeration. R-G3 consumes ONE gd_pct leaf (armor
        absorption, row-scoped), not the scale.
      * R-A2's "invested-conversion" is attribute points -> stats (x8), not a damage-type conversion.
      * R-M5 covers poe1_pct / poe2_pct modifier/mitigation leaves (crit, resist cap, move-speed, impale) -- PoE only.
      * R-N4 is monster resist / block / caps.
    So the three referent rows stay NULL under the dual-column law until a rule is minted.

THE RULE (R-CV1 v1, IDENTITY):
    rdr = source_value: the percent of the SOURCE damage type relabelled to the TARGET type, 0..100, carried 1:1
    (a percent of a packet is a percent of a packet). SCOPE BY PREDICATE, not by scale: rows whose numeric_key
    matches DAMAGE_FAMILY `_to_` DAMAGE_FAMILY `(_conversion)?_pct` with BOTH sides closed over the damage-family
    vocabulary (VOCAB below) -- AMENDED by the rule owner (gamora, collab 16f23ca88; conductor KP-326): the v1-as-
    proposed wildcard `[a-z]+_to_[a-z]+` would have captured chance_to_hit_pct / damage_to_mana_pct /
    life_to_mana_pct. A future family enters by amendment, never by wildcard. Every key matching KC-1b's
    `<original>_to_physical(_conversion)?_pct` (the conversion reader's predicate) matches this one. source_scale is the
    scope name 'damage_type_conversion_pct' (precedent: R-CTX-GEO's 'context_geometry_gating'), so the rule does
    NOT claim the whole gd_pct scale (weapon-damage %, bleed modifier %, damage reduction % stay uncovered).
    FENCED: a conversion fraction is a damage-TYPE relabel, never a damage-magnitude multiplier. Packet splitting,
    multi-source summation and GD's proportional scale-down when conversions exceed 100% are COMPOSITION (refused
    in v0 by the reader: PartialConversionUnsupported / ConversionMagnitudeInvalid), not a leaf rescale. Certifies the UNIT identity, not the values: Gutsmasher Chaos/Lightning
    DATAMINED 50/50 vs FOOTAGE 55/46 remains an open value disagreement (export UNKNOWNS).

ROWS (all on gd-eor-warlord-referent, source_scale gd_pct; predicate-matched corpus-wide = exactly these 3):
    eor_fire_to_physical_conversion_pct (100) · gutsmasher_chaos_to_physical_pct (50) ·
    gutsmasher_lightning_to_physical_pct (50)

USAGE
    python3 corpus_rcv1_conversion_rule_2026_10_07.py --dry-run            # in-memory copy; zero bytes written
    python3 corpus_rcv1_conversion_rule_2026_10_07.py --apply --confirmed KP-<n>   # only after conductor confirmation
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import re
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import corpus_js4b_rule_stamping_apply_2026_10_06 as A  # noqa: E402  (rowset / sha_file / table_counts / rows_digest)

DB, CURATED, KIT = A.DB, A.CURATED, A.KIT
EXPORT = CURATED / "kits-export" / f"{KIT}.json"
MANIFEST = CURATED / "kits-export" / f"{KIT}.manifest.json"
FILE_IN = "37635bad392181fea7c77ddd8ad96b5ceae4d8dd193405ef03e7f4768ddecd5b"
ROWSET_IN = "c3e0f121d2a7f44cc17c72107bd31db1bdf489f146a68898b3971b69b6c01597"
RULE_ID = "R-CV1"
RULE_SCOPE = "damage_type_conversion_pct"
RULE_OWNER = "gamora"
VOCAB = "physical|pierce|fire|cold|lightning|poison|acid|aether|chaos|life|vitality|bleeding|elemental"
PREDICATE = re.compile(rf"(?:^|_)(?:{VOCAB})_to_(?:{VOCAB})(?:_conversion)?_pct$")
PREDICATE_TEXT = PREDICATE.pattern
KC1B_SAMPLE = ["eor_fire_to_physical_conversion_pct", "x_chaos_to_physical_pct", "lightning_to_physical_pct"]
PROBES_MUST_NOT_MATCH = ["chance_to_hit_pct", "damage_to_mana_pct", "life_to_mana_pct", "retaliation_to_attack_pct"]
KEYS = ["eor_fire_to_physical_conversion_pct", "gutsmasher_chaos_to_physical_pct", "gutsmasher_lightning_to_physical_pct"]
SCHEMA_META_VERSION = "join1-j2-rcv1-conversion-rule-2026-10-07"
DESCRIPTION = (
    "Damage-type CONVERSION percentage -> RDR. IDENTITY_v1: rdr = source_value (the percent of the SOURCE damage type "
    "relabelled to the TARGET type, 0..100; a percent of a packet is a percent of a packet). SCOPE BY PREDICATE, not by "
    "scale: kit_numeric rows whose numeric_key matches " + PREDICATE_TEXT + " -- BOTH sides of _to_ closed over the "
    "damage-family vocabulary (J2 registry offense families + intake-only acid/elemental + GD vitality for Life); a "
    "future family enters by amendment, never by wildcard (rule-owner amendment, gamora 16f23ca88). Every key matching "
    "KC-1b's <original>_to_physical(_conversion)?_pct (the join2 conversion reader's predicate) matches. Covers gd_pct ONLY for "
    "predicate-matched rows; weapon-damage %, modifier % and damage-reduction % on gd_pct are NOT covered. FENCED: a "
    "conversion fraction is a damage-TYPE relabel, NEVER a damage-magnitude multiplier; packet split, multi-source "
    "summation and GD's proportional scale-down when conversions exceed 100% are COMPOSITION (refused in v0 by the "
    "reader), not a leaf rescale. Certifies the UNIT identity, not the values (Gutsmasher Chaos/Lightning DATAMINED 50/50 vs FOOTAGE 55/46 "
    "open). Proposed by elrond (JOIN-1 J2, conductor KP-324); rule owner gamora signed off with the predicate "
    "amendment (collab 16f23ca88); CONFIRMED conductor KP-326. Anchor: GD Edition IV .arz conversionPercentage / "
    "conversionPercentage2 fields.")


def main(mode, confirmed):
    st = os.statvfs(str(CURATED))
    free = st.f_bavail * st.f_frsize / 2**30
    print(f"free disk {free:.2f} GiB")
    assert free > 20, "HALT: free disk below 20 GiB"
    if mode == "apply":
        assert confirmed, "REFUSE: --apply needs --confirmed <conductor KP row>"
    assert all(PREDICATE.search(k) for k in KC1B_SAMPLE + KEYS), "predicate misses a KC-1b-shaped key"
    assert not any(PREDICATE.search(k) for k in PROBES_MUST_NOT_MATCH), "predicate captures a non-conversion probe"
    pre = A.sha_file(DB)
    assert pre == FILE_IN, f"REFUSE: corpus.db FILE is {pre}"
    bak = None
    if mode == "dry-run":
        con = sqlite3.connect(":memory:", isolation_level=None)
        s = sqlite3.connect(str(DB)); s.backup(con); s.close()
    else:
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        bak = CURATED / f"corpus.db.pre-rcv1-conversion-{ts}-backup"
        shutil.copy2(DB, bak)
        assert A.sha_file(bak) == pre
        print(f"backup {bak.name} FILE sha256 {pre}")
        con = sqlite3.connect(str(DB), isolation_level=None)
    con.execute("PRAGMA foreign_keys=ON")
    g = {}
    g["pre_rowset"] = A.rowset(con, KIT)
    assert g["pre_rowset"] == ROWSET_IN
    assert con.execute("SELECT count(*) FROM normalization_rule WHERE rule_id=?", (RULE_ID,)).fetchone()[0] == 0
    # predicate coverage, corpus-wide
    matched = sorted((k, n) for k, n in con.execute("SELECT kit_id, numeric_key FROM kit_numeric") if PREDICATE.search(n))
    g["predicate_matches_corpus_wide"] = matched
    assert matched == sorted((KIT, k) for k in KEYS), matched
    pre_rows = {r[0]: r[1:] for r in con.execute(
        "SELECT numeric_key, source_value, source_scale, rdr_value, rule_id, rule_version_applied FROM kit_numeric "
        "WHERE kit_id=? AND numeric_key IN (?,?,?)", (KIT, *KEYS))}
    assert all(v[1] == "gd_pct" and v[2] is None and v[3] is None and v[4] is None for v in pre_rows.values()), pre_rows
    sib = A.rowset(con, A.SIBLING)
    counts_pre = A.table_counts(con)
    other_sql = "SELECT * FROM kit_numeric WHERE NOT (kit_id=? AND numeric_key IN (?,?,?)) ORDER BY kit_id, numeric_key"
    others_pre = A.rows_digest(con, other_sql, (KIT, *KEYS))
    rules_pre = A.rows_digest(con, "SELECT * FROM normalization_rule ORDER BY rule_id")
    unst_pre = con.execute("SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rule_id IS NULL", (KIT,)).fetchone()[0]
    try:
        con.execute("BEGIN IMMEDIATE")
        con.execute("INSERT INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, "
                    "status, created_date) VALUES (?,?,?,?,?,?,?,?)",
                    (RULE_ID, 1, RULE_SCOPE, DESCRIPTION, RULE_OWNER,
                     "research/scripts/corpus_rcv1_conversion_rule_2026_10_07.py#R-CV1", "active", "2026-10-07"))
        cur = con.execute("UPDATE kit_numeric SET rdr_value = source_value, rule_id = ?, rule_version_applied = 1 "
                          "WHERE kit_id=? AND source_scale='gd_pct' AND numeric_key IN (?,?,?) AND rule_id IS NULL AND rdr_value IS NULL",
                          (RULE_ID, KIT, *KEYS))
        assert cur.rowcount == 3
        post_rows = {r[0]: r[1:] for r in con.execute(
            "SELECT numeric_key, source_value, rdr_value, rule_id, rule_version_applied FROM kit_numeric WHERE kit_id=? AND numeric_key IN (?,?,?)", (KIT, *KEYS))}
        assert all(v[1] == v[0] and v[2] == RULE_ID and v[3] == 1 for v in post_rows.values())
        g["stamped"] = {k: v[1] for k, v in post_rows.items()}
        g["rdr_is_not_source_on_stamped"] = con.execute(
            "SELECT count(*) FROM kit_numeric WHERE rule_id=? AND rdr_value IS NOT source_value", (RULE_ID,)).fetchone()[0]
        assert g["rdr_is_not_source_on_stamped"] == 0
        assert A.rows_digest(con, other_sql, (KIT, *KEYS)) == others_pre, "a kit_numeric row other than the 3 moved"
        assert A.rows_digest(con, "SELECT * FROM normalization_rule WHERE rule_id<>? ORDER BY rule_id", (RULE_ID,)) == rules_pre
        assert A.rowset(con, A.SIBLING) == sib
        g["unstamped_referent"] = (unst_pre, con.execute("SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rule_id IS NULL", (KIT,)).fetchone()[0])
        assert g["unstamped_referent"] == (85, 82)
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (SCHEMA_META_VERSION, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     f"R-CV1 v1 (damage-type conversion %, IDENTITY, predicate-scoped) minted on conductor confirmation "
                     f"{confirmed}; rule owner {RULE_OWNER}; proposed by elrond (KP-324). Stamped {', '.join(KEYS)} on {KIT}. "
                     f"Other rows and rules unchanged. Script research/scripts/corpus_rcv1_conversion_rule_2026_10_07.py."))
        exp = dict(counts_pre); exp["corpus_schema_meta"] += 1; exp["normalization_rule"] += 1
        assert A.table_counts(con) == exp, "a table row count moved other than normalization_rule +1, corpus_schema_meta +1"
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        g["integrity_check"] = con.execute("PRAGMA integrity_check").fetchone()[0]
        assert g["integrity_check"] == "ok"
        g["post_rowset"] = A.rowset(con, KIT)
        assert g["post_rowset"] != ROWSET_IN
        if mode == "dry-run":
            con.execute("ROLLBACK")
        else:
            con.execute("COMMIT")
    except Exception:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise
    out = {"mode": mode, "confirmed": confirmed, "pre_FILE": pre, "backup": bak.name if bak else None, "guards": g}
    if mode == "apply":
        con.close()
        con = sqlite3.connect(str(DB))
        assert A.rowset(con, KIT) == g["post_rowset"]
        assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        con.close()
        out["post_FILE"] = A.sha_file(DB)
        export_records(out, pre, bak, g, confirmed)
    print(json.dumps(out, indent=1, default=str))
    return out


STATUS = ("STAMPED (R-CV1 v1, IDENTITY; damage-type conversion %, predicate-scoped; rule owner gamora signed off with "
          "the predicate amendment, collab 16f23ca88; conductor KP-326). Certifies the unit, not the value.")


def export_records(out, pre, bak, g, confirmed):
    ex = json.loads(EXPORT.read_text())
    export_pre = A.sha_file(EXPORT)
    n_hit = 0
    for n in ex["numeric"]:
        if n["numeric_key"] in KEYS:
            assert n["rdr_value"] is None and n["rule_id"] is None and n["rule_stamp_status"].startswith("UNSTAMPED")
            n["rdr_value"] = g["stamped"][n["numeric_key"]]
            n["rule_id"] = RULE_ID
            n["rule_version_applied"] = 1
            n["rule_stamp_status"] = STATUS
            n_hit += 1
    assert n_hit == 3
    rs = ex["rule_stamping"]
    rs["R-CV1"] = sorted(KEYS)
    rs["R-CV1_status"] = STATUS
    rs["R-CV1_predicate"] = PREDICATE_TEXT
    rs["R-CV1_scope_limits"] = [
        "damage-type conversion % only; both sides of _to_ closed over the damage-family vocabulary (amendment, never wildcard)",
        "certifies the unit identity, not the values: Gutsmasher Chaos/Lightning DATAMINED 50/50 vs FOOTAGE 55/46 open",
        "split / summation / >100% scale-down are composition, refused in v0 by the reader"]
    rs["unstamped"] = g["unstamped_referent"][1]
    for u in ex["unknowns"]:
        if u["what"].startswith("rdr_value for the 85 unstamped"):
            u["what"] = "rdr_value for the 82 unstamped kit_numeric rows"
            u["settle"] = u["settle"].replace("gd_pct, ", "gd_pct (non-conversion), ")
    ex["corpus_rowset"]["digest"] = g["post_rowset"]
    ex["corpus_rowset"]["history"].append({"date": "2026-10-07", "digest": g["post_rowset"],
                                           "event": f"R-CV1 conversion stamping (3 rows; {confirmed})"})
    EXPORT.write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
    export_post = A.sha_file(EXPORT)
    man = json.loads(MANIFEST.read_text())
    assert man["files"]["export"]["sha256"] == export_pre
    man["files"]["export"]["sha256"] = export_post
    man["rowsets"][KIT]["digest"] = g["post_rowset"]
    man["corpus_db"]["current_FILE_sha256"] = out["post_FILE"]
    man["revisions"].append({
        "date": "2026-10-07", "by": "elrond", "event": f"R-CV1 v1 minted + 3 conversion rows stamped ({confirmed})",
        "corpus_db": {"pre_FILE_sha256": pre, "post_FILE_sha256": out["post_FILE"], "backup": bak.name},
        "rowset": {"pre": g["pre_rowset"], "post": g["post_rowset"]},
        "stamped_rows": sorted(KEYS), "rule": {"rule_id": RULE_ID, "rule_version": 1, "source_scale": RULE_SCOPE,
                                               "predicate": PREDICATE_TEXT, "rule_owner": RULE_OWNER},
        "files": {"rcv1_script": {"path": str(pathlib.Path(__file__).resolve()), "sha256": A.sha_file(pathlib.Path(__file__)), "kind": "FILE"},
                  "rule_owner_note": {"path": str(A.COLLAB / "agentic_orchestration/gamora/notes/2026-10-07-rcv1-rule-owner-objection.md"),
                                      "sha256": A.sha_file(A.COLLAB / "agentic_orchestration/gamora/notes/2026-10-07-rcv1-rule-owner-objection.md"), "kind": "FILE"},
                  "export": {"path": str(EXPORT), "sha256": export_post, "kind": "FILE"}}})
    MANIFEST.write_text(json.dumps(man, indent=2) + "\n")
    out["export_FILE"] = export_post
    out["manifest_FILE"] = A.sha_file(MANIFEST)


if __name__ == "__main__":
    argv = sys.argv
    conf = argv[argv.index("--confirmed") + 1] if "--confirmed" in argv else None
    main("apply" if "--apply" in argv else "dry-run", conf)
