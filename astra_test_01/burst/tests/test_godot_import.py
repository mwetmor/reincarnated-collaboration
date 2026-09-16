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


class PieceBurstImportTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True,exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t4h-godot-',dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cells = self.root/'cells';self.cells.mkdir()
        for kind in ('idle','cast'):
            Image.new('RGBA',(512,512)).save(self.cells/f'{kind}_E_0.png')
        source = self.root/'source';source.mkdir()
        image = Image.new('RGBA',(16,16),(170,170,170,255))
        image.save(source/'piece.png');image.save(source/'peak_index.png')
        (source/'pieces.json').write_text(json.dumps({'schema_version':2,'canvas':[16,16],
            'centre':[7.5,7.5],'peak_index':'peak_index.png','pieces':[{'id':1,'mask':'piece.png',
            'pivot':[7.5,7.5],'radial_angle_deg':0,'radial_distance_px':0,'dominant_band':2,'area_px':256}]}))
        definition = {'name':'pieces_fixture','element':'fire','ground_squash':.6,
            'material':{'palette':[[.25,.08,.04,1],[.7,.16,.08,1],[1,.55,.12,1],[1,.94,.75,1]]},
            'phases':{kind:{'sheet':'piece.png','frames':[{'file':'piece.png','hold_frames':2}]} for kind in ('cast','travel','impact')},
            'layers':{'dark_duplicate':True},'pieces':{'source':'pieces.json','template':'burst_v1','seed':2026}}
        (source/'effect.json').write_text(json.dumps(definition))
        from export.effect_kit import build
        build(source/'effect.json',self.root/'kit')
        self.catalogue = self.root/'kits.json'
        self.catalogue.write_text(json.dumps({'kits':[{'name':'pieces_fixture','dir':str(self.root/'kit')}]}))
        self.sockets = self.root/'sockets.json'
        self.sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_E':{'sockets':[[256,256]],'release_index':0}}}))
        self.project = self.root/'project'
        build_project(self.cells,self.project,vfx_kits=self.catalogue,sockets=self.sockets)

    def test_piece_nodes_clock_residue_path_and_g1_routing(self):
        scene = (self.project/'scenes/vfx/piece_burst.tscn').read_text()
        script = (self.project/'scripts/vfx/piece_burst.gd').read_text()
        self.assertIn('name="Piece_001" type="Sprite2D"',scene)
        self.assertIn('texture_filter = 2',scene)
        self.assertIn('Engine.get_physics_frames() - release_tick',script)
        self.assertIn('func set_effect_age(age: int)',script)
        self.assertIn('residue_erode',script)
        self.assertIn('Freeze scale BEFORE erosion',script)
        self.assertIn('int(item.area_px) >= 48',script)
        self.assertIn('vfx_pieces_fixture_impact.tscn',(self.project/'scripts/keeper.gd').read_text())
        self.assertEqual(scene,(self.project/'scenes/vfx_pieces_fixture_impact.tscn').read_text().replace('texture_filter = 2\ntexture_filter = 2','texture_filter = 2'))
        validate_resources(self.project,True)

    def test_grey_substitution_preserves_index_masks_for_identical_erosion(self):
        from export.godot_import import _grey_vfx
        mask = self.project/'vfx/pieces_fixture/pieces/piece.png'
        before = mask.read_bytes();_grey_vfx(self.project)
        self.assertEqual(mask.read_bytes(),before)
        self.assertIn('grey_bodies = true',(self.project/'scenes/vfx/piece_burst.tscn').read_text())
        self.assertIn('palette_', (self.project/'scripts/vfx/piece_burst.gd').read_text())

    @unittest.skipUnless(Path(GODOT).is_file(),'Godot unavailable')
    def test_headless_import_and_seeded_clock_runtime(self):
        settings = self.project/'project.godot'
        settings.write_text(settings.read_text().replace('[application]\n',
            '[application]\nconfig/use_custom_user_dir=true\nconfig/custom_user_dir="'+str(self.root/'user')+'"\n'))
        (self.project/'piece_probe.gd').write_text(PIECE_CLOCK_PROBE)
        for arguments in (['--import'],['--script','res://piece_probe.gd']):
            proc = subprocess.run([GODOT,'--headless','--path',str(self.project),'--log-file',str(self.root/'engine.log'),*arguments],capture_output=True,text=True,timeout=110)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode,0,log)
            self.assertNotIn('SCRIPT ERROR',log)
            self.assertNotIn('Parse Error',log)
        self.assertIn('T4H_CLOCK_COMPLETE',log)


