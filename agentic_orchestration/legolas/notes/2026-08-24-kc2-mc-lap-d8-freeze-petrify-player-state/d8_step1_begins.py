"""D-8 step 1 — full disassembly of Character::BeginFreeze / BeginPetrify and their siblings
(BeginTrap / BeginImmobilize / BeginKnockdown) so the Character-level lane can be compared with
the controller-level lane.  READ-ONLY."""
import sys; sys.path.insert(0, '.')
import d4b_dis as D

TARGETS = [
    ('Character::BeginFreeze',      0x0005b020),
    ('Character::BeginPetrify',     0x0005b150),
    ('Character::BeginTrap',        0x0005afc0),
    ('Character::BeginImmobilize',  0x0005b280),
    ('Character::BeginKnockdown',   0x0005b2e0),
]
for nm, rva in TARGETS:
    print(f'=== {nm}  @ {rva:#010x}   exported-as: {D.nearest(rva)}')
    for l in D.disasm(rva, 140, stop_at_ret=False):
        print(l)
    print()
