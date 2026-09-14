"""T3i socket, directional-resource, geometry and engine contracts."""
import copy
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from PIL import Image, ImageDraw
from export.sockets import build_sockets, load_sockets
from export.godot_import import build_project, discover_cells, validate_resources
from export.scene_kit import largest_walkable_rectangle, _contains

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT/'tests/tmp'
GODOT = '/Applications/Godot.app/Contents/MacOS/Godot'


def annotation():
    return {'plate_size': [100,100], 'walkable': [[[0,0],[100,0],[100,100],[0,100]]],
            'blocked': [], 'occluders': [], 'exits': [], 'spawn': [10,10], 'figure_height_px': 120}


class SocketTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=TMP, prefix='t3i-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cells = self.root/'cells'
        self.folder = self.cells/'cast_S/frames/cast/S'
        self.folder.mkdir(parents=True)
        im = Image.new('RGBA', (512,512)); draw = ImageDraw.Draw(im)
        draw.rectangle((225,155,265,195),fill='white');draw.rectangle((215,196,280,399),fill='white')
        draw.line((170,90,170,380), fill='white', width=3)
        for i in range(8): im.save(self.folder/f'cast_S_{i:02d}.png')
        self.path = self.root/'sockets.json'
        self.kit = self.root/'kit'
        for name in ('flare','impact'):
            (self.kit/name).mkdir(parents=True)
            for i in range(5): Image.new('RGBA',(32,32),(10,120,220,150)).save(self.kit/name/f'{name}_{i:02d}.png')
        (self.kit/'CREDITS.txt').write_text('Synthetic test asset credit.\n')
        self.scene = self.root/'scene';self.scene.mkdir()
        (self.scene/'annotation.json').write_text(json.dumps(annotation()))
        Image.new('RGBA',(100,100)).save(self.scene/'plate.png')

    def test_default_override_all_cells_and_invalid_release(self):
        data = build_sockets(self.cells,self.path)
        self.assertEqual(len(data['cells']['cast_S']['sockets']),8)
        self.assertEqual(data['cells']['cast_S']['release_index'],3)
        self.assertEqual(load_sockets(self.path, discover_cells(self.cells)),data)
        meta = self.cells/'cast_S/registration.json'
        meta.write_text('{"release_output_index":0}')
        self.assertEqual(build_sockets(self.cells,self.path)['cells']['cast_S']['release_index'],0)
        other = self.cells/'idle/E';other.mkdir(parents=True)
        Image.open(self.folder/'cast_S_00.png').save(other/'idle_E_00.png')
        self.assertEqual(len(build_sockets(self.cells,self.path)['cells']),1)
        self.assertEqual(len(build_sockets(self.cells,self.path,True)['cells']),2)
        for bad in (-1,8,True,1.5,'3'):
            with self.subTest(release=bad):
                meta.write_text(json.dumps({'release_output_index':bad}))
                with self.assertRaises(ValueError): build_sockets(self.cells,self.path)

    def test_missing_coordinate_is_explicit_and_malformed_rejected(self):
        Image.new('RGBA',(512,512)).save(self.folder/'cast_S_03.png')
        data=build_sockets(self.cells,self.path)
        self.assertIsNone(data['cells']['cast_S']['sockets'][3])
        self.assertEqual(data['cells']['cast_S']['measurements'][3]['reason'],'empty_alpha')
        for mutate in (lambda d:d['cells'].clear(),lambda d:d.update(canvas=[1,2]),
                       lambda d:d['cells']['cast_S'].update(release_index=8),
                       lambda d:d['cells']['cast_S']['sockets'].pop(),
                       lambda d:d['cells']['cast_S']['sockets'].__setitem__(0,[512,100]),
                       lambda d:d['cells']['cast_S']['sockets'].__setitem__(0,[float('nan'),100])):
            bad=copy.deepcopy(data);mutate(bad);self.path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError): load_sockets(self.path,discover_cells(self.cells))

    def build(self):
        build_sockets(self.cells,self.path)
        out=self.root/'project'
        report=build_project(self.cells,out,scene=self.scene,vfx_kit=self.kit,sockets=self.path)
        return out,report

    def test_all_new_resources_release_transform_directions_and_credits(self):
        (self.kit/'vfx_select.json').write_text('{"impact_range":[2,4]}')
        out,report=self.build()
        self.assertEqual(report['vfx_kit']['frames'],{'flare':5,'impact':3})
        rectangle_report = report['vfx_kit']['ambient_rectangle_report']
        self.assertEqual(rectangle_report['cell_size'], 8)
        self.assertEqual(rectangle_report['cells'], 144)
        self.assertEqual(rectangle_report['area_px2'], 6400)
        self.assertGreaterEqual(rectangle_report['wall_s'], 0)
        self.assertEqual(report['vfx_kit']['ambient_rectangle'], [8, 8, 88, 88])
        refs=validate_resources(out,True)
        self.assertTrue(refs)
        keeper=(out/'scripts/keeper.gd').read_text()
        cast=keeper.split('if Input.is_action_just_pressed("cast"):')[1].split('if Input.is_action_just_pressed("jump"):')[0]
        self.assertNotIn('_spawn_frost()',cast)
        for token in ('sprite.frame_changed.connect(_cast_frame_changed)', 'sprite.frame != int(cell.release_index)',
                      'cast_fired = true', 'sprite.to_global(local)', 'sprite.offset',
                      'FACING_VECTORS[facing].normalized()', 'flare.rotation = direction.angle()',
                      'CanvasItemMaterial.BLEND_MODE_ADD', 'sprite.global_transform.x.length()'):
            self.assertIn(token,keeper)
        bolt=(out/'scenes/frost_bolt.tscn').read_text()
        for token in ('type="Area2D"','type="CircleShape2D"','type="GradientTexture2D"',
                      'type="CPUParticles2D"','amount = 70','lifetime = 0.35','spread = 8.0',
                      'local_coords = false','initial_velocity_min = 40.0','initial_velocity_max = 60.0',
                      'scale_amount_curve = SubResource("Shrink")','color_ramp = SubResource("CometColors")'):
            self.assertIn(token,bolt)
        script=(out/'scripts/frost_bolt.gd').read_text()
        for token in ('520.0 * spell_scale','650.0 * spell_scale','is StaticBody2D','intersect_ray(query)',
                      '$Trail.direction = -direction','if expired:','_impact()'):
            self.assertIn(token,script)
        impact=(out/'scenes/frost_impact.tscn').read_text()
        shatter=impact.split('[node name="Shatter"')[1].split('[node name="Burst"')[0]
        self.assertNotIn('material',shatter)
        for token in ('one_shot = true','explosiveness = 1.0','amount = 40','spread = 180.0',
                      'initial_velocity_min = 120.0','initial_velocity_max = 260.0','gravity = Vector2(0, 300)','lifetime = 0.5'):
            self.assertIn(token,impact)
        self.assertIn('0.9 * 240.0 * spell_scale', (out/'scripts/frost_impact.gd').read_text())
        ambient=(out/'scenes/ambient.tscn').read_text()
        for token in ('amount = 40','lifetime = 6.0','gravity = Vector2(0, -4)',
                      'initial_velocity_min = 5.0','initial_velocity_max = 15.0','emission_shape = 3'):
            self.assertIn(token,ambient)
        self.assertIn('Synthetic test asset credit.',(out/'README.md').read_text())
        # Every external resource and every subresource is declared/used.
        for p in out.rglob('*.tscn'):
            s=p.read_text(); declared=re.findall(r'\[sub_resource .*? id="(.*?)"\]',s)
            self.assertEqual(len(declared),len(set(declared)))
            self.assertEqual(set(declared),set(re.findall(r'SubResource\("(.*?)"\)',s)))
        (out/'scenes/frost_bolt.tscn').write_text(bolt.replace('SubResource("Dot")','SubResource("MISSING")'))
        with self.assertRaises(ValueError): validate_resources(out,True)

    def test_invalid_kit_gap_range_rgb_and_missing_credit(self):
        for selection in ({'impact_range':[-1,4]}, {'impact_range':[4,2]}, {'impact_range':[0,9]}, {'impact_range':[True,4]}):
            (self.kit/'vfx_select.json').write_text(json.dumps(selection))
            with self.assertRaises(ValueError): build_project(self.cells,self.root/'bad',vfx_kit=self.kit)
        (self.kit/'vfx_select.json').unlink()
        frame=self.kit/'flare/flare_02.png';frame.rename(self.kit/'flare/flare_06.png')
        with self.assertRaises(ValueError): build_project(self.cells,self.root/'bad',vfx_kit=self.kit)
        (self.kit/'flare/flare_06.png').rename(frame)
        Image.new('RGB',(32,32)).save(frame)
        with self.assertRaises(ValueError): build_project(self.cells,self.root/'bad',vfx_kit=self.kit)
        (self.kit/'CREDITS.txt').unlink()
        with self.assertRaises(ValueError): build_project(self.cells,self.root/'bad',vfx_kit=self.kit)

    def test_real_cast_coverage(self):
        data=build_sockets(ROOT/'runs/C-3/cells',self.path)
        expected={'cast_'+d for d in ('S','SW','W','NW','N','NE','E','SE')}
        self.assertEqual(set(data['cells']),expected)
        for cell in data['cells'].values():
            self.assertEqual(len(cell['sockets']),8)
            self.assertEqual(cell['release_index'],3)
            self.assertTrue(all(p is not None for p in cell['sockets']))

    @unittest.skipUnless(Path(GODOT).is_file(),'Godot unavailable')
    def test_headless_directional_release_and_resources(self):
        out,_=self.build()
        (out/'probe.gd').write_text(PROBE)
        engine_errors=[]
        for args in (['--import'],['--script','res://probe.gd']):
            result=subprocess.run([GODOT,'--headless','--log-file',str(self.root/'godot.log'),'--path',str(out),*args],capture_output=True,text=True,timeout=60)
            log=result.stdout+result.stderr
            self.assertEqual(result.returncode,0,log)
            self.assertNotIn('SCRIPT ERROR',log)
            self.assertNotIn('T3I_ASSERTION:',log)
            engine_errors.extend(line for line in log.splitlines() if 'ERROR' in line)
        self.assertIn('T3I_RUNTIME_ASSERTIONS=complete',log)
        self.assertEqual(engine_errors,[], '\n'.join(engine_errors))


