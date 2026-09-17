"""Build an indexed, painted effect kit from a dict or JSON path.

Paths in a JSON definition resolve beside that JSON (dict paths resolve from
cwd). A phase's sheet identifies its source PNG; frame.file is an explicit
PNG, relative to the definition, not an implicit atlas rectangle. Repeating a
file is supported. No grid geometry is guessed. Cast/travel/impact are required;
residual and individual layers may be omitted. Travel defaults: 520 px/s,
streak=False. Omitted layers are disabled. Holds are integer 60 Hz ticks.
T4a material.palette is four RGBA colours for indices 0/85/170/255. PNG alpha
is independent coverage. Native PNG dimensions are retained; phase_scale is
runtime geometry with LINEAR filtering. tint/white_core_keep/pixel_scale kits
are rejected. Private _tint helpers remain diagnostic-only for old byte locks.
"""
import copy
import colorsys
import hashlib
import json
import math
from pathlib import Path
import re
import random
import time

import numpy as np
from PIL import Image

PHASES = {'cast': 'flare', 'travel': 'travel', 'impact': 'impact', 'residual': 'residual'}
TOP = {'name', 'element', 'element_class', 'tint', 'phases', 'layers', 'ground_squash', 'pixel_scale', 'phase_scale', 'material', 'distance_fields', 'pierce', 'pieces', 'screen_px', 'erode_noise', 'skill_spec', 'travel_primitives', 'key_states', 'impact_binding', 'decal_s', 'orb', 'g1'}
LAYER_KEYS = {
    'core': {'band', 'alpha', 'blur_px'},
    'contact_light': {'lerp', 'frames'},
    'shimmer': {'amplitude_px', 'seconds'},
    'glow': {'alpha', 'scale', 'peak'}, 'floor_light': {'duration_s', 'radius_px', 'curve', 'tint', 'alpha'},
    'cast': {'muzzle_puff', 'floor_light'}, 'travel': {'flicker_frames', 'trail', 'erode_noise', 'core', 'halo', 'boil', 'smear', 'eruption'},
    'flash': {'duration_s', 'alpha', 'scale_from', 'scale_to'},
    'decal': {'file', 'duration_s'}, 'hitstop': {'duration_s', 'time_scale'},
    'shake': {'distance', 'duration_s'},
    'particles': {'texture', 'amount', 'lifetime_s', 'velocity_px_s', 'direction', 'spread_deg'},
}


def _keys(value, allowed, required, label):
    if not isinstance(value, dict) or set(value)-allowed or not required <= set(value):
        raise ValueError(label+' has missing or unknown keys')


def _number(value, low, high, label, integer=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or not low <= value <= high
            or (integer and not isinstance(value, int))):
        raise ValueError(label+' has invalid numeric value')


def _png(value, root, grayscale=False, confined=False):
    if (not isinstance(value, str) or not value or '\\' in value
            or any(ord(c) < 32 or c == '"' for c in value)):
        raise ValueError('Invalid PNG path')
    path = (root/value).resolve()
    if confined and (Path(value).is_absolute() or not path.is_relative_to(root)):
        raise ValueError('Kit asset escapes its directory')
    if not path.is_file() or path.suffix.lower() != '.png':
        raise ValueError('Missing PNG: '+str(path))
    try:
        with Image.open(path) as im:
            if im.format != 'PNG':
                raise ValueError('Asset must be PNG')
            pixels = np.array(im.convert('RGBA'))
            if grayscale:
                rgb = pixels[..., :3][pixels[..., 3] > 0]
                if np.any(rgb[:, 0] != rgb[:, 1]) or np.any(rgb[:, 1] != rgb[:, 2]):
                    raise ValueError('Painted sheets and frames must be greyscale')
    except (OSError, SyntaxError) as exc:
        raise ValueError('Unreadable PNG: '+str(path)) from exc
    return path


# T4a: render state is selected at resource creation; Godot render_mode cannot
# be changed by a uniform. The fragment program is shared by all variants.
MATERIAL_DEFAULTS = {'blend_mode': 'MIX', 'light_participation': False,
                     'erode': 0.0, 'dissolve': 0.0}


LEGACY_DISSOLVE_ORDER = [[3], [2], [1], [0]]


def dissolve_thresholds(order=None):
    """Removal groups use legacy step times; omission preserves legacy arithmetic."""
    if order is None:
        order = LEGACY_DISSOLVE_ORDER
    if (not isinstance(order, list) or not order
            or any(not isinstance(group, list) or not group for group in order)):
        raise ValueError('dissolve_order must partition {0,1,2,3} into nonempty band groups')
    bands = [band for group in order for band in group]
    if (any(type(band) is not int for band in bands)
            or sorted(bands) != [0, 1, 2, 3]):
        raise ValueError('dissolve_order must partition {0,1,2,3}')
    if order == LEGACY_DISSOLVE_ORDER:
        return [1-band/6 for band in range(4)]
    thresholds = [0.0]*4
    for i, group in enumerate(order):
        for band in group:
            thresholds[band] = 1-(3-i)/6
    return thresholds


def validate_material(material):
    """Four low-to-high RGBA bands; coverage is always source alpha."""
    _keys(material, {'palette', 'dissolve_order', 'erode_outside_in', 'erode_noise', *MATERIAL_DEFAULTS}, {'palette'}, 'material')
    if 'dissolve_order' in material and material['dissolve_order'] is None:
        raise ValueError('dissolve_order must be a list of band groups')
    dissolve_thresholds(material.get('dissolve_order'))
    if not isinstance(material.get('erode_outside_in', False), bool):
        raise ValueError('erode_outside_in must be boolean')
    palette = material['palette']
    if not isinstance(palette, list) or len(palette) != 4:
        raise ValueError('material.palette requires four RGBA colours')
    for colour in palette:
        if not isinstance(colour, list) or len(colour) != 4:
            raise ValueError('material.palette requires four RGBA colours')
        for v in colour: _number(v, 0, 1, 'material.palette')
    if material.get('blend_mode', 'MIX') not in ('MIX', 'ADD', 'PREMULT_ALPHA'):
        raise ValueError('material.blend_mode must be MIX, ADD or PREMULT_ALPHA')
    if not isinstance(material.get('light_participation', False), bool):
        raise ValueError('material.light_participation must be boolean')
    for name in ('erode', 'dissolve', 'erode_noise'):
        _number(material.get(name, 0), 0, 1, 'material.'+name)
    return {**MATERIAL_DEFAULTS, **copy.deepcopy(material)}


def _reject_retired(data):
    if isinstance(data, dict):
        if 'white_core_keep' in data:
            raise ValueError('white_core_keep is retired; supply four explicit material.palette RGBA entries')
        for value in data.values(): _reject_retired(value)
    elif isinstance(data, list):
        for value in data: _reject_retired(value)


def distance_field(rgba):
    """Centre-out coverage quantiles, encoded as an independent 8-bit texture.

    Equal-radius pixels share a threshold. Coverage-weighted ranks make erode
    approximately a removed-alpha fraction even for irregular painted masks.
    The centre is the alpha centroid; disconnected components share this centre.
    Zero and one are reserved for the exact no-erosion/all-erosion endpoints.
    """
    rgba = np.asarray(rgba)
    if rgba.ndim != 3 or rgba.shape[2] != 4 or rgba.dtype != np.uint8:
        raise ValueError('distance_field requires uint8 HxWx4 RGBA')
    alpha = rgba[..., 3].astype(float)
    out = np.full(alpha.shape, 255, dtype=np.uint8)
    visible = alpha > 0
    total = alpha.sum()
    if not total: return out
    y, x = np.indices(alpha.shape)
    cx, cy = (x*alpha).sum()/total, (y*alpha).sum()/total
    radii = np.round(((x-cx)**2+(y-cy)**2)[visible], 10)
    _, inverse = np.unique(radii, return_inverse=True)
    weights = np.bincount(inverse, weights=alpha[visible])
    ranks = (np.cumsum(weights)-weights/2)/total
    out[visible] = np.clip(np.rint(ranks[inverse]*255), 1, 254).astype(np.uint8)
    return out


def piece_erode_noise(data):
    """V2 override order: pieces, kit, material; omission is byte-neutral zero."""
    pieces = data.get('pieces', {})
    if pieces.get('template') not in ('burst_v2', 'burst_v1r'):
        return 0.0
    return pieces.get('erode_noise', data.get('erode_noise', data['material'].get('erode_noise', 0.0)))


def erosion_noise_texture(rgba):
    """One whole-canvas RGB data texture: periodic value noise + painted weight.

    Three smoothstep-interpolated octaves (8/16/32 cells, weights 1/.5/.25),
    fixed local seed; no global RNG, frame, piece ID or runtime dependence.
    R is signed noise encoded in 0..255; G is a softly joined band weight.
    Extend paint across transparent pixels before smoothing, so shard edges
    never contribute dark padding to the erosion field. Call on the PEAK.
    """
    from scipy import ndimage
    rgba = np.asarray(rgba)
    h, w = rgba.shape[:2]
    rng = np.random.default_rng(17)
    yy, xx = np.indices((h, w), dtype=float)
    value = np.zeros((h, w), dtype=float)
    for cells, weight in ((8, 1.0), (16, .5), (32, .25)):
        grid = rng.uniform(-1, 1, (cells, cells))
        x, y = xx*cells/w, yy*cells/h
        ix, iy = x.astype(int), y.astype(int)
        fx, fy = x-ix, y-iy
        fx, fy = fx*fx*(3-2*fx), fy*fy*(3-2*fy)
        a = grid[iy % cells, ix % cells]*(1-fx) + grid[iy % cells, (ix+1) % cells]*fx
        b = grid[(iy+1) % cells, ix % cells]*(1-fx) + grid[(iy+1) % cells, (ix+1) % cells]*fx
        value += weight*(a*(1-fy)+b*fy)
    value /= 1.75
    # Fixed gain retains amplitude across canvases; no content-dependent tuning.
    value = np.clip(value*1.5, -1, 1)
    band = np.floor(rgba[..., 0].astype(float)/85+.5)/3
    visible = rgba[..., 3] > 0
    if visible.any() and not visible.all():
        nearest = ndimage.distance_transform_edt(~visible, return_distances=False, return_indices=True)
        band = band[tuple(nearest)]
    band = ndimage.gaussian_filter(band, 2.0, mode='wrap')
    result = np.zeros((h, w, 3), np.uint8)
    result[..., 0] = np.rint((value+1)*127.5).astype(np.uint8)
    result[..., 1] = np.rint(band*255).astype(np.uint8)
    return result


def erosion_distance(rgba, distance, erode_noise=0.0, noise_texture=None):
    """Outside-in resistance; CPU samples the exact exported data texels.

    A shared peak texture is required when evaluating individual shards. The
    omitted texture is useful for whole-peak callers and generated fixtures.
    """
    _number(erode_noise, 0, 1, 'erode_noise')
    value = np.asarray(distance)/255
    if not erode_noise:
        return value
    texture = erosion_noise_texture(rgba) if noise_texture is None else np.asarray(noise_texture)
    if texture.shape != (*np.shape(distance), 3) or texture.dtype != np.uint8:
        raise ValueError('noise_texture must be matching uint8 HxWx3 whole-body data')
    resistance = .5*(texture[..., 0]/255*2-1) + .5*(texture[..., 1]/255)
    return value - erode_noise*resistance


def residue_entry(rgba, field, fraction, erode_noise=0.0, noise_texture=None):
    """Select a whole-band/distance threshold against HOLD support, before dissolve."""
    eligible = np.asarray(rgba)[..., 3] > 0
    target = fraction * np.count_nonzero(eligible)
    if not erode_noise:
        # Preserve the legacy histogram and half-bin arithmetic exactly.
        cumulative = np.cumsum(np.bincount(field[eligible], minlength=256))
        cutoff = int(np.argmin(abs(cumulative-target)))
        outer, area = (cutoff+.5)/255, int(cumulative[cutoff])
    else:
        # Merge arithmetic-near ties before choosing an inter-bin midpoint.
        # Six decimals are finer than texture precision, above float32 noise.
        resistance = np.round(erosion_distance(rgba, field, erode_noise, noise_texture)[eligible], 6)
        values, counts = np.unique(resistance, return_counts=True)
        cumulative = np.cumsum(counts)
        cutoff = int(np.argmin(abs(cumulative-target)))
        # Midpoint avoids CPU/GPU equality differences; keep the complete tie.
        following = values[cutoff+1] if cutoff+1 < len(values) else values[cutoff]+1/255
        outer = float((values[cutoff]+following)/2)
        area = int(cumulative[cutoff])
    return dict(residue_erode=1-outer, residue_outer=outer,
                predicted_stationary_residue_area_px=area,
                source_peak_area_px=int(np.count_nonzero(eligible)),
                residue_denominator='maximum hold-frame body alpha>0 coverage')


def material_pixels(rgba, palette, distance=None, erode=0.0, dissolve=0.0,
                    blend_mode='MIX', dark_duplicate=False, dissolve_order=None, erode_outside_in=False, erode_noise=0.0, noise_texture=None):
    """CPU reference only, never represented as a Godot rendered-frame proof."""
    validate_material(dict(palette=palette, erode=erode, dissolve=dissolve, blend_mode=blend_mode, erode_noise=erode_noise))
    rgba = np.asarray(rgba)
    if rgba.ndim != 3 or rgba.shape[2] != 4 or rgba.dtype != np.uint8:
        raise ValueError('material_pixels requires uint8 HxWx4 RGBA')
    bands = np.floor(rgba[..., 0].astype(float)/85+.5).astype(int)
    result = np.asarray(palette, dtype=float)[bands].copy()
    result[..., 3] *= rgba[..., 3]/255
    if erode:
        if distance is None or np.shape(distance) != rgba.shape[:2]:
            raise ValueError('erode requires a matching distance texture')
        value = erosion_distance(rgba, distance, erode_noise, noise_texture) if erode_outside_in else np.asarray(distance)/255
        keep = (value <= 1-erode) if erode_outside_in else (value >= erode)
        result[..., 3] *= keep & (erode < 1)
    result[..., 3] *= dissolve < np.asarray(dissolve_thresholds(dissolve_order))[bands]
    if dark_duplicate: result[..., :3] = 0
    if blend_mode == 'PREMULT_ALPHA': result[..., :3] *= result[..., 3, None]
    return np.clip(np.rint(result*255), 0, 255).astype(np.uint8)


