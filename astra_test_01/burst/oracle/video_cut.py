"""C-3 loop instruments; no per-frame alignment, synthesis, or gate verdicts.

Coordinates are native pixels, measured at WORKING_SCALE. ``track`` accepts
alpha masks or RGBA images. Its JSON-serializable dict retains images in a
non-serialized ``frames`` attribute for RGB closure measurements. A reloaded
series must have that attribute restored (or supply a ``frames`` key).
After half-rate decoding, attach split's ``indices_native`` and ``times`` to
the series; fps arguments always mean the source/native fps. Periods, window
bounds and returned indices are native frame units, including at half rate.
Masks alone suffice for tracking/periods, but never fabricate RGB seam MAD.
"""
import inspect
import json
import math
from fractions import Fraction
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image
from scipy import ndimage, signal

from gates.matte import extract
from .idle_curves import period as autocorrelation_period
from .walk_landmarks import landmarks

FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'
WORKING_SCALE = 0.5
ALPHA_THRESHOLD = 128
PERIOD_CONFIDENCE = 0.3
DOWN_MIN_DISTANCE_B = 0.65
SPLICE_MEDIAN_MULTIPLIER = 4.0


class FrameSequence(list):
    """PIL frames with per-frame matte notes; list-compatible."""


class TrackedSeries(dict):
    """JSON data plus transient source images for exact RGB comparisons."""


def _positive(value, name):
    if isinstance(value, bool) or not np.isfinite(value) or value <= 0:
        raise ValueError(name + ' must be finite and positive')


def _integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(name + ' must be an integer >= ' + str(minimum))
    return int(value)


def split(clip, out_dir, t_max_s=4.4, half_rate=False):
    """Decode t < t_max_s to numbered PNGs, preserving source timestamps.

    The destination must contain no PNGs, avoiding stale frame contamination.
    Metadata fps is native; sample_fps describes the optional every-second cut.
    No synthesized duplicate frames or timestamp-based frame-rate conversion.
    """
    _positive(t_max_s, 't_max_s')
    out = Path(out_dir)
    if out.exists() and any(out.glob('*.png')):
        raise ValueError('out_dir already contains PNG frames')
    probe = subprocess.run([FFPROBE, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,avg_frame_rate,r_frame_rate:frame=best_effort_timestamp_time',
        '-of', 'json', str(clip)], check=True, capture_output=True, text=True)
    data = json.loads(probe.stdout)
    stream = data['streams'][0]
    rate = stream['avg_frame_rate']
    if rate == '0/0':
        rate = stream['r_frame_rate']
    fps = float(Fraction(rate))
    _positive(fps, 'fps')
    timestamps = [float(f['best_effort_timestamp_time']) for f in data['frames']]
    if not timestamps:
        raise ValueError('clip contains no decoded video frames')
    origin = timestamps[0]
    timestamps = [t-origin for t in timestamps]
    step = 2 if half_rate else 1
    indices = [i for i, t in enumerate(timestamps) if t < t_max_s and i % step == 0]
    if not indices:
        raise ValueError('empty decode interval')
    out.mkdir(parents=True, exist_ok=True)
    expression = f'lt(t,{t_max_s:.17g})'
    if half_rate:
        expression += '*not(mod(n,2))'
    subprocess.run([FFMPEG, '-v', 'error', '-i', str(clip), '-map', '0:v:0',
        '-vf', "setpts=PTS-STARTPTS,select='"+expression+"'", '-fps_mode', 'passthrough',
        '-frames:v', str(len(indices)), '-start_number', '0', '-compression_level', '1',
        str(out/'frame_%06d.png')], check=True, capture_output=True)
    paths = sorted(out.glob('frame_*.png'))
    if len(paths) != len(indices):
        raise ValueError('ffprobe/ffmpeg decoded frame counts disagree')
    return dict(fps=fps, sample_fps=fps/step, n=len(paths), w=int(stream['width']),
                h=int(stream['height']), times=[timestamps[i] for i in indices],
                indices_native=indices, paths=[str(p) for p in paths], half_rate=bool(half_rate))


