# D2 step 4: socket a weapon to a bone.
#
#   blender -b -noaudio --python scripts/11_weapon.py -- <weapon.glb>
#     <base.glb> <out.json> --bone RightHand --length 0.82 --grip 0.30
#     [--yaw -90] [--roll 0] [--pitch 0] [--push 0.0]
#
# The weapon arrives from Tripo height-normalised to 1.0 and yawed, so it is
# measured first: its own long axis, its own extent, and where along that axis
# a hand would close on it. Then it is scaled to a real weapon's length, laid
# along the bone's axis, and offset so the GRIP lands on the bone's head.
#
# The lead-hand rule from the knight's pollaxe applies to the axe: at the
# strike frame the cutting edge has to be FORWARD of the hand along the
# character's facing, or the swing is delivered backwards. That is asserted
# here rather than eyeballed, because a reversed thrust looked perfectly
# plausible in a still the first time.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
WEAPON, BASE, OUTJ = a[0], a[1], a[2]
BONE = a[a.index("--bone") + 1] if "--bone" in a else "RightHand"
LENGTH = float(a[a.index("--length") + 1]) if "--length" in a else 0.82
GRIP = float(a[a.index("--grip") + 1]) if "--grip" in a else 0.30
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else -90.0
ROLL = float(a[a.index("--roll") + 1]) if "--roll" in a else 0.0
PITCH = float(a[a.index("--pitch") + 1]) if "--pitch" in a else 0.0
PUSH = float(a[a.index("--push") + 1]) if "--push" in a else 0.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=WEAPON)
sc = bpy.context.scene
w = max([o for o in sc.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
w.matrix_world = Matrix.Rotation(math.radians(YAW), 4, 'Z') @ w.matrix_world
bpy.context.view_layer.update()
co = np.empty(len(w.data.vertices) * 3); w.data.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ np.array(w.matrix_world.to_3x3()).T + np.array(w.matrix_world.translation)
span = V.max(0) - V.min(0)
LA = int(np.argmax(span))
s = LENGTH / span[LA]
print("weapon %s: %d verts, span %s, long axis %s, scale x%.4f"
      % (os.path.basename(WEAPON), len(V), np.round(span, 4), "XYZ"[LA], s))
# measure the thickness profile along the long axis: the HEAD is the fat end
t = (V[:, LA] - V[:, LA].min()) / max(span[LA], 1e-9)
others = [i for i in range(3) if i != LA]
prof = []
for k in range(10):
    sel = (t >= k / 10) & (t < (k + 1) / 10)
    if sel.sum() < 10:
        prof.append(0.0); continue
    q = V[sel][:, others]
    prof.append(float(np.prod(q.max(0) - q.min(0))))
head_at_max = float(np.mean(prof[7:])) > float(np.mean(prof[:3]))
print("   cross-section by decile %s -> head at %s end"
      % (np.round(np.array(prof) / max(prof), 2).tolist(),
         "MAX" if head_at_max else "MIN"))
json.dump(dict(weapon=os.path.basename(WEAPON), bone=BONE, yaw=YAW, roll=ROLL,
               pitch=PITCH, length_m=LENGTH, grip_frac=GRIP, push=PUSH,
               long_axis="XYZ"[LA], scale=round(float(s), 6),
               span_m=[round(float(v * s), 4) for v in span],
               head_end="max" if head_at_max else "min",
               profile=[round(float(p / max(prof)), 3) for p in prof]),
          open(OUTJ, "w"), indent=1)
print("wrote %s" % OUTJ)
