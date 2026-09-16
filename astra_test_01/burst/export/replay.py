"""Godot 4.6 native-crop, fixed-seed replay and Movie Maker instruments.

No particle substitution, dropped layers, frame repair or background removal.
Unsupported seed controls and engine/render failures are reported as evidence.
The plate instrument reports thresholded composite-minus-plate support separately
from the frozen alpha/black-support oracle. Blend-class bakes carry age metadata.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import time

import numpy as np
from PIL import Image

from oracle.sheet_pack import numbered_frames

GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'


def _result(ident, subject, value, threshold, op, unit, notes='', evidence=(), passed=None):
    return {'id': ident, 'subject': subject, 'passed': passed, 'value': value,
            'threshold': threshold, 'op': op, 'unit': unit,
            'evidence': list(map(str, evidence)), 'notes': notes}


def _integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(name + ' must be an integer >= ' + str(minimum))
    return value


def _crop(crop):
    if len(crop) != 2:
        raise ValueError('crop must have two dimensions')
    for value in crop:
        _integer(value, 'crop dimension', 1)
        if value > 512 and tuple(crop) != (768, 768):
            raise ValueError('Native crop must not exceed 512x512, except the 768x768 burst crop')
    return tuple(crop)


# Installed only when bake=True, preserving the legacy export byte-for-byte.
BAKE_HOOK = '''extends Node
# Hide initial scene drawables individually. Ancestors and scripts remain live;
# subsequently spawned effect nodes, floor light, tint, hit-stop and shake survive.
func _ready() -> void:
    get_tree().process_frame.connect(_configure, CONNECT_ONE_SHOT)

static func hide_scene(node: Node) -> Array:
    var hidden: Array = []
    if node.is_in_group("replay_effect"):
        return hidden
    if node is Sprite2D or node is AnimatedSprite2D or node is Polygon2D or node is Line2D or node is Control or node is GPUParticles2D or node is CPUParticles2D or node is TileMapLayer or node is TileMap:
        node.hide()
        hidden.append(str(node.get_path()))
    for child in node.get_children():
        hidden.append_array(hide_scene(child))
    return hidden

func _configure() -> void:
    get_viewport().transparent_bg = true
    if get_tree().current_scene != null:
        hide_scene(get_tree().current_scene)
'''


PROBE = '''extends SceneTree
const VisibilityHook = preload("res://scripts/replay_visibility.gd")
var config: Dictionary
var report: Dictionary = {"frames": [], "particle_controls": [], "hidden": [], "probe_only": false}
var world: Node
var effect: Node2D
var camera: Camera2D
var release_tick: int = 0
var captures: int = 0
var started: bool = false
var flip_layers: Array = []
var effect_age: float = 0.0
var selected_indices: Array = []

func _advance_clock() -> void:
    if started:
        effect_age += Engine.time_scale

func _blend_class(node: CanvasItem) -> String:
    var owner: CanvasItem = node
    while owner.use_parent_material and owner.get_parent() is CanvasItem:
        owner = owner.get_parent()
    var material: Material = owner.material
    if material is CanvasItemMaterial:
        if material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD:
            return "add"
        if material.blend_mode != CanvasItemMaterial.BLEND_MODE_MIX:
            return "unsupported"
    if material is ShaderMaterial:
        var code: String = material.shader.code
        if "blend_add" in code:
            return "add"
        for mode in ["blend_sub", "blend_mul", "blend_premul_alpha", "blend_disabled"]:
            if mode in code:
                return "unsupported"
    return "mix"

func _filter_layers(node: Node) -> void:
    if node is Sprite2D or node is AnimatedSprite2D or node is Polygon2D or node is Line2D or node is CPUParticles2D or node is GPUParticles2D:
        var mode := _blend_class(node)
        if mode == "unsupported":
            push_error("Unsupported bake blend: " + str(node.get_path()))
        if not node.has_meta("replay_blend_recorded"):
            report.get_or_add("blend_layers", []).append({"node": str(node.get_path()), "blend": mode, "z_index": node.z_index})
            node.set_meta("replay_blend_recorded", true)
        if mode != str(config.bake_layer):
            # Scripts may call show() later (Residual). Cull without changing
            # authored visibility, animation callbacks, or emission schedules.
            node.visibility_layer = 0
    for child in node.get_children():
        _filter_layers(child)

func _before_draw() -> void:
    if bool(config.bake) and config.bake_layer != "all" and is_instance_valid(effect):
        _filter_layers(effect)
    _set_flip_frame()

func _initialize() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string("res://replay_config.json"))
    Engine.physics_ticks_per_second = 60
    Engine.time_scale = 1.0
    seed(int(config.seed))
    root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
    root.content_scale_size = Vector2i(int(config.crop[0]), int(config.crop[1]))
    root.size = Vector2i(int(config.crop[0]), int(config.crop[1]))
    root.transparent_bg = bool(config.bake)
    report.probe_only = bool(config.get("probe_only", false))
    report.viewport_size = [root.size.x, root.size.y]
    report.physics_ticks_per_second = Engine.physics_ticks_per_second
    call_deferred("_setup")

func _setup() -> void:
    world = load(config.world).instantiate()
    root.add_child(world)
    current_scene = world
    # Camera is independent of hidden Keeper art; its shake feedback stays live.
    for node in world.find_children("*", "Camera2D", true, false):
        node.enabled = false
    camera = Camera2D.new()
    camera.zoom = Vector2.ONE
    camera.position = Vector2(float(config.origin[0]), float(config.origin[1]))
    root.add_child(camera)
    camera.make_current()
    camera.reset_smoothing()
    camera.force_update_scroll()
    if bool(config.bake):
        report.hidden = VisibilityHook.hide_scene(world)
    elif str(config.get("background", "ground")) != "ground":
        report.hidden = VisibilityHook.hide_scene(world)
        var background := Sprite2D.new()
        var background_image: Image
        if config.background in ["black", "white"]:
            background_image = Image.create(int(config.crop[0]), int(config.crop[1]), false, Image.FORMAT_RGBA8)
            background_image.fill(Color.BLACK if config.background == "black" else Color.WHITE)
        else:
            background_image = Image.load_from_file(config.background_path)
        background.texture = ImageTexture.create_from_image(background_image)
        background.position = camera.position
        background.z_index = -4096
        root.add_child(background)
    for keeper in world.find_children("Keeper", "", true, false):
        keeper.set_physics_process(false)
    reset_effect()
    var definitions: Array = config.get("flipbook_layers", [])
    if not definitions.is_empty():
        if is_instance_valid(effect):
            effect.hide()
        var overlay := CanvasLayer.new()
        overlay.layer = 100
        root.add_child(overlay)
        for definition in definitions:
            var flip_textures: Array[ImageTexture] = []
            for path in definition.paths:
                var image := Image.load_from_file(str(path))
                if image == null or image.is_empty() or image.get_size() != Vector2i(int(config.crop[0]), int(config.crop[1])) or image.get_format() != Image.FORMAT_RGBA8:
                    report.flipbook_error = {"path": str(path), "image_size": str(image.get_size()) if image != null else "null", "viewport_size": str(root.size), "image_format": image.get_format() if image != null else -1}
                    push_error("Invalid flipbook RGBA image: " + str(path))
                    _finish()
                    return
                flip_textures.append(ImageTexture.create_from_image(image))
            var flip_sprite := Sprite2D.new()
            flip_sprite.centered = true
            flip_sprite.position = Vector2(root.size) * 0.5
            flip_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
            var material := CanvasItemMaterial.new()
            material.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD if definition.blend == "add" else CanvasItemMaterial.BLEND_MODE_MIX
            material.light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
            flip_sprite.material = material
            overlay.add_child(flip_sprite)
            flip_layers.append({"sprite": flip_sprite, "textures": flip_textures, "ages": definition.ages})
        report.flipbook_loaded = definitions.size()
        _set_flip_frame()
    physics_frame.connect(_advance_clock)
    # frame_pre_draw changes arrive one render late on Compatibility.
    process_frame.connect(_before_draw)
    _before_draw()
    if bool(config.get("probe_only", false)):
        process_frame.connect(func(): call_deferred("_capture"))
    else:
        RenderingServer.frame_post_draw.connect(_capture)
    started = true

func _set_flip_frame() -> void:
    selected_indices.clear()
    for layer in flip_layers:
        var index: int = 0
        # The source already contains hit-stop holds. Sample its recorded age,
        # never apply a second hold to an assumed uniform capture-count clock.
        for i in range(layer.ages.size()):
            if float(layer.ages[i]) <= effect_age + 0.00001:
                index = i
            else:
                break
        var flip_textures: Array = layer.textures
        var flip_sprite: Sprite2D = layer.sprite
        flip_sprite.texture = flip_textures[index]
        selected_indices.append(index)

func seed_particles(node: Node) -> void:
    if node is GPUParticles2D or node is CPUParticles2D:
        var names: Array = []
        for prop in node.get_property_list():
            names.append(prop.name)
        var supported: bool = "use_fixed_seed" in names and "seed" in names
        if supported:
            node.set("use_fixed_seed", true)
            node.set("seed", int(config.seed))
        report.particle_controls.append({"node": str(node.name), "class": node.get_class(), "fixed_seed_supported": supported, "seed": int(config.seed) if supported else null})
    for child in node.get_children():
        seed_particles(child)

func reset_effect() -> void:
    # Each public replay runs in a fresh process: no old SceneTree timers,
    # pooled instances, shader time or deferred callbacks can leak across resets.
    if is_instance_valid(effect):
        effect.free()
    Engine.time_scale = 1.0
    seed(int(config.seed))
    if bool(config.get("blank", false)):
        release_tick = Engine.get_physics_frames()
        return
    effect = load(config.effect).instantiate()
    effect.add_to_group("replay_effect")
    # Keep the supplied scene's parent/z-order, including its floor-light layer.
    var effect_parent: Node2D = world.find_child("Actors", true, false) as Node2D
    if effect_parent == null:
        effect_parent = world as Node2D
    if effect_parent == null:
        push_error("Replay world must provide a Node2D effect parent")
        quit(2)
        return
    effect.position = effect_parent.to_local(Vector2(float(config.origin[0]), float(config.origin[1])))
    seed_particles(effect)
    effect_parent.add_child(effect)
    release_tick = Engine.get_physics_frames()

func _layer_states() -> Array:
    var states: Array = []
    if is_instance_valid(effect):
        for node in effect.find_children("*", "CanvasItem", true, false):
            if node is Sprite2D or node is AnimatedSprite2D or node is CPUParticles2D or node is GPUParticles2D:
                var state: Dictionary = {"node": str(effect.get_path_to(node)), "visible": node.is_visible_in_tree(), "alpha": node.modulate.a, "visibility_layer": node.visibility_layer}
                if node is AnimatedSprite2D:
                    state.animation_frame = node.frame
                states.append(state)
    return states

func _capture() -> void:
    if not started:
        return
    report.observed_window_size = [root.size.x, root.size.y]
    var age: int = Engine.get_physics_frames() - release_tick
    var visible_scene: Array = []
    for path in report.hidden:
        var node: Node = root.get_node_or_null(path)
        if node is CanvasItem and node.is_visible_in_tree():
            visible_scene.append(path)
    var floor_live: bool = is_instance_valid(effect) and effect.has_node("FloorLight") and effect.get_node("FloorLight").is_visible_in_tree()
    report.frames.append({"movie_index": captures, "physics_frame": age, "effect_age": effect_age, "flipbook_indices": selected_indices.duplicate(), "time_scale": Engine.time_scale, "camera_offset": [camera.offset.x, camera.offset.y], "visible_scene_drawables": visible_scene, "floor_light_live": floor_live, "effect_layers": _layer_states()})
    captures += 1
    if int(config.frame) >= 0 and age >= int(config.frame):
        if not bool(config.get("probe_only", false)):
            var image: Image = root.get_texture().get_image()
            var error: int = image.save_png(config.capture)
            report.capture_error = error
        report.requested_frame = int(config.frame)
        report.captured_frame = age
        _finish()
    elif int(config.frame) < 0 and captures >= int(config.frames):
        _finish()

func _finish() -> void:
    started = false
    var file := FileAccess.open(config.report, FileAccess.WRITE)
    file.store_string(JSON.stringify(report, "  "))
    file.close()
    quit()
'''


def install_hooks(project, crop=(512, 512)):
    """Add effect-only visibility and replay hooks to an exported project."""
    crop = _crop(crop)
    project = Path(project)
    settings = project / 'project.godot'
    text = settings.read_text()
    for name, value in [('viewport_width', crop[0]), ('viewport_height', crop[1])]:
        text = re.sub(r'(?m)^window/size/' + name + r'=.*$', 'window/size/' + name + '=' + str(value), text)
    text = text.replace('[rendering]\n', '[rendering]\nviewport/transparent_background=true\n', 1)
    if '[physics]' not in text:
        text += '\n[physics]\ncommon/physics_ticks_per_second=60\n'
    if '[autoload]' not in text:
        text += '\n[autoload]\nReplayVisibility="*res://scripts/replay_visibility.gd"\n'
    else:
        text = text.replace('[autoload]\n', '[autoload]\nReplayVisibility="*res://scripts/replay_visibility.gd"\n', 1)
    settings.write_text(native_crop_settings(text, crop))
    (project / 'scripts').mkdir(exist_ok=True)
    (project / 'scripts/replay_visibility.gd').write_text(BAKE_HOOK)
    (project / 'replay_probe.gd').write_text(PROBE)


def prepare_project(source, out, crop=(512, 512)):
    """Copy a read-only T4b export; all runtime writes stay in the copy."""
    source, out = Path(source).resolve(), Path(out).resolve()
    _crop(crop)
    if source == out or source.is_relative_to(out) or out.is_relative_to(source):
        raise ValueError('Source and output must not overlap')
    if out.exists():
        raise ValueError('Output must not already exist')
    if not (source / 'project.godot').is_file():
        raise ValueError('Missing source project')
    for path in source.rglob('*'):
        if path.is_symlink():
            raise ValueError('Symlink in source project')
    shutil.copytree(source, out)
    install_hooks(out, crop)
    return out


def movie_command(project, out, frames=126, godot=GODOT):
    """Actual Movie Maker PNG command: native viewport, 60 fixed FPS."""
    _integer(frames, 'frames', 1)
    return [str(godot), '--path', str(Path(project).resolve()), '--audio-driver', 'Dummy',
            '--log-file', str(Path(out).resolve() / 'engine.log'), '--disable-vsync',
            '--write-movie', str(Path(out).resolve() / 'fx.png'), '--fixed-fps', '60',
            '--quit-after', str(frames), '--script', 'res://replay_probe.gd', '--', '--bake']


def run_replay(project, out, effect='res://scenes/vfx_frozen_orb_impact.tscn',
               frame=None, frames=126, seed=1, crop=(512, 512),
               origin=(2285.62, 2407.32), bake=True, blank=False,
               godot=GODOT, timeout=120, background='ground', background_path=None,
               flipbook=None, probe_only=False, bake_layer='all'):
    """Fresh-process reset, advance N actual physics frames, then capture.

    frame=None uses Movie Maker for `frames` rendered frames; frame=N captures
    the first post-draw at physics age N and reports the observed age explicitly.
    A missed age is never relabeled. Engine errors are evidence, never success.
    """
    _crop(crop)
    _integer(seed, 'seed')
    _integer(frames, 'frames', 1)
    if frame is not None:
        _integer(frame, 'frame')
    if len(origin) != 2 or any(not math.isfinite(v) for v in origin):
        raise ValueError('origin must be a finite pair')
    if not isinstance(bake, bool) or not isinstance(blank, bool):
        raise ValueError('bake and blank must be boolean')
    if not isinstance(probe_only, bool):
        raise ValueError('probe_only must be boolean')
    if background not in ('ground', 'black', 'white', 'foliage'):
        raise ValueError('Unknown background')
    if background == 'foliage':
        if background_path is None:
            raise ValueError('Foliage requires an explicit native crop')
        with Image.open(background_path) as im:
            if im.size != tuple(crop):
                raise ValueError('Background must match native crop; no resampling')
    if bake_layer not in ('all', 'add', 'mix'):
        raise ValueError('bake_layer must be all, add or mix')
    if bake_layer != 'all' and not bake:
        raise ValueError('bake_layer requires bake=True')
    definitions = flipbook_layers(flipbook, frames, crop) if flipbook is not None else []
    flip_paths = [Path(p) for layer in definitions for p in layer['paths']]
    if flip_paths:
        if bake:
            raise ValueError('Flipbook comparison requires live background and matching frame count')
        for path in flip_paths:
            with Image.open(path) as im:
                if im.mode != 'RGBA' or im.size != tuple(crop):
                    raise ValueError('Flipbook must contain native RGBA crop frames')
    project, out = Path(project).resolve(), Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Replay output must be empty')
    effect_path = project / effect.removeprefix('res://')
    if not effect.startswith('res://') or not effect_path.resolve().is_relative_to(project) or not effect_path.is_file():
        raise ValueError('Effect must be an existing project-local scene')
    settings = (project / 'project.godot').read_text()
    world = re.search(r'(?m)^run/main_scene="([^"]+)"', settings)
    if world is None:
        raise ValueError('Missing main scene')
    out.mkdir(parents=True, exist_ok=True)
    config = {'world': world[1], 'effect': effect, 'frame': -1 if frame is None else frame,
              'frames': frames, 'seed': seed, 'crop': list(crop), 'origin': list(origin),
              'bake': bake, 'bake_layer': bake_layer, 'blank': blank, 'report': str(out / 'probe.json'),
              'capture': str(out / 'capture.png'), 'background': background,
              'background_path': str(Path(background_path).resolve()) if background_path else None,
              'flipbook': [str(p.resolve()) for p in flip_paths], 'flipbook_layers': definitions, 'probe_only': probe_only}
    (project / 'replay_config.json').write_text(json.dumps(config, indent=2))
    # The probe owns visibility, including the live comparison configuration.
    settings = re.sub(r'(?m)^ReplayVisibility=.*\n', '', settings)
    (project / 'project.godot').write_text(native_crop_settings(settings, crop))
    (project / 'replay_probe.gd').write_text(PROBE)
    command = movie_command(project, out, frames, godot)
    if frame is not None or probe_only:
        index = command.index('--write-movie')
        del command[index:index + 2]
        command[command.index('--quit-after') + 1] = str(max(120, (frame or frames) * 20 + 60))
    if probe_only:
        command.insert(1, '--headless')
    started = time.monotonic()
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        log = proc.stdout + proc.stderr
        code, timed_out = proc.returncode, False
    except subprocess.TimeoutExpired as exc:
        def text(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else (value or '')
        log, code, timed_out = text(exc.stdout) + text(exc.stderr), None, True
    (out / 'process.log').write_text(log)
    result = {'command': command, 'returncode': code, 'timed_out': timed_out,
              'wall_s': time.monotonic() - started, 'config': config,
              'engine_errors': [line for line in log.splitlines() if 'ERROR:' in line],
              'probe_exists': (out / 'probe.json').exists()}
    if bake and bake_layer != 'all' and code == 0 and not result['engine_errors']:
        encode_blend_bake(out, bake_layer)
    (out / 'run.json').write_text(json.dumps(result, indent=2) + '\n')
    return result



def native_crop_settings(settings, crop):
    """Set both OS window and viewport before creation; no content stretching."""
    crop = _crop(crop)
    entries = {'window/size/viewport_width': crop[0], 'window/size/viewport_height': crop[1],
               'window/size/window_width_override': crop[0], 'window/size/window_height_override': crop[1],
               'window/stretch/mode': '"disabled"'}
    if '[display]' not in settings:
        settings += '\n[display]\n'
    for key, value in entries.items():
        settings = re.sub(r'(?m)^' + re.escape(key) + r'=.*\n?', '', settings)
        settings = settings.replace('[display]\n', '[display]\n' + key + '=' + str(value) + '\n', 1)
    return settings


def effect_age_indices(ages, elapsed):
    """Latest source sample at/before each scaled physics age (no double hold)."""
    import bisect
    if not ages or any(not math.isfinite(a) or a < 0 for a in ages) or any(b <= a for a, b in zip(ages, ages[1:])):
        raise ValueError('Source ages must be finite, nonnegative and strictly increasing')
    return [max(0, bisect.bisect_right(ages, age + 1e-5) - 1) for age in elapsed]


def flipbook_layers(baked, frames, crop):
    """A legacy directory remains MIX; a mapping supplies explicit blend classes.

    New bakes record scaled physics ages. Legacy probe traces reconstruct those
    ages using the preceding tick's time_scale; absent traces imply uniform 60Hz.
    MIX then ADD is deliberately explicit, and cannot preserve interleaved z-order.
    """
    sources = baked if isinstance(baked, dict) else {'mix': baked}
    if not sources or set(sources) - {'mix', 'add'}:
        raise ValueError('Flipbook classes must be mix and/or add')
    layers = []
    for mode in ('mix', 'add'):
        if mode not in sources:
            continue
        directory = Path(sources[mode])
        paths = numbered_frames(directory)
        if len(paths) != frames:
            raise ValueError('Flipbook frame counts must match')
        for path in paths:
            with Image.open(path) as im:
                if im.mode != 'RGBA' or im.size != tuple(crop):
                    raise ValueError('Flipbook must contain native RGBA crop frames')
        ages = list(range(frames))
        probe = directory / 'probe.json'
        if probe.exists():
            trace = json.loads(probe.read_text())['frames']
            if len(trace) != frames:
                raise ValueError('Flipbook age/frame counts must match')
            if all('effect_age' in row for row in trace):
                ages = [row['effect_age'] for row in trace]
            else:
                ages = [0.0]
                for before, after in zip(trace, trace[1:]):
                    ages.append(ages[-1] + (after['physics_frame'] - before['physics_frame']) * before['time_scale'])
        effect_age_indices(ages, [0])
        layers.append(dict(blend=mode, paths=[str(p.resolve()) for p in paths], ages=ages))
    return layers


def encode_blend_bake(directory, blend):
    """Compatibility Movie Maker stores premultiplied RGB on transparent crops.

    MIX needs straight RGB; ADD needs the accumulated RGB with unit alpha on nonzero RGB
    (zero-contribution black padding remains transparent). Do not touch the default 'all' legacy PNG bytes.
    This cannot recover clipping or restore interleaved blend/world draw order.
    """
    if blend not in ('add', 'mix'):
        raise ValueError('Explicit blend class required')
    for path in numbered_frames(directory):
        with Image.open(path) as im:
            rgba = np.array(im.convert('RGBA'))
        if blend == 'add':
            rgba[..., 3] = np.where(np.any(rgba[..., :3] > 0, axis=-1), 255, 0)
        else:
            alpha = rgba[..., 3:4].astype(float)
            rgb = np.divide(rgba[..., :3].astype(float) * 255, alpha,
                            out=np.zeros_like(rgba[..., :3], dtype=float), where=alpha > 0)
            rgba[..., :3] = np.clip(np.rint(rgb), 0, 255).astype(np.uint8)
        Image.fromarray(rgba).save(path)
    (Path(directory) / 'blend.json').write_text(json.dumps(dict(blend=blend,
        encoding='accumulated_rgb_unit_alpha' if blend == 'add' else 'straight_rgba',
        source='Compatibility Movie Maker premultiplied RGBA'), indent=2) + '\n')


def plate_envelope(plate, composite, tau=8):
    """Count RGB max-channel absolute differences strictly greater than tau."""
    if isinstance(tau, bool) or not isinstance(tau, (int, float)) or not math.isfinite(tau) or not 0 <= tau <= 255:
        raise ValueError('tau must be finite in [0,255]')
    def pixels(value):
        if isinstance(value, (str, Path)):
            with Image.open(value) as im:
                return np.array(im.convert('RGB'), dtype=np.int16)
        array = np.asarray(value)
        if array.ndim != 3 or array.shape[-1] not in (3, 4):
            raise ValueError('Expected RGB or RGBA frame')
        return array[..., :3].astype(np.int16)
    a, b = pixels(plate), pixels(composite)
    if a.shape != b.shape:
        raise ValueError('Plate and composite dimensions must agree')
    return int(np.count_nonzero(np.abs(a-b).max(axis=-1) > tau))


def plate_envelope_comparison(project, out, baked, grounds=('ground', 'black', 'white', 'foliage'),
                              foliage_crop=None, tau=8, frames=126):
    """Independent plate/live/flip captures; fixed 5% per-frame relative support.

    Unlike alpha VO1, this measures visible change against a synchronized blank
    world. Feedback is deliberately live; plate differences include shake/tint.
    The summary is report-only; the caller owns the >=95% milestone decision.
    """
    _integer(frames, 'frames', 1)
    if not grounds or len(set(grounds)) != len(grounds) or set(grounds) - {'ground','black','white','foliage'}:
        raise ValueError('Need distinct supported grounds')
    if 'foliage' in grounds and foliage_crop is None:
        raise ValueError('Foliage requires an explicit native crop')
    first = next(iter(baked.values())) if isinstance(baked, dict) else baked
    paths = numbered_frames(first)
    if len(paths) != frames:
        raise ValueError('Bake frame count must match')
    with Image.open(paths[0]) as im:
        crop = im.size
    out = Path(out)
    envelopes, runs = {}, {}
    for ground in grounds:
        runs[ground], sequences = {}, {}
        for mode in ('plate', 'live', 'flip'):
            directory = out / ground / mode
            result = run_replay(project, directory, bake=False, blank=mode == 'plate',
                frames=frames, crop=crop, background=ground, background_path=foliage_crop,
                flipbook=baked if mode == 'flip' else None)
            runs[ground][mode] = result
            if result['returncode'] != 0 or result['engine_errors'] or not result['probe_exists']:
                raise RuntimeError('Replay did not complete: ' + str(directory))
            sequences[mode] = numbered_frames(directory)
            if len(sequences[mode]) != frames:
                raise ValueError('Plate/live/flip frame counts must agree')
        envelopes[ground] = {mode: [plate_envelope(a, b, tau) for a, b in zip(sequences['plate'], sequences[mode])]
                             for mode in ('live', 'flip')}
    rows, summary = [], {}
    for ground, values in envelopes.items():
        # Reuse literal comparator without relaxing its original four-ground API.
        same_live = {key: values['live'] for key in ('ground','black','white','foliage')}
        same_flip = {key: values['flip'] for key in same_live}
        group = [r for r in compare_vo1(same_live, same_flip) if r['subject'].startswith(ground + '/')]
        for row in group:
            row.update(relative_difference=row['value'], tolerance=0.05,
                       notes=f'Plate envelope: max-channel |composite-plate| > {tau}; zero baseline requires exact zero.')
        rows.extend(group)
        errors = [abs(y-x)/x if x else (0 if y == 0 else math.inf) for x,y in zip(values['live'], values['flip'])]
        summary[ground] = dict(frames=frames, failed=sum(r['passed'] is False for r in group),
            worst_frame=max(range(frames), key=errors.__getitem__), live_peak=max(values['live']), flip_peak=max(values['flip']))
    result = dict(rows=rows, summary=summary, envelopes=envelopes, tau=tau, tolerance=0.05)
    (out / 'envelopes.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    return result


def replay_to_frame(project, out, frame, **kwargs):
    """Reset-and-replay entry point; seed=1, crop=(512,512), physics=60 Hz."""
    return run_replay(project, out, frame=frame, **kwargs)


def background_comparisons(project, out, baked_frames, foliage_crop, **kwargs):
    """Capture independent live and flipbook runs on all four required grounds.

    Feed these captures to the frozen VO1 oracle, then compare_vo1. This helper
    does not silently substitute RGB error for VO1 or claim that alpha/additive
    layer flattening is background independent.
    """
    out = Path(out)
    results = {}
    for background in ('ground', 'black', 'white', 'foliage'):
        results[background] = {}
        for mode in ('live', 'flipbook'):
            results[background][mode] = run_replay(
                project, out / background / mode, bake=False, background=background,
                background_path=foliage_crop if background == 'foliage' else None,
                flipbook=baked_frames if mode == 'flipbook' else None, **kwargs)
    return results


def compare_bakes(first, second, prefix='fx'):
    """Exact encoded PNG hashes, plus decoded differing-pixel diagnostics."""
    a, b = numbered_frames(first, prefix), numbered_frames(second, prefix)
    rows = []
    for index in range(max(len(a), len(b))):
        left = a[index] if index < len(a) else None
        right = b[index] if index < len(b) else None
        hashes = [hashlib.sha256(p.read_bytes()).hexdigest() if p else None for p in (left, right)]
        pixels = None
        if left and right:
            with Image.open(left) as im:
                aa = np.asarray(im.convert('RGBA'))
            with Image.open(right) as im:
                bb = np.asarray(im.convert('RGBA'))
            if aa.shape == bb.shape:
                pixels = int(np.any(aa != bb, axis=-1).sum())
        numbers = [int(re.search(r'(\d+)\.png$', p.name)[1]) if p else None for p in (left, right)]
        rows.append({'index': index, 'source_indices': numbers, 'first_sha256': hashes[0], 'second_sha256': hashes[1],
                     'identical': hashes[0] is not None and hashes[0] == hashes[1] and numbers[0] == numbers[1],
                     'different_pixels': pixels})
    differing = sum(not row['identical'] for row in rows)
    result = _result('t4c_bake_identity', 'effect', differing, 0, '==', 'frames',
                     'Exact encoded PNG sha256; decoded pixel counts are diagnostic.',
                     (first, second), differing == 0)
    return {'result': result, 'frames': rows}


def scene_pixel_probe(blank_frames, prefix='fx'):
    """Negative-control bake with the effect omitted: every pixel must be clear.

    This detects scene leakage without falsely classifying opaque effect pixels.
    A blank effect-only render alone cannot establish nonempty-effect capture.
    """
    counts = []
    for path in numbered_frames(blank_frames, prefix):
        with Image.open(path) as im:
            if im.mode != 'RGBA':
                raise ValueError('Scene exclusion requires RGBA output')
            counts.append(int(np.count_nonzero(np.asarray(im)[..., 3])))
    return _result('t4c_scene_pixels', 'blank_control', max(counts), 0, '==', 'pixels',
                   'Maximum nonzero-alpha pixel count with effect disabled.', (blank_frames,), max(counts) == 0)


def compare_vo1(live, baked, tolerance=0.05, committed=True):
    """Compare frozen VO1 measurements by background and frame (relative ±5%).

    Inputs map each of ground/black/white/foliage to equal nonempty sequences.
    Zero reference requires exact zero; null/nonfinite values are UNEVALUABLE.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('Invalid VO1 tolerance')
    expected = {'ground', 'black', 'white', 'foliage'}
    if set(live) != expected or set(baked) != expected:
        raise ValueError('Need ground, black, white and foliage measurements')
    if len({len(live[key]) for key in expected}) != 1:
        raise ValueError('All backgrounds must cover the same frames')
    rows = []
    for background in sorted(expected):
        a, b = live[background], baked[background]
        if not a or len(a) != len(b):
            raise ValueError('VO1 frame counts must agree and be nonempty')
        for index, (x, y) in enumerate(zip(a, b)):
            valid = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v >= 0 for v in (x, y))
            error = None if not valid else (abs(y - x) / abs(x) if x else (0.0 if y == 0 else None))
            within = valid and ((y == 0) if x == 0 else error <= tolerance + 1e-12)
            rows.append(_result('t4c_vo1', f'{background}/{index}', error, tolerance, '<=',
                                'relative_difference',
                                'Frozen VO1 measurements supplied by caller; zero baseline requires exact zero.' if valid else 'Missing/nonfinite VO1 measurement.',
                                passed=bool(within) if valid and committed else None))
    return rows


