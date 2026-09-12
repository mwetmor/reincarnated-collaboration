import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from lane import deps_ledger

class Tests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory(dir=Path(__file__).parent/'tmp');self.addCleanup(td.cleanup)
        self.root=Path(td.name);p=patch.object(deps_ledger,'ROOT',self.root);p.start();self.addCleanup(p.stop)
    def add(self,key,deps=(),state='generated',hash='a'*64):
        return deps_ledger.record('test',key,hash,list(deps),state)
    def test_transitive_diamond_slot_and_unrelated(self):
        self.add('base');self.add('head',['base'],'approved');self.add('body',['base'])
        self.add('bundle',['head','body']);self.add('unrelated')
        self.add('base',hash='b'*64)
        self.assertEqual(deps_ledger.invalidate('test','base'),{'base','head','body','bundle'})
        data=json.loads((self.root/'runs/test/deps.json').read_text())['assets']
        self.assertEqual(data['base']['content_hash'],'b'*64)
        self.assertEqual(data['unrelated']['state'],'generated')
        self.assertTrue(all(data[k]['state']=='invalidated' for k in ('base','head','body','bundle')))
    def test_human_protection(self):
        self.add('base');row=self.add('head',['base'],'human_edited');self.assertEqual(row['state'],'do_not_regenerate')
        self.add('bundle',['head'])
        self.assertEqual(deps_ledger.invalidate('test','base'),{'base','head','bundle'})
        data=json.loads((self.root/'runs/test/deps.json').read_text())['assets']
        self.assertEqual(data['head']['state'],'do_not_regenerate');self.assertTrue(data['head']['invalidated'])
        with self.assertRaises(ValueError):self.add('head',['base'],'generated')
    def test_cycle_and_invalid_are_atomic(self):
        self.add('one');self.add('two',['one']);path=self.root/'runs/test/deps.json';before=path.read_bytes()
        with self.assertRaises(ValueError):self.add('one',['two'])
        with self.assertRaises(ValueError):self.add('bad',state='unknown')
        with self.assertRaises(ValueError):self.add('bad',hash='not-a-hash')
        self.assertEqual(path.read_bytes(),before)
        self.assertFalse(list(path.parent.glob('.deps-*')))
