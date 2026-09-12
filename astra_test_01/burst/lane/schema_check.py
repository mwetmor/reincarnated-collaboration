"""Strict, dependency-free validator for the receipt schema's JSON subset."""
import argparse
import json
import math
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / 'receipt.schema.json'


def validate(value, schema=None, path='$'):
    """Return diagnostic strings; an empty list means valid."""
    if schema is None:
        schema = json.loads(SCHEMA.read_text())
    checks = {'object': lambda x: isinstance(x, dict),
              'array': lambda x: isinstance(x, list),
              'string': lambda x: isinstance(x, str),
              'integer': lambda x: type(x) is int,
              'number': lambda x: type(x) in (int, float) and (type(x) is int or math.isfinite(x)),
              'boolean': lambda x: type(x) is bool,
              'null': lambda x: x is None}
    kind = schema.get('type')
    if kind not in checks:
        return [f'{path}: unsupported schema type {kind!r}']
    if not checks[kind](value):
        return [f'{path}: expected {kind}']
    errors = []
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: value outside enum')
    if kind == 'object':
        props = schema.get('properties', {})
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{path}.{key}: missing')
        for key, item in value.items():
            if key in props:
                errors.extend(validate(item, props[key], f'{path}.{key}'))
            elif schema.get('additionalProperties') is False:
                errors.append(f'{path}.{key}: unexpected')
    elif kind == 'array':
        for i, item in enumerate(value):
            errors.extend(validate(item, schema['items'], f'{path}[{i}]'))
    return errors


def check(path):
    try:
        return validate(json.loads(Path(path).read_text()))
    except (OSError, ValueError) as exc:
        return [f'receipt unreadable: {exc}']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('receipt')
    args = parser.parse_args()
    errors = check(args.receipt)
    print(json.dumps({'valid': not errors, 'errors': errors}))
    raise SystemExit(2 if errors else 0)
