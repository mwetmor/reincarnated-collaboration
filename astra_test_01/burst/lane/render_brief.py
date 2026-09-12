"""Deterministic brief composition from frozen contract files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = ('TOOLING', 'GENERATE', 'CHECK', 'JUDGE', 'TRANSCRIBE', 'LABEL', 'ANNOTATE', 'PACK')


def render(task: dict, type: str) -> str:
    if type not in TYPES:
        raise ValueError(f'unknown burst type: {type}')
    rules = (ROOT / 'BURST_RULES.md').read_text()
    rows = [line for line in rules.splitlines() if line.startswith(f'| **{type}**')]
    if len(rows) != 1:
        raise ValueError(f'no frozen rules for {type}')
    before, after = rules.split('| Type |', 1)
    table_end = after.index('\n\n')
    selected = before + '| Type | May | May not | Image cap | Output |\n|---|---|---|---|---|\n' + rows[0] + after[table_end:]
    task_block = {'text': task['text'], 'outputs': task['outputs'],
                  'image_cap': task['image_cap'], 'minutes_cap': task['minutes_cap'],
                  'tool_call_cap': task['tool_call_cap']}
    refs = '\n'.join(f"Image {i}: {ref['role']} — {ref['path']}" for i, ref in enumerate(task['references'], 1))
    return ((ROOT / 'REGISTER_CARD.md').read_text() + '\n' + selected + '\nTASK\n' +
            json.dumps(task_block, sort_keys=True, ensure_ascii=False, indent=2) +
            '\nREFERENCES\n' + refs + '\nRETURN\n' + (ROOT / 'receipt.schema.json').read_text())
