# C-9 meshy_t1 steps 3+4: render a Meshy clip to the game's sprite format, in
# all eight directions, with the EbSynth guide passes baked in the same pass.
#
#   blender -b -noaudio --python scripts/04_render.py -- <clip.glb> <clipinfo.json>
#                        <state> <outdir> [--dirs S,SE,...] [--weapon <socket.json>]
#
# Generic rules, all measured rather than assumed:
#
#  * SCALE from the character, not the scene. px/m = 198.33 / character height,
#    where the height is the skinned meshes' bbox and the unskinned stray
#    (`Icosphere`) is excluded. For this knight 1.80 m -> 110.185 px/m. Taking
#    it off the scene bbox would give 2.8 m and a figure a third too small.
#
#  * FACING measured, not assumed. The direction the character faces is read
#    off the clip -- a planted foot slides BACKWARD, so facing is the opposite
#    of the stance foot's travel -- and the model is rotated so its facing is
#    +Y before the game's azimuth convention (S=0, SE=45, E=90 ...) is applied.
#    A rig that ships facing another way therefore needs no code change.
#
#  * GROUND ROW calibrated over the WHOLE cycle, not one probe frame: the sole
#    line the eye reads is the lowest one over the loop.
#
#  * GUIDES as baked vertex colours. `pos` is the REST (bind) vertex position
#    normalised over the bind bbox -- the StyLit-style "where on the body"
#    guide, invariant to the animation because it is stored per vertex before
#    skinning. `part` is a flat colour per DOMINANT BONE GROUP, which is the
#    single-skinned-mesh analogue of the per-piece guide. Both render unlit,
#    so they arrive flat.
import bpy, colorsys, json, math, os, re, sys
import numpy as np
from mathutils import Vector, Matrix, Euler

a = sys.argv[sys.argv.index('--') + 1:]
SRC, INFO, STATE, OUTDIR = a[0], a[1], a[2], a[3]
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
if "--dirs" in a:
    DIRS = a[a.index("--dirs") + 1].split(",")
SOCKET = a[a.index("--weapon") + 1] if "--weapon" in a else None
# ONE CHARACTER, ONE SCALE. The height must come from the BIND pose, not from
# the clip: measured per clip, this knight is 1.8242 m in the walk and 1.8007 m
# in the run, so walk and run would render the same character at two different
# sizes and the sprites would pop between states.
HEIGHT = float(a[a.index("--height") + 1]) if "--height" in a else None
# NEGATIVE CONTROL for the thrust assert. Reverses the hand line, reproducing the
# defect the assert exists to catch. An assert that passes on the broken version
# is not an assert, so this flag stays in the script rather than being a patch
# someone applied once and threw away. Never use it for a delivered render.
FLIP_HAND_LINE = "--flip-hand-line" in a
# run the asserts and stop, without spending the render
ASSERT_ONLY = "--assert-only" in a
# CARRY POSE. A library locomotion clip swings both arms freely, so a weapon
# socketed to the hand swings with it -- measured on this walk, the pollaxe
# reaches near-horizontal and points backwards by frame 8. That is not a
# carry; the approved stills hold it upright. With --carry the weapon arm is
# IK-solved to a grip point carried in the CHEST's frame, so the hand holds
# station against the torso while every other channel of the mocap is
# untouched. Off by default: it changes the authored motion, which is a design
# call, not a rendering one.
CARRY = "--carry" in a
# UPRIGHT. A socket fitted in the bind pose carries the bind wrist with it, so
# on a clip whose hand is authored differently the haft comes out at whatever
# angle that wrist implies -- measured on the text-to-motion carry walk, the
# pollaxe lay HORIZONTAL across the body while the grip itself was perfect.
# With --upright the socket's ROTATION is re-solved from the clip's own mean
# wrist orientation so the haft stands vertical, and the fan keeps its bearing.
UPRIGHT = "--upright" in a
# ALIGN-HANDS. --upright is wrong for a thrust: it would hold the haft vertical
# through an attack that drives it forward. A two-handed polearm's haft lies
# along the line BETWEEN THE HANDS, so for the attack the socket rotation is
# solved to put the weapon's own long axis on that line -- which is also what
# makes the haft pass through both gauntlets.
ALIGN_HANDS = "--align-hands" in a
# FACING IS A PROPERTY OF THE RIG, NOT OF THE CLIP. Derived per clip it is
# right for locomotion and NOISE for anything else: this knight's idle gave
# -90 deg from a 0.0001 m stance displacement and rendered facing the camera in
# every direction. Measured once on the walk and passed in here.
FACE = float(a[a.index("--face") + 1]) if "--face" in a else None
MIN_DISP = 0.15
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
# ONE camera, read from meshy_t1/camera.json so the integration session and
# this pipeline cannot drift apart. BODY_PX is no longer a stored constant: the
# scale comes from the measured px/m.
_CAM = json.load(open(os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "camera.json")))
FRAME = _CAM["frame_px"]
PX_PER_M = _CAM["px_per_m"]
BODY_PX = PX_PER_M * _CAM["character_height_m"]
SOLE_Y = _CAM["ground_row_y"]
ELEV = _CAM["elevation_deg"]