def matte_frames(paths, alpha_floor=40, edge_mode='unpremultiply'):
    """Return RGBA PIL frames; ``.notes`` records ignored pre-T3b edge_mode."""
    if edge_mode not in ('unpremultiply', 'clamp'):
        raise ValueError('edge_mode must be unpremultiply or clamp')
    supports_edge = 'edge_mode' in inspect.signature(extract).parameters
    kwargs = dict(alpha_floor=alpha_floor)
    if supports_edge:
        kwargs['edge_mode'] = edge_mode
    frames = FrameSequence()
    frames.notes = []
    for path in paths:
        with Image.open(path) as image:
            frame, note = extract(image, **kwargs)
        note = dict(note, edge_mode_requested=edge_mode,
                    edge_mode_applied=edge_mode if supports_edge else 'unpremultiply')
        if not supports_edge:
            note['edge_mode_note'] = 'edge_mode ignored: frozen extract predates T3b'
        frames.append(frame)
        frames.notes.append(note)
    if not frames:
        raise ValueError('empty frame sequence')
    return frames


def _array(frame):
    a = np.asarray(frame)
    if a.ndim not in (2, 3) or (a.ndim == 3 and a.shape[2] not in (3, 4)):
        raise ValueError('expected a 2D mask or RGB/RGBA image')
    return a


def _mask(frame):
    a = _array(frame)
    if a.ndim == 3:
        if a.shape[2] != 4:
            raise ValueError('tracking requires alpha, not an opaque RGB image')
        a = a[..., 3]
    return a if a.dtype == bool else a >= ALPHA_THRESHOLD


def _bbox(mask):
    y, x = np.where(mask)
    if not len(x):
        raise ValueError('empty alpha support')
    return [int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)]


def track(masks):
    """Largest 8-connected alpha component; 3-frame median head-top only.

    Chest is the full row span at floor(.30 H); tip is the farthest upper
    .35 H mask point from the centroid of torso pixels in [.25 H,.60 H).
    Empty masks have null coordinates and explicit invalid indices.
    """
    inputs = list(masks)
    if not inputs:
        raise ValueError('empty mask sequence')
    shape = _mask(inputs[0]).shape
    h0, w0 = shape
    size = (max(1, int(w0*WORKING_SCALE)), max(1, int(h0*WORKING_SCALE)))
    sx, sy = size[0]/w0, size[1]/h0
    out = TrackedSeries({k: [] for k in ('head_top_y', 'head_cx', 'sole_y', 'H', 'bbox', 'chest_w', 'tip_xy', 'area')})
    out.update(working_scale=WORKING_SCALE, working_scale_xy=[sx, sy],
               coordinate_units='native_px', invalid_indices=[], n=len(inputs))
    out.frames = inputs if all(_array(f).ndim == 3 for f in inputs) else None
    for i, frame in enumerate(inputs):
        native = _mask(frame)
        if native.shape != shape:
            raise ValueError('mask dimensions differ')
        small = np.asarray(Image.fromarray(native).resize(size, Image.Resampling.NEAREST))
        labels, _ = ndimage.label(small, structure=np.ones((3, 3)))
        counts = np.bincount(labels.ravel()); counts[0] = 0
        if not counts.max():
            out['invalid_indices'].append(i)
            for k in ('head_top_y', 'head_cx', 'sole_y', 'H', 'bbox', 'chest_w', 'tip_xy', 'area'):
                out[k].append(None)
            continue
        m = labels == counts.argmax()
        lm = landmarks(m)
        x0, y0, x1, y1 = _bbox(m)
        height = y1-y0
        row = np.flatnonzero(m[min(y1-1, y0+int(.30*height))])
        ty, tx = np.where(m[y0+int(.25*height):y0+max(int(.25*height)+1,int(.60*height))])
        torso = (float(tx.mean()), float(ty.mean()+y0+int(.25*height))) if len(tx) else (lm['torso_cx'], y0+.425*height)
        uy, ux = np.where(m[y0:y0+max(1,int(math.ceil(.35*height)))])
        uy = uy+y0
        far = int(np.argmax((ux-torso[0])**2+(uy-torso[1])**2))
        values = dict(head_top_y=y0/sy, head_cx=(lm['head_cx']+.5)/sx-.5,
            sole_y=y1/sy-1, H=height/sy, bbox=[x0/sx,y0/sy,x1/sx,y1/sy],
            chest_w=(int(row[-1]-row[0]+1)/sx if len(row) else 0.),
            tip_xy=[float((ux[far]+.5)/sx-.5),float((uy[far]+.5)/sy-.5)],
            area=float(m.sum()/(sx*sy)))
        for k, v in values.items():
            out[k].append(v)
    raw = out['head_top_y'][:]
    out['head_top_y_raw'] = raw
    # Never interpolate across invalid masks, including through a median filter.
    for i in range(len(raw)):
        window = raw[max(0,i-1):min(len(raw),i+2)]
        if raw[i] is not None and all(v is not None for v in window):
            out['head_top_y'][i] = float(np.median(window))
    return out


