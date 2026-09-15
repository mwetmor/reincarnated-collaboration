"""Measured synthetic traces and known-bad event inputs; no invented bands."""
import unittest
import numpy as np
from oracle.event_gates import activation_expiry, aura_attachment, evaluate, field_boundary, interval_cv


class EventGateTests(unittest.TestCase):
    def test_twelve_frame_late_expiry(self):
        trace = [dict(frame=f,active=10 <= f < 72) for f in range(80)]
        events = [dict(event='contact',frame=10),dict(event='expire',frame=60)]
        rows = activation_expiry(trace,events)
        self.assertEqual(rows[0]['value']['lag_frames'],0)
        self.assertEqual(rows[1]['value']['lag_frames'],12)
        self.assertEqual(rows[1]['value']['lag_ms'],200)
        self.assertTrue(all(r['passed'] is None for r in rows))

    def test_early_activation_negative_lag_and_censored_expiry(self):
        r = activation_expiry([dict(frame=0,active=False),dict(frame=1,active=True)],
                              [dict(event='contact',frame=3),dict(event='expire',frame=60)])
        self.assertEqual(r[0]['value']['lag_frames'],-2)
        self.assertIsNone(r[1]['value']['lag_frames'])

    def test_missing_and_ambiguous_events_not_zero(self):
        trace = [dict(frame=0,active=True),dict(frame=1,active=False)]
        for events in [[],[dict(event='contact',frame=0)]*2]:
            r = activation_expiry(trace,events)
            self.assertIsNone(r[0]['value']['lag_frames'])
            self.assertIsNone(r[1]['value']['lag_frames'])

    def test_field_radius_and_wrong_radius(self):
        points = [[10,0],[0,10],[-10,0],[0,-10]]
        self.assertEqual(field_boundary(points,(0,0),10)['value']['max_abs_error_px'],0)
        self.assertEqual(field_boundary(points,(0,0),8)['value']['max_abs_error_px'],2)
        self.assertIsNone(field_boundary([],(0,0),8)['value']['max_abs_error_px'])

    def test_aura_follows_moving_socket_and_drift(self):
        socket = np.array([[0,0],[10,4],[20,9]],float)
        aura = socket+[0,-5]
        self.assertEqual(aura_attachment(aura,socket,(0,-5))['value']['max_px'],0)
        aura[-1] += [3,4]
        self.assertEqual(aura_attachment(aura,socket,(0,-5))['value']['max_px'],5)
        self.assertIsNone(aura_attachment([],[])['value']['max_px'])

    def test_interval_cv_population_and_insufficient_samples(self):
        self.assertEqual(interval_cv([0,10,20,30])['value']['cv'],0)
        self.assertAlmostEqual(interval_cv([0,10,30])['value']['cv'],1/3)
        self.assertIsNone(interval_cv([0,10])['value']['cv'])

    def test_cast_clocks_are_not_mixed(self):
        trace = [dict(frame=f,active=f==1,cast_id=c) for c in ('a','b') for f in range(3)]
        events = [dict(frame=f,event=e,cast_id=c) for c in ('a','b')
                  for f,e in [(1,'contact'),(2,'expire')]]
        rows = evaluate(trace,dict(events=events))
        self.assertEqual(len(rows),8)
        self.assertEqual([r['value']['lag_frames'] for r in rows if r['id']=='expiry_lag'],[0,0])

    def test_known_bad_clock_and_shapes(self):
        for frames in [[1,1],[2,1],[-1,0],[0,True]]:
            with self.assertRaises(ValueError): interval_cv(frames)
        with self.assertRaises(ValueError): field_boundary([[float('nan'),0]],(0,0),10)
        with self.assertRaises(ValueError): field_boundary([[0,0]],(0,0),0)
        with self.assertRaises(ValueError): aura_attachment([[0,0]],[])
        with self.assertRaises(ValueError): activation_expiry([dict(frame=0,active=1)],[])
        with self.assertRaises(ValueError): activation_expiry([dict(frame=1,active=True)]*2,[])

    def test_native_g1_effect_id_and_age_frames(self):
        trace = [dict(frame=f,active=2<=f<72,effect_id=7) for f in range(75)]
        events = [dict(event='release',age_frames=0,effect_id=7),
                  dict(event='contact',age_frames=2,effect_id=7),
                  dict(event='expire',age_frames=60,effect_id=7)]
        rows = evaluate(trace,dict(events=events))
        self.assertEqual(rows[1]['subject'],'cast/7')
        self.assertEqual(rows[1]['value']['lag_frames'],12)
        bad = [dict(events[1],frame=3)]
        with self.assertRaises(ValueError): evaluate(trace,bad)


if __name__ == '__main__': unittest.main()
