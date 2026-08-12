#!/usr/bin/env python3
"""Second skill surface: the creature skill TREE (skillName1..N / skillLevel1..N).

UNMODELED-CONDITION CLOSURE. The 2026-08-08 harness decoded only the 8 attack SLOTS
(attackSkillName + specialAttack1..5 + initial + dying). Every creature also carries a
granted-skill tree via skillName<i>/skillLevel<i>, which holds passives (damage bonuses,
armor, resists), boss skills, auras and summons. Across the E-s09-cp150 roster that tree
is 1,733 skills against 667 slots -- 2.6x the surface the old schema saw.

This is the source of the damage_types divergence against A6 (t22_band_a_monster_stats.csv):
A6 counted tree passives such as damagebonus_physical03; the slot-only read cannot.

READ-ONLY. Same adapter, same merged() overlay stack as the slot lap.
"""
import re, csv, json, collections, sys
sys.path.insert(0, "/tmp/leg_s2")
from s2_lib import E3, roster

DIRECT = ["Physical", "Pierce", "Fire", "Cold", "Lightning", "Poison",
          "Aether", "Chaos", "Life", "Elemental"]
DOT = ["SlowPhysical", "SlowBleeding", "SlowFire", "SlowCold", "SlowLightning",
       "SlowPoison", "SlowLife", "SlowLifeLeach"]
CTRLFX = ["Stun", "Freeze", "Petrify", "Confusion", "Convert", "SlowTotalSpeed",
          "SlowRunSpeed", "SlowAttackSpeed", "SlowDefensiveAbility",
          "SlowOffensiveAbility", "SlowDamageMult", "SlowDefensiveReduction",
          "TotalDamageReductionPercent"]


def nz(v):
    if isinstance(v, list):
        return any(x for x in v if isinstance(x, (int, float)))
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0


def num(v, d=None):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def role_of(path, cls):
    """coarse functional bucket, read off the record's own folder + Class"""
    p = path.lower()
    if "/passive/" in p or cls.startswith("Skill_Passive"):
        return "passive"
    if "spawnpet" in cls.lower() or "summon" in p:
        return "summon"
    if cls.startswith(("Skill_Buff", "Skill_AttackBuff")):
        return "buff"
    if cls.startswith(("Skill_Attack", "Skill_WPAttack", "Skill_WeaponPool")):
        return "attack"
    if cls.startswith("Skill_Modifier"):
        return "modifier"
    return "other"


rows = []
stat = collections.Counter()
roll = {}

