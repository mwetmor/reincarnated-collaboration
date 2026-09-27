#!/usr/bin/env python3
"""C-9 R-C9-40: rasterise scenes/knight_rig_E.tscn OFF-LINE, and probe its JOINTS.

WHY THIS EXISTS.  Matt's report was "the legs detach at the thigh from the body and
move as ghosts".  That is a statement about PIXELS -- a hole opening in the figure's
silhouette at the hip -- and no bone-space number answers it.  probe_rig.gd measures
the rig's bones inside Godot and is the authority on foot slide and registration; it
cannot see a hole, because a hole is what the drawn sprites fail to cover.

So this reads the SHIPPED SCENE FILE (not the builder's intermediate state: if the
.tscn and the builder ever disagree, the .tscn is what Godot draws and therefore what
Matt saw), rebuilds the Skeleton2D transform chain, composites the part PNGs in their
z order, and reports for every frame of every clip:

    hip_gap_px        the largest run of TRANSPARENT pixels, in a column, between the
                      torso's lower edge and the top of a thigh -- the number Matt's
                      complaint is about.  Must be 0.
    ankle_gap_px      the same at the shin/sabaton seam, which heel-toe opens.
    knee_gap_px       the same at the poleyn.
    holes             enclosed background inside the figure in those bands.

It is a SECOND implementation of Godot's 2D transform composition, so it is checked
against a Godot render once per change (tools/check_render_vs_godot.py) rather than
trusted on its own.

    python3 tools/render_rig_E.py --probe            numbers only
    python3 tools/render_rig_E.py --frames DIR --clip walk --n 48 --zoom 3
"""
import argparse
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
TSCN = PROJ / "scenes" / "knight_rig_E.tscn"

BODY_PARTS = ["head", "torso", "skirt_back", "skirt_front", "arm_near_lo",
              "arm_far_lo", "hand_far"]


# ---------------------------------------------------------------------------
def parse_tscn(path):
    """Read the generated scene: ext resources, animations, bone tree, sprites."""
    text = path.read_text()
    ext = {}
    for m in re.finditer(r'\[ext_resource type="Texture2D" path="res://([^"]+)" id="([^"]+)"\]', text):
        ext[m.group(2)] = m.group(1)

    anims = {}
    for block in re.split(r"\n(?=\[)", text):
        if not block.startswith('[sub_resource type="Animation"'):
            continue
        name = re.search(r'resource_name = "([^"]+)"', block).group(1)
        length = float(re.search(r"length = ([-0-9.e]+)", block).group(1))
        tracks = {}
        for tm in re.finditer(
                r'tracks/(\d+)/path = NodePath\("([^"]+)"\)(.*?)"values": \[(.*?)\]\n\}',
                block, re.S):
            npath, body, vals = tm.group(2), tm.group(3), tm.group(4)
            times = [float(v) for v in
                     re.search(r'"times": PackedFloat32Array\((.*?)\)', body).group(1).split(",")]
            node, prop = npath.split(":")
            if prop == "position":
                vv = [(float(a), float(b)) for a, b in
                      re.findall(r"Vector2\(([-0-9.e]+), ([-0-9.e]+)\)", vals)]
            else:
                vv = [float(v) for v in vals.split(",")]
            tracks[(node, prop)] = (times, vv)
        anims[name] = {"length": length, "tracks": tracks}

    nodes = []
    for block in re.split(r"\n(?=\[node )", text):
        m = re.match(r'\[node name="([^"]+)" type="([^"]+)" parent="([^"]*)"\]', block)
        if not m:
            continue
        n = {"name": m.group(1), "type": m.group(2), "parent": m.group(3),
             "pos": (0.0, 0.0), "scale": (1.0, 1.0), "z": 0, "tex": None}
        p = re.search(r"\nposition = Vector2\(([-0-9.e]+), ([-0-9.e]+)\)", block)
        if p:
            n["pos"] = (float(p.group(1)), float(p.group(2)))
        s = re.search(r"\nscale = Vector2\(([-0-9.e]+), ([-0-9.e]+)\)", block)
        if s:
            n["scale"] = (float(s.group(1)), float(s.group(2)))
        z = re.search(r"\nz_index = ([-0-9]+)", block)
        if z:
            n["z"] = int(z.group(1))
        t = re.search(r'\ntexture = ExtResource\("([^"]+)"\)', block)
        if t:
            n["tex"] = ext[t.group(1)]
        nodes.append(n)
    return anims, nodes


