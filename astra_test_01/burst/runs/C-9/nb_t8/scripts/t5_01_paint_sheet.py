# C-9 T5 step 1: the PAINT SHEET, rendered from the model itself.
#
#   blender -b -noaudio --python scripts/01_paint_sheet.py -- <blend> <out.png>
#          [--layout packed|grid4x2] [--canvas 1536x1024] [--dirs S,SE,...]
#
# T5's whole claim is zero frame-to-frame drift BY CONSTRUCTION: the texture is
# painted ONCE and every frame after that is a render, so there is nothing left
# to drift. That only holds if the thing Astra paints is the MODEL, in the
# model's own views -- a sheet rendered from the mesh is consistent with the
# mesh by construction, which is exactly what the M-b projection lacked.
#
# LAYOUT. A quadruped does not project the same box from every direction: this
# one is 0.499 m wide from the front and 1.822 m from the side, aspects 0.33 to
# 1.51. A uniform 4x2 grid must therefore size every cell for the WIDEST view
# and waste the rest, which costs real paint resolution -- 210.8 px/m against
# the 253.8 px/m a row-packed layout gives, a fifth of the linear detail on
# every creature. Both layouts are built from the same renders; --layout picks.
# The approved MC-1 sheet is itself irregular (narrow front and back beside wide
# side views), so an irregular sheet is within what Astra has already painted.
#
# The camera is solved PER CELL and written to the layout JSON in full, because
# step 2 has to project the paint back onto the UVs and an ortho unprojection is
# only as good as the numbers it is handed. One px/m for every cell, so a texel
# painted in two views arrives at the same detail from both.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

def _load(path):
    """Open a .blend or import a .glb/.gltf -- the T5 scripts were written for
    a canonicalised .blend and this character arrives as a rigged GLB."""
    import bpy as _b
    if path.lower().endswith((".glb", ".gltf")):
        _b.ops.wm.read_factory_settings(use_empty=True)
        _b.ops.import_scene.gltf(filepath=path)
    else:
        _b.ops.wm.open_mainfile(filepath=path)




def _skinned(objs):
    """Meshy ships an unskinned Icosphere with every rigged GLB -- 42 verts, a
    unit sphere at the origin, no vertex groups. It renders nothing (no
    material) but it is in the scene, so any bbox taken over ALL meshes is the
    SPHERE's bbox: it inflated this figure's box from 0.94 x 0.37 x 1.70 to
    1.90 x 2.00 x 2.70 and made every paint cell three times the size of the
    figure inside it. It also made the character read as 2.70 m tall when he is
    1.70 m. Skinned meshes only. (Same stray cost a day in T1.)"""
    sk = [o for o in objs if o.vertex_groups and len(o.vertex_groups)]
    return sk or objs


a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTPNG = a[0], a[1]
LAYOUT = a[a.index("--layout") + 1] if "--layout" in a else "packed"
CW, CH = (int(v) for v in (a[a.index("--canvas") + 1] if "--canvas" in a
                           else "1536x1024").split("x"))