PIECE_CLOCK_PROBE = '''extends SceneTree
func _initialize() -> void:
    call_deferred("probe")
func need(value: bool, message: String) -> void:
    if not value:
        push_error(message)
        quit(7)
func probe() -> void:
    var a: Node2D = load("res://scenes/vfx/piece_burst.tscn").instantiate()
    var b: Node2D = load("res://scenes/vfx/piece_burst.tscn").instantiate()
    root.add_child(a)
    root.add_child(b)
    a.set_physics_process(false)
    b.set_physics_process(false)
    need(a.piece_motion(2026,1) == b.piece_motion(2026,1), "seed equal samples differ")
    var residue_scale: Vector2 = Vector2.ZERO
    for age in range(72):
        a.set_effect_age(age)
        b.set_effect_age(age)
        var left: Sprite2D = a.get_node("Art/Pieces/Piece_001")
        var right: Sprite2D = b.get_node("Art/Pieces/Piece_001")
        need(left.transform == right.transform,"seed equal transforms differ")
        need(left.scale.x >= 0.85 and left.scale.x <= 1.15,"piece scale outside limits")
        need(absf(left.rotation_degrees) <= 30.001,"rotation outside limits")
        if age == 15:
            residue_scale = left.scale
        if age >= 15:
            need(left.scale == residue_scale,"scale changed during erosion/residue")
        if age >= 36:
            need(left.material.get_shader_parameter("erode") > 0,"residue lacks erosion")
            need(left.material.get_shader_parameter("dissolve") == 0.5,"brightest band not removed")
    a.set_effect_age(72)
    need(not a.visible,"effect did not release to zero")
    b.queue_free()
    await process_frame
    print("T4H_CLOCK_COMPLETE")
    quit(0)
'''


