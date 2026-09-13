"""Measure exemplar-centred proposals without committing or editing old bands.

Missing and categorical quantities are retained in `unmeasured`/`diagnostics`,
not fabricated as zero. W2 extrema are numeric normalized frame positions;
phase-match truth is not a scalar motion amplitude. No shipping verdicts.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from gates.common import result
from gates import gait_intent, idle_intent
from gates.g6_seam import g6c
from oracle.idle_curves import curves
from oracle.motion_map import alpha_box, frame_paths

ROOT = Path(__file__).resolve().parents[1]
FACINGS = ('S','SW','W','NW','N','NE','E','SE')


def frame_digest(frames_dir):
    """SHA256 of ASCII hex frame hashes concatenated in natural frame order."""
    hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in frame_paths(frames_dir)]
    return hashlib.sha256(''.join(hashes).encode('ascii')).hexdigest()


def measure(kind, frames_dir, fps):
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError('fps must be finite and positive')
    if kind == 'idle':
        # Exactly the curves(..., ours=True) path of idle_bands --ours.
        data = curves(frames_dir, alpha_box(frames_dir), fps, ours=True)
        seed = dict(committed=False,provenance=dict(fps=fps),
            breath_amplitude_H={},head_sway_H={})
        intent = idle_intent.evaluate(frames_dir,seed,'exemplar')['value']
        values = {k:data['summary'][k] for k in ('breath_amplitude_H','head_sway_H')}
        # A static crop is explicitly zero in idle_intent, rather than missing.
        values['breath_amplitude_H'] = intent['breath']['value']
        values['head_sway_H'] = intent['head_bob']['value']
        values.update({name+'_displacement_H':v['displacement_H'] for name,v in intent['regions'].items()})
        diagnostic = dict(summary=data['summary'],regions=intent['regions'],estimator=data['estimator'])
    elif kind == 'walk':
        seed = dict(committed=False,bands={'W1':{'floor':0.}})
        checks = gait_intent.evaluate(frames_dir,seed,[None]*12)
        by = {r['id']:r for r in checks}
        values = dict(W1=by['W1_floor']['value'],W3a=by['W3a']['value'],
                      W3c=by['W3c_floor']['value'],W4=by['W4']['value'],W6=by['W6']['value'])
        for name,r in by.items():
            if name.startswith(('W5_','planted_sole_slip_')):
                values[name] = r['value']
        # Frozen gait pipeline's W3b is descriptive, not exposed as a gate.
        images = []
        for path in frame_paths(frames_dir):
            with Image.open(path) as im: images.append(np.array(im.convert('RGBA')))
        masks = [gait_intent.figure_mask(a) for a in images]
        summary = gait_intent.measure_sequence(gait_intent.track_landmarks_otsu_stance_lineage(masks))['summary']
        values['W3b'] = summary['W3b']
        extrema = json.loads(by['W2']['notes'])['observed_extrema']
        for key in ('min','max'):
            values['W2_'+key+'_count'] = len(extrema[key])
            for i,p in enumerate(extrema[key]):
                values[f'W2_{key}_{i}_cycle_fraction'] = p['frame']/len(images)
        seam = g6c([Image.fromarray(a) for a in images],str(frames_dir))
        seam['passed'] = None
        values['G6c'] = seam['value']
        diagnostic = dict(gait_checks=checks,W2=extrema,G6c=seam,
                          W2_note='phase labels unresolved; extrema frame positions / cycle length are numeric proposals')
    else:
        raise ValueError('kind must be idle or walk')
    return values, diagnostic


def propose(kind, frames_dir, label, fps, facing=None):
    if facing is not None and facing not in FACINGS:
        raise ValueError('invalid facing')
    values, diagnostic = measure(kind,frames_dir,fps)
    quantities, missing = {}, {}
    for name,value in values.items():
        if value is None or isinstance(value,bool) or not np.isfinite(value):
            missing[name] = dict(value=None,reason='frozen estimator unresolved; no numeric band fabricated')
        else:
            v = float(value)
            quantities[name] = dict(value=v,target=v,floor=.6*v,ceiling=1.5*v)
    return dict(proposed=True,committed=False,label=label,kind=kind,facing=facing,fps=float(fps),
        proposed_from=dict(frames_dir=str(Path(frames_dir).resolve()),sha256_of_sorted_frame_hashes=frame_digest(frames_dir)),
        hash_convention='SHA256(concatenated ASCII SHA256 hex digests in natural numbered frame order)',
        quantities=quantities,unmeasured=missing,diagnostics=diagnostic,
        governing_quantity='W1' if facing in ('E','W') and kind=='walk' else 'W3' if kind=='walk' else 'breath_amplitude_H',
        notes='R-45: idle exemplar covers the whole selected span; not evidence of a verified single breath cycle.' if kind=='idle' else 'Exemplar-centred proposal; no committed shipping gate.')


def score(values, row, subject='exemplar'):
    checks = []
    for name, band in row['quantities'].items():
        value = values.get(name)
        inside = None if value is None else bool(band['floor'] <= value <= band['ceiling'])
        r = result(name,subject,value=value,passed=None,unit='quantity_native_units',
                   notes=json.dumps(dict(inside=inside,proposed=True,committed=False)))
        r.update(threshold={k:band[k] for k in ('floor','target','ceiling')},op='report')
        checks.append(r)
    return checks


def facing_rows(east_row, committed_walk_rows):
    west = deepcopy(east_row)
    west.update(label='walk_W_video',facing='W',notes='E profile measurement reused for W bands only; no mirrored art or independent W evidence.')
    rows = {'walk_W_video':west}
    for facing,source in [('N','plate13_rear'),('S','plate13_front')]:
        row = deepcopy(committed_walk_rows[source])
        row.update(proposed=True,committed=False,proposed_from='muybridge',source_row=source,
                   facing=facing,governing_quantity='W3')
        rows['walk_'+facing+'_proposal'] = row
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind',choices=['idle','walk'],required=True)
    parser.add_argument('--frames',type=Path,required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--fps',type=float,required=True)
    parser.add_argument('--out',type=Path,default=Path('oracle/bands_proposed.json'))
    parser.add_argument('--facing',choices=FACINGS)
    args = parser.parse_args(argv)
    if args.out.resolve() in ((ROOT/'oracle/bands_idle.json').resolve(),(ROOT/'oracle/bands_walk.json').resolve()):
        parser.error('committed band files are read only')
    row = propose(args.kind,args.frames,args.label,args.fps,args.facing)
    rows = json.loads(args.out.read_text()) if args.out.exists() else {}
    rows[args.label] = row
    if args.label == 'walk_E_video' and args.facing=='E':
        rows.update(facing_rows(row,json.loads((ROOT/'oracle/bands_walk.json').read_text())))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(rows,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(dict(out=str(args.out),label=args.label,quantities=len(row['quantities']),unmeasured=row['unmeasured'])))
    return row


if __name__ == '__main__':
    main()
