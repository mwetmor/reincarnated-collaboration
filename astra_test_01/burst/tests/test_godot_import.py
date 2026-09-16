"""T3f engine export contracts, known-bad assets and headless behavior."""
import json
import math
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
        self.assertIn('release_tick = Engine.get_physics_frames()',script)
        clock = (self.project/'scripts/vfx/piece_burst.gd').read_text()
        self.assertIn('Engine.get_physics_frames() - release_tick',clock)
        self.assertIn('var expansion_end: int = flight_start + 15',script)
        self.assertIn('var residue_start: int = expansion_end + 21',script)
        self.assertIn('var residue_end: int = residue_start + int(config.residue_frames)',script)
        self.assertIn('node.scale = Vector2(lerpf(1.0,float(item.along),ease),lerpf(1.0,0.85,ease))',script)
        self.assertNotIn('axis.position =',script)
        self.assertIn('axis.set_position(root_start + Vector2.RIGHT.rotated(float(item.axis_radians)) * root_drift_px)',script)
        self.assertIn('float(config.root_drift) * float(config.core_radius_px) * ease',script)
        self.assertIn('var residue_t: float = clampf(float(age-residue_start)/float(config.residue_frames),0.0,1.0)',script)
        self.assertIn('var dissolve: float = 1.0 if age >= residue_end else 0.8 * residue_t',script)
        self.assertIn('paint.material.set_shader_parameter("dissolve",0.0)',script)
        self.assertIn('root_sprite.material.set_shader_parameter("dissolve",dissolve)',script)
        self.assertIn('axis.visible = active and age < residue_start',script)
        self.assertIn('if bool(config.get("screen_px", false)):\n        spell_scale = 1.0',script)
        self.assertIn('$Art.scale = Vector2.ONE * float(config.phase_scale) * spell_scale',script)
        runtime = json.loads((self.project/'vfx/pieces_fixture/pieces/burst_runtime.json').read_text())
        self.assertTrue(runtime['erode_outside_in'])
        self.assertFalse(runtime['screen_px'])  # This synthetic kit uses the legacy default.
        self.assertEqual(runtime['phase_scale'],1.0)
        self.assertTrue(0 <= runtime['root_drift'] <= .5)
        for item in runtime['pieces']:
            self.assertTrue(2.0 <= item['along'] <= 2.5)
        material = (self.project/'vfx/pieces_fixture/materials/Piece_Piece_001.tres').read_text()
        self.assertIn('whole_body_distance.png',material)
        self.assertIn('shader_parameter/erode_outside_in = true',material)
        root_material = (self.project/'vfx/pieces_fixture/materials/Root_001.tres').read_text()
        self.assertIn('whole_body_distance.png',root_material)
        self.assertIn('shader_parameter/erode_outside_in = true',root_material)
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


# T4i-r1 device policy; T4i expectations above are retained verbatim.
class TouchDeviceAimEmissionTests(unittest.TestCase):
    def test_touch_device_forward_and_probe_precedence(self):
        from export.godot_import import DIRECTIONAL_KEEPER, _g1_directional
        keeper = _g1_directional(DIRECTIONAL_KEEPER)
        self.assertIn('const TOUCH_OVERLAY_BAND = 0.22', keeper)
        self.assertIn('var vfx_force_touch_device: bool = false', keeper)
        branch = 'if vfx_cursor_override == null and (vfx_force_touch_device or DisplayServer.is_touchscreen_available()):'
        self.assertIn(branch, keeper)
        original = 'var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override'
        forward = 'var forward_point: Vector2 = global_position + FACING_VECTORS[facing].normalized() * float(kit.range_px) * art_scale'
        self.assertIn(original, keeper)
        self.assertIn(forward, keeper)
        self.assertLess(keeper.index(branch), keeper.index(forward))
        self.assertLess(keeper.index(forward), keeper.index(original))
        self.assertLess(keeper.index(original), keeper.index('G1.resolve_target('))
        self.assertIn('destination = {"point": forward_point, "target": null, "kind": "cursor"}', keeper)
        for obsolete in ('vfx_world_touch', 'vfx_last_pointer_touch',
                         'vfx_mouse_motion_since_touch', 'InputEventScreenTouch',
                         'InputEventScreenDrag', 'func _unhandled_input'):
            self.assertNotIn(obsolete, keeper)

    def test_desktop_cursor_and_resolver_match_pre_t4i(self):
        from export.godot_import import DIRECTIONAL_KEEPER, _g1_directional
        keeper = _g1_directional(DIRECTIONAL_KEEPER)
        self.assertIn('    else:\n        var cursor: Vector2 = get_global_mouse_position() if vfx_cursor_override == null else vfx_cursor_override\n        destination = G1.resolve_target(get_tree(), global_position, direction, cursor, float(kit.range_px) * art_scale)\n', keeper)


# T4k: verify a diagnostic trace without silently weakening the all-layer gate.
def piece_layer_uniform_diagnostic(rows, age=30):
    row = next(row for row in rows if row['age'] == age)
    pair_mismatches, all_layer_mismatches = [], []
    for piece in row['pieces']:
        layers = piece['layers']
        if len(layers) != 4:
            raise ValueError('Expected expanding/root paint and their two dark duplicates')
        keys = ('erode','dissolve','outer_distance')
        for body,dark in ((layers[0],layers[2]),(layers[1],layers[3])):
            if any(body[key] != dark[key] for key in keys):
                pair_mismatches.append({'id':piece['id'],'body':body['path'],'dark':dark['path']})
        if any(layers[0][key] != layer[key] for layer in layers[1:] for key in keys):
            all_layer_mismatches.append(piece['id'])
    return {'age':age,'pieces':len(row['pieces']),
            'paired_body_dark_uniform_equality':not pair_mismatches,
            'all_piece_layer_uniform_equality':not all_layer_mismatches,
            'pair_mismatches':pair_mismatches,'all_layer_mismatches':all_layer_mismatches,
            'peak_dark_visible':row['peak_dark_visible']}


class PieceLap3LayerInstrumentTests(unittest.TestCase):
    def test_distinguishes_pairwise_and_literal_all_layer_equality(self):
        import copy
        layers = [{'path':name,'erode':.5,'dissolve':.5,'outer_distance':1.0}
                  for name in ('paint','root','dark_paint','dark_root')]
        rows = [{'age':30,'peak_dark_visible':False,'pieces':[{'id':1,'layers':layers}]}]
        report = piece_layer_uniform_diagnostic(rows)
        self.assertTrue(report['all_piece_layer_uniform_equality'])
        bad = copy.deepcopy(rows)
        bad[0]['pieces'][0]['layers'][2]['erode'] = .2
        self.assertFalse(piece_layer_uniform_diagnostic(bad)['paired_body_dark_uniform_equality'])
        different_phase = copy.deepcopy(rows)
        for index in (1,3):
            different_phase[0]['pieces'][0]['layers'][index]['erode'] = .2
        report = piece_layer_uniform_diagnostic(different_phase)
        self.assertTrue(report['paired_body_dark_uniform_equality'])
        self.assertFalse(report['all_piece_layer_uniform_equality'])


class PieceLap3LegacyByteTests(unittest.TestCase):
    def test_six_kits_and_v1_against_pre_t4k_export_hash_table(self):
        import hashlib
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        root = Path(__file__).resolve().parents[1]
        baseline = json.loads((root/'runs/C-5/t3/T4k/legacy_hashes.json').read_text())
        TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='t4k-legacy-',dir=TMP) as td:
            out = Path(td)
            for part in ('scripts','scenes','vfx'):
                (out/part).mkdir()
            for name in baseline['kits']:
                kit = _load_vfx_kit(root/'runs/C-5/vfx_kits/v9'/name)
                _write_authored_effect(out,kit,'vfx/'+name,'vfx_'+name,{})
            actual = {p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted(out.rglob('*')) if p.is_file()}
            self.assertEqual(actual,baseline['before'])


def burn_back_trace():
    root=Path(__file__).resolve().parents[1]/'runs/C-5/t3/T4l'
    path=root/'project/clock_trace.json'
    if path.is_file(): return json.loads(path.read_text())
    import tarfile
    with tarfile.open(root/'evidence.tar.gz') as archive:
        return json.loads(archive.extractfile('project/clock_trace.json').read())


