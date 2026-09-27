#!/usr/bin/env python3
"""C-9: build the Illuminated-register ("B") texture set for the cliffside A/B build.

Reads the painted B art from runs/C-9/artifacts/ (READ-ONLY, conductor-owned) and
writes Godot-ready PNGs into this project's parallax/tiles_b/ and parallax/layers_b/,
plus parallax/layers_b/offsets.json.

  plate   CS9-band5/foreground.png       5376x4096 RGBA, STRAIGHT ALPHA, already
          matted (ground + rock + the ORIGINAL C-3 cloud band under the cliffs --
          band3 is deterministic, so the cloud pixels match H1's; band6 was fired in
          error and was already rejected in C-3 as R-C3-82).
          NO green key -- it arrives with its own alpha.  Split on the H1 tile grid:
             tiles_b/tile_0_0.png    (0,0,4096,4096)
             tiles_b/tile_4096_0.png (4096,0,1280,4096)
  sky     CS9-assembly/L11_layer_sky.png          opaque, no key (darker sunset)
  far     CS9-assembly/L12_layer_far.png          hills only -- the tower and cathedral
                                                  are REMOVED from the layer and placed
                                                  as sprites instead (R-C9-42); #00ff00
                                                  above the land -> UNMIX
  forest  CS9-assembly/L12_layer_forest.png       full-width burning band, 9 de-glitch
                                                  edits; #00ff00 above the treeline -> UNMIX
  mist    CS9-assembly/L10_layer_mist.png         light on black -> alpha=luminance,
                                                  capped 220/255, TINTED purple

ASPECT, NOT STRETCH.  The previous build resized every B layer to the H1 layer's exact
pixel size, which stretched sky and forest ~1.6x vertically because the painted art has
a different aspect from the H1 art.  This build scales each layer to the H1 layer's
WIDTH ONLY and keeps its aspect, then compensates with a per-style VERTICAL OFFSET so
the B layer's horizon lands on the same screen row the H1 layer's horizon did.  The
offset is written to offsets.json and applied by scripts/style_toggle.gd to the layer
Sprite2D's own position (A = 0, B = offsets.json), so the Parallax2D scroll maths,
camera, walkable.json and collision are untouched and the swap is reversible.

HORIZON.  For a layer with a keyed sky above it (far, forest) and for the mist, the
horizon is the first row whose opaque coverage (alpha > 128) crosses 50% -- the ridge
line, the treeline, the top of the mist bank.  The sky layer is opaque everywhere and
has no such row in either register, so it is BOTTOM-ALIGNED instead: the sky's bottom
edge is where the land begins, and both registers' skies are full-bleed sunsets.  Both
B sky and B far/forest/mist end up a superset or a near-superset of the H1 span in the
direction that matters, and the plate (z=0) covers anything short at the bottom.

KEY -> UNMIX (v3).  The L11 far and forest layers have SEMI-TRANSPARENT SMOKE painted
over the plate, and a key -- any key, hard or ramped -- is the wrong operation for it.
A key only ever chooses an alpha; it leaves the pixel's COLOUR as painted, and a
half-transparent smoke pixel painted over green IS half green.  Composited over the
sunset behind it, that smoke carries a measured +48.7/255 mean green excess on the far
layer and +58.1 on the forest: a green halo around every plume.

So v3 UNMIXES instead.  For a pixel P = a*F + (1-a)*G over a known backing G:

    a = 1 - d(P)/d(G)          d(x) = x_g - max(x_r, x_b)     [assumes d(F) ~ 0]
    F = (P - (1-a)*G) / a

Three things this needs that the obvious version gets wrong, all of them measured:

 1. G IS NOT #00ff00.  The painted plate arrives at RGB (3, 250, 7), d = 0.9529, not
    1.0.  Assume pure green and every plate pixel solves to a = 1 - 0.93 = 0.07 -- a
    7% green HAZE over the whole sky, not a fringe.  G is measured per layer as the
    median of the plate population (d > 0.8) and reported.

 2. THE PLATE STILL LEAKS.  Even against the measured G, 45% of plate pixels come out
    at a > 0.01 (max 0.156) because the plate itself is compression-noisy.  A small
    alpha floor (0.06, rescaled so the smoke is not clipped with it) takes that to
    0.7% and the max to 0.103.

 3. GREEN PAINT IS NOT PLATE.  Foliage painted at d = 0.2 solves to a = 0.79 -- the
    unmix would make the painter's own trees translucent and then despill the green
    out of them.  The plate is above the land by construction in both layers, so
    everything strictly below a column's LOWEST plate row is forced opaque, and
    despill is applied only where a < 0.98.  Fully opaque paint is returned untouched.

RESIDUAL, honestly measured.  The obvious check -- green excess of the unmixed
foreground -- reads 0.00 and always will: a = 1 - d/d(G) forces d(F) = 0 algebraically,
so that instrument is measuring its own arithmetic.  What is reported instead is the
green excess the layer ADDS to the composite over the sky behind it, across the smoke
band, which is what a player can actually see.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PROJ = Path(__file__).resolve().parent.parent
ART = PROJ.parent / "artifacts"
SRC = ART / "CS9-assembly"
BAND = ART / "CS9-band5"
A_LAYERS = PROJ / "parallax" / "layers"
OUT_TILES = PROJ / "parallax" / "tiles_b"
OUT_LAYERS = PROJ / "parallax" / "layers_b"

ALPHA_FLOOR = 0.06          # kills plate compression noise; see the docstring
MIST_TINT = np.array([150, 95, 170], np.float32) / 255.0
MIST_ALPHA_CAP = 220 / 255.0

# Horizontal placement of the B layers, in layer pixels, applied by style_toggle.gd the
# same way the vertical offsets are.  NONE of them needs one any more.
#
# It used to: far_ruins carried +160 x and a +626 y OVERRIDE, because the two giant
# landmarks painted INTO that layer stood 500-580 px above its ridge and the horizon
# rule put them off the top of the screen.  Matt's read of the result was that the
# horizon was "far too large" -- which it was: the override was sized for the
# landmarks, not for the land, and it dragged the whole ridge 598 px down the frame.
#
# R-C9-42 removes the cause instead of the symptom. The landmarks are cut OUT of the
# layer (CS9-assembly/L12_layer_far.png is the same painting with the tower and the
# cathedral removed and the hills continued behind them) and placed as two separate
# sprites, staggered in depth the way A's far layer staggers its own -- see
# tools/place_landmarks_b.py. With nothing tall left in it, the far layer is a layer of
# anonymous hills again and the plain horizon rule is exactly right for it: B's far
# ridge lands on the row A's far ridge occupies.
LAYER_DX = {"sky": 0.0, "far_ruins": 0.0, "forest_valley": 0.0, "mist": 0.0}
LAYER_DY_OVERRIDE = {}

# No layer's own top edge is in frame any more either, so the top-row fade that hid the
# guillotined plume is gone with the override that made it necessary. Kept as an empty
# dict rather than deleted: the mechanism is sound and the next layer that has to be
# dropped will want it.
TOP_FADE_PX = {}

# FG10 forest: 3x3 grid of 1536x1024 panels at step 1280x768 over 4096x2560
FG10_GRID = (3, 3)
FG10_PANEL = (1536, 1024)
FG10_STEP = (1280, 768)
FG10_CANVAS = (4096, 2560)


def load_rgb(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255.0


def _gx(c):
    """green excess: how much greener than the redder of red/blue."""
    return c[..., 1] - np.maximum(c[..., 0], c[..., 2])


def green_unmix(rgb, sky_for_residual=None):
    """-> (rgba, stats).  See the module docstring for why this is not a key."""
    d = _gx(rgb)
    plate = d > 0.8
    if plate.sum() < 1000:
        raise SystemExit("green_unmix: no plate population found (%d px)" % plate.sum())
    G = np.median(rgb[plate], axis=0)
    d_bg = float(G[1] - max(G[0], G[2]))

    a0 = np.clip(1.0 - d / d_bg, 0.0, 1.0)
    leak_before = float((a0[plate] > 0.01).mean())
    alpha = np.clip((a0 - ALPHA_FLOOR) / (1.0 - ALPHA_FLOOR), 0.0, 1.0)
    leak_after = float((alpha[plate] > 0.01).mean())

    # the plate is ABOVE the land in both of these layers, so nothing below a column's
    # lowest plate row can be backing -- force it opaque before anything else reads it
    clear = d > 0.5 * d_bg
    H = rgb.shape[0]
    rows = np.arange(H)[:, None]
    lowest = np.where(clear.any(0), (H - 1) - clear[::-1].argmax(0), -1)
    below = rows > lowest[None, :]
    forced = int((below & (alpha < 0.999)).sum())
    alpha = np.where(below, 1.0, alpha)

    a = np.maximum(alpha, 1e-4)[..., None]
    F = np.clip((rgb - (1.0 - a) * G) / a, 0.0, 1.0)
    mixed = alpha < 0.98
    mx = np.maximum(F[..., 0], F[..., 2])
    F[..., 1] = np.where(mixed & (F[..., 1] > mx), mx, F[..., 1])
    F = np.where((alpha >= 0.999)[..., None], rgb, F)      # opaque paint, untouched

    band = (alpha > 0.05) & (alpha < 0.95)
    # THE POPULATION TO MEASURE ON is semi-transparent smoke OVER THE PLATE, and it took
    # three tries to name it. Over the GUARDED band the hard key scores +0.00 and the
    # "improvement" is 0.0x -- the guard has already removed every pixel the key would
    # have damaged, and the instrument congratulates itself on a population it emptied.
    # Over the NAIVE band the unmix scores +36.29 against the key's +36.50 -- that band
    # is full of the painter's own green foliage, which the unmix correctly returns
    # untouched and the metric then charges it for. Both numbers are arithmetically
    # right and neither answers the question. The smoke over the plate is the
    # intersection: partial by the naive alpha, and above the plate boundary.
    naive_band = (a0 > 0.05) & (a0 < 0.95)
    stats = {"backing_rgb_255": [round(float(v) * 255, 2) for v in G],
             "d_backing": round(d_bg, 4),
             "plate_px_fraction": round(float(plate.mean()), 4),
             "plate_leak_before_floor": round(leak_before, 4),
             "plate_leak_after_floor": round(leak_after, 4),
             "alpha_floor": ALPHA_FLOOR,
             "forced_opaque_below_plate_px": forced,
             "smoke_band_px": int(band.sum()),
             "naive_band_px": int(naive_band.sum()),
             "smoke_over_plate_px": int((naive_band & ~below).sum())}
    stats_band = naive_band & ~below
    if sky_for_residual is not None and stats_band.sum():
        bg = np.asarray(sky_for_residual.resize((rgb.shape[1], rgb.shape[0]),
                                                Image.LANCZOS).convert("RGB"))
        bg = bg.astype(np.float32) / 255.0
        comp = a * F + (1.0 - a) * bg
        hard = (d < d_bg * 0.5).astype(np.float32)[..., None]
        comph = hard * rgb + (1.0 - hard) * bg
        ru = (_gx(comp) - _gx(bg))[stats_band]
        rh = (_gx(comph) - _gx(bg))[stats_band]
        stats["fringe_residual_over_sky_255"] = {
            "hard_key_mean": round(float(rh.mean()) * 255, 2),
            "hard_key_p99": round(float(np.percentile(rh, 99)) * 255, 2),
            "unmix_mean": round(float(ru.mean()) * 255, 2),
            "unmix_p99": round(float(np.percentile(ru, 99)) * 255, 2),
            "measured_over": "semi-transparent smoke over the plate (partial alpha AND above the plate boundary), %d px" % int(stats_band.sum()),
            "improvement_x": (round(float(rh.mean() / ru.mean()), 2)
                              if ru.mean() > 0.002 else "n/a (unmix residual ~0)"),
            # A key has TWO ways to be wrong and green excess only sees one of them.
            # Where the smoke is thin (a < 0.5) a hard key does not fringe it, it
            # DELETES it -- and a deleted plume scores a perfect 0.00 residual. The
            # forest reads "hard key +0.00" for exactly this reason, so the omission is
            # counted separately rather than left to look like a pass.
            "smoke_a_hard_key_would_delete_pct": round(
                100.0 * float((hard[..., 0][stats_band] < 0.5).mean()), 2),
        }
    rgba = np.dstack([F, alpha])
    rgba[alpha <= 0.0, :3] = 0.0
    return rgba, stats


def to_img(rgba):
    return Image.fromarray((np.clip(rgba, 0, 1) * 255.0 + 0.5).astype(np.uint8), "RGBA")


def horizon(img):
    """First row whose opaque coverage crosses 50%, or -1 if the layer never does."""
    a = np.asarray(img.convert("RGBA"))[..., 3]
    cov = (a > 128).mean(1)
    hit = np.nonzero(cov > 0.5)[0]
    return int(hit.min()) if len(hit) else -1


def assemble_fg10():
    """-> (PIL RGB 4096x2560, list of panel paths) or (None, missing) if incomplete."""
    picks, missing = [], []
    for r in range(FG10_GRID[1]):
        for c in range(FG10_GRID[0]):
            found = None
            for suffix in ("-r1", ""):        # a repaint wins over the first pass
                p = ART / f"FG10-{c}_{r}{suffix}" / f"FG10-{c}_{r}.png"
                if p.exists():
                    found = p
                    break
            if found is None:
                missing.append(f"FG10-{c}_{r}")
            else:
                picks.append((c, r, found))
    if missing:
        return None, missing
    canvas = Image.new("RGB", FG10_CANVAS, (0, 255, 0))
    for c, r, p in picks:                      # row-major, later over earlier
        panel = Image.open(p).convert("RGB")
        if panel.size != FG10_PANEL:
            panel = panel.resize(FG10_PANEL, Image.LANCZOS)
        canvas.paste(panel, (c * FG10_STEP[0], r * FG10_STEP[1]))
    return canvas, [str(p.relative_to(ART)) for _, _, p in picks]


def main():
    OUT_TILES.mkdir(parents=True, exist_ok=True)
    OUT_LAYERS.mkdir(parents=True, exist_ok=True)
    report = {}

    # ---- plate: already matted, no key ------------------------------------
    print("plate: CS9-band5/foreground.png (original C-3 clouds; straight alpha, no key)")
    plate = Image.open(BAND / "foreground.png").convert("RGBA")
    assert plate.size == (5376, 4096), f"plate is {plate.size}, expected (5376, 4096)"
    for name, x0, x1 in (("tile_0_0.png", 0, 4096), ("tile_4096_0.png", 4096, 5376)):
        cut = plate.crop((x0, 0, x1, 4096))
        cut.save(OUT_TILES / name)
        a = np.asarray(cut)[..., 3]
        print(f"  {name:<18} {cut.size[0]}x{cut.size[1]}  "
              f"alpha0 {(a <= 0).mean():.3f}  alpha1 {(a >= 254).mean():.3f}")
    del plate

    # ---- parallax layers ---------------------------------------------------
    sky_src = Image.open(SRC / "L11_layer_sky.png").convert("RGB")
    jobs = [
        ("sky.png", sky_src, "L11_layer_sky.png", "opaque"),
        ("far_ruins.png", Image.open(SRC / "L12_layer_far.png").convert("RGB"),
         "L12_layer_far.png", "unmix"),
        ("forest_valley.png", Image.open(SRC / "L12_layer_forest.png").convert("RGB"),
         "L12_layer_forest.png", "unmix"),
        ("mist.png", Image.open(SRC / "L10_layer_mist.png").convert("RGB"),
         "L10_layer_mist.png (tinted %s)" % list(map(int, MIST_TINT * 255)), "mist"),
    ]
    offsets, offsets_x, keystats = {}, {}, {}
    print("layers (scaled to the H1 WIDTH, aspect preserved):")
    for role, src_img, src_name, mode in jobs:
        rgb = np.asarray(src_img).astype(np.float32) / 255.0
        if mode == "opaque":
            rgba = np.dstack([rgb, np.ones(rgb.shape[:2], np.float32)])
        elif mode == "unmix":
            rgba, st = green_unmix(rgb, sky_for_residual=sky_src)
            keystats[role.replace(".png", "")] = st
            print("  %s unmix: backing %s d=%.4f  plate leak %.2f%%->%.2f%%  "
                  "band %d px  forced-opaque %d px"
                  % (role, st["backing_rgb_255"], st["d_backing"],
                     100 * st["plate_leak_before_floor"], 100 * st["plate_leak_after_floor"],
                     st["smoke_band_px"], st["forced_opaque_below_plate_px"]))
            fr = st.get("fringe_residual_over_sky_255")
            if fr:
                print("      FRINGE RESIDUAL over the sky behind it (0-255, smoke band): "
                      "hard key %+.2f mean / %+.2f p99   ->   unmix %+.2f / %+.2f   (%s)"
                      % (fr["hard_key_mean"], fr["hard_key_p99"],
                         fr["unmix_mean"], fr["unmix_p99"], str(fr["improvement_x"])))
                print("      a hard key would DELETE %.1f%% of that smoke outright "
                      "(thin plume, alpha < 0.5) -- invisible to the residual above"
                      % fr["smoke_a_hard_key_would_delete_pct"])
        else:
            # purple mist: DENSITY from the painting's luminance, COLOUR from the tint.
            # The painting is light-on-black, so luminance is exactly the mist's own
            # density map; taking colour from it as well would carry the greyscale
            # through and the tint would not read.
            lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
            alpha = np.minimum(lum, MIST_ALPHA_CAP)
            colour = np.broadcast_to(MIST_TINT, rgb.shape).copy()
            rgba = np.dstack([colour, alpha])
            rgba[alpha <= 0.0, :3] = 0.0
            keystats["mist"] = {"tint_rgb_255": [int(v) for v in MIST_TINT * 255],
                                "alpha_cap_255": int(round(MIST_ALPHA_CAP * 255)),
                                "alpha_mean": round(float(alpha.mean()), 4)}
        fade = TOP_FADE_PX.get(role.replace(".png", ""), 0)
        if fade:
            ramp = np.clip(np.arange(rgba.shape[0], dtype=np.float32) / float(fade), 0, 1)
            rgba[..., 3] *= ramp[:, None]
            print("  %s: top %d rows faded out (the layer's own edge is on screen after "
                  "the framing override)" % (role, fade))
        img = to_img(rgba)
        del rgb, rgba

        a_img = Image.open(A_LAYERS / role)
        aw, ah = a_img.size
        sw, sh = img.size
        tw, th = aw, int(round(aw * sh / sw))          # WIDTH match, aspect kept
        img = img.resize((tw, th), Image.LANCZOS)
        img.save(OUT_LAYERS / role)

        ha, hb = horizon(a_img), horizon(img)
        if ha <= 0 and hb <= 0:
            dy = ah - th                               # fully opaque: bottom-align
            rule = "bottom-aligned (no horizon row in either register)"
        else:
            dy = ha - hb
            rule = f"horizon A row {ha} <- B row {hb}"
        key = role.replace(".png", "")
        if key in LAYER_DY_OVERRIDE:
            dy = LAYER_DY_OVERRIDE[key]
            rule += "  [OVERRIDDEN to %+.0f for landmark framing -- see LAYER_DY_OVERRIDE]" % dy
        offsets[key] = float(dy)
        offsets_x[role.replace(".png", "")] = float(LAYER_DX.get(role.replace(".png", ""), 0.0))
        print(f"  {role:<18} {src_name}")
        print(f"      {sw}x{sh} -> {tw}x{th}   (H1 {aw}x{ah}, aspect kept, "
              f"{'taller' if th > ah else 'shorter'} by {abs(th - ah)})")
        print(f"      {rule}  ->  B sprite offset ({offsets_x[role.replace('.png','')]:+.0f}, {dy:+.0f})")
        del img, a_img

    (OUT_LAYERS / "offsets.json").write_text(json.dumps(
        {"note": "per-style vertical offset for the B parallax layer sprites; "
                 "A is always 0. Written by tools/build_b_assets.py.",
         "offsets": offsets, "offsets_x": offsets_x,
         "unmix": keystats, **report}, indent=1))
    print("wrote", OUT_LAYERS / "offsets.json")
    print("done ->", OUT_TILES, OUT_LAYERS)


if __name__ == "__main__":
    sys.exit(main())
