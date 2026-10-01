import sys, d4b_dis as D, d8_lib as L, e_dis as E, bisect, struct
OUT=sys.argv[1]
def w(name, lines, hdr):
    open(f"{OUT}/evidence/{name}","w").write(hdr+"\n"+"\n".join(lines)+"\n")
G="Game.dll Edition IV 32-bit (sha256 e75925d1403e4fab34390e9fe84a2a8b6c1cccdd5b32904fab7c149500068126); RVAs; capstone x86-32; READ-ONLY"
w("01_CloseEnoughToUseSkill_ControllerMonster.txt", L.bounded(0xd18a0,300), "?CloseEnoughToUseSkill@?$ControllerAIStateT@VControllerMonster@GAME@@VMonster@2@@GAME@@UAE_NII@Z  "+G+"\nreturns (GetTargetDistance(owner,target,skill) + this->vslot0x12c(skill)) >= centre_distance(owner,target)")
w("02_GetTargetDistance_Character.txt", L.bounded(0x491f0,300), "?GetTargetDistance@Character@GAME@@SAMIII@Z  "+G+"\n= skill->vslot0x120 (Skill::GetRange) + owner->vslot0xe4 (GetRadius) [+ target->vslot0xe4 if target is a Character]")
w("03_GetSkillUseTolerance.txt", L.bounded(0x62230,10)[:3], "?GetSkillUseTolerance@?$ControllerAIStateT@...@@MBEMI@Z (shared by every ControllerAIStateT incl. ControllerMonster; vslot 0x12c of ControllerMonsterStateAttack)  "+G+"\nreturns constant 0.5")
w("04_Skill_GetRange.txt", L.bounded(0x3c01a0,60)[:24], "?GetRange@Skill@GAME@@UBEMXZ (Skill vtable +0x120 on 126 of 129 Skill_* vtables)  "+G+"\nswitch(this->vslot0x11c = GetRangeProfile = [this+0x8c]) 0..5 -> gGameEngine+0xc48/c4c/c50/c54/c58/c5c ; default 1.0")
w("05_GameEngine_LoadFromDatabase_ranges.txt", D.disasm(0x24e2a6,40,stop_at_ret=False)[:36], "?LoadFromDatabase@GameEngine@GAME@@ excerpt  "+G+"\nmeleeRange->+0xc48 shortRange->+0xc4c moderateRange->+0xc50 longRange->+0xc54 maximumRange->+0xc58 bossRange->+0xc5c")
w("06_Skill_LoadResources_distanceProfile.txt", D.disasm(0x3be674,70,stop_at_ret=False)[:62], "?LoadResources@Skill@GAME@@ excerpt  "+G+"\ndistanceProfile: Melee->0 Short->1 Moderate->2 Long->3 Maximum->4 Boss->5 into [skill+0x8c]; unrecognised/absent leaves the ctor value (??0Skill@GAME@@QAE@XZ @0x3b2fe7: mov [esi+0x8c],0 = Melee)")
w("07_IsSkillInProperRange.txt", L.bounded(0xf8660,300), "?IsSkillInProperRange@ControllerMonster@GAME@@QBE_NIW4SkillUseRange@@@Z  "+G+"\nenum 0 (AnyRange/unparsed) -> TRUE; 1/2/3 -> [min,max] at +0x550/+0x558/+0x560; d_edge = max(0.5, centre - (r_target + r_self)); admit iff min < d_edge < max")
w("08_SkillUseRange_parse_and_band_load.txt", D.disasm(0xfdc50,30,stop_at_ret=False)+["----"]+D.disasm(0x2dad45,70,stop_at_ret=False)[:62], "band enum parser (ShortRange=1 MediumRange=2 LongRange=3 else 0) + ?InitSkillsInController@Monster excerpt loading short/medium/longRange{Min,Max} into ControllerMonster+0x550..0x564 (binary defaults 0/4, 4/8, 8/16)  "+G)
w("09_SpellBeam_GetRange_override.txt", L.bounded(0x3f0420,20)[:12], "?GetRange@Skill_AttackSpellBeam@GAME@@ (also Cone/Drain vtables): IsRunning ? 100.0 : Skill::GetRange  "+G)
# Engine.dll Actor::GetRadius
i=bisect.bisect_right(E.SORTED_RVA,0x25e30); end=E.SORTED_RVA[i]
el=[l for l in E.disasm(0x25e30,40,stop_at_ret=False) if int(l.split()[0],16)<end]
w("10_Engine_Actor_GetRadius.txt", el, "?GetRadius@Actor@GAME@@UBEMXZ  Engine.dll Edition IV 32-bit (sha256 f18e8658efc995e7...) = actorRadius([+0x2a4], loaded by Actor::Load @0x243df, default 1.0) x |vec(+0x370,+0x374,+0x378)|; ??_7Actor@GAME@@6BObject@1@@ +0xe4 -> this function")
# Spawn path
k=[k for k in D.EX if k.startswith('?PlaceNextObject@ProxyAmbush')][0]
ls=L.bounded(D.EX[k],600); j=[i for i,l in enumerate(ls) if '0x318]' in l][0]
w("11_ProxyAmbush_PlaceNextObject_EnableSpawnAnimation.txt", ls[j-8:j+6], k+"  "+G+"\nunconditional call [vtable+0x318] = Character::EnableSpawnAnimation (Character vtable +0x318; Monster override 0x2dded0 sets [+0x1c64]=1) immediately before GameEngine::FastSpawnEntity")
w("12_CharacterHandlerUpdate_SpawnAction.txt", D.disasm(0xea56b,40,stop_at_ret=False)[:30]+["---- JustSpawnedWithAnimation (Character vtable +0x320)"]+L.bounded(0x53570,20)[:9]+["---- SpawnAction::Execute"]+L.bounded(0x709c0,60)[:40], "?CharacterHandlerUpdate@ControllerBaseCharacter@GAME@@ excerpt  "+G+"\nfirst handler update: JustSpawnedWithAnimation() ([+0x1c64]!=0 && [+0x12c]<30) ? new SpawnAction (action type 19) : new IdleAction")
print("ok")
