# Acceptance for the staff hold, on the SEATED staff, per clip, per frame.
#
#   blender -b -noaudio --python scripts/s12_measure.py -- <seated_full.glb> <staff_carry.json> <out.json>
#        [--clips idle,walk,run] [--raw cast_fireball,cast_meteor]
#
# COMPOSITE = the clip's pose for every bone, then the carry pose's LOCAL transforms written over the
# filtered bones -- what a filtered Blend2 at weight 1 does, and what knight.gd's split does.
#   tilt     the shaft (weapon_r +Y) off world vertical, max over the loop -- accept <= 20 deg
#   tip      the crown's screen path over one loop at the PLAY CAMERA (100.6 px/m, pitch 52.95, yaw
#            47), both as total path length and as its extent -- accept <= 60 px -- taken at four
#            headings (25, 115, 205, 295) because her facing changes what the camera sees of it
#   inside   staff vertices inside the body by crossing parity, named by the body part they are in;
#            RightHand is the GRIP -- a shaft inside a closed fist is the point -- and is reported
#            apart, never counted as penetration
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s12_measure.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, CARRY, OUT = a[0], a[1], a[2]
CLIPS = [c for c in (a[a.index('--clips') + 1] if '--clips' in a else "idle,walk,run").split(",") if c and c != "none"]
RAW = (a[a.index('--raw') + 1] if '--raw' in a else "").split(",") if '--raw' in a else []
car = json.load(open(CARRY))
CB = {b: Matrix([m[i * 4:(i + 1) * 4] for i in range(4)]) for b, m in car["bones"].items()}
# --arm-only <clips>: apply the carry to the STAFF ARM only (RightShoulder..RightHand), leaving the
# spine and the left arm to the clip -- for a cast thrown from the free left hand.
ARM_ONLY = set((a[a.index('--arm-only') + 1] if '--arm-only' in a else "").split(",")) - {""}
ARM_BONES = ("RightShoulder", "RightArm", "RightForeArm", "RightHand")
# --upright <clips>: after the clip's pose, turn weapon_r by the minimal rotation that puts the shaft
# on world vertical, crown up -- the staff follows the fist but stays upright (raise, then stamp).
UPRIGHT = set((a[a.index('--upright') + 1] if '--upright' in a else "").split(",")) - {""}
# --blend <clips>: SEATED while the fist is high (the shaft across the fist clears a raised arm),
# UPRIGHT as it comes down (a stamp clears the legs). w = smoothstep of the fist's height between
# the shoulder (w=0) and the hips (w=1); the staff turns by slerp(identity, R_upright, w).
BLEND = set((a[a.index('--blend') + 1] if '--blend' in a else "").split(",")) - {""}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
FPS = float(sc.render.fps)
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
meshes = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
body = next(o for o in meshes if o.name.startswith("char1"))
staff = next(o for o in meshes if "staff" in o.name.lower())
MW = arm.matrix_world
gi = {g.index: g.name for g in body.vertex_groups}
BD = np.array([gi.get(max(v.groups, key=lambda x: x.weight).group, "?") if v.groups else "?" for v in body.data.vertices])
# play camera, carried from Godot (Y-up) into Blender (Z-up): (X, Y, Z)_godot = (x, z, -y)_blender
p, y_ = math.radians(52.95354112560294), math.radians(47.0)
fG = np.array([-math.sin(y_) * math.cos(p), -math.sin(p), -math.cos(y_) * math.cos(p)])
fB = np.array([fG[0], -fG[2], fG[1]])
right = np.cross(fB, [0, 0, 1]); right /= np.linalg.norm(right)
upS = np.cross(right, fB); upS /= np.linalg.norm(upS)
PPM = 100.617553710938
bpy.context.view_layer.update()
HEAD_REST = float((arm.matrix_world @ arm.data.bones["Head"].head_local).z)


def bind(act):
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        arm.animation_data.action_slot = act.slots[0]


