# C-9 meshy_t1 step 1: make a Meshy library clip usable as a game cycle.
#
#   blender -b -noaudio --python scripts/03_clips.py -- <clip.glb> <name> <out.json>
#
# Generic, because the point of T1 is a pipeline for ANY Meshy-rigged humanoid,
# not this knight:
#
#  * SKINNED MESHES ONLY. This rig ships a 42-vertex `Icosphere` alongside the
#    character, unskinned, sitting at z = -1.0. It is what made "lowest vertex"
#    read exactly -1.00000 on every frame of every clip, so any ground
#    calibration taken off the scene bbox would have been measuring a stray
#    sphere instead of the knight's feet. Meshes without an armature modifier
#    bound to the rig are ignored everywhere in this pipeline.
#
#  * BONES BY ROLE, NOT BY NAME. Meshy's naming is Mixamo-STYLE but not Mixamo:
#    `Spine, Spine01, Spine02` (Mixamo goes Spine, Spine1, Spine2), lowercase
#    `neck`, and `head_end` / `headfront` with no `HeadTop_End` or `Toe_End`.
#    Everything downstream resolves bones through a role map built by matching
#    lowercased names, so a differently-named rig still works.
#
#  * IN PLACE BY REMOVING THE LINEAR DRIFT ONLY. A clip may or may not arrive
#    with root travel. Fitting a straight line to the root's horizontal track
#    and subtracting it removes travel if there is any and is a no-op if there
#    is not, while leaving the sway and the vertical bob intact -- which
#    zeroing the root outright would destroy.
#
#  * TWO CLIP CONVENTIONS, DETECTED NOT ASSUMED. Meshy's free library clips
#    arrive IN PLACE: the ground speed is not in the root at all, it is in the
#    stance foot sliding backward under the body. Its text-to-motion clips
#    TRAVEL: the root moves and the stance foot stays put. Measuring the wrong
#    one silently returns nonsense -- the carry walk read 0.173 m/s on the
#    stance foot when it is really doing 1.22 m/s in the root. So the root's
#    linear drift decides which measurement is the speed.
#
#  * CYCLE BY SELF-SIMILARITY, with the root removed. A travelling 4 s walk is
#    several strides, not one cycle; the "does the last frame repeat the first"
#    test only works on a clip that is already one loop. The period is found by
#    comparing root-relative poses at every lag and taking the best, so a long
#    clip is cut to its own stride.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, NAME, OUTP = a[0], a[1], a[2]

# the game's cadence, from knight_fit.json / knight_foot_slide.json
CANVAS_PX_PER_M = 150.21354166666666 / 1.80          # 83.452
# the height every rig is normalised to at render time (04_render --height)
RENDER_HEIGHT_M = 1.80
GAME = {"walk": dict(px_s=247.0, period=0.5797, frames=12),
        "run": dict(px_s=494.0, period=0.5517, frames=8),
        # The idle and the attack keep their OWN duration: the game's idle slot
        # is 2.0 s but this library idle is 4.04 s, and compressing it would
        # make a standing knight fidget. The attack is played as authored at
        # ~12 fps. Both report their real fps rather than being forced.
        "idle": dict(px_s=0.0, period=None, frames=12),
        "attack": dict(px_s=0.0, period=None, frames=None)}

ROLES = {
    "hips": ["hips", "pelvis", "root"],
    # CHEST is its own role and is resolved BEFORE spine: Meshy names the
    # chain Spine, Spine01, Spine02, so an exact match on "spine" lands on the
    # LOWEST one, near the pelvis. Carrying a weapon relative to that puts the
    # grip too low and too far forward to reach.
    "chest": ["spine02", "spine2", "chest", "upperchest", "spine_03"],
    "spine": ["spine"], "head": ["head"], "neck": ["neck"],
    "l_upleg": ["leftupleg", "l_upleg", "thigh_l", "leftthigh"],
    "r_upleg": ["rightupleg", "r_upleg", "thigh_r", "rightthigh"],
    "l_leg": ["leftleg", "shin_l", "leftshin", "leftcalf"],
    "r_leg": ["rightleg", "shin_r", "rightshin", "rightcalf"],
    "l_foot": ["leftfoot", "foot_l"], "r_foot": ["rightfoot", "foot_r"],
    "l_toe": ["lefttoebase", "lefttoe", "toe_l"],
    "r_toe": ["righttoebase", "righttoe", "toe_r"],
    "l_hand": ["lefthand", "hand_l"], "r_hand": ["righthand", "hand_r"],
    "l_arm": ["leftarm", "upperarm_l"], "r_arm": ["rightarm", "upperarm_r"],
    "l_fore": ["leftforearm", "lowerarm_l"], "r_fore": ["rightforearm", "lowerarm_r"],
}