def sample(track, t, length):
    """Godot linear value track with loop_wrap; the clips key both endpoints."""
    times, vals = track
    if t <= times[0]:
        return vals[0]
    for i in range(1, len(times)):
        if t <= times[i]:
            f = (t - times[i - 1]) / max(times[i] - times[i - 1], 1e-9)
            a, b = vals[i - 1], vals[i]
            if isinstance(a, tuple):
                return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            return a + (b - a) * f
    return vals[-1]


def xform(pos, rot, sc):
    c, s = math.cos(rot), math.sin(rot)
    return np.array([[c * sc[0], -s * sc[1], pos[0]],
                     [s * sc[0], c * sc[1], pos[1]],
                     [0.0, 0.0, 1.0]])


class Rig:
    def __init__(self, tscn=TSCN):
        self.anims, self.nodes = parse_tscn(tscn)
        self.tex = {}
        self.by_path = {}
        for n in self.nodes:
            path = n["name"] if not n["parent"] or n["parent"] == "." \
                else n["parent"] + "/" + n["name"]
            n["path"] = path
            self.by_path[path] = n
            if n["tex"]:
                im = Image.open(PROJ / n["tex"]).convert("RGBA")
                self.tex[n["path"]] = np.asarray(im).astype(np.float32) / 255.0
        self.sprites = sorted([n for n in self.nodes if n["type"] == "Sprite2D"],
                              key=lambda n: n["z"])

    def pose(self, clip, t):
        """World (rig-local) 3x3 transform per node path."""
        a = self.anims[clip]
        out = {}
        for n in self.nodes:
            par = n["parent"]
            base = out.get(par, np.eye(3)) if par not in ("", ".") else np.eye(3)
            key = n["path"].replace("Skel/", "Skel/") if False else n["path"]
            # animation node paths are relative to the scene root: "Skel/hip/leg_n_th"
            rot = a["tracks"].get((key, "rotation"))
            pos = a["tracks"].get((key, "position"))
            r = sample(rot, t, a["length"]) if rot else 0.0
            p = sample(pos, t, a["length"]) if pos else n["pos"]
            out[n["path"]] = base @ xform(p, r, n["scale"])
        return out

    def render(self, clip, t, zoom=3.0, size=(360, 460), origin=(180, 430)):
        """Composite.  Returns (rgba float canvas, {part: alpha mask})."""
        W, H = size
        canvas = np.zeros((H, W, 4), np.float32)
        masks = {}
        poses = self.pose(clip, t)
        for n in self.sprites:
            tex = self.tex[n["path"]]
            th, tw = tex.shape[:2]
            M = poses[n["path"]]
            # texture px -> rig px: centred sprite
            T = M @ np.array([[1, 0, -tw / 2.0], [0, 1, -th / 2.0], [0, 0, 1]])
            # rig px -> canvas px
            C = np.array([[zoom, 0, origin[0]], [0, zoom, origin[1]], [0, 0, 1]])
            F = C @ T
            inv = np.linalg.inv(F)
            ys, xs = np.mgrid[0:H, 0:W]
            src = inv @ np.stack([xs.ravel() + 0.5, ys.ravel() + 0.5,
                                  np.ones(xs.size)])
            sx, sy = src[0].reshape(H, W), src[1].reshape(H, W)
            layer = np.zeros((H, W, 4), np.float32)
            inb = (sx >= 0) & (sx < tw) & (sy >= 0) & (sy < th)
            ix = np.clip(sx.astype(np.int32), 0, tw - 1)
            iy = np.clip(sy.astype(np.int32), 0, th - 1)
            layer[inb] = tex[iy[inb], ix[inb]]
            name = n["name"][2:] if n["name"].startswith("S_") else n["name"]
            masks[name] = layer[..., 3] > 0.5
            a = layer[..., 3:4]
            canvas[..., :3] = layer[..., :3] * a + canvas[..., :3] * (1 - a)
            canvas[..., 3:4] = a + canvas[..., 3:4] * (1 - a)
        return canvas, masks


