#!/usr/bin/env python3
"""
CA-guides-v1 — the cathedral arena GREY BOX spec solver.

Every number the grey box uses is computed HERE and written to cathedral_spec.json.
Nothing downstream (the Godot builder, the post pass) may invent a number.

Provenance classes, stamped per quantity in the emitted JSON:
  MEASURED   — read from a first-party measured artifact (the arena geometry file,
               the cliffside blockout meta, the runtime parallax.json).
  DERIVED    — computed from MEASURED quantities by a stated formula.
  RULED      — fixed by a Matt ruling / corrigendum, cited.
  DECLARED   — drax's choice. Carries a reason. Overrulable.

Authorities:
  R-C9-43/44 (Corrigendum-Forward 3) — indoors; two far walls rise out of frame;
              near side cut low at knee height; three window levels; west top breached.
  R-C9-45    (Corrigendum-Forward 4) — diagonal SE->NW camera; rising N+W; cut-low S+E;
              cruciform, crater at the crossing; aprons + only non-coinciding pools.
  Crack-law Corrigendum 2 sec 2 — interior obstacles are PROPS with footprints;
              "a pool moved" is decided by OVERLAP, never proximity.
  Crack-law Corrigendum 4 — entrances are one-way hazards with aprons.
  Art brief sec 3/sec 4 — room size from encounter math; full-bleed; back walls exit frame.
"""
import json, math, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".."))
# ROOT = reincarnated-collaboration
COLLAB = "/Users/admin/Games/reincarnated-collaboration"

GEOM = os.path.join(COLLAB, "agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json")
GREYROOM = os.path.join(COLLAB, "astra_test_01/burst/runs/C-9/greyroom/greyroom_manifest.json")
BLOCKOUT = os.path.join(COLLAB, "agentic_orchestration/drax/captures/2026-09-13-cliffside-blockout/blockout_meta_v2.json")
PARALLAX = os.path.join(COLLAB, "astra_test_01/burst/runs/C-9/cliffside_B/parallax/parallax.json")

gr = json.load(open(GREYROOM))
bo = json.load(open(BLOCKOUT))
px = json.load(open(PARALLAX))

# ---------------------------------------------------------------- 1. THE LAW
PPM         = bo["ortho_canvas_v2"]["px_per_m_screen_x"]            # MEASURED 100.617553710938
ALPHA_DEG   = gr["camera"]["pitch_alpha_deg"]                        # MEASURED 52.9535411256029
ALPHA       = math.radians(ALPHA_DEG)
PX_GROUND   = PPM * math.sin(ALPHA)     # px up-screen per metre along the view axis
PX_ELEV     = PPM * math.cos(ALPHA)     # px up-screen per metre of elevation

# cross-check against the independently authored cliffside pair (free check, must land at 0)
CHECK_GROUND = abs(PX_GROUND - bo["ortho_canvas_v2"]["px_per_ground_m_screen_y"])
CHECK_ELEV   = abs(PX_ELEV   - bo["ortho_canvas_v2"]["px_per_vertical_m_screen_y"])
assert CHECK_GROUND < 1e-9 and CHECK_ELEV < 1e-9, (CHECK_GROUND, CHECK_ELEV)

# YAW. RULED as a compass word ("from the SOUTH-EAST looking NORTH-WEST", R-C9-45 cl.1),
# not as a number. SE is exactly 45 deg between S and E, and 45 deg is the ONLY yaw at which
# the two rising walls (N, W) present equally and the two cut-low walls (S, E) recede equally,
# which is the symmetric condition the ruling describes. The GD runtime's own yaw constant is
# 47 deg, but that is a yaw inside the referent's axes, which carry no compass meaning.
YAW_DEG = 45.0
YAW = math.radians(YAW_DEG)
# plan view direction (away from camera) = NW ; screen-right = NE
D_PLAN = (-math.sin(YAW), math.cos(YAW))    # (east, north) components of NW at yaw 45
R_PLAN = ( math.cos(YAW), math.sin(YAW))    # (east, north) components of NE

