#!/usr/bin/env python3
"""JOIN-1 J4b generator: D2 Fire Sorceress primary rows + per-level tables + verification.

Reads the 1.13 txt tables (fabd/diablo2 @ 45112569) from the local raw/ copy, emits
primary_rows.json (verbatim DATAMINED rows, per-level tables, gear rows) and asserts
every computed table against Basin Wiki (1-60) and the Arreat Summit (1-20).
Aborts on any mismatch.

Usage: python3 fetch_sources.py && python3 gen_j4b.py <out_dir>
"""
import csv, hashlib, json, re, sys, os

RAW = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw/"
HERE = os.path.dirname(os.path.abspath(__file__))
# Second-source page texts (Basin, Arreat) written by fetch_sources.py; default ./sources next to this script.
SRC = os.environ.get("J4B_SOURCES", os.path.join(HERE, "sources"))
OUT = sys.argv[1]

def load(fn):
    rows = list(csv.reader(open(RAW + fn, encoding="latin-1"), delimiter="\t"))
    return rows[0], rows[1:]

def sha(fn):
    return hashlib.sha256(open(RAW + fn, "rb").read()).hexdigest()

def rowdict(fn, keycol, key):
    h, rows = load(fn)
    for r in rows:
        if r and len(r) > keycol and r[keycol] == key:
            return {k: v for k, v in zip(h, r) if v != ""}
    raise KeyError((fn, key))

# ---------------------------------------------------------------- rows
SK = {}
for name in ["Fire Ball", "Meteor", "Fire Bolt", "Fire Mastery", "Warmth", "Inferno", "Blaze", "Fire Wall", "Teleport"]:
    SK[name] = rowdict("Skills.txt", 0, name)
MI = {m: rowdict("Missiles.txt", 0, m) for m in ["fireball", "meteorcenter", "meteorfire", "firebolt", "meteor", "meteortail", "meteorexplode", "fireexplosion2" if False else "fireexplode"]}
SD = {d: rowdict("SkillDesc.txt", 0, d) for d in ["fire ball", "meteor", "fire bolt", "fire mastery", "warmth"]}
SC = {}
h, rows = load("SkillCalc.txt")
for r in rows:
    if r and r[0] in ("ln12", "par8", "clc1"):
        SC[r[0]] = {k: v for k, v in zip(h, r) if v != ""}
CS = rowdict("CharStats.txt", 0, "Sorceress")
ISC = {s: rowdict("ItemStatCost.txt", 0, s) for s in ["passive_fire_mastery", "passive_fire_pierce", "manarecoverybonus", "manarecovery", "item_fastercastrate", "fireresist", "maxmana", "energy", "item_maxmana_percent", "item_elemskill", "item_addclassskills", "item_allskills"]}
PR = {p: rowdict("Properties.txt", 0, p) for p in ["extra-fire", "pierce-fire", "cast2", "cast3", "regen-mana", "sor", "fireskill", "allskills", "mana", "mana%", "enr"]}
UQ = {u: rowdict("UniqueItems.txt", 0, u) for u in ["Eschuta's temper", "Harlequin Crest", "Magefist", "Arachnid Mesh", "Mara's Kaleidoscope"]}
RW = {}
h, rows = load("Runes.txt")
for r in rows:
    d = {k: v for k, v in zip(h, r) if v != ""}
    if d.get("*runes") in ("TalThulOrtAmn", "KoVexPulThul", "DolUmBerIst"):
        RW[d["*runes"]] = d

# ---------------------------------------------------------------- formulas
def lvlbonus(n, lev):
    """D2MOO D2Common SKILLS_CalculateDamageBonusByLevel (brackets 2-8, 9-16, 17-22, 23-28, 29+)."""
    a, b, c, d, e = lev
    if n <= 1:
        return 0
    if n > 28:
        return 7 * a + e * (n - 28) + 6 * (c + d) + 8 * b
    if n > 22:
        return 7 * a + d * (n - 22) + 6 * c + 8 * b
    if n > 16:
        return 7 * a + c * (n - 16) + 8 * b
    if n > 8:
        return 7 * a + b * (n - 8)
    return a * (n - 1)