def skinned(sc, arm):
    return [o for o in sc.objects if o.type == 'MESH'
            and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers)]


def unlit(objs, attr=None):
    """Emission shading. With `attr`, emit a named vertex-colour layer."""
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.use_nodes:
                continue
            nt = m.node_tree
            out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            if attr:
                at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = attr
                nt.links.new(at.outputs['Color'], em.inputs['Color'])
            else:
                bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if bsdf and bsdf.inputs['Base Color'].links:
                    nt.links.new(bsdf.inputs['Base Color'].links[0].from_socket,
                                 em.inputs['Color'])
            nt.links.new(em.outputs['Emission'], out.inputs['Surface'])


def bake_guides(objs, arm):
    """Two vertex-colour layers on the REST mesh: `gpos` and `gpart`."""
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for o in objs:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    span = Vector([max(hi[i] - lo[i], 1e-6) for i in range(3)])
    bones = [b.name for b in arm.data.bones]
    pal = {}
    for i, b in enumerate(bones):
        h = ((i * 7) % len(bones)) / len(bones)
        s = 0.85 + 0.15 * ((i % 3) / 2.0); v = 0.70 + 0.30 * (i % 2)
        pal[b] = colorsys.hsv_to_rgb(h, s, v)
    for o in objs:
        me = o.data
        gi = {g.index: g.name for g in o.vertex_groups}
        cp = me.color_attributes.new(name="gpos", type='FLOAT_COLOR', domain='POINT')
        cq = me.color_attributes.new(name="gpart", type='FLOAT_COLOR', domain='POINT')
        for v in me.vertices:
            w = o.matrix_world @ v.co
            cp.data[v.index].color = ((w.x - lo.x) / span.x, (w.y - lo.y) / span.y,
                                      (w.z - lo.z) / span.z, 1.0)
            best, bw = None, -1.0
            for g in v.groups:
                if g.weight > bw:
                    bw = g.weight; best = gi.get(g.group)
            c = pal.get(best, (0.5, 0.5, 0.5))
            cq.data[v.index].color = (c[0], c[1], c[2], 1.0)
    return dict(bind_bbox_lo=[round(v, 5) for v in lo],
                bind_bbox_span=[round(v, 5) for v in span],
                bone_colours={b: [round(c, 4) for c in pal[b]] for b in bones})


