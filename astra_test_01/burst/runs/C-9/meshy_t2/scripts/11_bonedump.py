# C-9 meshy_t2 step 9a: dump bone world positions and the E camera's matrix for
# every frame of every clip, so the contact sheet can draw the skeleton on top
# of the sprites that were actually rendered.
#
#   blender -b -noaudio --python scripts/11_bonedump.py -- <clips.blend> <out.json>
#
# The camera is rebuilt here with exactly the placement 08_render.py used
# (same px/m, same aim height, same per-frame hips tracking), and the matrix
# is dumped rather than re-derived on the drawing side -- a bone drawn from a
# reconstructed camera would agree with the render only as long as nobody
# edited either.
import bpy, json, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("11_bonedump.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTP = a[0], a[1]

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
clips = json.load(open(os.path.join(os.path.dirname(BLEND), "clips.json")))
gref = clips.get("ground_ref_z", 0.0)
el = math.radians(T.ELEV)
aim_z = (T.SOLE_Y - T.FRAME / 2.0) / (T.PX_PER_M * math.cos(el)) + gref
AIM_Y = -float(arm.data.bones["hips"].head_local.y)

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
cam.data.ortho_scale = T.FRAME / T.PX_PER_M
hips = arm.pose.bones["hips"]

out = dict(frame=T.FRAME, ortho_scale=T.FRAME / T.PX_PER_M, px_per_m=T.PX_PER_M,
           sole_y=T.SOLE_Y, aim_z=aim_z, clips={})
for state in ("idle", "walk", "run", "attack"):
    act = bpy.data.actions.get("mc_" + state)
    arm.animation_data_create()
    arm.animation_data.action = act
    try:
        sl = list(act.slots)
        if sl:
            arm.animation_data.action_slot = sl[0]
    except Exception:
        pass
    n = clips[state]["frames"]
    rows = []
    for i in range(n):
        sc.frame_set(i + 1)
        hw = arm.matrix_world @ hips.head
        per_dir = {}
        for d in T.DIRS:
            T.place_camera(cam, T.AZI[d], (hw.x, hw.y + AIM_Y), aim_z)
            bpy.context.view_layer.update()
            per_dir[d] = [list(r) for r in cam.matrix_world.inverted()]
        rows.append(dict(
            cams=per_dir,
            bones={b.name: dict(head=[round(v, 5) for v in (arm.matrix_world @ b.head)],
                                tail=[round(v, 5) for v in (arm.matrix_world @ b.tail)])
                   for b in arm.pose.bones}))
    out["clips"][state] = dict(frames=rows,
                               extreme=[], n=n)
json.dump(out, open(OUTP, "w"))
print("wrote", OUTP)
