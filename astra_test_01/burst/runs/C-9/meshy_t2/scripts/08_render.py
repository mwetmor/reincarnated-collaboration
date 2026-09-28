# C-9 meshy_t2 step 6: render a clip to the game's sprite format in all eight
# directions, with the EbSynth guide passes baked in the same pass.
#
#   blender -b -noaudio --python scripts/08_render.py -- <clips.blend> <state>
#                       <outdir> [--dirs S,SE,...] [--frames N]
#
# Compatible with meshy_t1's renderer by CONSTRUCTION, not by coincidence:
# 512 frame, sole row 398, elevation 19.77 deg, S=0/SE=45/E=90..., passes
# named colour / guides_pos / guides_part (+ mask here), files
# {tag}_{dir}_{NN}.png. What differs is deliberate and is the point of T2:
#
#  * SCALE IS SHARED, SIZE IS NOT. t1 divides the knight's 198.333 px by HIS
#    height to get px/m. Doing the same for the manticore would render a 1.20 m
#    monster the same pixel height as a 1.80 m man. So T2 takes t1's px/m --
#    110.185 px/m, the world's scale -- and lets the manticore come out 132 px
#    tall. Same world, different creatures.
#
#  * GROUND ROW ANALYTIC, NOT BY SILHOUETTE. t1 calibrates the aim point until
#    the LOWEST rendered pixel over the cycle sits on row 398. On a quadruped
#    that measures whatever hangs lowest, and this one's tail sweeps to 0.22 m
#    -- and in the gallop's suspension frames NOTHING touches the ground at
#    all. So the aim height is solved from the projection instead (a world
#    dz moves the image by dz * px_per_m * cos(elev)), which puts world z = 0
#    on row 398 for every clip, every frame. The render still MEASURES the
#    sole row on a known-planted frame and reports the error, so the analytic
#    claim is checked rather than trusted.
#
#  * ONE AIM HEIGHT FOR ALL FOUR CLIPS, so the creature cannot pop vertically
#    between idle and walk.
import bpy, colorsys, json, math, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("08_render.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, STATE, OUTDIR = a[0], a[1], a[2]
DIRS = a[a.index("--dirs") + 1].split(",") if "--dirs" in a else T.DIRS
NFR = int(a[a.index("--frames") + 1]) if "--frames" in a else None
PASSES = a[a.index("--passes") + 1].split(",") if "--passes" in a else \
    ["colour", "pos", "part", "mask"]


def bake_guides(objs, arm):
    """`gpos` = the REST vertex position normalised over the bind bbox (the
    StyLit "where on the body" guide, invariant to the pose because it is
    stored per vertex before skinning); `gpart` = a flat colour per DOMINANT
    bone group."""
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
        for nm in ("gpos", "gpart"):
            if nm in me.color_attributes:
                me.color_attributes.remove(me.color_attributes[nm])
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


def reshade(objs, attr=None, flat=None):
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.node_tree:
                continue
            nt = m.node_tree
            for n in list(nt.nodes):
                if n.type in ('EMISSION', 'ATTRIBUTE', 'RGB'):
                    nt.nodes.remove(n)
    if flat is not None:
        for o in objs:
            for slot in o.material_slots:
                nt = slot.material.node_tree
                out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
                em = nt.nodes.new('ShaderNodeEmission')
                em.inputs['Color'].default_value = (flat[0], flat[1], flat[2], 1.0)
                nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
        return
    T.unlit(objs, attr=attr)


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    objs = [o for o in sc.objects if o.type == 'MESH'
            and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers)]
    strays = [o.name for o in sc.objects if o.type == 'MESH' and o not in objs]
    for o in list(sc.objects):
        if o.type == 'MESH' and o not in objs:
            bpy.data.objects.remove(o, do_unlink=True)

    act = bpy.data.actions.get("mc_" + STATE)
    arm.animation_data_create()
    arm.animation_data.action = act
    # Blender 5 needs the action's SLOT assigned as well; without it the rig
    # stays in rest pose and every frame renders identically.
    try:
        slots = list(act.slots)
        if slots:
            arm.animation_data.action_slot = slots[0]
    except Exception:
        pass
    clips = json.load(open(os.path.join(os.path.dirname(BLEND), "clips.json")))
    info = clips[STATE]
    n = NFR or info["frames"]

    guides = bake_guides(objs, arm)
    px_per_m = T.PX_PER_M
    el = math.radians(T.ELEV)
    # world z -> image row:  row = 256 + (aim_z - z) * px_per_m * cos(elev).
    # The ground is the MEASURED sole, not the nominal z = 0: the paw mesh's
    # contact sits ~15 mm below the toe bone the IK drives, and that offset is
    # a property of the mesh (see 07_clips.py). clips.json carries the median
    # measured sole over every planted foot of every clip, so all four states
    # share one ground and the creature cannot pop vertically between them.
    gref = clips.get("ground_ref_z", 0.0)
    aim_z = (T.SOLE_Y - T.FRAME / 2.0) / (px_per_m * math.cos(el)) + gref

    sc.render.resolution_x = T.FRAME; sc.render.resolution_y = T.FRAME
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.color_mode = 'RGBA'
    engines = [i.identifier for i in
               bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in engines \
        else 'BLENDER_EEVEE'
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = T.FRAME / px_per_m
    hips = arm.pose.bones["hips"]
    # Aim at the BODY's centre, not at the hips. The hips sit 0.10 m behind
    # the nose-to-tail midpoint on a quadruped, so aiming at them alone put
    # the creature 11 px right of frame centre and spent the margin unevenly.
    # The aim still TRACKS the hips, so the sprite stays in place; it is only
    # offset by a constant.
    AIM_Y = -float(arm.data.bones["hips"].head_local.y)

    os.makedirs(OUTDIR, exist_ok=True)
    rep = dict(state=STATE, source=os.path.basename(BLEND), frame=T.FRAME,
               px_per_m=round(px_per_m, 4), px_per_m_source="knight 198.333 px / 1.80 m",
               sole_y=T.SOLE_Y, elevation_deg=T.ELEV, aim_z=round(aim_z, 5),
               aim_z_method="analytic: measured sole plane -> row 398 at this px/m "
                            "and elevation",
               ground_ref_z=round(clips.get("ground_ref_z", 0.0), 5),
               sole_z_range_m=info.get("sole_z_range_m"),
               azimuths=T.AZI, dirs=DIRS, frames=n,
               fps=info["fps"], period_s=info["period_s"],
               speed_m_s=info["speed_m_s"], stride_m=info["stride_m"],
               cycle=info["cycle"], ignored_unskinned=strays,
               facing="+Y in the blend; no facing correction needed (the rig was "
                      "built facing +Y)",
               guides=guides, passes={})

    def render_pass(tag, subdir):
        out = {}
        for d in DIRS:
            dd = os.path.join(OUTDIR, subdir, d)
            os.makedirs(dd, exist_ok=True)
            for i in range(n):
                sc.frame_set(i + 1)
                hw = arm.matrix_world @ hips.head
                T.place_camera(cam, T.AZI[d], (hw.x, hw.y + AIM_Y), aim_z)
                sc.render.filepath = os.path.join(dd, "%s_%s_%02d.png" % (tag, d, i))
                bpy.ops.render.render(write_still=True)
            out[d] = os.path.relpath(dd, OUTDIR)
        return out

    if "colour" in PASSES:
        reshade(objs)
        rep["passes"]["colour"] = render_pass(STATE, "colour")
        # CHECK the ground, with an instrument that answers the right
        # question. The first version compared the LOWEST OPAQUE ROW against
        # 398 and reported a 5 px error that was not an error: at a 19.77 deg
        # elevation the image row depends on the viewing-direction distance as
        # well as on height, so the NEAR-side paw projects
        # x * px_per_m * sin(elev) = 5.6 px lower than the midline for
        # x = 0.15 m. A knight's feet sit on his midline and never showed it;
        # a quadruped stands 0.30 m wide and always will. The lowest pixel is
        # SUPPOSED to be below the ground row.
        #
        # So the check now (a) confirms Blender's projection matches the
        # formula the aim height was solved from, by projecting the mesh
        # through the camera matrix and comparing with the rendered
        # silhouette, and (b) reports the ground-plane row at the creature's
        # own midline, which is the line the game draws.
        vdir = DIRS[0] if "E" not in DIRS else "E"
        planted = [i for i, r in enumerate(info["ik"])
                   if any(r[f]["planted"] for f in r)]
        chk = []
        for i in planted[:4]:
            pth = os.path.join(OUTDIR, "colour", vdir,
                               "%s_%s_%02d.png" % (STATE, vdir, i))
            if not os.path.exists(pth):
                continue
            sc.frame_set(i + 1)
            hw = arm.matrix_world @ hips.head
            T.place_camera(cam, T.AZI[vdir], (hw.x, hw.y + AIM_Y), aim_z)
            bpy.context.view_layer.update()
            V = cam.matrix_world.inverted()
            osc = cam.data.ortho_scale

            def row_of(P):
                q = V @ Vector(P)
                return T.FRAME / 2.0 - q.y / osc * T.FRAME

            dg = bpy.context.evaluated_depsgraph_get()
            ev = objs[0].evaluated_get(dg); me = ev.to_mesh()
            M = ev.matrix_world
            lowest = max(row_of(M @ v.co) for v in me.vertices)
            ev.to_mesh_clear()
            im = bpy.data.images.load(pth)
            px = np.array(im.pixels[:]).reshape(T.FRAME, T.FRAME, 4)[::-1]
            bpy.data.images.remove(im)
            ys = np.where((px[..., 3] > 0.5).any(axis=1))[0]
            chk.append(dict(frame=i,
                            midline_ground_row=round(row_of((hw.x, hw.y + AIM_Y, gref)), 2),
                            predicted_lowest_row=round(lowest, 2),
                            rendered_lowest_row=int(ys.max()) if len(ys) else None,
                            near_side_offset_px=round(
                                lowest - row_of((hw.x, hw.y + AIM_Y, gref)), 2)))
        rep["ground_check"] = dict(
            target_row=T.SOLE_Y, view=vdir, frames=chk,
            note="midline_ground_row is the line the game draws and must be 398; "
                 "rendered_lowest_row sits below it by the near-side paw's "
                 "x * px_per_m * sin(elev), and predicted_lowest_row confirms the "
                 "projection model against the render")
    if "pos" in PASSES:
        reshade(objs, attr="gpos")
        rep["passes"]["pos"] = render_pass("pos", "guides_pos")
    if "part" in PASSES:
        reshade(objs, attr="gpart")
        rep["passes"]["part"] = render_pass("part", "guides_part")
    if "mask" in PASSES:
        reshade(objs, flat=(1.0, 1.0, 1.0))
        rep["passes"]["mask"] = render_pass("mask", "guides_mask")

    json.dump(rep, open(os.path.join(OUTDIR, "render_%s.json" % STATE), "w"), indent=1)
    print("%s: %d dirs x %d frames, %.3f px/m, aim_z %.4f" % (STATE, len(DIRS), n,
                                                              px_per_m, aim_z))
    if "ground_check" in rep:
        print("  ground: midline row %s (want %d); lowest rendered row %s "
              "(near-side paw, offset %s px)"
              % ([c["midline_ground_row"] for c in rep["ground_check"]["frames"]],
                 T.SOLE_Y,
                 [c["rendered_lowest_row"] for c in rep["ground_check"]["frames"]],
                 [c["near_side_offset_px"] for c in rep["ground_check"]["frames"]]))


main()
