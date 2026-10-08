# R-C9-233: measure probe_face_r233.gd's passes and build the isolation sheets.
#   python3 r233_03_measure.py <probe out dir> <tag> [--variants live,nofronthair,...]
# Per clip x heading x variant, at zoom 3 (the play camera's own view, 3x the pixels):
#   F           the FACE FOOTPRINT (the _foot pass: her face texels alone, red) -- the denominator
#   covered by  hair (front G / other C), hood (B), other gear (M), the rest of her body (Y)  -- the _ida pass, inside F
#   pen         the WEB PEN's pixels inside F: where the frame is >= 25 luma darker than the same frame with the pen off
#               (_nopen; on the web build her hull lines are hidden, the depth-only screen pen draws her)
#   visible     face pixels in _ida (R) not under the pen
#   luminance   mean Rec.709 luma (0-255, the final frame: ramp, pen, grade, paper) over the VISIBLE face, and over all of F
#               (the opening as read: whatever covers the face counts at its own value)
# fill / noink / any variant without its own ID passes is measured with live's ID (the geometry is the same).
# noink is composited: live's frame outside F dilated, noink's inside -- "no ink inside the face opening".
import sys, os, json, glob, numpy as np
from PIL import Image, ImageDraw, ImageFilter
D, TAG = sys.argv[1], sys.argv[2]
VARS = sys.argv[sys.argv.index('--variants') + 1].split(',') if '--variants' in sys.argv else ['live', 'nofronthair', 'nohood', 'headzero', 'fill', 'noink']
HEADS = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
CLIPS = []
for p in sorted(glob.glob(D + '/live_*_S_z1_beauty.png')):
    CLIPS.append(os.path.basename(p)[len('live_'):-len('_S_z1_beauty.png')])
ORDER = ['idle', 'walk', 'cast_fireball_m']
CLIPS = [c for c in ORDER if c in CLIPS] + [c for c in CLIPS if c not in ORDER]
HEADS = [h for h in HEADS if os.path.exists('%s/live_%s_%s_z1_beauty.png' % (D, CLIPS[0], h))]

def load(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(int) if os.path.exists(p) else None

def cls(a, rgb):
    on = a > 200; off = a < 55
    m = np.ones(a.shape[:2], bool)
    for c, want in enumerate(rgb):
        m &= on[..., c] if want else off[..., c]
    return m

def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

def dil(m, r):
    im = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))
    return np.asarray(im) > 127

rows = []
for clip in CLIPS:
    for h in HEADS:
        for v in VARS:
            idv = v if os.path.exists('%s/%s_%s_%s_z3_ida.png' % (D, v, clip, h)) else 'live'
            fv = v if os.path.exists('%s/%s_%s_%s_z3_foot.png' % (D, v, clip, h)) else 'live'
            foot = load('%s/%s_%s_%s_z3_foot.png' % (D, fv, clip, h)); ida = load('%s/%s_%s_%s_z3_ida.png' % (D, idv, clip, h))
            beauty = load('%s/%s_%s_%s_z3_beauty.png' % (D, v, clip, h))
            nopen = load('%s/%s_%s_%s_z3_nopen.png' % (D, idv if v != 'fill' else 'live', clip, h))
            if foot is None or ida is None or beauty is None:
                continue
            F = cls(foot, (1, 0, 0)); n = int(F.sum())
            if v == 'noink':
                live = load('%s/live_%s_%s_z3_beauty.png' % (D, clip, h)); M = dil(F, 6)
                beauty = np.where(M[..., None], beauty, live)
                Image.fromarray(beauty.astype(np.uint8)).save('%s/noinkface_%s_%s_z3_beauty.png' % (D, clip, h))
                l1 = load('%s/live_%s_%s_z1_beauty.png' % (D, clip, h)); n1 = load('%s/noink_%s_%s_z1_beauty.png' % (D, clip, h))
                f1 = load('%s/live_%s_%s_z1_foot.png' % (D, clip, h))
                if l1 is not None and n1 is not None and f1 is not None:
                    M1 = dil(cls(f1, (1, 0, 0)), 2)
                    Image.fromarray(np.where(M1[..., None], n1, l1).astype(np.uint8)).save('%s/noinkface_%s_%s_z1_beauty.png' % (D, clip, h))
            ink = ((luma(beauty) < luma(nopen) - 25) & F) if (nopen is not None and v not in ('noink', 'fill')) else np.zeros_like(F)
            face_vis = cls(ida, (1, 0, 0)) & F & ~ink
            if v == 'noink':
                face_vis = cls(ida, (1, 0, 0)) & F
            pct = lambda m: round(100.0 * float((m & F).sum()) / max(n, 1), 1)
            r = dict(clip=clip, heading=h, variant=v, id_from=idv, footprint_px=n,
                     face_visible_pct=pct(face_vis),
                     hair_front_pct=pct(cls(ida, (0, 1, 0))), hair_other_pct=pct(cls(ida, (0, 1, 1))),
                     hood_pct=pct(cls(ida, (0, 0, 1))), gear_other_pct=pct(cls(ida, (1, 0, 1))), body_other_pct=pct(cls(ida, (1, 1, 0))),
                     pen_pct=pct(ink),
                     luma_visible_face=round(float(luma(beauty)[face_vis].mean()), 1) if face_vis.any() else None,
                     luma_footprint=round(float(luma(beauty)[F].mean()), 1) if n else None)
            rows.append(r)

