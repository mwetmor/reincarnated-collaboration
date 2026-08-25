"""RESID-D1-2 step 2: bounded listings for the named RVAs. READ-ONLY."""
import sys; sys.path.insert(0, '.')
import d8_lib as L, d4b_dis as D

TARGETS = [
    ('21-ControllerAI-Update',       0x0e5b80, 400),
    ('22-ControllerCombat-Update',   0x0eea10, 200),
    ('23-Alert-OnUpdate',            0x109430, 120),
    ('24-Alert-OnBegin',             0x109410, 120),
    ('25-ControllerAI-MoveTo',       0x0e6cd0, 200),
    ('26-ControllerAIStateT-MoveTo', 0x060d40, 80),
    ('27-CanMove-0xc3e0',            0x00c3e0, 20),
]
for name, rva, n in TARGETS:
    lines = L.bounded(rva, n)
    s = D.nearest(rva)
    body = f'=== {name}  RVA {rva:#010x}  sym={s} ===\n' + '\n'.join(lines) + '\n'
    open(f'evidence/{name}.asm', 'w').write(body)
    print(f'{name}: {len(lines)} lines -> evidence/{name}.asm')
