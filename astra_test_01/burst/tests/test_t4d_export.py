"""T4d regressions: grey export resources/alpha and cached flipbook uploads.

The optional real-render probe is tests/probe_t4d_flipbook.py --render. It uses
production replay_probe.gd and compares captured pixels against RGBA source-over.
"""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest import mock

import numpy as np
from PIL import Image

from export.godot_import import build_project, validate_resources
from export.replay import PROBE, install_hooks, run_replay

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/'runs/C-5/t3/T4f/project'


def restore_exported_kits(project, destination):
    """Rehydrate the T4f exported fixtures into the builder's phase layout."""
    entries = []
    for source in sorted((project/'vfx').iterdir()):
        if not (source/'kit.json').exists():
            continue
        target = destination/source.name
        target.mkdir(parents=True)
        data = json.loads((source/'kit.json').read_text())
        # Exported project paths carry sprites/; original kit paths do not.
        def phase_path(path):
            return path.removeprefix('sprites/')
        for record in data['phases'].values():
            record['sheet'] = phase_path(record['sheet'])
            for frame in record['frames']:
                original = frame['file']
                frame['file'] = phase_path(original)
                dest = target/frame['file']; dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source/original, dest)
        for folder in ('layers','distance'):
            if (source/folder).exists(): shutil.copytree(source/folder,target/folder)
        data['distance_fields'] = {phase_path(k):v for k,v in data['distance_fields'].items()}
        (target/'kit.json').write_text(json.dumps(data))
        (target/'vfx_select.json').write_text('{}')
        (target/'CREDITS.txt').write_text('Read-only T4f fixture; native index maps retained.\n')
        entries.append(dict(name=source.name,dir=str(target)))
    catalogue = destination/'kits.json'
    catalogue.write_text(json.dumps(dict(kits=entries)))
    return catalogue


class T4dExportTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp',prefix='t4d_export_')
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def test_t4f_grey_export_validates_resources_and_preserves_every_alpha(self):
        self.assertTrue(FIXTURE.is_dir(), 'Required T4f fixture missing')
        catalogue = restore_exported_kits(FIXTURE,self.path/'kits')
        out = self.path/'grey'
        build_project(FIXTURE/'sprites',out,sockets=FIXTURE/'sockets.json',
                      vfx_kits=catalogue,vfx_grey=True)
        self.assertTrue(validate_resources(out,include_scenes=True))
        count = 0
        for path in (out/'vfx').rglob('*.png'):
            if 'sprites' not in path.parts: continue
            original = FIXTURE/path.relative_to(out)
            with Image.open(path) as image: actual = np.array(image)
            with Image.open(original) as image: expected = np.array(image)
            np.testing.assert_array_equal(actual[...,3],expected[...,3])
            self.assertTrue(np.all(actual[...,:3] == 128),str(path))
            count += 1
        self.assertGreater(count,0)
        # Removing body materials must not remove glow or floor-light materials.
        scene = (out/'scenes/vfx_frozen_orb_impact.tscn').read_text()
        self.assertIn('id="MaterialAdditive"',scene)
        self.assertNotIn('id="MaterialBody"',scene)
        self.assertNotIn('id="MaterialMix"',scene) if 'ExtResource("MaterialMix")' not in scene else None
        for name in ('Shatter','Residual'):
            block = re.search(r'\[node name="'+name+r'"[^\n]*\n(.*?)(?=\n\[|\Z)',scene,re.S)[1]
            self.assertNotIn('material =',block)

    def test_known_bad_stale_scene_resource_declaration_rejected(self):
        cells = self.path/'cells'; cells.mkdir()
        Image.new('RGBA',(512,512),(100,80,60,255)).save(cells/'idle_S_00.png')
        out = self.path/'project'; build_project(cells,out)
        scene = out/'scenes/main.tscn'
        text = scene.read_text().replace('[node ', '[ext_resource type="Texture2D" path="res://sprites/idle/S/idle_S_00.png" id="Unused"]\n\n[node ',1)
        scene.write_text(text)
        with self.assertRaisesRegex(ValueError,'external resource references'):
            validate_resources(out,include_scenes=True)

    def test_flipbook_texture_upload_is_outside_draw_callback_and_retained(self):
        body = PROBE.split('func _set_flip_frame() -> void:',1)[1].split('\nfunc ',1)[0]
        self.assertNotIn('create_from_image',body)
        self.assertNotIn('load_from_file',body)
        self.assertIn('flip_textures[',body)
        self.assertIn('image.is_empty()',PROBE)
        self.assertIn('image.get_format() != Image.FORMAT_RGBA8',PROBE)
        self.assertIn('report.flipbook_loaded',PROBE)
        self.assertIn('flip_sprite.position = Vector2(root.size) * 0.5',PROBE)

    def test_known_bad_flipbook_rgb_rejected_before_engine(self):
        frames = self.path/'frames';frames.mkdir()
        Image.new('RGB',(64,64),(255,255,255)).save(frames/'fx00000000.png')
        with self.assertRaisesRegex(ValueError,'native RGBA'):
            run_replay(self.path/'unused',self.path/'out',frames=1,crop=(64,64),
                       bake=False,flipbook=frames)


if __name__ == '__main__': unittest.main()
