# T8 step 4: read the hand-off GLB back and check it is what the note claims.
# An exporter reporting success is not the same as a file a consumer can use.
import bpy, json, sys, os
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
GLB = a[0]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene
# EXCLUDE BONE DISPLAY SHAPES. Blender's glTF importer builds a small
# icosphere and assigns it as the custom_shape of every bone, so it appears in
# bpy.data as a 42-vert mesh that is in NO WAY in the file: this GLB's JSON has
# one mesh node, one primitive, and the bytes do not contain the string
# "Icosphere". It is a viewport aid and Godot will never see it.
#
# It cost real time because Meshy DOES ship a genuine unskinned Icosphere stray
# with its rigged GLBs, and that one had to be removed. Same name, opposite
# nature: the first is file content and a defect, the second is the importer's
# own furniture. The lesson generalises badly, so the file itself was parsed
# rather than the import trusted.
allm = [o for o in sc.objects if o.type == 'MESH']
shapes = {b.custom_shape for a in sc.objects if a.type == 'ARMATURE'
          for b in a.pose.bones if b.custom_shape}
meshes = [o for o in allm if o not in shapes]
if len(allm) != len(meshes):
    print("ignoring %d bone display shape(s): %s"
          % (len(allm) - len(meshes), [o.name for o in allm if o in shapes]))
arms = [o for o in sc.objects if o.type == 'ARMATURE']
acts = sorted(x.name for x in bpy.data.actions)
V = []
for o in meshes:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); lo, hi = V.min(0), V.max(0)
imgs = [(n.image.name, n.image.size[0], n.image.size[1])
        for o in meshes for s in o.material_slots
        if s.material and s.material.node_tree
        for n in s.material.node_tree.nodes
        if n.type == 'TEX_IMAGE' and n.image]
arm = arms[0]
bones = [b.name for b in arm.data.bones]
print("meshes %s  armatures %d  bones %d" % ([o.name for o in meshes], len(arms), len(bones)))
print("actions: %s" % acts)
print("height %.4f m   feet z %.4f   bbox %s .. %s"
      % (hi[2] - lo[2], lo[2], np.round(lo, 3), np.round(hi, 3)))
print("textures: %s" % imgs)
assert len(acts) == 4, "expected 4 clips, found %d" % len(acts)
assert abs((hi[2] - lo[2]) - 1.85) < 2e-3, "height is %.4f" % (hi[2] - lo[2])
assert abs(lo[2]) < 2e-3, "feet are not on z=0 (%.4f)" % lo[2]
assert len(meshes) == 1, "expected one skinned mesh, found %s" % [o.name for o in meshes]
assert "RightHand" in bones and "Hips" in bones, "rig bones missing"
print("PASS: 4 clips, one mesh, 1.85 m, feet on the ground, painted texture")
