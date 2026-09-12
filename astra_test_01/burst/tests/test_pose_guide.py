import numpy as np
from PIL import Image
from gates_helpers import TemporaryTest
from oracle.pose_guide import render_walk_guide,render_idle_guide,SOLE_COLORS
from oracle.dope_sheet import walk_sheet,idle_sheet
from test_dope_sheet import numeric_walk
from test_idle_intent import band_row
from test_oracle_idle import synthetic


class Tests(TemporaryTest):
    def test_twelve_pngs_exact_sole_pixels(self):
        sheet=walk_sheet(numeric_walk());images=render_walk_guide(sheet,400)
        self.assertEqual(list(images),[f'walk_{i:02}.png' for i in range(12)])
        for row,(name,im) in zip(sheet['frames'],images.items()):
            path=self.base/name;im.save(path)
            with Image.open(path) as loaded:
                self.assertEqual(loaded.size,(512,512))
                for j,sole in enumerate(row['soles'].values()):
                    x=round(256+sole['x_H']*400);y=round(round(512*.88)-sole['height_H']*400)
                    # Outline bottom at the exact numeric sole anchor.
                    self.assertEqual(loaded.getpixel((x,y)),SOLE_COLORS[j])
        moved=walk_sheet(numeric_walk());moved['frames'][0]['soles']['L']['x_H']+=.05
        other=render_walk_guide(moved,400)['walk_00.png']
        self.assertNotEqual(images['walk_00.png'].tobytes(),other.tobytes())

    def test_idle_overlay_extremes_and_input_unchanged(self):
        f=synthetic(static=True)[0];a=np.dstack((f,np.any(f,axis=2).astype(np.uint8)*255))
        im=Image.fromarray(a);before=im.tobytes()
        out=render_idle_guide(idle_sheet(band_row(),24,12),im)
        self.assertEqual(im.tobytes(),before);self.assertNotEqual(out.tobytes(),before)
        data=np.array(out)
        for color in SOLE_COLORS:self.assertTrue(np.any(np.all(data==color,axis=2)))
        with self.assertRaises(ValueError):render_walk_guide(walk_sheet(numeric_walk()),800)
