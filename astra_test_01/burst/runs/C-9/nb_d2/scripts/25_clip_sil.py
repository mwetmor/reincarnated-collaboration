# Does he still change size between clips? Silhouette at 52.95 deg, facing S.
#
#   blender -b -noaudio --python scripts/25_clip_sil.py -- <a.glb> <b.glb> <outdir>
#
# ONE ortho scale and ONE camera centre for BOTH files and every clip, fixed
# from the rest-pose height (identical in both), so a difference in the pixels
# is a difference in the figure and not in the framing.
#
# Frames, per the dispatch: the idle's mid-frame, and the walk and run at LEGS
# TOGETHER -- found by minimising the horizontal distance between the two feet
# rather than by picking a frame number, because the two clips do not share a
# phase and a hand-picked frame is a hand-picked answer.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("25_clip_sil.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
FILES, OUT = a[0:2], a[2]
os.makedirs(OUT, exist_ok=True)
EL, RES, REST_H = 52.95, 512, 1.85
rows = {}
for tag, path in zip(("before", "after"), FILES):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
    for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
        bpy.data.objects.remove(o, do_unlink=True)
    for o in body:                       # flat emission -> a clean matte
        for s_ in o.material_slots:
            m_ = s_.material
            if not m_ or not m_.node_tree:
                continue
            nt = m_.node_tree
            o_ = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            em.inputs['Color'].default_value = (1, 1, 1, 1)
            nt.links.new(em.outputs['Emission'], o_.inputs['Surface'])
    eng = [e.identifier for e in
           bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    sc.render.engine = ('BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng
                        else 'BLENDER_EEVEE')
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.color_mode = 'RGBA'
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = REST_H * 1.45
    ctr = Vector((0.0, 0.0, REST_H * 0.5))
    el, az = math.radians(EL), 0.0        # facing S
    pos = ctr + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                        math.sin(el))) * (10 * REST_H)
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    acts = {x.name: x for x in bpy.data.actions}

    def legs_together(ac):
        """Frame whose two feet are closest together on the ground plane."""
        arm.animation_data.action = ac
        f0, f1 = (int(round(x)) for x in ac.frame_range)
        best, bf = 1e9, f0
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            p = [(arm.matrix_world @ arm.pose.bones[b].matrix).translation
                 for b in ('LeftFoot', 'RightFoot')]
            d = float((p[0].xy - p[1].xy).length)
            if d < best:
                best, bf = d, f
        return bf, round(best, 4)

    picks = {}
    for cn in ('idle', 'walk', 'run'):
        if cn not in acts:
            continue
        ac = acts[cn]
        f0, f1 = (int(round(x)) for x in ac.frame_range)
        if cn == 'idle':
            picks[cn] = ((f0 + f1) // 2, None)
        else:
            picks[cn] = legs_together(ac)
    for cn, (f, sep) in picks.items():
        arm.animation_data.action = acts[cn]
        sc.frame_set(f)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(OUT, "%s_%s.png" % (tag, cn))
        bpy.ops.render.render(write_still=True)
        rows.setdefault(tag, {})[cn] = dict(frame=f, foot_sep=sep)
        print("%s %-5s frame %d%s" % (tag, cn, f,
              "" if sep is None else " (feet %.3f m apart)" % sep))
json.dump(dict(picks=rows, ortho_scale=REST_H * 1.45, res=RES, elev=EL,
               facing="S", note="body only, no gear"),
          open(os.path.join(OUT, "picks.json"), "w"), indent=1)
