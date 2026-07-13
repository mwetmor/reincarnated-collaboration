#!/usr/bin/env python3
"""
Corpus FOLD 1 + FOLD 2 — mint-dossier corrections + engine-key plane-keying.

Authority: gandalf returns-adjudication of elrond S1
  (agentic_orchestration/gandalf/notes/2026-07-13-returns-adjudication-elrond-s1-legolas-mint.md)
Source of record: legolas 9-mint-dossier series (commit aaa519d6)
  agentic_orchestration/legolas/findings/mint-dossiers-paste-ready-2026-07-13/
DB: agentic_orchestration/research/curated/corpus.db (gitignored, schema_meta 2.1 -> 2.2)
MIGRATION entry: v2.2

Runs AFTER corpus_completion_s1_2026_07_13.py in the D6 rebuild sequence.
Idempotent: ADD COLUMN pragma-guarded; pure-UPDATE backfills; engine_key inserts
scoped to the 9 mint kit_ids via INSERT OR REPLACE. Clean rebuild => byte-identical.

FOLD 1 (data corrections):
  1a  rename poe1-ring-of-shields -> le-ring-of-shields (kit_id + game field);
      Last Epoch Forge Guard skill, 2-source confirmed game-attribution error.
  1b  d3-call-of-the-ancients vs d3-ik-hota: RULED DISTINCT -- no dedup (verify both stand).
  1c  d2-sacrifice: negative=1 (KEEP; joins negative-canon family, excluded from
      S6 certification population, NOT deleted).
  1d  ingest 9 dossiers' stabilization_patch + skill_debut_year + source_urls;
      clear dossier_owed. (era_year left at P5 game-level -- see STEWARD NOTE below.)

FOLD 2 (plane-keying): add canon_engine_key rows so the mint kits PLOT.
  7 combat-kit  (geometry traced to dossier mechanical text):
    poe1-totem-hierophant   totem        full-move   -> SUMMON
    d3-call-of-the-ancients totem        full-move   -> SUMMON
    le-ring-of-shields      <orbit>      full-move   -> ORBITAL*
    d3-dashing-strike-monk  dash_attack  full-move   -> MELEE
    le-shift-bladedancer    dash_attack  full-move   -> MELEE
    poe1-vaal-blade-vortex  <orbit>      full-move   -> ORBITAL*
    d2-sacrifice            melee_strike walk        -> MELEE  (also negative=1)
  2 system-record (NOT a delivery skill -- honest off-plane classification):
    poe1-blood-magic-kit    <null geo>   full-move   route=resource-economy
    d2-teleport-sorc        <null geo>   full-move   route=mobility-grammar

  * orbit kits carry geometry_value=NULL + flags=["gx-candidate:orbit"] (DDL-legal).
    They key cleanly but render UNMAPPED until gandalf adds them to the renderer's
    UNMAPPED_COL hardcode (render-spec follow-up -- see fold log).

STEWARD NOTE (era_year): FOLD 1d header names "era_year"; the parenthetical notes P5
already filled era_year corpus-wide (per-GAME release year). The dossiers carry a
per-SKILL DEBUT year (e.g. d2-sacrifice 2001 vs game-level d2 2000; CotA 2017 vs d3 2012).
To avoid mixing two semantics in one column, era_year is LEFT at P5 game-level and the
dossier skill-debut year is captured in a NEW column `skill_debut_year`. Both signals
preserved; column semantics stay clean. Flagged to gandalf for ratification.

Every backfill traces to the dossier index / URL manifest. Where a dossier field is
genuinely absent (VBV + Sacrifice stabilization_patch), honest-NULL -- never invented.
"""
import json
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "curated" / "corpus.db"

RING_OLD = "poe1-ring-of-shields"
RING_NEW = "le-ring-of-shields"

# The 9 mint kits (post-rename ids).
MINT9 = [
    "poe1-totem-hierophant",
    "d3-call-of-the-ancients",
    RING_NEW,
    "poe1-blood-magic-kit",
    "d2-teleport-sorc",
    "d3-dashing-strike-monk",
    "le-shift-bladedancer",
    "poe1-vaal-blade-vortex",
    "d2-sacrifice",
]

