# Test 4 driving video: the Meshy knight's carry walk, in place, unlit, rendered as a smooth video at the stills' camera
# (ortho, 19.77 deg elevation), facing screen-right. Args: glb outdir az_deg n_frames fps size fig_px
import bpy, math, sys
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src,outdir,az,N,FPS,SIZE,FIG=a[0],a[1],float(a[2]),int(a[3]),float(a[4]),int(a[5]),float(a[6])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
for o in [o for o in bpy.context.scene.objects if o.type=='MESH']:
    if not any(m.type=='ARMATURE' for m in o.modifiers) and o.parent!=arm: o.hide_render=True   # stray unskinned meshes (the Icosphere)
    for slot in o.material_slots:
        m=slot.material
        if not m or not m.use_nodes: continue
        nt=m.node_tree; bsdf=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if not bsdf: continue
        link=bsdf.inputs['Base Color'].links; out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
        em=nt.nodes.new('ShaderNodeEmission')
        if link: nt.links.new(link[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
act=arm.animation_data.action; f0,f1=act.frame_range; clip_fps=24.0
sc=bpy.context.scene; sc.render.resolution_x=SIZE; sc.render.resolution_y=SIZE; sc.render.film_transparent=True; sc.view_settings.view_transform='Standard'
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam; cam.data.type='ORTHO'
cam.data.ortho_scale=1.8*SIZE/FIG
hips=next((b for b in arm.pose.bones if 'hip' in b.name.lower()), arm.pose.bones[0])
el=math.radians(19.77); A=math.radians(az); d=20.0; span=f1-f0
for i in range(N):
    t=i/FPS; fr=f0+ (t*clip_fps) % span
    sc.frame_set(int(fr), subframe=fr-int(fr))
    hw=arm.matrix_world@hips.head; aim=Vector((hw.x,hw.y,0.9))
    pos=aim+Vector((d*math.sin(A)*math.cos(el), -d*math.cos(A)*math.cos(el), d*math.sin(el)))
    cam.location=pos; cam.rotation_euler=(aim-pos).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{outdir}/d_{i:04d}.png'; bpy.ops.render.render(write_still=True)
