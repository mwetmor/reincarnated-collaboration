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
import time

import numpy as np
from PIL import Image

PHASES = {'cast': 'flare', 'travel': 'travel', 'impact': 'impact', 'residual': 'residual'}
TOP = {'name', 'element', 'element_class', 'tint', 'phases', 'layers', 'ground_squash', 'pixel_scale', 'phase_scale', 'material', 'distance_fields', 'pierce', 'pieces', 'screen_px', 'erode_noise'}
LAYER_KEYS = {
    'glow': {'alpha', 'scale'}, 'floor_light': {'duration_s', 'radius_px'},
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
    if pieces.get('template') != 'burst_v2':
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



def write_vfx_material(out, resource, material, distance_texture, dark_duplicate=False, noise_texture=None):
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
    shader_rel = shader.relative_to(out).as_posix()
    target.parent.mkdir(parents=True, exist_ok=True)
    shader.write_text(shader_source(mode, lit, order, material.get('erode_outside_in', False), noise))
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
            if a.mode != 'RGB' or a.size != b.size:
                raise ValueError('noise_texture must be RGB and match the whole-body distance')
        lines[0] = '[gd_resource type="ShaderMaterial" load_steps=4 format=3]'
        lines.insert(3, f'[ext_resource type="Texture2D" path="res://{noise_path.relative_to(out).as_posix()}" id="Noise"]')
        lines.append('shader_parameter/erosion_noise_texture = ExtResource("Noise")')
        lines.append('shader_parameter/erode_noise = '+repr(float(noise)))
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


def piece_stretch(seed, piece_id):
    """Stable, order-independent v2 samples; v1 sampling is unchanged."""
    digest = hashlib.sha256(f'{seed}:{piece_id}'.encode('ascii')).hexdigest()
    return {'along': 2.0 + .5 * int(digest[:8], 16) / 4294967295,
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


def load_pieces(config, root, runtime=False):
    """Consume T4e schema 2 as delivered; never segment or recolour a shard."""
    root = Path(root).resolve()
    _keys(config, {'source', 'template', 'root_drift', 'dissolve_order', 'erode_noise', *PIECES_DEFAULTS}, {'source', 'template'}, 'pieces')
    if config['template'] not in ('burst_v1', 'burst_v2'):
        raise ValueError('pieces.template must be burst_v1 or burst_v2')
    _number(config.get('erode_noise', 0), 0, 1, 'pieces.erode_noise')
    values = {**PIECES_DEFAULTS, **config}
    _number(values['hold_frames'], 1, 2, 'pieces.hold_frames', True)
    _number(values['base_speed_px_s'], 1e-9, math.inf, 'pieces.base_speed_px_s')
    _number(values['residue_s'], .3, 1, 'pieces.residue_s')
    _number(values['residue_fraction'], .15, .25, 'pieces.residue_fraction')
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
    assets = {}
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
    peak = _png(record.get('peak_index'), path.parent, grayscale=True, confined=True)
    with Image.open(peak) as image:
        if list(image.size) != canvas: raise ValueError('peak_index must match pieces.canvas')
    key = peak.relative_to(root).as_posix() if peak.is_relative_to(root) else str(peak)
    assets[key] = peak
    return values, record, assets


def _validate(data, root, runtime=False):
    _reject_retired(data)
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
    frame_paths = {assets[frame['file']] for phase in data['phases'].values()
                   for frame in phase['frames']}
    _keys(data['layers'], set(LAYER_KEYS)|{'dark_duplicate'}, set(), 'layers')
    for name, layer in data['layers'].items():
        if name == 'dark_duplicate':
            if not isinstance(layer, bool): raise ValueError('dark_duplicate must be boolean')
            continue
        fields = LAYER_KEYS[name]
        optional = ({'file'} if name == 'decal' else
                    {'amount', 'lifetime_s'} if name == 'particles' else set())
        _keys(layer, fields, fields-optional, name)
        for key, value in layer.items():
            if key in ('file', 'texture'):
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
        _, _, piece_assets = load_pieces(data['pieces'], root, runtime)
        assets.update(piece_assets)
    for path in set(assets.values()):
        with Image.open(path) as image: rgba = np.array(image.convert('RGBA'))
        rgb = rgba[..., :3][rgba[..., 3] > 0]
        if np.any(rgb[:, 0] != rgb[:, 1]) or np.any(rgb[:, 1] != rgb[:, 2]) or not np.isin(rgb, [0, 85, 170, 255]).all():
            raise ValueError('material source indices must be greyscale 0/85/170/255: '+str(path))
    if runtime:
        fields = data.get('distance_fields')
        if not isinstance(fields, dict) or set(fields) != set(assets):
            raise ValueError('distance_fields must map every kit texture')
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
        metadata['pieces'] = dict(config, source='pieces/pieces.json')
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
