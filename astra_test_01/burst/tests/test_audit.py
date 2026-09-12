import json
import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from lane import audit, ledger

FIXTURES = Path(__file__).resolve().parent / 'fixtures'


class ModuleTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / 'tmp')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.work = self.root / 'work'
        (self.work / 'out').mkdir(parents=True)
        self.home = self.root / 'codex'
        env = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        env.start()
        self.addCleanup(env.stop)
        self.caps = dict(image_cap=0, tool_call_cap=60, minutes_cap=1, add_dirs=[])

    def run_audit(self, events, **kwargs):
        return audit.audit(events, self.work, audit.take_snapshot(self.work),
                           self.caps, 'TOOLING', **kwargs)

    def events(self, items=(), thread=None):
        events = [] if thread is None else [dict(type='thread.started', thread_id=thread)]
        events += [dict(type='item.completed', item=item) for item in items]
        p = self.work / 'out/events.jsonl'
        p.write_text(''.join(json.dumps(e)+'\n' for e in events))
        return p

    def test_missing_event_log(self):
        self.assertTrue(self.run_audit(self.root / 'missing')['violations'])

    def test_real_streams_have_no_forbidden_hits(self):
        for name, count in [('x1_gen_01_events.jsonl', 2), ('x1_chk_01_events.jsonl', 6), ('t0c_events.jsonl', 16)]:
            with self.subTest(name=name):
                result = self.run_audit(FIXTURES / name)
                self.assertEqual(result['tool_calls'], count)
                self.assertEqual([v for v in result['violations'] if 'forbidden tool' in v], [])
        self.assertTrue(any('forbidden tool' in v for v in self.run_audit(FIXTURES / 'bad_events.jsonl')['violations']))

    def test_forbidden_fields_only(self):
        for item, forbidden in [
            ({'type': 'mcp_tool_call', 'server': 'web', 'tool': 'run'}, True),
            ({'type': 'custom_tool_call', 'name': 'web__run'}, True),
            ({'type': 'custom_tool_call', 'tool': 'safe', 'name': 'WEB__RUN'}, True),
            ({'type': 'collaboration.spawn_agent'}, True),
            ({'type': 'spawn'}, True),
            ({'type': 'webbed', 'name': 'cobweb'}, False),
            ({'type': 'command_execution', 'command': 'cat /x/reincarnated-collaboration/web/spawn.py'}, False),
        ]:
            with self.subTest(item=item):
                hits = [v for v in self.run_audit(self.events([item]))['violations'] if 'forbidden tool' in v]
                self.assertEqual(bool(hits), forbidden)

    def test_generated_images_truth_and_thread_scope(self):
        root = self.home / 'generated_images'
        thread = root / 'synthetic'
        thread.mkdir(parents=True)
        old = thread / 'old.png'
        old.write_bytes(b'old')
        before = audit.generated_images_snapshot()
        old.write_bytes(b'changed')
        new = thread / 'new.PNG'
        new.write_bytes(b'new')
        (thread / 'ignored.txt').write_text('not image')
        (thread / 'link.webp').symlink_to(new)
        (root / 'other').mkdir()
        (root / 'other/new.jpg').write_bytes(b'other')
        self.caps['image_cap'] = 0
        result = self.run_audit(self.events(thread='synthetic'), images_snapshot=before)
        self.assertEqual(result['image_calls'], 1)
        self.assertEqual(result['image_calls_events'], 0)
        self.assertEqual(result['generated_images_new'], [dict(path=str(new), sha256=ledger.sha256(new))])
        self.assertIn('image_cap exceeded', result['violations'])
        self.assertIn('image calls forbidden for TOOLING', result['violations'])
        self.assertEqual(self.run_audit(self.events(), images_snapshot=before)['image_calls'], 2)
        self.assertEqual(self.run_audit(self.events(thread='missing'), images_snapshot=before)['image_calls'], 0)
        self.assertTrue(any('invalid thread_id' in v for v in self.run_audit(self.events(thread='../other'), images_snapshot=before)['violations']))

    def test_missing_generated_directory(self):
        before = audit.generated_images_snapshot()
        self.assertEqual(before['files'], {})
        p = self.home / 'generated_images/new/image.webp'
        p.parent.mkdir(parents=True)
        p.write_bytes(b'new')
        self.assertEqual(audit.generated_images_diff(before), [dict(path=str(p), sha256=ledger.sha256(p))])

    def test_receipt_mismatch_only_for_valid_receipt(self):
        r = dict(task_id='test', status='DELIVERED', images=[], calls_used=1, retries=[],
                 self_report=dict(obeyed_invariants=True, concerns=[]), files=[])
        events = self.events()
        self.assertIn('image count mismatch (audit 0 vs receipt 1)', self.run_audit(events, receipt=r)['violations'])
        r['calls_used'] = 0
        self.assertEqual(self.run_audit(events, receipt=r)['violations'], [])
        r['calls_used'] = '1'
        self.assertFalse(any('image count mismatch' in v for v in self.run_audit(events, receipt=r)['violations']))

    def test_snapshot_roots_exclusions_and_type_permissions(self):
        added = self.root / 'added'
        added.mkdir()
        events = self.events()
        before = audit.take_snapshot(self.work, [added])
        self.assertEqual(before['roots'], [str(self.work), str(added)])
        for root in [self.work, added]:
            for directory in ['.git', '__pycache__']:
                (root / directory).mkdir()
                (root / directory / 'noise').write_text('ignored')
            (root / 'noise.pyc').write_bytes(b'ignored')
        for name in ['.wrapper-events.jsonl', '.wrapper-stderr.txt']:
            (self.work / 'out' / name).write_text('wrapper')
        file = added / 'source.py'
        file.write_text('source')
        (self.root / 'outside.txt').write_text('not snapshotted')
        caps = dict(image_cap=0, tool_call_cap=1, add_dirs=[str(added)])
        result = audit.audit(events, self.work, before, caps, 'TOOLING')
        self.assertEqual(result['writes_outside_out'], [])
        result = audit.audit(events, self.work, before, caps, 'CHECK')
        self.assertEqual(result['writes_outside_out'], [str(file)])
        leak = self.work / 'leak.txt'
        leak.write_text('bad')
        caps['add_dirs'].append(str(self.work))
        result = audit.audit(events, self.work, before, caps, 'TOOLING')
        self.assertEqual(result['writes_outside_out'], [str(leak)])

    def test_snapshot_scalar_compatibility_and_harvest_link_scan(self):
        self.assertEqual(audit.take_snapshot(self.work, self.work)['roots'], [str(self.work)])
        link = self.work / 'out/.git'
        link.symlink_to(self.home, target_is_directory=True)
        # Audit noise exclusion must not weaken the independent harvest check.
        self.assertTrue(audit.tree(self.work / 'out', audit_exclusions=False)[str(link)].startswith('link:'))
        link.unlink()
        self.home.mkdir()
        scope = self.home / 'generated_images'
        scope.mkdir()
        (scope / 'thread').symlink_to(self.work, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            audit.generated_images_diff({'root': str(scope), 'files': {}}, 'thread')
