#!/usr/bin/env python3
"""Post-export patch: adds the `attack` state (Eye of Reckoning spin) to an
already-exported Godot project produced by astra_test_01/burst/export/godot_import.py.

WHY THIS EXISTS: the exporter (frozen, C-5-owned, shared with another in-flight
run) knows exactly five states via its module-level FPS = {idle, walk, run,
jump, cast}. Run C-8 produced an eighth-direction-complete SIXTH state,
`attack`, as 8 cells under runs/C-8/cells/attack_<DIR>/ that the exporter
does not know about and ignores. This script patches the *output* of an
export, not the exporter itself, so the frozen exporter is never touched.
Re-export overwrites the staging directory, so this patch is meant to be
re-run after every re-export of the same project.

Usage:
    python3 attack_patch.py <path to exported godot dir>
    e.g. python3 attack_patch.py runs/C-8/cliffside_v40-warlord2/godot

What it does:
  1. Reads the 8 attack_<DIR> cells from runs/C-8/cells/, validating frame
     count / contiguity / registration.json (n, fps_out) per direction.
  2. Copies their frames into <project>/sprites/attack/<DIR>/, matching the
     exact directory convention the exporter already uses for every other
     state (sprites/<anim>/<direction>/<anim>_<direction>_NN.png).
  3. Rewrites <project>/frames/keeper.tres (the SpriteFrames resource the
     other 5 states already live in) to add attack_<DIR> animations with
     per-direction fps read from registration.json and loop=true. Every
     OTHER animation already in that resource is preserved byte-faithfully
     (frame list, fps, loop) by parsing the existing resource rather than by
     re-deriving fps from any assumption -- this project's walk/run fps are
     already overridden by parallax movement-speed matching (20.7 / 14.5,
     not the exporter's base 12), so re-deriving from the FPS table would be
     silently wrong.
  4. Adds an `attack` input action to <project>/project.godot bound to the
     F key (physical_keycode 70), following the exact InputMap syntax
     already used for the other actions.
  5. Extends <project>/scripts/keeper.gd so that holding `attack` plays
     attack_<facing> looping in place, and releasing it returns to idle.

State-gating rule chosen (see PATCH NOTE comments in keeper.gd once applied):
  attack is gated exactly like jump/cast already are: a state check at the
  TOP of _physics_process consumes the whole frame and returns before any
  other input is read. Concretely:
    - While state is "jump" or "cast", their existing early-return fires
      first, so the new `Input.is_action_just_pressed("attack")` check
      (which lives further down, alongside the jump trigger) is never
      reached -- attack cannot interrupt an in-flight jump or cast.
    - While state is "attack", the new early-return fires before the
      existing cast/jump trigger checks are reached -- cast and jump cannot
      start while attacking.
    - Attack is exited by input RELEASE (checked every physics frame while
      state == "attack"), not by animation_finished, because the attack
      animation loops (animation_finished still fires once per loop for a
      looping AnimatedSprite2D, but is harmless here: _animation_finished()
      only acts when state is "jump" or "cast").
  This is the simplest rule consistent with the file's existing idiom (a
  single top-of-function busy-state gate) and needed no new state variable.

Idempotent: safe to run twice against the same project. Re-running recopies
the attack frames (overwrite, same bytes) and regenerates frames/keeper.tres
from (a) every animation currently in it MINUS any attack_* entries (treated
as ours to regenerate, never hand-authored) plus (b) freshly computed
attack_* entries -- so the output is byte-identical across repeated runs.
project.godot and keeper.gd patches are marker-guarded no-ops on a second run.

Fails loudly: every validation happens before anything is written. Any
inconsistency (missing cells, malformed registration.json, an unrecognized
keeper.gd/project.godot shape) raises and exits non-zero with no partial
write to the project.
"""
import json
import math
import re
import shutil
import sys
from pathlib import Path

DIRECTIONS = ('S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE')
SCRIPT_DIR = Path(__file__).resolve().parent
CELLS_ROOT = SCRIPT_DIR.parent / 'cells'  # runs/C-8/cells

