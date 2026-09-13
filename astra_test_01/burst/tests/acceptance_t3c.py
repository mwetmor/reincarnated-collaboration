"""T3c real acceptance measurements; run separately from unittest discovery.

Upright rest = native 71, the pre-registered head-up window opening. Native
frame zero is additionally reported as a sensitivity check, never silently
substituted. No threshold is calibrated from these window means.
"""
import json
from pathlib import Path
import sys
import tempfile
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from oracle.bands_from_exemplar import main as proposal_cli, measure, score
from oracle.video_cut import split, matte_frames, track
from gates.head_pitch import evaluate as head_pitch
from gates.coherence import evaluate as coherence

OUT=ROOT/'runs/C-3/t3/T3c'


def window(rows,start,stop):
    values=[r['delta'] for r in rows[start:stop] if r['delta'] is not None]
    return dict(start=start,end_exclusive=stop,n=len(values),
                missing=stop-start-len(values),mean_delta=float(np.mean(values)) if values else None)


def main():
    begin=time.perf_counter();OUT.mkdir(parents=True,exist_ok=True)
    record=dict(task_id='T3c',passed=None,stage_seconds={},self_consistency={},head_pitch=None)
    proposed=ROOT/'oracle/bands_proposed.json'
    cells=[('idle','idle_relaxed_video','S',8,ROOT/'runs/C-1/artifacts/K3p-xv-idle-cut-01/frames/idle/S'),
           ('walk','walk_E_video','E',12,ROOT/'runs/C-1/artifacts/K3p-xv-cut-04/frames/walk/E')]
    for kind,label,facing,fps,frames in cells:
        tick=time.perf_counter()
        row=proposal_cli(['--kind',kind,'--frames',str(frames),'--label',label,'--fps',str(fps),
                          '--out',str(proposed),'--facing',facing])
        # Re-measure, not read-back of stored target as the measured value.
        values,_=measure(kind,frames,fps)
        checks=score(values,row,label)
        table=[dict(quantity=r['id'],value=r['value'],**r['threshold'],
                    inside=json.loads(r['notes'])['inside'],passed=r['passed']) for r in checks]
        record['self_consistency'][label]=dict(table=table,defined=len(table),
            inside_count=sum(r['inside'] is True for r in table),unmeasured=row['unmeasured'],results=checks)
        record['stage_seconds'][label]=time.perf_counter()-tick
    tick=time.perf_counter()
    record['coherence']=coherence(cells[0][-1],None)
    record['stage_seconds']['idle_coherence']=time.perf_counter()-tick
    temporary=OUT/'tmp';temporary.mkdir(exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=temporary,prefix='native_') as temp:
            clip=ROOT/'runs/C-1/xvideo/in/walk_E_grok.mp4'
            tick=time.perf_counter();meta=split(clip,Path(temp)/'frames',t_max_s=4.4)
            record['stage_seconds']['split']=time.perf_counter()-tick
            tick=time.perf_counter();frames=matte_frames(meta['paths'],edge_mode='clamp')
            record['stage_seconds']['matte']=time.perf_counter()-tick
            tick=time.perf_counter();series=track(frames)
            record['stage_seconds']['track']=time.perf_counter()-tick
            tick=time.perf_counter()
            report=head_pitch(frames,frames[71],times=meta['times'])
            control=head_pitch(frames,frames[0],times=meta['times'])
            record['stage_seconds']['head_pitch']=time.perf_counter()-tick
            rows=report['value']['frames'];down=window(rows,0,71);up=window(rows,71,105)
            difference=down['mean_delta']-up['mean_delta'] if down['n'] and up['n'] else None
            record['head_pitch']=dict(result=report,rest_native_index=71,
                rest_reason='R-51 head-up window opening; explicit upright baseline',
                windows=[down,up],mean_difference=difference,criterion='mean_difference > 0',
                first_second_head_down=report['value']['first_second_head_down'],
                first_second_mean_delta=report['value']['first_second_mean_delta'],
                threshold=report['threshold'],
                frame_zero_rest_sensitivity=dict(windows=[window(control['value']['frames'],0,71),window(control['value']['frames'],71,105)],
                    first_second_head_down=control['value']['first_second_head_down'],
                    first_second_mean_delta=control['value']['first_second_mean_delta']),
                source=dict(clip=str(clip),fps=meta['fps'],n=meta['n'],times=meta['times'],
                            head_top_y=series['head_top_y'],working_scale=series['working_scale']))
    finally:
        temporary.rmdir()
    record['wall_seconds']=time.perf_counter()-begin
    (OUT/'acceptance.json').write_text(json.dumps(record,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(dict(self_consistency={k:{a:v[a] for a in ('defined','inside_count','unmeasured')} for k,v in record['self_consistency'].items()},
        head_pitch={k:v for k,v in record['head_pitch'].items() if k not in ('result','source')},
        stage_seconds=record['stage_seconds'],wall_seconds=record['wall_seconds']),allow_nan=False))


if __name__=='__main__': main()