def fit_upright_socket(arm, R, sk, info, times, align_hands=False):
    """Re-solve the socket's rotation so the haft stands UPRIGHT in this clip.

    The weapon's world rotation is (hand world rotation) x (socket rotation).
    Averaging the hand's rotation over the cycle and asking for a weapon whose
    local +Z is world +Z, with the fan at its target bearing, gives
        socket = mean_hand_rotation^-1 x desired_world_rotation
    so the haft is vertical on average and wobbles only as the wrist does,
    which is what a carried polearm looks like.
    """
    hand = R.get("r_hand")
    if not hand:
        return None
    sc = bpy.context.scene
    qs = []
    for t in times:
        sc.frame_set(int(t), subframe=float(t) - int(t))
        qs.append((arm.matrix_world @ arm.pose.bones[hand].matrix).to_quaternion())
    ref = qs[0]
    acc = Vector((0.0, 0.0, 0.0, 0.0))
    for q in qs:
        if q.dot(ref) < 0:
            q = -q
        acc += Vector((q.w, q.x, q.y, q.z))
    from mathutils import Quaternion
    mq = Quaternion((acc.x, acc.y, acc.z, acc.w))
    mq.normalize()
    bearing = sk["fit"].get("carry_fan_bearing_deg", sk["fit"]["target_fan_bearing_deg"])
    fan_local = sk["fit"]["weapon_fan_local_bearing_deg"]
    if align_hands:
        # THE SIGN ALONG THE HAND LINE MATTERS. Aligning to (other hand - weapon
        # hand) put the axe head and spear point BEHIND the helm and drove the
        # butt cap forward: a reversed thrust. The head must lie beyond the LEAD
        # hand, so the line is taken from the REAR hand to the LEAD one.
        #
        # Lead and rear are decided ONCE, at the strike frame -- the frame where
        # a hand reaches furthest along the character's forward axis -- and held
        # for the whole clip. Deciding per frame would flip the weapon end over
        # end as the hands cross.
        oh = R.get("l_hand"); wh = R.get("r_hand")
        fwd = Vector((0.0, 1.0, 0.0))          # facing is normalised to +Y
        poses = []
        for t in times:
            sc.frame_set(int(t), subframe=float(t) - int(t))
            poses.append((arm.matrix_world @ arm.pose.bones[wh].head,
                          arm.matrix_world @ arm.pose.bones[oh].head))
        strike = max(range(len(poses)),
                     key=lambda i: max(poses[i][0] @ fwd, poses[i][1] @ fwd))
        lead_is_weapon_hand = (poses[strike][0] @ fwd) >= (poses[strike][1] @ fwd)
        acc_d = Vector((0.0, 0.0, 0.0))
        for pw, po in poses:
            lead, rear = (pw, po) if lead_is_weapon_hand else (po, pw)
            v = lead - rear
            if v.length > 1e-6:
                acc_d += v.normalized()
        if acc_d.length > 1e-6:
            d = acc_d.normalized()
            if FLIP_HAND_LINE:
                d = -d
            # rotation taking the weapon's long axis (+Z) onto the hand line
            z = Vector((0.0, 0.0, 1.0))
            ax = z.cross(d)
            if ax.length < 1e-8:
                desired = Matrix.Identity(4) if z.dot(d) > 0 else \
                    Matrix.Rotation(math.pi, 4, 'X')
            else:
                desired = Matrix.Rotation(math.acos(max(-1, min(1, z.dot(d)))),
                                          4, ax.normalized())
        else:
            desired = Matrix.Rotation(math.radians(bearing - fan_local), 4, 'Z')
    else:
        desired = Matrix.Rotation(math.radians(bearing - fan_local), 4, 'Z')
    R_sock = mq.to_matrix().to_4x4().inverted() @ desired
    extra = {}
    if align_hands:
        extra = dict(strike_frame=strike,
                     flipped_negative_control=FLIP_HAND_LINE,
                     lead_hand_bone=R.get("r_hand") if lead_is_weapon_hand
                     else R.get("l_hand"),
                     rear_hand_bone=R.get("l_hand") if lead_is_weapon_hand
                     else R.get("r_hand"),
                     lead_hand=("weapon hand (%s)" % R.get("r_hand"))
                     if lead_is_weapon_hand else ("off hand (%s)" % R.get("l_hand")),
                     hand_line=[round(v, 4) for v in d] if acc_d.length > 1e-6 else None)
    return dict(rot_matrix=R_sock, **extra,
                mean_wrist_quat=[round(v, 5) for v in mq],
                fan_bearing_deg=bearing,
                mode="align-hands" if align_hands else "upright",
                note="socket rotation re-solved from the clip's mean wrist")


