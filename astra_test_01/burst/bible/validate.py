"""Dependency-free validation of the JSON Schema subset used by bible v0.1.
Not a general Draft 2020-12 engine. Supports the explicit keywords in schema.json
and raises on unknown validation keywords instead of silently ignoring them.
"""
import json
import math
import re
from pathlib import Path

ANNOTATIONS={'$schema','title','description'}
KEYWORDS={'type','properties','required','additionalProperties','items','minItems','maxItems','minimum','maximum','pattern','enum','oneOf','anyOf'}

def validate(value,schema=None,path='$'):
    if schema is None:schema=json.loads((Path(__file__).parent/'schema.json').read_text())
    unknown=set(schema)-KEYWORDS-ANNOTATIONS
    if unknown:raise ValueError(f'Unsupported schema keywords: {sorted(unknown)}')
    errors=[]
    for keyword in ('anyOf','oneOf'):
        if keyword in schema:
            matches=sum(not validate(value,option,path) for option in schema[keyword])
            if (keyword=='anyOf' and matches<1) or (keyword=='oneOf' and matches!=1):errors.append(f'{path}: {keyword} constraint')
    kind=schema.get('type')
    checks={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),'string':lambda x:isinstance(x,str),'integer':lambda x:type(x) is int,'number':lambda x:type(x) in (int,float) and math.isfinite(x),'boolean':lambda x:type(x) is bool,'null':lambda x:x is None}
    if kind is not None:
        kinds=kind if isinstance(kind,list) else [kind]
        if any(k not in checks for k in kinds):raise ValueError('Unsupported schema type')
        if not any(checks[k](value) for k in kinds):return errors+[f'{path}: expected {kind}']
    if 'enum' in schema and value not in schema['enum']:errors.append(f'{path}: outside enum')
    if isinstance(value,dict):
        props=schema.get('properties',{})
        errors += [f'{path}.{key}: missing' for key in schema.get('required',[]) if key not in value]
        for key,item in value.items():
            if key in props:errors.extend(validate(item,props[key],f'{path}.{key}'))
            elif schema.get('additionalProperties') is False:errors.append(f'{path}.{key}: unexpected')
            elif isinstance(schema.get('additionalProperties'),dict):errors.extend(validate(item,schema['additionalProperties'],f'{path}.{key}'))
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0) or len(value)>schema.get('maxItems',math.inf):errors.append(f'{path}: array length')
        if 'items' in schema:
            for i,item in enumerate(value):errors.extend(validate(item,schema['items'],f'{path}[{i}]'))
    if isinstance(value,str) and 'pattern' in schema and re.search(schema['pattern'],value) is None:errors.append(f'{path}: pattern')
    if type(value) in (int,float):
        if value<schema.get('minimum',-math.inf) or value>schema.get('maximum',math.inf):errors.append(f'{path}: numeric bounds')
    return errors
