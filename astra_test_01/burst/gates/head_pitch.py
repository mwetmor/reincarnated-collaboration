"""Colour-bin face-height proxy; no claim to an anatomical angle.

Provisional calibration, fixed before real-clip evaluation: CIE76 tolerance
20 Lab units, head top 14% of largest alpha component height, hair L<30,
minimum visible face fraction .02; delta>.05 head heights marks head down.
The .05 threshold is one quarter of the specified synthetic .20 displacement,
not fitted to the real-clip window means. Upright rest selection is explicit.
"""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from gates.common import result

HEAD_FRACTION = .14
SKIN_LAB_TOL = 20.0
HAIR_DARK_L = 30.0
MIN_FACE_FRACTION = .02
HEAD_DOWN_DELTA = .05
CALIBRATION = (__doc__.strip())


def _rgba(frame):
    if isinstance(frame, (str, Path)):
        with Image.open(frame) as image:
            a = np.array(image.convert('RGBA'))
    else:
        a = np.asarray(frame)
    if a.ndim != 3 or a.shape[2] != 4 or a.dtype != np.uint8:
        raise ValueError('head pitch requires uint8 RGBA frames')
    return a


def _lab(rgb):
    rgb = np.asarray(rgb, dtype=float)/255.
    linear = np.where(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)
    xyz = linear @ np.array([[.4124564,.3575761,.1804375],
                            [.2126729,.7151522,.0721750],
                            [.0193339,.1191920,.9503041]]).T
    xyz /= [.95047,1.,1.08883]
    d = 6/29
    f = np.where(xyz>d**3, np.cbrt(xyz), xyz/(3*d*d)+4/29)
    return np.stack((116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])),axis=-1)


def _head(frame):
    a = _rgba(frame)
    labels, _ = ndimage.label(a[...,3] >= 128, np.ones((3,3)))
    counts = np.bincount(labels.ravel()); counts[0] = 0
    if not counts.max():
        return None
    mask = labels == counts.argmax()
    yy, xx = np.where(mask)
    top, bottom = int(yy.min()), int(yy.max()+1)
    height = max(1, int(np.ceil(HEAD_FRACTION*(bottom-top))))
    x0, x1 = int(xx.min()), int(xx.max()+1)
    return dict(lab=_lab(a[top:top+height,x0:x1,:3]),
                mask=mask[top:top+height,x0:x1], head_top_y=top, head_h=height)


def _proxy(head, skin):
    if head is None or skin is None:
        return dict(pitch_proxy=None, face_fraction=0., reason='face_not_visible')
    lab, mask = head['lab'], head['mask']
    face = mask & (lab[...,0] >= HAIR_DARK_L) & (np.linalg.norm(lab-skin,axis=-1) <= SKIN_LAB_TOL)
    fraction = float(face.sum()/mask.sum())
    info = dict(head_top_y=head['head_top_y'],head_h=head['head_h'],
                face_area=int(face.sum()),head_area=int(mask.sum()),face_fraction=fraction)
    if fraction < MIN_FACE_FRACTION:
        return dict(info,pitch_proxy=None,reason='face_not_visible')
    local_y = float(np.where(face)[0].mean())
    return dict(info,face_centroid_y=local_y+head['head_top_y'],
                pitch_proxy=local_y/head['head_h'],reason=None)


def evaluate(frames, rest_frame, *, fps=None, times=None):
    """Return per-frame deltas; optional native fps/times enables first-second report.

    first_second_head_down uses mean evaluable delta at 0<=t<1, strictly >.05.
    Without timing or visible faces this field stays null with a reason.
    """
    frames = list(frames)
    if not frames:
        raise ValueError('empty frame sequence')
    if fps is not None and (not np.isfinite(fps) or fps <= 0):
        raise ValueError('fps must be finite and positive')
    if times is None and fps is not None:
        times = [i/fps for i in range(len(frames))]
    if times is not None:
        times = np.asarray(times,dtype=float)
        if times.shape != (len(frames),) or not np.isfinite(times).all() or np.any(times<0) or np.any(np.diff(times)<0):
            raise ValueError('times must be finite nonnegative ordered timestamps matching frames')
    head = _head(rest_frame)
    candidates = None if head is None else head['lab'][head['mask'] & (head['lab'][...,0]>=HAIR_DARK_L)]
    skin = np.median(candidates,axis=0) if candidates is not None and len(candidates) else None
    rest = _proxy(head,skin)
    rows = []
    for i, frame in enumerate(frames):
        p = _proxy(_head(frame),skin)
        delta = p['pitch_proxy']-rest['pitch_proxy'] if p['pitch_proxy'] is not None and rest['pitch_proxy'] is not None else None
        rows.append(dict(p,index=i,time_s=float(times[i]) if times is not None else None,
                         delta=delta,head_down=bool(delta>HEAD_DOWN_DELTA) if delta is not None else None,
                         delta_reason='face_not_visible' if delta is None else None))
    first = [] if times is None else [p['delta'] for p in rows if p['time_s']<1 and p['delta'] is not None]
    mean = float(np.mean(first)) if first else None
    value = dict(frames=rows,rest=rest,skin_lab=skin.tolist() if skin is not None else None,
        first_second_mean_delta=mean,first_second_evaluable_frames=len(first),
        first_second_head_down=bool(mean>HEAD_DOWN_DELTA) if mean is not None else None,
        first_second_reason='timing_required' if times is None else 'face_not_visible' if mean is None else None,
        calibration=dict(head_fraction=HEAD_FRACTION,skin_lab_tol=SKIN_LAB_TOL,hair_dark_L=HAIR_DARK_L,
                         minimum_face_fraction=MIN_FACE_FRACTION,head_down_delta=HEAD_DOWN_DELTA))
    report = result('head_pitch','clip',value=value,passed=None,unit='fraction_head_h',notes=CALIBRATION)
    report.update(threshold=HEAD_DOWN_DELTA,op='report')
    return report
