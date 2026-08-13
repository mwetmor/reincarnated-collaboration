#!/usr/bin/env python3
"""KC2-PM3 Lap C -- decode the FOUR measured Crucible purchases into a stat contract. READ-ONLY.

Lineage: reuses `pm2b_lib_2026_08_12` (Lap B) unchanged for the overlay stack (`s2_lib.E3`,
Edition-III corpus, 8-archive last-wins merge), for the TEMPLATE-DERIVED offensive taxonomy
(`pm2b_lib.TAX`, IS-1) and for `evaleq` / `at_rank` (IS-2). Nothing about the corpus basis is
re-declared here; it is imported.

WHAT IS MEASURED WHERE (GL-12 -- decode, never estimate)
  * WHICH four things were bought  -> MEASURED FROM VIDEO PIXELS (`pm3c_video_2026_08_12`):
    the Defense-Site dialog text visible at the frame of each tribute decrement, plus the
    tribute counter stepping 145 -> 140 -> 135 -> 130 -> 125 at t = 477 / 484 / 502 / 510 s.
    The dialog's own prose is joined to the record by the record's `description` localization
    tag (`tagDefense_Turret01/02/03`, `tagDefense_Banner01/02`) -- a game-authored identity
    join, not a name guess.
  * WHAT each thing does           -> DECODED FROM the .arz records reached from that creature.
  * COSTS                          -> read off the dialog string in-frame
    ("Requires 5 Crucible Tributes and 10000 Iron Bits").
  * THE ARENA HAS EXACTLY FOUR DEFENCE POINTS -> decoded from the Crucible's own Lua,
    `mods/survivalmode/resources/Scripts.arc :: game/survival/defenses.lua`
    (`defensePointId = {0,0,0,0}`; state enum `0 none / 1 BannerDefense / 2 BannerOffense /
    3 TurretFire / 4 TurretIce / 5 TurretLightning / 6 Wall`). Matt's four purchases therefore
    filled every site the arena has.

INSTRUMENT SCHEMA
  IS-B1  Effect rows are emitted for every field on a reached record that (a) is in a gameplay
         field family and (b) carries a nonzero / non-False value. A shipped 0.0 is Crate's
         template default, not a contract term, and is NOT a row.
  IS-B2  `applies_to` is DECLARED from the record's own role in the chain, never inferred from
         the stat's name:
             creature `skillNameN` where the target Class is a Skill_Buff*  -> aura on allies
                 inside `skillTargetRadius` (the player is an ally of a player-built defence)
             `*_petbonus` reached via `<buff>.petBonusName`                 -> pets only
             creature `attackSkillName` / `specialAttackSkillName`          -> enemies
             `characterAttributeEquations` bio chain                        -> the object itself
  IS-B3  RANK. Every array field is resolved at the rank the CREATURE RECORD ITSELF declares
         (`skillLevelN` beside the matching `skillNameN`), evaluated with `pm2b_lib.evaleq`.
         Emitted columns: `rank_equation`, `rank_used`, `value_at_rank`, `value_raw_array`.
         The banner grants its aura at `skillLevel3 = 1` -- a LITERAL, so the banner contract is
         rank-EXACT with no free parameter. The turrets grant theirs at `charLevel/4+1`, which
         needs `charLevel`; see CLIFF C-2 in the lap README. `CHAR_LEVEL` below is the DECLARED
         basis for the turret read and is printed on every affected row.
  IS-B4  TIER identity. The purchases were tier-1: each cost 5 tributes (dialog text, in-frame)
         and the tribute counter never moved again for the remaining 358 s of the capture, so no
         upgrade was bought. Tier-1 == the un-suffixed record; the Lua's `defensePointDbrs` /
         `...Upgrade01` / `...Upgrade02` tables prove the three-record ladder directly.
  IS-B5  The four CELESTIAL BLESSINGS are decoded too and carried in the same CSV with
         `purchase_n = 0` and `[NOT PURCHASED - measured]` in the name. They are the fold's
         BLESSINGS-ON arm; the reference run is BLESSINGS-OFF.
"""
import sys
import csv
import math
import pathlib
import collections

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-12-kc2-roster-decode-completion")
from s2_lib import E3, ROOT                              # noqa: E402
import pm2b_lib_2026_08_12 as L                          # noqa: E402
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file   # noqa: E402

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "notes/2026-08-12-kc2-pm3-lap-c-blessings-reference-dot")

