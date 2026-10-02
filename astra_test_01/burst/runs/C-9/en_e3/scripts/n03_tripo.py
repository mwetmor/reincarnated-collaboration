# Tripo H3.1 multiview on the four cut-outs -- T8's call, unchanged, through the
# D7 ledger. Order [front, left, back, right], as T8 and the T6 bake-off.
#
#   FAL_KEY=... python3 scripts/s3_tripo.py <tag> <out.glb> <what>
#
# The wait is timed on its own and handed to timer.py, so the step's AGENT time
# is wall minus a measured vendor queue rather than a guess.
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.environ.setdefault("FAL_LEDGER", os.path.join(ROOT, "fal_spend_R-C9-132.json"))
os.environ.setdefault("FAL_BUDGET", "3.00")
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "t10_barrow"))
import fal_ledger as FL
import fal_client
tag, out, what = sys.argv[1], sys.argv[2], sys.argv[3]
step = sys.argv[4] if len(sys.argv) > 4 else "S3-tripo-base"
EP = "tripo3d/h3.1/multiview-to-3d"
print("ledger %s, running $%.2f of $%.2f" % (os.path.basename(FL.LEDGER), FL.total(), FL.BUDGET))
FL.check(EP)
u = {n: fal_client.upload_file(os.path.join(ROOT, "work", "cv_%s_%s.jpg" % (tag, n)))
     for n in ("front", "left", "back", "right")}
t0 = time.time()
r = fal_client.subscribe(EP, arguments=dict(
    image_urls=[u["front"], u["left"], u["back"], u["right"]],
    texture=True, pbr=False, texture_quality="detailed"))
wait = time.time() - t0
run = FL.record(EP, what, wait)
url = (r.get("model_mesh") or {}).get("url") or next(
    (x.get("url") for x in r.values() if isinstance(x, dict)
     and str(x.get("url", "")).endswith(".glb")), None)
subprocess.run(["curl", "-s", "-L", "-o", out, url], check=True)
json.dump(dict(endpoint=EP, wait_s=round(wait, 1), result=r),
          open(os.path.join(ROOT, "work", "tripo_%s.json" % os.path.basename(out)), "w"), indent=1)
subprocess.run([sys.executable, os.path.join(HERE, "timer.py"), "wait", step,
                str(round(wait, 1)), "--what", "tripo queue+build"])
print("done: %.0f s at the vendor, %.2f MB, ledger now $%.2f"
      % (wait, os.path.getsize(out) / 1e6, run))
