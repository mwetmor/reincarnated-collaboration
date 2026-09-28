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
#  * SPEED FROM THE FEET. These clips arrive in place, so the ground speed is
#    not in the root at all: it is in the stance foot, which slides backward
#    under the body at exactly the travel speed. Measured there.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, NAME, OUTP = a[0], a[1], a[2]

# the game's cadence, from knight_fit.json / knight_foot_slide.json
CANVAS_PX_PER_M = 150.21354166666666 / 1.80          # 83.452
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

    # ---- is the last frame a duplicate of the first? (a looping clip usually
    #      repeats it, and counting it would stretch the cycle by one frame)
    d_loop = float(np.mean([np.linalg.norm(P[b][-1] - P[b][0]) for b in bones]))
    d_step = float(np.mean([np.linalg.norm(P[b][1] - P[b][0]) for b in bones]))
    dup = d_loop < 0.4 * d_step
    cycle_frames = (N - 1) if dup else N
    period = cycle_frames / fps

    # ---- root drift: fit and remove the LINEAR horizontal component
    hips = R.get("hips", bones[0])
    t = np.arange(N)
    drift = {}
    for k, ax in ((0, "x"), (1, "y")):
        m, c = np.polyfit(t, P[hips][:, k], 1)
        drift[ax] = dict(per_frame=float(m), over_cycle=float(m * cycle_frames))
    drift_len = math.hypot(drift["x"]["over_cycle"], drift["y"]["over_cycle"])

    # ---- ground speed from the stance foot
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
    sp = float(np.median(list(speeds.values()))) if speeds else 0.0

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
    print("wrote", OUTP)


main()
