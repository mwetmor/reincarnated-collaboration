"""Godot 4.6 native-crop, fixed-seed replay and Movie Maker instruments.

No particle substitution, dropped layers, frame repair or background removal.
Unsupported seed controls and engine/render failures are reported as evidence.
The acceptance VO1 instrument consumes externally measured VO1 values: it does
not invent a replacement definition for the frozen oracle.
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
var flip_sprite: Sprite2D
var flip_paths: Array = []
var flip_textures: Array[ImageTexture] = []

func _initialize() -> void:
    config = JSON.parse_string(FileAccess.get_file_as_string("res://replay_config.json"))
    Engine.physics_ticks_per_second = 60
    Engine.time_scale = 1.0
    seed(int(config.seed))
    root.size = Vector2i(int(config.crop[0]), int(config.crop[1]))
    root.content_scale_size = root.size
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
            background_image = Image.create(root.size.x, root.size.y, false, Image.FORMAT_RGBA8)
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
    flip_paths = config.get("flipbook", [])
    if not flip_paths.is_empty():
        # Retain feedback on the world, including victim tint and camera shake.
        # The flipbook is screen-space: its recorded shake is not applied twice.
        if is_instance_valid(effect):
            effect.hide()
        # Upload once, before frame_pre_draw. Retain strong references for the
        # entire run: replacing/freeing an ImageTexture during frame_pre_draw
        # can leave the renderer drawing its white fallback texture.
        for path in flip_paths:
            var image := Image.new()
            var error := image.load(str(path))
            if error != OK or image.is_empty() or image.get_size() != root.size or image.get_format() != Image.FORMAT_RGBA8:
                report.flipbook_error = {"path": str(path), "load_error": error}
                push_error("Invalid flipbook RGBA image: " + str(path))
                _finish()
                return
            flip_textures.append(ImageTexture.create_from_image(image))
        report.flipbook_loaded = flip_textures.size()
        var overlay := CanvasLayer.new()
        overlay.layer = 100
        root.add_child(overlay)
        flip_sprite = Sprite2D.new()
        # Native bake pivot is the crop centre, at the effect origin. The
        # screen-space crop already records camera shake; do not shake twice.
        flip_sprite.centered = true
        flip_sprite.position = Vector2(root.size) * 0.5
        flip_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
        overlay.add_child(flip_sprite)
        _set_flip_frame()
        RenderingServer.frame_pre_draw.connect(_set_flip_frame)
    if bool(config.get("probe_only", false)):
        process_frame.connect(func(): call_deferred("_capture"))
    else:
        RenderingServer.frame_post_draw.connect(_capture)
    started = true

func _set_flip_frame() -> void:
    if not flip_textures.is_empty():
        flip_sprite.texture = flip_textures[mini(captures, flip_textures.size() - 1)]

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

func _capture() -> void:
    if not started:
        return
    var age: int = Engine.get_physics_frames() - release_tick
    var visible_scene: Array = []
    for path in report.hidden:
        var node: Node = root.get_node_or_null(path)
        if node is CanvasItem and node.is_visible_in_tree():
            visible_scene.append(path)
    var floor_live: bool = is_instance_valid(effect) and effect.has_node("FloorLight") and effect.get_node("FloorLight").is_visible_in_tree()
    report.frames.append({"movie_index": captures, "physics_frame": age, "time_scale": Engine.time_scale, "camera_offset": [camera.offset.x, camera.offset.y], "visible_scene_drawables": visible_scene, "floor_light_live": floor_live})
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
    settings.write_text(text)
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
               flipbook=None, probe_only=False):
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
    flip_paths = numbered_frames(flipbook) if flipbook is not None else []
    if flip_paths:
        if bake or len(flip_paths) != frames:
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
              'bake': bake, 'blank': blank, 'report': str(out / 'probe.json'),
              'capture': str(out / 'capture.png'), 'background': background,
              'background_path': str(Path(background_path).resolve()) if background_path else None,
              'flipbook': [str(p.resolve()) for p in flip_paths], 'probe_only': probe_only}
    (project / 'replay_config.json').write_text(json.dumps(config, indent=2))
    # The probe owns visibility, including the live comparison configuration.
    settings = re.sub(r'(?m)^ReplayVisibility=.*\n', '', settings)
    (project / 'project.godot').write_text(settings)
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
    (out / 'run.json').write_text(json.dumps(result, indent=2) + '\n')
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
