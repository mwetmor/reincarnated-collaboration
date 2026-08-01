#!/usr/bin/env python3
"""GD-PARITY — the numbers table and the camera arithmetic.

Everything downstream of the measured screen-heights is computed here so the
note carries no hand arithmetic.
"""
import json, math

OUT = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/"
       "captures/2026-07-31-gd-parity/gd-parity-numbers.json")

# ---- the shared camera (CAM-LOCK == GAL-CAM centre operands; PL-AUDIT verified)
PITCH = 52.9535411256029
FOV_V = 31.7861018306101
Z_PLAYER = 34.8165340347471          # camera -> player depth along the view axis
DEC = {"left": -17.6601, "right": 17.5867, "far": 15.2111, "near": -7.0197}

def focal_px(vh):  return (vh / 2.0) / math.tan(math.radians(FOV_V) / 2.0)
def gx(vh):        return focal_px(vh) / Z_PLAYER            # lateral ground px/m
def gz(vh):        return gx(vh) * math.sin(math.radians(PITCH))   # up-screen ground px/m
def gv(vh):        return gx(vh) * math.cos(math.radians(PITCH))   # UPRIGHT world-Y px/m

cam = {
    "pitch_deg": PITCH, "fov_v_deg": FOV_V, "z_player_m": Z_PLAYER,
    "focal_px_1080": focal_px(1080), "focal_px_720": focal_px(720),
    "gx_px_per_m_1080": gx(1080), "gx_px_per_m_720": gx(720),
    "gz_px_per_m_1080": gz(1080),
    "gv_upright_px_per_m_1080": gv(1080), "gv_upright_px_per_m_720": gv(720),
    "upright_metre_as_frac_of_frame_height": gv(1080) / 1080.0,
    "lateral_metre_as_frac_of_frame_height": gx(1080) / 1080.0,
    "decision_surface_m": DEC,
}

# ---- measured screen-height bounding boxes (source px; see note sec.2/3) ------
GD = [  # 1920x1080
    {"id": "Screenshot (87)",  "subject": "player werewolf", "state": "LongIdle",
     "top": 449, "bottom": 611, "left": 878, "right": 1040, "grade": "seg-bracketed manual"},
    {"id": "Screenshot (86)",  "subject": "player werewolf", "state": "Idle",
     "top": 455, "bottom": 615, "left": 880, "right": 1035, "grade": "manual"},
    {"id": "Screenshot (124)", "subject": "player werewolf", "state": "Idle",
     "top": 441, "bottom": 600, "left": 875, "right": 1030, "grade": "manual"},
    {"id": "video t=4200 s",   "subject": "player werewolf", "state": "MoveTo",
     "top": 432, "bottom": 580, "left": 880, "right": 1030, "grade": "manual, coarse"},
    {"id": "video t=200 s",    "subject": "player HUMAN form", "state": "LongIdle",
     "top": 497, "bottom": 573, "left": 945, "right": 985, "grade": "seg-bracketed manual"},
    {"id": "Screenshot (124) right", "subject": "humanoid trash monster", "state": "-",
     "top": 500, "bottom": 600, "left": 1097, "right": 1119, "grade": "manual, coarse"},
    {"id": "Screenshot (176)", "subject": "large monster (red-outlined)", "state": "-",
     "top": 679, "bottom": 824, "left": 780, "right": 900, "grade": "manual, coarse"},
    {"id": "Screenshot (286)", "subject": "hero/boss-tier monster (red-outlined)", "state": "-",
     "top": 581, "bottom": 814, "left": 800, "right": 940, "grade": "manual, coarse"},
]
OURS = [  # 1280x720
    {"id": "leg_014 (VFXBO_legacy NOHUD CAMLOCK)", "subject": "player werewolf 1.80 m",
     "top": 357, "bottom": 398, "left": 608, "right": 652, "grade": "manual on ruler crop"},
    {"id": "leg_014 (VFXBO_legacy NOHUD CAMLOCK)", "subject": "boss 2.75 m",
     "top": 288, "bottom": 348, "left": 592, "right": 670, "grade": "manual on ruler crop"},
]

def enrich(rows, vh):
    for r in rows:
        r["h_px"] = r["bottom"] - r["top"]
        r["w_px"] = r["right"] - r["left"]
        r["h_frac"] = r["h_px"] / vh
        r["w_ground_m"] = r["w_px"] / gx(vh)      # lateral -> metres, pitch-independent
        r["h_upright_equiv_m"] = r["h_px"] / gv(vh)
    return rows

enrich(GD, 1080); enrich(OURS, 720)