# --- FOLD 1d dossier fields (index table, commit aaa519d6) ---
# kit_id -> (stabilization_patch, skill_debut_year)
# NOTE: patch tokens are stored BARE (no leading "v"). The renderer's
# build_public_label() prepends "v" (line ~227: f" (v{patch})"), so a stored
# "v2.6.1" would render "vv2.6.1". Store "2.6.1"; renderer supplies the "v".
DOSSIER_META = {
    "poe1-totem-hierophant":   ("2.3.0", 2016),
    "d3-call-of-the-ancients": ("2.6.1", 2017),
    RING_NEW:                  ("1.0",   2024),
    "poe1-blood-magic-kit":    ("2.0.0", 2015),
    "d2-teleport-sorc":        ("1.10",  2003),
    "d3-dashing-strike-monk":  ("2.4.2", 2016),
    "le-shift-bladedancer":    ("1.0",   2024),
    "poe1-vaal-blade-vortex":  (None,    2016),  # honest-NULL patch
    "d2-sacrifice":            (None,    2001),  # honest-NULL patch
}

# le game-level era_year (P5 GAME_ERA_YEAR). After the 1a game rename poe1->le,
# era_year must move off the stale poe1 game-level (2013) to the le game-level (2024).
LE_GAME_ERA_YEAR = 2024

# --- FOLD 1d URL backfill manifest (url-backfill-manifest-2026-07-13.md) ---
SOURCE_URLS = {
    "poe1-totem-hierophant": [
        "https://www.poewiki.net/wiki/Ancestral_Warchief",
        "https://www.poewiki.net/wiki/Ancestral_Protector",
        "https://www.pathofexile.com/forum/view-thread/2769163",
        "https://www.angryroleplayer.com/path-of-exile-builds/ancestral-warchief-chieftain-path-of-exile-build/",
    ],
    "d3-call-of-the-ancients": [
        "https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king",
        "https://maxroll.gg/d3/guides/ik-hota-barbarian-guide",
        "https://www.diablofans.com/builds/101972-s16-immortal-king-hammer-of-the-ancients",
    ],
    RING_NEW: [
        "https://lastepoch.fandom.com/wiki/Ring_of_Shields",
        "https://www.lastepochtools.com/skills/ring_of_shields",
        "https://www.lastepochtools.com/skills/ring_of_shields/nodes",
        "https://forum.lastepoch.com/t/ring-of-shields-and-forge-guard-interactions/71851",
    ],
    "poe1-blood-magic-kit": [
        "https://www.poewiki.net/wiki/Blood_Magic",
        "https://pathofexile.fandom.com/wiki/Blood_Magic",
        "http://www.vhpg.com/blood-magic/",
    ],
    "d2-teleport-sorc": [
        "https://eu.forums.blizzard.com/en/d2r/t/the-enigmateleport-problem-a-solution/17407",
        "https://diablo2.diablowiki.net/Guide:Blizzard_Sorceress_v1.10,_by_Zhao_Yue",
        "https://diablo-archive.fandom.com/wiki/Patch_1.10_(Diablo_II)",
        "https://maxroll.gg/d2/guides/lightning-sorceress",
    ],
    "d3-dashing-strike-monk": [
        "https://www.icy-veins.com/d3/barbarian-immortal-kings-call-fresh-70-starter-build",
        "https://maxroll.gg/d3/guides/ik-hota-barbarian-guide",
    ],
    "le-shift-bladedancer": [
        "https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide",
        "https://maxroll.gg/last-epoch/build-guides/shadow-cascade-bladedancer-guide",
        "https://maxroll.gg/last-epoch/build-guides/dancing-strikes-bladedancer-guide",
    ],
    "poe1-vaal-blade-vortex": [
        "https://www.poewiki.net/wiki/Vaal_Blade_Vortex",
        "https://pathofexile.fandom.com/wiki/Vaal_Blade_Vortex",
        "https://www.poe-vault.com/items/vaal-blade-vortex",
        "https://pobarchives.com/builds?mainSkill=Vaal+Blade+Vortex",
    ],
    "d2-sacrifice": [
        "https://diablo.fandom.com/wiki/Sacrifice_(Diablo_II)",
        "https://diablo2.diablowiki.net/Sacrifice",
        "https://www.purediablo.com/d2wiki/Sacrifice",
        "https://odealo.com/articles/sacrifice-paladin-build-guide-for-pd2",
    ],
}

