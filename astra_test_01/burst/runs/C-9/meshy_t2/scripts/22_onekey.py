#!/usr/bin/env python3
"""C-9 meshy_t2 step 16: build a clip from ONE painted key per direction.

    python3 scripts/22_onekey.py <variant X|Y> [--clips walk,idle,run,attack]
                                 [--dirs S,SE,E,...] [--force] [--plan]

R-C9-65: no per-frame paint ships. The knight was rejected because cells Astra
painted individually drift -- helm, visor and pollaxe change shape between
frames -- while the EbSynth-propagated directions stayed steady. So every
frame except one per direction is propagated.

TWO VARIANTS, and the difference is which key drives which clip:

  X  a separate key per CLIP per direction. 32 keys for this character.
     Each clip is propagated from its own painted frame, so the key already
     shows roughly the right pose and EbSynth has less to do.

  Y  ONE key per direction, driving ALL FOUR clips. 8 keys for this character.
     This works at all only because the `pos` guide is CLIP-INVARIANT: it
     stores the REST-pose bind position of the surface under each pixel, baked
     per vertex before skinning, so idle frame 0 and attack frame 7 label the
     same body point with the same value. EbSynth is therefore matching "which
     part of the creature is this", not "which frame is this", and the source
     frame does not have to belong to the target's clip.
     Y is the one that scales: 1-2 Astra sheets per character instead of 8-16.
     The place it should struggle is the ATTACK lunge, whose poses are furthest
     from an idle key.

KEY CHOICE. For a painted direction (E, SE) the key is the frame whose pose is
NEAREST THE CLIP'S MEAN, measured on the render's own silhouettes rather than
picked by eye: the frame whose mask has the highest mean IoU against all the
other frames of that clip and direction. A mean-pose key is the shortest
average distance for EbSynth to travel, and for a cycle it beats frame 0,
which is usually an extreme. For the six propagated directions only two keys
were painted, so the better of the two is taken on the same measure.
"""
import argparse, json, os, shutil, subprocess, sys, time
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
WORK = os.path.join(ROOT, "work")
EBS = "/Users/admin/tools/ebsynth/bin/ebsynth"
GUIDES = [("pos", 4.0), ("part", 2.0), ("mask", 2.0)]
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
PAINTED = ["E", "SE"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}
FRAME = 512


def flat(src, dst):
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(dst)
    return dst


def gp(clip, d, i, which):
    return {"pos": os.path.join(OUT, clip, "guides_pos", d, "pos_%s_%02d.png" % (d, i)),
            "part": os.path.join(OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i)),
            "mask": os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i)),
            }[which]


def mask_of(clip, d, i):
    return np.asarray(Image.open(gp(clip, d, i, "mask")).convert("RGBA"))[..., 3] > 128


def mean_pose_frame(clip, d, candidates):
    """The candidate whose silhouette is most like all the clip's frames."""
    n = CLIPS[clip]
    allm = [mask_of(clip, d, i) for i in range(n)]
    best, bi = -1.0, candidates[0]
    scores = {}
    for c in candidates:
        mc = allm[c]
        s = float(np.mean([(mc & m).sum() / max((mc | m).sum(), 1) for m in allm]))
        scores[c] = round(s, 4)
        if s > best:
            best, bi = s, c
    return bi, scores


