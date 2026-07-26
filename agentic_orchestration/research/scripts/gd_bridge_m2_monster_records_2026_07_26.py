#!/usr/bin/env python3
"""
gd_bridge_m2_monster_records_2026_07_26.py — M2 of the GD display-name -> `.dbr` bridge.

WHAT THIS BANKS  (three additive tables in corpus.db)
    `gd_monster_record` — one row per `rtype == 'Monster'` `.dbr` in the Edition-II `.arz` set.
        Identity + the join columns: `description` tag key, the display string resolved against
        M1's `gd_display_tag`, `characterRacialProfile` + its resolved race noun,
        `monsterClassification`, `factions`, `controller`, and the
        `characterAttributeEquations` bio pointer -- which is where the statline actually lives.
    `gd_monster_field` — long-form statline surface, one row per (record, raw_field) for the
        curated families. Carries `raw_field` + `raw_value` alongside `canon_key` (the
        two-column tagged-not-encoded convention established by `exact_skill_field`).
    `gd_monster_bio` — the bio records the Monster rows point at. GD stores monster attributes
        as FORMULA STRINGS over `charLevel` (`((charLevel*4)^1.33)+24`), not as numbers. Those
        formulas are the statline; this table is the join target for any statline prediction.

SCOPE CHOICE (declared, per commission)
    **FULL bestiary — all 4,066 Monster records, not the nameplate-reachable subset.**
    The commission offered the 4,052-record tag-resolvable set as a defensible minimum. I banked
    the full 4,066 instead because (a) the whole pass runs in well under a minute, so the smaller
    scope buys nothing, and (b) the 14 records that carry NO tag are exactly the rows a future
    coverage question will ask about; excluding them would make their absence indistinguishable
    from an extraction failure. `display_name_status` names the three states explicitly:
    `resolved` / `tag-unresolved` / `no-tag`.

WHY NOT `monster_numeric`
    `monster_numeric` is the cross-game COMMUNITY-HARVEST surface: `source_url` and `source_date`
    are NOT NULL and every row runs through the `normalization_rule` / `rdr_value` pipeline. A
    `.arz` datamine has neither a URL nor a normalized value yet, and forcing one would be a
    fabricated provenance. So GD's primary-source monster data lands in its own `gd_monster_*`
    tables -- exactly the precedent `exact_skill` set against `kit_numeric`. The `canon_key`
    column deliberately reuses `monster_numeric`'s existing vocabulary (`life`, `fire_resist_pct`,
    `accuracy`, `defense`, `experience`, …) so a future normalization lap can promote these rows
    without re-deriving the mapping.

GRADE
    DATAMINED (era-substrate LAW §4). 4/4 `.arz` sha256-verified pre-parse.

GATES
    G1 EDITION PIN  — sha256 of every `.arz` read matches the recorded Edition-II pin.
    G2 CENSUS       — per-archive Monster counts + tag/bio coverage reproduce the probe §2 table
                      (1307/737/1064/958 = 4,066; 4,052 tagged; 4,050 with bio).
    G3 TIER-1       — `records/creatures/enemies/zombie_a01.dbr` fields byte-match probe §0/§4.
    G4 RESOLUTION   — every resolvable `description` tag resolves against M1; every
                      `characterRacialProfile` resolves to a `tagRace…` entry.

USAGE
    python3 gd_bridge_m2_monster_records_2026_07_26.py --verify-only
    python3 gd_bridge_m2_monster_records_2026_07_26.py
"""
import collections
import datetime
import re
import hashlib
import pathlib
import shutil
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gd_arz_adapter_2026_07_24 import ArzArchive   # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parent / "curated" / "corpus.db"
BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")

SCHEMA_VERSION = "gd-displayname-bridge-2026-07-26"
ADAPTER = "gd_bridge_m2_monster_records_2026_07_26.py"
EDITION = "gd-edition-II-20260724"
FIDELITY_GRADE = "DATAMINED"
RUN_DATE = "2026-07-26"

