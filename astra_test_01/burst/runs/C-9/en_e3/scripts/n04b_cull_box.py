# EN-E3: delete a Tripo artefact inside a world-space box (prep mesh, metres, Blender axes) and re-export, keeping material + UVs.
#   blender -b -noaudio --python scripts/n04b_cull_box.py -- <in.glb> <out.glb> x0 x1 y0 y1 z0 z1
# Why (frosthorn): the sheet's side views draw the FAR legs offset from the near ones, and Tripo built them as a SECOND hind pair
# under the belly centre (footprint grid: ground contact at y 0.0..0.3, |x| < 0.4, between the real fore and hind feet). The
# underside the cull opens is never seen from the game camera (52.95 deg down).
import bpy, bmesh, sys, json
a = sys.argv[sys.argv.index('--') + 1:]; IN, OUT = a[0], a[1]; x0, x1, y0, y1, z0, z1 = map(float, a[2:8])
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=IN)
ob = max((o for o in bpy.context.scene.objects if o.type == 'MESH'), key=lambda o: len(o.data.vertices))
bm = bmesh.new(); bm.from_mesh(ob.data); M = ob.matrix_world
kill = [v for v in bm.verts if (lambda p: x0 <= p.x <= x1 and y0 <= p.y <= y1 and z0 <= p.z <= z1)(M @ v.co)]
n0 = len(bm.verts); bmesh.ops.delete(bm, geom=kill, context='VERTS')
# (no island pass: a Tripo fur body is hundreds of small islands -- an island-size drop deleted 94 % of it on the first run)
small = []
bm.to_mesh(ob.data); bm.free()
for o in bpy.context.scene.objects: o.select_set(o == ob)
bpy.context.view_layer.objects.active = ob
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=95)
print(json.dumps(dict(culled_box=[x0, x1, y0, y1, z0, z1], verts_in=n0, verts_culled=len(kill), island_verts_dropped=len(small), verts_out=len(ob.data.vertices))))
