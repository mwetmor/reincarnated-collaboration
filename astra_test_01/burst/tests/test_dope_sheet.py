import json
import unittest
import numpy as np
from oracle.dope_sheet import idle_sheet,walk_sheet
from test_idle_intent import band_row
from test_gait_intent import walk_row


def numeric_walk():
    row=walk_row();seq=[]
    for i in range(12):
        dy=.015*np.cos(2*np.pi*(i-1)/6)
        seq.append(dict(H=200.,head_top_y=100+dy*200,torso_cx=100.,ground_line_y=300.,
            foot_L_x=100+30*np.cos(2*np.pi*i/12),foot_R_x=100-30*np.cos(2*np.pi*i/12),
            foot_L_y=300. if i<6 else 292.,foot_R_y=292. if i<6 else 300.))
    row['curves']={'landmarks':seq};row['summary']={'H_median':200.}
    row['bands']['W1']['floor']=.015;row['bands']['parameters']={'k_vert':2.}
    row['bands']['W5']={'L':{'target':.12},'R':{'target':.04}}
    return row


class Tests(unittest.TestCase):
    def test_idle_roundtrip_target_sine(self):
        row=band_row();row['breath_period_s']=2.
        sheet=json.loads(json.dumps(idle_sheet(row,24,12)))
        for i,f in enumerate(sheet['frames']):
            self.assertAlmostEqual(f['head_dy_H'],.01*np.sin(2*np.pi*i/24))
            self.assertAlmostEqual(f['chest_dw_H'],.03*np.sin(2*np.pi*i/24))
        self.assertEqual(sheet['lock_regions'],row['lock_regions'])
        self.assertIn('frame 24',sheet['prompt_text'])
        self.assertEqual(idle_sheet(band_row(),8,12)['period_s'],8/12)
        self.assertEqual(idle_sheet(band_row(),16,8)['period_s'],2.)

    def test_walk_roundtrip_source_positions_and_amplitude(self):
        row=numeric_walk();sheet=json.loads(json.dumps(walk_sheet(row)))
        self.assertAlmostEqual(np.ptp([f['head_height_H'] for f in sheet['frames']]),.03)
        source=row['curves']['landmarks'];ys=np.array([-d['head_top_y']/200 for d in source])
        for i,f in enumerate(sheet['frames']):
            self.assertEqual(f['phase'],row['phase_table'][i]['phase'])
            self.assertAlmostEqual(f['head_height_H'],1+(ys[i]-ys.mean()))
            self.assertAlmostEqual(f['soles']['L']['x_H'],(source[i]['foot_L_x']-100)/200)
            self.assertAlmostEqual(f['soles']['R']['height_H'],(300-source[i]['foot_R_y'])/200)
        self.assertAlmostEqual(np.ptp([f['arm_x_H']['L'] for f in sheet['frames']]),.12)

    def test_invalid_and_conflicts_not_repaired(self):
        with self.assertRaises(ValueError):idle_sheet(band_row(),0,12)
        with self.assertRaises(ValueError):walk_sheet(numeric_walk(),8)
        row=numeric_walk();row['phase_table'][0]['phase']=None
        with self.assertRaises(ValueError):walk_sheet(row)
        row=band_row();row['lock_regions'].append('head')
        self.assertTrue(idle_sheet(row,8,12)['conflicts'])
        row=numeric_walk();row['bands']['W1']['ceiling']=.02
        sheet=walk_sheet(row);self.assertTrue(sheet['conflicts']);self.assertEqual(sheet['head_amplitude_H'],.03)