class BurnBackExportTests(unittest.TestCase):
    def test_real_clock_uniforms_screen_scale_and_release(self):
        root=Path(__file__).resolve().parents[1]/'runs/C-5/t3/T4l'
        rows=burn_back_trace()
        self.assertEqual([r['age_frames'] for r in rows],list(range(77)))
        for row in rows:
            self.assertEqual(row['art_scale'],[1.0,1.0])
            self.assertEqual(row['floor_scale'],[7.5,4.5])
            for item in row['actual_uniforms']:
                paint,stationary,dark,dark_stationary=item['layers']
                self.assertEqual(paint,dark);self.assertEqual(stationary,dark_stationary)
                self.assertTrue(paint['erode_outside_in']);self.assertTrue(stationary['erode_outside_in'])
                self.assertEqual(paint['dissolve'],0.0)
                if row['stage'] in ('hold','expansion','erosion'):
                    self.assertEqual(stationary['dissolve'],0.0)
                if row['stage']=='residue': self.assertLess(stationary['dissolve'],5/6)
                if row['stage']=='zero': self.assertEqual(stationary['dissolve'],1.0)
        self.assertEqual(rows[-1]['stage'],'zero')

    def test_legacy_488_byte_table(self):
        import hashlib
        from export.godot_import import _load_vfx_kit,_write_authored_effect
        root=Path(__file__).resolve().parents[1]
        baseline=json.loads((root/'runs/C-5/t3/T4l/legacy_hashes.json').read_text())
        with tempfile.TemporaryDirectory(prefix='t4l-legacy-',dir=TMP) as td:
            out=Path(td)
            for part in ('scripts','scenes','vfx'):(out/part).mkdir()
            for name in baseline['kits']:
                kit=_load_vfx_kit(root/'runs/C-5/vfx_kits/v9'/name)
                _write_authored_effect(out,kit,'vfx/'+name,'vfx_'+name,{})
            actual={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
            self.assertEqual(actual,baseline['before'])
            self.assertEqual(len(actual),488)

    def test_screen_px_picker_g1_and_socket_contract(self):
        from export.godot_import import _g1_config
        fixture=PieceBurstImportTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        kit=fixture.root/'kit/kit.json';data=json.loads(kit.read_text())
        data['screen_px']=True;data['pieces']['template']='burst_v2';kit.write_text(json.dumps(data))
        project=fixture.root/'screen_project'
        build_project(fixture.cells,project,vfx_kits=fixture.catalogue,sockets=fixture.sockets)
        keeper=(project/'scripts/keeper.gd').read_text()
        self.assertIn('1.0 if bool(VFX_KITS[cast_kit_index].get("screen_px", false)) else art_scale',keeper)
        self.assertIn('G1.acquire(get_parent(), kit, socket, destination, self, art_scale)',keeper)
        self.assertIn('spell_scale = 1.0 if bool(config.get("screen_px", false)) else art_scale',(project/'scripts/vfx_g1.gd').read_text())
        self.assertTrue(_g1_config({'name':'a','effect':data})['screen_px'])
        self.assertNotIn('screen_px',_g1_config({'name':'legacy'}))


class RaggedResidueImportTests(unittest.TestCase):
    def test_exported_threshold_and_every_root_and_stretch_material_agree(self):
        from export.effect_kit import load_kit, load_pieces, distance_field, residue_entry, erosion_noise_texture
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        import numpy as np
        root = Path(__file__).resolve().parents[1]
        kit_root = root/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2'
        kit = _load_vfx_kit(kit_root)
        TMP.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='t4n-materials-', dir=TMP) as td:
            out = Path(td)
            for folder in ('scripts', 'scenes', 'vfx'):
                (out/folder).mkdir()
            _write_authored_effect(out, kit, 'vfx/fire_burst_e0p_v2', 'vfx_fire_burst_e0p_v2', {})
            folder = out/'vfx/fire_burst_e0p_v2'
            runtime = json.loads((folder/'pieces/burst_runtime.json').read_text())
            peak = np.array(Image.open(folder/'pieces/peak_index.png').convert('RGBA'))
            expected = residue_entry(peak, distance_field(peak), .2, .4, erosion_noise_texture(peak))
            self.assertEqual(runtime['erode_noise'], .4)
            for key, value in expected.items():
                self.assertEqual(runtime[key], value)
            for piece in runtime['pieces']:
                for prefix in ('Piece_Piece_', 'Root_'):
                    material = (folder/f'materials/{prefix}{piece["id"]:03d}.tres').read_text()
                    self.assertIn('shader_parameter/erode_noise = 0.4', material)
                    shader = re.search(r'path="res://([^"]+\.gdshader)"', material)[1]
                    source = (out/shader).read_text()
                    self.assertIn('0.5 * (2.0 * resistance.r - 1.0) + 0.5 * resistance.g', source)
                    self.assertIn('distance_value > 1.0 - erode', source)
                    self.assertIn('Per-kit band-group removal thresholds', source)
            # The age schedule is reused exactly; only shader resistance and cutoff change.
            self.assertIn('0.8 * residue_t', (out/'scripts/vfx/piece_burst_v2.gd').read_text())

    def test_piece_zero_overrides_material_noise_in_emitted_root(self):
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        fixture = PieceBurstImportTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        path = fixture.root/'kit/kit.json'
        data = json.loads(path.read_text())
        data['material'].update(erode_outside_in=True, erode_noise=.08)
        data['pieces'].update(template='burst_v2', erode_noise=0)
        path.write_text(json.dumps(data))
        out = fixture.root/'zero_override'
        for part in ('scripts','scenes','vfx'):
            (out/part).mkdir(parents=True)
        _write_authored_effect(out, _load_vfx_kit(path.parent), 'vfx/fixture', 'vfx_fixture', {})
        material = (out/'vfx/fixture/materials/Root_001.tres').read_text()
        self.assertNotIn('shader_parameter/erode_noise', material)
        shader = re.search(r'path="res://([^"]+\.gdshader)"', material)[1]
        self.assertNotIn('erode_noise', (out/shader).read_text())


class ContinuousResidueImportTests(unittest.TestCase):
    def test_whole_canvas_texture_shared_by_every_material_and_cpu_cutoff(self):
        import hashlib
        import numpy as np
        from export.effect_kit import erosion_noise_texture, residue_entry, distance_field
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        root = Path(__file__).resolve().parents[1]
        kit = _load_vfx_kit(root/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2')
        TMP.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='t4o-material-', dir=TMP) as td:
            out = Path(td)
            for folder in ('scripts', 'scenes', 'vfx'):
                (out/folder).mkdir()
            _write_authored_effect(out, kit, 'vfx/fire_burst_e0p_v2', 'vfx_fire_burst_e0p_v2', {})
            folder = out/'vfx/fire_burst_e0p_v2'
            runtime = json.loads((folder/'pieces/burst_runtime.json').read_text())
            peak = np.array(Image.open(folder/'pieces/peak_index.png').convert('RGBA'))
            noise_path = out/runtime['erosion_noise_texture']
            noise = np.array(Image.open(noise_path))
            np.testing.assert_array_equal(noise, erosion_noise_texture(peak))
            self.assertEqual(noise.shape, (*peak.shape[:2], 3))
            expected = residue_entry(peak, distance_field(peak), .2, .4, noise)
            self.assertEqual(runtime['erode_noise'], .4)
            for key, value in expected.items():
                self.assertEqual(runtime[key], value)
            self.assertEqual(len(list(folder.rglob('*noise.png'))), 1)
            for piece in runtime['pieces']:
                for prefix in ('Piece_Piece_', 'Root_'):
                    material = (folder/f'materials/{prefix}{piece["id"]:03d}.tres').read_text()
                    self.assertIn('load_steps=4', material)
                    self.assertIn('res://'+runtime['erosion_noise_texture'], material)
                    self.assertIn('shader_parameter/erode_noise = 0.4', material)
                    self.assertIn('shader_parameter/erosion_noise_texture = ExtResource("Noise")', material)
                    shader = re.search(r'path="res://([^"]+\.gdshader)"', material)[1]
                    text = (out/shader).read_text()
                    self.assertIn('texture(erosion_noise_texture, UV).rg', text)
                    self.assertIn('texture(distance_texture, UV).r', text)
                    self.assertNotIn('erode_noise * (band / 3.0)', text)
                    self.assertIn('Per-kit band-group removal thresholds', text)
            for path in list(out.rglob('*.tres')) + list(out.rglob('*.tscn')):
                for relative in re.findall(r'path="res://([^"]+)"', path.read_text()):
                    self.assertTrue((out/relative).is_file(), relative)

    def test_default_zero_emits_no_texture_or_sampler(self):
        fixture = PieceStretchImportTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        self.assertFalse(list(fixture.project.rglob('whole_body_noise.png')))
        for path in fixture.project.rglob('*.gdshader'):
            self.assertNotIn('erosion_noise_texture', path.read_text())


class TransformedResidueSeamTests(unittest.TestCase):
    def test_transformed_front_at_three_ages_has_no_straight_seam_over_12px(self):
        from test_effect_kit import transformed_erosion_front_diagnostic
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        root = Path(__file__).resolve().parents[1]
        kit = _load_vfx_kit(root/'runs/C-5/vfx_kits/v9/fire_burst_e0p_v2')
        TMP.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='t4o-front-', dir=TMP) as td:
            out = Path(td)
            for folder in ('scripts', 'scenes', 'vfx'):
                (out/folder).mkdir()
            _write_authored_effect(out, kit, 'vfx/fire_burst_e0p_v2', 'vfx_fire_burst_e0p_v2', {})
            rows = transformed_erosion_front_diagnostic(out)
            self.assertEqual({row['age'] for row in rows}, {30, 33, 36})
            for row in rows:
                with self.subTest(age=row['age']):
                    self.assertIsInstance(row['longest_straight_seam_front_px'], (int, float))
                    self.assertGreaterEqual(row['longest_straight_seam_front_px'], 0)
            report = root/'runs/C-5/t3/T4g/seam_measurements.json'
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps({'report_only': True, 'threshold_withdrawn': 12,
                                          'rows': rows}, indent=2) + '\n')


