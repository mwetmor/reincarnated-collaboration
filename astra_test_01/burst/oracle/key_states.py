"""T4q key-state registration and measurements; no per-piece registration.

Coordinates are integer pixel centres. Registration maps source to guide with
one positive uniform scale (<=1) and one XY translation. Alpha > .5 is the
shape contract. Piece masks MUST already be transformed into the guide canvas.
Reports expose literal thresholds and excesses; no threshold is fitted to art.
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage, optimize, signal
from oracle.peak_pieces import isolate, quantise, _index_rgba

CONNECTIVITY = np.ones((3, 3), bool)


def indexed(value, palette=None):
    """Isolate using T4e and quantise; optionally decode a rendered guide ramp."""
    rgba = np.array(isolate(value) if isinstance(value, (str, Path)) else value)
    if rgba.dtype != np.uint8 or rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError('expected uint8 RGBA')
    if palette is not None:
        ramp = np.asarray(palette, float)[:, :3]*255
        bands = np.argmin(((rgba[..., None, :3].astype(float)-ramp)**2).sum(axis=-1), axis=-1)
        return _index_rgba(bands, rgba[..., 3])
    bands, alpha, _ = quantise(rgba)
    return _index_rgba(bands, alpha)


def warp(rgba, scale, translation, shape):
    """The only painting transform: bilinear, premultiplied, uniform affine."""
    if not 0 < scale <= 1 or len(translation) != 2:
        raise ValueError('registration permits one downscale and XY translation only')
    rgba = np.asarray(rgba)
    a = rgba[..., 3].astype(float)/255
    offset = -np.asarray(translation, float)[::-1]/scale
    def sample(v):
        return ndimage.affine_transform(v, np.eye(2)/scale, offset=offset,
                                        output_shape=tuple(shape), order=1, mode='constant', prefilter=False)
    alpha = sample(a)
    result = np.zeros((*shape, 4), np.uint8)
    for channel in range(3):
        result[..., channel] = np.rint(np.divide(sample(rgba[..., channel]*a), alpha,
                                   out=np.zeros(shape), where=alpha > 0)).clip(0,255).astype(np.uint8)
    result[..., 3] = np.rint(alpha*255).astype(np.uint8)
    return result


def _iou(a, b):
    union = np.count_nonzero(a | b)
    return float(np.count_nonzero(a & b)/union) if union else 1.0


def register(painting, guide):
    """Return (registered four-band RGBA, reproducible affine metadata).

    Global coarse scale search + FFT translation, then multiresolution soft
    IoU optimisation. Rotation, shear, per-shard fits and upscaling are absent.
    The search is independent of colour and cannot improve interior planes.
    """
    source = np.array(isolate(painting) if isinstance(painting, (str, Path)) else painting)
    if source.dtype != np.uint8 or source.ndim != 3 or source.shape[2] != 4:
        raise ValueError('expected uint8 RGBA painting')
    target = indexed(guide)
    source_mask, target_mask = source[..., 3] > 127, target[..., 3] > 127
    if not source_mask.any() or not target_mask.any():
        raise ValueError('registration needs nonempty painting and guide')
    shape = target_mask.shape
    factor = min(1., 192/max(*shape, *source_mask.shape))
    small_source = ndimage.zoom(source_mask.astype(float), factor, order=1)
    small_target = ndimage.zoom(target_mask.astype(float), factor, order=1)
    nominal = min(shape[0]/source_mask.shape[0], shape[1]/source_mask.shape[1], 1.)
    area_scale = min(1., math.sqrt(target_mask.sum()/source_mask.sum()))
    lo = max(.05, min(nominal, area_scale)*.55)
    hi = min(1., max(nominal, area_scale)*1.5)
    best = None
    for scale in np.unique(np.r_[np.linspace(lo, hi, 65), nominal, area_scale]):
        resized = ndimage.zoom(small_source, scale, order=1)
        correlation = signal.fftconvolve(small_target, resized[::-1, ::-1], mode='full')
        y, x = np.unravel_index(np.argmax(correlation), correlation.shape)
        shift = np.array([x-resized.shape[1]+1, y-resized.shape[0]+1], float)
        overlap = correlation[y, x]
        score = overlap/max(1., small_target.sum()+resized.sum()-overlap)
        if best is None or score > best[0]: best = (score, np.r_[scale, shift/factor])
    params = best[1]
    # Fit at increasing resolution using the same original mask each time.
    for level in (min(1., 256/max(shape)), min(1., 512/max(shape)), 1.):
        yy, xx = np.indices(tuple(max(1, round(n*level)) for n in shape), dtype=float)
        coords = np.array([yy/level, xx/level])
        truth = ndimage.map_coordinates(target_mask.astype(float), coords, order=1, prefilter=False)
        def objective(p):
            s, tx, ty = p
            sample = ndimage.map_coordinates(source_mask.astype(float),
                          [(coords[0]-ty)/s, (coords[1]-tx)/s], order=1, mode='constant', prefilter=False)
            overlap = np.minimum(sample, truth).sum()
            return -float(overlap/max(1., np.maximum(sample, truth).sum()))
        result = optimize.minimize(objective, params, method='Powell',
                   bounds=[(lo, hi), (params[1]-12/level, params[1]+12/level),
                           (params[2]-12/level, params[2]+12/level)],
                   options={'xtol': .0001, 'ftol': 1e-7, 'maxiter': 35})
        if objective(result.x) < objective(params): params = result.x
    scale, tx, ty = map(float, params)
    registered = indexed(warp(source, scale, [tx, ty], shape))
    return registered, dict(scale=scale, translation_xy=[tx, ty],
        source_canvas_wh=list(source.shape[1::-1]), guide_canvas_wh=list(shape[::-1]),
        silhouette_iou=_iou(registered[..., 3] > 127, target_mask),
        transform='guide_xy = source_xy * scale + translation_xy; no rotation or per-piece fitting',
        interpolation='premultiplied bilinear; quantised after resampling')


def clipped(painting, guide, dilation_px=2):
    """Intersect with Euclidean 2-px dilation; fill uncovered guide pixels.

    RGB of added guide pixels comes from its decoded original index planes.
    No morphology removes islands or thins contours to make a metric pass.
    """
    painting, guide = indexed(painting), indexed(guide)
    mask = guide[..., 3] > 127
    allowed = ndimage.distance_transform_edt(~mask) <= dilation_px
    result = painting.copy()
    removed = (result[..., 3] > 127) & ~allowed
    result[~allowed] = 0
    fill = mask & (result[..., 3] <= 127)
    result[fill] = guide[fill]
    return result, dict(dilation_px=dilation_px, removed_pixels=int(removed.sum()),
        guide_fill_pixels=int(fill.sum()), guide_fill_fraction=float(fill.sum()/max(1, mask.sum())),
        painted_guide_fraction=float((mask & ~fill).sum()/max(1, mask.sum())))


def _centroid(mask):
    y, x = np.where(mask)
    return [float(x.mean()), float(y.mean())] if len(x) else None


def stroke_width(rgba):
    """Mean band-0 medial-ridge local diameter, 2*EDT-1, in native pixels.

    Ridge = 3x3 local EDT maxima. Interior band-zero marks are included. This
    is a reproducible raster width instrument, not a claim of vector width.
    """
    mask = (rgba[..., 3] > 127) & (rgba[..., 0] == 0)
    if not mask.any(): return 0.0
    distance = ndimage.distance_transform_edt(np.pad(mask, 1))[1:-1, 1:-1]
    ridge = mask & (distance >= ndimage.maximum_filter(distance, size=3))
    return float(np.mean(2*distance[ridge]-1))


def report(painting, guide, piece_masks, fps=60):
    """Matching region = covered piece + nearest-piece-assigned exterior.

    Overlapping transformed pieces retain independent expected footprints.
    Outside the whole guide, painting pixels are assigned to the nearest
    footprint (lowest ID tie); extras therefore affect centroid offsets.
    Fully occluded/eroded pieces are explicit null measurements, not successes.
    """
    p, g = indexed(painting), indexed(guide)
    if p.shape != g.shape: raise ValueError('painting and guide canvas differ')
    pm, gm = p[..., 3] > 127, g[..., 3] > 127
    if not gm.any() or not piece_masks: raise ValueError('nonempty guide and transformed pieces required')
    masks = {int(k): np.asarray(v, bool) & gm for k, v in piece_masks.items()}
    if any(v.shape != gm.shape for v in masks.values()): raise ValueError('piece canvas differs')
    best_distance = np.full(gm.shape, np.inf)
    owners = np.zeros(gm.shape, int)
    for ident, mask in sorted(masks.items()):
        if not mask.any(): continue
        distance = ndimage.distance_transform_edt(~mask)
        take = distance < best_distance
        owners[take], best_distance[take] = ident, distance[take]
    rows, failures = [], []
    for ident, mask in sorted(masks.items()):
        area = int(mask.sum())
        if not area:
            rows.append(dict(id=ident, guide_pixels=0, coverage_fraction=None,
                 centroid_offset_px=None, passed=None, reason='no visible guide footprint at this age'))
            continue
        covered = mask & pm
        matching = covered | (pm & ~gm & (owners == ident))
        fraction = float(covered.sum()/area)
        expected, actual = _centroid(mask), _centroid(matching)
        offset = float(np.linalg.norm(np.asarray(actual)-expected)) if actual is not None else None
        ok = fraction >= .9 and offset is not None and offset <= 1.
        row = dict(id=ident, guide_pixels=area, matching_pixels=int(matching.sum()),
            coverage_fraction=fraction, coverage_min=.9, coverage_shortfall=max(0., .9-fraction),
            guide_centroid_xy=expected, painting_centroid_xy=actual, centroid_offset_px=offset,
            centroid_max_px=1., centroid_excess_px=max(0., offset-1) if offset is not None else None, passed=bool(ok))
        rows.append(row)
        if fraction < .9: failures.append(dict(test='piece_coverage', piece=ident, value=fraction, threshold=.9, shortfall=.9-fraction))
        if offset is None or offset > 1: failures.append(dict(test='piece_centroid', piece=ident, value=offset, threshold=1., excess=None if offset is None else offset-1))
    union = np.logical_or.reduce(list(masks.values()))
    unmapped = int((gm & ~union).sum())
    if unmapped: failures.append(dict(test='guide_piece_mapping', value=unmapped, threshold=0, excess=unmapped))
    iou = _iou(pm, gm)
    pn, gn = int(ndimage.label(pm, CONNECTIVITY)[1]), int(ndimage.label(gm, CONNECTIVITY)[1])
    pw, gw = stroke_width(p), stroke_width(g)
    delta = pw-gw
    different = not np.array_equal(p, g)
    hashes = [hashlib.sha256(a.tobytes()).hexdigest() for a in (g, p)]
    seconds = 2/fps
    boil = dict(silhouette_iou=iou, silhouette_iou_min=.9,
        silhouette_iou_shortfall=max(0., .9-iou), guide_shards=gn, painting_shards=pn,
        shard_count_delta=pn-gn, shard_count_tolerance=1, shard_count_excess=max(0, abs(pn-gn)-1),
        guide_band0_width_px=gw, painting_band0_width_px=pw, contour_thickening_px=delta,
        contour_thickening_max_px=1., contour_thickening_excess_px=max(0., delta-1.),
        VO8=dict(unique_frames=len(set(hashes)), unique_frames_per_s=len(set(hashes))/seconds,
            drawing_changes=int(different), drawing_runs=1+int(different),
            drawing_runs_per_s=(1+int(different))/seconds, frame_sha256=hashes, duration_s=seconds,
            method='exact decoded indexed RGBA bytes, two frames at stated fps', fps=fps,
            in_band=bool(different and iou >= .9),
            band_definition='drawing changes while silhouette IoU >= 0.9; no additional temporal threshold supplied'),
        changed_pixel_fraction=float(np.any(p != g, axis=-1)[pm | gm].mean()),
        interior_band_change_fraction=float((p[..., 0] != g[..., 0])[pm & gm].mean()) if np.any(pm & gm) else None,
        drawing_changed=different, passed=bool(iou >= .9 and abs(pn-gn) <= 1 and delta <= 1 and different))
    for name, value, threshold, excess in [('silhouette_iou',iou,.9,.9-iou),
            ('shard_count',abs(pn-gn),1,abs(pn-gn)-1), ('contour_thickening',delta,1.,delta-1.)]:
        if excess > 0: failures.append(dict(test=name, value=value, threshold=threshold, excess=excess))
    if not different: failures.append(dict(test='drawing_changed', value=False, threshold=True))
    evaluated = [r for r in rows if r['guide_pixels']]
    correspondence = dict(pieces=rows, guide_unmapped_pixels=unmapped,
        passed=bool(evaluated and not unmapped and all(r['passed'] for r in evaluated)),
        matching_method='independent transformed footprint intersections plus nearest-footprint exterior; binary alpha > 0.5, 8-connectivity')
    def metric(identifier, subject, passed, value, threshold, op, unit, notes=''):
        return dict(id=identifier, subject=subject, passed=passed, value=value,
                    threshold=threshold, op=op, unit=unit, evidence=[], notes=notes)
    results = []
    for row in rows:
        value = row['coverage_fraction']
        results.append(metric('key_correspondence_coverage', 'piece/'+str(row['id']),
            None if value is None else value >= .9, value, .9, '>=', 'fraction', row.get('reason','')))
        value = row['centroid_offset_px']
        results.append(metric('key_correspondence_centroid', 'piece/'+str(row['id']),
            None if not row['guide_pixels'] else value is not None and value <= 1.,
            value, 1., '<=', 'native_px', row.get('reason','')))
    results.extend([
        metric('key_silhouette', 'whole_image', iou >= .9, iou, .9, '>=', 'iou'),
        metric('key_shards', 'whole_image', abs(pn-gn) <= 1, abs(pn-gn), 1, '<=', 'components'),
        metric('key_contour', 'whole_image', delta <= 1., delta, 1., '<=', 'native_px'),
        metric('VO8', 'guide_to_painting', boil['VO8']['in_band'], boil['VO8'],
               {'drawing_changes': 1, 'silhouette_iou_min': .9}, 'shape_band', 'mixed',
               'Two-state drawing-change measurement, not a calibrated temporal rate gate.')])
    return dict(correspondence=correspondence, boil=boil,
                passed=bool(correspondence['passed'] and boil['passed']), failures=failures,
                results=results)


def write_board(guide, painting, path):
    g, p = indexed(guide), indexed(painting)
    h, w = g.shape[:2]
    board = Image.new('RGB', (3*w, h+32), (35,39,48))
    for i, rgba in enumerate((g, p)):
        layer = Image.new('RGBA', (w,h), (35,39,48,255))
        layer.alpha_composite(Image.fromarray(rgba)); board.paste(layer, (i*w,32))
    overlay = np.zeros_like(g);gm=g[...,3]>127;pm=p[...,3]>127
    overlay[gm & pm] = [220,220,220,255]
    overlay[gm & ~pm] = [255,70,70,255]
    overlay[pm & ~gm] = [40,220,255,255]
    layer = Image.new('RGBA',(w,h),(35,39,48,255));layer.alpha_composite(Image.fromarray(overlay));board.paste(layer,(2*w,32))
    draw = ImageDraw.Draw(board)
    for i,title in enumerate(('Guide (decoded bands)','Registered painting','Overlay: red missing / cyan extra')): draw.text((i*w+8,8),title,fill='white')
    board.save(path)


def runtime_piece_masks(runtime, source_root, guide, age):
    """CPU bilinear footprints of the actual v2 transforms and erosion uniforms.

    Returns per-original-shard masks including root AND stretched coverage.
    A shard contributes wherever sampled alpha > 0 inside guide alpha > .5;
    this includes translucent layers whose composite exceeds .5 together.
    Raster edge disagreements are assigned to nearest computed footprint only
    within 1 native pixel; unexplained guide coverage remains a reported error.
    This is correspondence instrumentation, not a rendered-frame proof.
    """
    from export.effect_kit import distance_field, erosion_distance, erosion_noise_texture, dissolve_thresholds
    source_root = Path(source_root)
    peak = np.array(Image.open(source_root/'peak_index.png').convert('RGBA'))
    distance = erosion_distance(peak, distance_field(peak), runtime.get('erode_noise',0), erosion_noise_texture(peak))
    h,w = np.shape(guide)[:2]
    yy,xx = np.indices((h,w), dtype=float)
    screen = np.array([xx-w/2, yy-h/2]).reshape(2,-1)
    centre = np.asarray(runtime['centre'])
    flight = runtime['flash_frames']+runtime['hold_frames']
    ease = 1-(1-np.clip((age-flight)/15,0,1))**3
    erosion = float(np.clip((age-flight-15)/21,0,1))
    residue = flight+36
    dissolve = .8*float(np.clip((age-residue)/runtime['residue_frames'],0,1))
    thresholds = np.array(dissolve_thresholds(runtime.get('dissolve_order')))
    def rotation(angle): return np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
    masks={}
    for item in runtime['pieces']:
        rgba=np.array(Image.open(source_root/item['mask']).convert('RGBA'))
        alpha=rgba[...,3]/255
        bands=rgba[...,0]/85
        def sample(coords, erode, dissolve_value):
            co=[coords[1],coords[0]]
            a=ndimage.map_coordinates(alpha,co,order=1,mode='constant',prefilter=False)
            d=ndimage.map_coordinates(distance,co,order=1,mode='nearest',prefilter=False)
            b=np.clip(np.floor(ndimage.map_coordinates(bands,co,order=1,mode='constant',prefilter=False)+.5),0,3).astype(int)
            return ((a>0)&((erode<=0)|((d<=1-erode)&(erode<1)))&(dissolve_value<thresholds[b])).reshape(h,w)
        mask=np.zeros((h,w),bool)
        if item['area_px']>=48 and flight<=age<residue+runtime['residue_frames']:
            mask=sample(screen+centre[:,None],runtime['residue_erode']*erosion,dissolve)
            if age<residue:
                angle=item['axis_radians'];root=np.array(item['root'])
                if item['core']:
                    swell=1+.25*(1-(1-np.clip((age-flight)/9,0,1))**3);scales=[swell,swell];drift=0
                else:
                    scales=[1+(item['along']-1)*ease,1-.15*ease];drift=runtime['root_drift']*runtime['core_radius_px']*ease
                mat=rotation(angle+math.radians(item['rotation_deg'])*ease)@np.diag(scales)@rotation(-angle)
                position=root-centre+rotation(angle)[:,0]*drift
                coords=np.linalg.solve(mat,screen-position[:,None])+root[:,None]
                mask |= sample(coords,erosion,0)
        masks[item['id']]=mask
    gm=np.asarray(guide)[...,3]>127
    union=np.logical_or.reduce(list(masks.values()))
    # IDs remain the original T4e IDs. Edge assignment never resegments paint.
    missing=gm&~union
    if union.any() and missing.any():
        dist,nearest=ndimage.distance_transform_edt(~union,return_indices=True)
        for ident,mask in masks.items():
            mask |= missing & (dist<=1) & mask[tuple(nearest)]
    return {i:m&gm for i,m in masks.items()}


def bindings(reports, png_paths):
    """Only the measured CLIPPED form can be bound; null is not acceptance."""
    result = []
    for state in ('expanded', 'spent'):
        row = reports.get(state)
        if row is None:
            continue
        measured = row['clipped']
        if (measured.get('passed') is True
                and measured['correspondence'].get('passed') is True
                and measured['boil'].get('passed') is True
                and not measured.get('failures')):
            result.append(dict(state=state, png=png_paths[state],
                               hold_frames=row['hold_frames'], at_age=row['at_age']))
    return result


def build(painting, guide, piece_masks, out_dir, palette=None):
    """Write one state's RAW/CLIPPED measurements and three-column boards.

    piece_masks are original T4e IDs already transformed onto the guide
    canvas (runtime_piece_masks supplies them for v2). No binding occurs here.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    guide = indexed(guide, palette)
    painting, registration = register(painting, guide)
    limited, clipping = clipped(painting, guide)
    results = dict(registration=registration, clipping=clipping,
                   raw=report(painting, guide, piece_masks),
                   clipped=report(limited, guide, piece_masks))
    for name, pixels in (('raw', painting), ('clipped', limited)):
        Image.fromarray(pixels).save(out/(name+'.png'))
        write_board(guide, pixels, out/(name+'_board.png'))
    (out/'key_states.json').write_text(json.dumps(results, indent=2, allow_nan=False)+'\n')
    return results