def skill_elem(row, slvl, syn_pct=0, mastery_pct=0, which="min"):
    """Skill-side elemental damage in 1/256 points (D2MOO SKILLS_GetMin/MaxElemDamage).
    shift first, synergy on the shifted value, then mastery on the post-synergy value."""
    base = int(row["EMin" if which == "min" else "EMax"])
    lev = [int(row[("EMinLev%d" if which == "min" else "EMaxLev%d") % i]) for i in range(1, 6)]
    v = (base + lvlbonus(slvl, lev)) << int(row["HitShift"])
    if syn_pct and (which == "max" or v > 256 or lev[0]):
        v += v * syn_pct // 100
    if mastery_pct:
        v += v * mastery_pct // 100
    return v

def pyre_bitrate(slvl, inferno_blvl=0, mastery_pct=0, which="min"):
    """meteorfire (missile-side, D2MOO MISSILE_GetMin/MaxElemDamage): synergy on whole points
    BEFORE the shift; ApplyMastery=1 adds Fire Mastery after."""
    m = MI["meteorfire"]
    base = int(m["EMin" if which == "min" else "Emax"])
    lev = [int(m[("MinELev%d" if which == "min" else "MaxELev%d") % i]) for i in range(1, 6)]
    v = base + lvlbonus(slvl, lev)
    pct = 3 * inferno_blvl
    if pct:
        v += v * pct // 100
    v <<= int(m["HitShift"])
    if mastery_pct:
        v += v * mastery_pct // 100
    return v

def mana(row, slvl):
    return ((int(row["mana"]) + (slvl - 1) * int(row["lvlmana"])) << int(row["manashift"])) / 256

def ln12(row, slvl, p1="Param1", p2="Param2"):
    return int(row[p1]) + (slvl - 1) * int(row[p2])

FB, ME, BO, FM, WA = SK["Fire Ball"], SK["Meteor"], SK["Fire Bolt"], SK["Fire Mastery"], SK["Warmth"]

tables = {"fire_ball": [], "meteor": [], "fire_bolt": [], "fire_mastery": [], "warmth": []}
for s in range(1, 61):
    tables["fire_ball"].append({"slvl": s, "mana_cost": mana(FB, s),
        "fire_min": skill_elem(FB, s) / 256, "fire_max": skill_elem(FB, s, which="max") / 256})
    bmin, bmax = pyre_bitrate(s), pyre_bitrate(s, which="max")
    tables["meteor"].append({"slvl": s, "mana_cost": mana(ME, s),
        "impact_fire_min": skill_elem(ME, s) / 256, "impact_fire_max": skill_elem(ME, s, which="max") / 256,
        "impact_radius_subtiles": ln12(ME, s), "impact_radius_yards": round(ln12(ME, s) * 2 / 3, 4),
        "pyre_bitrate_min_256ths_per_frame": bmin, "pyre_bitrate_max_256ths_per_frame": bmax,
        "pyre_hp_per_second_per_missile_min": round(bmin * 25 / 256, 4), "pyre_hp_per_second_per_missile_max": round(bmax * 25 / 256, 4),
        "pyre_displayed_dps_min_3_missiles": bmin * 3 * 25 // 256, "pyre_displayed_dps_max_3_missiles": bmax * 3 * 25 // 256,
        "pyre_frames_code": ln12(ME, s, "Param3", "Param4"), "pyre_frames_basin": 14 + 15 * s})
    tables["fire_bolt"].append({"slvl": s, "mana_cost": mana(BO, s),
        "fire_min": skill_elem(BO, s) / 256, "fire_max": skill_elem(BO, s, which="max") / 256})
    tables["fire_mastery"].append({"slvl": s, "fire_skill_damage_pct": ln12(FM, s)})
    tables["warmth"].append({"slvl": s, "mana_regen_pct": ln12(WA, s)})

# ---------------------------------------------------------------- verification
log = []
def num(x):
    return float(x.replace(",", ""))

def basin_series(txtfile, label, n=60):
    t = open(os.path.join(SRC, txtfile)).read()
    t = t[t.rfind("Levels 1-60"):]
    vals = []
    for m in re.finditer(re.escape(label) + r" ((?:-?[\d,]+(?:\.\d+)? )+)", t + " "):
        vals += [num(v) for v in m.group(1).split()]
    if len(vals) != n:
        raise SystemExit(f"parse {txtfile} {label}: got {len(vals)}")
    return vals

