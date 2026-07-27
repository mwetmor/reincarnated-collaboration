#!/usr/bin/env python3
"""Health-globe NUMERAL reader (current/max HP), 60 fps capable.

WHY NUMERALS AND NOT FILL-FRACTION
----------------------------------
Round-1 calibration REJECTED globe fill-fraction as an instrument: it moved
4.6 pp against a 90.5 pp null band, i.e. it carries almost no signal at this
capture. The always-on numerals were 100% READY on the same frames. This
module therefore reads the NUMERALS ONLY. Fill-fraction is not consulted, not
as a prior, not as a tie-break.

GEOMETRY (measured, 1920x1080)
  numerals occupy roughly x 600-700, y 1005-1022; the string is
  "<cur>/<max>" in a near-white low-saturation face with a dark outline over
  the red globe. Crop is taken generously and the ink bbox found per frame,
  because the string's width changes with digit count and it is centred.

The mask is the same bright + achromatic rule as the FCT reader, which is what
keeps the red globe, the orange rune UI and the brown frame out.
"""
import numpy as np

CROP = dict(x=584, y=998, w=118, h=30)
BRIGHT_MIN = 150
CHROMA_MAX = 50
MIN_IOU = 0.70


def mask_of(sub):
    s = sub.astype(np.int16)
    mx = s.max(axis=2)
    mn = s.min(axis=2)
    return (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)


def segments(m):
    col = m.sum(axis=0)
    out, run = [], None
    for i, v in enumerate(col):
        if v > 0:
            run = [i, i] if run is None else [run[0], i]
        elif run is not None:
            out.append(tuple(run))
            run = None
    if run:
        out.append(tuple(run))
    return out


def iou(a, b):
    if a.shape != b.shape:
        h = max(a.shape[0], b.shape[0])
        w = max(a.shape[1], b.shape[1])
        A = np.zeros((h, w), bool)
        B = np.zeros((h, w), bool)
        A[:a.shape[0], :a.shape[1]] = a
        B[:b.shape[0], :b.shape[1]] = b
        a, b = A, B
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


class GlobeReader:
    """Greedy left-to-right template matching, NOT gap segmentation.

    Same reason as panel_ocr's G-4: adjacent glyphs touch (the '/4' pair in
    "300/491" merges into a single 15 px blob) and a merged blob still scores
    plausibly against one template -- a confidently WRONG read. Greedy
    matching at native glyph width avoids the failure entirely.
    """

    def __init__(self, templates):
        self.t = {k: [np.array(b, dtype=bool) for b in v]
                  for k, v in templates.items()}

    def _best(self, band, x, dxs=(0,)):
        best, bv, bw, bdx = None, -1.0, 0, 0
        H = band.shape[0]
        for ch, tl in self.t.items():
            for t in tl:
                th, tw = t.shape
                for dx in dxs:
                    if x + dx < 0 or x + dx + tw > band.shape[1]:
                        continue
                    win = band[:, x + dx:x + dx + tw]
                    tt = t
                    if th != H:                      # band trimmed differently
                        tt = t[:H] if th > H else np.vstack(
                            [t, np.zeros((H - th, tw), bool)])
                    v = iou(win, tt)
                    if v > bv:
                        best, bv, bw, bdx = ch, v, tw, dx
        return best, bv, bw, bdx

    def read(self, frame):
        c = CROP
        sub = frame[c["y"]:c["y"] + c["h"], c["x"]:c["x"] + c["w"]]
        m = mask_of(sub)
        ys, xs = np.nonzero(m)
        if not len(ys):
            return None, None, 0.0
        y0, y1 = ys.min(), ys.max()
        if y1 - y0 + 1 > 16:            # a tooltip or effect is bleeding in
            return None, None, 0.0
        band = m[y0:y1 + 1]
        x = int(xs.min())
        xmax = int(xs.max())
        out, confs = [], []
        first = True
        while x <= xmax:
            dxs = (0,) if first else (0, 1, 2, -1)
            ch, v, w, dx = self._best(band, x, dxs)
            if ch is None or v < MIN_IOU:
                out.append("?")
                break
            out.append(ch)
            confs.append(v)
            x += dx + w
            first = False
            col = band[:, x:x + 6].sum(axis=0)
            k = 0
            while k < len(col) and col[k] == 0:
                k += 1
            if k >= 4:
                break
            x += k
        s = "".join(out)
        conf = min(confs) if confs else 0.0
        if "?" in s or "/" not in s:
            return None, s, conf
        a, b = s.split("/", 1)
        if not (a.isdigit() and b.isdigit()):
            return None, s, conf
        return (int(a), int(b)), s, conf
