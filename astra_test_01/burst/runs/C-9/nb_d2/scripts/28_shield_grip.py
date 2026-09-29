# Matt: "there is no shield grip", and the shield "is not moving as a shield
# would need to as a defensive item."
#
#   blender -b -noaudio --python scripts/28_shield_grip.py -- <body.glb>
#        <shield.glb> [--json f] [--fix <out.glb>]
#
# A Viking round shield is CENTRE-GRIP: a single bar spanning the back of the
# boss, gripped in the middle of the disc. It is not strapped to the forearm
# like a heater shield. So the test is simple and geometric: how far is his
# fist from the centre of the disc, as a fraction of the radius? At 0 the boss
# is over his knuckles and it reads as a centre-grip shield. Near 1 it reads as
# a disc glued to his arm.
#
# Measured in the DISC'S OWN FRAME, not in world axes: in-plane offset is the
# defect, along-normal offset is just the standoff his hand needs behind the
# boss, and a world-axis box cannot tell the two apart. The last shield
# measurement in this run took four instruments before one of them answered the
# question asked; this one starts in the right frame.
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("28_shield_grip.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, SHIELD = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()

# the fist: hand vertices with grip_L CLOSED, because that is the hand the
# shield has to meet. Measuring the open hand measures a hand that is not there
# at runtime.
kb = body[0].data.shape_keys.key_blocks if body[0].data.shape_keys else {}
for nm in ("grip_L",):
    if nm in kb:
        kb[nm].value = 1.0
bpy.context.view_layer.update()
gi = {vg.index: vg.name for vg in body[0].vertex_groups}
hand_idx = [v.index for v in body[0].data.vertices if v.groups and
            gi.get(max(v.groups, key=lambda x: x.weight).group) == "LeftHand"
            and max(v.groups, key=lambda x: x.weight).weight >= 0.30]
W = G.world_verts(body[0])
fist = W[hand_idx]
fist_c = fist.mean(axis=0)
print("left fist: %d vertices, centre %s" % (len(hand_idx), np.round(fist_c, 4).tolist()))

before = set(sc.objects)
bpy.ops.import_scene.gltf(filepath=SHIELD)
# ONLY meshes with vertex groups. Blender's glTF importer invents an Icosphere
# as a custom_shape for EVERY bone, and those are real mesh objects in the
# scene -- 24 of them here, spread over the whole skeleton. Counting them gave
# a "shield" of radius 2.1337 m and thickness 1.9856 m: a 4 m blob, which is
# the armature's widget spread and not a shield at all. Third time in this run
# that these widgets have entered a measurement. They carry no vertex groups,
# which is the one clean thing about them.
shp = [o for o in sc.objects if o not in before and o.type == 'MESH'
       and o.vertex_groups]
junk = [o.name for o in sc.objects if o not in before and o.type == 'MESH'
        and not o.vertex_groups]
print("shield meshes: %s   (ignored %d bone display widgets)"
      % ([o.name for o in shp], len(junk)))
assert shp, "no shield mesh imported"
SV = np.vstack([G.world_verts(o) for o in shp])
ctr = SV.mean(axis=0)
# the disc's own frame: PCA. Smallest eigenvalue is the face normal.
cov = np.cov((SV - ctr).T)
ev, evec = np.linalg.eigh(cov)
normal = evec[:, 0] / np.linalg.norm(evec[:, 0])
inplane = evec[:, 1:]
rad = float(np.linalg.norm((SV - ctr) @ inplane, axis=1).max())
thick = float(np.ptp((SV - ctr) @ normal))
d = fist_c - ctr
off_plane = float(np.linalg.norm(d @ inplane))
off_norm = float(d @ normal)
print("shield: %d verts, radius %.4f m, thickness %.4f m" % (len(SV), rad, thick))
print("  disc normal (world) %s" % np.round(normal, 4).tolist())
print("  FIST relative to the disc centre:")
print("    IN-PLANE  %.4f m  = %.1f%% of the radius   <- the defect if large"
      % (off_plane, 100 * off_plane / rad))
print("    ALONG NORMAL %+.4f m  (behind the face is the correct side)" % off_norm)
# where does the fist sit radially -- boss, mid, or rim?
zone = ("BOSS (centre grip)" if off_plane < 0.20 * rad else
        "inner field" if off_plane < 0.50 * rad else
        "outer field" if off_plane < 0.80 * rad else "RIM")
print("    zone: %s" % zone)
res = dict(fist_centre=[round(float(x), 5) for x in fist_c],
           shield_centre=[round(float(x), 5) for x in ctr],
           radius_m=round(rad, 5), thickness_m=round(thick, 5),
           normal_world=[round(float(x), 5) for x in normal],
           fist_inplane_offset_m=round(off_plane, 5),
           fist_inplane_pct_of_radius=round(100 * off_plane / rad, 1),
           fist_along_normal_m=round(off_norm, 5), zone=zone,
           required_inplane_shift_m=round(off_plane, 5))
if OUTJ:
    json.dump(res, open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
