"""Deterministic painted-plane decomposition; no resize, repaint or gate verdict.

API: isolate -> PIL RGBA (isolation metadata in image.info['isolation']);
quantise -> (uint8 HxW band indices 0..3, unchanged uint8 alpha, histogram);
decompose -> list of dictionaries, with boolean ndarray 'mask' in memory.
build serializes that mask as a full-canvas RGBA PNG filename.

Coverage/support = alpha > 0 (vfx_measure convention). Centroids use alpha
weights. Pixel coordinates denote pixel centres at integer x,y; bboxes are
[left, top, right_exclusive, bottom_exclusive]. Angles are clockwise from +x.

Spatial segmentation is independent of RGB. Contour radial extrema mark
tongues and concavities; a compact seeded watershed uses negative silhouette
distance plus concavity ridges. Five core markers form wedges. Long tongues
are split at an interior width minimum. Adjacent slivers merge by longest
shared border, never by colour. Detached source islands cannot be merged
without inventing coverage: they remain explicit, connected pieces with an
unmergeable_sliver reason. No source pixels are discarded or bridged.
"""
import argparse
import colorsys
import heapq
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage, signal

CONNECTIVITY = np.ones((3, 3), dtype=bool)
BANDS = np.array([0, 85, 170, 255], dtype=np.uint8)


def _rgba(value):
    a = np.asarray(value)
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] != 4 or not all(a.shape[:2]):
        raise ValueError('expected nonempty uint8 HxWx4 straight-alpha RGBA')
    return a


def isolate(peak_png, plate='auto'):
    """Preserve real alpha byte-for-byte; otherwise key exact flat green.

    Green excess G-max(R,B) gives candidate coverage. Partial candidates are
    retained only within Euclidean distance <=1 px of a non-green core; their
    RGB is clamped to the nearest core pixel. Exact green remains transparent.
    Auto rejects an opaque image without exact green on its canvas border.
    Explicit alpha accepts fully opaque images; explicit green requires opaque
    input to avoid silently throwing away existing coverage.
    """
    if plate not in ('auto', 'green', 'alpha'):
        raise ValueError('plate must be green, alpha or auto')
    with Image.open(peak_png) as im:
        if im.format != 'PNG':
            raise ValueError('source must be PNG')
        rgba = np.array(im.convert('RGBA'))
    real_alpha = bool(np.any(rgba[..., 3] < 255))
    use_alpha = plate == 'alpha' or (plate == 'auto' and real_alpha)
    meta = dict(requested=plate, plate_path_used='alpha' if use_alpha else 'green',
                real_transparency=real_alpha, fringe_width_px=0.0,
                fringe_clamp_limit_px=0 if use_alpha else 1,
                removed_fringe_pixels=0)
    if not use_alpha:
        if real_alpha:
            raise ValueError('green key requires opaque input; use alpha for existing transparency')
        rgb = rgba[..., :3].astype(np.int16)
        exact = np.all(rgb == [0, 255, 0], axis=-1)
        border = np.zeros(exact.shape, dtype=bool)
        border[[0, -1], :] = True
        border[:, [0, -1]] = True
        if not np.any(exact & border):
            raise ValueError('no flat pure green plate on the border; specify --plate alpha if intentional')
        excess = np.maximum(0, rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]))
        candidate = (255-excess).astype(np.uint8)
        core = candidate == 255
        if not core.any():
            raise ValueError('green plate contains no non-green body core')
        distance, nearest = ndimage.distance_transform_edt(~core, return_indices=True)
        partial = (candidate > 0) & (candidate < 255)
        kept = partial & (distance <= 1.0)
        rejected = partial & ~kept
        candidate[rejected] = 0
        rgba[..., 3] = candidate
        rgba[kept, :3] = rgba[nearest[0][kept], nearest[1][kept], :3]
        rgba[candidate == 0, :3] = 0
        meta.update(fringe_width_px=float(distance[kept].max()) if kept.any() else 0.0,
                    removed_fringe_pixels=int(rejected.sum()),
                    keyed_plate_pixels=int(exact.sum()))
    if not np.any(rgba[..., 3]):
        raise ValueError('source has empty coverage')
    result = Image.fromarray(rgba)
    result.info['isolation'] = meta
    return result