# --- FOLD 2 engine-key rows (geometry traced to dossier mechanical text) ---
# kit_id -> dict(row_class, geometry_value, mob_policy, route, flags, mob_is_move, geo_desc, mob_desc)
FOLD2 = {
    "poe1-totem-hierophant": dict(
        row_class="combat-kit", geometry_value="totem", mob_policy="full-move",
        route=None, flags=[], mob_is_move=0,
        geo_desc="at-target totem placement; ancestral totems persist, wide ground-slam",
        mob_desc="FULL mobility while totems persist"),
    "d3-call-of-the-ancients": dict(
        row_class="combat-kit", geometry_value="totem", mob_policy="full-move",
        route=None, flags=[], mob_is_move=0,
        geo_desc="at-target summon; 3 ancestors roam a large zone (proxy economy)",
        mob_desc="full movement freedom during CotA"),
    RING_NEW: dict(
        row_class="combat-kit", geometry_value=None, mob_policy="full-move",
        route=None, flags=["gx-candidate:orbit"], mob_is_move=0,
        geo_desc="orbit delivery: shields form a rotating ring at fixed radius, follows player",
        mob_desc="full movement freedom; ring orbits with player"),
    "d3-dashing-strike-monk": dict(
        row_class="combat-kit", geometry_value="dash_attack", mob_policy="full-move",
        route=None, flags=[], mob_is_move=1,
        geo_desc="self-origin lane delivery; player body as projectile, carves a lane",
        mob_desc="maximum mobility; Dashing Strike is mobility AND primary damage"),
    "le-shift-bladedancer": dict(
        row_class="combat-kit", geometry_value="dash_attack", mob_policy="full-move",
        route=None, flags=[], mob_is_move=1,
        geo_desc="self-origin lane dash striking enemies in lane; blade trails persist",
        mob_desc="maximum mobility; Shift invuln frames"),
    "poe1-vaal-blade-vortex": dict(
        row_class="combat-kit", geometry_value=None, mob_policy="full-move",
        route=None, flags=["gx-candidate:orbit"], mob_is_move=0,
        geo_desc="self-origin homing-vortex blade cloud; semi-proxy orbiting movement",
        mob_desc="full mobility during BV and VBV"),
    "d2-sacrifice": dict(
        row_class="combat-kit", geometry_value="melee_strike", mob_policy="walk",
        route=None, flags=[], mob_is_move=0,
        geo_desc="at-target single-hit melee strike; single-target point delivery",
        mob_desc="standard movement; walk to enemy + hit"),
    # --- off-plane: NOT delivery skills -> system-record (honest non-combat class) ---
    "poe1-blood-magic-kit": dict(
        row_class="system-record", geometry_value=None, mob_policy="full-move",
        route="resource-economy", flags=["resolved:system-record"], mob_is_move=0,
        geo_desc="NOT a delivery skill: life-as-resource keystone/economy grammar",
        mob_desc="varies by chassis; economy keystone, not a placed geometry"),
    "d2-teleport-sorc": dict(
        row_class="system-record", geometry_value=None, mob_policy="full-move",
        route="mobility-grammar", flags=["resolved:system-record"], mob_is_move=1,
        geo_desc="NOT a damage-delivery skill: movement identity (Teleport IS the verb)",
        mob_desc="maximum mobility; entire identity is mobility"),
}

FOLD_TAG = "mint-dossier-fold12-2026-07-13"