ARCHIVES = {
    "database/database.arz": dict(
        file="database.arz", expansion="base", depot=219991, name="base",
        manifest="8006922163969537169",
        sha256="8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f",
        oracle_monster=1307),
    "gdx1/database/GDX1.arz": dict(
        file="GDX1.arz", expansion="gdx1", depot=642280, name="gdx1/AshesOfMalmouth",
        manifest="2275863479823292335",
        sha256="e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539",
        oracle_monster=737),
    "gdx2/database/GDX2.arz": dict(
        file="GDX2.arz", expansion="gdx2", depot=897670, name="gdx2/ForgottenGods",
        manifest="4804720554373426689",
        sha256="f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985",
        oracle_monster=1064),
    "gdx3/database/GDX3.arz": dict(
        file="GDX3.arz", expansion="gdx3", depot=2699230, name="gdx3/FangsOfAsterkarn",
        manifest="1575323658468418166",
        sha256="1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0",
        oracle_monster=958),
}
ORACLE_TOTAL_MONSTER = 4066
ORACLE_WITH_BIO = 4050
# TWO tag-coverage oracles, because the probe's single number silently encodes a predicate.
#   probe §2 "with `tag…` description" = description STARTS WITH 'tag'          -> 4,052
#   the broader "description is non-empty"                                       -> 4,055
# The 3-record gap is NOT a discrepancy: `records/sandbox/boss_{deino,enyo,pemphredo}_*.dbr`
# carry `xtagMonsterGraeae{1,2,3}` — the `x`-prefix is GD's authoring convention for a
# DISABLED tag. Both counts are correct under their own predicate; banking one and asserting
# the other would have looked like a parse bug forever. They land as `tag-unresolved`, which is
# the honest status: a description exists and does not resolve.
ORACLE_WITH_TAG_PREFIX = 4052
ORACLE_WITH_DESC = 4055
ORACLE_XTAG_SANDBOX = 3

# Resolution-coverage oracles, characterised this run against the FULL tag namespace.
#   32 description tags exist on a Monster record and resolve to nothing in ANY tag file. These
#   are GD authoring debris, not extraction failures: 3 are the `xtag`-disabled Graeae bosses,
#   the rest are dangling keys (`tagAnomalyA01`, `tagEnemyHarpyB02`, `tagMonsterName190`) whose
#   strings were never authored or were removed. They bank as `tag-unresolved`.
#   11 Monster records carry no `description` field at all (portals, door sequences, ritual
#   shells, test dummies) and bank as `no-tag`.
#   19 records carry a racial profile authored as a bare noun rather than a `Race0NN` key
#   ('Reanimated' on the test dummies, 'Magical', 'Anomaly'). PLUS one genuine GD typo,
#   `Race10` on `chthonic_cultistportal.dbr` -- the taxonomy key is `Race010`. That typo is
#   free-form by the regex and therefore does not halt; it is recorded here because it is a
#   defect in the SOURCE, and a future consumer should not spend an afternoon rediscovering it.
ORACLE_UNRESOLVED_TAGS = 32
ORACLE_NO_TAG = 11
ORACLE_FREEFORM_RACE = 20

# ---- header fields: identity + pointers. These do NOT go into gd_monster_field.
HEADER_POINTER_FIELDS = {
    "description", "characterRacialProfile", "characterAttributeEquations",
    "characterBaseAttackSpeedTag", "characterGenderProfile", "monsterClassification",
    "factions", "controller", "templateName", "charLevel", "Class",
}

# ---- gd_monster_field curated families. Prefix-matched, minus the header pointers above.
FIELD_PREFIXES = ("character", "defensive", "offensive", "skillLevel")
FIELD_EXTRAS = {"minLevel", "maxLevel", "experiencePoints", "angerMultiplier", "causesAnger"}

