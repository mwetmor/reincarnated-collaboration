"""Plate-pixel annotation, exact floor-complement polygons and room assets.

Geometry uses continuous plate coordinates. Raster samples are pixel centres;
cutouts use a one-pixel inward feather, preserving interior RGB and alpha.
No raster approximation is used for collision geometry.
"""
import json
import math
from pathlib import Path
import re
import time

import numpy as np
from PIL import Image

EPS = 1e-9


def _number(value):
    return (not isinstance(value, bool) and isinstance(value, (int, float))
            and math.isfinite(value))


def _cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def _on_segment(p, a, b):
    return (abs(_cross(a, b, p)) <= EPS and
            min(a[0], b[0])-EPS <= p[0] <= max(a[0], b[0])+EPS and
            min(a[1], b[1])-EPS <= p[1] <= max(a[1], b[1])+EPS)


def _intersects(a, b, c, d):
    u, v, s, t = _cross(a, b, c), _cross(a, b, d), _cross(c, d, a), _cross(c, d, b)
    return ((u*v < 0 and s*t < 0) or _on_segment(c, a, b) or
            _on_segment(d, a, b) or _on_segment(a, c, d) or _on_segment(b, c, d))


def _contains(p, polygon):
    inside = False
    for a, b in zip(polygon, polygon[1:]+polygon[:1]):
        if _on_segment(p, a, b):
            return True
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0] < x:
                inside = not inside
    return inside


def _validate(annotation):
    keys = {'plate_size', 'walkable', 'blocked', 'occluders', 'exits', 'spawn', 'figure_height_px'}
    if not isinstance(annotation, dict) or set(annotation) != keys:
        raise ValueError('Annotation must contain exactly the ANNOTATE schema fields')
    size = annotation['plate_size']
    if (not isinstance(size, list) or len(size) != 2 or
            any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in size)):
        raise ValueError('plate_size must be two positive integers')
    w, h = size

    def point(p):
        if (not isinstance(p, list) or len(p) != 2 or not all(_number(v) for v in p)
                or not (0 <= p[0] <= w and 0 <= p[1] <= h)):
            raise ValueError('Point must be finite [x,y] inside the plate rectangle')

    def polygon(poly):
        if not isinstance(poly, list) or len(poly) < 3:
            raise ValueError('Polygon needs at least three vertices, closed implicitly')
        for p in poly:
            point(p)
        if len({tuple(p) for p in poly}) != len(poly):
            raise ValueError('Polygon vertices must be distinct; closure is implicit')
        edges = list(zip(poly, poly[1:]+poly[:1]))
        area = sum(a[0]*b[1]-b[0]*a[1] for a, b in edges)
        if abs(area) <= EPS:
            raise ValueError('Polygon must have positive area')
        for i, (a, b) in enumerate(edges):
            prev = poly[i-1]
            if abs(_cross(prev, a, b)) <= EPS and _on_segment(b, prev, a):
                raise ValueError('Polygon has a backtracking edge')
            for j in range(i+1, len(edges)):
                if j == i+1 or (i == 0 and j == len(edges)-1):
                    continue
                if _intersects(a, b, *edges[j]):
                    raise ValueError('Polygon must be simple (no self-intersections)')

    for name in ('walkable', 'blocked', 'occluders', 'exits'):
        if not isinstance(annotation[name], list):
            raise ValueError(name+' must be a list')
    if not annotation['walkable']:
        raise ValueError('At least one walkable polygon is required')
    for name in ('walkable', 'blocked'):
        for poly in annotation[name]:
            polygon(poly)
    for name, fields in [('occluders', {'id', 'polygon', 'baseline_y'}),
                         ('exits', {'id', 'segment'})]:
        seen = set()
        for item in annotation[name]:
            if not isinstance(item, dict) or set(item) != fields:
                raise ValueError('Invalid '+name+' fields')
            ident = item['id']
            if (not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', ident)
                    or ident in seen):
                raise ValueError('IDs must be unique safe file names within each collection')
            seen.add(ident)
            if name == 'occluders':
                polygon(item['polygon'])
                if not _number(item['baseline_y']) or not 0 <= item['baseline_y'] <= h:
                    raise ValueError('baseline_y must be finite and inside the plate')
            else:
                segment = item['segment']
                if not isinstance(segment, list) or len(segment) != 2:
                    raise ValueError('Exit segment needs exactly two points')
                for p in segment:
                    point(p)
                if segment[0] == segment[1]:
                    raise ValueError('Exit segment must have nonzero length')
    point(annotation['spawn'])
    if (not any(_contains(annotation['spawn'], p) for p in annotation['walkable']) or
            any(_contains(annotation['spawn'], p) for p in annotation['blocked'])):
        raise ValueError('Spawn must lie on walkable, unblocked floor')
    if not _number(annotation['figure_height_px']) or annotation['figure_height_px'] <= 0:
        raise ValueError('figure_height_px must be finite and positive')
    return annotation


