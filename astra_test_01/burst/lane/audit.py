"""Event census and final-state filesystem audit (not a syscall monitor).

The codex --json stream does not surface image_gen calls. New image files in
CODEX_HOME/generated_images are authoritative; the event heuristic is diagnostic
only. Final-state snapshots cannot detect transient writes or deleted images.
"""
import hashlib
import json
import os
from pathlib import Path
import re

IMAGE_SUFFIXES = {'.png', '.jpg', '.webp'}
FORBIDDEN = re.compile(r'(?<![a-z0-9])(web|collaboration|spawn)(?![a-z0-9])')


def generated_images_snapshot():
    """List image paths and size/mtime before launch; never follow symlinks."""
    root = (Path(os.environ.get('CODEX_HOME', '~/.codex')).expanduser()
            / 'generated_images').resolve()
    files = {}
    if not root.exists():
        return {'root': str(root), 'files': files}
    def unreadable(exc):
        raise exc
    for base, dirs, names in os.walk(root, followlinks=False, onerror=unreadable):
        dirs[:] = sorted(d for d in dirs if not (Path(base) / d).is_symlink())
        for name in sorted(names):
            p = Path(base) / name
            if p.suffix.lower() in IMAGE_SUFFIXES and not p.is_symlink() and p.is_file():
                st = p.stat()
                files[str(p)] = [st.st_size, st.st_mtime_ns]
    return {'root': str(root), 'files': files}


def generated_images_diff(before, thread_id=None):
    """Count only new paths, restricted to the event thread when available."""
    root = Path(before['root'])
    scope = root
    if thread_id is not None:
        if not isinstance(thread_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', thread_id):
            raise ValueError('invalid thread_id')
        scope = root / thread_id
    result = []
    if scope.is_symlink():
        raise ValueError('generated image thread directory is a symlink')
    if not scope.exists():
        return result
    def unreadable(exc):
        raise exc
    for base, dirs, names in os.walk(scope, followlinks=False, onerror=unreadable):
        dirs[:] = sorted(d for d in dirs if not (Path(base) / d).is_symlink())
        for name in sorted(names):
            p = Path(base) / name
            if (p.suffix.lower() in IMAGE_SUFFIXES and str(p) not in before['files']
                    and not p.is_symlink() and p.is_file()):
                result.append({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    return sorted(result, key=lambda item: item['path'])


def within(path, root):
    return Path(path).is_relative_to(Path(root))


def tree(root, exclude=(), audit_exclusions=True):
    """Hash regular files; record directories and links without following links."""
    root = Path(root).absolute()
    result = {}
    excluded = {str(Path(p).absolute()) for p in exclude}
    for base, dirs, files in os.walk(root, followlinks=False):
        if audit_exclusions:
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
        for name in sorted(dirs + files):
            if audit_exclusions and (name.endswith('.pyc') or (Path(base) == root / 'out' and name in
                    ('.wrapper-events.jsonl', '.wrapper-stderr.txt'))):
                continue
            path = Path(base) / name
            if str(path) in excluded:
                continue
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


def take_snapshot(workdir, add_dirs=()):
    """Snapshot the workdir plus declared add_dirs, never an implicit repo root."""
    if isinstance(add_dirs, (str, os.PathLike)):
        add_dirs = [add_dirs]
    roots = list(dict.fromkeys(str(Path(p).resolve()) for p in (workdir, *add_dirs)))
    excluded = [str(Path(workdir).resolve() / 'out' / name)
                for name in ('.wrapper-events.jsonl', '.wrapper-stderr.txt')]
    return {'roots': roots, 'exclude': excluded,
            'files': {p: h for root in roots for p, h in tree(root, excluded).items()}}


def audit(events_path, workdir, snapshot, caps, type, images_snapshot=None, receipt=None):
    violations, tools_seen = [], {}
    image_calls_events = tool_calls = 0
    thread_id = None
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
                    if event.get('type') == 'thread.started' and 'thread_id' in event:
                        thread_id = event['thread_id']
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
                    descriptor = ' '.join(str(item.get(k, '')) for k in ('type', 'tool', 'name', 'server')).lower()
                    is_image = 'image' in kind.lower() or 'image_gen' in (descriptor + ' ' + command.lower())
                    is_tool = is_image or kind not in ('agent_message', 'reasoning', 'todo_list')
                    if is_tool:
                        tool_calls += 1
                        label = (server + '.' + name).strip('.') if server else name
                        tools_seen[label] = tools_seen.get(label, 0) + 1
                    if is_image:
                        image_calls_events += 1
                    if FORBIDDEN.search(descriptor):
                        violations.append(f'forbidden tool at line {line_number}: {name}')
                except (ValueError, TypeError) as exc:
                    violations.append(f'malformed event at line {line_number}: {exc}')
    except OSError as exc:
        violations.append(f'events unreadable: {exc}')
    generated_images_new = []
    if images_snapshot is not None:
        try:
            generated_images_new = generated_images_diff(images_snapshot, thread_id)
        except (OSError, ValueError) as exc:
            violations.append(f'generated images unreadable: {exc}')
    image_calls = len(generated_images_new)
    if receipt is not None:
        from lane.schema_check import validate
        if not validate(receipt) and receipt['calls_used'] != image_calls:
            violations.append(f"image count mismatch (audit {image_calls} vs receipt {receipt['calls_used']})")
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
    after = {p: h for root in snapshot['roots'] for p, h in tree(root, snapshot.get('exclude', ())).items()}
    out = Path(workdir).resolve() / 'out'
    allowed = [Path(p).resolve() for p in caps.get('add_dirs', [])] if type == 'TOOLING' else []
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
                tools_seen=tools_seen, writes_outside_out=outside,
                image_calls_events=image_calls_events, generated_images_new=generated_images_new)