def add_carry_ik(arm, R, sk, roots, wobjs):
    """CARRY POSE: weapon on the chest, hand pinned to a grip frame on the haft.

    Socketing the weapon to the HAND and steering the hand does not work -- IK
    sets the hand's position and says nothing about its rotation, so the haft
    inherits whatever wrist the solver picks. Inverting it (weapon on the
    chest) fixes the haft, but a POSITION-ONLY IK still leaves the gauntlet
    facing anywhere, and measured on the part-ID guide the hand touched the
    haft in only 19 % of visible walk frames -- the pollaxe stood in front of
    the knight, detached.

    So the hand is pinned to a full GRIP FRAME carried on the weapon:
      * the frame is the hand's own transform in WEAPON space, taken from the
        bind-pose socket fit (inverse of the socket's bone-space matrix), so
        it is the grip that was fitted, not a new guess;
      * IK brings the hand to it and lets the elbow solve;
      * COPY_ROTATION lands the gauntlet's orientation on it.
    The free arm is damped toward its bind pose so it does not flail against a
    now-static weapon arm.
    """
    import bpy as _b
    hand = R.get("r_hand")
    chest = R.get("chest") or R.get("spine") or R.get("hips")
    if not (hand and chest and roots):
        return None
    H = 1.80
    cb = arm.data.bones[chest]
    cw = arm.matrix_world @ arm.pose.bones[chest].head
    grip_w = Vector((cw.x + 0.195 * H, cw.y + 0.162 * H, 0.700 * H))
    # CLAMP THE GRIP INTO REACH. The offsets come from the painted knight's
    # proportions; this rig's arm may be shorter, and an unreachable target
    # leaves the IK pulling and stopping short -- measured 0.27 m short, which
    # is a floating haft. Pull the target toward the shoulder until it is
    # inside 95 % of the arm's length.
    sh_name = R.get("r_arm")
    if sh_name:
        shoulder = arm.matrix_world @ arm.pose.bones[sh_name].head
        el_name = R.get("r_fore"); hd_name = R.get("r_hand")
        if el_name and hd_name:
            el = arm.matrix_world @ arm.pose.bones[el_name].head
            hd = arm.matrix_world @ arm.pose.bones[hd_name].head
            reach = (el - shoulder).length + (hd - el).length
            d = grip_w - shoulder
            if d.length > 0.95 * reach:
                grip_w = shoulder + d.normalized() * (0.95 * reach)
    yaw = sk["fit"]["socket_yaw_deg"] + sk["fit"].get("carry_extra_yaw_deg", 0.0)
    gz = sk["fit"]["grip_local_z"]
    M_world = (Matrix.Translation(grip_w)
               @ Matrix.Rotation(math.radians(yaw), 4, 'Z')
               @ Matrix.Translation(Vector((0, 0, -gz))))
    parent_w = (arm.matrix_world @ arm.pose.bones[chest].matrix
                @ Matrix.Translation(Vector((0, cb.length, 0))))
    for o in roots:
        o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = chest
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.matrix_basis = parent_w.inverted() @ M_world

    # the GRIP FRAME: the hand's transform in weapon space, from the socket fit
    # The SCALE must be in this matrix. Meshy's armature imports at 0.01, so
    # bone space is 100x world: the socket's offset reads 16.1 units for a
    # 0.161 m grip. Inverting the matrix without the scale put the grip frame
    # 16 METRES from the hand -- out of reach, so the IK gave up, the arm hung,
    # and the assert read 0 % where it had been 19 %.
    M_sock = (Matrix.Translation(Vector(sk["offset"]))
              @ Euler([math.radians(v) for v in sk["rotation_euler_xyz_deg"]],
                      'XYZ').to_matrix().to_4x4()
              @ Matrix.Diagonal(Vector(sk["scale"]).to_4d()))
    hand_in_weapon = M_sock.inverted()
    emp = _b.data.objects.new("grip_frame", None)
    _b.context.scene.collection.objects.link(emp)
    emp.parent = roots[0]
    emp.matrix_parent_inverse = Matrix.Identity(4)
    emp.matrix_basis = hand_in_weapon
    _b.context.view_layer.objects.active = arm
    _b.ops.object.mode_set(mode='POSE')
    pbh = arm.pose.bones[hand]
    # IK DRIVES A BONE'S TAIL, so it must go on the bone whose TAIL is the
    # joint being placed -- the forearm, whose tail IS the hand's head. Put on
    # the hand itself it drives the hand's tail, and on a Meshy auto-rig the
    # hand is a childless LEAF whose tail sits 24.8 m away: driving that to the
    # grip leaves the head nowhere near it. This is why every earlier attempt
    # failed, hand-socketed and chest-carried alike.
    fore = R.get("r_fore")
    ikbone = arm.pose.bones[fore] if fore else pbh
    c = ikbone.constraints.new('IK'); c.target = emp
    c.chain_count = 2 if fore else 3
    cr = pbh.constraints.new('COPY_ROTATION')
    cr.target = emp; cr.target_space = 'WORLD'; cr.owner_space = 'WORLD'
    ik_on = ikbone.name

    # damp the free arm so it does not flail against a static weapon arm
    damped = []
    for role in ("l_arm", "l_fore"):
        bn = R.get(role)
        if not bn:
            continue
        e2 = _b.data.objects.new("bind_%s" % bn, None)
        _b.context.scene.collection.objects.link(e2)
        e2.matrix_world = arm.matrix_world @ arm.pose.bones[bn].matrix
        e2.parent = arm; e2.parent_type = 'BONE'; e2.parent_bone = chest
        e2.matrix_parent_inverse = parent_w.inverted()
        e2.matrix_basis = parent_w.inverted() @ (arm.matrix_world
                                                 @ arm.pose.bones[bn].matrix)
        cc = arm.pose.bones[bn].constraints.new('COPY_ROTATION')
        cc.target = e2; cc.target_space = 'WORLD'; cc.owner_space = 'WORLD'
        cc.influence = 0.5
        damped.append(bn)
    _b.ops.object.mode_set(mode='OBJECT')
    return dict(mode="chest-carry, hand pinned to a grip frame on the haft",
                chest_bone=chest, hand_bone=hand,
                grip_world=[round(v, 4) for v in grip_w],
                arm_reach_m=round(reach, 4) if sh_name and el_name else None,
                yaw_deg=round(yaw, 3),
                carry_extra_yaw_deg=sk["fit"].get("carry_extra_yaw_deg", 0.0),
                ik_bone=ik_on, ik_note="IK on the bone whose TAIL is the hand's head",
                free_arm_damped=damped, free_arm_influence=0.5)



