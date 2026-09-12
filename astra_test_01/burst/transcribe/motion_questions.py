"""Closed, boolean motion observations; question files contain no measured truth.

Frame indices in JSON are zero-based; displayed frame numbers are one-based.
Dependencies describe evidence links, never permission to skip an answer.
Annotation phase notes and planted flags are independent evidence: neither is
silently repaired. Continuity is a sampled pose-step proxy, not an image seam
gate, a velocity test, or an assertion that a source plate is a perfect loop.
"""
import math
import statistics


VERSION = 'X0-M.motion.v1'


def _finite(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError('Finite numeric measurement required')
    return value


def _frames(data, kind):
    frames = data.get('frames')
    n = data.get('n_frames', len(frames) if isinstance(frames, list) else 0)
    if data.get('kind') != kind or type(n) is not int or n < 2:
        raise ValueError('Expected a nonempty animation sheet')
    if not isinstance(frames, list) or len(frames) != n:
        raise ValueError('Frame count does not match sheet')
    if any(type(f.get('frame')) is not int or f['frame'] != i for i, f in enumerate(frames)):
        raise ValueError('Frames must be ordered, contiguous and zero-based')
    return frames


def answer_schema(questions):
    ids = [q['id'] for q in questions]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Nonempty unique closed question IDs required')
    return dict(type='object', properties={key: {'type': 'boolean'} for key in ids},
                required=ids, additionalProperties=False)


def validate_answers(question_set, answers):
    """Strict boolean-only equivalent of the emitted answer JSON schema."""
    ids = answer_schema(question_set['questions'])['required']
    if not isinstance(answers, dict) or set(answers) != set(ids):
        raise ValueError('Answer every closed question exactly once; no extra fields')
    if any(type(value) is not bool for value in answers.values()):
        raise ValueError('Answers must be JSON booleans: true=YES, false=NO')


def _question(key, predicate, frames, parts, text, dependencies=(), control=False):
    return dict(id=key, predicate=predicate, frames=frames, parts=parts,
                question=text, depends_on=list(dependencies),
                declared_absent_control=control, expected=False if control else None)


def _set(kind, frames, parts, questions, notes=()):
    ids = {q['id'] for q in questions}
    if sum(q['declared_absent_control'] for q in questions) != 1:
        raise ValueError('Exactly one DECLARED-ABSENT control required')
    for q in questions:
        if not set(q['depends_on']) <= ids or q['id'] in q['depends_on']:
            raise ValueError('Invalid evidence dependency')
    return dict(version=VERSION, kind=kind, n_frames=len(frames),
                frame_index_base=0, displayed_frame_index_base=1, closed_parts=parts,
                instructions='Answer every question using only JSON true (YES) or false (NO). '
                'Dependencies link evidence; answer all questions even when a dependency is NO. '
                'Do not return coordinates, explanations, new labels, or additional keys. '
                'Near/far identify persistent sides, not left/right positions on screen.',
                notes=list(notes), questions=questions, answer_schema=answer_schema(questions))


def _sides(frames):
    sides = set(frames[0]['soles'])
    if sides == {'near', 'far'}:
        result = ['near', 'far']
    elif sides == {'L', 'R'}:
        result = ['L', 'R']
    else:
        raise ValueError('Soles must use near/far or anatomical L/R')
    for frame in frames:
        if set(frame['soles']) != sides or set(frame['arm_x_H']) != sides:
            raise ValueError('Side identities must remain fixed')
        _finite(frame['head_height_H'])
        for side in result:
            sole = frame['soles'][side]
            if type(sole['planted']) is not bool:
                raise ValueError('Explicit boolean planted flags required')
            for value in (sole['x_H'], sole['height_H'], frame['arm_x_H'][side]):
                _finite(value)
    return result


def questions_from_walk_sheet(sheet):
    frames = _frames(sheet, 'walk')
    if len(frames) != 12:
        raise ValueError('The registered walk question set requires 12 frames')
    sides = _sides(frames)
    contacts = [f['frame'] for f in frames if f['phase'] == 'CONTACT']
    passing = [f['frame'] for f in frames if f['phase'] == 'PASSING']
    if len(contacts) != 2 or len(passing) != 2:
        raise ValueError('Two CONTACT and two PASSING frames required')
    questions = []
    for f in frames:
        i = f['frame']
        for side in sides:
            questions.append(_question(f'walk.f{i+1:02}.{side}.planted', 'planted', [i],
                [side+'_foot'], f'Frame {i+1}: is the {side} foot planted on the ground?'))
            questions.append(_question(f'walk.f{i+1:02}.{side}.arm_opposes_leg',
                'arm_opposes_leg', [i], [side+'_arm', side+'_foot'],
                f'Frame {i+1}: are the {side} wrist and {side} sole on opposite horizontal '
                'sides of the hip? A wrist or sole aligned with the hip is NO.'))
    for j, a in enumerate(contacts):
        b = contacts[(j+1) % len(contacts)]
        questions.append(_question(f'walk.f{a+1:02}_f{b+1:02}.lead_alternates',
            'lead_alternates', [a, b], [s+'_foot' for s in sides],
            f'Between CONTACT frames {a+1} and {b+1}, does the leading foot switch identity? '
            'Compare the horizontal order of the two soles; a tie is NO.',
            [f'walk.f{i+1:02}.{s}.planted' for i in (a, b) for s in sides]))
    for p in passing:
        c = min(contacts, key=lambda c: (p-c) % len(frames))
        questions.append(_question(f'walk.f{c+1:02}_f{p+1:02}.head_higher',
            'head_higher_at_passing', [c, p], ['head'],
            f'Is the head top higher above the local ground in PASSING frame {p+1} '
            f'than in preceding CONTACT frame {c+1} (wrapping the sequence when needed)?'))
    questions.append(_question('walk.f12_f01.continuous', 'sampled_pose_continuity',
        [11, 0], ['head']+[s+'_'+part for s in sides for part in ('foot', 'arm')],
        'Is frame 12 to frame 1 continuous in sampled pose: is its average change in head '
        'height, hip-relative sole positions/sole heights and hip-relative wrist positions '
        'no greater than the largest such change between adjacent frames inside the clip? '
        'Ignore whole-body translation. This is a pose-step proxy, not appearance continuity.'))
    grounded = next((f['frame'] for f in frames if any(
        f['soles'][s]['planted'] for s in sides)), None)
    if grounded is None:
        raise ValueError('No grounded frame available for the declared-absent control')
    questions.append(_question(f'walk.f{grounded+1:02}.airborne_control', 'both_feet_airborne',
        [grounded], [s+'_foot' for s in sides],
        f'Frame {grounded+1}: are both feet simultaneously unplanted, clear of the ground?',
        control=True))
    return _set('walk', frames, ['head']+[s+'_'+p for s in sides for p in ('foot', 'arm')],
                questions, sheet.get('conflicts', [])+sheet.get('question_notes', []))


def questions_from_idle_sheet(sheet):
    frames = _frames(sheet, 'idle')
    # The foot control must follow an explicit non-conflicting LOCK declaration.
    if 'feet' not in sheet.get('lock_regions', []) or 'feet' in sheet.get('motion_regions', []):
        raise ValueError('Idle control requires feet LOCK and not MOTION')
    n = len(frames)
    full = list(range(n))
    questions = [
        _question('idle.feet_move', 'feet_move', full, ['feet'],
                  'Do the feet visibly change position at any point in the cycle?'),
        _question('idle.chest_breathes', 'chest_breathes', full, ['chest'],
                  'Does the chest expand and contract during the cycle (the rise and fall of breathing)?'),
        _question('idle.head_drifts', 'head_drifts', full, ['head'],
                  'Does the head visibly change position during the cycle, including bob or sway?'),
        _question('idle.staff_tip_drifts', 'staff_tip_drifts', full, ['staff_tip'],
                  'Is there a visible staff tip that changes position during the cycle? '
                  'Answer NO if no staff tip is present.'),
        _question(f'idle.f{n:02}_f01.continuous', 'sampled_pose_continuity', [n-1, 0],
                  ['feet', 'chest', 'head', 'staff_tip'],
                  f'Is frame {n} to frame 1 continuous in sampled pose: are changes in the '
                  'visible listed parts no larger than the largest changes between adjacent '
                  'frames inside the clip? Ignore absent parts.'),
        _question('idle.airborne_control', 'both_feet_airborne', full, ['feet'],
                  'Do both feet leave the ground together at any point in the cycle?', control=True)]
    notes = list(sheet.get('conflicts', []))
    if 'staff_tip' not in sheet.get('lock_regions', [])+sheet.get('motion_regions', []):
        notes.append('Staff-tip presence/motion is unspecified by the sheet; observe it, do not infer truth from arm LOCKs.')
    notes.append('Feet LOCK is the declared grounded idle control; LOCK permits subthreshold displacement, not a jump.')
    return _set('idle', frames, ['feet', 'chest', 'head', 'staff_tip'], questions, notes)


def _pose(frame, sides):
    values = [frame['head_height_H']]
    for side in sides:
        values += [frame['soles'][side]['x_H'], frame['soles'][side]['height_H'],
                   frame['arm_x_H'][side]]
    return values


def _step(a, b):
    return statistics.mean(abs(x-y) for x, y in zip(a, b))


def _walk_truth(sheet, question_set):
    frames = sheet['frames']
    sides = _sides(frames)
    poses = [_pose(f, sides) for f in frames]
    internal = [_step(a, b) for a, b in zip(poses, poses[1:])]
    seam = _step(poses[-1], poses[0])
    answers, evidence = {}, {}
    for q in question_set['questions']:
        a = frames[q['frames'][0]]
        predicate = q['predicate']
        detail = {'frames': q['frames'], 'predicate': predicate}
        if predicate == 'planted':
            side = q['parts'][0].removesuffix('_foot')
            value = a['soles'][side]['planted']
            detail['source'] = 'explicit planted flag'
        elif predicate == 'arm_opposes_leg':
            side = q['parts'][0].removesuffix('_arm')
            product = a['arm_x_H'][side]*a['soles'][side]['x_H']
            value = product < 0
            detail.update(source='same-side hip-relative wrist_x times sole_x < 0', product_H2=product)
        elif predicate == 'lead_alternates':
            b = frames[q['frames'][1]]
            differences = [f['soles'][sides[0]]['x_H']-f['soles'][sides[1]]['x_H'] for f in (a, b)]
            value = differences[0]*differences[1] < 0
            detail.update(source='strict sole-order reversal between annotated contacts', differences_H=differences)
        elif predicate == 'head_higher_at_passing':
            b = frames[q['frames'][1]]
            delta = b['head_height_H']-a['head_height_H']
            value = delta > 0
            detail.update(source='ground-relative head-top height; annotated phase notes', delta_H=delta)
        elif predicate == 'sampled_pose_continuity':
            value = seam <= max(internal)+1e-12
            detail.update(source='sampled pose-step proxy, not G6/G6b/G6c',
                          seam_mean_abs_H=seam, internal_max_mean_abs_H=max(internal),
                          internal_mean_abs_H=internal, numerical_tolerance_H=1e-12)
        elif predicate == 'both_feet_airborne':
            value = not any(a['soles'][s]['planted'] for s in sides)
            detail['source'] = 'both explicit planted flags false'
        else:
            raise ValueError('Unknown closed predicate')
        answers[q['id']] = bool(value)
        evidence[q['id']] = detail
    validate_answers(question_set, answers)
    return answers, evidence


def questions_and_truth_from_annotation(annotation):
    """Derive plate questions/truth from annotation only, never the target arms.

    Contacts/PASSING use stride_notes literally. Per-frame contact questions use
    planted flags literally. Confidence is preserved, never used to drop a hard
    observation from the denominator. All numeric evidence stays in truth only.
    """
    raw = annotation.get('frames')
    if not isinstance(raw, list) or len(raw) != 12:
        raise ValueError('Twelve lateral annotation frames required')
    if annotation.get('row') != 'lateral':
        raise ValueError('Lateral annotation required')
    H = _finite(annotation['subject_height_px'])
    if H <= 0:
        raise ValueError('Positive subject height required')
    notes = annotation['stride_notes']
    contacts, passing = notes['contact_frames'], notes['passing_frames']
    for indices in (contacts, passing):
        if len(indices) != 2 or len(set(indices)) != 2 or any(type(i) is not int or not 0 <= i < 12 for i in indices):
            raise ValueError('Two distinct zero-based phase-note indices required')
    if set(contacts) & set(passing):
        raise ValueError('CONTACT and PASSING notes overlap')
    frames = []
    for i, f in enumerate(raw):
        if type(f['frame']) is not int or f['frame'] != i:
            raise ValueError('Annotation must be ordered with zero-based indices')
        def point(name):
            p = f[name]
            if not isinstance(p, (list, tuple)) or len(p) != 2:
                raise ValueError('Annotated point must have two components')
            return [_finite(v) for v in p]
        hip = point('hip'); head = point('head_top'); ground = _finite(f['ground_y'])
        soles, arms = {}, {}
        for side in ('near', 'far'):
            sole, wrist = point(side+'_sole'), point(side+'_wrist')
            soles[side] = dict(x_H=(sole[0]-hip[0])/H, height_H=(ground-sole[1])/H,
                               planted=f['planted_'+side])
            arms[side] = (wrist[0]-hip[0])/H
        frames.append(dict(frame=i, phase='CONTACT' if i in contacts else 'PASSING' if i in passing else None,
                           head_height_H=(ground-head[1])/H, soles=soles, arm_x_H=arms))
    onsets = [i for i in range(12) if any(raw[i]['planted_'+s] and not raw[(i-1)%12]['planted_'+s]
                                        for s in ('near', 'far'))]
    warnings = []
    if set(onsets) != set(contacts):
        warnings.append(f'Annotation stride-note contacts {contacts} differ from planted-flag onsets {onsets} '
                        '(zero-based); each is retained for its own questions.')
    sheet = dict(kind='walk', n_frames=12, frames=frames, question_notes=warnings)
    questions = questions_from_walk_sheet(sheet)
    questions['source'] = dict(kind='annotation', plate=annotation.get('plate'), row='lateral')
    answers, evidence = _walk_truth(sheet, questions)
    truth = dict(version=VERSION, source=questions['source'], answers=answers,
                 controls=[q['id'] for q in questions['questions'] if q['declared_absent_control']],
                 evidence=evidence, notes=warnings,
                 annotation_confidence=[dict(frame=f['frame'], confidence=f.get('confidence', {})) for f in raw],
                 confidence_policy='All observations scored; confidence retained without filtering or relabeling.')
    return questions, truth
