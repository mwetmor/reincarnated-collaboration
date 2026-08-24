"""STEP 4 — verification passes on the convention decode.
V1: the two named float constants are exactly 10.0f and 0.1f (bit-exact, not 'about').
V2: NO float division anywhere in the whole application chain (a divide-by-duration is the
    TOTAL signature; its ABSENCE is what makes the verdict PER-SECOND).
V3: the DoT tick period constant in Update() is 0x64 = 100 ms (corroborates D-4 M-1 from binary)."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe = D.pe

print('--- V1: constants, bit-exact ---')
for label, rva in [('tickcount multiplier', 0x5f58a4), ('per-tick multiplier', 0x5f57ac)]:
    b = pe.at(rva, 4); f = struct.unpack('<f', b)[0]
    print(f'  {label:<22} rva {rva:#x}  bytes {b.hex()}  f32 = {f!r}   exact10={f==10.0} exact0.1={b.hex()=="cdcccc3d"}')

print('\n--- V2: float-division scan across the whole chain ---')
CHAIN = [
    ('DamageAttributeDur::AddDamageToAccumulator (roll + ctor)', 0x1425b0, 190),
    ('CombatAttributeDurDamage::ctor',                            0xd7c80,  40),
    ('CombatAttributeDurDamage::Process',                         0xd7dd0, 130),
    ('CombatAttributeDurDamage::Execute',                         0xd80c0,  25),
    ('DurationDamageManager::AddDamage',                          0x208a30, 200),
    ('DurationDamageManager::ModifyDuration',                     0x209db0, 120),
    ('entry insert/merge  @0x20d6b0',                             0x20d6b0, 200),
    ('entry per-tick sum  @0x20da10',                             0x20da10, 200),
    ('DurationDamageManager::ExecuteDamage',                      0x208370, 260),
    ('DurationDamageManager::Update',                             0x207f40, 120),
]
FDIV = ('divss','divps','divsd','divpd','fdiv','fdivp','fdivr','fdivrp','fidiv','fidivr')
for name, rva, n in CHAIN:
    lines = D.disasm(rva, n, stop_at_ret=False)
    hits = [l for l in lines if any(f' {m} ' in l or l.split()[1] == m for m in FDIV if len(l.split()) > 1)]
    print(f'  {name:<56} float-div sites: {len(hits)}')
    for h in hits: print('      ', h.strip())

print('\n--- V3: DoT tick period in Update() ---')
for l in D.disasm(0x207f40, 40, stop_at_ret=False):
    if 'cmp' in l and '0x64' in l: print('  ', l.strip())
    if '0x51eb851f' in l: print('   (magic-number divide-by-100 idiom) ', l.strip())
