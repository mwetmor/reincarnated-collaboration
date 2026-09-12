"""T1c: synthetic motion questions, annotation lineage and calibration controls."""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest

from oracle.dope_sheet import idle_sheet, walk_sheet
from test_oracle_walk import synthetic_annotation
from transcribe.motion_questions import (questions_from_walk_sheet,
    questions_from_idle_sheet, questions_and_truth_from_annotation, validate_answers)
from compare.calibrate_motion_transcriber import score, main, DEFAULT_OUT

ROOT = Path(__file__).resolve().parents[1]


def synthetic_walk_sheet():
    phases = []
    for i in range(12):
        phases.append(dict(frame=i, phase=['CONTACT', 'DOWN', 'PASSING', 'UP', 'UP', 'UP'][i % 6],
                           planted=dict(near=i < 6, far=i >= 6)))
    return walk_sheet(dict(committed=False, phase_table=phases, bands={
        'W1': {'floor': .015, 'ceiling': .05}, 'parameters': {'k_vert': 2},
        'W2': {'min': [{'frame': 1}, {'frame': 7}], 'max': [{'frame': 2}, {'frame': 8}]}}))


def synthetic_idle_sheet():
    return idle_sheet(dict(committed=False, breath_period_s=None,
        breath_amplitude_H=dict(target=.03, ceiling=.05), head_sway_H=dict(target=.01, ceiling=.02),
        lock_regions=['feet', 'staff_tip'], motion_regions=['head', 'shoulders_chest']), 8, 12)


def annotated():
    ann = synthetic_annotation()
    ann['stride_notes']['passing_frames'] = [2, 8]
    return ann