def _luminance(rgba):
    # Encoded sRGB levels, not linear-light or L*: the source index contract.
    return rgba[..., :3].astype(float) @ np.array([0.2126, 0.7152, 0.0722])


def quantise(rgba):
    """Nearest 0/85/170/255 in encoded-sRGB luminance; midpoint ties go up.

    Histogram keys '0'..'3' count alpha>0 pixels, including opaque band zero.
    Four bands are the allowed alphabet; absent bands retain zero counts.
    """
    rgba = _rgba(rgba)
    alpha = rgba[..., 3].copy()
    index_map = np.clip(np.floor(_luminance(rgba)/85 + 0.5), 0, 3).astype(np.uint8)
    index_map[alpha == 0] = 0
    counts = np.bincount(index_map[alpha > 0], minlength=4)
    return index_map, alpha, {str(i): int(counts[i]) for i in range(4)}


def plane_quality(rgba):
    """Report source defects without smoothing or changing the quantisation."""
    rgba = _rgba(rgba)
    visible = rgba[..., 3] > 0
    if not visible.any():
        raise ValueError('source has empty coverage')
    luma = _luminance(rgba)
    error = np.min(np.abs(luma[..., None]-BANDS.astype(float)), axis=-1)
    far = (error > 20) & visible
    rgb = rgba[..., :3][visible]
    opaque = rgba[..., 3] == 255
    counts = np.bincount(np.clip(np.rint(luma[visible]), 0, 255).astype(int), minlength=256)
    return dict(luminance='encoded sRGB: 0.2126 R + 0.7152 G + 0.0722 B',
                support_pixels=int(visible.sum()), source_rgb_levels=int(len(np.unique(rgb, axis=0))),
                source_rounded_luminance_levels=int(np.count_nonzero(counts)),
                luminance_histogram=counts.tolist(),
                farther_than_20_pixels=int(far.sum()),
                farther_than_20_fraction=float(far.sum()/visible.sum()),
                farther_than_20_alpha_weighted_fraction=float(rgba[..., 3][far].sum()/rgba[..., 3].sum()),
                opaque_pixels=int(opaque.sum()),
                opaque_farther_than_20_pixels=int((far & opaque).sum()),
                opaque_farther_than_20_fraction=float((far & opaque).sum()/opaque.sum()) if opaque.any() else None,
                non_greyscale_pixels=int(np.count_nonzero(rgb.max(axis=1) != rgb.min(axis=1))),
                partial_alpha_pixels=int(np.count_nonzero(visible & ~opaque)),
                more_than_four_source_levels=bool(len(np.unique(rgb, axis=0)) > 4))


def coverage_centroid(alpha):
    a = np.asarray(alpha, dtype=float)
    if a.ndim != 2 or not np.isfinite(a).all() or np.any(a < 0) or a.sum() <= 0:
        raise ValueError('centroid requires nonempty nonnegative coverage')
    y, x = np.indices(a.shape)
    return [float((x*a).sum()/a.sum()), float((y*a).sum()/a.sum())]


def _centre(value, alpha):
    if value is None:
        return coverage_centroid(alpha)
    a = np.asarray(value, dtype=float)
    if a.shape != (2,) or not np.isfinite(a).all():
        raise ValueError('centre must contain two finite pixel coordinates')
    return a.tolist()


def _pivot(mask, alpha):
    centroid = coverage_centroid(np.where(mask, alpha, 0))
    x, y = np.floor(np.array(centroid)+0.5).astype(int)
    if mask[y, x]:
        return centroid, centroid, False
    yy, xx = np.where(mask)
    # np.argmin provides deterministic row-major tie breaking.
    nearest = np.argmin((xx-centroid[0])**2+(yy-centroid[1])**2)
    return [int(xx[nearest]), int(yy[nearest])], centroid, True


