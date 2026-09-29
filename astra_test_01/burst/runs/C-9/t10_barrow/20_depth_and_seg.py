#!/usr/bin/env python3
"""C-9 T10: depth and segmentation for both Frost King's Barrow concept variants.

    python3 20_depth_and_seg.py [--force]

FOUR DEPTH MODELS, NOT ONE. A monocular depth model returns a plausible surface, not a
measured one, and it returns it with the same confidence whether it is right or wrong --
which in this run is the failure mode that has cost the most time. Four independent
estimates can be compared against each other and against the one thing in the picture whose
true size is known (the barbarian, 1.85 m), and where they agree the terrain is probably
real. Where they disagree, the variance map says so and that region gets no vote.

  depth-anything/v2  relative inverse depth, sharp at edges
  marigold-depth     diffusion-based, smooth and usually the best absolute ordering
  imageutils/depth   MiDaS-family baseline
  midas              returns a NORMAL MAP as well, which is an independent read on slope:
                     a heightfield derived from depth can be differentiated and checked
                     against it without going through depth twice.

SEGMENTATION serves two different questions and needs two models:
  sam2/auto-segment  every instance, unprompted -- the object LIST, including things I
                     would not have thought to ask for.
  evf-sam            one text prompt at a time -- the CLASS of a region, and the figure's
                     own silhouette, which is the scale bar the whole level is built on.

Everything is cached by filename: fal is cheap but not free, and a re-run while iterating
on the unprojection should cost nothing.
"""
import argparse
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"

DEPTH = {
    "depthanything": ("fal-ai/image-preprocessors/depth-anything/v2", "image"),
    "marigold": ("fal-ai/imageutils/marigold-depth", "image"),
    "imageutils": ("fal-ai/imageutils/depth", "image"),
    "midas": ("fal-ai/image-preprocessors/midas", "depth_map"),
    "midas_normal": ("fal-ai/image-preprocessors/midas", "normal_map"),
}

# what to ask evf-sam for, one prompt per call
PROMPTS = {
    "figure": "the viking warrior man standing in the snow",
    "standing_stones": "the tall upright standing stones",
    "barrow_door": "the stone doorway with its carved lintel",
    "ice": "the frozen lake of blue ice",
    "trees": "the bare birch trees",
    "juniper": "the dark green juniper bushes",
    "rock": "the grey rock outcrops",
    "path": "the trodden footprint path in the snow",
    "raven": "the black raven bird",
    "mound": "the grassy barrow mound",
}


def fetch(url: str, dst: pathlib.Path) -> None:
    subprocess.run(["curl", "-s", "-L", "-o", str(dst), url], check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    import fal_client

    WORK.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for v in ("a", "b"):
        src = ART / ("T10C-barrow_%s.png" % v)
        url = fal_client.upload_file(str(src))
        rec = {"source": str(src), "depth": {}, "evf": {}, "sam2": None}

        for name, (mid, key) in DEPTH.items():
            dst = WORK / ("depth_%s_%s.png" % (v, name))
            if dst.exists() and not a.force:
                print("cached  depth %s %s" % (v, name))
                rec["depth"][name] = str(dst)
                continue
            try:
                r = fal_client.subscribe(mid, arguments={"image_url": url})
                u = r[key]["url"] if isinstance(r.get(key), dict) else r[key]
                fetch(u, dst)
                rec["depth"][name] = str(dst)
                print("ok      depth %s %-13s -> %s" % (v, name, dst.name))
            except Exception as e:
                print("FAIL    depth %s %-13s %s" % (v, name, str(e)[:90]), file=sys.stderr)

        for pname, prompt in PROMPTS.items():
            dst = WORK / ("evf_%s_%s.png" % (v, pname))
            if dst.exists() and not a.force:
                rec["evf"][pname] = str(dst)
                continue
            try:
                r = fal_client.subscribe("fal-ai/evf-sam",
                                         arguments={"image_url": url, "prompt": prompt})
                u = r["image"]["url"] if isinstance(r.get("image"), dict) else r["image"]
                fetch(u, dst)
                rec["evf"][pname] = str(dst)
                print("ok      evf   %s %-16s" % (v, pname))
            except Exception as e:
                print("FAIL    evf   %s %-16s %s" % (v, pname, str(e)[:80]), file=sys.stderr)

        dst = WORK / ("sam2_%s.json" % v)
        if dst.exists() and not a.force:
            rec["sam2"] = str(dst)
        else:
            try:
                r = fal_client.subscribe("fal-ai/sam2/auto-segment",
                                         arguments={"image_url": url})
                dst.write_text(json.dumps(r, indent=1) + "\n")
                cm = r.get("combined_mask")
                if cm:
                    fetch(cm["url"] if isinstance(cm, dict) else cm,
                          WORK / ("sam2_%s_combined.png" % v))
                ims = r.get("individual_masks") or []
                for i, m in enumerate(ims):
                    fetch(m["url"] if isinstance(m, dict) else m,
                          WORK / ("sam2_%s_%03d.png" % (v, i)))
                rec["sam2"] = str(dst)
                print("ok      sam2  %s -> %d instance masks" % (v, len(ims)))
            except Exception as e:
                print("FAIL    sam2  %s %s" % (v, str(e)[:90]), file=sys.stderr)
        manifest[v] = rec

    (HERE / "sources.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print("-> %s" % (HERE / "sources.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
