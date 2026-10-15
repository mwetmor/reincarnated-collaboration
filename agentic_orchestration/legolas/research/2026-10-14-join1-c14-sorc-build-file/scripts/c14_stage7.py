#!/usr/bin/env python3
"""C-14 stage 7: numeric facts for drax's J4b kit open questions (read-only). Laws and sources in README § 11."""
import json, math, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
J4B = P.parent / "2026-10-01-join1-j4b-d2-fire-sorc" / "primary_rows.json"
prim = json.loads(J4B.read_text())
off = prim["missile_notes"]["meteor offsets (D2MOO MISSMODE_CreateMeteor_MoltenBoulderSubmissiles, 1.10f reconstruction; DATAMINED from code)"]
vel, rng = 20, 50
path_vel = (vel << 8) * 75 // 100                     # Missiles.cpp L123-146
fp16_per_frame = 4096 * path_vel >> 8                  # direction vector |v| = 0x1000 (Step.cpp lutTanToDirection), PathMisc velocity>>8
sub_per_frame = fp16_per_frame / 65536
sheet = json.loads((P / "sorc_build_sheet.json").read_text())["sheets"]["FINAL_charms_BO_BC_FA (KP-436/437)"]
vit = sheet["attributes_total"]["vit"]
stam = 74 + 1 * (99 - 1) + 1 * (vit - 10)
frw = 25; frw_eff = 150 * frw // (150 + frw)
def chill_ticks(frames, base_speed=256, coldeffect=-33):
    rate = max(15, min(175, 100 + coldeffect))
    sp = rate * base_speed // 100
    return math.ceil(frames * 256 / sp)
doc = {
    "fire_ball": {"Vel": vel, "path_velocity": path_vel, "fp16_per_frame": fp16_per_frame, "subtiles_per_frame": sub_per_frame,
                  "subtiles_per_s": sub_per_frame * 25, "yd_per_s_at_2_3": sub_per_frame * 25 * 2 / 3,
                  "range_frames": rng, "travel_subtiles": sub_per_frame * rng, "travel_yd": sub_per_frame * rng * 2 / 3,
                  "size": 1, "explosion_radius_subtiles": 4, "CollideKill": 1, "AlwaysExplode": "", "Explosion": ""},
    "meteor_pyre_offsets_subtiles": [{"dx": x, "dy": y} for x, y in zip(off["x"], off["y"])],
    "meteor_pyre_missile_size": 2,
    # ⚑ STAGE 8: War Traveler item_staminadrainpct 40 applies after armour speed (PlrModes.cpp L265-286):
    #   L = 2*RunDrain*(speed/10+1) = 40; L += L*40/-100 (C truncation toward zero) -> 24; min 1.
    #   BO skill_staminapercent op 1 (D2StatList.cpp case 1 = % of the pre-op accumulated base, like op 11): applies to
    #   74 + (clvl-1) + (allocated Vit - 10) [+ flat +stamina items], NOT to item-Vitality stamina (Basin Battle Orders).
    "stamina": {"vit_total": vit, "max_stamina_noBO": stam,
                "max_stamina_BO80": (74 + 98 + (441 - 10)) * 180 // 100 + (vit - 441),
                "max_stamina_BO80_stage7_superseded": stam * 180 // 100,
                "armor_speed": {"Dusk Shroud": 0, "Monarch": 0}, "staminadrainpct_WarTraveler": 40,
                "drain_256_per_frame": (lambda L: max(1, L + int(L * 40 / -100)))(2 * 20 * (0 // 10 + 1)),
                "drain_256_per_frame_stage7_superseded": 40},
    "movement": {"WalkVelocity": 6, "RunVelocity": 9, "FRW": frw, "FRW_eff": frw_eff,
                 "walk": 6 * (100 + frw_eff) / 100, "run": 9 + 6 * frw_eff / 100, "unit": "CharStats velocity units (Basin reads as yd/s)"},
    "chill_tick_examples_basespeed256": {f"{n}_frames": {c: chill_ticks(n, coldeffect=c) for c in (0, -25, -33, -40, -50)} for n in (8, 12, 16, 20)},
}
(P / "c14_stage7.json").write_text(json.dumps(doc, indent=1))
doc["stamina"]["drain_points_per_s"] = doc["stamina"]["drain_256_per_frame"] / 256 * 25
(P / "c14_stage7.json").write_text(json.dumps(doc, indent=1))
print(json.dumps({k: doc[k] for k in ("fire_ball", "stamina", "movement")}, indent=0)[:1700]); print(doc["chill_tick_examples_basespeed256"])