# figure height — the CONFLICT is carried, not resolved (greyroom manifest scale_figures)
KEEPER_PX          = gr["scale_figures"]["keeper_130px_convention"]           # 130.0
KEEPER_PX_IMPLIES  = gr["scale_figures"]["keeper_130px_implies_body_m"]       # 2.1446 m
KC2_HFIG_M         = gr["scale_figures"]["kc2_h_fig_m"]                       # 1.9 m
KC2_HFIG_PX        = gr["scale_figures"]["kc2_h_fig_px_on_this_plate"]        # 115.175 px

# runtime camera (MEASURED, cliffside_B/parallax/parallax.json — the 2D game camera)
VIEW_W, VIEW_H   = px["camera"]["view"]          # 1920, 1080
ANCHOR_X, ANCHOR_Y = px["camera"]["anchor"]      # 962, 595
WALK_PX_S        = px["movement"]["walk_px_s"]   # 247
RUN_PX_S         = px["movement"]["run_px_s"]    # 494
WALK_M_S         = WALK_PX_S / PPM
RUN_M_S          = RUN_PX_S / PPM

# ------------------------------------------------- 2. THE ROOM (encounter math)
AREA_WALKABLE_M2 = gr["arena"]["walkable_area_m2"]     # MEASURED 2354.3412243939315
EXT_EW, EXT_NS   = gr["arena"]["extent_m"]             # MEASURED 57.285 x 76.665
BAY_M            = gr["derived_from_geometry"]["bay_m"]                  # 6.564460927936452
CENTRAL_VESSEL_M = gr["derived_from_geometry"]["central_vessel_width_m"] # 13.128921855872903
PIER_W           = 1.6   # lineage declared_not_measured
AISLE_W          = 4.5
AISLE_WALL       = 1.5
CHAPEL_D         = 2.5
NEAR_CUT_M       = 0.9   # lineage declared_not_measured "D2-style knee/waist break"

# crossing split. Gothic proportion nave:chancel = 2:1, and it is what R-C9-45 cl.2's own
# sequence describes (road in through the south facade -> NORTH UP THE NAVE -> crater at the
# crossing -> dais and apse): the walk before the crater is the long leg.
NAVE_CHANCEL_RATIO = 2.0
Y_N =  EXT_NS / (1.0 + NAVE_CHANCEL_RATIO)      # +25.555
Y_S =  Y_N - EXT_NS                              # -51.110
X_W = -EXT_EW / 2.0                              # -28.6425
X_E =  EXT_EW / 2.0                              # +28.6425

# crater at the crossing. DECLARED radius.
R_CRATER = 4.5
# crypt mouth (east), a hole in the floor by the cut-low east wall. DECLARED.
CRYPT_CX, CRYPT_CY = 24.0, 0.0
CRYPT_W, CRYPT_H   = 6.0, 4.0

A_CRATER = math.pi * R_CRATER ** 2
A_CRYPT  = CRYPT_W * CRYPT_H

# Solve the cruciform limb width w so NET walkable == the MEASURED area.
#   gross(w) = EXT_NS*w + EXT_EW*w - w^2      (vertical bar + horizontal bar - overlap)
#   net(w)   = gross(w) - A_CRATER - A_CRYPT  == AREA_WALKABLE_M2
# Piers do NOT subtract: their inner face is set exactly on the limb edge (the lineage's own
# architecture -- the dado's "INNER edge = the measured ring and is load-bearing"), so they
# stand OUTSIDE the walkable and are emitted as PROP FOOTPRINTS (Crack-law Corr.2 sec 2).
S = EXT_NS + EXT_EW
T = AREA_WALKABLE_M2 + A_CRATER + A_CRYPT
disc = S * S - 4.0 * T
assert disc > 0
W_LIMB = (S - math.sqrt(disc)) / 2.0
HW = W_LIMB / 2.0
GROSS = S * W_LIMB - W_LIMB ** 2
NET = GROSS - A_CRATER - A_CRYPT