def _native_indices(series, n):
    indices = series.get('indices_native', list(range(n)))
    if len(indices) != n or any(not isinstance(i, (int, np.integer)) for i in indices):
        raise ValueError('indices_native must match series length and contain integers')
    a = np.asarray(indices, dtype=int)
    if len(a)>1 and (np.any(np.diff(a) <= 0) or len(set(np.diff(a))) != 1):
        raise ValueError('series must have uniformly spaced native indices')
    return a, int(a[1]-a[0]) if len(a)>1 else 1


def detect_period(kind, series, fps, prompted_s=None, sibling_stride_frames=None):
    """Reuse the frozen >=2-cycle autocorrelation helper, confidence >= .3."""
    _positive(fps, 'fps')
    if kind not in ('walk', 'run', 'idle'):
        raise ValueError('loop kind must be walk, run or idle')
    values = np.asarray(series['chest_w' if kind == 'idle' else 'head_top_y'], dtype=float)
    _, step = _native_indices(series, len(values))
    usable = values.ndim == 1 and len(values)>=6 and np.isfinite(values).all()
    measured = values
    if usable and kind != 'idle':
        measured = signal.detrend(values, type='linear')
    p, _, confidence = autocorrelation_period(measured, fps/step)
    bob = None
    if p is not None and confidence >= PERIOD_CONFIDENCE:
        bob = int(p*step) if kind != 'idle' else None
        frames = int(p*step*(2 if kind != 'idle' else 1))
        source = 'chest_width_autocorr' if kind == 'idle' else 'head_bob_autocorr'
    elif kind == 'idle':
        seconds = 2.0 if prompted_s is None else prompted_s
        _positive(seconds, 'prompted_s')
        frames = max(1, round(seconds*fps)); source = 'prompted_fallback'
    elif sibling_stride_frames is not None:
        frames = _integer(sibling_stride_frames, 'sibling_stride_frames', 2)
        source = 'sibling'
    else:
        frames = None; source = None
    return dict(frames=frames, seconds=frames/fps if frames is not None else None,
        source=source, confidence=float(confidence), bob_frames=bob,
        bob_seconds=bob/fps if bob is not None else None,
        notes='confidence measures observed autocorrelation, not the prompted/sibling prior')


def _rgb(frame):
    a = _array(frame)
    if a.ndim != 3:
        raise ValueError('RGB MAD requires RGB/RGBA frames, not masks')
    rgb = a[..., :3].astype(np.float32)
    if a.shape[2] == 4:
        rgb *= a[..., 3:4].astype(np.float32)/255.
    return rgb


def _mad(a, b, figure_bbox=False):
    aa, bb = _array(a), _array(b)
    if aa.shape != bb.shape:
        raise ValueError('frame dimensions differ')
    if figure_bbox:
        if aa.ndim != 3 or aa.shape[2] != 4:
            raise ValueError('figure-bbox MAD requires RGBA frames')
        mask = _mask(aa) | _mask(bb)
        if not mask.any():
            return None
        x0, y0, x1, y1 = _bbox(mask)
        aa, bb = aa[y0:y1,x0:x1], bb[y0:y1,x0:x1]
    return float(np.mean(np.abs(_rgb(aa)-_rgb(bb)), dtype=np.float64))


