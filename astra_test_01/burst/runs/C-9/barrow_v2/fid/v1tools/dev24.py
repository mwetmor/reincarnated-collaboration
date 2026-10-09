#!/usr/bin/env python3
"""BV2F DEV-24 (R-C9-243 design, revived R-C9-262/263): MASKED LOCAL REPAINT, the paste. A region of the finished stitch is
repainted by the image service with its painted surroundings as context (fid/pt/tools/local_repaint.py stages it and
writes the brief); this module pastes the result back:
  M    = the region grown GROW px, inside the patch's paste classes (a canvas-local mask pinned with the patch)
  w    = M feathered (Gaussian FEATHER px), zero outside the paste classes
  corr = DEV-23's idea on a ring of paste-class pixels just OUTSIDE M (RING_IN..RING_OUT px): the low-frequency difference
         old - new, spread over the patch by normalised convolution (sigma CORR_SIGMA)
  out  = old * (1 - w) + (new + corr) * w
Everything the painter changed outside w is discarded. No cascade: a patch touches only its own w > 0 pixels.

guided_stitch.py (Tier-B) calls apply() after the stitch only with BV2F_DEV24=1 and a cfg `dev24` block:
  {"layers": [{"base_pixels_sha256": <sha256 of the raw RGB bytes of the image this layer was staged on: the stitch for
                                      layer 1, the previous layer's result after>,
               "patches": [{"name", "rect_xy": [x, y], "region_png", "region_sha256", "paste_png", "paste_sha256",
                            "new_png", "new_sha256"}, ...]}, ...]}
Patches in one layer have disjoint supports; a patch that must overlap another is staged on its result (a later layer).
A changed base, a moved file or an overlap inside a layer HALTs. Unset = v1's stitch byte for byte.
R-C9-272: a patch may pin `read_sha256` (read_sha() of its staged base over its read region); when every patch of a
layer does, the layer is checked per patch over what it reads instead of over the whole image."""
import hashlib
import numpy as np
from PIL import Image
from scipy import ndimage

CW, CH = 1536, 1024
GROW, FEATHER, RING_IN, RING_OUT, CORR_SIGMA = 12, 6, 8, 40, 48


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def pixels_sha(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.uint8).tobytes()).hexdigest()


def weights(R: np.ndarray, pc: np.ndarray):
    M = ndimage.binary_dilation(R, iterations=GROW) & pc
    w = ndimage.gaussian_filter(M.astype(np.float64), FEATHER) * pc
    return M, w


def paste_local(old: np.ndarray, new: np.ndarray, R: np.ndarray, pc: np.ndarray, corr=None):
    """old, new: canvas-local float64 RGB; R region, pc paste classes (bool). -> (out float64, w, corr, M).
    corr given (R-C9-301: a PINNED correction field, computed once on the patch's staged base) = used as is."""
    M, w = weights(R, pc)
    if corr is None:
        ring = ndimage.binary_dilation(M, iterations=RING_OUT) & ~ndimage.binary_dilation(M, iterations=RING_IN) & pc
        num = np.stack([ndimage.gaussian_filter((old - new)[..., i] * ring, CORR_SIGMA) for i in range(3)], -1)
        den = ndimage.gaussian_filter(ring.astype(np.float64), CORR_SIGMA)[..., None]
        corr = num / np.maximum(den, 1e-6) * (den > 0.02)
    out = old * (1 - w[..., None]) + (new + corr) * w[..., None]
    return out, w, corr, M


def _load_mask(p, sha):
    if _sha(p) != sha:
        raise SystemExit("DEV-24 HALT: %s is not the pinned file" % p)
    return np.asarray(Image.open(p)) > 127


def read_region(R: np.ndarray, pc: np.ndarray) -> np.ndarray:
    """R-C9-272: the canvas-local pixels a paste READS from the base -- its support (w > 0: the blend reads old there)
    and its tone ring (the only pixels the correction samples). Nothing else in the rect affects the result."""
    M, w = weights(R, pc)
    ring = ndimage.binary_dilation(M, iterations=RING_OUT) & ~ndimage.binary_dilation(M, iterations=RING_IN) & pc
    return (w > 0) | ring


