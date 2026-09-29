# T8 look renders: unlit (emission = base colour) ortho views of a GLB, named by the figure's FACING (game convention:
# facing E = screen right), at a given elevation (R-C9-68: 52.95354112560294 = the world camera). Model faces -Y after glTF import.
import bpy, math, sys
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src,outdir,el_deg=a[0],a[1],float(a[2]); facings=a[3].split(',')
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=src)
objs=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in objs:
    for s in o.material_slots:
        m=s.material
        if not m or not m.use_nodes: continue
        nt=m.node_tree; b=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not b: continue
        out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL'); em=nt.nodes.new('ShaderNodeEmission'); L=b.inputs['Base Color'].links
        if L: nt.links.new(L[0].from_socket,em.inputs['Color'])
        else: em.inputs['Color'].default_value=b.inputs['Base Color'].default_value
        nt.links.new(em.outputs['Emission'],out.inputs['Surface'])
dg=bpy.context.evaluated_depsgraph_get(); mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
for o in objs:
    for c in o.bound_box: w=o.matrix_world@Vector(c); mn=Vector(map(min,mn,w)); mx=Vector(map(max,mx,w))
ctr=(mn+mx)/2; H=(mx-mn).z
sc=bpy.context.scene; eng=[e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine='BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x=768; sc.render.resolution_y=768; sc.render.film_transparent=True; sc.view_settings.view_transform='Standard'
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=H*1.15; el=math.radians(el_deg)
FAC={'S':0,'SE':45,'E':90,'NE':135,'N':180,'NW':225,'W':270,'SW':315}
for f in facings:
    az=math.radians((360-FAC[f])%360); d=10*H
    pos=ctr+Vector((d*math.sin(az)*math.cos(el),-d*math.cos(az)*math.cos(el),d*math.sin(el)))
    cam.location=pos; cam.rotation_euler=(ctr-pos).to_track_quat('-Z','Y').to_euler(); bpy.context.view_layer.update()
    sc.render.filepath=f'{outdir}/face_{f}_el{int(round(el_deg))}.png'; bpy.ops.render.render(write_still=True)
print('bbox',tuple(round(x,3) for x in mn),tuple(round(x,3) for x in mx))