ELEV = float(a[a.index("--elev") + 1]) if "--elev" in a else 19.77
NAME = a[a.index("--name") + 1] if "--name" in a else "a"
# "head" frames the cells on the HEAD BLOCK instead of the whole creature. The
# face is this creature's identity and step 5's deliverable is a face close-up,
# and on a whole-body sheet the head lands at 81 x 54 px. A dedicated cell at
# 3x the scale makes it 250 px across. The body is cropped away in such a cell,
# by design, so the edge-touch check does not apply to it.
SUBJECT = a[a.index("--subject") + 1] if "--subject" in a else "body"
# WHICH WAY THE MODEL FACES IS NOT A CONSTANT OF THIS SCRIPT. It was written
# for the manticore's canon.blend, which t2lib canonicalises to face +Y, and
# its camera for direction S sits at +Y accordingly. This barbarian faces -Y,
# so every cell came out 180 degrees from its label -- harmless for the eight
# body views, which still cover the same eight directions under other names,
# and ruinous for the two face close-ups, which spent the sheet's most valuable
# cells on the back of his head.
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else 0.0
SCALE = float(a[a.index("--scale") + 1]) if "--scale" in a else 1.0
# A PLAN lets one sheet mix cells that do not share a camera: four top-down
# body views beside two head close-ups, each with its own elevation, subject
# and scale. The cell set is a parameter of this pipeline, so the packer and
# the camera solve both take it per cell rather than per sheet.
PLAN = json.load(open(a[a.index("--plan") + 1])) if "--plan" in a else None
KEY = (0, 255, 0)           # #00ff00, the matte key Astra paints around
GAP = 16                    # px between cells, so no two creatures touch
# MARGIN is not cosmetic. Sized to the exact projected bbox, the creature
# touches all four of its own cell edges by construction (measured: 46-75% of
# the border), which leaves the painted INK OUTLINE nowhere to go -- it would
# be clipped at the silhouette, and with a thin gap it would bleed into the
# neighbouring creature. With a margin, "alpha on the cell border" stops being
# the normal case and becomes a real crop detector.
MARGIN = 14
DIRS = a[a.index("--dirs") + 1].split(",") if "--dirs" in a else \
    ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135,
       "N": 180, "NW": 225, "W": 270, "SW": 315}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import t2lib_ref as T

_load(BLEND)
sc = bpy.context.scene
objs = _skinned([o for o in sc.objects if o.type == 'MESH'])
T.unlit(objs)                       # base colour -> emission: the Meshy texture

P = []
for o in objs:
    M = np.array(o.matrix_world.to_3x3()).T
    co = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", co)
    P.append(co.reshape(-1, 3) @ M + np.array(o.matrix_world.translation))
P = np.vstack(P)

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
el = math.radians(ELEV)
base_aim = Vector((0.0, 0.0, float(P[:, 2].max() + P[:, 2].min()) * 0.5))



def basis(d, elev=None):
    A = math.radians(AZI[d] + YAW)
    e = math.radians(elev) if elev is not None else el
    pos = base_aim + Vector((math.sin(A) * math.cos(e), math.cos(A) * math.cos(e),
                             math.sin(e))) * 20.0
    cam.location = pos
    cam.rotation_euler = (base_aim - pos).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()     # else matrix_world is stale identity
    R = np.array(cam.matrix_world.to_3x3())
    return pos, R[:, 0], R[:, 1]


def subject_pts(sub):
    """'head' is the top band of the figure. The T5 version also required the
    points to be forward of the body's mid-depth, which is right for a
    quadruped whose head is at one END of a long body and wrong for a biped
    whose head is directly above it -- on this barbarian that filter would
    throw away the back of his skull and half his hair."""
    if not sub.startswith("head"):
        return P
    frac = float(sub[4:]) if len(sub) > 4 else 0.82
    zmin, zmax = P[:, 2].min(), P[:, 2].max()
    return P[P[:, 2] > zmin + frac * (zmax - zmin)]


if PLAN is None:
    PLAN = [dict(id=d, dir=d, elev=ELEV, subject=SUBJECT, scale=1.0) for d in DIRS]
for c in PLAN:
    c.setdefault("elev", ELEV); c.setdefault("subject", "body")
    c.setdefault("scale", 1.0); c.setdefault("dir", c["id"])
IDS = [c["id"] for c in PLAN]
SPEC = {c["id"]: c for c in PLAN}
box = {}
for c in PLAN:
    Q = subject_pts(c["subject"])
    _, right, up = basis(c["dir"], c["elev"])
    x, y = Q @ right, Q @ up
    # scale>1 shrinks the cell relative to the subject, so the box is divided
    box[c["id"]] = dict(w=float(x.max() - x.min()), h=float(y.max() - y.min()),
                        cx=float((x.max() + x.min()) * 0.5),
                        cy=float((y.max() + y.min()) * 0.5),
                        right=right.tolist(), up=up.tolist())

