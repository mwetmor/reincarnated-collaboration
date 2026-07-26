#!/usr/bin/env python3
"""
gd_bridge_m1_display_tags_2026_07_26.py — M1 of the GD display-name -> `.dbr` bridge.

WHAT THIS BANKS
    `gd_display_tag` — GD's shipped English localization tag table (tag_key -> display string),
    extracted from the `ARC` v3 `Text_EN.arc` containers of the Edition-II pinned tree.
    Domains banked: `creature` (the nameplate lane -- the bridge's first hop) and `skill`
    (banked in the same pass because it costs nothing and RETIRES the standing
    `exact_skill.name_provenance` PENDING caveat from the GD-SLICE migration).

    Views: `monster_display_tag` (the commissioned name; creature slice)
           `v_gd_display_tag_resolved` (one winning row per key, precedence applied)

NAMING NOTE (elrond seam call, deviation from the commission's literal wording)
    The commission asked for a table named `monster_display_tag`. The bytes on disk are not
    monster-specific -- `tags_creatures.txt` also carries the 18 racial-profile nouns
    (`tagRace005=Aether Corruption`) and their plurals, and the same archives carry the skill
    tags. A table named `monster_display_tag` holding race nouns and skill names would be a
    name that hides what the data is. So: base table `gd_display_tag` with an explicit
    `tag_domain` column (tagged, not encoded), and `monster_display_tag` exists as a VIEW over
    the creature domain so the commissioned name is a real, queryable surface.

MERGE-MODEL FINDING (this run — CORRECTS probe §1 by scope)
    The probe's "key-collision census across the four archives: ZERO" is TRUE **for the creature
    domain** (0/2,060) and therefore the bridge's own merge model is a plain union, as claimed.
    It is NOT true for the skill domain: **28 cross-archive key collisions**, all base<-expansion.
    27 of them are placeholder fills (base ships `''` or `'?'` for masteries that shipped later --
    e.g. `tagSkillClassName07` base `'?'` -> gdx1 `'Inquisitor'`). ONE is a substantive rewording
    with two real values: `tagDecreaseMasteryError` base 'Cannot reclaim points from the mastery.'
    -> gdx1 'You cannot reset a mastery selection.'
    Because a real override exists, this schema does NOT collapse on merge. Every row is banked
    with its `expansion`, and precedence (base < gdx1 < gdx2 < gdx3) is recorded as the derived
    columns `expansion_rank` / `is_resolved` / `shadowed_by`. The raw fan-out survives; the
    resolved lookup is a view over it. Discarding the shadowed rows would have destroyed the
    only evidence that the override is real rather than a placeholder.

GRADE
    DATAMINED (era-substrate LAW §4): verified against the source game's own shipped data files,
    edition-pinned + sha256-verified pre-parse. Attests AUTHORED DATA, not runtime behavior.

GATES (fire in order; failure HALTs before a single row is written)
    G1 EDITION PIN     — sha256 of every `.arc` read matches the recorded Edition-II pin.
    G2 CREATURE MERGE  — ZERO creature-domain key collisions (the load-bearing bridge claim).
    G2b SKILL MERGE    — skill collisions admitted + characterised; the count of SUBSTANTIVE
                         (non-placeholder) overrides is asserted against a regression oracle so a
                         source change is noticed rather than absorbed.
    G3 TIER-1 ANCHORS  — tagEnemyZombieA01 -> "Walking Dead"; tagRace005 -> "Aether Corruption";
                         tagGDX1Class07SkillName04A -> "Flames of Ignaffar".
    G4 NON-EMPTY       — every RESOLVED display string is non-empty (shadowed placeholders may be
                         empty by construction -- that is the finding, not a defect).

USAGE
    python3 gd_bridge_m1_display_tags_2026_07_26.py --verify-only   # gates only, no DB writes
    python3 gd_bridge_m1_display_tags_2026_07_26.py                 # backup, DDL, land rows, verify
"""
import collections
import datetime
import hashlib
import pathlib
import shutil
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file   # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parent / "curated" / "corpus.db"
BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")

SCHEMA_VERSION = "gd-displayname-bridge-2026-07-26"
ADAPTER = "gd_bridge_m1_display_tags_2026_07_26.py"
EDITION = "gd-edition-II-20260724"
LOCALE = "EN"
FIDELITY_GRADE = "DATAMINED"
RUN_DATE = "2026-07-26"

# precedence: later expansions override earlier ones (empirically justified — every observed
# collision has the later expansion supplying the substantive value)
EXPANSION_RANK = {"base": 0, "gdx1": 1, "gdx2": 2, "gdx3": 3}

