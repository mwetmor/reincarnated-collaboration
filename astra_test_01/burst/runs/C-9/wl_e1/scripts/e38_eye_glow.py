# STAGE J (3b, Matt R-C9-121: "I cannot discern the eye slits"): an EMISSION MASK painted into the helm's own UVs -- no light.
# The slit is found on the helm's painted texture: FRONT-facing faces (normal toward his forward, Blender -Y) whose texel at the
# face's UV centre is the visor's violet lining (hue 255-320 deg, sat > 0.20, value < 0.75) -- the T-shaped visor slot -- kept to
# the HORIZONTAL eye slit (the upper EYE_BAND m of that slot's height). Those faces' UV triangles are rasterised into a mask,
# dilated by DIL px; the emission is the glow colour on the mask and a hot near-white CORE where the mask survives an erosion.
#   blender -b -noaudio --python e38_eye_glow.py -- <helm.glb> <out.glb> --glow r,g,b --core r,g,b [--strength 4] [--json f]
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
GLOW = [float(x) for x in opt('--glow', '0.62,0.30,1.0').split(',')]; CORE = [float(x) for x in opt('--core', '0.96,0.92,1.0').split(',')]
STR = float(opt('--strength', '4.0')); BAND = float(opt('--band', '0.035')); DIL = int(opt('--dil', '3'))
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene; arm = next(o for o in sc.objects if o.type == 'ARMATURE')
ob = max([o for o in sc.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices)); me = ob.data
mat = ob.material_slots[0].material; nt = mat.node_tree
tex = next(n for n in nt.nodes if n.type == 'TEX_IMAGE'); img = tex.image; W_, H_ = img.size
px = np.array(img.pixels[:], np.float32).reshape(H_, W_, img.channels)[..., :3]
M = np.array(ob.matrix_world); uvl = me.uv_layers.active.data
me.calc_loop_triangles(); co = np.array([v.co[:] for v in me.vertices]) @ M[:3, :3].T + M[:3, 3]
sel = []
for t in me.loop_triangles:
    c = co[list(t.vertices)].mean(0); n = (M[:3, :3] @ np.array(t.normal[:])); n /= np.linalg.norm(n)
    if n[1] > -0.35: continue
    uv = np.array([uvl[l].uv[:] for l in t.loops]); u, v = uv.mean(0)
    r, g, b = px[min(H_ - 1, int(v * H_)), min(W_ - 1, int(u * W_))]
    mx, mn = max(r, g, b), min(r, g, b); s = (mx - mn) / max(mx, 1e-6)
    h = (math.degrees(math.atan2(math.sqrt(3) * (g - b), 2 * r - g - b)) % 360)
    if 255 <= h <= 320 and s > 0.20 and mx < 0.75: sel.append((t, c, uv))
zs = np.array([c[2] for _, c, _ in sel]); ztop = float(np.percentile(zs, 98)) if len(zs) else 0
keep = [(t, c, uv) for t, c, uv in sel if c[2] >= ztop - BAND / (1.96 / 1.70)]
# BLENDER HAS NO PIL: the mask is rasterised OUTSIDE (e38b_eye_mask.py) from the UV triangles written here, then attached.
UVJ = OUT.replace('.glb', '_uv.json'); EMP = os.path.abspath(OUT.replace('.glb', '_emission.png'))
if not os.path.exists(EMP):
    json.dump(dict(size=[W_, H_], tris=[[[float(u_), float(v_)] for u_, v_ in uv] for _, _, uv in keep], faces_violet_front=len(sel), faces_slit=len(keep)),
              open(UVJ, 'w')); print('EYE UV', UVJ, len(keep)); raise SystemExit(0)
emi = bpy.data.images.load(EMP)
bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
et = nt.nodes.new('ShaderNodeTexImage'); et.image = emi
nt.links.new(et.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = STR
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=False, export_image_format='AUTO')
rep = dict(src=SRC, out=OUT, faces_violet_front=len(sel), faces_slit=len(keep), emission_png=EMP,
           glow=GLOW, core=CORE, strength=STR, band_m=BAND, dilate_px=DIL, tex=[W_, H_]); print('EYE', json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