# ------------------------------------------------------------ 3. ELEVATION
WALL_RISE_M   = 34.0     # DECLARED: "true scale, 30+ m nave" (brief cl.3 / Corr.3 cl.1)
ARCADE_TOP    = 12.0     # ground arcade band 0 -> 12 m (arch apex ~11 m)
TRIF_BOT, TRIF_TOP = 12.0, 17.0
CLER_BOT, CLER_TOP = 17.0, 26.0
VAULT_SPRING  = 26.0
DAIS_H        = 1.2
CROSS_MOUNT   = dict(cx=0.0, base_h=14.0, height=6.0, width=3.6, arm_thick=1.2)

# ------------------------------------------------------------ 4. ENTRANCES
# player spawn: DECLARED, 2.0 m inside the south door on the nave axis.
SPAWN = (0.0, Y_S + 2.0)
# p05, the near ambush: ||p05|| = 7.16 m from the player (MEASURED, KP-66 Class 3 /
# Crack-law Corr.4 cl.2 "the 7 m ambush at t = 4 s"). Placed on the south facade east of the
# door so the decoded distance is reproduced exactly rather than approximated.
P05_NORM = 7.16
_dy = SPAWN[1] - Y_S                                   # 2.0
_dx = math.sqrt(max(P05_NORM**2 - _dy**2, 0.0))        # 6.875...
SE_BREACH = (_dx, Y_S)
SE_BREACH_W = 4.0

NORTH_BREACH = (-7.0, Y_N)     # DECLARED: beside the apse, west of the axis
NORTH_BREACH_W = 4.0

# apron depth. DERIVED from measured walk rate + the ruled D-LIFT-1/2 cadence:
# a 3.0 m apron is crossed in 3.0/WALK_M_S s (~1.22 s) = about ONE ~1 s tick, while death
# takes ~6 s => crossable-not-campable (Crack-law Corr.4 cl.2).
APRON_M = 3.0
APRON_CROSS_S = APRON_M / WALK_M_S

# ------------------------------------------------------ 5. POOL REGISTRATION
# The six MEASURED pools live in the arena geometry frame (+x EAST, +y SOUTH, origin = the
# geometry file's frame origin). The registration transform onto the cruciform frame is
# DERIVED, not chosen:
#   (a) Corrigendum 2 sec 2 of the crack-law doc re-ruled the arena: the player enters from
#       the SOUTH FACADE and the apse is NORTH. The measured plan has its apse at LARGE old-y
#       (the old frame called that south). So the compass is re-labelled by a yaw.
#   (b) The bbox is 57.285 x 76.665 -- NOT square -- so a +-90 deg yaw cannot map the measured
#       bbox onto the arena bbox. Only 0 deg and 180 deg can. 0 deg keeps the apse in the south
#       and is refuted by (a). => THE YAW IS 180 deg, forced, not assumed.
#   (c) 180 deg about the vertical: old-east -> new-west, old-south -> new-north. With both
#       bboxes carrying the SAME measured extent (we reuse it), the translation is fixed by
#       corner coincidence.
OLD_BBOX = gr["arena"]["bbox_m"]              # [xmin, ymin, xmax, ymax] in old frame
C_X = X_E + OLD_BBOX[2] * -1.0 - 0.0          # placeholder, solved below
C_X = X_W + OLD_BBOX[2]                       # X_new = -old_x + C_X  ; old_x=xmax -> X_W
C_Y = Y_S - OLD_BBOX[1]                       # Y_new =  old_y + C_Y  ; old_y=ymin -> Y_S
def reg(oldx, oldy):
    return (-oldx + C_X, oldy + C_Y)
