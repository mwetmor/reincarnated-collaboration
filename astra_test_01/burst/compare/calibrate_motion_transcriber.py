"""X0-M closed motion calibration: measurements for conductor adjudication.

CLI: --questions questions_plate13.json --truth truth_plate13.json
     --answers inventory1.json [inventory2.json ...] [--out ...]
Defaults to runs/C-1/x0m/calibration_summary.json. No model or image calls.
"""
import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from transcribe.motion_questions import validate_answers

ACCURACY_MIN = .85
CONTROL_PASS_RATE_MIN = 1.
DEFAULT_OUT = Path(__file__).resolve().parents[1]/'runs/C-1/x0m/calibration_summary.json'


def score(question_set, truth, answers, *, subject='plate13_lateral'):
    expected = truth['answers']
    validate_answers(question_set, expected)
    controls = [q['id'] for q in question_set['questions'] if q['declared_absent_control']]
    if len(controls) != 1 or truth.get('controls') != controls or any(expected[k] for k in controls):
        raise ValueError('Exactly one matching, false DECLARED-ABSENT control required')
    if any(q.get('expected') is not False for q in question_set['questions'] if q['declared_absent_control']):
        raise ValueError('Question control must explicitly declare false')
    if isinstance(answers, dict):
        raise ValueError('Supply a list of independent answer objects')
    answers = list(answers)
    for answer in answers:
        validate_answers(question_set, answer)
    per_question = {k: dict(truth=v, correct=0, total=len(answers), accuracy=None,
                            yes_count=0, no_count=0) for k, v in expected.items()}
    totals = dict(tp=0, fp=0, fn=0, tn=0, correct=0, total=0, controls_correct=0, controls_total=0)

    def metrics(t):
        def ratio(a, b):
            return a/b if b else None
        return dict(accuracy=ratio(t['correct'], t['total']),
                    presence_precision=ratio(t['tp'], t['tp']+t['fp']),
                    presence_recall=ratio(t['tp'], t['tp']+t['fn']),
                    control_pass_rate=ratio(t['controls_correct'], t['controls_total']),
                    counts=dict(t))

    bursts = []
    for i, answer in enumerate(answers):
        counts = dict.fromkeys(totals, 0)
        for key, actual in answer.items():
            target = expected[key]
            counts['tp' if target and actual else 'fn' if target else 'fp' if actual else 'tn'] += 1
            counts['correct'] += int(actual == target)
            counts['total'] += 1
            if key in controls:
                counts['controls_correct'] += int(not actual)
                counts['controls_total'] += 1
            row = per_question[key]
            row['correct'] += int(actual == target)
            row['yes_count' if actual else 'no_count'] += 1
        bursts.append(dict(index=i, **metrics(counts)))
        for key in totals:
            totals[key] += counts[key]
    for row in per_question.values():
        row['accuracy'] = row['correct']/len(answers) if answers else None
    aggregate = metrics(totals)
    # The fixed bars are reported, not retuned; adjudication belongs to conductor.
    results = [dict(id='X0-M.'+key, subject=subject, passed=None,
                    value=aggregate[key], threshold=limit, op='>=', unit='fraction', evidence=[],
                    notes='Measurement only; conductor adjudicates.' if answers else 'N=0: no transcriber answers.')
               for key, limit in [('accuracy', ACCURACY_MIN), ('control_pass_rate', CONTROL_PASS_RATE_MIN)]]
    return dict(id='X0-M', subject=subject, passed=None, value=aggregate['accuracy'],
                threshold=ACCURACY_MIN, op='>=', unit='fraction', evidence=[],
                notes='Measurement only; conductor adjudicates.' if answers else 'N=0: no transcriber answers.',
                metrics=dict(n_bursts=len(answers), n_questions=len(expected), controls=controls,
                             aggregate=aggregate, per_burst=bursts, per_question=per_question,
                             thresholds=dict(accuracy=ACCURACY_MIN, control_pass_rate=CONTROL_PASS_RATE_MIN),
                             results=results, precision_recall_policy='YES is presence, NO is absence; controls included. '
                             'A zero denominator is null, never perfect. Every question is scored; dependencies do not mask errors.'))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--questions', required=True)
    parser.add_argument('--truth', required=True)
    parser.add_argument('--answers', nargs='+', required=True)
    parser.add_argument('--out', default=str(DEFAULT_OUT))
    args = parser.parse_args(argv)
    def read(path):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('Duplicate JSON key: '+key)
                result[key] = value
            return result
        return json.loads(Path(path).read_text(), object_pairs_hook=unique)
    result = score(read(args.questions), read(args.truth), [read(p) for p in args.answers])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    return result


if __name__ == '__main__':
    main()