class AmbientRectangleTests(unittest.TestCase):
    def contained(self,a,rect):
        x0,y0,x1,y1=rect
        for i in range(51):
            for j in range(51):
                p=(x0+(x1-x0)*(i+.01)/50.02,y0+(y1-y0)*(j+.01)/50.02)
                self.assertTrue(any(_contains(p,poly) for poly in a['walkable']),p)
                self.assertFalse(any(_contains(p,poly) for poly in a['blocked']),p)

    def test_rectangle_hole_union_and_concavity_largest_and_contained(self):
        # Full 8-px cells, largest raster rectangle, then an 8-px inset.
        cases=[]
        a=annotation();cases.append((a,80*80))
        a=annotation();a['blocked']=[[[40,40],[60,40],[60,60],[40,60]]];cases.append((a,24*80))
        a=annotation();a['walkable']=[[[0,0],[60,0],[60,100],[0,100]],[[40,0],[100,0],[100,100],[40,100]]];cases.append((a,80*80))
        a=annotation();a['walkable']=[[[0,0],[100,0],[100,30],[30,30],[30,100],[0,100]]];cases.append((a,80*8))
        for a,area in cases:
            with self.subTest(area=area):
                rect=largest_walkable_rectangle(a);self.contained(a,rect)
                self.assertEqual((rect[2]-rect[0])*(rect[3]-rect[1]),area)
                self.assertTrue(all(v % 8 == 0 for v in rect))

    def test_slanted_fractional_global_optimum(self):
        a=annotation();a['walkable']=[[[0,0],[100,0],[0,100]]]
        rect=largest_walkable_rectangle(a);self.contained(a,rect)
        # Triangle: a 6x6-cell maximum becomes 4x4 after inset.
        self.assertEqual((rect[2]-rect[0])*(rect[3]-rect[1]),32*32)
        a['walkable']=[[[0.25,0.25],[99.75,0.25],[99.75,99.75],[0.25,99.75]]]
        rect=largest_walkable_rectangle(a)
        # Fractional edges discard their partial cells: 11x11 -> 9x9.
        self.contained(a,rect)
        self.assertEqual(rect,[16,16,88,88])
        self.assertEqual((rect[2]-rect[0])*(rect[3]-rect[1]),72*72)

    def test_fixture_room_rectangle_avoids_blocked_pillar(self):
        # Same fixture geometry, sourced from the authorized synthetic test.
        from test_scene_kit import annotation as fixture_annotation
        a=fixture_annotation()
        rect=largest_walkable_rectangle(a);self.contained(a,rect)
        # Raster room corridor is 28x32 full cells before the one-cell inset.
        self.assertEqual((rect[2]-rect[0])*(rect[3]-rect[1]),208*240)
        self.assertTrue(all(v % 8 == 0 for v in rect))

    def test_bad_geometry_rejected(self):
        a=annotation();a['walkable']=[]
        with self.assertRaises(ValueError):largest_walkable_rectangle(a)