def shader_source(blend_mode='MIX', light_participation=False, dissolve_order=None, erode_outside_in=False, erode_noise=0.0):
    """Compatibility variants use only CanvasItem fragment operations."""
    validate_material({'palette': [[0, 0, 0, 1]]*4,
                       'blend_mode': blend_mode, 'light_participation': light_participation, 'erode_noise': erode_noise})
    modes = {'MIX': 'blend_mix', 'ADD': 'blend_add', 'PREMULT_ALPHA': 'blend_premul_alpha'}
    mode = modes[blend_mode]+('' if light_participation else ', unshaded')
    source = Path(__file__).with_name('vfx_material.gdshader').read_text()
    if not (erode_outside_in and erode_noise):
        source = source.replace('uniform float erode_noise : hint_range(0.0, 1.0) = 0.0;\n', '')
        source = source.replace('uniform sampler2D erosion_noise_texture : filter_linear, repeat_enable;\n', '')
        source = source.replace('        vec2 resistance = texture(erosion_noise_texture, UV).rg;\n        distance_value -= erode_noise * (0.5 * (2.0 * resistance.r - 1.0) + 0.5 * resistance.g);\n', '')
    if not erode_outside_in:
        # Strip the opt-in branch so legacy exported shaders stay byte-identical.
        source = source.replace('uniform bool erode_outside_in = false;\n', '')
        source = source.replace('    if (erode_outside_in) {\n        if (erode > 0.0 && (erode >= 1.0 || distance_value > 1.0 - erode)) { coverage = 0.0; }\n    } else {\n        if (erode > 0.0 && (erode >= 1.0 || distance_value < erode)) { coverage = 0.0; }\n    }', '    if (erode > 0.0 && (erode >= 1.0 || distance_value < erode)) { coverage = 0.0; }')
    thresholds = dissolve_thresholds(dissolve_order)
    if dissolve_order is not None and dissolve_order != LEGACY_DISSOLVE_ORDER:
        # A separate shader variant keeps every legacy shader byte unchanged.
        table = 'vec4(' + ', '.join(format(v, '.17g') if v % 1 else format(v, '.1f') for v in thresholds) + ')'
        source = source.replace('(1.0 - band / 6.0)', table+'[int(band)]')
        source = source.replace('// Hold until 0.5, then remove band 3, 2, 1, 0 at 0.5, 2/3, 5/6, 1.',
                                '// Per-kit band-group removal thresholds, indexed by band.')
    source = source.replace('render_mode blend_mix, unshaded;', 'render_mode '+mode+';')
    return source.replace('const bool PREMULTIPLIED = false;',
                          'const bool PREMULTIPLIED = '+str(blend_mode == 'PREMULT_ALPHA').lower()+';')



def write_vfx_material(out, resource, material, distance_texture, dark_duplicate=False, noise_texture=None, noise_uv_transform=None):
    """Write a ShaderMaterial and its fixed-blend/light shader variant.

    Paths are project-relative; the distance texture must already exist.
    Material uniforms can be edited/tweened after instantiation. To change
    blend/light state select another material produced by this function.
    """
    out = Path(out).resolve()
    material = validate_material(material)
    if not isinstance(dark_duplicate, bool):
        raise ValueError('dark_duplicate must be boolean')
    target = out/resource
    if (not target.resolve().is_relative_to(out) or target.suffix != '.tres'
            or any(c in str(resource) for c in ('"', '\\', '\n', '\r'))):
        raise ValueError('material resource must be a confined .tres path')
    field = _png(distance_texture, out, confined=True)
    mode, lit = material['blend_mode'], material['light_participation']
    shader = target.parent/f'vfx_material_{mode.lower()}_{"lit" if lit else "unlit"}.gdshader'
    order = material.get('dissolve_order')
    if order is not None and order != LEGACY_DISSOLVE_ORDER:
        suffix = hashlib.sha256(json.dumps(order).encode()).hexdigest()[:12]
        shader = shader.with_name(shader.stem+'_order_'+suffix+shader.suffix)
    if material.get('erode_outside_in', False):
        shader = shader.with_name(shader.stem+'_outside_in'+shader.suffix)
    noise = material.get('erode_noise', 0.0) if material.get('erode_outside_in', False) else 0.0
    if noise:
        shader = shader.with_name(shader.stem+'_noise'+shader.suffix)
    if noise_uv_transform is not None:
        if not noise or len(noise_uv_transform) != 4 or not all(math.isfinite(v) for v in noise_uv_transform):
            raise ValueError('noise_uv_transform requires noise and four finite components')
        shader = shader.with_name(shader.stem+'_boil'+shader.suffix)
    shader_rel = shader.relative_to(out).as_posix()
    target.parent.mkdir(parents=True, exist_ok=True)
    source = shader_source(mode, lit, order, material.get('erode_outside_in', False), noise)
    if noise_uv_transform is not None:
        source = source.replace('uniform bool dark_duplicate',
            'uniform vec2 noise_uv_scale = vec2(1.0);\nuniform vec2 noise_uv_origin = vec2(0.0);\nuniform vec2 noise_uv_offset = vec2(0.0);\nuniform bool dark_duplicate')
        source = source.replace('texture(erosion_noise_texture, UV)',
            'texture(erosion_noise_texture, UV * noise_uv_scale + noise_uv_origin - noise_uv_offset)')
    shader.write_text(source)
    lines = ['[gd_resource type="ShaderMaterial" load_steps=3 format=3]',
             f'[ext_resource type="Shader" path="res://{shader_rel}" id="Shader"]',
             f'[ext_resource type="Texture2D" path="res://{field.relative_to(out).as_posix()}" id="Distance"]',
             '[resource]', 'resource_local_to_scene = true', 'shader = ExtResource("Shader")',
             'shader_parameter/distance_texture = ExtResource("Distance")']
    for i, colour in enumerate(material['palette']):
        lines.append(f'shader_parameter/palette_{i} = Color('+', '.join(format(float(v), '.12g') for v in colour)+')')
    for name in ('erode', 'dissolve'):
        lines.append('shader_parameter/'+name+' = '+repr(float(material[name])))
    if material.get('erode_outside_in', False):
        lines.append('shader_parameter/erode_outside_in = true')
    if noise:
        if noise_texture is None:
            raise ValueError('erode_noise requires a whole-body noise_texture')
        noise_path = _png(noise_texture, out, confined=True)
        with Image.open(noise_path) as a, Image.open(field) as b:
            if a.mode != 'RGB' or (a.size != b.size and noise_uv_transform is None):
                raise ValueError('noise_texture must be RGB and match the whole-body distance')
        lines[0] = '[gd_resource type="ShaderMaterial" load_steps=4 format=3]'
        lines.insert(3, f'[ext_resource type="Texture2D" path="res://{noise_path.relative_to(out).as_posix()}" id="Noise"]')
        lines.append('shader_parameter/erosion_noise_texture = ExtResource("Noise")')
        lines.append('shader_parameter/erode_noise = '+repr(float(noise)))
        if noise_uv_transform is not None:
            for key, values in [('scale', noise_uv_transform[:2]), ('origin', noise_uv_transform[2:])]:
                lines.append('shader_parameter/noise_uv_'+key+' = Vector2('+', '.join(map(str, values))+')')
    lines.append('shader_parameter/dark_duplicate = '+str(dark_duplicate).lower())
    target.write_text('\n'.join(lines)+'\n')
    return target


MATERIAL_BINDING_SCRIPT = '''
# ShaderMaterial instances belong to individual sprites, including duplicates.
# A new animation frame always selects its own distance field.
static func bind(node: CanvasItem, fields: Dictionary) -> void:
    node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    if not node.material is ShaderMaterial:
        return
    node.material = node.material.duplicate()
    if node is AnimatedSprite2D:
        var animated: AnimatedSprite2D = node as AnimatedSprite2D
        animated.frame_changed.connect(update.bind(node, fields))
        animated.animation_changed.connect(update.bind(node, fields))
    update(node, fields)

static func update(node: CanvasItem, fields: Dictionary) -> void:
    var texture: Texture2D
    if node is AnimatedSprite2D:
        var animated: AnimatedSprite2D = node as AnimatedSprite2D
        texture = animated.sprite_frames.get_frame_texture(animated.animation, animated.frame)
    elif node is Sprite2D:
        texture = (node as Sprite2D).texture
    elif node is CPUParticles2D:
        texture = (node as CPUParticles2D).texture
    if texture != null and fields.has(texture.resource_path):
        var paint: ShaderMaterial = node.material as ShaderMaterial
        paint.set_shader_parameter("distance_texture", load(fields[texture.resource_path]))

static func bind_tree(node: Node, fields: Dictionary) -> void:
    if node is CanvasItem:
        bind(node, fields)
    for child in node.get_children():
        bind_tree(child, fields)
'''

PIECES_DEFAULTS = {'hold_frames': 2, 'base_speed_px_s': 1400.0,
                   'residue_s': 0.6, 'residue_fraction': 0.2, 'seed': 1}


def piece_motion(seed, piece_id):
    """Portable per-piece samples, independent of order and global RNG state.

    GDScript uses the same SHA256 text and unsigned 32-bit divisions. The
    scale sample requests a native-pixel step, not a continuously scaled tail.
    """
    digest = hashlib.sha256(f'{seed}:{piece_id}'.encode('ascii')).hexdigest()
    samples = [int(digest[i:i+8], 16)/4294967295 for i in (0, 8, 16)]
    return {'speed_factor': .6+.8*samples[0],
            'rotation_deg': -30+60*samples[1], 'scale_delta': -.08+.16*samples[2]}


def validate_piece_stretch(value):
    """Opt-in rooted stretch; omission retains the original template bytes."""
    _keys(value, {'along', 'across'}, {'along', 'across'}, 'pieces.stretch')
    along = value['along']
    if not isinstance(along, list) or len(along) != 2:
        raise ValueError('pieces.stretch.along requires an ascending pair')
    for v in along: _number(v, 1.0, 2.6, 'pieces.stretch.along')
    if along[0] > along[1]:
        raise ValueError('pieces.stretch.along requires an ascending pair')
    _number(value['across'], .7, 1.0, 'pieces.stretch.across')
    return value


def piece_stretch(seed, piece_id, stretch=None):
    """Stable, order-independent v2 samples; v1 sampling is unchanged."""
    digest = hashlib.sha256(f'{seed}:{piece_id}'.encode('ascii')).hexdigest()
    bounds = validate_piece_stretch(stretch)['along'] if stretch is not None else [2.0, 2.5]
    return {'along': bounds[0] + (bounds[1]-bounds[0]) * int(digest[:8], 16) / 4294967295,
            'rotation_deg': -10 + 20 * int(digest[8:16], 16) / 4294967295}


def piece_geometry(record, source_root):
    """Roots and axes from original masks; no segmentation or mask edits.

    Core membership takes precedence over the dominant-band tongue heuristic.
    The largest inscribed circle is measured on alpha support with an exterior
    zero border, including when a synthetic fixture touches its canvas edge.
    """
    from scipy import ndimage
    with Image.open(Path(source_root)/record['peak_index']) as image:
        peak = np.asarray(image.convert('RGBA'))
    edt = ndimage.distance_transform_edt(np.pad(peak[..., 3] > 0, 1))[1:-1, 1:-1]
    cy, cx = np.unravel_index(np.argmax(edt), edt.shape)
    radius = float(edt[cy, cx])
    centre = np.asarray(record['centre'], dtype=float)
    items = []
    for piece in record['pieces']:
        with Image.open(Path(source_root)/piece['mask']) as image:
            pixels = np.asarray(image.convert('RGBA'))
        ys, xs = np.nonzero(pixels[..., 3])
        squared = (xs-centre[0])**2 + (ys-centre[1])**2
        near = int(np.argmin(squared))
        root = np.array([xs[near], ys[near]], dtype=float)
        tip = np.asarray(piece.get('tip', [xs[np.argmax(squared)], ys[np.argmax(squared)]]), dtype=float)
        axis = tip-root
        angle = math.atan2(axis[1], axis[0]) if np.any(axis) else 0.0
        core = math.hypot(piece['pivot'][0]-cx, piece['pivot'][1]-cy) <= radius
        items.append({**copy.deepcopy(piece), 'root': root.tolist(),
                      'axis_radians': angle, 'core': core,
                      'animated': piece['area_px'] >= 48})
    return {'core_centre': [int(cx), int(cy)], 'core_radius_px': radius,
            'pieces': items}



def load_interleave(config, root):
    """Explicit spatial tongue library; never infer art or segment at runtime."""
    _keys(config, {'count', 'library', 'angle_slots'}, {'count', 'library', 'angle_slots'}, 'interleave')
    if config['count'] not in ([3, 5], [5, 7]) or any(type(v) is not int for v in config['count']):
        raise ValueError('interleave.count must be [3,5] or [5,7]')
    if config['angle_slots'] != 'gaps': raise ValueError('interleave.angle_slots must be gaps')
    root = Path(root).resolve()
    folder = (root/config['library']).resolve()
    if Path(config['library']).is_absolute() or not folder.is_relative_to(root):
        raise ValueError('interleave library escapes kit')
    record = json.loads((folder/'pieces.json').read_text())
    if record.get('canvas') != [512,512] or len(record.get('pieces', [])) != 10:
        raise ValueError('interleave requires ten 512-square tongues')
    ids, assets = set(), {}
    for item in record['pieces']:
        _number(item.get('id'), 1, 10, 'tongue.id', True)
        if item['id'] in ids: raise ValueError('duplicate tongue id')
        ids.add(item['id'])
        _number(item.get('radial_angle_deg'), 0, 360, 'tongue radial angle')
        path = _png(item.get('png'), folder, grayscale=True, confined=True)
        with Image.open(path) as image: a = np.asarray(image.convert('RGBA'))
        if a.shape != (512,512,4): raise ValueError('tongue canvas mismatch')
        pivot = item.get('pivot')
        if not isinstance(pivot,list) or len(pivot) != 2: raise ValueError('tongue pivot requires x,y')
        for v in pivot: _number(v,0,511,'tongue pivot',True)
        if not a[pivot[1],pivot[0],3]: raise ValueError('tongue root outside mask')
        from scipy.ndimage import label
        if label(a[:,:,3]>0, np.ones((3,3)))[1] != 1: raise ValueError('tongue must be connected')
        if np.count_nonzero(a[:,:,3]) != item.get('area_px'): raise ValueError('tongue area mismatch')
        assets[path.relative_to(root).as_posix()] = path
    return record, assets