ATTACK_KEY_PHYSICAL_KEYCODE = 70  # F key, per brief.

EXT_RESOURCE_RE = re.compile(
    r'\[ext_resource type="Texture2D" path="res://([^"]+)" id="(\d+)"\]')
ANIMATION_BLOCK_RE = re.compile(
    r'\{"frames": \[(?P<frames>.*?)\], "loop": (?P<loop>true|false), '
    r'"name": &"(?P<name>[^"]+)", "speed": (?P<speed>[0-9.]+)\}', re.DOTALL)
FRAME_ID_RE = re.compile(r'ExtResource\("(\d+)"\)')


def fail(msg):
    print('attack_patch: FAIL: ' + msg, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Step 1: read + validate the 8 attack cells from runs/C-8/cells/
# ---------------------------------------------------------------------------

def load_attack_cells():
    if not CELLS_ROOT.is_dir():
        fail(f'cells directory does not exist: {CELLS_ROOT}')
    cells = {}
    for d in DIRECTIONS:
        cell_dir = CELLS_ROOT / f'attack_{d}'
        frames_dir = cell_dir / 'frames' / 'attack' / d
        reg_path = cell_dir / 'registration.json'
        if not frames_dir.is_dir():
            fail(f'attack_{d}: missing frames directory: {frames_dir}')
        if not reg_path.is_file():
            fail(f'attack_{d}: missing registration.json: {reg_path}')
        try:
            reg = json.loads(reg_path.read_text())
        except json.JSONDecodeError as exc:
            fail(f'attack_{d}: registration.json is not valid JSON: {exc}')
        n = reg.get('n')
        fps = reg.get('fps_out')
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
            fail(f'attack_{d}: registration.json missing a valid integer "n" (got {n!r})')
        if isinstance(fps, bool) or not isinstance(fps, (int, float)) or not math.isfinite(fps) or fps <= 0:
            fail(f'attack_{d}: registration.json missing a valid positive "fps_out" (got {fps!r})')
        frame_re = re.compile(rf'attack_{re.escape(d)}_(\d+)\.png')
        found = {}
        for p in sorted(frames_dir.glob('*.png')):
            m = frame_re.fullmatch(p.name)
            if not m:
                fail(f'attack_{d}: unexpected file in frames dir (does not match '
                     f'attack_{d}_NN.png): {p}')
            found[int(m.group(1))] = p
        indices = sorted(found)
        if indices != list(range(n)):
            fail(f'attack_{d}: frame indices {indices} are not contiguous from 0 '
                 f'matching registration.json n={n}')
        loop_seconds = n / fps
        if abs(loop_seconds - 0.40) > 1e-6:
            fail(f'attack_{d}: n/fps_out = {n}/{fps} = {loop_seconds:.6f}s, expected '
                 f'exactly 0.40s (one whirlwind revolution) per the brief -- refusing '
                 f'to patch with a mismatched loop length')
        cells[d] = dict(n=n, fps=float(fps), frames=[found[i] for i in indices])
    return cells


# ---------------------------------------------------------------------------
# Step 2 + 3: copy frames, rewrite frames/keeper.tres
# ---------------------------------------------------------------------------

def parse_spriteframes(text):
    """Return {name: (paths, fps, loop)} for every animation currently in the resource."""
    ext = {}
    for m in EXT_RESOURCE_RE.finditer(text):
        ext[m.group(2)] = m.group(1)  # id -> res://-relative path
    if not ext:
        fail('frames/keeper.tres: found no ext_resource texture declarations -- '
             'unrecognized SpriteFrames resource shape')
    animations = {}
    for m in ANIMATION_BLOCK_RE.finditer(text):
        name = m.group('name')
        loop = m.group('loop') == 'true'
        speed = float(m.group('speed'))
        ids = FRAME_ID_RE.findall(m.group('frames'))
        if not ids:
            fail(f'frames/keeper.tres: animation "{name}" has no frames')
        try:
            paths = [ext[i] for i in ids]
        except KeyError as exc:
            fail(f'frames/keeper.tres: animation "{name}" references undeclared '
                 f'ext_resource id {exc}')
        animations[name] = (paths, speed, loop)
    if not animations:
        fail('frames/keeper.tres: found no animation blocks -- unrecognized '
             'SpriteFrames resource shape')
    return animations


def write_spriteframes(out_project, resource_relpath, animations):
    """Mirrors export.godot_import.write_spriteframes's exact on-disk format
    (duration 1.0 per frame; textures + animation blocks both iterate
    sorted(animations.items()), matching the exporter's own convention so a
    future real `attack` state in the exporter would produce the identical
    file shape)."""
    textures = []
    blocks = []
    for name, (paths, fps, loop) in sorted(animations.items()):
        frames = []
        for path in paths:
            ident = str(len(textures) + 1)
            textures.append(f'[ext_resource type="Texture2D" path="res://{path}" id="{ident}"]')
            frames.append('{"duration": 1.0, "texture": ExtResource("' + ident + '")}')
        blocks.append('{"frames": [' + ',\n'.join(frames) + '], "loop": ' + str(loop).lower() +
                       ', "name": &' + json.dumps(name) + ', "speed": ' + str(float(fps)) + '}')
    target = out_project / resource_relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        '[gd_resource type="SpriteFrames" load_steps=' + str(len(textures) + 1) +
        ' format=3]\n\n' + '\n'.join(textures) + '\n\n[resource]\nanimations = [' +
        ',\n'.join(blocks) + ']\n')


