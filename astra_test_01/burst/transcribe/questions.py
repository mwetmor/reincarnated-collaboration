"""O9 deterministic DSG-shaped questions for a closed per-part motif inventory.
The counted object is the declared motif ON each part, not the anatomical part
itself. Excluded surfaces are declared-absent motif controls. No image access.
Each count question depends on its unique presence question. Multiple motifs
require separate TRANSCRIBE bursts and schemas; never merge their answers.
"""

def from_bible(bible,scope='character'):
    parts=[p['name'] for p in bible['PARTS']]
    if len(parts)!=len(set(parts)):raise ValueError('Duplicate closed part name')
    rules=[r for r in bible['RULE'] if r['scope']==scope and r['class']=='motif']
    if len(rules)!=1:raise ValueError('Exactly one motif per transcription question set required')
    r=rules[0];allowed={p['where']:p['count'] for p in r['placements']};excluded=set(r['exclusions'])
    if not excluded or not excluded<=set(parts):raise ValueError('At least one closed declared-absent control required')
    if set(allowed)&excluded or not set(allowed)<=set(parts):raise ValueError('Conflicting or open placement declarations')
    questions=[]
    for part in parts:
        if part not in allowed and part not in excluded:raise ValueError('Part lacks a motif presence declaration')
        pid=f'{r["id"]}.{part}.present';absent=part in excluded
        questions.append({'id':pid,'part':part,'predicate':'present','question':f'Is {r["id"]} present on {part}?','depends_on':[],'declared_absent_control':absent,'expected':False if absent else None})
        questions.append({'id':f'{r["id"]}.{part}.count','part':part,'predicate':'count','question':f'How many instances of {r["id"]} are on {part}?','depends_on':[pid],'declared_absent_control':absent,'maximum':0 if absent else allowed[part]})
    return questions

def schema_from_bible(bible,scope='character'):
    from_bible(bible,scope)
    def obj(p):return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    return obj({p['name']:obj({'present':{'type':'boolean'},'count':{'type':'integer','minimum':0}}) for p in bible['PARTS']})


def _closed_parts(parts, controls):
    parts, controls = list(parts), list(controls)
    if any(not isinstance(p, str) or not p for p in parts+controls):
        raise ValueError('Part names must be nonempty strings')
    if len(set(parts)) != len(parts) or len(set(controls)) != len(controls):
        raise ValueError('Duplicate closed part/control name')
    if not controls:
        raise ValueError('At least one declared-absent PART control required')
    return parts+[p for p in controls if p not in parts], set(controls)


def parts_questions(parts, controls):
    """Separate anatomical PART inventory; controls join the closed vocabulary.

    Counts of ordinary parts are observations, not invented declarations. A
    declared-absent part has an explicit expected presence False and count 0.
    """
    closed, absent = _closed_parts(parts, controls)
    questions = []
    for part in closed:
        pid = f'parts.{part}.present'
        control = part in absent
        questions.append(dict(id=pid, part=part, predicate='present',
            question=f'Is the anatomical part {part} present?', depends_on=[],
            declared_absent_control=control, expected=False if control else None))
        questions.append(dict(id=f'parts.{part}.count', part=part, predicate='count',
            question=f'How many anatomical instances of {part} are present?',
            depends_on=[pid], declared_absent_control=control,
            expected=0 if control else None, maximum=0 if control else None))
    return questions


def parts_from_bible(bible):
    return parts_questions([p['name'] for p in bible['PARTS']],
                           bible.get('controls', {}).get('declared_absent_parts', []))


def parts_schema(parts, controls):
    closed, _ = _closed_parts(parts, controls)
    def obj(properties):
        return dict(type='object', properties=properties, required=list(properties),
                    additionalProperties=False)
    return obj({p: obj({'present': {'type': 'boolean'},
                        'count': {'type': 'integer', 'minimum': 0}}) for p in closed})
