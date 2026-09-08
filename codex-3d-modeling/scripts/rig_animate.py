"""Create a deform skeleton and three looping, in-place locomotion clips."""
import bpy
import math
import json
from pathlib import Path
from mathutils import Vector, Quaternion
ROOT=Path('/Users/admin/Games/reincarnated-collaboration/codex-3d-modeling')
char=bpy.data.collections['Wizard_Character']
for obj in list(char.objects):
    if obj.type=='ARMATURE': bpy.data.objects.remove(obj,do_unlink=True)
for action in list(bpy.data.actions):
    if action.name in ['Idle','Walk','Run']:
        bpy.data.actions.remove(action)
bpy.ops.object.select_all(action='DESELECT')
data=bpy.data.armatures.new('Wizard humanoid skeleton')
rig=bpy.data.objects.new('WizardRig',data);char.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None):
    b=data.edit_bones.new(name);b.head=head;b.tail=tail
    if parent:b.parent=data.edit_bones[parent]
    return b
bone('Root',(0,0,0),(0,0,.12))
bone('Hips',(0,0,1.045),(0,0,1.16),'Root')
bone('Spine',(0,0,1.16),(0,0,1.31),'Hips')
bone('Chest',(0,0,1.31),(0,0,1.49),'Spine')
bone('Neck',(0,0,1.49),(0,0,1.575),'Chest')
bone('Head',(0,0,1.575),(0,0,1.77),'Neck')
for side,s in [('L',1),('R',-1)]:
    bone('UpperArm.'+side,(s*.205,0,1.465),(s*.355,0,1.277),'Chest')
    bone('Forearm.'+side,(s*.355,0,1.277),(s*.5,0,1.063),'UpperArm.'+side)
    bone('Hand.'+side,(s*.5,0,1.063),(s*.54,-.009,1.00),'Forearm.'+side)
    for name,offset,length in [('Index',-.027,.076),('Middle',-.009,.083),('Ring',.009,.077),('Little',.025,.062)]:
        x=s*(.540+offset);z=1.002-offset*.3
        bone(name+'.'+side,(x,-.006,z),(x+s*.015,-.027,z-length),'Hand.'+side)
    bone('Thumb.'+side,(s*.510,-.010,1.029),(s*.488,-.035,.980),'Hand.'+side)
    bone('Thigh.'+side,(s*.110,0,1.045),(s*.120,-.025,.62),'Hips')
    bone('Shin.'+side,(s*.120,-.025,.62),(s*.127,.009,.14),'Thigh.'+side)
    bone('Foot.'+side,(s*.127,.009,.14),(s*.128,-.116,.042),'Shin.'+side)
    bone('Toe.'+side,(s*.128,-.116,.042),(s*.128,-.17,.035),'Foot.'+side)
    for prefix,y in [('Front',-.080),('Back',.080)]:
        bone('Coat.'+prefix+'.'+side,(s*.11,y,1.10),(s*.19,y*1.6,.46),'Hips')
bone('Tabard',(0,-.116,1.10),(0,-.18,.62),'Hips')
bpy.ops.object.mode_set(mode='OBJECT')
rig.show_in_front=True

unweighted=0
for obj in list(char.objects):
    if obj.type!='MESH':continue
    obj.data.validate(clean_customdata=False)
    # All generated groups must resolve to the actual deform skeleton.
    for group in obj.vertex_groups:
        assert group.name in data.bones, (obj.name,group.name)
    for v in obj.data.vertices:
        total=sum(g.weight for g in v.groups)
        if total < .999 or total > 1.001:unweighted+=1
    for old in list(obj.modifiers):
        if old.type=='ARMATURE':obj.modifiers.remove(old)
    mod=obj.modifiers.new('Wizard deform','ARMATURE');mod.object=rig
    obj.parent=rig
assert unweighted==0, f'Non-normalized vertex weights: {unweighted}'
rest={b.name:b.matrix_local.to_quaternion() for b in data.bones}
identity=Quaternion((1,0,0,0))
def rotation(axis,angle):return Quaternion(Vector(axis),angle)

