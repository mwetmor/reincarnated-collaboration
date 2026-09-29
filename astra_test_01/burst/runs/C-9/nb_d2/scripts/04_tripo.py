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
jobs = []
for spec in sys.argv[1:]:
    tag, views = spec.split(":", 1)
    jobs.append((tag, views.split(",")))


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
