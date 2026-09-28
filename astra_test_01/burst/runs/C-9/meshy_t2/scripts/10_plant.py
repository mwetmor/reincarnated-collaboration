# C-9 meshy_t2 step 8: the plant instrument, and the natural ground speed.
#
#   blender -b -noaudio --python scripts/10_plant.py -- <clips.blend> <out.json>
#
# This re-derives the speed FROM THE POSED SKELETON, exactly the way
# meshy_t1's 03_clips.py derives it for a Meshy library clip -- it does not
# read back the numbers 07_clips.py authored. That matters: the authored
# target and the solved pose are different things, and the whole point of the
# assert is to catch the gap between them.
#
# The clips are IN PLACE, so the ground runs backwards past the animal at the
# gait speed. A planted toe therefore has to travel backwards at exactly that
# speed, and the slide is the difference. Measured on the TOE (the tail of the
# paw bone), which is this digitigrade creature's actual contact.
#
# Contact is detected by height, not by the authored `planted` flag: a foot is
# down when its toe is within CONTACT_BAND of the clip's own minimum toe
# height for that foot. Using the flag would only tell me whether the code
# agrees with itself.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("10_plant.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTP = a[0], a[1]
# The band is swept, not picked. At 20 mm the gallop's hind right reported
# 41.6 mm of slide on a foot whose two unambiguous contact frames slide
# 2.6 mm -- the third "contact" frame was the descent into touchdown, which
# with 8 frames at duty 0.27 falls between samples. A slide figure that moves
# with the detection threshold is a figure about the threshold, so all three
# are reported and the tightest is the one quoted.
BANDS = [0.006, 0.012, 0.020]
FEET = ["fpaw.L", "fpaw.R", "hpaw.L", "hpaw.R"]
CONTACT_BAND = 0.006            # m above the foot's own lowest point
# 20 mm and 12 mm both caught the DESCENT INTO TOUCHDOWN on the gallop's hind
# right -- a third "contact" frame whose step spans the landing -- and read
# 41.6 mm of slide on a foot whose unambiguous contact frames slide 2.6 mm.
# With 8 frames at duty 0.27 the touchdown falls between samples, so the band
# has to be tighter than the descent's last step, not merely small.

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
clips = json.load(open(os.path.join(os.path.dirname(BLEND), "clips.json")))
rep = dict(contact_band_m=CONTACT_BAND, bands_m=BANDS, clips={})

