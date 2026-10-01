# R-C9-105: the great maul (GS-BMAUL2 b) as a SEPARATE PROP (Matt: no weapon on the character): 1.30 m overall, the HAFT
# thinned radially to 5.0 cm about its own axis (the sheet's haft read 6.3 cm at 1.30 m -- borderline for his 0.224 m hand;
# stage 1b proportion check). The head and the butt cap are untouched; a 2 cm blend at each end of the thinned span.
#   blender -b -noaudio --python s36_maul.py -- <maul_build.glb> <out.glb> [--json f]
import bpy, bmesh, json, math, os, sys
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '.json')
TOTAL, HAFT_D = 1.30, 0.050
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
ms = [o for o in sc.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]
if len(ms) > 1: bpy.ops.object.join()
o = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); bm.to_mesh(o.data); bm.free()
m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = min(1.0, 12000 / max(len(o.data.polygons), 1)); bpy.ops.object.modifier_apply(modifier='dec')
co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co); V = co.reshape(-1, 3)
lo, hi = V[:, 2].min(), V[:, 2].max()
s = TOTAL / float(hi - lo)
V = (V - np.array([0, 0, lo])) * s                      # butt at z 0, head at the top, 1.30 m
cx, cy = np.median(V[:, 0]), np.median(V[:, 1])
r = np.hypot(V[:, 0] - cx, V[:, 1] - cy)
# the haft's own radius along its length: 25th percentile radius per 1 cm slice (the thin core, not the langets' fins)
zs = np.arange(0.0, TOTAL, 0.01); prof = []
for z in zs:
    m_ = (V[:, 2] >= z) & (V[:, 2] < z + 0.01)
    prof.append(float(np.percentile(r[m_], 50)) if m_.sum() > 10 else np.nan)
prof = np.array(prof)
mid_r = float(np.nanmedian(prof[(zs > 0.25 * TOTAL) & (zs < 0.65 * TOTAL)]))
# the head: the top slices whose radius exceeds 2.5x the haft's; the butt cap: the lowest 6%
head_rows = zs[prof > 2.5 * mid_r]; head_lo = float(head_rows.min()) if len(head_rows) else 0.8 * TOTAL
z_a, z_b = 0.06 * TOTAL, head_lo - 0.01
f = (HAFT_D / 2) / mid_r
w = np.clip(np.minimum((V[:, 2] - z_a) / 0.02, (z_b - V[:, 2]) / 0.02), 0, 1)
k = 1 + (f - 1) * w
V[:, 0] = cx + (V[:, 0] - cx) * k; V[:, 1] = cy + (V[:, 1] - cy) * k
o.data.vertices.foreach_set("co", V.ravel()); o.data.update()
o.name = "great_maul"
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=False, export_image_format='AUTO')
rep = dict(source=SRC, total_m=TOTAL, haft_diameter_before_m=round(2 * mid_r, 4), haft_diameter_after_m=HAFT_D,
           radial_factor=round(f, 4), thinned_span_m=[round(z_a, 3), round(z_b, 3)], head_from_m=round(head_lo, 3),
           head_len_m=round(float((V[V[:, 2] > head_lo][:, :2].max(0) - V[V[:, 2] > head_lo][:, :2].min(0)).max()), 3),
           verts=len(V), faces=len(o.data.polygons), mb=round(os.path.getsize(OUT) / 1e6, 2),
           his_height_m=1.85, total_over_height=round(TOTAL / 1.85, 3), prop="static GLB, not skinned, not bound to him")
json.dump(rep, open(OUTJ, 'w'), indent=1)
print("MAUL", json.dumps(rep))
