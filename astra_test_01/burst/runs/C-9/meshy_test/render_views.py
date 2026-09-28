# Render the Meshy GLB unlit (emission = base colour) from the 4 cardinal + 4 diagonal directions at the stills' fitted
# ortho elevation (19.77 deg, drax M-a), so the texture is judged as paint, not as 3D lighting.
import bpy, math, sys
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]; src,outdir=args[0],args[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
objs=[o for o in bpy.context.scene.objects if o.type=='MESH']
# unlit: route base colour texture to emission
for o in objs:
    for slot in o.material_slots:
        m=slot.material
        if not m or not m.use_nodes: continue
        nt=m.node_tree; bsdf=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bsdf: continue
        link=bsdf.inputs['Base Color'].links
        out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        em=nt.nodes.new('ShaderNodeEmission')
        if link: nt.links.new(link[0].from_socket, em.inputs['Color'])
        else: em.inputs['Color'].default_value=bsdf.inputs['Base Color'].default_value
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
# bounds
mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
for o in objs:
    for c in o.bound_box:
        w=o.matrix_world@Vector(c); mn=Vector(map(min,mn,w)); mx=Vector(map(max,mx,w))
ctr=(mn+mx)/2; H=max(mx-mn)
sc=bpy.context.scene; sc.render.engine='BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
sc.render.resolution_x=512; sc.render.resolution_y=512; sc.render.film_transparent=True
sc.view_settings.view_transform='Standard'
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=H*1.15
el=math.radians(19.77); up_axis = 'Y' if (mx-mn).y>(mx-mn).z else 'Z'
print('bbox',mn,mx,'up',up_axis)
for name,az in [('S',0),('SE',45),('E',90),('NE',135),('N',180),('NW',225),('W',270),('SW',315)]:
    a=math.radians(az); d=10*H
    if up_axis=='Z':
        # glTF import converts Y-up to Z-up; front of model faces -Y
        pos=ctr+Vector((d*math.sin(a)*math.cos(el), -d*math.cos(a)*math.cos(el), d*math.sin(el)))
    else:
        pos=ctr+Vector((d*math.sin(a)*math.cos(el), d*math.sin(el), d*math.cos(a)*math.cos(el)))
    cam.location=pos
    dirv=(ctr-pos); cam.rotation_euler=dirv.to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{outdir}/view_{name}.png'; bpy.ops.render.render(write_still=True)
