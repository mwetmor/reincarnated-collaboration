"""Run once: real run_03 VFX reports, known-bad copies, and socket MP4.

Run from burst: PYTHONDONTWRITEBYTECODE=1 python3 -B tests/acceptance_t3e.py
All persistent outputs are beneath runs/C-3/t3/T3e. No decoded temp frames.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gates.element_hue import evaluate as element_hue
from gates.vfx_lifecycle import evaluate as lifecycle, sequence_pse
from review.composite_socket import composite, estimate_sockets

OUT = ROOT/'runs/C-3/t3/T3e'
VFX = ROOT.parent/'run_03/vfx/frames'
CHARACTER = ROOT/'runs/C-1/artifacts/K3p-xv-cut-04/frames/walk/E'
FFPROBE = '/opt/homebrew/bin/ffprobe'


def read_frames(folder):
    paths = sorted(folder.glob('*.png'))
    frames = []
    for path in paths:
        with Image.open(path) as im:
            frames.append(np.array(im))
    return paths, frames


def digest(paths):
    return [dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]


def fire_copy(frames):
    """Rotate hue by 180 degrees on a Pillow 256-step hue circle; keep alpha."""
    output = []
    for a in frames:
        hsv = np.array(Image.fromarray(a[..., :3]).convert('HSV'))
        hsv[..., 0] = ((hsv[..., 0].astype(int)+128) % 256).astype(np.uint8)
        rgb = np.array(Image.fromarray(hsv, mode='HSV').convert('RGB'))
        output.append(np.dstack([rgb, a[..., 3]]))
    return output


def main():
    start = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    report = dict(task_id='T3e', modules={}, known_bad={},
                  checkpoint_scope='run_03 certifies counts/style/alpha and zero impact residual; composite browser playback unverified. No lifecycle/seam/symmetry certification.',
                  criteria=dict(counts={'cast': 8, 'travel': 6, 'impact': 10}, cast_fps=20,
                                energy='one interior peak; monotone rise and release',
                                impact_final_alpha_fraction_max=.005,
                                frost_hue_degrees=[180, 230],
                                travel_g6='seam MAD <= minimum internal MAD',
                                travel_g6b='seam MAD <= median internal MAD; second instrument only',
                                symmetry='report only: no committed threshold',
                                attachment_max_px=6,
                                pse_max_flashes_per_second=3,
                                composite='MP4 builds; no browser verification criterion'))
    real = {}
    for module in ('cast', 'travel', 'impact'):
        tick = time.perf_counter()
        paths, frames = read_frames(VFX/module); real[module] = frames
        results = lifecycle(module, frames, 20)
        results.append(element_hue(frames, 'frost'))
        report['modules'][module] = dict(inputs=digest(paths), results=results,
                                         elapsed_s=time.perf_counter()-tick)
    # These stay in memory, preserving source art and requiring no file cleanup.
    for module, frames in real.items():
        rotated = fire_copy(frames)
        report['known_bad'][module+'_fire_rotation'] = dict(
            frost=element_hue(rotated, 'frost'), fire=element_hue(rotated, 'fire'),
            pse=sequence_pse(rotated, 20, module+'.fire_rotation', loop=module == 'travel'))
    opaque = [a.copy() for a in real['impact']]
    opaque[-1][..., 3] = 255
    report['known_bad']['impact_opaque_tail'] = dict(results=lifecycle('impact', opaque, 20),
                                                    mutation='Last frame alpha set to 255 over the full canvas')
    paths, characters = read_frames(CHARACTER)
    estimate = estimate_sockets(characters)
    # Fix the socket once, at the median registered staff-tip proxy. Do not
    # re-fit to flare centroids, and do not assert anatomical attachment.
    socket = np.median(np.asarray(estimate['xy_per_frame']), axis=0).tolist()
    tick = time.perf_counter()
    comp = composite(characters, real['cast'], socket, OUT/'composite', 20)
    elapsed = time.perf_counter()-tick
    probe = subprocess.run([FFPROBE, '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                            '-show_entries', 'stream=codec_name,pix_fmt,width,height,r_frame_rate,nb_read_frames,duration',
                            '-of', 'json', comp['mp4']], capture_output=True, text=True, timeout=60, check=True)
    report['composite'] = dict(inputs=digest(paths), fixed_socket_xy=socket,
                               socket_estimate=estimate, report=comp,
                               elapsed_s=elapsed, ffprobe=json.loads(probe.stdout),
                               mp4_sha256=hashlib.sha256(Path(comp['mp4']).read_bytes()).hexdigest())
    report['elapsed_s'] = time.perf_counter()-start
    (OUT/'acceptance.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    compact = dict(elapsed_s=report['elapsed_s'], composite_elapsed_s=elapsed,
                   fixed_socket_xy=socket, ffprobe=report['composite']['ffprobe'],
                   modules={m: [{k:r[k] for k in ('id', 'value', 'threshold', 'passed')}
                                for r in row['results']] for m,row in report['modules'].items()},
                   attachment={k:comp['attachment'][k] for k in ('value', 'threshold', 'passed')},
                   composite_pse={k: {n:r[n] for n in ('value', 'threshold', 'passed')}
                                  for k,r in comp['pse'].items()},
                   known_bad={m: {'frost_hue':r['frost']['value'], 'frost_passed':r['frost']['passed'],
                                  'fire_hue':r['fire']['value'], 'fire_passed':r['fire']['passed']}
                              for m,r in report['known_bad'].items() if 'frost' in r})
    print(json.dumps(compact, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