def _contour(mask):
    """Ordered Moore outer contour (8-neighbours), without altering support."""
    filled = np.pad(ndimage.binary_fill_holes(mask), 1)
    yy, xx = np.where(filled)
    start = (int(yy[0]), int(xx[0]))
    offsets = [(0, -1), (-1, -1), (-1, 0), (-1, 1),
               (0, 1), (1, 1), (1, 0), (1, -1)]
    current, back = start, (start[0], start[1]-1)
    points, states = [], set()
    for _ in range(int(mask.sum())*16+8):
        state = (current, back)
        if state in states:
            break
        states.add(state)
        points.append([current[1]-1, current[0]-1])
        delta = (back[0]-current[0], back[1]-current[1])
        begin = offsets.index(delta)
        for step in range(1, 9):
            k = (begin+step) % 8
            dy, dx = offsets[k]
            nxt = (current[0]+dy, current[1]+dx)
            if filled[nxt]:
                py, px = offsets[(k-1) % 8]
                back = (current[0]+py, current[1]+px)
                current = nxt
                break
        else:
            break
    return np.asarray(points, dtype=float)


def _nearest(mask, point):
    yy, xx = np.where(mask)
    i = np.argmin((xx-point[0])**2+(yy-point[1])**2)
    return [int(xx[i]), int(yy[i])]


def _geometry(mask, origin):
    distance = ndimage.distance_transform_edt(np.pad(mask, 1))[1:-1, 1:-1]
    cy, cx = np.unravel_index(np.argmax(distance), mask.shape)
    radius = float(distance[cy, cx])
    contour = _contour(mask)
    radial = np.linalg.norm(contour-np.asarray(origin), axis=1)
    body_radius = float(radial.max())
    # Smooth sampling noise, not the silhouette or its coverage.
    smooth = ndimage.gaussian_filter1d(radial, max(1., .01*body_radius), mode='wrap')
    n = len(contour)
    peaks, props = signal.find_peaks(np.tile(smooth, 3), prominence=.15*body_radius,
                                    distance=max(2, int(.15*body_radius)))
    tips = sorted(int(i-n) for i in peaks if n <= i < 2*n)
    roots = []
    for i, tip in enumerate(tips):
        end = tips[(i+1) % len(tips)]
        arc = np.arange(tip, end if end > tip else end+n+1) % n
        roots.append(int(arc[np.argmin(smooth[arc])]))
    return distance, dict(core_centre=[int(cx), int(cy)], core_radius_px=radius,
                         burst_centre=list(origin),
                         body_radius_px=body_radius, prominence_px=.15*body_radius,
                         tips=[contour[i].astype(int).tolist() for i in tips],
                         roots=[contour[i].astype(int).tolist() for i in roots])


def _tongue_marker(mask, distance, tip, roots):
    """Connected interior marker from the contour tip toward its root pair.

    A boundary point alone makes a high-EDT core swallow the tongue's shaft.
    Extend that marker 65% toward its root along a shortest interior path;
    positive inverse-EDT costs prefer the medial shaft, including hooked tips.
    """
    target = _nearest(mask, .35*np.asarray(tip)+.65*np.mean(roots, axis=0))
    tx, ty = target
    sx, sy = tip
    queue = [(0., sy, sx)]
    costs = {(sy, sx): 0.}
    parents = {}
    h, w = mask.shape
    while queue:
        score, y, x = heapq.heappop(queue)
        if score != costs[(y, x)]:
            continue
        if (x, y) == (tx, ty):
            path = [(x, y)]
            while (y, x) != (sy, sx):
                y, x = parents[(y, x)]
                path.append((x, y))
            return path
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y+dy, x+dx
                if not (dx or dy) or not (0 <= ny < h and 0 <= nx < w and mask[ny, nx]):
                    continue
                value = score+math.hypot(dx, dy)*(1.+4./max(1., distance[ny, nx]))
                if value < costs.get((ny, nx), math.inf):
                    costs[(ny, nx)] = value
                    parents[(ny, nx)] = (y, x)
                    heapq.heappush(queue, (value, ny, nx))
    return [tip]


