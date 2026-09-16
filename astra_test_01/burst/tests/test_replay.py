from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from export.godot_import import build_project
from export.replay import (BAKE_HOOK, PROBE, compare_bakes, compare_vo1,
                           background_comparisons, diagnose, install_hooks, movie_command, prepare_project,
                           replay_to_frame, run_replay, scene_pixel_probe)


class ReplayTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1] / 'runs/C-5/t3/T4g/unit_tmp'
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def sequence(self, name, count=3, color=(0, 0, 0, 0)):
        root = self.root / name
        root.mkdir()
        for index in range(count):
            Image.new('RGBA', (8, 8), color).save(root / f'fx{index:05}.png')
        return root

    def test_identical_and_known_bad_frame(self):
        a, b = self.sequence('a'), self.sequence('b')
        self.assertEqual(compare_bakes(a, b)['result']['value'], 0)
        path = b / 'fx00001.png'
        with Image.open(path) as im:
            im.putpixel((2, 2), (255, 0, 0, 255))
            im.save(path)
        result = compare_bakes(a, b)
        self.assertEqual(result['result']['value'], 1)
        self.assertEqual(result['frames'][1]['different_pixels'], 1)
        self.assertFalse(result['result']['passed'])

    def test_missing_frame_is_not_identical(self):
        result = compare_bakes(self.sequence('a', 3), self.sequence('b', 2))
        self.assertEqual(result['result']['value'], 1)

    def test_shifted_numbering_is_not_identical(self):
        a, b = self.sequence('a', 1), self.sequence('b', 1)
        (b / 'fx00000.png').rename(b / 'fx00001.png')
        self.assertEqual(compare_bakes(a, b)['result']['value'], 1)

    def test_byte_identity_not_only_decoded_pixels(self):
        from PIL.PngImagePlugin import PngInfo
        a, b = self.sequence('a', 1), self.sequence('b', 1)
        info = PngInfo()
        info.add_text('different', 'encoding')
        Image.new('RGBA', (8, 8)).save(b / 'fx00000.png', pnginfo=info)
        result = compare_bakes(a, b)
        self.assertEqual(result['result']['value'], 1)
        self.assertEqual(result['frames'][0]['different_pixels'], 0)

    def test_scene_pixels_known_bad(self):
        blank = self.sequence('blank')
        self.assertEqual(scene_pixel_probe(blank)['value'], 0)
        Image.new('RGBA', (8, 8), (60, 70, 80, 255)).save(blank / 'fx00001.png')
        result = scene_pixel_probe(blank)
        self.assertEqual(result['value'], 64)
        self.assertFalse(result['passed'])
        Image.new('RGB', (8, 8)).save(blank / 'fx00001.png')
        with self.assertRaises(ValueError):
            scene_pixel_probe(blank)

    def test_vo1_every_background_every_frame(self):
        live = {name: [10, 0, 100] for name in ('ground', 'black', 'white', 'foliage')}
        baked = {name: [10.5, 0, 106] for name in live}
        rows = compare_vo1(live, baked)
        self.assertEqual(len(rows), 12)
        self.assertEqual(sum(r['passed'] is False for r in rows), 4)
        self.assertTrue(all(r['passed'] is None for r in compare_vo1(live, baked, committed=False)))
        baked['black'][1] = 1
        self.assertFalse(compare_vo1(live, baked)[1]['passed'])
        baked['black'][0] = None
        self.assertIsNone(compare_vo1(live, baked)[0]['passed'])

    def test_vo1_invalid_alignment(self):
        with self.assertRaises(ValueError):
            compare_vo1({}, {})
        live = {name: [1] for name in ('ground', 'black', 'white', 'foliage')}
        with self.assertRaises(ValueError):
            compare_vo1(live, {**live, 'white': []})

    def test_movie_recipe_native_and_fixed(self):
        command = movie_command(self.root, self.root / 'bake')
        self.assertEqual(command[command.index('--fixed-fps') + 1], '60')
        self.assertTrue(command[command.index('--write-movie') + 1].endswith('/fx.png'))
        self.assertNotIn('--headless', command)
        with self.assertRaises(ValueError):
            movie_command(self.root, self.root, 0)

    def project(self):
        source = self.root / 'source'
        source.mkdir()
        (source / 'project.godot').write_text('config_version=5\n[application]\nrun/main_scene="res://main.tscn"\n[display]\nwindow/size/viewport_width=1920\nwindow/size/viewport_height=1080\n[rendering]\n')
        (source / 'main.tscn').write_text('[gd_scene format=3]\n[node name="Main" type="Node2D"]\n')
        return source

    def test_copy_preserves_source_and_installs_visibility(self):
        source = self.project()
        original = (source / 'project.godot').read_bytes()
        output = prepare_project(source, self.root / 'copy', (320, 256))
        self.assertEqual((source / 'project.godot').read_bytes(), original)
        settings = (output / 'project.godot').read_text()
        self.assertIn('viewport_width=320', settings)
        self.assertIn('viewport_height=256', settings)
        self.assertIn('viewport/transparent_background=true', settings)
        self.assertIn('common/physics_ticks_per_second=60', settings)
        self.assertTrue((output / 'replay_probe.gd').exists())
        with self.assertRaises(ValueError):
            prepare_project(source, output)
        with self.assertRaises(ValueError):
            prepare_project(source, source / 'nested')
        with self.assertRaises(ValueError):
            install_hooks(output, (1920, 1080))

    def test_legacy_export_unchanged_by_default(self):
        cells = self.root / 'cells'
        cells.mkdir()
        Image.new('RGBA', (512, 512)).save(cells / 'idle_S_0.png')
        a, b, c = (self.root / n for n in ('default', 'false', 'bake'))
        build_project(cells, a)
        build_project(cells, b, bake=False)
        build_project(cells, c, bake=True)
        for path in a.rglob('*'):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (b / path.relative_to(a)).read_bytes())
        self.assertFalse((a / 'replay_probe.gd').exists())
        self.assertIn('viewport_width=512', (c / 'project.godot').read_text())
        with self.assertRaises(ValueError):
            build_project(cells, self.root / 'invalid', bake='yes')

    def test_reset_to_frame_validation_and_forwarding(self):
        with patch('export.replay.run_replay', return_value={'frame': 9}) as run:
            self.assertEqual(replay_to_frame('p', 'out', 9, seed=2), {'frame': 9})
            run.assert_called_once_with('p', 'out', frame=9, seed=2)
        for kwargs in ({'frame': -1}, {'seed': True}, {'crop': (513, 512)}, {'bake': 'yes'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_replay(self.root, self.root / 'out', **kwargs)

    def test_four_backgrounds_use_independent_live_and_flipbook(self):
        with patch('export.replay.run_replay', return_value={}) as run:
            results = background_comparisons('project', self.root, 'baked', 'foliage.png', seed=4)
        self.assertEqual(set(results), {'ground', 'black', 'white', 'foliage'})
        self.assertEqual(run.call_count, 8)
        self.assertEqual(sum(c.kwargs['flipbook'] is not None for c in run.call_args_list), 4)
        self.assertTrue(all(c.kwargs['bake'] is False for c in run.call_args_list))

    def test_reject_bad_comparison_canvas(self):
        paths = self.sequence('frames')
        for kwargs in ({'background': 'unknown'}, {'background': 'foliage'},
                       {'flipbook': paths, 'bake': False, 'frames': 3},
                       {'probe_only': 'yes'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                run_replay(self.root, self.root / 'out', **kwargs)

    def test_diagnosis_reports_source_not_verdict(self):
        source = self.project()
        (source / 'effect.tscn').write_text('[node name="Particles" type="CPUParticles2D"]\n')
        (source / 'effect.gdshader').write_text('float clock = TIME;\n')
        kinds = {r['kind'] for r in diagnose(source)}
        self.assertEqual(kinds, {'cpu_particles', 'wall_clock'})




class BlendEnvelopeTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]/'runs/C-5/t3/T4g/unit_tmp'
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_plate_envelope_strict_threshold_and_alignment(self):
        import numpy as np
        from export.replay import plate_envelope
        plate = np.full((4, 5, 4), 255, np.uint8)
        composite = plate.copy()
        composite[0, :, 0] -= 9
        composite[1, :, 1] -= 8
        composite[..., 3] = 0  # alpha is deliberately irrelevant
        self.assertEqual(plate_envelope(plate, composite), 5)
        self.assertEqual(plate_envelope(composite, plate), 5)
        self.assertEqual(plate_envelope(plate, plate), 0)
        with self.assertRaises(ValueError):
            plate_envelope(plate, composite[:2])
        with self.assertRaises(ValueError):
            plate_envelope(plate, composite, tau=float('nan'))

    def test_three_tick_hitstop_uses_scaled_age_without_double_hold(self):
        from export.replay import effect_age_indices
        scales = [.1, .1, .1, 1., 1., 1.]
        ages = [0.]
        for scale in scales:
            ages.append(ages[-1] + scale)
        self.assertEqual(effect_age_indices(list(range(7)), ages), [0,0,0,0,1,2,3])
        self.assertNotEqual(effect_age_indices(list(range(7)), ages), list(range(7)))
        # Movie bakes contain the hold already: recorded ages give identity.
        self.assertEqual(effect_age_indices(ages, ages), list(range(7)))
        with self.assertRaises(ValueError):
            effect_age_indices([0,0], [0])

    def test_known_two_colour_stack_and_premultiplied_encoding(self):
        import numpy as np
        from export.replay import encode_blend_bake, plate_envelope
        # MIX blue and ADD orange occupy separate pixels. An ADD source is
        # invisible on white; legacy MIX turns that same pixel orange.
        mix = np.array([[[0,0,128,128],[0,0,0,0]]], np.uint8)
        add = np.array([[[0,0,0,0],[128,64,0,128]]], np.uint8)
        for name, rgba in [('mix',mix),('add',add)]:
            directory = self.root/name; directory.mkdir()
            Image.fromarray(rgba).save(directory/'fx00000.png')
            encode_blend_bake(directory,name)
        m = np.array(Image.open(self.root/'mix/fx00000.png')).astype(float)
        a = np.array(Image.open(self.root/'add/fx00000.png')).astype(float)
        white = np.full((1,2,3),255.)
        live = np.minimum(255, mix[...,:3] + white*(1-mix[...,3,None]/255) + add[...,:3])
        replay = np.minimum(255, m[...,:3]*m[...,3,None]/255 + white*(1-m[...,3,None]/255) + a[...,:3]*a[...,3,None]/255)
        old = mix.astype(float)+add.astype(float)
        old_replay = old[...,:3]*old[...,3,None]/255 + white*(1-old[...,3,None]/255)
        np.testing.assert_allclose(replay, live, atol=1)
        self.assertEqual(plate_envelope(white,live),1)
        self.assertEqual(plate_envelope(white,replay),1)
        self.assertEqual(plate_envelope(white,old_replay),2)

    def test_plate_comparison_counts_zeros_and_missing_frames(self):
        import numpy as np
        from export.replay import plate_envelope_comparison
        baked = self.root/'baked'; baked.mkdir()
        for i in range(3):
            Image.new('RGBA',(8,8)).save(baked/f'fx{i:05}.png')
        def capture(project, out, **kwargs):
            out = Path(out); out.mkdir(parents=True)
            for i in range(3):
                frame = np.zeros((8,8,4),np.uint8)
                frame[...,3] = 255
                count = 0 if kwargs['blank'] else (0 if i == 0 else 20)
                if kwargs['flipbook'] is not None and i == 2:
                    count = 22
                frame.reshape(-1,4)[:count,0] = 9
                Image.fromarray(frame).save(out/f'fx{i:05}.png')
            return dict(returncode=0,engine_errors=[],probe_exists=True)
        with patch('export.replay.run_replay',side_effect=capture) as runner:
            result = plate_envelope_comparison('project',self.root/'comparison',baked,
                                               grounds=('black','white'),frames=3)
        self.assertEqual(runner.call_count,6)
        self.assertEqual(len(result['rows']),6)
        self.assertEqual(result['summary']['black'],dict(frames=3,failed=1,worst_frame=2,live_peak=20,flip_peak=22))
        self.assertEqual(result['rows'][0]['relative_difference'],0)
        self.assertEqual(result['rows'][2]['relative_difference'],.1)
        self.assertEqual(result['rows'][2]['tolerance'],.05)
        with self.assertRaises(ValueError):
            plate_envelope_comparison('project',self.root/'bad',baked,grounds=('black',),frames=4)

    def test_crop_settings_and_age_metadata_are_written(self):
        import json
        import subprocess
        project = self.synthetic_project()
        with patch('export.replay.subprocess.run',return_value=subprocess.CompletedProcess([],0,'','')):
            result = run_replay(project,self.root/'mock',effect='res://effect.tscn',crop=(768,768))
        settings = (project/'project.godot').read_text()
        self.assertIn('window/size/viewport_width=768',settings)
        self.assertIn('window/size/window_width_override=768',settings)
        self.assertIn('window/stretch/mode="disabled"',settings)
        self.assertEqual(result['config']['bake_layer'],'all')
        self.assertIn('camera.zoom = Vector2.ONE',PROBE)
        self.assertIn('effect_age += Engine.time_scale',PROBE)
        self.assertNotIn('mini(captures',PROBE)
        for kwargs in ({'bake_layer':'unknown'},{'bake':False,'bake_layer':'mix'}):
            with self.assertRaises(ValueError):
                run_replay(project,self.root/'invalid',effect='res://effect.tscn',**kwargs)

    def synthetic_project(self):
        from export.replay import install_hooks
        source = self.root/'project'; source.mkdir()
        (source/'project.godot').write_text('config_version=5\n[application]\nrun/main_scene="res://main.tscn"\n[display]\nwindow/size/viewport_width=512\nwindow/size/viewport_height=512\nwindow/stretch/mode="canvas_items"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
        (source/'main.tscn').write_text('[gd_scene format=3]\n[node name="Main" type="Node2D"]\n')
        (source/'effect.tscn').write_text('''[gd_scene load_steps=3 format=3]
[sub_resource type="CanvasItemMaterial" id="Add"]
blend_mode = 1
light_mode = 1
[sub_resource type="CanvasItemMaterial" id="Mix"]
blend_mode = 0
light_mode = 1
[node name="Effect" type="Node2D"]
[node name="MixBlue" type="Polygon2D" parent="."]
material = SubResource("Mix")
polygon = PackedVector2Array(-32,-32,0,-32,0,32,-32,32)
color = Color(0,0,1,0.5)
[node name="AddOrange" type="Polygon2D" parent="."]
material = SubResource("Add")
polygon = PackedVector2Array(0,-32,32,-32,32,32,0,32)
color = Color(1,0.5,0,0.5)
''')
        install_hooks(source)
        return source

    def render(self, project, name, **kwargs):
        from export.replay import GODOT
        import os
        unavailable = os.environ.get('T4G_RENDERING_UNAVAILABLE_REASON')
        if unavailable:
            self.skipTest(unavailable)
        if not Path(GODOT).exists():
            self.skipTest('Godot executable unavailable')
        result = run_replay(project, self.root/name, effect='res://effect.tscn',
                            origin=(0,0), frames=4, timeout=119, **kwargs)
        self.assertEqual(result['returncode'],0,result)
        self.assertEqual(result['engine_errors'],[],result)
        self.assertTrue(result['probe_exists'],result)
        return self.root/name

    def test_native_crop_64px_body_512_and_768_and_class_replay(self):
        import numpy as np
        from export.replay import plate_envelope
        project = self.synthetic_project()
        measurements = []
        for size in (512,768):
            output = self.render(project, f'crop_{size}', crop=(size,size))
            with Image.open(sorted(output.glob('fx*.png'))[-1]) as image:
                rgba = np.array(image)
            self.assertEqual(rgba.shape[:2],(size,size))
            y,x = np.where(rgba[...,:3].max(-1)>0)
            measurements.append([int(x.max()-x.min()+1),int(y.max()-y.min()+1)])
            self.assertEqual(measurements[-1],[64,64])
            self.assertEqual([(x.min()+x.max()+1)/2,(y.min()+y.max()+1)/2],[size/2,size/2])
        self.assertEqual(measurements[0],measurements[1])
        add = self.render(project,'add',bake_layer='add')
        mix = self.render(project,'mix',bake_layer='mix')
        live = self.render(project,'live',bake=False,background='white')
        plate = self.render(project,'plate',bake=False,blank=True,background='white')
        flip = self.render(project,'flip',bake=False,background='white',flipbook={'add':add,'mix':mix})
        old = self.render(project,'old',bake=False,background='white',flipbook=self.root/'crop_512')
        def last(directory):
            return sorted(directory.glob('fx*.png'))[-1]
        baseline = last(plate)
        expected = plate_envelope(baseline,last(live))
        self.assertEqual(expected,32*64)
        self.assertEqual(plate_envelope(baseline,last(flip)),expected)
        self.assertEqual(plate_envelope(baseline,last(old)),64*64)

if __name__ == '__main__':
    unittest.main()