# verification of the transform on the bbox corners (must land on the arena bbox exactly)
_v0 = reg(OLD_BBOX[0], OLD_BBOX[1]); _v1 = reg(OLD_BBOX[2], OLD_BBOX[3])
REG_RESIDUAL = max(abs(_v0[0] - X_E), abs(_v0[1] - Y_S), abs(_v1[0] - X_W), abs(_v1[1] - Y_N))

K_DISJOINT = gr["dot_zones"]["k_disjoint"]
POOLS = []
for z in gr["dot_zones"]["zones"]:
    ox, oy = z["interior_point_m"]
    nx, ny = reg(ox, oy)
    rub = z["radius_upper_bound_m"]
    rdis = z.get("radius_disjoint_m", rub * K_DISJOINT)
    POOLS.append(dict(id=z["id"], witness_shot=z["witness_shot"],
                      old_m=[ox, oy], arena_m=[nx, ny],
                      radius_disjoint_m=rdis, radius_upper_bound_m=rub))

# ------------------------------------------------------- 6. CAMERA / CLAMP
# The runtime is a 2D camera 1:1 on the plate (cliffside_B/parallax/parallax.json):
# view 1920x1080, player anchored at (962, 595). So the elevation band a player can ever see
# above his own plan position is ANCHOR_Y px:
VISIBLE_ELEV_AT_S0_M = ANCHOR_Y / PX_ELEV
# and the ground distance ahead (up-screen, NW) before the frame top:
VISIBLE_GROUND_AHEAD_M = ANCHOR_Y / PX_GROUND
# minimum wall height whose crown clears a VIEW_H-tall frame when its base is at frame bottom:
MIN_WALL_FOR_CROWN_CLEARANCE_M = VIEW_H / PX_ELEV
CROWN_RISE_PX = WALL_RISE_M * PX_ELEV
CROWN_CLEARANCE_PX = CROWN_RISE_PX - VIEW_H
# and at the earlier arena guide's ZOOM-GD review scale, for the record
ZOOM_GD_PPM = 75.668403
ZOOM_GD_PX_ELEV = ZOOM_GD_PPM * math.cos(ALPHA)
ZOOM_GD_MIN_WALL_M = VIEW_H / ZOOM_GD_PX_ELEV
ZOOM_GD_CROWN_CLEARANCE_PX = WALL_RISE_M * ZOOM_GD_PX_ELEV - VIEW_H
# the zoom-out that would be needed to bring each upper storey into frame at s = 0:
def ppm_to_see(h_m):
    return (ANCHOR_Y / h_m) / math.cos(ALPHA)
PPM_TO_SEE_TRIF_BOT = ppm_to_see(TRIF_BOT)
PPM_TO_SEE_CLER_BOT = ppm_to_see(CLER_BOT)
PPM_TO_SEE_CLER_TOP = ppm_to_see(CLER_TOP)

# ------------------------------------------------------------- 7. SURROUND
SURROUND_NW = AISLE_W + AISLE_WALL + CHAPEL_D + 1.5   # 10.0 m of real rooms beyond
SURROUND_SE = 12.0                                    # exterior ground so near frames carry content

