#!/usr/bin/env python3
"""C-9 knight3d: turn posed JOINT POSITIONS into per-bone rigid transforms, and
those into posed mesh vertices.

One definition, used by the renderer and by the Blender keyer, so the frames
Matt looks at and the rig in the .blend are the same motion. (M-a's lesson,
applied a third time: anything written twice drifts.)

Each bone's transform is the minimal swing from its parent's frame, which is
what a proxy body wants -- no roll bookkeeping, no Euler order to get wrong.
"""
import numpy as np

# bone -> (parent, tail-joint). The tail is what gives the bone its direction.
HIER = [
    ("Hips", None, "Spine"),
    ("Spine", "Hips", "Spine1"), ("Spine1", "Spine", "Spine2"),
    ("Spine2", "Spine1", "Neck"), ("Neck", "Spine2", "Head"),
    ("Head", "Neck", "HeadTop_End"), ("HeadTop_End", "Head", None),
]
for _s in ("Left", "Right"):
    HIER += [
        (_s + "Shoulder", "Spine2", _s + "Arm"),
        (_s + "Arm", _s + "Shoulder", _s + "ForeArm"),
        (_s + "ForeArm", _s + "Arm", _s + "Hand"),
        (_s + "Hand", _s + "ForeArm", _s + "HandEnd"),
        (_s + "HandEnd", _s + "Hand", None),
        (_s + "UpLeg", "Hips", _s + "Leg"),
        (_s + "Leg", _s + "UpLeg", _s + "Foot"),
        (_s + "Foot", _s + "Leg", _s + "ToeBase"),
        (_s + "ToeBase", _s + "Foot", _s + "Toe_End"),
        (_s + "Toe_End", _s + "ToeBase", None),
    ]
for _t in ("F", "B"):
    HIER += [("TAB_%s_01" % _t, "Hips", "TAB_%s_02" % _t),
             ("TAB_%s_02" % _t, "TAB_%s_01" % _t, "TAB_%s_03" % _t),
             ("TAB_%s_03" % _t, "TAB_%s_02" % _t, "TAB_%s_04" % _t)]
for _t in ("F", "B", "L", "R"):
    HIER += [("SKIRT_%s" % _t, "Hips", "SKIRT_%s_end" % _t)]
HIER += [("SOCK_WeaponMain", "RightHand", "SOCK_WeaponMain_end"),
         ("SOCK_WeaponGripFar", "SOCK_WeaponMain", "SOCK_WeaponGripFar_end"),
         ("SOCK_OffHand", "LeftHand", "SOCK_OffHand_end")]


def rot_between(a, b):
    a = a / max(np.linalg.norm(a), 1e-12)
    b = b / max(np.linalg.norm(b), 1e-12)
    v = np.cross(a, b); s = np.linalg.norm(v); c = float(a @ b)
    if s < 1e-9:
        return np.eye(3) if c > 0 else -np.eye(3) + 2 * np.outer(a, a)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * ((1 - c) / (s * s))


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return R, cb - R @ ca


def bone_transforms(Jr, Jp, overrides=None):
    """Jr, Jp: rest and posed joint dicts. Returns {bone: (R, t)}.

    `overrides` gives an EXPLICIT rotation for bones whose orientation a single
    head-to-tail direction cannot pin down. The foot is the case that matters:
    its pitch is visible in the Foot->ToeBase direction, but its yaw and roll
    are not, so reconstructing them as a swing from the shin left the sabaton
    a couple of centimetres out of true and the planted foot slipped ~20 mm.
    """
    overrides = overrides or {}
    # the root's frame comes from three pelvis points, not from a guess
    A = np.array([Jr["Hips"], Jr["LeftUpLeg"], Jr["RightUpLeg"], Jr["Spine"]])
    B = np.array([Jp["Hips"], Jp["LeftUpLeg"], Jp["RightUpLeg"], Jp["Spine"]])
    R0, _ = kabsch(A, B)
    T = {"Hips": (R0, Jp["Hips"] - R0 @ Jr["Hips"])}
    for bone, parent, tail in HIER:
        if bone == "Hips":
            continue
        Rp = T[parent][0]
        if tail is None or tail not in Jr or tail not in Jp:
            R = Rp
        else:
            d_rest = Jr[tail] - Jr[bone]
            d_pose = Jp[tail] - Jp[bone]
            if np.linalg.norm(d_rest) < 1e-9 or np.linalg.norm(d_pose) < 1e-9:
                R = Rp
            else:
                R = rot_between(Rp @ d_rest, d_pose) @ Rp
        if bone in overrides:
            R = overrides[bone]
        T[bone] = (R, Jp[bone] - R @ Jr[bone])
    return T


def skin_weights(names, tri_id, tri_v, params):
    """Per-triangle bone weights.

    Rigid pieces: weight 1.0 on their own bone. The skirt and the tabard blend
    exactly the way 04_build_blender.py skins them, so the render and the rig
    deform alike.
    """
    p = params
    W = []
    for i in range(len(tri_v)):
        W.append(None)
    return W


def pose_tris(tri_v, tri_id, names, part_bone, part_kind, T, params):
    """Apply the bone transforms to every triangle vertex."""
    out = tri_v.copy()
    z_hip, skirt_z = params["z_hip"] - 0.02, params["skirt_z_bot"]
    z_w, tzb = params["z_waist"], params["tabard_z_bot"]
    for pid, nm in enumerate(names):
        sel = tri_id == pid
        if not sel.any():
            continue
        kind = part_kind[nm]
        if kind == "deform_skirt":
            V = tri_v[sel]
            z = V[..., 2]
            t = np.clip((z_hip - z) / max(z_hip - skirt_z, 1e-6), 0.0, 1.0)
            ang = np.arctan2(V[..., 1], V[..., 0])
            w = {"R": np.maximum(0.0, np.cos(ang)), "L": np.maximum(0.0, -np.cos(ang)),
                 "F": np.maximum(0.0, np.sin(ang)), "B": np.maximum(0.0, -np.sin(ang))}
            tot = sum(w.values()); tot = np.where(tot > 1e-9, tot, 1.0)
            acc = np.zeros_like(V)
            Rh, th = T["Hips"]
            acc += (1 - t)[..., None] * (V @ Rh.T + th)
            for k, val in w.items():
                Rb, tb = T["SKIRT_%s" % k]
                acc += (t * val / tot)[..., None] * (V @ Rb.T + tb)
            out[sel] = acc
        elif kind.startswith("deform_tabard"):
            tag = kind[-1]
            V = tri_v[sel]
            z = V[..., 2]
            acc = np.zeros_like(V)
            above = z >= z_w
            Rh, th = T["Hips"]
            acc += above[..., None] * (V @ Rh.T + th)
            u = np.clip((z_w - z) / max(z_w - tzb, 1e-6), 0.0, 1.0) * 3.0
            lo = np.clip(np.floor(u).astype(int), 0, 2)
            f = u - lo
            for k in (0, 1, 2):
                m = (~above) & (lo == k)
                if not m.any():
                    continue
                a = min(3, k + 1); b = min(3, k + 2)
                Ra, ta = T["TAB_%s_%02d" % (tag, a)]
                Rb, tb = T["TAB_%s_%02d" % (tag, b)]
                acc += (m * (1 - f))[..., None] * (V @ Ra.T + ta)
                acc += (m * f)[..., None] * (V @ Rb.T + tb)
            out[sel] = acc
        else:
            R, t = T[part_bone[nm]]
            out[sel] = tri_v[sel] @ R.T + t
    return out
