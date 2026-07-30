#!/usr/bin/env python3
"""
wall-read-probe.py — WALL-READ cell (galadriel, 2026-07-30).

Answers Matt's question "why are the inside faces of the walls black in these
versions?" from EXISTING frames only. No render is taken; this repo tree
(reincarnated-godot) is READ-ONLY for this cell (drax holds the single-writer
lock under AMB-HUE).

THE DISCRIMINATOR IS WITHIN ONE FRAME, not across frames. Cross-frame luma is
NOT comparable here (different cameras, distances, exposures), so the two
assumption-free readings are:

  (a) TEXTURE ENERGY  |grad| = mean absolute 1-px luma gradient. A brick wall
      that is merely UNDERLIT still carries its coursing; a flat untextured
      material carries none. Exposure-insensitive in the way mean luma is not.
  (b) WITHIN-FRAME RATIO against a surface in the same frame under the same
      lights (the floor, and the kit wall-top course that stands ABOVE the
      suspect slab).

Run from the reincarnated-godot repo root:
    python3 <this>/wall-read-probe.py /Users/admin/Games/reincarnated-godot
"""
import sys
import numpy as np
from PIL import Image
from pathlib import Path


def srgb2lin(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def stats(path, box, label):
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
    x0, y0, x1, y1 = box
    r = a[y0:y1, x0:x1]
    L = 0.2126 * r[:, :, 0] + 0.7152 * r[:, :, 1] + 0.0722 * r[:, :, 2]
    gx = np.abs(np.diff(L, axis=1)).mean()
    gy = np.abs(np.diff(L, axis=0)).mean()
    z = int(np.all(r == 0, axis=2).sum())
    print(
        f"  {label:44s} mean={L.mean():6.2f} p50={np.percentile(L,50):6.2f} "
        f"p95={np.percentile(L,95):6.2f} max={L.max():6.2f} "
        f"|grad|={0.5*(gx+gy):5.2f} true-black={100.0*z/L.size:5.1f}%"
    )
    return L.mean(), 0.5 * (gx + gy)


def brightest_patch(path, xr, yr, bw, bh, bloom_cut=120.0):
    """Locate the brightest non-bloom bw x bh box in a region — used to find the
    kit masonry course that survives ABOVE the suspect slab, without hand-picking
    a flattering box."""
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
    L = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    best = None
    for y in range(yr[0], yr[1], 2):
        for x in range(xr[0], xr[1], 2):
            w = L[y:y + bh, x:x + bw]
            if w.size == 0 or w.max() > bloom_cut:
                continue
            if best is None or w.mean() > best[0]:
                best = (w.mean(), x, y)
    return best


def main(godot_root):
    G = Path(godot_root)

    print("=" * 96)
    print("§A  ALBEDO ARITHMETIC — what the two materials are, before any pixel is read")
    print("=" * 96)
    tex = np.asarray(
        Image.open(G / "Assets/Synty/polygon-dark-fantasy/SourceFiles/Textures/Misc/Brick_Small_01.png").convert("RGB"),
        dtype=np.float64,
    ) / 255.0
    brick_srgb = tex.reshape(-1, 3).mean(axis=0)
    brick_lin = srgb2lin(tex).reshape(-1, 3).mean(axis=0)
    slab_srgb = np.array([0.115, 0.118, 0.132])   # wr2_playback.gd::_dress_wall_faces face_mat
    pil_srgb = np.array([0.145, 0.148, 0.163])    # ditto, corner pilasters
    slab_lin, pil_lin = srgb2lin(slab_srgb), srgb2lin(pil_srgb)
    print(f"  Brick_Small_01 (kit tex_wall)   sRGB {np.round(brick_srgb,4)} -> LINEAR {np.round(brick_lin,5)}")
    print(f"  ArenaShellFace slab             sRGB {slab_srgb} -> LINEAR {np.round(slab_lin,5)}")
    print(f"  ArenaShellFace pilaster         sRGB {pil_srgb} -> LINEAR {np.round(pil_lin,5)}")
    print(f"  LINEAR reflectance slab/brick = {slab_lin.mean()/brick_lin.mean():.4f}"
          f"   (the slab is {brick_lin.mean()/slab_lin.mean():.1f}x darker than the masonry it stands in front of)")

    P = G / "tmp/camlock/plates/_raw_plate1080.png"
    print()
    print("=" * 96)
    print("§B  THE WITHIN-FRAME CONTROL — CAM-LOCK player_lock plate, 1920x1080")
    print("    (wr2_playback.gd lineage: _dress_wall_faces() ACTIVE)")
    print("=" * 96)
    slab_m, slab_g = stats(P, (200, 100, 350, 160), "the 'black wall' (arena-shell slab)")
    floor_m, _ = stats(P, (380, 265, 470, 310), "floor, kit tile (same frame)")
    b = brightest_patch(P, (60, 320), (80, 170), 24, 14)
    cap_m, cap_g = stats(P, (b[1], b[2], b[1] + 24, b[2] + 14),
                         f"kit masonry ABOVE the slab @({b[1]},{b[2]})")
    print(f"  --> slab / floor luma        = {slab_m/floor_m:.3f}")
    print(f"  --> slab / masonry luma      = {slab_m/cap_m:.3f}   ({cap_m/slab_m:.2f}x darker, SAME FRAME)")
    print(f"  --> masonry|grad| / slab|grad| = {cap_g/max(slab_g,1e-6):.0f}x   (the slab carries no surface detail at all)")

    Q = G / "tmp/wr1/lvl_inside0_small.png"
    print()
    print("=" * 96)
    print("§C  THE SAME 37.5 m ROOM, SAME LIGHTING, WITHOUT the WR2 dressing")
    print("    (wr1_level.gd -> kit_replica_level.gd; tmp/wr1/lvl_inside0_small.png)")
    print("=" * 96)
    w_m, w_g = stats(Q, (20, 148, 150, 178), "inner wall face (kit masonry)")
    f_m, _ = stats(Q, (240, 255, 420, 330), "floor, kit tile (same frame)")
    print(f"  --> wall / floor luma        = {w_m/f_m:.3f}    (vs {slab_m/floor_m:.3f} once the slab is in front of it)")
    print(f"  --> wall |grad|              = {w_g:.2f}      (vs {slab_g:.2f} for the slab)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/Users/admin/Games/reincarnated-godot")
