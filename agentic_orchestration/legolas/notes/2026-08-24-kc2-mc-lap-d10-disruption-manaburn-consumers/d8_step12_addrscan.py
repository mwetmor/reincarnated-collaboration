"""D-8 step 12 — second, INDEPENDENT search technique for hidden entries into the freeze/petrify
lane: scan the ENTIRE image for the 4-byte little-endian VA of each entry point (a function-pointer
take or a vtable placement would show here even though no E8/E9 does).  READ-ONLY."""
import sys, struct; sys.path.insert(0,'.')
import d4b_dis as D
pe=D.pe; IB=pe.image_base
TG={'Character::BeginFreeze':0x0005b020,'Character::EndFreeze':0x0005b110,
    'Character::BeginPetrify':0x0005b150,'Character::EndPetrify':0x0005b240,
    'Character::StartInvoluntaryEffect':0x0005acc0,'Character::StopInvoluntaryEffect':0x0005adb0,
    'ControllerPlayer::BeginImmobilize':0x000f6a10,
    'DefaultBeginImmobilizeAction':0x0011f480}
raw=pe.raw
for nm,rva in TG.items():
    pat=struct.pack('<I', IB+rva); hits=[]; i=raw.find(pat)
    while i!=-1:
        # translate file offset back to an RVA if it lies in a mapped section
        r=None
        for s in pe.sections:
            if s['raddr']<=i<s['raddr']+s['rsize']: r=s['vaddr']+(i-s['raddr']); sec=s['name']; break
        hits.append((i,r,sec if r is not None else '-'))
        i=raw.find(pat,i+1)
    print(f'=== {nm} @ {rva:#010x}  VA {IB+rva:#010x}: {len(hits)} 4-byte occurrences image-wide')
    for off,r,sec in hits:
        print(f'   file{off:#010x}  rva {r if r is None else hex(r)}  sec={sec}  nearest={D.nearest(r) if r else "-"}')
