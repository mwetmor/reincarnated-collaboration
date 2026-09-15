"""T4d field, event timing, attachment and FF-08 interval instruments.

All clocks are effect-age frames at 60 Hz; no wall-clock substitution. Signed
lags are observed minus stamped (positive is late). No tolerance/acceptance
band was specified for these reports, so §1 passed/threshold are always null.
Missing samples/events are unevaluable, never silently measured as zero.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from oracle.vfx_measure import _row


def _points(value, name):
    a = np.asarray(value, dtype=float)
    if a.size == 0:
        return np.empty((0, 2))
    if a.ndim != 2 or a.shape[1] != 2 or not np.all(np.isfinite(a)):
        raise ValueError(name+' must contain finite xy pairs')
    return a


def _frame(value):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < 0:
        raise ValueError('frame must be a nonnegative integer')
    return int(value)


def _stamp(event):
    # Native G1 events.json uses effect_id / age_frames. The concise frame key
    # is also accepted for synthetic traces, but conflicting clocks are invalid.
    value = event.get('age_frames', event.get('frame'))
    if 'age_frames' in event and 'frame' in event and event['age_frames'] != event['frame']:
        raise ValueError('conflicting event frame and age_frames')
    return _frame(value)


def _cast(row):
    value = row.get('effect_id', row.get('cast_id', 0))
    if 'effect_id' in row and 'cast_id' in row and row['effect_id'] != row['cast_id']:
        raise ValueError('conflicting effect_id and cast_id')
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('effect_id/cast_id must be a string or integer')
    return value


def _report(ident, value, unit, notes='', subject='effect'):
    return _row(ident, subject, value, unit, notes or 'Measurement only; no committed tolerance.', [])


def field_boundary(boundary_xy, centre_xy, radius_px):
    """Compare supplied observed boundary points with the authored circle."""
    points = _points(boundary_xy, 'boundary_xy')
    centre = _points([centre_xy], 'centre_xy')[0]
    if isinstance(radius_px, bool) or not math.isfinite(radius_px) or radius_px <= 0:
        raise ValueError('radius_px must be positive and finite')
    delta = np.linalg.norm(points-centre, axis=1)-radius_px
    return _report('field_boundary', dict(radius_px=float(radius_px), samples=len(points),
                   signed_error_px=delta.tolist(),
                   max_abs_error_px=float(np.max(np.abs(delta))) if len(delta) else None,
                   mean_abs_error_px=float(np.mean(np.abs(delta))) if len(delta) else None),
                   'pixels', 'No observed boundary.' if not len(points) else '')


def activation_expiry(trace, events, activation_event='contact', expiry_event='expire'):
    """Trace rows {frame, active}; event rows {event, frame} for ONE cast.

    Activation is the first observed active sample. Expiry is the first inactive
    sample after the final active sample; a clip cut while active is censored.
    Sampling gaps are exposed, and missing preceding samples leave the onset's
    exact transition unproven. Multiple stamps of a chosen event are ambiguous.
    """
    frames = [_frame(row['frame']) for row in trace]
    if any(b <= a for a, b in zip(frames, frames[1:])):
        raise ValueError('trace frames must strictly increase')
    if any(type(row['active']) is not bool for row in trace):
        raise ValueError('trace active must be boolean')
    active_indices = [i for i, row in enumerate(trace) if row['active']]
    activation = frames[active_indices[0]] if active_indices else None
    tail = active_indices[-1]+1 if active_indices else len(trace)
    expiry = frames[tail] if tail < len(trace) else None
    rows = []
    for label, event_name, observed in [('activation', activation_event, activation),
                                         ('expiry', expiry_event, expiry)]:
        stamps = [_stamp(e) for e in events if e.get('event') == event_name]
        stamped = stamps[0] if len(stamps) == 1 else None
        lag = observed-stamped if observed is not None and stamped is not None else None
        reason = ('No visible transition sample.' if observed is None else
                  'Missing or ambiguous event stamp.' if stamped is None else '')
        rows.append(_report(label+'_lag', dict(observed_frame=observed, event=event_name,
                            stamped_frame=stamped, lag_frames=lag,
                            lag_ms=lag*1000/60 if lag is not None else None,
                            event_matches=len(stamps),
                            sample_gaps=[[a,b] for a,b in zip(frames, frames[1:]) if b-a > 1]),
                            'frames', reason))
    return rows


def aura_attachment(aura_xy, attachment_xy, offset_xy=(0, 0)):
    """Pointwise drift after subtracting the declared constant socket offset."""
    aura, socket = _points(aura_xy, 'aura_xy'), _points(attachment_xy, 'attachment_xy')
    offset = _points([offset_xy], 'offset_xy')[0]
    if aura.shape != socket.shape:
        raise ValueError('aura and attachment samples must pair one-to-one')
    errors = np.linalg.norm(aura-socket-offset, axis=1)
    return _report('aura_attachment_drift', dict(per_sample_px=errors.tolist(),
                   max_px=float(errors.max()) if len(errors) else None,
                   mean_px=float(errors.mean()) if len(errors) else None,
                   offset_xy=offset.tolist()), 'pixels', 'No paired positions.' if not len(errors) else '')


def interval_cv(event_frames):
    """FF-08: population SD / mean interval; >=2 intervals (3 stamps)."""
    frames = [_frame(f) for f in event_frames]
    if any(b <= a for a,b in zip(frames, frames[1:])):
        raise ValueError('event frames must strictly increase (no duplicate stamps)')
    intervals = np.diff(frames)
    enough = len(intervals) >= 2
    mean = float(intervals.mean()) if len(intervals) else None
    sd = float(intervals.std(ddof=0)) if enough else None
    return _report('FF-08_interval_cv', dict(intervals_frames=intervals.tolist(),
                   mean_frames=mean, population_sd_frames=sd,
                   cv=sd/mean if enough else None, ddof=0), 'coefficient_of_variation',
                   '' if enough else 'At least three stamps required to measure interval variation.')


def evaluate(trace, events, radius_px=None, centre_xy=(0, 0), aura_offset_xy=(0, 0),
             activation_event='contact', expiry_event='expire', interval_event='contact'):
    """Report per-cast timing/geometry and intervals within each cast.

    Optional trace keys: boundary_xy, aura_xy, attachment_xy; both inputs accept
    effect_id or cast_id (default 0). Native stamps use age_frames; synthetic
    stamps may use frame. An events.json object may wrap rows in ``events``.
    """
    if isinstance(events, (str, Path)):
        events = json.loads(Path(events).read_text())
    if isinstance(events, dict):
        events = events['events']
    casts = list(dict.fromkeys([_cast(r) for r in trace]+[_cast(e) for e in events]))
    output = []
    for cast in casts:
        samples = [r for r in trace if _cast(r) == cast]
        stamps = [e for e in events if _cast(e) == cast]
        rows = activation_expiry(samples, stamps, activation_event, expiry_event)
        if radius_px is not None:
            for sample in samples:
                if 'boundary_xy' in sample:
                    row = field_boundary(sample['boundary_xy'], sample.get('centre_xy', centre_xy), radius_px)
                    row['frame'] = sample['frame']; rows.append(row)
        pairs = [s for s in samples if 'aura_xy' in s and 'attachment_xy' in s]
        rows.append(aura_attachment([s['aura_xy'] for s in pairs], [s['attachment_xy'] for s in pairs], aura_offset_xy))
        rows.append(interval_cv([_stamp(e) for e in stamps if e.get('event') == interval_event]))
        for row in rows:
            row['subject'] = 'cast/'+str(cast)
        output.extend(rows)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace', type=Path)
    parser.add_argument('events', type=Path)
    parser.add_argument('--radius-px', type=float)
    parser.add_argument('--centre-xy', type=float, nargs=2, default=(0,0))
    args = parser.parse_args(argv)
    print(json.dumps(evaluate(json.loads(args.trace.read_text()), args.events,
                             args.radius_px, args.centre_xy), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
