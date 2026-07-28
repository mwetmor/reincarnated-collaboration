#!/usr/bin/env python3
"""
NON-PRODUCTION SCRATCH — KIT-CAL-1 work-package G-5a (legolas, 2026-07-28).

Read-only resolver: given a GD monster DBR + a concrete charLevel, resolve
HP / damage / armor / speed by evaluating the .arz level-scaling machinery:

  monster.dbr
    .characterAttributeEquations -> bios/*.dbr  (characterLife/OA/DA/str/dex/int equations in charLevel)
    .skillNameN + .skillLevelN   -> nonplayerskills passives (rank-indexed arrays)

Reuses legolas's ArzArchive parser via gandalf's G-4 wrapper (import, no reimplementation).
Writes nothing outside this scratch dir.
"""
import importlib.util
import pathlib
import re
import sys
import json

G4 = pathlib.Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "gandalf/scratch/2026-07-28-kitcal1-g4-arz/g4_arz_probe.py"
)
_spec = importlib.util.spec_from_file_location("g4", G4)
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

ARCS = ["database", "GDX1", "GDX2", "GDX3"]


def rec(path):
    """Read a record from whichever archive holds it (later archives override)."""
    last = None
    for a in ARCS:
        try:
            if path in G.arc(a).records:
                last = G.arc(a).read_record(path)
        except Exception:
            continue
    if last is None:
        raise KeyError(path)
    return last


def has(path):
    for a in ARCS:
        if path in G.arc(a).records:
            return True
    return False


def evaleq(expr, charLevel):
    """Evaluate a GD attribute equation string in charLevel. ^ is power."""
    if not isinstance(expr, str) or not expr.strip():
        return None
    e = expr.replace("^", "**")
    if not re.fullmatch(r"[0-9charLevelspd\.\+\-\*\/\(\)\s\*]+", e.replace("charLevel", "")+"charLevel"):
        pass
    try:
        return eval(e, {"__builtins__": {}}, {"charLevel": float(charLevel)})
    except Exception:
        return None


def arr(v, rank):
    """Rank-indexed array lookup, 1-based rank, clamped to array bounds."""
    if v is None:
        return None
    if not isinstance(v, list):
        return v
    if not v:
        return None
    i = min(max(int(rank) - 1, 0), len(v) - 1)
    return v[i]


DMG_KEYS = [
    "offensivePhysicalMin", "offensivePhysicalMax",
    "offensivePierceRatioMin", "offensivePierceMin", "offensivePierceMax",
    "offensiveFireMin", "offensiveFireMax",
    "offensiveColdMin", "offensiveColdMax",
    "offensiveLightningMin", "offensiveLightningMax",
    "offensivePoisonMin", "offensivePoisonMax",
    "offensiveLifeMin", "offensiveLifeMax",
    "offensiveElementalMin", "offensiveElementalMax",
    "offensiveTotalDamageModifier", "offensivePhysicalModifier",
    "offensiveBleedingMin", "offensiveBleedingMax",
    "offensiveChaosMin", "offensiveChaosMax",
    "offensiveAetherMin", "offensiveAetherMax",
]
DEF_KEYS = [
    "defensiveProtection", "characterLifeModifier", "characterLife",
    "defensiveAbsorption", "defensivePhysical", "defensiveFire", "defensiveCold",
    "defensiveLightning", "defensivePoison", "defensivePierce", "defensiveAether",
    "defensiveChaos", "defensiveBleeding", "defensiveLife", "defensiveElementalResistance",
    "characterOffensiveAbility", "characterDefensiveAbility",
    "characterAttackSpeedModifier", "characterRunSpeedModifier",
    "characterTotalSpeedModifier",
]
ALL_KEYS = DMG_KEYS + DEF_KEYS


MONSTER_PAK = "records/game/balancingadjustment_mp+difficulty_enemies01.dbr"
# gameengine.dbr .monsterAttributePak; 12-elem arrays = 3 difficulties x 4 player counts.
# index = difficulty*4 + (players-1). Normal / 1 player = 0.
PAK_IDX = 0


def pak_vals():
    p = rec(MONSTER_PAK)
    out = {}
    for k, v in p.items():
        if isinstance(v, list) and len(v) == 12:
            out[k] = v[PAK_IDX]
        elif isinstance(v, (int, float)) and k != "Class":
            out[k] = v
    return out


PAK = None