def _watershed(mask, distance, geometry):
    """Compact marker watershed on negative EDT with concavity-root ridges.

    Priority is the maximum topographic elevation along the flooding path,
    then geodesic path length for deterministic ties. A compactness term of
    2 * path_length / core_radius balances the core wedges: without it, tiny
    raster variations in a near-flat basin let one centre marker swallow its
    neighbours. Markers extend inward from tips and stay independent of bands.
    """
    radius = geometry['core_radius_px']
    cx, cy = geometry['core_centre']
    yy, xx = np.indices(mask.shape)
    cost = 1. + (radius-distance)/max(radius, 1.)
    # Concavity-root ridges taper inward; EDT bends the watershed around necks.
    for rx, ry in geometry['roots']:
        vx, vy = rx-cx, ry-cy
        length2 = max(1., vx*vx+vy*vy)
        t = np.clip(((xx-cx)*vx+(yy-cy)*vy)/length2, 0, 1)
        d2 = (xx-cx-t*vx)**2+(yy-cy-t*vy)**2
        cost += 3.*np.exp(-d2/(2*max(1., .06*radius)**2))*t
    seeds = [(p, dict(kind='tongue', tongue_id=i+1,
                      contour_tip=p, contour_roots=[geometry['roots'][i-1], geometry['roots'][i]]))
             for i, p in enumerate(geometry['tips'])]
    # 3..6 evenly spaced core markers: five normally, fewer for tiny bodies.
    count = min(5, max(3, int(mask.sum()/48)))
    phase = math.atan2(geometry['tips'][0][1]-cy, geometry['tips'][0][0]-cx) if seeds else 0.
    core = mask & ((xx-cx)**2+(yy-cy)**2 <= radius**2) & (distance >= .2*radius)
    seed_cx, seed_cy = _nearest(core, geometry['burst_centre'])
    for i in range(count):
        angle = phase+(i+.5)*2*math.pi/count
        p = _nearest(core, [seed_cx+.65*radius*math.cos(angle), seed_cy+.65*radius*math.sin(angle)])
        if all(p != old for old, _ in seeds):
            seeds.append((p, dict(kind='core_wedge', core_seed=p)))
    labels = np.zeros(mask.shape, dtype=np.int32)
    arrival = np.full(mask.shape, np.inf)
    travel = np.full(mask.shape, np.inf)
    queue = []
    descriptions = {}
    for label, (point, desc) in reversed(list(enumerate(seeds, 1))):
        marker = (_tongue_marker(mask, distance, point, desc['contour_roots'])
                  if desc['kind'] == 'tongue' else [point])
        for x, y in marker:
            if labels[y, x] == 0:
                labels[y, x], arrival[y, x], travel[y, x] = label, -math.inf, 0.
                heapq.heappush(queue, (-math.inf, 0., label, y, x))
        descriptions[label] = desc
    h, w = mask.shape
    offsets = [(dy, dx, math.hypot(dx, dy)) for dy in (-1, 0, 1)
               for dx in (-1, 0, 1) if dx or dy]
    while queue:
        level, walked, label, y, x = heapq.heappop(queue)
        if arrival[y, x] != level or travel[y, x] != walked or labels[y, x] != label:
            continue
        for dy, dx, step in offsets:
            ny, nx = y+dy, x+dx
            if not (0 <= ny < h and 0 <= nx < w and mask[ny, nx]):
                continue
            next_walked = walked+step
            next_level = max(level, cost[ny, nx]+2.*next_walked/max(radius, 1.))
            if (next_level, next_walked) < (arrival[ny, nx], travel[ny, nx]):
                arrival[ny, nx], travel[ny, nx], labels[ny, nx] = next_level, next_walked, label
                heapq.heappush(queue, (next_level, next_walked, label, ny, nx))
    return labels, descriptions


