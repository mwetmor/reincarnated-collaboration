# R-C9-119: the OPEN GRIMOIRE built as exact geometry and textured from Astra's painted sheet GS-SBOOK2_a (the sheet's side
# views came back as CLOSED page blocks, so a Tripo build would have had contradictory views; the conductor allowed "build
# the open form in Blender").
#   python3 s48_open_book.py atlas <sheet.png> <boxes.json> <atlas.png>          (compose the texture atlas, PIL)
#   blender -b -noaudio --python s48_open_book.py -- <atlas.png> <out.glb> [--json f]
# BOOK FRAME: spine along +Y (bottom at y=0, top at y=H), page normal +Z (the pages face +Z), across the spread +X.
# Each half = a cover slab + a page block, hinged at the spine and turned up HALF of (180 - OPEN) so the covers stand
# OPEN degrees apart; a half-round spine under the hinge. Pages' top faces carry the painted spread (left page -> left
# half), the covers' outside carries the painted back view (mirrored: the left cover's outside is the RIGHT half of the
# back view), the page edges a cream strip from the spread's own margin.
import json, math, os, sys
OPEN = 155.0; H = 0.28; WH = 0.20; TP = 0.020; TC = 0.006; SPR = 0.022
if len(sys.argv) > 1 and sys.argv[1] == "atlas":
    from PIL import Image
    sheet, boxes, out = sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4]
    im = Image.open(sheet).convert("RGB")
    (fx0, fy0, fx1, fy1), _, (bx0, by0, bx1, by1), _ = boxes
    # the spread: drop the ribbon hanging below -- keep the covers' height (the back view's) from the top
    hh = by1 - by0
    spread = im.crop((fx0, fy0, fx1, fy0 + hh)).resize((1024, 512), Image.LANCZOS)
    back = im.crop((bx0, by0, bx1, by1)).resize((1024, 512), Image.LANCZOS)
    A = Image.new("RGB", (1024, 1024), (233, 222, 196))
    A.paste(spread, (0, 0)); A.paste(back, (0, 512))
    A.save(out); print("atlas", out); raise SystemExit(0)

import bpy, bmesh
from mathutils import Vector, Matrix
a = sys.argv[sys.argv.index('--') + 1:]
ATLAS, OUT = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '.json')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
me = bpy.data.meshes.new("grimoire_open"); ob = bpy.data.objects.new("grimoire_open", me); sc.collection.objects.link(ob)
bm = bmesh.new(); uvl = bm.loops.layers.uv.new("UVMap")
EDGE_UV = (0.985, 0.25)                    # a cream texel at the right margin of the spread (the page block's own edge)


def box(x0, x1, z0, z1, top_uv=None, bot_uv=None, side_uv=EDGE_UV):
    """axis-aligned box in the HALF's local frame (x across, y spine, z up); uv rects (u0,v0,u1,v1) for top / bottom"""
    V = [bm.verts.new((x, y, z)) for z in (z0, z1) for y in (0.0, H) for x in (x0, x1)]
    # index: z0: (y0,x0)0 (y0,x1)1 (y1,x0)2 (y1,x1)3 ; z1: 4 5 6 7
    faces = {"top": (4, 5, 7, 6), "bot": (0, 2, 3, 1), "s1": (0, 1, 5, 4), "s2": (2, 6, 7, 3), "s3": (0, 4, 6, 2), "s4": (1, 3, 7, 5)}
    out = []
    for k, idx in faces.items():
        f = bm.faces.new([V[i] for i in idx]); out.append(f)
        for lp in f.loops:
            x, y, z = lp.vert.co
            if k == "top" and top_uv:
                u0, v0, u1, v1 = top_uv; lp[uvl].uv = (u0 + (x - x0) / (x1 - x0) * (u1 - u0), v0 + y / H * (v1 - v0))
            elif k == "bot" and bot_uv:
                u0, v0, u1, v1 = bot_uv; lp[uvl].uv = (u0 + (x - x0) / (x1 - x0) * (u1 - u0), v0 + y / H * (v1 - v0))
            else:
                lp[uvl].uv = side_uv
    return V


# glTF/Blender UV: v up from the image BOTTOM. Atlas: spread in the TOP half (v 0.5..1), back view in the BOTTOM half (v 0..0.5).
halves = []
for side in (-1, 1):                                   # -1 = the LEFT half (x < 0), +1 = the RIGHT half
    page_uv = (0.0, 0.5, 0.5, 1.0) if side < 0 else (0.5, 0.5, 1.0, 1.0)
    cover_uv = (1.0, 0.0, 0.5, 0.5) if side < 0 else (0.5, 0.0, 0.0, 0.5)   # mirrored halves of the back view
    x0, x1 = (-WH, 0.0) if side < 0 else (0.0, WH)
    Vp = box(x0, x1, TC, TC + TP, top_uv=page_uv)
    xc0, xc1 = (x0 - 0.004, x1) if side < 0 else (x0, x1 + 0.004)
    Vc = box(xc0, xc1, 0.0, TC, bot_uv=cover_uv)
    ang = math.radians((180.0 - OPEN) / 2.0) * (-side)                  # each half turned up about the spine (y axis)
    R = Matrix.Rotation(ang, 4, 'Y')
    for v in Vp + Vc:
        v.co = R @ v.co
    halves.append(ang)
# the half-round spine under the hinge
bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=SPR, radius2=SPR, depth=H,
                      matrix=Matrix.Translation((0, H / 2, 0.0)) @ Matrix.Rotation(math.radians(90), 4, 'X'))
for f in bm.faces:
    for lp in f.loops:
        if lp[uvl].uv.length == 0:
            lp[uvl].uv = (0.5, 0.25)                                         # the spine band: the back view's centre (steel)
bm.normal_update(); bm.to_mesh(me); bm.free()
img = bpy.data.images.load(os.path.abspath(ATLAS))
mat = bpy.data.materials.new("grimoire_open"); mat.use_nodes = True
nt = mat.node_tree; bs = nt.nodes.get("Principled BSDF"); tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = img
nt.links.new(tx.outputs["Color"], bs.inputs["Base Color"]); bs.inputs["Roughness"].default_value = 0.8
me.materials.append(mat)
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='AUTO')
open_w = 2 * WH * math.cos(math.radians((180 - OPEN) / 2))
rep = dict(open_deg=OPEN, half_width_m=WH, height_m=H, page_block_m=TP, cover_m=TC, spine_radius_m=SPR, open_width_m=round(open_w, 4),
           frame="spine +Y (0..H), pages face +Z, across +X", faces=len(me.polygons), atlas=ATLAS,
           note="the painted page spread is 0.59 wide per page height; each half is stretched 1.2x across for presence at play scale")
json.dump(rep, open(OUTJ, 'w'), indent=1); print("BOOK", json.dumps(rep))
