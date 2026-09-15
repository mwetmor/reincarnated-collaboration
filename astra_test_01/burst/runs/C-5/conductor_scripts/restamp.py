# Re-stamp 00-system.md § 7 SYNC rows whose source hash changed (date = today), then run check_sync.
import hashlib, re, subprocess, pathlib, datetime
ROOT = pathlib.Path('/Users/admin/Games/reincarnated-collaboration'); DOC = ROOT/'canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md'
SRC = {'agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md': ROOT/'agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md',
 'astra_test_01/burst/SPEC.md': ROOT/'astra_test_01/burst/SPEC.md', 'astra_test_01/burst/BURST_RULES.md': ROOT/'astra_test_01/burst/BURST_RULES.md',
 'astra_test_01/burst/REGISTER_CARD.md': ROOT/'astra_test_01/burst/REGISTER_CARD.md', 'astra_test_01/burst/JUDGE_RUBRIC.md': ROOT/'astra_test_01/burst/JUDGE_RUBRIC.md',
 'astra_test_01/burst/receipt.schema.json': ROOT/'astra_test_01/burst/receipt.schema.json', 'astra_test_01/burst/lane/run_burst.py': ROOT/'astra_test_01/burst/lane/run_burst.py',
 'astra_test_01/burst/MANIFEST.sha256': ROOT/'astra_test_01/burst/MANIFEST.sha256', '~/.codex/astra-burst.config.toml': pathlib.Path.home()/'.codex/astra-burst.config.toml',
 'AGENTS.md': ROOT/'AGENTS.md'}
today = datetime.date.today().isoformat(); text = DOC.read_text(); changed = []
for key, path in SRC.items():
    h = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    pat = re.compile(r'^(\| `' + re.escape(key) + r'`[^|]* \| [^|]* \| )([0-9a-f]{12})( \| )(\d{4}-\d{2}-\d{2})( \|)$', re.M)
    m = pat.search(text); assert m, key
    if m.group(2) != h:
        text = text[:m.start()] + m.group(1) + h + m.group(3) + today + m.group(5) + text[m.end():]; changed.append((key, m.group(2), h))
DOC.write_text(text)
for c in changed: print('restamped', c)
print('unchanged rows:', len(SRC)-len(changed))
print(subprocess.run(['python3', str(ROOT/'astra_test_01/burst/lane/check_sync.py')], capture_output=True, text=True).stdout.count('OK '), '/ 10 OK')