def _split_tongues(labels, descriptions, geometry):
    """Split long tongue basins at the narrowest interior axial waist.

    Terminal 20% on either end is excluded: terminal taper is not a waist.
    Choose the narrowest admissible section, including endpoint minima. Width
    counts a one-pixel axial slab; a sigma=1 profile suppresses raster aliasing.
    """
    cx, cy = geometry['core_centre']
    for label, desc in list(descriptions.items()):
        if desc['kind'] != 'tongue':
            continue
        tip = np.asarray(desc['contour_tip'], dtype=float)
        roots = np.asarray(desc['contour_roots'], dtype=float)
        root = roots.mean(axis=0)
        length = float(np.linalg.norm(tip-root))
        desc['tongue_length_px'] = length
        if length <= 1.5*geometry['core_radius_px']:
            continue
        yy, xx = np.where(labels == label)
        if len(xx) < 48:
            continue
        axis = tip-np.array([cx, cy])
        axis /= max(1., np.linalg.norm(axis))
        projection = xx*axis[0]+yy*axis[1]
        bins = np.floor(projection-projection.min()).astype(int)
        width = ndimage.gaussian_filter1d(np.bincount(bins).astype(float), 1.)
        lo, hi = max(1, int(.2*len(width))), min(len(width)-1, int(.8*len(width)))
        if hi <= lo:
            continue
        candidates = list(range(lo, hi+1))
        # Both sides must support non-sliver connected pieces after cutting.
        candidates = [v for v in candidates if (bins <= v).sum() >= 24 and (bins > v).sum() >= 24]
        if not candidates:
            continue
        waist = min(candidates, key=lambda v: (width[v], abs(v-len(width)/2), v))
        new = max(descriptions)+1
        selected = bins > waist
        labels[yy[selected], xx[selected]] = new
        waist_info = dict(axis_xy=axis.tolist(), projection_px=float(projection.min()+waist+.5),
                          width_px=float(width[waist]), axial_bin=waist,
                          admissible_bins=[lo, hi])
        desc.update(kind='tongue_base', waist=waist_info)
        descriptions[new] = {**desc, 'kind': 'tongue_tip'}
    return labels, descriptions


def _connected_merge(labels, descriptions):
    """Split every component, then merge <24-px fragments across longest border."""
    separated = np.zeros_like(labels)
    info = {}
    for old in sorted(descriptions):
        components, n = ndimage.label(labels == old, CONNECTIVITY)
        for i in range(1, n+1):
            new = len(info)+1
            separated[components == i] = new
            info[new] = {**descriptions[old], 'merged_slivers': []}
    while True:
        changed = False
        sizes = np.bincount(separated.ravel())
        for sid in sorted(info, key=lambda i: (sizes[i], i)):
            if sizes[sid] >= 24:
                continue
            mask = separated == sid
            # Count shared pixel-edge contacts, diagonals only as fallback.
            counts = {}
            for structure in (ndimage.generate_binary_structure(2, 1), CONNECTIVITY):
                touches = ndimage.convolve(mask.astype(np.int32), structure.astype(np.int32), mode='constant')
                neighbours = separated[(touches > 0) & ~mask & (separated > 0)]
                weights = touches[(touches > 0) & ~mask & (separated > 0)]
                if len(neighbours):
                    totals = np.bincount(neighbours, weights=weights)
                    counts = {int(k): float(totals[k]) for k in np.flatnonzero(totals)}
                    break
            if not counts:
                info[sid]['unmergeable_sliver'] = 'detached source island; no shared border; coverage preserved'
                continue
            target = max(counts, key=lambda k: (counts[k], sizes[k], -k))
            info[target]['merged_slivers'].append(dict(area_px=int(sizes[sid]), shared_border=counts[target]))
            info[target]['merged_slivers'].extend(info[sid]['merged_slivers'])
            separated[mask] = target
            del info[sid]
            changed = True
            break
        if not changed:
            return separated, info


