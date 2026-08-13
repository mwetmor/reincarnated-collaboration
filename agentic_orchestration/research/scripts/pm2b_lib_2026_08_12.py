#!/usr/bin/env python3
"""KC2-PM2 Lap B shared library -- damage-magnitude / rank-resolution / spawn-chain primitives.

READ-ONLY on the vendor corpus. Extends (does not fork) the s2_* harness of
`legolas/notes/2026-08-12-kc2-roster-decode-completion/` -- `s2_lib.E3` and `s2_lib.roster()`
are imported unchanged, so the roster basis and the eight-archive overlay stack are identical.

THREE INSTRUMENT-SCHEMA CORRECTIONS THIS MODULE CARRIES (all declared in the lap README):

  IS-1  The damage-type vocabulary is DERIVED, not hand-listed. The 08-08 / 08-12 harnesses
        used a hand-written 10-name DIRECT list + 8-name DOT list. A census of every
        `offensive*` field carrying a nonzero value across the roster's 711 distinct skill
        records returns 113 populated field names spanning families the hand list never had
        (`offensiveLifeLeechMin` x42, `offensivePercentCurrentLifeMin` x73, `offensiveFumbleMin`,
        `offensiveDisruptionMin`, `offensiveTotalDamageModifier`, ...). Here the family
        taxonomy is read out of GRIM DAWN'S OWN TEMPLATE -- `templatebase/parameters_offensive.tpl`
        inside `database/templates.arc` -- so the classification is MEASURED from the source,
        not inferred from field-name spelling.

  IS-2  `skillLevel<i>` is a STRING EQUATION on every one of the 1,733 tree rows -- never a
        number. The 08-12 harness cast it with a numeric guard and therefore emitted an empty
        `skill_level` column for 100% of rows, silently. Rank assignment was structurally
        invisible to that schema. Here the equations are evaluated.

  IS-3  Spawn targets are classified by the TARGET RECORD'S `Class`, not by its path. 15 of the
        57 pet creature records live under `records/skills/.../pets/` yet carry `Class = Monster`;
        a path-prefix classifier drops them, and a path-prefix classifier equally MISCOUNTS loot
        chests (`Class = Destructible` / `FixedItemContainer`) as summons. The prior lap's
        "92 identities summon" is the path-blind count.
"""
import re
import sys
import math
import pathlib

NOTES = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-12-kc2-roster-decode-completion")
sys.path.insert(0, NOTES)
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")

from s2_lib import E3, roster, ROOT            # noqa: E402  (identical overlay stack + roster basis)
from gd_arc_reader_2026_07_26 import ArcArchive  # noqa: E402

TEMPLATES_ARC = ROOT / "database/templates.arc"
OFFENSIVE_TPL = "templatebase/parameters_offensive.tpl"

# ---------------------------------------------------------------- numeric helpers

def num(v, d=None):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def as_list(v):
    if isinstance(v, list):
        return [x for x in v if isinstance(x, (int, float)) and not isinstance(x, bool)]
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return [v]
    return []


def nonzero(v):
    return any(x != 0 for x in as_list(v))


def evaleq(eq, charLevel):
    """Evaluate a GD attribute/level equation. Only `charLevel` is bound. `^` is power.

    Lineage: s2_stats.evaleq, unchanged in semantics. Returns None when the equation
    references a variable this caller does not bind -- that is a documented gap, never a guess.
    """
    if isinstance(eq, (int, float)) and not isinstance(eq, bool):
        return float(eq)
    if not isinstance(eq, str) or not eq.strip():
        return None
    e = eq.replace("^", "**")
    if re.search(r"[A-Za-z_]+", e.replace("charLevel", "")):
        return None
    try:
        return float(eval(e, {"__builtins__": {}}, {"charLevel": float(charLevel)}))
    except Exception:
        return None


# ---------------------------------------------------------------- IS-1: template-derived taxonomy

_ASPECTS = ["DurationModifier", "DurationMin", "DurationMax", "ModifierChance", "Modifier",
            "Chance", "Global", "XOR", "Min", "Max"]

# Declared kind rule, keyed on the TEMPLATE'S OWN group name (measured), not on field spelling.
# The mapping group-name -> kind is the one reasoning step in this module; it is stated in full
# so a reader can overrule any single row of it.
_DOT_FAMILIES = {"Bleeding", "Cold", "Fire", "Life", "Lightning", "Physical", "Poison",
                 "Life Leach", "Mana Leach"}
_SLOW_DEBUFF_FAMILIES = {"Attack Speed", "Defensive Ability", "Defensive Reduction",
                         "Offensive Ability", "Offensive Reduction", "Run Speed",
                         "Total Speed", "Spell Cast Speed"}
