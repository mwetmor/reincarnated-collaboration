"""RESID-D1-2 step 5: the action-arbitration chain (does pushing the alert animation cancel the
move action?).  READ-ONLY."""
import sys; sys.path.insert(0, '.')
import d8_lib as L, d4b_dis as D

TARGETS = [
    ('51-ControllerAI-PlayAnimation',   0x0e77f0, 300),
    ('52-CBC-HandleAction',             0x0ea480, 60),
    ('53-CBC-LocalHandleAction',        0x0ea4e0, 120),
    ('54-CAH-Execute',                  0x0724f0, 200),
    ('55-CAH-Stop',                     0x0725a0, 60),
    ('56-PlayAnimationAction-ctor',     0x070400, 120),
    ('57-PlayAnimationAction-Execute',  0x0704b0, 150),
    ('58-ControllerAI-AddTemporaryState', 0x0e6990, 300),
    ('59-CAB-QueryActionPermission-Attack', 0x06d870, 150),
    ('60-Character-UpdatePath',         0x048dc0, 200),
    ('61-CAH-IsActive',                 0x0725f0, 30),
    ('62-CAH-GetActionType',            0x072610, 30),
    ('63-CAB-IsActive',                 0x06b580, 20),
    ('64-CAB-Finish',                   0x06b570, 20),
]
for name, rva, n in TARGETS:
    lines = L.bounded(rva, n)
    body = f'=== {name}  RVA {rva:#010x}  sym={D.nearest(rva)} ===\n' + '\n'.join(lines) + '\n'
    open(f'evidence/{name}.asm', 'w').write(body)
    print(f'{name}: {len(lines)} lines')