def decompose(index_map, alpha, centre=None):
    """Connected spatial shards, preserving every source band and alpha byte."""
    bands, alpha = np.asarray(index_map), np.asarray(alpha)
    if (bands.ndim != 2 or bands.dtype != np.uint8 or alpha.dtype != np.uint8
            or bands.shape != alpha.shape or not np.isin(bands, [0, 1, 2, 3]).all()):
        raise ValueError('expected matching uint8 band-index 0..3 and alpha maps')
    origin = _centre(centre, alpha)
    source_labels, n = ndimage.label(alpha > 0, CONNECTIVITY)
    pieces = []
    for component in range(1, n+1):
        body = source_labels == component
        geometry = None
        if body.sum() < 200:
            labels = body.astype(np.int32)
            descriptions = {1: dict(kind='source_island')}
        else:
            distance, geometry = _geometry(body, origin)
            labels, descriptions = _watershed(body, distance, geometry)
            labels, descriptions = _split_tongues(labels, descriptions, geometry)
        labels, descriptions = _connected_merge(labels, descriptions)
        for sid in sorted(descriptions):
            mask = labels == sid
            yy, xx = np.where(mask)
            pivot, centroid, adjusted = _pivot(mask, alpha)
            dx, dy = pivot[0]-origin[0], pivot[1]-origin[1]
            histogram = np.bincount(bands[mask], minlength=4)
            tip = int(np.argmax((xx-origin[0])**2+(yy-origin[1])**2))
            pieces.append(dict(id=len(pieces)+1, mask=mask,
                               dominant_band=int(np.argmax(histogram)),
                               band_histogram={str(i): int(histogram[i]) for i in range(4)},
                               pivot=pivot, coverage_centroid=centroid, pivot_adjusted=adjusted,
                               radial_angle_deg=float(math.degrees(math.atan2(dy, dx)) % 360),
                               radial_distance_px=float(math.hypot(dx, dy)),
                               tip=[int(xx[tip]), int(yy[tip])],
                               area_px=int(mask.sum()), alpha_area_px=float(alpha[mask].sum()/255),
                               bbox=[int(xx.min()), int(yy.min()), int(xx.max()+1), int(yy.max()+1)],
                               source_component=component, geometry=geometry,
                               connected_components=int(ndimage.label(mask, CONNECTIVITY)[1]),
                               **descriptions[sid]))
    return pieces


def _index_rgba(bands, alpha):
    out = np.repeat(BANDS[bands][..., None], 4, axis=2)
    out[..., 3] = alpha
    out[alpha == 0, :3] = 0
    return out


def _contact_sheet(rgba, pieces):
    h, w = rgba.shape[:2]
    swatches = np.array([np.array(colorsys.hsv_to_rgb((i*.61803398875) % 1, .65, .95))*255
                         for i in range(len(pieces))], dtype=np.uint8)
    tint = np.zeros_like(rgba)
    for piece in pieces:
        tint[piece['mask'], :3] = swatches[piece['id']-1]
    tint[..., 3] = rgba[..., 3]
    left = Image.new('RGBA', (w, h), (40, 44, 54, 255))
    left.alpha_composite(Image.fromarray(rgba))
    right = Image.new('RGBA', (w, h), (40, 44, 54, 255))
    right.alpha_composite(Image.fromarray(tint))
    draw = ImageDraw.Draw(right)
    for piece in pieces:
        x, y = piece['pivot']
        draw.text((x, y), str(piece['id']), fill='white', stroke_width=2, stroke_fill='black', anchor='mm')
    sheet = Image.new('RGB', (2*w, h+48), (40, 44, 54))
    sheet.paste(left, (0, 32)); sheet.paste(right, (w, 32))
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), 'Source silhouette / original planes', fill='white')
    draw.text((w+8, 8), 'Spatial shards / piece ID at pivot', fill='white')
    draw.text((8, h+34), 'Distinct colour per shard. All bands travel together. Full canvas; coverage unchanged.', fill='white')
    return sheet