# ---- canon_key vocabulary. Reuses `monster_numeric.numeric_key` where a concept already exists
#      there; `is_core=1` marks the cross-game concepts, `is_core=0` the GD-specific ones.
#      NOTE ON `defensiveLife`: GD names VITALITY damage "Life" internally. Mapping it to
#      `vitality_resist_pct` rather than to anything life-total-shaped is deliberate; the raw
#      field name is preserved in `raw_field` so the rename is reversible and inspectable.
CANON = {
    "characterLife": ("life", 1), "characterMana": ("mana", 1),
    "characterStrength": ("strength", 1), "characterDexterity": ("dexterity", 1),
    "characterIntelligence": ("intelligence", 1),
    "characterOffensiveAbility": ("accuracy", 1), "characterDefensiveAbility": ("defense", 1),
    "characterLifeRegen": ("life_regen", 1), "characterManaRegen": ("mana_regen", 1),
    "characterAttackSpeed": ("attack_speed_mult", 1),
    "characterRunSpeed": ("run_speed_mult", 1),
    "characterSpellCastSpeed": ("cast_speed_mult", 1),
    "experiencePoints": ("experience", 1),
    "minLevel": ("level_min", 1), "maxLevel": ("level_max", 1),
    "defensiveFire": ("fire_resist_pct", 1), "defensiveCold": ("cold_resist_pct", 1),
    "defensiveLightning": ("lightning_resist_pct", 1),
    "defensivePoison": ("poison_resist_pct", 1), "defensiveChaos": ("chaos_resist_pct", 1),
    "defensivePhysical": ("physical_resist_pct", 1),
    "defensivePierce": ("pierce_resist_pct", 1),
    "defensiveAether": ("aether_resist_pct", 0), "defensiveLife": ("vitality_resist_pct", 0),
    "defensiveStun": ("stun_resist_pct", 0), "defensiveFreeze": ("freeze_resist_pct", 0),
    "defensiveSleep": ("sleep_resist_pct", 0), "defensivePetrify": ("petrify_resist_pct", 0),
    "defensiveTrap": ("trap_resist_pct", 0), "defensiveKnockdown": ("knockdown_resist_pct", 0),
    "characterDodgePercent": ("dodge_pct", 0),
    "characterDeflectProjectile": ("deflect_projectile_pct", 0),
    "characterEnergyAbsorptionPercent": ("energy_absorption_pct", 0),
}

BIO_CANON = {
    "characterLife": "life", "characterMana": "mana",
    "characterStrength": "strength", "characterDexterity": "dexterity",
    "characterIntelligence": "intelligence",
    "characterOffensiveAbility": "accuracy", "characterDefensiveAbility": "defense",
    "characterLifeRegen": "life_regen", "characterManaRegen": "mana_regen",
}

# ---- G3 tier-1 anchor (probe §0.3 / §4)
ANCHOR_PATH = "records/creatures/enemies/zombie_a01.dbr"
ANCHOR_HEADER = dict(
    description_tag="tagEnemyZombieA01", display_name="Walking Dead",
    racial_profile="Race005", race_display="Aether Corruption",
    monster_classification="Common",
    factions_record="records/controllers/factions/faction_aetherial.dbr",
    bio_record="records/creatures/enemies/bios/bio_zombie_01.dbr",
    char_level_expr="charLevel*1", level_min=1, level_max=250)
ANCHOR_BIO = {
    "characterLife": "((charLevel*4)^1.33)+24",
    "characterMana": "((charLevel*8)^1.22)+100",
    "characterStrength": "(charLevel*4.5)+10",
    "characterDexterity": "(charLevel*6.5)+10",
    "characterIntelligence": "(charLevel*6)+15",
    "characterOffensiveAbility": "(charLevel*6)+5",
    "characterDefensiveAbility": "(charLevel*3)+25",
}

