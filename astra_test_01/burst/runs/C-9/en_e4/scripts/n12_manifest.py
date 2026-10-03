# EN-E3 clip manifest for a shipped creature GLB: every number RE-READ from the GLB itself (the D7 lesson: hand-copied speeds go
# stale), joined with the build's lint rows and the VFX rows.
#   python3 scripts/n12_manifest.py <export.glb> <cfg.json> <vfx.json> <out.json>
import json, struct, hashlib, sys, os
import numpy as np
GLB, CFG, VFX, OUT = sys.argv[1:5]
b = open(GLB, 'rb').read(); n = struct.unpack('<I', b[12:16])[0]; js = json.loads(b[20:20 + n])
bin0 = 20 + n + 8
cfg = json.load(open(CFG)); rig = json.load(open(GLB.replace('.glb', '.rig.json')))
def acc(i):
    a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
    return a, bv
clips = {}
for an in js.get('animations', []):
    tmax = 0.0
    for s in an['samplers']:
        a, _ = acc(s['input']); tmax = max(tmax, a['max'][0])
    clips[an['name']] = round(tmax, 5)
img = js['images'][0]
mats = [dict(name=m.get('name'), double_sided=m.get('doubleSided', False), has_texture='baseColorTexture' in m.get('pbrMetallicRoughness', {})) for m in js['materials']]
pos = [p['attributes']['POSITION'] for m in js['meshes'] for p in m['primitives']]
lo = np.min([js['accessors'][i]['min'] for i in pos], 0); hi = np.max([js['accessors'][i]['max'] for i in pos], 0)
FPS = 30
out = dict(schema='en3-creature-clips/1', creature=cfg['name'], roster_type_id=cfg['type_id'],
           glb=os.path.abspath(GLB), glb_sha256=hashlib.sha256(b).hexdigest(), glb_bytes=len(b),
           frame='glTF: +Y up, creature faces +Z (Blender -Y), metres; root = ground origin under the body; root motion STRIPPED',
           h_model_m=round(float(hi[1] - lo[1]), 4), length_m=round(float(hi[2] - lo[2]), 4), width_m=round(float(hi[0] - lo[0]), 4),
           skin_joints=len(js['skins'][0]['joints']), materials=mats, texture_embedded=bool(img.get('bufferView') is not None), texture_mime=img.get('mimeType'),
           clips={})
for name, c in cfg['clips'].items():
    T = clips.get(name)
    e = dict(kind=c['kind'], frames=c['frames'] if c['kind'] == 'oneshot' else c['frames'] + 1, duration_s=T, fps=FPS, source=c.get('src'),
             lint=rig['lint'].get(name))
    if c['kind'] == 'loop': e['loop'] = 'closing key == first key (frames 0..N, N = %d intervals)' % c['frames']
    if c.get('speed'): e['ground_speed_m_s'] = c['speed']; e['stride_m_per_cycle'] = round(c['speed'] * T, 4) if T else None
    if 'contact' in c: e['contact_frame'] = c['contact']; e['contact_s'] = round(c['contact'] / FPS, 4)
    if 'release' in c: e['release_frame'] = c['release']; e['release_s'] = round(c['release'] / FPS, 4)
    if c.get('hold_last'): e['hold_last'] = True
    if T is None: e['MISSING_IN_GLB'] = True
    out['clips'][name] = e
out['vfx'] = json.load(open(VFX)) if os.path.exists(VFX) else None
out['landmarks'] = rig['landmarks']
json.dump(out, open(OUT, 'w'), indent=1)
miss = [k for k, v in out['clips'].items() if v.get('MISSING_IN_GLB')]
print('manifest', OUT, 'clips', len(clips), 'missing', miss, 'texture_embedded', out['texture_embedded'], 'h', out['h_model_m'], 'len', out['length_m'])
