"""Reference-derived wizard geometry. Run inside the dedicated Blender MCP session.

Coordinates: metres, Z up, -Y forward, character left is +X.
Original reference PNGs remain unchanged; UVs sample them as material atlases.
"""
import bpy
import math
import json
from mathutils import Vector
from pathlib import Path

ROOT = Path('/Users/admin/Games/reincarnated-collaboration/codex-3d-modeling')
for folder in ['assets', 'renders', 'godot/assets', 'logs']:
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

# This script is restricted to the fresh character scene opened by start_blender.py.
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for collection in list(bpy.data.collections):
    if collection.name.startswith('Wizard'):
        bpy.data.collections.remove(collection)
CHAR = bpy.data.collections.new('Wizard_Character')
bpy.context.scene.collection.children.link(CHAR)
STUDIO = bpy.data.collections.new('Wizard_Studio')
bpy.context.scene.collection.children.link(STUDIO)

def material(name, color, metallic=0, roughness=.7, image_path=None):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1)
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color, 1)
    node.inputs['Metallic'].default_value = metallic
    node.inputs['Roughness'].default_value = roughness
    if image_path:
        texture = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texture.image = bpy.data.images.load(str(image_path), check_existing=True)
        texture.image.pack()
        mat.node_tree.links.new(texture.outputs['Color'], node.inputs['Base Color'])
    return mat

PURPLE = material('Royal plum | woven cloth', (.040,.015,.068))
LINING = material('Robe lining | midnight violet', (.045,.026,.071))
GOLD = material('Antique gold | raised piping', (.56,.35,.095), .7,.36)
LEATHER = material('Dark brown leather', (.045,.025,.013),0,.62)
PANTS = material('Charcoal trousers', (.055,.047,.043))
SKIN = material('Warm fair skin', (.56,.365,.26),0,.64)
HAIR = material('Chestnut hair', (.017,.008,.004),0,.72)
HAIR_LIT = material('Chestnut hair ridges', (.029,.014,.007),0,.68)
PAGES = material('Ivory parchment', (.69,.58,.39),0,.85)
FRONT = material('Reference front | original image atlas', (1,1,1),0,.76,
    ROOT/'Codex Image Sep 7, 2026, 08_12_34 PM.png')
BACK = material('Reference rear | original turnaround atlas', (1,1,1),0,.76,
    ROOT/'Codex Image Sep 7, 2026, 08_13_21 PM.png')

def move_collection(obj, collection=CHAR):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)

def skin_weights(obj, bone_or_fn):
    for vertex in obj.data.vertices:
        weights = bone_or_fn(vertex.co) if callable(bone_or_fn) else {bone_or_fn:1.0}
        for name, weight in weights.items():
            if weight > .0001:
                group = obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)
                group.add([vertex.index], weight, 'REPLACE')

def atlas(obj, fallback, back=True, front=True):
    obj.data.materials.clear()
    for mat in [fallback, FRONT, BACK]:
        obj.data.materials.append(mat)
    uv = obj.data.uv_layers.new(name='ReferenceUV')
    obj.data.update()
    for poly in obj.data.polygons:
        n = poly.normal
        use_front = front and n.y < -.45
        use_back = back and n.y > .45
        poly.material_index = 1 if use_front else (2 if use_back else 0)
        for index in poly.loop_indices:
            co = obj.data.vertices[obj.data.loops[index].vertex_index].co
            projection_x = co.x * (0.88 if obj.name.startswith('Tailored upper') else 1.0)
            if use_back:
                u, v = (1222-projection_x*519.5)/1536, 1-(980-co.z*519.5)/1024
            else:
                u, v = (611+projection_x*678)/1223, 1-(1232-co.z*678)/1286
            uv.data[index].uv = (u,v)

