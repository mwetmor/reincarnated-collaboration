"""Real-clip T3a measurements, intentionally separate from run_t0c.py.

Run from the frozen tree with ``python3 -B tests/acceptance_t3a.py``.
Reports measurements in the shared envelope with passed=null: conductor rules.
Decoded temporaries are deleted even if an instrument raises an exception.
"""
import gc
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import traceback
import unittest

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from oracle import video_cut as vc

OUT = ROOT/'runs/C-3/t3/T3a-1'
EXPECTED_WALK = [71,74,77,79,82,85,88,91,94,97,99,102]


def quantity(name, subject, value, threshold, op, unit, notes=''):
    return dict(id=name,subject=subject,passed=None,value=value,threshold=threshold,
                op=op,unit=unit,evidence=[],notes='Measurement only; conductor criterion. '+notes)


def strip(frames, indices, path):
    result = Image.new('RGB',(512*len(frames),536),(58,63,74))
    draw = ImageDraw.Draw(result)
    for i,(frame,native) in enumerate(zip(frames,indices)):
        result.paste(frame,(512*i,24),frame)
        draw.text((512*i+8,6),f'{i:02d} / native {native}',fill=(240,240,240))
    result.save(path)


def measure(kind, filename, count):
    begin = time.perf_counter()
    clip = ROOT/'runs/C-1/xvideo/in'/filename
    record = dict(kind=kind,clip=str(clip),clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),
                  t_max_s=4.4,output_n=count,results=[],stage_seconds={})
    with tempfile.TemporaryDirectory(dir=OUT/'tmp',prefix=kind+'_') as temporary:
        tick = time.perf_counter()
        # Decode the whole six-second source for performance and splice evidence.
        # Period uses the supplied full series; t_max_s constrains selection only.
        meta = vc.split(clip,Path(temporary)/'decoded',t_max_s=6.1)
        record['stage_seconds']['split'] = time.perf_counter()-tick
        record['source'] = {k:v for k,v in meta.items() if k!='paths'}
        tick = time.perf_counter(); rgba = vc.matte_frames(meta['paths'])
        record['stage_seconds']['matte'] = time.perf_counter()-tick
        record['matte_notes'] = dict(frames=len(rgba),first=rgba.notes[0],last=rgba.notes[-1])
        tick = time.perf_counter(); series = vc.track(rgba)
        series['indices_native'] = meta['indices_native']; series['times'] = meta['times']
        record['stage_seconds']['track'] = time.perf_counter()-tick
        record['series'] = dict(series)
        tick = time.perf_counter(); period = vc.detect_period(kind,series,meta['fps'])
        record['stage_seconds']['period'] = time.perf_counter()-tick
        record['period'] = period; record['period_estimation_frames'] = len(rgba)
        tick = time.perf_counter(); splice = vc.splice_check(rgba); series['splice'] = splice
        record['stage_seconds']['splice'] = time.perf_counter()-tick
        record['splice'] = splice
        tick = time.perf_counter()
        selection = vc.select_cycle(kind,series,period,meta['fps'],4.4)
        record['stage_seconds']['select'] = time.perf_counter()-tick
        record['selection'] = selection
        if selection['start'] is None:
            raise ValueError('no eligible real-clip cycle: '+selection['reason'])
        indices = vc.resample(selection['start'],selection['end_exclusive'],count)
        record['indices_native'] = indices
        record['output_times_native_s'] = [i/meta['fps'] for i in indices]
        tick = time.perf_counter()
        registered, transform = vc.register([rgba[i] for i in indices]+[rgba[0]])
        record['stage_seconds']['register'] = time.perf_counter()-tick
        record['transform'] = transform
        record['rest'] = dict(native_index=0,same_transform=True,
            bbox=vc._bbox(vc._mask(registered[-1])))
        record['pipeline_seconds'] = time.perf_counter()-begin
        strip_path = OUT/(kind+'_strip.png')
        strip(registered[:-1],indices,strip_path)
        record['strip'] = str(strip_path)
        record['results'] += [
            quantity('end_to_end_wall',kind,record['pipeline_seconds'],180,'<=','seconds',
                     'Whole 145-frame source through registered loop and rest; excludes strip encoding and cleanup.'),
            quantity('anchor_height_error',kind,abs(transform['anchor_H']-240),1,'<=','px'),
            quantity('anchor_sole_row',kind,transform['anchor_sole_row'],399,'==','px'),
            quantity('anchor_center_x',kind,transform['anchor_cx'],255.5,'==','px'),
            quantity('single_transform',kind,transform['one_transform_for_every_frame'],True,'==','boolean')]
        if kind == 'walk':
            errors = [abs(a-b) for a,b in zip(indices,EXPECTED_WALK)]
            record['expected_indices_native'] = EXPECTED_WALK
            record['indices_abs_error'] = errors
            record['results'] += [
                quantity('selected_window',kind,[selection['start'],selection['end_exclusive']],
                         [71,105],'==','native_frames'),
                quantity('maximum_native_index_error',kind,max(errors),1,'<=','native_frames')]
        else:
            record['results'] += [quantity('window_length',kind,
                selection['end_exclusive']-selection['start'],48,'==','native_frames'),
                quantity('period_source_reported',kind,period['source'] is not None,True,'==','boolean')]
        del rgba,series,registered
    gc.collect()
    record['total_seconds_including_strip_cleanup'] = time.perf_counter()-begin
    return record


class Acceptance(unittest.TestCase):
    def test_real_clips_report(self):
        OUT.mkdir(parents=True,exist_ok=True); (OUT/'tmp').mkdir(exist_ok=True)
        report = dict(task_id='T3a-1',tool_sha256=hashlib.sha256(Path(vc.__file__).read_bytes()).hexdigest(),
                      notes=['Real sources are 768x1168 at 24fps, not 720p.',
                             'All 145 source frames decoded/matted/tracked for each performance measurement.',
                             'Period evidence uses the full supplied series; selection uses t<4.4s.',
                             'Idle C-2 used a 98-frame whole breath; this contract requires a 48-frame window.',
                             'No G6/G6b shipping decision is made.'],clips=[])
        for kind,filename,count in [('walk','walk_E_grok.mp4',12),('idle','idle_C_grok.mp4',16)]:
            started = time.perf_counter()
            try:
                record = measure(kind,filename,count)
            except Exception as exc:
                record = dict(kind=kind,error=str(exc),traceback=traceback.format_exc(),
                              total_seconds=time.perf_counter()-started)
            report['clips'].append(record)
            (OUT/'acceptance.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
            print('T3A_REAL '+json.dumps({k:v for k,v in record.items()
                if k in ('kind','period','indices_native','pipeline_seconds','results','error','total_seconds_including_strip_cleanup')},allow_nan=False),flush=True)
        self.assertEqual(len(report['clips']),2)
        self.assertFalse(any('error' in r for r in report['clips']),
                         'instrument execution errors are recorded in acceptance.json')


if __name__ == '__main__':
    unittest.main()
