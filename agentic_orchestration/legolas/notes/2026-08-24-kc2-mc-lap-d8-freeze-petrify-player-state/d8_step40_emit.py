"""D-8 step 40 — emit the two machine-readable products:
  evidence/d8_family_request_matrix.csv  — family x request-slot x verdict x RVA (the ask)
  evidence/d8_routing_and_lifecycle.csv  — every decoded routing/lifecycle rule, RVA-pinned
Every verdict is read off a vtable slot occupant in Game.dll; nothing here is asserted.  READ-ONLY."""
import sys, struct, re, csv; sys.path.insert(0,'.')
import d4b_dis as D
from d8_step8_slotnames import NAMES, slots, IDLE
pe=D.pe; IB=pe.image_base; N=83

def lines(rva,k=8):
    try: return [x.split('  ',3)[-1].strip() for x in D.disasm(rva,k)[:k]]
    except Exception: return []
def classify(rva):
    ls=lines(rva,4); num=lambda s: bool(re.fullmatch(r'(0x[0-9a-f]+|\d+)',s))
    if not ls: return 'EMPTY-BODY'
    if len(ls)==1 and (num(ls[0]) or ls[0]==''): return 'STUB-ret'
    if len(ls)>=2 and ls[0]=='al, al' and num(ls[1]): return 'STUB-false'
    return 'IMPL'

# family -> (enum, Character entry RVA, controller slot, controller-slot symbol, player state class)
FAM = [
  ('Stun',       0x2a, 0x0005acc0, 0x090, 'BeginStun@ControllerPlayer',       'Stunned',     'ref'),
  ('Sleep',      0x2b, 0x0005acc0, 0x0a8, 'BeginSleep@ControllerPlayer',      'Sleep',       'ref'),
  ('Trap',       0x2c, 0x0005afc0, 0x0b8, 'BeginTrap@ControllerPlayer',       'Trapped',     'ref'),
  ('Freeze',     0x2d, 0x0005b020, 0x0b0, 'BeginImmobilize@ControllerPlayer', 'Immobilized', 'D-8'),
  ('Petrify',    0x2e, 0x0005b150, 0x0b0, 'BeginImmobilize@ControllerPlayer', 'Immobilized', 'D-8'),
  ('Immobilize', 0x2f, 0x0005b280, 0x0b0, 'BeginImmobilize@ControllerPlayer', 'Immobilized', 'ref'),
  ('Knockdown',  0x30, 0x0005b2e0, 0x0c0, 'BeginKnockdown@ControllerPlayer',  'KnockedDown', 'ref'),
]
STATE_VT={c:D.EX[f'??_7ControllerPlayerState{c}@GAME@@6B@']
          for c in ('Stunned','Sleep','Trapped','Immobilized','KnockedDown')}
TAB={c:slots(v) for c,v in STATE_VT.items()}
REQ=sorted([k for k in range(N) if NAMES[k].startswith('Request')]+[54,55,56,57])

rows=[]
for fam,enum,begin_rva,cslot,csym,state,prov in FAM:
    t=TAB[state]
    for k in REQ:
        permitted = (t[k]==IDLE[k])
        verdict = 'PERMITTED' if permitted else classify(t[k])
        rows.append(dict(
            family=fam, combat_attribute_type=hex(enum),
            character_entry_fn=f'Character::Begin{ "Freeze" if fam=="Freeze" else "Petrify" if fam=="Petrify" else fam}',
            character_entry_rva=hex(begin_rva),
            controller_vtable_off=hex(cslot), controller_slot_symbol=csym,
            player_state_class=f'ControllerPlayerState{state}',
            player_state_vftable_rva=hex(STATE_VT[state]),
            vtable_slot=k, vtable_offset=hex(4*k), request=NAMES[k],
            verdict=verdict,
            occupant_rva=hex(t[k]), occupant_symbol=D.nearest(t[k]) or '',
            idle_occupant_rva=hex(IDLE[k]),
            provenance='decoded', lap=prov))