def paint_root(chosen, clip, d):
    """Where the painted cells for this clip/direction live."""
    src = chosen.get(clip, {})
    if d in PAINTED:
        v = src.get(d)
        return (os.path.join(ROOT, "paint_%s" % v), list(range(CLIPS[clip]))) if v else (None, [])
    k = src.get("keys")
    v = (k.get(d) if isinstance(k, dict) else k)
    return ((os.path.join(ROOT, "paint_%s" % v), [0, CLIPS[clip] // 2])
            if v else (None, []))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("variant", choices=["X", "Y"])
    ap.add_argument("--clips", default="walk,idle,run,attack")
    ap.add_argument("--dirs", default=",".join(DIRS))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--ykey-clip", default="idle")
    args = ap.parse_args()
    chosen = json.load(open(os.path.join(WORK, "chosen.json")))
    clips = args.clips.split(",")
    dirs = args.dirs.split(",")
    dest_root = os.path.join(ROOT, "sprites_%s" % args.variant.lower())

    # ---- choose the key(s) -------------------------------------------------
    keys = {}       # (clip, dir) -> (src_clip, src_frame, src_png)
    plan = dict(variant=args.variant, key_rule=(
        "one key per clip per direction" if args.variant == "X"
        else "one key per direction from the %s clip, driving all clips"
             % args.ykey_clip), keys={}, scores={})
    for d in dirs:
        if args.variant == "Y":
            kc = args.ykey_clip
            root, cands = paint_root(chosen, kc, d)
            if root is None:
                print("  no paint for %s %s - skipped" % (kc, d)); continue
            bi, sc = mean_pose_frame(kc, d, cands)
            png = os.path.join(root, kc, d, "%s_%s_%02d.png" % (kc, d, bi))
            plan["scores"]["%s/%s" % (kc, d)] = sc
            for clip in clips:
                keys[(clip, d)] = (kc, bi, png)
            plan["keys"][d] = dict(src_clip=kc, src_frame=bi,
                                   src=os.path.relpath(png, ROOT))
        else:
            for clip in clips:
                root, cands = paint_root(chosen, clip, d)
                if root is None:
                    continue
                bi, sc = mean_pose_frame(clip, d, cands)
                png = os.path.join(root, clip, d, "%s_%s_%02d.png" % (clip, d, bi))
                keys[(clip, d)] = (clip, bi, png)
                plan["scores"]["%s/%s" % (clip, d)] = sc
                plan["keys"]["%s/%s" % (clip, d)] = dict(
                    src_clip=clip, src_frame=bi, src=os.path.relpath(png, ROOT))
    runs = sum(CLIPS[c] - (1 if k[0] == c else 0)
               for (c, d), k in keys.items())
    plan["ebsynth_runs"] = runs
    json.dump(plan, open(os.path.join(WORK, "onekey_plan_%s.json" % args.variant), "w"),
              indent=1)
    print("variant %s: %d (clip,dir) pairs, %d EbSynth runs" % (args.variant, len(keys), runs))
    if args.plan:
        for k, v in sorted(plan["keys"].items()):
            print("   %-12s <- %s frame %02d" % (k, v["src_clip"], v["src_frame"]))
        return

    # ---- propagate ---------------------------------------------------------
    rep = dict(plan, dirs={}, total_s=0.0)
    t0 = time.time()
    for (clip, d), (kc, ki, kpng) in sorted(keys.items()):
        n = CLIPS[clip]
        tmp = os.path.join(WORK, "ebs_%s" % args.variant.lower(), clip, d)
        os.makedirs(tmp, exist_ok=True)
        style = flat(kpng, os.path.join(tmp, "style.png"))
        # guides flattened once per (clip, dir); the SOURCE guide comes from the
        # key's own clip and frame, which for Y is a different clip entirely
        src_g = {nm: flat(gp(kc, d, ki, nm), os.path.join(tmp, "src_%s.png" % nm))
                 for nm, _ in GUIDES}
        dd = os.path.join(dest_root, clip, d)
        os.makedirs(dd, exist_ok=True)
        times = []
        for i in range(n):
            outp = os.path.join(dd, "%s_%s_%02d.png" % (clip, d, i))
            if os.path.exists(outp) and not args.force:
                continue
            m = mask_of(clip, d, i)
            if clip == kc and i == ki:
                shutil.copy(kpng, outp)     # the key ships as painted
                continue
            tg = {nm: flat(gp(clip, d, i, nm), os.path.join(tmp, "tgt_%s.png" % nm))
                  for nm, _ in GUIDES}
            cmd = [EBS, "-style", style]
            for nm, w in GUIDES:
                cmd += ["-guide", src_g[nm], tg[nm], "-weight", str(w)]
            raw = os.path.join(tmp, "raw_%02d.png" % i)
            cmd += ["-output", raw, "-backend", "cpu"]
            t = time.time()
            r = subprocess.run(cmd, capture_output=True)
            if r.returncode != 0:
                raise RuntimeError(r.stderr.decode()[-400:])
            times.append(time.time() - t)
            rgb = np.asarray(Image.open(raw).convert("RGB"))
            rgba = np.zeros((FRAME, FRAME, 4), np.uint8)
            rgba[..., :3][m] = rgb[m]
            rgba[..., 3][m] = 255
            Image.fromarray(rgba, "RGBA").save(outp)
        rep["dirs"]["%s/%s" % (clip, d)] = dict(
            key="%s f%02d" % (kc, ki), runs=len(times),
            mean_s=round(float(np.mean(times)), 2) if times else None)
        print("  %-7s %-3s key %s f%02d  %2d runs  %s"
              % (clip, d, kc, ki, len(times),
                 ("%.1f s mean" % float(np.mean(times))) if times else "cached"))
    rep["total_s"] = round(time.time() - t0, 1)
    json.dump(rep, open(os.path.join(WORK, "onekey_%s.json" % args.variant), "w"),
              indent=1)
    print("variant %s done in %.0f s -> %s"
          % (args.variant, rep["total_s"], os.path.relpath(dest_root, ROOT)))


if __name__ == "__main__":
    main()