class PieceStretchImportTests(unittest.TestCase):
    def setUp(self):
        fixture = PieceBurstImportTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.root = fixture.root
        self.project = self.root/'project_v2'
        kit_path = self.root/'kit/kit.json'
        data = json.loads(kit_path.read_text())
        data['pieces']['template'] = 'burst_v2'
        data['phase_scale'] = {'impact':1.0}
        kit_path.write_text(json.dumps(data))
        build_project(fixture.cells,self.project,vfx_kits=fixture.catalogue,sockets=fixture.sockets)

    def test_axes_whole_field_root_residue_clock_and_grey(self):
        from export.godot_import import _grey_vfx
        scene = (self.project/'scenes/vfx/piece_burst_v2.tscn').read_text()
        script = (self.project/'scripts/vfx/piece_burst_v2.gd').read_text()
        self.assertIn('name="Axis_001" type="Node2D"',scene)
        self.assertIn('name="Stretch" type="Sprite2D"',scene)
        self.assertIn('name="Piece_001" type="Sprite2D"',scene)
        self.assertIn('name="Root_001" type="Sprite2D"',scene)
        self.assertIn('func set_effect_age(age: int)',script)
        self.assertIn('residue_erode',script)
        self.assertIn('outer_distance',script)
        self.assertIn('node.scale = Vector2(lerpf',script)
        self.assertNotIn('axis.position =',script)
        material = (self.project/'vfx/pieces_fixture/materials/Piece_Piece_001.tres').read_text()
        self.assertIn('whole_body_distance.png',material)
        mask = self.project/'vfx/pieces_fixture/pieces/piece.png'
        before = mask.read_bytes()
        _grey_vfx(self.project)
        self.assertEqual(mask.read_bytes(),before)
        self.assertIn('grey_bodies = true',(self.project/'scenes/vfx/piece_burst_v2.tscn').read_text())
        validate_resources(self.project,True)

    def test_native_768_crop_backward_compatible_default(self):
        from export.replay import _crop, install_hooks
        self.assertEqual(_crop((512,512)),(512,512))
        self.assertEqual(_crop((768,768)),(768,768))
        with self.assertRaises(ValueError): _crop((769,768))
        install_hooks(self.project,(768,768))
        self.assertIn('viewport_width=768',(self.project/'project.godot').read_text())

    @unittest.skipUnless(Path(GODOT).is_file(),'Godot unavailable')
    def test_v2_headless_import_and_seed_equal_rooted_clock(self):
        settings = self.project/'project.godot'
        settings.write_text(settings.read_text().replace('[application]\n',
            '[application]\nconfig/use_custom_user_dir=true\nconfig/custom_user_dir="'+str(self.root/'user')+'"\n'))
        (self.project/'stretch_probe.gd').write_text(STRETCH_CLOCK_PROBE)
        for arguments in (['--import'],['--script','res://stretch_probe.gd']):
            proc = subprocess.run([GODOT,'--headless','--path',str(self.project),'--log-file',str(self.root/'engine.log'),*arguments],capture_output=True,text=True,timeout=110)
            log = proc.stdout+proc.stderr
            self.assertEqual(proc.returncode,0,log)
            self.assertNotIn('SCRIPT ERROR',log)
            self.assertNotIn('Parse Error',log)
        self.assertIn('T4H_V2_CLOCK_COMPLETE',log)


STRETCH_CLOCK_PROBE = '''extends SceneTree
func _initialize() -> void:
    call_deferred("probe")
func need(value: bool, message: String) -> void:
    if not value:
        push_error(message)
        quit(7)
func probe() -> void:
    var a: Node2D = load("res://scenes/vfx/piece_burst_v2.tscn").instantiate()
    var b: Node2D = load("res://scenes/vfx/piece_burst_v2.tscn").instantiate()
    root.add_child(a)
    root.add_child(b)
    a.set_physics_process(false)
    b.set_physics_process(false)
    var flight: int = int(a.config.flash_frames) + int(a.config.hold_frames)
    var residue: int = flight + 36
    var end: int = residue + int(a.config.residue_frames)
    var fixed: Array = []
    for item in a.pieces:
        fixed.append(item.axis.position)
    for age in range(end):
        a.set_effect_age(age)
        b.set_effect_age(age)
        need(a.trace[-1] == b.trace[-1],"seed equal clock states differ")
        for i in range(a.pieces.size()):
            var data: Dictionary = a.pieces[i]
            need(data.axis.position == fixed[i],"root translated")
            need(data.root.scale == Vector2.ONE,"residue reached by scaling")
            need(absf(a.trace[-1].pieces[i].rotation_deg) <= 10.001,"rotation exceeds ten degrees")
            if age >= flight + 15:
                var expected: Vector2 = Vector2.ONE * 1.25 if data.record.core else Vector2(float(data.record.along),0.7)
                need(data.node.scale.is_equal_approx(expected),"final stretch incorrect or shrank during erosion")
            if age >= residue:
                need(not data.axis.visible,"expanded art survived into stationary residue")
                need(data.root.material.get_shader_parameter("erode") > 0,"residue lacks root-first erosion")
                need(data.root.material.get_shader_parameter("dissolve") == 0.5,"band three not dissolved")
    a.set_effect_age(end)
    need(not a.visible,"effect did not release")
    b.queue_free()
    await process_frame
    print("T4H_V2_CLOCK_COMPLETE")
    quit(0)
'''


if __name__ == '__main__':
    unittest.main()
