#!/usr/bin/env python3
"""C-9 image bake-off (R-C9-79): two variants per job from Nano Banana and Nano Banana Pro.

    python3 02_generate.py [J1 J2 J3 J4]

ENDPOINTS, verified through fal's pricing API before the first call (2026-09-29):
    fal-ai/nano-banana/edit       $0.0398 per image
    fal-ai/nano-banana-pro/edit   $0.15   per image   (1K and 2K; 4K is billed double)
The /edit endpoints for every job, because every Astra brief in this study carried reference
images -- at least the style hand -- and the generate endpoints take none. Sending the
candidates to the text-only endpoint would test them without an input Astra had.

SAME CALL SHAPE FOR BOTH: one image per call, the job's aspect, PNG; Pro at 2K (the largest
size at the base price -- 1K would hand it LESS resolution than Astra's 1536 px and 4K would
double its bill). Two separate calls per variant rather than num_images=2, so every image
has its OWN seconds: "seconds per image" is then a measurement, not a division.

THE STOP IS A RESERVATION, NOT A READ. The four calls of a job run concurrently, and four
threads each reading the ledger total and then spending would each see the same total. So
under one lock a call reserves its list price against total + everything in flight, and only
then goes; it records when it returns. The ledger is fal_ledger.py's, under this study's
own file and its $5.00 budget (FAL_LEDGER / FAL_BUDGET set below).
"""
import json
import os
import pathlib
import subprocess
import sys
import threading
import time

HERE = pathlib.Path(__file__).resolve().parent
os.environ["FAL_LEDGER"] = str(HERE / "fal_spend_R-C9-79.json")
os.environ["FAL_BUDGET"] = "5.00"
os.environ["FAL_LEDGER_NOTE"] = ("gandalf's $5.00 hard stop for the image bake-off (R-C9-79), "
                                 "including its one Tripo build; starts at $0 for this study.")
sys.path.insert(0, str(HERE.parent / "t10_barrow"))
import fal_ledger  # noqa: E402

CANDS = {"nb": "fal-ai/nano-banana/edit", "nbp": "fal-ai/nano-banana-pro/edit"}
LOCK = threading.Lock()
INFLIGHT = [0.0]


def reserve(ep):
    with LOCK:
        price = fal_ledger.PRICE[ep]
        t = fal_ledger.total()
        if t + INFLIGHT[0] + price > fal_ledger.BUDGET + 1e-9:
            return None, t
        INFLIGHT[0] += price
        return price, t


def call(job, cand, v, prompt, urls, aspect, out_dir, results):
    import fal_client
    ep = CANDS[cand]
    dst = out_dir / ("%s_%s_%s.png" % (job, cand, v))
    if dst.exists():
        results.append({"file": dst.name, "skipped": "exists"})
        return
    price, t = reserve(ep)
    if price is None:
        print("   %s %s %s REFUSED: running $%.4f + in-flight would exceed $%.2f"
              % (job, cand, v, t, fal_ledger.BUDGET), flush=True)
        results.append({"file": dst.name, "refused": True})
        return
    args = {"prompt": prompt, "image_urls": urls, "num_images": 1,
            "aspect_ratio": aspect, "output_format": "png"}
    if cand == "nbp":
        args["resolution"] = "2K"
    t0 = time.time()
    try:
        r = fal_client.subscribe(ep, arguments=args)
        sec = time.time() - t0
    except Exception as e:                       # a failed request produces no image
        with LOCK:
            INFLIGHT[0] -= price
        print("   %s %s %s FAILED after %.1f s: %s" % (job, cand, v, time.time() - t0, e), flush=True)
        results.append({"file": dst.name, "failed": str(e)[:300], "seconds": round(time.time() - t0, 1)})
        return
    with LOCK:
        INFLIGHT[0] -= price
        run = fal_ledger.record(ep, "%s %s %s" % (job, cand, v), sec)   # price AND seconds
    imgs = r.get("images") or []
    if not imgs:
        results.append({"file": dst.name, "no_image": True, "seconds": round(sec, 1),
                        "description": r.get("description")})
        print("   %s %s %s NO IMAGE (%.1f s) %s" % (job, cand, v, sec, str(r)[:200]), flush=True)
        return
    subprocess.run(["curl", "-s", "-L", "-o", str(dst), imgs[0]["url"]], check=True)
    results.append({"file": dst.name, "endpoint": ep, "seconds": round(sec, 1), "usd": price,
                    "width": imgs[0].get("width"), "height": imgs[0].get("height"),
                    "description": r.get("description"), "args": {k: v_ for k, v_ in args.items()
                                                                  if k not in ("prompt", "image_urls")}})
    print("   %s %-3s %s  %5.1f s  $%.4f  -> %s   fal running $%.4f"
          % (job, cand, v, sec, price, dst.name, run), flush=True)


def main() -> int:
    import fal_client
    prompts = json.loads((HERE / "prompts" / "prompts.json").read_text())
    want = sys.argv[1:] or ["J1", "J2", "J3", "J4"]
    out_dir = HERE / "out"
    out_dir.mkdir(exist_ok=True)
    log = HERE / "generate_log.json"
    allres = json.loads(log.read_text()) if log.exists() else {}
    for job in want:
        p = prompts[job]
        prompt = (HERE / "prompts" / ("%s.txt" % job)).read_text()
        urls = [fal_client.upload_file(path) for path in p["images_in_order"]]   # uploads are free
        print("%s: %d reference image(s) uploaded, aspect %s" % (job, len(urls), p["aspect_ratio"]), flush=True)
        results, threads = [], []
        for cand in CANDS:
            for v in ("a", "b"):
                th = threading.Thread(target=call, args=(job, cand, v, prompt, urls,
                                                         p["aspect_ratio"], out_dir, results))
                th.start()
                threads.append(th)
        for th in threads:
            th.join()
        allres.setdefault(job, [])
        allres[job] = [x for x in allres[job] if x["file"] not in {y["file"] for y in results}] + results
        log.write_text(json.dumps(allres, indent=1, ensure_ascii=False) + "\n")
    print("fal running $%.4f of $%.2f" % (fal_ledger.total(), fal_ledger.BUDGET))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
