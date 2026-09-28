# Render one animation cycle, unlit, from a given azimuth at the stills' 19.77 deg ortho elevation; follow the hips horizontally (in-place sprites).
import bpy, math, sys
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src,outdir,az,nf=a[0],a[1],float(a[2]),int(a[3])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in meshes:
    for slot in o.material_slots:
        m=slot.material
        if not m or not m.use_nodes: continue
        nt=m.node_tree; bsdf=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bsdf: continue
        link=bsdf.inputs['Base Color'].links; out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        em=nt.nodes.new('ShaderNodeEmission')
        if link: nt.links.new(link[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
act=arm.animation_data.action if arm.animation_data else None
f0,f1=(int(act.frame_range[0]),int(act.frame_range[1])) if act else (1,1)
print('action',act.name if act else None,'frames',f0,f1,'bones',[b.name for b in arm.pose.bones][:8])
sc=bpy.context.scene; sc.render.resolution_x=512; sc.render.resolution_y=512; sc.render.film_transparent=True; sc.view_settings.view_transform='Standard'
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam; cam.data.type='ORTHO'
hips=next((b for b in arm.pose.bones if 'hip' in b.name.lower()), arm.pose.bones[0])
el=math.radians(19.77); A=math.radians(az); d=20.0
cam.data.ortho_scale=512/117.5   # 117.5 px/m: helm-to-sole ~199 px as the Grok cells
# ground: lowest vertex at rest ~ 0; aim point = hips xy, fixed z so the ground line stays put
for i in range(nf):
    fr=f0+(f1-f0)*i/nf; sc.frame_set(int(fr), subframe=fr-int(fr))
    hw=arm.matrix_world@hips.head
    aim=Vector((hw.x,hw.y,1.284))   # sole lands on the game ground row ~398
    pos=aim+Vector((d*math.sin(A)*math.cos(el), -d*math.cos(A)*math.cos(el), d*math.sin(el)))
    cam.location=pos; cam.rotation_euler=(aim-pos).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{outdir}/f_{i:02d}.png'; bpy.ops.render.render(write_still=True)