def upright(w=1.0):
    wb = arm.pose.bones["weapon_r"]
    Mw = MW @ wb.matrix
    cur = (Mw.to_3x3() @ Vector((0, 1, 0))).normalized()
    tgt = Vector((0, 0, 1))
    LEAN = float(a[a.index('--lean') + 1]) if '--lean' in a else 0.0
    if LEAN:
        # crown leans AWAY from her: along the horizontal line from her hips through the fist,
        # by LEAN degrees x w -- so the high fist (w~0) is untouched and the slam leans fully
        # LATERAL, to her right: forward lean cleared the head but ran through her thighs, which
        # are IN FRONT of the fist in a ground-slam crouch (44 -> 134 verts as the lean grew)
        if '--lean-dir' in a and a[a.index('--lean-dir') + 1] == 'forward':
            o = (MW @ arm.pose.bones["RightHand"].head) - (MW @ arm.pose.bones["Hips"].head)
        else:
            o = (MW @ arm.pose.bones["RightArm"].head) - (MW @ arm.pose.bones["LeftArm"].head)
        o.z = 0.0
        if o.length > 1e-6:
            # the lean follows the CROUCH (her head dropping toward the slam), not the fist: the fist
            # is below the hips at the clip's START too, arm hanging, and a slam-sized lean there tipped
            # the butt into her own thigh. HEAD_REST is her standing head height.
            hz = (MW @ arm.pose.bones["Head"].head).z
            cw = min(1.0, max(0.0, (HEAD_REST - hz) / max(HEAD_REST - 0.90, 1e-6)))
            cw = cw * cw * (3 - 2 * cw)
            BASE = float(a[a.index('--lean-base') + 1]) if '--lean-base' in a else 0.0
            o.normalize(); th = math.radians(BASE + (LEAN - BASE) * cw)
            tgt = Vector((0, 0, 1)) * math.cos(th) + o * math.sin(th)
    q = cur.rotation_difference(tgt)
    if w < 1.0:
        from mathutils import Quaternion
        q = Quaternion().slerp(q, w)
    R = q.to_matrix().to_4x4()
    t = Mw.translation.copy()
    wb.matrix = MW.inverted() @ (Matrix.Translation(t) @ R @ Matrix.Translation(-t) @ Mw)


def blend_w():
    z = lambda n: (MW @ arm.pose.bones[n].head).z
    zs, zh, zf = z("RightArm"), z("Hips"), z("RightHand")
    x = min(1.0, max(0.0, (zs - zf) / max(zs - zh, 1e-6)))
    return x * x * (3 - 2 * x)


def frame_state(carry, arm_only=False, up=False, blend=False):
    if up:
        bpy.context.view_layer.update(); upright()
    if blend:
        bpy.context.view_layer.update(); upright(blend_w())
    if carry:
        for b, m in CB.items():
            if arm_only and b not in ARM_BONES:
                continue
            arm.pose.bones[b].matrix_basis = m.copy()
    bpy.context.view_layer.update()
    wb = arm.pose.bones["weapon_r"]
    s = ((MW @ wb.matrix).to_3x3() @ Vector((0, 1, 0))).normalized()
    SV = G.world_verts(staff)
    tip = SV[np.argmax(SV @ np.array(s))]
    return s, tip, SV


DEPTH = [0.0]
FDEPTH = [0.0]
GRIP_R = 0.10      # staff vertices within this of the grip are the GRIP REGION: a shaft leaving a
                   # closed fist passes the wrist, whose vertices are forearm-weighted


def grip_pt():
    return np.array((MW @ arm.pose.bones["weapon_r"].matrix).translation)


def inside(SV):
    dg = bpy.context.evaluated_depsgraph_get()
    bt = BVHTree.FromObject(body, dg); ev = body.evaluated_get(dg)
    binv = ev.matrix_world.inverted()
    BV = G.world_verts(body)
    up = Vector((0, 0, 1)); parts = {}
    GP = grip_pt()
    for q in SV[::4]:
        o = binv @ Vector(q.tolist()); h_ = 0
        for _ in range(24):
            hit = bt.ray_cast(o, up, 10.0)
            if hit[0] is None: break
            h_ += 1; o = hit[0] + up * 1e-4
        if h_ % 2:
            hn = bt.find_nearest(binv @ Vector(q.tolist()))
            if hn[0] is not None and np.linalg.norm(q - GP) >= GRIP_R:      # grip region excluded
                _dd = float((ev.matrix_world @ hn[0] - Vector(q.tolist())).length)
                DEPTH[0] = max(DEPTH[0], _dd); FDEPTH[0] = max(FDEPTH[0], _dd)
            k = BD[int(np.argmin(np.linalg.norm(BV - q, axis=1)))]
            if np.linalg.norm(q - GP) < GRIP_R:
                k = "RightHand"                       # grip region: reported apart
            parts[k] = parts.get(k, 0) + 1
    return parts


