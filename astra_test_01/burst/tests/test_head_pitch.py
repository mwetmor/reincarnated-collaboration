import json
import unittest
import numpy as np
from gates.head_pitch import evaluate, HEAD_DOWN_DELTA, _lab


def head_frame(shift=0,face=True):
    a=np.zeros((200,160,4),np.uint8)
    a[20:160,50:110]=(20,20,20,255)
    a[40:160,50:110]=(35,55,95,255)
    if face: a[25+shift:30+shift,70:95]=(205,145,100,255)
    return a


class Tests(unittest.TestCase):
    def test_lowered_twenty_percent_and_raised(self):
        rest=head_frame();r=evaluate([head_frame(4),head_frame(-3)],rest,fps=1)
        down,up=r['value']['frames']
        self.assertAlmostEqual(down['delta'],.20)
        self.assertTrue(down['head_down']);self.assertFalse(up['head_down'])
        self.assertTrue(r['value']['first_second_head_down']);self.assertIsNone(r['passed'])
        self.assertEqual(r['threshold'],HEAD_DOWN_DELTA);json.dumps(r,allow_nan=False)
    def test_back_view_and_absent_rest_are_null(self):
        r=evaluate([head_frame(face=False)],head_frame(),fps=24)
        self.assertIsNone(r['value']['frames'][0]['delta'])
        self.assertEqual(r['value']['frames'][0]['reason'],'face_not_visible')
        r=evaluate([head_frame()],head_frame(face=False))
        self.assertIsNone(r['value']['frames'][0]['head_down'])
    def test_translation_invariance_and_timing_boundary(self):
        a=head_frame(4);b=np.roll(a,7,axis=0)
        r=evaluate([a,b,head_frame(-3)],head_frame(),times=[0,.999,1.])
        self.assertAlmostEqual(r['value']['frames'][0]['delta'],r['value']['frames'][1]['delta'])
        self.assertEqual(r['value']['first_second_evaluable_frames'],2)
        self.assertTrue(r['value']['first_second_head_down'])
        self.assertIsNone(evaluate([a],head_frame())['value']['first_second_head_down'])
    def test_validation_and_lab(self):
        with self.assertRaises(ValueError): evaluate([],head_frame())
        with self.assertRaises(ValueError): evaluate([head_frame()],head_frame(),fps=0)
        with self.assertRaises(ValueError): evaluate([head_frame()],head_frame(),times=[0,1])
        np.testing.assert_allclose(_lab(np.array([255,255,255])),[100,0,0],atol=.001)
        np.testing.assert_allclose(_lab(np.array([0,0,0])),[0,0,0],atol=.001)