for state in ("idle", "walk", "run", "attack"):
    act = bpy.data.actions.get("mc_" + state)
    arm.animation_data_create()
    arm.animation_data.action = act
    try:
        sl = list(act.slots)
        if sl:
            arm.animation_data.action_slot = sl[0]
    except Exception:
        pass
    info = clips[state]
    n, T_ = info["frames"], info["period_s"]
    dt = T_ / n
    P = {f: [] for f in FEET}
    hips = []
    for i in range(n):
        sc.frame_set(i + 1)
        for f in FEET:
            P[f].append(np.array(arm.matrix_world @ arm.pose.bones[f].tail))
        hips.append(np.array(arm.matrix_world @ arm.pose.bones["hips"].head))
    P = {f: np.array(v) for f, v in P.items()}
    hips = np.array(hips)

    band_slide = {}
    for bnd in BANDS:
        worst = 0.0
        for f in FEET:
            z = P[f][:, 2]
            dn = z < z.min() + bnd
            ii = np.where(dn)[0]
            if len(ii) < 2:
                continue
            rr, cu = [], [int(ii[0])]
            for j in ii[1:]:
                if j == cu[-1] + 1:
                    cu.append(int(j))
                else:
                    rr.append(cu); cu = [int(j)]
            rr.append(cu)
            if info["cycle"] and len(rr) > 1 and rr[0][0] == 0 and rr[-1][-1] == n - 1:
                rr[0] = rr[-1] + [k + n for k in rr[0]]; rr.pop()
            bb = max(rr, key=len)
            for k in range(1, len(bb)):
                dv = (P[f][bb[k] % n] - P[f][bb[k - 1] % n]) / dt
                worst = max(worst, float(abs(-dv[1] - info["speed_m_s"])) * dt)
        band_slide[str(bnd)] = round(worst, 5)

    feet = {}
    speeds = []
    for f in FEET:
        z = P[f][:, 2]
        down = z < z.min() + CONTACT_BAND
        # the longest contiguous run, wrapping if the clip is a cycle
        idx = np.where(down)[0]
        runs = []
        if len(idx):
            cur = [int(idx[0])]
            for j in idx[1:]:
                if j == cur[-1] + 1:
                    cur.append(int(j))
                else:
                    runs.append(cur); cur = [int(j)]
            runs.append(cur)
            if info["cycle"] and len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == n - 1:
                runs[0] = runs[-1] + [k + n for k in runs[0]]
                runs.pop()
        best = max(runs, key=len) if runs else []
        row = dict(contact_frames=len(best), duty=round(len(best) / n, 3),
                   frames=[k % n for k in best])
        if len(best) >= 2:
            steps = []
            for k in range(1, len(best)):
                p0 = P[f][best[k - 1] % n]; p1 = P[f][best[k] % n]
                steps.append((p1 - p0) / dt)
            steps = np.array(steps)
            back = -steps[:, 1]                       # backward is -Y
            row.update(
                back_speed_mean_m_s=round(float(back.mean()), 4),
                back_speed_min_m_s=round(float(back.min()), 4),
                back_speed_max_m_s=round(float(back.max()), 4),
                lateral_speed_max_m_s=round(float(np.abs(steps[:, 0]).max()), 4),
                vertical_speed_max_m_s=round(float(np.abs(steps[:, 2]).max()), 4),
                contact_travel_m=round(float(
                    np.linalg.norm(P[f][best[-1] % n][:2] - P[f][best[0] % n][:2])), 4))
            if info["speed_m_s"] > 0:
                speeds.append(float(back.mean()))
        feet[f] = row

    v_auth = info["speed_m_s"]
    v_meas = float(np.median(speeds)) if speeds else 0.0
    slide = {}
    for f, row in feet.items():
        if "back_speed_mean_m_s" not in row:
            continue
        if v_auth > 0:
            per = [abs(row["back_speed_%s_m_s" % k] - v_auth) for k in ("min", "max")]
            row["slide_max_m_per_frame"] = round(max(per) * dt, 5)
            row["slide_max_pct_of_stride"] = round(
                100.0 * max(per) * dt / (v_auth * T_), 3)
        else:
            row["slide_max_m_per_frame"] = round(
                max(abs(row["back_speed_min_m_s"]), abs(row["back_speed_max_m_s"])) * dt, 5)
            row["slide_max_pct_of_stride"] = None
        slide[f] = row["slide_max_m_per_frame"]

    rep["clips"][state] = dict(
        frames=n, period_s=T_, fps=round(n / T_, 3),
        authored_speed_m_s=v_auth,
        measured_speed_m_s=round(v_meas, 4),
        speed_error_pct=(round(100 * (v_meas - v_auth) / v_auth, 3) if v_auth else None),
        stride_m=round(v_meas * T_, 4) if v_meas else 0.0,
        stride_over_withers=round(v_meas * T_ / T.TARGET_WITHERS_M, 3) if v_meas else 0.0,
        froude=round(v_meas ** 2 / (9.81 * T.TARGET_WITHERS_M), 3) if v_meas else 0.0,
        canvas_px_s=round(v_meas * T.PX_PER_M, 1) if v_meas else 0.0,
        max_slide_m=round(max(slide.values()), 5) if slide else 0.0,
        max_slide_by_band_m=band_slide,
        feet=feet,
        hips_bob_m=round(float(hips[:, 2].max() - hips[:, 2].min()), 4),
        root_motion=dict(
            in_place=True,
            per_frame_forward_m=round(v_auth * dt, 5),
            per_cycle_forward_m=round(v_auth * T_, 5),
            note="the clip is in place; the game advances the sprite by "
                 "per_frame_forward_m each frame"))
    r = rep["clips"][state]
    print("%-7s %d fr @ %.2f fps  authored %.2f m/s  MEASURED %.3f m/s (%s)  "
          "stride %.3f m (%.2f x withers, Fr %.2f)  max slide %.1f mm  "
          "bob %.0f mm  %.0f px/s   slide by band %s"
          % (state, n, r["fps"], v_auth, v_meas,
             ("%+.2f %%" % r["speed_error_pct"]) if r["speed_error_pct"] is not None else "-",
             r["stride_m"], r["stride_over_withers"], r["froude"],
             1000 * r["max_slide_m"], 1000 * r["hips_bob_m"], r["canvas_px_s"],
             {k: round(1000 * v, 1) for k, v in band_slide.items()}))
    for f, row in feet.items():
        print("        %-7s contact %d/%d (duty %.2f)  back %.3f m/s [%.3f..%.3f]  "
              "lateral %.3f  slide %.1f mm"
              % (f, row["contact_frames"], n, row["duty"],
                 row.get("back_speed_mean_m_s", 0), row.get("back_speed_min_m_s", 0),
                 row.get("back_speed_max_m_s", 0), row.get("lateral_speed_max_m_s", 0),
                 1000 * row.get("slide_max_m_per_frame", 0)))

json.dump(rep, open(OUTP, "w"), indent=1)
print("wrote", OUTP)