DDL = """
CREATE TABLE IF NOT EXISTS gd_monster_record (
    record_path            TEXT NOT NULL,
    source_file            TEXT NOT NULL,
    expansion              TEXT NOT NULL,
    record_type            TEXT NOT NULL,
    description_tag        TEXT,
    display_name           TEXT,
    display_name_status    TEXT NOT NULL
        CHECK (display_name_status IN ('resolved','tag-unresolved','no-tag')),
    display_name_tag_domain TEXT,
    racial_profile         TEXT,
    racial_tag             TEXT,
    race_display           TEXT,
    monster_classification TEXT,
    factions_record        TEXT,
    controller_record      TEXT,
    bio_record             TEXT,
    template_name          TEXT,
    char_level_expr        TEXT,
    level_min              INTEGER,
    level_max              INTEGER,
    experience_points      INTEGER,
    source_version         TEXT NOT NULL,
    fidelity_grade         TEXT NOT NULL,
    adapter                TEXT NOT NULL,
    schema_version         TEXT NOT NULL,
    created_date           TEXT NOT NULL,
    PRIMARY KEY (record_path, source_file)
);
CREATE INDEX IF NOT EXISTS ix_gd_monster_record_tag  ON gd_monster_record (description_tag);
CREATE INDEX IF NOT EXISTS ix_gd_monster_record_name ON gd_monster_record (display_name);
CREATE INDEX IF NOT EXISTS ix_gd_monster_record_bio  ON gd_monster_record (bio_record);

CREATE TABLE IF NOT EXISTS gd_monster_field (
    record_path    TEXT NOT NULL,
    source_file    TEXT NOT NULL,
    raw_field      TEXT NOT NULL,
    raw_value      TEXT NOT NULL,
    value_num      REAL,
    canon_key      TEXT,
    field_family   TEXT NOT NULL,
    is_core        INTEGER,
    schema_version TEXT NOT NULL,
    created_date   TEXT NOT NULL,
    PRIMARY KEY (record_path, source_file, raw_field),
    FOREIGN KEY (record_path, source_file)
        REFERENCES gd_monster_record (record_path, source_file)
);
CREATE INDEX IF NOT EXISTS ix_gd_monster_field_canon ON gd_monster_field (canon_key);

CREATE TABLE IF NOT EXISTS gd_monster_bio (
    bio_record     TEXT NOT NULL,
    source_file    TEXT NOT NULL,
    raw_field      TEXT NOT NULL,
    formula_expr   TEXT NOT NULL,
    canon_key      TEXT,
    source_version TEXT NOT NULL,
    fidelity_grade TEXT NOT NULL,
    adapter        TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    created_date   TEXT NOT NULL,
    PRIMARY KEY (bio_record, source_file, raw_field)
);
"""


def pin_for(rel):
    m = ARCHIVES[rel]
    return (f"{EDITION}; depot={m['depot']}({m['name']}); manifest={m['manifest']}; "
            f"arz_sha256={m['sha256']}")


def verify_edition():
    print("G1 — EDITION PIN (sha256 of every .arz read)")
    ok = True
    for rel, meta in ARCHIVES.items():
        h = hashlib.sha256((BASE / rel).read_bytes()).hexdigest()
        good = h == meta["sha256"]
        ok &= good
        print(f"    {'OK  ' if good else 'FAIL'} {rel:28s} {h[:16]}…  depot={meta['depot']}")
    if not ok:
        raise SystemExit("HALT — .arz bytes do not match the recorded edition pin.")
    print(f"    edition = {EDITION}  (4/4 archives byte-verified)\n")


def load_tags():
    """
    M1's resolved tag table, read back from the DB — the bridge's first hop must use BANKED rows,
    not a re-parse, so that M2 verifies M1's product rather than an independent copy.

    ALL domains, not just `creature`. Monster `description` tags are not confined to
    `tags_creatures.txt`: NPC nameplates live in `tags_storyelements.txt` and breakable-object
    names in `tags_items.txt`. The resolving domain is recorded per row
    (`gd_monster_record.display_name_tag_domain`) so "this nameplate came from the story-element
    table" stays a visible fact rather than being flattened away.
    """
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT tag_key, display_string, tag_domain FROM v_gd_display_tag_resolved").fetchall()
    con.close()
    if not rows:
        raise SystemExit("HALT — v_gd_display_tag_resolved is empty. Run M1 first.")
    tags = {}
    for k, v, d in rows:
        # creature wins ties on the rare cross-domain key; it is the nameplate table of record
        if k not in tags or d == "creature":
            tags[k] = (v, d)
    print(f"    M1 tags loaded from corpus.db: {len(rows)} rows -> {len(tags)} distinct keys\n")
    return tags


def field_family(name):
    for p in ("defensive", "skillLevel", "offensive"):
        if name.startswith(p):
            return p
    if name.startswith("character"):
        return "character"
    return "misc"


def to_num(v):
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    return None


