# GODOT'S BLEND, the rule the JOIN renderer's pixels come from -- one implementation for j_measure.py and
# j_weapon_clamp.py (and anything else that must see the pose the pack shows).
#
# render_cells.gd poses the body with an AnimationTree: the state's clip, then one FILTERED Blend2 per layer, bottom to
# top. Blend2 at amount w gives its input 0 (everything below) weight 1 - w and its input 1 (the layer) weight w on the
# filtered bones, so on a bone every layer covers, the clip ends at prod(1 - w_i) and layer k at w_k prod_{j>k}(1 - w_j).
# Godot 4's AnimationMixer then accumulates EACH contribution, in processing order (the clip first, then the layers
# bottom to top), RELATIVE TO THE BONE'S REST (init):
#     rot  = init . prod_k  Quaternion().slerp(init^-1 . q_k, w_k)        (normalized after every step)
#     loc  = init + sum_k w_k (loc_k - init)          scale likewise
# That is NOT slerp(clip, layer, w). At w = 0 or 1 the two agree exactly; in between they differ, by as much as the two
# poses are far from rest -- the JOIN pack found it: the death's guards blending out and the shout's raise blending in
# measured 5.9 cm and 9.1 cm from the renderer's own sockets under slerp, 0.02 mm under this rule.
# A bone a layer's action does not key sits at rest in that action (the glTF rule), so it contributes the identity.
import math
import numpy as np

I4 = np.array([0.0, 0.0, 0.0, 1.0])


def qmul(a, b):                                                         # Hamilton product, glTF / Godot order x y z w
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return np.array([aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz])


def qinv(q):
    q = np.asarray(q, float); return np.array([-q[0], -q[1], -q[2], q[3]]) / float(np.dot(q, q))


def qpow(q, a):                                                         # Quaternion().slerp(q, a), Godot's shortest path
    q = np.asarray(q, float); c = float(q[3])
    if c < 0.0:
        q = -q; c = -c
    if 1.0 - c > 1e-5:
        om = math.acos(min(1.0, c)); so = math.sin(om)
        s0 = math.sin((1.0 - a) * om) / so; s1 = math.sin(a * om) / so
    else:
        s0, s1 = 1.0 - a, a
    return s0 * I4 + s1 * q


def slerp(a, b, u):                                                     # Quaternion::slerp: a key-to-key rotation (glTF LINEAR)
    a = np.asarray(a, float); b = np.asarray(b, float); c = float(np.dot(a, b))
    if c < 0.0:
        b = -b; c = -c
    if 1.0 - c > 1e-5:
        om = math.acos(min(1.0, c)); so = math.sin(om)
        v = (math.sin((1.0 - u) * om) / so) * a + (math.sin(u * om) / so) * b
    else:
        v = (1.0 - u) * a + u * b
    return v / np.linalg.norm(v)


def mix(rest, contribs):
    """rest = (loc, rot, scale) of the bone; contribs = [((loc, rot, scale), weight), ...] in processing order."""
    t0, q0, s0 = [np.asarray(x, float) for x in rest]
    rot = q0 / np.linalg.norm(q0); qi = qinv(rot); tr = t0.copy(); sc = s0.copy()
    for (t, q, s), w in contribs:
        if w <= 0.0:
            continue
        q = np.asarray(q, float); q = q / np.linalg.norm(q)
        rot = qmul(rot, qpow(qmul(qi, q), w)); rot = rot / np.linalg.norm(rot)
        tr = tr + (np.asarray(t, float) - t0) * w; sc = sc + (np.asarray(s, float) - s0) * w
    return [tr, rot, sc]


def blend(rest_of, base, layers):
    """rest_of(i) -> (loc, rot, scale); base = {bone index: [loc, rot, scale]} (the clip at t, rest where un-keyed);
    layers = [(set of bone indices, weight, {bone index: [loc, rot, scale]}), ...] bottom to top.
    Returns the locals Godot's mixer produces. A bone no layer covers keeps the clip's value exactly."""
    out = dict(base)
    covered = set()
    for b_, w_, _ in layers:
        if w_ > 0.0:
            covered |= set(b_)
    for i in covered:
        ws = [(base[i], 1.0)]
        for b_, w_, pl in layers:
            if i in b_ and w_ > 0.0:
                ws = [(v, a * (1.0 - w_)) for v, a in ws] + [(pl[i], w_)]
        out[i] = mix(rest_of(i), ws)
    return out
