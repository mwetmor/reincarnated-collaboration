# Four flat looks at an isolated piece (front, right, back, left), textured, for a by-eye
# check that the predicate kept the garment and nothing else (braid, boots, skin).
#   blender -b -noaudio --python scripts/s8_look.py -- <piece.glb> <out.png>
import bpy, math, sys
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
sc = bpy.context.scene
obs = [o for o in sc.objects if o.type == 'MESH' and len(o.data.vertices) > 200]
for o in sc.objects:
    if o.type == 'MESH' and o not in obs: o.hide_render = True
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
for o in obs:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c); lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
ctr = (lo + hi) / 2; H = max(hi.z - lo.z, hi.x - lo.x, hi.y - lo.y)
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = 1600, 520
sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.92, 0.92, 0.92, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.4
for o in obs:
    for s in o.material_slots:
        if s.material and s.material.node_tree:
            nt = s.material.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
            tex = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None)
            if tex:
                em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(tex.outputs[0], em.inputs[0]); nt.links.new(em.outputs[0], out.inputs[0])
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = H * 1.12 * (1600 / 520) / 4
import os
tiles = []
for i, az in enumerate((0, 90, 180, 270)):
    r = math.radians(az)
    cam.location = ctr + Vector((math.sin(r), -math.cos(r), 0)) * 10
    cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.resolution_x = 400
    f = a[1].replace(".png", "_%d.png" % i); sc.render.filepath = f
    bpy.ops.render.render(write_still=True); tiles.append(f)
print("TILES", ",".join(tiles))