def check(name, got, want):
    if list(got) != list(want):
        bad = [(i + 1, g, w) for i, (g, w) in enumerate(zip(got, want)) if g != w]
        raise SystemExit(f"MISMATCH {name}: {bad[:5]}")
    log.append(f"{name}: exact ({len(want)} levels)")

T = tables
check("Basin Fire_Ball mana 1-60", [r["mana_cost"] for r in T["fire_ball"]], basin_series("b_Fire_Ball.txt", "Mana Cost"))
check("Basin Fire_Ball min fire 1-60", [r["fire_min"] for r in T["fire_ball"]], basin_series("b_Fire_Ball.txt", "Minimum Fire Damage"))
check("Basin Fire_Ball max fire 1-60", [r["fire_max"] for r in T["fire_ball"]], basin_series("b_Fire_Ball.txt", "Maximum Fire Damage"))
check("Basin Meteor mana 1-60", [r["mana_cost"] for r in T["meteor"]], basin_series("b_Meteor.txt", "Mana Cost"))
check("Basin Meteor min fire 1-60", [r["impact_fire_min"] for r in T["meteor"]], basin_series("b_Meteor.txt", "Minimum Fire Damage"))
check("Basin Meteor max fire 1-60", [r["impact_fire_max"] for r in T["meteor"]], basin_series("b_Meteor.txt", "Maximum Fire Damage"))
check("Basin Meteor displayed min fire/s 1-60 (3 missiles)", [r["pyre_displayed_dps_min_3_missiles"] for r in T["meteor"]], basin_series("b_Meteor.txt", "Displayed Minimum Fire Damage/S"))
check("Basin Meteor displayed max fire/s 1-60 (3 missiles)", [r["pyre_displayed_dps_max_3_missiles"] for r in T["meteor"]], basin_series("b_Meteor.txt", "Displayed Maximum Fire Damage/S"))
check("Basin Meteor seconds 1-60 = (14+15*slvl)/25", [round(r["pyre_frames_basin"] / 25, 2) for r in T["meteor"]], basin_series("b_Meteor.txt", "Seconds"))
check("Basin Fire_Mastery 1-60", [r["fire_skill_damage_pct"] for r in T["fire_mastery"]], basin_series("b_Fire_Mastery.txt", "+% Fire Skill Damage"))
check("Basin Warmth 1-60", [r["mana_regen_pct"] for r in T["warmth"]], basin_series("b_Warmth.txt", "Regenerate Mana +%"))
check("Basin Fire_Bolt min fire 1-60", [r["fire_min"] for r in T["fire_bolt"]], basin_series("b_Fire_Bolt.txt", "Minimum Fire Damage"))
check("Basin Fire_Bolt max fire 1-60", [r["fire_max"] for r in T["fire_bolt"]], basin_series("b_Fire_Bolt.txt", "Maximum Fire Damage"))

# Arreat (1-20). Arreat's damage tables include the MINIMUM synergies forced by prerequisites:
# Fire Ball needs Fire Bolt (blvl>=1 -> +14%); Meteor needs Fire Ball (+ Fire Bolt): +10%; pyre needs Inferno (via Fire Wall<-Blaze<-Inferno): +3%.
A = open(os.path.join(SRC, "arreat_fire.txt")).read()
def arreat_after(anchor, label, n=20, ranges=True):
    seg = A[A.find(anchor):]
    i = seg.find(" " + label + " ")
    seg = seg[i + len(label) + 2:]
    toks = seg.split()[:n]
    if ranges:
        return [tuple(int(x) for x in t.split("-")) for t in toks]
    return [num(t) for t in toks]

