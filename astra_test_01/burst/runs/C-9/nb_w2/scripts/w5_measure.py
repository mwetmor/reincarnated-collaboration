# The sword at the GUARD, measured on the shipped files -- the T12 gate's HOLD numbers, adapted to a
# sword, plus penetration and the fist on the named grip feature.
#
#   blender -b -noaudio --python scripts/w5_measure.py -- <nb-body.glb> <sword.glb> <out.json>
#        [--weapon-l axe_l.glb] [--frames 8]
#
# POSE: idle_guard (whose right arm IS axe_guard_R) and walk_armed with the right arm taken from
# axe_guard_R -- the T12 (c) runtime guard layer (RightShoulder..RightHand) that the scene plays,
# weapon_r from the clip's own channel track. grip_R = 1 (the fist closed on the grip).
# HOLD (T12 gate, 53_weapon_gate.py; the speed-split probe's definitions), per frame, his frame
# F forward, U up, R his right (= outboard for the right hand):
#   tilt      the blade (weapon_r +Y) from vertical            sword: 30-60 deg
#   fwd, out  the blade's components along F and R            both > 0 (forward AND outboard)
#   tip_out   (tip - grip) . R, metres                         > 0 (tip outboard of the fist)
#   edge      heading of the edge (weapon_r +Z) on the ground against F, atan2(e.R, e.F)   |edge| <= 45
# PEN: sword vertices inside the body -- odd crossings along ALL SIX axis directions (the T12 PEN
# instrument, second version: two rays are fooled by the body's own overlaps), the fist excluded:
# vertices on the grip (|y_local| <= half the grip) and any vertex within 2 cm of a RightHand-weighted
# body vertex. FIST: the closed hand's centroid (RightHand-weighted verts, grip_R = 1) to main_grip,
# and the angle between the hand's channel (gearlib.hand_frame) and the blade axis.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("w5_measure.py")][0]))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
import gearlib as GL
a = sys.argv[sys.argv.index('--') + 1:]
BODY, SWORD, OUT = a[0], a[1], a[2]
WL = a[a.index('--weapon-l') + 1] if '--weapon-l' in a else None
NF = int(a[a.index('--frames') + 1]) if '--frames' in a else 8
ARM = ("RightShoulder", "RightArm", "RightForeArm", "RightHand")
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = next(o for o in sc.objects if o.type == 'MESH' and o.name.startswith('char1'))
kb = body.data.shape_keys.key_blocks
kb['grip_R'].value = 1.0
if 'helmet_on' in kb: kb['helmet_on'].value = 0.0


def bring(path):
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    add = [o for o in sc.objects if o not in before]
    ms = [o for o in add if o.type == 'MESH' and o.vertex_groups]
    for o in ms:
        for m in o.modifiers:
            if m.type == 'ARMATURE':
                m.object = arm
        mw = o.matrix_world.copy(); o.parent = arm; o.matrix_world = mw
    for o in add:
        if o.type == 'ARMATURE':
            bpy.data.objects.remove(o, do_unlink=True)
    for x in [x for x in bpy.data.actions if x.users == 0 and x.name not in [y.name for y in bpy.data.actions if y.users]]:
        pass
    return ms


sword = bring(SWORD)[0]
wl = bring(WL)[0] if WL else None
MW = arm.matrix_world
# grip half-length for the fist exclusion, from the w3 record beside the sword
rec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(OUT)), "w3_skin.json")))
HALF = rec["features"]["grip_m"] / 2
TIP = rec["sockets"]["main_tip"][1]
gi = {g.index: g.name for g in body.vertex_groups}
rh = np.array([bool(v.groups) and gi.get(max(v.groups, key=lambda x: x.weight).group) == "RightHand"
               for v in body.data.vertices])


def bind(act):
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        arm.animation_data.action_slot = act.slots[0]


