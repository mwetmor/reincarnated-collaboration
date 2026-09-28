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
import bpy, colorsys, json, math, os, sys
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
# CARRY POSE. A library locomotion clip swings both arms freely, so a weapon
# socketed to the hand swings with it -- measured on this walk, the pollaxe
# reaches near-horizontal and points backwards by frame 8. That is not a
# carry; the approved stills hold it upright. With --carry the weapon arm is
# IK-solved to a grip point carried in the CHEST's frame, so the hand holds
# station against the torso while every other channel of the mocap is
# untouched. Off by default: it changes the authored motion, which is a design
# call, not a rendering one.
CARRY = "--carry" in a
# FACING IS A PROPERTY OF THE RIG, NOT OF THE CLIP. Derived per clip it is
# right for locomotion and NOISE for anything else: this knight's idle gave
# -90 deg from a 0.0001 m stance displacement and rendered facing the camera in
# every direction. Measured once on the walk and passed in here.
FACE = float(a[a.index("--face") + 1]) if "--face" in a else None
MIN_DISP = 0.15
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
FRAME = 512
BODY_PX = 198.33333333333334          # the Grok cells' helm-to-sole
SOLE_Y = 398.0                        # the game's ground row
ELEV = 19.77


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


def add_carry_ik(arm, R, sk, roots, wobjs):
    """CARRY POSE, by inverting the attachment.

    Socketing the weapon to the HAND and then steering the hand does not work:
    IK sets the hand's position but not its rotation, and a bone-relative
    socket inherits whatever wrist the solver picks -- tried both ways, the
    pollaxe came out lying across the body either time.

    So for a carry the weapon is parented to the CHEST, upright, at the grip
    offset measured from the approved E still, and the HAND is IK-solved onto
    a point on its haft. The weapon cannot tilt because nothing downstream of
    the chest touches it, and the grip cannot drift because the hand is
    constrained to the haft itself -- the same grip-socket argument as
    R-C9-51, reached from the other end.
    """
    import bpy as _b
    hand = R.get("r_hand")
    chest = R.get("spine") or R.get("hips")
    if not (hand and chest and roots):
        return None
    H = 1.80
    cb = arm.data.bones[chest]
    cw = arm.matrix_world @ arm.pose.bones[chest].head
    grip_w = Vector((cw.x + 0.195 * H, cw.y + 0.162 * H, 0.700 * H))
    yaw = sk["fit"]["socket_yaw_deg"]
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
    # the hand goes to the haft, not the other way round
    emp = _b.data.objects.new("grip_target", None)
    _b.context.scene.collection.objects.link(emp)
    emp.parent = roots[0]
    emp.matrix_parent_inverse = Matrix.Identity(4)
    emp.matrix_basis = Matrix.Translation(Vector((0, 0, gz)))
    _b.context.view_layer.objects.active = arm
    _b.ops.object.mode_set(mode='POSE')
    c = arm.pose.bones[hand].constraints.new('IK')
    c.target = emp; c.chain_count = 3
    _b.ops.object.mode_set(mode='OBJECT')
    return dict(mode="chest-parented carry", chest_bone=chest,
                grip_world=[round(v, 4) for v in grip_w], yaw_deg=yaw)


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
        M = (Matrix.Translation(Vector(sk["offset"]))
             @ Euler([math.radians(v) for v in sk["rotation_euler_xyz_deg"]],
                     'XYZ').to_matrix().to_4x4()
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
    px_per_m = BODY_PX / h

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
               character_height_m=h, elevation_deg=ELEV,
               facing_yaw_corrected_deg=round(face_yaw, 3),
               facing_source=face_src,
               aim_z=round(aim_z, 5), azimuths=AZI, dirs=DIRS,
               frames=len(times), fps=info["resample"]["out_fps"],
               carry_pose=bool(CARRY), weapon=os.path.basename(SOCKET) if SOCKET else None,
               carry=(carry_info if SOCKET else None),
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