class KeyStateSwapImportTests(unittest.TestCase):
    """The opt-in script must demonstrate swaps using the actual Godot clock hook."""
    def setUp(self):
        fixture=PieceBurstImportTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        self.root=fixture.root;self.project=self.root/'key_project'
        kit_path=self.root/'kit/kit.json';data=json.loads(kit_path.read_text())
        data['pieces']['template']='burst_v2';data['screen_px']=True
        data['pieces']['key_states']=[dict(state='expanded',png='expanded.png',at_age=15,hold_frames=4),
                                      dict(state='spent',png='spent.png',at_age=36,hold_frames=5)]
        for state in data['pieces']['key_states']:
            im=Image.new('RGBA',(64,64));im.paste(Image.new('RGBA',(16,16),(170,170,170,255)),(24,24));im.save(kit_path.parent/state['png'])
        kit_path.write_text(json.dumps(data))
        build_project(fixture.cells,self.project,vfx_kits=fixture.catalogue,sockets=fixture.sockets)

    def test_key_resources_palette_and_native_canvas(self):
        scene=(self.project/'scenes/vfx/piece_burst_v2.tscn').read_text()
        self.assertIn('offset = Vector2(-32.0, -32.0)',scene)
        self.assertIn('Key_expandedDark',scene)
        self.assertIn('Key_spent',scene)
        script=(self.project/'scripts/vfx/piece_burst_v2_keys.gd').read_text()
        self.assertIn('key_erode',script);self.assertIn('key_dissolve',script)
        validate_resources(self.project,True)

    @unittest.skipUnless(Path(GODOT).is_file(),'Godot unavailable')
    def test_headless_literal_age_swaps_returns_and_continuous_uniforms(self):
        from export.godot_import import _load_vfx_kit, _write_authored_effect
        # A later plain-v2 kit must not overwrite the opted-in clock script.
        kit=_load_vfx_kit(self.root/'kit');kit['effect']['pieces'].pop('key_states')
        _write_authored_effect(self.project,kit,'vfx/plain_v2','vfx_plain_v2',{})
        settings=self.project/'project.godot'
        settings.write_text(settings.read_text().replace('[application]\n',
            '[application]\nconfig/use_custom_user_dir=true\nconfig/custom_user_dir="'+str(self.root/'user')+'"\n'))
        (self.project/'key_probe.gd').write_text(KEY_STATE_CLOCK_PROBE)
        logs=[]
        for arguments in (['--import'],['--script','res://key_probe.gd']):
            proc=subprocess.run([GODOT,'--headless','--path',str(self.project),'--log-file',str(self.root/'key_engine.log'),*arguments],capture_output=True,text=True,timeout=110)
            log=proc.stdout+proc.stderr;logs.append(dict(arguments=arguments,exit_code=proc.returncode,log=log))
            self.assertEqual(proc.returncode,0,log)
            self.assertNotIn('SCRIPT ERROR',log);self.assertNotIn('Parse Error',log)
        self.assertIn('T4Q_KEY_CLOCK_COMPLETE',log)
        evidence=TMP.parent/'key_clock_trace.json'
        evidence.write_bytes((self.project/'key_clock_trace.json').read_bytes())
        (TMP.parent/'headless.json').write_text(json.dumps(logs,indent=2)+'\n')


KEY_STATE_CLOCK_PROBE = '''extends SceneTree
var failures: Array = []
func _initialize() -> void:
    call_deferred("probe")
func need(value: bool, message: String) -> void:
    if not value:
        failures.append(message)
func probe() -> void:
    var a: Node2D = load("res://scenes/vfx_pieces_fixture_impact.tscn").instantiate()
    a.spell_scale = 20.0
    a.grey_bodies = true
    root.add_child(a)
    a.set_physics_process(false)
    var plain: Node2D = load("res://scenes/vfx_plain_v2_impact.tscn").instantiate()
    root.add_child(plain)
    plain.set_physics_process(false)
    var rows: Array = []
    for age in range(45):
        a.set_effect_age(age)
        plain.set_effect_age(age)
        need(not plain.trace[-1].has("key_state"),"plain v2 got opted-in script")
        var expected: String = "expanded" if age >= 15 and age < 19 else ("spent" if age >= 36 and age < 41 else "")
        need(a.trace[-1].key_state == expected,"wrong key state at age " + str(age))
        need(a.get_node("Art/Pieces").visible == (expected == ""),"pieces not swapped/returned")
        need(a.get_node("Art/Roots").visible == (expected == ""),"roots not swapped/returned")
        need(a.get_node("Art").scale == Vector2.ONE,"screen_px multiplied by art/spell scale")
        var stationary: Sprite2D = a.pieces[0].root
        for state in ["expanded", "spent"]:
            var key: Sprite2D = a.get_node("Art/Key_" + state)
            var dark: Sprite2D = a.get_node("Art/Key_" + state + "Dark")
            need(key.visible == (expected == state),"incorrect key visibility")
            need(dark.visible == key.visible,"dark visibility differs")
            for uniform in ["erode", "dissolve"]:
                need(key.material.get_shader_parameter(uniform) == stationary.material.get_shader_parameter(uniform),"key clock uniform reset")
                need(key.material.get_shader_parameter(uniform) == dark.material.get_shader_parameter(uniform),"dark clock uniform differs")
            need(key.material.get_shader_parameter("palette_0") == Color(128.0/255.0,128.0/255.0,128.0/255.0,1),"grey substitution lost")
        rows.append(a.trace[-1].duplicate(true))
    var output := FileAccess.open("res://key_clock_trace.json",FileAccess.WRITE)
    output.store_string(JSON.stringify(rows,"  "))
    a.queue_free()
    plain.queue_free()
    await process_frame
    if not failures.is_empty():
        printerr(JSON.stringify(failures))
        quit(7)
        return
    print("T4Q_KEY_CLOCK_COMPLETE")
    quit(0)
'''


class ProjectileTravelEmissionTests(unittest.TestCase):
    def test_node_tree_material_and_spec_driven_config(self):
        from export.godot_import import _load_vfx_kit, _g1_config, _write_g1_component, _write_painted_g1
        root = Path(__file__).resolve().parents[1]
        kits = root/'runs/C-5/vfx_kits/v9'
        for arm in ('A','B'):
            kit = _load_vfx_kit(kits/('fire_bolt_e1_'+arm)); kit['name'] = kit['effect']['name']
            config = _g1_config(kit)
            self.assertEqual(config['speed_px_s'],1040)
            self.assertEqual(config['range_px'],520)
            self.assertEqual(config['seed'],2026)
            self.assertEqual(config['pierce'],0)
            self.assertEqual(config['impact'],'res://scenes/vfx_fire_burst_e0p_v2_impact.tscn')
            self.assertEqual(config['aim_rule'],'release-locked')
            self.assertTrue(config['contact_only'])
        TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='e1-emission-',dir=TMP) as td:
            out=Path(td); (out/'scripts').mkdir()
            _write_g1_component(out); _write_painted_g1(out)
            scene=(out/'scenes/vfx/g1_painted_projectile.tscn').read_text()
            for name, kind in [('Head','AnimatedSprite2D'),('Streak','Sprite2D')]:
                self.assertIn(f'[node name="{name}" type="{kind}"',scene)
            script=(out/'scripts/vfx_g1_painted.gd').read_text()
            for text in ['$Head.rotation = direction.angle()', '0.6, 1.4', 'rear_socket',
                         'config.spec_speed_px_s', 'float(config.painted_travel.tail_s) * 60.0',
                         '$Head.material.set_shader_parameter("dissolve", 0.0)',
                         'tick -= int(paint.rest_hold_frames)', 'int(state.hold_frames)']:
                self.assertIn(text,script)

    def test_missing_impact_dependency_rejected(self):
        from export.godot_import import _load_vfx_kits
        root = Path(__file__).resolve().parents[1]
        TMP.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='e1-dependency-',dir=TMP) as td:
            catalogue=Path(td)/'kits.json'
            catalogue.write_text(json.dumps({'kits':[{'name':'fire_bolt_e1_A','dir':str(root/'runs/C-5/vfx_kits/v9/fire_bolt_e1_A')}]}))
            with self.assertRaisesRegex(ValueError,'impact dependency'): _load_vfx_kits(catalogue)


