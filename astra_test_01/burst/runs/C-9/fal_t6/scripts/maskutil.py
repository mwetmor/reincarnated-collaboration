# Masks for the silhouette-IoU pass, and for the orientation fit that precedes it.
#
# The painted input plates are white-ground JPEGs that still carry the black
# vertical RULES from the sheet they were sliced out of. Those rules are pure
# subject to any "not white" test, and on the manticore's left plate the tail
# crosses one, so a largest-connected-component test alone would swallow it.
# Kill the rules first (tall, thin, dark columns), THEN take the largest blob.
import numpy as np
from PIL import Image
from scipy import ndimage


def input_mask(path, dark=70, colfrac=0.45, max_bar_w=45):
    a = np.array(Image.open(path).convert('RGB')).astype(np.float32)
    lum = a.mean(2)
    sat = a.max(2) - a.min(2)
    m = ~((lum > 232) & (sat < 22))            # anything not white ground
    # --- strike the sheet rules -------------------------------------------
    d = lum < dark
    cf = d.mean(0)
    cols = np.where(cf > colfrac)[0]
    if len(cols):
        runs, start = [], cols[0]
        for i in range(1, len(cols) + 1):
            if i == len(cols) or cols[i] != cols[i - 1] + 1:
                runs.append((start, cols[i - 1])); start = cols[i] if i < len(cols) else 0
        for lo, hi in runs:
            if hi - lo + 1 <= max_bar_w:
                m[:, lo:hi + 1] = False
    # --- largest blob ------------------------------------------------------
    m = ndimage.binary_opening(m, np.ones((3, 3)))
    lab, n = ndimage.label(m)
    if n > 1:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = lab == (int(np.argmax(sizes)) + 1)
    m = ndimage.binary_closing(m, np.ones((5, 5)))
    return m, a


def render_mask(path, thr=0.35):
    im = Image.open(path).convert('RGBA')
    a = np.array(im).astype(np.float32) / 255.0
    return a[..., 3] > thr, a[..., :3] * 255.0


def main_blob(mask):
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


def robust_box(mask, plo=0.0, phi=100.0):
    """The box that sets the scale. Taken from the LARGEST BLOB, not the whole
    mask, and optionally trimmed by percentile over the blob's own pixels.

    Both guards are load-bearing and were added after the naive version gave a
    wrong answer that looked fine. Hunyuan's manticore ships small detached
    flakes a body-length away from the figure; a plain bbox let a 200-pixel
    flake set the scale for a million-triangle mesh, and the orientation fit
    then chose yaw=90 on an IoU of 0.22. The percentile trim is for the other
    direction: the painted back plate draws the manticore's tail as a spike
    ABOVE the head, which no generator reproduces, so a full-height box
    measures the tail on one side and the skull on the other."""
    m = main_blob(mask)
    ys, xs = np.where(m)
    if not len(ys):
        return None
    if plo > 0 or phi < 100:
        y0, y1 = np.percentile(ys, [plo, phi])
        x0, x1 = np.percentile(xs, [plo, phi])
    else:
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    return int(np.floor(y0)), int(np.ceil(y1)) + 1, int(np.floor(x0)), int(np.ceil(x1)) + 1


def norm_by_height(mask, rgb=None, H=256, W=512, plo=0.0, phi=100.0):
    """Scale so the robust box HEIGHT is H (aspect kept, so a wide figure stays
    wide), paste centred in a W x H canvas. Scale and alignment come from the
    main blob; the FULL mask rides along and is scored, so a floating fragment
    still costs IoU -- it just no longer gets to set the scale."""
    box = robust_box(mask, plo, phi)
    if box is None:
        return np.zeros((H, W), bool), np.zeros((H, W, 3), np.float32)
    y0, y1, x0, x1 = box
    mh, mw = y1 - y0, x1 - x0
    pad = int(round(mh * 0.6))                      # room for what lies outside
    y0p, y1p, x0p, x1p = y0 - pad, y1 + pad, x0 - pad, x1 + pad
    def _cut(a):
        out = np.zeros((y1p - y0p, x1p - x0p) + a.shape[2:], a.dtype)
        sy0, sy1 = max(0, y0p), min(a.shape[0], y1p)
        sx0, sx1 = max(0, x0p), min(a.shape[1], x1p)
        out[sy0 - y0p:sy1 - y0p, sx0 - x0p:sx1 - x0p] = a[sy0:sy1, sx0:sx1]
        return out
    mask = _cut(mask)
    rgb = _cut(rgb) if rgb is not None else None
    y0, y1, x0, x1 = pad, pad + mh, pad, pad + mw
    s = H / float(mh)                               # one scale, box height -> H
    ph, pw = mask.shape
    nh, nw = max(1, int(round(ph * s))), max(1, int(round(pw * s)))
    mi = np.array(Image.fromarray((mask * 255).astype(np.uint8)).resize((nw, nh), Image.BILINEAR)) > 127
    ci = (np.array(Image.fromarray(rgb.astype(np.uint8)).resize((nw, nh), Image.BILINEAR)).astype(np.float32)
          if rgb is not None else np.zeros((nh, nw, 3), np.float32))
    # the box's centre must land on the canvas centre
    cy, cx = (y0 + y1) / 2.0 * s, (x0 + x1) / 2.0 * s
    oy, ox = int(round(H / 2.0 - cy)), int(round(W / 2.0 - cx))
    out = np.zeros((H, W), bool)
    oc = np.zeros((H, W, 3), np.float32)
    dy0, dy1 = max(0, oy), min(H, oy + nh)
    dx0, dx1 = max(0, ox), min(W, ox + nw)
    if dy1 > dy0 and dx1 > dx0:
        out[dy0:dy1, dx0:dx1] = mi[dy0 - oy:dy1 - oy, dx0 - ox:dx1 - ox]
        oc[dy0:dy1, dx0:dx1] = ci[dy0 - oy:dy1 - oy, dx0 - ox:dx1 - ox]
    return out, oc


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0


def colour_sim(ma, ca, mb, cb):
    """Mean colour agreement over the overlap, 1 = identical, 0 = opposite."""
    ov = ma & mb
    if ov.sum() < 50:
        return 0.0
    d = np.abs(ca[ov] - cb[ov]).mean(1)
    return float(np.clip(1.0 - d / 128.0, 0, 1).mean())
