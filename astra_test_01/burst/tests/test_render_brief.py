import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from lane import render_brief, run_burst


class ModuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root_card = 'ROOT REGISTER CARD\nFrozen default text.\n'
        (self.root / 'REGISTER_CARD.md').write_text(self.root_card)
        (self.root / 'BURST_RULES.md').write_text(
            'Frozen rules.\n\n| Type | May | May not | Image cap | Output |\n'
            '|---|---|---|---|---|\n'
            '| **TOOLING** | code | images | 0 | tools |\n\nFrozen footer.\n')
        (self.root / 'receipt.schema.json').write_text('{"type": "object"}\n')
        self.task = dict(text='Test task.', outputs=['out/files.json'],
                         image_cap=0, minutes_cap=40, tool_call_cap=60,
                         references=[dict(role='fixture', path='in/example.png')])
        self.root_patch = patch.object(render_brief, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def test_missing_type_rules(self):
        from lane.render_brief import render
        with self.assertRaises(ValueError):
            render({}, 'bogus')

    def test_default_equals_explicit_root_card(self):
        self.assertEqual(render_brief.render(self.task, 'TOOLING'),
                         render_brief.render(self.task, 'TOOLING',
                                             card_path=self.root / 'REGISTER_CARD.md'))

    def test_card_override_changes_only_card(self):
        card = self.root / 'custom-card.md'
        custom_text = 'RUN REGISTER CARD\nDifferent register.\n'
        card.write_text(custom_text)
        default = render_brief.render(self.task, 'TOOLING')
        overridden = render_brief.render(self.task, 'TOOLING', card_path=card)
        self.assertTrue(default.startswith(self.root_card))
        self.assertTrue(overridden.startswith(custom_text))
        self.assertNotIn(self.root_card, overridden)
        self.assertEqual(overridden[len(custom_text):], default[len(self.root_card):])

    def test_register_card_for(self):
        with patch.object(run_burst, 'ROOT', self.root):
            self.assertEqual(run_burst.register_card_for('missing-run'),
                             self.root / 'REGISTER_CARD.md')
            card = self.root / 'runs' / 'test-run' / 'REGISTER_CARD.md'
            card.parent.mkdir(parents=True)
            card.write_text('Run card.\n')
            self.assertEqual(run_burst.register_card_for('test-run'), card)
            self.assertEqual(run_burst.register_card_for('other-run'),
                             self.root / 'REGISTER_CARD.md')
