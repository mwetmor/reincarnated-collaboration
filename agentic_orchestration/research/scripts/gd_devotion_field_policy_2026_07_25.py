#!/usr/bin/env python3
"""
gd_devotion_field_policy_2026_07_25.py — the FIELD POLICY module (GATE 2) for the devotion
payload banking run. Imported by the banker; runnable standalone to print the policy census.

WHY THIS EXISTS (probe §3.1): a naive "bank every non-zero field" dump of the devotion lane
produces 117,363 rows dominated by engine scaffolding. The 10x gap between that and the
payload is a CURATION decision, not a parsing one, so it is written down as code with a
census attached — not buried in a comprehension.

POLICY, in three layers:

  L1 RECORD SCOPE  — which records are in the lane at all.
  L2 FIELD DENY    — named scaffolding/presentation fields excluded by name or prefix.
  L3 VALUE TYPE    — `exact_skill_field.canon_value` is REAL NOT NULL, so only numeric and
                     boolean values can land there. String-valued fields (record pointers,
                     enum tags) are NOT dropped — they are routed to the header `ext_json`
                     and to `devotion_power`, where they are first-class.

Everything excluded is COUNTED and NAMED by the census (`--census`), so the exclusion is
legible and auditable rather than silent.
"""
import re

# ---------------------------------------------------------------- L1 RECORD SCOPE
LANE_PREFIX = "records/skills/devotion/"

# Excluded record classes. Pet / PetPlayerScaling records under records/skills/devotion/pets/
# are MONSTER-ACTOR records (actorHeight, controller, animation tables, characterRacialProfile,
# ~120 records carrying most of the lane's 2,907 distinct field names). They are a different
# schema shape entirely and the corpus already has a monster-side store (`monster_numeric`).
# Banking them through a SKILL lane would be a category error. Excluded, named, flagged as a
# future lane -- NOT silently dropped.
EXCLUDED_CLASSES = {"Pet", "PetPlayerScaling"}
EXCLUDED_PATH_SUBSTR = ("/pets/",)

# Records that are pure registry/scaffolding, not behaviour.
EXCLUDED_RECORD_NAMES = ("_devotiontree.dbr", "_blank_passive.dbr")


def record_in_scope(record_path: str, rec: dict) -> tuple[bool, str]:
    if not record_path.startswith(LANE_PREFIX):
        return False, "outside-lane"
    if any(record_path.endswith(n) for n in EXCLUDED_RECORD_NAMES):
        return False, "registry-record"
    if any(s in record_path for s in EXCLUDED_PATH_SUBSTR):
        return False, "pet-actor-lane"
    if (rec.get("Class") or "") in EXCLUDED_CLASSES:
        return False, "pet-actor-class"
    return True, "in-scope"