def load_annotation(path):
    """Read and validate the ANNOTATE object; malformed geometry raises ValueError."""
    return _validate(json.loads(Path(path).read_text()))


def cut_occluders(plate_png, annotation, out_dir):
    """Return/write cutout records; positions are integer crop top-lefts."""
    _validate(annotation)
    with Image.open(plate_png) as source:
        if list(source.size) != annotation['plate_size']:
            raise ValueError('Plate image size differs from plate_size')
        plate = source.convert('RGBA')
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for item in annotation['occluders']:
        poly = item['polygon']
        x0, y0 = [math.floor(min(p[k] for p in poly)) for k in (0, 1)]
        x1, y1 = [math.ceil(max(p[k] for p in poly)) for k in (0, 1)]
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(float)
        xx += 0.5
        yy += 0.5
        inside = np.zeros(xx.shape, dtype=bool)
        distance2 = np.full(xx.shape, np.inf)
        for a, b in zip(poly, poly[1:]+poly[:1]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            if dy:
                inside ^= ((a[1] > yy) != (b[1] > yy)) & (xx < a[0]+(yy-a[1])*dx/dy)
            t = np.clip(((xx-a[0])*dx+(yy-a[1])*dy)/(dx*dx+dy*dy), 0, 1)
            distance2 = np.minimum(distance2, (xx-a[0]-t*dx)**2+(yy-a[1]-t*dy)**2)
        pixels = np.array(plate.crop((x0, y0, x1, y1)))
        feather = np.minimum(np.sqrt(distance2), 1.0)*inside
        pixels[:, :, 3] = np.rint(pixels[:, :, 3]*feather).astype(np.uint8)
        filename = item['id']+'.png'
        Image.fromarray(pixels).save(out/filename)
        records.append({'file': filename, 'position': [x0, y0], 'baseline_y': item['baseline_y']})
    (out/'occluders.json').write_text(json.dumps(records, indent=2, allow_nan=False)+'\n')
    return records


def collision(annotation):
    """Blocked polygons plus an exact trapezoid decomposition of non-floor.

    Split at every vertex and inter-polygon edge crossing. Within each open
    horizontal slab edge order is fixed, so merging walkable x intervals and
    taking their complement gives convex polygons, including islands/holes.
    Shared boundaries have zero area and remain collision boundaries.
    """
    _validate(annotation)
    w, h = annotation['plate_size']
    polygons = annotation['walkable']
    edges = [edge for p in polygons for edge in zip(p, p[1:]+p[:1])]
    levels = {0.0, float(h)} | {float(p[1]) for poly in polygons for p in poly}
    for i, (a, b) in enumerate(edges):
        dx, dy = b[0]-a[0], b[1]-a[1]
        for c, d in edges[i+1:]:
            ex, ey = d[0]-c[0], d[1]-c[1]
            den = dx*ey-dy*ex
            if abs(den) <= EPS:
                continue
            t = ((c[0]-a[0])*ey-(c[1]-a[1])*ex)/den
            u = ((c[0]-a[0])*dy-(c[1]-a[1])*dx)/den
            if 0 < t < 1 and 0 < u < 1:
                levels.add(a[1]+t*dy)

    def x_at(edge, y):
        a, b = edge
        return a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])

    result = [[list(p) for p in poly] for poly in annotation['blocked']]
    levels = sorted(levels)
    left, right = ([0, 0], [0, h]), ([w, 0], [w, h])
    for y0, y1 in zip(levels, levels[1:]):
        if y1-y0 <= EPS:
            continue
        mid = (y0+y1)/2
        intervals = []
        for poly in polygons:
            active = [e for e in zip(poly, poly[1:]+poly[:1])
                      if min(e[0][1], e[1][1]) < mid < max(e[0][1], e[1][1])]
            active.sort(key=lambda e: x_at(e, mid))
            intervals.extend(zip(active[::2], active[1::2]))
        intervals.sort(key=lambda pair: x_at(pair[0], mid))
        merged = []
        for lo, hi in intervals:
            if merged and x_at(lo, mid) <= x_at(merged[-1][1], mid)+EPS:
                if x_at(hi, mid) > x_at(merged[-1][1], mid):
                    merged[-1][1] = hi
            else:
                merged.append([lo, hi])
        cursor = left
        gaps = []
        for lo, hi in merged:
            gaps.append((cursor, lo))
            cursor = hi
        gaps.append((cursor, right))
        for lo, hi in gaps:
            if x_at(hi, mid)-x_at(lo, mid) <= EPS:
                continue
            vertices = [[max(0.0, min(float(w), x_at(e, y))), y]
                        for e, y in [(lo, y0), (hi, y0), (hi, y1), (lo, y1)]]
            clean = []
            for p in vertices:
                if not clean or math.dist(p, clean[-1]) > EPS:
                    clean.append(p)
            if len(clean) > 1 and math.dist(clean[0], clean[-1]) <= EPS:
                clean.pop()
            if len(clean) >= 3:
                result.append(clean)
    return result


