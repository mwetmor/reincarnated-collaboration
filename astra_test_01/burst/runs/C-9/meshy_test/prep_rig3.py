import bpy, sys
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src,dst=a[0],a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
body=[o for o in bpy.context.scene.objects if o.type=='MESH'][0]
bpy.context.view_layer.objects.active=body; body.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
def bb(o):
    ws=[o.matrix_world@Vector(c) for c in o.bound_box]
    return Vector((min(w.x for w in ws),min(w.y for w in ws),min(w.z for w in ws))),Vector((max(w.x for w in ws),max(w.y for w in ws),max(w.z for w in ws)))
rm=[]
for o in parts:
    mn,mx=bb(o); c=(mn+mx)/2
    if c.x>0.545 or (mn.z>0.5 and c.x>0.44): rm.append(o)
zs=[(round(bb(o)[0].z,2),round(bb(o)[1].z,2)) for o in rm]
print('removing',len(rm),'islands; z span',min(z[0] for z in zs),'..',max(z[1] for z in zs),'faces',sum(len(o.data.polygons) for o in rm))
for o in rm: bpy.data.objects.remove(o,do_unlink=True)
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join()
body=bpy.context.view_layer.objects.active; n0=len(body.data.polygons)
m=body.modifiers.new('dec','DECIMATE'); m.ratio=240000/n0; bpy.ops.object.modifier_apply(modifier='dec')
print('faces',n0,'->',len(body.data.polygons))
for img in bpy.data.images:
    if img.size[0]>2048: img.scale(2048,2048)
bpy.ops.export_scene.gltf(filepath=dst,export_format='GLB',export_image_format='JPEG',export_jpeg_quality=90)
