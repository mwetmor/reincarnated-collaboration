"""STEP 6 — bank the load-bearing disassembly listings as evidence files, so the verdict is
re-checkable without re-running capstone."""
import sys; sys.path.insert(0,'.')
import d4b_dis as D
CUTS = [
 ('E1-addamagetoaccumulator-roll-and-ctor.asm','DamageAttributeDur::AddDamageToAccumulator (.dbr roll -> CombatAttributeDurDamage ctor, inlined)',0x1425b0,205),
 ('E2-combatattributedurdamage-ctor.asm','CombatAttributeDurDamage::ctor  [+0x1c]=damage [+0x20]=[+0x24]=duration',0xd7c80,35),
 ('E3-combatattributedurdamage-process.asm','CombatAttributeDurDamage::Process  (percent modifier only)',0xd7dd0,130),
 ('E4-combatattributedurdamage-execute.asm','CombatAttributeDurDamage::Execute -> DurationDamageManager::AddDamage',0xd80c0,25),
 ('E5-durationdamagemanager-adddamage.asm','DurationDamageManager::AddDamage (damage stored verbatim)',0x208a30,210),
 ('E6-entry-insert-merge.asm','entry vtable slot1 @0x20d6b0 — THE DECISIVE SITE: nTicks=dur*10.0, perTick=dmg*0.1',0x20d6b0,200),
 ('E7-entry-pertick-sum.asm','entry vtable slot2 @0x20da10 — per-tick sum over 24-byte instances',0x20da10,140),
 ('E8-durationdamagemanager-update.asm','DurationDamageManager::Update — 100 ms (0x64) DoT tick accumulator',0x207f40,80),
 ('E9-durationdamagemanager-executedamage.asm','DurationDamageManager::ExecuteDamage -> CombatManager::ApplyDamage',0x208370,270),
]
for fn, title, rva, n in CUTS:
    body = D.disasm(rva, n, stop_at_ret=False)
    open('evidence/'+fn,'w').write(f'; {title}\n; Game.dll RVA {rva:#010x}  (image_base {D.pe.image_base:#x})\n; READ-ONLY disassembly, capstone x86-32\n\n' + '\n'.join(body) + '\n')
    print('wrote evidence/'+fn, f'({len(body)} lines)')
