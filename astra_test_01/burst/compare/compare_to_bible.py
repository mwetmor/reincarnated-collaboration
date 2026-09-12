"""Closed-form O9 inventory/declaration comparison and O3 measured cross-check.
Measurements override neither declarations nor transcription: disagreement is
reported explicitly. Without per-part masks, only global count can be checked.
Uncalibrated bible fields are not silently certified; coverage lists omissions.
"""
import json
from transcribe.questions import from_bible,schema_from_bible
from lane.schema_check import validate
from oracles.common import report
from oracles.motif import count_instances

def compare_answers(bible,answers,*,scope='character',motif_measurement=None,subject=''):
    questions=from_bible(bible,scope);errors=validate(answers,schema_from_bible(bible,scope))
    if not errors:
        for part,item in answers.items():
            if item['count']<0:errors.append(f'{part}: count must be nonnegative')
    if errors:return report('O9',subject,None,0,reason='Invalid strict inventory',metrics={'errors':errors})
    violations=[]
    for q in questions:
        item=answers[q['part']]
        if q['predicate']=='present':
            if item['present']!=(item['count']>0):violations.append(q['id']+': presence/count inconsistency')
            if q['declared_absent_control'] and item['present']:violations.append(q['id']+': declared-absent control claimed present')
        elif item['count']>q['maximum']:violations.append(q['id']+': count exceeds declaration')
    if motif_measurement is not None:
        metrics=json.loads(motif_measurement['notes'])['metrics']
        if motif_measurement['value'] is None:return report('O9',subject,None,0,reason='O3 measurement unevaluable')
        measured=metrics['inside']+metrics['outside'];hypothesis=sum(x['count'] for x in answers.values())
        if measured!=hypothesis:violations.append(f'O3 cross-check: transcription={hypothesis}, measured={measured}')
    return report('O9',subject,len(violations),0,unit='violations',metrics={'violations':violations})

def compare_to_bible(image,bible,*,template_rgb,allowed_masks,scales,rotations_deg,thresh,answers=None,scope='character',display_scale=None,subject='',**nms):
    rules=[r for r in bible['RULE'] if r['scope']==scope and r['class']=='motif' and r['oracle']['id']=='O3']
    if len(rules)!=1:return report('compare_to_bible',subject,None,0,reason='Requires one declared O3 motif rule')
    if allowed_masks is None:return report('compare_to_bible',subject,None,0,reason='Reviewed allowed-region annotations required')
    row=count_instances(image,template_rgb,scales,rotations_deg,thresh,allowed_masks,max_outside=rules[0]['oracle']['threshold'],display_scale=display_scale,subject=subject,**nms)
    rows=[row]
    if answers is not None:rows.append(compare_answers(bible,answers,scope=scope,motif_measurement=row,subject=subject))
    unavailable=any(r['passed'] is None for r in rows)
    violations=sum(r['passed'] is False for r in rows)
    return report('compare_to_bible',subject,None if unavailable else violations,0,unit='violated_rules',metrics={'results':rows,'coverage':['O3']+(['O9'] if answers is not None else []),'unassessed':'JUDGE-only and undeclared palette/light/construction/scale thresholds'},reason='A required instrument is unevaluable' if unavailable else '')
