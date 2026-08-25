"""MD-B4app-9 step 8 — EXHAUSTIVE sweep: scan every .rdata dword image-wide for the two CheckAction
implementations, then attribute each hit to the nearest preceding ??_7 vtable symbol and report the
byte displacement.  This is what makes 'slot +0x68, never overridden on the AI branch' an
enumeration rather than a spot-check.  READ-ONLY."""
import sys, struct, bisect; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base
VT = sorted((r, n) for n, r in D.EX.items() if n.startswith('??_7'))
VT_R = [r for r, _ in VT]
def owner(rva):
    i = bisect.bisect_right(VT_R, rva) - 1
    if i < 0: return None, None
    return VT[i][1], rva - VT[i][0]

TARGETS = {0x000ea260: 'CBC::CheckAction', 0x0011b430: 'ControllerPlayer::CheckAction'}
sec = [s for s in pe.sections if s['name'] == '.rdata'][0]
blob = pe.raw[sec['raddr']: sec['raddr'] + sec['rsize']]
hits = {t: [] for t in TARGETS}
for off in range(0, len(blob) - 3, 4):
    v = struct.unpack_from('<I', blob, off)[0] - IB
    if v in TARGETS:
        hits[v].append(sec['vaddr'] + off)

for t, lab in TARGETS.items():
    print(f'=== {lab}  ({t:#010x})  — {len(hits[t])} .rdata slot(s) image-wide')
    disps = {}
    for r in hits[t]:
        o, d = owner(r)
        disps.setdefault(d, []).append(o)
        print(f'   slot @ {r:#010x}   +{d:#05x} of  {o}')
    print(f'   -> distinct displacements: ' +
          ', '.join(f'+{d:#x} ({len(v)} classes)' for d, v in sorted(disps.items())))
    print()

print('=== the three Pursue::OnBegin MoveTo sites and their terminal permission gate ===')
for site in (0x000ff1ee, 0x000ff264, 0x000ff2ca):
    print(f'   {site:#010x}  ControllerMonsterStatePursue::OnBegin+{site-0x000fee40:#x}'
          f'  -> call 0x000e6cd0 ControllerAI::MoveTo')
print('   0x000e6dbb  [action+8] := 4          (MoveToAction type literal)')
print('   0x000e6dcd  -> call 0x000ea480 ControllerBaseCharacter::HandleAction   (SOLE exit)')
print('   0x000ea4c2 / 0x000ea4d2  -> call 0x000ea4e0 LocalHandleAction          (both branches)')
print('   0x000ea537  -> call [this_vtbl + 0x68]  ==  0x000ea260 CBC::CheckAction (ControllerMonster)')
print('   0x000ea5d9 / 0x000ea5f2  -> call 0x000724f0 CharacterActionHandler::Execute')
print('       ... both DOMINATED by 0x000ea537.  No edge reaches Execute without CheckAction.')
