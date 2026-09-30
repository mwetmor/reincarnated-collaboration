# Re-ground EVERY locomotion/stance clip from its feet, not only the ones whose
# scale was stripped.
#
#   blender -b -noaudio --python scripts/43_reground_all.py -- <in.glb> <out.glb>
#        [--skip a,b] [--json f]
#
# THE GAP THIS CLOSES, found by my own band rule on a file I had already
# shipped: idle_armed (Meshy 85 "Axe Stance") sits at root height 44.9-61.7
# against 83-122 for every other clip -- about 0.35 m lower. He stands in a
# hole whenever he holds the axe at rest.
#
# It was missed because the clip-hygiene step re-grounds clips whose JOINT
# SCALE was stripped, on the theory that the scale and the bad root translation
# came from the same retarget. axe_stance has no scale track, so it was never
# re-grounded, and nothing else looked. The scale was the SYMPTOM I had seen
# before; the root height is the defect, and it arrives without the symptom.
#
# The band rule is what caught it: a clip whose root-height range overlaps no
# other clip's is not standing on the same ground as the set. That rule was
# added in W1 as a better discriminator than the 5% rest comparison, and this
# is the first defect it found on its own.
import bpy, json, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("43_reground_all.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
SKIP = set((a[a.index('--skip') + 1] if '--skip' in a else "").split(","))
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
# clips where the feet SHOULD leave the floor, or that are pose layers
SKIP |= {"shield_carry_L", "shield_guard_L"}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
masks = {o.name: G.foot_verts(o) for o in body}
rep = {}
for act in sorted(bpy.data.actions, key=lambda x: x.name):
    if act.name in SKIP:
        continue
    fz = G.foot_track(arm, body, act, masks)
    lo, hi = float(fz.min()), float(fz.max())
    mid = (lo + hi) / 2.0
    if abs(mid) < 0.02:
        rep[act.name] = dict(skipped="already within 2 cm of the floor",
                             feet=[round(lo, 4), round(hi, 4)])
        continue
    r = G.reground_from_feet(arm, body, act)
    rep[act.name] = r
    print("  %-28s %+.4f m: feet %+.4f..%+.4f -> %+.4f..%+.4f"
          % (act.name, r["dz"], r["before"]["min"], r["before"]["max"],
             r["after"]["min"], r["after"]["max"]))
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
import importlib
L = importlib.import_module("21_lint_export").lint(DST)
print("wrote %s (%.2f MB) LINT %s fails %d"
      % (DST, os.path.getsize(DST) / 1e6, L["verdict"], len(L["fails"])))
for w in L["warns"]:
    if "overlaps NO other" in w:
        print("  STILL ISOLATED: %s" % w.split("clip '")[1].split("'")[0])
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"],
                   isolated=[w.split("clip '")[1].split("'")[0] for w in L["warns"]
                             if "overlaps NO other" in w])
assert not L["fails"]
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