_DIRECT_GROUPS = {"Offensive Physical", "Offensive Pierce", "Offensive Fire", "Offensive Cold",
                  "Offensive Lightning", "Offensive Poison", "Offensive Aether",
                  "Offensive Chaos", "Offensive Life", "Offensive Elemental",
                  "Offensive Disruption", "Offensive Mana Burn"}
_CONTROL_GROUPS = {"Stun", "Freeze", "Petrify", "Confusion", "Convert", "Fear", "Knockdown",
                   "Sleep", "Taunt", "Trap"}


def kind_of(group):
    g = (group or "").strip()
    if g.startswith("Offensive Slow "):
        fam = g[len("Offensive Slow "):]
        if fam in _DOT_FAMILIES:
            return "dot"
        if fam in _SLOW_DEBUFF_FAMILIES:
            return "debuff"
        return "debuff"
    if g in _DIRECT_GROUPS:
        return "direct"
    if g == "Offensive Life Leech":
        return "leech"
    if g == "Offensive Percent Current Life":
        return "percent_current_life"
    if g == "Offensive PierceRatio":
        return "armor_pierce_ratio"
    if g in _CONTROL_GROUPS:
        return "control"
    if g in ("Offensive Fumble", "Offensive Projectile Fumble"):
        return "debuff"
    if ("Modifier" in g or "Multiplier" in g or "Reduction" in g or "Resistance" in g):
        return "modifier"
    return "other"


class OffensiveTaxonomy:
    """field name -> (group, family_key, aspect, kind), read out of the shipped .tpl."""

    def __init__(self):
        arc = ArcArchive(TEMPLATES_ARC)
        text = arc.read_file(OFFENSIVE_TPL).decode("utf-8", errors="replace")
        self.group_of = {}
        cur = None
        for m in re.finditer(r'Group\s*\{\s*name\s*=\s*"([^"]+)"'
                             r'|Variable\s*\{\s*name\s*=\s*"([^"]+)"', text):
            if m.group(1):
                cur = m.group(1)
            elif m.group(2) and cur:
                self.group_of.setdefault(m.group(2), cur)
        self._cache = {}

    def split(self, field):
        """(group, family_key, aspect, kind). family_key = field minus aspect suffix."""
        if field in self._cache:
            return self._cache[field]
        aspect = ""
        base = field
        for a in _ASPECTS:
            if field.endswith(a) and len(field) > len(a):
                aspect, base = a, field[: -len(a)]
                break
        grp = self.group_of.get(field) or self.group_of.get(base + "Min") or ""
        res = (grp, base, aspect, kind_of(grp))
        self._cache[field] = res
        return res


TAX = OffensiveTaxonomy()


def offensive_families(skill_rec):
    """{family_key: {aspect: raw_value}} for every offensive family with a nonzero Min or Max."""
    fam = {}
    for k, v in skill_rec.items():
        if not k.startswith("offensive"):
            continue
        grp, base, aspect, kind = TAX.split(k)
        if not aspect:
            continue
        fam.setdefault(base, {"__group__": grp, "__kind__": kind})[aspect] = v
    return {b: d for b, d in fam.items()
            if nonzero(d.get("Min")) or nonzero(d.get("Max"))}


def n_ranks(skill_rec):
    n = 0
    for k, v in skill_rec.items():
        if k.startswith("offensive") and isinstance(v, list):
            n = max(n, len(v))
    return n


def at_rank(v, rank_used):
    """Value of a field at 1-based skill rank. Scalars are rank-invariant.

    Returns (value, grade). Grades: SCALAR / EXACT / CLAMPED-HIGH / ABSENT.
    """
    if v is None:
        return None, "ABSENT"
    if isinstance(v, list):
        vals = [x if isinstance(x, (int, float)) and not isinstance(x, bool) else 0.0 for x in v]
        if not vals:
            return None, "ABSENT"
        if rank_used is None:
            return None, "NO-RANK"
        i = int(rank_used) - 1
        if i < 0:
            return None, "RANK-BELOW-1"
        if i >= len(vals):
            return vals[-1], "CLAMPED-HIGH"
        return vals[i], "EXACT"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v), "SCALAR"
    return None, "ABSENT"


# ---------------------------------------------------------------- IS-2: rank assignment

# IS-4: the NESTED skill surface. A `Skill_Buff*` / auto-cast skill carries no damage of its
# own -- it points at a second record that does. Neither the 08-08 nor the 08-12 harness followed
# either pointer, so 89 damage-bearing records were structurally invisible to both. Census over
# this roster: 84 `buffSkillName` refs (51 damage-bearing) + 62 `autoCastSkill` refs (36
# damage-bearing); the chain runs to depth 6 and contains no cycles.
NEST_FIELDS = ["buffSkillName", "autoCastSkill"]


def nested_refs(skill_rec):
    out = []
    for f in NEST_FIELDS:
        v = skill_rec.get(f)
        if isinstance(v, str) and v.lower().endswith(".dbr"):
            out.append((f, v.lower()))
    return out


