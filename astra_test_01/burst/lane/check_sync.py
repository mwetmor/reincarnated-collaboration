"""Read-only verification of the source hash table in 00-system.md section 7."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[3]
DOC = REPO / 'canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md'


def parse_rows(text):
    active = False
    sections = 0
    rows = []
    for line in text.splitlines():
        if re.match(r'^##\s+', line):
            active = bool(re.match(r'^##\s+7(?:[.\s]|$)', line))
            sections += int(active)
            continue
        if not active or not line.lstrip().startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if cells[0].lower() == 'source' or all(re.fullmatch(r'[-:]+', c) for c in cells):
            continue
        path = re.fullmatch(r'`([^`]+)`(?:\s+\(.*\))?', cells[0])
        if (len(cells) != 4 or not path or not re.fullmatch(r'[0-9a-fA-F]{12}', cells[2])
                or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', cells[3])):
            raise ValueError(f'malformed SYNC row: {line}')
        rows.append((path.group(1), cells[2].lower()))
    if sections != 1 or not rows:
        raise ValueError('expected one section 7 with at least one SYNC source row')
    return rows


def check(doc=DOC):
    rows = parse_rows(Path(doc).read_text())
    results = []
    for name, stamped in rows:
        path = Path(name).expanduser()
        if not path.is_absolute():
            path = REPO / path
        try:
            h = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            actual = h.hexdigest()[:12]
            error = None
        except OSError as exc:
            actual, error = 'UNREADABLE', str(exc)
        result = dict(status='OK' if actual == stamped else 'DRIFT',
                      stamped=stamped, actual=actual, path=str(path))
        if error:
            result['error'] = error
        results.append(result)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--doc', type=Path, default=DOC)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        results = check(args.doc)
    except (OSError, ValueError) as exc:
        print(f'SYNC parse error: {exc}', file=sys.stderr)
        if args.json:
            print('[]')
        return 2
    if args.json:
        print(json.dumps(results))
    else:
        for row in results:
            print('{status} {stamped} {actual} {path}'.format(**row))
    return int(any(row['status'] != 'OK' for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