def extract(tags):
    headers, fields, bios = [], [], []
    census, unresolved, no_tag, bad_race = [], [], [], []
    bio_refs = collections.defaultdict(set)     # bio_path -> {source_file that referenced it}
    archives = {}

    for rel, meta in ARCHIVES.items():
        arc = ArzArchive(BASE / rel)
        archives[rel] = arc
        sf, exp, pin = meta["file"], meta["expansion"], pin_for(rel)
        n_mon = n_desc = n_tagpfx = n_bio = 0
        for path, rmeta in arc.records.items():
            if rmeta["rtype"] != "Monster":
                continue
            n_mon += 1
            rec = arc.read_record(path)

            desc = rec.get("description")
            desc = desc if isinstance(desc, str) and desc.strip() else None
            if desc:
                n_desc += 1
                if desc.startswith("tag"):
                    n_tagpfx += 1
            hit = tags.get(desc) if desc else None
            name, name_domain = hit if hit else (None, None)
            if desc is None:
                status, no_tag_row = "no-tag", (sf, path)
                no_tag.append(no_tag_row)
            elif name is None:
                status = "tag-unresolved"
                unresolved.append((sf, path, desc))
            else:
                status = "resolved"

            race = rec.get("characterRacialProfile")
            race = race if isinstance(race, str) and race.strip() else None
            race_tag = f"tag{race}" if race else None
            rhit = tags.get(race_tag) if race_tag else None
            race_disp = rhit[0] if rhit else None
            if race and race_disp is None:
                bad_race.append((sf, path, race))

            bio = rec.get("characterAttributeEquations")
            bio = bio if isinstance(bio, str) and bio.strip() else None
            if bio:
                n_bio += 1
                bio_refs[bio].add(rel)

            def s(k):
                v = rec.get(k)
                return v if isinstance(v, str) and v.strip() else None

            def i(k):
                v = rec.get(k)
                return int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None

            headers.append((
                path, sf, exp, rmeta["rtype"], desc, name, status, name_domain,
                race, race_tag, race_disp, s("monsterClassification"), s("factions"),
                s("controller"), bio, s("templateName"), s("charLevel"),
                i("minLevel"), i("maxLevel"), i("experiencePoints"),
                pin, FIDELITY_GRADE, ADAPTER, SCHEMA_VERSION, RUN_DATE))

            for k, v in rec.items():
                if k in HEADER_POINTER_FIELDS:
                    continue
                if not (k.startswith(FIELD_PREFIXES) or k in FIELD_EXTRAS):
                    continue
                if isinstance(v, list):
                    v = ";".join(str(x) for x in v)
                ck, core = CANON.get(k, (None, None))
                fields.append((path, sf, k, str(v), to_num(v), ck, field_family(k), core,
                               SCHEMA_VERSION, RUN_DATE))
        census.append((sf, len(arc.records), n_mon, n_desc, n_tagpfx, n_bio,
                       meta["oracle_monster"]))

    # ---- bio records: resolve each referenced path against the archives (expansion precedence)
    order = list(ARCHIVES)
    missing_bio = []
    for bio_path in sorted(bio_refs):
        found = None
        for rel in reversed(order):                 # gdx3 -> base: later expansion wins
            if bio_path in archives[rel].records:
                found = rel
                break
        if found is None:
            missing_bio.append(bio_path)
            continue
        arc = archives[found]
        rec = arc.read_record(bio_path)
        for k, v in rec.items():
            if k == "templateName" or not isinstance(v, str) or not v.strip():
                continue
            bios.append((bio_path, ARCHIVES[found]["file"], k, v, BIO_CANON.get(k),
                         pin_for(found), FIDELITY_GRADE, ADAPTER, SCHEMA_VERSION, RUN_DATE))

    stats = dict(census=census, unresolved=unresolved, no_tag=no_tag, bad_race=bad_race,
                 bio_refs=len(bio_refs), missing_bio=missing_bio)
    return headers, fields, bios, stats


