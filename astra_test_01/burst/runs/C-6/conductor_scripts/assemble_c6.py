# Conductor assembly for C-6 (copy + MIRROR only; no art transformation beyond the ruled horizontal flip — R-C6-30 F17(a)).
# Writes runs/C-6/cells/<anim>_<dir>/{frames/, registration.json, numbers.json, checks.json, <anim>_<dir>_1to1.mp4, <anim>_<dir>_2x.mp4}
# and runs/C-6/cells/matrix_index.json. Unique dirs: S, SW, E (+ N, NW when their seeds pass). Mirrors: SE←SW, W←E (NE←NW when NW exists).
import sys, json, shutil, pathlib, glob, hashlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from PIL import Image, ImageOps
from review import encode
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); R = B/'runs/C-6'; P4 = R/'p4'; OUT = R/'cells'
CUTS = {'S_idle':'S_idle_p4','SW_idle':'SW_idle_p4','E_idle':'E_idle_p4','S_walk':'S_walk_sib','SW_walk':'SW_walk','E_walk':'E_walk','S_run':'S_run','SW_run':'SW_run','E_run':'E_run','S_cast':'S_cast','SW_cast':'SW_cast','E_cast':'E_cast','S_jump':'S_jump','SW_jump':'SW_jump','E_jump':'E_jump'}
MIRROR = {'SE':'SW', 'W':'E', 'NE':'NW'}
ANIMS = ['idle','walk','run','jump','cast']; DIRS = ['S','SW','W','NW','N','NE','E','SE']
FLAGS = {'S_walk':['period from E sibling stride (no head-bob cycle walking toward the camera) — FLAGGED'], 'SW_walk':['slow stride 3.0 s (C-3 W class) — FLAGGED'], 'SW_run':['slow 2.75 s — FLAGGED'],
         'S_jump':['settle by last-valid-frame fallback; 8 border-touch frames excluded — FLAGGED'], 'E_jump':['20 border-touch frames (jump leaves the plate) excluded; keys moved to nearest valid — FLAGGED'], 'E_cast':['1 border-touch frame excluded']}
index = {}; OUT.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write_cell(cell, frames_dir_src, rest_src, reg, numbers, checks, mp4s, extra):
    a, d = cell.split('_'); dst = OUT/f'{a}_{d}'
    if dst.exists(): shutil.rmtree(dst)
    (dst/'frames'/a/d).mkdir(parents=True); (dst/'frames'/'rest'/d).mkdir(parents=True)
    for i, f in enumerate(sorted(glob.glob(str(frames_dir_src/'*.png')))):
        im = Image.open(f); im = ImageOps.mirror(im) if extra.get('mirrored') else im; im.save(dst/'frames'/a/d/f'{a}_{d}_{i:02d}.png')
    rim = Image.open(rest_src); rim = ImageOps.mirror(rim) if extra.get('mirrored') else rim; rim.save(dst/'frames'/'rest'/d/f'rest_{d}.png')
    reg = dict(reg); reg.update(extra); json.dump(reg, open(dst/'registration.json','w'), indent=1)
    json.dump(numbers, open(dst/'numbers.json','w'), indent=1); json.dump(checks, open(dst/'checks.json','w'), indent=1)
    if mp4s:  # unique cell: copy the frozen packet builder's encodes
        for src, name in mp4s: shutil.copyfile(src, dst/name)
    else:     # mirrored cell: encode the flipped frames with the frozen encoder, same parameters as the packet builder (12 fps, five repeats)
        frs = [Image.open(f) for f in sorted(glob.glob(str(dst/'frames'/a/d/'*.png')))]
        encode.encode_loop(frs, 12, str(dst/f'{a}_{d}_1to1.mp4'), scale=1, loops=5); encode.encode_loop(frs, 12, str(dst/f'{a}_{d}_2x.mp4'), scale=2, resample='lanczos', loops=5)
    return dst
for cell, cd in CUTS.items():
    d, a = cell.split('_'); cut = P4/cd/'cut'; pk = P4/cd/'packet'   # cut folders are <dir>_<anim>; cells are <anim>_<dir>
    frames_src = cut/'frames'/a/d; rest_src = cut/'frames'/'rest'/d/f'rest_{d}.png'
    if not frames_src.exists() or not list(frames_src.glob('*.png')): index[f'{a}_{d}'] = dict(status='INCOMPLETE', reason='no frames cut'); continue
    reg = json.load(open(cut/'registration.json')); checks = json.load(open(P4/cd/'checks.json')) if (P4/cd/'checks.json').exists() else {}
    numbers = json.load(open(pk/'numbers.json')) if (pk/'numbers.json').exists() else []
    mp4s = [(pk/f'{a}_{d}_1to1.mp4', f'{a}_{d}_1to1.mp4'), (pk/f'{a}_{d}_2x.mp4', f'{a}_{d}_2x.mp4')] if (pk/f'{a}_{d}_1to1.mp4').exists() else None
    flags = list(checks.get('flags', [])) + FLAGS.get(cell, [])   # FLAGS keyed <dir>_<anim>
    dst = write_cell(f'{a}_{d}', frames_src, rest_src, reg, numbers, checks, mp4s, dict(cell=f'{a}_{d}', source_cut=cd, mirrored=False, flags=flags))
    index[f'{a}_{d}'] = dict(status='COMPLETE', source_cut=cd, clip=reg.get('clip'), frames=len(list((dst/'frames'/a/d).glob('*.png'))), flags=flags, packet_mp4=bool(mp4s), clip_sha256=reg.get('clip_sha256'))
for d, src in MIRROR.items():
    for a in ANIMS:
        scell = f'{a}_{src}'; cell = f'{a}_{d}'
        if index.get(scell, {}).get('status') != 'COMPLETE': index[cell] = dict(status='INCOMPLETE', reason=f'mirror source {scell} not complete'); continue
        sdir = OUT/scell; reg = json.load(open(sdir/'registration.json')); checks = json.load(open(sdir/'checks.json')); numbers = json.load(open(sdir/'numbers.json'))
        extra = dict(cell=cell, mirrored=True, mirror_of=scell, mirror_rule='R-C6-30 F17(a): horizontal flip of the registered frames; canvas 512 → x\' = 511 - x for any socket; light key reads upper-RIGHT on this cell', flags=reg.get('flags', []) + ['MIRRORED cell (horn/tome/grip hand on the opposite side; key light flipped) — Matt P5 eye judges'])
        dst = write_cell(cell, sdir/'frames'/a/src, sdir/'frames'/'rest'/src/f'rest_{src}.png', reg, numbers, checks, None, extra)
        index[cell] = dict(status='COMPLETE', mirror_of=scell, frames=len(list((dst/'frames'/a/d).glob('*.png'))), flags=extra['flags'])
for d in DIRS:
    for a in ANIMS:
        index.setdefault(f'{a}_{d}', dict(status='INCOMPLETE', reason=f'no approved seed for {d} (N12 hold edits blocked by the Codex limit, T25)'))
json.dump(dict(rule='F17(a) mirror set: unique S, SW, E (+N, NW pending) ; mirrors SE←SW, W←E, NE←NW', cells=index, complete=sum(1 for v in index.values() if v['status']=='COMPLETE')), open(OUT/'matrix_index.json','w'), indent=1)
print('complete', sum(1 for v in index.values() if v['status']=='COMPLETE'), '/ 40'); print({k: v['status'][:4] + ('/m' if v.get('mirror_of') else '') for k, v in index.items()})