def shadow_texture(out_png, w=64, h=20):
    """Write a black soft radial ellipse, centre alpha round(0.45*255)."""
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 3 for v in (w, h)):
        raise ValueError('Shadow dimensions must be integers >= 3')
    yy, xx = np.mgrid[:h, :w]
    radius2 = ((xx-(w-1)/2)/((w-1)/2))**2 + ((yy-(h-1)/2)/((h-1)/2))**2
    alpha = np.maximum(1-radius2, 0)**2
    alpha *= 0.45/alpha.max()
    pixels = np.zeros((h, w, 4), dtype=np.uint8)
    pixels[:, :, 3] = np.rint(alpha*255).astype(np.uint8)
    out = Path(out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pixels).save(out)
    return out


def _walkable_grid(annotation, cell_size):
    """Conservative full-cell raster of the floor union minus blocked union.

    The existing exact complement decomposition preserves overlapping walkable
    polygons and shared edges. Rasterize its obstacles by centre membership
    plus segment/open-cell intersection: even sub-cell holes and narrow gaps
    are excluded. A cell touching only an obstacle boundary remains eligible;
    the returned rectangle is subsequently inset by a whole cell.
    Partial cells at the right/bottom plate edges are discarded.
    """
    w, h = annotation['plate_size']
    rows, cols = h // cell_size, w // cell_size
    grid = np.ones((rows, cols), dtype=bool)
    for poly in collision(annotation):
        x0 = max(0, math.floor(min(p[0] for p in poly) / cell_size))
        y0 = max(0, math.floor(min(p[1] for p in poly) / cell_size))
        x1 = min(cols, math.ceil(max(p[0] for p in poly) / cell_size))
        y1 = min(rows, math.ceil(max(p[1] for p in poly) / cell_size))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(float)
        xx *= cell_size
        yy *= cell_size
        cx, cy = xx + cell_size / 2, yy + cell_size / 2
        inside = np.zeros(xx.shape, dtype=bool)
        boundary = np.zeros(xx.shape, dtype=bool)
        for a, b in zip(poly, poly[1:] + poly[:1]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            if dy:
                inside ^= ((a[1] > cy) != (b[1] > cy)) & (cx < a[0] + (cy-a[1])*dx/dy)
            # Clip the edge to each open cell. This catches obstacles too
            # small to contain a sample centre, without blocking shared edges.
            low = np.zeros(xx.shape)
            high = np.ones(xx.shape)
            valid = np.ones(xx.shape, dtype=bool)
            for origin, delta, coord in ((a[0], dx, xx), (a[1], dy, yy)):
                if delta == 0:
                    valid &= (origin > coord) & (origin < coord + cell_size)
                else:
                    first = (coord-origin)/delta
                    last = (coord+cell_size-origin)/delta
                    low = np.maximum(low, np.minimum(first, last))
                    high = np.minimum(high, np.maximum(first, last))
            boundary |= valid & (low < high)
        grid[y0:y1, x0:x1] &= ~(inside | boundary)
    return grid


def _maximal_rectangle(grid):
    """Largest all-true rectangle [left,top,right,bottom], O(rows*cols).

    Bounds are half-open cell indices. Ties use (top,left,bottom,right), so
    traversal, polygon ordering and winding never select a random winner.
    """
    rows, cols = grid.shape
    heights = [0] * cols
    best, best_area = None, 0
    for row in range(rows):
        for col in range(cols):
            heights[col] = heights[col] + 1 if grid[row, col] else 0
        stack = []
        for col in range(cols + 1):
            height = heights[col] if col < cols else 0
            start = col
            while stack and stack[-1][1] > height:
                left, previous = stack.pop()
                area = previous * (col-left)
                candidate = (row+1-previous, left, row+1, col)
                if area > best_area or (area == best_area and (best is None or candidate < best)):
                    best, best_area = candidate, area
                start = left
            if height and (not stack or stack[-1][1] < height):
                stack.append((start, height))
    if best is None:
        raise ValueError('No positive-area walkable rectangle on the grid')
    top, left, bottom, right = best
    return [left, top, right, bottom]


def largest_walkable_rectangle(annotation, cell_size=8, report=None):
    """Return an inset grid rectangle [x0,y0,x1,y1] in plate pixels.

    Rasterize full cells, select the maximum by a histogram/stack scan, then
    shrink every side by one cell. No LP/optimizer or per-polygon corridor
    enumeration. The list return is backward compatible; optional ``report``
    receives cells (total grid count), area_px2 (after inset), wall_s (including
    validation/rasterization), and explicit grid/before-inset measurements.
    A maximum less than three cells wide/high cannot survive the required
    inset and raises ValueError; no unsafe fallback or degenerate rectangle.
    """
    started = time.monotonic()
    if isinstance(cell_size, bool) or not isinstance(cell_size, int) or cell_size <= 0:
        raise ValueError('cell_size must be a positive integer in plate pixels')
    if report is not None and not isinstance(report, dict):
        raise ValueError('report must be a dict or None')
    _validate(annotation)
    grid = _walkable_grid(annotation, cell_size)
    left, top, right, bottom = _maximal_rectangle(grid)
    if right-left <= 2 or bottom-top <= 2:
        raise ValueError('Largest walkable rectangle cannot survive one-cell inset')
    rectangle = [(left+1)*cell_size, (top+1)*cell_size,
                 (right-1)*cell_size, (bottom-1)*cell_size]
    if report is not None:
        report.update(cell_size=cell_size, cells=int(grid.size),
                      grid_shape=list(grid.shape), walkable_cells=int(grid.sum()),
                      rectangle_cells=(right-left-2)*(bottom-top-2),
                      unshrunk_rectangle=[v*cell_size for v in (left, top, right, bottom)],
                      unshrunk_area_px2=(right-left)*(bottom-top)*cell_size**2,
                      area_px2=(rectangle[2]-rectangle[0])*(rectangle[3]-rectangle[1]),
                      wall_s=time.monotonic()-started)
    return rectangle