# a shadowed value counting as a PLACEHOLDER (not a real prior meaning)
PLACEHOLDERS = {"", "?"}

# regression oracle: number of SUBSTANTIVE (non-placeholder) skill-domain overrides.
ORACLE_SUBSTANTIVE_OVERRIDES = 1          # tagDecreaseMasteryError
ORACLE_SKILL_EMPTY = 2                    # tagEnemySkillD16 + _Desc ship authored-blank
ORACLE_CREATURE_TAGS = 2060
ORACLE_ARZ_MONSTER_TOTAL = 4066           # probe §2 — checked in M2, recorded here for lineage

# ---- G1: the `.arc` edition pin. sha256 values are from the Edition-I freeze fingerprint §3
#      (base/gdx1/gdx2, byte-identical across editions) and this run for gdx3.
#
#      DEPOT/MANIFEST DELIBERATELY OMITTED FOR THE `.arc` LANE. The freeze §4 depot table maps
#      depot_id -> manifest_id but does NOT attest which depot ships `resources/Text_EN.arc`.
#      Putting a guessed depot in a provenance column is worse than a shorter pin. The sha256 is
#      self-verifying against the frozen bytes with zero dependency on any external table, so the
#      pin still passes the steward test ("exactly which bytes produced this row?").
ARCS = {
    "resources/Text_EN.arc": dict(
        expansion="base", creature_file="tags_creatures.txt", skill_file="tags_skills.txt",
        sha256="613457c8df72fe5a16de88def05dd00f518cf4e61c14cf375ef2ccab6dbd6e01"),
    "gdx1/resources/Text_EN.arc": dict(
        expansion="gdx1", creature_file="tagsgdx1_creatures.txt", skill_file="tagsgdx1_skills.txt",
        sha256="85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a"),
    "gdx2/resources/Text_EN.arc": dict(
        expansion="gdx2", creature_file="tagsgdx2_creatures.txt", skill_file="tagsgdx2_skills.txt",
        sha256="8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1"),
    "gdx3/resources/Text_EN.arc": dict(
        expansion="gdx3", creature_file="tagsgdx3_creatures.txt", skill_file="tagsgdx3_skills.txt",
        sha256="d6e7f7810ab251e3ad9e0dcf87e22d0af8f7d1611c02e1be4d431c44fd0d1f18"),
}

ANCHORS = {
    ("creature", "tagEnemyZombieA01"): "Walking Dead",
    ("creature", "tagRace005"): "Aether Corruption",
    ("skill", "tagGDX1Class07SkillName04A"): "Flames of Ignaffar",
}

DDL = """
CREATE TABLE IF NOT EXISTS gd_display_tag (
    locale            TEXT NOT NULL,
    tag_domain        TEXT NOT NULL CHECK (tag_domain IN ('creature','skill')),
    tag_key           TEXT NOT NULL,
    expansion         TEXT NOT NULL CHECK (expansion IN ('base','gdx1','gdx2','gdx3')),
    display_string    TEXT NOT NULL,
    expansion_rank    INTEGER NOT NULL,
    is_resolved       INTEGER NOT NULL CHECK (is_resolved IN (0,1)),
    shadowed_by       TEXT,
    tag_file          TEXT NOT NULL,
    source_arc        TEXT NOT NULL,
    source_arc_sha256 TEXT NOT NULL,
    source_version    TEXT NOT NULL,
    fidelity_grade    TEXT NOT NULL,
    adapter           TEXT NOT NULL,
    schema_version    TEXT NOT NULL,
    created_date      TEXT NOT NULL,
    PRIMARY KEY (locale, tag_domain, tag_key, expansion)
);
CREATE INDEX IF NOT EXISTS ix_gd_display_tag_string
    ON gd_display_tag (display_string, tag_domain, is_resolved);

DROP VIEW IF EXISTS v_gd_display_tag_resolved;
CREATE VIEW v_gd_display_tag_resolved AS
    SELECT locale, tag_domain, tag_key, display_string, expansion, tag_file,
           source_arc, source_arc_sha256, source_version, fidelity_grade
    FROM gd_display_tag WHERE is_resolved = 1;

DROP VIEW IF EXISTS monster_display_tag;
CREATE VIEW monster_display_tag AS
    SELECT tag_key, display_string, expansion, tag_file, source_arc, source_arc_sha256,
           source_version, fidelity_grade, locale
    FROM gd_display_tag
    WHERE tag_domain = 'creature' AND is_resolved = 1;
"""


def pin_for(rel):
    return (f"{EDITION}; arc={rel}; arc_sha256={ARCS[rel]['sha256']}; "
            f"depot=NOT-ATTESTED-FOR-ARC-LANE")


