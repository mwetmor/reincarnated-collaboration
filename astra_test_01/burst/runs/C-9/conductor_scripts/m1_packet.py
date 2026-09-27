# C-9 M1 style-gate packet (conductor evidence tool, not lane code): m1_packet.py <out_dir>
# Builds: metrics.json (tone/colour per image, the metrics-2026-09-26 revision 2 instruments), game-scale views,
# knight-on-chunk composites (A = Keeper on chunk_A; B = each knight on each merged chunk), and review.html.
import sys, json, pathlib, hashlib, html
import numpy as np
from PIL import Image

B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A_CHUNK = B/'runs/C-3/artifacts/CS-chunk-A/chunk_A.png'
A_KEEPER = B/'runs/C-3/artifacts/K2c-gen-SE/k2c_SE.png'
ART = B/'runs/C-9/artifacts'
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
GAME = 130 / 176          # chunk text scale (176 px person) -> in-game Keeper height 130 px
KNIGHT_PX = 130

def lab(a):
    a = a.astype(float) / 255
    c = np.where(a <= .04045, a / 12.92, ((a + .055) / 1.055) ** 2.4)
    M = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
    xyz = c @ M.T / np.array([.9505, 1, 1.089])
    f = np.where(xyz > .008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return 116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])

def keymask(a):  # True = figure/scenery (not #00ff00 plate)
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return ~((g > 150) & (g - r > 70) & (g - b > 70))

def metrics(path):
    a = np.asarray(Image.open(path).convert('RGB')); m = keymask(a)
    L, A_, B_ = lab(a); C = np.hypot(A_, B_); Lm, Cm, Am, Bm = L[m], C[m], A_[m], B_[m]
    d = Lm <= np.percentile(Lm, 2)
    return dict(L5=round(float(np.percentile(Lm, 5)), 1), L95=round(float(np.percentile(Lm, 95)), 1),
                Cmean=round(float(Cm.mean()), 1), C95=round(float(np.percentile(Cm, 95)), 1),
                pctC40=round(float(100 * (Cm > 40).mean()), 1),
                dark2_L=round(float(Lm[d].mean()), 1), dark2_C=round(float(np.hypot(Am[d].mean(), Bm[d].mean())), 1),
                dark2_h=round(float(np.degrees(np.arctan2(Bm[d].mean(), Am[d].mean()))), 0),
                pct_ink=round(float(100 * (Lm < 35).mean()), 1), px=int(m.sum()))

def cutout(path, height):
    im = Image.open(path).convert('RGB'); a = np.asarray(im); m = keymask(a)
    ys, xs = np.where(m); box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    rgba = np.dstack([a, (m * 255).astype('uint8')]); fig = Image.fromarray(rgba, 'RGBA').crop(box)
    arr = np.asarray(fig).copy(); g = arr[..., 1].astype(int); rb = np.maximum(arr[..., 0], arr[..., 2]).astype(int)
    arr[..., 1] = np.minimum(g, rb + 10).astype('uint8')          # simple despill (evidence only)
    fig = Image.fromarray(arr, 'RGBA')
    return fig.resize((max(1, round(fig.width * height / fig.height)), height), Image.LANCZOS)

def game_view(chunk_path, fig_path, name):
    ch = Image.open(chunk_path).convert('RGB'); ch = ch.resize((round(ch.width * GAME), round(ch.height * GAME)), Image.LANCZOS)
    a = np.asarray(ch).copy(); a[~keymask(a)] = (40, 44, 58)   # void shown as a neutral dark, not green
    ch = Image.fromarray(a)
    if fig_path:
        f = cutout(fig_path, KNIGHT_PX); x, y = int(ch.width * 0.42), int(ch.height * 0.30)
        ch.paste(f, (x, y), f)
    p = OUT / name; ch.save(p); return p.name

rows, pairs = [], []
cands = sorted(ART.glob('S1-*/out/*.png')) + sorted(ART.glob('K1-*/out/*.png'))
imgs = [('A chunk_A (H1)', A_CHUNK), ('A Keeper SE (H1)', A_KEEPER)] + [(p.stem, p) for p in cands]
for label, p in imgs:
    rows.append(dict(label=label, path=str(p), sha12=hashlib.sha256(p.read_bytes()).hexdigest()[:12], **metrics(p)))
json.dump(rows, open(OUT / 'metrics.json', 'w'), indent=1)

views = [('A — Keeper on chunk_A (H1)', game_view(A_CHUNK, A_KEEPER, 'game_A.png'))]
for s in [p for p in cands if p.stem.startswith('S1-')]:
    arm = s.stem.split('_')[0].split('-')[1]
    ks = [k for k in cands if k.stem.startswith(f'K1-{arm}')]
    views.append((f'B — {ks[0].stem if ks else "(no knight)"} on {s.stem}', game_view(s, ks[0] if ks else None, f'game_{s.stem}.png')))
for label, p in imgs:
    im = Image.open(p).convert('RGB'); im.thumbnail((900, 900)); im.save(OUT / f'full_{pathlib.Path(p).stem}.png')

def tr(r): return '<tr>' + ''.join(f'<td>{html.escape(str(r[k]))}</td>' for k in ('label', 'L5', 'L95', 'Cmean', 'pctC40', 'dark2_L', 'dark2_h', 'pct_ink', 'sha12')) + '</tr>'
h = ['<!doctype html><meta charset=utf-8><title>C-9 M1 style gate</title><style>body{font:14px system-ui;margin:24px;background:#f4f1ea}img{max-width:100%;border:1px solid #bbb}figure{display:inline-block;margin:8px;vertical-align:top;max-width:46%}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:3px 7px}</style>',
     '<h1>Run C-9 — M1 style gate</h1><p>Question: do you prefer the Illuminated merge (B) to H1 (A)? Rule GO (+ pick INK or WARM line) / ITERATE / ADD-ASTRA-ARM.</p>',
     '<h2>1. At game scale (knight 130 px, chunk scaled to the Keeper)</h2>']
h += [f'<figure><img src="{v}"><figcaption>{html.escape(l)}</figcaption></figure>' for l, v in views]
h += ['<h2>2. Full size</h2>'] + [f'<figure><img src="full_{pathlib.Path(p).stem}.png"><figcaption>{html.escape(l)}</figcaption></figure>' for l, p in imgs]
h += ['<h2>3. Numbers (metrics-2026-09-26 rev 2 instruments; plate pixels excluded)</h2><p>Figure band: L95 ≈ 83–92, dark ink allowed. Scene: painted-book palette; walkable floor brightest and calmest.</p><table><tr><th>image</th><th>L5</th><th>L95</th><th>C mean</th><th>% C&gt;40</th><th>line L</th><th>line hue</th><th>% ink</th><th>sha12</th></tr>']
h += [tr(r) for r in rows] + ['</table>']
(OUT / 'review.html').write_text('\n'.join(h)); print(OUT / 'review.html', len(rows), 'images')