def assert_thrust(sc, arm, R, objs, wobjs, times, wmeta, upright_info):
    """Does the weapon POINT lead, and does it stay out of the body?

    Two questions, and the render cannot answer the first one: a reversed thrust
    and a correct one both put a haft across the frame, which is how the first
    attack pass shipped with the axe head behind the helm. The sign lives in 3D,
    so it is measured in 3D.

      LEADS   at the strike frame, the point must be beyond the LEAD HAND along
              the character's forward axis, and forward of the pelvis.
      CLEAR   in EVERY frame, the weapon must be outside the body mesh -- not
              merely at some distance from a bone, which would need a per-rig
              radius and would not transfer to the manticore. Signed distance
              from a BVH of the posed mesh answers it for any rig.

    CLEAR samples the WHOLE HAFT, not just the point. Testing the point alone
    was the first version and it passed while the render plainly showed the butt
    cap crossing the helm: correcting the sign rotates the weapon 180 degrees
    about the grip, so it moves whatever was fouling the helm from one end of
    the haft to the other and a point-only test follows it out of the way.

    CLEAR also NAMES THE PART it is inside, and ignores the hands and forearms.
    A hand closed around a haft puts the haft inside the hand mesh -- that is
    what holding something IS -- so a bare inside/outside test reports a foul on
    every correctly gripped weapon. The second version did exactly that: it read
    a constant +0.0095 m at u=0.54 on every non-striking frame (the grip against
    its own palm, rigidly socketed, so the same number forever -- a constant is
    a tell) and it counted the REAR hand's grip at u=0.42 as a body
    penetration. Only a part that is not a hand or a forearm is a foul.
    """
    from mathutils.bvhtree import BVHTree
    GRIP_PART = re.compile(r'hand|fore|wrist|finger|thumb', re.I)
    fwd = Vector((0.0, 1.0, 0.0))
    lead = upright_info.get("lead_hand_bone")
    if not lead or not wobjs:
        return None
    # the point: the haft axis at the head end of the weapon's long axis
    hx, hy = wmeta.get("haft_axis_xy", [0.0, 0.0])
    zlo, zhi = wmeta["bbox_lo"][2], wmeta["bbox_hi"][2]
    tip_z = zhi if wmeta.get("head_end") == "max" else zlo
    butt_z = zlo if wmeta.get("head_end") == "max" else zhi
    P_tip = Vector((hx, hy, tip_z)); P_butt = Vector((hx, hy, butt_z))
    NS = 25
    haft = [(k / (NS - 1.0), P_butt.lerp(P_tip, k / (NS - 1.0))) for k in range(NS)]
    dg = bpy.context.evaluated_depsgraph_get()
    rows = []
    for i, t in enumerate(times):
        sc.frame_set(int(t), subframe=float(t) - int(t))
        W = wobjs[0].matrix_world
        tip = W @ P_tip; butt = W @ P_butt
        lh = arm.matrix_world @ arm.pose.bones[lead].head
        pel = arm.matrix_world @ arm.pose.bones[R["hips"]].head
        # inside-ness against the posed body, whichever mesh is nearest.
        # The BVH is built ONCE PER FRAME: building it inside the point loop
        # made 25x the trees and turned a 20 s render into minutes.
        trees = []
        for ob in objs:
            me = ob.evaluated_get(dg).data
            gname = {g.index: g.name for g in ob.vertex_groups}

            def vg(poly_i, me=me, ob=ob, gname=gname):
                """Dominant vertex group over the hit polygon = the body part."""
                if poly_i is None or poly_i >= len(me.polygons):
                    return None
                tot = {}
                for vi in me.polygons[poly_i].vertices:
                    for g in ob.data.vertices[vi].groups:
                        tot[g.group] = tot.get(g.group, 0.0) + g.weight
                return gname.get(max(tot, key=tot.get)) if tot else None
            trees.append((ob, BVHTree.FromObject(ob, dg),
                          ob.matrix_world.inverted(), vg))

        def signed(pt):
            w = None, None
            for ob, bvh, inv, vg in trees:
                hit = bvh.find_nearest(inv @ pt)
                if hit[0] is None:
                    continue
                loc = ob.matrix_world @ hit[0]
                nor = ob.matrix_world.to_3x3() @ hit[1]
                v = pt - loc
                sd = v.length * (1.0 if v.dot(nor) >= 0 else -1.0)
                if w[0] is None or sd < w[0]:
                    w = sd, vg(hit[2])
            return w
        worst, worst_part = signed(tip)
        haft_sd = [(u,) + signed(W @ q) for u, q in haft]
        haft_sd = [r for r in haft_sd if r[1] is not None]
        # a hand or forearm on the haft is a GRIP, not a foul
        fouls = [r for r in haft_sd if not GRIP_PART.search(r[2] or "")]
        hw_u, hw_v, hw_p = min(fouls, key=lambda r: r[1]) if fouls else (None, None, None)
        gr_u, gr_v, gr_p = min(haft_sd, key=lambda r: r[1]) if haft_sd else (None,) * 3
        rows.append(dict(
            i=i, frame=round(float(t), 3),
            tip_beyond_lead_hand_m=round((tip - lh).dot(fwd), 4),
            tip_forward_of_pelvis_m=round((tip - pel).dot(fwd), 4),
            butt_beyond_lead_hand_m=round((butt - lh).dot(fwd), 4),
            tip_signed_dist_to_body_m=round(worst, 4) if worst is not None else None,
            haft_min_signed_dist_m=round(hw_v, 4) if hw_v is not None else None,
            haft_min_at=round(hw_u, 3) if hw_u is not None else None,
            haft_min_part=hw_p,
            nearest_any_part=gr_p,
            nearest_any_m=round(gr_v, 4) if gr_v is not None else None,
            tip_nearest_part=worst_part,
            tip_z=round(tip.z, 4)))
    st = int(upright_info.get("strike_frame", 0))
    st = min(st, len(rows) - 1)
    pen = [r for r in rows if r["haft_min_signed_dist_m"] is not None
           and r["haft_min_signed_dist_m"] < 0]
    res = dict(
        strike_index=st, strike_row=rows[st], per_frame=rows,
        lead_hand_bone=lead,
        LEADS=bool(rows[st]["tip_beyond_lead_hand_m"] > 0
                   and rows[st]["tip_forward_of_pelvis_m"] > 0),
        CLEAR=bool(not pen),
        frames_penetrating=[r["i"] for r in pen],
        min_signed_dist_m=round(min(
            (r["haft_min_signed_dist_m"] for r in rows
             if r["haft_min_signed_dist_m"] is not None), default=0.0), 4),
        tip_min_signed_dist_m=round(min(
            (r["tip_signed_dist_to_body_m"] for r in rows
             if r["tip_signed_dist_to_body_m"] is not None), default=0.0), 4),
        worst_frame=min(
            (r for r in rows if r["haft_min_signed_dist_m"] is not None),
            key=lambda r: r["haft_min_signed_dist_m"], default={}).get("i"),
        worst_at_along_haft=min(
            (r for r in rows if r["haft_min_signed_dist_m"] is not None),
            key=lambda r: r["haft_min_signed_dist_m"], default={}).get("haft_min_at"),
        worst_part=min(
            (r for r in rows if r["haft_min_signed_dist_m"] is not None),
            key=lambda r: r["haft_min_signed_dist_m"], default={}).get("haft_min_part"),
        # the reversed pass would show this NEGATIVE at the strike: the sign of
        # this one number is the whole defect
        strike_tip_beyond_lead_hand_m=rows[st]["tip_beyond_lead_hand_m"])
    print("  thrust assert: LEADS %s (tip %+.3f m beyond lead hand %s, %+.3f m "
          "forward of pelvis)  CLEAR %s (worst non-grip %+.4f m into '%s' at "
          "u=%s on frame %s; tip alone %+.4f m%s)"
          % ("PASS" if res["LEADS"] else "FAIL",
             rows[st]["tip_beyond_lead_hand_m"], lead,
             rows[st]["tip_forward_of_pelvis_m"],
             "PASS" if res["CLEAR"] else "FAIL", res["min_signed_dist_m"],
             res["worst_part"], res["worst_at_along_haft"], res["worst_frame"],
             res["tip_min_signed_dist_m"],
             "" if res["CLEAR"] else ", frames %s" % res["frames_penetrating"]))
    return res