def mesh(name, vertices, faces, mat, weights, use_atlas=False, solid=0, sub=0):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    CHAR.objects.link(obj)
    for poly in data.polygons:
        poly.use_smooth = True
    data.materials.append(mat)
    if use_atlas:
        atlas(obj, mat)
    if weights:
        skin_weights(obj, weights)
    if solid:
        modifier = obj.modifiers.new('Tailored thickness','SOLIDIFY')
        modifier.thickness = solid
        modifier.offset = 0
    if sub:
        modifier = obj.modifiers.new('Surface refinement','SUBSURF')
        modifier.levels = sub
        modifier.render_levels = sub
    return obj

def blend_between(z, low, high, lower, upper):
    t=max(0,min(1,(z-low)/(high-low)))
    return {lower:1-t,upper:t}

def torso_weight(co):
    if co.z < 1.2:
        return blend_between(co.z,1.1,1.2,'Hips','Spine')
    return blend_between(co.z,1.25,1.40,'Spine','Chest')

def loft(name, rings, mat, weights, n=32, textured=False, sub=1):
    # rings: (x,y,z,half_width,half_depth); generate smooth elliptical sections.
    vertices=[]
    for x,y,z,rx,ry in rings:
        for i in range(n):
            theta=2*math.pi*i/n
            vertices.append((x+rx*math.sin(theta),y-ry*math.cos(theta),z))
    faces=[]
    for j in range(len(rings)-1):
        for i in range(n):
            a=j*n+i; b=j*n+(i+1)%n
            faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
    return mesh(name,vertices,faces,mat,weights,textured,sub=sub)

def ellipsoid(name,center,scale,mat,bone,segments=24,rings=12,textured=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=center)
    obj=bpy.context.object; obj.name=name; obj.scale=scale
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    move_collection(obj)
    for p in obj.data.polygons: p.use_smooth=True
    obj.data.materials.append(mat)
    if textured: atlas(obj,mat)
    skin_weights(obj,bone)
    return obj