gd_ww = [r["h_frac"] for r in GD if r["subject"] == "player werewolf"]
gd_ww.sort()
med = gd_ww[len(gd_ww) // 2] if len(gd_ww) % 2 else 0.5 * (gd_ww[len(gd_ww)//2 - 1] + gd_ww[len(gd_ww)//2])
ours_ww = OURS[0]["h_frac"]
ours_boss = OURS[1]["h_frac"]

# ---- analytic ladder (bodies are metres-true; target_height is exact) ---------
LADDER = {"swarm": 1.65, "player": 1.80, "elite": 2.00, "boss": 2.75}
ladder = {k: {"h_m": v, "h_px_720": v * gv(720), "h_frac": v * gv(720) / 720.0}
          for k, v in LADDER.items()}

# ---- the camera change that would close the gap ------------------------------
k = med / ours_ww
close = {
    "required_linear_magnification_k": k,
    "lever_A_dolly_in": {
        "new_stand_off_m": Z_PLAYER / k,
        "new_camera_height_m": (Z_PLAYER / k) * math.sin(math.radians(PITCH)),
        "fov_v_deg": FOV_V,
    },
    "lever_B_narrow_fov": {
        "new_fov_v_deg": 2 * math.degrees(math.atan((720 / 2.0) / (focal_px(720) * k))),
        "stand_off_m": Z_PLAYER,
    },
    "decision_surface_after": {kk: vv / k for kk, vv in DEC.items()},
    "floor_area_retained": 1.0 / (k * k),
}
# ring visibility after the change: our boss nova is circle 10.0 m
close["boss_nova_10m_fits_horizontally_after"] = (10.0 <= abs(DEC["left"]) / k)
close["escort_6p5m_fits_near_side_after"] = (6.5 <= abs(DEC["near"]) / k)
close["escort_6p5m_fits_near_side_now"] = (6.5 <= abs(DEC["near"]))

# ---- pose-controlled decomposition -------------------------------------------
gd_human = [r for r in GD if "HUMAN" in r["subject"]][0]
decomp = {
    "upright_humanoid_ratio_GD_over_ours": gd_human["h_frac"] / ladder["player"]["h_frac"],
    "GD_werewolf_over_GD_human_bbox": med / gd_human["h_frac"],
    "our_werewolf_over_our_human_height": 1.0,   # rig target == RIG_PLAYER_H == human height
    "product": (gd_human["h_frac"] / ladder["player"]["h_frac"]) * (med / gd_human["h_frac"]),
    "direct_measured_ratio": k,
}
prop = {
    "GD_bosslike_over_GD_player": [r for r in GD if "hero/boss" in r["subject"]][0]["h_frac"] / med,
    "ours_boss_over_ours_player": ours_boss / ours_ww,
    "ours_boss_over_ours_player_analytic": ladder["boss"]["h_frac"] / ladder["player"]["h_frac"],
}

# ---- the third camera lever: pitch (raises upright height, keeps lateral extent)
cosp = math.cos(math.radians(PITCH))
pitch_lever = {
    "cos_pitch_now": cosp,
    "max_gain_from_pitch_alone": 1.0 / cosp,        # pitch -> 0 deg (horizontal camera)
    "pitch_for_1p29x_deg": math.degrees(math.acos(min(1.0, cosp * 1.2866))),
    "pitch_for_1p50x_deg": math.degrees(math.acos(min(1.0, cosp * 1.50))),
    "note": "lateral ground scale gx is INDEPENDENT of pitch; only upright bodies and "
            "up-screen ground depth move. Cannot supply the full 2.59x.",
}

# ---- body-scale prescriptions that leave the camera alone --------------------
body = {
    "rig_h_for_GD_height_parity_m": med * 720 / gv(720),
    "rig_h_for_GD_ground_span_parity_m": LADDER["player"] *
        ([r for r in GD if r["id"] == "Screenshot (87)"][0]["w_ground_m"] / OURS[0]["w_ground_m"]),
    "screen_area_ratio_GD_over_ours": (162 * 162 / (1920 * 1080)) / (41 * 44 / (1280 * 720)),
}

res = {"camera": cam, "gd": GD, "ours": OURS, "ladder_analytic": ladder,
       "pitch_lever": pitch_lever, "body_scale_prescription": body,
       "gd_werewolf_h_frac_median": med, "gd_werewolf_h_frac_range": [min(gd_ww), max(gd_ww)],
       "ours_werewolf_h_frac": ours_ww, "ours_boss_h_frac": ours_boss,
       "gap": close, "decomposition": decomp, "relative_proportion": prop}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({kk: res[kk] for kk in
                  ("gd_werewolf_h_frac_median", "gd_werewolf_h_frac_range",
                   "ours_werewolf_h_frac", "ours_boss_h_frac", "gap",
                   "decomposition", "relative_proportion")}, indent=1))
print("\nladder:", json.dumps(ladder, indent=1))
print("\ncam:", json.dumps(cam, indent=1))
print("\nGD rows:")
for r in GD:
    print(f"  {r['id']:34s} {r['subject']:38s} h={r['h_px']:4d}px "
          f"{100*r['h_frac']:5.2f}%  w_ground={r['w_ground_m']:.2f} m  "
          f"upright-equiv={r['h_upright_equiv_m']:.2f} m")
print("OURS rows:")
for r in OURS:
    print(f"  {r['subject']:38s} h={r['h_px']:4d}px {100*r['h_frac']:5.2f}%  "
          f"w_ground={r['w_ground_m']:.2f} m  upright-equiv={r['h_upright_equiv_m']:.2f} m")