spec = dict(
    generated="2026-09-27", author="drax (presentation seam)", run="C-9",
    product="CA-guides-v1 — cathedral arena grey box",
    authorities=["R-C9-43", "R-C9-44", "R-C9-45",
                 "crack-law Corrigendum 2 sec 2", "crack-law Corrigendum 4",
                 "rdr-art-illuminated-archive-brief sec 3 / sec 4"],
    projection=dict(
        _prov="MEASURED (ppm, alpha) + RULED-as-compass-word (yaw)",
        ppm_plate=PPM, alpha_deg=ALPHA_DEG, yaw_deg=YAW_DEG,
        yaw_reason="R-C9-45 cl.1 'from the SOUTH-EAST looking NORTH-WEST'. SE is 45 deg exactly; "
                   "45 deg is the only yaw at which both rising walls present equally. The GD "
                   "runtime's 47 deg is a yaw in referent axes, which carry no compass.",
        px_per_m_screen_right=PPM,
        px_per_m_along_view=PX_GROUND, px_per_m_elevation=PX_ELEV,
        d_plan_NW=list(D_PLAN), r_plan_NE=list(R_PLAN),
        cliffside_cross_check_residual_px=[CHECK_GROUND, CHECK_ELEV],
        rule="screen_x = ppm*((P-O).r) ; screen_y = -(ppm*sin(a)*((P-O).d) + ppm*cos(a)*h)",
    ),
    figure_height_conflict=dict(
        _prov="MEASURED, CARRIED UNRESOLVED (greyroom manifest scale_figures)",
        keeper_convention_px=KEEPER_PX, keeper_px_implies_body_m=KEEPER_PX_IMPLIES,
        kc2_h_fig_m=KC2_HFIG_M, kc2_h_fig_px_on_this_plate=KC2_HFIG_PX,
        note="this grey box adopts the PLATE SCALE (what '130 px' pins) and carries both figures."
    ),
    runtime_camera=dict(_prov="MEASURED (cliffside_B/parallax/parallax.json)",
                        view_px=[VIEW_W, VIEW_H], anchor_px=[ANCHOR_X, ANCHOR_Y],
                        walk_px_s=WALK_PX_S, walk_m_s=WALK_M_S,
                        run_px_s=RUN_PX_S, run_m_s=RUN_M_S,
                        kind="2D camera, 1:1 on the plate"),
    room=dict(
        _prov="MEASURED extent + MEASURED walkable area (arena geometry v1, sha "
              + gr["arena"]["geometry_sha256"][:16] + "...)",
        extent_ew_m=EXT_EW, extent_ns_m=EXT_NS,
        walkable_area_target_m2=AREA_WALKABLE_M2,
        bbox_m=[X_W, Y_S, X_E, Y_N],
        origin="the CROSSING centre",
        nave_chancel_ratio=NAVE_CHANCEL_RATIO, y_north=Y_N, y_south=Y_S,
        limb_width_m=W_LIMB, limb_half_m=HW,
        gross_cruciform_m2=GROSS, net_walkable_m2=NET,
        net_walkable_residual_m2=NET - AREA_WALKABLE_M2,
        limb_width_prov="DERIVED: solves gross(w) - crater - crypt = the MEASURED walkable area "
                        "inside the MEASURED extent. Not chosen.",
        measured_central_vessel_width_m=CENTRAL_VESSEL_M,
        bay_m=BAY_M,
    ),
    elevation=dict(_prov="DECLARED (heights); RULED (that they rise out of frame, R-C9-43 cl.1)",
                   wall_rise_m=WALL_RISE_M, near_cut_m=NEAR_CUT_M,
                   arcade=[0.0, ARCADE_TOP], triforium=[TRIF_BOT, TRIF_TOP],
                   clerestory=[CLER_BOT, CLER_TOP], vault_spring_m=VAULT_SPRING,
                   dais_h=DAIS_H, cross_mount=CROSS_MOUNT),
    rise_rule=dict(_prov="DERIVED from the camera azimuth. No list of faces is authored.",
                   rule="a wall rises to wall_rise_m iff its INNER normal n satisfies "
                        "n . SE > 0 where SE = (+1,-1)/sqrt(2); otherwise it is cut to near_cut_m.",
                   consequence="rising: apse wall, transept NORTH walls, nave/chancel WEST arcade, "
                               "west transept end wall.  cut low: south facade, transept SOUTH "
                               "walls, nave/chancel EAST arcade, east transept end wall."),
    crater=dict(_prov="DECLARED radius", centre_m=[0.0, 0.0], radius_m=R_CRATER,
                walkable=False, hazard=True,
                reason="leaves %.2f m of walkable floor between the crater lip and each crossing "
                       "edge -- room to circle it, which is the ruled funnel-to-the-middle "
                       "(Corr.4 cl.4). Under half the crossing width." % (HW - R_CRATER)),
    entrances=[
        dict(id="E-CRYPT", kind="crypt_mouth_floor_hole", one_way=True,
             centre_m=[CRYPT_CX, CRYPT_CY], size_m=[CRYPT_W, CRYPT_H],
             apron="bluefire", _prov="DECLARED position (by the cut-low east wall, R-C9-45 cl.1)"),
        dict(id="E-SE-FIRE", kind="fire_breach_south_facade", one_way=True,
             centre_m=list(SE_BREACH), width_m=SE_BREACH_W, apron="fire",
             _prov="DERIVED from MEASURED ||p05|| = %.2f m: placed on the south facade so its "
                   "distance from the declared player spawn reproduces the decoded near-ambush "
                   "distance exactly." % P05_NORM,
             p05_norm_m=P05_NORM, dist_from_spawn_m=math.dist(SPAWN, SE_BREACH)),
        dict(id="E-N-CHANCEL", kind="chancel_breach_ground_with_broken_stair", one_way=True,
             centre_m=list(NORTH_BREACH), width_m=NORTH_BREACH_W, apron="bluefire",
             _prov="DECLARED position (beside the apse, R-C9-45 / Corr.4 cl.3)"),
    ],
    spawn=dict(player_spawn_m=list(SPAWN),
               _prov="DECLARED: 2.0 m inside the south door on the nave axis (R-C9-45 cl.2 "
                     "'road in through the south facade')"),
    apron=dict(depth_m=APRON_M, cross_time_s=APRON_CROSS_S,
               _prov="DERIVED from MEASURED walk rate %.3f m/s and the RULED D-LIFT-1/2 cadence "
                     "(~1 s ticks, death ~6 s): crossed in ~one tick, so crossable-not-campable."
                     % WALK_M_S,
               rule="apron = dilate(mouth, depth) INTERSECT walkable floor"),
    pool_registration=dict(
        _prov="DERIVED transform on MEASURED interior points",
        transform=dict(yaw_deg=180.0, X_new="-old_x + %.6f" % C_X, Y_new="old_y + %.6f" % C_Y,
                       derivation="(a) the re-ruling puts the apse NORTH and the entry SOUTH; "
                                  "(b) the bbox 57.285 x 76.665 is not square so +-90 deg cannot "
                                  "map bbox to bbox; (c) 0 deg keeps the apse south and is refuted "
                                  "by (a). 180 deg is forced.",
                       bbox_corner_residual_m=REG_RESIDUAL),
        k_disjoint=K_DISJOINT,
        radius_caveat="radius_disjoint = upper_bound * k_disjoint. The INTERIOR POINTS are "
                      "MEASURED; the RADII are an upper bound scaled by drax's k_disjoint call. "
                      "Every overlap verdict is recomputed at BOTH radii and flagged if it flips.",
        pools=POOLS),
    camera_clamp=dict(
        _prov="DERIVED from the MEASURED runtime camera + the projection law",
        visible_elevation_at_own_position_m=VISIBLE_ELEV_AT_S0_M,
        visible_ground_ahead_m=VISIBLE_GROUND_AHEAD_M,
        min_wall_height_for_crown_clearance_m=MIN_WALL_FOR_CROWN_CLEARANCE_M,
        crown_rise_px=CROWN_RISE_PX, crown_clearance_px=CROWN_CLEARANCE_PX,
        crown_clearance_m=CROWN_CLEARANCE_PX / PX_ELEV,
        zoom_gd=dict(ppm=ZOOM_GD_PPM, px_per_m_elevation=ZOOM_GD_PX_ELEV,
                     min_wall_height_m=ZOOM_GD_MIN_WALL_M,
                     crown_clearance_px=ZOOM_GD_CROWN_CLEARANCE_PX),
        ppm_that_would_reveal=dict(triforium_bottom=PPM_TO_SEE_TRIF_BOT,
                                   clerestory_bottom=PPM_TO_SEE_CLER_BOT,
                                   clerestory_top=PPM_TO_SEE_CLER_TOP),
    ),
    surround=dict(_prov="DECLARED", nw_m=SURROUND_NW, se_m=SURROUND_SE,
                  aisle_w=AISLE_W, aisle_wall=AISLE_WALL, chapel_d=CHAPEL_D, pier_w=PIER_W),
)

