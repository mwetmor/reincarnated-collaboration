# R-C9-105 paint pass: build the two REST-POSE scenes the paint sheets are rendered from and baked onto.
#   blender -b -noaudio --python s38_paint_scenes.py -- <nb-body_champion.glb> <export_dir> <out_dir>
# body_rest.glb    the champion body alone (no clips, all morphs 0)
# dressed_rest.glb the body + all eight pieces, every mesh under ONE armature; objects named B_body / P_<piece>[_n]
# Every piece was exported with the body's object transform (gearlib.align_space), so re-parenting to the body's armature
# and copying the body's world matrix puts it exactly where the assembler fitted it.
import bpy, os, sys, json
a = sys.argv[sys.argv.index('--') + 1:]
BODY, EXP, OUT = a[0], a[1], a[2]
PIECES = ["helm", "chest", "pauldron", "wrists", "girdle", "kilt", "wraps", "greaves"]
os.makedirs(OUT, exist_ok=True)


def base():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=BODY)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    arm.animation_data_clear()
    for pb in arm.pose.bones:
        pb.matrix_basis.identity()
    for act in list(bpy.data.actions):
        bpy.data.actions.remove(act)
    bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
    for o in [o for o in sc.objects if o.type == 'MESH' and o is not bo]:
        bpy.data.objects.remove(o, do_unlink=True)
    if bo.data.shape_keys:
        for k in bo.data.shape_keys.key_blocks:
            k.value = 0.0
    bo.name = "B_body"
    return sc, arm, bo


def export(sc, arm, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in sc.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False,
                              export_morph=True, export_image_format='AUTO')


sc, arm, bo = base()
export(sc, arm, os.path.join(OUT, "body_rest.glb"))
rep = {"body_rest": [bo.name]}
for p in PIECES:
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(EXP, p + ".glb"))
    new = [o for o in sc.objects if o not in before]
    ms = [o for o in new if o.type == 'MESH' and len(o.data.vertices) > 200]
    for i, o in enumerate(ms):
        for m in o.modifiers:
            if m.type == 'ARMATURE':
                m.object = arm
        o.parent = bo.parent
        o.matrix_parent_inverse = bo.matrix_parent_inverse.copy()
        o.matrix_basis = bo.matrix_basis.copy()
        o.name = "P_%s" % p if len(ms) == 1 else "P_%s_%d" % (p, i)
    for o in new:
        if o not in ms:
            bpy.data.objects.remove(o, do_unlink=True)
    rep.setdefault("dressed_rest", []).extend(o.name for o in ms)
bpy.context.view_layer.update()
export(sc, arm, os.path.join(OUT, "dressed_rest.glb"))
# the atlas each mesh samples (pieces share the armoured build's atlas; the body has its own)
imgs = {}
for o in sc.objects:
    if o.type != 'MESH':
        continue
    for s in o.material_slots:
        if s.material and s.material.node_tree:
            for n in s.material.node_tree.nodes:
                if n.type == 'TEX_IMAGE' and n.image:
                    imgs[o.name] = [n.image.name, list(n.image.size)]
rep["images"] = imgs
json.dump(rep, open(os.path.join(OUT, "scenes.json"), "w"), indent=1)
print("SCENES", json.dumps(rep)[:900])
