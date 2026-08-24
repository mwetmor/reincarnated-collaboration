"""D-7 step 21 — enumerate the CombatAttributeTypes that the two CrowdControl defense attributes
EXPAND into.  Each expansion writes the type into the freshly-allocated CombatAttribute at +4 as an
immediate, so the census is `mov dword ptr [eax + 4], <imm>` inside the function body. READ-ONLY."""
import sys, re, json; sys.path.insert(0, '.')
from d4b_dis import disasm

ENUM = json.load(open('evidence/combat_attribute_type_enum.json'))
NAME = {}
for v, cls in ENUM.items():
    fams = {c.split('_')[-1] for c in cls if '_' in c}
    NAME[int(v)] = '/'.join(sorted(fams)) if fams else '?'
NAME.setdefault(47, 'Immobilize (StartInvoluntaryEffect->BeginImmobilize)')
NAME.setdefault(49, 'TakeHit (StartInvoluntaryEffect->Controller+0xa0)')

for lbl, a, n in [('DefenseAttributeAbs_CrowdControl::AddToAccumulator', 0x1acc70, 400),
                  ('DefenseAttributeDefenseCap_CrowdControl::AddToAccumulator', 0x1af030, 400)]:
    print(f'=== {lbl} @ {a:#x}')
    seq = []
    for ln in disasm(a, n, stop_at_ret=True):
        m = re.search(r'mov\s+dword ptr \[eax \+ 4\], (0x[0-9a-f]+|\d+)$', ln.strip())
        if m:
            v = int(m.group(1), 0)
            seq.append(v)
            print(f'   emits type {v:#04x} ({v:>2}) = {NAME.get(v, "UNMAPPED")}')
    print(f'   -> {len(seq)} entries: {[hex(x) for x in seq]}\n')