rep = {}
LHD = []
for cn, carry in [(c, False) for c in BLEND] + [(c, False) for c in UPRIGHT] + [(c, True) for c in CLIPS] + [(c, True) for c in ARM_ONLY] + [(c, False) for c in CLIPS if '--no-raw' not in a] + [(c, False) for c in RAW if c]:
    act = bpy.data.actions[cn]
    bind(act)
    f0, f1 = (int(round(v)) for v in act.frame_range)
    tilts, tips, pen = [], [], {}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        s, tip, SV = frame_state(carry, arm_only=(cn in ARM_ONLY), up=(cn in UPRIGHT and cn not in BLEND), blend=(cn in BLEND))
        tilts.append(math.degrees(math.acos(max(-1, min(1, s.z)))))
        tips.append(np.array(tip))
        if (f - f0) % 3 == 0 or '--perframe' in a:
            FDEPTH[0] = 0.0
            _pp = inside(SV)
            for k, v in _pp.items():
                pen[k] = max(pen.get(k, 0), v)
            _real = {str(k): v for k, v in _pp.items() if k != "RightHand"}
            if '--perframe' in a:
                # the off hand to the shaft (segment), for the two-handed IK window
                wb = arm.pose.bones["weapon_r"]; Mw = MW @ wb.matrix
                o_ = np.array(Mw.translation); d_ = np.array(Mw.to_3x3() @ Vector((0, 1, 0)))
                L_ = np.array(MW @ arm.pose.bones["LeftHand"].head)
                tt = float(np.clip((L_ - o_) @ d_, -0.96, 0.79))
                # can the LEFT ARM reach the shaft at all? shoulder to the nearest point of the band
                # 0.15-0.40 m above the right grip, against the arm's own reach (upper + fore)
                Sh = np.array(MW @ arm.pose.bones["LeftArm"].head)
                # from WORLD joint positions: bone head/tail are armature units, and the first
                # version read a 50.4 m arm off them
                _j = lambda n: np.array(MW @ arm.pose.bones[n].head)
                reach = float(np.linalg.norm(_j("LeftForeArm") - _j("LeftArm")) + np.linalg.norm(_j("LeftHand") - _j("LeftForeArm")))
                band = [o_ + u * d_ for u in np.linspace(0.15, 0.40, 6)]
                need = min(float(np.linalg.norm(Sh - b)) for b in band)
                LHD.append((f, (f - f0) / FPS, float(np.linalg.norm(L_ - (o_ + tt * d_))), tt, need, reach))
            if '--perframe' in a and _real:
                print("    f%3d t=%.2fs depth %.4f m fist z %.2f head z %.2f %s-> %s" % (
                    f, (f - f0) / FPS, FDEPTH[0], (MW @ arm.pose.bones['RightHand'].head).z,
                    (MW @ arm.pose.bones['Head'].head).z,
                    ("w=%.2f " % blend_w()) if cn in BLEND else "", _real))
    T = np.array(tips)
    best = {}
    for hd in (25, 115, 205, 295):
        r = math.radians(hd)
        Rz = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])
        Tr = T @ Rz.T
        sx, sy = Tr @ right * PPM, Tr @ upS * PPM
        path = float(np.sum(np.hypot(np.diff(sx), np.diff(sy))))
        ext = float(np.hypot(np.ptp(sx), np.ptp(sy)))
        best[hd] = dict(path_px=round(path, 1), extent_px=round(ext, 1))
    key = "%s%s" % (cn, (" (STAFF ARM carry only)" if cn in ARM_ONLY else "") if carry else (" (weapon_r SEATED->UPRIGHT by fist height)" if cn in BLEND else (" (weapon_r UPRIGHT)" if cn in UPRIGHT else " (raw clip, no carry)")))
    grip = pen.pop("RightHand", 0)
    rep[key] = dict(frames=[f0, f1], tilt_max_deg=round(max(tilts), 2), tilt_mean_deg=round(float(np.mean(tilts)), 2),
                    tip_screen=best, tip_path_px_worst=max(v["path_px"] for v in best.values()),
                    tip_extent_px_worst=max(v["extent_px"] for v in best.values()),
                    staff_in_body_by_part=pen, staff_in_body_worst=sum(pen.values()), shaft_in_grip_hand=grip)
    r = rep[key]
    print("  %-34s tilt max %6.2f deg (mean %5.2f) | tip path %6.1f px, extent %5.1f px | inside body %3d %s | in the grip %d"
          % (key, r["tilt_max_deg"], r["tilt_mean_deg"], r["tip_path_px_worst"], r["tip_extent_px_worst"],
             r["staff_in_body_worst"], pen or "", grip))
if '--perframe' in a:
    print("  max penetration DEPTH over every inside vertex: %.4f m" % DEPTH[0])
    if LHD:
        dmin = min(LHD, key=lambda r: r[2])
        near = [r for r in LHD if r[2] < 0.30]
        print("  off hand to shaft: min %.3f m at %.2fs (along shaft %+.2f m from the grip); frames within 0.30 m: %s"
              % (dmin[2], dmin[1], dmin[3], ["%.2f" % r[1] for r in near][:40]))
        ok = [r for r in LHD if r[4] <= 0.92 * r[5]]
        print("  left-arm REACH %.3f m; shaft band reachable (<= 92%% of reach) at %d of %d frames: %s"
              % (LHD[0][5], len(ok), len(LHD), ["%.2f" % r[1] for r in ok]))
        json.dump(dict(off_hand_to_shaft=[dict(f=r[0], t=round(r[1], 4), dist_m=round(r[2], 4), along_m=round(r[3], 4),
                                                shoulder_to_band_m=round(r[4], 4), reach_m=round(r[5], 4)) for r in LHD],
                       max_depth_m=round(DEPTH[0], 4)), open(OUT.replace('.json', '_perframe.json') if OUT != '/dev/null' else '/dev/null', 'w'), indent=1)
json.dump(rep, open(OUT, "w"), indent=1)
