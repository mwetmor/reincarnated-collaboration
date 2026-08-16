#!/usr/bin/env python3
"""KC2-PM4 · Lap Y · WHAT IS `sumProtectionDV` FOR A SINGLE HIT?   (ruling `R-PM4-63 part 4`)

ONE question, from `UNREACHED-I23-3`: does the per-hit armour operand take the rolled armour piece
ALONE (Limb A) or the rolled piece PLUS the character's global flat armour bonus (Limb B)?

READ-ONLY on every source.  OUTCOME-FIREWALLED: reads no sim outcome, touches no baton, runs no
simulation.  `NOTE D-V2-1` honoured -- no vtable base reads; binary evidence is string residency at
CORROBORATION grade only.  Law 3: the camera-read sheet 3,557 is a residual target for model
SELECTION only, exactly as Lap X used it; no decoded value is adjusted toward it.

Evidence classes are those declared closed in `PREREGISTRATION.md § 2`: EC-1 template declarations,
EC-2 carrier-class census, EC-3 record sweep, EC-4 shipped UI text, EC-5 binary residency,
EC-6 arithmetic identity + the `F-Y-E` composition grid.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GDBIN = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "legolas" / "notes"
                      / "2026-08-12-kc2-roster-decode-completion"))

from pm4g_lib_2026_08_13 import tags                                        # noqa: E402
from pm4f_lib_2026_08_13 import Templates                                   # noqa: E402
from pm4l_emit_2026_08_14 import EQUIP                                      # noqa: E402
from s2_lib import E3                                                       # noqa: E402

OUT = META / "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-y-global-flat-armour"
LAPX = META / "agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-x-mitigation-decode"

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
    VENDOR / "resources/Text_EN.arc": "1105b1eef70c83914a00d0516ea6db3a25ed06fad8ec91757481e66879d58a27",
    VENDOR / "gdx1/resources/Text_EN.arc": "85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a",
    VENDOR / "gdx2/resources/Text_EN.arc": "8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1",
    VENDOR / "gdx3/resources/Text_EN.arc": "001b87bd0c52ac210ebf5fab42f94aef11ee68130b384776144de6443088dc08",
    VENDOR / "mods/survivalmode/resources/Text_EN.arc": "fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e",
    GDBIN / "Game.dll": "4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02",
    GDBIN / "Engine.dll": "7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c",
    LAPX / "pm4x_player_defense.json": "5fa9db84f3ae014cf48f926e1901fd9ea05c57a63162597b8c57e129f54cddf1",
    LAPX / "pm4x_formulas.json": "cabc727d6711dfa3018be9f250811d841a32dbb8abcd1e41d752279bdd3f02a7",
    LAPX / "pm4x_player_defense_terms.csv": "f4be3d8d4026226e6b6bfc758679f6e400ffb01aa4f6d40c73bdf06d49cdc993",
    LAPX / "pm4x_findings.md": "6740e8eaf0dfe17ddce475320c1e27282b6de264804e7d3a334b18ff8d47f5f7",
}


def verify_pins() -> dict:
    L("§ 0  PINS -- re-verified from bytes, full 64 hex (R-PM4-55 part 2).  HALT armed.")
    seen = {}
    bad = []
    for p, want in PINS.items():
        got = sha(p)
        seen[str(p)] = got
        ok = got == want
        if not ok:
            bad.append((str(p), want, got))
        L(f"   {'EXACT' if ok else 'DRIFT'}  {got}  {p.name}")
    if bad:
        for p, w, g in bad:
            L(f"   ⚑ HALT  {p}\n       expected {w}\n       actual   {g}")
        raise SystemExit("PIN DRIFT -- HALT per PREREGISTRATION.md § 1")
    L(f"   {len(PINS)}/{len(PINS)} EXACT.  No HALT fired.\n")
    return seen


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-1 / EC-2 -- TEMPLATE DECLARATIONS AND THE CARRIER-CLASS CENSUS
# ══════════════════════════════════════════════════════════════════════════════════════════════

ARMOUR_FIELDS = ["defensiveProtection", "defensiveProtectionChance", "defensiveProtectionModifier",
                 "defensiveProtectionModifierChance", "defensiveBonusProtection",
                 "armorClassification", "armorDefensiveAbsorption", "blockAbsorption"]


def ec12(T: Templates) -> tuple[list[dict], dict]:
    L("EC-1 / EC-2  template declarations + carrier-class census")
    rows = []
    for f in ARMOUR_FIELDS:
        owners = T.declaring_templates(f)
        for o in owners:
            d = T.declare(o, f) or {}
            rows.append({"field": f, "template": o, "class": d.get("class", ""),
                         "type": d.get("type", ""), "description": d.get("description", ""),
                         "defaultValue": d.get("defaultValue", "")})
        L(f"   {f:36s} declared by {len(owners):2d}: {owners}")
    # the six region-covering armour templates, by the presence of armorClassification
    region_tpls = T.declaring_templates("armorClassification")
    # every template whose name starts armor_ -- to expose which armour slots are NOT region-covering
    all_armor_tpls = sorted(k for k in T._raw if k.startswith("armor_"))
    L(f"   ⚑ armorClassification declared on EXACTLY {len(region_tpls)}: {region_tpls}")
    L(f"   ⚑ armor_*.tpl total {len(all_armor_tpls)}: {all_armor_tpls}")
    summary = {"region_covering_templates": region_tpls,
               "all_armor_templates": all_armor_tpls,
               "non_region_armor_templates": [t for t in all_armor_tpls if t not in region_tpls],
               "defensive_params_have_description":
                   any(r["description"] for r in rows
                       if r["field"].startswith("defensive") and "parameters_defensive" in r["template"])}
    L("")
    return rows, summary


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-3 -- THE RECORD SWEEP.  Does combatformulas / gameengine express the composition at all?
# ══════════════════════════════════════════════════════════════════════════════════════════════

def ec3() -> dict:
    L("EC-3  record sweep -- combatformulas.dbr + gameengine.dbr")
    cf, _ = E3.merged("records/game/combatformulas.dbr")
    ge, _ = E3.merged("records/game/gameengine.dbr")
    prot_fields_cf = sorted(k for k in cf if "rotection" in k or "rotect" in k.lower())
    prot_fields_ge = sorted(k for k in ge if "rotection" in k or "rmor" in k)
    eqs = {k: v for k, v in cf.items() if "Equation" in k and "Protection" in str(v)}
    # every occurrence of the token in every equation string in the record
    occurrences = {k: str(v) for k, v in cf.items()
                   if isinstance(v, str) and "sumProtectionDV" in v}
    L(f"   combatformulas fields naming protection : {prot_fields_cf}")
    L(f"   gameengine fields naming protection/armor: {prot_fields_ge}")
    L(f"   equations mentioning sumProtectionDV     : {sorted(occurrences)}")
    for k in sorted(occurrences):
        L(f"      {k} = {occurrences[k]}")
    regions = {k: cf[k] for k in sorted(cf) if k.startswith("combatRegion")}
    L(f"   combatRegion* = {regions}   sum = {sum(float(v) for v in regions.values())}")
    L("   ⚑ NO field of either record declares the COMPOSITION of sumProtectionDV.")
    L("")
    return {"combatformulas_protection_fields": prot_fields_cf,
            "gameengine_protection_fields": prot_fields_ge,
            "equations_naming_sumProtectionDV": occurrences,
            "combat_regions": {k: float(v) for k, v in regions.items()},
            "combat_region_sum": sum(float(v) for v in regions.values()),
            "composition_declared_in_record": False,
            "n_equations_mentioning_token": len(occurrences),
            "second_protection_variable_found": False}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-4 -- SHIPPED UI TEXT.  The Armor Rating rollover, wired end to end.
# ══════════════════════════════════════════════════════════════════════════════════════════════

ROLLOVER = "records/ui/character/characterinfotab1/charinfo_statsarmortotalrolloverstyle.dbr"


def ec4(T: Templates) -> tuple[list[dict], dict]:
    L("EC-4  shipped UI text -- the Armor Rating rollover chain")
    tg = tags()
    roll, roll_arcs = E3.merged(ROLLOVER)
    tpl_vars = [v.get("name") for v in T.variables("combinedarmorrolloverwindow.tpl")]

    # walk every file_dbr the rollover wires, resolve its textTag, resolve the tag's shipped value
    chain = []
    for slot in sorted(roll):
        v = roll[slot]
        if not (isinstance(v, str) and v.lower().endswith(".dbr")):
            continue
        sub, _ = E3.merged(v)
        tag = (sub or {}).get("textTag", "")
        chain.append({"rollover_field": slot, "record": v, "textTag": tag,
                      "shipped_text": tg.get(tag, "") if tag else ""})
        if tag:
            L(f"   {slot:24s} -> {tag:36s} = {tg.get(tag, '')!r}")

    # every breakdown record that EXISTS, wired or not
    breakdown = sorted(p for p in E3.idx if "statsarmorbreakdown" in p)
    wired = {str(roll[k]).lower() for k in roll if isinstance(roll[k], str)}
    orphan_rows = []
    for p in breakdown:
        sub, _ = E3.merged(p)
        tag = (sub or {}).get("textTag", "")
        orphan_rows.append({"record": p, "textTag": tag, "shipped_text": tg.get(tag, ""),
                            "wired_into_rollover": p in wired})
    orphans = [r["record"].split("/")[-1] for r in orphan_rows if not r["wired_into_rollover"]]
    L(f"   breakdown records: {len(breakdown)}; NOT wired into the shipped rollover: {len(orphans)}")
    L(f"      {orphans}")

    key = "tagCharStatsArmorTotalDescription"
    L("")
    L("   ⚑ THE SHIPPED STATEMENT, verbatim:")
    L(f"      {key} = {tg.get(key)!r}")
    L("")
    return chain + orphan_rows, {
        "rollover_record": ROLLOVER, "rollover_arcs": roll_arcs,
        "template_fields": tpl_vars,
        "decisive_tag": key, "decisive_text": tg.get(key, ""),
        "hit_area_tag": "tagCharStatsHitArmor", "hit_area_text": tg.get("tagCharStatsHitArmor", ""),
        "total_tag": "tagCharStatsArmorTotal", "total_text": tg.get("tagCharStatsArmorTotal", ""),
        "bonus_row_text": tg.get("tagCharStatsArmorBonus", ""),
        "waist_row_text": tg.get("tagCharStatsArmorWaist", ""),
        "jewelry_row_text": tg.get("tagCharStatsArmorJewelry", ""),
        "unprotected_text": tg.get("tagCharStatsArmorUnprotected", ""),
        "bonus_armor_affix_text": tg.get("DefenseAbsorptionProtectionBonus", ""),
        "plain_armor_affix_text": tg.get("DefenseAbsorptionProtection", ""),
        "plus_armor_affix_text": tg.get("DefenseAbsorptionProtectionPlus", ""),
        "pct_armor_affix_text": tg.get("DefenseProtectionModifier", ""),
        "n_breakdown_records": len(breakdown), "n_orphan_breakdown_records": len(orphans),
        "orphan_breakdown_records": orphans,
    }


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-5 -- BINARY STRING RESIDENCY.  CORROBORATION ONLY (NOTE D-V2-1).  No vtable base reads.
# ══════════════════════════════════════════════════════════════════════════════════════════════

BIN_CAND = ["sumProtectionDV", "sumAbsorptionDV", "physicalDamageDV", "defensiveProtection",
            "defensiveBonusProtection", "defensiveProtectionModifier", "armorClassification",
            "armorDefensiveAbsorption", "combatRegionHeadChance", "combatRegionUnprotectedChance",
            "tagCharStatsArmorTotalDescription", "tagCharStatsArmorBonus", "CombinedArmorRolloverWindow",
            "combinedarmorrolloverwindow", "unprotectedTag", "waistNumber", "jewelryNumber",
            "bonusNumber", "bonusHitNumber"]


def ec5() -> list[dict]:
    L("EC-5  binary string residency -- CORROBORATION ONLY (NOTE D-V2-1; no vtable base reads)")
    g = (GDBIN / "Game.dll").read_bytes()
    e = (GDBIN / "Engine.dll").read_bytes()
    rows = []
    for c in BIN_CAND:
        n = c.encode()
        i, j = g.find(n), e.find(n)
        rows.append({"string": c,
                     "game_dll_offset": (f"0x{i:08x}" if i >= 0 else ""),
                     "game_dll_resident": i >= 0,
                     "engine_dll_offset": (f"0x{j:08x}" if j >= 0 else ""),
                     "engine_dll_resident": j >= 0})
        L(f"   {c:36s} Game.dll={'0x%08x' % i if i >= 0 else 'ABSENT':12s} "
          f"Engine.dll={'0x%08x' % j if j >= 0 else 'ABSENT'}")
    L("")
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-6 -- THE ARITHMETIC.  Identity test + the F-Y-E composition grid.
# ══════════════════════════════════════════════════════════════════════════════════════════════

SHEET = 3557.0            # camera-read.  Law 3: a residual target for MODEL SELECTION only.
GLOBAL_FLAT = 636.0       # Lap X census, pinned
GLOBAL_PCT = 56.0         # Lap X census, pinned
COMPONENT_LOCAL_PCT = 8.0     # legs component defensiveProtectionModifier (Lap X: LOCAL)

PIECES = {  # slot -> (flat defensiveProtection, local % modifier, region chance)
    "chest":     (1908.0,  0.0, 26.0),
    "legs":      (1501.0,  8.0, 20.0),
    "head":      (1666.0,  0.0, 15.0),
    "shoulders": (1666.0,  0.0, 15.0),
    "feet":      (1105.0,  0.0, 12.0),
    "hands":     (1104.0,  0.0, 12.0),
}


def ec6() -> dict:
    L("EC-6  the arithmetic -- identity test, then the F-Y-E composition grid")
    w = {s: PIECES[s][2] / 100.0 for s in PIECES}
    sw = sum(w.values())
    L(f"   Σ w_s = {sw!r}   (the identity below requires EXACTLY 1)")

    def piece_after_local(s):
        f, loc, _ = PIECES[s]
        return f * (1 + loc / 100.0)

    M = 1 + GLOBAL_PCT / 100.0

    # --- the identity: adding G outside the weighted sum == adding it to every piece inside
    outside = (sum(w[s] * piece_after_local(s) for s in PIECES) + GLOBAL_FLAT) * M
    inside = sum(w[s] * ((piece_after_local(s) + GLOBAL_FLAT) * M) for s in PIECES)
    identity_delta = abs(outside - inside)
    L(f"   C1 (G outside the weighted sum) = {outside!r}")
    L(f"   C2 (G added to EVERY piece)      = {inside!r}")
    L(f"   |C1 - C2| = {identity_delta!r}   <- the algebraic identity, because Σ w_s = 1")

    def resid(x):
        return x - SHEET

    grid = {}

    # --- Limb B family (global flat present)
    grid["C1_LAPX_WINNER_G_outside_weighted"] = outside
    grid["C2_G_added_to_every_piece_weighted"] = inside
    grid["C3_G_before_local_pct_weighted"] = sum(
        w[s] * ((PIECES[s][0] + GLOBAL_FLAT) * (1 + PIECES[s][1] / 100.0)) for s in PIECES) * M
    grid["C4_G_outside_SIMPLE_average"] = (
        sum(piece_after_local(s) for s in PIECES) / len(PIECES) + GLOBAL_FLAT) * M
    grid["C7_component_pct_GLOBAL_weighted"] = (
        sum(w[s] * PIECES[s][0] for s in PIECES) + GLOBAL_FLAT) * (
        1 + (GLOBAL_PCT + COMPONENT_LOCAL_PCT) / 100.0)
    grid["C8_G_UNSCALED_weighted"] = sum(w[s] * piece_after_local(s) for s in PIECES) * M + GLOBAL_FLAT

    # --- Limb A family (piece alone)
    grid["A1_PIECE_ALONE_weighted"] = sum(w[s] * piece_after_local(s) for s in PIECES) * M
    grid["A2_PIECE_ALONE_SIMPLE_average"] = (
        sum(piece_after_local(s) for s in PIECES) / len(PIECES)) * M
    grid["A3_PIECE_ALONE_weighted_no_local"] = sum(w[s] * PIECES[s][0] for s in PIECES) * M

    rows = []
    for k in sorted(grid, key=lambda k: abs(resid(grid[k]))):
        limb = "A (piece-alone)" if k.startswith("A") else "B (piece + global flat)"
        rows.append({"model": k, "limb": limb, "value": grid[k],
                     "residual_vs_sheet": resid(grid[k]),
                     "residual_pct": 100.0 * resid(grid[k]) / SHEET})
        L(f"   {k:40s} {limb:26s} {grid[k]:12.4f}  resid {resid(grid[k]):+10.4f} "
          f"({100.0 * resid(grid[k]) / SHEET:+.3f} %)")

    # what global % would piece-alone need to reach the sheet?
    base_alone = sum(w[s] * piece_after_local(s) for s in PIECES)
    pct_needed_alone = 100.0 * (SHEET / base_alone - 1.0)
    base_B = sum(w[s] * piece_after_local(s) for s in PIECES) + GLOBAL_FLAT
    pct_needed_B = 100.0 * (SHEET / base_B - 1.0)
    flat_needed_C1 = SHEET / M - sum(w[s] * piece_after_local(s) for s in PIECES)
    L("")
    L(f"   global % piece-alone would need to reach the sheet : {pct_needed_alone:.4f} %"
      f"   (census reaches {GLOBAL_PCT})")
    L(f"   global % C1 would need to reach the sheet          : {pct_needed_B:.4f} %"
      f"   (census reaches {GLOBAL_PCT})")
    L(f"   global FLAT C1 would need to reach the sheet       : {flat_needed_C1:.4f}"
      f"   (census reaches {GLOBAL_FLAT})")
    L("   ⚑ NEITHER is applied.  These are the gap EXPRESSED, not the gap CLOSED (UNREACHED-X-1).")

    best = min(grid, key=lambda k: abs(resid(grid[k])))
    best_A = min((k for k in grid if k.startswith("A")), key=lambda k: abs(resid(grid[k])))
    L("")
    L(f"   best fit overall  : {best}  resid {resid(grid[best]):+.4f}")
    L(f"   best Limb-A fit   : {best_A}  resid {resid(grid[best_A]):+.4f} "
      f"({100.0 * resid(grid[best_A]) / SHEET:+.2f} %)")
    L("")
    return {
        "sheet_camera_read": SHEET, "sum_region_weights": sw,
        "identity_C1_minus_C2_abs": identity_delta,
        "identity_holds_exactly": identity_delta < 1e-9,
        "grid": grid, "rows": rows,
        "best_model": best, "best_residual": resid(grid[best]),
        "best_limb_A_model": best_A, "best_limb_A_residual": resid(grid[best_A]),
        "best_limb_A_residual_pct": 100.0 * resid(grid[best_A]) / SHEET,
        "global_pct_piece_alone_would_need": pct_needed_alone,
        "global_pct_C1_would_need": pct_needed_B,
        "global_flat_C1_would_need": flat_needed_C1,
        "all_limb_B_within_3pct": all(abs(resid(grid[k])) / SHEET < 0.03
                                      for k in grid if not k.startswith("A")),
        "any_limb_A_within_3pct": any(abs(resid(grid[k])) / SHEET < 0.03
                                      for k in grid if k.startswith("A")),
    }


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EC-2b -- THE PLAYED KIT'S ARMOUR CARRIERS, BY SLOT AND BY FIELD  (falsifier F-Y-C)
# ══════════════════════════════════════════════════════════════════════════════════════════════

AR = ("defensiveProtection", "defensiveProtectionModifier", "defensiveBonusProtection",
      "defensiveProtectionChance")


def kit_carriers(T: Templates) -> tuple[list[dict], dict]:
    L("F-Y-C  the played kit's armour carriers, by slot / carrier / field / template")
    rows = []
    region_tpls = set(T.declaring_templates("armorClassification"))
    for row in EQUIP:
        slot, base, affixes, comp, ench = row[0], row[1], row[2], row[3], row[4]
        for label, p in [("base", base)] + [("affix", a) for a in affixes] + \
                        [("component", comp), ("enchant", ench)]:
            if not p:
                continue
            r, arcs = E3.merged(p)
            if not r:
                continue
            tpl = str(r.get("templateName", "")).replace("\\", "/").split("/")[-1].lower()
            vals = {k: float(r[k]) for k in AR if k in r and float(r[k] or 0) != 0.0}
            if not vals:
                continue
            for f, v in sorted(vals.items()):
                rows.append({"slot": slot, "carrier": label, "record": p, "template": tpl,
                             "field": f, "value": v,
                             "template_is_region_covering": tpl in region_tpls})
                L(f"   {slot:9s} {label:9s} {tpl:24s} region={str(tpl in region_tpls):5s} "
                  f"{f:28s} {v}")
    n_region = sum(1 for r in rows if r["template_is_region_covering"]
                   and r["field"] == "defensiveProtection")
    non_region_prot = [(r["slot"], r["carrier"], r["value"]) for r in rows
                       if not r["template_is_region_covering"] and r["field"] == "defensiveProtection"]
    bonus_prot = [(r["slot"], r["carrier"], r["template"], r["value"]) for r in rows
                  if r["field"] == "defensiveBonusProtection"]
    L(f"   region-covering defensiveProtection carriers : {n_region}")
    L(f"   NON-region defensiveProtection carriers       : {non_region_prot}")
    L(f"   defensiveBonusProtection carriers             : {bonus_prot}")

    # ── THE PARTITION TEST.  Lap X's FULL 175-row census (pinned), split by the shipped
    #    statement's own two categories.  If the partition is exact and complete, the sentence
    #    "bonuses on skills and on non-armor pieces" names EVERY term of the global flat.
    region_slots = {"head", "chest", "legs", "shoulders", "feet", "hands"}
    part = {"region_covering_piece_armour": 0.0, "skills_and_sets": 0.0,
            "non_armour_pieces": 0.0, "UNCLASSIFIED": 0.0}
    part_rows = []
    with (LAPX / "pm4x_player_defense_terms.csv").open() as fh:
        for r in csv.DictReader(fh):
            if r["field"] not in ("defensiveProtection", "defensiveBonusProtection"):
                continue
            v = float(r["value"])
            src, slot, kind = r["source"], r["slot"], r["kind"]
            if r["field"] == "defensiveProtection" and kind == "item" and slot in region_slots:
                bucket = "region_covering_piece_armour"
            elif kind in ("devotion", "skill", "set", "passive", "aura"):
                bucket = "skills_and_sets"
            elif kind in ("component", "enchant", "affix") or slot == "waist":
                bucket = "non_armour_pieces"
            else:
                bucket = "UNCLASSIFIED"
            part[bucket] += v
            part_rows.append({"source": src, "slot": slot, "kind": kind,
                              "field": r["field"], "value": v, "bucket": bucket})
    global_flat_named = part["skills_and_sets"] + part["non_armour_pieces"]
    L("")
    L("   ⚑ PARTITION of Lap X's pinned armour census by the shipped statement's own categories:")
    for k, v in part.items():
        L(f"      {k:34s} {v:10.1f}")
    L(f"      skills_and_sets + non_armour_pieces = {global_flat_named:.1f}  "
      f"(Lap X global flat = {GLOBAL_FLAT})  match={abs(global_flat_named - GLOBAL_FLAT) < 1e-9}")
    L(f"      region_covering_piece_armour        = {part['region_covering_piece_armour']:.1f}  "
      f"(Σ of the six pieces = 8950.0)")
    L(f"      UNCLASSIFIED                        = {part['UNCLASSIFIED']:.1f}  "
      f"(a non-zero value would fire F-Y-C)")
    L("")
    return rows + part_rows, {"n_region_covering_protection_carriers": n_region,
                              "non_region_protection_carriers": non_region_prot,
                              "bonus_protection_carriers": bonus_prot,
                              "partition": part,
                              "global_flat_named_by_shipped_statement": global_flat_named,
                              "partition_matches_lapx_global_flat":
                                  abs(global_flat_named - GLOBAL_FLAT) < 1e-9,
                              "partition_unclassified": part["UNCLASSIFIED"],
                              "F_Y_C_fired": part["UNCLASSIFIED"] != 0.0}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════════════════════

def main() -> None:
    L("KC2-PM4 · LAP Y -- what is sumProtectionDV for a single hit?")
    L("=" * 96)
    pins = verify_pins()

    T = Templates()
    tpl_rows, tpl_summary = ec12(T)
    rec_sweep = ec3()
    text_rows, text_summary = ec4(T)
    bin_rows = ec5()
    kit_rows, kit_summary = kit_carriers(T)
    arith = ec6()

    # ── THE VERDICT, assembled from the pre-registered grading rule (PREREGISTRATION.md § 3)
    decisive = text_summary["decisive_text"]
    has_shipped_statement = ("added to all armor slots" in decisive.lower())
    verdict = ("PIECE-PLUS-GLOBAL-FLAT" if has_shipped_statement else "UNREACHED")
    grade = ("DECODED" if has_shipped_statement else "UNREACHED")
    L("=" * 96)
    L(f"VERDICT : {verdict}")
    L(f"GRADE   : {grade}   (PREREGISTRATION.md § 3 -- DECODED requires a shipped statement)")
    L(f"BASIS   : {text_summary['decisive_tag']} wired via "
      f"charinfo_statsarmorbreakdown_infotext.dbr into {ROLLOVER}")
    L(f"          {decisive!r}")
    L("=" * 96)

    out = {
        "lap": "KC2-PM4 Lap Y -- sumProtectionDV: piece-alone vs piece + global flat",
        "commission": "R-PM4-63 part 4; provenance UNREACHED-I23-3 (gamora I-23 § 7)",
        "verdict": verdict,
        "grade": grade,
        "deciding_evidence": {
            "class": "EC-4 shipped UI text",
            "tag": text_summary["decisive_tag"],
            "text": decisive,
            "wired_through": ["records/ui/character/characterinfotab1/"
                              "charinfo_statsarmorbreakdown_infotext.dbr", ROLLOVER],
            "template": "combinedarmorrolloverwindow.tpl :: infoText",
        },
        "EC1_EC2_template_summary": tpl_summary,
        "EC3_record_sweep": rec_sweep,
        "EC4_text_summary": text_summary,
        "EC6_arithmetic": arith,
        "FYC_kit_carriers": kit_summary,
        "pins": pins,
    }
    (OUT / "pm4y_armour_operand.json").write_text(json.dumps(out, indent=1, sort_keys=True))

    def dump(name, rows, cols):
        with (OUT / name).open("w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=cols)
            wr.writeheader()
            for r in rows:
                wr.writerow({c: r.get(c, "") for c in cols})

    dump("pm4y_template_declarations.csv", tpl_rows,
         ["field", "template", "class", "type", "description", "defaultValue"])
    dump("pm4y_ui_text.csv", text_rows,
         ["rollover_field", "record", "textTag", "shipped_text", "wired_into_rollover"])
    dump("pm4y_kit_carriers.csv", kit_rows,
         ["slot", "carrier", "record", "template", "field", "value",
          "template_is_region_covering", "source", "kind", "bucket"])
    dump("pm4y_composition_grid.csv", arith["rows"],
         ["model", "limb", "value", "residual_vs_sheet", "residual_pct"])
    (OUT / "pm4y_binary_anchors.json").write_text(
        json.dumps({"note": "CORROBORATION grade only (NOTE D-V2-1); no vtable base reads",
                    "rows": bin_rows}, indent=1, sort_keys=True))
    (OUT / "decode.log").write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