def select_cycle(kind, series, period, fps, t_max_s, min_start_s=0):
    """Latest walk DOWN start, or minimum idle s-to-s+P figure-bbox RGB MAD.

    MAD uses straight RGBA composited on black, in native resolution, with no
    alignment. Walk seam is the emitted window's last native sample to first;
    closure_mad separately measures s to s+P. Idle selection uses closure_mad.
    Splice flags are descriptive and never silently change the selected start.
    """
    _positive(fps, 'fps'); _positive(t_max_s, 't_max_s')
    if not np.isfinite(min_start_s) or min_start_s < 0:
        raise ValueError('min_start_s must be finite and nonnegative')
    if kind not in ('walk', 'run', 'idle'):
        raise ValueError('loop kind must be walk, run or idle')
    y = np.asarray(series['head_top_y'], dtype=float)
    native, step = _native_indices(series, len(y))
    frames = getattr(series, 'frames', None)
    if frames is None:
        frames = series.get('frames')
    if frames is not None and len(frames) != len(y):
        raise ValueError('RGB frame count must match series')
    p = period.get('frames')
    empty = dict(start=None, end_exclusive=None, indices_native=[], reason='no detected period',
                 seam_mad=None, candidates=[], suspect_inside_selected=None)
    if p is None:
        return empty
    p = _integer(p, 'period frames', 1)
    if kind == 'idle' and frames is None:
        raise ValueError('idle closure selection requires source RGBA frames')
    times = np.asarray(series.get('times', native/fps), dtype=float)
    if len(times) != len(y) or not np.isfinite(times).all():
        raise ValueError('times must match series and be finite')
    valid = np.flatnonzero((times >= min_start_s) & (times < t_max_s))
    allowed = set(map(int, valid))
    if kind == 'idle':
        starts = valid
    elif np.isfinite(y).all() and len(y)>2:
        b = period.get('bob_frames') or p/2
        # Every sample of a flat maximum is DOWN. Honour LATEST within each
        # plateau too, rather than scipy's default earlier midpoint rounding.
        _, peaks = signal.find_peaks(y,
            distance=max(1, int(round(DOWN_MIN_DISTANCE_B*b/step))), plateau_size=True)
        starts = peaks['right_edges']
    else:
        starts = []
    by_native = {int(v): i for i,v in enumerate(native)}
    candidates = []
    for j in starts:
        start, end = int(native[j]), int(native[j]+p)
        members = np.flatnonzero((native >= start) & (native < end))
        if j not in allowed or end/fps > t_max_s+1e-12 or not len(members):
            continue
        # A complete half-open interval must be covered by the decoded samples.
        if native[-1]+step < end or any(int(k) not in allowed for k in members):
            continue
        endpoint = by_native.get(end)
        if kind == 'idle' and (endpoint is None or times[endpoint] >= t_max_s):
            continue
        seam = _mad(frames[j], frames[int(members[-1])], True) if frames is not None else None
        closure = _mad(frames[j], frames[endpoint], True) if frames is not None and endpoint is not None else None
        if kind == 'idle' and closure is None:
            continue
        candidates.append(dict(start=start,end_exclusive=end,seam_mad=seam,closure_mad=closure,
                               indices_native=[int(native[k]) for k in members]))
    if not candidates:
        empty['reason'] = 'no complete eligible cycle with required closure evidence'
        return empty
    chosen = max(candidates, key=lambda c:c['start']) if kind != 'idle' else min(
        candidates, key=lambda c:(c['closure_mad'], -c['start']))
    result = dict(chosen, reason='latest eligible DOWN stride' if kind != 'idle' else
                  'minimum s-to-s+P figure-bbox RGB MAD; exact ties choose latest', candidates=candidates)
    result['seam_mad_note'] = 'native RGB on black, pair-union bbox; null without RGB evidence'
    # Reuse supplied full-clip scan when available; otherwise scan these frames.
    splice = series.get('splice')
    if splice is None and frames is not None:
        splice = splice_check(frames)
    suspects = [] if splice is None else splice['suspect_pairs']
    inside = [[int(native[a]),int(native[b])] for a,b in suspects
              if chosen['start'] <= native[a] < native[b] < chosen['end_exclusive']]
    result['suspect_pairs_inside_selected'] = inside
    result['suspect_inside_selected'] = bool(inside) if splice is not None else None
    return result


def resample(start, end_exclusive, n):
    """Native indices using Python's ties-to-even round; no interpolation."""
    start = _integer(start, 'start'); end_exclusive = _integer(end_exclusive, 'end_exclusive')
    n = _integer(n, 'n', 1)
    length = end_exclusive-start
    if length <= 0:
        raise ValueError('cycle length must be positive')
    return [start+round(i*length/n) for i in range(n)]


def splice_check(frames):
    """Consecutive canvas RGB MAD; strict >4x median, including zero median."""
    values = [_mad(a,b) for a,b in zip(frames,frames[1:])]
    median = float(np.median(values)) if values else None
    suspects = [[i,i+1] for i,v in enumerate(values) if v > SPLICE_MEDIAN_MULTIPLIER*median]
    return dict(per_pair_mad=values, suspect_pairs=suspects, median_pair_mad=median,
                multiplier=SPLICE_MEDIAN_MULTIPLIER, notes='RGB composited on black; no loop seam; pairs index supplied frames')


