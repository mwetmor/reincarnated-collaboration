#!/usr/bin/env python3
"""Stat fold for the E-s09-cp150 roster -- A6-lineage (t22_band_a_monster_stats.csv), 100% cov.

Life source chain, decoded: creature.characterAttributeEquations -> bios/*.dbr, whose
characterLife is a charLevel equation. Evaluated at the roster's own level band (from the
baton), then the creature's own characterLifeModifier and the granted-tree passives applied.

SCOPE HONESTY: A6's ehp_w{1,47,93} additionally fold Crucible wave scaling, armor and
resist mitigation. That wave-scaling ladder is NOT reproduced here -- this lap emits
base life at roster level plus every declared multiplier it can cite. eHP-with-wave-scaling
remains A6's, at its own 66/169 coverage.
READ-ONLY.
"""
import re, csv, math, collections, sys
sys.path.insert(0, "/tmp/leg_s2")
from s2_lib import E3, roster


def num(v, d=None):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def nzs(s, pref):
    for k, v in s.items():
        if k.startswith(pref):
            if isinstance(v, list) and any(x for x in v if isinstance(x, (int, float))):
                return True
            if isinstance(v, (int, float)) and v:
                return True
    return False


def evaleq(eq, charLevel):
    """Evaluate a GD attribute equation. '^' is power. Only charLevel is bound."""
    if not isinstance(eq, str) or not eq.strip():
        return None
    e = eq.replace("^", "**")
    if re.search(r'[A-Za-z_]+', e.replace("charLevel", "")):
        return None          # references a variable we do not bind (lifeRegen, elapsedTime...)
    try:
        return float(eval(e, {"__builtins__": {}}, {"charLevel": float(charLevel)}))
    except Exception:
        return None


rows = []
stat = collections.Counter()

for r in roster():
    rec, _ = E3.merged(r["record"])
    bio_p = rec.get("characterAttributeEquations")
    bio_p = bio_p if isinstance(bio_p, str) and bio_p.lower().endswith(".dbr") else ""
    bio, bown = E3.merged(bio_p) if bio_p else (None, [])
    if bio is None:
        stat["bio_ABSENT"] += 1
    else:
        stat["bio_resolved"] += 1

    lvlo = r["level_min"] if r["level_min"] != "" else None
    lvhi = r["level_max"] if r["level_max"] != "" else None
    life_eq = (bio or {}).get("characterLife", "")
    life_eq = life_eq if isinstance(life_eq, str) else ""
    base_lo = evaleq(life_eq, lvlo) if lvlo is not None else None
    base_hi = evaleq(life_eq, lvhi) if lvhi is not None else None
    if base_lo is not None:
        stat["life_MEASURED"] += 1
    elif life_eq:
        stat["life_EQ-UNEVALUABLE"] += 1
    else:
        stat["life_NO-EQUATION"] += 1

    # creature's own declared life modifier
    own_mod = num(rec.get("characterLifeModifier"), 0.0) or 0.0
    own_flat = num(rec.get("characterLife"), 0.0) or 0.0

    # granted-tree passives that move life / armor / resists
    tree_life_pct = 0.0; tree_armor = []; tree_resist = []
    for k in list(rec):
        m = re.match(r'^skillName(\d+)$', k)
        if not m:
            continue
        sp = rec[k]
        if not (isinstance(sp, str) and sp.lower().endswith(".dbr")):
            continue
        s, _ = E3.merged(sp)
        if not s:
            continue
        b = sp.rsplit("/", 1)[-1].replace(".dbr", "")
        lm = s.get("characterLifeModifier")
        if isinstance(lm, list) and lm:
            lm = max(x for x in lm if isinstance(x, (int, float)))
        if isinstance(lm, (int, float)) and lm:
            tree_life_pct += float(lm)
        if "armorbase" in b or nzs(s, "defensiveAbsorption") or nzs(s, "defensiveProtection"):
            tree_armor.append(b)
        if "resist" in b:
            tree_resist.append(b)

    dfa = evaleq((bio or {}).get("characterDefensiveAbility", ""), lvlo) if bio else None
    ofa = evaleq((bio or {}).get("characterOffensiveAbility", ""), lvlo) if bio else None

    tot_pct = own_mod + tree_life_pct
    life_lo = base_lo * (1 + tot_pct / 100.0) + own_flat if base_lo is not None else None
    life_hi = base_hi * (1 + tot_pct / 100.0) + own_flat if base_hi is not None else None
    # the baton's own post-scaling life multiplier for this record in this run
    bat_lo = r["life_modifier_pct_min"]; bat_hi = r["life_modifier_pct_max"]
    run_lo = life_lo * (1 + float(bat_lo) / 100.0) if (life_lo is not None and bat_lo != "") else None

    rows.append(dict(
        record=r["record"], display_name=r["display_name"], stratum=r["stratum"],
        level_min=lvlo, level_max=lvhi,
        bio_record=bio_p, bio_archives="|".join(bown),
        life_equation=life_eq,
        base_life_at_level_min=round(base_lo) if base_lo is not None else "",
        base_life_at_level_max=round(base_hi) if base_hi is not None else "",
        own_life_modifier_pct=own_mod, own_life_flat=own_flat,
        tree_life_modifier_pct=round(tree_life_pct, 2),
        total_declared_life_mod_pct=round(tot_pct, 2),
        life_at_level_min=round(life_lo) if life_lo is not None else "",
        life_at_level_max=round(life_hi) if life_hi is not None else "",
        baton_life_modifier_pct_min=bat_lo, baton_life_modifier_pct_max=bat_hi,
        life_run_scaled_at_level_min=round(run_lo) if run_lo is not None else "",
        defensive_ability_at_level_min=round(dfa) if dfa is not None else "",
        offensive_ability_at_level_min=round(ofa) if ofa is not None else "",
        armor_passives="|".join(sorted(set(tree_armor))),
        resist_passives="|".join(sorted(set(tree_resist))),
        life_grade=("MEASURED" if base_lo is not None else
                    ("EQ-UNEVALUABLE" if life_eq else "NO-EQUATION")),
        ehp_wave_scaled="NOT-DERIVED (A6 scope: Crucible wave ladder + mitigation)",
    ))

keys = list(rows[0].keys())
with open("/tmp/leg_s2/tg2_monster_stats.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for x in rows:
        w.writerow({k: ("" if x.get(k) is None else x.get(k)) for k in keys})
print("tg2_monster_stats.csv", len(rows), "rows,", len(keys), "cols")
print("stats:", dict(sorted(stat.items())))
