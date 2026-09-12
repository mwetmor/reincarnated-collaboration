"""Harness ONLY: prompts are authored/frozen by the conductor at HITL.

freeze validates the set and reference hashes, then hashes exact manifest bytes.
No generation and no invented production prompts. distance matches PNG relative
paths exactly and reports O5 aligned silhouette, O1 Lab-histogram and O8 source-
normalised spectral-profile distances. Alarm threshold is a NAMED parameter;
passed is null until calibrated on K1. Every drift alarm requires revalidation
of MODEL-COUPLED matte instruments. Constant foreground has a zero O8 profile.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from bible.validate import validate
from oracles.common import image_array,report
from oracles.silhouette64 import distance as silhouette_distance
from oracles.sheet_consistency import palette_histogram
from oracles.grain import band_energy


def freeze(probe_set_path):
    path=Path(probe_set_path);raw=path.read_bytes();data=json.loads(raw)
    schema=json.loads((Path(__file__).with_name('probe_set.schema.json')).read_text())
    errors=validate(data,schema)
    if errors:raise ValueError('Invalid probe set: '+'; '.join(errors))
    ids=[p['id'] for p in data['probes']]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate probe id')
    for probe in data['probes']:
        if not probe['prompt'].strip():raise ValueError('Empty conductor prompt')
        for ref in probe['references']:
            target=Path(ref['path']).expanduser()
            if not target.is_absolute():target=path.parent/target
            if hashlib.sha256(target.read_bytes()).hexdigest()!=ref['sha256']:
                raise ValueError('Probe reference hash mismatch: '+ref['path'])
    return hashlib.sha256(raw).hexdigest()


def _profile(a):
    row=band_energy(a,a[...,3],[a.shape[1],a.shape[0]])
    notes=json.loads(row['notes'])
    if notes['reason']=='No spectral energy':return np.zeros(32)
    if 'profile' not in notes['metrics']:raise ValueError(notes['reason'] or 'O8 profile unavailable')
    return np.asarray(notes['metrics']['profile'])


def distance(probe_outputs_dir,approved_dir,*,alarm_threshold=None,subject=''):
    if alarm_threshold is not None and (not np.isfinite(alarm_threshold) or alarm_threshold<0):
        raise ValueError('Alarm threshold must be nonnegative')
    def listing(root):
        root=Path(root)
        if not root.is_dir():raise ValueError('Probe directory missing')
        return {str(p.relative_to(root)):p for p in root.rglob('*.png') if p.is_file()}
    try:
        candidates=listing(probe_outputs_dir);approved=listing(approved_dir)
        if not approved or set(candidates)!=set(approved):
            return report('model_drift_probe',subject,None,alarm_threshold,
                metrics={'missing':sorted(set(approved)-set(candidates)),
                         'extra':sorted(set(candidates)-set(approved))},reason='Probe sets must be nonempty and match exactly')
        probes=[]
        for name in sorted(approved):
            a=image_array(candidates[name]);b=image_array(approved[name])
            if a.shape!=b.shape:raise ValueError('Probe canvas differs: '+name)
            values=dict(O5=float(silhouette_distance(a,b)),
                        O1=float(np.linalg.norm(palette_histogram(a)-palette_histogram(b))),
                        O8=float(np.linalg.norm(_profile(a)-_profile(b))))
            probes.append(dict(probe=name,**values,aggregate=float(np.mean(list(values.values())))))
    except (ValueError,OSError) as exc:
        return report('model_drift_probe',subject,None,alarm_threshold,reason=str(exc))
    aggregate={k:float(np.mean([p[k] for p in probes])) for k in ('O5','O1','O8')}
    maximum=max(p['aggregate'] for p in probes)
    return report('model_drift_probe',subject,maximum,alarm_threshold,unit='max_probe_mean_distance',
        metrics=dict(per_probe=probes,aggregate=aggregate,mean_distance=float(np.mean([p['aggregate'] for p in probes])),
                     max_distance=maximum,calibration_set='K1; not yet calibrated'),
        reason='Alarm threshold awaits K1 calibration; conductor authors probe prompts at HITL' if alarm_threshold is None else '')
