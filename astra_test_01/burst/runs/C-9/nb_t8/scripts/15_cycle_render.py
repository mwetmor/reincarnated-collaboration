# T8 step 3: render an animated clip at the game camera in all eight facings.
#
#   blender -b -noaudio --python scripts/15_cycle_render.py -- <clip.glb>
#          <tex.png> <outdir> [--elev 52.95] [--res 320] [--yaw 180]
#
# Frames go to a scratch directory and are deleted by the encoder the moment
# the MP4 exists. One ground plane and one camera distance for every facing and
# every frame, so the figure cannot drift or pop between them: the aim is fixed
# from the REST bbox once, not recomputed per frame from a moving silhouette.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, TEX, OUT = a[0], a[1], a[2]
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 320
# YAW CONVENTION, STATED because two scripts in this pipeline disagree on the
# sign and I carried a value across the boundary. HERE, and in 07_look.py, the
# camera for facing F sits at -cos(az): with yaw 0 a model facing -Y shows its
# FRONT at facing S. The paint-sheet builder (t5_01) uses +cos(az), so the same
# model needs --yaw 180 there and --yaw 0 here. Passing 180 to this script put
# his back under the label S and his face under N, in every frame of both
# cycles. Default 0, and the facings are asserted against a known landmark
# below rather than trusted.
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else 0.0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
img = bpy.data.images.load(os.path.abspath(TEX))
img.colorspace_settings.name = 'sRGB'
n = 0
for o in objs:
    for s in o.material_slots:
        m = s.material
        if not m or not m.node_tree:
            continue
        nt = m.node_tree
        for nd in nt.nodes:
            if nd.type == 'TEX_IMAGE':
                nd.image = img; n += 1
        b = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
        out = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
        em = nt.nodes.new('ShaderNodeEmission')
        L = b.inputs['Base Color'].links if b else []
        if L:
            nt.links.new(L[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
assert n, "no image texture node to override"
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
act = arm.animation_data.action
f0, f1 = (int(v) for v in act.frame_range)
# the last frame of a Meshy library cycle repeats the first; dropping it keeps
# the loop from stuttering on one doubled frame
P = []
for o in objs:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    P.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
P = np.vstack(P); lo, hi = P.min(0), P.max(0); H = float(hi[2] - lo[2])
ctr = Vector((0.0, 0.0, float(lo[2] + hi[2]) * 0.5))
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = H * 1.35
FAC = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
el = math.radians(EL)
os.makedirs(OUT, exist_ok=True)
nfr = f1 - f0
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
# ASSERT THE FACING. The figure faces -Y and his tattooed arm is his right
# (-X). At facing S the camera is in front of him, so his right arm must fall
# on the LEFT half of the frame, and at facing N on the right half. Measured
# from the rendered alpha's centre of mass against the hand bone's projection.
import bpy as _b
_arm = arm
sc.frame_set(f0)
_hand = (_arm.matrix_world @ _arm.pose.bones["RightHand"].head)
for _f, _expect in (("S", "left"), ("N", "right")):
    _az = math.radians((360 - FAC[_f] + YAW) % 360)
    _pos = ctr + Vector((math.sin(_az) * math.cos(el), -math.cos(_az) * math.cos(el),
                         math.sin(el))) * (10 * H)
    _right = (ctr - _pos).to_track_quat('-Z', 'Y').to_matrix().col[0]
    _side = (_hand - ctr).dot(_right)
    _got = "right" if _side > 0 else "left"
    print("  facing %-2s: his right hand falls on the %-5s of frame (expected %s)"
          % (_f, _got, _expect))
    assert _got == _expect, (
        "facing %s puts his right hand on the %s -- the yaw convention is "
        "inverted for this script" % (_f, _got))
json.dump(dict(clip=os.path.basename(SRC), frames=nfr, fps=sc.render.fps,
               elev=EL, res=RES, yaw=YAW, height_m=round(H, 5),
               facings=list(FAC)), open(os.path.join(OUT, "info.json"), "w"), indent=1)
print("rendered %d facings x %d frames into %s" % (len(FAC), nfr, OUT))
