"""D-4c STEP 9 — bank the disassembly listings this lap rests on, so every claim is re-checkable
without capstone. READ-ONLY."""
import sys, hashlib, pathlib; sys.path.insert(0, '.')
import d4b_dis as D
from d4b_lib import VENDOR_FULL, VENDOR_E3
OUT = pathlib.Path('evidence'); OUT.mkdir(exist_ok=True)

BANK = [
 ('F1-entry-dtor-two-lists.asm',        0x20c050,  40, 'entry dtor: proves TWO std::list members (+0x0c scratch, +0x14 live) and sizeof(entry)=0x24'),
 ('F2-endattack-scratch-to-live.asm',   0x20d940,  75, 'DurationDamageManager::EndAttack per-entry: live = scratch, then scratch.clear()'),
 ('F3-bucket-vector-assign.asm',        0x20e2e0, 120, 'vector<Instance>::operator= — EndAttack transfer is OVERWRITE, not append'),
 ('F4-std-sort-introsort.asm',          0x20ea70,  95, 'MSVC std::sort(first,last,ideal,pred) over 24-byte instances'),
 ('F5-insertion-sort-comparator.asm',   0x20ef70,  55, 'inlined comparator: comiss on inst+0x00, DESCENDING'),
 ('F6-bucket-retire-popfront.asm',      0x20dc80,  55, 'per-entry retire: pop_front x ticksDue on the live list'),
 ('F7-getduration-and-queries.asm',     0x20dc30,   4, 'GetDurationMs = liveList.size() x 100'),
 ('F8-next-second-query.asm',           0x20dbd0,  40, 'sum of inst+0x04 over the next 10 buckets = the 1-second rate query'),
 ('F9-total-remaining-query.asm',       0x20dc40,  40, 'sum of inst+0x04 over ALL live buckets = total remaining DoT'),
 ('F10-loadfromdatabase-damageMagnitude.asm', 0x2579e4, 20, 'GameEngine::LoadFromDatabase reads "damageMagnitude" into gGameEngine+0x292d4'),
 ('F11-store-adddamagetoaccumulator.asm', 0x156bf0, 175, 'DamageAttributeStore::AddDamageToAccumulator — the Global roll + XOR roulette'),
 ('F12-getdamagesourceid.asm',          0xda0b0,    3, 'CombatAttribute::GetDamageSourceId -> &this[0x10] (the 8-byte DurationDamageSource)'),
 ('F13-setskillsource.asm',             0xd70e0,    6, 'CombatAttribute::SetSkillSource -> this[0x18] (the fallback key)'),
 ('F14-fixed-damage-sibling-insert.asm', 0x20e060,  70, 'CombatAttributeDurFixedDamage insert: same buckets, flat maxss, NO source key / NO sort'),
]
for name, rva, n, note in BANK:
    body = D.disasm(rva, n, stop_at_ret=False)
    hdr = [f'; {note}', f'; Game.dll RVA {rva:#010x}  (image_base {D.IB:#x})',
           '; READ-ONLY disassembly, capstone x86-32', '']
    (OUT / name).write_text('\n'.join(hdr + body) + '\n')
    print(f'  banked {name}  ({len(body)} lines)')

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
lines = ['D-4c source digests (all vendor paths READ-ONLY)', '']
for lbl, p in (('Game.dll (v1.2.3.4)',        VENDOR_FULL / 'Game.dll'),
               ('database.arz (v1.2.3.4)',    VENDOR_FULL / 'database' / 'database.arz'),
               ('templates.arc (v1.2.3.4)',   VENDOR_FULL / 'database' / 'templates.arc'),
               ('database.arz (ed-III)',      VENDOR_E3 / 'database' / 'database.arz'),
               ('templates.arc (ed-III)',     VENDOR_E3 / 'database' / 'templates.arc')):
    lines.append(f'{lbl:<30} {sha(p)}')
(OUT / 'DIGESTS.txt').write_text('\n'.join(lines) + '\n')
print('\n' + '\n'.join(lines))
