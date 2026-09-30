# T12_11: ONE TURN IN THE FIST before a strike's swing, not a flicker -- reshapes a STRIKES-mode
# weapon_r channel (attack_lab/t12/godot/tools/weapon_channel_solve.gd) for one clip.
#
#   python3 scripts/61_strike_ramp.py <solve.json> <clip> <t0> <t1> <out.json>
#
# The solver blends each key between the guard (held in his frame) and the edge-leading roll by the
# axe head's speed at that key (smoothstep, 15-35% of the clip's peak). On a wind-up whose speed dips
# and recovers (the slash re-cut on nbt_attack.glb's own keys: 22, 19, 16, 22, 32, 33, 25, 11, 38% of
# peak from 0.20 s to 0.50 s) the weight flips key to key, and the axe spins in the fist by up to 80
# deg between two 30 fps keys -- its butt then enters the heel of his hand (0.333 s, 0.48 s: 2.5-2.9 cm).
#
# Reshaped: up to t0 the axe is RIGID IN THE FIST at the clip's first key (the guard, so the fade-in
# from the locomotion guard still has nothing to turn); from t0 to t1 it makes ONE turn in the fist,
# a slerp to the solved key at t1 (the edge-leading roll at the swing's start), eased with smoothstep;
# from t1 on, the solved keys unchanged (the swing's edge lead; after the swing the recovery release
# owns weapon_r). Output: the 54_weapon_channel.py `channel` format, the one clip.
import json, math, sys
import numpy as np


def slerp(a, b, u):
    a = np.asarray(a, float); b = np.asarray(b, float)
    d = float(np.dot(a, b))
    if d < 0:
        b = -b; d = -d
    if d > 0.9995:
        q = a + u * (b - a)
        return q / np.linalg.norm(q)
    th = math.acos(d)
    return (math.sin((1 - u) * th) * a + math.sin(u * th) * b) / math.sin(th)


def ang(a, b):
    return math.degrees(2 * math.acos(min(1.0, abs(float(np.dot(a, b))))))


if __name__ == "__main__":
    src, clip, t0, t1, dst = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    d = json.load(open(src))
    c = d["weapon_r"][clip]
    ts = [float(t) for t in c["times"]]
    qs = [np.array(q, float) / np.linalg.norm(q) for q in c["quats"]]
    i1 = min(range(len(ts)), key=lambda i: abs(ts[i] - t1))
    q0, qt1 = qs[0], qs[i1]
    out_q, rows = [], []
    for t, q in zip(ts, qs):
        if t <= t0:
            n = q0
        elif t < ts[i1]:
            u = (t - t0) / (ts[i1] - t0)
            n = slerp(q0, qt1, u * u * (3 - 2 * u))
        else:
            n = q
        out_q.append(n)
    for i in range(1, len(out_q)):
        if np.dot(out_q[i], out_q[i - 1]) < 0:
            out_q[i] = -out_q[i]
    step_old = [ang(qs[i], qs[i - 1]) for i in range(1, len(qs)) if ts[i] <= ts[i1]]
    step_new = [ang(out_q[i], out_q[i - 1]) for i in range(1, len(out_q)) if ts[i] <= ts[i1]]
    rep = dict(clip=clip, t0=t0, t1=ts[i1], keys=len(ts), turn_total_deg=round(ang(q0, qt1), 1),
               max_key_step_before_swing_deg=dict(solved=round(max(step_old), 1), reshaped=round(max(step_new), 1)))
    json.dump({"weapon_r": {clip: {"times": ts, "quats": [list(map(float, q)) for q in out_q]}},
               "_ramp": rep, "_from": src}, open(dst, "w"), indent=1)
    print(json.dumps(rep))