def patch_frames(project, cells):
    resource_path = project / 'frames' / 'keeper.tres'
    if not resource_path.is_file():
        fail(f'expected SpriteFrames resource not found: {resource_path}')
    existing = parse_spriteframes(resource_path.read_text())

    # Anything already named attack_* is ours to regenerate, never hand-authored
    # (second-run idempotency: don't double up on our own prior output).
    preserved = {name: v for name, v in existing.items() if not name.startswith('attack_')}
    for state in ('idle', 'walk', 'run', 'jump', 'cast'):
        if not any(name.startswith(state + '_') for name in preserved):
            fail(f'frames/keeper.tres: expected to find "{state}_*" animations '
                 f'(the exporter\'s known states) but found none -- refusing to patch '
                 f'an unrecognized project')

    # Copy the 8 attack cells' frames into the project's frame tree, same
    # layout convention as every other state: sprites/<anim>/<dir>/<anim>_<dir>_NN.png
    animations = dict(preserved)
    for d, cell in cells.items():
        dest_dir = project / 'sprites' / 'attack' / d
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True)
        rel_paths = []
        for src in cell['frames']:
            dest = dest_dir / src.name
            shutil.copyfile(src, dest)
            rel_paths.append(dest.relative_to(project).as_posix())
        animations[f'attack_{d}'] = (rel_paths, cell['fps'], True)  # loop = true

    write_spriteframes(project, Path('frames') / 'keeper.tres', animations)
    return sorted(name for name in animations if name.startswith('attack_'))


# ---------------------------------------------------------------------------
# Step 4: project.godot input action
# ---------------------------------------------------------------------------

ATTACK_INPUT_LINE = (
    'attack={"deadzone":0.2,"events":[Object(InputEventKey,"physical_keycode":' +
    str(ATTACK_KEY_PHYSICAL_KEYCODE) + ')]}')


def patch_project_godot(project):
    path = project / 'project.godot'
    if not path.is_file():
        fail(f'project.godot not found: {path}')
    text = path.read_text()
    if '\n[input]\n' not in text:
        fail('project.godot: no [input] section found -- unrecognized project shape')
    cast_line_re = re.compile(r'^cast=.*$', re.MULTILINE)
    if not cast_line_re.search(text):
        fail('project.godot: no existing "cast=" input action found to anchor the '
             'new "attack=" action next to -- unrecognized project shape')

    # Idempotent: drop any existing attack= line (ours from a prior run, or
    # anything else claiming that action name) before re-inserting canonically.
    attack_line_re = re.compile(r'^attack=.*\n', re.MULTILINE)
    text = attack_line_re.sub('', text)

    text = cast_line_re.sub(lambda m: m.group(0) + '\n' + ATTACK_INPUT_LINE, text, count=1)
    path.write_text(text)


