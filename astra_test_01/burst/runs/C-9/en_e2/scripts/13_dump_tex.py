# Pull the base-colour image out of a GLB. Sheet B's canvas needs it: where
# sheet A's cameras were blind, the canvas must show FLAT RENDER, and that is
# this texture, not the island-fill guess the bake leaves behind.
import bpy, os, sys
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
img = None
for o in bpy.context.scene.objects:
    if o.type != 'MESH' or not o.vertex_groups:
        continue
    for s in o.material_slots:
        if s.material and s.material.node_tree:
            for n in s.material.node_tree.nodes:
                if n.type == 'TEX_IMAGE' and n.image:
                    img = n.image
assert img, "no image texture on a skinned mesh"
img.filepath_raw = a[1]; img.file_format = 'PNG'; img.save()
print("wrote %s  %dx%d" % (a[1], img.size[0], img.size[1]))