# ---------------------------------------------------------------------------
def column_gap(front_mask, back_mask, gapmask):
    """Largest run of GAP pixels in a column between the bottom of `front_mask` and
    the top of `back_mask`.  `gapmask` is the ENCLOSED-hole mask, not raw
    transparency -- the first version of this used raw transparency and reported 62
    rig px at the knee, which was a true reading of the OPEN notch inside a bent
    knee and the wrong answer to 'has the limb come away from the body'.  A
    detachment is a HOLE: background surrounded by figure.  An open notch is anatomy.
    """
    worst, where = 0, None
    H, W = gapmask.shape
    for x in range(W):
        bk = np.nonzero(back_mask[:, x])[0]
        if len(bk) == 0:
            continue
        top = bk[0]
        fr = np.nonzero(front_mask[:top, x])[0]
        if len(fr) == 0:
            continue
        bot = fr[-1]
        if top - bot <= 1:
            continue
        seg = gapmask[bot + 1:top, x]
        run = best = 0
        for v in seg:
            run = run + 1 if v else 0
            best = max(best, run)
        if best > worst:
            worst, where = best, (int(x), int(bot), int(top))
    return worst, where


def hole_mask(alpha):
    """Transparent pixels not reachable from the canvas border: enclosed background."""
    bg = ~alpha
    lab, _ = ndimage.label(bg)
    border = set(lab[0].tolist()) | set(lab[-1].tolist()) | \
        set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    border.discard(0)
    return bg & ~np.isin(lab, list(border))