# ================================================================= gates + extraction
def verify_edition():
    print("G1 — EDITION PIN (sha256 of every .arc read)")
    ok = True
    for rel, meta in ARCS.items():
        h = hashlib.sha256((BASE / rel).read_bytes()).hexdigest()
        good = h == meta["sha256"]
        ok &= good
        print(f"    {'OK  ' if good else 'FAIL'} {rel:28s} {h[:16]}…")
    if not ok:
        raise SystemExit("HALT — .arc bytes do not match the recorded edition pin.")
    print(f"    edition = {EDITION}  ({len(ARCS)}/{len(ARCS)} archives byte-verified)\n")


def extract():
    """Return (rows, stats). Every source row is kept; precedence is annotated, not applied."""
    raw = []       # (domain, key, expansion, value, rel, tag_file)
    per_file = []
    for rel, meta in ARCS.items():
        arc = ArcArchive(BASE / rel)
        for domain, fname in (("creature", meta["creature_file"]), ("skill", meta["skill_file"])):
            if fname not in arc.entries:
                print(f"    NOTE  {rel}: {fname} absent — skipped")
                continue
            pairs = parse_tag_file(arc.read_file(fname))
            per_file.append((rel, domain, fname, len(pairs),
                             len(pairs) - len({k for k, _ in pairs})))
            for k, v in pairs:
                raw.append((domain, k, meta["expansion"], v, rel, fname))

    # annotate precedence
    by_key = collections.defaultdict(list)
    for r in raw:
        by_key[(r[0], r[1])].append(r)

    collisions = collections.defaultdict(list)   # domain -> [(key, [(exp,val)...])]
    rows = []
    for (domain, key), group in by_key.items():
        group = sorted(group, key=lambda r: EXPANSION_RANK[r[2]])
        winner = group[-1]
        if len(group) > 1:
            collisions[domain].append((key, [(g[2], g[3]) for g in group]))
        for r in group:
            is_res = 1 if r is winner else 0
            rows.append((LOCALE, domain, key, r[2], r[3], EXPANSION_RANK[r[2]], is_res,
                         None if is_res else winner[2], r[5], r[4],
                         ARCS[r[4]]["sha256"], pin_for(r[4]), FIDELITY_GRADE, ADAPTER,
                         SCHEMA_VERSION, RUN_DATE))
    return rows, dict(per_file=per_file, collisions=collisions)


def gates(rows, stats):
    print("G2 — MERGE MODEL")
    for rel, domain, fname, n, dup in stats["per_file"]:
        print(f"    {rel:28s} {domain:8s} {fname:26s} {n:6d} tags  ({dup} intra-file dup keys)")

    cre_coll = stats["collisions"].get("creature", [])
    print(f"\n    CREATURE cross-archive key collisions = {len(cre_coll)}  "
          f"(probe §1 claim: ZERO)")
    if cre_coll:
        for c in cre_coll[:10]:
            print(f"        {c}")
        raise SystemExit("HALT — creature-domain tag-key collisions. The bridge's merge model "
                         "(plain union) is invalid; a precedence rule must be ruled on first.")

    skl_coll = stats["collisions"].get("skill", [])
    substantive = [(k, g) for k, g in skl_coll
                   if any(v.strip() not in PLACEHOLDERS for _, v in g[:-1])]
    print(f"\nG2b — SKILL cross-archive key collisions = {len(skl_coll)} "
          f"(probe §1 did NOT scope this domain)")
    print(f"    placeholder fills (shadowed value '' or '?') : {len(skl_coll) - len(substantive)}")
    print(f"    SUBSTANTIVE overrides (two real values)      : {len(substantive)} "
          f"(oracle {ORACLE_SUBSTANTIVE_OVERRIDES})")
    for k, g in substantive:
        print(f"        {k}")
        for exp, val in g:
            print(f"            {exp:5s} = {val!r}")
    if len(substantive) != ORACLE_SUBSTANTIVE_OVERRIDES:
        raise SystemExit("HALT — substantive-override count moved off the regression oracle. "
                         "The source changed; re-characterise before banking.")

    print("\nG3 — TIER-1 ANCHORS")
    idx = {(r[1], r[2]): r[4] for r in rows if r[6] == 1}
    bad = 0
    for (domain, key), expect in ANCHORS.items():
        got = idx.get((domain, key))
        good = got == expect
        bad += not good
        print(f"    {'PASS' if good else 'FAIL'} {domain}/{key} -> {got!r} (expect {expect!r})")
    if bad:
        raise SystemExit("HALT — tier-1 anchor mismatch.")

    print("\nG4 — NON-EMPTY RESOLVED DISPLAY STRINGS")
    empties = [r for r in rows if r[6] == 1 and not r[4].strip()]
    cre_empty = [r for r in empties if r[1] == "creature"]
    skl_empty = [r for r in empties if r[1] == "skill"]
    print(f"    creature empties : {len(cre_empty)}  (must be 0 — the bridge reads this domain)")
    print(f"    skill empties    : {len(skl_empty)} (oracle {ORACLE_SKILL_EMPTY}): "
          f"{[e[2] for e in skl_empty]}")
    if cre_empty:
        print(f"        {[(e[2]) for e in cre_empty[:10]]}")
        raise SystemExit("HALT — a creature display string resolved empty.")
    if len(skl_empty) != ORACLE_SKILL_EMPTY:
        raise SystemExit("HALT — skill-empty count moved off the regression oracle. "
                         "Re-characterise before banking.")
    # NOT a defect: `tagEnemySkillD16` / `_Desc` ship authored-blank in base `tags_skills.txt`
    # (verified in-source: the literal lines are `tagEnemySkillD16=`). A reserved/unused pair.
    # Banked verbatim -- coercing them to NULL would be a silent transformation.

    creature = [r for r in rows if r[1] == "creature" and r[6] == 1]
    print(f"\n    creature tags banked (resolved) : {len(creature)} "
          f"(oracle {ORACLE_CREATURE_TAGS})")
    if len(creature) != ORACLE_CREATURE_TAGS:
        raise SystemExit("HALT — creature tag count moved off the probe's 2,060.")
    multi = collections.Counter(r[4] for r in creature)
    many = {k: v for k, v in multi.items() if v > 1}
    print(f"    distinct creature display strings : {len(multi)}")
    print(f"    display strings produced by >1 tag key : {len(many)} "
          f"(worst: {sorted(many.items(), key=lambda x: -x[1])[:3]})")
    print(f"    skill rows banked : {sum(1 for r in rows if r[1] == 'skill')} "
          f"({sum(1 for r in rows if r[1] == 'skill' and r[6] == 0)} shadowed)\n")


