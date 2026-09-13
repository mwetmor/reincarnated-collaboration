"""Run once explicitly: real K3p-xv-cut-04 packet and decode comparison.

This is deliberately outside unittest discovery. Decoded frames stay in memory.
Only the named Desktop video is searched/read; no Desktop metadata or other
assets are used. When unavailable, compare to a Pillow Lanczos source render.
"""
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import time

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gates.g6_seam import evaluate, g6c
from review.cell_packet import build_packet, validate_packet_html
from test_encode import decode, probe


def result(name, value, threshold, unit, notes='', op='<=', evidence=None):
    return {'id': name, 'subject': 'walk/E', 'passed': None, 'value': value,
            'threshold': threshold, 'op': op, 'unit': unit, 'evidence': evidence or [],
            'notes': 'Acceptance measurement; conductor owns verdict. '+notes}


def main():
    started = time.monotonic()
    out = ROOT/'runs/C-3/t3/T3d'; out.mkdir(parents=True, exist_ok=True)
    cell = ROOT/'runs/C-1/artifacts/K3p-xv-cut-04'
    frames = sorted((cell/'frames/walk/E').glob('*.png'))
    checks = evaluate(frames, 'walk/E') + [g6c(frames, 'walk/E')]
    (out/'checks_walk_E.json').write_text(json.dumps(checks, indent=2, allow_nan=False)+'\n')
    packet = out/'packet_walk_E'
    built = build_packet(cell, checks, packet)
    video = packet/'walk_E_2x.mp4'
    new = decode(video, 1)[0]
    desktop = Path.home()/'Desktop/Astra Burst Review - 2026-09-12'
    reference = None
    notes = []
    try:
        matches = sorted(desktop.rglob('walk_E_12fps.mp4'))
    except OSError as exc:
        matches = []; notes.append(type(exc).__name__+': '+str(exc))
    # Prefer packet 18 if multiple exact-name copies exist.
    matches.sort(key=lambda p: (not any('18' in part for part in p.relative_to(desktop).parts[:-1]), str(p)))
    for candidate in matches:
        try:
            reference = decode(candidate, 1)[0]
            reference_path = str(candidate)
            mode = 'desktop_decode'
            break
        except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
            notes.append(type(exc).__name__+': '+str(exc))
    if reference is None:
        with Image.open(frames[0]) as im:
            source = im.convert('RGBA')
        background = Image.new('RGBA', source.size, '#3a3f4a')
        background.alpha_composite(source)
        reference = np.asarray(background.convert('RGB').resize((1024, 1024), Image.Resampling.LANCZOS))
        reference_path = str(frames[0])
        mode = 'pil_lanczos_fallback'
        notes.append('Named Desktop video not readable/found; SPEC fallback used.')
    matching_shape = new.shape == reference.shape
    mad = float(np.abs(new.astype(np.float32)-reference.astype(np.float32)).mean()) if matching_shape else None
    refs = validate_packet_html(packet/'review.html')
    info = probe(video)
    metrics = [result('decode_frame0_mad', mad, 3, 'rgb_levels', mode+'; full-canvas RGB MAD; no alignment or crop', evidence=['packet_walk_E/walk_E_2x.mp4']),
               result('packet_wall', built['wall_s'], 120, 'seconds'),
               result('external_or_missing_html_references', 0, 0, 'references', f'{len(refs)} references checked', op='=='),
               result('summary_lines', len((packet/'summary.txt').read_text().splitlines()), 12, 'lines')]
    report = {'task_id': 'T3d', 'results': metrics, 'reference_mode': mode,
              'reference_path': reference_path, 'reference_notes': notes,
              'decoded_shape': list(new.shape), 'reference_shape': list(reference.shape),
              'source_frame_sha256': hashlib.sha256(frames[0].read_bytes()).hexdigest(),
              'video': {k: info.get(k) for k in ('codec_name', 'codec_tag_string', 'pix_fmt', 'width', 'height', 'r_frame_rate', 'nb_frames', 'duration')},
              'packet': built, 'wall_s': time.monotonic()-started,
              'decoded_temporaries_on_disk': 0}
    (out/'acceptance.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