# ---------------------------------------------------------------------------
# Step 5: keeper.gd controller
# ---------------------------------------------------------------------------

MARKER = '    # PATCH(drax attack_patch): attack state'

JUMP_CAST_GATE_ANCHOR = '''    if state == "jump" or state == "cast":
        velocity = Vector2.ZERO
        if fallback_remaining >= 0.0:
            fallback_remaining -= delta
            if fallback_remaining <= 0.0:
                _animation_finished()
        return
'''

ATTACK_HOLD_BLOCK = MARKER + '''
    if state == "attack":
        velocity = Vector2.ZERO
        if not Input.is_action_pressed("attack"):
            state = "idle"
            _play_state()
        return
'''

JUMP_TRIGGER_ANCHOR = '''    if Input.is_action_just_pressed("jump"):
        state = "jump"
        velocity = Vector2.ZERO
        _play_state()
        return
'''

ATTACK_TRIGGER_BLOCK = '''    if Input.is_action_just_pressed("attack"):
        state = "attack"
        velocity = Vector2.ZERO
        _play_state()
        return
'''

FALLBACK_KINDS_ANCHOR = 'for kind in ["walk", "run", "jump", "cast"]:'
FALLBACK_KINDS_PATCHED = 'for kind in ["walk", "run", "jump", "cast", "attack"]:'


def patch_keeper_gd(project):
    path = project / 'scripts' / 'keeper.gd'
    if not path.is_file():
        fail(f'keeper.gd not found: {path}')
    text = path.read_text()

    if MARKER in text:
        return False  # already patched; idempotent no-op

    if text.count(JUMP_CAST_GATE_ANCHOR) != 1:
        fail('keeper.gd: expected exactly one occurrence of the jump/cast busy-state '
             'gate in _physics_process -- unrecognized controller shape, refusing to '
             'guess where to insert the attack gate')
    text = text.replace(JUMP_CAST_GATE_ANCHOR, JUMP_CAST_GATE_ANCHOR + ATTACK_HOLD_BLOCK, 1)

    if text.count(JUMP_TRIGGER_ANCHOR) != 1:
        fail('keeper.gd: expected exactly one occurrence of the jump-trigger block -- '
             'unrecognized controller shape, refusing to guess where to insert the '
             'attack trigger')
    text = text.replace(JUMP_TRIGGER_ANCHOR, JUMP_TRIGGER_ANCHOR + ATTACK_TRIGGER_BLOCK, 1)

    if text.count(FALLBACK_KINDS_ANCHOR) != 1:
        fail('keeper.gd: expected exactly one occurrence of the _play_state fallback '
             'kind list -- unrecognized controller shape')
    text = text.replace(FALLBACK_KINDS_ANCHOR, FALLBACK_KINDS_PATCHED, 1)

    path.write_text(text)
    return True


# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        fail('usage: python3 attack_patch.py <path to exported godot dir>')
    project = Path(sys.argv[1]).resolve()
    if not project.is_dir():
        fail(f'not a directory: {project}')

    cells = load_attack_cells()
    print(f'attack_patch: loaded {len(cells)} attack cells from {CELLS_ROOT}')
    for d in DIRECTIONS:
        c = cells[d]
        print(f'  attack_{d}: n={c["n"]} fps={c["fps"]} loop={c["n"] / c["fps"]:.3f}s')

    added = patch_frames(project, cells)
    print(f'attack_patch: wrote {project / "frames" / "keeper.tres"} with animations: {added}')

    patch_project_godot(project)
    print(f'attack_patch: ensured "attack" input action (physical_keycode='
          f'{ATTACK_KEY_PHYSICAL_KEYCODE}, F key) in {project / "project.godot"}')

    patched = patch_keeper_gd(project)
    if patched:
        print(f'attack_patch: patched {project / "scripts" / "keeper.gd"} with attack state gating')
    else:
        print(f'attack_patch: {project / "scripts" / "keeper.gd"} already patched (idempotent no-op)')

    print('attack_patch: done.')


if __name__ == '__main__':
    main()
