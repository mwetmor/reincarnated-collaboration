"""Reproducible production-probe alpha regression. No GPU required by default.

python3 -B tests/probe_t4d_flipbook.py [--render] [--out DIR]
Default headless probe verifies Godot loads actual external RGBA paths and
creates all cached textures. --render runs the production replay's real viewport
capture over black, white and a coloured ground; expected = source-over pixels.
Run --render outside the sandbox if the platform cannot expose its GL renderer.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from export.replay import install_hooks,run_replay


def probe(out, render=False):
    started = time.monotonic()
    out = Path(out).resolve()
    project = out/'project';project.mkdir(parents=True,exist_ok=False)
    (project/'scripts').mkdir()
    (project/'scenes').mkdir()
    (project/'project.godot').write_text('''config_version=5
[application]
config/name="T4d flipbook alpha probe"
run/main_scene="res://scenes/main.tscn"
[display]
window/size/viewport_width=64
window/size/viewport_height=64
[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
environment/defaults/default_clear_color=Color(0,0,0,1)
''')
    (project/'scenes/main.tscn').write_text('''[gd_scene format=3]
[node name="World" type="Node2D"]
[node name="Ground" type="Polygon2D" parent="."]
polygon = PackedVector2Array(0,0,64,0,64,64,0,64)
color = Color(0.1254901961,0.2509803922,0.5019607843,1)
''')
    (project/'scenes/effect.tscn').write_text('[gd_scene format=3]\n[node name="Effect" type="Node2D"]\n')
    install_hooks(project,(64,64))
    frames = out/'external_rgba';frames.mkdir()
    rgba = np.full((64,64,4),[255,255,255,0],np.uint8)
    rgba[8:24,8:24] = [240,40,20,255]
    rgba[32:48,32:48] = [20,200,60,128]
    for index in range(3): Image.fromarray(rgba).save(frames/f'fx{index:08d}.png')
    reports = {}
    backgrounds = {'ground':(32,64,128),'black':(0,0,0),'white':(255,255,255)}
    for background,colour in backgrounds.items():
        result = run_replay(project,out/background,effect='res://scenes/effect.tscn',
                            frame=1,frames=3,crop=(64,64),origin=(32,32),bake=False,
                            background=background,flipbook=frames,probe_only=not render,timeout=30)
        report_path = out/background/'probe.json'
        observed = json.loads(report_path.read_text()) if report_path.exists() else {}
        entry = {'returncode':result['returncode'],'engine_errors':result['engine_errors'],
                 'loaded_textures':observed.get('flipbook_loaded'), 'wall_s':result['wall_s']}
        if render and (out/background/'capture.png').exists():
            actual = np.array(Image.open(out/background/'capture.png').convert('RGB')).astype(float)
            alpha = rgba[...,3:4]/255.
            expected = np.rint(rgba[...,:3]*alpha+np.array(colour)*(1-alpha))
            entry.update(max_channel_error=float(np.abs(actual-expected).max()),
                         mean_channel_error=float(np.abs(actual-expected).mean()),
                         nonwhite_pixels=int(np.any(actual != 255,axis=-1).sum()),
                         clear_region_max_error=float(np.abs(actual[:8]-np.array(colour)).max()),
                         capture_sha256=hashlib.sha256((out/background/'capture.png').read_bytes()).hexdigest())
        reports[background] = entry
    result = {'rendered':render,'grounds':reports,'criterion_max_channel_error':2,
              'criterion_cached_textures':3,'wall_s':time.monotonic()-started}
    (out/'alpha_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--out',type=Path,default=ROOT/'runs/C-5/t3/T4d/flipbook_probe')
    args = parser.parse_args()
    result = probe(args.out,args.render)
    print(json.dumps(result,indent=2))
    good = all(r['returncode']==0 and not r['engine_errors'] and r['loaded_textures']==3
               and (not args.render or (r.get('max_channel_error',999)<=2 and r.get('nonwhite_pixels',0)>0))
               for r in result['grounds'].values())
    raise SystemExit(0 if good else 1)
