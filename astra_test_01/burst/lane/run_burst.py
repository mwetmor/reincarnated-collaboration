"""Serial conductor CLI. Child artifacts are untrusted until audit + validation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import time
import tomllib

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lane import audit, ledger, render_brief, schema_check, provenance_capture, ref_provenance

ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = Path.home() / 'astra-burst' / 'runs'


def validate_task(task, type):
    expected = {'text': str, 'references': list, 'image_cap': int, 'minutes_cap': int,
                'tool_call_cap': int, 'outputs': list, 'effort': str, 'add_dirs': list}
    for key, cls in expected.items():
        if key not in task or task[key].__class__ is not cls:
            raise ValueError(f'invalid task field {key}')
    if type not in render_brief.TYPES:
        raise ValueError('unknown burst type')
    minutes_limit, tool_limit = (40, 60) if type == 'TOOLING' else (15, 20)
    if not 1 <= task['minutes_cap'] <= minutes_limit or not 0 <= task['tool_call_cap'] <= tool_limit:
        raise ValueError('wall/tool cap outside charter limits')
    image_limit = {'GENERATE': 12, 'LABEL': 2}.get(type, 0)
    if not 0 <= task['image_cap'] <= image_limit:
        raise ValueError('image cap outside type limits')
    if task['effort'] != 'high':
        raise ValueError('effort must equal high')
    if type != 'TOOLING' and task['add_dirs']:
        raise ValueError('non-TOOLING add_dirs must be empty')
    if any(not isinstance(p, str) for p in task['outputs'] + task['add_dirs']):
        raise ValueError('output/add_dirs entries must be strings')
    for ref in task['references']:
        if not isinstance(ref, dict) or any(not isinstance(ref.get(k), str) for k in ('path', 'role')):
            raise ValueError('invalid reference')
        ok, reason = ref_provenance.check(ref['path'])
        if not ok:
            raise ValueError('reference provenance: ' + reason)
    for output in task['outputs']:
        p = Path(output)
        if p.is_absolute() or '..' in p.parts or not p.parts:
            raise ValueError('outputs must be relative paths without traversal')


def prepare_task(task):
    task = dict(task)
    task['references'] = [dict(ref, path=f"in/{i:02d}_{Path(ref['path']).name}")
                          for i, ref in enumerate(task['references'], 1)]
    task['add_dirs'] = [str(Path(p).expanduser().resolve()) for p in task['add_dirs']]
    return task


def build_command(workdir, task, brief):
    cmd = ['codex', 'exec', '--ignore-user-config', '-p', 'astra-burst', '-C', str(workdir),
           '-s', 'workspace-write', '--ephemeral', '--skip-git-repo-check', '-c',
           f'model_reasoning_effort="{task["effort"]}"']
    for ref in task['references']:
        cmd += ['-i', ref['path']]
    for directory in task['add_dirs']:
        cmd += ['--add-dir', directory]
    return cmd + ['--output-schema', str(ROOT / 'receipt.schema.json'), '-o', 'out/receipt.json', '--json', brief]


def profile_metadata():
    """The --json stream does not echo the model; record the pinned profile."""
    path = Path.home() / '.codex/astra-burst.config.toml'
    raw = path.read_bytes()
    profile = tomllib.loads(raw.decode())
    model = profile.get('model')
    if not isinstance(model, str) or not model:
        raise ValueError('profile model missing')
    version = subprocess.run(['codex', '--version'], check=True, capture_output=True,
                             text=True, timeout=30).stdout.strip()
    return dict(model=model, model_source='profile', codex_version=version,
                profile_sha256=hashlib.sha256(raw).hexdigest())


def verify_files(receipt, workdir, type='CHECK', add_dirs=()):
    """Return (harvest artifacts, errors, in-place artifacts); never copy here.

    Relative paths use out/ first, then a unique declared add_dir. Ambiguous
    existing paths are rejected. Links in any component and '..' are rejected.
    """
    workdir = Path(workdir).resolve()
    out = workdir / 'out'
    roots = [Path(p).expanduser().absolute() for p in add_dirs] if type == 'TOOLING' else []
    artifacts, in_place, errors = {}, {}, []
    for item in receipt['files'] + receipt['images']:
        supplied = Path(item['path'])
        if '..' in supplied.parts or not supplied.parts:
            errors.append(f'artifact traversal: {item["path"]}')
            continue
        if supplied.is_absolute():
            candidates = [supplied]
        elif supplied.parts[0] == 'out':
            candidates = [workdir / supplied]
        else:
            candidates = [out / supplied] + [root / supplied for root in roots]
            candidates = list(dict.fromkeys(p for p in candidates if p.exists() or p.is_symlink()))
        if len(candidates) != 1:
            errors.append(f'artifact missing or ambiguous: {item["path"]}')
            continue
        p = candidates[0]
        # A declared add_dir can never relax the workdir's under-out rule.
        root = out if p.is_relative_to(out) else None
        if root is None and not p.is_relative_to(workdir):
            root = next((d for d in roots if p.is_relative_to(d)), None)
        if root is None:
            errors.append(f'artifact outside permitted roots: {item["path"]}')
            continue
        if p.is_symlink() or any(a.is_symlink() for a in p.parents):
            errors.append(f'artifact symlink: {item["path"]}')
            continue
        try:
            valid = p.resolve().is_relative_to(root.resolve()) and p.is_file() and ledger.sha256(p) == item['sha256']
        except OSError:
            valid = False
        if not valid:
            errors.append(f'artifact missing or hash mismatch: {item["path"]}')
            continue
        name = str(p.relative_to(root))
        if root == out:
            artifacts[name] = item['sha256']
        else:
            in_place[(str(root), name)] = item['sha256']
    return ([{'name': n, 'sha256': h} for n, h in sorted(artifacts.items())], errors,
            [{'root': r, 'name': n, 'sha256': h} for (r, n), h in sorted(in_place.items())])


def run(args):
    ledger.identifier(args.run)
    ledger.identifier(args.burst_id)
    task = json.loads(Path(args.task).read_text())
    validate_task(task, args.type)
    prepared = prepare_task(task)
    brief = render_brief.render(prepared, args.type)
    workdir = WORK_ROOT / args.run / args.burst_id
    cmd = build_command(workdir, prepared, brief)
    if args.dry_run:
        print(brief)
        print('\nCOMMAND\n' + shlex.join(cmd) + ' </dev/null > events.jsonl 2> stderr.txt')
        return 0
    if workdir.exists():
        raise ValueError('workdir already exists; use a fresh burst id')
    current_path = ROOT / 'runs' / args.run / 'ledger.json'
    current = json.loads(current_path.read_text()) if current_path.exists() else ledger.empty()
    if current['images_used'] + task['image_cap'] > current['images_cap']:
        raise ValueError('insufficient run image budget')
    provenance = profile_metadata()
    workdir.mkdir(parents=True)
    (workdir / 'in').mkdir()
    out = workdir / 'out'
    out.mkdir()
    refs = []
    for original, staged in zip(task['references'], prepared['references']):
        destination = workdir / staged['path']
        shutil.copyfile(Path(original['path']).expanduser(), destination)
        refs.append(dict(staged, sha256=ledger.sha256(destination)))
    (workdir / 'references.json').write_text(json.dumps(refs, indent=2) + '\n')
    (workdir / 'brief.txt').write_text(brief)
    snapshot = audit.take_snapshot(workdir, prepared['add_dirs'])
    images_snapshot = audit.generated_images_snapshot()
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic()
    execution_error = None
    # Logs are initially inside out so wrapper IO cannot create false audit writes.
    events = out / '.wrapper-events.jsonl'
    stderr = out / '.wrapper-stderr.txt'
    with events.open('w') as stdout, stderr.open('w') as err:
        try:
            proc = subprocess.Popen(cmd, cwd=workdir, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=err, start_new_session=True)
            try:
                code = proc.wait(timeout=task['minutes_cap'] * 60)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                code, execution_error = 3, 'TIMEOUT'
            if code and execution_error is None:
                execution_error = f'codex exit {code}'
        except OSError as exc:
            execution_error = f'codex launch: {exc}'
    ended = datetime.now(timezone.utc).isoformat()
    minutes = (time.monotonic() - tick) / 60
    errors = schema_check.check(out / 'receipt.json')
    artifacts, artifacts_in_place = [], []
    receipt = None
    if not errors:
        receipt = json.loads((out / 'receipt.json').read_text())
        artifacts, errors, artifacts_in_place = verify_files(receipt, workdir, args.type, prepared['add_dirs'])
        if receipt['task_id'] != args.burst_id:
            errors.append('receipt task_id mismatch')
        if receipt['status'] == 'FAILED':
            execution_error = execution_error or 'receipt reports unsuccessful execution'
    result = audit.audit(events, workdir, snapshot, prepared, args.type,
                         images_snapshot=images_snapshot, receipt=receipt)
    if args.type in ('GENERATE', 'LABEL'):
        for generated in result['generated_images_new']:
            sidecar = provenance_capture.write_sidecar(generated['path'], out)
            artifacts.append(dict(name=sidecar.name, sha256=ledger.sha256(sidecar)))
    # Reject all special files/links, including unlisted files, before copytree.
    for path, kind in audit.tree(out, audit_exclusions=False).items():
        if kind.startswith('link:') or kind == 'special':
            errors.append(f'unsafe output: {path}')
    result['violations'].extend(errors)
    if execution_error:
        result['execution_error'] = execution_error
    # Process error/timeout takes precedence over absent/partial receipt.
    exit_code = 3 if execution_error else (2 if result['violations'] else 0)
    events.replace(workdir / 'events.jsonl')
    stderr.replace(workdir / 'stderr.txt')
    if exit_code == 0:
        target = ROOT / 'runs' / args.run / 'artifacts' / args.burst_id
        shutil.copytree(out, target)
    receipt_path = out / 'receipt.json'
    ledger.append(args.run, dict(id=args.burst_id, type=args.type, experiment=task.get('experiment'),
                  brief_sha256=hashlib.sha256(brief.encode()).hexdigest(), started=started, ended=ended,
                  minutes=minutes, image_calls=result['image_calls'], tool_calls=result['tool_calls'],
                  audit=result, receipt_sha256=ledger.sha256(receipt_path) if receipt_path.is_file() else None,
                  artifacts=artifacts if exit_code == 0 else [],
                  artifacts_in_place=artifacts_in_place, effort=task['effort'],
                  image_calls_events=result['image_calls_events'],
                  generated_images_new=result['generated_images_new'],
                  generator=dict(observed_fingerprint=None, probe_set_sha256=None),
                  regeneratable_until=None,
                  **provenance, exit=exit_code))
    print(json.dumps({'exit': exit_code, 'audit': result}))
    return exit_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--burst-id', required=True)
    parser.add_argument('--type', choices=render_brief.TYPES, required=True)
    parser.add_argument('--task', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