def tube(name, points, radii, mat, weights, n=10):
    vertices=[]
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize()
        a=tangent.cross(Vector((0,1,0))).normalized()
        if a.length < .1: a=Vector((1,0,0))
        b=tangent.cross(a).normalized()
        radius=radii[i] if isinstance(radii,(list,tuple)) else radii
        for j in range(n):
            v=Vector(p)+radius*(math.cos(j*2*math.pi/n)*a+math.sin(j*2*math.pi/n)*b)
            vertices.append(tuple(v))
    faces=[]
    for i in range(len(points)-1):
        for j in range(n):
            faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces += [tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
    return mesh(name,vertices,faces,mat,weights,sub=1)

def box(name,center,size,mat,bone,bevel=.008):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    obj=bpy.context.object; obj.name=name; obj.scale=size
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    move_collection(obj)
    obj.data.materials.append(mat)
    skin_weights(obj,bone)
    if bevel:
        mod=obj.modifiers.new('Rounded edges','BEVEL'); mod.width=bevel; mod.segments=3
    for p in obj.data.polygons: p.use_smooth=True
    return obj

loft('Tailored upper robe',[
    (0,0,1.10,.139,.087),(0,0,1.13,.147,.089),(0,0,1.20,.153,.091),
    (0,0,1.30,.177,.101),(0,0,1.41,.207,.099),(0,0,1.47,.217,.083),
    (0,0,1.50,.170,.071),(0,0,1.515,.086,.060)],PURPLE,torso_weight,textured=True)
loft('Neck',[(0,0,1.49,.046,.045),(0,0,1.53,.048,.044),(0,0,1.58,.049,.046)],SKIN,'Neck')

# Standing collar is open at the throat; edging is real geometry.
verts=[]; faces=[]
for z,rx,ry in [(1.48,.075,.063),(1.515,.075,.060),(1.565,.066,.055)]:
    for i in range(25):
        t=math.radians(28+304*i/24)
        verts.append((rx*math.sin(t),-ry*math.cos(t),z))
for j in range(2):
    for i in range(24): faces.append((j*25+i,j*25+i+1,(j+1)*25+i+1,(j+1)*25+i))
mesh('High collar',verts,faces,PURPLE,'Chest',False,solid=.006,sub=1)
for j in [0,24]:
    tube('Collar gold edge',[verts[j],verts[25+j],verts[50+j]],.0035,GOLD,'Chest')
tube('Collar gold rim',verts[50:],.0032,GOLD,'Chest')

for side,s in [('L',1),('R',-1)]:
    upper=f'UpperArm.{side}'; fore=f'Forearm.{side}'; hand=f'Hand.{side}'
    def arm_weights(co,upper=upper,fore=fore,s=s):
        return blend_between(abs(co.x),.325,.385,upper,fore)
    points=[(s*.198,0,1.465),(s*.245,0,1.431),(s*.300,0,1.359),
            (s*.353,0,1.280),(s*.397,0,1.216),(s*.453,0,1.139),(s*.477,0,1.109)]
    arm=tube('Robe sleeve '+side,points,[.081,.087,.077,.068,.066,.073,.077],PURPLE,arm_weights,n=24)
    ellipsoid('Tailored shoulder '+side,(s*.210,0,1.465),(.089,.086,.058),PURPLE,upper)
    for y in [-.072,.072]:
        tube('Shoulder gold seam '+side,[(s*.130,y*.70,1.504),(s*.205,y,1.505),
             (s*.259,y*.98,1.459),(s*.292,y*.72,1.417)],.0035,GOLD,upper,n=8)
    # Cuff and fitted inner wrist, rings perpendicular to the sleeve.
    axis=(Vector(points[-1])-Vector(points[-2])).normalized()
    for k,radius in [(0,.073),(-.025,.070)]:
        c=Vector(points[-1])+axis*k
        u=axis.cross(Vector((0,1,0))).normalized(); v=axis.cross(u).normalized()
        pts=[tuple(c+radius*(math.cos(i*2*math.pi/32)*u+math.sin(i*2*math.pi/32)*v)) for i in range(33)]
        tube('Cuff gold piping '+side,pts,.004,GOLD,fore,n=8)
    tube('Leather wrist '+side,[(s*.468,0,1.116),(s*.495,0,1.073),(s*.505,0,1.058)],
         [.045,.040,.038],LEATHER,fore,n=16)
    # Palm and individual articulated fingers, relaxed and clear of the tome.
    palm=tube('Palm '+side,[(s*.501,-.001,1.065),(s*.523,-.007,1.027),(s*.541,-.009,1.001)],
        [.033,.037,.030],SKIN,hand,n=16)
    for finger,offset,length in [('Index',-.027,.076),('Middle',-.009,.083),('Ring',.009,.077),('Little',.025,.062)]:
        x=s*(.540+offset); z=1.002-offset*.3
        tube(f'{finger} finger {side}',[(x,-.006,z),(x+s*.014,-.018,z-length*.5),(x+s*.015,-.027,z-length)],
             [.009,.008,.0055],SKIN,f'{finger}.{side}',n=10)
    tube('Thumb '+side,[(s*.510,-.010,1.029),(s*.493,-.026,1.001),(s*.488,-.035,.980)],
         [.013,.011,.007],SKIN,f'Thumb.{side}',n=12)
    # Pants and tall leather boots.
    thigh=f'Thigh.{side}'; shin=f'Shin.{side}'; foot=f'Foot.{side}'
    def leg_weights(co,thigh=thigh,shin=shin):
        if co.z > .98:
            return blend_between(co.z,.98,1.08,thigh,'Hips')
        return blend_between(co.z,.535,.66,shin,thigh)
    trousers=loft('Trousers '+side,[(s*.105,0,1.08,.091,.090),(s*.110,0,1.00,.095,.087),
        (s*.115,.003,.89,.091,.080),(s*.118,-.009,.75,.077,.068),
        (s*.12,-.02,.625,.066,.062),(s*.122,-.008,.555,.065,.058),
        (s*.125,0,.43,.059,.057)],PANTS,leg_weights)
    # The fitted trousers must sit inside the belted robe, including at the hip.
    for vertex in trousers.data.vertices:
        t=max(0,min(1,(vertex.co.z-.60)/.40))
        center=s*(.110 if vertex.co.z <= 1.04 else .105)
        vertex.co.x=center+(vertex.co.x-center)*(1-.43*t)
        vertex.co.y*=1-.30*t
    loft('Boot shaft '+side,[(s*.127,.009,.11,.048,.055),(s*.127,.009,.16,.055,.059),
        (s*.126,.008,.25,.059,.062),(s*.124,.003,.36,.064,.066),
        (s*.123,-.003,.455,.070,.067),(s*.123,-.003,.469,.071,.068)],LEATHER,shin)
    loft('Boot foot '+side,[(s*.128,-.045,.022,.060,.123),(s*.128,-.049,.037,.062,.125),
        (s*.128,-.05,.080,.063,.121),(s*.128,-.027,.129,.054,.090),
        (s*.128,.002,.17,.043,.052)],LEATHER,foot)
    loft('Boot sole '+side,[(s*.128,-.047,.008,.061,.126),(s*.128,-.047,.026,.064,.129),
        (s*.128,-.047,.034,.062,.127)],PANTS,foot,sub=1)
    for z,rx,ry in [(.438,.072,.068),(.194,.058,.063)]:
        pts=[(s*.125+rx*math.sin(t),.003-ry*math.cos(t),z+.010*math.sin(t)) for t in [i*2*math.pi/32 for i in range(33)]]
        tube('Boot strap '+side,pts,.009,LEATHER,shin,n=8)
        box('Boot buckle '+side,(s*.164,-.047,z),(.026,.013,.022),GOLD,shin,.003)

loft('Belt',[ (0,0,1.092,.151,.100),(0,0,1.103,.155,.102),
    (0,0,1.146,.155,.102),(0,0,1.158,.150,.100)],LEATHER,'Hips',textured=True)
# Small diamond buckle in the front.
buckle=box('Belt diamond buckle',(0,-.113,1.125),(.044,.016,.044),GOLD,'Hips',.003)
for vertex in buckle.data.vertices:
    x,z=vertex.co.x,vertex.co.z-1.125
    vertex.co.x=(x-z)/math.sqrt(2); vertex.co.z=1.125+(x+z)/math.sqrt(2)

# Four split panels; flexible cloth weights blend away from the belt.
for name,a0,a1 in [('Front.L',22,89),('Back.L',91,176),('Back.R',184,269),('Front.R',271,338)]:
    verts=[]; faces=[]; n=18; levels=12
    for j in range(levels):
        t=j/(levels-1); z=1.104-.762*t
        rx=.149+.156*t; ry=.105+.080*t
        for i in range(n):
            angle=math.radians(a0+(a1-a0)*i/(n-1))
            pleat=(.003+.004*t)*math.sin(i/(n-1)*math.pi*6)
            verts.append(((rx+pleat)*math.sin(angle),-(ry+pleat)*math.cos(angle),z))
    for j in range(levels-1):
        for i in range(n-1):
            a=j*n+i; faces.append((a,a+n,a+n+1,a+1))
    def cloth_weights(co,name=name):
        t=max(0,min(1,(1.10-co.z)/.12))
        return {'Hips':1-t,'Coat.'+name:t}
    panel=mesh('Split robe '+name,verts,faces,PURPLE,cloth_weights,False,solid=.006,sub=1)
    for edge in [0,n-1]:
        pts=[verts[j*n+edge] for j in range(levels)]
        tube('Panel piping '+name+str(edge),pts,.0045,GOLD,cloth_weights,n=8)
    tube('Panel hem '+name,verts[-n:],.005,GOLD,cloth_weights,n=8)

verts=[(-.045,-.116,1.104),(.045,-.116,1.104),(-.047,-.145,.92),(.047,-.145,.92),
       (-.048,-.178,.69),(.048,-.178,.69),(-.047,-.185,.624),(.047,-.185,.624),(0,-.186,.586)]
faces=[(0,2,3,1),(2,4,5,3),(4,6,7,5),(6,8,7)]
def tabard_weights(co):
    t=max(0,min(1,(1.1-co.z)/.26)); return {'Hips':1-t,'Tabard':t}
mesh('Central pointed tabard',verts,faces,PURPLE,tabard_weights,True,solid=.005,sub=1)
for ids in [[0,2,4,6,8],[1,3,5,7,8]]:
    tube('Tabard edging',[verts[i] for i in ids],.0035,GOLD,tabard_weights,n=8)

# Book is separately weighted rigidly to the pelvis; bindings are actual volumes.
book=(.218,-.071,1.00)
box('Tome page block',book,(.113,.046,.192),PAGES,'Hips',.004)
for y in [-.100,-.041]:
    cover=box('Tome purple cover',(.218,y,1.00),(.126,.012,.207),PURPLE,'Hips',.006)
box('Tome leather spine',(.157,-.071,1.00),(.016,.067,.207),LEATHER,'Hips',.006)
for x in [.166,.270]:
    for z in [.909,1.091]:
        box('Tome gold corner',(x,-.110,z),(.020,.010,.027),GOLD,'Hips',.003)
for z in [.937,1.052]:
    box('Tome spine binding',(.153,-.071,z),(.019,.070,.012),GOLD,'Hips',.003)
box('Tome retaining strap',(.218,-.116,1.001),(.140,.013,.021),LEATHER,'Hips',.003)
box('Tome clasp',(.240,-.126,1.001),(.020,.009,.029),GOLD,'Hips',.003)
for x in [.180,.246]:
    tube('Tome belt loop',[(x,-.07,1.138),(x,-.101,1.127),(x,-.106,1.087)],.009,LEATHER,'Hips',n=10)
for i in range(17):
    box('Page edge',(.282,-.070,.915+i*.010),(.002,.041,.001),LEATHER,'Hips',0)
tube('Tome diamond sigil',[(.218,-.110,1.066),(.242,-.110,1.031),
     (.218,-.110,.996),(.194,-.110,1.031),(.218,-.110,1.066)],.0025,GOLD,'Hips',n=8)

# Head: deliberately sculpted profile, with reference UVs retaining identity.
head=loft('Sculpted head',[(0,-.014,1.552,.028,.035),(0,-.012,1.560,.044,.045),
    (0,-.005,1.578,.063,.055),(0,0,1.608,.071,.063),(0,.002,1.638,.077,.071),
    (0,.003,1.665,.075,.071),(0,.007,1.700,.074,.070),(0,.012,1.735,.071,.068),
    (0,.014,1.761,.049,.045),(0,.012,1.776,.015,.015)],SKIN,'Head',n=48,textured=True,sub=2)
# Add nose bridge and tip, keeping the front-atlas identity consistent.
nose=mesh('Nose sculpt',[(-.010,-.063,1.687),(.010,-.063,1.687),
    (-.009,-.085,1.655),(.009,-.085,1.655),(-.014,-.096,1.635),(.014,-.096,1.635),
    (-.014,-.073,1.625),(.014,-.073,1.625),(0,-.109,1.638)],
    [(0,2,3,1),(2,4,8,3),(3,8,5),(4,6,7,5,8),(0,6,4,2),(1,3,5,7)],SKIN,'Head',True,sub=2)
for s in [-1,1]:
    ellipsoid('Ear',(s*.078,.002,1.640),(.013,.017,.028),SKIN,'Head')

# Swept-back hair shell; its front boundary follows a shallow widow's peak.
verts=[]; faces=[]; n=48; rows=13
for j in range(rows):
    t=j/(rows-1)
    for i in range(n):
        phi=2*math.pi*i/n
        bottom=1.620 if math.cos(phi)<-.1 else 1.727-.012*math.cos(phi)**4
        z=bottom+(1.790-bottom)*math.sin(t*math.pi/2)
        radius=math.cos(t*math.pi/2)
        verts.append((.084*radius*math.sin(phi),.012-.082*radius*math.cos(phi),z))
for j in range(rows-1):
    for i in range(n):
        a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
mesh('Swept hair mass',verts,faces,HAIR,'Head',sub=1)
ellipsoid('Loose tied hair bun',(0,.093,1.744),(.040,.034,.041),HAIR,'Head')
for i in range(17):
    x=(i-8)*.0093
    tube('Swept hair lock',[(x,-.065,1.722+.010*abs(x)/.075),
        (x*.97,-.046,1.754),(x*.88,-.012,1.781),(x*.68,.032,1.783),
        (x*.40,.067,1.764),(x*.1,.10,1.744)],
        [.003,.006,.006,.005,.004,.001],HAIR_LIT if i%3==0 else HAIR,'Head',n=8)
for s in [-1,1]:
    tube('Temple loose lock',[(s*.063,-.048,1.731),(s*.071,-.062,1.690),
        (s*.068,-.066,1.650),(s*.080,-.039,1.612)], [.011,.010,.008,.0015],HAIR,'Head')
    tube('Nape loose lock',[(s*.042,.061,1.707),(s*.052,.079,1.640),(s*.049,.073,1.575)],
        [.015,.011,.002],HAIR,'Head')

# Apply refinement before rigging so the exported weights are deterministic.
for obj in list(CHAR.objects):
    import bmesh
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data);bm.free()
    bpy.context.view_layer.objects.active=obj
    obj.select_set(True)
    for modifier in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.data.validate(clean_customdata=False)
    obj.select_set(False)

