"""RESID-D1-2 step 4: the locomotion actuator chain. READ-ONLY."""
import sys; sys.path.insert(0, '.')
import d8_lib as L, d4b_dis as D

TARGETS = [
    ('32-Character-UpdateSelf',        0x04cad0, 900),
    ('33-CMM-Update',                  0x0781a0, 120),
    ('34-CMM-MoveToNextWaypoint',      0x0771a0, 400),
    ('35-CMM-Stop',                    0x0780e0, 40),
    ('36-CMM-IsMoving-0x9010',         0x009010, 20),
    ('37-CMM-MoveTo',                  0x077f40, 200),
    ('38-Character-MoveTo',            0x04a670, 300),
    ('39-Character-DisallowsMovement', 0x05b3d0, 60),
    ('40-CMM-IsMovementDisabled',      0x078170, 20),
    ('41-CMM-DisableMovement',         0x078160, 20),
    ('42-CMM-Activate',                0x078100, 40),
    ('43-CMM-Deactivate',              0x078130, 40),
    ('44-CMM-IsActivated',             0x078150, 20),
]
for name, rva, n in TARGETS:
    lines = L.bounded(rva, n)
    body = f'=== {name}  RVA {rva:#010x}  sym={D.nearest(rva)} ===\n' + '\n'.join(lines) + '\n'
    open(f'evidence/{name}.asm', 'w').write(body)
    print(f'{name}: {len(lines)} lines')
