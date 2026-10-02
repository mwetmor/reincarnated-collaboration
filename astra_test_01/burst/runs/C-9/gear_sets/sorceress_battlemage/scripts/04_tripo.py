# COPIED from so_d7/scripts (read-only there) for R-C9-98; patched: absolute t10_barrow path, R-C9-98 ledger required.
# D2: build each gear piece with Tripo H3.1 multiview -- the generator T6 chose
# and T8 confirmed on this character.
#
#   python3 scripts/04_tripo.py <tag>:<front>,<left>,<back>,<right> ...
#
# The three body sheets go in DRESSED: the piece is isolated afterwards by its
# distance from the base body, which needs the gear and the body to come from
# the same generator in the same pose. The two objects go in on their own.
import concurrent.futures as cf
import json, os, subprocess, sys, time
import fal_client
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = 'tripo3d/h3.1/multiview-to-3d'
# THROUGH THE LEDGER, CHECKED AS A BATCH. The inherited copy paid for every
# build without a spend total seeing it. And because these run CONCURRENTLY, a
# per-build check() would race: five threads can each read the same running
# total and each conclude there is room. So the whole batch is checked once,
# up front, against n x the build price; each build is recorded as it lands.
assert os.environ.get("FAL_LEDGER","").endswith(("fal_spend_R-C9-98.json", "fal_spend_R-C9-119.json", "fal_spend_R-C9-134.json")), "set FAL_LEDGER (R-C9-98, R-C9-119 or R-C9-134)"
os.environ.setdefault("FAL_BUDGET", "3.00")
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/t10_barrow")
import fal_ledger as FL
jobs = []
for spec in sys.argv[1:]:
    tag, views = spec.split(":", 1)
    jobs.append((tag, views.split(",")))
_need = len(jobs) * FL.PRICE[EP]
if FL.total() + _need > FL.BUDGET + 1e-9:
    raise SystemExit("FAL BUDGET STOP: running $%.4f + %d builds x $%.2f = $%.4f exceeds "
                     "$%.2f. Nothing submitted." % (FL.total(), len(jobs), FL.PRICE[EP],
                                                    FL.total() + _need, FL.BUDGET))
print("ledger $%.4f + %d builds x $%.2f = $%.4f of $%.2f"
      % (FL.total(), len(jobs), FL.PRICE[EP], FL.total() + _need, FL.BUDGET), flush=True)


def run(j):
    tag, paths = j
    t0 = time.time()
    try:
        urls = [fal_client.upload_file(os.path.join(ROOT, p)) for p in paths]
        h = fal_client.submit(EP, arguments={
            'image_urls': urls, 'texture': True, 'pbr': False,
            'texture_quality': 'detailed'})
        res = h.get()
        el = time.time() - t0
        FL.record(EP, "R-C9-98 build %s" % tag, el)
        out = dict(tag=tag, endpoint=EP, views=paths, request_id=h.request_id,
                   elapsed_s=round(el, 1), result=res)
        url = (res.get('model_mesh') or {}).get('url') or res.get('model_url')
        if url:
            dst = os.path.join(ROOT, "builds", "%s.glb" % tag)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            subprocess.run(['curl', '-s', '-L', '-o', dst, url], check=True)
            out['glb'] = dst
            out['glb_mb'] = round(os.path.getsize(dst) / 1e6, 1)
        print("%-8s %6.1fs  %s" % (tag, el, out.get('glb_mb', 'NO GLB')), flush=True)
    except Exception as e:
        out = dict(tag=tag, error=str(e)[:400], elapsed_s=round(time.time() - t0, 1))
        print("%-8s ERROR %s" % (tag, str(e)[:160]), flush=True)
    json.dump(out, open(os.path.join(ROOT, "work", "tripo_%s.json" % tag), "w"), indent=1)
    return out


with cf.ThreadPoolExecutor(max_workers=5) as ex:
    res = list(ex.map(run, jobs))
tot = sum(r.get('elapsed_s', 0) for r in res)
print("%d builds, %.0f s wall-sum, est $%.2f at $0.40 each" % (len(res), tot, 0.40 * len(res)))