# A modest neutral studio is only for reviewing the modeled geometry.
floor_mat=material('Studio graphite',(.055,.066,.079),0,.82)
bpy.ops.mesh.primitive_plane_add(size=200)
floor=bpy.context.object;floor.name='Studio ground';floor.location.z=-.002
move_collection(floor,STUDIO);floor.data.materials.append(floor_mat)
world=bpy.context.scene.world or bpy.data.worlds.new('Wizard studio world')
bpy.context.scene.world=world;world.use_nodes=True
world.node_tree.nodes.get('Background').inputs[0].default_value=(.20,.24,.30,1)
world.node_tree.nodes.get('Background').inputs[1].default_value=.35
def light(name,loc,power,size,color):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);STUDIO.objects.link(obj);obj.location=loc
    obj.rotation_euler=(Vector((0,0,1))-obj.location).to_track_quat('-Z','Y').to_euler()
light('Large warm key',(-3,-4,5),450,4,(1,.89,.76))
light('Soft cool fill',(3,-2,2.5),250,3,(.69,.80,1))
light('Hair and robe rim',(1,3,4),250,3,(.85,.90,1))
data=bpy.data.cameras.new('Wizard camera');camera=bpy.data.objects.new('Wizard camera',data)
STUDIO.objects.link(camera);camera.location=(2.4,-5,2.5)
camera.rotation_euler=(Vector((0,0,.96))-camera.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO';data.ortho_scale=2.3;bpy.context.scene.camera=camera
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1000;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/purple_wizard.blend'))
report={'meshes':len(CHAR.objects),'vertices':sum(len(o.data.vertices) for o in CHAR.objects),
        'triangles':sum(len(p.vertices)-2 for o in CHAR.objects for p in o.data.polygons)}
(ROOT/'logs/geometry.json').write_text(json.dumps(report,indent=2))
print('WIZARD_GEOMETRY',json.dumps(report))