def author_clip(name,frames):
    rig.animation_data_create()
    action=bpy.data.actions.new(name)
    rig.animation_data.action=action
    for frame in range(frames+1):
        phase=frame/frames
        desired={}
        def orient(name,delta=identity):
            b=data.bones[name];parent=b.parent
            base=rest[name] if not parent else desired[parent.name]@rest[parent.name].inverted()@rest[name]
            world=delta@rest[name]
            pb=rig.pose.bones[name];pb.rotation_mode='QUATERNION'
            pb.rotation_quaternion=base.inverted()@world
            pb.location=(0,0,0)
            desired[name]=world
        t=2*math.pi*phase
        moving=name!='Idle';running=name=='Run'
        bob=(.012 if running else .009)*math.cos(2*t) if moving else .002*math.sin(t)
        drop=(-.075 if running else -.035) if moving else 0
        orient('Root');orient('Hips')
        rig.pose.bones['Hips'].location=rest['Hips'].inverted()@Vector((0,0,drop+bob))
        lean=.10 if running else (.025 if moving else .004*math.sin(t))
        orient('Spine',rotation((1,0,0),lean*.4))
        orient('Chest',rotation((1,0,0),lean))
        orient('Neck',rotation((1,0,0),lean*.4))
        orient('Head',rotation((1,0,0),lean*.15))
        for side,s in [('L',1),('R',-1)]:
            p=(phase+(0 if s==1 else .5))%1
            swing=math.sin(2*math.pi*p)
            arm_swing=(.60 if running else .29)*swing if moving else .012*math.sin(t)
            # Hold elbows slightly away from the belted tome.
            arm_delta=rotation((1,0,0),arm_swing)@rotation((0,1,0),s*.49)
            orient('UpperArm.'+side,arm_delta)
            fore_delta=rotation((1,0,0),arm_swing-(.9 if running else .17))@rotation((0,1,0),s*.49)
            orient('Forearm.'+side,fore_delta)
            orient('Hand.'+side,fore_delta)
            for finger in ['Index','Middle','Ring','Little','Thumb']:
                orient(finger+'.'+side,fore_delta)
            if moving:
                stance=.40 if running else .60
                stride=.36 if running else .28
                if p<stance:
                    foot_y=-stride+2*stride*p/stance
                    lift=0
                else:
                    q=(p-stance)/(1-stance)
                    foot_y=stride*math.cos(math.pi*q)
                    lift=(.20 if running else .105)*math.sin(math.pi*q)
                hip=Vector((s*.110,0,1.045+drop+bob))
                ankle=Vector((s*.127,foot_y,.14+lift))
                upper_len=data.bones['Thigh.'+side].length
                lower_len=data.bones['Shin.'+side].length
                direction=ankle-hip;d=min(direction.length,upper_len+lower_len-.002)
                unit=direction.normalized()
                a=(upper_len**2-lower_len**2+d*d)/(2*d)
                h=math.sqrt(max(0,upper_len**2-a*a))
                perpendicular=Vector((0,unit.z,-unit.y)).normalized()
                knee=hip+a*unit+h*perpendicular
                rest_upper=data.bones['Thigh.'+side].tail_local-data.bones['Thigh.'+side].head_local
                rest_lower=data.bones['Shin.'+side].tail_local-data.bones['Shin.'+side].head_local
                orient('Thigh.'+side,rest_upper.rotation_difference(knee-hip))
                orient('Shin.'+side,rest_lower.rotation_difference(ankle-knee))
                orient('Foot.'+side)
                orient('Toe.'+side)
            else:
                for part in ['Thigh','Shin','Foot','Toe']:orient(part+'.'+side)
            # The coat must clear the actual solved knee, including its forward
            # excursion during stance. A sine-only sway clips through the thigh.
            front_angle=min(-.04, math.atan2(knee.y-hip.y,hip.z-knee.z)-.12) if moving else -.025+.009*math.sin(t+s)
            back_angle=max(.04, math.atan2(ankle.y,1.10-ankle.z)+.08) if moving else .025-.009*math.sin(t+s)
            orient('Coat.Front.'+side,rotation((1,0,0),front_angle)@rotation((0,1,0),-s*.055))
            orient('Coat.Back.'+side,rotation((1,0,0),back_angle)@rotation((0,1,0),-s*.055))
        orient('Tabard',rotation((1,0,0),-.12-((.12 if running else .06)*abs(math.sin(t)) if moving else 0)))
        for pb in rig.pose.bones:
            pb.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=pb.name)
            if pb.name=='Hips':pb.keyframe_insert(data_path='location',frame=frame,group=pb.name)
    action.use_fake_user=True
    track=rig.animation_data.nla_tracks.new();track.name=name
    strip=track.strips.new(name,0,action);strip.action_frame_start=0;strip.action_frame_end=frames
    track.mute=True
    return action

clips=[author_clip('Idle',90),author_clip('Walk',24),author_clip('Run',18)]
rig.animation_data.action=clips[0]
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=0;scene.frame_end=90;scene.frame_set(0)
bpy.ops.object.select_all(action='DESELECT')
for obj in char.objects:obj.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/purple_wizard.blend'))
kwargs=dict(filepath=str(ROOT/'godot/assets/purple_wizard.glb'),export_format='GLB',
    use_selection=True,export_animations=True,export_skins=True,export_yup=True,
    export_animation_mode='ACTIONS',export_force_sampling=True,export_frame_range=False)
supported=bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
kwargs={k:v for k,v in kwargs.items() if k in supported}
bpy.ops.export_scene.gltf(**kwargs)
report={'bones':len(data.bones),'clips':{a.name:list(a.frame_range) for a in clips},
    'weights_normalized':True,'in_place':True,'export':str(ROOT/'godot/assets/purple_wizard.glb')}
(ROOT/'logs/rig.json').write_text(json.dumps(report,indent=2))
print('WIZARD_RIG',json.dumps(report))