def mean(key, sel):
    a = [r[key] for r in sel if r[key] is not None]
    return round(float(np.mean(a)), 1) if a else None

KEYS = ['footprint_px', 'face_visible_pct', 'hair_front_pct', 'hair_other_pct', 'hood_pct', 'pen_pct', 'luma_visible_face', 'luma_footprint']
FACING = ['S', 'SE', 'SW', 'E', 'W']    # the headings where her face is toward the camera (N, NE, NW show the hood's back)
summary = {}
print('means over the face-toward-camera headings', FACING)
print('%-16s %-12s ' % ('clip', 'variant') + ' '.join('%9s' % k.replace('_pct', '%').replace('luma_', 'L_')[:9] for k in KEYS))
for clip in CLIPS:
    for v in VARS:
        sel = [r for r in rows if r['clip'] == clip and r['variant'] == v and r['heading'] in FACING]
        if not sel: continue
        s = {k: mean(k, sel) for k in KEYS}; summary.setdefault(clip, {})[v] = s
        print('%-16s %-12s ' % (clip, v) + ' '.join('%9s' % ('-' if s[k] is None else s[k]) for k in KEYS))
json.dump({'tag': TAG, 'mean_over_headings': summary, 'rows': rows}, open('%s/%s_measure.json' % (D, TAG), 'w'), indent=1)

# --- sheets: rows = variants, columns = headings; z1 (the play camera, x2 nearest) and z3 (x0.67) -----------------------
LABEL = {'live': 'live (as played)', 'nofronthair': 'front hair hidden', 'nohood': 'hood hidden', 'headzero': 'head+neck at rest',
         'fill': 'face fill light', 'noink': 'no ink in the face opening', 'inksync': 'ink follows her morphs',
         'fixA': 'FIX A: + face strands tucked', 'fixB': 'FIX B: + face lifted', 'fixC': 'FIX C', 'fixD': 'FIX D: all hair in, lifted, lining', 'fixE': 'FIX E: D, outer strands kept', 'fixF': 'FIX F: all hair in, head lifted, lining', 'fixG': 'FIX G: F + forehead repainted', 'fixE+thin+thinlining': 'G + RIM'}
for clip in CLIPS:
    for zoom, cell, src_px in ((1, 280, 70), (3, 300, 200)):
        vs = [v for v in VARS if os.path.exists('%s/%s_%s_S_z%d_beauty.png' % (D, 'noinkface' if v == 'noink' else v, clip, zoom)) or v == 'noink']
        W = 150 + cell * len(HEADS); Hh = 30 + cell * len(vs)
        sheet = Image.new('RGB', (W, Hh), (24, 24, 28)); d = ImageDraw.Draw(sheet)
        for j, h in enumerate(HEADS):
            d.text((150 + j * cell + 6, 8), 'heading %s' % h, fill=(235, 235, 235))
        for i, v in enumerate(vs):
            d.text((6, 30 + i * cell + 6), LABEL.get(v, v), fill=(235, 235, 235))
            for j, h in enumerate(HEADS):
                p = '%s/%s_%s_%s_z%d_beauty.png' % (D, 'noinkface' if v == 'noink' else v, clip, h, zoom)
                if not os.path.exists(p): continue
                im = Image.open(p).convert('RGB')
                # re-centred on her face: live's footprint centroid at this zoom (the probe's crop centre is the Head bone,
                # which unprojects ~0.3 m off the face), the window src_px wide, a little below the face (head and shoulders)
                fp = load('%s/live_%s_%s_z%d_foot.png' % (D, clip, h, zoom))
                ys, xs = np.nonzero(cls(fp, (1, 0, 0))) if fp is not None else ([], [])
                cx, cy = (float(np.mean(xs)), float(np.mean(ys)) + src_px * 0.10) if len(xs) else (im.width / 2, im.height / 2)
                x0 = int(min(max(cx - src_px / 2, 0), im.width - src_px)); y0 = int(min(max(cy - src_px / 2, 0), im.height - src_px))
                im = im.crop((x0, y0, x0 + src_px, y0 + src_px))
                im = im.resize((cell, cell), Image.NEAREST if zoom == 1 else Image.LANCZOS)
                sheet.paste(im, (150 + j * cell, 30 + i * cell))
        sheet.save('%s/%s_sheet_%s_z%d.jpg' % (D, TAG, clip, zoom), quality=90)
print('sheets:', sorted(os.path.basename(p) for p in glob.glob('%s/%s_sheet_*.jpg' % (D, TAG))))