SLOT_FIELDS = [("basic", "attackSkillName"),
               ("special1", "specialAttackSkillName"),
               ("special2", "specialAttack2SkillName"),
               ("special3", "specialAttack3SkillName"),
               ("special4", "specialAttack4SkillName"),
               ("special5", "specialAttack5SkillName"),
               ("initial", "initialSkillName"),
               ("dying", "dyingSkillName")]

CHAIN_FIELDS = [("chain_initial", "chainInitialSkill"), ("chain_next", "chainNextSkill")]


def tree_entries(creature_rec):
    """[(tree_index, skill_path_lower, level_equation)] -- EVERY occurrence, duplicates kept.

    Two roster identities grant the same skill at two tree indices (nemesis_chthonickurn_01 /
    chthonickurn_teleport, nemesis_kymon_01 / kymon1_pneumabreath); both pairs carry identical
    level equations, so the duplicate costs nothing in rank terms, but dropping it would break a
    row-for-row join against tg2_skill_tree.csv. Occurrences are preserved.
    """
    out = []
    for k, v in creature_rec.items():
        m = re.match(r"^skillName(\d+)$", k)
        if not (m and isinstance(v, str) and v.lower().endswith(".dbr")):
            continue
        out.append((int(m.group(1)), v.lower(), creature_rec.get("skillLevel" + m.group(1))))
    out.sort()
    return out


def tree_of(creature_rec):
    """{skill_path_lower: (first_tree_index, level_equation_string)} -- the rank lookup."""
    out = {}
    for idx, p, lvl in tree_entries(creature_rec):
        out.setdefault(p, (idx, lvl))
    return out


def resolve_rank(level_eq, char_level, nranks):
    """(rank_raw, rank_used, grade). GD skill level 1 == array index 0."""
    if level_eq is None:
        return None, None, "NO-LEVEL-FIELD"
    raw = evaleq(level_eq, char_level)
    if raw is None:
        return None, None, "LEVEL-EQ-UNEVALUABLE"
    r = int(math.floor(raw))
    if r <= 0:
        return raw, r, "RANK-0-NOT-GRANTED"
    if nranks and r > nranks:
        return raw, nranks, "RANK-CLAMPED-TO-TABLE"
    return raw, r, "MEASURED"


# ---------------------------------------------------------------- IS-3: spawn chain

SPAWN_FIELDS = ["spawnObjects", "spawnObjects2", "spawnObjects3", "alternateSpawn"]
SPAWN_WEIGHT_FIELDS = {"spawnObjects": "spawnObjectWeights",
                       "spawnObjects2": "spawnObjectWeights2",
                       "spawnObjects3": "spawnObjectWeights3"}


def spawn_targets(skill_rec):
    """[(field, dbr_path)] for every spawn reference on a skill record."""
    out = []
    for f in SPAWN_FIELDS:
        v = skill_rec.get(f)
        if isinstance(v, str) and v.lower().endswith(".dbr"):
            out.append((f, v.lower()))
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str) and x.lower().endswith(".dbr"):
                    out.append((f, x.lower()))
    return out


def record_class(path):
    r, _ = E3.merged(path)
    return (r or {}).get("Class", ""), r


def bio_stats(creature_rec, char_level):
    """(bio_path, life, DA, OA) evaluated at char_level. Lineage: s2_stats life chain."""
    bp = creature_rec.get("characterAttributeEquations")
    bp = bp if isinstance(bp, str) and bp.lower().endswith(".dbr") else ""
    bio, _ = E3.merged(bp) if bp else (None, [])
    if bio is None:
        return bp, None, None, None
    life = evaleq(bio.get("characterLife", ""), char_level)
    da = evaleq(bio.get("characterDefensiveAbility", ""), char_level)
    oa = evaleq(bio.get("characterOffensiveAbility", ""), char_level)
    return bp, life, da, oa


def declared_life_mods(creature_rec):
    """(own_pct, own_flat, tree_pct) -- the multipliers s2_stats already validated against A6."""
    own_mod = num(creature_rec.get("characterLifeModifier"), 0.0) or 0.0
    own_flat = num(creature_rec.get("characterLife"), 0.0) or 0.0
    tree_pct = 0.0
    for p in tree_of(creature_rec):
        s, _ = E3.merged(p)
        if not s:
            continue
        lm = s.get("characterLifeModifier")
        if isinstance(lm, list) and lm:
            cand = [x for x in lm if isinstance(x, (int, float))]
            lm = max(cand) if cand else 0
        if isinstance(lm, (int, float)) and lm:
            tree_pct += float(lm)
    return own_mod, own_flat, tree_pct


def dump_csv(path, rows):
    import csv
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in keys})
    print(path, len(rows), "rows,", len(keys), "cols")
