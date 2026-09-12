"""Event census and final-state filesystem audit (not a syscall monitor)."""
import hashlib
import json
import os
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[3]


def within(path, root):
    return Path(path).is_relative_to(Path(root))


def tree(root):
    """Hash regular files; record directories and links without following links."""
    root = Path(root).absolute()
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(base) / name
            if path.is_symlink():
                result[str(path)] = 'link:' + os.readlink(path)
            elif path.is_dir():
                result[str(path)] = 'dir'
            elif path.is_file():
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(block)
                result[str(path)] = f'{path.stat().st_mode & 0o7777}:' + digest.hexdigest()
            else:
                result[str(path)] = 'special'
    return result


def take_snapshot(workdir, repo=None):
    roots = list(dict.fromkeys(str(Path(p).resolve()) for p in (workdir, repo or REPO)))
    return {'roots': roots, 'files': {p: h for root in roots for p, h in tree(root).items()}}


def audit(events_path, workdir, snapshot, caps, type):
    violations, tools_seen = [], {}
    image_calls = tool_calls = 0
    seen = set()
    try:
        with Path(events_path).open() as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError('event must be an object')
                    if event.get('type') != 'item.completed':
                        continue
                    item = event.get('item')
                    if not isinstance(item, dict):
                        raise ValueError('completed item must be an object')
                    ident = item.get('id')
                    if ident is not None:
                        if ident in seen:
                            continue
                        seen.add(ident)
                    kind = str(item.get('type', 'unknown'))
                    command = str(item.get('command', ''))
                    name = str(item.get('tool', item.get('name', kind)))
                    server = str(item.get('server', ''))
                    descriptor = ' '.join((kind, name, server, command)).lower()
                    is_image = 'image' in kind.lower() or 'image_gen' in descriptor
                    is_tool = is_image or kind not in ('agent_message', 'reasoning', 'todo_list')
                    if is_tool:
                        tool_calls += 1
                        label = (server + '.' + name).strip('.') if server else name
                        tools_seen[label] = tools_seen.get(label, 0) + 1
                    if is_image:
                        image_calls += 1
                    if re.search(r'(?<![a-z])(web|collaboration|spawn)(?![a-z])', descriptor):
                        violations.append(f'forbidden tool at line {line_number}: {name}')
                except (ValueError, TypeError) as exc:
                    violations.append(f'malformed event at line {line_number}: {exc}')
    except OSError as exc:
        violations.append(f'events unreadable: {exc}')
    if image_calls > caps['image_cap']:
        violations.append('image_cap exceeded')
    image_limit = {'GENERATE': 12, 'LABEL': 2}.get(type, 0)
    minutes_limit, tool_limit = (40, 60) if type == 'TOOLING' else (15, 20)
    if type not in ('TOOLING', 'GENERATE', 'CHECK', 'JUDGE', 'TRANSCRIBE', 'LABEL', 'ANNOTATE', 'PACK'):
        violations.append('unknown burst type')
    if caps['image_cap'] < 0 or caps['image_cap'] > image_limit or image_calls > image_limit:
        violations.append('image cap outside type limits')
    if not 0 <= caps['tool_call_cap'] <= tool_limit or tool_calls > tool_limit:
        violations.append('tool cap outside charter limits')
    if 'minutes_cap' in caps and not 1 <= caps['minutes_cap'] <= minutes_limit:
        violations.append('wall cap outside charter limits')
    if type not in ('GENERATE', 'LABEL') and image_calls:
        violations.append(f'image calls forbidden for {type}')
    if tool_calls > caps['tool_call_cap']:
        violations.append('tool_call_cap exceeded')
    after = {p: h for root in snapshot['roots'] for p, h in tree(root).items()}
    out = Path(workdir).resolve() / 'out'
    allowed = [Path(p).resolve() for p in caps.get('add_dirs', [])]
    outside = []
    for p in sorted(set(snapshot['files']) | set(after)):
        if snapshot['files'].get(p) == after.get(p):
            continue
        # Workdir changes are only permitted under out, regardless of add_dirs.
        if within(p, Path(workdir).resolve()):
            permitted = within(p, out) and within(Path(p).resolve(), out)
        else:
            permitted = any(within(p, d) and within(Path(p).resolve(), d) for d in allowed)
        if not permitted:
            outside.append(p)
    if outside:
        violations.append('filesystem writes outside permitted paths')
    return dict(violations=violations, image_calls=image_calls, tool_calls=tool_calls,
                tools_seen=tools_seen, writes_outside_out=outside)