# ---------------------------------------------------------------- L2 FIELD DENY
# Exact field names that are engine scaffolding, presentation, or already carried by the
# header. Each entry carries its reason so the deny-list is self-documenting.
DENY_EXACT = {
    # --- rank-axis / progression scaffolding: carried by the HEADER (rank_axis, rank_axis_max) ---
    "skillExperienceLevels":       "rank-axis XP table -> header (rank_axis_source)",
    "skillMaxLevel":               "header meta (ext_json)",
    "skillUltimateLevel":          "header meta (ext_json)",
    "skillMasteryLevelRequired":   "header meta (ext_json)",
    "skillTier":                   "header meta (ext_json)",
    # --- engine template chains: the len-44..48 arrays the probe mistook for a deeper rank axis ---
    "skillTemplates":              "engine base-template chain (string array, len 44-48)",
    "skillBlackList":              "engine template exclusion list",
    "templateName":                "engine template pointer -> header ext_json",
    "Class":                       "record class -> header record_type",
    # --- presentation ---
    "FileDescription":             "in-record display name -> header display_name",
    "skillDisplayName":            "localization tag -> header ext_json",
    "skillBaseDescription":        "localization tag -> header ext_json",
    "skillUpBitmapName":           "icon asset",
    "skillDownBitmapName":         "icon asset",
    "bitmapName":                  "icon asset",
    "bitmapNameUp":                "icon asset",
    "bitmapNameDown":              "icon asset",
    "bitmapNameInFocus":           "icon asset",
    "bitmapNameDisabled":          "icon asset",
    "bitmapPositionX":             "UI layout",
    "bitmapPositionY":             "UI layout",
    "isCircular":                  "UI layout",
    "soundNameDown":               "audio asset",
    "cameraShakeAmplitude":        "camera FX",
    "cameraShakeFrequency":        "camera FX",
    "cameraShakeDuration":         "camera FX",
    "cameraShakeDistance":         "camera FX",
}
# Prefixes that are wholesale presentation / asset / animation scaffolding.
DENY_PREFIX = (
    ("skillLevel",   "devotion-tree registry pointer (all values '0')"),
    ("skillName",    "devotion-tree registry pointer"),
    ("skillType",    "devotion-tree registry pointer"),
    ("fx",           "visual FX asset"),
    ("sound",        "audio asset"),
    ("Sound",        "audio asset"),
    ("mesh",         "art asset"),
    ("anim",         "animation asset"),
    ("Anim",         "animation asset"),
    ("actor",        "monster-actor scaffolding"),
    ("controller",   "monster-actor scaffolding"),
    ("debug",        "debug scaffolding"),
    ("ragDoll",      "ragdoll physics presentation"),
    ("charFxPak",    "visual FX asset"),
    ("targetFxPak",  "visual FX asset"),
    ("particleEffect", "visual FX asset"),
    ("lightningName",  "visual FX asset"),
    ("lineEffectName", "visual FX asset"),
    ("weaponEnchantment", "visual FX asset"),
    ("endBuffSelfNames",  "visual FX asset"),
    ("charBuffFxType",    "visual FX asset"),
)
# Substrings anywhere in the field name that mark an asset/presentation field.
DENY_SUBSTR = (
    ("BitmapName", "icon asset"),
    ("SoundName",  "audio asset"),
    ("MeshName",   "art asset"),
    ("Texture",    "art asset"),
    ("_fx",        "visual FX asset"),
    ("FXName",     "visual FX asset"),
    ("AnimSpeed",  "animation scaffolding"),
    ("AnimName",   "animation scaffolding"),
    ("Sound",      "audio asset"),
    ("AuraName",   "visual FX asset"),
    ("cameraShake", "camera FX"),
)


def field_denied(name: str):
    if name in DENY_EXACT:
        return DENY_EXACT[name]
    for p, why in DENY_PREFIX:
        if name.startswith(p):
            return why
    for s, why in DENY_SUBSTR:
        if s in name:
            return why
    return None


# ---------------------------------------------------------------- L3 PAYLOAD FAMILIES
# A field is PAYLOAD if it belongs to a behaviour family. Anything not denied and not in a
# payload family is EXCLUDED-UNCLASSIFIED and reported by name in the census -- so the
# residual is visible, not assumed empty.
PAYLOAD_FAMILY = [
    (re.compile(r"^offensive"),            "offense"),
    (re.compile(r"^defensive"),            "defense"),
    (re.compile(r"^retaliation"),          "retaliation"),
    (re.compile(r"^character"),            "character_stat"),
    (re.compile(r"^skillCooldown"),        "cadence"),
    (re.compile(r"^skillActive"),          "duration"),
    (re.compile(r"^skillLife|^skillMana|^skillEnergy"), "cost_or_sustain"),
    (re.compile(r"^skillTarget"),          "targeting"),
    (re.compile(r"^skillProjectile"),      "projectile"),
    (re.compile(r"^projectile"),           "projectile"),
    (re.compile(r"^weaponDamagePct"),      "weapon_scaling"),
    (re.compile(r"^conversion"),           "conversion"),
    (re.compile(r"^racialBonus"),          "racial_bonus"),
    (re.compile(r"^petLimit|^pet[A-Z]"),   "pet_binding"),
    (re.compile(r"^spawn"),                "summon"),
    (re.compile(r"^buffSkillName|^petSkillName|^petBonusName|^templateAutoCast"), "binding_pointer"),
    (re.compile(r"^targetingMode|^distanceProfile|^isPet"), "delivery_flag"),
    (re.compile(r"^maxRange|^minRange|^startWidth|^endWidth|^radius|^angle"), "geometry"),
    (re.compile(r"^timeBetweenAttacks|^chargeLevel|^chargeDuration"), "cadence"),
    # --- families recovered from the first census pass's "unclassified" residual ---
    # These are genuine behaviour, not scaffolding. Leaving them unclassified would have
    # silently dropped 483 rows including the ONLY authored contagion parameters in the lane.
    (re.compile(r"^damageAbsorption"),     "defense"),
    (re.compile(r"^contagion"),            "contagion"),
    (re.compile(r"^wave[A-Z]"),            "geometry"),
    (re.compile(r"^drop(Height|Radius|Variation)$"), "geometry"),
    (re.compile(r"^spark"),                "projectile"),
    (re.compile(r"^numProjectiles$|^launchAboveTarget$|^pointBlank$|^useTargetDir$"), "projectile"),
    (re.compile(r"^expansionTime$|^refreshTime$"), "cadence"),
    (re.compile(r"^instantCast$|^debufSkill$|^dispelDamageOverTime$"), "delivery_flag"),
    (re.compile(r"^\w+DamageQualifier$"),  "damage_qualifier"),
]