def gates(headers, fields, bios, stats):
    print("G2 — CENSUS (vs probe §2)")
    print(f"    {'archive':14s} {'records':>8s} {'Monster':>8s} {'oracle':>7s} "
          f"{'w/desc':>7s} {'tag-pfx':>8s} {'w/bio':>7s}")
    tot_m = tot_d = tot_t = tot_b = 0
    bad = 0
    for sf, nrec, nm, nd, nt, nb, oracle in stats["census"]:
        good = nm == oracle
        bad += not good
        print(f"    {sf:14s} {nrec:8d} {nm:8d} {oracle:7d} {nd:7d} {nt:8d} {nb:7d}  "
              f"{'OK' if good else 'MISMATCH'}")
        tot_m += nm
        tot_d += nd
        tot_t += nt
        tot_b += nb
    print(f"    {'TOTAL':14s} {'':8s} {tot_m:8d} {ORACLE_TOTAL_MONSTER:7d} "
          f"{tot_d:7d} {tot_t:8d} {tot_b:7d}")
    print(f"    oracle: Monster {ORACLE_TOTAL_MONSTER} / w-desc {ORACLE_WITH_DESC} / "
          f"tag-prefixed {ORACLE_WITH_TAG_PREFIX} (probe §2) / bio {ORACLE_WITH_BIO}")
    print(f"    the {ORACLE_WITH_DESC - ORACLE_WITH_TAG_PREFIX}-record gap = "
          f"`xtag`-disabled sandbox Graeae bosses (see module docstring)")
    if bad or tot_m != ORACLE_TOTAL_MONSTER or tot_d != ORACLE_WITH_DESC \
            or tot_t != ORACLE_WITH_TAG_PREFIX or tot_b != ORACLE_WITH_BIO:
        raise SystemExit("HALT — census does not reproduce the probe §2 table.")

    print("\nG3 — TIER-1 ANCHOR (zombie_a01.dbr)")
    cols = ("record_path", "source_file", "expansion", "record_type", "description_tag",
            "display_name", "display_name_status", "display_name_tag_domain",
            "racial_profile", "racial_tag",
            "race_display", "monster_classification", "factions_record", "controller_record",
            "bio_record", "template_name", "char_level_expr", "level_min", "level_max",
            "experience_points")
    anchor = [h for h in headers if h[0] == ANCHOR_PATH and h[1] == "database.arz"]
    if len(anchor) != 1:
        raise SystemExit(f"HALT — anchor record not found exactly once ({len(anchor)}).")
    a = dict(zip(cols, anchor[0]))
    nbad = 0
    for k, expect in ANCHOR_HEADER.items():
        good = a[k] == expect
        nbad += not good
        print(f"    {'PASS' if good else 'FAIL'} {k:24s} = {a[k]!r}")
    biorows = {r[2]: r[3] for r in bios if r[0] == ANCHOR_BIO_PATH}
    for k, expect in ANCHOR_BIO.items():
        good = biorows.get(k) == expect
        nbad += not good
        print(f"    {'PASS' if good else 'FAIL'} bio.{k:20s} = {biorows.get(k)!r}")
    if nbad:
        raise SystemExit("HALT — tier-1 anchor mismatch.")

    print("\nG4 — RESOLUTION COVERAGE")
    st = collections.Counter(h[6] for h in headers)
    dom = collections.Counter(h[7] for h in headers if h[7])
    print(f"    display_name_status: {dict(st)}")
    print(f"    resolving tag domain: {dict(dom)}")
    print(f"    tag present but UNRESOLVED against M1 : {len(stats['unresolved'])}")
    for r in stats["unresolved"][:10]:
        print(f"        {r}")
    print(f"    NO description tag at all             : {len(stats['no_tag'])}")
    for r in stats["no_tag"][:20]:
        print(f"        {r}")
    # Race-lane classification. A `Race\d{3}` that fails to resolve is a BROKEN JOIN and halts.
    # A racial profile authored as a bare noun ('Reanimated', 'Magical', 'Anomaly') is not broken
    # -- it is GD content authored outside the Race0NN taxonomy, and it resolves to nothing by
    # construction. Halting on it would be gating on my own assumption about how GD authors data.
    wellformed = [r for r in stats["bad_race"] if re.fullmatch(r"Race\d{3}", r[2])]
    freeform = [r for r in stats["bad_race"] if r not in wellformed]
    print(f"    characterRacialProfile that does NOT resolve to a tagRace… entry: "
          f"{len(stats['bad_race'])}")
    print(f"        well-formed Race0NN that FAILED to resolve : {len(wellformed)} "
          f"(must be 0 — a broken join)")
    for r in wellformed:
        print(f"            {r}")
    print(f"        free-form racial nouns (never in the Race0NN taxonomy) : {len(freeform)} "
          f"(oracle {ORACLE_FREEFORM_RACE}) — "
          f"{sorted({r[2] for r in freeform})}")
    if wellformed:
        raise SystemExit("HALT — a well-formed Race0NN failed to resolve; the race lane is broken.")
    if len(freeform) != ORACLE_FREEFORM_RACE:
        raise SystemExit("HALT — free-form racial-noun count moved off the regression oracle.")

    print(f"\n    UNRESOLVED description tags : {len(stats['unresolved'])} "
          f"(oracle {ORACLE_UNRESOLVED_TAGS})")
    if len(stats["unresolved"]) != ORACLE_UNRESOLVED_TAGS:
        raise SystemExit("HALT — unresolved-tag count moved off the regression oracle.")
    if len(stats["no_tag"]) != ORACLE_NO_TAG:
        raise SystemExit("HALT — no-tag count moved off the regression oracle.")

    print(f"\n    distinct bio records referenced : {stats['bio_refs']}")
    print(f"    bio records NOT FOUND in any archive : {len(stats['missing_bio'])}")
    for b in stats["missing_bio"][:10]:
        print(f"        {b}")
    print(f"\n    gd_monster_record rows : {len(headers)}")
    print(f"    gd_monster_field  rows : {len(fields)}")
    print(f"    gd_monster_bio    rows : {len(bios)}\n")


