#!/usr/bin/env python3
"""KC2-PM4 · Lap X · THE MITIGATION-PIPELINE DECODE, BOTH DIRECTIONS  (ruling R-PM4-61 part 5).

READ-ONLY on every source.  OUTCOME-FIREWALLED: this instrument reads NO sim outcome.  The single
baton it touches is the FROZEN ROSTER BASIS (`kc2-baton-v1-E-s09-cp150-20260809_052836.json`) and
from it only `(wave, record_path, level, is_champion)` -- the same roster-basis read Lap I ratified.
No `path`, no `engage_*`, no `hp_max`, no duration, no outcome field is read.

GL-12 decode-never-estimate.  NOTE-9: every emitted quantity carries its own basis.
Law 3: the referent's numbers are GRADES; not one of them enters a decoded value here.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-15.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import pathlib
import statistics
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GDBIN = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4g_lib_2026_08_13 import (                                            # noqa: E402
    E3, rec, arc_of, at_rank, read_skill_block, PLAYED_SAVE, LAP_A_SHEET,
    sheet_skill_bonuses, TEXT_ARCS,
)
from pm4f_lib_2026_08_13 import Templates                                    # noqa: E402
from gd_arc_reader_2026_07_26 import ArcArchive                              # noqa: E402
import pm4i_lib_2026_08_13 as I                                              # noqa: E402
from gamora_kc2_c1_closure_ed3_2026_08_08 import ev                          # noqa: E402
from pm4l_emit_2026_08_14 import EQUIP, WARBORN, ALWAYS_ON, AURA_MODS, ITEM_PASSIVES  # noqa: E402

OUT = META / "agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode"
LAPD = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp"
LAPI = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-i-monster-offense"
LAPL = META / "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-l-player-offense"
LAPG = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit"
LAPC = META / "agentic_orchestration/legolas/notes/2026-08-12-kc2-pm3-lap-c-blessings-reference-dot"

COMBATF = "records/game/combatformulas.dbr"
GAMEENG = "records/game/gameengine.dbr"

log_lines: list[str] = []


def L(msg: str = "") -> None:
    print(msg)
    log_lines.append(msg)


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 0 -- THE PINS.  HALT on the first mismatch.  (PREREGISTRATION.md § 1)
# ══════════════════════════════════════════════════════════════════════════════════════════════

PINS = {
    VENDOR / "database/database.arz": "2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd",
    VENDOR / "gdx1/database/GDX1.arz": "431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292",
    VENDOR / "gdx2/database/GDX2.arz": "13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072",
    VENDOR / "gdx3/database/GDX3.arz": "e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4",
    VENDOR / "mods/survivalmode/database/SurvivalMode.arz": "e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6",
    VENDOR / "survivalmode1/database/SurvivalMode1.arz": "6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252",
    VENDOR / "survivalmode2/database/SurvivalMode2.arz": "940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95",
    VENDOR / "survivalmode3/database/SurvivalMode3.arz": "e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a",
    VENDOR / "database/templates.arc": "679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602",
    VENDOR / "mods/survivalmode/resources/Scripts.arc": "47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009",
    GDBIN / "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    GDBIN / "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
    PLAYED_SAVE: "b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5",
    LAP_A_SHEET: "6852794382b9bf608f13433ea18be7a52d1f2f0942801e5bb7c4e1be8899badd",
    LAPG / "pm4g_played_kit.csv": "2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3",
    LAPG / "pm4g_defensive_actives.csv": "0cdfd3af9a22e2d6d7de59ca0b8238f0e2c04c64192a16dee894ef71ae0be306",
    LAPD / "pm4d_band_b_ehp_by_wave.csv": "3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024",
    LAPI / "pm4i_dot_riders.csv": "2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1",
    LAPI / "pm4i_wave_damage_modifier.csv": "f0852cec35a0362c101618b2a269446c4fba658ee0b80821aa5e4ae47eab910b",
    LAPI / "pm4i_survival_wave_arrays_full.csv": "eab2d141cb41ad83c89b02c9da2a9c7b75ba49d6cb38b27a988a2a172dbd1ce9",
    LAPL / "pm4l_mitigation_by_body.csv": "a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6",
    LAPL / "pm4l_eor_per_hit.csv": "120990d998ac23a4b2dadc134e0f5cf3e51a3f7f6eb34ee400d5e2531b26d5a8",
    LAPL / "method.md": "d33f396d5d47950b9a13a35f1fbeb6ca5c28adaf92346deaae0b10dd8aa0db32",
    LAPC / "measured-reference-truth.csv": "4546046efd0d01eaceefe5548b46d14c829b8975474f162a007c586b7dcf5642",
}


def verify_pins() -> dict:
    out = {}
    bad = []
    for p, want in PINS.items():
        got = sha(p)
        out[str(p)] = got
        if got != want:
            bad.append((str(p), want, got))
    if bad:
        for b in bad:
            L(f"⚑ PIN MISMATCH  {b[0]}\n   expected {b[1]}\n   got      {b[2]}")
        raise SystemExit("HALT — pinned input digest mismatch (PREREGISTRATION.md § 1)")
    L(f"§0  pins verified EXACT: {len(out)}/{len(out)}")
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 1 -- THE FORMULA STACK, VERBATIM
# ══════════════════════════════════════════════════════════════════════════════════════════════

GE_KEEP = ("armorDefensiveAbsorption", "playerDefenseCap", "monsterDefenseCap",
           "monsterLevelGapFixer", "playerReflectCap", "absMaxDamageScaling",
           "damageMagnitude", "defaultCombatManagerRecord", "meleeTargetDistance",
           "meleeRange", "meleeAutoTargetDistance", "2hWeaponDamageFactor",
           "dwWeaponDamageFactor", "dwWeaponSpeedFactor", "monsterAttackSpeedCapMin",
           "monsterAttackSpeedCapMax", "playerAttackSpeedCapMax", "playerAttackSpeedCapMin",
           "absorbShieldPercentHealth")


def formulas() -> dict:
    cf = rec(COMBATF)
    ge = rec(GAMEENG)
    T = Templates()
    tag_index = ui_tags()
    decl = {}
    for f in ("playerDefenseCap", "monsterDefenseCap", "monsterLevelGapFixer",
              "armorDefensiveAbsorption", "damageAbsorption", "damageAbsorptionPercent",
              "defensiveProtection", "defensiveProtectionModifier", "defensiveAbsorption",
              "defensiveAbsorptionModifier", "defensiveBlock", "defensiveBlockChance",
              "blockAbsorption", "blockRecoveryTime", "defensiveBlockAmountModifier",
              "defensivePercentCurrentLife", "absMaxDamageScaling", "damageMagnitude"):
        ts = T.declaring_templates(f)
        if ts:
            d = T.declare(ts[0], f)
            decl[f] = {"template": ts[0], "class": d.get("class"), "type": d.get("type"),
                       "description": d.get("description"), "defaultValue": d.get("defaultValue")}
        else:
            decl[f] = {"template": None, "grade": "TEMPLATE-ABSENT"}
    out = {
        "combatformulas.dbr": {"archive": arc_of(COMBATF), "fields": {k: cf[k] for k in sorted(cf)}},
        "gameengine.dbr": {"archive": arc_of(GAMEENG),
                           "fields": {k: ge.get(k) for k in GE_KEEP}},
        "template_declarations": decl,
        "ui_format_strings": tag_index,
    }
    L("§1  combatformulas.dbr fields: %d ; gameengine keeps: %d"
      % (len(cf), sum(1 for k in GE_KEEP if ge.get(k) is not None)))
    return out


def ui_tags() -> dict:
    """The shipped UI format strings that DISCRIMINATE flat-vs-percent semantics."""
    want = ("SkillDamageAbsorption", "SkillDamageAbsorptionPercent", "DamagePercentCurrentLife",
            "DefensePercentCurrentLife", "ShieldBlockRecoveryTime", "tagCharStatsBlockRecovery",
            "DefenseAbsorptionProtection", "DefenseProtection", "DefenseAbsorption",
            "tagCharStatsArmor", "tagCharStatsArmorInfo", "SkillDistanceFormat")
    out: dict[str, dict] = {}
    for t in TEXT_ARCS:
        p = VENDOR / t
        if not p.exists():
            continue
        A = ArcArchive(p)
        for name in A.names():
            if not name.endswith(".txt"):
                continue
            try:
                data = A.read_file(name).decode("utf-8-sig", errors="replace")
            except Exception:
                continue
            for line in data.splitlines():
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                if k in want and k not in out:
                    out[k] = {"value": v.strip(), "arc": t, "file": name}
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 2 -- THE PLAYER'S DEFENSIVE STACK  (T-A / T-B / T-C)
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: Slots that actually COVER a hit region.  `combatRegion*Chance` names six regions; the player
#: has exactly six armour-bearing slots.  Everything else (rings/neck/medal/relic/waist/weapon)
#: contributes only GLOBAL terms.
REGION_SLOT = {"head": "combatRegionHeadChance", "shoulders": "combatRegionShouldersChance",
               "hands": "combatRegionArmsChance", "chest": "combatRegionTorsoChance",
               "legs": "combatRegionLegsChance", "feet": "combatRegionFeetChance"}

RES_FIELDS = ("defensivePhysical", "defensivePierce", "defensiveFire", "defensiveCold",
              "defensiveLightning", "defensivePoison", "defensiveLife", "defensiveAether",
              "defensiveChaos", "defensiveBleeding", "defensiveElemental",
              "defensivePercentCurrentLife", "defensiveStun", "defensiveSlowLifeLeach",
              "defensiveReflect", "defensiveDisruption", "defensiveFreeze", "defensiveSlowRunSpeed")

BLOCK_FIELDS = ("defensiveBlock", "defensiveBlockChance", "defensiveBlockModifier",
                "defensiveBlockModifierChance", "defensiveBlockAmountModifier",
                "blockAbsorption", "blockRecoveryTime",
                "characterDefensiveBlockRecoveryReduction")

DEF_PREFIX = ("defensive", "damageAbsorption", "block", "characterLife", "characterDefensive",
              "characterEnergyAbsorption", "conversion")


def player_defense() -> tuple[dict, list[dict]]:
    """Per-source census of every defensive term the played save actually carries."""
    _h, _b8, _v, _n, skillrows, _isc, _t = read_skill_block(PLAYED_SAVE)
    bonuses = sheet_skill_bonuses()
    rows: list[dict] = []

    def add(src, slot, r, rank=1, kind=""):
        if not r:
            return
        for k, v in r.items():
            if not str(k).startswith(DEF_PREFIX):
                continue
            if isinstance(v, list):
                if not v or not isinstance(v[0], (int, float)) or isinstance(v[0], bool):
                    continue
                vv, how = at_rank(v, rank)
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                vv, how = v, "scalar"
            else:
                continue
            if not vv:
                continue
            rows.append({"source": src, "slot": slot, "kind": kind, "field": k,
                         "value": float(vv), "rank": rank, "index_state": how,
                         "grade": "MEASURED"})

    for slot, base, affixes, comp, aug in EQUIP:
        add(f"gear:{slot}:base", slot, rec(base), 1, "item")
        for a in affixes:
            add(f"gear:{slot}:affix", slot, rec(a), 1, "affix")
        if comp:
            add(f"gear:{slot}:component", slot, rec(comp), 1, "component")
        if aug:
            add(f"gear:{slot}:augment", slot, rec(aug), 1, "augment")

    sr = rec(WARBORN)
    for k, v in sr.items():
        if str(k).startswith(DEF_PREFIX) and isinstance(v, list) and v \
                and isinstance(v[0], (int, float)) and not isinstance(v[0], bool) and len(v) >= 3 and v[2]:
            rows.append({"source": "set:warborn@3pc", "slot": "GLOBAL", "kind": "set",
                         "field": k, "value": float(v[2]), "rank": 3,
                         "index_state": "set-index=pieces-1=2", "grade": "MEASURED"})

    for r in skillrows:
        p = r["record"]
        if p.startswith("records/skills/devotion/") and r["rank_allocated"] == 1:
            rr = rec(p)
            if rr.get("Class") == "Skill_Passive":
                add("devotion:" + p.split("/")[-1], "GLOBAL", rr, 1, "devotion")

    mdir = {"playerclass01": "bonus_soldier_skills", "playerclass09": "bonus_oathkeeper_skills"}
    for r in skillrows:
        p = r["record"]
        if not p.startswith("records/skills/playerclass") or r["rank_allocated"] <= 0:
            continue
        eff = (r["rank_allocated"] + bonuses.get("bonus_all_skills", 0)
               + bonuses.get(mdir.get(p.split("/")[2], "_"), 0))
        rr = rec(p)
        if rr.get("Class") in ALWAYS_ON:
            tgt = rr.get("buffSkillName")
            add(f"skill:{p.split('/')[-1]}", "GLOBAL", rec(tgt) if tgt else rr, eff, "skill")
        elif p in AURA_MODS:
            add(f"auramod:{p.split('/')[-1]}", "GLOBAL", rr, eff, "auramod")

    for gp, lvl in ITEM_PASSIVES:
        add("itemskill:" + gp.split("/")[-1], "GLOBAL", rec(gp), lvl, "itemskill")

    # ── the four armour models ──────────────────────────────────────────────────────────────
    cf = rec(COMBATF)
    piece_flat: dict[str, float] = collections.defaultdict(float)
    piece_pct: dict[str, float] = collections.defaultdict(float)
    global_flat = 0.0
    global_pct = 0.0
    abs_local: dict[str, float] = collections.defaultdict(float)
    abs_global = 0.0
    for r in rows:
        if r["field"] == "defensiveProtection":
            if r["slot"] in REGION_SLOT:
                piece_flat[r["slot"]] += r["value"]
            else:
                global_flat += r["value"]          # waist / ring component / devotion flats
        elif r["field"] == "defensiveBonusProtection":
            global_flat += r["value"]              # ⚑ the "+X Armor" family, GLOBAL by name
        elif r["field"] == "defensiveProtectionModifier":
            if r["slot"] in REGION_SLOT:
                piece_pct[r["slot"]] += r["value"]
            else:
                global_pct += r["value"]
        elif r["field"] == "defensiveAbsorptionModifier":
            if r["slot"] in REGION_SLOT:
                abs_local[r["slot"]] += r["value"]
            else:
                abs_global += r["value"]

    w = {s: float(cf[f]) for s, f in REGION_SLOT.items()}
    wsum = sum(w.values())
    per_piece = {}
    for s in REGION_SLOT:
        local = piece_flat[s] * (1.0 + piece_pct[s] / 100.0)
        per_piece[s] = {
            "flat": piece_flat[s], "local_pct": piece_pct[s],
            "after_local": local,
            "after_local_and_global": local * (1.0 + global_pct / 100.0),
            "all_pct_global": piece_flat[s] * (1.0 + (piece_pct[s] + global_pct) / 100.0),
            "region_chance_pct": w[s],
            "absorption_local_pct": abs_local[s],
        }
    sum_lg = sum(v["after_local_and_global"] for v in per_piece.values())
    avg_lg = sum(v["after_local_and_global"] * v["region_chance_pct"]
                 for v in per_piece.values()) / wsum
    models = {
        "M-SUM-PIECESONLY": sum_lg,
        "M-SUM-PLUS-GLOBALFLAT": sum_lg + global_flat * (1.0 + global_pct / 100.0),
        "M-AVG-PIECESONLY": avg_lg,
        "M-AVG-PLUS-GLOBALFLAT": (sum(v["after_local"] * v["region_chance_pct"]
                                      for v in per_piece.values()) / wsum + global_flat)
                                 * (1.0 + global_pct / 100.0),
        "M-AVG-GLOBALFLAT-UNSCALED": avg_lg + global_flat,
        "M-SUM-FLAT-ONLY": sum(v["flat"] for v in per_piece.values()),
    }

    sheet = sheet_rows()
    sheet_armor = float(sheet["armor_rating"])
    winner = min(models, key=lambda k: abs(models[k] - sheet_armor))
    resid = {k: models[k] - sheet_armor for k in models}

    # ── armour ABSORPTION, both composition limbs, DECLARED-CLAMPED at 100 ──────────────────
    base_abs = float(rec(GAMEENG)["armorDefensiveAbsorption"])
    abs_limbs = {}
    for s in REGION_SLOT:
        pts = base_abs + abs_local[s] + abs_global
        mul = base_abs * (1.0 + (abs_local[s] + abs_global) / 100.0)
        abs_limbs[s] = {"ADDITIVE_POINTS_uncapped": pts, "MULTIPLICATIVE_uncapped": mul,
                        "ADDITIVE_POINTS_clamped100": min(100.0, pts),
                        "MULTIPLICATIVE_clamped100": min(100.0, mul)}

    # ── resistances, reconstructed as a FALSIFIER of the stack itself ───────────────────────
    res_recon: dict[str, float] = collections.defaultdict(float)
    for r in rows:
        if r["field"] in RES_FIELDS:
            res_recon[r["field"]] += r["value"]

    # ── block census: P-X-3's named falsifier ───────────────────────────────────────────────
    block_rows = [r for r in rows if r["field"] in BLOCK_FIELDS]

    defense = {
        "sheet": sheet,
        "armour": {
            "per_piece": per_piece,
            "global_pct_armour": global_pct,
            "global_flat_armour": global_flat,
            "absorption_global_pct_modifier": abs_global,
            "absorption_limbs_by_region": abs_limbs,
            "base_absorption_pct": base_abs,
            "region_weights": w,
            "models": models,
            "sheet_armor_rating": sheet_armor,
            "residual_vs_sheet": resid,
            "winner": winner,
            "winner_residual": resid[winner],
            "winner_residual_pct": 100.0 * resid[winner] / sheet_armor,
        },
        "resist_reconstruction": dict(res_recon),
        "block_census": {"n_nonzero_block_fields": len(block_rows), "rows": block_rows},
        "resist_caps": {"playerDefenseCap": rec(GAMEENG)["playerDefenseCap"],
                        "monsterDefenseCap": rec(GAMEENG)["monsterDefenseCap"],
                        "difficulty_index_of_record": 2,
                        "basis": "Lap A sheet difficulty=Ultimate (gdc block1 raw byte 2)"},
    }
    L("§2  defensive-term rows: %d ; armour models: %s"
      % (len(rows), {k: round(v, 1) for k, v in models.items()}))
    L("§2  sheet armor_rating %.0f -> winner %s (residual %+.1f = %+.2f%%)"
      % (sheet_armor, winner, resid[winner], 100.0 * resid[winner] / sheet_armor))
    L("§2  ⚑ non-zero BLOCK fields anywhere in the played build: %d" % len(block_rows))
    return defense, rows


def sheet_rows() -> dict:
    d = {}
    with LAP_A_SHEET.open() as f:
        for r in csv.DictReader(f):
            d[r["stat"]] = r["value"]
    return d


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 3 -- THE DEFENSIVE PROCS, RECORD-TRUTH ONLY (T-D).  NO UPTIME.
# ══════════════════════════════════════════════════════════════════════════════════════════════

PROC_KEEP = ("damageAbsorption", "damageAbsorptionPercent", "defensiveProtectionModifier",
             "defensiveAbsorptionModifier", "characterLifeRegen", "skillLifePercent",
             "offensiveTotalDamageReductionPercentMin", "offensiveTotalDamageReductionAbsoluteMin",
             "skillActiveDuration", "skillCooldownTime", "defensivePhysical",
             "defensiveTotalSpeedResistance", "characterDefensiveAbility")


def procs() -> list[dict]:
    out = []
    with (LAPG / "pm4g_defensive_actives.csv").open() as f:
        src = list(csv.DictReader(f))
    for r in src:
        p, rank = r["skill_record"], int(float(r["rank"] or 1))
        rr = rec(p)
        row = {"skill_record": p, "display_name": r["display_name"],
               "engine_class": r["engine_class"], "kind": r["kind"], "rank": rank,
               "rank_basis": r["rank_basis"], "trigger": r["trigger"],
               "trigger_param": r["trigger_param"], "trigger_chance_pct": r["trigger_chance_pct"],
               "grade": "MEASURED", "uptime": "NOT-MODELLED — I-23's, per R-PM4-61 part 5"}
        for k in PROC_KEEP:
            v = rr.get(k)
            if v is None:
                continue
            vv, how = at_rank(v, rank)
            if vv in (None, 0, 0.0):
                continue
            row[k] = float(vv)
            row[k + "__index_state"] = how
        out.append(row)
    L("§3  defensive-proc record-truth rows: %d" % len(out))
    return out


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 4/5 -- MONSTER OFFENSE + RESIST REDUCTION (T-E1 / T-B monster side)
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: (type key, record stem, player sheet resistance row)
DMG_TYPES = (
    ("physical",           "Physical",           "resist_physical"),
    ("pierce",             "Pierce",             "resist_pierce"),
    ("fire",               "Fire",               "resist_fire"),
    ("cold",               "Cold",               "resist_cold"),
    ("lightning",          "Lightning",          "resist_lightning"),
    ("poison",             "Poison",             "resist_acid_poison"),
    ("vitality",           "Life",               "resist_vitality"),
    ("aether",             "Aether",             "resist_aether"),
    ("chaos",              "Chaos",              "resist_chaos"),
    ("percentCurrentLife", "PercentCurrentLife", None),
)
#: DoT families: the "slow" stems, with the resistance row they answer to.
DOT_TYPES = (
    ("bleeding",   "SlowBleeding",  "resist_bleeding"),
    ("burn",       "SlowFire",      "resist_fire"),
    ("frostburn",  "SlowCold",      "resist_cold"),
    ("electrocute", "SlowLightning", "resist_lightning"),
    ("poison_dot", "SlowPoison",    "resist_acid_poison"),
    ("vitdecay",   "SlowLife",      "resist_vitality"),
    ("trauma",     "SlowPhysical",  "resist_physical"),
)

RR_FAMILIES = ("offensiveTotalResistanceReductionAbsolute",
               "offensiveTotalResistanceReductionPercent",
               "offensiveElementalResistanceReductionAbsolute",
               "offensiveElementalResistanceReductionPercent",
               "offensivePhysicalResistanceReductionAbsolute",
               "offensivePhysicalResistanceReductionPercent",
               "offensiveTotalDamageReductionPercent",
               "offensiveTotalDamageReductionAbsolute")


def _pick(arr, rank):
    if isinstance(arr, list):
        if not arr:
            return 0.0, "empty"
        i, st = I._idx(arr, rank)
        v = arr[i]
        return (float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0), st
    if isinstance(arr, (int, float)) and not isinstance(arr, bool):
        return float(arr), "scalar"
    return 0.0, "n/a"


def monster_offense(records_levels: dict[str, tuple[int, int]]) -> tuple[list[dict], list[dict]]:
    """ONE ROW PER (record, level-limb, SKILL).

    ⚑ THE ROW GRAIN IS THE WHOLE POINT.  A monster fires ONE skill on an attack round; it does
    not fire its entire skill closure at once.  Summing the closure is an over-read by the size
    of the closure, and this instrument's first build did exactly that.  The per-skill grain lets
    the consumer choose a policy explicitly instead of inheriting one silently.

    `is_default_attack` marks the creature's DECLARED `attackSkillName` -- the only skill the
    records themselves nominate.  Skill SELECTION among the rest is an AI/cooldown policy that
    lives in the engine, not in the corpus: NAMED, not decoded (`R-PM4-56 part 4` class).
    """
    off_rows: list[dict] = []
    rr_rows: list[dict] = []
    for record, (llo, lhi) in sorted(records_levels.items()):
        base = rec(record)
        default_atk = base.get("attackSkillName")
        if isinstance(default_atk, list):
            default_atk = default_atk[0] if default_atk else None
        default_atk = (default_atk or "").lower().replace("\\", "/")
        for limb, Lv in (("LO", llo), ("HI", lhi)):
            closure = I.skill_closure(record, float(Lv))
            if default_atk and default_atk not in closure:
                closure[default_atk] = (1, 0, "MEASURED-RANK", "attackSkillName")
            own_pct, _src = I.own_total_damage_modifier(record, float(Lv))
            for skill, (rank, depth, rgrade, via) in sorted(closure.items()):
                s = rec(skill)
                if not s:
                    continue
                row = {"record": record, "level_limb": limb, "level": Lv, "skill": skill,
                       "skill_class": s.get("Class"), "rank": rank, "depth": depth,
                       "rank_grade": rgrade, "via": via,
                       "is_default_attack": (skill == default_atk),
                       "own_totalDamageModifier_pct": own_pct}
                touched = False
                for key, stem, _ in DMG_TYPES:
                    mn, st = _pick(s.get(f"offensive{stem}Min"), rank)
                    mx, _ = _pick(s.get(f"offensive{stem}Max"), rank)
                    row[f"raw_{key}_min"] = mn
                    row[f"raw_{key}_max"] = mx or mn
                    row[f"raw_{key}_index_state"] = st
                    if mn or mx:
                        touched = True
                for key, stem, _ in DOT_TYPES:
                    mn, st = _pick(s.get(f"offensive{stem}Min"), rank)
                    du, _ = _pick(s.get(f"offensive{stem}DurationMin"), rank)
                    row[f"dot_{key}_min"] = mn
                    row[f"dot_{key}_dur_s"] = du
                    if mn:
                        touched = True
                row["carries_damage"] = touched
                row["grade"] = "MEASURED" if touched else "DECODED-ZERO-DAMAGE"
                off_rows.append(row)
                for fam in RR_FAMILIES:
                    mn, _ = _pick(s.get(fam + "Min"), rank)
                    if mn:
                        rr_rows.append({"record": record, "level_limb": limb, "level": Lv,
                                        "skill": skill, "rank": rank, "depth": depth,
                                        "family": fam, "value_min": mn,
                                        "chance_pct": _pick(s.get(fam + "Chance"), rank)[0],
                                        "duration_min_s": _pick(s.get(fam + "DurationMin"), rank)[0],
                                        "global": bool(s.get(fam + "Global")),
                                        "xor": bool(s.get(fam + "XOR")),
                                        "grade": rgrade})
            # the creature's own record may carry flat offensive lines: one synthetic row
            row = {"record": record, "level_limb": limb, "level": Lv, "skill": "(creature record)",
                   "skill_class": base.get("Class"), "rank": 1, "depth": -1,
                   "rank_grade": "MEASURED-RECORD", "via": "creature-own-fields",
                   "is_default_attack": False, "own_totalDamageModifier_pct": own_pct}
            touched = False
            for key, stem, _ in DMG_TYPES:
                mnv, _ = _pick(base.get(f"offensive{stem}Min"), 1)
                mxv, _ = _pick(base.get(f"offensive{stem}Max"), 1)
                row[f"raw_{key}_min"] = mnv
                row[f"raw_{key}_max"] = mxv or mnv
                if mnv or mxv:
                    touched = True
            for key, stem, _ in DOT_TYPES:
                mnv, _ = _pick(base.get(f"offensive{stem}Min"), 1)
                row[f"dot_{key}_min"] = mnv
                row[f"dot_{key}_dur_s"] = _pick(base.get(f"offensive{stem}DurationMin"), 1)[0]
                if mnv:
                    touched = True
            row["carries_damage"] = touched
            row["grade"] = "MEASURED" if touched else "DECODED-ZERO-DAMAGE"
            off_rows.append(row)
    L("§4  monster-offense rows (per record × limb × SKILL): %d over %d records ; "
      "rows carrying damage: %d ; resist-reduction rows: %d"
      % (len(off_rows), len(records_levels),
         sum(1 for r in off_rows if r["carries_damage"]), len(rr_rows)))
    return off_rows, rr_rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 6 -- THE INTAKE ARITHMETIC (both armour limbs, published)
# ══════════════════════════════════════════════════════════════════════════════════════════════

def armour_applied(raw: float, armour: float, absorption_pct: float) -> float:
    """`combatformulas.dbr` verbatim.  Two branches, damage <= armour and damage > armour."""
    a = absorption_pct / 100.0
    if raw <= armour:
        return raw * (1.0 - a)                                  # ...DefenseEquationDLEP
    return armour * (1.0 - a) + (raw - armour)                  # ...DefenseEquationDGP


def player_resists(sheet: dict) -> dict:
    out = {}
    for key, _stem, row in DMG_TYPES + DOT_TYPES:
        if row is None:
            out[key] = 0.0
        else:
            try:
                out[key] = float(sheet[row])
            except Exception:
                out[key] = 0.0
    return out


def intake(off_rows, defense, wave_mod_pct: float, sheet: dict, actors: list[dict],
           wave: int = 151):
    res = player_resists(sheet)
    cap = float(defense["resist_caps"]["playerDefenseCap"][2])
    per_piece = defense["armour"]["per_piece"]
    absL = defense["armour"]["absorption_limbs_by_region"]
    base_abs = defense["armour"]["base_absorption_pct"]
    # aggregate limb == the camera-measured sheet Armor Rating (the run-of-record aggregate,
    # exactly as Lap L used the camera-measured EoR per-hit); per-piece limb == region expectation
    agg_armour = float(defense["sheet"]["armor_rating"])
    by_rec: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in off_rows:
        by_rec[(r["record"], r["level_limb"])].append(r)

    def one_skill(r: dict, scale: float) -> dict:
        """Mitigate ONE skill's declared damage through the decoded pipeline, three armour limbs."""
        o = {"direct_perpiece": 0.0, "direct_aggregate": 0.0, "direct_perpiece_base70abs": 0.0,
             "dot_total": 0.0, "pct_current_life": r.get("raw_percentCurrentLife_min", 0.0),
             "types": {}}
        for key, _stem, _row in DMG_TYPES:
            raw = float(r.get(f"raw_{key}_min") or 0.0) * scale
            if raw <= 0:
                continue
            rp = min(res[key], cap)
            if key == "physical":
                # LIMB 1 -- per-region armour, absorption ADDITIVE-POINTS clamped at 100
                pp = sum(armour_applied(raw, per_piece[s]["after_local_and_global"],
                                        absL[s]["ADDITIVE_POINTS_clamped100"])
                         * per_piece[s]["region_chance_pct"] / 100.0 for s in per_piece)
                # LIMB 2 -- the camera sheet's aggregate armour, absorption at the BASE 70 %
                ag = armour_applied(raw, agg_armour, base_abs)
                # LIMB 3 -- per-region armour at the BASE 70 % (the conservative limb)
                bs = sum(armour_applied(raw, per_piece[s]["after_local_and_global"], base_abs)
                         * per_piece[s]["region_chance_pct"] / 100.0 for s in per_piece)
            elif key == "percentCurrentLife":
                continue               # a PERCENT of current life; carried, never summed in HP
            else:
                pp = ag = bs = raw
            f_ = max(0.0, 1.0 - rp / 100.0)
            o["direct_perpiece"] += pp * f_
            o["direct_aggregate"] += ag * f_
            o["direct_perpiece_base70abs"] += bs * f_
            o["types"][key] = {"raw": raw, "applied_perpiece": pp * f_,
                               "player_res_pct_capped": rp}
        for key, _stem, _row in DOT_TYPES:
            d = float(r.get(f"dot_{key}_min") or 0.0) * scale
            if d <= 0:
                continue
            rp = min(res[key], cap)
            o["dot_total"] += d * max(0.0, 1.0 - rp / 100.0)
        return o

    rows = []
    for a in actors:
        recp = a["record_path"].lower()
        for limb in ("LO", "HI"):
            cands = by_rec.get((recp, limb), [])
            if not cands:
                rows.append({"wave": wave, "actor_id": a["actor_id"], "record": recp,
                             "level_limb": limb, "grade": "DECLARED-GAP-NO-OFFENSE-ROW"})
                continue
            own = cands[0]["own_totalDamageModifier_pct"]
            scale = 1.0 + (own + wave_mod_pct) / 100.0
            evald = [(r, one_skill(r, scale)) for r in cands]
            dmg = [(r, o) for r, o in evald if o["direct_perpiece"] > 0 or o["dot_total"] > 0]
            dflt = [(r, o) for r, o in evald if r["is_default_attack"]]
            creat = [(r, o) for r, o in evald if r["depth"] == -1 and o["direct_perpiece"] > 0]
            best = max(dmg, key=lambda t: t[1]["direct_perpiece"], default=(None, None))
            out = {"wave": wave, "actor_id": a["actor_id"], "record": recp,
                   "level_limb": limb,
                   "level": cands[0]["level"], "is_champion": bool(a.get("is_champion")),
                   "wave_plus_own_damage_modifier_pct": own + wave_mod_pct,
                   "n_skills_carrying_damage": len(dmg),
                   "default_attack_skill": (dflt[0][0]["skill"] if dflt else ""),
                   "deepest_hitter_skill": (best[0]["skill"] if best[0] else ""),
                   "grade": "MEASURED" if dmg else "DECODED-ZERO-DIRECT-DAMAGE"}
            crea = sum(o["direct_perpiece"] for _r, o in creat)
            #: ⚑ RUN-OF-RECORD LIMB.  `attackSkillName` where the record declares one; where it
            #: does not (8 of 13 w151 records), the closure's deepest hitter -- because a body
            #: with no declared basic attack still attacks, and MAX is the only non-arbitrary
            #: fallback.  The choice is NAMED here, never buried.
            runrec = dflt if dflt else ([best] if best[0] else [])
            out["run_of_record_source"] = "attackSkillName" if dflt else "MAX-fallback"
            for tag, sel in (("DEFAULT", dflt), ("MAX", [best] if best[0] else []),
                             ("RUNREC", runrec), ("SUMALL", dmg)):
                for fld in ("direct_perpiece", "direct_aggregate",
                            "direct_perpiece_base70abs", "dot_total"):
                    v = sum(o[fld] for _r, o in sel)
                    if tag in ("DEFAULT", "RUNREC") and fld.startswith("direct"):
                        v += crea          # the creature's own flat lines ride the basic attack
                    out[f"{tag}_{fld}"] = v
                out[f"{tag}_pct_current_life"] = sum(o["pct_current_life"] for _r, o in sel)
            rows.append(out)
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 7 -- THE KILL-RATE SIDE: full player damage vector vs the full monster resist vector
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: Composition of the player's per-tick EoR output, ALL from Lap A's camera sheet + Lap L's
#: record decode.  `physical` is the sheet's own composed per-hit figure (43,691-59,761), which
#: ALREADY contains the fire->physical, chaos->physical and lightning->physical conversions.
PLAYER_HIT = {
    "physical": (43691.0, 59761.0, "sheet eye_of_reckoning_damage_per_hit, frame 511"),
    "pierce": (155.0, 206.0, "sheet pierce_damage_flat, frame 513 — NOT scaled by pierce_modifier "
                             "because the sheet line is already the composed flat"),
}
PLAYER_DOT = {
    "bleeding": (21117.0, 3.0, "Gutsmasher EoR-scoped weapon-granted line, Lap A frame 495"),
    "trauma": (2640.0, 3.0, "sheet trauma_damage frame 513; duration modifier +80% carried "
                            "separately — DECLARED, see findings"),
}
MON_RES_COL = {"physical": "res_physical", "pierce": "res_pierce", "bleeding": "res_bleeding",
               "trauma": "res_physical"}


