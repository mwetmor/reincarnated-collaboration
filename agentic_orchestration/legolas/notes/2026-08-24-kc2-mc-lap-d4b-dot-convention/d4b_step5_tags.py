"""STEP 5 — CORROBORATION (supporting, never primary): the localization strings.
Lap I found these but could not tell whether the character sheet DISPLAYS the raw .dbr field or a
transformed one. With the binary decode in hand the strings are now interpretable."""
import sys, re; sys.path.insert(0,'.')
from d4b_lib import *
a = ArcArchive(VENDOR_E3/'resources'/'Text_EN.arc')
want = re.compile(r'(PoisonAbsDmgInfo|PoisonDurationInfo|BleedingAbsDmgInfo|BurnAbsDmgInfo|'
                  r'DamageDurationPoison|DamageSingleFormatTime|DamageRangeFormatTime|tagPerSecond|'
                  r'FrostburnAbsDmgInfo|ElectrocuteAbsDmgInfo|VitalityDecayAbsDmgInfo)', re.I)
seen = {}
for n in a.names():
    if not n.lower().endswith('.txt'): continue
    try: payload = a.read_file(n)
    except Exception: continue
    for k, v in parse_tag_file(payload):
        if want.search(k): seen.setdefault(k, (n, v))
for k in sorted(seen):
    f, v = seen[k]
    print(f'{k}\n    file : {f}\n    value: {v!r}\n')