def bake_weapon_guides(wobjs, guides):
    """The weapon gets the same two layers: `gpos` from its own rest position
    (normalised over the BODY's bind bbox so the two share one space) and a
    reserved flat `gpart` colour that no bone uses."""
    lo = Vector(guides["bind_bbox_lo"]); span = Vector(guides["bind_bbox_span"])
    for i, o in enumerate(wobjs):
        me = o.data
        cp = me.color_attributes.new(name="gpos", type='FLOAT_COLOR', domain='POINT')
        cq = me.color_attributes.new(name="gpart", type='FLOAT_COLOR', domain='POINT')
        c = (1.0, 1.0, 1.0) if i == 0 else (0.85, 0.85, 0.85)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            cp.data[v.index].color = (min(max((w.x - lo.x) / span.x, 0), 1),
                                      min(max((w.y - lo.y) / span.y, 0), 1),
                                      min(max((w.z - lo.z) / span.z, 0), 1), 1.0)
            cq.data[v.index].color = (c[0], c[1], c[2], 1.0)


def main():
    info = json.load(open(INFO))
    os.makedirs(OUTDIR, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    objs = skinned(sc, arm)
    for o in list(sc.objects):
        if o.type == 'MESH' and o not in objs:
            bpy.data.objects.remove(o, do_unlink=True)   # the stray sphere

    # ---- FACING, measured off the clip, then rotated to +Y ----------------
    R = info["role_map"]
    key = R.get("l_toe") or R.get("l_foot")
    st = info["stance"].get(key)
    face_yaw, face_src = 0.0, "none"
    if FACE is not None:
        face_yaw, face_src = FACE, "given"
    elif st:
        d = st["disp_m"][:2]                     # the stance foot's travel
        if math.hypot(d[0], d[1]) < MIN_DISP:
            raise SystemExit(
                "REFUSING to derive facing from a %.4f m stance displacement in "
                "'%s' -- that is noise, not travel. Pass --face from a "
                "locomotion clip (see work/rig_facing.json)."
                % (math.hypot(d[0], d[1]), STATE))
        face_yaw = math.degrees(math.atan2(-d[0], -d[1]))
        face_src = "derived"
    rot = Matrix.Rotation(math.radians(-face_yaw), 4, 'Z')
    for o in list(sc.objects):
        if o.parent is None:
            o.matrix_world = rot @ o.matrix_world

    guides = bake_guides(objs, arm)

    # ---- WEAPON on a bone socket (modular gear) ---------------------------
    wobjs = []
    if SOCKET:
        sk = json.load(open(SOCKET))
        before = set(o.name for o in sc.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(os.path.dirname(SOCKET),
                                                        "..", sk["weapon"]))
        wobjs = [o for o in sc.objects if o.name not in before and o.type == 'MESH']
        roots = [o for o in sc.objects if o.name not in before and o.parent is None]
        carry_info = None
        upright_info = None
        if (UPRIGHT or ALIGN_HANDS) and not CARRY:
            upright_info = fit_upright_socket(arm, R, sk, info,
                                              info["resample"]["frames"],
                                              align_hands=ALIGN_HANDS)
        M = (Matrix.Translation(Vector(sk["offset"]))
             @ (Euler([math.radians(v) for v in sk["rotation_euler_xyz_deg"]],
                      'XYZ').to_matrix().to_4x4() if not upright_info
                else upright_info["rot_matrix"])
             @ Matrix.Diagonal(Vector(sk["scale"]).to_4d()))
        pbname = sk["bone"]
        for o in ([] if CARRY else roots):
            o.parent = arm
            o.parent_type = 'BONE'
            o.parent_bone = pbname
            b = arm.data.bones[pbname]
            # Blender parents to the bone TAIL; the socket is written in bone
            # space from the HEAD, so undo the tail offset here rather than
            # baking a renderer-specific convention into the socket file.
            o.matrix_parent_inverse = Matrix.Translation(Vector((0, -b.length, 0)))
            o.matrix_basis = M
        if CARRY:
            carry_info = add_carry_ik(arm, R, sk, roots, wobjs)
        unlit(wobjs)

    # ---- scale from the CHARACTER -----------------------------------------
    h = HEIGHT if HEIGHT else info["character_height_m"]
    px_per_m = PX_PER_M if HEIGHT else BODY_PX / h

    # ---- camera ------------------------------------------------------------
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = FRAME / px_per_m
    sc.render.resolution_x = FRAME; sc.render.resolution_y = FRAME
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in \
        [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] \
        else 'BLENDER_EEVEE'

    hips = arm.pose.bones[R["hips"]]
    times = info["resample"]["frames"]
    el = math.radians(ELEV)

    def place(az, aim_z, hw):
        A = math.radians(az)
        aim = Vector((hw.x, hw.y, aim_z))
        pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                            math.sin(el))) * 20.0
        cam.location = pos
        cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()

    # ---- calibrate the ground row over the WHOLE cycle ---------------------
    unlit(objs)
    aim_z = 0.0
    soles = []
    for t in times:
        sc.frame_set(int(t), subframe=float(t) - int(t))
        hw = arm.matrix_world @ hips.head
        place(AZI[DIRS[0]], aim_z, hw)
        sc.render.filepath = os.path.join(OUTDIR, "_cal.png")
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(sc.render.filepath)
        px = np.array(im.pixels[:]).reshape(FRAME, FRAME, 4)[::-1]
        bpy.data.images.remove(im)
        ys = np.where((px[..., 3] > 0.03).any(axis=1))[0]
        soles.append(float(ys.max()) if len(ys) else SOLE_Y)
    # Raising the aim point moves the figure DOWN the frame, so the correction
    # ADDS the shortfall. Written the other way round first, it drove the aim
    # 1.22 m the wrong way and put the knight's feet at row 139 with his head
    # off the top of the frame.
    # A world +Z displacement does not move the image by z * px_per_m: at an
    # elevated camera it moves it by z * px_per_m * cos(elevation). Omitting
    # the cosine left exactly the shortfall it predicts -- 8 px of a 133 px
    # correction at 19.77 deg -- which is how it was found.
    aim_z = aim_z + (SOLE_Y - max(soles)) / (px_per_m * math.cos(el))
    os.remove(os.path.join(OUTDIR, "_cal.png"))

    rep = dict(state=STATE, source=os.path.basename(SRC), frame=FRAME,
               px_per_m=round(px_per_m, 4), sole_y=SOLE_Y,
               camera_json="meshy_t1/camera.json",
               character_height_m=h, elevation_deg=ELEV,
               facing_yaw_corrected_deg=round(face_yaw, 3),
               facing_source=face_src,
               aim_z=round(aim_z, 5), azimuths=AZI, dirs=DIRS,
               frames=len(times), fps=info["resample"]["out_fps"],
               carry_pose=bool(CARRY), weapon=os.path.basename(SOCKET) if SOCKET else None,
               carry=(carry_info if SOCKET else None),
               upright=({k: v for k, v in upright_info.items() if k != "rot_matrix"}
                        if SOCKET and upright_info else None),
               guides=guides, passes={})

    def render_pass(tag, subdir):
        out = {}
        for d in DIRS:
            dd = os.path.join(OUTDIR, subdir, d)
            os.makedirs(dd, exist_ok=True)
            for i, t in enumerate(times):
                sc.frame_set(int(t), subframe=float(t) - int(t))
                hw = arm.matrix_world @ hips.head
                place(AZI[d], aim_z, hw)
                sc.render.filepath = os.path.join(dd, "%s_%s_%02d.png" % (tag, d, i))
                bpy.ops.render.render(write_still=True)
            out[d] = dd
        return out

    if SOCKET and wobjs and upright_info and upright_info.get("mode") == "align-hands":
        rep["thrust_assert"] = assert_thrust(
            sc, arm, R, objs, wobjs, times,
            json.load(open(os.path.join("work", "weapon.json"))), upright_info)
    if ASSERT_ONLY:
        return
    rep["passes"]["colour"] = render_pass(STATE, "colour")
    if wobjs:
        # the weapon as its OWN layer, for modular gear, then the body alone
        for o in objs:
            o.hide_render = True
        rep["passes"]["weapon"] = render_pass("weapon", "weapon")
        for o in objs:
            o.hide_render = False
    # guides
    # guides cover the body AND the weapon: EbSynth needs correspondence for
    # every pixel it will be asked to synthesise, and the weapon is in frame
    if wobjs:
        bake_weapon_guides(wobjs, guides)
    unlit(objs, attr="gpos"); unlit(wobjs, attr="gpos")
    rep["passes"]["pos"] = render_pass("pos", "guides_pos")
    unlit(objs, attr="gpart"); unlit(wobjs, attr="gpart")
    rep["passes"]["part"] = render_pass("part", "guides_part")
    json.dump(rep, open(os.path.join(OUTDIR, "render_%s.json" % STATE), "w"), indent=1)
    print("%s: %d dirs x %d frames, %.3f px/m, aim_z %.4f, facing corrected %.1f deg"
          % (STATE, len(DIRS), len(times), px_per_m, aim_z, face_yaw))


main()