def diagnose(project):
    """Static source inventory, hypotheses only; never a determinism verdict."""
    project = Path(project)
    findings = []
    patterns = {'cpu_particles': r'type="CPUParticles2D"',
                'gpu_particles': r'type="GPUParticles2D"',
                'wall_clock': r'Time\.get_ticks|\bTIME\b',
                'randomize': r'\brandomize\s*\(',
                'random_calls': r'\brand[fi](?:_range)?\s*\(',
                'idle_timing': r'create_tween\(|create_timer\('}
    for path in sorted(project.rglob('*')):
        if path.suffix not in ('.gd', '.gdshader', '.tscn') or '.godot' in path.parts:
            continue
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            for kind, pattern in patterns.items():
                if re.search(pattern, line):
                    findings.append({'kind': kind, 'path': path.relative_to(project).as_posix(),
                                     'line': line_number, 'source': line.strip()})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--effect', default='res://scenes/vfx_frozen_orb_impact.tscn')
    parser.add_argument('--frame', type=int)
    parser.add_argument('--frames', type=int, default=126)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--crop', type=int, nargs=2, default=(512, 512))
    parser.add_argument('--origin', type=float, nargs=2, default=(2285.62, 2407.32))
    parser.add_argument('--bake', action='store_true')
    parser.add_argument('--blank', action='store_true')
    parser.add_argument('--godot', default=GODOT)
    args = parser.parse_args()
    project = prepare_project(args.source, args.project, args.crop)
    print(json.dumps(run_replay(project, args.out, args.effect, args.frame, args.frames,
                                args.seed, args.crop, args.origin, args.bake, args.blank,
                                args.godot), indent=2))


if __name__ == '__main__':
    main()