fb_ar = arreat_after("Fireball Required Level: 12", "Damage")
check("Arreat Fireball 1-20 (Fire Bolt.blvl=1, +14%)", [(skill_elem(FB, s, 14) // 256, skill_elem(FB, s, 14, which="max") // 256) for s in range(1, 21)], fb_ar)
fbm_ar = arreat_after("Fireball Required Level: 12", "Mana Cost", ranges=False)
check("Arreat Fireball mana 1-20", [mana(FB, s) for s in range(1, 21)], fbm_ar)
me_ar = arreat_after("Meteor Casting Delay", "Fire Damage")
_me = [(skill_elem(ME, s, 10) // 256, skill_elem(ME, s, 10, which="max") // 256) for s in range(1, 21)]
# KNOWN single-cell discrepancy: Arreat prints 696 for slvl 17 minimum; code gives 695 (raw 632, Basin 632; 632*256*1.10/256 = 695.2).
assert _me[16] == (695, 752) and me_ar[16] == (696, 752), (_me[16], me_ar[16])
_me_cmp = list(_me); _me_cmp[16] = me_ar[16]
check("Arreat Meteor impact 1-20", _me_cmp, me_ar)
log[-1] = "Arreat Meteor impact 1-20 (Fire Bolt=1, Fire Ball=1, +10%): 39/40 cells exact; slvl 17 minimum Arreat 696 vs code 695 (Basin raw 632 agrees with the code; 632 x 1.10 = 695.2)"
mp_ar = arreat_after("Meteor Casting Delay", "Fire Damage per second")
check("Arreat Meteor fire/s 1-20 (Inferno.blvl=1, +3%, 3 missiles)", [(pyre_bitrate(s, 1) * 75 // 256, pyre_bitrate(s, 1, which="max") * 75 // 256) for s in range(1, 21)], mp_ar)
mm_ar = arreat_after("Meteor Casting Delay", "Mana Cost", ranges=False)
check("Arreat Meteor mana 1-20 (Arreat floors to whole points)", [int(mana(ME, s)) for s in range(1, 21)], mm_ar)
bo_ar = arreat_after("Fire Bolt Required Level: 1", "Damage")
check("Arreat Fire Bolt 1-20 (no synergy)", [(skill_elem(BO, s) // 256, skill_elem(BO, s, which="max") // 256) for s in range(1, 21)], bo_ar)
fm_ar = arreat_after("Fire Mastery Required Level: 30", "Fire Damage Increase %", ranges=False)
check("Arreat Fire Mastery 1-20", [ln12(FM, s) for s in range(1, 21)], fm_ar)
wa_seg = A[A.find("Warmth Required Level: 1"):]
wa_seg = wa_seg[wa_seg.find(" 20 % ") + 6:]
check("Arreat Warmth 1-20", [ln12(WA, s) for s in range(1, 21)], [num(t) for t in wa_seg.split()[:20]])

# Spot-check of the synergy/mastery ORDER on a kit-shaped example is not possible against a
# published table (none prints mastery-applied values); the order is D2MOO + Basin Fire Mastery text.

# ---------------------------------------------------------------- loadout (kit record) resolution
def props_uq(d):
    out = []
    for i in range(1, 13):
        if f"prop{i}" in d:
            out.append({"code": d[f"prop{i}"], "param": d.get(f"par{i}", ""), "min": d.get(f"min{i}", ""), "max": d.get(f"max{i}", "")})
    return out
def props_rw(d):
    out = []
    for i in range(1, 8):
        if f"T1Code{i}" in d:
            out.append({"code": d[f"T1Code{i}"], "param": d.get(f"T1Param{i}", ""), "min": d.get(f"T1Min{i}", ""), "max": d.get(f"T1Max{i}", "")})
    return out

gear = {
    "note": "Items the kit record names (dossier.item_alterations.key_items + capstone_alterations), resolved in the 1.13 tables. Runeword props = Runes.txt T1 codes only; the runes' own socket mods (Gems.txt) are not expanded here because none of them carries FCR, +skills, +% fire skill damage or -enemy fire resist. Property -> stat via Properties.txt.",
    "uniques": {k: {"lvl_req": v.get("lvl req"), "base_code": v.get("code"), "base": v.get("*type"), "props": props_uq(v)} for k, v in UQ.items()},
    "runewords": {
        "Spirit": {"row_key": RW["TalThulOrtAmn"]["Name"], "rune_name_column": RW["TalThulOrtAmn"]["Rune Name"], "itypes": [RW["TalThulOrtAmn"].get("itype1"), RW["TalThulOrtAmn"].get("itype2")], "props": props_rw(RW["TalThulOrtAmn"])},
        "Heart of the Oak": {"row_key": RW["KoVexPulThul"]["Name"], "rune_name_column": RW["KoVexPulThul"]["Rune Name"], "itypes": [RW["KoVexPulThul"].get("itype1"), RW["KoVexPulThul"].get("itype2")], "props": props_rw(RW["KoVexPulThul"])},
        "Chains of Honor": {"row_key": RW["DolUmBerIst"]["Name"], "rune_name_column": RW["DolUmBerIst"]["Rune Name"], "itypes": [RW["DolUmBerIst"].get("itype1")], "props": props_rw(RW["DolUmBerIst"]),
                            "flag": "1.13 Runes.txt names this row 'Bound by Duty' in its Rune Name column; identified as Chains of Honor by its runes Dol-Um-Ber-Ist (same quirk as Grief='Widowmaker' in J4a)."},
    },
    "not_in_1_13": {"Flickering Flame": "No row in 1.13 UniqueItems.txt. Basin Mana page lists 'Flickering Flame helm ... (D2R only)'. The 1.13 profile must take the record's alternative, Harlequin Crest."},
    "property_codes": PR,
    "itemstatcost": ISC,
}

out = {
    "schema": "join1-j4b-primary-rows/v1",
    "date": "2026-10-01",
    "author": "legolas (UNKNOWN-RESEARCHER)",
    "commissioner": "gandalf (Run JOIN-1, wave J4b)",
    "version": "Diablo II: Lord of Destruction 1.13 txt data, expansion game. Not D2R. Where D2R differs it is flagged.",
    "label": "Every value under 'rows' is DATAMINED: copied verbatim (as strings) from the named file. Only non-empty columns are kept.",
    "source": {"repo": "https://github.com/fabd/diablo2", "commit": "45112569deb9384738ccafe5c24ebbb71f41c7c9", "path": "code/d2_113_data/",
               "local_copy": "reincarnated-collaboration/agentic_orchestration/research/datamine-acquisition/d2/raw/",
               "file_sha256": {f: sha(f) for f in ["Skills.txt", "Missiles.txt", "SkillDesc.txt", "SkillCalc.txt", "CharStats.txt", "ItemStatCost.txt", "Properties.txt", "UniqueItems.txt", "Runes.txt", "Levels.txt", "MonStats.txt"]},
               "DifficultyLevels.txt": "not re-fetched; J4a packet primary_rows.json carries its sha256 (aaa1a5d9...) and its rows; J-S7 manifest per KP-160 Q12"},
    "formula_evaluation_rule": {
        "lnXY": "ParamX + (slvl - 1) * ParamY (SkillCalc comment 'a+lvl*b'; D2MOO evaluates with slvl-1; reproduced by Arreat and Basin below).",
        "par8": "Param8 (SkillCalc 'a').",
        "mana": "((mana + (slvl-1)*lvlmana) << manashift) / 256 (D2MOO Skills.cpp; Basin 'Mana cost' lines).",
        "elemental_level_brackets": "EMin + EMinLev1*(slvl-1) for slvl 2-8; then EMinLev2 per level for 9-16, EMinLev3 for 17-22, EMinLev4 for 23-28, EMinLev5 for 29+ (D2MOO D2Common SKILLS_CalculateDamageBonusByLevel). Same for EMax / Missiles MinELev/MaxELev.",
        "HitShift": "value << HitShift gives 1/256 points. Fire Ball and Fire Bolt HitShift 7 (=half points), Meteor HitShift 8 (whole points), meteorfire HitShift 3 (=1/32 point per frame).",
    },
    "kit_scope": {
        "castable_rows": {"47": "Fire Ball", "56": "Meteor"},
        "operand_rows_pinned_by_charter": {
            "36 Fire Bolt": "CONFIRMED. blvl operand in row 47 EDmgSymPerCalc (+14%/blvl) and row 56 EDmgSymPerCalc (+5%/blvl).",
            "61 Fire Mastery": "CONFIRMED. passive_fire_mastery (stat 329) = 30 + 7*(slvl-1) %. Read by the skill-side damage (both castables) and by meteorfire (ApplyMastery=1).",
            "37 Warmth": "CONFIRMED. passivestat1 manarecoverybonus = 30 + 12*(slvl-1) %. Enters only the resource economy; it is NOT a synergy for Fire Ball or Meteor in 1.13 (no reference in either EDmgSymPerCalc)."},
        "cross_references_between_castables": "Row 47 synergy reads Meteor.blvl; row 56 synergy reads Fire Ball.blvl. Each castable is an operand of the other.",
        "operand_rows_added_v0_5_1": {
            "41 Inferno": "PINNED as the fourth operand by charter v0.5.1 (jack-ryan census Gate-2; first surfaced by this leg). Reached through Skills#56 srvmissilea meteorcenter -> Missiles meteorcenter HitSubMissile1 meteorfire -> meteorfire EDmgSymPerCalc skill('Inferno'.blvl)*3. Printed on Meteor's synergy panel: SkillDesc meteor dsc3line4 = skillname41, 'AFDImm', calc 3. Arreat: 'Inferno: +3% Average Fire Damage Per Second Per Level'. Basin: '+% Pyre Fire Damage 3 * Inferno.blvl'. Only its blvl enters the kit; Inferno is not castable here. Floor: blvl >= 1 for any Meteor caster (prerequisite chain), so the pyre always carries at least +3%."},
        "prerequisite_rows_v0_5_1": {
            "51 Fire Wall": "Meteor reqskill2 = Fire Wall. Level floor 1 hard point. Referenced by no damage or resource field of the kit rows.",
            "46 Blaze": "Fire Wall reqskill1 = Blaze; Blaze reqskill1 = Inferno (verbatim reqskill columns). Level floor 1 hard point. Referenced by no damage or resource field of the kit rows."},
        "prerequisite_chain_DATAMINED": "Meteor reqskill1 Fire Ball, reqskill2 Fire Wall; Fire Ball reqskill1 Fire Bolt; Fire Wall reqskill1 Blaze; Blaze reqskill1 Inferno (Skills.txt reqskill columns; Arreat Meteor prerequisites line 'Fire Bolt [1], Inferno [6], Blaze [12], Fire Wall [18], Fireball [12]'). Forced minimum hard points for a Meteor caster: Fire Bolt 1, Fire Ball 1, Inferno 1, Blaze 1, Fire Wall 1. Forced minimum synergies: Fire Ball +14%, Meteor impact +10%, pyre +3%.",
        "excluded": {"54 Teleport": "Named only in the kit record's motion_frame, not its skills[]; movement<->engagement BOUNDARY question for a later kit (charter J-S3b). Row included verbatim for reference only.",
                     "shield block (Sorceress BL mode, FBR law)": "EXCLUDED under the pin (charter v0.5.1). Her kit record carries a shield (Spirit Monarch), so BL is reachable in the home game; not modelled. A named fidelity cost.",
                     "Sorceress cold/lightning rows": "The Meteorb hybrid is variant-scope in the kit record (fidelity_notes)."},
    },
    "rows": {
        "Skills.txt#47 Fire Ball": SK["Fire Ball"],
        "Skills.txt#56 Meteor": SK["Meteor"],
        "Skills.txt#36 Fire Bolt": SK["Fire Bolt"],
        "Skills.txt#61 Fire Mastery": SK["Fire Mastery"],
        "Skills.txt#37 Warmth": SK["Warmth"],
        "Skills.txt#41 Inferno (operand, v0.5.1)": SK["Inferno"],
        "Missiles.txt#62 fireball": MI["fireball"],
        "Missiles.txt#101 meteorcenter": MI["meteorcenter"],
        "Missiles.txt#240 meteorfire": MI["meteorfire"],
        "Missiles.txt#58 firebolt": MI["firebolt"],
        "Missiles.txt#100 meteor (client visual)": MI["meteor"],
        "Missiles.txt#102 meteortail (client visual)": MI["meteortail"],
        "Missiles.txt#103 meteorexplode (client visual)": MI["meteorexplode"],
        "SkillDesc.txt fire ball": SD["fire ball"],
        "SkillDesc.txt meteor": SD["meteor"],
        "SkillDesc.txt fire bolt": SD["fire bolt"],
        "SkillDesc.txt fire mastery": SD["fire mastery"],
        "SkillDesc.txt warmth": SD["warmth"],
        "SkillCalc.txt": SC,
        "CharStats.txt Sorceress": CS,
    },
    "rows_prerequisite": {"Skills.txt#51 Fire Wall (floor 1)": SK["Fire Wall"], "Skills.txt#46 Blaze (floor 1)": SK["Blaze"]},
    "damage_types": {
        "rule": "Every damage component the kit emits, by type. DATAMINED from the EType / MinDam / MaxDam / SrcDam columns (an absent column is absent from the row).",
        "Fire Ball hit (Skills#47 + Missiles fireball, area radius 4 subtiles)": "FIRE only. Row 47 EType fire; no MinDam/MaxDam (no physical); no SrcDam (no weapon damage); fireball missile EType fire, no physical columns.",
        "Meteor impact (Skills#56 via meteorcenter, area radius 6 subtiles)": "FIRE only. Row 56 EType fire; no MinDam/MaxDam (no physical in 1.13); no SrcDam.",
        "Meteor pyre (Missiles meteorfire x18, per frame)": "FIRE only. meteorfire EType fire, EMin/Emax; no physical columns.",
        "Fire Bolt (operand only, never cast by this kit)": "FIRE only (row 36 EType fire).",
        "Inferno (operand only, never cast by this kit)": "its own damage is FIRE; only its blvl enters the kit.",
        "Not emitted": "physical, magic, cold, lightning, poison: none of the castable rows or their missiles carries them. No burn (STAT_FIRELENGTH) component: no ELen columns on rows 47/56/meteorfire. No leech.",
        "client-only visual missiles": "meteor, meteortail, meteorexplode, explodingarrowexp, fireexplosion2, firemedium, firesmall: CLIENT visuals spawned by pCltHitFunc/Clt* columns; the server damage path does not use them (firemedium/firesmall carry EType fire values 2/1 in the file but are spawned only as CltHitSubMissile3/4 of meteorcenter)."},
    "rows_excluded_reference_only": {"Skills.txt#54 Teleport": SK["Teleport"]},
    "fidelity_costs_named_here": ["Sorceress shield block (BL / FBR) EXCLUDED under the pin (charter v0.5.1)."],
    "missile_notes": {
        "fireball explosion_missile": "Missiles.txt fireball ExplosionMissile = 'explodingarrowexp' and CltHitSubMissile1 = 'fireexplosion2' are CLIENT visuals. The server damage radius is sHitPar1 = 4 ('damage radius'), applied by D2MOO MISSMODE_SrvHit01 around the missile's own position.",
        "meteor offsets (D2MOO MISSMODE_CreateMeteor_MoltenBoulderSubmissiles, 1.10f reconstruction; DATAMINED from code)": {
            "x": [2, -2, 0, 0, -3, 0, 3, -1, 1, -1, 2, -4, -3, -1, 0, 1, 3, 4],
            "y": [-2, -2, 2, 5, 3, 3, 3, 2, 1, -1, -1, -2, -2, -3, -4, -3, -3, -2],
            "unit": "subtiles from the impact point; step = meteorcenter sHitPar2 = 1 (all 18 spawned)"},
    },
    "per_level_tables": {
        "levels_the_kit_record_uses": "NONE. d2-fire-sorc.json pins no slvl, clvl, hard points or +skills. Its verify_ledger anchor quotes Icy Veins: '20 points to Fire Ball ... 20 points to Meteor ... 20 points to Fire Mastery' (hard points, not effective slvl). Full 1-60 tables follow; values are RAW (no synergy, no mastery) unless named.",
        "units": "fire_min/max in points (Fire Ball/Fire Bolt carry .5 because HitShift 7). pyre bit rate in 1/256 point per frame per missile.",
        **tables},
    "gear_rows": gear,
    "verification_log": log,
}
json.dump(out, open(os.path.join(OUT, "primary_rows.json"), "w"), indent=1, ensure_ascii=False)
print("\n".join(log))
print("OK")