PROBE='''extends SceneTree
func check(ok: bool, message: String) -> void:
    if not ok:
        printerr("T3I_ASSERTION: ", message)
        quit(7)
func _initialize() -> void:
    call_deferred("probe")
func probe() -> void:
    var scene: Node = load("res://scenes/main.tscn").instantiate()
    root.add_child(scene)
    await process_frame
    var keeper: Node = scene.get_node("Keeper")
    keeper.set_physics_process(false)
    keeper.state = "cast"
    keeper.cast_fired = false
    keeper._play_state()
    keeper.sprite.pause()
    keeper.sprite.frame = 2
    check(not keeper.cast_fired, "no fire before release")
    var before: int = scene.get_child_count()
    keeper.sprite.frame = 3
    check(keeper.cast_fired, "fires at release")
    check(scene.get_child_count() == before + 2, "flare and bolt")
    var bolt: Area2D = scene.get_child(scene.get_child_count()-1)
    check(bolt.direction == Vector2.DOWN, "south facing")
    check(bolt.global_position.distance_to(keeper._socket_world()) < 0.01, "socket transform")
    keeper._cast_frame_changed()
    check(scene.get_child_count() == before + 2, "only one fire")
    bolt.set_physics_process(false)
    bolt._physics_process(10.0)
    check(bolt.expired, "range expiration")
    check(is_equal_approx(bolt.distance, 650.0), "range cap")
    for key in keeper.FACING_VECTORS:
        check(is_equal_approx(keeper.FACING_VECTORS[key].normalized().length(),1), "normalized facing")
    var wall := StaticBody2D.new()
    var shape := CollisionShape2D.new()
    var circle := CircleShape2D.new()
    circle.radius = 10.0
    shape.shape = circle
    wall.add_child(shape)
    scene.add_child(wall)
    wall.position = Vector2(700,300)
    await physics_frame
    await physics_frame
    var hit_bolt: Area2D = load("res://scenes/frost_bolt.tscn").instantiate()
    hit_bolt.direction = Vector2.RIGHT
    hit_bolt.spell_scale = 0.5
    scene.add_child(hit_bolt)
    hit_bolt.position = Vector2(600,300)
    hit_bolt.set_physics_process(false)
    hit_bolt._physics_process(0.1)
    check(is_equal_approx(hit_bolt.position.x,626.0), "scaled 260 px/s")
    hit_bolt._physics_process(1.0)
    check(hit_bolt.expired, "static wall collision")
    check(hit_bolt.position.x < 700.0, "continuous collision does not tunnel")
    keeper.sprite.scale = Vector2(0.5,0.5)
    keeper.sprite.rotation = 0.2
    keeper.sprite.frame = 0
    var expected_socket: Vector2 = keeper.sprite.to_global(Vector2(170,90) + keeper.sprite.offset)
    check(keeper._socket_world().distance_to(expected_socket) <= 2.0, "scaled rotated socket")
    await create_timer(1.0).timeout
    print("T3I_RUNTIME_ASSERTIONS=complete")
    quit(0)
'''

if __name__ == '__main__':unittest.main()