def resolve(mpath, spawnLevel, verbose=False):
    """spawnLevel = the level the proxy pool assigns (f(averagePlayerLevel) via lvN.dbr).
    The monster record's own `charLevel` equation remaps that to the creature's
    effective character level, which is what every stat equation/array is indexed by."""
    global PAK
    if PAK is None:
        PAK = pak_vals()
    m = rec(mpath)
    _cl = evaleq(m.get("charLevel"), spawnLevel)
    charLevel = int(_cl) if _cl is not None else spawnLevel
    out = {
        "record": mpath,
        "spawnLevel": spawnLevel,
        "charLevelEq": m.get("charLevel"),
        "charLevel": charLevel,
        "classification": m.get("monsterClassification"),
        "minLevel": m.get("minLevel"),
        "maxLevel": m.get("maxLevel"),
        "characterAttackSpeed": m.get("characterAttackSpeed"),
        "characterRunSpeed": m.get("characterRunSpeed"),
        "walkSpeed": m.get("walkSpeed"),
        "actorRadius": m.get("actorRadius"),
        "controller": m.get("controller"),
        "bio": m.get("characterAttributeEquations"),
        "description": m.get("description"),
        "skills": [],
        "contrib": {},
    }
    # 1. base attributes from bio equations
    bio = m.get("characterAttributeEquations")
    base = {}
    if bio and has(bio):
        b = rec(bio)
        for k in ("characterLife", "characterMana", "characterStrength",
                  "characterDexterity", "characterIntelligence",
                  "characterOffensiveAbility", "characterDefensiveAbility"):
            base[k] = evaleq(b.get(k), charLevel)
        out["bio_equations"] = {k: b.get(k) for k in (
            "characterLife", "characterStrength", "characterDexterity",
            "characterIntelligence", "characterOffensiveAbility",
            "characterDefensiveAbility")}
    out["base"] = base

    # 2. skill passives, ranked by skillLevelN equation
    import collections
    acc = collections.defaultdict(list)
    for _k in ALL_KEYS:
        acc[_k] = []
    for i in range(1, 13):
        sn = m.get(f"skillName{i}")
        sl = m.get(f"skillLevel{i}")
        if not sn:
            continue
        rank = evaleq(sl, charLevel) if isinstance(sl, str) else sl
        rank = 0 if rank is None else int(rank)  # GD truncates to int skill level
        entry = {"slot": i, "skill": sn, "levelEq": sl, "rank": rank, "vals": {},
                 "class": None}
        if rank >= 1 and has(sn):
            s = rec(sn)
            entry["class"] = s.get("Class")
            # ONLY Skill_Passive entries modify the creature's own stat block.
            # Everything else (Skill_Attack*, Skill_Buff*, Skill_OnDeath*) is a
            # separately-triggered ability and must NOT be folded into base attack.
            passive = s.get("Class") == "Skill_Passive"
            for k in ALL_KEYS:
                if k in s:
                    v = arr(s[k], rank)
                    if v not in (None, 0, 0.0):
                        entry["vals"][k] = v
                        if passive:
                            acc[k].append((sn, v))
            if not passive:
                out.setdefault("abilities", []).append(
                    {"skill": sn, "class": s.get("Class"), "rank": rank,
                     "vals": entry["vals"]})
        out["skills"].append(entry)
    out["contrib"] = {k: v for k, v in acc.items() if v}

    # 3. compose — skill contributions PLUS the global monster attribute pak
    #    (gameengine.monsterAttributePak, Normal / 1 player slice)
    def S(key):
        return sum(v for _, v in acc[key])

    # --- HP
    life = base.get("characterLife") or 0.0
    life_mod = S("characterLifeModifier") + PAK.get("characterLifeModifier", 0.0)
    life_flat = S("characterLife")
    life_mult = PAK.get("characterLifeMultModifier", 0.0)      # multi-player scalar
    out["hp"] = (life + life_flat) * (1 + life_mod / 100.0) * (1 + life_mult / 100.0)
    out["hp_terms"] = {"bioBase": life, "flat": life_flat,
                       "skillModPct": S("characterLifeModifier"),
                       "pakModPct": PAK.get("characterLifeModifier", 0.0),
                       "pakMultPct": life_mult}

    # --- attributes with pak % modifiers
    dex = (base.get("characterDexterity") or 0.0) * (
        1 + PAK.get("characterDexterityModifier", 0.0) / 100.0)
    stre = (base.get("characterStrength") or 0.0) * (
        1 + PAK.get("characterStrengthModifier", 0.0) / 100.0)
    out["dex"], out["str"] = dex, stre

    # --- damage
    pmin, pmax = S("offensivePhysicalMin"), S("offensivePhysicalMax")
    # COMPOSITION RULE (see note, s.2): skill-passive TDM sources sum into ONE pool;
    # the monster attribute pak's TDM is a SEPARATE multiplicative stage. Additive
    # composition is falsified by the source: zombiemutated_a01 at its own spawn level
    # would yield -103% => negative damage, which is impossible.
    tdm_skill = S("offensiveTotalDamageModifier")
    tdm_pak = PAK.get("offensiveTotalDamageModifier", 0.0)
    tdm_mult = (1 + tdm_skill / 100.0) * (1 + tdm_pak / 100.0)
    tdm = (tdm_mult - 1) * 100.0
    dexmult = (dex / 245.0) + 1.0          # combatformulas.physicalDamageEquation
    out["dmg_terms"] = {"physMin_raw": pmin, "physMax_raw": pmax,
                        "skillTdmPct": tdm_skill, "pakTdmPct": tdm_pak,
                        "tdmMult": tdm_mult, "effTdmPct": tdm,
                        "dex": dex, "dexMult": dexmult}
    out["dmg_min"] = pmin * tdm_mult * dexmult
    out["dmg_max"] = max(pmax, pmin) * tdm_mult * dexmult
    out["dmg_maxClamped"] = pmax < pmin      # passive adds flat Min with no Max
    for el in ("Fire", "Cold", "Lightning", "Poison", "Aether", "Chaos", "Life",
               "Pierce", "Bleeding", "Elemental"):
        lo, hi = S(f"offensive{el}Min"), S(f"offensive{el}Max")
        if lo or hi:
            out.setdefault("dmg_elemental", {})[el] = [
                round(lo * tdm_mult, 1), round(max(hi, lo) * tdm_mult, 1)]

    out["armor"] = S("defensiveProtection")

    # --- OA / DA via combatformulas equations
    oa_base = (base.get("characterOffensiveAbility") or 0.0) + S("characterOffensiveAbility")
    da_base = (base.get("characterDefensiveAbility") or 0.0) + S("characterDefensiveAbility") \
        + PAK.get("characterDefensiveAbility", 0.0)
    oa_base += PAK.get("characterOffensiveAbility", 0.0)
    oa_mod = PAK.get("characterOffensiveAbilityModifier", 0.0)
    da_mod = PAK.get("characterDefensiveAbilityModifier", 0.0)
    out["OA"] = (oa_base + charLevel * 12 + dex * 0.5) * (1 + oa_mod / 100.0) + 53
    out["DA"] = (da_base + charLevel * 12 + stre * 0.5) * (1 + da_mod / 100.0) + 53

    # --- speeds (pak % modifiers)
    aspd = (m.get("characterAttackSpeed") or 1.0) * (
        1 + PAK.get("characterAttackSpeedModifier", 0.0) / 100.0)
    rspd = (m.get("characterRunSpeed") or 1.0) * (
        1 + PAK.get("characterRunSpeedModifier", 0.0) / 100.0)
    out["attackSpeed_eff"] = aspd
    out["runSpeed_eff"] = rspd

    # --- resistances: skill flats + pak flats
    RES = ("defensivePhysical", "defensiveFire", "defensiveCold", "defensiveLightning",
           "defensivePoison", "defensivePierce", "defensiveAether", "defensiveChaos",
           "defensiveBleeding", "defensiveLife")
    out["resists"] = {k.replace("defensive", ""): S(k) + PAK.get(k, 0.0)
                      for k in RES if (acc[k] or PAK.get(k, 0.0))}
    out["weaponEquipped"] = bool(m.get("chanceToEquipRightHand") or
                                 m.get("chanceToEquipLeftHand"))
    out["weaponTables"] = [m.get(f"lootRightHandItem{i}") for i in (1, 2, 3)
                           if m.get(f"lootRightHandItem{i}")]
    return out