def ttk(records_levels, defense):
    """Player TTK per body, physical-only (Lap L's limb) AND full-vector (this lap's)."""
    mit = {}
    with (LAPL / "pm4l_mitigation_by_body.csv").open() as f:
        for r in csv.DictReader(f):
            if (r.get("wave") or "").strip() == "151":
                mit[r["record"]] = r
    ehp = {}
    with (LAPD / "pm4d_band_b_ehp_by_wave.csv").open() as f:
        for r in csv.DictReader(f):
            if (r.get("wave") or "").strip() == "151":
                ehp[r["record"]] = r
    rows = []
    for record in sorted(records_levels):
        m = mit.get(record)
        e = ehp.get(record)
        if not m or not e:
            continue
        armour = float(m["armor"])
        absorb = float(m["absorption_pct"])
        out = {"record": record, "wave": 151, "monster_armor": armour,
               "monster_absorption_pct": absorb}
        for limb, ix in (("LO", 0), ("HI", 1)):
            phys_raw = PLAYER_HIT["physical"][ix]
            pier_raw = PLAYER_HIT["pierce"][ix]
            rphys = min(float(m["res_physical"]), 100.0)
            rpier = min(float(m["res_pierce"]), 100.0)
            phys = armour_applied(phys_raw, armour, absorb) * max(0.0, 1.0 - rphys / 100.0)
            pier = pier_raw * max(0.0, 1.0 - rpier / 100.0)
            out[f"applied_physonly_{limb}"] = phys
            out[f"applied_fullvector_{limb}"] = phys + pier
        rbleed = min(float(m["res_bleeding"]), 100.0)
        out["dot_bleed_per_s_applied"] = (PLAYER_DOT["bleeding"][0] / PLAYER_DOT["bleeding"][1]) \
            * max(0.0, 1.0 - rbleed / 100.0)
        out["ehp_lo"] = float(e["ehp_lo"])
        out["ehp_hi"] = float(e["ehp_hi"])
        for limb in ("LO", "HI"):
            for mode in ("physonly", "fullvector"):
                d = out[f"applied_{mode}_{limb}"]
                out[f"ticks_to_kill_{mode}_{limb}"] = (out["ehp_lo"] / d) if d > 0 else None
        rows.append(out)
    L("§7  ttk rows: %d" % len(rows))
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════════════════════