# GD weapon-type gating on a proc (a real mechanic — WPS/devotion procs restricted by the
# weapon in hand). Authored as bare capitalized boolean fields, so they need an exact set.
WEAPON_RESTRICTION = {
    "Axe", "Axe2h", "Mace", "Mace2h", "Sword", "Sword2h", "Spear2h",
    "Dagger", "Scepter", "Shield", "Offhand", "Ranged1h", "Ranged2h",
}


def payload_family(name: str):
    if name in WEAPON_RESTRICTION:
        return "weapon_restriction"
    for rx, fam in PAYLOAD_FAMILY:
        if rx.match(name):
            return fam
    return None


# ---------------------------------------------------------------- is_core / canon_key
# TSR-2 core = a concept that exists in D2/PoE too, so a later adapter can land into the same
# canon_key. GD-only concepts land is_core=0 as extension rows (the property the FoI slice proved).
CORE_FAMILIES = {"offense", "defense", "cadence", "duration", "cost_or_sustain",
                 "targeting", "projectile", "weapon_scaling", "geometry", "summon"}

# Curated canonical keys. Anything not here gets a MECHANICAL snake_case key and is flagged
# `canon_key_provenance='mechanical'` -- we do not silently invent canonical semantics for
# 200+ GD field names we have not actually mapped across games.
CANON_KEY = {
    "offensiveFireMin": "damage_fire_min",       "offensiveFireMax": "damage_fire_max",
    "offensiveColdMin": "damage_cold_min",       "offensiveColdMax": "damage_cold_max",
    "offensiveLightningMin": "damage_lightning_min", "offensiveLightningMax": "damage_lightning_max",
    "offensivePoisonMin": "damage_poison_min",   "offensivePoisonMax": "damage_poison_max",
    "offensiveLifeMin": "damage_vitality_min",   "offensiveLifeMax": "damage_vitality_max",
    "offensivePhysicalMin": "damage_physical_min", "offensivePhysicalMax": "damage_physical_max",
    "offensivePierceMin": "damage_pierce_min",   "offensivePierceMax": "damage_pierce_max",
    "offensiveElementalMin": "damage_elemental_min", "offensiveElementalMax": "damage_elemental_max",
    "offensiveTotalDamageModifier": "damage_total_pct",
    "offensiveLifeLeechMin": "leech_life_pct",
    "offensiveStunChance": "ailment_stun_chance_pct",
    "offensiveFreezeChance": "ailment_freeze_chance_pct",
    "skillCooldownTime": "cooldown_sec",
    "skillActiveDuration": "effect_duration_sec",
    "skillManaCost": "cost_resource",
    "skillTargetRadius": "target_radius",
    "skillTargetNumber": "target_count",
    "skillTargetAngle": "target_angle_deg",
    "weaponDamagePct": "weapon_damage_pct",
    "maxRange": "range_max",
    "startWidth": "cone_start_width",
    "endWidth": "cone_end_width",
    "timeBetweenAttacks": "cast_cadence_ms",
    "projectileLaunchNumber": "projectile_count",
    "projectilePiercingChance": "projectile_pierce_chance_pct",
    "projectileLaunchRotation": "projectile_spread_deg",
}

_SNAKE_1 = re.compile(r"(.)([A-Z][a-z]+)")
_SNAKE_2 = re.compile(r"([a-z0-9])([A-Z])")


def canon_key_for(raw_field: str) -> tuple[str, str]:
    if raw_field in CANON_KEY:
        return CANON_KEY[raw_field], "curated"
    s = _SNAKE_1.sub(r"\1_\2", raw_field)
    s = _SNAKE_2.sub(r"\1_\2", s).lower()
    return f"gd_{s}", "mechanical"


