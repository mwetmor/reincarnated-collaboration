"""T3f engine export contracts, known-bad assets and headless behavior."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from PIL import Image
from export.godot_import import (DIRECTIONS, FPS, build_project, discover_cells,
                                 validate_resources)

GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'
TMP = Path(__file__).resolve().parent/'tmp'


class GodotImportTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t3f-godot-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cells = self.root/'cells'
        self.cells.mkdir()

    def cell(self, anim='idle', direction='E', count=1, root=None):
        folder = (root or self.cells)/anim/direction
        folder.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            Image.new('RGBA', (512, 512), (30+i, 50, 70, 255)).save(folder/f'{anim}_{direction}_{i:02d}.png')
        return folder

    def test_all_fps_loops_resources_pivot_and_original_bytes(self):
        for anim in FPS:
            self.cell(anim, count=2)
        (self.cells/'registration.json').write_text('{"fps_out": 60, "fps": 24}')
        out = self.root/'project'
        report = build_project(self.cells, out)
        self.assertEqual(report['frames'], 10)
        self.assertEqual(len(validate_resources(out)), 10)
        resource = (out/'frames/keeper.tres').read_text()
        for anim, fps in FPS.items():
            self.assertIn(f'"name": &"{anim}_E", "speed": {float(fps)}', resource)
            self.assertRegex(resource, r'"loop": '+str(anim not in ('jump', 'cast')).lower()+
                             r', "name": &"'+anim+'_E"')
            for source in (self.cells/anim/'E').glob('*.png'):
                self.assertEqual(source.read_bytes(), (out/'sprites'/anim/'E'/source.name).read_bytes())
        scene = (out/'scenes/main.tscn').read_text()
        self.assertIn('offset = Vector2(-256, -400)', scene)
        self.assertIn('centered = false', scene)
        self.assertIn('default_texture_filter=2', (out/'project.godot').read_text())

    def test_missing_texture_and_undeclared_resource_rejected(self):
        self.cell()
        out = self.root/'project'
        build_project(self.cells, out)
        texture = out/'sprites/idle/E/idle_E_00.png'
        texture.unlink()
        with self.assertRaises(ValueError):
            validate_resources(out)
        Image.new('RGBA', (512, 512)).save(texture)
        resource = out/'frames/keeper.tres'
        resource.write_text(resource.read_text().replace('ExtResource("1")', 'ExtResource("99")'))
        with self.assertRaises(ValueError):
            validate_resources(out)

    def test_gap_duplicate_malformed_and_wrong_canvas_rejected(self):
        folder = self.cell(count=3)
        (folder/'idle_E_01.png').unlink()
        with self.assertRaises(ValueError):
            discover_cells(self.cells)
        (folder/'idle_E_02.png').rename(folder/'idle_E_01.png')
        duplicate = self.cells/'duplicate'
        duplicate.mkdir()
        (duplicate/'idle_E_00.png').write_bytes((folder/'idle_E_00.png').read_bytes())
        with self.assertRaises(ValueError):
            discover_cells(self.cells)
        (duplicate/'idle_E_00.png').unlink()
        (folder/'idle_E_01.png').rename(folder/'idle_BAD_01.png')
        with self.assertRaises(ValueError):
            discover_cells(self.cells)
        (folder/'idle_BAD_01.png').unlink()
        Image.new('RGBA', (511, 512)).save(folder/'idle_E_00.png')
        with self.assertRaises(ValueError):
            discover_cells(self.cells)
        Image.new('RGB', (512, 512)).save(folder/'idle_E_00.png')
        with self.assertRaises(ValueError):
            discover_cells(self.cells)

    def test_empty_overlapping_nonempty_and_escaping_inputs_rejected(self):
        with self.assertRaises(ValueError):
            build_project(self.cells, self.root/'project')
        folder = self.cell()
        with self.assertRaises(ValueError):
            build_project(self.cells, self.cells/'project')
        out = self.root/'occupied';out.mkdir();(out/'keep.txt').write_text('keep')
        with self.assertRaises(ValueError):
            build_project(self.cells, out)
        self.assertEqual((out/'keep.txt').read_text(), 'keep')
        outside = self.root/'outside.png'
        (folder/'idle_E_00.png').rename(outside)
        (folder/'idle_E_00.png').symlink_to(outside)
        with self.assertRaises(ValueError):
            discover_cells(self.cells)

    def test_numeric_order_and_native_fps_ignored(self):
        folder = self.cell(count=12)
        for path in list(folder.glob('*.png')):
            path.rename(folder/f'idle_E_{int(path.stem.rsplit("_",1)[1])}.png')
        (self.cells/'registration.json').write_text('{"fps":24}')
        entry = discover_cells(self.cells)['idle_E']
        self.assertEqual(entry['fps'], 8)
        self.assertEqual([int(p.stem.rsplit('_',1)[1]) for p in entry['frames']], list(range(12)))
        for bad in (0, -1, True, '12', float('nan')):
            with self.subTest(fps=bad):
                (self.cells/'registration.json').write_text(json.dumps({'fps_out': bad}))
                with self.assertRaises(ValueError):
                    discover_cells(self.cells)

    def test_cut_diagnostic_sheets_and_rest_are_not_cells(self):
        self.cell('walk', count=2)
        sheets = self.cells/'sheets';sheets.mkdir()
        Image.new('RGBA', (1024, 512)).save(sheets/'walk_E_strip.png')
        rest = self.cells/'frames/rest/E';rest.mkdir(parents=True)
        Image.new('RGBA', (512, 512)).save(rest/'rest_E.png')
        self.assertEqual(list(discover_cells(self.cells)), ['walk_E'])

    def test_gear_vfx_and_bad_vfx(self):
        self.cell()
        gear = self.root/'gear';self.cell('cast', 'N', 2, gear)
        vfx = self.root/'effects';vfx.mkdir()
        for name in ('cast', 'travel', 'impact'):
            Image.new('RGBA', (64, 64)).save(vfx/f'{name}_00.png')
        out = self.root/'project'
        report = build_project(self.cells, out, vfx=vfx, gear_variant=gear)
        self.assertEqual(report['gear_cells'], 1)
        self.assertEqual(report['vfx_animations'], 3)
        self.assertEqual(len(validate_resources(out)), 6)
        self.assertTrue((out/'frames/keeper_advanced.tres').is_file())
        self.assertTrue((out/'vfx/frost_bolt.tres').is_file())
        (vfx/'cast_00.png').rename(vfx/'cast_02.png')
        with self.assertRaises(ValueError):
            build_project(self.cells, self.root/'bad', vfx=vfx)

    @unittest.skipUnless(Path(GODOT).is_file(), 'Godot 4.6 binary unavailable')
    def test_headless_state_machine_input_map_gear_vfx_and_nearest_fallback(self):
        for anim in FPS:
            for direction in DIRECTIONS:
                self.cell(anim, direction)
        gear = self.root/'gear';self.cell('idle', 'E', root=gear)
        self.cell('walk', 'E', root=gear)
        vfx = self.root/'effects';vfx.mkdir()
        Image.new('RGBA', (32, 32)).save(vfx/'cast_00.png')
        out = self.root/'project'
        build_project(self.cells, out, vfx=vfx, gear_variant=gear)
        (out/'probe.gd').write_text(PROBE)
        engine_errors = []
        for args in (['--import'], ['--script', 'res://probe.gd']):
            proc = subprocess.run([GODOT, '--headless', '--path', str(out), *args],
                                  capture_output=True, text=True, timeout=90)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode, 0, log)
            self.assertNotIn('SCRIPT ERROR', log)
            self.assertNotIn('T3F_ASSERTION:', log)
            engine_errors.extend(line for line in log.splitlines() if 'ERROR' in line)
        self.assertIn('T3F_RUNTIME_ASSERTIONS=complete', log)
        self.assertEqual(engine_errors, [], '\n'.join(engine_errors))


PROBE = '''extends SceneTree

func check(value: bool, message: String) -> void:
    if not value:
        printerr("T3F_ASSERTION: ", message)
        quit(7)

func _initialize() -> void:
    call_deferred("probe")

func probe() -> void:
    var scene = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    var expected = {"move_left": [KEY_LEFT, KEY_A], "move_right": [KEY_RIGHT, KEY_D],
        "move_up": [KEY_UP, KEY_W], "move_down": [KEY_DOWN, KEY_S], "jump": [KEY_SPACE],
        "cast": [KEY_E], "gear_toggle": [KEY_G], "run_modifier": [KEY_SHIFT]}
    for action in expected:
        var keys: Array = []
        for event in InputMap.action_get_events(action):
            if event is InputEventKey:
                keys.append(event.physical_keycode)
        check(keys == expected[action], "input map " + action)
    check(InputMap.action_get_events("cast")[1].button_index == MOUSE_BUTTON_LEFT, "cast mouse")
    check(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter") == 2, "linear filter")
    var vectors = [Vector2.DOWN, Vector2(-1,1), Vector2.LEFT, Vector2(-1,-1),
        Vector2.UP, Vector2(1,-1), Vector2.RIGHT, Vector2(1,1)]
    var directions = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
    for i in range(8):
        for action in ["move_left", "move_right", "move_up", "move_down"]:
            Input.action_release(action)
        var v = vectors[i]
        if v.x < 0: Input.action_press("move_left")
        if v.x > 0: Input.action_press("move_right")
        if v.y < 0: Input.action_press("move_up")
        if v.y > 0: Input.action_press("move_down")
        keeper._physics_process(0.016)
        check(keeper.facing == directions[i], "facing " + directions[i])
        check(keeper.state == "walk", "walk state")
        check(keeper.sprite.animation == "walk_" + directions[i], "walk selection")
        check(not keeper.sprite.flip_h, "no mirroring")
    Input.action_press("run_modifier")
    keeper._physics_process(0.016)
    check(keeper.state == "run", "run with Shift")
    check(is_equal_approx(keeper.velocity.length(), keeper.run_speed), "run speed")
    for action in ["move_left", "move_right", "move_up", "move_down", "run_modifier"]:
        Input.action_release(action)
    keeper._physics_process(0.016)
    check(keeper.state == "idle", "movement returns idle")
    for action in ["jump", "cast"]:
        await process_frame
        Input.action_press(action)
        keeper._physics_process(0.016)
        Input.action_release(action)
        check(keeper.state == action, "action entered: " + action)
        check(not keeper.sprite.sprite_frames.get_animation_loop(keeper.sprite.animation), "action no-loop")
        if action == "cast":
            var effect = scene.get_child(scene.get_child_count()-1)
            check(effect is AnimatedSprite2D, "cast spawns VFX")
            check(effect.global_position == keeper.global_position + keeper.staff_tip_offset, "staff tip offset")
        await create_timer(0.3).timeout
        check(keeper.state == "idle", "animation_finished returns idle")
    await process_frame
    Input.action_press("gear_toggle")
    keeper._physics_process(0.016)
    Input.action_release("gear_toggle")
    check(keeper.sprite.sprite_frames == keeper.advanced_frames, "gear toggle")
    await process_frame
    keeper.facing = "N"
    keeper.state = "walk"
    keeper._play_state()
    check(keeper.sprite.animation == "walk_E", "nearest available fallback")
    var warnings: int = keeper.warned.size()
    keeper._play_state()
    check(keeper.warned.size() == warnings, "fallback prints once")
    keeper.state = "cast"
    keeper._play_state()
    check(keeper.fallback_remaining > 0.0, "missing action on looping set uses timer")
    keeper._physics_process(1.0)
    check(keeper.state == "idle", "missing cast does not stick")
    # Exact nearest angular direction, including wrap-around and deterministic tie.
    var sparse := SpriteFrames.new()
    sparse.remove_animation("default")
    sparse.add_animation("walk_NW")
    sparse.add_animation("walk_SE")
    keeper.sprite.sprite_frames = sparse
    keeper.facing = "N"
    check(keeper._nearest_animation("walk") == "walk_NW", "nearest north")
    keeper.facing = "S"
    check(keeper._nearest_animation("walk") == "walk_SE", "nearest across wrap")
    print("T3F_RUNTIME_ASSERTIONS=complete")
    scene.queue_free()
    await process_frame
    quit(0)
'''


if __name__ == '__main__':
    unittest.main()
