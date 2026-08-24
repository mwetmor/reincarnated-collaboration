"""Read the full HP trace off eor-test-1 (the sibling, 2498.37 s) with the validated reader.
Memoised on the ROI mask so long constant-HP stretches cost one classification."""
import numpy as np, csv, sys, time
from d4_ocr import stream, mask_of, FPS
from d4_reader import read
V1='/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-1/video/eor-warlord-2026-08-04 21-09-31.mp4'
cache={}
out=[]; t0=time.time()
for i,img in stream(V1):
    key=mask_of(img).tobytes()
    v=cache.get(key,'MISS')
    if v=='MISS':
        v=read(img); cache[key]=v
        if len(cache)>400000: cache.clear()
    out.append((i, v))
    if i%30000==0:
        ok=sum(1 for _,x in out if x)
        print(f'  frame {i} t={i/FPS:8.1f}s  read {ok}/{len(out)}  cache {len(cache)}  {time.time()-t0:.0f}s', flush=True)
with open('d4_sibling_hp_trace.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['frame','t_s','hp_cur','hp_max'])
    for i,v in out:
        w.writerow([i, f'{i/FPS:.4f}', v[0] if v else '', v[1] if v else ''])
ok=sum(1 for _,x in out if x)
print(f'DONE frames={len(out)} read={ok} ({100*ok/len(out):.2f}%) elapsed={time.time()-t0:.0f}s')
