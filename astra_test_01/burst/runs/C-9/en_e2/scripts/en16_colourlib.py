# EN-E2 colour helpers: sRGB <-> CIE Lab (D65), HSV, and the acolytes' REGION rule used for both the atlas grade and the
# sheet-vs-render measure. Regions (HSV on sRGB 0..1; h in degrees):
#   lapis  h 185-265, s > 0.10                 (robe / chasuble / stole)
#   brass  h 22-62,  s > 0.33, v > 0.22         (gears, bracer, circlet, clock disc, embroidery)
#   ivory  h 20-70 or s < 0.10, s < 0.33, v > 0.62   (under-robe / alb)
#   skin   from the body's own UVs (Head/neck/hands weights > 0.5), never by hue  (en11's rule)
import numpy as np

def srgb2lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lin2srgb(c): return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055)
M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
WP = np.array([0.95047, 1.0, 1.08883])
def rgb2lab(rgb):
    xyz = srgb2lin(rgb) @ M.T / WP
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def lab2rgb(lab):
    fy = (lab[..., 0] + 16) / 116; fx = fy + lab[..., 1] / 500; fz = fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1); d = 6 / 29
    xyz = np.where(f > d, f ** 3, 3 * d * d * (f - 4 / 29)) * WP
    return np.clip(lin2srgb(xyz @ np.linalg.inv(M).T), 0, 1)
def hsv(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1); d = mx - mn; r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(mx); nz = d > 1e-6
    hr = nz & (mx == r); hg = nz & (mx == g) & ~hr; hb = nz & ~hr & ~hg
    h[hr] = (((g - b)[hr] / d[hr]) % 6) * 60; h[hg] = (((b - r)[hg] / d[hg]) + 2) * 60; h[hb] = (((r - g)[hb] / d[hb]) + 4) * 60
    return h, np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0), mx
def regions(rgb, skin=None):
    h, s, v = hsv(rgb)
    lapis = (h > 185) & (h < 265) & (s > 0.10)
    brass = (h > 22) & (h < 62) & (s > 0.33) & (v > 0.22)
    ivory = (((h > 20) & (h < 70)) | (s < 0.10)) & (s < 0.33) & (v > 0.62) & ~brass
    out = dict(lapis=lapis, brass=brass, ivory=ivory)
    if skin is not None:
        for k in out: out[k] = out[k] & ~skin
        out['skin'] = skin
    return out
def dE(a, b): return float(np.linalg.norm(np.asarray(a) - np.asarray(b)))

# v2 (round 1 found the HSV rule wrong for this bake: the baked robe is low-chroma grey-blue, s ~0.05-0.15, so it fell into
# "ivory" or "other"; and the warm ivory, b ~ +20, fell into "brass"). The rule is now in Lab, applied IDENTICALLY to the sheet
# pixels and the atlas texels:
#   lapis  b* < 1.5 and L* < 72                     (cool or cool-neutral cloth)
#   ivory  L* >= 58, not lapis                      (pale cloth, however warm the bake made it)
#   brass  L* < 58, C* >= 14, hue angle 35-80 deg    (the metal; leather is darker and lower-chroma)
#   other  the rest (leather, leggings, shoes, cord, shadow)
def classify_lab(lab):
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]; ch = np.hypot(A, B); hue = np.degrees(np.arctan2(B, A)) % 360
    lapis = (B < 1.5) & (L < 72)
    ivory = (L >= 58) & ~lapis
    brass = (L < 58) & (ch >= 14) & (hue > 35) & (hue < 80) & ~lapis
    return dict(lapis=lapis, ivory=ivory, brass=brass)
