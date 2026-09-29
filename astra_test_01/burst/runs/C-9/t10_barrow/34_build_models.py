#!/usr/bin/env python3
"""C-9 T9-1a: build each prop with the T6 winner (Tripo H3.1 multiview on fal).

Same endpoint and arguments as nb_t8/04_tripo_model.py, which built the barbarian -- the
props he stands among are made by the method he was made by, which is the whole of R-C9-71.

THE ORDER IS THE TRAP. The sheets are laid out front, right, back, left, reading left to
right, because that is how a model sheet is read. Tripo wants front, LEFT, back, RIGHT. The
reorder happens here and only here; a model built from a swapped pair comes back looking
entirely plausible and mirrored, which is not a thing that shows up in a screenshot.

    python3 12_build_models.py [object ...]     # default: all five
"""
import json
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
OBJECTS = ["stone_tall","stone_mid","lintel","post","rock_large","rock_small","birch","stone_short","juniper"]
TRIPO_ORDER = ["front", "left", "back", "right"]      # NOT the sheet order


def main() -> int:
    import fal_client
    (HERE / "builds").mkdir(exist_ok=True)
    want = sys.argv[1:] or OBJECTS
    picks = json.loads((HERE / "choose_props.json").read_text())["picks"]
    for obj in want:
        glb = HERE / "builds" / ("%s.glb" % obj)
        if glb.exists():
            print("%-6s already built (%.1f MB)" % (obj, glb.stat().st_size / 1e6))
            continue
        urls = [fal_client.upload_file(str(HERE / "placed" / ("%s_%s.jpg" % (obj, n))))
                for n in TRIPO_ORDER]
        t0 = time.time()
        r = fal_client.subscribe("tripo3d/h3.1/multiview-to-3d", arguments={
            "image_urls": urls, "texture": True, "pbr": False,
            "texture_quality": "detailed"})
        el = round(time.time() - t0, 1)
        url = (r.get("model_mesh") or {}).get("url") or next(
            (x.get("url") for x in r.values()
             if isinstance(x, dict) and str(x.get("url", "")).endswith(".glb")), None)
        if not url:
            print("%-6s NO MESH in result: %s" % (obj, list(r)))
            continue
        subprocess.run(["curl", "-s", "-L", "-o", str(glb), url], check=True)
        (HERE / "builds" / ("%s.json" % obj)).write_text(json.dumps({
            "endpoint": "tripo3d/h3.1/multiview-to-3d", "variant": picks[obj]["variant"],
            "view_order_sent": TRIPO_ORDER, "elapsed_s": el, "result": r}, indent=1) + "\n")
        print("%-6s built in %ss -> %s (%.1f MB)" % (obj, el, glb.name, glb.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