def read_sha(img: np.ndarray, p: dict) -> str:
    """the sha of the pixels the patch reads from `img`. R-C9-301: a patch may carry `read_zone` [x0, y0, x1, y1] (plate
    px, exclusive ends; the pilot identity zone): only its read pixels inside the zone are pinned -- outside it the patch
    reads whatever the (full-site) stitch blended there, and the build's own sha pins the result. No read_zone = all.
    Such a patch also pins its tone-correction field (`corr_npz` + `corr_sha256`, computed once on its staged base), so the
    ring pixels outside the zone cannot move the correction: inside the zone the paste is byte-identical to its staging."""
    x0, y0 = p["rect_xy"]
    R = _load_mask(p["region_png"], p["region_sha256"])
    pc = _load_mask(p["paste_png"], p["paste_sha256"])
    rr = read_region(R, pc)
    if "read_zone" in p:
        zx0, zy0, zx1, zy1 = p["read_zone"]
        yy, xx = np.mgrid[0:CH, 0:CW]
        rr &= (xx + x0 >= zx0) & (xx + x0 < zx1) & (yy + y0 >= zy0) & (yy + y0 < zy1)
    return pixels_sha(img[y0:y0 + CH, x0:x0 + CW][rr])


def apply_layer(img: np.ndarray, layer: dict):
    """one LAYER: patches staged on the same image, with pairwise-disjoint supports. Base check: per patch over its READ
    REGION when every patch pins `read_sha256` (R-C9-272: a full-site stitch may change pixels no patch reads), else the
    whole image (`base_pixels_sha256`)."""
    if all("read_sha256" in p for p in layer["patches"]):
        for p in layer["patches"]:
            if read_sha(img, p) != p["read_sha256"]:
                raise SystemExit("DEV-24 HALT: patch %s reads pixels that differ from its staged base" % p["name"])
    elif pixels_sha(img) != layer["base_pixels_sha256"]:
        raise SystemExit("DEV-24 HALT: the image is not the base this layer's patches were staged on")
    full = img.copy()
    support = np.zeros(img.shape[:2], bool)
    rep = []
    for p in layer["patches"]:
        x0, y0 = p["rect_xy"]
        R = _load_mask(p["region_png"], p["region_sha256"])
        pc = _load_mask(p["paste_png"], p["paste_sha256"])
        if _sha(p["new_png"]) != p["new_sha256"]:
            raise SystemExit("DEV-24 HALT: %s is not the pinned repaint" % p["new_png"])
        new = np.asarray(Image.open(p["new_png"]).convert("RGB")).astype(np.float64)
        old = img[y0:y0 + CH, x0:x0 + CW].astype(np.float64)
        fixed = None
        if "corr_npz" in p:   # R-C9-301: a read_zone patch carries its correction field, pinned (computed on its staged base)
            if _sha(p["corr_npz"]) != p["corr_sha256"]:
                raise SystemExit("DEV-24 HALT: %s is not the pinned correction field" % p["corr_npz"])
            fixed = np.load(p["corr_npz"])["corr"].astype(np.float64)
        out, w, corr, M = paste_local(old, new, R, pc, fixed)
        sup = np.zeros_like(support); sup[y0:y0 + CH, x0:x0 + CW] = w > 0
        if (sup & support).any():
            raise SystemExit("DEV-24 HALT: patch %s overlaps an earlier patch's support in its layer" % p["name"])
        support |= sup
        loc = np.clip(out + 0.5, 0, 255).astype(np.uint8)
        cur = full[y0:y0 + CH, x0:x0 + CW]
        cur[w > 0] = loc[w > 0]
        rep.append({"name": p["name"], "paste_px": int(M.sum()), "support_px": int(sup.sum()),
                    "tone_corr_mean_abs": round(float(np.abs(corr[M]).mean()), 2) if M.any() else None})
    return full, {"patches": rep, "changed_px": int((full != img).any(-1).sum())}


def apply(img: np.ndarray, block: dict):
    """img: the stitch, uint8 H x W x 3; block = {"layers": [layer, ...]} applied in order, each verified against the
    image it was staged on (the stitch for the first, the previous layer's result after). -> (patched uint8, report)"""
    cur, rep = img, []
    for i, layer in enumerate(block["layers"]):
        cur, r = apply_layer(cur, layer)
        r["layer"] = i + 1
        rep.append(r)
    return cur, {"layers": rep, "changed_px": int((cur != img).any(-1).sum()), "result_pixels_sha256": pixels_sha(cur)}