def interleave_gaps(record):
    """All eleven substantial peak-01 shards, including its core wedges.

    Tiny detached alpha islands are not arms. Angles are the frozen record's
    radial angles, not a newly inferred contour or the stretching axis.
    """
    angles = sorted(p['radial_angle_deg'] % 360 for p in record['pieces'] if p['area_px'] >= 48)
    gaps = [{'start_deg': a, 'width_deg': (angles[(i+1)%len(angles)]-a)%360}
            for i,a in enumerate(angles)]
    return sorted(gaps, key=lambda g: (-g['width_deg'],g['start_deg']))


def interleave_placement(seed, gaps, library):
    """Port of the engine SHA-256 counter sampler (no stateful RNG).

    Normalize seed with int(seed) & 0x7fffffff, including JSON numeric floats.
    Engine sequence: rank library by pick<integer id>, draw count, take the
    pre-ranked largest gaps; per rank draw angle jitter, scale, then mirror.
    Each label hashes ASCII '<integer seed>:<label>', first 8 hex digits as
    unsigned uint32. Division is by 4294967295. Independent labels make
    comparator invocation order irrelevant. Float seed spellings are never
    hashed: Godot JSON numbers and Python integers must select the same ids.
    """
    seed = int(seed) & 0x7fffffff
    def sample(label):
        return int(hashlib.sha256(f'{seed}:{label}'.encode('ascii')).hexdigest()[:8],16)
    count = 5 + sample('count') % 3
    selected = sorted(library, key=lambda p:(sample('pick'+str(int(p['id']))),p['id']))[:count]
    slots = [dict(g) for g in gaps]
    placed = []
    for rank,item in enumerate(selected):
        slots.sort(key=lambda g:(-g['width_deg'],g['start_deg']))
        gap = slots.pop(0)
        limit = min(12.0, max(0.0,40.0-gap['width_deg']/2))
        jitter = (sample('angle'+str(rank))/4294967295*2-1)*limit
        angle = (gap['start_deg']+gap['width_deg']/2+jitter)%360
        left = gap['width_deg']/2+jitter
        slots.extend([{'start_deg':gap['start_deg'],'width_deg':left},
                      {'start_deg':angle,'width_deg':gap['width_deg']-left}])
        placed.append({'id':item['id'],'gap_rank':rank,'angle_deg':angle,
                       'jitter_deg':jitter,'scale':1.2+.4*sample('scale'+str(rank))/4294967295,
                       'mirrored':bool(sample('mirror'+str(rank))%2),'speed_factor':.85})
    return placed

def load_pieces(config, root, runtime=False):
    """Consume T4e schema 2 as delivered; never segment or recolour a shard."""
    root = Path(root).resolve()
    _keys(config, {'source', 'template', 'root_drift', 'dissolve_order', 'erode_noise', 'key_states', 'embers', 'boil', 'timing', 'ember_ending', 'interleave', 'stretch', 'core_residue', 'smoke', *PIECES_DEFAULTS}, {'source', 'template'}, 'pieces')
    if config['template'] not in ('burst_v1', 'burst_v2', 'burst_v1r'):
        raise ValueError('pieces.template must be burst_v1, burst_v2 or burst_v1r')
    if 'stretch' in config:
        validate_piece_stretch(config['stretch'])
        if config['template'] != 'burst_v2': raise ValueError('pieces.stretch requires burst_v2')
    _number(config.get('erode_noise', 0), 0, 1, 'pieces.erode_noise')
    if 'embers' in config: validate_motes(config['embers'], True)
    if 'boil' in config:
        validate_anti_decal('boil', config['boil'])
        if config['template'] != 'burst_v2': raise ValueError('pieces.boil requires burst_v2')
    values = {**PIECES_DEFAULTS, **config}
    states = values.get('key_states', [])
    if not isinstance(states, list):
        raise ValueError('pieces.key_states must be a list')
    if states and values['template'] != 'burst_v2':
        raise ValueError('pieces.key_states requires burst_v2')
    seen, intervals, key_assets = set(), [], {}
    for state in states:
        _keys(state, {'state', 'png', 'hold_frames', 'at_age'},
              {'state', 'png', 'hold_frames', 'at_age'}, 'key_state')
        if state['state'] not in ('expanded', 'spent') or state['state'] in seen:
            raise ValueError('key_state state must be unique expanded or spent')
        seen.add(state['state'])
        _number(state['at_age'], 0, 100000, 'key_state.at_age', True)
        _number(state['hold_frames'], 1, 100000, 'key_state.hold_frames', True)
        interval = (state['at_age'], state['at_age']+state['hold_frames'])
        if any(interval[0] < end and start < interval[1] for start, end in intervals):
            raise ValueError('key_state hold intervals overlap')
        intervals.append(interval)
        asset = _png(state['png'], root, grayscale=True, confined=runtime)
        key_assets[state['png']] = asset
    if not states:
        values.pop('key_states', None)  # explicit [] is byte-equivalent to omission
    _number(values['hold_frames'], 1, 2, 'pieces.hold_frames', True)
    _number(values['base_speed_px_s'], 1e-9, math.inf, 'pieces.base_speed_px_s')
    for role in ('core_residue', 'smoke'):
        if role in values:
            validate_fire_ending(role, values[role])
            if 'ember_ending' not in values: raise ValueError(role+' requires ember_ending')
    if 'ember_ending' in values:
        validate_ember_ending(values['ember_ending'])
        _number(values['residue_s'], 0, 0, 'pieces.residue_s')
        if values['template'] != 'burst_v2' or values['residue_s'] != 0 or 'embers' in values:
            raise ValueError('ember_ending requires burst_v2 and is mutually exclusive with painted residue/embers')
        if 'timing' not in values: raise ValueError('ember_ending requires timing')
    else:
        _number(values['residue_s'], .3, 1, 'pieces.residue_s')
        _number(values['residue_fraction'], .1 if 'timing' in values else .15, .25, 'pieces.residue_fraction')
    if 'timing' in values:
        timing = values['timing']
        _keys(timing, {'expanded_age','erosion_age','paint_end_age'}, {'expanded_age','erosion_age','paint_end_age'}, 'pieces.timing')
        for key in timing: _number(timing[key], 4, 36, 'pieces.timing.'+key, True)
        if not timing['expanded_age'] < timing['erosion_age'] < timing['paint_end_age']:
            raise ValueError('pieces.timing must increase')
        if values['template'] != 'burst_v2': raise ValueError('pieces.timing requires burst_v2')
        for state in states:
            expected = timing['expanded_age'] if state['state']=='expanded' else timing['paint_end_age']-state['hold_frames']
            if state['at_age'] != expected or state['hold_frames'] > 2:
                raise ValueError('key state disagrees with pieces.timing')
    _number(values['seed'], 0, 2147483647, 'pieces.seed', True)
    if 'dissolve_order' in values:
        if values['dissolve_order'] is None:
            raise ValueError('dissolve_order must be a list of band groups')
        dissolve_thresholds(values['dissolve_order'])
    if values['template'] == 'burst_v2':
        values.setdefault('root_drift', .5)
    if 'root_drift' in values:
        _number(values['root_drift'], 0, .5, 'pieces.root_drift')
    source = values['source']
    if not isinstance(source, str) or not source or any(c in source for c in '\\"\n\r'):
        raise ValueError('pieces.source must be a JSON path')
    path = (root/source).resolve()
    if runtime and (Path(source).is_absolute() or not path.is_relative_to(root)):
        raise ValueError('pieces.source escapes kit')
    if not path.is_file() or path.suffix != '.json':
        raise ValueError('Missing pieces.source')
    record = json.loads(path.read_text())
    if record.get('schema_version') != 2 or not isinstance(record.get('pieces'), list) or not record['pieces']:
        raise ValueError('pieces requires T4e schema_version 2 and nonempty pieces')
    canvas = record.get('canvas')
    if not isinstance(canvas, list) or len(canvas) != 2:
        raise ValueError('pieces.canvas requires width, height')
    for value in canvas: _number(value, 1, 8192, 'pieces.canvas', True)
    centre = record.get('centre')
    if not isinstance(centre, list) or len(centre) != 2:
        raise ValueError('pieces.centre requires x, y')
    for value, size in zip(centre, canvas): _number(value, 0, size-1, 'pieces.centre')
    assets = dict(key_assets)
    ids = set()
    for piece in record['pieces']:
        if not isinstance(piece, dict): raise ValueError('piece must be an object')
        _number(piece.get('id'), 0, 2147483647, 'piece.id', True)
        if piece['id'] in ids: raise ValueError('Duplicate piece.id')
        ids.add(piece['id'])
        _number(piece.get('dominant_band'), 0, 3, 'piece.dominant_band', True)
        _number(piece.get('radial_angle_deg'), -360, 360, 'piece.radial_angle_deg')
        _number(piece.get('radial_distance_px'), 0, math.inf, 'piece.radial_distance_px')
        mask = _png(piece.get('mask'), path.parent, grayscale=True, confined=True)
        if runtime and not mask.is_relative_to(root): raise ValueError('piece mask escapes kit')
        with Image.open(mask) as image: rgba = np.asarray(image.convert('RGBA'))
        if list(rgba.shape[1::-1]) != canvas: raise ValueError('piece mask must retain full canvas')
        pivot = piece.get('pivot')
        if not isinstance(pivot, list) or len(pivot) != 2:
            raise ValueError('piece.pivot requires x, y')
        for value, size in zip(pivot, canvas): _number(value, 0, size-1, 'piece.pivot')
        x, y = (int(math.floor(v+.5)) for v in pivot)
        if not rgba[y, x, 3]: raise ValueError('piece pivot outside its mask')
        area = int(np.count_nonzero(rgba[..., 3]))
        if piece.get('area_px') != area: raise ValueError('piece.area_px disagrees with mask')
        if not np.isin(rgba[..., 0][rgba[..., 3] > 0], [0, 85, 170, 255]).all():
            raise ValueError('piece band must be in 0..3')
        key = mask.relative_to(root).as_posix() if mask.is_relative_to(root) else str(mask)
        assets[key] = mask
    if 'interleave' in values:
        if values['template'] != 'burst_v2' or states:
            raise ValueError('interleave requires burst_v2 and empty key_states')
        _, library_assets = load_interleave(values['interleave'], root)
        assets.update(library_assets)
    peak = _png(record.get('peak_index'), path.parent, grayscale=True, confined=True)
    with Image.open(peak) as image:
        if list(image.size) != canvas: raise ValueError('peak_index must match pieces.canvas')
    key = peak.relative_to(root).as_posix() if peak.is_relative_to(root) else str(peak)
    assets[key] = peak
    return values, record, assets


