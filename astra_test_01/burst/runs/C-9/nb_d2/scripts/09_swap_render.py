# D2 step 6: THE SWAP TEST. Render the same man, the same clip, the same body
# texture, with gear stacked on -- and nothing about the body repainted between
# stacks.
#
#   blender -b -noaudio --python scripts/09_swap_render.py -- <clip.glb>
#     <bodytex.png> <outdir> --gear a.glb,b.glb [--elev 52.95] [--res 300]
#
# Each gear GLB carries its own copy of the 24-bone armature, because that is
# how a skinned mesh travels. Here the meshes are lifted OFF that copy and
# re-bound to the clip's armature: same bone names, so the vertex groups land
# without remapping, and one skeleton drives everything. Importing the copies
# and leaving them would give five armatures playing one animation out of sync
# with themselves.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
CLIP, TEX, OUT = a[0], a[1], a[2]
GEAR = [g for g in (a[a.index("--gear") + 1].split(",") if "--gear" in a else []) if g]
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 300
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else 0.0


def unlit(objs, img=None):
    for o in objs:
        for s in o.material_slots:
            m = s.material
            if not m or not m.node_tree:
                continue
            nt = m.node_tree
            if img:
                for nd in nt.nodes:
                    if nd.type == 'TEX_IMAGE':
                        nd.image = img
                        nd.image.colorspace_settings.name = 'sRGB'
            b = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
            out = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            L = b.inputs['Base Color'].links if b else []
            if L:
                nt.links.new(L[0].from_socket, em.inputs['Color'])
            nt.links.new(em.outputs['Emission'], out.inputs['Surface'])


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
unlit(body, img)
worn = []
for gp in GEAR:
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=gp)
    added = [o for o in sc.objects if o not in before]
    gmesh = [o for o in added if o.type == 'MESH']
    garm = [o for o in added if o.type == 'ARMATURE']
    for o in gmesh:
        o.parent = arm
        for m in list(o.modifiers):
            if m.type == 'ARMATURE':
                m.object = arm
        if not any(m.type == 'ARMATURE' for m in o.modifiers):
            mm = o.modifiers.new('arm', 'ARMATURE'); mm.object = arm
    for o in garm:
        bpy.data.objects.remove(o, do_unlink=True)
    unlit(gmesh)
    worn += gmesh
    bpy.context.view_layer.update()
    for o in gmesh:
        cv = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", cv)
        wv = cv.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T + np.array(o.matrix_world.translation)
        print("      %-20s %6d f  bbox z %.3f..%.3f  x %.3f..%.3f  vgroups %d  mods %s"
              % (o.name, len(o.data.polygons), wv[:, 2].min(), wv[:, 2].max(),
                 wv[:, 0].min(), wv[:, 0].max(), len(o.vertex_groups),
                 [m.type for m in o.modifiers]))
    print("  + %-14s %d mesh(es), %d faces"
          % (os.path.basename(gp), len(gmesh), sum(len(o.data.polygons) for o in gmesh)))
allm = body + worn
act = arm.animation_data.action if arm.animation_data else None
f0, f1 = (int(v) for v in act.frame_range) if act else (1, 2)
nfr = max(1, f1 - f0)
V = []
for o in body:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); lo, hi = V.min(0), V.max(0); H = float(hi[2] - lo[2])
ctr = Vector((0.0, 0.0, float(lo[2] + hi[2]) * 0.5))
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = H * 1.40
FAC = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
el = math.radians(EL)
os.makedirs(OUT, exist_ok=True)
for f in FAC:
    az = math.radians((360 - FAC[f] + YAW) % 360)
    pos = ctr + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                        math.sin(el))) * (10 * H)
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    for i in range(nfr):
        sc.frame_set(f0 + i)
        sc.render.filepath = os.path.join(OUT, "%s_%03d.png" % (f, i))
        bpy.ops.render.render(write_still=True)
json.dump(dict(clip=os.path.basename(CLIP), gear=[os.path.basename(g) for g in GEAR],
               frames=nfr, fps=sc.render.fps, elev=EL, res=RES, yaw=YAW,
               facings=list(FAC), body_faces=sum(len(o.data.polygons) for o in body),
               gear_faces=sum(len(o.data.polygons) for o in worn)),
          open(os.path.join(OUT, "info.json"), "w"), indent=1)
print("rendered %d facings x %d frames (body %d + gear %d faces)"
      % (len(FAC), nfr, sum(len(o.data.polygons) for o in body),
         sum(len(o.data.polygons) for o in worn)))
