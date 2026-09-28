#!/usr/bin/env python3
"""C-9 knight3d: render the CUT-OUT RIG's frames, so the M-b comparison has
the thing the 3D body is being compared against.

Read-only on cliffside_B. The rig is fully specified there --
scenes/knight_rig_E.tscn holds the Bone2D hierarchy, the Sprite2D parts with
their z-order, and the walk/run/idle animation tracks -- so this parses that
file and composites the same parts through the same transforms, rather than
screenshotting a running scene (another session is rebuilding cliffside_B for
the mist swap, and this must not touch it).

Output is the game's 512x512 frame with the sole on the same ground line the
Grok cells use, so all three columns of the M-b sheet are at one scale.
"""
import json, math, os, re, sys
import numpy as np
from PIL import Image

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
CB = os.path.join(ROOT, "cliffside_B")
K3 = os.path.join(ROOT, "knight3d")
OUT = os.path.join(K3, "out")
TSCN = os.path.join(CB, "scenes", "knight_rig_E.tscn")
FRAME = 512


def parse(path):
    txt = open(path).read()
    ext = dict(re.findall(r'\[ext_resource type="Texture2D" path="res://([^"]+)" id="([^"]+)"\]', txt))
    ext = {v: k for k, v in ext.items()}
    # --- animations ----------------------------------------------------
    anims = {}
    for m in re.finditer(r'\[sub_resource type="Animation" id="([^"]+)"\](.*?)(?=\n\[)', txt, re.S):
        body = m.group(2)
        name = re.search(r'resource_name = "([^"]+)"', body).group(1)
        length = float(re.search(r'length = ([\d.]+)', body).group(1))
        tracks = {}
        for t in re.finditer(r'tracks/(\d+)/path = NodePath\("([^"]+)"\)(.*?)(?=tracks/\d+/type|\Z)',
                             body, re.S):
            p = t.group(2)
            blk = t.group(3)
            tm = re.search(r'"times": PackedFloat32Array\(([^)]*)\)', blk)
            vm = re.search(r'"values": \[(.*?)\]\s*\}', blk, re.S)
            if not tm or not vm:
                continue
            times = [float(x) for x in tm.group(1).split(",") if x.strip()]
            raw = vm.group(1)
            if "Vector2" in raw:
                vals = [(float(a), float(b)) for a, b in
                        re.findall(r'Vector2\(([-\d.e]+),\s*([-\d.e]+)\)', raw)]
            else:
                vals = [float(x) for x in raw.split(",") if x.strip()]
            tracks[p] = (times, vals)
        anims[name] = dict(length=length, tracks=tracks)
    # --- nodes ----------------------------------------------------------
    nodes = {}
    order = []
    for m in re.finditer(r'\[node name="([^"]+)" type="([^"]+)"(?: parent="([^"]*)")?\](.*?)(?=\n\[node|\Z)',
                         txt, re.S):
        name, typ, parent, body = m.group(1), m.group(2), m.group(3), m.group(4)
        path = name if parent in (None, "") else (name if parent == "." else parent + "/" + name)
        def v2(key):
            mm = re.search(key + r' = Vector2\(([-\d.e]+),\s*([-\d.e]+)\)', body)
            return (float(mm.group(1)), float(mm.group(2))) if mm else None
        rot = re.search(r'\brotation = ([-\d.e]+)', body)
        z = re.search(r'z_index = (-?\d+)', body)
        tex = re.search(r'texture = ExtResource\("([^"]+)"\)', body)
        nodes[path] = dict(name=name, type=typ, parent=None if parent in (None, "", ".") else parent,
                           position=v2("position") or (0.0, 0.0),
                           scale=v2("scale") or (1.0, 1.0),
                           offset=v2("offset") or (0.0, 0.0),
                           rotation=float(rot.group(1)) if rot else 0.0,
                           z=int(z.group(1)) if z else 0,
                           texture=ext.get(tex.group(1)) if tex else None)
        order.append(path)
    return nodes, anims, order