with open('evidence/d8_family_request_matrix.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f'-> evidence/d8_family_request_matrix.csv  ({len(rows)} rows, {len(FAM)} families x {len(REQ)} slots)')

R=[]
def r(id_,claim,rva,fn,kind='decoded',note=''):
    R.append(dict(id=id_,claim=claim,rva=rva,fn=fn,kind=kind,note=note))
r('D8-1','StartInvoluntaryEffect(0x2d) -> Character::BeginFreeze','0x0005ad6a','StartInvoluntaryEffect@Character')
r('D8-2','StartInvoluntaryEffect(0x2e) -> Character::BeginPetrify','0x0005ad7a','StartInvoluntaryEffect@Character')
r('D8-3','BeginFreeze limb B: controller vtable +0xb0 = BeginImmobilize@ControllerPlayer','0x0005b05a','Character::BeginFreeze')
r('D8-4','BeginPetrify limb B: controller vtable +0xb0 = BeginImmobilize@ControllerPlayer','0x0005b18a','Character::BeginPetrify')
r('D8-5','ControllerPlayer vtable +0xb0 occupant','0x000f6a10','BeginImmobilize@ControllerPlayer')
r('D8-6','BeginImmobilize@ControllerPlayer forwards to CURRENT state slot 40 (+0xa0)','0x000f6a2e','BeginImmobilize@ControllerPlayer')
r('D8-7','ControllerPlayerStateUseSkill slot 40 IS Idle\'s occupant -> a channelling player takes the Idle path','0x0011ff90','BeginImmobilize@ControllerPlayerStateIdle')
r('D8-8','Idle BeginImmobilize tail-jmps to DefaultBeginImmobilizeAction','0x0011ff90','BeginImmobilize@ControllerPlayerStateIdle')
r('D8-9','DefaultBeginImmobilizeAction calls SetState("Immobilized") with ZEROED ControllerAIStateData','0x0011f4ef','DefaultBeginImmobilizeAction@ControllerPlayerState')
r('D8-10','state-name literal, length 0xb','0x0052ff18','.rdata "Immobilized"','decoded','VA 0x1052ff18')
r('D8-11','OnBegin@Immobilized issues ImmobilizeAction (code 0xd, prio 250.0f) via HandleAction','0x0012320e','OnBegin@ControllerPlayerStateImmobilized')
r('D8-12','Execute@ImmobilizeAction calls SkillManager::StopCurrentSkill','0x0006f722','Execute@ImmobilizeAction')
r('D8-13','StopCurrentSkill clears current-skill id then calls skill vtable +0x24c (StopSkill) if IsRunning','0x0043ea3e','StopCurrentSkill@SkillManager')
r('D8-14','StopSkill@Skill_AttackRadiusSpin calls vtable +0x394 = StopSpinning','0x003e8e38','StopSkill@Skill_AttackRadiusSpin','decoded','shared body with Skill_AttackRadiusGrow / Skill_AttackSpellDrain')
r('D8-15','StopSpinning clears the spin flag Skill+0x4f4','0x003eba0e','StopSpinning@Skill_AttackRadiusSpin')
r('D8-16','ActivateNow sets the spin flag Skill+0x4f4 = 1','0x003eb2ab','ActivateNow@Skill_AttackRadiusSpin')
r('D8-17','CollectPassiveDefenseAttributes early-returns when Skill+0x4f4 == 0','0x003ebdc6','CollectPassiveDefenseAttributes@Skill_AttackRadiusSpin')
r('D8-18','=> EoR defensiveCrowdControl is CHANNEL-CONDITIONAL (decoded, not assumed)','0x003ebdc0','CollectPassiveDefenseAttributes@Skill_AttackRadiusSpin')
r('D8-19','SkillManager::GetDefenseAttributes gates each skill on vtable +0xe4 = GetCurrentLevel (rank>0), NOT on active','0x0043ba40','GetDefenseAttributes@SkillManager')
r('D8-20','ExecuteImmobilize@Character sets the movement-lock byte Character+0x1cb7 = 1','0x00048835','ExecuteImmobilize@Character')
r('D8-21','ExecuteStun@Character does NOT touch Character+0x1cb7','0x000486a0','ExecuteStun@Character','clean-negative','14 disp32-0x1cb7 sites scanned in .text; none in ExecuteStun')
r('D8-22','DisallowsMovement@Character is literally the +0x1cb7 byte','0x0005b3d0','DisallowsMovement@Character')
r('D8-23','+0x1cb7 also gates MoveToAction / WalkAction / JumpAttackAction / EvadeAction at Execute time','0x0006c64b','Execute@MoveToAction (+3 siblings)')
r('D8-24','StopInvoluntaryEffect(0x2d) -> Character::EndFreeze','0x0005ae4b','StopInvoluntaryEffect@Character')
r('D8-25','StopInvoluntaryEffect(0x2e) -> Character::EndPetrify','0x0005ae59','StopInvoluntaryEffect@Character')
r('D8-26','EndFreeze/EndPetrify limb B: controller vtable +0xb4 = EndImmobilize@ControllerPlayer','0x0005b12e','Character::EndFreeze')
r('D8-27','EndImmobilize@ControllerPlayerStateImmobilized calls SetState("Idle") - no skill restart','0x0012334f','EndImmobilize@ControllerPlayerStateImmobilized')
r('D8-28','OnUpdate@Immobilized is the shared ret-4 stub: NO self-timer at all','0x000084d0','OnUpdate slot 70 occupant','decoded','Stunned by contrast has a real OnUpdate at 0x00123490')
r('D8-29','Start/StopInvoluntaryEffect have EXACTLY ONE call site each: UpdateFxAndInfluence','0x0020a104','UpdateFxAndInfluence@DurationDamageManager','clean-negative','+0x0020a10d for Start')
r('D8-30','ladder order 0x2f>0x2e>0x2d>0x2c>0x2b>0x2a>0x30>0x31, first hit wins, re-evaluated every update','0x00209fd0','UpdateFxAndInfluence@DurationDamageManager')
r('D8-31','BeginFreeze limb A: SpecialCharHandler from records/fx/damagedefault/dmgspecial_freeze_handler.dbr','0x0005b0a0','Character::BeginFreeze','decoded','handler cached at Character+0x2e84')
r('D8-32','BeginPetrify limb A: ... dmgspecial_petrify_handler.dbr','0x0005b1d0','Character::BeginPetrify','decoded','handler cached at Character+0x2e88')
r('D8-33','both handler records carry handlerType="Freeze" -> SpecialCharHandler_IcyCharacter','0x00462390','CreateHandler@SpecialCharHandler')
r('D8-34','handler limb is PURE PRESENTATION: 7 DBR fields = 3 sounds, 1 chunk mesh, 1 overlay texture, template, handlerType','n/a','database.arz','decoded','sha256 8cdeff12...')
r('D8-35','handler vtable +8 / +0xc = Enable/Disable@SpecialCharHandler_IcyCharacter (graphics only)','0x00463080','SpecialCharHandler_IcyCharacter')
r('D8-36','no ControllerPlayerStateFrozen / ...Petrified class exists','n/a','export table','clean-negative','25,091 exports searched')
r('D8-37','IsFrozenOrPetrified@Character reads the FX handler enabled byte; ONE caller: Update@Skill_Shapeshift','0x0005b3a0','IsFrozenOrPetrified@Character','clean-negative','not on the KC2 kit path')
r('D8-38','no break-on-damage / break-on-input / cleanse path into the freeze-petrify lane','n/a','two search techniques','clean-negative','E8/E9 rel32 xref + image-wide 4-byte VA scan, both zero outside the two known sites')
r('D8-39','ImDead@DurationDamageManager is the only reachable full clear of the fixed list (death path)','0x00209e50','ImDead@DurationDamageManager')
r('D8-40','RemoveAllDamages is vtable slot 6 with no reachable caller found by either technique','0x00208f40','RemoveAllDamages@DurationDamageManager','residual','R-D8-1')
r('D8-41','Immobilized vs Stunned full 83-slot diff = 6 slots, ALL 16 request/select slots identical','n/a','vtable diff','decoded','dtor, EndStun/EndImmobilize hooks, OnBegin, OnEnd, OnUpdate')
r('D8-42','EoR defensiveCrowdControl / ...MaxResist = 26-rank arrays 10.0 -> 25.0','n/a','records/skills/playerclass09/eyeofreckoning1.dbr','decoded','Class=Skill_AttackRadiusSpin, GDX2.arz')
with open('evidence/d8_routing_and_lifecycle.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','claim','rva','fn','kind','note']); w.writeheader(); w.writerows(R)
print(f'-> evidence/d8_routing_and_lifecycle.csv  ({len(R)} rows)')