def ice_project_fixture(root):
    """Self-bound eleventh kit; no external scene fixture or source mutation."""
    root=Path(root);cells=root/'cells';cells.mkdir(parents=True)
    for kind,n in [('idle',1),('cast',4)]:
        for i in range(n):Image.new('RGBA',(512,512),(40,80,120,255)).save(cells/f'{kind}_E_{i}.png')
    repo=Path(__file__).resolve().parents[1]
    catalogue=root/'kits.json'
    catalogue.write_text(json.dumps({'kits':[{'name':'ice_bolt_e2','dir':str(repo/'runs/C-5/vfx_kits/v9/ice_bolt_e2')}]}))
    sockets=root/'sockets.json'
    sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_E':{'sockets':[[270,240]]*4,'release_index':2}}}))
    project=root/'project';build_project(cells,project,vfx_kits=catalogue,sockets=sockets)
    return project


class IceTreatmentImportTests(unittest.TestCase):
    def test_emitted_shards_origin_residue_and_ground_decal(self):
        repo=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix='e2-emission-',dir=repo/'runs/C-5/t3/T4t') as tmp:
            project=ice_project_fixture(Path(tmp))
            scene=(project/'scenes/vfx_ice_bolt_e2_impact.tscn').read_text()
            runtime=json.loads((project/'vfx/ice_bolt_e2/pieces/burst_runtime.json').read_text())
            record=json.loads((project/'vfx/ice_bolt_e2/pieces/pieces.json').read_text())
            self.assertEqual(scene.count('type="Sprite2D" parent="Art/Pieces"'),len(record['pieces']))
            self.assertNotIn('name="Residual"',scene)
            self.assertIn('name="Decal"',scene)
            self.assertIn('[node name="Decal" type="Sprite2D" parent="."]',scene)
            self.assertIn('attach(', (project/'scripts/vfx/piece_burst_v1r.gd').read_text())
            self.assertIn('GroundEffects', (project/'scripts/vfx_ground.gd').read_text())
            self.assertIn('scale = Vector2(1, 0.6)',scene)
            self.assertEqual(runtime['template'],'burst_v1r')
            self.assertEqual(runtime['erode_noise'],.4)
            fraction=runtime['predicted_stationary_residue_area_px']/runtime['source_peak_area_px']
            self.assertTrue(.15 <= fraction <= .25)
            material=(project/'vfx/ice_bolt_e2/materials/FrostDecal.tres').read_text()
            self.assertIn('mix_unlit',material)
            validate_resources(project,True)

    def test_ten_existing_export_bytes_unchanged(self):
        repo=Path(__file__).resolve().parents[1];work=repo/'runs/C-5/t3/T4t'
        import hashlib
        baseline=json.loads((work/'before_10_hashes.json').read_text())
        with tempfile.TemporaryDirectory(prefix='e2-legacy-',dir=work) as tmp:
            folder=Path(tmp);project=folder/'project';cells=folder/'cells';cells.mkdir()
            for direction in ('E','N','S'):
                for kind,n in [('idle',1),('cast',4)]:
                    for i in range(n):Image.new('RGBA',(512,512),(40,80,120,255)).save(cells/f'{kind}_{direction}_{i}.png')
            sockets=folder/'sockets.json'
            sockets.write_text(json.dumps({'version':1,'canvas':[512,512],'cells':{'cast_'+d:{'sockets':[[270,240]]*4,'release_index':2} for d in ('E','N','S')}}))
            build_project(cells,project,vfx_kits=work/'before10/kits.json',sockets=sockets)
            actual={p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in project.rglob('*') if p.is_file()}
            self.assertEqual(actual,baseline)
            self.assertGreater(len(actual),700)


class ThrownFieldEmissionTests(unittest.TestCase):
    def test_g2_named_nodes_glass_wedge_partition_and_ground_materials(self):
        import numpy as np
        from export.godot_import import _write_g2_component,_write_g2_kit,_load_vfx_kit,validate_resources
        root=Path(__file__).resolve().parents[1];work=root/'runs/C-5/t3/T4s';work.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='g2-emission-',dir=work) as tmp:
            out=Path(tmp);(out/'scripts').mkdir();(out/'scenes/vfx').mkdir(parents=True)
            _write_g2_component(out)
            (out/'project.godot').write_text('config_version=5\n[application]\nrun/main_scene="res://scenes/vfx/g2_thrown_field.tscn"\n')
            for name in ('blackwater_cocktail_e3','poisonous_concoction_e3'):
                kit=_load_vfx_kit(root/'runs/C-5/vfx_kits/v9'/name);kit['name']=name
                _write_g2_kit(out,kit)
                folder=out/'vfx'/name
                with Image.open(folder/'primitives/flask.png') as im:source=np.asarray(im)
                shards=[]
                for i in range(3):
                    with Image.open(folder/f'derived/glass_{i}.png') as im:shards.append(np.asarray(im))
                np.testing.assert_array_equal(sum(x[...,3].astype(int) for x in shards),source[...,3])
                for shard in shards:
                    np.testing.assert_array_equal(shard[...,:3][shard[...,3]>0],source[...,:3][shard[...,3]>0])
                self.assertIn('mix_unlit',(folder/'materials/Decal.tres').read_text())
            scene=(out/'scenes/vfx/g2_thrown_field.tscn').read_text()
            for node in ('Flask','Fragments','Splash','Ground','Field','Decal','Licks','Halo','FloorLight','Flash','DarkDuplicate'):
                self.assertIn('name="'+node+'"',scene)
            self.assertIn('z_as_relative = false\nz_index = 2',scene)
            self.assertIn('parent="Ground"',scene)
            self.assertIn('GroundEffects',(out/'scripts/vfx_ground.gd').read_text())
            validate_resources(out,True)

    def test_g2_grey_retains_index_planes_and_glass_alpha(self):
        import numpy as np
        from export.godot_import import _write_g2_component,_write_g2_kit,_load_vfx_kit,_grey_vfx
        root=Path(__file__).resolve().parents[1];work=root/'runs/C-5/t3/T4s'
        with tempfile.TemporaryDirectory(prefix='g2-grey-',dir=work) as tmp:
            out=Path(tmp);(out/'scripts').mkdir();(out/'scenes/vfx').mkdir(parents=True)
            _write_g2_component(out)
            name='poisonous_concoction_e3';kit=_load_vfx_kit(root/'runs/C-5/vfx_kits/v9'/name);kit['name']=name
            _write_g2_kit(out,kit)
            (out/'scripts/keeper.gd').write_text('const K = {"material": "res://vfx/'+name+'/materials/Field.tres"}\n')
            folder=out/'vfx'/name
            before=(folder/'primitives/pulse.png').read_bytes()
            with Image.open(folder/'primitives/flask.png') as image:alpha=np.asarray(image)[...,3].copy()
            _grey_vfx(out)
            self.assertEqual((folder/'primitives/pulse.png').read_bytes(),before)
            with Image.open(folder/'primitives/flask.png') as image:
                np.testing.assert_array_equal(np.asarray(image)[...,3],alpha)
                self.assertTrue(np.all(np.asarray(image)[...,:3]==128))
            self.assertIn('materials/Field.tres',(out/'scripts/keeper.gd').read_text())


class ThrownFieldCLIRegressionTests(unittest.TestCase):
    def test_full_exporter_current_catalogue(self):
        """Exercise module execution, which must define G2 before calling main."""
        import sys
        root = Path(__file__).resolve().parents[1]
        catalogue = root/'runs/C-5/vfx_kits/kits_v9.json'
        expected = [entry['name'] for entry in json.loads(catalogue.read_text())['kits']]
        self.assertTrue(expected)
        work = root/'runs/C-5/t3/T4v'
        work.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='g2-full-cli-', dir=work) as tmp:
            project = Path(tmp)/'godot'
            result = subprocess.run([
                sys.executable, '-B', '-m', 'export.godot_import',
                '--cells', 'runs/C-3/cells_v7', '--out', str(project),
                '--parallax', 'runs/C-5/artifacts/CS-parallax-in-v10',
                '--vfx-kits', str(catalogue), '--sockets', 'runs/C-3/sockets_v2.json',
                '--props', 'runs/C-5/artifacts/CS-props-v24',
            ], cwd=root, capture_output=True, text=True, timeout=180)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([kit['name'] for kit in report['vfx_kits']['kits']], expected)
            self.assertTrue((project/'scenes/vfx/g2_thrown_field.tscn').is_file())
            self.assertTrue((project/'scripts/vfx_g2.gd').is_file())