# ---- solve ONE px/m and the cell rectangles --------------------------------
if LAYOUT == "grid4x2":
    cols, rows_n = 4, 2
    cw, ch = CW // cols, CH // rows_n
    mw = max(b["w"] for b in box.values()); mh = max(b["h"] for b in box.values())
    ppm = min((cw - 2 * MARGIN) / mw, (ch - 2 * MARGIN) / mh)
    cells = {d: (i % cols * cw, i // cols * ch, cw, ch) for i, d in enumerate(IDS)}
    rows = [IDS[i:i + cols] for i in range(0, len(IDS), cols)]
    rows = [DIRS[i:i + cols] for i in range(0, len(DIRS), cols)]
else:
    # SHELF PACK with a binary search on scale. The first version hardcoded the
    # row grouping for the eight-view case, and on a four-view sheet it put the
    # two narrow views in rows of their own and lost a third of the scale
    # (199.9 px/m against the 314 a two-row pack gives). The set of cells is a
    # parameter of this pipeline -- eight body views, four top-down, a couple of
    # head close-ups -- so the packer has to be one too.
    def cw_(d, ppm):
        return int(round(box[d]["w"] * ppm * SPEC[d]["scale"])) + 2 * MARGIN

    def ch_(d, ppm):
        return int(round(box[d]["h"] * ppm * SPEC[d]["scale"])) + 2 * MARGIN

    def shelf(ppm, order):
        rows_, x, cur = [], 0, []
        for d in order:
            w = cw_(d, ppm)
            if cur and x + GAP + w > CW - 2 * GAP:
                rows_.append(cur); cur, x = [], 0
            cur.append(d); x += w + (GAP if x else 0)
        if cur:
            rows_.append(cur)
        H = sum(max(ch_(d, ppm) for d in r)
                for r in rows_) + GAP * (len(rows_) + 1)
        widest = max(sum(cw_(d, ppm) for d in r)
                     + GAP * (len(r) + 1) for r in rows_)
        return rows_, H, widest

    # One greedy ordering is one packing, not the best packing: height-sorted
    # first-fit left the bottom third of the eight-view sheet empty because it
    # was WIDTH-bound at 4+4 when a 3+3+2 uses the height. Try several orderings
    # and keep whichever admits the largest scale. Still greedy, but the search
    # is over strategies rather than committed to one.
    # An EXPLICIT row structure, when the plan carries one. A standing figure
    # is mostly air in its own bounding box -- 0.5 m wide against 1.85 m tall --
    # so eight of them fit in ONE row with room to spare, and the greedy
    # orderings were splitting them across three rows and losing half the
    # scale (139 px/m against the 292 one row admits). The packer is a good
    # default and a poor oracle; when the right structure is known, say it.
    ROWS = [r for r in (PLAN[0].get("_rows") or []) if r] if PLAN and \
        isinstance(PLAN[0], dict) and PLAN[0].get("_rows") else None
    cands = [sorted(IDS, key=lambda d: -box[d]["h"]),
             sorted(IDS, key=lambda d: -box[d]["w"]),
             sorted(IDS, key=lambda d: -box[d]["w"] * box[d]["h"]),
             sorted(IDS, key=lambda d: box[d]["w"] / box[d]["h"]),
             list(IDS)]
    if ROWS:
        def feas(ppm):
            H_ = sum(max(ch_(d, ppm) for d in r) for r in ROWS) + GAP * (len(ROWS) + 1)
            W_ = max(sum(cw_(d, ppm) for d in r) + GAP * (len(r) + 1) for r in ROWS)
            return H_ <= CH and W_ <= CW
        loR, hiR = 10.0, 3000.0
        for _ in range(60):
            mid = 0.5 * (loR + hiR)
            if feas(mid):
                loR = mid
            else:
                hiR = mid
        ppm = SCALE * loR
        rows = ROWS
        print("   explicit row structure from the plan: %s" % [len(r) for r in ROWS])
    else:
        best = None
    for order in (cands if not ROWS else []):
        lo, hi = 10.0, 3000.0
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            _, H, wdt = shelf(mid, order)
            if H <= CH and wdt <= CW:
                lo = mid
            else:
                hi = mid
        if best is None or lo > best[0]:
            best = (lo, order)
    if not ROWS:
        ppm = SCALE * best[0]
        rows, _, _ = shelf(ppm, best[1])
    cells = {}
    y = GAP
    for r in rows:
        rowh = max(ch_(d, ppm) for d in r)
        widths = [cw_(d, ppm) for d in r]
        x = int((CW - sum(widths) - GAP * (len(r) - 1)) / 2)
        for d, wpx in zip(r, widths):
            # each cell keeps its OWN height and is centred in the row: giving
            # every cell the row's height renders a tall narrow view into a
            # frame twice its content and wastes the pixels on empty key
            hh = ch_(d, ppm)
            cells[d] = (x, y + (rowh - hh) // 2, wpx, hh)
            x += wpx + GAP
        y += rowh + GAP

sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
eng = [i.identifier for i in
       bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng \
    else 'BLENDER_EEVEE'

tmp = os.path.join(ROOT, "work", "_cells_%s" % NAME)
os.makedirs(tmp, exist_ok=True)
layout = dict(canvas=[CW, CH], key_rgb=list(KEY), layout=LAYOUT, gap_px=GAP,
              margin_px=MARGIN,
              px_per_m=round(float(ppm), 5), elevation_deg=ELEV,
              pose="rest", subject=SUBJECT, name=NAME, yaw_deg=YAW,
              source_blend=os.path.abspath(BLEND), cells={})
for d in IDS:
    x0, y0, wpx, hpx = cells[d]
    b = box[d]
    c = SPEC[d]
    elc = math.radians(c["elev"])
    pos, right, up = basis(c["dir"], c["elev"])
    # aim so THIS view's own box lands in the middle of its cell.
    # cx/cy are ABSOLUTE projections onto the camera axes, so the offset from
    # base_aim is (cx - base_aim.right), not cx. Assuming base_aim projects to
    # zero is true for `right` (horizontal, and base_aim is on the z axis) and
    # FALSE for `up`, which carries cos(elev): it pushed every creature down by
    # 0.601 m * cos(19.77) * ppm = 127 px and clipped the paws and tails off the
    # bottom of every cell. Measure the term; do not assume it away.
    rv, uv = Vector(right.tolist()), Vector(up.tolist())
    aim = base_aim + rv * (b["cx"] - base_aim.dot(rv)) \
                   + uv * (b["cy"] - base_aim.dot(uv))
    _A = math.radians(AZI[c["dir"]] + YAW)
    pos = aim + Vector((math.sin(_A) * math.cos(elc),
                        math.cos(_A) * math.cos(elc),
                        math.sin(elc))) * 20.0
    cam.location = pos
    cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    sc.render.resolution_x, sc.render.resolution_y = wpx, hpx
    cam.data.ortho_scale = max(wpx, hpx) / (ppm * c["scale"])
    sc.render.filepath = os.path.join(tmp, "cell_%s.png" % d)
    bpy.ops.render.render(write_still=True)
    layout["cells"][d] = dict(
        dir=c["dir"], azimuth_deg=AZI[c["dir"]], elevation_deg=c["elev"],
        subject=c["subject"], rect=[x0, y0, wpx, hpx],
        ortho_scale=round(cam.data.ortho_scale, 6),
        cam_location=[round(float(v), 6) for v in cam.location],
        cam_rotation_euler=[round(float(v), 6) for v in cam.rotation_euler],
        aim=[round(float(v), 6) for v in aim],
        screen_right=[round(float(v), 6) for v in right],
        screen_up=[round(float(v), 6) for v in up],
        box_m=[round(b["w"], 5), round(b["h"], 5)],
        px_per_m=round(float(ppm * c["scale"]), 5), scale=c["scale"])
json.dump(layout, open(os.path.join(ROOT, "work", "layout_%s.json" % NAME), "w"),
          indent=1)
print("PAINT SHEET %s: base px/m %.2f, %d cells, canvas %dx%d"
      % (LAYOUT, ppm, len(IDS), CW, CH))
for d in IDS:
    x0, y0, wpx, hpx = cells[d]
    print("   %-9s cell %4d,%4d  %4dx%-4d px  el %5.2f %-4s  %6.1f px/m"
          % (d, x0, y0, wpx, hpx, SPEC[d]["elev"], SPEC[d]["subject"],
             ppm * SPEC[d]["scale"]))