_TAGS = None


def tags():
    """tagEnemyX -> display name, from resources/Text_EN.arc (+ expansions)."""
    global _TAGS
    if _TAGS is not None:
        return _TAGS
    _spec2 = importlib.util.spec_from_file_location(
        "arc", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
        "research/scripts/gd_arc_reader_2026_07_26.py")
    A = importlib.util.module_from_spec(_spec2)
    _spec2.loader.exec_module(A)
    V = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
    _TAGS = {}
    for arcp in sorted(V.rglob("[Tt]ext_[Ee][Nn].arc")):
        try:
            arch = A.ArcArchive(arcp)
        except Exception:
            continue
        for n in arch.names():
            if not n.lower().endswith(".txt"):
                continue
            try:
                for k, v in A.parse_tag_file(arch.read_file(n)):
                    _TAGS.setdefault(k, v)
            except Exception:
                continue
    return _TAGS


def name_of(r):
    t = r.get("description")
    return tags().get(t, t or "?")


def main():
    cmd = sys.argv[1]
    if cmd == "resolve":
        lvl = int(sys.argv[2])
        for p in sys.argv[3:]:
            print(json.dumps(resolve(p, lvl), indent=1, default=str))
    elif cmd == "table":
        lvl = int(sys.argv[2])
        rows = []
        for p in sys.argv[3:]:
            try:
                r = resolve(p, lvl)
            except KeyError:
                print(f"MISSING\t{p}")
                continue
            rows.append(r)
            flags = ("W" if r["weaponEquipped"] else "") + ("C" if r["dmg_maxClamped"] else "")
            print(f"{name_of(r)}\t{p.split('/')[-1]}\t{r['classification']}\t"
                  f"HP={r['hp']:.0f}\tdmg={r['dmg_min']:.0f}-{r['dmg_max']:.0f}\t"
                  f"armor={r['armor']:.0f}\tOA={r['OA']:.0f}\tDA={r['DA']:.0f}\t"
                  f"aspd={r['attackSpeed_eff']:.2f}\trun={r['runSpeed_eff']:.2f}\t"
                  f"elem={r.get('dmg_elemental','')}\t{flags}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