ANCHOR_BIO_PATH = "records/creatures/enemies/bios/bio_zombie_01.dbr"


def apply(headers, fields, bios):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak = DB.with_name(DB.name + f".pre-bridge-m2-{ts}-backup")
    shutil.copy2(DB, bak)
    md5 = hashlib.md5(bak.read_bytes()).hexdigest()
    bak.with_name(bak.name + ".md5.txt").write_text(f"{md5}  {bak.name}\n")
    print(f"BACKUP {bak.name} md5={md5}")

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    try:
        con.executescript(DDL)
        con.execute("BEGIN")
        con.execute("DELETE FROM gd_monster_field WHERE schema_version = ?", (SCHEMA_VERSION,))
        con.execute("DELETE FROM gd_monster_bio   WHERE schema_version = ?", (SCHEMA_VERSION,))
        con.execute("DELETE FROM gd_monster_record WHERE schema_version = ?", (SCHEMA_VERSION,))
        con.executemany("INSERT INTO gd_monster_record VALUES (" + ",".join("?" * 25) + ")",
                        headers)
        con.executemany("INSERT INTO gd_monster_field VALUES (" + ",".join("?" * 10) + ")",
                        fields)
        con.executemany("INSERT INTO gd_monster_bio VALUES (" + ",".join("?" * 10) + ")", bios)
        con.execute(
            "INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
            (SCHEMA_VERSION + "/M2",
             datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
             f"GD display-name bridge M2 (elrond). ADDITIVE: gd_monster_record ({len(headers)}), "
             f"gd_monster_field ({len(fields)}), gd_monster_bio ({len(bios)}). FIRST GD monster "
             "extraction from primary source — corpus.db previously held ZERO GD monster rows. "
             "Full-bestiary scope (all 4,066 Monster records, not the tag-resolvable subset); "
             "census reproduces probe §2 exactly (1307/737/1064/958; 4052 tagged; 4050 bio). "
             "Grade DATAMINED; edition gd-edition-II-20260724; 4/4 .arz sha256-verified. "
             "NOT written to monster_numeric (community-harvest surface, NOT NULL source_url) — "
             "canon_key reuses that vocabulary so a later normalization lap can promote."))
        con.commit()
    except Exception:
        con.rollback()
        raise
    for t in ("gd_monster_record", "gd_monster_field", "gd_monster_bio"):
        print(f"    {t:20s} {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")
    print("integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
    print("fk_check :", con.execute("PRAGMA foreign_key_check").fetchall() or "clean")
    con.close()


def main():
    verify_edition()
    tags = load_tags()
    headers, fields, bios, stats = extract(tags)
    gates(headers, fields, bios, stats)
    if "--verify-only" in sys.argv:
        print("--verify-only: NO DB writes.")
        return
    apply(headers, fields, bios)


if __name__ == "__main__":
    main()