def role_map(arm):
    got, used = {}, set()
    low = {b.name: b.name.lower().replace(":", "").replace("mixamorig", "")
           for b in arm.pose.bones}
    for role, pats in ROLES.items():
        best = None
        for bname, l in low.items():
            if bname in used:
                continue
            for p in pats:
                if l == p:
                    best = bname; break
            if best:
                break
        if best is None:
            for bname, l in low.items():
                if bname in used:
                    continue
                if any(l.startswith(p) or p in l for p in pats):
                    best = bname; break
        if best:
            got[role] = best; used.add(best)
    return got


def steadiness(P, cyc, fps, game_period, game_px_s):
    """Per-window arc speed over every cycle-length window of the root path."""
    P = np.asarray(P)[:, :2]
    d = np.diff(P, axis=0)
    step = np.hypot(d[:, 0], d[:, 1])
    dt = cyc / fps
    rows = []
    for s0 in range(0, max(1, len(P) - cyc)):
        arc = float(step[s0:s0 + cyc].sum())
        chord = float(np.hypot(*(P[s0 + cyc] - P[s0]))) if s0 + cyc < len(P) else arc
        rows.append((s0, arc, chord, arc / dt, arc / max(chord, 1e-9)))
    sp = np.array([r[3] for r in rows])
    # Which window should be RESAMPLED? This script resamples from frame 1, which
    # is the right answer only for a clip that starts at speed. On a ramping clip
    # frame 1 is the ramp: carry_run3 reads 6.26 m/s there and 7.54 on its
    # plateau. Report where the plateau starts so the renderer can be pointed at
    # it; the resample itself still starts at frame 1 so already-shipped sheets
    # stay reproducible. KNOWN GAP, tracked in the T1 notes.
    # the PLATEAU is the modal speed, not the extreme: take the median of the
    # middle half of the windows ranked by speed, so one ramp frame cannot set it
    hi = np.sort(sp)[len(sp) // 2:]
    plateau = float(np.median(hi))
    spread = float((sp.max() - sp.min()) / max(sp.mean(), 1e-9))
    ts = dt / game_period if game_period else 1.0
    return dict(
        n_windows=len(rows), cycle_frames=cyc, window_seconds=round(dt, 4),
        win_speed_min_m_s=round(float(sp.min()), 4),
        win_speed_max_m_s=round(float(sp.max()), 4),
        win_speed_plateau_m_s=round(plateau, 4),
        spread=round(spread, 4), steady=bool(spread < 0.10),
        arc_over_chord_max=round(float(max(r[4] for r in rows)), 4),
        px_s_min_at_game_cadence=round(float(sp.min()) * ts * CANVAS_PX_PER_M, 1),
        px_s_max_at_game_cadence=round(float(sp.max()) * ts * CANVAS_PX_PER_M, 1),
        px_s_plateau_at_game_cadence=round(plateau * ts * CANVAS_PX_PER_M, 1),
        px_s_plateau_at_clip_cadence=round(plateau * CANVAS_PX_PER_M, 1),
        plateau_window_start_frame=int(rows[int(np.argmin(np.abs(sp - plateau)))][0]) + 1,
        resampled_window_start_frame=1,
        resample_window_is_plateau=bool(
            abs(sp[0] - plateau) / max(plateau, 1e-9) < 0.05),
        plateau_stride_m=round(plateau * dt, 4),
        period_that_plants_plateau_s=round(
            plateau * dt * CANVAS_PX_PER_M / game_px_s, 4))


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    fps = sc.render.fps
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    skin = [o for o in sc.objects if o.type == 'MESH'
            and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers)]
    strays = [o.name for o in sc.objects if o.type == 'MESH' and o not in skin]
    R = role_map(arm)
    act = arm.animation_data.action
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])

    # ---- sample every bone's world head, plus the character's lowest vertex
    bones = [b.name for b in arm.pose.bones]
    P = {b: [] for b in bones}
    lows, tops = [], []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        for b in bones:
            w = arm.matrix_world @ arm.pose.bones[b].head
            P[b].append([w.x, w.y, w.z])
        dg = bpy.context.evaluated_depsgraph_get()
        lo, hi = 1e9, -1e9
        for o in skin:
            ev = o.evaluated_get(dg); me = ev.to_mesh()
            for v in me.vertices:
                z = (o.matrix_world @ v.co).z
                lo = min(lo, z); hi = max(hi, z)
            ev.to_mesh_clear()
        lows.append(lo); tops.append(hi)
    for b in bones:
        P[b] = np.array(P[b])
    N = f1 - f0 + 1

    # ---- root-relative pose stack, for cycle detection -------------------
    hips0 = R.get("hips", bones[0])
    Q = np.stack([P[b] - P[hips0] for b in bones], 1)      # (N, nbones, 3)

    def pose_dist(lag):
        n = N - lag
        if n < 3:
            return 1e9
        return float(np.linalg.norm(Q[:n] - Q[lag:lag + n], axis=2).mean())

    d_loop = float(np.mean([np.linalg.norm(P[b][-1] - P[b][0]) for b in bones]))
    d_step = float(np.mean([np.linalg.norm(P[b][1] - P[b][0]) for b in bones]))
    dup = d_loop < 0.4 * d_step
    base = (N - 1) if dup else N
    # a cycle must be at least 6 frames and at most the clip; pick the lag that
    # best repeats the pose, preferring the SHORTEST such lag so a clip holding
    # several strides is cut to one
    cands = [(lag, pose_dist(lag)) for lag in range(6, max(7, int(N * 0.7)))]
    # How much does this clip MOVE at all? A near-static idle looks
    # self-similar at every lag, so without this guard the detector returns the
    # smallest lag it is allowed to (it returned 6 frames for a 4 s idle).
    motion = float(np.linalg.norm(Q - Q.mean(0, keepdims=True), axis=2).mean())
    cycle_frames, cyc_score, cyc_why = base, None, "clip length"
    if cands and motion > 0.02:
        ds = np.array([c[1] for c in cands])
        best = float(ds.min()); med = float(np.median(ds))
        # a real period is a clear MINIMUM against the typical lag, not merely
        # the smallest number in a flat curve
        bi = int(np.argmin(ds))
        # A period is a genuine MINIMUM, so the curve must rise again after it.
        # A monotonically rising curve has its smallest value at the smallest
        # lag searched and means "no repeat", not "a 6-frame cycle" -- which is
        # what a 4 s idle returned before this test.
        rises = bool(ds[bi:].max() > 1.5 * best) and bi >= 2
        if med > 0 and best < 0.60 * med and rises:
            cycle_frames = int(min(c[0] for c in cands if c[1] <= best * 1.15))
            cyc_score = round(best / med, 4); cyc_why = "pose self-similarity"
        elif not rises:
            cyc_why = "no clear period (self-similarity never recovers)"
        else:
            cyc_why = "no clear period (flat self-similarity curve)"
    elif cands:
        cyc_why = "near-static clip; whole clip is the loop"
    cyc_curve = {int(c[0]): round(c[1], 5) for c in cands[::2]}
    period = cycle_frames / fps

    # ---- root drift: fit and remove the LINEAR horizontal component
    hips = hips0
    t = np.arange(N)
    drift = {}
    for k, ax in ((0, "x"), (1, "y")):
        m, c = np.polyfit(t, P[hips][:, k], 1)
        drift[ax] = dict(per_frame=float(m), over_cycle=float(m * cycle_frames))
    drift_len = math.hypot(drift["x"]["over_cycle"], drift["y"]["over_cycle"])

    # ---- ground speed: root travel if the clip travels, else the stance foot
    travels = drift_len > 0.30
    speeds, stance = {}, {}
    for side in ("l", "r"):
        key = R.get(side + "_toe") or R.get(side + "_foot")
        if not key:
            continue
        p = P[key]
        z = p[:, 2]
        planted = z < z.min() + 0.03
        idx = np.where(planted)[0]
        if len(idx) < 3:
            continue
        runs, cur = [], [idx[0]]
        for i in idx[1:]:
            (cur.append(i) if i == cur[-1] + 1 else (runs.append(cur), cur.clear(), cur.append(i)))
        runs.append(list(cur))
        best = max(runs, key=len)
        if len(best) < 3:
            continue
        dxy = p[best[-1], :2] - p[best[0], :2]
        dt = (best[-1] - best[0]) / fps
        speeds[key] = float(np.linalg.norm(dxy) / dt)
        stance[key] = dict(frames=len(best), fraction=round(len(best) / cycle_frames, 3),
                           disp_m=[round(float(v), 4) for v in dxy])
    sp_foot = float(np.median(list(speeds.values()))) if speeds else 0.0
    sp_root = drift_len / period if period else 0.0
    sp = sp_root if travels else sp_foot

    g = GAME.get(NAME, GAME["attack"])
    out = dict(
        name=NAME, source=os.path.basename(SRC), fps=fps,
        skinned_meshes=[o.name for o in skin], ignored_unskinned=strays,
        role_map=R, unmapped_bones=[b for b in bones if b not in R.values()],
        action=act.name, frame_range=[f0, f1], n_frames=N,
        last_frame_duplicates_first=bool(dup),
        cycle_frames=cycle_frames, cycle_period_s=round(period, 5),
        character_height_m=round(max(tops) - min(lows), 4),
        char_lowest_z=[round(v, 5) for v in lows],
        root_linear_drift=drift, root_drift_over_cycle_m=round(drift_len, 5),
        in_place_already=bool(drift_len < 0.02),
        stance=stance, foot_speeds_m_s={k: round(v, 4) for k, v in speeds.items()},
        clip_travels=bool(travels),
        speed_source="root travel" if travels else "stance foot",
        speed_from_root_m_s=round(sp_root, 4), speed_from_feet_m_s=round(sp_foot, 4),
        cycle_detected_by=cyc_why, cycle_selfsim_ratio=cyc_score,
        pose_motion=round(motion, 5), selfsim_curve=cyc_curve,
        clip_ground_speed_m_s=round(sp, 4),
        clip_stride_m=round(sp * period, 4),
    )
    if g["px_s"]:
        game_sp = g["px_s"] / CANVAS_PX_PER_M
        out["game"] = dict(
            px_s=g["px_s"], period_s=g["period"], frames=g["frames"],
            speed_m_s=round(game_sp, 4), stride_m=round(game_sp * g["period"], 4))
        out["verdict"] = dict(
            time_scale_to_game_cadence=round(period / g["period"], 4),
            speed_after_time_scale_m_s=round(sp * period / g["period"], 4),
            speed_ratio_game_over_clip=round(game_sp / sp, 4) if sp else None,
            residual_slide_if_timescaled=round(
                (game_sp - sp * period / g["period"]) / game_sp, 4) if sp else None,
            px_s_that_would_plant_the_feet=round(
                sp * period / g["period"] * CANVAS_PX_PER_M, 1) if sp else None)
        # ---- IS THE CYCLE STEADY? ------------------------------------------
        # A single speed for a whole clip assumes the clip holds one speed.
        # carry_run3 does not: it accelerates from 6.26 m/s, plateaus at 7.5,
        # then decelerates to a stop, so "the clip's speed" was whatever window
        # happened to be measured -- and the window this script measures is
        # frame 1, the acceleration ramp, the slowest usable part. Sweep every
        # candidate cycle window and report the spread, so a ramp cannot pass as
        # a cycle.
        #
        # Also report arc/chord per window: the earlier per-frame heading test
        # called this clip a 111-degree curve, which was noise from the frames
        # where it had nearly stopped. Arc over chord is immune to that.
        out["verdict"]["steady"] = steadiness(P[hips], cycle_frames, fps, g["period"], g["px_s"])
    # NOT height-normalised, and deliberately: the renderer does not rescale the
    # rig, it fixes px/m from camera.json, and this rig's BIND height is exactly
    # 1.800 m (bind_bbox_span z, identical in every render). The per-clip
    # character_height_m above is a POSE EXTREME -- top of head at full stride
    # extension minus the lowest sole, with the airborne rise folded in -- and
    # it reads 1.829 / 1.843 / 1.910 for one unchanged rig. It is not a scale
    # and must not be used as one.
    # resample times: N_out samples over exactly one cycle
    per = g["period"] or period
    nout = g["frames"] or int(round(period * 12))
    out["resample"] = dict(n=nout, period_s=round(per, 4),
                           frames=[round(f0 + cycle_frames * i / nout, 4)
                                   for i in range(nout)],
                           out_fps=round(nout / per, 4))
    json.dump(out, open(OUTP, "w"), indent=1)
    print("%-6s cycle %d frames (%.4f s)  speed %.3f m/s  stride %.3f m  drift %.4f m"
          % (NAME, cycle_frames, period, sp, sp * period, drift_len))
    if "verdict" in out:
        v = out["verdict"]
        print("       game wants %.3f m/s (stride %.3f m); time-scale x%.3f -> %.3f m/s, "
              "residual slide %.1f %%; feet would plant at %.0f px/s"
              % (out["game"]["speed_m_s"], out["game"]["stride_m"],
                 v["time_scale_to_game_cadence"], v["speed_after_time_scale_m_s"],
                 100 * v["residual_slide_if_timescaled"], v["px_s_that_would_plant_the_feet"]))
        st = v["steady"]
        print("  steady? %s  window speed %.3f..%.3f m/s (spread %.1f%%)  "
              "arc/chord max %.4f" % (
                  "YES" if st["steady"] else "NO", st["win_speed_min_m_s"],
                  st["win_speed_max_m_s"], 100 * st["spread"], st["arc_over_chord_max"]))
        print("  plants at %.1f..%.1f px/s across windows at the game's cadence, "
              "PLATEAU %.1f (target %.1f, +-10%% = %.1f..%.1f)" % (
                  st["px_s_min_at_game_cadence"], st["px_s_max_at_game_cadence"],
                  st["px_s_plateau_at_game_cadence"],
                  g["px_s"], 0.9 * g["px_s"], 1.1 * g["px_s"]))
        print("  period that would plant the PLATEAU stride exactly: %.4f s "
              "(game %.4f s), plateau stride %.3f m (game %.3f m)" % (
                  st["period_that_plants_plateau_s"], g["period"],
                  st["plateau_stride_m"], out["game"]["stride_m"]))
    print("wrote", OUTP)


main()