# ---------------------------------------------------------------- unit + direction
def unit_for(raw_field: str) -> str:
    n = raw_field
    if n.endswith("Chance") or "Modifier" in n or n.endswith("Pct") or "Percent" in n:
        return "gd_pct"
    if "Duration" in n or "Time" in n or n.endswith("Sec"):
        return "gd_sec"
    if "Radius" in n or "Range" in n or "Width" in n or "Distance" in n:
        return "gd_wu"
    if n.startswith("offensive") or n.startswith("retaliation"):
        return "gd_dmg"
    if n.startswith("defensive"):
        return "gd_resist"
    if "Mana" in n or "Energy" in n:
        return "gd_energy"
    return "gd_raw"


def monotonic_dir(values) -> str:
    """
    Direction-aware monotonicity. E16 finding: 22 devotion arrays are monotone DECREASING
    (resist-reduction debuffs authored as negatives; cooldown-reduction buffs) -- they grow in
    POWER while shrinking in value. A direction-blind `monotonic_class` flags those as defects.
    """
    v = [x for x in values]
    if len(v) < 2:
        return "none"
    up = all(v[i] <= v[i + 1] for i in range(len(v) - 1))
    down = all(v[i] >= v[i + 1] for i in range(len(v) - 1))
    if up and down:
        return "flat"
    if up:
        return "up"
    if down:
        return "down"
    return "none"


# ---------------------------------------------------------------- census (standalone)
def _census():
    import sys, pathlib, collections
    HERE = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE))
    from gd_arz_adapter_2026_07_24 import ArzArchive
    BASE = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
    ARCH = ["database/database.arz", "gdx1/database/GDX1.arz",
            "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]
    ars = {a: ArzArchive(BASE / a) for a in ARCH}
    union = {}
    for a in ARCH:
        for r in ars[a].records:
            union[r] = a
    DEV = sorted(r for r in union if r.startswith(LANE_PREFIX))

    scope = collections.Counter()
    naive = payload = denied = unclass = strrows = 0
    denied_names = collections.Counter()
    unclass_names = collections.Counter()
    fam_rows = collections.Counter()
    core_rows = collections.Counter()
    for r in DEV:
        try:
            rec = ars[union[r]].read_record(r)
        except Exception:
            scope["unreadable"] += 1
            continue
        ok, why = record_in_scope(r, rec)
        scope[why] += 1
        if not ok:
            continue
        for k, v in rec.items():
            vals = v if isinstance(v, list) else [v]
            nz = [x for x in vals if x not in (0, 0.0, False, "", None)]
            if not nz:
                continue
            n = len(vals)
            naive += n
            d = field_denied(k)
            if d:
                denied += n
                denied_names[k] += 1
                continue
            fam = payload_family(k)
            if fam is None:
                unclass += n
                unclass_names[k] += 1
                continue
            if isinstance(vals[0], str):
                strrows += n
                fam_rows[(fam, "string->header")] += n
                continue
            payload += n
            fam_rows[(fam, "banked")] += n
            core_rows["core" if fam in CORE_FAMILIES else "ext"] += n

    print("=" * 78)
    print("L1 RECORD SCOPE")
    for k, v in scope.most_common():
        print(f"    {k:22s} {v:5d}")
    print("\n" + "=" * 78)
    print("ROW ACCOUNTING (in-scope records only; array entries counted individually)")
    print(f"    naive  (every non-default field, arrays expanded) : {naive:7d}")
    print(f"    L2 denied (scaffolding/presentation)              : {denied:7d}")
    print(f"    L3 string-valued payload -> header/devotion_power : {strrows:7d}")
    print(f"    excluded-unclassified (residual, named below)     : {unclass:7d}")
    print(f"    ===> BANKED exact_skill_field ROWS                : {payload:7d}")
    print(f"         of which is_core=1 / is_core=0               : "
          f"{core_rows['core']} / {core_rows['ext']}")
    print("\n  payload rows by family:")
    for (fam, disp), n in sorted(fam_rows.items(), key=lambda x: -x[1]):
        print(f"    {fam:18s} {disp:16s} {n:7d}")
    print(f"\n  L2 deny-list hits: {len(denied_names)} distinct field names")
    for k, n in denied_names.most_common(20):
        print(f"    {k:44s} {n:5d} recs   [{field_denied(k)}]")
    print(f"\n  EXCLUDED-UNCLASSIFIED: {len(unclass_names)} distinct field names "
          f"(named so the residual is auditable)")
    for k, n in unclass_names.most_common(40):
        print(f"    {k:44s} {n:5d} recs")


if __name__ == "__main__":
    _census()