OUT = os.path.join(os.path.dirname(__file__), "..", "cathedral_spec.json")
json.dump(spec, open(os.path.abspath(OUT), "w"), indent=1)

# -------------------------------------------------------------- report
print("PROJECTION  ppm %.6f  alpha %.10f deg  yaw %.1f deg" % (PPM, ALPHA_DEG, YAW_DEG))
print("            px/m along view %.6f   px/m elevation %.6f" % (PX_GROUND, PX_ELEV))
print("            cliffside cross-check residual  %.3e / %.3e px" % (CHECK_GROUND, CHECK_ELEV))
print()
print("ROOM        extent %.3f EW x %.3f NS m   (MEASURED, reused)" % (EXT_EW, EXT_NS))
print("            bbox  x [%.4f, %.4f]  y [%.4f, %.4f]" % (X_W, X_E, Y_S, Y_N))
print("            limb width w = %.6f m  (half %.6f)" % (W_LIMB, HW))
print("            gross cruciform %.4f  - crater %.4f - crypt %.4f = %.4f m2"
      % (GROSS, A_CRATER, A_CRYPT, NET))
print("            MEASURED target %.4f m2   residual %.3e m2" % (AREA_WALKABLE_M2, NET - AREA_WALKABLE_M2))
print("            *** measured central-vessel width %.4f m -- CONFLICT, see README" % CENTRAL_VESSEL_M)
print()
print("CAMERA      visible elevation at own position  %.4f m  (anchor %d px / %.4f px/m)"
      % (VISIBLE_ELEV_AT_S0_M, ANCHOR_Y, PX_ELEV))
