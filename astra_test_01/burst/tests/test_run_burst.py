import hashlib
import subprocess
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from lane import ledger, run_burst


class ModuleTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / 'tmp')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()

    def test_incomplete_task_rejected(self):
        with self.assertRaises(ValueError):
            run_burst.validate_task({'text': 'incomplete'}, 'CHECK')

    def test_effort_and_add_dirs(self):
        t = dict(text='test', references=[], image_cap=0, minutes_cap=1,
                 tool_call_cap=1, outputs=[], effort='high', add_dirs=[])
        run_burst.validate_task(t, 'CHECK')
        for effort in ['medium', 'low', 'xhigh', 'HIGH', '']:
            with self.subTest(effort=effort), self.assertRaises(ValueError):
                run_burst.validate_task(dict(t, effort=effort), 'TOOLING')
        for typ in ['GENERATE', 'CHECK', 'JUDGE', 'TRANSCRIBE', 'LABEL', 'ANNOTATE', 'PACK']:
            with self.subTest(typ=typ), self.assertRaises(ValueError):
                run_burst.validate_task(dict(t, add_dirs=[str(self.root)]), typ)
        run_burst.validate_task(dict(t, add_dirs=[str(self.root)]), 'TOOLING')

    def test_in_place_files(self):
        work, added = self.root / 'work', self.root / 'added'
        work.mkdir()
        added.mkdir()
        p = added / 'source.py'
        p.write_text('source')
        digest = ledger.sha256(p)
        def verify(path, sha=digest, typ='TOOLING'):
            return run_burst.verify_files(dict(files=[dict(path=path, sha256=sha)], images=[]), work, typ, [added])
        expected = [dict(root=str(added), name='source.py', sha256=digest)]
        for path in [str(p), 'source.py']:
            self.assertEqual(verify(path), ([], [], expected))
        for path, sha, typ in [(str(p), '0'*64, 'TOOLING'), (str(p), digest, 'CHECK'),
                               ('../added/source.py', digest, 'TOOLING'),
                               ('missing.py', digest, 'TOOLING')]:
            self.assertTrue(verify(path, sha, typ)[1])
        (added / 'link.py').symlink_to(p)
        self.assertTrue(verify('link.py')[1])
        (added / 'sub').symlink_to(added, target_is_directory=True)
        self.assertTrue(verify('sub/source.py')[1])
        outside = self.root / 'outside.py'
        outside.write_text('source')
        self.assertTrue(verify(str(outside))[1])
        self.assertFalse((work / 'out').exists())
        (work / 'out').mkdir()
        (work / 'out/source.py').write_text('source')
        self.assertTrue(verify('source.py')[1])  # ambiguous relative name
        self.assertEqual(verify('out/source.py'), ([dict(name='source.py', sha256=digest)], [], []))

    def test_profile_metadata(self):
        path = self.root / '.codex/astra-burst.config.toml'
        path.parent.mkdir()
        raw = b'model = "gpt-6-astra"\nmodel_reasoning_effort = "high"\n'
        path.write_bytes(raw)
        with patch.object(run_burst.Path, 'home', return_value=self.root), patch.object(run_burst.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'codex 1.2.3\n', '')) as proc:
            self.assertEqual(run_burst.profile_metadata(), dict(model='gpt-6-astra', model_source='profile', codex_version='codex 1.2.3', profile_sha256=hashlib.sha256(raw).hexdigest()))
            self.assertEqual(proc.call_args.args[0], ['codex', '--version'])
            path.write_text('model_reasoning_effort = "high"\n')
            with self.assertRaises(ValueError):
                run_burst.profile_metadata()

    def test_wrapper_image_truth_and_tooling_in_place(self):
        import argparse
        import contextlib
        import io
        import json
        import os
        from lane import render_brief, schema_check
        contract = Path(__file__).resolve().parent / 'fixtures/lane_contract'
        for typ, reported, expected in [('GENERATE', 1, 0), ('GENERATE', 0, 2), ('TOOLING', 0, 0)]:
            with self.subTest(typ=typ, reported=reported):
                base = self.root / f'{typ}-{reported}'
                base.mkdir()
                added = base / 'declared'
                added.mkdir()
                repo = base / 'repo'
                home = base / 'codex'
                preexisting = home / 'generated_images/synthetic/old.png'
                preexisting.parent.mkdir(parents=True)
                preexisting.write_bytes(b'old')
                t = dict(text='test', references=[], image_cap=1 if typ == 'GENERATE' else 0,
                         minutes_cap=1, tool_call_cap=1, outputs=[], effort='high',
                         add_dirs=[str(added)] if typ == 'TOOLING' else [])
                tp = base / 'task.json'
                tp.write_text(json.dumps(t))
                args = argparse.Namespace(run='test', burst_id='test', type=typ, task=str(tp), dry_run=False)
                class FakeProcess:
                    def __init__(self, cmd, **kw):
                        wd = Path(kw['cwd'])
                        r = dict(task_id='test', status='DELIVERED', images=[], calls_used=reported,
                                 retries=[], self_report=dict(obeyed_invariants=True, concerns=[]), files=[])
                        if typ == 'GENERATE':
                            (preexisting.parent / 'new.png').write_bytes(b'new')
                            other = home / 'generated_images/other/new.png'
                            other.parent.mkdir()
                            other.write_bytes(b'other')
                        else:
                            source = added / 'tool.py'
                            source.write_text('source')
                            r['files'] = [dict(path='tool.py', sha256=ledger.sha256(source))]
                        (wd / 'out/receipt.json').write_text(json.dumps(r))
                        kw['stdout'].write('{"type":"thread.started","thread_id":"synthetic"}\n')
                    def wait(self, timeout=None):
                        return 0
                meta = dict(model='gpt-6-astra', model_source='profile', codex_version='test', profile_sha256='a'*64)
                with patch.object(run_burst, 'ROOT', repo), patch.object(ledger, 'ROOT', repo), patch.object(run_burst, 'WORK_ROOT', base/'work'), patch.object(run_burst, 'profile_metadata', return_value=meta), patch.object(render_brief, 'ROOT', contract), patch.object(schema_check, 'SCHEMA', contract/'receipt.schema.json'), patch.dict(os.environ, {'CODEX_HOME': str(home)}), patch.object(run_burst.subprocess, 'Popen', FakeProcess), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(run_burst.run(args), expected)
                data = json.loads((repo/'runs/test/ledger.json').read_text())
                entry = data['bursts'][0]
                self.assertEqual(data['images_used'], int(typ == 'GENERATE'))
                self.assertEqual(entry['image_calls'], int(typ == 'GENERATE'))
                self.assertEqual(entry['image_calls_events'], 0)
                if typ == 'TOOLING':
                    self.assertEqual(entry['artifacts_in_place'], [dict(root=str(added), name='tool.py', sha256=ledger.sha256(added/'tool.py'))])
                    self.assertEqual(entry['artifacts'], [])
                    self.assertFalse((repo/'runs/test/artifacts/test/tool.py').exists())
                else:
                    self.assertEqual(entry['generated_images_new'], [dict(path=str(preexisting.parent/'new.png'), sha256=ledger.sha256(preexisting.parent/'new.png'))])
                    self.assertEqual('image count mismatch (audit 1 vs receipt 0)' in entry['audit']['violations'], reported == 0)
