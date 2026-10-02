#!/usr/bin/env python3
"""
corpus_js4b_referent_mint_2026_10_02.py -- JOIN-1 J-S4b: mint the KC2 referent Warlord's corpus record.

Owner: elrond (data steward). Conductor: gandalf, Run JOIN-1 (charter v0.6.1; KC2 ledger KP-237,
Matt-approved). Occasioned by jack-ryan J0/J1 Gate-2 (qa/findings/2026-10-02-join1-j0-j1-gate2.md)
EL-1 (sibling build), EL-2 (original_element semantics + export fields), EL-3 (no numeric rows).

WHAT IT DOES
    Adds ONE new kit `gd-eor-warlord-referent` (Matt's actual EoR Warlord: EoRWarlGuts, grimtools
    b28gD0KN, save FILE b8e6f510...bfa5) beside the guide build `gd-eor-warlord`, which it never
    touches. Writes: 1 canon_corpus row, 1 kit_mapping row, N kit_numeric rows, 1 corpus_schema_meta
    row. DATA-ONLY: no DDL. Then writes the JSON export + a FILE-sha256 manifest.

LAWS HELD
    * Derive, don't relay: every value is READ from its source when this runs (pack JSON, pack-source
      CSVs, GD Edition IV .arz, the decoded save). Nothing below is a retyped number except the
      identity labels and the per-row source-path selectors.
    * No value is invented. Where no source settles a value it is UNKNOWN in the export with what
      would settle it; kit_numeric gets no row for it.
    * Agreement with the KC2 pack of record v3.11 is CHECKED, not assumed. A disagreement is a
      FINDING printed in the export and the report; it never edits the value or the pack.
    * Dual-column law: kit_numeric.source_value is the anchored value; rdr_value stays NULL and
      rule_id NULL. rdr derivation is the normalization-rule owner's act (gamora), not elrond's.
    * gd-eor-warlord is not modified: its ROWSET digest is computed before and after and asserted equal.

USAGE
    python3 corpus_js4b_referent_mint_2026_10_02.py --dry-run   # in-memory copy, zero bytes written to corpus.db
    python3 corpus_js4b_referent_mint_2026_10_02.py --apply     # backup, write, assert, export, manifest
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import json
import math
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gd_arz_adapter_2026_07_24 as ARZ  # noqa: E402  (read-only TQIT reader)

COLLAB = HERE.parents[2]
CURATED = HERE.parent / "curated"
DB = CURATED / "corpus.db"
EXPORT_DIR = CURATED / "kits-export"
KIT = "gd-eor-warlord-referent"
SIBLING = "gd-eor-warlord"

ENGINE = pathlib.Path.home() / "Games" / "reincarnated-engine"
PACK = ENGINE / "src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
PACK_DIGEST_OF_RECORD = "997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788"
KC2 = ENGINE / "data/kc2"
PM2 = KC2 / "pm2_measured_player_sheet.csv"
PM4G = KC2 / "pm4g_played_kit.csv"
PM4L = KC2 / "pm4l_eor_per_hit.csv"
LEG = COLLAB / "agentic_orchestration/legolas"
PACKET = LEG / "research/2026-10-01-eor-warlord-animation-and-gear/packet.json"
PACKET_README = LEG / "research/2026-10-01-eor-warlord-animation-and-gear/README.md"
SAVE = LEG / "scratch/2026-08-05-eorwarlguts-parse/player.gdc"
SAVE_DECODE = LEG / "scratch/2026-08-05-eorwarlguts-parse/p_gdc.json"
SAVE_SHA_OF_RECORD = "b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5"
GD4 = pathlib.Path.home() / "Games/vendor/grim-dawn-edition-IV-20260929"
ARCHIVES = [("base", GD4 / "database/database.arz"), ("gdx1", GD4 / "gdx1/database/GDX1.arz"),
            ("gdx2", GD4 / "gdx2/database/GDX2.arz"), ("gdx3", GD4 / "gdx3/database/GDX3.arz")]
GD4_BUILD = "Edition IV, build 24825149 (grim-dawn-edition-IV-20260929)"

SCHEMA_META_VERSION = "join1-js4b-referent-mint-2026-10-02"
ROWSET_TABLES = ["canon_corpus", "kit_mapping", "kit_numeric", "kit_composition", "kit_citations",
                 "kit_dossier", "kit_deviation", "kit_delta_t4", "kit_acceptance_assert",
                 "kit_door_arg", "skill_geometry_band", "verify_ledger"]
EXPECT_BEFORE = {"canon_corpus": 590, "kit_mapping": 574, "kit_numeric": 458, "kit_master": 574,
                 "corpus_schema_meta": 38}


def sha_file(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def jload(p: pathlib.Path):
    return json.loads(p.read_text())


# ----------------------------------------------------------------------------------- sources
def load_sources():
    src = {}
    # pack of record: verify every member digest and the pack digest by its own law
    man = jload(PACK / "manifest.json")
    lines = {}
    for m in man["members"]:
        rp = m.get("relpath") or m.get("path")
        real = sha_file(PACK / rp)
        assert real == m["sha256"], f"pack member digest mismatch: {rp}"
        lines[rp] = real
    dg = hashlib.sha256("\n".join(f"{r}  {lines[r]}" for r in sorted(lines)).encode("utf-8")).hexdigest()
    assert dg == man["pack_digest"] == PACK_DIGEST_OF_RECORD, "pack digest is not the v3.11 pack of record"
    src["pack_members"] = lines
    for name in ("player_kit", "rng_contract", "math_rules", "provenance", "summons"):
        src[name] = jload(PACK / "model" / f"{name}.json")
    # pack-source CSVs: verify the digests the pack's provenance pins
    prov_txt = (PACK / "model/provenance.json").read_text() + (PACK / "model/player_kit.json").read_text()
    for p in (PM2, PM4G):
        h = sha_file(p)
        assert h in prov_txt or h[:32] in prov_txt, f"{p.name} sha not pinned by pack provenance"
    src["pm2"] = {r["stat"]: r for r in csv.DictReader(PM2.open())}
    src["pm4g"] = list(csv.DictReader(PM4G.open()))
    src["pm4l"] = {r["quantity"]: r for r in csv.DictReader(PM4L.open())}
    src["packet"] = jload(PACKET)
    assert sha_file(SAVE) == SAVE_SHA_OF_RECORD, "save FILE digest is not b8e6f510...bfa5"
    sd = jload(SAVE_DECODE)
    assert sd["file"] == "player.gdc" and sd["file_size"] == SAVE.stat().st_size
    src["save"] = sd
    # GD Edition IV: expansion-wins precedence (gdx3 > gdx2 > gdx1 > base)
    arcs = [(n, ARZ.ArzArchive(p)) for n, p in ARCHIVES]
    src["arz_sha"] = {n: hashlib.sha256(a.raw).hexdigest() for n, a in arcs}

    def dbr(path):
        for n in ("gdx3", "gdx2", "gdx1", "base"):
            a = dict(arcs)[n]
            if path in a.records:
                return n, a.read_record(path)
        raise KeyError(path)
    src["dbr"] = dbr
    return src


# ----------------------------------------------------------------------------------- helpers
def f32(x: float) -> float:
    """Present an IEEE-754 float32 DB value at 7 significant digits (the precision the file holds)."""
    return float(f"{x:.7g}")


def rank_idx(arr, rank):
    """GD rank arrays are 1-based in game terms; index rank-1. A scalar applies at every rank."""
    if isinstance(arr, list):
        return arr[rank - 1]
    return arr


def close(a, b, tol=1e-6):
    return a is not None and b is not None and math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)


def pk_row(rows, rid):
    for r in rows:
        if r.get("id") == rid:
            return r
    raise KeyError(rid)


# ----------------------------------------------------------------------------------- build
def build(src):
    pk, rng, mr, sm = src["player_kit"], src["rng_contract"], src["math_rules"], src["summons"]
    pm2, pm4l, dbr = src["pm2"], src["pm4l"], src["dbr"]
    pm4g = {r["skill_record"]: r for r in src["pm4g"]}
    v3p2 = pk["⚑ v3p2_rows"]
    x1 = {r["record_path"]: r for r in pk["⚑ v3p4_rows"]["x1_per_cast_energy_cost"]}
    binds = {b["skill_id"]: b for b in pk["binding_model"]["bindings"]}
    s13 = pk["⚑ v3p6p1_rows"]["s13_secondary_streams"]
    v12 = mr["⚑ v3p2_rows"]

    def v12row(rid):
        for k, rows in v12.items():
            if isinstance(rows, list):
                for r in rows:
                    if r.get("id") == rid:
                        return r
        raise KeyError(rid)

    eor_arc, eor = dbr("records/skills/playerclass09/eyeofreckoning1.dbr")
    sf_arc, sf = dbr("records/skills/playerclass09/eyeofreckoning2.dbr")
    gm_arc, gmod = dbr("records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr")
    gs_arc, guts = dbr("records/items/gearweapons/melee2h/d107_blunt2h.dbr")
    ge_arc, geng = dbr("records/game/gameengine.dbr")
    pc_arc, pc = dbr("records/creatures/pc/malepc01.dbr")
    vm_arc, vm = dbr("records/skills/playerclass09/viremight1.dbr")
    wc_arc, wc = dbr("records/skills/playerclass01/warcry1.dbr")
    bz_arc, bz = dbr("records/skills/playerclass01/blitz1.dbr")
    as_arc, asc = dbr("records/skills/playerclass09/ascension1.dbr")
    ru_arc, rune = dbr("records/skills/itemskillsgdx2/runes/rush_d203.dbr")
    sg_arc, sguard = dbr("records/skills/playerclass09/summon_celestialguardian1.dbr")
    sd_arc, sdeath = dbr("records/skills/itemskillsgdx1/relics/summondeathstalker.dbr")

    def DM(arc, rec, field, idx=None):
        return f"DATAMINED {GD4_BUILD} {arc.upper()} {rec}::{field}" + (f"[rank {idx}]" if idx else "")

    ch = pk["channel"]
    eor_total = pk["fixture"]["eor_rank_total"]                 # PACK 26
    eor_alloc = ch["rank"]["value"]                             # PACK 15 (PRV-LAP-2D-SAVE)
    rows = []

    def row(key, value, scale, unit, grades, evidence, pack=None, pack_alt=None, note=None):
        """pack = (row_id, value) the pack of record carries for this exact quantity, or None if silent.
        pack_alt = further pack rows carrying the same quantity (checked too)."""
        rows.append(dict(numeric_key=key, value=float(value), scale=scale, unit=unit, grades=grades,
                         evidence=evidence, pack=pack, pack_alt=pack_alt or [], note=note))

    # ---------------- Eye of Reckoning (the channel) ----------------
    E = "records/skills/playerclass09/eyeofreckoning1.dbr"
    row("eor_radius_m", eor["skillTargetRadius"], "gd_metres", "m", ["DATAMINED", "PACK"],
        [DM(eor_arc, E, "skillTargetRadius")],
        pack=("player_kit.json::channel.radius_m (PRV-BATON-V1)", ch["radius_m"]["value"]),
        note="V17-HITTEST-1: a TRUE UNIFORM DISC re-centred every tick; no angular gate, no target cap")
    row("eor_tick_period_s", rng["tick"]["tick_period_s"]["value"], "gd_seconds", "s", ["PACK"],
        ["law tick = 0.16 s x 100/AS% (INFERRED-strong, legolas PE-1 s1.4) reproduces it at AS 196"],
        pack=("rng_contract.json::tick.tick_period_s (PRV-MPOL2-SEAL)", rng["tick"]["tick_period_s"]["value"]))
    row("eor_ticks_per_s", round(1.0 / rng["tick"]["tick_period_s"]["value"], 9), "gd_per_second", "Hz", ["PACK"],
        ["1 / tick_period_s, rounded to 9 decimals (the pack note calls 12.25 a terminating rational)"],
        pack=("player_kit.json::v3p2_rows.v15_energy V15-1 note ('16.0 x 12.25 x 0.90 = 176.4')", 12.25))
    row("eor_time_between_attacks_db", eor["timeBetweenAttacks"], "gd_ms_quanta", "0.8 ms quanta",
        ["DATAMINED"], [DM(eor_arc, E, "timeBetweenAttacks"),
                        f"oracle-source pm4l channel_timeBetweenAttacks = {pm4l['channel_timeBetweenAttacks']['value']}"],
        note="x0.8 quantum (200 -> 0.16 s) holds on 9 channel skills (PE-1 s1.3); WHY is UNKNOWN")
    row("eor_period_at_100pct_as_s", float(pm4l["channel_period_at_100pct_AS"]["value"]), "gd_seconds", "s",
        ["DATAMINED"], ["Text_EN tagGDX2Class09SkillDescription07A 'every 0.16s at 100% Attack Speed' (legolas packet, CLIENT-VERBATIM)",
                        "oracle-source pm4l channel_period_at_100pct_AS"])
    row("eor_channel_tail_s", eor["duration"], "gd_seconds", "s", ["DATAMINED", "PACK"],
        [DM(eor_arc, E, "duration") + " (useResetsDuration=1)"],
        pack=("player_kit.json::channel.channel_tail_s (PRV-BATON-V1)", ch["channel_tail_s"]["value"]))
    row("eor_rotation_speed_multiplier", f32(eor["rotationSpeedMultiplier"]), "gd_ratio", "x", ["DATAMINED", "PACK"],
        [DM(eor_arc, E, "rotationSpeedMultiplier") + f" (f32 {eor['rotationSpeedMultiplier']!r})"],
        pack=("player_kit.json::channel.rotation_speed_multiplier (PRV-BATON-V1)", ch["rotation_speed_multiplier"]["value"]))
    row("eor_mana_cost_per_tick_r26", rank_idx(eor["skillManaCost"], eor_total), "gd_energy", "energy/tick",
        ["DATAMINED", "PACK"], [DM(eor_arc, E, "skillManaCost", eor_total)],
        pack=("player_kit.json::v3p2_rows.v15_energy V15-6", pk_row(v3p2["v15_energy"], "V15-6")["value"]))
    row("eor_energy_cost_factor", pk_row(v3p2["v15_energy"], "V15-7")["value"], "gd_ratio", "x", ["PACK", "FOOTAGE"],
        [f"FOOTAGE PRV-PLAYER-SHEET skill_energy_cost {pm2['skill_energy_cost']['value']}% (screenshot 514)"],
        pack=("player_kit.json::v3p2_rows.v15_energy V15-7 (MEASURED-EXACT-SOURCE-UNLOCATED)", pk_row(v3p2["v15_energy"], "V15-7")["value"]))
    row("eor_drain_per_s", ch["drain_rate_per_s"]["value"], "gd_energy_per_second", "energy/s", ["PACK"],
        ["V15-1 CLIENT-VERBATIM in-video tooltip; applied PER_TICK"],
        pack=("player_kit.json::channel.drain_rate_per_s (PRV-EOR-SPIN)", ch["drain_rate_per_s"]["value"]),
        pack_alt=[("player_kit.json::v3p2_rows.v15_energy V15-1", pk_row(v3p2["v15_energy"], "V15-1")["value"])])
    save_eor = next(s for s in src["save"]["blocks"]["character_skills"]["skills"]
                    if s["skill-name"] == E)
    row("eor_rank_allocated", save_eor["level"], "gd_rank", "rank", ["SAVE", "PACK"],
        [f"SAVE player.gdc {SAVE_SHA_OF_RECORD[:8]}...::character_skills[{E}].level"],
        pack=("player_kit.json::channel.rank (PRV-LAP-2D-SAVE)", eor_alloc))
    row("eor_rank_total", eor_total, "gd_rank", "rank", ["PACK", "DATAMINED"],
        ["DATAMINED grants: Gutsmasher augmentSkillLevel2 +4, Warborn Visor +2, Warborn Chestguard +2, "
         "Sandreaver Bracers +2, Kaisan's Burning Eye augmentAllLevel +1 (legolas C-2, 2026-08-08); "
         f"15 + 11 = 26 = skillUltimateLevel {eor['skillUltimateLevel']}"],
        pack=("player_kit.json::fixture.eor_rank_total", eor_total),
        pack_alt=[("pack-source pm4g_played_kit.csv eyeofreckoning1 rank_effective (PRV played kit)", float(pm4g[E]["rank_effective"])),
                  ("oracle-source pm4l eor_rank_effective (the oracle's run-of-record rank)", float(pm4l["eor_rank_effective"]["value"]))])
    row("eor_weapon_damage_pct_skill_r26", rank_idx(eor["weaponDamagePct"], eor_total), "gd_pct", "%",
        ["DATAMINED"], [DM(eor_arc, E, "weaponDamagePct", eor_total)])
    row("eor_weapon_damage_pct_gutsmasher_mod", gmod["weaponDamagePct"], "gd_pct", "%", ["DATAMINED", "FOOTAGE"],
        [DM(gm_arc, "mace2h_d107_eyeofreckoning.dbr", "weaponDamagePct"),
         f"FOOTAGE PRV-PLAYER-SHEET eye_of_reckoning_weapon_damage {pm2['eye_of_reckoning_weapon_damage']['value']}% (screenshot 495)"])
    wd1 = v12row("V1-WD-1")["value"]
    row("eor_weapon_damage_pct_total_r26", rank_idx(eor["weaponDamagePct"], eor_total) + gmod["weaponDamagePct"],
        "gd_pct", "%", ["PACK", "DATAMINED"], ["skill 50 + Gutsmasher 14 (Warborn set +5 gated off at 3 pieces)"],
        pack=("player_kit.json::channel.weapon_damage_pct (PRV-PLAYER-SHEET)", ch["weapon_damage_pct"]["value"]),
        pack_alt=[("math_rules.json::v3p2_rows.v1_leech_ladder V1-WD-1 oracle_reads (rank 20; HONEST-FAIL ABS-EOR-RANK-OF-RECORD)",
                   wd1["oracle_reads"]["pct"])])
    row("eor_weapon_damage_pct_oracle_leech_r20", wd1["oracle_reads"]["pct"], "gd_pct", "%", ["PACK"],
        ["the operand the ORACLE reads for %WD leech; rank 20 = 15+1+0+4 (pm4l) omits Visor/Chest/Sandreaver +6"],
        pack=("math_rules.json::v3p2_rows.v1_leech_ladder V1-WD-1 value.oracle_reads.pct", wd1["oracle_reads"]["pct"]),
        note="recorded so B0-N can reproduce the oracle exactly; it is NOT the rank-of-record value")
    row("eor_fire_to_physical_conversion_pct", gmod["conversionPercentage"], "gd_pct", "%", ["DATAMINED", "FOOTAGE"],
        [DM(gm_arc, "mace2h_d107_eyeofreckoning.dbr", "conversionPercentage") +
         f" ({gmod['conversionInType']}->{gmod['conversionOutType']})",
         f"FOOTAGE PRV-PLAYER-SHEET eye_of_reckoning_fire_to_physical {pm2['eye_of_reckoning_fire_to_physical']['value']}%",
         f"oracle-source pm4l eor_conversion_skill_scoped '{pm4l['eor_conversion_skill_scoped']['value']}'"])
    row("eor_flat_physical_min_r26", rank_idx(eor["offensivePhysicalMin"], eor_total), "gd_flat_damage", "damage",
        ["DATAMINED"], [DM(eor_arc, E, "offensivePhysicalMin", eor_total)])
    row("eor_flat_physical_max_r26", rank_idx(eor["offensivePhysicalMax"], eor_total), "gd_flat_damage", "damage",
        ["DATAMINED"], [DM(eor_arc, E, "offensivePhysicalMax", eor_total)])
    row("eor_flat_fire_min_r26", rank_idx(eor["offensiveFireMin"], eor_total), "gd_flat_damage", "damage",
        ["DATAMINED"], [DM(eor_arc, E, "offensiveFireMin", eor_total) + " -- 100% converted to physical by Gutsmasher's EoR modifier"])
    bl = pk_row(s13, "S13-BL-FLAT")["value"]["components"]
    row("eor_bleed_flat_gutsmasher", gmod["offensiveSlowBleedingMin"], "gd_flat_damage", "damage/3s", ["DATAMINED", "PACK"],
        [DM(gm_arc, "mace2h_d107_eyeofreckoning.dbr", "offensiveSlowBleedingMin")],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-BL-FLAT components[mace2h_d107_eyeofreckoning]",
              bl["mace2h_d107_eyeofreckoning.offensiveSlowBleedingMin"]))
    row("eor_bleed_flat_sandreaver", bl["hands_d206_eyeofreckoning.offensiveSlowBleedingMin"], "gd_flat_damage", "damage/3s",
        ["PACK"], ["hands_d206_eyeofreckoning.dbr offensiveSlowBleedingMin, as carried by the pack"],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-BL-FLAT components[hands_d206_eyeofreckoning]",
              bl["hands_d206_eyeofreckoning.offensiveSlowBleedingMin"]))
    row("eor_bleed_base_duration_s", gmod["offensiveSlowBleedingDurationMin"], "gd_seconds", "s", ["DATAMINED", "PACK"],
        [DM(gm_arc, "mace2h_d107_eyeofreckoning.dbr", "offensiveSlowBleedingDurationMin")],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-BL-BASE-DUR", pk_row(s13, "S13-BL-BASE-DUR")["value"]))
    row("eor_bleed_modifier_pct_eor_scoped", gmod["offensiveSlowBleedingModifier"], "gd_pct", "%", ["DATAMINED", "PACK"],
        [DM(gm_arc, "mace2h_d107_eyeofreckoning.dbr", "offensiveSlowBleedingModifier")],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-BL-MOD-EOR", pk_row(s13, "S13-BL-MOD-EOR")["value"]))

    # ---------------- Soulfire (EoR's orbiting secondary) ----------------
    SF = "records/skills/playerclass09/eyeofreckoning2.dbr"
    row("soulfire_period_s", f32(sf["projectilePeriod"]), "gd_seconds", "s", ["DATAMINED", "PACK"],
        [DM(sf_arc, SF, "projectilePeriod") + f" (f32 {sf['projectilePeriod']!r})"],
        pack=("player_kit.json::channel.soulfire.period_s", ch["soulfire"]["period_s"]),
        pack_alt=[("player_kit.json::v3p6p1_rows.s13 S13-SF-PERIOD", f32(pk_row(s13, "S13-SF-PERIOD")["value"])),
                  ("player_kit.json::v3p2_rows.v15_energy V15-8", pk_row(v3p2["v15_energy"], "V15-8")["value"])])
    row("soulfire_explosion_radius_m", f32(sf["projectileExplosionRadius"]), "gd_metres", "m", ["DATAMINED", "PACK"],
        [DM(sf_arc, SF, "projectileExplosionRadius")],
        pack=("player_kit.json::channel.soulfire.explosion_radius_m", ch["soulfire"]["explosion_radius_m"]))
    row("soulfire_projectiles_per_proc", sf["skillProjectileNumber"], "gd_count", "count", ["DATAMINED", "PACK"],
        [DM(sf_arc, SF, "skillProjectileNumber")],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-SF-PROJ", pk_row(s13, "S13-SF-PROJ")["value"]))
    row("soulfire_flat_lightning", pk_row(s13, "S13-SF-FLAT")["value"], "gd_flat_damage", "damage", ["PACK"],
        ["eyeofreckoning2.dbr lightning damage at rank 13 (MEASURED-BY-PROSE, as carried by the pack)"],
        pack=("player_kit.json::v3p6p1_rows.s13 S13-SF-FLAT", pk_row(s13, "S13-SF-FLAT")["value"]))

    # ---------------- player sheet ----------------
    PS = "PRV-PLAYER-SHEET pm2_measured_player_sheet.csv"
    row("player_attack_speed_pct", ch["attack_speed_pct"]["value"], "gd_pct_sheet", "%", ["PACK", "FOOTAGE"],
        [f"FOOTAGE {PS} attack_speed {pm2['attack_speed']['value']} (screenshot 511)"],
        pack=("player_kit.json::channel.attack_speed_pct (PRV-PLAYER-SHEET)", ch["attack_speed_pct"]["value"]),
        pack_alt=[("pm2 attack_speed (the PRV-PLAYER-SHEET source row)", float(pm2["attack_speed"]["value"]))],
        note="the sheet's own APS/weapon-APS ratio implies 182.19% (pm4l attack_speed_implied_by_APS); the pack runs 196")
    for key, stat, scale, unit, shot in [
            ("player_cast_speed_pct", "cast_speed", "gd_pct_sheet", "%", "514"),
            ("player_run_speed_pct", "run_speed", "gd_pct_sheet", "%", "511"),
            ("player_attacks_per_second", "attacks_per_second", "gd_per_second", "attacks/s", "511"),
            ("weapon_attacks_per_second", "weapon_attacks_per_second", "gd_per_second", "attacks/s", "495"),
            ("player_offensive_ability", "offensive_ability", "gd_points", "OA", "495/508"),
            ("player_critical_damage_pct", "critical_damage", "gd_pct_sheet", "%", "511"),
            ("player_level", "level", "gd_level", "level", "495/508 + gdc header")]:
        row(key, float(pm2[stat]["value"]), scale, unit, ["FOOTAGE"],
            [f"FOOTAGE {PS} {stat} (screenshot {shot}); pinned by pack provenance, not lifted as a pack row"])
    for key, stat, rid, grp, scale, unit in [
            ("player_hp_max", "health_max", "V16-1", "v16_player_fixture", "gd_hp", "hp"),
            ("player_energy_max", "energy_max", "V15-3", "v15_energy", "gd_energy", "energy"),
            ("player_energy_regen_per_s", "energy_regeneration", "V15-2", "v15_energy", "gd_energy_per_second", "energy/s"),
            ("player_energy_usable_ceiling", "energy_current", "V15-5", "v15_energy", "gd_energy", "energy"),
            ("player_defensive_ability", "defensive_ability", "V2-SHEET-02", "v2_player_defensive_sheet", "gd_points", "DA"),
            ("player_armor_rating_sheet", "armor_rating", "V2-SHEET-03", "v2_player_defensive_sheet", "gd_points", "armor"),
            ("player_adcth_pct", "life_steal_adcth", "V2-SHEET-05", "v2_player_defensive_sheet", "gd_pct_sheet", "%"),
            ("player_hp_regen_per_s", "health_regeneration", "V2-SHEET-06", "v2_player_defensive_sheet", "gd_hp_per_second", "hp/s"),
            ("player_resist_physical_pct", "resist_physical", "V2-RESIST-11", "v2_player_defensive_sheet", "gd_pct_sheet", "%")]:
        pv = pk_row(v3p2[grp], rid)["value"]
        row(key, float(pm2[stat]["value"]), scale, unit, ["FOOTAGE", "PACK"],
            [f"FOOTAGE {PS} {stat}"], pack=(f"player_kit.json::v3p2_rows.{grp} {rid}", pv))
    row("player_energy_reserved", pk_row(v3p2["v15_energy"], "V15-4")["value"], "gd_energy", "energy", ["PACK"],
        ["MO-2: aura reservation, binding-derived"],
        pack=("player_kit.json::v3p2_rows.v15_energy V15-4", pk_row(v3p2["v15_energy"], "V15-4")["value"]))
    v164 = pk_row(v3p2["v16_player_fixture"], "V16-4")["value"]
    row("player_v_ref_m_per_s", v164["value"], "gd_metres_per_second", "m/s", ["PACK"],
        ["DECLARED-FREE-PARAMETER (player base m/s is named-absent from the corpus); derived 5.4 = 4.0 x 1.35"],
        pack=("player_kit.json::v3p2_rows.v16_player_fixture V16-4 (DECLARED-FREE-PARAMETER)", v164["value"]),
        note="NOT a measurement: the pack labels it a free parameter")
    row("player_attack_speed_cap_pct", geng["playerAttackSpeedCapMax"], "gd_pct_sheet", "%", ["DATAMINED"],
        [DM(ge_arc, "records/game/gameengine.dbr", "playerAttackSpeedCapMax")])
    row("player_run_speed_cap_pct", geng["playerRunSpeedCapMax"], "gd_pct_sheet", "%", ["DATAMINED"],
        [DM(ge_arc, "records/game/gameengine.dbr", "playerRunSpeedCapMax") + " -- the measured 135% sits AT the cap"])
    row("pc_base_attack_speed", pc["characterAttackSpeed"], "gd_ratio", "x", ["DATAMINED"],
        [DM(pc_arc, "records/creatures/pc/malepc01.dbr", "characterAttackSpeed")])
    row("pc_base_cast_speed", pc["characterSpellCastSpeed"], "gd_ratio", "x", ["DATAMINED"],
        [DM(pc_arc, "records/creatures/pc/malepc01.dbr", "characterSpellCastSpeed")])

    # ---------------- Gutsmasher ----------------
    G = "records/items/gearweapons/melee2h/d107_blunt2h.dbr"
    row("gutsmasher_base_attack_speed", f32(guts["characterBaseAttackSpeed"]), "gd_ratio", "x", ["DATAMINED"],
        [DM(gs_arc, G, "characterBaseAttackSpeed") + " (tagAttackSpeedVerySlow)"])
    row("gutsmasher_physical_min", guts["offensivePhysicalMin"], "gd_flat_damage", "damage", ["DATAMINED", "FOOTAGE"],
        [DM(gs_arc, G, "offensivePhysicalMin"), f"FOOTAGE {PS} weapon_base_damage {pm2['weapon_base_damage']['value']}"])
    row("gutsmasher_physical_max", guts["offensivePhysicalMax"], "gd_flat_damage", "damage", ["DATAMINED", "FOOTAGE"],
        [DM(gs_arc, G, "offensivePhysicalMax"), f"FOOTAGE {PS} weapon_base_damage {pm2['weapon_base_damage']['value']}"])
    row("gutsmasher_chaos_to_physical_pct", guts["conversionPercentage"], "gd_pct", "%", ["DATAMINED"],
        [DM(gs_arc, G, "conversionPercentage") + f" ({guts['conversionInType']}->{guts['conversionOutType']})",
         f"FOOTAGE {PS} weapon_chaos_to_physical_conversion {pm2['weapon_chaos_to_physical_conversion']['value']}% DISAGREES"])
    row("gutsmasher_lightning_to_physical_pct", guts["conversionPercentage2"], "gd_pct", "%", ["DATAMINED"],
        [DM(gs_arc, G, "conversionPercentage2") + f" ({guts['conversionInType2']}->{guts['conversionOutType2']})",
         f"FOOTAGE {PS} weapon_lightning_to_physical_conversion {pm2['weapon_lightning_to_physical_conversion']['value']}% DISAGREES"])

    # ---------------- the other bar skills ----------------
    def skill_rows(prefix, rec_path, arc, rec, bind_id, x1_path=None, eff_rank=None):
        g = pm4g[rec_path]
        er = eff_rank if eff_rank is not None else (int(g["rank_effective"]) if g["rank_effective"] else 1)
        if g["rank_allocated"]:
            row(f"{prefix}_rank_allocated", float(g["rank_allocated"]), "gd_rank", "rank", ["SAVE"],
                [f"SAVE via pack-source pm4g_played_kit.csv rank_allocated (player.gdc block 8, MEASURED)"])
            row(f"{prefix}_rank_effective", er, "gd_rank", "rank", ["PACK-SOURCE"] + (["PACK"] if x1_path else []),
                [f"pack-source pm4g_played_kit.csv rank_effective, basis '{g['rank_effective_basis']}' "
                 "(omits item-specific +skill grants by construction)"],
                pack=((f"player_kit.json::v3p4_rows.x1 {x1[x1_path]['id']}.value.total_rank",
                       float(x1[x1_path]["value"]["total_rank"])) if x1_path else None))
        if "skillCooldownTime" in rec:
            cd = f32(rec["skillCooldownTime"])
            bpack = None
            alt = []
            if bind_id and bind_id in binds and binds[bind_id].get("cooldown_s"):
                bpack = (f"player_kit.json::binding_model.bindings[{bind_id}].cooldown_s (PRV-LAP-2D-SAVE)",
                         binds[bind_id]["cooldown_s"]["value"])
            if x1_path:
                alt.append((f"player_kit.json::v3p4_rows.x1 {x1[x1_path]['id']}.value.cooldown_s", x1[x1_path]["value"]["cooldown_s"]))
            row(f"{prefix}_cooldown_s", cd, "gd_seconds", "s", ["DATAMINED"] + (["PACK"] if bpack else []),
                [DM(arc, rec_path, "skillCooldownTime")], pack=bpack or (alt[0] if alt else None),
                pack_alt=alt if bpack else alt[1:])
        if "skillManaCost" in rec:
            mc = rank_idx(rec["skillManaCost"], er)
            xp = (f"player_kit.json::v3p4_rows.x1 {x1[x1_path]['id']}.value.parent_skillManaCost",
                  x1[x1_path]["value"]["parent_skillManaCost"]) if x1_path else None
            row(f"{prefix}_mana_cost_r{er}", mc, "gd_energy", "energy/cast", ["DATAMINED"] + (["PACK"] if xp else []),
                [DM(arc, rec_path, "skillManaCost", er if isinstance(rec["skillManaCost"], list) else None)], pack=xp)
        return er

    VMP = "records/skills/playerclass09/viremight1.dbr"
    skill_rows("vires_might", VMP, vm_arc, vm, "vires_might", VMP)
    row("vires_might_target_radius_m", f32(vm["skillTargetRadius"]), "gd_metres", "m", ["DATAMINED"],
        [DM(vm_arc, VMP, "skillTargetRadius") + f"; endRadiusMultiplier {vm['endRadiusMultiplier']}"])
    WCP = "records/skills/playerclass01/warcry1.dbr"
    wer = skill_rows("war_cry", WCP, wc_arc, wc, "war_cry", WCP)
    wcrow = pk_row(v3p2["v13_potion_and_warcry"], "V13-WARCRY-1")["value"]
    row(f"war_cry_radius_m_r{wer}", f32(rank_idx(wc["skillTargetRadius"], wer)), "gd_metres", "m", ["DATAMINED"],
        [DM(wc_arc, WCP, "skillTargetRadius", wer)],
        pack=("player_kit.json::v3p2_rows.v13_potion_and_warcry V13-WARCRY-1 value.skill_target_radius_m", wcrow["skill_target_radius_m"]),
        note="presentation-scale only in the oracle (legolas open question 5)")
    row("war_cry_duration_s", wcrow["duration_s"], "gd_seconds", "s", ["PACK"], ["V13-WARCRY-1 of-record limb COOLDOWN"],
        pack=("player_kit.json::v3p2_rows.v13_potion_and_warcry V13-WARCRY-1 value.duration_s", wcrow["duration_s"]))
    row("war_cry_damage_reduction_pct", wcrow["reduction_pct"], "gd_pct", "%", ["PACK"], ["V13-WARCRY-1"],
        pack=("player_kit.json::v3p2_rows.v13_potion_and_warcry V13-WARCRY-1 value.reduction_pct", wcrow["reduction_pct"]))
    BZP = "records/skills/playerclass01/blitz1.dbr"
    skill_rows("blitz", BZP, bz_arc, bz, "blitz", BZP)
    ASP = "records/skills/playerclass09/ascension1.dbr"
    k6 = v12row("V12-K6")["value"]
    skill_rows("ascension", ASP, as_arc, asc, None, None)
    rows[-2]["pack"] = ("math_rules.json::v3p2_rows V12-K6 value.cooldown_s", k6["cooldown_s"])
    rows[-2]["grades"] = ["DATAMINED", "PACK"]
    row("ascension_duration_s", asc["skillActiveDuration"], "gd_seconds", "s", ["DATAMINED", "PACK"],
        [DM(as_arc, ASP, "skillActiveDuration")], pack=("math_rules.json::v3p2_rows V12-K6 value.duration_s", k6["duration_s"]))
    row("ascension_absorb_points", k6["absorb_points"], "gd_points", "absorb", ["PACK"], ["V12-K6 (DECODED, kc2/counterplay.py)"],
        pack=("math_rules.json::v3p2_rows V12-K6 value.absorb_points", k6["absorb_points"]))
    RUP = "records/skills/itemskillsgdx2/runes/rush_d203.dbr"
    skill_rows("violent_delights", RUP, ru_arc, rune, "rune_of_rush", RUP, eff_rank=1)
    row("violent_delights_weapon_damage_pct", rune["weaponDamagePct"], "gd_pct", "%", ["DATAMINED"],
        [DM(ru_arc, RUP, "weaponDamagePct")])
    row("violent_delights_target_radius_m", f32(rune["skillTargetRadius"]), "gd_metres", "m", ["DATAMINED"],
        [DM(ru_arc, RUP, "skillTargetRadius")])
    SGP = "records/skills/playerclass09/summon_celestialguardian1.dbr"
    ger = skill_rows("guardian_of_empyrion", SGP, sg_arc, sguard, None, None)
    row(f"guardian_of_empyrion_pet_limit_r{ger}", rank_idx(sguard["petLimit"], ger), "gd_count", "pets", ["DATAMINED"],
        [DM(sg_arc, SGP, "petLimit", ger)])
    SDP = "records/skills/itemskillsgdx1/relics/summondeathstalker.dbr"
    skill_rows("deathstalker", SDP, sd_arc, sdeath, None, None, eff_rank=1)
    row("deathstalker_pet_limit", sdeath["petLimit"], "gd_count", "pets", ["DATAMINED"], [DM(sd_arc, SDP, "petLimit")])

    # ---------------- skill modifiers: per-cast mana add-ons ----------------
    for prefix, mod_path, parent_path in [
            ("blindside", "records/skills/playerclass01/blitz2.dbr", BZP),
            ("tectonic_shift", "records/skills/playerclass09/viremight3.dbr", VMP),
            ("break_morale", "records/skills/playerclass01/warcry2.dbr", WCP),
            ("clarity_of_purpose", "records/skills/playerclass09/ascension2.dbr", None)]:
        marc, mrec = dbr(mod_path)
        g = pm4g[mod_path]
        er = int(g["rank_effective"])
        row(f"{prefix}_rank_allocated", float(g["rank_allocated"]), "gd_rank", "rank", ["SAVE"],
            ["SAVE via pack-source pm4g_played_kit.csv rank_allocated (player.gdc block 8, MEASURED)"])
        xp = None
        if parent_path:
            xv = x1[parent_path]["value"]
            xp = (f"player_kit.json::v3p4_rows.x1 {x1[parent_path]['id']}.value.modifier_skillManaCost ({xv['modifier']})",
                  xv["modifier_skillManaCost"])
        row(f"{prefix}_mana_cost_r{er}", rank_idx(mrec["skillManaCost"], er), "gd_energy", "energy/cast",
            ["DATAMINED"] + (["PACK"] if xp else []),
            [DM(marc, mod_path, "skillManaCost", er) + f" at pm4g rank_effective {er} ({g['rank_effective_basis']})"],
            pack=xp, note="modifier cost is an INCREASE on the parent (X1 composition, INFERRED)")

    # ---------------- celestial power levels ----------------
    dp = {r["value"]["devotion_skill_record"]: r for r in pk["devotion_procs"]["rows"]}
    savesk = src["save"]["blocks"]["character_skills"]["skills"]
    for s in savesk:
        n = s["skill-name"]
        if n.startswith("records/skills/devotion/") and n.endswith("_skill.dbr") and s["level"] > 0:
            r = dp[n]
            row(f"devotion_level_{r['value']['proc_id']}", s["devotion-level"], "gd_level", "devotion level", ["SAVE"],
                [f"SAVE player.gdc::character_skills[{n}].devotion-level"],
                pack=(f"player_kit.json::devotion_procs.rows {r['id']}.value.devotion_level", float(r["value"]["devotion_level"])),
                note="the pack's DP row carries the HOST skill row's devotion_level field from pm4g")
    return rows


def agreement(rows):
    out, dis = [], []
    for r in rows:
        checks = []
        if r["pack"]:
            checks.append(r["pack"])
        checks += r["pack_alt"]
        res = []
        for rid, pv in checks:
            ok = close(r["value"], pv)
            res.append({"pack_row": rid, "pack_value": pv, "agree": ok})
            if not ok:
                dis.append({"numeric_key": r["numeric_key"], "record_value": r["value"], "pack_row": rid,
                            "pack_value": pv, "note": r.get("note")})
        r["checks"] = res
        out.append(r)
    return out, dis


def anchor(r):
    parts = [f"GRADE={'+'.join(r['grades'])}", f"VALUE={r['value']:g} {r['unit']}"]
    parts += [f"EVIDENCE: {e}" for e in r["evidence"]]
    if r["checks"]:
        for c in r["checks"]:
            parts.append(f"PACK {c['pack_row']} = {c['pack_value']} -> {'AGREES' if c['agree'] else 'DISAGREES (finding; not edited)'}")
    else:
        parts.append("PACK: silent on this quantity (no row in v3.11)")
    if r.get("note"):
        parts.append(f"NOTE: {r['note']}")
    parts.append(f"PACK_OF_RECORD v3.11 digest {PACK_DIGEST_OF_RECORD[:16]}")
    return " | ".join(parts)


# ----------------------------------------------------------------------------------- record rows
def canon_row():
    return dict(
        kit_id=KIT, folk_name="Eye of Reckoning Warlord -- KC2 referent (EoRWarlGuts, grimtools b28gD0KN)",
        game="gd", corpus_bucket="gd", tier=None, canon_tier=None, eras=None, negative=0, lineage="genre/spin",
        gx=None, source="kc2-referent-save", is_system=0, unresolved=0, mint=0, dossier_owed=0,
        provenance_tag="kc2-referent-save-js4b", source_date="2026-10-02",
        range_val="melee", commit_val="channel", prefix_conf_provenance="derived-js4b-datamine",
        elem_raw="fire", original_element="fire", court="physical",
        mech_note=("KC2 referent build of record (J-S4b). Soldier+Oathkeeper Warlord L100, Gutsmasher two-handed mace, "
                   "no shield. Eye of Reckoning channel (Skill_AttackRadiusSpin): 3.0 m true disc, 12.25 Hz at 196% AS, "
                   "move-while-channel, Fire->Physical 100% via Gutsmasher's EoR modifier. Bar: Vire's Might, War Cry, "
                   "Ascension, Violent Delights (rune), Blitz, weapon attack, EoR, Summon Guardian of Empyrion, "
                   "Summon Deathstalker (relic). Seven devotion procs. Sibling of gd-eor-warlord (a forum guide build), "
                   "which is a different build and is not modified."),
        prov="save;pack-v3.11;arz-edition-IV;legolas-packet",
        grain="kit", core_skills=json.dumps(["Eye of Reckoning"]), core_skills_prov="js4b-save-bar",
        corpus_class="record", roster_status="parked",
        roster_status_note=("J-S4b referent fixture record (JOIN-1 B0-N binder positive control). A second build of the "
                            "gd-eor-warlord identity: parked so active-roster and atlas denominators do not double-count "
                            "the EoR Warlord identity. Not a harvest kit."),
        roster_status_date="2026-10-02", suffix_rekey_status="descriptor-final",
        flags="referent", mech_note_extra=None)


def mapping_json():
    def sk(name, geom, notes, rec, cls, bar, inp):
        return {"source_skill": name, "geometry_value": geom, "element_primary": None, "element_secondary": None,
                "ailments": [], "delivery_notes": notes, "record": rec, "dbr_class": cls, "bar_ordinal": bar, "input": inp}
    return {
        "skills": [
            sk("Eye of Reckoning", "whirlwind",
               "self-origin spin channel; 3.0 m true disc re-centred every tick, no target cap (PACK V17-HITTEST-1; DATAMINED "
               "skillTargetRadius 3.0); usable while moving (DATAMINED canUseWhileMoving). Physical-converted (Fire->Physical 100%, "
               "Gutsmasher) -> element-neutral per THE PHYSICAL RULE; court=physical.",
               "records/skills/playerclass09/eyeofreckoning1.dbr", "Skill_AttackRadiusSpin", "6|7", "weapon-set-1 RIGHT click"),
            sk("Vire's Might", "dash_attack", "path charge with end impact (DATAMINED Skill_AttackPathCharge, radius 2.2 m, "
               "endRadiusMultiplier 1.5); hosts the Maul devotion proc.",
               "records/skills/playerclass09/viremight1.dbr", "Skill_AttackPathCharge", "0", "hotbar"),
            sk("War Cry", "circle", "self-origin radius shout (DATAMINED Skill_AttackRadius); hosts Ulzaad's Decree.",
               "records/skills/playerclass01/warcry1.dbr", "Skill_AttackRadius", "1", "hotbar"),
            sk("Ascension", "self_buff", "timed self buff (DATAMINED Skill_BuffSelfDuration, 10 s).",
               "records/skills/playerclass09/ascension1.dbr", "Skill_BuffSelfDuration", "2", "hotbar"),
            sk("Violent Delights", "dash_attack", "medal-rune path charge (DATAMINED Skill_AttackPathCharge, radius 2.0 m).",
               "records/skills/itemskillsgdx2/runes/rush_d203.dbr", "Skill_AttackPathCharge", "3", "hotbar"),
            sk("Blitz", "dash_attack", "weapon charge to target (DATAMINED Skill_AttackWeaponCharge, 3 targets, 180 deg).",
               "records/skills/playerclass01/blitz1.dbr", "Skill_AttackWeaponCharge", "4", "weapon-set-1 LEFT click"),
            sk("Weapon Attack", "melee_strike", "default weapon attack (Skill_WeaponPool_Default).",
               "records/skills/default/defaultweaponattack.dbr", "Skill_WeaponPool_Default", "5", "hotbar"),
            sk("Summon Guardian of Empyrion", "totem", "targeted pet summon (DATAMINED Skill_TargetedSpawnPet); hosts Shifting Sands.",
               "records/skills/playerclass09/summon_celestialguardian1.dbr", "Skill_TargetedSpawnPet", "8", "hotbar"),
            sk("Summon Deathstalker", "totem", "relic pet summon (DATAMINED Skill_SpawnPet).",
               "records/skills/itemskillsgdx1/relics/summondeathstalker.dbr", "Skill_SpawnPet", "9", "hotbar"),
        ],
        "motion_frame": "hold the EoR spin while moving through the pack; Vire's Might / Blitz / Violent Delights to reposition; "
                        "War Cry and Ascension on cooldown; two summons kept up",
        "resource_economy": {"persistent_condition_shape": "tick-cost",
                             "cost_scale": "EoR 16 energy/tick at total rank 26 x 0.9 cost factor = 176.4 energy/s at 12.25 Hz "
                                           "(PACK V15-1/V15-6/V15-7); usable ceiling 1594 after 982 aura reservation"},
        "trigger_grammar": None,
        "t4_doors": ["ELEMENT_CONVERSION_PHYSICAL"],
        "scaffold": None,
        "option_c_substrate_flags": None,
        "fidelity_notes": ("J-S4b referent record, minted from the measured save + the KC2 pack of record v3.11 + GD Edition IV "
                           "records. Geometry tokens are mapped from each skill's DATAMINED engine class by elrond at J-S4b; "
                           "no prose source. Ordinal 0 is EoR (primary); bar slots are in bar_ordinal. Mapping grade is NOT "
                           "assigned here (owed at the J4a deconfound)."),
    }


# ----------------------------------------------------------------------------------- rowset digest
def rowset(con, kit):
    """ROWSET digest law (J-S4 pin): for each table in ROWSET_TABLES, every row WHERE kit_id = ?, ordered by
    rowid, serialised as json.dumps(dict(row), sort_keys=True, separators=(',',':'), ensure_ascii=False);
    lines '<table>\\t<json>' joined by '\\n' in ROWSET_TABLES order; sha256 of the UTF-8 bytes."""
    con.row_factory = sqlite3.Row
    lines, counts = [], {}
    for t in ROWSET_TABLES:
        rs = con.execute(f"SELECT * FROM {t} WHERE kit_id = ? ORDER BY rowid", (kit,)).fetchall()
        counts[t] = len(rs)
        for r in rs:
            lines.append(t + "\t" + json.dumps(dict(r), sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    con.row_factory = None
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest(), counts


def counts(con):
    return {t: con.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in EXPECT_BEFORE}


# ----------------------------------------------------------------------------------- write
def write(con, rows):
    cc = canon_row()
    cc.pop("mech_note_extra")
    cols = list(cc)
    con.execute(f"INSERT INTO canon_corpus ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", [cc[c] for c in cols])
    con.execute("INSERT INTO kit_mapping (kit_id, mapping_json, grade, deviation_notes, terminal_state, mapping_provenance, authored_date) "
                "VALUES (?,?,?,?,?,?,?)",
                (KIT, json.dumps(mapping_json(), ensure_ascii=False), None,
                 "UNGRADED: this is the referent's own measured kit, not a forum mapping; its mapping grade is owed at the "
                 "J4a deconfound (charter s4.2), not assigned by the data steward.", None, "referent-save-js4b", "2026-10-02"))
    for r in rows:
        con.execute("INSERT INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, rdr_value, rule_id, "
                    "rule_version_applied, source_anchor, verify_ledger_id, created_date) VALUES (?,?,?,?,NULL,NULL,NULL,?,NULL,?)",
                    (KIT, r["numeric_key"], r["value"], r["scale"], anchor(r), "2026-10-02"))


def main(mode):
    import os
    st = os.statvfs(str(CURATED))
    free_gib = st.f_bavail * st.f_frsize / 2**30
    print(f"free disk {free_gib:.2f} GiB")
    assert free_gib > 20, "HALT: free disk below the charter's 20 GiB line"
    src = load_sources()
    rows, dis = agreement(build(src))
    keys = [r["numeric_key"] for r in rows]
    assert len(keys) == len(set(keys)), "duplicate numeric_key"
    pre_sha = sha_file(DB)
    if mode == "dry-run":
        con = sqlite3.connect(":memory:")
        sqlite3.connect(str(DB)).backup(con)
    else:
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        bak = CURATED / f"corpus.db.pre-js4b-referent-{ts}-backup"
        shutil.copy2(DB, bak)
        assert sha_file(bak) == pre_sha
        print(f"backup {bak.name} sha256 {pre_sha}")
        con = sqlite3.connect(str(DB))
    con.execute("PRAGMA foreign_keys=ON")
    before = counts(con)
    assert before == EXPECT_BEFORE, f"pre-counts drifted: {before}"
    assert con.execute("SELECT count(*) FROM canon_corpus WHERE kit_id=?", (KIT,)).fetchone()[0] == 0
    sib_before = rowset(con, SIBLING)
    try:
        con.execute("BEGIN")
        write(con, rows)
        con.execute("INSERT INTO corpus_schema_meta (version, applied_utc, note) VALUES (?,?,?)",
                    (SCHEMA_META_VERSION, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     f"J-S4b referent mint (elrond; conductor gandalf; Matt-approved KC2 KP-237, JOIN-1 charter v0.6.1). "
                     f"DATA-ONLY, no DDL. ADDITIVE: canon_corpus +1, kit_mapping +1, kit_numeric +{len(rows)} for {KIT} "
                     f"(rdr_value NULL, rule_id NULL: rule stamping owed by the rule owner). gd-eor-warlord ROWSET unchanged "
                     f"({sib_before[0][:16]}). Pack of record v3.11 {PACK_DIGEST_OF_RECORD[:16]}; save {SAVE_SHA_OF_RECORD[:16]}. "
                     f"original_element=fire (pre-conversion) / court=physical (post-conversion). {len(dis)} pack disagreements "
                     f"recorded as findings, none edited. Script research/scripts/corpus_js4b_referent_mint_2026_10_02.py."))
        after = counts(con)
        exp = dict(EXPECT_BEFORE)
        exp.update(canon_corpus=591, kit_mapping=575, kit_numeric=458 + len(rows), kit_master=575, corpus_schema_meta=39)
        assert after == exp, f"post-counts wrong: {after} vs {exp}"
        assert con.execute("SELECT count(*) FROM kit_numeric WHERE kit_id=? AND rdr_value IS NULL AND rule_id IS NULL",
                           (KIT,)).fetchone()[0] == len(rows)
        assert con.execute("PRAGMA foreign_key_check").fetchall() == []
        assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        sib_after = rowset(con, SIBLING)
        assert sib_after == sib_before, "gd-eor-warlord ROWSET moved"
        ref = rowset(con, KIT)
        con.commit()
    except Exception:
        con.rollback()
        raise
    km = con.execute("SELECT kit_id, grade, elements_attested FROM kit_master WHERE kit_id=?", (KIT,)).fetchone()
    con.close()
    post_sha = sha_file(DB) if mode == "apply" else None
    if mode == "apply":
        assert post_sha != pre_sha
    result = dict(rows=rows, dis=dis, before=before, after=after, sib=sib_before, ref=ref, pre_sha=pre_sha,
                  post_sha=post_sha, km=km, src=src)
    print(f"{mode}: {len(rows)} numeric rows; {len(dis)} disagreements; rowset {ref[0]}; counts {after}")
    for d in dis:
        print("  DISAGREE", d["numeric_key"], d["record_value"], "vs", d["pack_row"], d["pack_value"])
    if mode == "apply":
        emit(result)
    return result


# ----------------------------------------------------------------------------------- export
def emit(res):
    src = res["src"]
    sd = src["save"]
    skills = sd["blocks"]["character_skills"]["skills"]
    pm4g = src["pm4g"]
    packet = src["packet"]
    cc = canon_row()
    # skills with ranks (class + item skills that hold a rank or sit on the bar)
    sk_out = []
    for g in pm4g:
        if g["mastery"] == "devotion":
            continue
        if not (g["rank_allocated"] not in ("0", "") or g["bound_on_bar"] == "True"):
            continue
        if g["mastery"] == "default" and g["bound_on_bar"] != "True":
            continue
        sk_out.append({"record": g["skill_record"], "display_name": g["display_name"] or None, "mastery": g["mastery"],
                       "dbr_class_pm4g": g["engine_class"], "rank_allocated": int(g["rank_allocated"]) if g["rank_allocated"] else None,
                       "rank_allocated_grade": "SAVE (player.gdc block 8 via pm4g, MEASURED)",
                       "rank_effective_pm4g": int(g["rank_effective"]) if g["rank_effective"] else None,
                       "rank_effective_basis": g["rank_effective_basis"],
                       "skill_max_level": g["skill_max_level"] or None, "skill_ultimate_level": g["skill_ultimate_level"] or None,
                       "bound_on_bar": g["bound_on_bar"] == "True", "bar_ordinals": g["binding_ordinals"] or None,
                       "item_record": g["item_record"] or None,
                       "bound_devotion_proc": g["autocast_devotion_skill"] or None,
                       "proc_controller": g["autocast_controller"] or None})
    eor = next(s for s in sk_out if s["record"].endswith("eyeofreckoning1.dbr"))
    eor["rank_total_of_record"] = 26
    eor["rank_total_grade"] = "PACK fixture.eor_rank_total + DATAMINED item grants (legolas C-2)"
    gear = []
    for s in packet["gear_of_record"]["slots"]:
        f = s["fields"]
        gear.append({"slot": s["slot"], "item": s["name"], "record": s["record"], "archive": s["archive"],
                     "class": f.get("Class"), "armor_classification": f.get("armorClassification"),
                     "rarity": f.get("itemClassification"),
                     "prefix": (s.get("prefix") or {}).get("name"), "suffix": (s.get("suffix") or {}).get("name"),
                     "component": (s.get("component") or {}).get("name", "").lstrip("^k") or None,
                     "component_record": (s.get("component") or {}).get("record"),
                     "augment": (s.get("augment") or {}).get("name"), "augment_record": (s.get("augment") or {}).get("record"),
                     "craft_modifier": (s.get("craft_modifier") or {}).get("record"),
                     "grade": "SAVE (player.gdc equipment, seeds intact) + DATAMINED names (Edition IV) + COMMUNITY-VERIFIED 13/13 vs b28gD0KN"})
    gear.insert(13, {"slot": "weapon_set_1_offhand", "item": None, "note": "empty: two-hander (SAVE attached=0; sheet block 0%)"})
    gear.append({"slot": "weapon_set_2", "item": None, "note": "both slots empty; alt-weapon-set-enabled=1 (SAVE) -- a standing hazard (legolas 2026-08-05 s3.1)"})
    # devotions
    const_names = {"tier1_08": "Assassin's Blade", "tier1_29": "Tortoise", "tier1_38": "Jackal", "tier1_39": "Stag",
                   "tier1_42": "Toad", "tier2_02": "Scales of Ulcama", "tier2_05": "Dire Bear", "tier2_17": "Crab",
                   "tier2_21": "Kraken", "tier2_37": "Ulzaad, Herald of Korvaak", "tier3_20": "Azrakaa, the Eternal Sands"}
    nodes = [s for s in skills if s["skill-name"].startswith("records/skills/devotion/") and s["level"] > 0]
    by = {}
    for s in nodes:
        stem = s["skill-name"].split("/")[-1][:8]
        by.setdefault(stem, []).append(s["skill-name"].split("/")[-1].replace(".dbr", ""))
    constellations = [{"constellation": const_names.get(k, "UNKNOWN (name not in the save-decode note)"), "id": k,
                       "nodes": v, "n_nodes": len(v)} for k, v in by.items()]
    hosts = {s["autocast-skill-name"]: s for s in skills if s["autocast-skill-name"]}
    dp = {r["value"]["devotion_skill_record"]: r for r in src["player_kit"]["devotion_procs"]["rows"]}
    powers = []
    for s in nodes:
        n = s["skill-name"]
        if not n.endswith("_skill.dbr"):
            continue
        r = dp[n]["value"]
        h = hosts.get(n)
        powers.append({"proc_id": r["proc_id"], "devotion_record": n, "devotion_level": s["devotion-level"],
                       "devotion_level_grade": "SAVE", "host_skill_record": h["skill-name"] if h else None,
                       "controller": h["autocast-controller-name"] if h else None,
                       "trigger": {"chance_pct": r["trigger_chance_pct"], "direction": r["trigger_direction"],
                                   "event": r["trigger_event"], "skill_cooldown_s": r["skill_cooldown_s"],
                                   "duration_s": r.get("duration_s")},
                       "trigger_grade": f"PACK player_kit.json::devotion_procs.rows {dp[n]['id']}"})
    numeric = [{"numeric_key": r["numeric_key"], "value": r["value"], "unit": r["unit"], "source_scale": r["scale"],
                "grades": r["grades"], "evidence": r["evidence"], "pack_checks": r["checks"],
                "note": r.get("note"), "rdr_value": None, "rule_id": None} for r in res["rows"]]
    n_cmp = sum(1 for r in res["rows"] if r["checks"])
    n_cmp_ok = sum(1 for r in res["rows"] if r["checks"] and all(c["agree"] for c in r["checks"]))
    export = {
        "kit_id": KIT,
        "export_shape": "kits-export/referent-v1 (J-S4b). Extends the 576-kit shape with identity / skills / gear / "
                        "devotions / element / numeric / agreement_check / unknowns / corpus_rowset blocks.",
        "spine": {k: cc[k] for k in ("kit_id", "folk_name", "game", "corpus_bucket", "tier", "canon_tier", "eras", "negative",
                                     "is_system", "lineage", "source", "provenance_tag", "source_date", "corpus_class",
                                     "roster_status", "roster_status_note", "range_val", "commit_val",
                                     "original_element", "court")}
                 | {"grade": None, "terminal_state": None, "mapping_provenance": "referent-save-js4b"},
        "element": {"original_element": "fire", "court": "physical",
                    "semantics": "original_element = the PRE-conversion (raw) element, promoted from elem_raw (VDM-2 law); "
                                 "court = the reconciled POST-conversion element, enum-checked. Both are exported because the "
                                 "kit compiler reads canon_corpus, not this JSON (EL-2).",
                    "conversion": {"skill": "Eye of Reckoning", "from": "Fire", "to": "Physical", "pct": 100.0,
                                   "source_record": "records/skills/itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr",
                                   "grade": "DATAMINED + FOOTAGE (sheet 100%)"},
                    "other_conversions": [
                        {"from": "Chaos", "to": "Physical", "pct_datamined": 50.0, "pct_footage": 55.0, "source": "Gutsmasher"},
                        {"from": "Lightning", "to": "Physical", "pct_datamined": 50.0, "pct_footage": 46.0, "source": "Gutsmasher"},
                        {"from": "Aether", "to": "Physical", "pct": 25.0, "source": "Seal of Might (compa_sealmight)",
                         "grade": "oracle-source pm4l (not re-read here)"}],
                    "compiler_note": "kit_compiler reads original_element when element_primary is null, so this record compiles "
                                     "as fire until gamora's KC-1 fix lands (jack-ryan Gate-2 KC-1, WARN, gamora)."},
        "identity": {"class_combination": "Soldier + Oathkeeper (Warlord)", "class_tag": "tagSkillClassName0109",
                     "character_name": "EoRWarlGuts", "level": 100, "build_of_record": "b28gD0KN",
                     "masteries": {"Soldier": 46, "Oathkeeper": 50},
                     "attributes_sheet": {"physique": 914, "cunning": 1219, "spirit": 398},
                     "save": {"file": "player.gdc", "sha256": SAVE_SHA_OF_RECORD, "bytes": SAVE.stat().st_size,
                              "copies": ["/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc",
                                         "/Volumes/reincarnated/GD-matt-test/eor-test-2/save/_EoRWarlGuts/player.gdc",
                                         "agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/player.gdc"],
                              "verified_this_pass": "the legolas scratch copy (sha256 recomputed); the two /Volumes copies "
                                                    "were not reachable this pass (share hung) -- byte-identity rests on legolas 2026-10-01"},
                     "pack_of_record": {"dir": str(PACK.relative_to(ENGINE)), "pack_digest": PACK_DIGEST_OF_RECORD,
                                        "version": "v3.11", "player_sheet_provenance": "PRV-PLAYER-SHEET (pm2_measured_player_sheet.csv)"},
                     "gd_data": {"edition": GD4_BUILD, "arz_sha256": src["arz_sha"]}},
        "skills": sk_out,
        "gear": gear,
        "devotions": {"points_spent": 55, "points_unspent": 0, "constellations": constellations,
                      "celestial_powers": powers, "grade": "SAVE (55 nodes) + PACK trigger rows"},
        "mapping": {"grade": None, "terminal_state": None, "mapping_provenance": "referent-save-js4b",
                    "mapping_json": mapping_json()},
        "numeric": numeric,
        "agreement_check": {"pack_of_record": PACK_DIGEST_OF_RECORD, "n_rows": len(res["rows"]),
                            "n_rows_compared_to_pack": n_cmp, "n_rows_all_checks_agree": n_cmp_ok,
                            "n_rows_pack_silent": len(res["rows"]) - n_cmp,
                            "disagreements": res["dis"],
                            "categorical_disagreements": CATEGORICAL},
        "unknowns": UNKNOWNS,
        "corpus_rowset": {"law": rowset.__doc__.strip(), "tables": ROWSET_TABLES, "digest": res["ref"][0],
                          "row_counts": res["ref"][1],
                          "sibling_gd_eor_warlord_rowset_unchanged": res["sib"][0]},
        "_row_counts": {"canon_corpus": 1, "kit_mapping": 1, "kit_numeric": len(res["rows"]),
                        "citations": 0, "dossier_facts": 0, "verify_claims": 0},
    }
    out = EXPORT_DIR / f"{KIT}.json"
    out.write_text(json.dumps(export, indent=2, ensure_ascii=False) + "\n")
    sib_json = EXPORT_DIR / f"{SIBLING}.json"
    files = {
        "export": out, "sibling_export_unchanged": sib_json, "corpus_db_post_apply": DB,
        "mint_script": pathlib.Path(__file__),
        "pack_manifest": PACK / "manifest.json", "pack_player_kit": PACK / "model/player_kit.json",
        "pack_rng_contract": PACK / "model/rng_contract.json", "pack_math_rules": PACK / "model/math_rules.json",
        "pack_provenance": PACK / "model/provenance.json", "pack_summons": PACK / "model/summons.json",
        "pm2_measured_player_sheet": PM2, "pm4g_played_kit": PM4G, "pm4l_eor_per_hit": PM4L,
        "legolas_packet": PACKET, "legolas_readme": PACKET_README, "save_player_gdc": SAVE, "save_decode_json": SAVE_DECODE,
    }
    files.update({f"gd_arz_{n}": p for n, p in ARCHIVES})
    manifest = {
        "kit_id": KIT, "minted": "2026-10-02", "by": "elrond", "schema_meta_version": SCHEMA_META_VERSION,
        "files": {k: {"path": str(p), "sha256": sha_file(p), "kind": "FILE"} for k, p in files.items()},
        "rowsets": {KIT: {"digest": res["ref"][0], "counts": res["ref"][1], "kind": "ROWSET"},
                    SIBLING: {"digest": res["sib"][0], "counts": res["sib"][1], "kind": "ROWSET",
                              "note": "identical before and after the mint (asserted)"}},
        "rowset_law": rowset.__doc__.strip(),
        "corpus_db": {"pre_FILE_sha256": res["pre_sha"], "post_FILE_sha256": res["post_sha"]},
        "pack_digest_of_record": PACK_DIGEST_OF_RECORD,
    }
    (EXPORT_DIR / f"{KIT}.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("export", out, sha_file(out))


CATEGORICAL = [
    {"field": "Vire's Might dbr_class", "record_value": "Skill_AttackPathCharge",
     "record_grade": "DATAMINED (viremight1.dbr Class, GDX2 Edition IV) + pack-source pm4g engine_class",
     "pack_row": "player_kit.json::binding_model.bindings[vires_might].dbr_class", "pack_value": "Skill_AttackWeaponCharge"},
    {"field": "devotion_level on the seven DP-* rows", "record_value": "25/25/20/20/20/20/15 (SAVE, the power rows)",
     "pack_row": "player_kit.json::devotion_procs.rows[*].value.devotion_level", "pack_value": "0 on all seven",
     "note": "the pack copied the HOST skill row's devotion_level field from pm4g; the power rows of the same CSV carry 25/20/15"},
]

UNKNOWNS = [
    {"what": "EoR mapping grade (EXACT/CLOSE/APPROX/GAPPED)", "settle": "the J4a deconfound re-grade against the sealed pack (charter s4.2); not a data-steward call"},
    {"what": "rdr_value for every kit_numeric row", "settle": "the normalization-rule owner (gamora) stamps rules; no rule yet covers gd_metres, gd_energy, gd_rank, gd_pct_sheet, etc. R-T2 names gd_seconds but its derivation SQL is kit-scoped"},
    {"what": "EoR rank of record for the ORACLE's operands (15 vs 20 vs 26)", "settle": "ABS-EOR-RANK-OF-RECORD in the pack; the oracle owner rules which rank each operand reads. DATAMINED item grants close 26"},
    {"what": "spin clip playback vs attack speed (0.300 s vs 0.153 s per loop)", "settle": "re-pin Creatures.arc (Matt-only depot pull) or frame-count referent footage (legolas OQ1)"},
    {"what": "weapon-swing law A vs B (0.376 vs 0.340 s)", "settle": "frame-count one referent swing (legolas OQ2)"},
    {"what": "why the x0.8 quantum turns timeBetweenAttacks 200 into 0.16 s", "settle": "Game.dll decode of the channel tick (PE-1 s1.3)"},
    {"what": "Summon Deathstalker body-clip slot and pet level", "settle": "footage, or Game.dll class-to-slot / JoinMe@Monster decode (legolas OQ3; ABS-SUMMON-CHARLEVEL-BINDING-deathstalker)"},
    {"what": "Gutsmasher Chaos/Lightning conversion as applied (DB 50/50 vs tooltip 55/46)", "settle": "the GD conversion display rule, or an in-game damage probe"},
    {"what": "Tectonic Shift / Blindside / Break Morale effective ranks (pack X1 implies 5 / 7-8 / 22; pm4g says 2 / 5 / 16)", "settle": "legolas C-2 rank basis for the modifiers, or a grimtools per-skill read"},
    {"what": "era fields (eras / era_year) for the referent build", "settle": "the build's patch of origin (fordprefect 2022 file, migrated by client 1.3.0.5) mapped into the eras vocabulary"},
    {"what": "attr_val / tempo_val / amp_val / proxy_val lattice coordinates", "settle": "harvest-time judgments; not derivable from DATAMINED or PACK values without an authored rule"},
]


if __name__ == "__main__":
    m = "apply" if "--apply" in sys.argv else "dry-run"
    main(m)
