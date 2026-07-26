#!/usr/bin/env python3
"""
gd_bridge_m4_retire_name_pending_2026_07_26.py — M4 tail of the GD display-name bridge.

ONE ROW, ONE COLUMN. Retires the `.arc` tag-bridge PENDING caveat that has stood on
`exact_skill.name_provenance` since the GD-SLICE migration (2026-07-24). The caveat said the
authoritative display name for Flames of Ignaffar was unavailable because `.arc` parsing was out
of scope. M1 banked the `.arc` tag tables, so it is available now.

WHAT IS AND IS NOT CHANGED
    `display_name` is NOT touched. The `skillBitmapName` workaround had already produced
    "Flames of Ignaffar", and the authoritative tag `tagGDX1Class07SkillName04A` resolves to the
    SAME string -- so the workaround is now VINDICATED, not corrected. Rewriting an identical
    value would create a spurious change in the audit trail.
    `name_provenance` IS rewritten, because it currently asserts something false (that the bridge
    is pending). A provenance column that lies about its own state is worse than a blunt one.

GATE
    The banked tag must resolve to exactly the string already in `display_name`. If it does not,
    that is a real discrepancy between the workaround and the authoritative source and it HALTs
    for a ruling rather than silently overwriting either.

USAGE
    python3 gd_bridge_m4_retire_name_pending_2026_07_26.py [--verify-only]
"""
import datetime
import hashlib
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parent / "curated" / "corpus.db"
SCHEMA_VERSION = "gd-displayname-bridge-2026-07-26"
ENTITY = "gd-flames-of-ignaffar-purifier"
TAG = "tagGDX1Class07SkillName04A"


def main():
    verify_only = "--verify-only" in sys.argv
    con = sqlite3.connect(DB)
    banked = con.execute(
        "SELECT display_string, tag_file, source_arc, source_arc_sha256 "
        "FROM v_gd_display_tag_resolved WHERE tag_key = ? AND tag_domain = 'skill'",
        (TAG,)).fetchone()
    if not banked:
        raise SystemExit(f"HALT — {TAG} is not banked. Run M1 first.")
    current = con.execute(
        "SELECT display_name, name_provenance FROM exact_skill WHERE entity_id = ?",
        (ENTITY,)).fetchone()
    if not current:
        raise SystemExit(f"HALT — {ENTITY} not in exact_skill.")

    print(f"    banked tag  {TAG} -> {banked[0]!r}  ({banked[1]} in {banked[2]})")
    print(f"    display_name currently                 = {current[0]!r}")
    if banked[0] != current[0]:
        raise SystemExit("HALT — the authoritative tag disagrees with the skillBitmapName "
                         "workaround. This is a real discrepancy; it needs a ruling, not an "
                         "overwrite.")
    print("    PASS — authoritative tag CONFIRMS the skillBitmapName workaround verbatim.")

    new_prov = (
        f"display name CONFIRMED against the authoritative `.arc` localization tag "
        f"{TAG} = '{banked[0]}' ({banked[1]}, {banked[2]}, sha256 {banked[3][:16]}…), banked in "
        f"gd_display_tag by {SCHEMA_VERSION}/M1. The prior skillBitmapName workaround "
        f"('skillicon_flamesofignaffar1up.tex') produced the identical string and is therefore "
        f"VINDICATED, not superseded. The PENDING caveat raised by "
        f"gd-slice-exact-fields-2026-07-24 §G4 is RETIRED.")
    if verify_only:
        print(f"\n    would set name_provenance to:\n      {new_prov}")
        print("\n--verify-only: NO DB writes.")
        return

    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak = DB.with_name(DB.name + f".pre-bridge-m4-{ts}-backup")
    shutil.copy2(DB, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    bak.with_name(bak.name + ".md5.txt").write_text(f"{md5}  {bak.name}\n")
    print(f"\nBACKUP {bak.name} md5={md5}")
    con.execute("BEGIN")
    n = con.execute("UPDATE exact_skill SET name_provenance = ? WHERE entity_id = ?",
                    (new_prov, ENTITY)).rowcount
    con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                (SCHEMA_VERSION + "/M4",
                 datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "GD display-name bridge M4 (elrond). DATA-ONLY, one row, one column: "
                 "exact_skill.name_provenance on gd-flames-of-ignaffar-purifier. The .arc "
                 "tag-bridge PENDING caveat standing since gd-slice-exact-fields-2026-07-24 §G4 "
                 "is RETIRED — tagGDX1Class07SkillName04A resolves to 'Flames of Ignaffar', "
                 "identical to the skillBitmapName workaround, which is therefore vindicated. "
                 "display_name UNCHANGED (identical value; no spurious edit)."))
    con.commit()
    print(f"    rows updated: {n}")
    print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
    con.close()


if __name__ == "__main__":
    main()
