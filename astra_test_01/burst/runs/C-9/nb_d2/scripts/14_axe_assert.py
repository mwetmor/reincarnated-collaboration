# D2: does the axe's cutting edge LEAD the slash?
#
#   blender -b -noaudio --python scripts/14_axe_assert.py -- <attack.glb> <out.json>
#
# The knight's pollaxe taught half of this: a reversed weapon looks perfectly
# plausible in a still, and only the sign along the swing tells you.
#
# The other half is that A SLASH'S STRIKE IS NOT A THRUST'S. The pollaxe test
# took the strike to be the frame where the weapon HAND reaches furthest
# forward, which is right for a thrust and wrong here: at that frame (14) this
# clip has the hand punched out and the blade still trailing by 0.52 m, and the
# blade whips past it two frames later to lead by 0.59. Judged by the hand, a
# correctly-oriented axe FAILS. The strike of a cut is where the EDGE reaches
# furthest forward, so that is what is measured -- and the hand-forward frame
# is reported beside it, because the difference between them is the swing.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("14_axe_assert.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
CLIP, OUTJ = a[0], a[1]
ROOT = os.path.dirname(HERE)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "builds", "axe.glb"), before)
G.decimate(pc, 9000)
info = G.socket_weapon2(pc, arm, "RightHand", 0.82, 0.22,
                        axis_world=(0, 0, 1), face_world=(0, -1, 0))
G.align_space(pc, body[0])
bpy.context.view_layer.update()
act = arm.animation_data.action
f0, f1 = (int(v) for v in act.frame_range)
fwd = np.array([0.0, -1.0, 0.0])          # he faces -Y
dg = bpy.context.evaluated_depsgraph_get()
rows = []
for i in range(f1 - f0):
    sc.frame_set(f0 + i)
    dg = bpy.context.evaluated_depsgraph_get()
    hand = np.array(arm.matrix_world @ arm.pose.bones["RightHand"].head)
    pel = np.array(arm.matrix_world @ arm.pose.bones["Hips"].head)
    eo = pc.evaluated_get(dg); me = eo.to_mesh()
    cv = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", cv)
    V = (cv.reshape(-1, 3) @ np.array(eo.matrix_world.to_3x3()).T
         + np.array(eo.matrix_world.translation))
    # the cutting EDGE: the vertex furthest from the hand, at the head end
    d = np.linalg.norm(V - hand, axis=1)
    edge = V[int(np.argmax(d))]
    eo.to_mesh_clear()
    rows.append(dict(i=i, hand_fwd=float(hand @ fwd),
                     edge_beyond_hand=float((edge - hand) @ fwd),
                     edge_fwd_of_pelvis=float((edge - pel) @ fwd),
                     edge_z=float(edge[2])))
hand_frame = max(range(len(rows)), key=lambda k: rows[k]["hand_fwd"])
strike = max(range(len(rows)), key=lambda k: rows[k]["edge_fwd_of_pelvis"])
r = rows[strike]
leads = [x["i"] for x in rows if x["edge_beyond_hand"] > 0]
print("edge leads the hand in %d of %d frames; max lead %+0.3f m at frame %d"
      % (len(leads), len(rows),
         max(x["edge_beyond_hand"] for x in rows),
         max(rows, key=lambda x: x["edge_beyond_hand"])["i"]))
print("hand reaches furthest forward at frame %d (a thrust's strike); the EDGE "
      "does at frame %d (a cut's)" % (hand_frame, strike))
ok_lead = r["edge_beyond_hand"] > 0
ok_fwd = r["edge_fwd_of_pelvis"] > 0
print("strike frame %d of %d" % (strike, len(rows)))
print("  cutting edge %+0.4f m beyond the hand along forward   %s"
      % (r["edge_beyond_hand"], "LEADS" if ok_lead else "*** TRAILS ***"))
print("  cutting edge %+0.4f m forward of the pelvis           %s"
      % (r["edge_fwd_of_pelvis"], "OK" if ok_fwd else "*** BEHIND ***"))
print("  head height at rest frame 0: edge z %.3f m (idle should ride high)"
      % rows[0]["edge_z"])
json.dump(dict(strike_frame=strike, hand_forward_frame=hand_frame,
               frames_leading=len(leads), frames=len(rows), leads=bool(ok_lead),
               forward_of_pelvis=bool(ok_fwd), strike=r, socket=info,
               per_frame=rows), open(OUTJ, "w"), indent=1)