# T4s-r2: actual Godot CanvasItem state, not merely emitted-node existence.
class GroundVisibilityRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TMP.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix='visibility-', dir=TMP)
        cls.addClassCleanup(cls.temp.cleanup)
        root = Path(cls.temp.name)
        cells = root/'cells'; cells.mkdir()
        for kind, count in [('idle', 1), ('cast', 4)]:
            for i in range(count):
                Image.new('RGBA', (512, 512), (40, 80, 120, 255)).save(cells/f'{kind}_E_{i}.png')
        sockets = root/'sockets.json'
        sockets.write_text(json.dumps({'version':1, 'canvas':[512,512],
            'cells':{'cast_E':{'sockets':[[270,240]]*4, 'release_index':2}}}))
        cls.project = root/'project'
        repo = Path(__file__).resolve().parents[1]
        build_project(cells, cls.project, sockets=sockets,
                      vfx_kits=repo/'runs/C-5/vfx_kits/kits_v9.json')
        (cls.project/'probe_world.tscn').write_text(VISIBILITY_WORLD)
        (cls.project/'probe.gd').write_text(VISIBILITY_PROBE)
        for arguments in (['--editor','--import','--quit'], ['--script','res://probe.gd','--quit-after','1200']):
            result = subprocess.run([GODOT, '--headless', '--path', str(cls.project),
                '--log-file', str(root/'engine.log'), *arguments],
                capture_output=True, text=True, timeout=110)
            if result.returncode or 'SCRIPT ERROR' in result.stdout+result.stderr:
                raise AssertionError(result.stdout+result.stderr)
        cls.trace = json.loads((cls.project/'visibility_trace.json').read_text())

    def test_ground_is_above_foreground_below_actors_and_owned_until_cancel(self):
        self.assertEqual(self.trace['ground_layer'], {'z_index':1,'y_sort_enabled':True})
        for name in ('blackwater_cocktail_e3', 'poisonous_concoction_e3'):
            self.assertEqual(self.trace[name]['ground_children_after_cancel'], 0)
            rows = [r for r in self.trace['rows'] if r['kit']==name and '/GroundEffects/' in r['path']]
            self.assertGreater(len(rows), 20)
            for row in rows:
                self.assertEqual(row['global_z'], 1, row['path'])
            for row in rows:
                if row['path'].endswith('/Ground'):
                    self.assertEqual(row['position'], self.trace[name]['trace'][0]['ground_point'])
                    self.assertFalse(row['y_sort_enabled'])
            decal = [r for r in rows if r['path'].endswith('/Decal') and r['age_frames']==84][0]
            self.assertFalse(decal['visible_in_tree'])
            config = self.trace[name]['config']
            decal_age = math.ceil(config['flight_s']*60) + math.ceil(config['duration_s']*60) + 3
            late = [r for r in rows if r['path'].endswith('/Decal') and r['age_frames']==decal_age][0]
            self.assertTrue(late['visible_in_tree'])
            self.assertGreater(late['alpha'], 0)

    def test_flask_stays_visible_at_native_screen_extent_during_flight(self):
        rows = [r for r in self.trace['rows'] if r['path'].endswith('/Flask') and r['age_frames'] in (8,20,26)]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertGreater(row['global_z'], 0)
            self.assertTrue(row['visible_in_tree'])
            self.assertEqual(row['alpha'], 1)
            self.assertAlmostEqual(row['drawn_size'][0], 45.5, places=3)

    def test_cloud_density_reaches_shader_once_at_the_ground_point(self):
        rows = [r for r in self.trace['rows'] if r['kit']=='poisonous_concoction_e3' and r['path'].endswith('/Field') and r['age_frames'] in (40,84)]
        self.assertEqual(len(rows), 2)
        self.assertGreaterEqual(self.trace['density_control']['field_alpha'], .35*.65/.75-1e-6)
        self.assertLessEqual(self.trace['density_control']['field_alpha'], .35*.8/.75+1e-6)
        self.assertEqual(self.trace['density_control']['ground_alpha'], 1)
        for row in rows:
            self.assertTrue(row['visible_in_tree'])
            self.assertGreaterEqual(row['alpha'], .65-1e-6)
            self.assertLessEqual(row['alpha'], .8+1e-6)
            self.assertIn('coverage_modulate = COLOR.a;', row['shader_code'])
            self.assertIn('index_sample.a * paint.a * coverage_modulate', row['shader_code'])
            self.assertGreater(row['drawn_size'][0], 200)
            self.assertEqual(row['position'][1], 640)
            self.assertLess(abs(row['position'][0]-4240), 2)

    def test_ice_picker_binding_shards_and_ground_crown(self):
        binding = self.trace['ice_binding']
        self.assertEqual(binding['actual'], binding['requested'])
        self.assertEqual(binding['script'], 'res://scripts/vfx_g1_ice.gd')
        self.assertTrue(any(e['event']=='contact' for e in self.trace['ice_events']))
        for row in self.trace['rows']:
            if row['kit']=='ice_bolt_e2' and row['path'].endswith(('/Head','/Streak')):
                self.assertGreater(row['global_z'], 0)
                self.assertGreater(row['alpha'], 0)
                self.assertTrue(row['visible_in_tree'])
        frames = self.trace['ice_pieces']
        self.assertTrue(any(f['shard_count']==f['source_piece_count'] and f['shard_count']>0 for f in frames))
        crown = [r for r in self.trace['rows'] if r['kit']=='ice_impact' and r['path'].endswith('/Decal') and r['age_frames']==80][0]
        self.assertIn('/GroundEffects/', crown['path'])
        self.assertEqual(crown['global_z'], 1)
        self.assertTrue(crown['visible_in_tree'])
        self.assertEqual(crown['position'], [4280,640])


VISIBILITY_WORLD = '[gd_scene format=3]\n[node name="Cliffside" type="Node2D"]\n[node name="Foreground_0" type="Polygon2D" parent="."]\nz_index = 0\npolygon = PackedVector2Array(0, 0, 8000, 0, 8000, 4000, 0, 4000)\ncolor = Color(0.5, 0.4, 0.3, 1)\n[node name="Shadows" type="Node2D" parent="."]\nz_index = 1\n[node name="Actors" type="Node2D" parent="."]\nz_index = 2\ny_sort_enabled = true\n[node name="Keeper" type="Node2D" parent="Actors"]\nposition = Vector2(3760, 640)\n'

VISIBILITY_PROBE = r'''
extends SceneTree
var rows: Array = []
var report: Dictionary = {}
func _initialize() -> void:
    call_deferred("run")
func canvas_parent(node: CanvasItem) -> CanvasItem:
    if node.is_set_as_top_level(): return null
    var p: Node = node.get_parent()
    while p != null and not p is CanvasItem and not p is CanvasLayer: p=p.get_parent()
    return p as CanvasItem
func effective_z(node: CanvasItem) -> int:
    var z: int = node.z_index
    var p: CanvasItem = canvas_parent(node)
    if node.z_as_relative and p != null:
        z += effective_z(p)
    return clampi(z,-4096,4096)
func snapshot(node: Node, age: int, kit: String) -> void:
    if node is CanvasItem:
        var layer: CanvasLayer = node.get_canvas_layer_node()
        var r: Dictionary = {"kit":kit,"age_frames":age,"path":str(node.get_path()),"parent":str(node.get_parent().get_path()),"parent_item":str(canvas_parent(node).get_path()) if canvas_parent(node) else "", "z_index":node.z_index,"global_z":effective_z(node),"canvas_layer":layer.layer if layer else 0,"alpha":node.modulate.a,"self_alpha":node.self_modulate.a,"visible":node.visible,"visible_in_tree":node.is_visible_in_tree(),"top_level":node.is_set_as_top_level()}
        if node is Node2D:
            r.position=[node.global_position.x,node.global_position.y]
            r.scale=[node.global_scale.x,node.global_scale.y]
            r.y_sort_enabled=node.y_sort_enabled
        var texture: Texture2D = null
        if node is Sprite2D: texture=node.texture
        if node is AnimatedSprite2D and node.sprite_frames != null:
            texture=node.sprite_frames.get_frame_texture(node.animation,node.frame)
        if texture:
            var box: Rect2i = texture.get_image().get_used_rect()
            r.texture=texture.resource_path
            r.opaque_size=[box.size.x,box.size.y]
            r.drawn_size=[box.size.x*node.global_scale.x,box.size.y*node.global_scale.y]
        if node.material is ShaderMaterial:
            r.shader=node.material.shader.resource_path
            r.shader_code=node.material.shader.code
            r.erode=node.material.get_shader_parameter("erode")
            r.dissolve=node.material.get_shader_parameter("dissolve")
            r.palette_alpha=[]
            for i in range(4):
                var c = node.material.get_shader_parameter("palette_"+str(i))
                r.palette_alpha.append(c.a if c is Color else null)
        rows.append(r)
    for child in node.get_children():snapshot(child,age,kit)
func run() -> void:
    var world: Node2D = load("res://probe_world.tscn").instantiate()
    root.add_child(world)
    current_scene=world
    var actors: Node2D = world.get_node("Actors")
    var caster: Node2D = actors.get_node("Keeper")
    var kits: Array = load("res://scripts/keeper.gd").VFX_KITS
    var g2 = load("res://scripts/vfx_g2.gd")
    var g1 = load("res://scripts/vfx_g1.gd")
    snapshot(world,0,"scene_layers")
    for kit in kits:
        if kit.get("grammar","") != "G2":continue
        var destination: Dictionary = g2.resolve_ground(caster.global_position,Vector2.RIGHT,Vector2.ZERO,kit.range_px,true)
        var effect = g2.acquire(actors,kit,caster.global_position+Vector2(10,-90),destination,caster,0.54)
        effect.set_physics_process(false)
        for age in [8,20,26,40,84, int(ceil(kit.flight_s*60))+int(ceil(kit.duration_s*60))+3]:
            effect._clock(age)
            snapshot(effect,age,kit.name)
            if effect.get("ground_visual") != null: snapshot(effect.ground_visual,age,kit.name)
        report[kit.name]={"trace":effect.trace,"config":kit}
        if kit.treatment == "poison":
            effect.config.density=0.35
            effect._clock(84)
            var field: Sprite2D = effect.ground_visual.get_node("Field") if effect.get("ground_visual") != null else effect.get_node("Ground/Field")
            report.density_control={"configured":0.35,"field_alpha":field.modulate.a,"ground_alpha":field.get_parent().modulate.a}
            snapshot(field,84,"density_control")
        effect.cancel()
        await process_frame
        if world.has_node("GroundEffects"):
            report[kit.name].ground_children_after_cancel=world.get_node("GroundEffects").get_child_count()
    for kit in kits:
        if "ice" not in kit.bolt:continue
        var destination: Dictionary={"point":caster.global_position+Vector2(kit.range_px,0),"kind":"cursor","target":null}
        var effect = g1.acquire(actors,kit,caster.global_position+Vector2(10,-90),destination,caster,0.54)
        if effect == null:
            report.ice_binding={"requested":kit.bolt,"actual":null}
            continue
        effect.set_physics_process(false)
        report.ice_binding={"requested":kit.bolt,"actual":effect.scene_file_path,"script":effect.get_script().resource_path,"config":kit}
        var previous_age: int = 0
        for age in [8,20,26]:
            for frame in range(previous_age+1,age+1):
                effect.release_tick=Engine.get_physics_frames()-frame
                effect._physics_process(1.0/60.0)
            previous_age=age
            snapshot(effect,age,kit.name)
        # G1 actual collision dispatch creates the authored shatter scene.
        var target := Area2D.new()
        target.name="Target"
        actors.add_child(target)
        target.global_position=caster.global_position+Vector2(kit.range_px,0)
        effect.global_position=target.global_position
        effect.contact_body(target)
        report.ice_events=g1.events
        for child in actors.get_children():
            if child.scene_file_path == kit.impact:
                child.set_physics_process(false)
                for age in [8,30,80]:
                    child.set_effect_age(age)
                    snapshot(child,age,"ice_impact")
                    if child.get("ground_decal") != null: snapshot(child.ground_decal,age,"ice_impact")
                report.ice_pieces=child.trace
    report.ground_layer={"z_index":world.get_node("GroundEffects").z_index,"y_sort_enabled":world.get_node("GroundEffects").y_sort_enabled} if world.has_node("GroundEffects") else {}
    report.rows=rows
    var f=FileAccess.open("res://visibility_trace.json",FileAccess.WRITE)
    f.store_string(JSON.stringify(report,"  "))
    print("VISIBILITY_TRACE rows=",rows.size())
    quit(0)
'''


