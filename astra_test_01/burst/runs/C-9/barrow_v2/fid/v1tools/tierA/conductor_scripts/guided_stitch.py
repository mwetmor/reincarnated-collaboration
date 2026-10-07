# C-9 stitch for guided_paint.py chunks. usage: guided_stitch.py <cfg.json> <out.png> [preview.jpg]
# Every chunk is a 1536x1024 canvas at a 1280x768 stride, so neighbours overlap by 256 px. Astra EDIT
# re-synthesises the neighbour strips it was handed (mean abs diff 3-13 of 255 on T10BF), so a hard paste
# leaves a join. Each chunk gets linear ramps across its overlaps (up on the left/top, down on the
# right/bottom, only where a neighbour exists); the ramps form a partition of unity, so the weights
# sum to exactly 1 everywhere, corners where four chunks meet included.
import json, sys, pathlib, hashlib
import numpy as np
from PIL import Image
A9 = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts')
cfg = json.load(open(sys.argv[1])); P, COLS, ROWS = cfg['prefix'], cfg['cols'], cfg['rows']
W, H, SX, SY = 1536, 1024, 1280, 768; OV = W - SX
assert OV == H - SY
def src(k):
    for d in (f'{P}-{k}-r1', f'{P}-{k}'):
        p = A9/d/f'{P}-{k}.png'
        if p.exists(): return p
    sys.exit(f'chunk {k} is not painted')
acc = np.zeros(((ROWS-1)*SY + H, (COLS-1)*SX + W, 3)); wsum = np.zeros(acc.shape[:2])
up = np.linspace(0, 1, OV, endpoint=False) + 0.5/OV
for r in range(ROWS):
    for c in range(COLS):
        im = np.asarray(Image.open(src(f'{c}_{r}')).convert('RGB'), dtype=np.float64)
        assert im.shape == (H, W, 3), (c, r, im.shape)
        wx, wy = np.ones(W), np.ones(H)
        if c > 0: wx[:OV] *= up
        if c < COLS-1: wx[W-OV:] *= up[::-1]
        if r > 0: wy[:OV] *= up
        if r < ROWS-1: wy[H-OV:] *= up[::-1]
        w = np.outer(wy, wx)
        acc[r*SY:r*SY+H, c*SX:c*SX+W] += im * w[..., None]; wsum[r*SY:r*SY+H, c*SX:c*SX+W] += w
assert abs(wsum.min() - 1) < 1e-9 and abs(wsum.max() - 1) < 1e-9, (wsum.min(), wsum.max())
out = Image.fromarray((acc / wsum[..., None]).clip(0, 255).round().astype(np.uint8))
out.save(sys.argv[2], optimize=True)
print(pathlib.Path(sys.argv[2]).name, out.size, 'sha256', hashlib.sha256(pathlib.Path(sys.argv[2]).read_bytes()).hexdigest())
if len(sys.argv) > 3:
    out.resize((out.width // 2, out.height // 2), Image.LANCZOS).save(sys.argv[3], quality=86)
