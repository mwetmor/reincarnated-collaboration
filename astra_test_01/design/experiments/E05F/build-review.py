from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
p=Path(__file__).resolve().parent;r=json.loads((p/'evidence/batch-01/validation.json').read_text());contact=json.loads((p/'evidence/batch-02/runtime-contact.json').read_text());videos=json.loads((p/'evidence/batch-02/playback-validation.json').read_text())['videos'];probes=[]
for v in videos:
 f=p/'evidence/batch-02'/f"{v['clip']}-{v['outfit']}.webm";q=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));probes.append({'path':str(f.relative_to(p)),'width':q['streams'][0]['width'],'height':q['streams'][0]['height'],'duration_s':float(q['format']['duration'])})
(p/'evidence/batch-02/video-probe.json').write_text(json.dumps(probes,indent=2)+'\n')
html=['<!doctype html><html><meta charset="utf-8"><title>E05F · Fractional motion</title><style>body{background:#192128;color:#eee;font:16px system-ui;margin:32px}a{color:#9ed7ff}.pair{display:flex;gap:16px;overflow:auto}figure{margin:10px 0}img{max-width:100%;height:auto}video{width:960px;max-width:100%}code{color:#bde5d2}h2{margin-top:40px}</style><h1>E05F · Fractional source and runtime motion</h1><p>Godot is the shipping target; Pixi is the test harness.</p><p><b>Scoped PASS:</b> 312 fractional source checks, 864 rendered comparisons, exact 216 integer palettes and all three recorded walk contacts. No final art, full animation state machine, lighting or suite completion claim.</p><p>Original Bézier source and E05E failures remain unchanged. This separate source copy changes only interpolation; all 76,650 key times and values are preserved. The manifest describes raw local channels, normalized quaternion interpolation, bone hierarchy and source hashes without renderer types.</p><p>Maximum render MAE 0.00907; fraction of pixels over 8 error 0.000964. Shift and wrong-pose controls fail as expected. <b>Normal ablation is insensitive</b> under this chamber light policy; it is not evidence that correction data can be removed.</p><p>Recorded walk contact drift: starter 0.354 mm; advanced/head 0.380 mm; advanced/hair 0.507 mm. Continuous timing control 0.506 mm; old quantized-pose control 32.668 mm fails the 20 mm limit.</p><p><a href="REPORT.md">Report</a> · <a href="motion.asset.json">Neutral motion manifest</a> · <a href="evidence/batch-01/validation.json">All raster measurements and hashes</a> · <a href="evidence/batch-02/runtime-contact.json">Actual playback contact</a></p>']
for pose,outfit in [('walk-012_5','advanced-head'),('cast-036_5','advanced-hair'),('idle-024_5','starter')]:
 for res in [1,3]:
  html.append(f'<h2>{pose} · {outfit} · '+('native raster'if res==1 else 'fresh 3× raster, not enlarged native pixels')+'</h2><div class="pair">')
  for mode in ['skin','oracle']:
   name=f'r{res}-{pose}-h135-{outfit}-warm-{mode}.png';html.append(f'<figure><figcaption>{mode} · heading 135° · warm light · {400*res} × {380*res} pixels</figcaption><a href="evidence/batch-01/{name}"><img src="evidence/batch-01/{name}" width="{400*res}"></a></figure>')
  html.append('</div>')
html.append('<h2>Normal-speed chamber playback</h2><p>Full native 960 × 640 recording, continuous root motion. The partition correctly occludes the later walk; gameplay cutaway/outline remains a separate visibility test. Character floor/contact shadows have not yet been carried onto this source.</p>')
for v in videos:
 name=f"{v['clip']}-{v['outfit']}";html.append(f'<h3>{name}</h3><video controls loop preload="metadata" src="evidence/batch-02/{name}.webm"></video>')
html.append('<h2>Retained negative controls</h2>')
for bad in ['shift','wrong-pose','normals']:
 html.append(f'<h3>{bad}</h3><div class="pair">')
 for mode in ['skin','oracle']:html.append(f'<figure><figcaption>{mode} · native raster</figcaption><img src="evidence/batch-01/r1-control-{bad}-{mode}.png" width="400"></figure>')
 html.append('</div>')
html.append('<h2>Next action</h2><p>E07B: carry the previously bounded floor-shadow method onto the current fractional pilot and reprove source-derived shadow witnesses, changed pose/outfit/root and stale/missing controls. Full start/stop/steering, cloth, roster, richer faction architecture, reusable VFX, actual combat binding and hardware scale remain open.</p></html>');(p/'review.html').write_text('\n'.join(html))