class Tests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def assert_question_contract(self, question_set, count):
        questions = question_set['questions']
        self.assertEqual(len(questions), count)
        schema = question_set['answer_schema']
        self.assertEqual(schema['type'], 'object')
        self.assertIs(schema['additionalProperties'], False)
        self.assertEqual(set(schema['required']), {q['id'] for q in questions})
        self.assertEqual(set(schema['properties']), set(schema['required']))
        self.assertTrue(all(v == {'type': 'boolean'} for v in schema['properties'].values()))
        controls = [q for q in questions if q['declared_absent_control']]
        self.assertEqual(len(controls), 1)
        self.assertIs(controls[0]['expected'], False)
        self.assertTrue(all(q['expected'] is None for q in questions if not q['declared_absent_control']))
        seen = set()
        for q in questions:
            self.assertLessEqual(set(q['depends_on']), seen)
            self.assertLessEqual(set(q['parts']), set(question_set['closed_parts']))
            self.assertTrue(all(0 <= f < question_set['n_frames'] for f in q['frames']))
            seen.add(q['id'])
        validate_answers(question_set, {q['id']: False for q in questions})
        encoded = json.dumps(question_set, allow_nan=False)
        self.assertNotIn('head_height_H', encoded)
        self.assertNotIn('product_H2', encoded)
        self.assertNotIn('annotation_confidence', encoded)

    def test_walk_sheet_counts_schema_and_dependencies(self):
        sheet = synthetic_walk_sheet(); before = copy.deepcopy(sheet)
        q = questions_from_walk_sheet(sheet)
        self.assertEqual(sheet, before)
        self.assert_question_contract(q, 54)
        counts = {}
        for item in q['questions']:
            counts[item['predicate']] = counts.get(item['predicate'], 0)+1
        self.assertEqual(counts, dict(planted=24, arm_opposes_leg=24, lead_alternates=2,
                                     head_higher_at_passing=2, sampled_pose_continuity=1, both_feet_airborne=1))
        self.assertEqual(next(x for x in q['questions'] if x['predicate']=='sampled_pose_continuity')['frames'], [11, 0])

    def test_idle_sheet_counts_control_and_conflicts(self):
        sheet = synthetic_idle_sheet(); before = copy.deepcopy(sheet)
        q = questions_from_idle_sheet(sheet)
        self.assertEqual(sheet, before)
        self.assert_question_contract(q, 6)
        self.assertEqual(q['questions'][-2]['frames'], [7, 0])
        sheet['conflicts'] = ['head is LOCK but has nonzero amplitude']
        sheet['lock_regions'].remove('staff_tip')
        other = questions_from_idle_sheet(sheet)
        self.assertIn(sheet['conflicts'][0], other['notes'])
        self.assertTrue(any('unspecified' in s for s in other['notes']))

    def test_closed_answers_reject_missing_extra_and_non_boolean(self):
        q, t = questions_and_truth_from_annotation(annotated())
        valid = t['answers']; first = next(iter(valid))
        for bad in [{}, {**valid, 'coordinates': [1, 2]}, {**valid, first: 1},
                    {**valid, first: 'YES'}, {**valid, first: None},
                    {**valid, first: {'present': True}}, list(valid)]:
            with self.subTest(bad_type=type(bad)):
                with self.assertRaises(ValueError): validate_answers(q, bad)

    def test_annotation_truth_is_literal_not_designed_opposition(self):
        ann = annotated(); q, t = questions_and_truth_from_annotation(ann)
        self.assert_question_contract(q, 54)
        # Synthetic annotation's arms and soles share signs about the hip.
        for i, f in enumerate(ann['frames']):
            for side in ('near', 'far'):
                self.assertEqual(t['answers'][f'walk.f{i+1:02}.{side}.planted'], f['planted_'+side])
                self.assertIs(t['answers'][f'walk.f{i+1:02}.{side}.arm_opposes_leg'], False)
        self.assertFalse(t['answers']['walk.f01_f03.head_higher'])
        self.assertFalse(t['answers']['walk.f07_f09.head_higher'])
        self.assertFalse(t['answers']['walk.f01_f07.lead_alternates'])
        for f in ann['frames']:
            for side in ('near', 'far'):
                f[side+'_wrist'][0] = 2*f['hip'][0]-f[side+'_sole'][0]
        _, opposed = questions_and_truth_from_annotation(ann)
        self.assertTrue(all(v for k, v in opposed['answers'].items() if k.endswith('arm_opposes_leg')))

    def test_annotation_coordinate_translation_and_scale_invariance(self):
        ann = annotated(); q, t = questions_and_truth_from_annotation(ann)
        ann['subject_height_px'] *= 2
        for i, f in enumerate(ann['frames']):
            dx, dy = 27*i, [0, 31, -14, 8][i % 4]
            f['ground_y'] = 2*f['ground_y']+dy
            for key in ('head_top', 'chin', 'hip', 'near_sole', 'far_sole', 'near_wrist', 'far_wrist'):
                f[key] = [2*f[key][0]+dx, 2*f[key][1]+dy]
        moved_q, moved_t = questions_and_truth_from_annotation(ann)
        self.assertEqual(q, moved_q)
        self.assertEqual(t['answers'], moved_t['answers'])

    def test_phase_notes_not_repaired_and_confidence_retained(self):
        ann = annotated(); ann['stride_notes']['contact_frames'] = [5, 11]
        ann['frames'][0]['confidence']['far_wrist'] = .1
        q, t = questions_and_truth_from_annotation(ann)
        self.assertEqual(len(t['answers']), 54)
        self.assertEqual(t['annotation_confidence'][0]['confidence']['far_wrist'], .1)
        self.assertEqual(len(t['notes']), 1)
        self.assertIn('walk.f12_f03.head_higher', t['answers'])
        self.assertTrue(t['answers']['walk.f01.near.planted'])
        self.assertEqual(q['notes'], t['notes'])

    def test_continuity_truth_distinguishes_broken_wrap(self):
        ann = annotated()
        # Large monotonic head-height changes make wrap larger than every step.
        for i, f in enumerate(ann['frames']):
            f['head_top'][1] -= 1000*i
        _, t = questions_and_truth_from_annotation(ann)
        self.assertFalse(t['answers']['walk.f12_f01.continuous'])
        # A periodic sampled trajectory has a wrap step represented internally.
        for i, f in enumerate(ann['frames']):
            f['head_top'][1] = f['ground_y']-500-10000*math.sin(2*math.pi*i/12)
        _, t = questions_and_truth_from_annotation(ann)
        self.assertTrue(t['answers']['walk.f12_f01.continuous'])

    def test_invalid_sources_rejected(self):
        for change in [lambda a: a['frames'].pop(),
                       lambda a: a.update(subject_height_px=0),
                       lambda a: a['frames'][0].update(planted_near=1),
                       lambda a: a['frames'][0].update(head_top=[0, float('nan')]),
                       lambda a: a['frames'][0].update(frame=1),
                       lambda a: a['stride_notes'].update(contact_frames=[0, 0])]:
            ann = annotated(); change(ann)
            with self.assertRaises(ValueError): questions_and_truth_from_annotation(ann)
        sheet = synthetic_idle_sheet(); sheet['lock_regions'] = []
        with self.assertRaises(ValueError): questions_from_idle_sheet(sheet)
        sheet = synthetic_walk_sheet(); sheet['frames'][0]['phase'] = 'DOWN'
        with self.assertRaises(ValueError): questions_from_walk_sheet(sheet)

    def test_perfect_calibration_and_fixed_bars(self):
        q, t = questions_and_truth_from_annotation(annotated())
        result = score(q, t, [t['answers']]); m = result['metrics']
        for k in ('accuracy', 'presence_precision', 'presence_recall', 'control_pass_rate'):
            self.assertEqual(m['aggregate'][k], 1.)
        self.assertEqual(m['thresholds'], dict(accuracy=.85, control_pass_rate=1.))
        self.assertEqual(m['aggregate']['counts']['total'], 54)
        self.assertTrue(all(v['accuracy']==1 for v in m['per_question'].values()))
        self.assertIsNone(result['passed'])
        json.dumps(result, allow_nan=False)

    def test_control_failed_answers_remain_in_denominator(self):
        q, t = questions_and_truth_from_annotation(annotated())
        bad = dict(t['answers']); control = t['controls'][0]; bad[control] = True
        m = score(q, t, [bad])['metrics']
        self.assertEqual(m['aggregate']['accuracy'], 53/54)
        self.assertEqual(m['aggregate']['control_pass_rate'], 0.)
        self.assertEqual(m['aggregate']['counts']['fp'], 1)
        self.assertEqual(m['per_question'][control]['accuracy'], 0.)
        # An unrelated YES cannot hide the control; two bursts give 1/2 controls.
        mixed = score(q, t, [t['answers'], bad])['metrics']
        self.assertEqual(mixed['aggregate']['control_pass_rate'], .5)
        self.assertEqual(mixed['aggregate']['accuracy'], 107/108)

    def test_presence_metrics_exact_counts(self):
        q, t = questions_and_truth_from_annotation(annotated())
        bad = dict(t['answers'])
        yes = next(k for k, v in bad.items() if v)
        no = next(k for k, v in bad.items() if not v and k not in t['controls'])
        n_yes = sum(bad.values()); bad[yes] = False; bad[no] = True
        m = score(q, t, [bad])['metrics']['aggregate']
        self.assertEqual(m['presence_precision'], (n_yes-1)/n_yes)
        self.assertEqual(m['presence_recall'], (n_yes-1)/n_yes)
        self.assertEqual(m['accuracy'], 52/54)
        self.assertEqual(m['control_pass_rate'], 1.)

    def test_empty_and_zero_denominators_are_not_perfect(self):
        q, t = questions_and_truth_from_annotation(annotated())
        m = score(q, t, [])['metrics']
        self.assertEqual(m['n_bursts'], 0)
        self.assertIsNone(m['aggregate']['accuracy'])
        self.assertIsNone(m['aggregate']['control_pass_rate'])
        self.assertIsNone(m['aggregate']['presence_precision'])
        all_no = {k: False for k in t['answers']}
        m = score(q, t, [all_no])['metrics']['aggregate']
        self.assertIsNone(m['presence_precision'])
        self.assertEqual(m['presence_recall'], 0.)

    def test_bad_controls_and_incomplete_bursts_rejected(self):
        q, t = questions_and_truth_from_annotation(annotated())
        for bad in [{**t, 'controls': []}, {**t, 'controls': ['unknown']},
                    {**t, 'answers': {**t['answers'], t['controls'][0]: True}}]:
            with self.assertRaises(ValueError): score(q, bad, [t['answers']])
        with self.assertRaises(ValueError): score(q, t, [{}])
        with self.assertRaises(ValueError): score(q, t, t['answers'])

    def test_cli_writes_summary_and_rejects_duplicate_keys(self):
        q, t = questions_and_truth_from_annotation(annotated())
        for name, data in [('q.json', q), ('t.json', t), ('a.json', t['answers'])]:
            (self.base/name).write_text(json.dumps(data))
        args = ['--questions', str(self.base/'q.json'), '--truth', str(self.base/'t.json'),
                '--answers', str(self.base/'a.json'), '--out', str(self.base/'summary.json')]
        main(args)
        output = json.loads((self.base/'summary.json').read_text())
        self.assertEqual(output['metrics']['aggregate']['accuracy'], 1.)
        self.assertEqual(DEFAULT_OUT, ROOT/'runs/C-1/x0m/calibration_summary.json')
        (self.base/'a.json').write_text('{"duplicate":true,"duplicate":false}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'): main(args)


if __name__ == '__main__':
    unittest.main()