def guard_arm():
    """the axe_guard_R pose's matrix_basis for the four right-arm bones"""
    bind(bpy.data.actions['axe_guard_R']); sc.frame_set(int(bpy.data.actions['axe_guard_R'].frame_range[0]))
    bpy.context.view_layer.update()
    return {b: arm.pose.bones[b].matrix_basis.copy() for b in ARM}


GA = guard_arm()
# his frame, Blender: faces -Y, up +Z, his right -X (verified in 07_look.py's convention)
F = np.array([0, -1.0, 0]); U = np.array([0, 0, 1.0]); R = np.array([-1.0, 0, 0])
dirs = [Vector(d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]


def inside(tree, p):
    for d in dirs:
        o = Vector(p.tolist()); n = 0
        for _ in range(24):
            h = tree.ray_cast(o, d, 10.0)
            if h[0] is None:
                break
            n += 1; o = h[0] + d * 1e-4
        if n % 2 == 0:
            return False
    return True


def measure(clip, layer):
    act = bpy.data.actions[clip]; bind(act)
    f0, f1 = (int(round(v)) for v in act.frame_range)
    frames = sorted(set(np.linspace(f0, f1, NF).round().astype(int).tolist()))
    rows = []
    for f in frames:
        sc.frame_set(f)
        if layer:
            for b, m in GA.items():
                arm.pose.bones[b].matrix_basis = m.copy()
        bpy.context.view_layer.update()
        # THE SWORD'S FRAME FROM ITS OWN SKINNED GEOMETRY, not from Blender's bone axes (the importer's
        # bone heuristic may re-orient a bone's local frame): grip = weapon_r's joint (a position, which
        # no heuristic changes), h = grip -> the farthest vertex (the tip, 0.78 m against the pommel's
        # 0.12), e = the blade's widest spread across h (its edge line; double-edged, so its sign is
        # taken nearest his forward).
        grip = np.array(MW @ arm.pose.bones['weapon_r'].head)
        dg = bpy.context.evaluated_depsgraph_get()
        tree = BVHTree.FromObject(body, dg)
        BW = GL.world_verts(body)
        SV = GL.world_verts(sword)
        dd = np.linalg.norm(SV - grip, axis=1); tip = SV[int(np.argmax(dd))]
        h = (tip - grip) / np.linalg.norm(tip - grip)
        bl = SV[((SV - grip) @ h > 0.25) & ((SV - grip) @ h < 0.60)]
        q = (bl - grip) - np.outer((bl - grip) @ h, h); q -= q.mean(0)
        e = np.linalg.eigh(q.T @ q)[1][:, -1]
        if e @ F < 0:
            e = -e
        rel = (SV - grip) @ h
        cand = np.nonzero(np.abs(rel) > HALF)[0][::3]
        rhv = BW[rh]
        pen = []
        for i in cand:
            if np.min(np.linalg.norm(rhv - SV[i], axis=1)) < 0.02:
                continue
            if inside(tree, SV[i]):
                pen.append(i)
        fist = rhv.mean(0)
        rows.append(dict(frame=f, tilt=math.degrees(math.acos(float(np.clip(h @ U, -1, 1)))), fwd=float(h @ F), out=float(h @ R),
                         tip_out=float((tip - grip) @ R), edge=math.degrees(math.atan2(float(e @ R), float(e @ F))),
                         pen=len(pen), fist_to_grip_m=float(np.linalg.norm(fist - grip)), tip_z=float(tip[2]),
                         h=[round(float(v), 5) for v in h], e=[round(float(v), 5) for v in e]))
    ok = [r for r in rows if 30 <= r['tilt'] <= 60 and r['fwd'] > 0 and r['out'] > 0 and r['tip_out'] > 0 and abs(r['edge']) <= 45]
    med = {k: round(float(np.median([r[k] for r in rows])), 3) for k in ('tilt', 'fwd', 'out', 'tip_out', 'edge', 'fist_to_grip_m')}
    res = dict(clip=clip, arm_layer="axe_guard_R" if layer else None, frames=len(rows), at_guard=len(ok),
               median=med, pen_max=max(r['pen'] for r in rows), rows=rows)
    print("  %-11s %s: at guard %d/%d | tilt %.1f fwd %+.2f out %+.2f tip_out %+.3f m edge %+.1f | pen max %d | fist centroid to main_grip %.3f m"
          % (clip, "(+ guard arm)" if layer else "", len(ok), len(rows), med['tilt'], med['fwd'], med['out'], med['tip_out'], med['edge'],
             res['pen_max'], med['fist_to_grip_m']))
    return res


# channel vs blade at rest: the hand's across-palm axis (gearlib.hand_frame) against weapon_r +Y
bpy.context.view_layer.update()
arm.data.pose_position = 'REST'; bpy.context.view_layer.update()
c, chan, al, pal = GL.hand_frame(body, arm, "RightHand")
g0 = np.array(MW @ arm.data.bones['weapon_r'].head_local)
SV0 = GL.world_verts(sword)
t0_ = SV0[int(np.argmax(np.linalg.norm(SV0 - g0, axis=1)))]
h0 = (t0_ - g0) / np.linalg.norm(t0_ - g0)
ch = np.array(chan, float); ch /= np.linalg.norm(ch)
seat = dict(channel_vs_blade_deg=round(math.degrees(math.acos(min(1.0, abs(float(ch @ h0))))), 2),
            channel_centre_to_main_grip_m=round(float(np.linalg.norm(np.array(c) - g0)), 4),
            tip_from_grip_m=round(float(np.linalg.norm(t0_ - g0)), 4))
arm.data.pose_position = 'POSE'
print("  seat at rest: blade vs the fist's channel %.2f deg; channel centre to main_grip %.4f m; tip %.4f m from the grip" % (seat['channel_vs_blade_deg'], seat['channel_centre_to_main_grip_m'], seat['tip_from_grip_m']))
out = dict(seat=seat, idle=measure('idle_guard', False), walk=measure('walk_armed', True))
if wl is not None:
    # the pairing's first look: the off-hand weapon's vertices inside the body, at the idle guard
    act = bpy.data.actions['idle_guard']; bind(act); sc.frame_set(int(act.frame_range[0])); bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); tree = BVHTree.FromObject(body, dg)
    LV = GL.world_verts(wl)
    lhv = GL.world_verts(body)[np.array([bool(v.groups) and gi.get(max(v.groups, key=lambda x: x.weight).group) == "LeftHand" for v in body.data.vertices])]
    pl = [i for i in range(0, len(LV), 3) if np.min(np.linalg.norm(lhv - LV[i], axis=1)) >= 0.02 and inside(tree, LV[i])]
    out['weapon_l_idle_guard_pen'] = len(pl)
    # weapon against weapon: the nearest approach of the two pieces (a thin blade makes parity
    # unreliable, so distance is the number), and which parts meet
    SVi = GL.world_verts(sword)
    from mathutils.kdtree import KDTree        # Blender's own Python has no scipy
    kd = KDTree(len(SVi))
    for i_, p_ in enumerate(SVi):
        kd.insert(Vector(p_.tolist()), i_)
    kd.balance()
    q_ = [kd.find(Vector(p_.tolist())) for p_ in LV[::2]]
    dd = np.array([x[2] for x in q_]); ii = np.array([x[1] for x in q_])
    k = int(np.argmin(dd))
    gs = np.array(MW @ arm.pose.bones['weapon_r'].head)
    out['weapon_to_weapon_min_m'] = round(float(dd[k]), 4)
    out['weapon_to_weapon_where'] = dict(on_sword_from_grip_m=round(float(np.linalg.norm(SVi[ii[k]] - gs)), 3))
    print("  weapon_l piece at idle_guard: %d sampled verts inside the body (left hand excluded); nearest sword-axe approach %.4f m (%.3f m from the sword's grip)"
          % (len(pl), dd[k], out['weapon_to_weapon_where']['on_sword_from_grip_m']))
json.dump(out, open(OUT, "w"), indent=1)