def has_column(con, table, col):
    return col in {r[1] for r in con.execute(f"PRAGMA table_info({table})")}


def add_column(con, table, col, decl):
    if not has_column(con, table, col):
        con.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
        print(f"  + ADD COLUMN {table}.{col} {decl}")
    else:
        print(f"  = {table}.{col} present (idempotent skip)")


def main():
    con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys=OFF")  # PK rename cascade handled manually
    cur = con.cursor()

    print(f"DB: {DB}")
    print("=== FOLD 1 — data corrections ===")

    # ---- 1a rename poe1-ring-of-shields -> le-ring-of-shields (idempotent) ----
    have_old = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", (RING_OLD,)).fetchone()[0]
    have_new = cur.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", (RING_NEW,)).fetchone()[0]
    if have_old and not have_new:
        # cascade every table that keys on kit_id (probe_facts has 0 rows for mint; engine_key none yet)
        # game poe1->le AND era_year off the stale poe1 game-level (2013) to le game-level (2024)
        cur.execute("UPDATE canon_corpus  SET kit_id=?, game='le', era_year=? WHERE kit_id=?",
                    (RING_NEW, LE_GAME_ERA_YEAR, RING_OLD))
        cur.execute("UPDATE canon_probe_facts SET kit_id=? WHERE kit_id=?", (RING_NEW, RING_OLD))
        cur.execute("UPDATE canon_engine_key  SET kit_id=? WHERE kit_id=?", (RING_NEW, RING_OLD))
        print(f"  1a rename: {RING_OLD} -> {RING_NEW} (game poe1 -> le, era_year -> {LE_GAME_ERA_YEAR})")
    elif have_new and not have_old:
        # idempotent: ensure era_year is the le game-level even on re-run
        cur.execute("UPDATE canon_corpus SET era_year=? WHERE kit_id=? AND era_year<>?",
                    (LE_GAME_ERA_YEAR, RING_NEW, LE_GAME_ERA_YEAR))
        print(f"  1a rename: already applied ({RING_NEW} present) — idempotent skip")
    else:
        raise SystemExit(f"1a ABORT: unexpected ring state old={have_old} new={have_new}")

    # ---- 1b CotA vs IK-HotA: verify both stand, no dedup ----
    cota = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE kit_id='d3-call-of-the-ancients'").fetchone()[0]
    hota = cur.execute("SELECT COUNT(*) FROM canon_corpus WHERE kit_id='d3-ik-hota'").fetchone()[0]
    assert cota == 1 and hota == 1, f"1b RULED-DISTINCT violated: cota={cota} hota={hota}"
    print(f"  1b CotA + IK-HotA both stand (no dedup) — cota={cota} hota={hota} OK")

    # ---- 1c d2-sacrifice negative=1 (KEEP) ----
    cur.execute("UPDATE canon_corpus SET negative=1 WHERE kit_id='d2-sacrifice'")
    print("  1c d2-sacrifice negative=1 (joins negative-canon family)")

    # ---- 1d columns + backfill ----
    add_column(con, "canon_corpus", "skill_debut_year", "INTEGER")
    add_column(con, "canon_corpus", "source_urls", "TEXT")  # JSON array
    for kid in MINT9:
        patch, debut = DOSSIER_META[kid]
        urls = json.dumps(SOURCE_URLS[kid])
        cur.execute(
            "UPDATE canon_corpus SET stabilization_patch=?, skill_debut_year=?, "
            "source_urls=?, dossier_owed=0 WHERE kit_id=?",
            (patch, debut, urls, kid))
    filled_patch = sum(1 for kid in MINT9 if DOSSIER_META[kid][0] is not None)
    print(f"  1d ingested 9 dossiers: skill_debut_year 9/9; stabilization_patch {filled_patch}/9 "
          f"(2 honest-NULL: VBV + Sacrifice); source_urls 9/9; dossier_owed cleared 9/9")

    print("=== FOLD 2 — plane-keying (canon_engine_key inserts) ===")
    for kid, spec in FOLD2.items():
        geo = spec["geometry_value"]
        flags = json.dumps(spec["flags"])
        prov = json.dumps({
            "source": FOLD_TAG,
            "authority": "gandalf returns-adjudication 2026-07-13",
            "geo_descriptor": spec["geo_desc"],
            "mob_descriptor": spec["mob_desc"],
            "geometry_rule_fired": "mint-dossier-curation",
        })
        raw = json.dumps({
            "kit_id": kid, "source": FOLD_TAG,
            "row_class": spec["row_class"], "geometry_value": geo,
            "mob_policy_while_casting": spec["mob_policy"], "route": spec["route"],
            "flags": spec["flags"],
        })
        cur.execute(
            "INSERT OR REPLACE INTO canon_engine_key "
            "(kit_id, geometry_value, geometry_rule_fired, geometry_conf, "
            " mob_skill_is_movement, mob_policy_while_casting, "
            " row_class, route, flags, provenance_json, raw_json, delivery_value) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (kid, geo, FOLD_TAG, (0.70 if spec["row_class"] == "combat-kit" else None),
             spec["mob_is_move"], spec["mob_policy"],
             spec["row_class"], spec["route"], flags, prov, raw, None))
        col = ("ORBITAL*" if "gx-candidate:orbit" in spec["flags"]
               else ("system-record" if spec["row_class"] == "system-record" else geo))
        print(f"  + {kid:26s} {spec['row_class']:13s} geo={str(geo):12s} mob={spec['mob_policy']:9s} -> {col}")

    con.commit()

    # ================= VERIFICATION =================
    print("=== VERIFICATION ===")

    def one(q, p=()):
        return cur.execute(q, p).fetchone()[0]

    corpus_n = one("SELECT COUNT(*) FROM canon_corpus")
    ek_n = one("SELECT COUNT(*) FROM canon_engine_key")
    combat_n = one("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit'")
    sysrec_n = one("SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record'")
    canon_combat = one(
        "SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c ON k.kit_id=c.kit_id "
        "WHERE k.row_class='combat-kit' AND c.mint=0")
    neg_n = one("SELECT COUNT(*) FROM canon_corpus WHERE negative=1")
    mint_keyed = one(
        "SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c ON k.kit_id=c.kit_id "
        "WHERE c.mint=1")
    ring_old = one("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", (RING_OLD,))
    ring_new = one("SELECT game FROM canon_corpus WHERE kit_id=?", (RING_NEW,)) if \
        one("SELECT COUNT(*) FROM canon_corpus WHERE kit_id=?", (RING_NEW,)) else None
    owed = one("SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1")

    # cone Path-2 split must be untouched (no new row is a cone)
    beam = one("SELECT COUNT(*) FROM canon_engine_key WHERE geometry_value='cone' AND delivery_value='beam'")
    proj = one("SELECT COUNT(*) FROM canon_engine_key WHERE geometry_value='cone' AND delivery_value='projectile'")

    checks = [
        ("corpus rows unchanged (524)", corpus_n, 524),
        ("engine_key 478 + 9 = 487", ek_n, 487),
        ("combat-kit 463 + 7 = 470", combat_n, 470),
        ("system-record 15 + 2 = 17", sysrec_n, 17),
        ("CANON combat (mint=0) still 463", canon_combat, 463),
        ("negative 37 + 1 = 38", neg_n, 38),
        ("all 9 mint kits keyed", mint_keyed, 9),
        ("ring OLD id gone", ring_old, 0),
        ("ring NEW game=le", ring_new, "le"),
        ("dossier_owed all cleared", owed, 0),
        ("cone Path-2 BEAM untouched (5)", beam, 5),
        ("cone Path-2 PROJECTILE untouched (6)", proj, 6),
    ]
    ok = True
    for label, got, want in checks:
        flag = "OK " if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"  [{flag}] {label}: {got} (expect {want})")

    if not ok:
        raise SystemExit("VERIFICATION FAILED")
    print("=== ALL GATES PASSED ===")
    con.close()


if __name__ == "__main__":
    main()