def register(rgba_frames, anchor_index=0, target_h=240, sole_row=399, cx=255.5, canvas=512):
    """One exact isotropic Lanczos sampling box and integer paste per clip.

    Include native frame zero in rgba_frames to register the rest frame with
    precisely the same transform. Translation is computed only from the anchor.
    Floor-sized output excludes <1 output pixel of source plate on right/bottom.
    A bounded raster calibration may adjust the ONE scale by <=1 source output
    pixel to attain requested height and centre parity; never per-frame scaling.
    """
    images = [Image.fromarray(np.asarray(f).astype(np.uint8)) if not isinstance(f,Image.Image) else f for f in rgba_frames]
    if not images:
        raise ValueError('empty RGBA sequence')
    anchor_index = _integer(anchor_index, 'anchor_index')
    if anchor_index >= len(images):
        raise ValueError('anchor_index outside frames')
    canvas = _integer(canvas,'canvas',1); target_h = _integer(target_h,'target_h',1)
    sole_row = _integer(sole_row,'sole_row')
    if sole_row >= canvas or not np.isfinite(cx) or not 0 <= cx < canvas:
        raise ValueError('anchor target outside canvas')
    if any(f.mode != 'RGBA' or f.size != images[0].size for f in images):
        raise ValueError('same-sized RGBA images required')
    anchor = images[anchor_index]
    source_box = _bbox(_mask(anchor)); source_h = source_box[3]-source_box[1]
    nominal = target_h/source_h
    if nominal > 1:
        raise ValueError('upscaling is forbidden')
    w,h = anchor.size
    def scaled(image, scale):
        size = (max(1,math.floor(w*scale)), max(1,math.floor(h*scale)))
        box = (0.,0.,size[0]/scale,size[1]/scale)
        return image.resize(size, Image.Resampling.LANCZOS, box=box), size, box
    choices = []
    # Closest-to-nominal first; the calibration is clip-independent and bounded.
    for delta in sorted(np.linspace(-1.,1.,81), key=lambda d:(abs(d),d)):
        scale = (target_h+float(delta))/source_h
        if not 0 < scale <= 1:
            continue
        resized, size, box = scaled(anchor,scale)
        b = _bbox(_mask(resized))
        center = (b[0]+b[2]-1)/2
        dx = round(cx-center); dy = sole_row-(b[3]-1)
        cost = (abs(b[3]-b[1]-target_h), abs(center+dx-cx), abs(scale-nominal))
        choices.append((cost,scale,size,box,b,dx,dy))
        if cost[:2] == (0,0):
            break
    if not choices:
        raise ValueError('no valid downscale')
    _,scale,size,box,b,dx,dy = min(choices,key=lambda c:c[0])
    if abs(b[3]-b[1]-target_h)>1:
        raise ValueError('raster anchor height could not be calibrated within one pixel')
    result = []
    for image in images:
        resized = image.resize(size,Image.Resampling.LANCZOS,box=box)
        rb = _bbox(_mask(resized))
        if rb[0]+dx<0 or rb[1]+dy<0 or rb[2]+dx>canvas or rb[3]+dy>canvas:
            raise ValueError('shared transform would clip figure alpha support')
        output = Image.new('RGBA',(canvas,canvas))
        output.paste(resized,(dx,dy))
        result.append(output)
    measured = _bbox(_mask(result[anchor_index]))
    transform = dict(scale=scale,nominal_scale=nominal,translation_xy=[dx,dy],
        scaled_size=list(size),source_sampling_box_xyxy=list(box),source_size=[w,h],
        anchor_index=anchor_index,anchor_native_bbox=source_box,canvas=[canvas,canvas],
        anchor_bbox=measured,anchor_H=measured[3]-measured[1],anchor_sole_row=measured[3]-1,
        anchor_cx=(measured[0]+measured[2]-1)/2,target_h=target_h,sole_row=sole_row,cx=cx,
        one_transform_for_every_frame=True,upscaling=False,
        resampling='PIL Lanczos; exact isotropic sampling box; integer unmasked paste',
        calibration='closest nominal scale attaining raster height/centre, search +/-1 output px in .025 px steps')
    return result,transform