print("            visible ground ahead (NW)          %.4f m" % VISIBLE_GROUND_AHEAD_M)
print("            min wall height to clear a 1080 frame  %.4f m" % MIN_WALL_FOR_CROWN_CLEARANCE_M)
print("            wall %.1f m rises %.1f px; clearance over 1080 = %.1f px (%.3f m)"
      % (WALL_RISE_M, CROWN_RISE_PX, CROWN_CLEARANCE_PX, CROWN_CLEARANCE_PX / PX_ELEV))
print("            ZOOM-GD ppm %.4f: min wall %.4f m, clearance %.1f px"
      % (ZOOM_GD_PPM, ZOOM_GD_MIN_WALL_M, ZOOM_GD_CROWN_CLEARANCE_PX))
print("            ppm that would reveal: triforium %.3f  clerestory %.3f  clerestory top %.3f"
      % (PPM_TO_SEE_TRIF_BOT, PPM_TO_SEE_CLER_BOT, PPM_TO_SEE_CLER_TOP))
print()
print("ENTRANCES   spawn %s ; SE fire breach %s ; |p05| target %.3f actual %.6f"
      % (SPAWN, tuple(round(v,4) for v in SE_BREACH), P05_NORM, math.dist(SPAWN, SE_BREACH)))
print("            apron depth %.2f m crossed in %.3f s at walk %.4f m/s" % (APRON_M, APRON_CROSS_S, WALK_M_S))
print()
print("POOLS       transform: X = -old_x + %.6f ; Y = old_y + %.6f ; corner residual %.3e m"
      % (C_X, C_Y, REG_RESIDUAL))
for p in POOLS:
    print("            %-6s old (%8.3f,%8.3f) -> arena (%8.3f,%8.3f)  r_dis %6.3f  r_ub %6.3f"
          % (p["id"], p["old_m"][0], p["old_m"][1], p["arena_m"][0], p["arena_m"][1],
             p["radius_disjoint_m"], p["radius_upper_bound_m"]))
print()
print("wrote", os.path.abspath(OUT))
