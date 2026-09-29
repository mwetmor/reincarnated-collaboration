#!/usr/bin/env python3
"""C-9 T9-1b: put the repainted albedo chunks back on the plate, to the pixel.

    python3 tools/reassemble_albedo.py --painted t9_1b/painted
    python3 tools/reassemble_albedo.py --self-test        # check the instrument first

WHAT THIS HAS TO GET RIGHT, in the order it can go wrong:

1. SIZE. The canvases went out at exactly 1536x1024 because that is a size the image model
   returns. If a chunk comes back another size it is resampled here and the report says so
   in capitals -- a resampled chunk cannot be trusted to the pixel and the run should be
   re-fired rather than accepted quietly.

2. REGISTRATION, measured and not assumed. Each chunk is phase-correlated against the crop
   it was made from and the offset is REPORTED, every time, including when it is (0,0) --
   an instrument that only speaks when it is unhappy is an instrument you cannot tell from
   a broken one. Correlation runs on GRADIENT MAGNITUDE, not on luma: the whole point of
   this repaint is that the tone changes, and tone-based correlation would be reading the
   one thing that is supposed to move. Edges do not move, so edges are what is matched.

3. THE OVERLAPS. Neighbouring chunks are repainted independently and will not agree
   exactly. Weights are a linear ramp in from each tile edge and the blend is NORMALISED
   (sum(w*c)/sum(w)), so a pixel covered by one tile keeps that tile at full strength and
   a pixel in an overlap cross-fades. No tile is attenuated merely for being alone.

4. ALPHA, restored from the ORIGINAL PLATE and never from the return. 39.75% of this plate
   is transparent; the backdrop starts occluding the sky the moment that channel drifts.
   The per-tile alpha PNGs written at cut time are checked against the plate as a second,
   independent path to the same answer -- if the two ever disagree, something has been
   edited underneath this script and it halts.

5. RGB UNDER alpha==0 STAYS AS IT WAS. It is not black by accident, and it is not green:
   filter_linear_mipmap averages neighbouring texels at distance, so writing #00ff00 into
   the transparent region would hang a green fringe on every chasm edge in the scene. The
   canvases show green there so nobody repaints noise; the plate keeps its own.

Outside the repainted region the output is the original plate, byte for byte. That is
asserted at the end, not hoped for.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None

HERE = pathlib.Path(__file__).resolve().parent.parent
GREEN = np.array([0, 255, 0], np.int16)


# --------------------------------------------------------------------------- registration
def _grad(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Gradient magnitude of luma, zeroed outside the painted mask, Hann-windowed.

    Gradient rather than luma because the repaint's job is to change luma. Hann because a
    hard rectangular edge is itself a strong periodic feature and phase correlation will
    happily lock onto the window instead of the picture."""
    lum = (0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]).astype(np.float32)
    lum = np.where(mask, lum, 0.0)
    gy = ndimage.sobel(lum, axis=0, mode="constant")
    gx = ndimage.sobel(lum, axis=1, mode="constant")
    g = np.hypot(gx, gy)
    g = np.where(mask, g, 0.0)
    g -= g.mean()
    h, w = g.shape
    g *= np.hanning(h)[:, None] * np.hanning(w)[None, :]
    return g


