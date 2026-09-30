#!/usr/bin/env python3
"""C-9 T10-1b: build each scatter-kit prop with Tripo H3.1 multiview on fal (the T6 winner).

Same endpoint and arguments as 34_build_models.py, which built the barrow's stones and the
barbarian's T8 body. The kit is made by the method the scene is made by.

THE ORDER IS THE TRAP AND IT HAS NOT CHANGED. The sheets read front, right, back, left,
left-to-right, because that is how a model sheet is read. Tripo wants front, LEFT, back,
RIGHT. A build from a swapped pair comes back plausible and MIRRORED, which no screenshot
shows. The reorder happens here and only here.

    python3 53_kit_build.py [object ...]     # default: all six
"""
import json
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fal_ledger  # noqa: E402

SETS = {"kit": ("kit_work", ["rocks", "stump", "log", "cairn", "skull", "shield"]),
        "kit2": ("kit_work2", ["rocks", "stump", "skull", "boulder"]),
        "kit3": ("kit_work3", ["outcrop_a", "outcrop_b", "heather_clump", "dead_tree"])}
TRIPO_ORDER = ["front", "left", "back", "right"]      # NOT the sheet order
EP = "tripo3d/h3.1/multiview-to-3d"


def main() -> int:
    import fal_client
    args = sys.argv[1:]
    setname = args[0] if args and args[0] in SETS else "kit"
    WORK, OBJECTS = HERE / SETS[setname][0], SETS[setname][1]
    (WORK / "builds").mkdir(exist_ok=True)
    want = [a for a in args if a not in SETS] or OBJECTS
    picks = json.loads((WORK / "choose_kit.json").read_text())["picks"]
    for obj in want:
        glb = WORK / "builds" / ("%s.glb" % obj)
        if glb.exists():
            print("%-7s already built (%.1f MB)" % (obj, glb.stat().st_size / 1e6))
            continue
        # THE GUARD RUNS BEFORE THE UPLOAD, not after the build: a refusal here costs
        # nothing, and a refusal after the call is a report, not a stop.
        before = fal_ledger.check(EP)
        urls = [fal_client.upload_file(str(WORK / "placed" / ("%s_%s.jpg" % (obj, n))))
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
            print("%-7s NO MESH in result: %s" % (obj, list(r)))
            continue
        run_total = fal_ledger.record(EP, "%s build %s" % (setname, obj))
        subprocess.run(["curl", "-s", "-L", "-o", str(glb), url], check=True)
        (WORK / "builds" / ("%s.json" % obj)).write_text(json.dumps({
            "endpoint": "tripo3d/h3.1/multiview-to-3d", "variant": picks[obj]["variant"],
            "view_order_sent": TRIPO_ORDER, "elapsed_s": el, "result": r}, indent=1) + "\n")
        print("%-13s built in %ss -> %s (%.1f MB)   fal running $%.4f -> $%.4f"
              % (obj, el, glb.name, glb.stat().st_size / 1e6, before, run_total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