# DECLARED basis for the turret rank equation `charLevel/4+1`. Player level 100 is MEASURED from
# the main-menu character card at video t=30 ("EoRWarlGuts / Level 100 Warlord"). The BINDING of a
# player-built defence's charLevel to the player's level is NOT decoded -- CLIFF C-2.
CHAR_LEVEL = 100.0

PURCHASES = [
    dict(n=1, t=477, name="Deathchill Beacon",  root="records/creatures/defenses/turret_ice.dbr"),
    dict(n=2, t=484, name="Stormcaller Beacon", root="records/creatures/defenses/turret_lightning.dbr"),
    dict(n=3, t=502, name="Inferno Beacon",     root="records/creatures/defenses/turret_fire.dbr"),
    dict(n=4, t=510, name="Vanguard Banner",    root="records/creatures/defenses/banner_offense.dbr"),
]
TRIBUTE_COST = 5
IRONBITS_COST = 10000

BLESSINGS = [
    ("Blessing of Ulo",     "records/skills/powerups/blessingulo.dbr"),
    ("Empyrion's Guidance", "records/skills/powerups/empyrionguidance.dbr"),
    ("Might of Amatok",     "records/skills/powerups/mightamatok.dbr"),
    ("Ulzuin's Pact",       "records/skills/powerups/ulzuinpact.dbr"),
]

TAG_ARCS = ["resources/Text_EN.arc", "gdx1/resources/Text_EN.arc", "gdx2/resources/Text_EN.arc",
            "gdx3/resources/Text_EN.arc", "mods/survivalmode/resources/Text_EN.arc",
            "survivalmode1/resources/Text_EN.arc", "survivalmode3/resources/Text_EN.arc"]


def load_tags():
    t = {}
    for rel in TAG_ARCS:
        a = ArcArchive(ROOT / rel)
        for f in a.names():
            if f.lower().endswith(".txt"):
                try:
                    t.update(dict(parse_tag_file(a.read_file(f))))
                except Exception:
                    pass
    return t


TAGS = load_tags()

PREFIX = ("character", "defensive", "offensive", "retaliation", "pet", "skill", "projectile")
SKIP_EXACT = {"characterBaseAttackSpeedTag", "characterGenderProfile", "characterRacialProfile",
              "characterAttributeEquations", "skillUpBitmapName", "skillDownBitmapName",
              "skillActivatedSound", "skillDeactivatedSound", "skillDisplayName",
              "skillBaseDescription", "skillConnectionSound", "skillMasteryLevelRequired",
              "skillTier", "skillProjectileName", "skillHitSound", "skillSpecialAnimationName"}
SKIP_SUFFIX = ("BitmapName", "Sound", "SoundName", "Anim", "AnimSpeed", "AnimWeight",
               "Texture", "FxPak", "Mesh", "PakName", "PakNames")


def gameplay(k, v):
    if k in SKIP_EXACT or not k.startswith(PREFIX):
        return False
    if any(k.endswith(s) for s in SKIP_SUFFIX):
        return False
    if isinstance(v, bool) or isinstance(v, str):
        return False
    if isinstance(v, list):
        return any(isinstance(x, (int, float)) and x != 0 for x in v)
    return isinstance(v, (int, float)) and v != 0


def group_of(k):
    grp, base, aspect, kind = L.TAX.split(k)
    if grp:
        return grp, kind
    for pre, g, ki in (("defensive", "Defensive (parameters_defensive.tpl)", "defense"),
                       ("character", "Character (parameters_character.tpl)", "character"),
                       ("retaliation", "Retaliation (parameters_retaliation.tpl)", "retaliation"),
                       ("skill", "Skill control (Skill_Base.tpl)", "skill_control"),
                       ("projectile", "Projectile (Skill_Projectile.tpl)", "projectile")):
        if k.startswith(pre):
            return g, ki
    return "", "other"


