import argparse
import contextlib
import io
import json
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from lane import audit, ledger, render_brief, run_burst, schema_check

FIXTURES = Path(__file__).parent / 'fixtures'


def task():
    return dict(text='Synthetic task', references=[], image_cap=0, minutes_cap=1,
                tool_call_cap=20, outputs=['result.txt'], effort='high', add_dirs=[])


def receipt():
    return dict(task_id='T-test', status='DELIVERED', images=[], calls_used=0, retries=[],
                self_report=dict(obeyed_invariants=True, concerns=[]), files=[])


class LaneTests(unittest.TestCase):
    def setUp(self):
        contract = FIXTURES / 'lane_contract'
        for obj, key, value in [(render_brief, 'ROOT', contract), (schema_check, 'SCHEMA', contract / 'receipt.schema.json')]:
            patcher = patch.object(obj, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / "tmp")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.work = self.base / 'work'
        self.repo = self.base / 'repo'
        (self.work / 'out').mkdir(parents=True)
        self.repo.mkdir()

    def test_render_deterministic_and_ordered(self):
        t = task()
        t['references'] = [{'role': 'anchor', 'path': 'in/01.png'}]
        a = render_brief.render(t, 'CHECK')
        self.assertEqual(a, render_brief.render(dict(reversed(list(t.items()))), 'CHECK'))
        markers = ['REGISTER CARD —', '**Every burst:**', '\nTASK\n', '\nREFERENCES\n', '\nRETURN\n']
        offsets = [a.index(m) for m in markers]
        self.assertEqual(offsets, sorted(offsets))
        self.assertIn('Image 1: anchor — in/01.png', a)
        self.assertIn('| **CHECK**', a)
        self.assertNotIn('| **GENERATE**', a)
        for typ in ('LABEL', 'TRANSCRIBE'):
            self.assertIn('| **' + typ + '**', render_brief.render(t, typ))
        for typ in ('bogus',):
            with self.assertRaises(ValueError):
                render_brief.render(t, typ)

    def test_exact_command_and_dry_run(self):
        t = task()
        t.update(references=[{'path': '/a/source image.png', 'role': 'anchor'}], add_dirs=[str(self.repo)])
        prepared = run_burst.prepare_task(t)
        expected = ['codex', 'exec', '--ignore-user-config', '-p', 'astra-burst', '-C', str(self.work),
                    '-s', 'workspace-write', '--ephemeral', '--skip-git-repo-check', '-c',
                    'model_reasoning_effort="high"', '-i', 'in/01_source image.png',
                    '--add-dir', str(self.repo), '--output-schema', str(run_burst.ROOT / 'receipt.schema.json'),
                    '-o', 'out/receipt.json', '--json', 'BRIEF']
        self.assertEqual(run_burst.build_command(self.work, prepared, 'BRIEF'), expected)
        tp = self.base / 'task.json'
        tp.write_text(json.dumps(t))
        args = argparse.Namespace(run='C-test', burst_id='T-test', type='TOOLING', task=str(tp), dry_run=True)
        out = io.StringIO()
        with patch.object(run_burst, 'WORK_ROOT', self.base / 'runs'), patch.object(subprocess, 'Popen') as popen, contextlib.redirect_stdout(out):
            self.assertEqual(run_burst.run(args), 0)
            popen.assert_not_called()
        brief = render_brief.render(prepared, 'TOOLING')
        command = run_burst.build_command(self.base / 'runs/C-test/T-test', prepared, brief)
        self.assertEqual(out.getvalue(), brief + '\n\nCOMMAND\n' + shlex.join(command) + ' </dev/null > events.jsonl 2> stderr.txt\n')
        self.assertFalse((self.base / 'runs').exists())

    def test_audit_planted_events(self):
        snap = audit.take_snapshot(self.work)
        caps = dict(image_cap=1, tool_call_cap=2, add_dirs=[])
        result = audit.audit(FIXTURES / 'bad_events.jsonl', self.work, snap, caps, 'GENERATE')
        self.assertEqual(result['image_calls'], 0)
        self.assertEqual(result['image_calls_events'], 2)
        self.assertEqual(result['tool_calls'], 4)
        self.assertTrue(any('forbidden' in v for v in result['violations']))
        self.assertNotIn('image_cap exceeded', result['violations'])
        self.assertIn('tool_call_cap exceeded', result['violations'])

    def test_filesystem_diff_new_modified_deleted_and_allowed(self):
        original = self.work / 'input.txt'
        original.write_text('old')
        deleted = self.work / 'deleted.txt'
        deleted.write_text('old')
        allowed = self.repo / 'allowed'
        allowed.mkdir()
        snap = audit.take_snapshot(self.work, [allowed])
        original.write_text('changed')
        deleted.unlink()
        (self.work / 'planted.txt').write_text('bad')
        (self.repo / 'planted.txt').write_text('bad')
        (allowed / 'ok.txt').write_text('ok')
        (self.work / 'out/ok.txt').write_text('ok')
        result = audit.audit(FIXTURES / 'clean_events.jsonl', self.work, snap,
                             dict(image_cap=0, tool_call_cap=1, add_dirs=[str(allowed)]), 'TOOLING')
        self.assertEqual(set(result['writes_outside_out']), {str(original), str(deleted),
                         str(self.work / 'planted.txt')})

    def test_clean_and_malformed_events(self):
        snap = audit.take_snapshot(self.work)
        caps = dict(image_cap=0, tool_call_cap=1)
        clean = audit.audit(FIXTURES / 'clean_events.jsonl', self.work, snap, caps, 'CHECK')
        self.assertEqual(clean['violations'], [])
        self.assertEqual(clean['tool_calls'], 1)
        bad = audit.audit(FIXTURES / 'malformed_events.jsonl', self.work, snap, caps, 'CHECK')
        self.assertEqual(len(bad['violations']), 2)

    def test_schema_known_bad_and_strict_objects(self):
        self.assertEqual(schema_check.validate(receipt()), [])
        bad = receipt()
        bad['status'] = 'PASS'
        self.assertTrue(schema_check.validate(bad))
        bad = receipt()
        bad['calls_used'] = True
        self.assertTrue(schema_check.validate(bad))
        bad = receipt()
        bad['self_report']['extra'] = 1
        self.assertTrue(schema_check.validate(bad))
        del bad['task_id']
        self.assertTrue(schema_check.validate(bad))
        schema = json.loads(schema_check.SCHEMA.read_text())
        def walk(s):
            if s['type'] == 'object':
                self.assertIs(s['additionalProperties'], False)
                self.assertEqual(set(s['properties']), set(s['required']))
                for value in s['properties'].values(): walk(value)
            elif s['type'] == 'array': walk(s['items'])
        walk(schema)

    def test_ledger_atomic_replacement_and_rollback(self):
        with patch.object(ledger, 'ROOT', self.repo):
            ledger.append('C-test', dict(id='one', image_calls=2))
            p = self.repo / 'runs/C-test/ledger.json'
            prior = p.read_bytes()
            with patch.object(ledger.os, 'replace', side_effect=OSError('injected replace error')):
                with self.assertRaises(OSError):
                    ledger.append('C-test', dict(id='two', image_calls=3))
            self.assertEqual(p.read_bytes(), prior)
            self.assertEqual(list(p.parent.glob('.ledger-*')), [])
            data = ledger.append('C-test', dict(id='two', image_calls=3))
            self.assertEqual(data['images_used'], 5)
            self.assertEqual(data['images_cap'], 250)
            with self.assertRaises(ValueError):
                ledger.append('C-test', dict(id='two', image_calls=0))
            with self.assertRaises(ValueError):
                ledger.append('../escape', dict(id='three', image_calls=0))

    def test_artifact_hash_escape_and_symlink(self):
        f = self.work / 'out/result.txt'
        f.write_text('ok')
        r = receipt()
        r['files'] = [dict(path='out/result.txt', sha256=ledger.sha256(f))]
        self.assertEqual(run_burst.verify_files(r, self.work)[1], [])
        r['files'][0]['sha256'] = '0' * 64
        self.assertTrue(run_burst.verify_files(r, self.work)[1])
        r['files'][0]['path'] = '../escape'
        self.assertTrue(run_burst.verify_files(r, self.work)[1])
        (self.work / 'out/link').symlink_to(f)
        r['files'] = [dict(path='link', sha256=ledger.sha256(f))]
        self.assertTrue(run_burst.verify_files(r, self.work)[1])

    def test_task_caps(self):
        for key, value in [('minutes_cap', 16), ('tool_call_cap', 21), ('image_cap', 1), ('effort', 'low'), ('outputs', ['../x'])]:
            t = task()
            t[key] = value
            with self.assertRaises(ValueError): run_burst.validate_task(t, 'CHECK')

    def test_wrapper_roundtrip_error_timeout_and_void(self):
        real_snapshot = audit.take_snapshot
        for mode, expected in [('delivered', 0), ('bad_hash', 2), ('error', 3), ('timeout', 3)]:
            with self.subTest(mode=mode):
                local = self.base / mode
                repo = local / 'repo'
                repo.mkdir(parents=True)
                tp = local / 'task.json'
                tp.write_text(json.dumps(task()))
                args = argparse.Namespace(run='C-test', burst_id='T-test', type='CHECK', task=str(tp), dry_run=False)
                class FakeProcess:
                    pid = 999999
                    def __init__(self, cmd, **kw):
                        self.waits = 0
                        wd = Path(kw['cwd'])
                        (wd / 'out/result.txt').write_text('result')
                        r = receipt()
                        r['files'] = [dict(path='result.txt', sha256='bad' if mode == 'bad_hash' else ledger.sha256(wd / 'out/result.txt'))]
                        (wd / 'out/receipt.json').write_text(json.dumps(r))
                        kw['stdout'].write((FIXTURES / 'clean_events.jsonl').read_text())
                    def wait(self, timeout=None):
                        self.waits += 1
                        if mode == 'timeout' and self.waits == 1:
                            raise subprocess.TimeoutExpired('codex', timeout)
                        return 7 if mode == 'error' else 0
                with patch.object(run_burst, 'ROOT', repo), patch.object(ledger, 'ROOT', repo), patch.object(run_burst, 'WORK_ROOT', local / 'runs'), patch.object(run_burst, 'profile_metadata', return_value=dict(model='gpt-6-astra', model_source='profile', codex_version='codex test', profile_sha256='a'*64)), patch.dict(run_burst.os.environ, {'CODEX_HOME': str(local / 'codex')}), patch.object(subprocess, 'Popen', FakeProcess), patch.object(os_module(), 'killpg') as kill, contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(run_burst.run(args), expected)
                data = json.loads((repo / 'runs/C-test/ledger.json').read_text())
                entry = data['bursts'][0]
                self.assertEqual(entry['exit'], expected)
                self.assertEqual(entry['tool_calls'], 1)
                self.assertEqual(entry['model'], 'gpt-6-astra')
                self.assertEqual(entry['model_source'], 'profile')
                self.assertEqual(entry['effort'], 'high')
                self.assertEqual(entry['codex_version'], 'codex test')
                self.assertEqual(entry['profile_sha256'], 'a'*64)
                self.assertEqual(entry['image_calls_events'], 0)
                self.assertEqual(entry['generated_images_new'], [])
                self.assertEqual(entry['artifacts_in_place'], [])
                self.assertEqual((repo / 'runs/C-test/artifacts/T-test/result.txt').exists(), expected == 0)
                self.assertEqual(kill.call_count, int(mode == 'timeout'))
                if mode == 'timeout': self.assertEqual(entry['audit']['execution_error'], 'TIMEOUT')


def os_module():
    return run_burst.os


if __name__ == '__main__':
    unittest.main()