def _validate(data, root, runtime=False):
    _reject_retired(data)
    if isinstance(data, dict) and 'g4' in data:
        return validate_aura_loop(data, root, runtime)
    if isinstance(data, dict) and 'g3' in data:
        return validate_bolt_chain(data, root, runtime)
    if isinstance(data, dict) and 'g2' in data:
        return validate_thrown_field(data, root, runtime)
    if isinstance(data, dict) and 'tint' in data:
        raise ValueError('tint multiply-tint/ramp baking is retired; use material.palette')
    if isinstance(data, dict) and 'pixel_scale' in data:
        raise ValueError('pixel_scale is retired; native sprites use LINEAR filtering')
    _keys(data, TOP-{'tint', 'pixel_scale'},
          {'name', 'element', 'phases', 'layers', 'ground_squash', 'material'}, 'effect')
    if not isinstance(data['name'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', data['name']):
        raise ValueError('name must be a safe identifier')
    if not isinstance(data['element'], str) or not data['element'].strip():
        raise ValueError('element must be nonempty text')
    if data.get('element_class', 'strike') not in ('strike', 'holy', 'field'):
        raise ValueError('element_class must be strike, holy or field')
    if not isinstance(data.get('screen_px', False), bool):
        raise ValueError('screen_px must be boolean')
    _number(data.get('pierce', 0), -1, math.inf, 'pierce', True)
    _keys(data.get('g1', {}), {'collision_radius_bh'}, set(), 'g1')
    _number(data.get('g1', {}).get('collision_radius_bh', .25), .1, .5, 'g1.collision_radius_bh')
    if data.get('pieces', {}).get('template') == 'burst_v1r' and ('decal_s' not in data or not data.get('screen_px')):
        raise ValueError('burst_v1r requires screen_px and decal_s')
    if 'decal_s' in data:
        _number(data['decal_s'], .3, 1, 'decal_s')
        if (data.get('pieces', {}).get('template') != 'burst_v1r'
                or 'file' not in data['layers'].get('decal', {})
                or data['layers']['decal'].get('duration_s') != data['decal_s']
                or 'residual' in data['phases']):
            raise ValueError('decal_s requires burst_v1r, matching painted decal duration and no residual phase')
    validate_material(data['material'])
    _number(data.get('erode_noise', 0), 0, 1, 'erode_noise')
    _keys(data.get('phase_scale', {}), set(PHASES), set(), 'phase_scale')
    for value in data.get('phase_scale', {}).values():
        _number(value, .5, 4, 'phase_scale')
    _number(data['ground_squash'], .5, .65, 'ground_squash')
    _keys(data['phases'], set(PHASES), {'cast', 'travel', 'impact'}, 'phases')
    assets = {}
    for name, phase in data['phases'].items():
        fields = {'sheet', 'frames'} | ({'speed_px_s', 'streak'} if name == 'travel' else set())
        _keys(phase, fields, {'sheet', 'frames'}, name)
        assets[phase['sheet']] = _png(phase['sheet'], root, not runtime, runtime)
        if not isinstance(phase['frames'], list) or not phase['frames']:
            raise ValueError(name+' requires at least one frame')
        for frame in phase['frames']:
            _keys(frame, {'file', 'hold_frames'}, {'file', 'hold_frames'}, 'frame')
            _number(frame['hold_frames'], 1, math.inf, 'hold_frames', True)
            assets[frame['file']] = _png(frame['file'], root, not runtime, runtime)
        if name == 'travel':
            _number(phase.get('speed_px_s', 520), 1e-9, math.inf, 'speed_px_s')
            if not isinstance(phase.get('streak', False), bool):
                raise ValueError('streak must be boolean')
    if 'orb' in data:
        assets.update(validate_orb(data, root, runtime))
    elif 'travel_primitives' in data:
        assets.update(validate_projectile(data, root, runtime))
    elif any(k in data for k in ('skill_spec', 'key_states', 'impact_binding')):
        raise ValueError('projectile metadata requires travel_primitives')
    frame_paths = {assets[frame['file']] for phase in data['phases'].values()
                   for frame in phase['frames']}
    _keys(data['layers'], set(LAYER_KEYS)|{'dark_duplicate'}, set(), 'layers')
    for name, layer in data['layers'].items():
        if name == 'dark_duplicate':
            if not isinstance(layer, bool): raise ValueError('dark_duplicate must be boolean')
            continue
        if name in ('core', 'contact_light', 'shimmer'):
            validate_anti_decal(name, layer)
            continue
        if name in ('cast', 'travel'):
            validate_fire_layer(name, layer)
            continue
        fields = LAYER_KEYS[name]
        optional = ({'file'} if name == 'decal' else
                    {'amount', 'lifetime_s'} if name == 'particles' else set())
        optional |= {'peak'} if name == 'glow' else {'curve', 'tint', 'alpha'} if name == 'floor_light' else set()
        _keys(layer, fields, fields-optional, name)
        for key, value in layer.items():
            if key == 'peak':
                _keys(value, {'alpha','scale'}, {'alpha','scale'}, 'glow.peak')
                _number(value['alpha'], .2, .6, 'glow.peak.alpha')
                _number(value['scale'], 1, 1.15, 'glow.peak.scale')
            elif key in ('curve', 'tint'):
                if value not in (('linear','ease_out') if key == 'curve' else ('palette_2',)):
                    raise ValueError('invalid floor_light.'+key)
            elif key in ('file', 'texture'):
                assets[value] = _png(value, root, key == 'texture' and not runtime, runtime)
                if key == 'texture' and not runtime and assets[value] not in frame_paths:
                    with Image.open(assets[value]) as image:
                        if max(image.size) > 16:
                            raise ValueError('Independent particle texture must be at most 16 px per side')
            elif key == 'direction':
                if not isinstance(value, list) or len(value) != 2:
                    raise ValueError('direction requires two components')
                for v in value: _number(v, -math.inf, math.inf, key)
                if value == [0, 0]: raise ValueError('direction cannot be zero')
            elif key == 'velocity_px_s':
                if isinstance(value, list):
                    if len(value) != 2: raise ValueError('velocity bounds require two values')
                    for v in value: _number(v, 0, math.inf, key)
                    if value[1] < value[0]: raise ValueError('velocity bounds must be ordered')
                else: _number(value, 0, math.inf, key)
            else:
                lo = 1e-9 if key in ('scale', 'scale_from', 'scale_to', 'radius_px', 'lifetime_s', 'time_scale') else 0
                hi = 1 if key in ('alpha', 'time_scale') else (180 if key == 'spread_deg' else math.inf)
                if key == 'amount': lo, hi = 1, 512
                _number(value, lo, hi, key, key == 'amount')
    if 'pieces' in data:
        piece_config, _, piece_assets = load_pieces(data['pieces'], root, runtime)
        flight = max(1, round(data['layers'].get('flash', {}).get('duration_s', 1/60)*60)) + piece_config['hold_frames']
        end = flight + 36 + math.ceil(piece_config['residue_s']*60)
        for state in piece_config.get('key_states', []):
            if state['at_age'] < flight or state['at_age'] + state['hold_frames'] > end:
                raise ValueError('key_state interval must lie inside piece lifetime')
        assets.update(piece_assets)
    for path in set(assets.values()):
        with Image.open(path) as image: rgba = np.array(image.convert('RGBA'))
        rgb = rgba[..., :3][rgba[..., 3] > 0]
        if np.any(rgb[:, 0] != rgb[:, 1]) or np.any(rgb[:, 1] != rgb[:, 2]) or not np.isin(rgb, [0, 85, 170, 255]).all():
            raise ValueError('material source indices must be greyscale 0/85/170/255: '+str(path))
    if runtime:
        fields = data.get('distance_fields')
        # Key-state distance textures are emitter-owned: their retained range
        # depends on the v2 clock at activation, unlike ordinary kit textures.
        key_pngs = {s['png'] for s in data.get('pieces', {}).get('key_states', [])}
        key_pngs.update(s['png'] for s in data.get('key_states', []))
        if not isinstance(fields, dict) or not set(assets)-key_pngs <= set(fields) <= set(assets):
            raise ValueError('distance_fields must map every non-key-state kit texture')
        for source, field in fields.items():
            field_path = _png(field, root, confined=True)
            with Image.open(assets[source]) as a, Image.open(field_path) as b:
                if a.size != b.size or b.mode != 'L':
                    raise ValueError('distance_fields must be L textures matching source dimensions')
    elif 'distance_fields' in data:
        raise ValueError('distance_fields is builder-owned output metadata')
    return assets


def load_kit(directory, preserve_ramp=False):
    """Validate a material kit. preserve_ramp remains a no-op API argument.

    Legacy baked-tint kits are rejected explicitly, never silently migrated.
    """
    root = Path(directory).resolve()
    path = root/'kit.json'
    if not path.resolve().is_relative_to(root):
        raise ValueError('kit.json escapes its directory')
    data = json.loads(path.read_text())
    _validate(data, root, runtime=True)
    if 'particles' in data['layers']:
        data['layers']['particles'].setdefault('amount', 8)
        data['layers']['particles'].setdefault('lifetime_s', .5)
    data.setdefault('pierce', 0)
    data['material'] = validate_material(data['material'])
    return data


def _tint(path, tint, scale, phase_scale=1, band_levels=None):
    """Tint, then NEAREST pixel-scale and phase-scale in separate steps.

    Ramp bands are visible source grey levels, bright to dark, shared across
    each phase's sheet and frames. Hidden RGB never introduces a ramp band.
    Fractional phase sizes round to nearest integer (half up), minimum one.
    Legacy list tint deliberately retains its original byte arithmetic.
    """
    with Image.open(path) as im:
        pixels = np.array(im.convert('RGBA'))
    # RGB channels are equal on visible body pixels; retain transparent RGB too.
    luminance = pixels[..., :3].astype(float) @ np.array([.2126, .7152, .0722])
    if isinstance(tint, dict):
        grey = np.rint(luminance).astype(np.uint8)
        levels = (np.unique(grey[pixels[..., 3] > 0])[::-1]
                  if band_levels is None else band_levels)
        lookup = np.zeros((256, 3), dtype=np.uint8)
        core, rim = np.array(tint['core']), np.array(tint['rim'])
        for band, level in enumerate(levels):
            light = float(level)/255
            weight = light*light*(3-2*light)
            colour = (rim+(core-rim)*weight)*light
            h, s, v = colorsys.rgb_to_hsv(*colour)
            h = (h+tint.get('hue_shift_deg_per_band', 0)*band/360) % 1
            lookup[level] = np.rint(np.array(colorsys.hsv_to_rgb(h, s, v))*255).astype(np.uint8)
        rgb = pixels[..., :3].copy()
        visible = pixels[..., 3] > 0
        rgb[visible] = lookup[grey[visible]]
        rgb[visible & (grey/255 >= tint.get('white_core_keep', .92))] = 255
    else:
        rgb = np.rint(pixels[..., :3].astype(float)*np.array(tint)).astype(np.uint8)
        rgb[luminance >= .92*255] = 255
    pixels[..., :3] = rgb
    image = Image.fromarray(pixels)
    image = image.resize((image.width*scale, image.height*scale), Image.Resampling.NEAREST)
    if phase_scale != 1:
        size = tuple(max(1, int(math.floor(v*phase_scale+.5))) for v in image.size)
        image = image.resize(size, Image.Resampling.NEAREST)
    return image


def _tint_particles(path, tint, scale):
    """Multiply by core/plain RGB, without white preservation or ramp bands.

    A proportional brightness ceiling of 250 retains hue even on white input.
    Small motes (at most 4 px) use body pixel_scale capped at 4 px. Larger
    legacy textures retain their historical size contract.
    Alpha is untouched; no white_core_keep setting affects particles.
    """
    with Image.open(path) as image:
        pixels = np.array(image.convert('RGBA'))
    colour = tint['core'] if isinstance(tint, dict) else tint
    rgb = pixels[..., :3].astype(float)*np.array(colour)
    peak = rgb.max(axis=2, keepdims=True)
    rgb *= np.minimum(1, 250/np.maximum(peak, 1))
    pixels[..., :3] = np.rint(rgb).astype(np.uint8)
    image = Image.fromarray(pixels)
    factor = min(scale, 4/max(image.size)) if max(image.size) <= 4 else scale
    image = image.resize(tuple(max(1, int(v*factor)) for v in image.size), Image.Resampling.NEAREST)
    return image


def build(effect_json, out_dir):
    """Build native index textures and independent distance fields, no tint/resize."""
    started = time.monotonic()
    if isinstance(effect_json, (str, Path)):
        path = Path(effect_json).resolve()
        data, root = json.loads(path.read_text()), path.parent
    else:
        data, root = copy.deepcopy(effect_json), Path.cwd()
    if 'g4' in data:
        return _build_aura_definition(data, root, Path(out_dir).resolve())
    if 'g3' in data:
        return _build_bolt_definition(data, root, Path(out_dir).resolve())
    if 'g2' in data:
        return _build_thrown_definition(data, root, Path(out_dir).resolve())
    assets = _validate(data, root)
    out = Path(out_dir).resolve()
    if any(p.is_relative_to(out) or out == p for p in assets.values()):
        raise ValueError('Output overlaps input assets')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('Output must be empty')
    from export.godot_import import write_spriteframes
    out.mkdir(parents=True, exist_ok=True)
    metadata = copy.deepcopy(data)
    metadata.pop('pierce', None)
    metadata['material'] = validate_material(data['material'])
    metadata['distance_fields'] = {}
    metadata.setdefault('element_class', 'strike')
    metadata['pierce'] = data.get('pierce', 0)
    if 'particles' in metadata['layers']:
        metadata['layers']['particles'].setdefault('amount', 8)
        metadata['layers']['particles'].setdefault('lifetime_s', .5)

    def copy_index(source, file):
        with Image.open(assets[source]) as im: rgba = np.array(im.convert('RGBA'))
        (out/file).parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(rgba).save(out/file)
        field = 'distance/'+file
        (out/field).parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(distance_field(rgba)).save(out/field)
        metadata['distance_fields'][file] = field

    counts = {}
    for phase, definition in data['phases'].items():
        name = PHASES[phase]
        frames = []
        for i, frame in enumerate(definition['frames']):
            file = f'{name}/{name}_{i:02d}.png'
            copy_index(frame['file'], file)
            frames.append({'file': file, 'hold_frames': frame['hold_frames']})
        metadata['phases'][phase]['frames'] = frames
        metadata['phases'][phase]['sheet'] = frames[0]['file']
        if phase == 'travel':
            metadata['phases'][phase].setdefault('speed_px_s', 520)
            metadata['phases'][phase].setdefault('streak', False)
        write_spriteframes(out, name+'.tres', {name: ([f['file'] for f in frames], 1, phase == 'travel')},
                           frame_durations={name: [f['hold_frames']/60 for f in frames]})
        counts[name] = len(frames)
    for name, key in (('decal', 'file'), ('particles', 'texture')):
        layer = metadata['layers'].get(name, {})
        if key in layer:
            file = f'layers/{name}.png'
            copy_index(layer[key], file)
            layer[key] = file
    if 'orb' in data:
        for role in ('body', 'shard'):
            item = metadata['orb'][role]
            file = 'primitives/'+role+'.png'
            copy_index(item['png'], file)
            item['png'] = file
    if 'travel_primitives' in data:
        for role in ('head', 'streak'):
            source = data['travel_primitives'][role]['png']
            file = 'primitives/'+role+'.png'
            copy_index(source, file)
            metadata['travel_primitives'][role]['png'] = file
        for index, state in enumerate(data.get('key_states', [])):
            file = 'travel_keys/key_%d.png' % (index+1)
            copy_index(state['png'], file)
            metadata['key_states'][index]['png'] = file
    if 'pieces' in data:
        config, record, piece_assets = load_pieces(data['pieces'], root)
        source_root = (root/config['source']).resolve().parent
        for item in [record['peak_index']] + [p['mask'] for p in record['pieces']]:
            source = (source_root/item).resolve()
            key = next(k for k, value in piece_assets.items() if value == source)
            copy_index(key, 'pieces/'+item)
            (out/'pieces'/item).write_bytes(source.read_bytes())
        (out/'pieces/pieces.json').write_text(json.dumps(record, indent=2)+'\n')
        if config['template'] == 'burst_v2':
            with Image.open(source_root/record['peak_index']) as image:
                whole_field = distance_field(np.asarray(image.convert('RGBA')))
            for piece in record['pieces']:
                Image.fromarray(whole_field).save(out/metadata['distance_fields']['pieces/'+piece['mask']])
        states = []
        for state in config.get('key_states', []):
            file = 'key_states/'+state['state']+'.png'
            (out/file).parent.mkdir(parents=True, exist_ok=True)
            (out/file).write_bytes(assets[state['png']].read_bytes())
            states.append(dict(state, png=file))
        metadata['pieces'] = dict(config, source='pieces/pieces.json')
        if states:
            metadata['pieces']['key_states'] = states
        if 'interleave' in config:
            library, library_assets = load_interleave(config['interleave'], root)
            for key in library_assets:
                copy_index(key, key)
            folder = out/config['interleave']['library']
            (folder/'pieces.json').write_text(json.dumps(library, indent=2)+'\n')
            metadata['pieces']['key_states'] = []
        counts['pieces'] = len(record['pieces'])
    for mode in ('MIX', 'ADD', 'PREMULT_ALPHA'):
        for lit in (False, True):
            name = f'vfx_material_{mode.lower()}_{"lit" if lit else "unlit"}.gdshader'
            (out/name).write_text(shader_source(mode, lit, data['material'].get('dissolve_order'), data['material'].get('erode_outside_in', False), piece_erode_noise(data)))
    (out/'kit.json').write_text(json.dumps(metadata, indent=2, allow_nan=False)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source': 'effect_kit', 'name': data['name']})+'\n')
    (out/'CREDITS.txt').write_text('Effect '+data['name']+' ('+data['element']+'). Source assets supplied by the effect definition; no license is inferred.\n')
    return {'id': 'effect_kit', 'subject': data['name'], 'passed': None, 'value': counts,
            'threshold': None, 'op': None, 'unit': 'frames', 'evidence': [str(out/'kit.json')],
            'notes': 'Native index frames, independent coverage alpha, LINEAR runtime palette material.',
            'wall_s': time.monotonic()-started}


# Shared runtime fragment is embedded only in authored-kit scripts. Timers for
# feedback ignore Engine.time_scale, and the tree-owned stop controller survives
# an effect being freed. Multiple hits extend one stop without losing baseline.
LAYER_SCRIPT = '''
@export var ground_squash: float = 0.6
@export var hitstop_duration: float = 0.0
@export var hitstop_time_scale: float = 1.0
@export var shake_distance: float = 0.0
@export var shake_duration: float = 0.0
var spell_scale: float = 1.0

func _start_layers(animation_name: String, angle: float = 0.0) -> void:
    $Ground.scale = Vector2(1, ground_squash) * spell_scale
    for node in $Ground.get_children():
        if node is AnimatedSprite2D:
            node.rotation = angle
            node.play(animation_name)
    if has_node("FloorLight"):
        $FloorLight.scale *= spell_scale
        create_tween().tween_property($FloorLight, "modulate:a", 0.0, FLOOR_DURATION)
    if has_node("Ground/Flash"):
        var flash: AnimatedSprite2D = $Ground/Flash
        var tween: Tween = create_tween().set_parallel(true)
        tween.tween_property(flash, "modulate:a", 0.0, FLASH_DURATION)
        tween.tween_property(flash, "scale", Vector2.ONE * FLASH_TO, FLASH_DURATION)
    if has_node("Decal"):
        $Decal.scale *= spell_scale
        create_tween().tween_property($Decal, "modulate:a", 0.0, DECAL_DURATION)
    if has_node("Particles"):
        $Particles.initial_velocity_min *= spell_scale
        $Particles.initial_velocity_max *= spell_scale
        $Particles.scale = Vector2.ONE * spell_scale

func _feedback() -> void:
    var tree: SceneTree = get_tree()
    if hitstop_duration > 0.0:
        var controller: Node = tree.root.get_node_or_null("EffectHitstop")
        if controller == null:
            controller = Node.new()
            controller.name = "EffectHitstop"
            controller.set_meta("baseline", Engine.time_scale)
            controller.set_meta("generation", 0)
            tree.root.add_child(controller)
        var generation: int = int(controller.get_meta("generation")) + 1
        controller.set_meta("generation", generation)
        Engine.time_scale = hitstop_time_scale
        tree.create_timer(hitstop_duration, true, false, true).timeout.connect(func():
            if is_instance_valid(controller) and int(controller.get_meta("generation")) == generation:
                Engine.time_scale = float(controller.get_meta("baseline"))
                controller.name = "EffectHitstopDone"
                controller.queue_free())
    var camera: Camera2D = get_viewport().get_camera_2d()
    if camera != null and shake_duration > 0.0 and shake_distance > 0.0:
        if camera.has_meta("effect_shake_tween"):
            var previous: Tween = camera.get_meta("effect_shake_tween")
            previous.kill()
        else:
            camera.set_meta("effect_shake_baseline", camera.offset)
        var baseline: Vector2 = camera.get_meta("effect_shake_baseline")
        camera.offset = baseline + Vector2(shake_distance, 0)
        var shake: Tween = tree.create_tween().bind_node(camera).set_ignore_time_scale(true)
        camera.set_meta("effect_shake_tween", shake)
        shake.tween_property(camera, "offset", baseline - Vector2(shake_distance, 0), shake_duration * 0.5)
        shake.tween_property(camera, "offset", baseline, shake_duration * 0.5)
        shake.tween_callback(func():
            camera.remove_meta("effect_shake_tween")
            camera.remove_meta("effect_shake_baseline"))
'''

AUTHORED_BOLT = '''extends Area2D
var direction: Vector2 = Vector2.RIGHT
var distance: float = 0.0
var expired: bool = false
var caster: CollisionObject2D
@export var speed_px_s: float = 520.0

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    _start_layers("travel", direction.angle())
    if has_node("Ground/Streak"):
        $Ground/Streak.position = -direction * STREAK_OFFSET
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius *= spell_scale

func _physics_process(delta: float) -> void:
    if expired:
        return
    var step: float = minf(speed_px_s * spell_scale * delta, 650.0 * spell_scale - distance)
    var target: Vector2 = global_position + direction * step
    var query := PhysicsRayQueryParameters2D.create(global_position, target, collision_mask)
    var excluded: Array[RID] = [get_rid()]
    if is_instance_valid(caster):
        excluded.append(caster.get_rid())
    query.exclude = excluded
    var hit: Dictionary = get_world_2d().direct_space_state.intersect_ray(query)
    if not hit.is_empty() and hit.collider is StaticBody2D:
        global_position = hit.position
        _impact()
        return
    global_position = target
    distance += step
    if distance >= 650.0 * spell_scale - 0.001:
        _impact()

func _on_body_entered(body: Node2D) -> void:
    if body is StaticBody2D:
        _impact()

func _impact() -> void:
    if expired:
        return
    expired = true
    $Ground.hide()
    if has_node("Particles"):
        $Particles.emitting = false
    set_deferred("monitoring", false)
    var effect: Node2D = load(IMPACT_PATH).instantiate()
    effect.spell_scale = spell_scale
    effect.position = get_parent().to_local(global_position)
    get_parent().add_child(effect)
    get_tree().create_timer(TAIL_DURATION).timeout.connect(queue_free)
'''

AUTHORED_IMPACT = '''extends Node2D
func _ready() -> void:
    _start_layers("impact")
    _feedback()
    $Ground/Shatter.animation_finished.connect(_body_finished)
    if has_node("Residual"):
        $Residual.scale = Vector2(1, ground_squash) * spell_scale
        $Residual.animation_finished.connect($Residual.hide)
    get_tree().create_timer(TOTAL_DURATION).timeout.connect(queue_free)

func _body_finished() -> void:
    $Ground.hide()
    if has_node("Residual"):
        $Residual.show()
        $Residual.play("residual")
'''


# T4p: opt-in, spec-carried G1 travel. No kit-name inference or legacy defaults.
def quantise_projectile(rgba):
    """Nearest four value planes; preserve source coverage and native canvas."""
    pixels = np.asarray(rgba)
    if pixels.dtype != np.uint8 or pixels.ndim != 3 or pixels.shape[2] != 4:
        raise ValueError('primitive requires uint8 RGBA')
    result = pixels.copy()
    luminance = pixels[..., :3].astype(float) @ np.array([.2126, .7152, .0722])
    values = (np.floor(luminance/85+.5)*85).astype(np.uint8)
    result[..., :3] = values[..., None]
    return result


def validate_projectile(data, root, runtime=False):
    spec = data.get('skill_spec', {})
    _keys(spec, {'skill_id', 'source_game', 'grammar', 'visual_treatment_id', 'response_class',
                 'mechanics', 'presentation', 'provenance'},
          {'skill_id', 'grammar', 'visual_treatment_id', 'response_class', 'mechanics', 'presentation'}, 'skill_spec')
    mechanics = spec['mechanics']
    expected = {'origin_socket': 'cast_release', 'aim_rule': 'release-locked',
                'radius_px': 0, 'count': 1, 'hop_count': 0,
                'travel': {'kind': 'straight', 'streak': True},
                'active_duration_s': None, 'tick_schedule': None,
                'termination': 'first_contact_or_range', 'pierce': 0}
    optional = {'radius_px', 'active_duration_s', 'tick_schedule'} if spec.get('skill_id') == 'ice_bolt_e2' else set()
    _keys(mechanics, set(expected)|{'speed_px_s', 'range_px', 'range_expiry'}, (set(expected)-optional)|{'speed_px_s', 'range_px'}, 'mechanics')
    if spec['grammar'] != 'G1' or any(mechanics.get(k, v) != v for k, v in expected.items()):
        raise ValueError('unsupported G1 mechanics; no inferred grammar')
    if mechanics.get('range_expiry', 'burst') not in ('fizzle', 'burst'):
        raise ValueError('mechanics.range_expiry must be fizzle or burst')
    for key in ('range_px', 'speed_px_s'):
        _number(mechanics[key], 1e-9, math.inf, key)
    if (not data.get('screen_px') or data.get('pierce', 0) != mechanics['pierce']
            or data['phases']['travel'].get('speed_px_s') != mechanics['speed_px_s']
            or data['phases']['travel'].get('streak') is not True):
        raise ValueError('projectile mechanics disagree with kit')
    if spec['visual_treatment_id'] != data['element'] or spec['response_class'] != data['element_class']:
        raise ValueError('projectile treatment disagrees with spec')
    presentation = spec['presentation']
    for key in ('primitive_bindings', 'body_extents_bh', 'phase_envelope_s', 'enabled_layers'):
        if key not in presentation: raise ValueError('missing presentation.'+key)
    binding = data.get('impact_binding')
    _keys(binding, {'kit', 'phase', 'template', 'seed'}, {'kit', 'phase', 'template', 'seed'}, 'impact_binding')
    if (not isinstance(binding['kit'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', binding['kit'])
            or binding['phase'] != 'pieces' or binding['template'] not in ('burst_v2', 'burst_v1r')):
        raise ValueError('impact_binding requires a named pieces burst_v2 kit')
    _number(binding['seed'], 0, 2**32-1, 'seed', True)
    if binding['template'] == 'burst_v1r':
        if (binding['kit'] != data['name'] or data.get('pieces', {}).get('template') != 'burst_v1r'
                or data['pieces'].get('seed') != binding['seed'] or spec['skill_id'] != 'ice_bolt_e2'
                or data['element'] != 'ice' or 'decal_s' not in data):
            raise ValueError('burst_v1r requires the ice self-bound pieces and decal')
    elif not presentation['primitive_bindings'].get('impact', '').startswith(binding['kit']+' '):
        raise ValueError('impact binding disagrees with spec')
    primitives = data['travel_primitives']
    _keys(primitives, {'head', 'streak', 'rest_hold_frames', 'tail_s'}, {'head', 'streak', 'rest_hold_frames', 'tail_s'}, 'travel_primitives')
    _number(primitives['rest_hold_frames'], 3, 4, 'rest_hold_frames', True)
    if primitives['tail_s'] != .15: raise ValueError('travel tail_s must be 0.15')
    assets = {}
    for role in ('head', 'streak'):
        item = primitives[role]
        keys = {'binding', 'png', 'pivot', 'scale'} | ({'rear_socket'} if role == 'head' else set())
        _keys(item, keys|({'alpha'} if role == 'streak' else set()), keys, 'primitive.'+role)
        if 'alpha' in item: _number(item['alpha'], 0, 1, 'primitive.alpha')
        if item['binding'] != presentation['primitive_bindings'].get('travel_'+role):
            raise ValueError('primitive binding disagrees with spec')
        path = _png(item['png'], root, True, runtime)
        assets[item['png']] = path
        with Image.open(path) as im: size = im.size
        for key in ('pivot', 'rear_socket'):
            if key not in item: continue
            if not isinstance(item[key], list) or len(item[key]) != 2: raise ValueError(key+' requires x,y')
            for value, extent in zip(item[key], size): _number(value, 0, extent, key)
        _number(item['scale'], 1e-9, 1, 'primitive.scale')
    states = data.get('key_states', [])
    if not isinstance(states, list) or len(states) > 2: raise ValueError('key_states supports at most two paintings')
    names = set()
    for state in states:
        _keys(state, {'state', 'png', 'hold_frames', 'pivot', 'scale'},
              {'state', 'png', 'hold_frames', 'pivot', 'scale'}, 'travel key_state')
        if not isinstance(state['state'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', state['state']) or state['state'] in names:
            raise ValueError('key_state names must be unique safe identifiers')
        names.add(state['state'])
        _number(state['hold_frames'], 3, 4, 'key_state.hold_frames', True)
        _number(state['scale'], 1e-9, 1, 'key_state.scale')
        path = _png(state['png'], root, True, runtime)
        assets[state['png']] = path
        if not isinstance(state['pivot'], list) or len(state['pivot']) != 2: raise ValueError('key_state pivot requires x,y')
        with Image.open(path) as im:
            for value, extent in zip(state['pivot'], im.size): _number(value, 0, extent, 'key_state.pivot')
    return assets


def build_projectile_arms(spec_path, head_path, streak_path, impact_dir, out_parent, staging, key_states=None):
    """Build A/B from one explicit spec. Future keys are authored kit metadata.

    Impact is a catalogue dependency, reused by name with seed/template checks.
    No per-frame travel drawing is synthesized. Empty key lists are identical.
    """
    spec_path, impact_dir, staging = Path(spec_path), Path(impact_dir), Path(staging)
    spec = json.loads(spec_path.read_text())
    impact = load_kit(impact_dir)
    staging.mkdir(parents=True, exist_ok=True)
    primitives = {}
    for role, source in [('head', head_path), ('streak', streak_path)]:
        with Image.open(source) as im: pixels = quantise_projectile(np.array(im.convert('RGBA')))
        file = staging/(role+'.png'); Image.fromarray(pixels).save(file)
        box = Image.fromarray(pixels[..., 3]).getbbox()
        if box is None: raise ValueError('empty primitive')
        left, top, right, bottom = box
        extent = spec['presentation']['body_extents_bh']['head' if role == 'head' else 'streak_len']*130
        scale = min(1., extent/(right-left))
        # +x-facing head: origin at its tip; rear socket at the body rear.
        item = dict(binding=spec['presentation']['primitive_bindings']['travel_'+role],
                    png=str(file.resolve()), pivot=[right-1, (top+bottom-1)/2], scale=scale)
        if role == 'head': item['rear_socket'] = [left, (top+bottom-1)/2]
        primitives[role] = item
    base = dict(element=spec['visual_treatment_id'], element_class=spec['response_class'],
                screen_px=True, ground_squash=impact['ground_squash'],
                phase_scale=copy.deepcopy(impact.get('phase_scale', {})),
                material=copy.deepcopy(impact['material']), layers=copy.deepcopy(impact['layers']),
                pierce=spec['mechanics']['pierce'], skill_spec=spec, key_states=[],
                travel_primitives=dict(primitives, rest_hold_frames=3, tail_s=.15),
                impact_binding=dict(kit=impact['name'], phase='pieces', template=impact['pieces']['template'], seed=impact['pieces']['seed']))
    base['phases'] = {}
    for phase in ('cast', 'impact'):
        base['phases'][phase] = copy.deepcopy(impact['phases'][phase])
        base['phases'][phase]['sheet'] = str((impact_dir/base['phases'][phase]['sheet']).resolve())
        for frame in base['phases'][phase]['frames']: frame['file'] = str((impact_dir/frame['file']).resolve())
    head = primitives['head']['png']
    base['phases']['travel'] = dict(sheet=head, frames=[dict(file=head, hold_frames=1)],
                                   speed_px_s=spec['mechanics']['speed_px_s'], streak=True)
    states = copy.deepcopy(key_states or [])
    if not isinstance(states, list) or len(states) > 2:
        raise ValueError('key_states supports at most two paintings')
    for index, state in enumerate(states):
        with Image.open(state['png']) as im:
            pixels = quantise_projectile(np.array(im.convert('RGBA')))
        file = staging/('travel_key_%d.png' % (index+1))
        Image.fromarray(pixels).save(file)
        state['png'] = str(file.resolve())
    reports = []
    for arm in ('A', 'B'):
        data = dict(copy.deepcopy(base), name=spec['skill_id']+'_'+arm)
        data['key_states'] = states if arm == 'A' else []
        reports.append(build(data, Path(out_parent)/data['name']))
    return reports


# T4s: explicit G2 metadata; RGB material assets never enter value-index validation.
def tick_schedule_report(schedule, minimum=.25):
    if not isinstance(schedule, list) or len(schedule) < 3:
        raise ValueError('tick_schedule_s requires at least three ticks')
    for value in schedule: _number(value, 0, math.inf, 'tick_schedule_s')
    intervals = np.diff(schedule)
    if schedule[0] != 0 or np.any(intervals <= 0):
        raise ValueError('tick_schedule_s must start at zero and strictly increase')
    cv = float(intervals.std()/intervals.mean())
    return {'intervals_s': intervals.tolist(), 'interval_cv': cv, 'minimum_cv': minimum,
            'ff08_satisfied': cv >= minimum, 'tick_count': len(schedule)}


def assert_tick_schedule(schedule, minimum=.25):
    report = tick_schedule_report(schedule, minimum)
    if not report['ff08_satisfied']:
        raise ValueError('FF-08 interval CV %.9f < %.9f; authored schedule retained' % (report['interval_cv'], minimum))
    return report


def validate_thrown_field(data, root, runtime=False):
    _keys(data, {'name','element','element_class','screen_px','ground_squash','material',
                 'phases','layers','pierce','skill_spec','g2','density','distance_fields'},
          {'name','element','element_class','screen_px','ground_squash','material','phases','layers','skill_spec','g2'}, 'G2 kit')
    if not isinstance(data['name'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', data['name']):
        raise ValueError('name must be a safe identifier')
    spec = data['skill_spec']; mechanics = spec['mechanics']; field = mechanics['field']
    if (spec['grammar'] != 'G2' or mechanics['aim_rule'] != 'ground-locked'
            or mechanics['origin_socket'] != 'cast_release' or mechanics['termination'] != 'field_expiry'):
        raise ValueError('unsupported G2 mechanics; grammar is explicit')
    if data['element'] != spec['visual_treatment_id'] or data['element_class'] != 'field' or not data['screen_px'] or data['ground_squash'] != spec['presentation'].get('ground_squash', .58):
        raise ValueError('G2 treatment, screen_px or ground squash disagrees')
    if data['element'] not in ('fire','poison'): raise ValueError('unsupported G2 treatment')
    for value in [mechanics['range_px'],mechanics['arc']['apex_px'],mechanics['arc']['flight_s'],field['radius_px'],field['duration_s']]:
        _number(value, 1e-9, math.inf, 'G2 mechanic')
    presentation = spec['presentation']
    if 'lick_flicker_hz' in presentation:
        hz = presentation['lick_flicker_hz']
        if not isinstance(hz, list) or len(hz) != 2:
            raise ValueError('lick_flicker_hz requires two ascending frequencies')
        for value in hz: _number(value, 2, 6, 'lick_flicker_hz')
        if hz[0] >= hz[1]: raise ValueError('lick_flicker_hz must be ascending')
        if not isinstance(presentation.get('lick_coherence'), str) or not presentation['lick_coherence'].startswith('low'):
            raise ValueError('lick_coherence must be low')
    if 'launch_angle_deg' in mechanics['arc']:
        _number(mechanics['arc']['launch_angle_deg'], 0.01, 89, 'launch_angle_deg')
    if 'residue_diameter' in presentation['body_extents_bh']:
        _number(presentation['body_extents_bh']['residue_diameter'], 1e-9, math.inf, 'residue_diameter')
    minimum = field.get('tick_cv_min', .25)
    _number(minimum, .25, math.inf, 'tick_cv_min')
    tick_schedule_report(field['tick_schedule_s'], minimum)
    if field['tick_schedule_s'][-1] >= field['duration_s']: raise ValueError('tick outside field lifetime')
    validate_material(data['material'])
    if data['material'].get('blend_mode','MIX') != 'MIX': raise ValueError('G2 requires MIX')
    if data['element'] == 'poison': _number(data.get('density'),0,1,'density')
    elif 'density' in data: raise ValueError('density is a separate poison layer only')
    g = data['g2']
    _keys(g, {'flask','field_source','pulse','splash','seed','field_binding','roil_uv_per_s','dark_offset_px','dark_alpha'}, {'flask','field_source','pulse','splash','seed'}, 'g2')
    for key,high in [('roil_uv_per_s',.2),('dark_offset_px',12),('dark_alpha',1)]:
        _number(g.get(key,0),0,high,'g2.'+key)
    binding = g.get('field_binding')
    if binding is not None:
        _keys(binding, {'kind','scale','pivot','dissolve_s'}, {'kind','scale','pivot','dissolve_s'}, 'field_binding')
        if (data['element'] != 'fire' or binding['kind'] != 'painted_pool'
                or isinstance(binding['scale'], bool) or binding['scale'] != 1.0
                or binding['dissolve_s'] != .4):
            raise ValueError('painted_pool requires fire, native scale 1.0 and dissolve_s 0.4')
        if not isinstance(binding['pivot'], list) or len(binding['pivot']) != 2:
            raise ValueError('field_binding.pivot requires two pixel coordinates')
        for v in binding['pivot']: _number(v, 0, 511, 'field_binding.pivot')
        if data['material'].get('dissolve_order') != [[3],[2],[1,0]]:
            raise ValueError('painted_pool requires dissolve_order 3, 2, then 1+0')
    _number(g['seed'],0,2**32-1,'seed',True)
    splash = g['splash']
    if data['element'] == 'fire':
        _keys(splash, {'kit','scale','template'}, {'kit','scale','template'}, 'splash')
        if splash['template'] != 'burst_v2' or splash['scale'] != .7: raise ValueError('fire splash requires burst_v2 at 0.7')
    elif splash != {'template':'burst_v1','count':4,'duration_s':.25,'residue_s':0}:
        raise ValueError('poison splash requires four translating lobes, .25 s, no residue')
    envelope = spec['presentation']['phase_envelope_s']
    _number(envelope['residue'],1e-9,math.inf,'residue_s')
    if envelope['flight'] != mechanics['arc']['flight_s'] or envelope.get('field',envelope.get('cloud')) != field['duration_s']:
        raise ValueError('G2 envelope disagrees with mechanics')
    assets = {}
    for role in ('flask','field_source','pulse'):
        assets[g[role]] = _png(g[role],root,confined=runtime)
    for phase in data['phases'].values():
        for source in [phase['sheet'],*[f['file'] for f in phase['frames']]]:
            assets[source] = _png(source,root,confined=runtime)
    for key,path in assets.items():
        with Image.open(path) as im: rgba = np.asarray(im.convert('RGBA'))
        if not np.any(rgba[...,3]): raise ValueError('G2 primitive is empty')
        if key == g['field_source'] and binding is not None:
            if rgba.shape != (512,512,4) or not np.any((rgba[...,0] == 255) & (rgba[...,3] > 0)):
                raise ValueError('painted_pool requires 512 RGBA and plane-3 flame pixels')
        if key == g['flask']: continue
        rgb = rgba[...,:3][rgba[...,3]>0]
        if not np.isin(rgb,[0,85,170,255]).all() or np.any(rgb[:,0]!=rgb[:,1]) or np.any(rgb[:,1]!=rgb[:,2]):
            raise ValueError('G2 indexed source indices must be greyscale 0/85/170/255')
    return assets


def build_thrown_field(spec_path, flask_path, field_path, pulse_path, out_dir, material, splash, density=1.0):
    """Copy painted primitives intact. Runtime emitter cuts shards and derives the field.

    CV is a separate instrument: valid authored fixtures can expose a contradictory
    conductor gate without silently rewriting their mechanics.
    """
    spec=json.loads(Path(spec_path).read_text()); out=Path(out_dir)
    if out.exists() and any(out.iterdir()): raise ValueError('Output must be empty')
    out.mkdir(parents=True,exist_ok=True)
    for role,source in [('flask',flask_path),('field_source',field_path),('pulse',pulse_path)]:
        target=out/'primitives'/f'{role}.png';target.parent.mkdir(exist_ok=True)
        if role == 'flask': target.write_bytes(Path(source).read_bytes())
        else:
            with Image.open(source) as im: pixels=quantise_projectile(np.asarray(im.convert('RGBA')))
            Image.fromarray(pixels).save(target)
    phases={}
    for phase,folder in [('cast','flare'),('travel','travel'),('impact','impact')]:
        file=f'{folder}/{folder}_00.png'; (out/folder).mkdir()
        (out/file).write_bytes((out/'primitives/pulse.png').read_bytes())
        phases[phase]={'sheet':file,'frames':[{'file':file,'hold_frames':2}]}
    data=dict(name=spec['skill_id']+'_e3',element=spec['visual_treatment_id'],element_class='field',screen_px=True,
              ground_squash=spec['presentation'].get('ground_squash',.58), material=copy.deepcopy(material),phases=phases,layers={},pierce=0,skill_spec=spec,
              g2=dict(flask='primitives/flask.png',field_source='primitives/field_source.png',pulse='primitives/pulse.png',splash=splash,seed=2026))
    if data['element']=='poison':
        data['density']=spec['presentation'].get('density',density)
        for key in ('roil_uv_per_s','dark_offset_px','dark_alpha'):
            if key in spec['presentation']: data['g2'][key]=spec['presentation'][key]
        if 'erode_noise' in spec['presentation']: data['material'].update(erode_noise=spec['presentation']['erode_noise'],erode_outside_in=True,erode=.3)
    validate_thrown_field(data,out,True)
    (out/'kit.json').write_text(json.dumps(data,indent=2)+'\n')
    (out/'CREDITS.txt').write_text('G2 '+data['name']+': supplied painted primitives; derived shards/field, no new painting.\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':data['name']})+'\n')
    return data


def _build_thrown_definition(data, root, out):
    """Normal build() entry point for explicit G2 definitions, including RGB."""
    assets=validate_thrown_field(data,root,False)
    if out.exists() and (not out.is_dir() or any(out.iterdir())): raise ValueError('Output must be empty')
    if any(p.is_relative_to(out) for p in assets.values()): raise ValueError('Output overlaps input assets')
    out.mkdir(parents=True,exist_ok=True)
    metadata=copy.deepcopy(data)
    for role in ('flask','field_source','pulse'):
        file='primitives/'+role+'.png';target=out/file;target.parent.mkdir(exist_ok=True)
        target.write_bytes(assets[data['g2'][role]].read_bytes());metadata['g2'][role]=file
    for phase,definition in metadata['phases'].items():
        folder=PHASES[phase];frames=[]
        for i,frame in enumerate(definition['frames']):
            file=f'{folder}/{folder}_{i:02d}.png';target=out/file;target.parent.mkdir(exist_ok=True)
            target.write_bytes(assets[frame['file']].read_bytes());frames.append(dict(frame,file=file))
        definition['frames']=frames;definition['sheet']=frames[0]['file']
    metadata.pop('distance_fields',None)
    metadata['material']=validate_material(metadata['material'])
    (out/'kit.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':metadata['name']})+'\n')
    (out/'CREDITS.txt').write_text('G2 '+metadata['name']+': supplied painted primitives; derived shards/field, no new painting.\n')
    return {'id':'effect_kit','subject':metadata['name'],'passed':None,'value':{'grammar':'G2'},'threshold':None,'op':None,'unit':'kit','evidence':[str(out/'kit.json')],'notes':'RGB flask retained; indexed field separate; FF-08 reported separately.'}


# T4t: grammar and presentation are explicit metadata, never name heuristics.
def chain_schedule_report(chain):
    _number(chain['count'], 0, 32, 'chain.count', True)
    _number(chain['hop_range_px'], 1e-9, math.inf, 'chain.hop_range_px')
    authored = chain['hop_delay_s']
    delays = authored if isinstance(authored, list) else [authored]*chain['count']
    if len(delays) != chain['count']: raise ValueError('chain delay count must equal additional hop count')
    for delay in delays: _number(delay, 1/60, 10, 'chain.hop_delay_s')
    cv = float(np.std(delays)/np.mean(delays)) if len(delays)>1 else None
    minimum = chain.get('hop_delay_cv_min', .25)
    _number(minimum, .25, 1, 'hop_delay_cv_min')
    if cv is not None and cv < minimum: raise ValueError('FF-08 chain interval CV below minimum')
    cumulative = np.cumsum(delays).tolist()
    return dict(delays_s=delays, cumulative_s=cumulative, interval_cv=cv, minimum_cv=minimum,
                cv_evaluable=len(delays)>1, count_semantics='additional hops after initial contact')


def validate_bolt_chain(data, root, runtime=False):
    _keys(data, {'name','element','element_class','screen_px','ground_squash','material','phases','layers','pierce','skill_spec','g3','distance_fields'},
          {'name','element','element_class','screen_px','ground_squash','material','phases','layers','skill_spec','g3'}, 'G3 kit')
    if not isinstance(data['name'], str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',data['name']): raise ValueError('name must be a safe identifier')
    spec=data['skill_spec'];m=spec['mechanics'];p=spec['presentation'];g=data['g3']
    if (spec['grammar']!='G3' or m['aim_rule']!='target-tracking' or m['origin_socket']!='cast_release'
            or m['instant'] is not True or m['termination'] not in ('instant','chain_end')):
        raise ValueError('unsupported G3 mechanics; no inferred grammar')
    if data['screen_px'] is not True or data['element_class']!='strike' or data.get('pierce',0)!=0:
        raise ValueError('G3 requires screen_px, strike and no pierce')
    for key in ('range_px','width_px'): _number(m[key],1e-9,4096,key)
    chain_schedule_report(m['chain'])
    material=validate_material(data['material'])
    if material['blend_mode']!='ADD' or data['layers']!={'dark_duplicate':False}:
        raise ValueError('G3 requires ADD body and dark duplicate OFF')
    if material.get('dissolve_order',LEGACY_DISSOLVE_ORDER)!=LEGACY_DISSOLVE_ORDER:
        raise ValueError('G3 afterimage requires band 3 first')
    allowed={'link','branch','prong','seed','max_branches','prongs','width_multiplier','life_s','afterimage_s','segment_fraction','jitter_px','min_links','max_links'}
    _keys(g,allowed,allowed,'g3')
    _number(g['seed'],0,2**32-1,'g3.seed',True)
    _number(g['max_branches'],0,2,'max_branches',True)
    _number(g['prongs'],1,8,'prongs',True)
    _number(g['min_links'],1,3,'min_links',True)
    _number(g['max_links'],g['min_links'],64,'max_links',True)
    _number(g['width_multiplier'],1,1.35,'width_multiplier')
    envelope=p['phase_envelope_s']; life=envelope.get('bolt_life',envelope.get('link_life'))
    _number(life,1/60,1,'bolt life')
    if g['life_s']!=life or g['afterimage_s']!=.15 or g['segment_fraction']!=.8 or g['jitter_px']!=12:
        raise ValueError('G3 bolt envelope/geometry disagrees with contract')
    if envelope.get('afterimage',.15)!=g['afterimage_s']: raise ValueError('afterimage disagrees with spec')
    if g['width_multiplier']>1 and (g['max_branches']>1 or g['prongs']!=2 or material['palette'][3]!=[1.,1.,.98,1.]):
        raise ValueError('wide dialect requires one branch maximum, two prongs, jewel-white core')
    assets={}
    for role in ('link','branch','prong'):
        item=g[role];_keys(item,{'png','start','end','region','coverage_width'}, {'png','start','end','region','coverage_width'},'g3.'+role)
        _number(item['coverage_width'],1,512,'primitive coverage_width')
        if not isinstance(item['region'],list) or len(item['region'])!=4: raise ValueError('primitive region requires xywh')
        for v in item['region']: _number(v,0,512,'primitive region',True)
        if min(item['region'][2:])<1 or item['region'][0]+item['region'][2]>512 or item['region'][1]+item['region'][3]>512: raise ValueError('primitive region outside source')
        assets[item['png']]=_png(item['png'],root,confined=runtime)
        for key in ('start','end'):
            if not isinstance(item[key],list) or len(item[key])!=2: raise ValueError('primitive socket requires two coordinates')
            for v in item[key]: _number(v,0,511,'primitive socket')
        if math.dist(item['start'],item['end'])<1: raise ValueError('primitive sockets must differ')
    for phase in data['phases'].values():
        for src in [phase['sheet'],*[f['file'] for f in phase['frames']]]: assets[src]=_png(src,root,confined=runtime)
    for src,path in assets.items():
        with Image.open(path) as im:
            a=np.array(im)
            if im.mode!='RGBA' or im.size!=(512,512) or not np.any(a[...,3]): raise ValueError('G3 requires nonempty 512 RGBA primitives')
        rgb=a[...,:3][a[...,3]>0]
        if not np.isin(rgb,[0,85,170,255]).all() or np.any(rgb[:,0]!=rgb[:,1]) or np.any(rgb[:,1]!=rgb[:,2]):
            raise ValueError('G3 source indices must be greyscale 0/85/170/255')
    return assets


def build_bolt_chain(spec_path, primitive_paths, out_dir, *, max_branches, prongs, width_multiplier=1., palette=None, seed=2026, min_links=1, max_links=64):
    """Assemble supplied drawings, keeping all source alpha and native dimensions."""
    spec=json.loads(Path(spec_path).read_text());out=Path(out_dir).resolve()
    if out.exists() and any(out.iterdir()): raise ValueError('Output must be empty')
    out.mkdir(parents=True,exist_ok=True);(out/'primitives').mkdir()
    g=dict(seed=seed,max_branches=max_branches,prongs=prongs,width_multiplier=width_multiplier,min_links=min_links,max_links=max_links,
           life_s=spec['presentation']['phase_envelope_s'].get('bolt_life',spec['presentation']['phase_envelope_s'].get('link_life')),
           afterimage_s=.15,segment_fraction=.8,jitter_px=12)
    for role,path in primitive_paths.items():
        with Image.open(path) as im: rgba=quantise_projectile(np.asarray(im.convert('RGBA')))
        y,x=np.nonzero(rgba[...,3]>=128);left=int(x.min());right=int(x.max())
        if role=='prong': # Authored needle runs from lower-left root to upper-right tip.
            start=[float(left),float(y[x==left].mean())];end=[float(right),float(y[x==right].mean())]
        else:
            start=[float(left),float(y[x==left].mean())];end=[float(right),float(y[x==right].mean())]
        file='primitives/'+role+'.png';Image.fromarray(rgba).save(out/file)
        g[role]=dict(png=file,start=start,end=end,region=[left,0,right-left+1,512],coverage_width=int(y.max()-y.min()+1))
    phases={}
    for phase,folder,role in [('cast','flare','prong'),('travel','travel','link'),('impact','impact','prong')]:
        (out/folder).mkdir();file=f'{folder}/{folder}_00.png';(out/file).write_bytes((out/g[role]['png']).read_bytes())
        phases[phase]=dict(sheet=file,frames=[dict(file=file,hold_frames=1)])
    data=dict(name=spec['skill_id']+'_e3',element=spec['visual_treatment_id'],element_class='strike',screen_px=True,ground_squash=.6,
              material=dict(palette=palette or [[.025,.05,.12,1],[.16,.32,.6,1],[.48,.74,1,1],[.88,.96,1,1]],blend_mode='ADD',light_participation=False),
              phases=phases,layers={'dark_duplicate':False},skill_spec=spec,g3=g,pierce=0)
    validate_bolt_chain(data,out,True)
    (out/'kit.json').write_text(json.dumps(data,indent=2)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':data['name']})+'\n')
    (out/'CREDITS.txt').write_text('G3: supplied lightning link, branch and prong drawings; four-band quantisation, original coverage alpha.\n')
    return data


def _build_bolt_definition(data, root, out):
    assets=validate_bolt_chain(data,root,False)
    if out.exists() and any(out.iterdir()): raise ValueError('Output must be empty')
    if any(p.is_relative_to(out) for p in assets.values()): raise ValueError('Output overlaps inputs')
    out.mkdir(parents=True,exist_ok=True)
    for src,path in assets.items():
        target=out/src
        if Path(src).is_absolute() or not target.resolve().is_relative_to(out): raise ValueError('G3 build requires confined relative assets')
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
    (out/'kit.json').write_text(json.dumps(data,indent=2)+'\n')
    (out/'CREDITS.txt').write_text('G3: supplied indexed lightning primitives.\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':data['name']})+'\n')
    return {'id':'effect_kit','subject':data['name'],'passed':None,'value':{'grammar':'G3'},'threshold':None,'op':None,'unit':'kit','evidence':[str(out/'kit.json')],'notes':'Explicit instant bolt / chain.'}


# T4u: owner-tracked support aura; the authored schedule is never repaired.
def validate_aura_loop(data, root, runtime=False):
    required={'name','element','element_class','screen_px','ground_squash','material','phases','layers','skill_spec','g4'}
    _keys(data,required|{'pierce'},required,'G4 kit')
    if not isinstance(data['name'],str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',data['name']):
        raise ValueError('name must be a safe identifier')
    spec=data['skill_spec'];m=spec['mechanics'];p=spec['presentation'];g=data['g4']
    if spec['grammar']!='G4' or any(m.get(k)!=v for k,v in dict(origin_socket='caster_root',aim_rule='owner-tracking',stack='refresh',termination='duration').items()):
        raise ValueError('unsupported G4 mechanics; no inferred grammar')
    if data['screen_px'] is not True or data['element_class']!='support' or data['element']!=spec['visual_treatment_id'] or data['ground_squash']!=.58:
        raise ValueError('G4 requires support, screen_px and 0.58 orbit ellipse')
    for key in ('radius_px','duration_s'): _number(m[key],1/60,4096,key)
    _number(m['pulse_cv_min'],.25,1,'pulse_cv_min')
    # Structural validity and the conductor's FF-08 assertion are separate.
    tick_schedule_report(m['pulse_schedule_s'],m['pulse_cv_min'])
    if m['pulse_schedule_s'][-1]>=m['duration_s']: raise ValueError('pulse outside aura lifetime')
    if len({round(v*60) for v in m['pulse_schedule_s']})!=len(m['pulse_schedule_s']): raise ValueError('pulses collide on the 60 Hz clock')
    envelope=p['phase_envelope_s']
    if envelope['loop']!=m['duration_s'] or envelope['petal_life']!=.45: raise ValueError('G4 envelope disagrees')
    _number(envelope['ring_orbit_period'],1/60,60,'ring_orbit_period')
    if data['layers']!={'dark_duplicate':False,'glow':{'alpha':.2,'scale':1.02},'floor_light':{'duration_s':m['duration_s'],'radius_px':m['radius_px']}}:
        raise ValueError('G4 support requires halo, floor light and dark duplicate OFF')
    material=validate_material(data['material'])
    if material['blend_mode']!='ADD' or not material.get('erode_outside_in') or material.get('dissolve_order')!=[[3],[2],[1,0]]:
        raise ValueError('G4 requires ADD, outside-in release and dissolve 3,2,1+0')
    _keys(g,{'ring','petal','seal','seed','release_s','support_tint','seal_aspect'},{'ring','petal','seal','seed','release_s','support_tint','seal_aspect'},'g4')
    _number(g['seal_aspect'],.01,4,'seal_aspect')
    with Image.open(_png(g['seal']['png'],root,confined=runtime)) as im:
        box=im.getchannel('A').getbbox()
    if not box or abs(g['seal_aspect']-(box[3]-box[1])/(box[2]-box[0]))>1e-9:
        raise ValueError('seal_aspect disagrees with alpha bbox')
    _number(g['seed'],0,2**32-1,'seed',True)
    if g['release_s']!=.3 or g['support_tint']!=[1.,.94,.72,1.]: raise ValueError('G4 support/release contract disagrees')
    assets={}
    for role in ('ring','petal','seal'):
        item=g[role];_keys(item,{'png','pivot','scale'},{'png','pivot','scale'},role)
        if not isinstance(item['pivot'],list) or len(item['pivot'])!=2: raise ValueError('pivot requires xy')
        for v in item['pivot']: _number(v,0,511,'pivot')
        _number(item['scale'],.01,4,'scale')
        if role=='seal' and item['scale']!=1.: raise ValueError('seal is already foreshortened; scale 1.0 required')
        assets[item['png']]=_png(item['png'],root,confined=runtime)
    _keys(data['phases'],set(PHASES),{'cast','travel','impact'},'phases')
    for phase in data['phases'].values():
        if not phase['frames']: raise ValueError('empty phase')
        for f in phase['frames']:
            _number(f['hold_frames'],1,math.inf,'hold_frames',True)
        for src in [phase['sheet'],*[f['file'] for f in phase['frames']]]: assets[src]=_png(src,root,confined=runtime)
    for path in assets.values():
        with Image.open(path) as im:
            a=np.asarray(im)
            if im.mode!='RGBA' or im.size!=(512,512) or not np.any(a[...,3]): raise ValueError('G4 requires nonempty 512 RGBA')
        rgb=a[...,:3][a[...,3]>0]
        if not np.isin(rgb,[0,85,170,255]).all() or np.any(rgb[:,0]!=rgb[:,1]) or np.any(rgb[:,1]!=rgb[:,2]): raise ValueError('G4 requires four greyscale index planes')
    return assets


def build_aura_loop(spec_path, primitive_paths, out_dir, seed=2026):
    spec=json.loads(Path(spec_path).read_text());out=Path(out_dir).resolve()
    if out.exists() and any(out.iterdir()): raise ValueError('Output must be empty')
    out.mkdir(parents=True,exist_ok=True);(out/'primitives').mkdir()
    g=dict(seed=seed,release_s=.3,support_tint=[1.,.94,.72,1.])
    for role in ('ring','petal','seal'):
        with Image.open(primitive_paths[role]) as im: a=quantise_projectile(np.asarray(im.convert('RGBA')))
        y,x=np.nonzero(a[...,3]);pivot=[float((x.min()+x.max())/2),float(y.max() if role=='petal' else (y.min()+y.max())/2)]
        scale=(spec['presentation']['body_extents_bh']['petal']*130/(y.max()-y.min()+1) if role=='petal' else 1.)
        if role=='seal': g['seal_aspect']=float((y.max()-y.min()+1)/(x.max()-x.min()+1))
        file='primitives/'+role+'.png';Image.fromarray(a).save(out/file);g[role]=dict(png=file,pivot=pivot,scale=float(scale))
    phases={}
    for phase,folder in [('cast','flare'),('travel','travel'),('impact','impact')]:
        (out/folder).mkdir();file=f'{folder}/{folder}_00.png';(out/file).write_bytes((out/g['petal']['png']).read_bytes())
        phases[phase]=dict(sheet=file,frames=[dict(file=file,hold_frames=1)])
    m=spec['mechanics']
    data=dict(name=spec['skill_id']+'_e3',element=spec['visual_treatment_id'],element_class='support',screen_px=True,ground_squash=.58,
              material=dict(palette=[[.18,.14,.055,1],[.52,.43,.19,1],[.88,.77,.43,1],[1.,.96,.78,1]],blend_mode='ADD',light_participation=False,erode_outside_in=True,dissolve_order=[[3],[2],[1,0]]),
              phases=phases,layers={'dark_duplicate':False,'glow':{'alpha':.2,'scale':1.02},'floor_light':{'duration_s':m['duration_s'],'radius_px':m['radius_px']}},skill_spec=spec,g4=g,pierce=0)
    validate_aura_loop(data,out,True)
    (out/'kit.json').write_text(json.dumps(data,indent=2)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':data['name']})+'\n')
    (out/'CREDITS.txt').write_text('G4: supplied holy ring, folded petal and interrupted seal; quantised index RGB, original alpha.\n')
    return data


def _build_aura_definition(data, root, out):
    assets=validate_aura_loop(data,root,False)
    if out.exists() and any(out.iterdir()): raise ValueError('Output must be empty')
    if any(p.is_relative_to(out) for p in assets.values()): raise ValueError('Output overlaps inputs')
    for src in assets:
        if Path(src).is_absolute() or not (out/src).resolve().is_relative_to(out): raise ValueError('G4 requires confined relative assets')
    out.mkdir(parents=True,exist_ok=True)
    for src,path in assets.items():
        target=out/src;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
    (out/'kit.json').write_text(json.dumps(data,indent=2)+'\n')
    (out/'vfx_select.json').write_text(json.dumps({'source':'effect_kit','name':data['name']})+'\n')
    (out/'CREDITS.txt').write_text('G4: supplied indexed holy primitives.\n')
    return {'id':'effect_kit','subject':data['name'],'passed':None,'value':{'grammar':'G4'},'threshold':None,'op':None,'unit':'kit','evidence':[str(out/'kit.json')],'notes':'Authored pulse schedule retained; assert_tick_schedule is the separate FF-08 instrument.'}


def orb_schedule_report(data):
    m = data['skill_spec']['mechanics']
    flight = min(math.ceil(m['range_px']/m['speed_px_s']*60), math.ceil(m['expiry']['time_s']*60))
    choices = data['orb']['interval_frames_choices']
    if not isinstance(choices, list) or len(choices) < 2:
        raise ValueError('orb.interval_frames_choices requires at least two distinct choices')
    for choice in choices:
        _number(choice, 1, math.inf, 'orb.interval_frames_choices', True)
    if len(set(choices)) < 2:
        raise ValueError('orb.interval_frames_choices requires at least two distinct choices')
    _number(data['orb']['seed'], 0, 2147483647, 'orb.seed', True)
    rng = random.Random(data['orb']['seed'])
    if data['orb'].get('interval_draw') != 'balanced_shuffle':
        raise ValueError('orb.interval_draw must be balanced_shuffle')
    intervals = choices * math.ceil(math.ceil(flight/min(choices))/len(choices))
    rng.shuffle(intervals)
    ages, age = [], 0
    for interval in intervals:
        age += interval
        if age > flight:
            break
        ages.append(age)
    report = tick_schedule_report([(age-ages[0])/60 for age in ages])
    return dict(report, emission_ages=ages, emission_count=len(ages), flight_frames=flight,
                expiry_distance_px=min(m['range_px'], m['speed_px_s']*flight/60),
                range_reached=m['range_px'] <= m['speed_px_s']*flight/60)


def validate_orb(data, root, runtime=False):
    spec=data.get('skill_spec', {}); m=spec.get('mechanics', {}); g=data['orb']
    _keys(m, {'origin_socket','aim_rule','range_px','speed_px_s','count','emission','expiry','termination','pierce'},
          {'origin_socket','aim_rule','range_px','speed_px_s','count','emission','expiry','termination','pierce'}, 'orb.mechanics')
    if (spec.get('grammar') != 'G1' or m['origin_socket'] != 'cast_release' or m['aim_rule'] != 'release-locked'
            or m['termination'] != 'expiry' or m['pierce'] != -1 or m['count'] != 1
            or data.get('pierce') != -1 or not data.get('screen_px') or data['element'] != spec['visual_treatment_id']):
        raise ValueError('unsupported orb G1 mechanics or treatment')
    for key in ('range_px','speed_px_s'): _number(m[key], 1e-9, math.inf, key)
    if data['phases']['travel']['speed_px_s'] != m['speed_px_s']: raise ValueError('orb speed disagrees')
    _keys(m['emission'], {'child','schedule','child_speed_px_s','child_range_px'}, {'child','schedule','child_speed_px_s','child_range_px'}, 'emission')
    if m['emission']['schedule'] != 'every 2–4 frames (seeded balanced shuffle, FF-08), spiral, 3 per revolution': raise ValueError('unsupported explicit emission schedule')
    for key in ('child_speed_px_s','child_range_px'): _number(m['emission'][key], 1e-9, math.inf, key)
    if m['expiry']['kind'] != 'range_or_time' or m['expiry']['on_expiry'] != 'shard_burst 16 radial': raise ValueError('unsupported expiry')
    _number(m['expiry']['time_s'], 1e-9, math.inf, 'expiry.time_s')
    required={'interval_draw','expiry_mode','expiry_core_bh','expiry_decal','body','shard','interval_frames_choices','angle_step_deg','seed','pool_size','turn_s','rim_count','rim_radius_px','expiry_count','child_pierce'}
    _keys(g, required, required, 'orb')
    orb_schedule_report(data)  # Validates choices and reports FF-08 without changing its threshold.
    if (g['angle_step_deg'] != 137 or g['turn_s'] != 1.2
            or g['rim_count'] != 4 or g['expiry_count'] != 16 or g['child_pierce'] != 0): raise ValueError('orb emission/rotation/count disagrees')
    if g['expiry_mode'] not in ('peak','nova'): raise ValueError('orb.expiry_mode must be peak or nova')
    _number(g['expiry_core_bh'],.4,1.2,'orb.expiry_core_bh')
    if not isinstance(g['expiry_decal'],bool): raise ValueError('orb.expiry_decal must be boolean')
    if g['expiry_mode']=='nova' and g['expiry_decal']: raise ValueError('nova has no decal')
    _number(g['seed'],0,2147483647,'orb.seed',True)
    _number(g['pool_size'], math.ceil(m['emission']['child_range_px']/m['emission']['child_speed_px_s']*60/min(g['interval_frames_choices']))+2,64,'orb.pool_size',True)
    _number(g['rim_radius_px'],1,256,'orb.rim_radius_px')
    if (data['pieces']['template'] != 'burst_v1r' or data['pieces']['hold_frames'] != 2
            or data['decal_s'] != spec['presentation']['phase_envelope_s']['residue']): raise ValueError('orb expiry pieces/decal disagree')
    _,record,_=load_pieces(data['pieces'],root,runtime)
    if len(record['pieces']) != g['expiry_count']: raise ValueError('orb expiry requires 16 pieces')
    assets={}
    for role in ('body','shard'):
        item=g[role];_keys(item,{'png','pivot','scale','binding'} | ({'collision_radius_bh'} if role == 'shard' else set()),{'png','pivot','scale','binding'},'orb.'+role)
        if role == 'shard': _number(item.get('collision_radius_bh', .15), .1, .5, 'orb.shard.collision_radius_bh')
        expected=spec['presentation']['primitive_bindings']['travel_head' if role=='body' else 'child']
        if item['binding'] != expected: raise ValueError('orb primitive binding disagrees')
        assets[item['png']]=_png(item['png'],root,True,runtime)
        _number(item['scale'],1e-9,1,'orb.scale')
        if not isinstance(item['pivot'],list) or len(item['pivot'])!=2: raise ValueError('orb pivot requires x,y')
        with Image.open(assets[item['png']]) as im:
            for value,extent in zip(item['pivot'],im.size): _number(value,0,extent,'orb.pivot')
    return assets


def validate_motes(value, residue=False):
    """Bound opt-in pools and physical sizes; omission leaves legacy data alone."""
    keys = {'count','size_px','life_s','rise_px_s','lateral_px','bands'} if residue else {'rate_per_s','size_px','life_s','rise_px_s','lateral_px','bands'}
    _keys(value, keys, keys if residue else keys-{'bands'}, 'embers' if residue else 'trail')
    def pair(key, lo, hi, integer=False):
        v=value[key]
        if not isinstance(v,list) or len(v)!=2: raise ValueError(key+' requires ordered bounds')
        for x in v: _number(x,lo,hi,key,integer)
        if v[0]>v[1]: raise ValueError(key+' requires ordered bounds')
    pair('size_px',3,5 if residue or 'bands' in value else 4,True)
    if not residue and 'bands' in value and value['bands'] != [3,2]: raise ValueError('trail.bands must be [3,2]')
    if residue:
        pair('count',8,12,True); pair('life_s',.5,.9)
        if value['bands'] != [2,3] or any(type(x) is not int for x in value['bands']): raise ValueError('embers.bands must be [2,3]')
    else:
        _number(value['rate_per_s'],1,20,'trail.rate_per_s')
        _number(value['life_s'],.1,.5,'trail.life_s')
    _number(value['rise_px_s'],0,80,'rise_px_s')
    _number(value['lateral_px'],0,20,'lateral_px')


def validate_fire_layer(name, value):
    keys=LAYER_KEYS[name]
    _keys(value,keys,set(),name)
    if name=='cast':
        for role,item in value.items():
            fields={'scale','frames'} if role=='muzzle_puff' else {'radius_bh','frames','alpha'}
            _keys(item,fields,fields,'cast.'+role)
            _number(item['frames'],2,8,'cast.frames',True)
            if role=='muzzle_puff': _number(item['scale'],.3,.6,'cast.scale')
            else:
                _number(item['radius_bh'],.5,1.2,'cast.radius_bh')
                _number(item['alpha'],.2,.8,'cast.alpha')
    else:
        if 'flicker_frames' in value: _number(value['flicker_frames'],1,8,'travel.flicker_frames',True)
        if 'erode_noise' in value: _number(value['erode_noise'],0,1,'travel.erode_noise')
        if 'trail' in value: validate_motes(value['trail'])
        for role in ('core','halo','boil','smear','eruption'):
            if role in value:
                fields = TRAVEL_RANGES[role]
                _keys(value[role], set(fields), set(fields), 'travel.'+role)
                for key,(lo,hi,integer) in fields.items(): _number(value[role][key],lo,hi,'travel.'+role+'.'+key,integer)
        if 'eruption' in value and value['eruption']['sheet_delay_frames'] >= value['eruption']['frames']: raise ValueError('eruption sheet delay must precede full size')
        if 'boil' in value and value.get('erode_noise',0) <= 0: raise ValueError('travel.boil requires erode_noise')


# FL-3: absent fields are OFF, with no defaults inserted into legacy metadata.
ANTI_DECAL_RANGES = {
    'core': {'band': (3,3,True), 'alpha': (0,1,False), 'blur_px': (0,12,False)},
    'contact_light': {'lerp': (0,1,False), 'frames': (1,30,True)},
    'shimmer': {'amplitude_px': (0,6,False), 'seconds': (.1,1.5,False)},
    'boil': {'uv_per_s': (0,1,False), 'erode_amp': (0,.15,False), 'hz': (0,15,False)},
}

def validate_anti_decal(name, value):
    fields = ANTI_DECAL_RANGES[name]
    _keys(value, set(fields), set(fields), name)
    for key, (lo, hi, integer) in fields.items():
        _number(value[key], lo, hi, name+'.'+key, integer)


# FL-4a: strict opt-in fields; omission leaves every old clock and resource alone.
TRAVEL_RANGES = {
    'eruption': {'frames':(1,60,True),'scale_from':(.01,1,False),'sheet_delay_frames':(0,59,True)},
    'core': {'band':(3,3,True),'alpha':(0,1,False),'blur_px':(0,12,False),'pulse_scale':(1,1.2,False),'hz':(1,15,False)},
    'halo': {'alpha':(0,1,False),'scale':(1,2,False)},
    'boil': {'uv_per_s':(0,1,False),'erode_amp':(0,.15,False),'hz':(1,15,False)},
    'smear': {'band':(2,2,True),'alpha':(0,1,False),'length_bh':(.1,2,False),'frames':(1,12,True)},
}

def validate_ember_ending(value):
    scalar = {'amount':(16,64,True),'glow_radius_bh':(.1,2,False),'glow_alpha':(0,1,False),'glow_s':(.1,1.5,False),'core_radius_bh':(.1,1,False),'core_s':(.1,1,False)}
    pairs = {'rect_bh':(.1,3),'life_s':(.9,1.6),'speed_px_s':(1,120),'scale':(.05,.5)}
    _keys(value,set(scalar)|set(pairs)|{'spread_deg'},set(scalar)|set(pairs),'ember_ending')
    if 'spread_deg' in value: _number(value['spread_deg'],0,90,'ember_ending.spread_deg')
    for key,(lo,hi,integer) in scalar.items(): _number(value[key],lo,hi,'ember_ending.'+key,integer)
    for key,(lo,hi) in pairs.items():
        pair=value[key]
        if not isinstance(pair,list) or len(pair)!=2: raise ValueError('ember_ending.'+key+' requires pair')
        for number in pair: _number(number,lo,hi,'ember_ending.'+key)
        if key != 'rect_bh' and pair[0]>pair[1]: raise ValueError('ember_ending.'+key+' bounds reversed')
    if value['life_s'][0] > (114-50)/60: raise ValueError('ember_ending minimum life cannot fit total deadline')


def validate_fire_ending(role, value):
    fields = {'scale_bh':(.1,1,False),'seconds':(.1,1,False)} if role == 'core_residue' else {'radius_bh':(.1,2,False),'alpha':(0,1,False),'rise_px_s':(0,80,False),'seconds':(.1,1.5,False)}
    extra = set() if role == 'core_residue' else {'sheet','tint'}
    _keys(value, set(fields)|extra, set(fields)|extra, role)
    for key,(lo,hi,integer) in fields.items(): _number(value[key],lo,hi,role+'.'+key,integer)
    if role == 'smoke':
        if value['sheet'] != 'noise': raise ValueError('smoke.sheet must be noise')
        if not isinstance(value['tint'],list) or len(value['tint']) != 3: raise ValueError('smoke.tint requires RGB')
        for channel in value['tint']: _number(channel,0,1,'smoke.tint')