def rows_for_record(path, applies_to, delivery, ctx, rank_eq=None, rank_used=None):
    r, arcs = E3.merged(path)
    if r is None:
        return [dict(ctx, effect_record=path, stat="", value_at_rank="",
                     rank_basis="DECLARED-ABSENT",
                     note="record not present in the Edition-III overlay")]
    dur = r.get("skillActiveDuration")
    disp = TAGS.get(r.get("skillDisplayName", ""), "")
    desc = TAGS.get(r.get("skillBaseDescription", ""), "")
    out = []
    for k, v in sorted(r.items()):
        if not gameplay(k, v):
            continue
        grp, kind = group_of(k)
        if isinstance(v, list):
            val, grade = L.at_rank(v, rank_used)
            raw = "|".join(str(x) for x in v)
            basis = f"ARRAY[{len(v)}]@rank{rank_used}:{grade}" if rank_used else f"ARRAY[{len(v)}]:NO-RANK"
        else:
            val, raw, basis = float(v), "", "SCALAR"
        out.append(dict(ctx, effect_record=path, effect_archives="|".join(arcs),
                        effect_display_name=disp, effect_description=desc,
                        stat=k, stat_group=grp, stat_kind=kind,
                        value_at_rank=val, value_raw_array=raw,
                        applies_to=applies_to, delivery=delivery,
                        rank_equation=rank_eq or "", rank_used=rank_used if rank_used else "",
                        skill_active_duration_s=dur if dur else "",
                        skill_target_radius_units=("resolved in its own row"
                                                   if "skillTargetRadius" in r else ""),
                        rank_basis=basis, note=""))
    return out


# Class -> who the record's stats land on. MEASURED from the Class string, which is a `static`
# template field (Crate declares it, the DBR cannot override it), so this table is a decode of
# Crate's own taxonomy, not a naming guess.
#   Skill_Passive              -> a self-passive on the carrier (armour, CC immunity)
#   Skill_BuffRadius*          -> an EMITTER; it holds no stats, its buffSkillName child does
#   SkillBuff_Passive          -> the payload; lands on whoever the emitter targets
SELF_CLASSES = ("Skill_Passive",)
EMITTER_CLASSES = ("Skill_BuffRadiusToggled", "Skill_BuffRadius", "Skill_BuffOther",
                   "Skill_BuffSelf", "Skill_BuffSelfDuration")
ALLY = "allies in radius (the player is an ally of a player-built defence)"


def walk_creature(p):
    r, _ = E3.merged(p["root"])
    base = dict(purchase_n=p["n"], purchase_name=p["name"], purchase_video_t=p["t"],
                tribute_cost=TRIBUTE_COST, ironbits_cost=IRONBITS_COST,
                source_record=p["root"],
                source_display_name=TAGS.get(r.get("description", ""), "") if r else "")
    rows = []
    if r is None:
        return [dict(base, effect_record=p["root"], rank_basis="DECLARED-ABSENT",
                     note="creature record absent")]

    bio = r.get("characterAttributeEquations")
    if isinstance(bio, str) and bio.endswith(".dbr"):
        b, barcs = E3.merged(bio)
        if b:
            for k, v in sorted(b.items()):
                if k.startswith("character") and isinstance(v, str) and v.strip():
                    rows.append(dict(base, effect_record=bio, effect_archives="|".join(barcs),
                                     stat=k, stat_group="Bio equation", stat_kind="body",
                                     value_at_rank=L.evaleq(v, CHAR_LEVEL), value_raw_array=v,
                                     applies_to="the defence object itself", delivery="body",
                                     rank_equation="charLevel", rank_used=CHAR_LEVEL,
                                     rank_basis=f"EQUATION@charLevel={CHAR_LEVEL:.0f}",
                                     note="CLIFF C-2: defence charLevel binding not decoded"))

    seen = set()
    # (a) skill-tree grants -- this is where the rank equation lives
    for idx, path, lvl in L.tree_entries(r):
        s, _ = E3.merged(path)
        cls = (s or {}).get("Class", "")
        raw = L.evaleq(lvl, CHAR_LEVEL)
        rank = int(math.floor(raw)) if raw is not None else None
        if cls in SELF_CLASSES:
            applies, deliver, child = ("the defence object itself",
                                       f"self-passive, tree slot {idx}", "the defence object itself")
        elif cls in EMITTER_CLASSES:
            applies, deliver, child = (f"none (emitter only, Class={cls})",
                                       f"aura emitter, tree slot {idx}", ALLY)
        else:
            applies, deliver, child = ("enemies", f"defence output, tree slot {idx}", "enemies")
        if path not in seen:
            rows += rows_for_record(path, applies, deliver, base, rank_eq=str(lvl), rank_used=rank)
            seen.add(path)
        for f, np_ in L.nested_refs(s or {}):
            if np_ in seen:
                continue
            nb, _ = E3.merged(np_)
            rows += rows_for_record(np_, child, f"{deliver} -> {f}", base,
                                    rank_eq=str(lvl), rank_used=rank)
            seen.add(np_)
            pb = (nb or {}).get("petBonusName")
            if isinstance(pb, str) and pb.lower().endswith(".dbr") and pb.lower() not in seen:
                rows += rows_for_record(pb.lower(), "pets only", f"{deliver} -> petBonus", base,
                                        rank_eq=str(lvl), rank_used=rank)
                seen.add(pb.lower())

    # (b) slot skills not already reached through the tree
    for slot, field in L.SLOT_FIELDS:
        sp = r.get(field)
        if not (isinstance(sp, str) and sp.lower().endswith(".dbr")):
            continue
        sp = sp.lower()
        if sp in seen:
            continue
        s, _ = E3.merged(sp)
        cls = (s or {}).get("Class", "")
        applies = (ALLY if cls in EMITTER_CLASSES
                   else "the defence object itself" if cls in SELF_CLASSES else "enemies")
        rows += rows_for_record(sp, applies, f"slot:{slot}", base)
        seen.add(sp)
        for f, np_ in L.nested_refs(s or {}):
            if np_ not in seen:
                rows += rows_for_record(np_, applies, f"slot:{slot} -> {f}", base)
                seen.add(np_)
    return rows


