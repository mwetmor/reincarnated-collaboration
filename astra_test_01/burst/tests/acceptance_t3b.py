"""Real T3b measurement, run separately from run_t0c.py; no gate verdicts.

Decode only the 16 frozen native indices. Report native and registered values
separately; registered frames use the original K3p shared isotropic transform.
Large decoded temporaries are removed even if a measurement raises.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gates.matte_quality import alpha_area, direct_luminance_fringe, rim_luma_excess
from oracle.video_cut import matte_frames

OUT = ROOT/'runs/C-3/t3/T3b'
CLIP = ROOT/'runs/C-1/xvideo/in/idle_C_grok.mp4'
REGISTRATION = ROOT/'runs/C-1/artifacts/K3p-xv-idle-cut-01/registration.json'
BG = (58, 63, 74)
MODES = ('unpremultiply', 'clamp')


def registered(frame, transform):
    scale = transform['scale']
    if not 0 < scale <= 1:
        raise ValueError('Registration must downscale uniformly')
    resized = frame.transform(tuple(transform['scaled_canvas_size']), Image.Transform.AFFINE,
                              (1/scale, 0, 0, 0, 1/scale, 0), Image.Resampling.BICUBIC)
    canvas = Image.new('RGBA', tuple(transform['canvas']))
    canvas.paste(resized, tuple(transform['integer_translation_xy']))
    return canvas


def measurements(frame):
    return dict(rim_luma_excess=rim_luma_excess(frame, BG), alpha_area=alpha_area(frame),
                direct_luminance_fringe=direct_luminance_fringe(frame, frame, BG))


def summary(rows, stage):
    result = {}
    for mode in MODES:
        values = [row[stage][mode]['rim_luma_excess']['value'] for row in rows]
        valid = [v for v in values if v is not None]
        result[mode] = dict(mean=float(np.mean(valid)) if valid else None,
                            minimum=min(valid) if valid else None, maximum=max(valid) if valid else None,
                            evaluable_frames=len(valid), total_frames=len(rows))
    old_area = sum(row[stage]['unpremultiply']['alpha_area']['value'] for row in rows)
    new_area = sum(row[stage]['clamp']['alpha_area']['value'] for row in rows)
    result['alpha_area'] = dict(unpremultiply=old_area, clamp=new_area,
                                lost_percent=100*(old_area-new_area)/old_area if old_area else None,
                                byte_identical_all_frames=all(row[stage]['alpha_byte_identical'] for row in rows))
    result['criteria'] = [
        dict(id='matte_quality.rim_luma_excess', subject=stage+'/unpremultiply', passed=None,
             value=result['unpremultiply']['mean'], threshold=5, op='>', unit='luma_0_255',
             evidence=['edge_crops.png'], notes='Known-bad reproduction; mean of 16 per-frame measurements; conductor evaluates.'),
        dict(id='matte_quality.rim_luma_excess', subject=stage+'/clamp', passed=None,
             value=result['clamp']['mean'], threshold=5, op='<=', unit='luma_0_255',
             evidence=['edge_crops.png'], notes='Mean of 16 per-frame measurements; ranges also reported; conductor evaluates.'),
        dict(id='matte_quality.alpha_area_lost', subject=stage, passed=None,
             value=result['alpha_area']['lost_percent'], threshold=1, op='<=', unit='percent',
             evidence=[], notes='Integrated alpha area; expected zero; conductor evaluates.')]
    return result


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    tmp_root = OUT/'tmp'
    tmp_root.mkdir(exist_ok=True)
    registration = json.loads(REGISTRATION.read_text())
    indices = [frame['native_index'] for frame in registration['frames']]
    if len(indices) != 16 or indices != sorted(set(indices)):
        raise ValueError('Expected 16 ordered unique frozen native indices')
    transform = registration['transform']
    timings = {}
    rows = []
    crops = Image.new('RGB', (512, 16*280), BG)
    draw = ImageDraw.Draw(crops)
    with tempfile.TemporaryDirectory(dir=tmp_root) as temp:
        temp = Path(temp)
        expression = '+'.join('eq(n,%d)' % i for i in indices)
        stage_start = time.monotonic()
        subprocess.run(['/opt/homebrew/bin/ffmpeg', '-v', 'error', '-i', str(CLIP),
                        '-vf', "select='"+expression+"'", '-fps_mode', 'passthrough',
                        '-frames:v', str(len(indices)), '-start_number', '0',
                        str(temp/'frame_%02d.png')], check=True, capture_output=True)
        paths = sorted(temp.glob('frame_*.png'))
        if len(paths) != len(indices):
            raise ValueError('Decoded count differs from frozen index count')
        timings['decode_s'] = time.monotonic()-stage_start
        for ordinal, (index, path) in enumerate(zip(indices, paths)):
            row = dict(frame=ordinal, native_index=index, native={}, registered={})
            native = {}
            output = {}
            for mode in MODES:
                stage_start = time.monotonic()
                frames = matte_frames([path], alpha_floor=40, edge_mode=mode)
                native[mode] = frames[0]
                row.setdefault('matte_notes', {})[mode] = frames.notes[0]
                timings[mode+'_matte_s'] = timings.get(mode+'_matte_s', 0)+time.monotonic()-stage_start
                output[mode] = registered(native[mode], transform)
                row['native'][mode] = measurements(native[mode])
                row['registered'][mode] = measurements(output[mode])
            for stage, images in (('native', native), ('registered', output)):
                row[stage]['alpha_byte_identical'] = bool(np.array_equal(
                    np.asarray(images['unpremultiply'])[..., 3], np.asarray(images['clamp'])[..., 3]))
            # Fixed anatomical-height crop rule, identical coordinates in both modes.
            mask = np.asarray(output['unpremultiply'])[..., 3] >= 128
            ys, xs = np.where(mask)
            cy = int(ys.min()+.30*(ys.max()-ys.min()+1))
            row_x = np.flatnonzero(mask[cy])
            cx = int(row_x.min()) if len(row_x) else int(xs.min())
            box = (cx-32, cy-32, cx+32, cy+32)
            row['registered_edge_crop_xyxy'] = list(box)
            for column, mode in enumerate(MODES):
                composite = Image.new('RGBA', output[mode].size, BG+(255,))
                composite.alpha_composite(output[mode])
                crop = composite.convert('RGB').crop(box).resize((256, 256), Image.Resampling.NEAREST)
                crops.paste(crop, (column*256, ordinal*280+24))
                draw.text((column*256+4, ordinal*280+5), f'native {index}: {mode} x4', fill=(220, 225, 235))
            rows.append(row)
    crops.save(OUT/'edge_crops.png')
    timings['total_s'] = time.monotonic()-started
    result = dict(task_id='T3b', indices_native=indices, alpha_floor=40,
                  background_rgb=list(BG), luma='Rec.709 display RGB, 0..255',
                  ring='Opaque pixels at Euclidean distance 1..3 from partial-alpha band',
                  aggregation='Arithmetic mean of all 16 per-frame values; native and registered reported separately',
                  transform=transform, frames=rows,
                  summary={stage: summary(rows, stage) for stage in ('native', 'registered')},
                  timings=timings, decoded_temporaries_removed=True,
                  source_sha256={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in (CLIP, REGISTRATION)},
                  notes=['No acceptance verdicts; thresholds are reported for the conductor.',
                         'direct_luminance_fringe was absent from the permitted pre-T3b modules; added with explicit untrimmed reference.',
                         'Original K3p affine bicubic registration is replayed with one scale and translation for every frame and both modes.'])
    (OUT/'matte_edge_acceptance.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(summary=result['summary'], timings=timings), indent=2))


if __name__ == '__main__':
    main()
