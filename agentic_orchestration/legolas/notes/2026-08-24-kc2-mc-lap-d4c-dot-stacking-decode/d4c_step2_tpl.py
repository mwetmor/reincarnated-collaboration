"""D-4c STEP 2 — declared authoring schema for `damageMagnitude` (the stack-ordinal multiplier
table read into gGameEngine+0x292d4). READ-ONLY."""
import sys; sys.path.insert(0, '.')
from d4b_lib import ArcArchive, VENDOR_FULL, VENDOR_E3

for tag, root in (('FULL v1.2.3.4', VENDOR_FULL), ('ED-III', VENDOR_E3)):
    arc = root / 'database' / 'templates.arc'
    if not arc.exists():
        print(f'[{tag}] no templates.arc'); continue
    a = ArcArchive(arc)
    hits, bad = [], 0
    for n in a.names():
        try: blob = a.read_file(n)
        except Exception: bad += 1; continue
        if b'damageMagnitude' in blob: hits.append((n, blob))
    print(f'[{tag}] tpl files scanned, undecodable={bad}, hits={[h[0] for h in hits]}')
    for n, blob in hits:
        txt = blob.decode('latin-1')
        i = txt.find('damageMagnitude')
        s = txt.rfind('Variable', 0, i); e = txt.find('}', i)
        print(f'  --- {n} ---')
        print('  ' + txt[s:e+1].replace('\n', '\n  ').strip())