def holes_near(holes, centre, radius):
    """Enclosed-hole pixels within `radius` of a joint's CURRENT position, and the
    largest such hole's vertical extent."""
    H, W = holes.shape
    yy, xx = np.mgrid[0:H, 0:W]
    near = holes & (((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) <= radius * radius)
    n = int(near.sum())
    ext = 0
    if n:
        lab, k = ndimage.label(near)
        for i in range(1, k + 1):
            ys = np.nonzero((lab == i).any(1))[0]
            ext = max(ext, int(ys.max() - ys.min() + 1))
    return n, ext


SPR = "Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft/S_leg_%s_foot"
# The limb axes.  Each is (name, bone whose origin starts it, bone whose origin ends it).
LIMB_AXES = [
    ("thigh_%s", "Skel/hip", "Skel/hip/leg_%s_th/leg_%s_sh"),
    ("shin_%s", "Skel/hip/leg_%s_th/leg_%s_sh", "Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft"),
    ("foot_%s", "Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft", None),
]
AXIS_OFFSETS = (-2.0, 0.0, 2.0)      # rig px, perpendicular to the limb


def limb_axes(rig, poses, side):
    """World endpoints of each limb segment, for the near ('n') or far ('f') leg."""
    tag = side

    def P(path):
        return np.array([poses[path][0, 2], poses[path][1, 2]])
    hip = P("Skel/hip")
    knee = P("Skel/hip/leg_%s_th/leg_%s_sh" % (tag, tag))
    ankle = P("Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft" % (tag, tag, tag))
    foot = P(SPR % (tag, tag, tag, "near" if tag == "n" else "far"))
    if tag == "f":
        # the far leg hangs off its own socket, not the near one
        hip = P("Skel/hip/leg_f_th")
    return [("thigh", hip + np.array([0.0, -6.0]), knee),
            ("shin", knee, ankle),
            ("foot", ankle, foot)]


def joint_gap(alpha, joint, u, zoom, origin, R=9.0, half_w=4.0, want_pts=False):
    """Largest BOUNDED transparent run across a joint, in rig px.

    Scan lines parallel to the limb's own axis, through a disc of radius R about the
    joint, and count only transparent runs with PLATE ON BOTH SIDES.  Three things
    follow, and each one was learned by getting it wrong first:

      * bounded, so the scan leaving the limb at its silhouette is not a gap.  An
        unrestricted axis scan called the OUTSIDE of the greave a 9 rig px hole in the
        painted, unmoved pose.
      * near the joint, so an open notch further down a limb -- the inside of a bent
        knee -- is not counted.  It is anatomy; it belongs there.
      * MONOTONE.  Adding pixels to a plate can only shorten a bounded run.  The
        enclosed-hole measure is not: filling one gap can seal an open notch into a new
        hole, and a build/harvest loop against it oscillated (ankle 28 -> 18 -> 20 rig
        px over three passes, every pass an improvement by its own lights).

    This is the number Matt's report is about: a band across the leg with nothing drawn
    in it, where the leg meets what it hangs from.
    """
    H, W = alpha.shape
    perp = np.array([-u[1], u[0]])
    worst, pts = 0.0, []
    n = int(2 * R * zoom)
    for k in range(int(-half_w), int(half_w) + 1):
        line, coords = [], []
        for i in range(n + 1):
            q = joint + u * (-R + 2 * R * i / n) + perp * k
            px = int(origin[0] + q[0] * zoom)
            py = int(origin[1] + q[1] * zoom)
            line.append(0 <= px < W and 0 <= py < H and alpha[py, px])
            coords.append(q)
        i = 0
        while i <= n:
            if line[i]:
                i += 1
                continue
            j = i
            while j <= n and not line[j]:
                j += 1
            if i > 0 and j <= n:                      # plate on both sides
                worst = max(worst, (j - i) * 2 * R / n)
                if want_pts:
                    pts.extend(coords[i:j])
            i = j + 1
    return (worst, pts) if want_pts else worst


# joint -> (name, bone at the joint, bone whose origin gives the limb's far end)
def joint_frames(poses, tag):
    def P(path):
        return np.array([poses[path][0, 2], poses[path][1, 2]])
    hip = P("Skel/hip/leg_%s_th" % tag)
    knee = P("Skel/hip/leg_%s_th/leg_%s_sh" % (tag, tag))
    ankle = P("Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft" % (tag, tag, tag))
    toe = P("Skel/hip/leg_%s_th/leg_%s_sh/leg_%s_ft/S_leg_%s_foot"
            % (tag, tag, tag, "near" if tag == "n" else "far"))

    def uni(a, b):
        d = b - a
        L = float(np.hypot(*d))
        return d / L if L > 1e-6 else np.array([0.0, 1.0])
    # The window is sized to the JOIN, not to a single radius.  The hip's join is not
    # a 9 px neighbourhood: the thigh is covered by the tabard for its whole upper
    # length, so "the thigh has come away from the body" shows anywhere from the
    # torso's lower edge down past the hem -- 38 rig px below the socket.  A 9 px
    # window around the socket read 0.67 rig px on the build Matt called detached.
    # The knee and ankle joins really are local, and a wide window there would start
    # counting the open inside of a bent knee.
    return [("hip", hip + uni(hip, knee) * 14.0, uni(hip, knee), 26.0),
            ("knee", knee, uni(knee, ankle), 12.0),
            ("ankle", ankle, uni(ankle, toe), 10.0)]


JOINT_BONES = {
    "hip_near": "Skel/hip/leg_n_th", "hip_far": "Skel/hip/leg_f_th",
    "knee_near": "Skel/hip/leg_n_th/leg_n_sh", "knee_far": "Skel/hip/leg_f_th/leg_f_sh",
    "ankle_near": "Skel/hip/leg_n_th/leg_n_sh/leg_n_ft",
    "ankle_far": "Skel/hip/leg_f_th/leg_f_sh/leg_f_ft",
}
# radius, in RIG px, around a joint inside which an enclosed hole is that joint's
# detachment.  22 rig px is a little over half a thigh length on a 194 px figure.
JOINT_R = 22.0


def probe(rig, zoom=3.0, n_walk=64, n_run=64, verbose=True):
    rep = {}
    origin = (180, 430)
    for clip, N in (("walk", n_walk), ("run", n_run), ("idle", 12)):
        if clip not in rig.anims:
            continue
        L = rig.anims[clip]["length"]
        keys = list(JOINT_BONES)
        worst = {k: 0 for k in keys}
        worst_px = {k: 0 for k in keys}
        worst_at = {k: None for k in keys}
        ax_keys = ["%s_%s" % (s, sd) for sd in ("near", "far")
                   for s in ("hip", "knee", "ankle")]
        ax_worst = {k: 0.0 for k in ax_keys}
        ax_at = {k: None for k in ax_keys}
        for i in range(N):
            t = L * i / N
            canvas, mk = rig.render(clip, t, zoom=zoom, origin=origin)
            poses = rig.pose(clip, t)
            # The silhouette a JOINT is judged against excludes the POLLAXE.  The haft
            # runs from the fist to the ground past the knight's front, so body + haft
            # encloses a tall slot of background that has nothing to do with any joint
            # -- the first run of this probe reported 37 rig px at the knee, which was
            # a true reading of that slot and the wrong answer to the question.  The
            # painting has that slot too; it is the gap between a man and the weapon he
            # is carrying, and it is supposed to be there.
            alpha = np.zeros(canvas.shape[:2], bool)
            for k, v in mk.items():
                if k != "hand_pollaxe":
                    alpha |= v
            holes = hole_mask(alpha)
            body = np.zeros_like(alpha)
            for p in BODY_PARTS:
                if p in mk:
                    body |= mk[p]
            for tag, sd in (("n", "near"), ("f", "far")):
                for seg, jp, u, r in joint_frames(poses, tag):
                    g = joint_gap(alpha, jp, u, zoom, origin, R=r)
                    k = "%s_%s" % (seg, sd)
                    if g > ax_worst[k]:
                        ax_worst[k], ax_at[k] = g, round(t, 4)
            for k, bone in JOINT_BONES.items():
                jx = origin[0] + poses[bone][0, 2] * zoom
                jy = origin[1] + poses[bone][1, 2] * zoom
                n, ext = holes_near(holes, (jx, jy), JOINT_R * zoom)
                if ext > worst[k]:
                    worst[k], worst_px[k], worst_at[k] = ext, n, round(t, 4)
                elif ext == worst[k]:
                    worst_px[k] = max(worst_px[k], n)
        rep[clip] = {"zoom": zoom, "samples": N, "joint_radius_rig_px": JOINT_R,
                     "joint_gap_rig_px": {k: round(v, 2) for k, v in ax_worst.items()},
                     "joint_gap_worst_at_s": ax_at,
                     "max_hole_extent_canvas_px": worst,
                     "max_hole_extent_rig_px": {k: round(v / zoom, 2) for k, v in worst.items()},
                     "hole_area_px": worst_px, "worst_at_s": worst_at}
        if verbose:
            print("  %-5s  JOINT GAP rig px:  hip n/f %5.2f %5.2f | knee n/f %5.2f %5.2f"
                  " | ankle n/f %5.2f %5.2f      [enclosed holes: %4.1f/%4.1f %4.1f/%4.1f"
                  " %4.1f/%4.1f]"
                  % (clip, ax_worst["hip_near"], ax_worst["hip_far"],
                     ax_worst["knee_near"], ax_worst["knee_far"],
                     ax_worst["ankle_near"], ax_worst["ankle_far"],
                     worst["hip_near"] / zoom, worst["hip_far"] / zoom,
                     worst["knee_near"] / zoom, worst["knee_far"] / zoom,
                     worst["ankle_near"] / zoom, worst["ankle_far"] / zoom))
    return rep


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--frames")
    ap.add_argument("--clip", default="walk")
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--zoom", type=float, default=3.0)
    ap.add_argument("--tscn", default=str(TSCN))
    ap.add_argument("--bg", default="30,34,44")
    ap.add_argument("--out-json")
    a = ap.parse_args()
    rig = Rig(Path(a.tscn))
    if a.probe:
        print("== joint-gap probe on %s ==" % a.tscn)
        rep = probe(rig, zoom=a.zoom)
        if a.out_json:
            Path(a.out_json).write_text(json.dumps(rep, indent=1))
    if a.frames:
        d = Path(a.frames)
        d.mkdir(parents=True, exist_ok=True)
        bg = np.array([float(v) / 255.0 for v in a.bg.split(",")], np.float32)
        L = rig.anims[a.clip]["length"]
        for i in range(a.n):
            c, _ = rig.render(a.clip, L * i / a.n, zoom=a.zoom)
            al = c[..., 3:4]
            rgb = c[..., :3] * al + bg[None, None, :] * (1 - al)
            Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(
                d / ("%s_%03d.png" % (a.clip, i)))
        print("wrote %d frames to %s" % (a.n, d))


if __name__ == "__main__":
    main()
