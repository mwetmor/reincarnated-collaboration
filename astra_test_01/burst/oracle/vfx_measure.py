"""VFX outcome measurements on registered frames; no alignment or verdict.

PNG filenames are naturally sorted. Alpha support is alpha > 0; black support
is max(R,G,B) > 0 (exact black plate). RGB is interpreted as straight sRGB,
never unpremultiplied or colour-keyed. A gameplay crop is not a black plate.
Durations are milliseconds, one positive finite duration per input frame.
Onset is first nonempty support, peak is first maximum, half is first <= 50%
after peak, life ends at first < 10% after peak. Missing crossings are censored
and returned as null, with an observed lower bound. Residue is final/peak area.

VO10 uses 100 one-L* bins, Gaussian sigma=1 bin, peaks separated by >=5 bins
with >=5% maximum-height prominence. It is inspect-only, not calibrated.
Straight-alpha edges counts partial-alpha boundary pixels whose RGB maximum
exceeds alpha; these prove incompatibility with bounded premultiplied RGB,
but their absence does NOT establish premultiplication. RGB plate: unavailable.
"""
import argparse
import hashlib
import json
import math
import numbers
from pathlib import Path
import re

import numpy as np
from PIL import Image
from scipy import ndimage, signal


def _positive(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise ValueError(name + ' must be a positive finite number')
    if not math.isfinite(value) or value <= 0:
        raise ValueError(name + ' must be a positive finite number')
    return float(value)


def _durations(value, n):
    if isinstance(value, numbers.Real):
        fps = _positive(value, 'fps')
        return np.full(n, 1000.0 / fps), fps
    if isinstance(value, (str, bytes, dict)):
        raise ValueError('durations must be a sequence in milliseconds')
    try:
        raw = list(value)
    except TypeError as exc:
        raise ValueError('expected fps or durations in milliseconds') from exc
    if len(raw) != n:
        raise ValueError('one duration per frame is required')
    durations = np.array([_positive(v, 'duration_ms') for v in raw])
    return durations, None


def _hsv(rgb):
    """Vectorized sRGB HSV, hue in degrees; avoids Pillow HSV quantization."""
    v = rgb.max(axis=-1)
    low = rgb.min(axis=-1)
    delta = v-low
    s = np.divide(delta, v, out=np.zeros_like(v), where=v > 0)
    d = np.where(delta > 0, delta, 1.)
    sector = rgb.argmax(axis=-1)
    h = np.select([sector == 0, sector == 1],
                  [(rgb[..., 1]-rgb[..., 2])/d,
                   (rgb[..., 2]-rgb[..., 0])/d+2],
                  default=(rgb[..., 0]-rgb[..., 1])/d+4)
    h = np.where(delta > 0, (60*h) % 360, 0.)
    return h, s, v


def _modes(rgb):
    linear = np.where(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)
    y = linear @ np.array([.2126, .7152, .0722])
    delta = 6/29
    f = np.where(y > delta**3, np.cbrt(y), y/(3*delta**2)+4/29)
    lightness = 116*f-16
    hist, _ = np.histogram(lightness, bins=100, range=(0, 100))
    smooth = ndimage.gaussian_filter1d(hist.astype(float), 1., mode='constant')
    # Zero padding lets endpoint black/white modes count, too.
    padded = np.pad(smooth, 1)
    peaks, _ = signal.find_peaks(padded, distance=5, prominence=.05*smooth.max())
    return int(len(peaks)), [float(i-.5) for i in peaks], hist.tolist()


def _row(identifier, subject, value, unit, notes, evidence):
    return dict(id=identifier, subject=subject, passed=None, value=value,
                threshold=None, op='report', unit=unit, evidence=evidence, notes=notes)


def _vo_names(value):
    """Read legacy references without emitting legacy metric names.

    Historical white-core reference bands retain their original meaning by
    targeting VO3_white_legacy, never the new saturated-band population.
    """
    if isinstance(value, dict):
        return {_vo_names(k): _vo_names(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_vo_names(v) for v in value]
    if isinstance(value, str):
        return re.sub(r'\b' + 'O' + r'(\d+)',
                      lambda m: 'VO3_white_legacy' if m[1] == '3' else 'V' + m[0], value)
    return value


class _Measurements(dict):
    """Deprecated lookup aliases only; iteration/JSON contain VO names only.

    Existing Python consumers can continue reading their historical quantities.
    Membership, keys(), items(), copied dicts and serialized reports are VO-only.
    """
    def __missing__(self, key):
        translated = _vo_names(key)
        if translated != key and translated in self:
            return self[translated]
        raise KeyError(key)


def measure(frames_dir, fps_or_durations, body_h_px=130, plate='alpha'):
    """Return VO1/VO2/VO3/VO4/VO5/VO6/VO8/VO10, VO3_white_legacy and §1 rows.

    VO3 measures V > .85 and S >= .25 over effect pixels. Legacy white-core
    quantities remain byte-identical under VO3_white_legacy.

    Exact drawing identity includes every decoded RGBA byte, even hidden RGB.
    Unique frames/s = globally distinct drawings / full playback seconds;
    consecutive drawing runs/s is also reported, disambiguating repeats A,B,A.
    White-core order compares the first maximum core FRACTION with area peak:
    <= peak is flash-first, > peak is core-last; no white pixels is no-core.
    Bright/dim percentiles select exactly ceil(.15 N)/ceil(.25 N) by HSV V,
    using stable pixel order to break ties. Null denotes an empty population.
    """
    body_h_px = _positive(body_h_px, 'body_h_px')
    if plate not in ('alpha', 'black'):
        raise ValueError('plate must be alpha or black')
    root = Path(frames_dir)
    if not root.is_dir():
        raise ValueError('frames_dir must be an existing directory')
    def key(path):
        return [(1, int(x)) if x.isdigit() else (0, x.lower())
                for x in re.split(r'(\d+)', path.name)]
    paths = sorted((p for p in root.iterdir() if p.suffix.lower() == '.png'), key=key)
    if not paths:
        raise ValueError('no PNG frames')
    durations, fps = _durations(fps_or_durations, len(paths))
    # Native constant-rate timestamps avoid cumulative drift (e.g. a genuine
    # 60 drawings/s sequence must not become 59.99999999999997 against [60,60]).
    starts = (np.arange(len(paths)+1, dtype=float)*1000./fps if fps is not None
              else np.r_[0., np.cumsum(durations)])
    area, cores, pales, hues, sats, boxes, modes, edges, hashes = [], [], [], [], [], [], [], [], []
    size = None
    for path in paths:
        with Image.open(path) as im:
            if im.mode not in (('RGBA',) if plate == 'alpha' else ('RGB', 'RGBA')):
                raise ValueError('alpha requires RGBA; black requires RGB or RGBA')
            if size is not None and im.size != size:
                raise ValueError('mixed frame sizes')
            size = im.size
            rgba = np.array(im.convert('RGBA'))
        hashes.append(hashlib.sha256(rgba.tobytes()).hexdigest())
        rgb = rgba[..., :3].astype(float)/255.
        mask = rgba[..., 3] > 0 if plate == 'alpha' else rgba[..., :3].max(axis=-1) > 0
        count = int(mask.sum()); area.append(count)
        if plate == 'alpha':
            boundary = mask & ~ndimage.binary_erosion(mask, structure=np.ones((3, 3)))
            partial = (rgba[..., 3] > 0) & (rgba[..., 3] < 255)
            straight = rgba[..., :3].max(axis=-1) > rgba[..., 3]
            edges.append(int(np.count_nonzero(boundary & partial & straight)))
        else:
            edges.append(None)
        if not count:
            cores.append(None); pales.append(None); hues.append(dict(sd_deg=None, mean_deg=None, n=0))
            sats.append(dict(bright_15_median=None, dim_25_median=None, median=None))
            boxes.append(None); modes.append(dict(count=None, centers_Lstar=[], histogram=[]))
            continue
        pixels = rgb[mask]
        h, s, v = _hsv(pixels)
        cores.append(float(np.mean((v > .95) & (s < .25))))
        # Integer comparison keeps inclusive S=.25 exact at byte boundaries.
        byte_pixels = rgba[..., :3][mask].astype(np.int16)
        hi, lo = byte_pixels.max(axis=-1), byte_pixels.min(axis=-1)
        pales.append(float(np.mean((hi > .85*255) & (4*(hi-lo) >= hi))))
        angles = np.deg2rad(h[s > .3])
        if len(angles):
            z = np.exp(1j*angles).mean()
            length = float(abs(z))
            sd = float(np.rad2deg(np.sqrt(-2*np.log(min(1., length))))) if length > 1e-12 else None
            mean = float(np.rad2deg(np.angle(z)) % 360) if length > 1e-12 else None
        else:
            sd = mean = None
        hues.append(dict(sd_deg=sd, mean_deg=mean, n=int(len(angles))))
        order = np.argsort(v, kind='stable')
        sats.append(dict(bright_15_median=float(np.median(s[order[-math.ceil(.15*count):]])),
                         dim_25_median=float(np.median(s[order[:math.ceil(.25*count)]])),
                         median=float(np.median(s))))
        yy, xx = np.where(mask)
        boxes.append([int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)])
        num, centers, hist = _modes(pixels)
        modes.append(dict(count=num, centers_Lstar=centers, histogram=hist))
    peak_area = max(area)
    onset = next((i for i, a in enumerate(area) if a > 0), None)
    peak = int(np.argmax(area)) if peak_area else None
    norm = [a/peak_area for a in area] if peak_area else [None]*len(area)
    half = next((i for i in range(peak+1, len(area)) if norm[i] <= .5), None) if peak is not None else None
    end = next((i for i in range(peak+1, len(area)) if norm[i] < .1), None) if peak is not None else None
    def elapsed(a, b):
        return float(starts[b]-starts[a]) if a is not None and b is not None else None
    def difference(a, b):
        return b-a if a is not None and b is not None else None
    core_max = max((x for x in cores if x is not None), default=0.)
    core_frame = cores.index(core_max) if core_max > 0 else None
    order = ('no-core' if core_frame is None else
             'flash-first' if core_frame <= peak else 'core-last')
    bbox = boxes[peak] if peak is not None else None
    width, height = (bbox[2]-bbox[0], bbox[3]-bbox[1]) if bbox else (None, None)
    seconds = float(starts[-1]/1000)
    changes = sum(a != b for a, b in zip(hashes, hashes[1:]))
    data = _Measurements(schema_version=2, subject=str(root), n_frames=len(paths), canvas_wh=list(size),
                plate=plate, body_h_px=body_h_px, fps=fps, durations_ms=durations.tolist(),
                duration_ms=float(starts[-1]), frame_files=[p.name for p in paths],
                method=dict(mask='alpha > 0' if plate == 'alpha' else 'max(R,G,B) > 0',
                            duration_unit='ms', residue='last frame area / peak area',
                            VO10='100 L* bins; sigma=1; distance=5; prominence=5% of max',
                            straight_alpha_edges='partial-alpha boundary pixels with max(RGB) > alpha'))
    data['VO1'] = dict(area_px=area, peak_area_px=peak_area, envelope_area_over_peak=norm,
                      onset_frame=onset, peak_frame=peak, rise_frames=difference(onset, peak),
                      rise_ms=elapsed(onset, peak), half_frame=half,
                      frames_to_half=difference(peak, half), ms_to_half=elapsed(peak, half),
                      decay_area_over_peak=norm[peak:] if peak is not None else [])
    data['VO2'] = dict(visible_life_frames=difference(onset, end), visible_life_ms=elapsed(onset, end),
                      end_frame=end, censored=onset is not None and end is None,
                      observed_life_frames=difference(onset, end if end is not None else len(area)),
                      observed_life_ms=elapsed(onset, end if end is not None else len(area)))
    data['VO3_white_legacy'] = dict(white_core_fraction=cores, core_frac_at_peak=cores[peak] if peak is not None else None,
                      core_max_frame=core_frame, classification=order)
    data['VO3'] = dict(palest_saturated_fraction=pales,
                       fraction_at_peak=pales[peak] if peak is not None else None,
                       classifier='V > 0.85 and S >= 0.25 over effect pixels')
    data['VO4'] = dict(series=hues, hue_sd_deg_at_peak=hues[peak]['sd_deg'] if peak is not None else None)
    data['VO5'] = dict(series=sats, bright_15_median_at_peak=sats[peak]['bright_15_median'] if peak is not None else None,
                      dim_25_median_at_peak=sats[peak]['dim_25_median'] if peak is not None else None)
    data['VO6'] = dict(bbox_at_peak=bbox, width_px=width, height_px=height,
                      width_bh=width/body_h_px if width is not None else None,
                      height_bh=height/body_h_px if height is not None else None)
    data['VO8'] = dict(unique_frames=len(set(hashes)), unique_frames_per_s=len(set(hashes))/seconds,
                      drawing_changes=changes, drawing_runs=changes+1, drawing_runs_per_s=(changes+1)/seconds,
                      frame_sha256=hashes, method='exact decoded RGBA bytes; globally distinct frames / full playback seconds')
    data['VO10'] = dict(series=modes, count_at_peak=modes[peak]['count'] if peak is not None else None,
                       inspect_only=True)
    data['straight_alpha_edges'] = dict(per_frame=edges, count=sum(x for x in edges if x is not None) if plate == 'alpha' else None,
                                        available=plate == 'alpha')
    data['residue_fraction'] = norm[-1]
    evidence = [str(p) for p in paths]
    data['results'] = [_row(k, str(root), data[k], 'mixed',
                            'Inspect only; uncalibrated mode counter.' if k == 'VO10' else 'Measurement only.', evidence)
                       for k in ('VO1', 'VO2', 'VO3', 'VO3_white_legacy', 'VO4', 'VO5', 'VO6', 'VO8', 'VO10')]
    data['results'] += [_row('straight_alpha_edges', str(root), data['straight_alpha_edges'], 'pixels',
                             'Straight-alpha-compatible boundary evidence; not an alpha encoding verdict.', evidence),
                        _row('residue_fraction', str(root), norm[-1], 'fraction',
                             'Final-frame support / peak support; cut-dependent.', evidence)]
    return data


def compare(measure_json, reference_json):
    """Compare selected scalar/list paths; echo bounds and preserve provisional status.

    Arguments are dicts or JSON file paths. ``in_band`` is descriptive; the
    shared ``passed`` field stays null for uncommitted/proposed/inspect rows.
    Missing, null, nonfinite or nonnumeric values are unevaluable, never in-band.
    Bounds are inclusive. Null upper/lower edges represent one-sided bands;
    two null edges mean no calibrated reference, not an unrestricted band.
    """
    def read(value):
        return json.loads(Path(value).read_text()) if isinstance(value, (str, Path)) else value
    measured, reference = _vo_names(read(measure_json)), _vo_names(read(reference_json))
    rows = []
    for band in reference['bands']:
        value = measured
        try:
            for part in band['path'].split('.'):
                value = value[int(part)] if isinstance(value, list) else value[part]
        except (KeyError, IndexError, TypeError, ValueError):
            value = None
        low, high = band.get('min'), band.get('max')
        for bound in (low, high):
            if bound is not None and (isinstance(bound, bool) or not isinstance(bound, numbers.Real) or not math.isfinite(bound)):
                raise ValueError('reference bounds must be finite numbers or null')
        if low is not None and high is not None and low > high:
            raise ValueError('reference min exceeds max')
        valid = isinstance(value, numbers.Real) and not isinstance(value, bool) and math.isfinite(value)
        inside = bool((low is None or value >= low) and (high is None or value <= high)) if valid and (low is not None or high is not None) else None
        inspect = band.get('inspect_only', False) or band['path'].startswith('VO10.')
        committed = band.get('committed', reference.get('committed', False)) is True
        proposed = band.get('proposed', reference.get('proposed', False)) is True
        row = _row(band.get('id', band['path']), measured.get('subject', 'vfx'), value,
                   band.get('unit', 'number'), band.get('notes', ''), band.get('evidence', []))
        if not valid:
            row['value'] = None
        row.update(threshold=dict(min=low, max=high), op='in_band', in_band=inside,
                   passed=inside if committed and not proposed and not inspect else None,
                   path=band['path'], committed=committed, proposed=proposed, inspect_only=inspect,
                   tolerance=band.get('tolerance', 0), exemplars=band.get('exemplars', []))
        if inside is None:
            row['notes'] += ' Unevaluable: missing/nonfinite measurement or no reference bounds.'
        elif not committed or proposed or inspect:
            row['notes'] += ' Descriptive comparison only; no committed verdict.'
        rows.append(row)
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames_dir', type=Path)
    parser.add_argument('--fps', type=float, default=60.)
    parser.add_argument('--durations', type=Path, help='JSON list of per-frame durations in milliseconds')
    parser.add_argument('--ref', type=Path)
    parser.add_argument('--plate', choices=('alpha', 'black'), default='alpha')
    parser.add_argument('--body-h-px', type=float, default=130.)
    args = parser.parse_args(argv)
    try:
        _positive(args.fps, 'fps')
        timing = json.loads(args.durations.read_text()) if args.durations else args.fps
        result = measure(args.frames_dir, timing, args.body_h_px, args.plate)
        if args.ref:
            result['comparison'] = compare(result, args.ref)
        print(json.dumps(result, allow_nan=False))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
