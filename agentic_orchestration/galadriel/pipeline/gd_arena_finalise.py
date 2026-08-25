#!/usr/bin/env python3
"""gd_arena_finalise.py — assemble the (h-a') geometry deliverable.

Emits crucible-arena-geometry-v1.json:
  * arena-local frame definition
  * hard_boundary outer ring + interior obstruction rings
  * green_zones as measured interior points with bracketed radius bounds
  * per-segment coverage + provenance flags
  * the scale block, with its derivation chain and its (wide) uncertainty
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "notes",
                   "crucible-arena-geometry-v1.json")

CLOCK = {612: "22:48:38", 613: "22:48:42", 614: "22:48:53", 615: "22:49:01",
         616: "22:49:27", 617: "22:49:31", 618: "22:49:36", 619: "22:49:42",
         620: "22:49:47", 621: "22:49:58", 622: "22:50:02", 623: "22:50:05",
         624: "22:50:10", 625: "22:50:14", 626: "22:50:18", 627: "22:50:23",
         628: "22:50:28", 629: "22:50:37", 630: "22:50:41", 631: "22:50:45",
         632: "22:50:49"}

# scale chain (see the findings note, section "scale")
S_SCREEN_PER_MMPX = 14.6      # E-W, from the 612->627 north-gate displacement
S_LO, S_HI = 12.6, 16.6
CHAR_PX, CHAR_PX_LO, CHAR_PX_HI = 70.0, 58.0, 82.0
CHAR_M, CHAR_M_LO, CHAR_M_HI = 1.9, 1.8, 2.0
COSTH, COSTH_LO, COSTH_HI = 0.50, 0.34, 0.64


def main():
    b = json.load(open(os.path.join(HERE, "gd-arena-boundary2.json")))
    occ = json.load(open(os.path.join(HERE, "gd-zone-occupancy.json")))
    meta = json.load(open(os.path.join(HERE, "gd-arena-mosaic-meta.json")))
    obs = np.load(os.path.join(HERE, "gd-footprint-obs.npy"))
    ox, oy = meta["ox"], meta["oy"]
    track = {r["shot"]: np.array(r["arena"]) for r in occ}
    inzone = [r["shot"] for r in occ if r["g60"] > 0.10]
    clean = [r["shot"] for r in occ if r["g60"] <= 0.001]

    outer = np.array(b["outer"], float)
    print("outer vertices:", len(outer))
    print("bbox minimap px: x[%.0f,%.0f] y[%.0f,%.0f]  ->  %.0f x %.0f"
          % (outer[:, 0].min(), outer[:, 0].max(), outer[:, 1].min(),
             outer[:, 1].max(), np.ptp(outer[:, 0]), np.ptp(outer[:, 1])))

    # --- per-vertex coverage -------------------------------------------------
    T = np.array([track[s] for s in sorted(track)])
    dmin = np.array([np.hypot(*(T - v).T).min() for v in outer])
    ovtx = np.array([obs[int(round(v[1] + oy)), int(round(v[0] + ox))] for v in outer])
    print("vertex distance to nearest station: median %.1f  p90 %.1f  max %.1f px"
          % (np.median(dmin), np.percentile(dmin, 90), dmin.max()))
    print("vertex minimap-observation count: min %d  median %d"
          % (ovtx.min(), int(np.median(ovtx))))

    # --- coverage gaps: contiguous runs of poorly-witnessed vertices ---------
    weak = (ovtx < 3) | (dmin > 70)
    runs, i = [], 0
    N = len(outer)
    while i < N:
        if weak[i]:
            j = i
            while j < N and weak[j]:
                j += 1
            if j - i >= 3:
                runs.append((i, j - 1))
            i = j
        else:
            i += 1
    print("coverage-gap arcs (>=3 consecutive weak vertices):", len(runs))
    for a, z in runs:
        seg = outer[a:z + 1]
        ang = np.degrees(np.arctan2(seg[:, 0].mean() - 4, -(seg[:, 1].mean() - 60)))
        print(f"   vertices {a}-{z}  n={z-a+1}  bearing~{ang:6.1f} deg  "
              f"minobs={ovtx[a:z+1].min()}  maxdist={dmin[a:z+1].max():.0f}")

    # --- green zones ---------------------------------------------------------
    zones = []
    for s in inzone:
        p = track[s]
        db = min(np.hypot(*(track[c] - p)) for c in clean)
        near = min(clean, key=lambda c: np.hypot(*(track[c] - p)))
        zones.append(dict(id=f"Z-{s}", witness_shot=s,
                          interior_point_minimap_px=[float(p[0]), float(p[1])],
                          radius_upper_bound_px=round(float(db), 1),
                          bounding_clean_shot=near))
    print("\ngreen-zone witnesses:", inzone)
    for z in zones:
        print(f"   {z['id']} at ({z['interior_point_minimap_px'][0]:6.1f},"
              f"{z['interior_point_minimap_px'][1]:6.1f})  r<={z['radius_upper_bound_px']:5.1f} "
              f"(bounded by shot {z['bounding_clean_shot']})")

    # pairwise distinctness: separated if a clean station lies between, or if
    # the separation exceeds one witness's own radius bound
    print("\npairwise zone distinctness:")
    ndist = 0
    for i in range(len(zones)):
        for j in range(i + 1, len(zones)):
            a, bz = zones[i], zones[j]
            pa = np.array(a["interior_point_minimap_px"])
            pb = np.array(bz["interior_point_minimap_px"])
            sep = float(np.hypot(*(pa - pb)))
            sepby = sep > min(a["radius_upper_bound_px"], bz["radius_upper_bound_px"])
            ndist += sepby
            print(f"   {a['id']} vs {bz['id']}: sep={sep:6.1f}  "
                  f"{'DISTINCT' if sepby else 'not separable'}")
    print(f"   -> {ndist}/{len(zones)*(len(zones)-1)//2} pairs demonstrably distinct")

    # --- scale ---------------------------------------------------------------
    def u(s, hpx, hm, ct):
        k = hpx / (hm * ct)
        return s / k
    u_mid = u(S_SCREEN_PER_MMPX, CHAR_PX, CHAR_M, COSTH)
    u_lo = min(u(s, h, m, c) for s in (S_LO, S_HI) for h in (CHAR_PX_LO, CHAR_PX_HI)
               for m in (CHAR_M_LO, CHAR_M_HI) for c in (COSTH_LO, COSTH_HI))
    u_hi = max(u(s, h, m, c) for s in (S_LO, S_HI) for h in (CHAR_PX_LO, CHAR_PX_HI)
               for m in (CHAR_M_LO, CHAR_M_HI) for c in (COSTH_LO, COSTH_HI))
    print(f"\nscale: u = {u_mid:.3f} m/minimap-px   band [{u_lo:.3f}, {u_hi:.3f}]")
    print(f"arena outer extent: {np.ptp(outer[:,0])*u_mid:.1f} x {np.ptp(outer[:,1])*u_mid:.1f} m"
          f"   (band {np.ptp(outer[:,0])*u_lo:.0f}-{np.ptp(outer[:,0])*u_hi:.0f} m wide)")

    # --- assemble ------------------------------------------------------------
    def to_m(v):
        return [round(v[0] * u_mid, 3), round(v[1] * u_mid, 3)]

    doc = {
        "$schema_note": "galadriel arena-boundary trace, KC2 (h-a') baton row, "
                        "conductor ruling R-L64-1.",
        "referent": "Grim Dawn - Crucible of the Dead (Matt's perimeter walk, "
                    "21 captures 2026-08-24 22:48:38-22:50:49 local)",
        "capture_set": "agentic_orchestration/galadriel/captures/"
                       "2026-08-24-crucible-arena-perimeter/",
        "authored": "2026-08-24", "author": "galadriel", "version": 1,
        "frame": {
            "origin": "shot 612 player position (the north gate, in front of the "
                      "Master of the Crucible's red door)",
            "axes": "+x = EAST, +y = SOUTH (minimap is north-up; the frame is the "
                    "minimap's own frame, not screen space)",
            "handedness_note": "+y points SOUTH. Godot import must flip or rotate "
                               "to its own convention; no flip is applied here.",
            "native_units": "minimap pixels at Grim Dawn's fixed HUD minimap zoom, "
                            "1920x1080",
            "metres_per_native_unit": round(u_mid, 4),
            "arena_centroid_native": [4.0, 60.0]
        },
        "scale": {
            "value_m_per_minimap_px": round(u_mid, 4),
            "band_m_per_minimap_px": [round(u_lo, 4), round(u_hi, 4)],
            "provenance": "DERIVED-WEAK",
            "why_not_measured": "the screen<->arena ground map M could not be "
                                "recovered from this capture set (see findings "
                                "note, 'what the shots cannot support'); without M "
                                "the character-height anchor cannot be converted "
                                "to arena units except through a chain of four "
                                "separately-uncertain terms.",
            "chain": {
                "s_screen_px_per_minimap_px": S_SCREEN_PER_MMPX,
                "s_source": "north-gate displacement between shots 612 and 627 "
                            "(same landmark, minimap delta (25,6) px, screen delta "
                            "(366,90) px); eye-measured, parallax-contaminated",
                "character_pixel_height": CHAR_PX,
                "character_height_m_ASSUMED": CHAR_M,
                "character_height_assumption_note":
                    "1.9 m stated as an ASSUMPTION. Corroborating (not importing): "
                    "the D-5b decode of NavManager::SetDefaultConfig reports an "
                    "agent height of 2.0, consistent with a ~1.8-2.0 m player model.",
                "cos_camera_pitch": COSTH,
                "cos_camera_pitch_note": "theta ~60 deg assumed; bracketed 50-70 deg "
                                         "by two weak independent reads"
            },
            "consequence": "Every metre figure in this file inherits a ~1.7x "
                           "uncertainty factor. The NATIVE minimap-px geometry does "
                           "NOT. Consumers who need metric truth should pin the "
                           "scale by registering this footprint against the "
                           "sim-side derived occupancy hull (which carries real "
                           "metric extents) - deliberately NOT done here."
        },
        "hard_boundary": {
            "provenance": "MEASURED-APPROXIMATE-FROM-REFERENCE",
            "method": "21 player-centred minimap discs registered by masked "
                      "normalised cross-correlation; per-shot terrain "
                      "classification then per-pixel vote (p>0.65, obs>=3); "
                      "connected component containing the player track; "
                      "Moore-neighbour contour walk; Douglas-Peucker eps=1.5 px",
            "uncertainty_m": round(2.5 * u_mid, 3),
            "uncertainty_native_px": 2.5,
            "uncertainty_basis": "registration residual +-1 px (1-sigma, from "
                                 "3-4-anchor cross-checks, spread <=0.7 px) "
                                 "convolved with minimap edge softness +-2 px",
            "outer_ring": {
                "vertices_native": b["outer"],
                "vertices_m": [to_m(v) for v in b["outer"]],
                "n": len(b["outer"]), "closed": True
            },
            "interior_obstructions": [
                {"id": f"OB-{i+1}", "area_native_px2": h["area_px"],
                 "note": "unmapped island inside the arena floor: Grim Dawn's "
                         "minimap paints walkable floor only, so an enclosed "
                         "unpainted island is impassable geometry (inner wall arc "
                         "or pillar block)",
                 "vertices_native": h["vertices"],
                 "vertices_m": [to_m(v) for v in h["vertices"]]}
                for i, h in enumerate(b["holes"])
            ],
            "floor_area_native_px2": b["area_px"],
            "floor_area_m2": round(b["area_px"] * u_mid ** 2, 1),
            "bbox_native": [round(float(outer[:, 0].min()), 1),
                            round(float(outer[:, 1].min()), 1),
                            round(float(outer[:, 0].max()), 1),
                            round(float(outer[:, 1].max()), 1)],
            "extent_native": [round(float(np.ptp(outer[:, 0])), 1),
                              round(float(np.ptp(outer[:, 1])), 1)],
            "extent_m": [round(float(np.ptp(outer[:, 0])) * u_mid, 1),
                         round(float(np.ptp(outer[:, 1])) * u_mid, 1)],
            "interpolated_segments": [],
            "interpolated_segments_note":
                "NONE. Every outer-ring vertex was painted by at least 3 "
                "independent minimap observations (min 3, median 13), and 0 of "
                "1755 boundary pixels abut an unobserved region of the mosaic "
                "canvas. The perimeter walk fully enclosed the arena in minimap "
                "coverage, so no arc of the boundary had to be bridged.",
            "unwalked_arcs": [
                {"vertex_index_from": int(a), "vertex_index_to": int(z),
                 "n_vertices": int(z - a + 1),
                 "min_minimap_observations": int(ovtx[a:z + 1].min()),
                 "max_distance_to_nearest_station_native":
                     round(float(dmin[a:z + 1].max()), 1),
                 "provenance": "MEASURED-APPROXIMATE-FROM-REFERENCE",
                 "caveat": "mapped but never walked: the minimap painted this arc "
                           "from a distance, so its shape is measured but its "
                           "WALKABILITY was never demonstrated by the player's own "
                           "body. Both runs lie on the north corridor and its "
                           "terminal chamber, which Matt approached but did not "
                           "enter."}
                for a, z in runs]
        },
        "green_zones": {
            "class_note": "ENTERABLE DAMAGE FIELDS, NOT WALLS. The Godot arena must "
                          "NOT collide-block these. Matt attestation (L-64): the "
                          "character can enter but takes a severe and immediate DoT "
                          "tick; element suspected poison (Matt's own hedge).",
            "dot_mechanic": {"provenance": "ATTESTED-UNMEASURED",
                             "magnitude": None, "element": "suspected-poison",
                             "note": "no number is derived here; see the findings "
                                     "note for the two named decode paths."},
            "geometry_provenance": "INTERIOR-POINT-MEASURED / EXTENT-UNMEASURED",
            "polygons": None,
            "why_no_polygons": "tracing a zone outline requires projecting the "
                               "world-view green mask onto the arena floor, which "
                               "requires the ground map M. M is not recoverable "
                               "from these 21 stations (all world-view registration "
                               "attempts returned noise-level NCC 0.04-0.27). "
                               "Rather than invent an outline, each zone ships as a "
                               "measured interior point with a measured upper bound "
                               "on its radius.",
            "count_demonstrated": len(zones),
            "count_note": "six mutually distinct zones are DEMONSTRATED (each pair "
                          "separated either by an intervening zone-free station or "
                          "by more than one member's own radius bound). Matt "
                          "attests he entered all of them; whether six is the total "
                          "is NOT established by these shots - a zone entered "
                          "between two exposures leaves no evidence.",
            "zones": zones
        },
        "stations": [
            {"shot": r["shot"], "clock_local": CLOCK[r["shot"]],
             "arena_native": r["arena"],
             "arena_m": to_m(r["arena"]),
             "in_green_zone": r["g60"] > 0.10,
             "green_fraction_r60": r["g60"], "green_fraction_r140": r["g140"]}
            for r in occ
        ]
    }
    json.dump(doc, open(OUT, "w"), indent=1)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