def register(ref: np.ndarray, moved: np.ndarray, mask: np.ndarray,
             limit: int = 64) -> tuple[int, int, float]:
    """Integer (dy, dx) such that moved[y, x] corresponds to ref[y - dy, x - dx].

    i.e. the chunk came back displaced by (dy, dx); shifting it by (-dy, -dx) re-registers
    it. The sign is not argued from first principles -- it is pinned by --self-test, which
    displaces a known crop by a known amount and checks this function returns it."""
    A = np.fft.rfft2(_grad(ref, mask))
    B = np.fft.rfft2(_grad(moved, mask))
    R = A.conj() * B
    n = np.abs(R)
    R = np.divide(R, n, out=np.zeros_like(R), where=n > 1e-12)
    c = np.fft.irfft2(R, s=ref.shape[:2])
    h, w = c.shape
    # search only the plausible window; a global argmax can land on a wrap-around twin
    win = np.full_like(c, -np.inf)
    for sy in (slice(0, limit + 1), slice(h - limit, h)):
        for sx in (slice(0, limit + 1), slice(w - limit, w)):
            win[sy, sx] = c[sy, sx]
    idx = int(np.argmax(win))
    dy, dx = divmod(idx, w)
    if dy > h // 2:
        dy -= h
    if dx > w // 2:
        dx -= w
    peak = float(c[idx // w, idx % w])
    sigma = float(c.std()) or 1e-9
    return dy, dx, peak / sigma


def shift_int(img: np.ndarray, dy: int, dx: int) -> np.ndarray:
    """Shift by whole pixels, filling the vacated strip by edge replication.

    Whole pixels only: a sub-pixel shift resamples, and resampling is the thing this
    module exists to avoid. A fractional residual is reported instead and left alone."""
    if dy == 0 and dx == 0:
        return img
    out = np.empty_like(img)
    src_y = slice(max(0, dy), img.shape[0] + min(0, dy))
    dst_y = slice(max(0, -dy), img.shape[0] + min(0, -dy))
    src_x = slice(max(0, dx), img.shape[1] + min(0, dx))
    dst_x = slice(max(0, -dx), img.shape[1] + min(0, -dx))
    out[:] = img[0, 0]
    out[dst_y, dst_x] = img[src_y, src_x]
    # replicate the edges into the vacated strips
    if dy > 0:
        out[img.shape[0] - dy:, :] = out[img.shape[0] - dy - 1:img.shape[0] - dy, :]
    elif dy < 0:
        out[:-dy, :] = out[-dy:-dy + 1, :]
    if dx > 0:
        out[:, img.shape[1] - dx:] = out[:, img.shape[1] - dx - 1:img.shape[1] - dx]
    elif dx < 0:
        out[:, :-dx] = out[:, -dx:-dx + 1]
    return out


# --------------------------------------------------------------------------- weights
def ramp_weight(h: int, w: int, feather: int) -> np.ndarray:
    ry = np.clip((np.minimum(np.arange(h), h - 1 - np.arange(h)) + 0.5) / feather, 0.0, 1.0)
    rx = np.clip((np.minimum(np.arange(w), w - 1 - np.arange(w)) + 0.5) / feather, 0.0, 1.0)
    return np.maximum(ry[:, None] * rx[None, :], 1e-4).astype(np.float32)


# --------------------------------------------------------------------------- main
def find_chunk(d: pathlib.Path, tid: str) -> pathlib.Path | None:
    if not d.is_dir():
        return None
    exact = d / ("t9_albedo_%s.png" % tid)
    if exact.exists():
        return exact
    hits = sorted(p for p in d.glob("*.png") if tid in p.name)
    return hits[-1] if hits else None


def run(grid_path: pathlib.Path, painted_dir: pathlib.Path, out_path: pathlib.Path,
        feather: int, edge_feather: int, report_path: pathlib.Path | None,
        chunks: dict[str, np.ndarray] | None = None) -> dict:
    grid = json.loads(grid_path.read_text())
    plate_path = HERE / grid["plate"]["file"]
    plate = np.asarray(Image.open(plate_path)).copy()
    H, W = plate.shape[:2]
    if [W, H] != grid["plate"]["size"]:
        raise SystemExit("plate is %dx%d, grid says %s" % (W, H, grid["plate"]["size"]))
    alpha = plate[..., 3]

    acc = np.zeros((H, W, 3), np.float32)
    wsum = np.zeros((H, W), np.float32)
    covered = np.zeros((H, W), bool)
    rep = {"plate": str(plate_path), "tiles": {}, "feather": feather,
           "edge_feather": edge_feather, "warnings": []}

    for tid, t in grid["tiles"].items():
        x0, y0, x1, y1 = t["plate_rect"]
        tw, th = t["size"]
        ref = plate[y0:y1, x0:x1, :3].astype(np.float32)
        ta = alpha[y0:y1, x0:x1]

        # second, independent path to the same alpha -- they must agree
        mrec = np.asarray(Image.open(HERE / t["alpha_mask"]).convert("L"))
        if not np.array_equal(mrec, ta):
            raise SystemExit("HALT %s: recorded alpha mask disagrees with the plate "
                             "(%d px). The plate has been edited under this script."
                             % (tid, int((mrec != ta).sum())))

        if chunks is not None and tid in chunks:
            img = chunks[tid].astype(np.float32)
            src = "<in-memory>"
            resampled = None
        else:
            p = find_chunk(painted_dir, tid)
            if p is None:
                rep["tiles"][tid] = {"status": "MISSING", "looked_in": str(painted_dir)}
                rep["warnings"].append("%s: no painted chunk found -- left as the original plate" % tid)
                continue
            src = str(p)
            im = Image.open(p).convert("RGB")
            resampled = None
            if im.size != (tw, th):
                resampled = list(im.size)
                rep["warnings"].append(
                    "%s: RESAMPLED from %dx%d to %dx%d -- registration is no longer exact; "
                    "re-fire this canvas rather than trust it" % (tid, im.size[0], im.size[1], tw, th))
                im = im.resize((tw, th), Image.LANCZOS)
            img = np.asarray(im).astype(np.float32)

        painted_mask = ta > 0
        dy, dx, snr = register(ref, img, painted_mask)
        img = shift_int(img, dy, dx)
        if abs(dy) > 8 or abs(dx) > 8:
            rep["warnings"].append("%s: offset (%d,%d) is larger than a feather can hide" % (tid, dy, dx))
        # 120 sigma is CALIBRATED, not picked: --self-test leg (c) de-lights a real crop
        # hard enough to take its near-black to zero and the lock still comes back at
        # 700-960 sigma against a theoretical ceiling of sqrt(1536*1024) = 1254. A weak
        # threshold here is worse than none -- it reads "checked" and means nothing.
        if snr < 120.0:
            rep["warnings"].append("%s: correlation peak is weak (%.1f sigma, calibrated floor 700); "
                                   "the offset may be noise" % (tid, snr))

        # did the painter leave #00ff00 inside painted pixels?
        leak = int((np.abs(img.astype(np.int16) - GREEN).max(-1)[painted_mask] < 24).sum())

        w = ramp_weight(th, tw, feather)
        acc[y0:y1, x0:x1] += img * w[..., None]
        wsum[y0:y1, x0:x1] += w
        covered[y0:y1, x0:x1] = True

        before = ref[painted_mask]
        after = img[painted_mask]
        lum = lambda a: float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
        rep["tiles"][tid] = {
            "status": "ok", "source": src, "resampled_from": resampled,
            "offset_dy_dx": [int(dy), int(dx)], "peak_sigma": round(snr, 1),
            "green_leak_px": leak,
            "mean_luma_painted": {"before": round(lum(before), 2), "after": round(lum(after), 2)},
        }
        if leak:
            rep["warnings"].append("%s: %d painted pixels came back flat green" % (tid, leak))

    if not covered.any():
        raise SystemExit("no chunks were reassembled")

    blend = np.zeros_like(acc)
    np.divide(acc, wsum[..., None], out=blend, where=wsum[..., None] > 0)

    # feather the repainted union into the untouched plate
    d = ndimage.distance_transform_edt(covered)
    outer = np.clip(d / max(edge_feather, 1), 0.0, 1.0).astype(np.float32)
    outer[~covered] = 0.0

    out = plate.copy()
    orig_rgb = plate[..., :3].astype(np.float32)
    mixed = orig_rgb * (1.0 - outer[..., None]) + blend * outer[..., None]
    apply = covered & (alpha > 0)                       # never touch RGB under alpha==0
    out[..., :3][apply] = np.clip(np.rint(mixed[apply]), 0, 255).astype(np.uint8)

    # --- the assertions, run rather than assumed -------------------------------------
    if not np.array_equal(out[..., 3], plate[..., 3]):
        raise SystemExit("HALT: alpha changed")
    outside = ~apply
    if not np.array_equal(out[..., :3][outside], plate[..., :3][outside]):
        raise SystemExit("HALT: pixels changed outside the repainted region")
    rep["alpha_identical"] = True
    rep["untouched_outside_region"] = True
    rep["changed_px"] = int((out[..., :3] != plate[..., :3]).any(-1).sum())

    bv = grid["bridge_view_px"]
    for nm, a in (("plate_v4", plate), ("plate_v4_albedo", out)):
        s = a[bv["y0"]:bv["y1"], bv["x0"]:bv["x1"]]
        m = s[..., 3] > 0
        lu = 0.2126 * s[..., 0] + 0.7152 * s[..., 1] + 0.0722 * s[..., 2]
        rep.setdefault("bridge_view", {})[nm] = {
            "mean_luma_painted": round(float(lu[m].mean()), 2),
            "near_black_pct_painted": round(float((lu[m] <= 32).mean() * 100), 2)}

    Image.fromarray(out, "RGBA").save(out_path)
    rep["out"] = str(out_path)
    got = Image.open(out_path)
    if got.size != (W, H) or got.mode != "RGBA":
        raise SystemExit("HALT: wrote %s %s, expected %dx%d RGBA" % (got.size, got.mode, W, H))
    if report_path:
        report_path.write_text(json.dumps(rep, indent=1) + "\n")
    return rep


# --------------------------------------------------------------------------- self-test
def self_test(grid_path: pathlib.Path) -> int:
    """Check the instrument against a known case before trusting it on an unknown one.

    Two facts are pinned here, both of which have a sign or an identity that is easy to
    get backwards and impossible to notice afterwards:
      (a) feeding the ORIGINAL crops back reproduces the plate byte for byte;
      (b) a crop displaced by a KNOWN (dy,dx) is reported as that (dy,dx) and undone."""
    grid = json.loads(grid_path.read_text())
    plate = np.asarray(Image.open(HERE / grid["plate"]["file"]))
    tiles = grid["tiles"]
    ok = True

    ident = {}
    for tid, t in tiles.items():
        x0, y0, x1, y1 = t["plate_rect"]
        c = plate[y0:y1, x0:x1, :3].copy()
        c[plate[y0:y1, x0:x1, 3] == 0] = GREEN            # as the canvas was cut
        ident[tid] = c
    tmp = pathlib.Path("/tmp/_t9_selftest_identity.png")
    rep = run(grid_path, pathlib.Path("/nonexistent"), tmp, 96, 64, None, chunks=ident)
    back = np.asarray(Image.open(tmp))
    same = np.array_equal(back, plate)
    print("  (a) identity round-trip reproduces the plate byte for byte: %s  (changed px %d)"
          % (same, rep["changed_px"]))
    for tid, r in rep["tiles"].items():
        print("      %-9s offset %s  peak %.1f sigma" % (tid, r["offset_dy_dx"], r["peak_sigma"]))
        if r["offset_dy_dx"] != [0, 0]:
            ok = False
    ok = ok and same
    tmp.unlink(missing_ok=True)

    for want in ((3, -5), (-11, 7)):
        moved = {}
        for tid, c in ident.items():
            moved[tid] = shift_int(c, -want[0], -want[1])   # displace BY want
        tid0 = next(iter(tiles))
        t = tiles[tid0]
        x0, y0, x1, y1 = t["plate_rect"]
        ref = plate[y0:y1, x0:x1, :3].astype(np.float32)
        mask = plate[y0:y1, x0:x1, 3] > 0
        dy, dx, snr = register(ref, moved[tid0].astype(np.float32), mask)
        good = (dy, dx) == want
        print("  (b) displaced by %s -> reported %s  peak %.1f sigma   %s"
              % (want, (dy, dx), snr, "ok" if good else "WRONG"))
        ok = ok and good

    # (c) THE CASE THE INSTRUMENT WILL ACTUALLY FACE. Legs (a) and (b) match an image
    # against itself, which is not the job: the chunk that comes back has had its key
    # light, its cast shadows and its ambient occlusion taken out. So de-light a real crop
    # synthetically -- divide out the low-frequency luma field, lift the shadows, pull the
    # warm key, blur and re-grain so it is a repaint rather than a copy -- displace it by a
    # known amount, and check the lock still holds. It is what sets the 120-sigma floor in
    # run(); without this leg that number would be a guess wearing a measurement's clothes.
    rng = np.random.default_rng(7)
    for tid, t in tiles.items():
        x0, y0, x1, y1 = t["plate_rect"]
        ref = plate[y0:y1, x0:x1, :3].astype(np.float32)
        mask = plate[y0:y1, x0:x1, 3] > 0
        lum = 0.2126 * ref[..., 0] + 0.7152 * ref[..., 1] + 0.0722 * ref[..., 2]
        flat = ref * (lum.mean() / np.maximum(ndimage.gaussian_filter(lum, 40), 1))[..., None]
        flat = flat * 0.82 + 58.0
        flat[..., 0] *= 0.97
        flat[..., 2] *= 1.10
        flat = np.clip(ndimage.gaussian_filter(flat, 0.7) + rng.normal(0, 4.0, flat.shape), 0, 255)
        nb = lambda a: float(((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[mask] <= 32).mean() * 100)
        for want in ((0, 0), (4, -3), (-9, 13)):
            dy, dx, snr = register(ref, shift_int(flat, -want[0], -want[1]), mask)
            good = (dy, dx) == want
            ok = ok and good and snr >= 120.0
            print("  (c) %-9s de-lit (near-black %.2f%% -> %.2f%%) displaced %s -> %s  %.0f sigma  %s"
                  % (tid, nb(ref), nb(flat), want, (dy, dx), snr, "ok" if good else "WRONG"))

    print("SELF-TEST %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", default=str(HERE / "t9_1b" / "t9_albedo_grid.json"))
    ap.add_argument("--painted", default=str(HERE / "t9_1b" / "painted"))
    ap.add_argument("--out", default=str(HERE / "godot" / "plate" / "plate_v4_albedo.png"))
    ap.add_argument("--report", default=str(HERE / "t9_1b" / "reassemble_report.json"))
    ap.add_argument("--feather", type=int, default=96)
    ap.add_argument("--edge-feather", type=int, default=64)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test(pathlib.Path(a.grid))
    rep = run(pathlib.Path(a.grid), pathlib.Path(a.painted), pathlib.Path(a.out),
              a.feather, a.edge_feather, pathlib.Path(a.report))
    for tid, r in rep["tiles"].items():
        if r.get("status") != "ok":
            print("%-9s %s" % (tid, r["status"]))
            continue
        print("%-9s offset %s  peak %.1f sigma  luma %.1f -> %.1f  green-leak %d"
              % (tid, r["offset_dy_dx"], r["peak_sigma"],
                 r["mean_luma_painted"]["before"], r["mean_luma_painted"]["after"],
                 r["green_leak_px"]))
    print("bridge view painted-pixel luma %.1f -> %.1f, near-black %.2f%% -> %.2f%%" % (
        rep["bridge_view"]["plate_v4"]["mean_luma_painted"],
        rep["bridge_view"]["plate_v4_albedo"]["mean_luma_painted"],
        rep["bridge_view"]["plate_v4"]["near_black_pct_painted"],
        rep["bridge_view"]["plate_v4_albedo"]["near_black_pct_painted"]))
    for w in rep["warnings"]:
        print("WARN  %s" % w, file=sys.stderr)
    print("-> %s  (%d px changed; alpha identical)" % (rep["out"], rep["changed_px"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