for r in roster():
    rec, _ = E3.merged(r["record"])
    idx = sorted(int(m.group(1)) for k in rec
                 for m in [re.match(r'^skillName(\d+)$', k)]
                 if m and isinstance(rec[k], str) and rec[k].lower().endswith(".dbr"))
    agg = dict(direct=set(), dot=set(), ctrl=set(), cls=[], roles=collections.Counter(),
               n=0, pets=[], unresolved=0)
    for i in idx:
        sp = rec["skillName%d" % i]
        s, own = E3.merged(sp)
        if s is None:
            stat["tree_skill_unresolved"] += 1
            agg["unresolved"] += 1
            rows.append(dict(record=r["record"], display_name=r["display_name"],
                             stratum=r["stratum"], tree_index=i, skill=sp,
                             status="UNRESOLVED-IN-ARZ"))
            continue
        cls = s.get("Class", "")
        dd = [t for t in DIRECT if nz(s.get("offensive%sMin" % t)) or nz(s.get("offensive%sMax" % t))]
        do = [t for t in DOT if nz(s.get("offensive%sMin" % t))]
        dc = [t for t in CTRLFX if nz(s.get("offensive%sMin" % t))]
        role = role_of(sp, cls)
        pet = s.get("spawnObjects") if isinstance(s.get("spawnObjects"), str) else ""
        if not pet and isinstance(s.get("spawnObjects"), list) and s["spawnObjects"]:
            pet = str(s["spawnObjects"][0])
        nr = 0
        for k, v in s.items():
            if k.startswith("offensive") and isinstance(v, list):
                nr = max(nr, len(v))
        agg["direct"] |= set(dd); agg["dot"] |= set(do); agg["ctrl"] |= set(dc)
        agg["cls"].append(cls); agg["roles"][role] += 1; agg["n"] += 1
        if pet:
            agg["pets"].append(pet.rsplit("/", 1)[-1])
        stat["role_" + role] += 1
        rows.append(dict(
            record=r["record"], display_name=r["display_name"], stratum=r["stratum"],
            tree_index=i, skill=sp, status="OK", skill_class=cls,
            skill_role=role,
            skill_level=num(rec.get("skillLevel%d" % i)),
            arz_owners="|".join(own),
            damage_types_direct="|".join(t for t in DIRECT if t in dd),
            damage_types_dot="|".join(t for t in DOT if t in do),
            control_effects="|".join(t for t in CTRLFX if t in dc),
            n_damage_ranks=nr or "",
            skill_cooldown_s=num(s.get("skillCooldownTime")),
            skill_active_duration_s=num(s.get("skillActiveDuration")),
            skill_charge_duration_s=num(s.get("skillChargeDuration")),
            skill_radius=num(s.get("skillTargetRadius")),
            skill_max_targets=num(s.get("skillTargetNumber")),
            skill_angle=num(s.get("skillTargetAngle")),
            wave_time_s=num(s.get("waveTime")), wave_distance=num(s.get("waveDistance")),
            time_between_attacks_ms=num(s.get("timeBetweenAttacks")),
            instant_cast=s.get("instantCast", ""),
            distance_profile=s.get("distanceProfile", ""),
            projectile=s.get("skillProjectileName") if isinstance(s.get("skillProjectileName"), str) else "",
            spawn_pet=pet,
            special_anim_ref=s.get("skillSpecialAnimationName")
                if isinstance(s.get("skillSpecialAnimationName"), str) else "",
        ))
    roll[r["record"]] = agg

with open("/tmp/leg_s2/tg2_skill_tree.csv", "w", newline="") as f:
    keys = []
    for x in rows:
        for k in x:
            if k not in keys:
                keys.append(k)
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for x in rows:
        w.writerow({k: ("" if x.get(k) is None else x.get(k)) for k in keys})
print("tg2_skill_tree.csv", len(rows), "rows,", len(keys), "cols")
print("stats:", dict(sorted(stat.items())))

# ---- fold the tree axes back onto the monster row (UNION of both surfaces) ----
MT = "/tmp/leg_s2/tg2_monster_timing.csv"
mrows = list(csv.DictReader(open(MT)))
for m in mrows:
    a = roll.get(m["record"])
    if not a:
        continue
    sd = set(x for x in m["damage_types"].split("|") if x)
    so = set(x for x in m["damage_types_dot"].split("|") if x)
    sc = set(x for x in m["control_effects"].split("|") if x)
    ud, uo, uc = sd | a["direct"], so | a["dot"], sc | a["ctrl"]
    m["tree_n_skills"] = a["n"]
    m["tree_unresolved"] = a["unresolved"]
    m["tree_skill_classes"] = "|".join(sorted(set(a["cls"])))
    m["tree_roles"] = "|".join(f"{k}:{v}" for k, v in sorted(a["roles"].items()))
    m["tree_damage_types"] = "|".join(t for t in DIRECT if t in a["direct"])
    m["tree_control_effects"] = "|".join(t for t in CTRLFX if t in a["ctrl"])
    m["tree_summons"] = "|".join(sorted(set(a["pets"])))
    m["n_summons"] = len(set(a["pets"]))
    m["damage_types_union"] = "|".join(t for t in DIRECT if t in ud)
    m["damage_types_union_nonphysical"] = "|".join(t for t in DIRECT if t in ud and t != "Physical")
    m["damage_types_dot_union"] = "|".join(t for t in DOT if t in uo)
    m["control_effects_union"] = "|".join(t for t in CTRLFX if t in uc)
    m["n_control_effects_union"] = len(uc)
    m["n_skills_total"] = int(m["n_slots_decoded"] or 0) + a["n"]

keys = list(mrows[0].keys())
with open(MT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for m in mrows:
        w.writerow({k: m.get(k, "") for k in keys})
print("tg2_monster_timing.csv refolded with tree axes:", len(mrows), "rows,", len(keys), "cols")