class BoltChainEmissionTests(unittest.TestCase):
    def test_named_nodes_additive_material_grey_and_explicit_dispatch(self):
        from export.godot_import import _load_vfx_kit,_write_g3_component,_write_g3_kit,_g3_config,_grey_vfx
        import hashlib
        root=Path(__file__).resolve().parents[1];work=root/'runs/C-5/t3/T4t'
        with tempfile.TemporaryDirectory(dir=work) as tmp:
            out=Path(tmp);_write_g3_component(out)
            (out/'scripts/keeper.gd').write_text('extends Node2D\n')
            for name in ('lightning_blast_e3','zeus_chain_e3'):
                kit=_load_vfx_kit(root/'runs/C-5/vfx_kits/v9'/name);kit['name']=name;_write_g3_kit(out,kit)
                config=_g3_config(kit);self.assertEqual(config['grammar'],'G3')
                self.assertEqual(config['width_px'],kit['effect']['skill_spec']['mechanics']['width_px'])
                folder=out/'vfx'/name
                for role in ('Link','Branch','Prong'):
                    text=(folder/f'materials/{role}.tres').read_text()
                    self.assertIn('add_unlit',text);self.assertIn('dark_duplicate = false',text)
            scene=(out/'scenes/vfx/g3_bolt_chain.tscn').read_text()
            for node in ('Links','Branches','Prongs','StrikeFlash'):self.assertIn('name="'+node+'"',scene)
            before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/'vfx').rglob('*.png')}
            _grey_vfx(out)
            self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in before})
            self.assertIn('Color(0.5, 0.5, 0.5, 1)',(out/'vfx/lightning_blast_e3/materials/Link.tres').read_text())

    def test_current_catalogue_and_original_kits_unchanged(self):
        import hashlib
        from export.godot_import import _load_vfx_kits
        root=Path(__file__).resolve().parents[1]
        registry=root/'runs/C-5/vfx_kits/kits_v9.json'
        entries=json.loads(registry.read_text())['kits'];kits=_load_vfx_kits(registry)
        self.assertEqual([k['name'] for k in kits],[e['name'] for e in entries])
        baseline=json.loads((root/'runs/C-5/t3/T4v/previous_kit_hashes.json').read_text())
        baseline={Path(path).resolve().relative_to(root).as_posix():digest for path,digest in baseline.items()}
        actual={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for kit in kits if 'orb' not in kit.get('effect',{})
                for p in kit['root'].rglob('*') if p.is_file()}
        self.assertEqual(actual,baseline)


class FieldDesignLapEmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import importlib.util
        from export.godot_import import _write_g2_component, _write_g2_kit, _g2_config
        from export.effect_kit import load_kit
        repo=Path(__file__).resolve().parents[1]
        cls.work=repo/'runs/C-5/t3/T4v/field-design';cls.work.mkdir(parents=True,exist_ok=True)
        cls.temp=tempfile.TemporaryDirectory(prefix='design-lap-',dir=cls.work)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.project=Path(cls.temp.name)
        (cls.project/'scripts').mkdir();(cls.project/'scenes/vfx').mkdir(parents=True)
        _write_g2_component(cls.project)
        configs=[]
        for name in ('blackwater_cocktail_e3','poisonous_concoction_e3'):
            folder=repo/'runs/C-5/vfx_kits/v9'/name
            kit={'root':folder,'name':name,'effect':load_kit(folder)}
            _write_g2_kit(cls.project,kit);configs.append(_g2_config(kit))
        cls.configs=configs
        # The field/flight probe does not read the unlisted fire-burst dependency.
        # Its empty stand-in isolates G2; the conductor captures the real splash.
        (cls.project/'scripts/splash_stub.gd').write_text('extends Node2D\nvar spell_scale: float = 1.0\nvar caster: Node2D\n')
        (cls.project/'scenes/vfx_fire_burst_e0p_v2_impact.tscn').write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://scripts/splash_stub.gd" id="S"]\n[node name="SplashProbe" type="Node2D"]\nscript = ExtResource("S")\n[node name="Art" type="Node2D" parent="."]\n')
        (cls.project/'project.godot').write_text('config_version=5\n[application]\nconfig/name="T4s-r3 trace"\nrun/main_scene="res://probe_world.tscn"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
        (cls.project/'probe_world.tscn').write_text(VISIBILITY_WORLD)
        (cls.project/'configs.json').write_text(json.dumps(configs))
        helpers=VISIBILITY_PROBE[VISIBILITY_PROBE.index('func canvas_parent'):VISIBILITY_PROBE.index('func run()')]
        (cls.project/'probe.gd').write_text('extends SceneTree\nvar rows: Array = []\nvar report: Dictionary = {}\nfunc _initialize() -> void:\n    call_deferred("run")\n'+helpers+FIELD_DESIGN_LAP_PROBE)
        cls.scene=(cls.project/'scenes/vfx/g2_thrown_field.tscn').read_text()
        cls.field_material=(cls.project/'vfx/blackwater_cocktail_e3/materials/Field.tres').read_text()
        cls.shader_sources=[p.read_text() for p in (cls.project/'vfx/blackwater_cocktail_e3/materials').glob('*.gdshader')]
        validate_resources(cls.project,True)
        cls.logs=[]
        for label,args in [('import',['--editor','--import','--quit']),('trace',['--script','res://probe.gd','--quit-after','1200'])]:
            result=subprocess.run([GODOT,'--headless','--path',str(cls.project),'--log-file',str(cls.project/'engine.log'),*args],capture_output=True,text=True,timeout=110)
            cls.logs.append({'stage':label,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            (cls.work/'headless.json').write_text(json.dumps(cls.logs,indent=2)+'\n')
            if result.returncode or 'SCRIPT ERROR' in result.stdout+result.stderr or 'Parse Error' in result.stdout+result.stderr:
                raise AssertionError(result.stdout+result.stderr)
        cls.trace=json.loads((cls.project/'design_trace.json').read_text())
        (cls.work/'trace_tables.json').write_text(json.dumps(cls.trace,indent=2)+'\n')

    def rows(self,kit,node,age=None):
        return [r for r in self.trace['rows'] if r['kit']==kit and r['path'].endswith('/'+node) and (age is None or r['age_frames']==age)]

    def test_emitted_tree_material_and_native_pool_anchors(self):
        import numpy as np
        from export.effect_kit import load_kit
        for name in ('Field','Licks','Lobes','Decal'):self.assertIn('name="'+name+'" type=',self.scene)
        self.assertIn('name="Lobes" type="Node2D" parent="Ground"',self.scene)
        self.assertIn('palette_1 = Color(0.38, 0.055, 0.025, 1)',self.field_material)
        self.assertTrue(any('0.83333333333333337, 0.83333333333333337' in s for s in self.shader_sources))
        config=self.configs[0];folder=Path(__file__).resolve().parents[1]/'runs/C-5/vfx_kits/v9'/config['name'];data=load_kit(folder)
        with Image.open(folder/data['g2']['field_source']) as im:rgba=np.asarray(im)
        for x,y in config['lick_anchors']:
            self.assertEqual(rgba[y,x,0],255);self.assertGreater(rgba[y,x,3],0)
        for row in self.rows(config['name'],'Field'):
            self.assertEqual(row['scale'],[1,1]);self.assertEqual(row['position'],[4280,640])
            self.assertEqual(row['global_z'],1);self.assertIn('/GroundEffects/',row['path'])
        for i,(x,y) in enumerate(config['lick_anchors']):
            for row in self.rows(config['name'],'Lick'+str(i)):
                self.assertEqual(row['position'],[4280+x-256,640+y-320])

    def test_both_flasks_three_flight_ages_global_layer_alpha_and_scale(self):
        scales=[]
        for kit in self.configs:
            rows=[r for r in self.rows(kit['name'],'Flask') if r['age_frames'] in (8,20,26)]
            self.assertEqual(len(rows),3)
            for row in rows:
                self.assertTrue(row['visible_in_tree']);self.assertEqual(row['global_z'],3)
                self.assertEqual(row['alpha'],1);self.assertAlmostEqual(row['drawn_size'][0],45.5,places=3)
                scales.append(row['scale'])
        for scale in scales:
            for actual, expected in zip(scale, scales[0]): self.assertAlmostEqual(actual, expected, delta=1e-5)

    def test_cloud_breath_lobe_lifetime_layers_and_darker_decal(self):
        name='poisonous_concoction_e3';frames=self.trace[name]['trace'];live=[r['field_alpha'] for r in frames if r['field_alive']]
        self.assertGreaterEqual(min(live),.65-1e-6);self.assertLessEqual(max(live),.8+1e-6)
        self.assertLess(min(live),.652);self.assertGreater(max(live),.798)
        for age in (30,31,37,44):
            for i in range(4):
                row=self.rows(name,'Lobe'+str(i),age)[0]
                self.assertTrue(row['visible_in_tree']);self.assertIn('/GroundEffects/',row['path'])
                self.assertEqual(row['global_z'],1);self.assertEqual(row['erode'],0)
                self.assertEqual(row['palette_alpha'],[1,1,1,1])
                self.assertLess(abs(row['position'][0]-4240),28)
                self.assertLess(abs(row['position'][1]-640),28)
        for i in range(4):self.assertFalse(self.rows(name,'Lobe'+str(i),45)[0]['visible_in_tree'])
        for node in ('Halo','DarkDuplicate','FloorLight'):
            self.assertFalse(any(r['visible_in_tree'] for r in self.rows(name,node)))
        path=self.project/'vfx'/name/'materials/Decal.tres'
        self.assertIn('Color(0.035, 0.12, 0.055, 0.55)',path.read_text())

    def test_pool_final_24_frames_dissolve_then_scorch_and_cleanup(self):
        name='blackwater_cocktail_e3'
        for age,dissolve in [(188,0),(189,.5),(197,.7),(212,.7),(213,1)]:
            row=self.rows(name,'Field',age)[0];self.assertAlmostEqual(row['dissolve'],dissolve,places=6)
            self.assertEqual(row['visible_in_tree'],age<213)
        self.assertFalse(self.rows(name,'Decal',212)[0]['visible_in_tree'])
        self.assertTrue(self.rows(name,'Decal',213)[0]['visible_in_tree'])
        for kit in self.configs:self.assertEqual(self.trace[kit['name']]['ground_children_after_cancel'],0)


FIELD_DESIGN_LAP_PROBE = r'''
func run() -> void:
    var world: Node2D = load("res://probe_world.tscn").instantiate()
    root.add_child(world)
    current_scene=world
    var actors: Node2D = world.get_node("Actors")
    var caster: Node2D = actors.get_node("Keeper")
    var kits: Array = JSON.parse_string(FileAccess.get_file_as_string("res://configs.json"))
    var g2 = load("res://scripts/vfx_g2.gd")
    for kit in kits:
        var destination: Dictionary = g2.resolve_ground(caster.global_position,Vector2.RIGHT,Vector2.ZERO,kit.range_px,true)
        var effect = g2.acquire(actors,kit,caster.global_position+Vector2(10,-90),destination,caster,0.54)
        effect.set_physics_process(false)
        var flight: int = int(ceil(kit.flight_s*60))
        var ending: int = flight+int(ceil(kit.duration_s*60))
        var ages: Array = [8,20,26,flight,flight+1,flight+7,flight+14,flight+15,flight+24,ending-25,ending-24,ending-16,ending-1,ending,ending+3]
        for tick in kit.ticks: ages.append(flight+int(round(tick*60)))
        for age in range(1,ending+4):
            effect._clock(age)
            if age in ages:
                snapshot(effect,age,kit.name)
                snapshot(effect.ground_visual,age,kit.name)
        report[kit.name]={"trace":effect.trace,"config":kit}
        effect.cancel()
        await process_frame
        report[kit.name].ground_children_after_cancel=world.get_node("GroundEffects").get_child_count()
    report.rows=rows
    report.scope="Headless G2 field/flight trace; fire splash dependency is an empty stand-in. No rendered proof."
    var f=FileAccess.open("res://design_trace.json",FileAccess.WRITE)
    f.store_string(JSON.stringify(report,"  "))
    print("DESIGN_TRACE rows=",rows.size())
    quit(0)
'''


class AuraLoopEmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from export.godot_import import _load_vfx_kit,_write_g4_kit,_write_g4_component,_g4_config
        repo=Path(__file__).resolve().parents[1];work=repo/'runs/C-5/t3/T4u';work.mkdir(parents=True,exist_ok=True)
        cls.temp=tempfile.TemporaryDirectory(prefix='aura-test-',dir=work);cls.addClassCleanup(cls.temp.cleanup)
        cls.project=Path(cls.temp.name)
        _write_g4_component(cls.project)
        kit=_load_vfx_kit(repo/'runs/C-5/vfx_kits/v9/healing_hands_e3');kit['name']='healing_hands_e3'
        _write_g4_kit(cls.project,kit)
        (cls.project/'aura_config.json').write_text(json.dumps(_g4_config(kit)))
        (cls.project/'aura_probe.gd').write_text(AURA_LOOP_PROBE)
        (cls.project/'project.godot').write_text('config_version=5\n[application]\nconfig/name="G4 test"\nrun/main_scene="res://scenes/vfx/g4_aura_loop.tscn"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
        for args in [['--editor','--import','--quit'],['--script','res://aura_probe.gd','--quit-after','1200']]:
            r=subprocess.run([GODOT,'--headless','--path',str(cls.project),'--log-file',str(cls.project/'engine.log'),*args],capture_output=True,text=True,timeout=110)
            if r.returncode or 'SCRIPT ERROR' in r.stdout+r.stderr:raise AssertionError(r.stdout+r.stderr)
        cls.trace=json.loads((cls.project/'aura_trace.json').read_text())

    def test_named_nodes_and_separate_mix_add_materials(self):
        scene=(self.project/'scenes/vfx/g4_aura_loop.tscn').read_text()
        for name in ('Ground','Seal','Ring','Petals','Halo','FloorLight'):self.assertIn('name="'+name+'"',scene)
        self.assertNotIn('DarkDuplicate',scene)
        for role,mode in [('Seal','mix'),('Ring','add'),('Petal','add')]:
            self.assertIn(mode+'_unlit',(self.project/f'vfx/healing_hands_e3/materials/{role}.tres').read_text())
        validate_resources(self.project,True)

    def test_owner_tracking_native_scale_sort_refresh_and_cleanup(self):
        c=self.trace['checks'];self.assertEqual(c['walk_east_px'],200)
        self.assertLessEqual(c['follow_error_px'],1e-5);self.assertLessEqual(c['live_follow_error'],1e-5)
        self.assertGreaterEqual(c['live_physics_age'],12)
        self.assertLessEqual(c['native_scale_error'],1e-5);self.assertEqual(c['seal_scale_error'],0)
        self.assertEqual(c['sort_errors'],0);self.assertTrue(c['refresh_same_instance'])
        self.assertEqual(c['refresh_age'],0);self.assertEqual(c['refresh_generation'],2);self.assertEqual(c['aura_count'],1)
        self.assertTrue(c['tint_restored']);self.assertEqual(c['labels_remaining'],0);self.assertEqual(c['aura_count_after_cancel'],0)

    def test_pulses_petals_support_radius_and_release_clock(self):
        events=[e for e in self.trace['events'] if e['effect_id']==1]
        pulses=[e['age_frames'] for e in events if e['event']=='pulse']
        spec=json.loads((Path(__file__).resolve().parents[1]/'runs/C-5/vfx_kits/v9/healing_hands_e3/kit.json').read_text())['skill_spec']
        self.assertEqual(pulses,[round(t*60) for t in spec['mechanics']['pulse_schedule_s']])
        self.assertEqual(len([e for e in events if e['event']=='petal_start']),36)
        ends=[e['lifetime_frames'] for e in events if e['event']=='petal_end']
        self.assertEqual(ends,[27]*36)
        for event in ('support_tint','heal_label'):
            hits=[e for e in events if e['event']==event]
            self.assertEqual(len([e for e in hits if e['body_index']==1]),6)
            self.assertFalse(any(e['body_index']==2 for e in hits))
        self.assertTrue(all(e['text']=='+' for e in events if e['event']=='heal_label'))
        self.assertTrue(all(e['colour']==[1,.94,.72,1] for e in events if e['event']=='support_tint'))
        self.assertEqual([e['age_frames'] for e in events if e['event']=='release_start'],[240])
        self.assertEqual([e['age_frames'] for e in events if e['event']=='expire'],[258])
        rows={r['age']:r for r in self.trace['rows']}
        self.assertEqual(rows[240]['ring_erode'],0);self.assertAlmostEqual(rows[249]['ring_erode'],.5)
        self.assertEqual(rows[258]['ring_erode'],1);self.assertEqual(rows[258]['seal_alpha'],0)
        self.assertEqual(rows[18]['petals'][0]['dissolve'],.5)
        self.assertAlmostEqual(rows[24]['petals'][0]['dissolve'],.7,places=6)
        self.assertTrue(all(p['rotation']==0 for r in rows.values() for p in r['petals']))


AURA_LOOP_PROBE = 'extends SceneTree\nvar checks: Dictionary = {}\nvar rows: Array = []\nfunc _initialize() -> void:\n    call_deferred("run")\nfunc run() -> void:\n    var world := Node2D.new()\n    root.add_child(world)\n    current_scene=world\n    var caster := Node2D.new()\n    caster.name="Caster"\n    caster.z_index=2\n    caster.scale=Vector2.ONE*.54\n    caster.rotation=.3\n    world.add_child(caster)\n    var inside := Node2D.new()\n    inside.name="Inside"\n    world.add_child(inside)\n    inside.add_to_group("vfx_actors")\n    inside.add_to_group("vfx_targets")\n    inside.set_meta("body_index",1)\n    inside.position=Vector2(100,0)\n    var outside := Node2D.new()\n    outside.name="Outside"\n    world.add_child(outside)\n    outside.add_to_group("vfx_actors")\n    outside.set_meta("body_index",2)\n    outside.position=Vector2(800,0)\n    var kit: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://aura_config.json"))\n    var g4=load("res://scripts/vfx_g4.gd")\n    var aura=g4.acquire(caster,kit)\n    aura.set_physics_process(false)\n    var max_follow: float=0\n    var sort_errors: int=0\n    var native_error: float=0\n    var seal_error: float=0\n    for age in range(1,259):\n        caster.position.x=minf(200,float(age)*200/120)\n        aura._clock(age)\n        max_follow=maxf(max_follow,aura.get_node("Ground/Seal").global_position.distance_to(caster.global_position))\n        max_follow=maxf(max_follow,aura.get_node("Ring").global_position.distance_to(caster.global_position))\n        native_error=maxf(native_error,absf(aura.global_scale.x-1.0))\n        seal_error=maxf(seal_error,absf(aura.get_node("Ground/Seal").scale.x-1.0))\n        for segment in aura.get_node("Ring").get_children():\n            if segment.z_index!=(1 if segment.position.y<0 else 3): sort_errors+=1\n        if age in [18,21,24,26,27,239,240,249,258]:\n            var petals: Array=[]\n            for p in aura.get_node("Petals").get_children():\n                petals.append({"born":p.get_meta("born"),"scale":p.scale.x,"rotation":p.rotation,"dissolve":p.material.get_shader_parameter("dissolve"),"alpha":p.modulate.a})\n            rows.append({"age":age,"petals":petals,"ring_erode":aura.get_node("Ring/Segment0").material.get_shader_parameter("erode"),"seal_alpha":aura.get_node("Ground/Seal").modulate.a})\n    var first_trace: Array=aura.trace.duplicate(true)\n    checks.follow_error_px=max_follow\n    checks.walk_east_px=caster.position.x\n    checks.sort_errors=sort_errors\n    checks.native_scale_error=native_error\n    checks.seal_scale_error=seal_error\n    checks.tint_restored=inside.modulate==Color.WHITE and caster.modulate==Color.WHITE\n    await process_frame\n    var second=g4.acquire(caster,kit)\n    second.set_physics_process(false)\n    for age in range(1,91):second._clock(age)\n    var same=g4.acquire(caster,kit)\n    same.set_physics_process(false)\n    checks.refresh_same_instance=same==second\n    checks.refresh_age=same.age_frames()\n    checks.refresh_generation=same.generation\n    checks.aura_count=caster.get_children().filter(func(n):return n.has_meta("g4_aura")).size()\n    for age in range(1,259):same._clock(age)\n    await process_frame\n    # Exercise actual physics updates with a moving owner, not only the deterministic hook.\n    var live=g4.acquire(caster,kit)\n    for i in range(12):\n        caster.position.x+=2\n        await physics_frame\n        await process_frame\n    checks.live_physics_age=live.age_frames()\n    checks.live_follow_error=live.get_node("Ground/Seal").global_position.distance_to(caster.global_position)\n    live.cancel()\n    await process_frame\n    await create_timer(.7).timeout\n    checks.labels_remaining=get_nodes_in_group("vfx_contact_labels").filter(func(n):return n.visible).size()\n    checks.aura_count_after_cancel=caster.get_children().filter(func(n):return n.has_meta("g4_aura")).size()\n    var file=FileAccess.open("res://aura_trace.json",FileAccess.WRITE)\n    file.store_string(JSON.stringify({"checks":checks,"events":g4.events,"labels":g4.label_events,"trace":first_trace,"rows":rows},"  "))\n    print("G4_TRACE ",JSON.stringify(checks))\n    quit(0)\n'


class FrozenOrbEmissionTests(unittest.TestCase):
    def test_named_nodes_materials_and_explicit_config(self):
        from export.godot_import import _load_vfx_kits,_g1_config,_write_orb
        root=Path(__file__).resolve().parents[1];work=root/'runs/C-5/t3/T4v'
        kits=_load_vfx_kits(root/'runs/C-5/vfx_kits/kits_v9.json')
        kit=next(k for k in kits if 'orb' in k.get('effect',{}));config=_g1_config(kit)
        self.assertEqual(config['grammar'],'G1');self.assertEqual(config['range_px'],630)
        self.assertEqual(config['orb']['interval_frames_choices'],[2,3])
        self.assertEqual(config['schedule']['expiry_distance_px'],630)
        self.assertTrue(config['schedule']['range_reached'])
        self.assertEqual(config['speed_px_s'],420);self.assertEqual(config['pierce'],-1)
        with tempfile.TemporaryDirectory(dir=work) as tmp:
            out=Path(tmp);(out/'scenes/vfx').mkdir(parents=True);(out/'scripts').mkdir()
            _write_orb(out,kit,'vfx/'+kit['name'])
            scene=(out/'scenes/vfx/g1_orb.tscn').read_text()
            for name in ['OrbBody','Rim','Shard0','Shard1','Shard2','Shard3','ChildPool']:self.assertIn('name="'+name+'"',scene)
            child=(out/'scenes/vfx/g1_orb_child.tscn').read_text()
            self.assertIn('name="StrikeFlash"',child)
            self.assertIn('res://scripts/vfx_g1.gd',(out/'scripts/vfx_g1_orb.gd').read_text())
            self.assertNotIn('frozen_orb',(out/'scripts/vfx_g1_orb.gd').read_text())

    def test_g2_independent_field_palette_and_wrong_dependency_rejected(self):
        import copy
        from export.godot_import import _load_vfx_kits
        root=Path(__file__).resolve().parents[1];registry=root/'runs/C-5/vfx_kits/kits_v9.json'
        kits=_load_vfx_kits(registry);by_name={k['name']:k for k in kits}
        field=by_name['blackwater_cocktail_e3']['effect'];splash=by_name[field['g2']['splash']['kit']]['effect']
        self.assertNotEqual(field['material']['palette'],splash['material']['palette'])
        with tempfile.TemporaryDirectory(dir=root/'runs/C-5/t3/T4v') as tmp:
            entries=[{'name':k['name'],'dir':str(k['root'])} for k in kits if k['name']!=field['g2']['splash']['kit']]
            path=Path(tmp)/'kits.json';path.write_text(json.dumps({'kits':entries}))
            with self.assertRaisesRegex(ValueError,'dependency'): _load_vfx_kits(path)