def build(peak_png, out_dir, centre=None, plate='auto'):
    """Write index PNG, masks, contact sheet and versioned T4h manifest.

    Every asset path is relative to pieces.json. Distance fields remain T4h's
    builder-owned output: apply effect_kit.distance_field to each mask PNG,
    then populate the kit's distance_fields map (texture path -> field path).
    """
    source, out = Path(peak_png).resolve(), Path(out_dir).resolve()
    if source == out or source.is_relative_to(out):
        raise ValueError('output overlaps source')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('output directory must be empty')
    isolated = isolate(source, plate)
    rgba = np.asarray(isolated)
    bands, alpha, histogram = quantise(rgba)
    origin = _centre(centre, alpha)
    pieces = decompose(bands, alpha, origin)
    metadata = dict(schema_version=2, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                    source_file=source.name, canvas=[int(rgba.shape[1]), int(rgba.shape[0])],
                    centre=origin, centre_source='explicit' if centre is not None else 'alpha_weighted_centroid',
                    plate_path_used=isolated.info['isolation']['plate_path_used'],
                    isolation=isolated.info['isolation'], band_histogram=histogram,
                    plane_quality=plane_quality(rgba), peak_index='peak_index.png',
                    contact_sheet='contact_sheet.png',
                    conventions=dict(paths='relative to pieces.json', canvas='[width, height]',
                        coverage='alpha > 0; alpha bytes preserved independently from RGB',
                        band_index='per-pixel integer 0..3; RGB = band_index * 85; never use dominant_band as texture colour',
                        band_histogram='keys 0..3 count alpha>0 pixels; dominant_band is the largest bin (lower index tie)',
                        tip='canvas [x,y] mask pixel farthest from burst centre; row-major tie',
                        centroid='alpha-weighted pixel centres; integer coordinates address pixel centres',
                        pivot='canvas [x,y]; nearest pixel uses floor(coordinate + 0.5)',
                        bbox='[left, top, right_exclusive, bottom_exclusive]; PNG remains full canvas',
                        radial_angle_deg='degrees, screen coordinates, +x=0, clockwise positive',
                        sprite_placement='uncentred sprite offset = -pivot; initial position = pivot - centre',
                        connectivity=8, sliver_area_px=24,
                        sliver_merge='longest shared border; 8-connected; detached islands retained and reported, never bridged',
                        segmentation='compact minimax watershed on negative EDT; contour tips + five core seeds; concavity-root ridges; long-tongue waist split',
                        watershed_compactness='2 * geodesic_path_length / core_radius; deterministic row-major ties',
                        distance_fields='T4h builder-owned: effect_kit.distance_field(mask RGBA) per texture'),
                    pieces=[])
    out.mkdir(parents=True, exist_ok=True)
    Image.fromarray(_index_rgba(bands, alpha)).save(out/'peak_index.png')
    for piece in pieces:
        filename = f"piece_{piece['id']:03d}.png"
        mask_alpha = np.where(piece['mask'], alpha, 0).astype(np.uint8)
        Image.fromarray(_index_rgba(bands, mask_alpha)).save(out/filename)
        metadata['pieces'].append({**{k: v for k, v in piece.items() if k != 'mask'}, 'mask': filename})
    _contact_sheet(rgba, pieces).save(out/'contact_sheet.png')
    (out/'pieces.json').write_text(json.dumps(metadata, indent=2, allow_nan=False)+'\n')
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('peak_png', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--centre', nargs=2, type=float)
    parser.add_argument('--plate', choices=('green', 'alpha', 'auto'), default='auto')
    args = parser.parse_args(argv)
    try:
        result = build(args.peak_png, args.out, args.centre, args.plate)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(dict(id='peak_pieces', subject=str(args.peak_png), passed=None,
                          value=dict(piece_count=len(result['pieces']), band_histogram=result['band_histogram'],
                                     isolation=result['isolation'], plane_quality=result['plane_quality']),
                          threshold=None, op='report', unit='mixed', evidence=[str(args.out/'pieces.json')],
                          notes='Decomposition measurements only; acceptance is conductor-owned.'), allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
