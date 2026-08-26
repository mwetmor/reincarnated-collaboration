"""Cut the MEASURED impact frame from every leg, and a fx-context strip.

Uses out/series_<row>.json (spec_mass peak) rather than a guessed seek time --
the first contact sheet was cut at a flat 62% of duration and was unreadable
for identification. The instrument already knows which frame carries the event.
"""
import json, os, subprocess, sys, glob
MAP = {}
for line in open('run_ta.py'):
    line = line.strip()
    if line.startswith('("') and line.endswith('),'):
        parts = line.split('"')
        MAP[parts[1]] = parts[3]
os.makedirs('sheet2', exist_ok=True)
rows = []
for sp in sorted(glob.glob('out/series_*.json')):
    row = os.path.basename(sp)[len('series_'):-len('.json')]
    S = json.load(open(sp))
    sm = [float(x) for x in S['spec_mass']]
    i = max(range(len(sm)), key=lambda k: sm[k])
    idx = int(S['idx'][i]); t = float(S['t'][i])
    media = MAP.get(row)
    if not media: continue
    out = f'sheet2/{row}_t{t:.2f}.png'
    subprocess.run(['ffmpeg','-v','error','-nostdin','-ss',f'{t:.3f}','-i',media,
                    '-frames:v','1','-vf','scale=640:-2','-y',out], check=False)
    rows.append((row, t, idx, out))
    print(f'{row:24s} impact t={t:6.2f}s frame={idx:4d}')
json.dump(rows, open('out/impact_frames.json','w'), indent=2)
