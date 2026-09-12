"""Closed-form O9 inventory/declaration comparison and O3 measured cross-check.
Measurements override neither declarations nor transcription: disagreement is
reported explicitly. Without per-part masks, only global count can be checked.
Uncalibrated bible fields are not silently certified; coverage lists omissions.
"""
import json
from transcribe.questions import from_bible,schema_from_bible,parts_from_bible,parts_schema
from lane.schema_check import validate
from oracles.common import report
from oracles.motif import count_instances,count_family,FAMILY_PARAMETERS

def compare_answers(bible,answers,*,scope='character',motif_measurement=None,subject='',question_set='auto'):
    controls=bible.get('controls',{}).get('declared_absent_parts',[])
    if question_set=='auto':
        question_set='parts' if isinstance(answers,dict) and set(answers)&set(controls) else 'motif'
    if question_set=='parts':
        questions=parts_from_bible(bible)
        schema=parts_schema([p['name'] for p in bible['PARTS']],controls)
    elif question_set=='motif':
        questions=from_bible(bible,scope);schema=schema_from_bible(bible,scope)
    else:raise ValueError('question_set must be auto, parts or motif')
    errors=validate(answers,schema)
    if not errors:
        for part,item in answers.items():
            if item['count']<0:errors.append(f'{part}: count must be nonnegative')
    if errors:return report('O9',subject,None,0,reason='Invalid strict inventory',metrics={'errors':errors})
    violations=[]
    for q in questions:
        item=answers[q['part']]
        if q['predicate']=='present':
            if item['present']!=(item['count']>0):violations.append(q['id']+': presence/count inconsistency')
            if q['declared_absent_control'] and (item['present'] or item['count']>0):violations.append(q['id']+': declared-absent control claimed present')
        elif q['maximum'] is not None and item['count']>q['maximum']:violations.append(q['id']+': count exceeds declaration')
    if motif_measurement is not None and question_set=='motif':
        metrics=json.loads(motif_measurement['notes'])['metrics']
        if motif_measurement['value'] is None:return report('O9',subject,None,0,reason='O3 measurement unevaluable')
        measured=metrics['inside']+metrics['outside'];hypothesis=sum(x['count'] for x in answers.values())
        if measured!=hypothesis:violations.append(f'O3 cross-check: transcription={hypothesis}, measured={measured}')
    return report('O9',subject,len(violations),0,unit='violations',metrics={'violations':violations})

def compare_to_bible(image,bible,*,template_rgb=None,allowed_masks=None,scales=None,rotations_deg=None,thresh=None,answers=None,scope='character',display_scale=None,subject='',**nms):
    rules=[r for r in bible['RULE'] if r['scope']==scope and r['class']=='motif' and r['oracle']['id']=='O3']
    if len(rules)!=1:return report('compare_to_bible',subject,None,0,reason='Requires one declared O3 motif rule')
    if allowed_masks is None:return report('compare_to_bible',subject,None,0,reason='Reviewed allowed-region annotations required')
    oracle=rules[0]['oracle'];mode=oracle.get('mode','template')
    if mode not in ('template','family','both'):raise ValueError('Unknown motif mode')
    rows=[]
    if mode in ('template','both'):
        if template_rgb is None or thresh is None or not scales or not rotations_deg:
            rows.append(report('O3',subject,None,oracle['threshold'],reason='Template inputs required'))
        else:
            rows.append(count_instances(image,template_rgb,scales,rotations_deg,thresh,allowed_masks,
                max_outside=oracle['threshold'],display_scale=display_scale,subject=subject,**nms))
    if mode in ('family','both'):
        parameters=dict(FAMILY_PARAMETERS);parameters.update(oracle.get('family_parameters',{}))
        rows.append(count_family(image,family=oracle.get('family','ring'),allowed_masks=allowed_masks,
            max_outside=oracle['threshold'],display_scale=display_scale,subject=subject,**parameters))
    motif_rows=list(rows)
    if answers is not None:
        # These are alternative measurements of the same primitive, never add
        # the template/family counts. Record each available O9 cross-check.
        rows += [compare_answers(bible,answers,scope=scope,motif_measurement=row,subject=subject)
                 for row in list(rows)]
    unavailable=any(r['passed'] is None for r in rows)
    violations=int(any(r['passed'] is False for r in motif_rows))
    violations+=int(any(r['passed'] is False for r in rows[len(motif_rows):]))
    return report('compare_to_bible',subject,violations if violations else (None if unavailable else 0),0,unit='violated_rules',metrics={'results':rows,'coverage':list(dict.fromkeys(r['id'] for r in rows)),'unassessed':'JUDGE-only and undeclared palette/light/construction/scale thresholds'},reason='A required instrument is unevaluable' if unavailable and not violations else '')
