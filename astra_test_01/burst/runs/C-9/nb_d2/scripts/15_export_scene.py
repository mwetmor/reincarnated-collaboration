# D2 step 3: export the assembled character for the 3D cliffside.
#
#   blender -b -noaudio --python scripts/15_export_scene.py -- <clip.glb>
#     <bodytex.png> <outdir> --gear "<same spec as 10_swap>" [--height 1.85]
#
# ONE assembled scene, then one export per piece plus one for the body. Pieces
# are never exported alone and re-imported: Meshy ships the body at 0.01 object
# scale, and a piece built in metres and parented to that armature collapses to
# a 1.7 cm speck -- in the FILE. Everything here is fitted in this session and
# written out with the body's transform already baked in.
#
# The body carries the `helmet_on` shape key, so the consumer toggles the
# helmet and the hair compresses with it: reversible, and no repaint.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("15_export_scene.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
CLIP, TEX, OUT = a[0], a[1], a[2]
SPEC = a[a.index("--gear") + 1] if "--gear" in a else ""
HGT = float(a[a.index("--height") + 1]) if "--height" in a else 1.85
ROOT = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
for o in body:
    for s_ in o.material_slots:
        if s_.material and s_.material.node_tree:
            for nd in s_.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img
                    nd.image.colorspace_settings.name = 'sRGB'
BV, BT, names, W, tree = G.body_sampler(body[0])
PIECE_REF_H = 1.70                # the rig the pieces were isolated against
BH_NOW = float(BV[:, 2].max() - BV[:, 2].min())
PSCALE = BH_NOW / PIECE_REF_H
print("body is %.4f m; pieces were built against %.2f m -> scaling each by "
      "x%.5f" % (BH_NOW, PIECE_REF_H, PSCALE))
made_all, manifest = [], []
SPECS = dict(axe=dict(axis_world=(0, 0, 1), face_world=(0, -1, 0)),
             shield=dict(axis_world=(1, 0.25, 0), face_world=(0, -1, 0),
                         offset_world=(0.09, 0, -0.13), anchor="normal"))
for item in [x for x in SPEC.split(",") if x]:
    parts = item.split(":")
    nm, mode = parts[0], parts[1]
    bones = parts[2].split("|") if len(parts) > 2 and parts[2] else []
    split = len(parts) > 3 and parts[3] == "split"
    faces = dict(helmet=12000, bracers=12000, byrnie=26000, mantle=24000,
                 axe=9000, shield=9000).get(nm, 16000)
    offs = dict(helmet=0.0, bracers=0.002, byrnie=0.005, mantle=0.008,
                axe=0.0, shield=0.0).get(nm, 0.004)
    before = set(sc.objects)
    src = "builds" if mode == "socket" else "pieces"
    pc = G.import_piece(os.path.join(ROOT, src, "%s.glb" % nm), before)
    if mode != "socket":
        G.rescale_piece(pc, PSCALE)       # sockets are sized from --length
    G.decimate(pc, faces)
    if offs > 0:
        P, pushed = G.clear_body(pc, tree, offs)
    else:
        co = np.empty(len(pc.data.vertices) * 3)
        pc.data.vertices.foreach_get("co", co)
        P, pushed = co.reshape(-1, 3), 0
    if mode == "socket":
        ln = float(parts[3]) if len(parts) > 3 else 0.82
        gr = float(parts[4]) if len(parts) > 4 else 0.3
        info = G.socket_weapon2(pc, arm, bones[0], ln, gr, **SPECS[nm])
        G.align_space(pc, body[0])
        made = [(pc, bones[0])]
    elif mode == "skin":
        G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
        G.align_space(pc, body[0])
        made = [(pc, "skinned")]
    else:
        made = G.bone_bind(pc, arm, bones, split)
        for o, _ in made:
            G.align_space(o, body[0])
    if nm == "helmet":
        mv, ca, kk = G.helmet_on_key(body[0], made[0][0], arm)
        kk.value = 0.0                    # OFF by default; the consumer sets it
        print("   helmet_on key on the body: %d of %d vertices" % (mv, ca))
    for i, (o, b) in enumerate(made):
        o.name = "%s_%02d" % (nm, i) if len(made) > 1 else nm
    made_all.append((nm, mode, made))
    manifest.append(dict(piece=nm, mode=mode, bones=[b for _, b in made],
                         objects=[o.name for o, _ in made], faces=faces,
                         offset_m=offs, glb="%s.glb" % nm))
    print("  + %-8s %-6s %d object(s)" % (nm, mode, len(made)))

# scale the whole assembly to the declared height, measured on the BODY
co = np.empty(len(body[0].data.vertices) * 3)
body[0].data.vertices.foreach_get("co", co)
BW = (co.reshape(-1, 3) @ np.array(body[0].matrix_world.to_3x3()).T
      + np.array(body[0].matrix_world.translation))
H0 = float(BW[:, 2].max() - BW[:, 2].min())
s = HGT / H0
for o in list(sc.objects):
    if o.parent is None:
        o.matrix_world = Matrix.Scale(s, 4) @ o.matrix_world
bpy.context.view_layer.update()
print("scaled x%.5f: body height %.4f -> %.4f m" % (s, H0, H0 * s))


def export(objs, path, anim=False):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB',
                              use_selection=True, export_animations=anim,
                              export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


mb = export(body, os.path.join(OUT, "nb-body.glb"), anim=True)
print("wrote nb-body.glb (%.2f MB) with the helmet_on morph and the clips" % mb)
for nm, mode, made in made_all:
    p = os.path.join(OUT, "%s.glb" % nm)
    sz = export([o for o, _ in made], p)
    print("wrote %-12s %.2f MB" % (os.path.basename(p), sz))
json.dump(dict(body="nb-body.glb", height_m=HGT, scale_applied=round(float(s), 6),
               facing="-Y", his_right="-X", up="+Z",
               body_shape_keys=["helmet_on"],
               helmet_on="set to 1 when the helmet is equipped, 0 when removed",
               layer_order=["body", "byrnie", "mantle", "bracers", "helmet",
                            "shield", "axe"],
               world_scale_rule=dict(factor=1.25178,
                                     world_height_m=round(HGT * 1.25178, 5)),
               pieces=manifest), open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
print("wrote manifest.json")
