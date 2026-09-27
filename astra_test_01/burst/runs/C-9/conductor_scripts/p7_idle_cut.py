# C-9 explicit idle cut (C-8 oneshot_c8.py lineage, R-C3-17 method on the FROZEN oracle.video_cut module): 12 frames evenly over ONE
# prompted breath (48 native frames = 2.0 s at 24 fps) starting at native 36 (1.5 s, after settle), one register transform.
# usage: p7_idle_cut.py <D>   -> runs/C-9/p7/<D>_idle_x/{frames/idle/<D>/, frames/rest/<D>/, registration.json, strip.png}
import sys, json, pathlib, tempfile, hashlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from oracle import video_cut as vc
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); D = sys.argv[1]
SUF = sys.argv[2] if len(sys.argv) > 2 else ''
clip = B/f'runs/C-9/xvideo/in/{D}_idle{SUF}.mp4'; out = B/f'runs/C-9/p7/{D}_idle_x{SUF}'
(out/'frames'/'idle'/D).mkdir(parents=True, exist_ok=True); (out/'frames'/'rest'/D).mkdir(parents=True, exist_ok=True)
wd = pathlib.Path(tempfile.mkdtemp(prefix=f'idle_{D}_', dir='/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad'))
m = vc.split(str(clip), str(wd), t_max_s=99); paths = m['paths']
START, SPAN, N = 36, 48, 12
idx = [START + round(i * SPAN / N) for i in range(N)]
fr = vc.matte_frames([paths[i] for i in [0] + idx], edge_mode='clamp'); fr = fr[0] if isinstance(fr, tuple) else fr
reg, transform = vc.register(fr, anchor_index=1)
reg[0].save(out/'frames'/'rest'/D/f'rest_{D}.png')
for k, im in enumerate(reg[1:]): im.save(out/'frames'/'idle'/D/f'idle_{D}_{k:02d}.png')
w, h = reg[1].size; strip = Image.new('RGBA', (w * N, h), (58, 63, 74, 255))
for k, im in enumerate(reg[1:]): strip.alpha_composite(im, (k * w, 0))
strip.save(out/'strip.png')
json.dump(dict(kind='idle', direction=D, clip=str(clip), clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(), indices_native=idx, n_native=len(paths),
               period=dict(frames=SPAN, seconds=SPAN / 24, source='prompted (explicit conductor cut; frozen tool autocorr locked on a 0.25 s chest flicker)'),
               transform=transform, conductor_derived=True, method='explicit even-sampling cut on frozen vc.split/matte_frames/register'), open(out/'registration.json', 'w'), indent=1)
print(D, 'idle cut', idx[0], '..', idx[-1])
