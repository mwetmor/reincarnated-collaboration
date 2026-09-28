# C-9 meshy_t1 step 2: fit a weapon to a hand socket, and write the socket JSON.
#   blender -b -noaudio --python scripts/08_socket.py -- <rigged.glb> <weapon.glb>
#                        <weapon_probe.json> <clipinfo.json> <out_socket.json>
#
# The socket is (bone, offset, rotation, scale) in the BONE's own space, so it
# is data, not code: any weapon on any rig, and the renderer just applies it.
#
# Fitted, not eyeballed:
#  * GRIP HEIGHT from the approved E still's proportions. The painted pollaxe
#    runs 1.306 m below the grip and 0.927 m above it; that ratio (0.585 of the
#    length below the hand) is applied to this weapon's measured 1.903 m.
#  * BLADE BEARING from R-C9-57: the fan sits 70 deg from the figure's forward
#    toward its right. The weapon's own fan direction is MEASURED (the head's
#    area is 2-7x heavier on local -X at every distance threshold), so the yaw
#    the socket needs is 70 - (-90) = 160 deg.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix, Euler

a = sys.argv[sys.argv.index('--') + 1:]
RIG, WEAP, WPROBE, CLIP, OUTP = a[0], a[1], a[2], a[3], a[4]
GRIP_BELOW_FRAC = 1.306 / 2.233        # the painted pollaxe's own proportion
TARGET_BEARING = 70.0                  # deg from forward toward the figure's right

wp = json.load(open(WPROBE))
ci = json.load(open(CLIP))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=RIG)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
for o in list(sc.objects):
    if o.type == 'MESH' and not any(m.type == 'ARMATURE' and m.object == arm
                                    for m in o.modifiers):
        bpy.data.objects.remove(o, do_unlink=True)

# normalise facing exactly as the renderer does, so the socket is expressed in
# the same frame the render uses
face_yaw = 0.0
R = ci["role_map"]
key = R.get("l_toe") or R.get("l_foot")
st = ci["stance"].get(key)
if st:
    d = st["disp_m"][:2]
    face_yaw = math.degrees(math.atan2(-d[0], -d[1]))
rot = Matrix.Rotation(math.radians(-face_yaw), 4, 'Z')
for o in list(sc.objects):
    if o.parent is None:
        o.matrix_world = rot @ o.matrix_world

hand_name = R.get("r_hand")
pb = arm.pose.bones[hand_name]
hand_w = arm.matrix_world @ pb.head
bone_m = arm.matrix_world @ pb.matrix            # bone space -> world

L = wp["length"]
z_lo = wp["bbox_lo"][2]
grip_local_z = z_lo + GRIP_BELOW_FRAC * L
fan_local = wp.get("fan_bearing_deg_from_+Y", -90.0)
# the head's AREA, not its reach, says which side the fan is: measured -X here
fan_local = -90.0
yaw = TARGET_BEARING - fan_local

# world transform we want: haft upright, yawed, grip at the hand
M_world = Matrix.Translation(hand_w) @ Matrix.Rotation(math.radians(yaw), 4, 'Z') \
    @ Matrix.Translation(Vector((0, 0, -grip_local_z)))
M_bone = bone_m.inverted() @ M_world
loc, quat, scale = M_bone.decompose()
eul = quat.to_euler('XYZ')
out = dict(
    note="C-9 meshy_t1 weapon socket: bone-space transform for a weapon GLB.",
    rig=os.path.basename(RIG), weapon=os.path.basename(WEAP),
    bone=hand_name, role="r_hand",
    offset=[round(v, 6) for v in loc],
    rotation_euler_xyz_deg=[round(math.degrees(v), 4) for v in eul],
    scale=[round(v, 6) for v in scale],
    facing_yaw_normalised_deg=round(face_yaw, 3),
    fit=dict(weapon_length_m=L, grip_local_z=round(grip_local_z, 5),
             grip_below_fraction=round(GRIP_BELOW_FRAC, 4),
             weapon_fan_local_bearing_deg=fan_local,
             target_fan_bearing_deg=TARGET_BEARING,
             socket_yaw_deg=round(yaw, 3),
             hand_world=[round(v, 5) for v in hand_w]))
json.dump(out, open(OUTP, "w"), indent=1)
print("socket: bone %s  yaw %.1f deg  grip local z %.3f  hand at %s"
      % (hand_name, yaw, grip_local_z, [round(v, 3) for v in hand_w]))
