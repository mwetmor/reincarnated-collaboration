# C-9 meshy_t2 step 4c: render the rig for inspection, and dump the exact ortho
# mapping so the bones can be drawn on top in image space.
#
#   blender -b -noaudio --python scripts/06_rigshot.py -- <rigged.blend> <outdir> [pose.json]
#
# Passes written per view: `mesh` (unlit colour), `weights` (a flat colour per
# dominant bone group -- the skinning made visible), `head` (the rigid island
# in red). The bone overlay is drawn afterwards by 06b_draw.py, using the
# `mapping` in shot.json, because Blender renders no armature in background
# mode and PIL is not in Blender's Python.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("06_rigshot.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTDIR = a[0], a[1]
POSEJSON = a[2] if len(a) > 2 else None
RES = 900

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
objs = [o for o in sc.objects if o.type == 'MESH']
obj = objs[0]
os.makedirs(OUTDIR, exist_ok=True)

poses = json.load(open(POSEJSON)) if POSEJSON else {"rest": {}}


def apply_pose(p):
    for b in arm.pose.bones:
        b.rotation_mode = 'XYZ'
        b.rotation_euler = (0, 0, 0)
        b.location = (0, 0, 0)
    for name, rot in p.items():
        if name in arm.pose.bones:
            pb = arm.pose.bones[name]
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler = Euler([math.radians(v) for v in rot], 'XYZ')
    bpy.context.view_layer.update()


# flat colour per dominant bone group
names = [b.name for b in arm.data.bones]
import colorsys
pal = {n: colorsys.hsv_to_rgb(((i * 7) % len(names)) / len(names),
                              0.85 + 0.15 * ((i % 3) / 2.0), 0.70 + 0.30 * (i % 2))
       for i, n in enumerate(names)}
me = obj.data
gi = {g.index: g.name for g in obj.vertex_groups}
cw = me.color_attributes.new(name="gpart", type='FLOAT_COLOR', domain='POINT')
ch = me.color_attributes.new(name="ghead", type='FLOAT_COLOR', domain='POINT')
hid = set()
for v in me.vertices:
    best, bw = None, -1.0
    hw = 0.0
    for g in v.groups:
        n = gi.get(g.group)
        if g.weight > bw:
            bw, best = g.weight, n
        if n == "head":
            hw = g.weight
    c = pal.get(best, (0.5, 0.5, 0.5))
    cw.data[v.index].color = (c[0], c[1], c[2], 1.0)
    ch.data[v.index].color = (0.15 + 0.85 * hw, 0.25 * (1 - hw), 0.3 * (1 - hw), 1.0)

sc.render.resolution_x = RES; sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'

VIEWS = {"side": (1.0, 0.0, 0.0), "front": (0.0, 1.0, 0.0), "top": (0.0, 0.0, 1.0),
         "q": (0.62, 0.72, 0.31)}
CENTRE = Vector((0.0, -0.05, 0.62))
SPAN = 2.3
cam.data.ortho_scale = SPAN

shot = dict(resolution=RES, ortho_scale=SPAN, centre=[round(v, 4) for v in CENTRE],
            views={}, poses=list(poses.keys()), bones={}, palette={})
for n in names:
    shot["palette"][n] = [round(c, 4) for c in pal[n]]

for vn, d in VIEWS.items():
    d = Vector(d).normalized()
    pos = CENTRE + d * 12
    cam.location = pos
    up = 'Z' if vn == "top" else 'Y'
    cam.rotation_euler = (CENTRE - pos).to_track_quat('-Z', up).to_euler()
    bpy.context.view_layer.update()
    M = cam.matrix_world.inverted()
    shot["views"][vn] = dict(cam_matrix_world_inv=[list(r) for r in M],
                             dir=[round(v, 4) for v in d])

for pname, p in poses.items():
    apply_pose(p)
    bones = {}
    for b in arm.pose.bones:
        bones[b.name] = dict(head=[round(v, 5) for v in (arm.matrix_world @ b.head)],
                             tail=[round(v, 5) for v in (arm.matrix_world @ b.tail)],
                             parent=b.parent.name if b.parent else None)
    shot["bones"][pname] = bones
    for vn in VIEWS:
        d = Vector(VIEWS[vn]).normalized()
        pos = CENTRE + d * 12
        cam.location = pos
        cam.rotation_euler = (CENTRE - pos).to_track_quat('-Z', 'Z' if vn == "top" else 'Y').to_euler()
        for tag, attr in (("mesh", None), ("weights", "gpart"), ("head", "ghead")):
            # rebuild shading each time: unlit() appends nodes, so do it on a
            # fresh copy of the material graph
            for slot in obj.material_slots:
                m = slot.material
                nt = m.node_tree
                for n in list(nt.nodes):
                    if n.type in ('EMISSION', 'ATTRIBUTE'):
                        nt.nodes.remove(n)
            T.unlit(objs, attr=attr)
            sc.render.filepath = os.path.join(OUTDIR, "%s_%s_%s.png" % (pname, vn, tag))
            bpy.ops.render.render(write_still=True)

json.dump(shot, open(os.path.join(OUTDIR, "shot.json"), "w"), indent=1)
print("wrote", OUTDIR, len(poses), "poses x", len(VIEWS), "views")