# ================================================================= apply
def apply(rows):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak = DB.with_name(DB.name + f".pre-bridge-m1-{ts}-backup")
    shutil.copy2(DB, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    bak.with_name(bak.name + ".md5.txt").write_text(f"{md5}  {bak.name}\n")
    print(f"BACKUP {bak.name} md5={md5}")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    try:
        con.executescript(DDL)
        con.execute("BEGIN")
        con.execute("DELETE FROM gd_display_tag WHERE schema_version = ?", (SCHEMA_VERSION,))
        con.executemany(
            "INSERT INTO gd_display_tag (locale, tag_domain, tag_key, expansion, display_string,"
            " expansion_rank, is_resolved, shadowed_by, tag_file, source_arc, source_arc_sha256,"
            " source_version, fidelity_grade, adapter, schema_version, created_date)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        con.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            (SCHEMA_VERSION + "/M1",
             datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
             "GD display-name bridge M1 (elrond, gandalf commission). ADDITIVE: gd_display_tag "
             "(GD EN localization tag table, ARC v3 Text_EN.arc base+gdx1/2/3) + views "
             "monster_display_tag (creature slice, the commissioned name) and "
             "v_gd_display_tag_resolved. Grade DATAMINED; edition gd-edition-II-20260724; "
             "4/4 .arc sha256-verified pre-parse. FINDING: probe's zero-collision claim holds "
             "for the CREATURE domain (0/2060) but NOT for skills (28 collisions: 27 base "
             "placeholder-fills + 1 substantive rewording, tagDecreaseMasteryError). Shadowed "
             "rows are BANKED, not discarded; precedence carried as expansion_rank/is_resolved/"
             "shadowed_by. Skill domain retires the exact_skill.name_provenance PENDING caveat "
             "from gd-slice-exact-fields-2026-07-24."))
        con.commit()
    except Exception:
        con.rollback()
        raise
    n = con.execute("SELECT COUNT(*) FROM gd_display_tag").fetchone()[0]
    per = con.execute("SELECT tag_domain, is_resolved, COUNT(*) FROM gd_display_tag "
                      "GROUP BY 1,2").fetchall()
    mv = con.execute("SELECT COUNT(*) FROM monster_display_tag").fetchone()[0]
    print(f"APPLIED gd_display_tag rows={n} {per}; view monster_display_tag rows={mv}")
    print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
    print("fk_check :", con.execute("PRAGMA foreign_key_check").fetchall() or "clean")
    con.close()


def main():
    verify_edition()
    rows, stats = extract()
    gates(rows, stats)
    if "--verify-only" in sys.argv:
        print("--verify-only: NO DB writes.")
        return
    apply(rows)


if __name__ == "__main__":
    main()