def sample(track, t, length):
    times, vals = track
    if t <= times[0]:
        return vals[0]
    if t >= times[-1]:
        return vals[-1]
    i = np.searchsorted(times, t) - 1
    f = (t - times[i]) / max(times[i + 1] - times[i], 1e-9)
    a, b = vals[i], vals[i + 1]
    if isinstance(a, tuple):
        return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
    return a + (b - a) * f


def world(nodes, path, over):
    """2x3 affine of `path` in scene space (Godot: y down, rotation CW)."""
    M = np.eye(3)
    chain = []
    p = path
    while p is not None:
        chain.append(p)
        p = nodes[p]["parent"]
    for p in reversed(chain):
        n = nodes[p]
        pos = over.get(p + ":position", n["position"])
        rot = over.get(p + ":rotation", n["rotation"])
        sc = n["scale"]
        c, s = math.cos(rot), math.sin(rot)
        L = np.array([[c * sc[0], -s * sc[1], pos[0]],
                      [s * sc[0], c * sc[1], pos[1]],
                      [0, 0, 1.0]])
        M = M @ L
    return M


def render(state, frames, out_dir, sole_target):
    nodes, anims, order = parse(TSCN)
    anim = anims[state]
    sprites = [p for p in order if nodes[p]["type"] == "Sprite2D" and nodes[p]["texture"]]
    sprites.sort(key=lambda p: nodes[p]["z"])
    os.makedirs(out_dir, exist_ok=True)
    SS = 2
    made = []
    for i in range(frames):
        t = anim["length"] * i / frames
        over = {k: sample(v, t, anim["length"]) for k, v in anim["tracks"].items()}
        canvas = Image.new("RGBA", (FRAME * SS, FRAME * SS), (0, 0, 0, 0))
        for p in sprites:
            n = nodes[p]
            img = Image.open(os.path.join(CB, n["texture"])).convert("RGBA")
            M = world(nodes, p, over)
            w, h = img.size
            # Godot draws a Sprite2D centred on its node
            A = M @ np.array([[1, 0, -w / 2.0], [0, 1, -h / 2.0], [0, 0, 1]])
            A = np.array([[1, 0, FRAME / 2.0], [0, 1, sole_target], [0, 0, 1]]) @ A
            A = np.array([[SS, 0, 0], [0, SS, 0], [0, 0, 1]]) @ A
            inv = np.linalg.inv(A)
            layer = img.transform((FRAME * SS, FRAME * SS), Image.AFFINE,
                                  tuple(inv[:2].flatten()), resample=Image.BICUBIC)
            canvas.alpha_composite(layer)
        small = canvas.resize((FRAME, FRAME), Image.LANCZOS)
        made.append(np.asarray(small))
    # one shared vertical shift so the rig stands on the same ground line
    soles = [int(np.where((a[..., 3] > 8).any(axis=1))[0].max()) for a in made]
    dy = int(round(sole_target - float(np.mean(soles))))
    for i, a in enumerate(made):
        img = Image.fromarray(a)
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sh.paste(img, (0, dy))
        sh.save(os.path.join(out_dir, "rig_%s_E_%02d.png" % (state, i)))
    print("  rig %-4s %2d frames, sole %d->%d (shift %+d)"
          % (state, frames, int(np.mean(soles)), int(np.mean(soles)) + dy, dy))
    return dy


def main():
    r = json.load(open(os.path.join(OUT, "render_walk.json")))
    tgt = r["grok_sole_target"]
    rep = {"note": "Cut-out rig frames, reproduced from cliffside_B/scenes/"
                   "knight_rig_E.tscn (read-only) for the M-b comparison.",
           "sole_target": tgt, "shifts": {}}
    for state, n in (("walk", 12), ("run", 8)):
        rep["shifts"][state] = render(state, n, os.path.join(OUT, "rig", state), tgt)
    with open(os.path.join(OUT, "rig_frames.json"), "w") as f:
        json.dump(rep, f, indent=1)


if __name__ == "__main__":
    main()