def dump_csv(name: str, rows, cols=None) -> str:
    p = OUT / name
    if cols is None:
        cols = []
        for r in rows:
            for k in r:
                if k not in cols:
                    cols.append(k)
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return sha(p)


def dump_json(name: str, obj) -> str:
    p = OUT / name
    p.write_text(json.dumps(obj, indent=1, sort_keys=True, default=str))
    return sha(p)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pins = verify_pins()

    # ── the prediction, transcribed from PREREGISTRATION.md BEFORE anything is computed ──────
    pred = {
        "lap": "KC2-PM4 Lap X — the mitigation-pipeline decode",
        "source": "PREREGISTRATION.md § 2, committed alone at meta commit 64eea319fef4def32431d4f4821e686941c35e4c",
        "P-X-1a": {"claim": "gross post-mitigation intake on the 28-body w151 board ∈ [300,1500] HP/s",
                   "lo": 300.0, "hi": 1500.0, "unit": "HP/s"},
        "P-X-1b": {"claim": "gross intake exceeds bare regen 129.38 HP/s", "threshold": 129.38},
        "P-X-1c": {"claim": "gross intake below 20005/16.0 = 1250.3 HP/s", "threshold": 1250.3125},
        "P-X-2a": {"claim": "full damage-type vector moves median ticks-to-kill by <±25% from "
                            "Lap L's physical-only 7.62 ticks", "baseline_ticks": 7.62,
                   "tolerance_pct": 25.0},
        "P-X-2b": {"claim": "decoded band player kill rate ≥ 1.0 bodies/s at the Lap-L disc geometry",
                   "threshold_bodies_per_s": 1.0},
        "P-X-3a": {"claim": "shield block DECODED-ABSENT: chance 0, amount 0, recovery 0",
                   "prereg_sighted": True},
        "P-X-3b": {"claim": "FALSIFIER — any non-zero defensiveBlock/defensiveBlockChance/"
                            "blockAbsorption/blockRecoveryTime anywhere in the played build FAILS P-X-3a"},
        "P-X-4a": {"claim": "combatRegion*Chance is a hit-location roll ⇒ armour applies per covering piece"},
        "P-X-4b": {"claim": "sheet armor_rating 3557 is the SUM of the six pieces, not their "
                            "hit-weighted average", "bet": "SUM"},
        "P-X-5a": {"claim": "playerDefenseCap=80 is the player resistance cap; the sheet's 80s are AT cap"},
        "P-X-5b": {"claim": "armour applies to physical only, and BEFORE resistance"},
        "P-X-5c": {"claim": "≥1 band-A roster record on 151–160 carries a non-zero "
                            "offensive*ResistanceReduction* field", "threshold": 1},
    }
    h_pred = dump_json("pm4x_prediction.json", pred)
    L("§0  prediction transcribed and hashed BEFORE any computation: %s" % h_pred)

    fm = formulas()
    h_form = dump_json("pm4x_formulas.json", fm)

    defense, defrows = player_defense()
    h_pieces = dump_csv("pm4x_player_defense_terms.csv", defrows)

    prow = procs()
    h_procs = dump_csv("pm4x_defensive_procs.csv", prow)

    # ── population: Lap D's band-B record set, at its own decoded level limbs, per wave ─────
    lapd: dict[int, dict[str, tuple[int, int]]] = collections.defaultdict(dict)
    with (LAPD / "pm4d_band_b_ehp_by_wave.csv").open() as f:
        for r in csv.DictReader(f):
            w = (r.get("wave") or "").strip()
            if not w:
                L("§6  Lap-D named zero-magnitude gap carried as a DECLARED GAP: %s" % r["record"])
                continue
            if not (r.get("level_lo") or "").strip():
                continue
            lapd[int(w)][r["record"]] = (int(r["level_lo"]), int(r["level_hi"]))

    wave_mods: dict[int, float] = {}
    with (LAPI / "pm4i_wave_damage_modifier.csv").open() as f:
        for r in csv.DictReader(f):
            w = (r.get("wave") or "").strip()
            if w:
                wave_mods[int(w)] = float(r["sum_total_damage_modifier_pct"])

    sheet = defense["sheet"]
    all_off: list[dict] = []
    all_rr: list[dict] = []
    all_in: list[dict] = []
    per_wave: dict[int, dict] = {}

    #: 151 is the commission's board.  160 is the referent's DEATH wave and is run as a
    #: POSITIVE CONTROL on the same pipeline -- no referent number enters it, only the roster.
    for wave in (151, 160):
        actors = [{"actor_id": a["actor_id"], "record_path": a["record_path"],
                   "is_champion": a["is_champion"], "level": a["level"]}
                  for a in I.rolled_actors(wave, wave)]
        rolled = {a["record_path"].lower() for a in actors}
        recs_levels = {k: v for k, v in lapd[wave].items() if k in rolled}
        for m in sorted(rolled - set(recs_levels)):
            lv = int(next(a["level"] for a in actors if a["record_path"].lower() == m))
            recs_levels[m] = (lv, lv)
            L("§6  w%d rolled record absent from the Lap-D set, level taken from the roster "
              "basis: %s" % (wave, m))
        L("§6  wave-%d rolled actors (roster basis only): %d over %d distinct records"
          % (wave, len(actors), len(recs_levels)))
        off_rows, rr_rows = monster_offense(recs_levels)
        for r in off_rows:
            r["wave"] = wave
        for r in rr_rows:
            r["wave"] = wave
        wm = wave_mods[wave]
        L("§6  wave-%d sum_total_damage_modifier_pct = %+.1f (Lap I, pinned)" % (wave, wm))
        irows = intake(off_rows, defense, wm, sheet, actors, wave=wave)
        all_off += off_rows
        all_rr += rr_rows
        all_in += irows
        lo = [r for r in irows if r.get("level_limb") == "LO"]
        per_wave[wave] = {
            "n_actors": len(actors), "n_distinct_records": len(recs_levels),
            "wave_damage_modifier_pct": wm,
            "board_per_round_HP": {
                tag: {fld: sum(float(r.get(f"{tag}_{fld}") or 0.0) for r in lo)
                      for fld in ("direct_perpiece", "direct_aggregate",
                                  "direct_perpiece_base70abs", "dot_total")}
                for tag in ("DEFAULT", "MAX", "RUNREC", "SUMALL")},
            "board_pct_current_life_RUNREC": sum(float(r.get("RUNREC_pct_current_life") or 0.0)
                                                 for r in lo),
            "per_body_RUNREC_perpiece": {
                "median": statistics.median([float(r.get("RUNREC_direct_perpiece") or 0.0)
                                             for r in lo]) if lo else None,
                "max": max([float(r.get("RUNREC_direct_perpiece") or 0.0) for r in lo],
                           default=None)},
            "rounds_to_empty_20005_pool_RUNREC": (
                20005.0 / sum(float(r.get("RUNREC_direct_perpiece") or 0.0) for r in lo)
                if sum(float(r.get("RUNREC_direct_perpiece") or 0.0) for r in lo) > 0 else None),
            "per_second_at_declared_cadence_grid_RUNREC": {
                f"{c:.1f}s": sum(float(r.get("RUNREC_direct_perpiece") or 0.0) for r in lo) / c
                for c in (1.0, 1.5, 2.0, 2.5, 3.0)},
            "cadence_grade": ("DECLARED-GRID, NOT DECODED — monster attack-round length is "
                              "animation-driven (`characterBaseAttackSpeedTag`, a STRING tag) "
                              "and is UNREACHED from the corpus (UNREACHED-X-2)"),
        }

    h_off = dump_csv("pm4x_monster_offense.csv", all_off)
    h_rr = dump_csv("pm4x_monster_resist_reduction.csv", all_rr)
    h_in = dump_csv("pm4x_intake_by_wave.csv", all_in)
    h_pw = dump_json("pm4x_intake_board.json", per_wave)

    trows = ttk({k: v for k, v in lapd[151].items()
                 if k in {a["record_path"].lower() for a in I.rolled_actors(151, 151)}}, defense)
    h_ttk = dump_csv("pm4x_ttk_by_body.csv", trows)
    wave_mod = wave_mods[151]
    off_rows = all_off
    rr_rows = all_rr

    summary = {
        "wave_151_actors": per_wave[151]["n_actors"],
        "wave_mod_pct": wave_mod,
        "n_offense_rows": len(off_rows),
        "n_rr_rows": len(rr_rows),
        "n_records_with_nonzero_rr": len({r["record"] for r in rr_rows}),
        "per_wave": per_wave,
        "digests": {"pm4x_prediction.json": h_pred, "pm4x_formulas.json": h_form,
                    "pm4x_player_defense_terms.csv": h_pieces,
                    "pm4x_defensive_procs.csv": h_procs,
                    "pm4x_monster_offense.csv": h_off,
                    "pm4x_monster_resist_reduction.csv": h_rr,
                    "pm4x_intake_by_wave.csv": h_in, "pm4x_intake_board.json": h_pw,
                    "pm4x_ttk_by_body.csv": h_ttk},
        "pins": pins,
    }
    dump_json("pm4x_player_defense.json", defense)
    dump_json("pm4x_decode_summary.json", summary)
    (OUT / "decode.log").write_text("\n".join(log_lines) + "\n")
    L("DONE")


if __name__ == "__main__":
    main()
