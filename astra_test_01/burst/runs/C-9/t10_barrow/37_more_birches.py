#!/usr/bin/env python3
"""C-9 T10: a second prompted pass for the birches evf-sam missed the first time.

The first pass asked for "the bare birch trees" and returned ONE tree out of several;
SAM2's 68 automatic proposals contained none at all. So this asks several narrower ways
and keeps the UNION, then splits it into instances. A prompted segmenter is a different
answer per phrasing, which is a weakness when you ask once and a lever when you ask five
times: the failure mode is a mask that is too small, not one that invents a tree, so the
union of five under-answers is closer to the truth than the best single one.
"""
import json, pathlib, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"
PROMPTS = {
    "birch2_all":    "every white-barked birch tree in the picture",
    "birch2_thin":   "the thin bare white tree trunks",
    "birch2_right":  "the bare trees on the right side",
    "birch2_left":   "the bare trees on the left side",
    "birch2_dead":   "the leafless dead trees with pale bark",
}

def main() -> int:
    import fal_client
    url = fal_client.upload_file(str(ART / "T10C-barrow_a.png"))
    got = []
    for name, prompt in PROMPTS.items():
        dst = WORK / ("evf_a_%s.png" % name)
        if not dst.exists():
            try:
                r = fal_client.subscribe("fal-ai/evf-sam",
                                         arguments={"image_url": url, "prompt": prompt})
                u = r["image"]["url"] if isinstance(r.get("image"), dict) else r["image"]
                subprocess.run(["curl", "-s", "-L", "-o", str(dst), u], check=True)
            except Exception as e:
                print("FAIL %-14s %s" % (name, str(e)[:70]), file=sys.stderr); continue
        m = np.asarray(Image.open(dst).convert("L")) > 127
        got.append((name, m))
        print("%-14s %5.2f%% of frame" % (name, m.mean() * 100))

    old = WORK / "evf_a_trees.png"
    union = np.asarray(Image.open(old).convert("L")) > 127 if old.exists() else None
    for _, m in got:
        union = m if union is None else (union | m)
    union = ndimage.binary_opening(union, np.ones((3, 3)))
    lab, n = ndimage.label(union)
    sizes = ndimage.sum(union, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s > 600]
    K, COS_P = 140.86, 0.602462172508240
    out = []
    for i in keep:
        ys, xs = np.nonzero(lab == i)
        out.append({"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                    "px": int((lab == i).sum()),
                    "height_m": round((ys.max() - ys.min() + 1) / (K * COS_P), 2),
                    "width_m": round((xs.max() - xs.min() + 1) / K, 2)})
    out.sort(key=lambda o: -o["px"])
    Image.fromarray((union * 255).astype(np.uint8)).save(WORK / "evf_a_birch_union.png")
    (HERE / "birches.json").write_text(json.dumps({"instances": out}, indent=1) + "\n")
    print("\nunion -> %d birch instances over 600 px: heights %s"
          % (len(out), [o["height_m"] for o in out]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
