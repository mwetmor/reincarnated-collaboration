import json
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from gates.idle_intent import evaluate
from gates_helpers import TemporaryTest, ROOT
from test_oracle_idle import synthetic


def band_row(committed=True):
    return dict(committed=committed,provenance={'fps':12},
        breath_amplitude_H=dict(floor=.04,target=.06,ceiling=.09),
        head_sway_H=dict(floor=.012,target=.02,ceiling=.03),
        lock_regions=['hips','legs','feet'],motion_regions=['head','shoulders_chest'])


class Tests(TemporaryTest):
    def save(self,frames):
        directory=self.base/'idle';directory.mkdir(exist_ok=True)
        for i,f in enumerate(frames):
            a=np.dstack((f,np.any(f,axis=2).astype(np.uint8)*255))
            Image.fromarray(a).save(directory/f'frame_{i:03}.png')
        return directory

    def test_target_and_displacement_regions(self):
        frames=synthetic()[:48]
        # Static hip-level instrument tips preserve the original 100px-wide
        # synthetic measurement box under alpha-union registration.
        for f in frames:
            f[260:280,206:210]=(110,95,85)
            f[260:280,302:306]=(110,95,85)
        r=evaluate(self.save(frames),band_row(),'synthetic')
        self.assertTrue(r['passed'],r)
        self.assertFalse(r['value']['breath']['below_floor'])
        self.assertAlmostEqual(r['value']['breath']['value'],.06,delta=.06*.15)
        self.assertIn('shoulders_chest',r['value']['classification']['MOTION'])
        self.assertEqual(r['value']['sole_displacement_H'],0.)
        json.dumps(r,allow_nan=False)

    def test_static_below_floor_and_provisional(self):
        path=self.save(synthetic(static=True)[:8]);r=evaluate(path,band_row(),'static')
        self.assertFalse(r['passed']);self.assertTrue(r['value']['head_bob']['below_floor'])
        provisional=evaluate(path,band_row(False),'static')
        self.assertIsNone(provisional['passed'])
        self.assertTrue(all(c['passed'] is None for c in provisional['value']['checks']))

    def test_sole_slide_and_panting(self):
        frames=synthetic()[:24]
        for i,f in enumerate(frames):
            f[310:330]=np.roll(f[310:330],i%3,axis=1)
        row=band_row();row['breath_amplitude_H']['ceiling']=.01
        r=evaluate(self.save(frames),row,'bad')
        self.assertFalse(r['passed']);self.assertTrue(r['value']['breath']['panting'])
        self.assertGreater(r['value']['sole_displacement_H'],.0025)

    def test_k3_combat_report_only(self):
        path=ROOT/'runs/C-1/artifacts/K3-reg-02/frames/idle/S'
        if not path.exists():self.skipTest('K3 registered idle absent')
        row=dict(json.loads((ROOT/'oracle/bands_idle.json').read_text())['combat'], committed=False)
        r=evaluate(path,row,'combat')
        self.assertIsNone(r['passed'])
        self.assertTrue(r['value']['breath']['below_floor'])
        self.assertTrue(r['value']['head_bob']['below_floor'])

    def test_frozen_narrow_box_search_limit_reported(self):
        r=evaluate(self.save(synthetic()[:24]),band_row(),'narrow')
        self.assertTrue(r['value']['breath']['below_floor'])
        limits=r['value']['regions']['shoulders_chest']['search_limit_frames']['horizontal']
        self.assertTrue(limits['left'] or limits['right'])
