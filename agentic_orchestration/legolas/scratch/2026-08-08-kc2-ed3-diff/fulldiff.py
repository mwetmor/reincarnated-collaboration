#!/usr/bin/env python3
"""FULL record-level II->III diff across all 84,663 shared records. READ-ONLY."""
import sys, json, time, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-08-kc2-ed3-diff")
import lib2
t0 = time.time()
i2, i3 = lib2.E2.idx, lib2.E3.idx
shared = sorted(set(i2) & set(i3))
onlyIII = sorted(set(i3) - set(i2))
onlyII  = sorted(set(i2) - set(i3))
changed, ident, detail = [], 0, {}
bucket = collections.Counter()
for n, p in enumerate(shared):
    v, d = lib2.diff_rec(p)
    if v.startswith("IDENTICAL"):
        ident += 1
    else:
        changed.append(p); detail[p] = d
        bucket[p.split("/")[1] if "/" in p else "?"] += 1
    if n % 10000 == 0:
        print(f"  {n}/{len(shared)}  changed={len(changed)}  {time.time()-t0:.0f}s", flush=True)
print(f"DONE {time.time()-t0:.0f}s")
print(f"shared={len(shared)} IDENTICAL={ident} CHANGED={len(changed)} onlyIII={len(onlyIII)} onlyII={len(onlyII)}")
print("changed by top-level dir:", dict(bucket.most_common(30)))
json.dump({"changed": changed, "onlyIII": onlyIII, "onlyII": onlyII,
           "counts": {"shared": len(shared), "identical": ident, "changed": len(changed)}},
          open("fulldiff_summary.json","w"), indent=1)
json.dump({k: {kk: (vv if kk != "changed" else {a: [str(b[0])[:200], str(b[1])[:200]] for a,b in vv.items()})
               for kk, vv in v.items()} for k, v in detail.items()},
          open("fulldiff_detail.json","w"), indent=1, default=str)
print("written")
