"""BV2F lane PH (galadriel) -- shared helpers for the v1-parity harness P1-P11.
Every function here is pure (numpy/scipy/PIL); no file is written outside fid/ph/."""
import hashlib
import json
import os
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

C9 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9")
BF = C9 / "barrow_full"
B2 = C9 / "barrow_v2"
FID = B2 / "fid"
PH = FID / "ph"
ART = C9 / "artifacts"
PPM_V1 = 100.617553710938          # barrow_full.gd PPM: play-camera screen px per metre (cam.size = rows / PPM)
PITCH = 52.95354112560294


def sha256(p, n=None):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest() if n is None else h.hexdigest()[:n]


def load_rgb(p, scale=None):
    im = Image.open(p).convert("RGB")
    if scale and scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.BOX)
    return np.asarray(im, dtype=np.float32)


def jload(p):
    return json.load(open(p))


def srgb_to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rgb_to_lab(rgb):
    """sRGB 0-255 (..., 3) -> CIE Lab (D65)."""
    lin = srgb_to_lin(np.asarray(rgb, dtype=np.float64))
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ M.T
    xyz = xyz / np.array([0.95047, 1.0, 1.08883])
    e = 216 / 24389
    k = 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)


def luma(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def radial_spectrum(gray, nbins=None):
    """Radially averaged power spectrum of a square-ish tile (Hann-windowed, mean removed).
    Returns (period_px[], power[]) for integer radii 1..N/2."""
    g = gray.astype(np.float64)
    g = g - g.mean()
    h, w = g.shape
    win = np.outer(np.hanning(h), np.hanning(w))
    F = np.fft.fftshift(np.fft.fft2(g * win))
    P = np.abs(F) ** 2
    yy, xx = np.indices(P.shape)
    cy, cx = h // 2, w // 2
    # normalised radius in cycles/px * N  (use the shorter side as N)
    N = min(h, w)
    r = np.hypot((yy - cy) * N / h, (xx - cx) * N / w)
    ri = np.round(r).astype(int)
    nb = N // 2
    sums = np.bincount(ri.ravel(), P.ravel(), minlength=nb + 1)[:nb + 1]
    cnt = np.bincount(ri.ravel(), minlength=nb + 1)[:nb + 1]
    pw = sums / np.maximum(cnt, 1)
    k = np.arange(1, nb + 1)
    return N / k, pw[1:]


def tiles(shape, size, stride=None):
    stride = stride or size
    H, W = shape[:2]
    for y in range(0, max(H - size, 0) + 1, stride):
        for x in range(0, max(W - size, 0) + 1, stride):
            yield y, x


def dump(obj, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))


def glb_json(p):
    import struct
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    return json.loads(b[20:20 + n])


def glb_aabb(p):
    """Native AABB (min, max) of every POSITION accessor in a GLB (accessor min/max; the normalised builds
    carry one node with no transform -- asserted)."""
    j = glb_json(p)
    for nd in j.get("nodes", []):
        assert not any(k in nd for k in ("matrix", "rotation", "scale")) or nd.get("scale", [1, 1, 1]) == [1, 1, 1], \
            "node transform present in %s: extend glb_aabb" % p
    mn, mx = np.full(3, np.inf), np.full(3, -np.inf)
    for m in j["meshes"]:
        for pr in m["primitives"]:
            a = j["accessors"][pr["attributes"]["POSITION"]]
            mn = np.minimum(mn, a["min"])
            mx = np.maximum(mx, a["max"])
    return mn, mx
