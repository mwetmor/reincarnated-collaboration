#!/usr/bin/env python3
"""C-9 meshy_t1: assemble the shipping sprite set and its manifest.

    python3 scripts/13_assemble.py walk idle

Pulls each direction from the best source available and says which, per
direction, in the manifest -- the integration session should not have to guess
whether a frame was painted or propagated:

    painted_full   the Astra sheet for that direction, cut back (E, SE)
    ebsynth_2key   propagated from two painted keys (the other six)
    render         the raw 3D render, only if neither exists

Every frame is checked against its own guide mask before it ships: a frame
whose alpha disagrees with the geometry it was rendered from is not a sprite,
it is a registration error, and shipping it would put the error into the game
rather than into this report.
"""
import json, os, shutil, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
OUT = os.path.join(T1, "out")
DEST = os.path.join(T1, "sprites_t1")
ALL = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
# which painted variant won, per state and direction (gandalf's call)
PAINT_PICK = {("walk", "E"): "a", ("walk", "SE"): "a",
              ("idle", "E"): "b", ("idle", "SE"): "b"}


def despill(rgba):
    """Remove plate green from a sprite.

    The fully painted directions carry ~0.01 % green pixels; every PROPAGATED
    direction carried 2-6 %. EbSynth is a patch synthesiser, so the thin green
    rim left in a key's matte does not stay at the rim -- it gets copied into
    the interior wherever that patch matches. Hard-replace the strongly green
    pixels from their nearest clean neighbour inside the figure, and pull the
    green channel down on the merely tinted ones.
    """
    a = rgba[..., 3] > 8
    rgb = rgba[..., :3].astype(np.int16)
    g = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
    hard = (g > 25) & a
    if hard.any():
        src = a & ~hard
        if src.any():
            _, ind = ndi.distance_transform_edt(~src, return_indices=True)
            for c in range(3):
                ch = rgba[..., c]
                ch[hard] = ch[ind[0][hard], ind[1][hard]]
    rgb = rgba[..., :3].astype(np.int16)
    g = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
    soft = (g > 6) & a
    if soft.any():
        cap = np.maximum(rgb[..., 0], rgb[..., 2]) + 6
        rgba[..., 1] = np.where(soft, np.clip(cap, 0, 255), rgba[..., 1]).astype(np.uint8)
    return rgba


def mask_of(p):
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 8


def guide_mask(state, d, i):
    g = os.path.join(OUT, state, "guides_part", d, "part_%s_%02d.png" % (d, i))
    return np.asarray(Image.open(g).convert("RGBA"))[..., 3] > 8


def main():
    states = sys.argv[1:] or ["walk", "idle"]
    cam = json.load(open(os.path.join(T1, "camera.json")))
    man = {"note": "C-9 meshy_t1 T1 sprite set.",
           "px_per_m": cam["px_per_m"], "frame_px": cam["frame_px"],
           "ground_row_y": cam["ground_row_y"],
           "elevation_deg": cam["elevation_deg"],
           "azimuths_deg": cam["azimuths_deg"],
           "source_faces": [], "states": {}}
    for st in states:
        rj = json.load(open(os.path.join(OUT, st, "render_%s.json" % st)))
        n = rj["frames"]
        ent = dict(frames=n, fps=round(rj["fps"], 4),
                   cycle_period_s=round(n / rj["fps"], 4), dirs={})
        for d in ALL:
            dd = os.path.join(DEST, st, d)
            os.makedirs(dd, exist_ok=True)
            pick = PAINT_PICK.get((st, d))
            src, kind = None, None
            if pick:
                cand = os.path.join(T1, "paint_%s" % pick, st, d)
                if os.path.isdir(cand):
                    src, kind = cand, "painted_full(%s)" % pick
            if src is None:
                cand = os.path.join(T1, "ebs_t1", st, d)
                if os.path.isdir(cand) and len(os.listdir(cand)) >= n:
                    src, kind = cand, "ebsynth_2key"
            if src is None:
                src, kind = os.path.join(OUT, st, "colour", d), "render"
            ok, bad = 0, []
            green_before = green_after = 0
            for i in range(n):
                f = "%s_%s_%02d.png" % (st, d, i)
                sp = os.path.join(src, f)
                if not os.path.exists(sp):
                    bad.append(dict(frame=i, why="missing")); continue
                m = mask_of(sp); g = guide_mask(st, d, i)
                iou = float((m & g).sum()) / max(int((m | g).sum()), 1)
                if iou < 0.55:
                    bad.append(dict(frame=i, why="registration", iou=round(iou, 3)))
                    continue
                arr = np.asarray(Image.open(sp).convert("RGBA")).copy()
                before = int(((arr[..., 1].astype(np.int16)
                               - np.maximum(arr[..., 0], arr[..., 2]).astype(np.int16)) > 25)
                             [arr[..., 3] > 8].sum())
                arr = despill(arr)
                after = int(((arr[..., 1].astype(np.int16)
                              - np.maximum(arr[..., 0], arr[..., 2]).astype(np.int16)) > 25)
                            [arr[..., 3] > 8].sum())
                green_before += before; green_after += after
                Image.fromarray(arr).save(os.path.join(dd, f))
                ok += 1
            ent["dirs"][d] = dict(source=kind, frames_written=ok,
                                  rejected=bad, src_dir=os.path.relpath(src, T1),
                                  green_px_before=green_before,
                                  green_px_after=green_after)
            print("  %-5s %-3s %-18s %2d/%2d%s" % (st, d, kind, ok, n,
                                                   "  REJECTED %s" % bad if bad else ""))
        ent["complete"] = all(v["frames_written"] == n for v in ent["dirs"].values())
        man["states"][st] = ent
    man["complete"] = all(v["complete"] for v in man["states"].values())
    os.makedirs(DEST, exist_ok=True)
    json.dump(man, open(os.path.join(DEST, "manifest.json"), "w"), indent=1)
    print("\ncomplete: %s   ->  %s" % (man["complete"], DEST))


if __name__ == "__main__":
    main()