def declared_absent_rows():
    """Tier-2/3-only contracts the purchase did NOT buy -- named, not silently missing."""
    out = []
    for pn, pname, rec, why in [
        (4, "Vanguard Banner", "records/skills/defenses/banneroffense_frenzy.dbr",
         "granted only by banner_offense02/03 (skillName4); tier-1 banner_offense has no "
         "skillName4 -> the Frenzy pulse (+35% total speed, +6% attack/cast speed max, 5-8 s, "
         "15 s cooldown, 16 m) was NOT purchased"),
        (1, "Deathchill Beacon", "records/skills/defenses/turretice_chillingsurge.dbr",
         "granted only by turret_ice02/03 (skillName4 + specialAttackSkillName); tier-1 "
         "turret_ice has no special attack -> NOT purchased"),
        (3, "Inferno Beacon", "records/skills/defenses/turretfire_firestorm.dbr",
         "tier-2/3 only -> NOT purchased"),
        (2, "Stormcaller Beacon", "records/skills/defenses/turretlightning_stormcaller.dbr",
         "tier-2/3 only -> NOT purchased"),
    ]:
        out.append(dict(purchase_n=pn, purchase_name=pname, purchase_video_t="",
                        tribute_cost="", ironbits_cost="", source_record="",
                        effect_record=rec, stat="", value_at_rank="",
                        rank_basis="DECLARED-ABSENT", applies_to="", delivery="",
                        note=why))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in PURCHASES:
        rows += walk_creature(p)
    rows += declared_absent_rows()
    for name, root in BLESSINGS:
        r, _ = E3.merged(root)
        base = dict(purchase_n=0, purchase_name=f"{name} [NOT PURCHASED - measured]",
                    purchase_video_t="", tribute_cost="", ironbits_cost="",
                    source_record=root, source_display_name=name)
        b = (r or {}).get("buffSkillName", "")
        if b:
            rows += rows_for_record(b.lower(), "player (self)",
                                    "celestial blessing (whole-run self buff)", base)
            nb, _ = E3.merged(b.lower())
            pb = (nb or {}).get("petBonusName")
            if isinstance(pb, str):
                rows += rows_for_record(pb.lower(), "pets only",
                                        "celestial blessing pet bonus", base)

    cols = ["purchase_n", "purchase_name", "purchase_video_t", "tribute_cost", "ironbits_cost",
            "source_record", "source_display_name", "effect_record", "effect_archives",
            "effect_display_name", "effect_description", "stat", "stat_group", "stat_kind",
            "value_at_rank", "value_raw_array", "applies_to", "delivery", "rank_equation",
            "rank_used", "skill_active_duration_s", "rank_basis", "note"]
    fp = OUT / "measured-blessing-sheet.csv"
    with fp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in cols})
    print(fp, len(rows), "rows")
    print("  PURCHASED rows      :", sum(1 for r in rows if r.get("purchase_n") and r.get("stat")))
    print("  DECLARED-ABSENT rows:", sum(1 for r in rows if r.get("rank_basis") == "DECLARED-ABSENT"))
    print("  NOT-PURCHASED blessing rows:", sum(1 for r in rows if r.get("purchase_n") == 0))
    print("  rank_basis census   :",
          dict(collections.Counter(r.get("rank_basis") for r in rows)))


if __name__ == "__main__":
    main()
