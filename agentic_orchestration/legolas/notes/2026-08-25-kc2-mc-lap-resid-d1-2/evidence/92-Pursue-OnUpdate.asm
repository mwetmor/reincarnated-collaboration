=== 92-Pursue-OnUpdate RVA 0x000ff380 sym=?OnUpdate@ControllerMonsterStatePursue@GAME@@MAEXH@Z ===
  0x000ff380  push     ebp
  0x000ff381  mov      ebp, esp
  0x000ff383  mov      eax, dword ptr fs:[0]
  0x000ff389  push     -1
  0x000ff38b  push     0x104c84be
  0x000ff390  push     eax
  0x000ff391  mov      dword ptr fs:[0], esp
  0x000ff398  sub      esp, 0x80
  0x000ff39e  push     ebx
  0x000ff39f  mov      ebx, ecx
  0x000ff3a1  push     esi
  0x000ff3a2  push     edi
  0x000ff3a3  cmp      byte ptr [ebx + 0x1d], 0
  0x000ff3a7  je       0x100ff4d9
  0x000ff3ad  mov      edi, dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000ff3b3  lea      ecx, [ebp - 0x2c]
  0x000ff3b6  call     edi
  0x000ff3b8  mov      ecx, dword ptr [ebx + 4]
  0x000ff3bb  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff3c0  mov      esi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ff3c6  push     dword ptr [eax]
  0x000ff3c8  call     esi
  0x000ff3ca  mov      ecx, eax
  0x000ff3cc  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000ff3d1  test     eax, eax
  0x000ff3d3  je       0x100ff451
  0x000ff3d5  mov      ecx, eax
  0x000ff3d7  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x000ff3dd  mov      ecx, dword ptr [ebx + 4]
  0x000ff3e0  movups   xmm0, xmmword ptr [eax]
  0x000ff3e3  movups   xmmword ptr [ebp - 0x4c], xmm0
  0x000ff3e7  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff3ec  mov      ecx, dword ptr [ebx + 4]
  0x000ff3ef  mov      eax, dword ptr [eax + 8]
  0x000ff3f2  mov      dword ptr [ebp + 8], eax
  0x000ff3f5  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff3fa  mov      eax, dword ptr [eax]
  0x000ff3fc  mov      dword ptr [ebp - 0x10], eax
  0x000ff3ff  mov      eax, dword ptr [ebx + 8]
  0x000ff402  test     eax, eax
  0x000ff404  jne      0x100ff418
  0x000ff406  mov      eax, dword ptr [ebx + 4]
  0x000ff409  push     dword ptr [eax + 0x24]
  0x000ff40c  call     esi
  0x000ff40e  mov      ecx, eax
  0x000ff410  call     0x1000b0c0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd00
  0x000ff415  mov      dword ptr [ebx + 8], eax
  0x000ff418  lea      ecx, [ebp - 0x4c]
  0x000ff41b  push     ecx
  0x000ff41c  push     dword ptr [ebp + 8]
  0x000ff41f  lea      ecx, [ebp - 0x84]
  0x000ff425  push     dword ptr [ebp - 0x10]
  0x000ff428  push     ecx
  0x000ff429  mov      ecx, eax
  0x000ff42b  call     0x10049980   ; -> ?GetMoveToPoint@Character@GAME@@QBE?AVWorldVec3@2@IIABV32@@Z
  0x000ff430  mov      ecx, dword ptr [ebx + 4]
  0x000ff433  lea      edx, [ebp - 0x2c]
  0x000ff436  push     edx
  0x000ff437  lea      edx, [ebp - 0x84]
  0x000ff43d  movups   xmm0, xmmword ptr [eax]
  0x000ff440  push     edx
  0x000ff441  movups   xmmword ptr [ebp - 0x2c], xmm0
  0x000ff445  mov      eax, dword ptr [ecx]
  0x000ff447  call     dword ptr [eax + 0x60]
  0x000ff44a  movups   xmm0, xmmword ptr [eax]
  0x000ff44d  movups   xmmword ptr [ebp - 0x2c], xmm0
  0x000ff451  lea      ecx, [ebp - 0x2c]
  0x000ff454  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x000ff45a  test     eax, eax
  0x000ff45c  jne      0x100ff4c2
  0x000ff45e  push     0x1052ce5c
  0x000ff463  lea      ecx, [ebp - 0x54]
  0x000ff466  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff46b  mov      dword ptr [ebp - 4], 0
  0x000ff472  mov      ecx, dword ptr [ebx + 4]
  0x000ff475  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff47a  lea      ecx, [ebp - 0x84]
  0x000ff480  mov      esi, dword ptr [eax]
  0x000ff482  call     edi
  0x000ff484  mov      ecx, dword ptr [ebx + 4]
  0x000ff487  mov      dword ptr [ebp - 0x74], esi
  0x000ff48a  mov      dword ptr [ebp - 0x70], 0
  0x000ff491  movups   xmm0, xmmword ptr [eax]
  0x000ff494  lea      eax, [ebp - 0x74]
  0x000ff497  mov      dword ptr [ebp - 0x6c], 0
  0x000ff49e  push     eax
  0x000ff49f  lea      eax, [ebp - 0x54]
  0x000ff4a2  push     eax
  0x000ff4a3  movups   xmmword ptr [ebp - 0x68], xmm0
  0x000ff4a7  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000ff4ac  mov      edx, dword ptr [ebp - 0x40]
  0x000ff4af  cmp      edx, 0x10
  0x000ff4b2  jb       0x100ff4c2
  0x000ff4b4  mov      ecx, dword ptr [ebp - 0x54]
  0x000ff4b7  inc      edx
  0x000ff4b8  push     1
  0x000ff4ba  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x000ff4bf  add      esp, 4
  0x000ff4c2  pop      edi
  0x000ff4c3  pop      esi
  0x000ff4c4  mov      byte ptr [ebx + 0x1d], 0
  0x000ff4c8  pop      ebx
  0x000ff4c9  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff4cc  mov      dword ptr fs:[0], ecx
  0x000ff4d3  mov      esp, ebp
  0x000ff4d5  pop      ebp
  0x000ff4d6  ret      4
  0x000ff4d9  mov      ecx, dword ptr [ebx + 4]
  0x000ff4dc  mov      esi, dword ptr [ebp + 8]
  0x000ff4df  mov      dword ptr [ebx + 0x18], 0
  0x000ff4e6  cmp      dword ptr [ecx + 0x2fc], 0
  0x000ff4ed  je       0x100ff547
  0x000ff4ef  sub      dword ptr [ebx + 0x10], esi
  0x000ff4f2  jns      0x100ff547
  0x000ff4f4  push     0x1052ce74
  0x000ff4f9  lea      ecx, [ebp - 0x8c]
  0x000ff4ff  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff504  mov      dword ptr [ebp - 4], 1
  0x000ff50b  lea      ecx, [ebp - 0x4c]
  0x000ff50e  mov      dword ptr [ebp - 0x58], 0
  0x000ff515  mov      dword ptr [ebp - 0x54], 0
  0x000ff51c  mov      dword ptr [ebp - 0x50], 0
  0x000ff523  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000ff529  mov      ecx, dword ptr [ebx + 4]
  0x000ff52c  lea      eax, [ebp - 0x58]
  0x000ff52f  push     eax
  0x000ff530  lea      eax, [ebp - 0x8c]
  0x000ff536  push     eax
  0x000ff537  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000ff53c  lea      ecx, [ebp - 0x8c]
  0x000ff542  jmp      0x100ff77c   ; -> ?OnUpdate@ControllerMonsterStatePursue@GAME@@MAEXH@Z+0x3fc
  0x000ff547  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff54c  mov      ecx, dword ptr [ebx + 4]
  0x000ff54f  push     dword ptr [eax]
  0x000ff551  call     0x100fb220   ; -> ?IsEnemyValid@ControllerMonster@GAME@@QBE_NI@Z
  0x000ff556  test     al, al
  0x000ff558  jne      0x100ff573
  0x000ff55a  push     0x1052ce6c
  0x000ff55f  lea      ecx, [ebp - 0x8c]
  0x000ff565  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff56a  mov      dword ptr [ebp - 4], 2
  0x000ff571  jmp      0x100ff50b   ; -> ?OnUpdate@ControllerMonsterStatePursue@GAME@@MAEXH@Z+0x18b
  0x000ff573  sub      dword ptr [ebx + 0x14], esi
  0x000ff576  jns      0x100ff5e7
  0x000ff578  mov      ecx, dword ptr [ebx + 4]
  0x000ff57b  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff580  push     dword ptr [eax + 8]
  0x000ff583  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ff589  mov      ecx, eax
  0x000ff58b  call     0x1000d4f0   ; -> ?CreateUISummaryText@AmbientCharacter@GAME@@UBEXW4GameTextClass@2@AAV?$vector@UGameTextLine@GAME@@@mem@@@Z+0x7e0
  0x000ff590  mov      ecx, eax
  0x000ff592  test     ecx, ecx
  0x000ff594  je       0x100ff5e0
  0x000ff596  mov      eax, dword ptr [ecx]
  0x000ff598  mov      eax, dword ptr [eax + 0x280]
  0x000ff59e  call     eax
  0x000ff5a0  test     al, al
  0x000ff5a2  je       0x100ff5e0
  0x000ff5a4  mov      ecx, dword ptr [ebx + 4]
  0x000ff5a7  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff5ac  mov      ecx, dword ptr [ebx + 4]
  0x000ff5af  push     0
  0x000ff5b1  push     dword ptr [eax]
  0x000ff5b3  call     0x100f8020   ; -> ?ChooseBestSkill@ControllerMonster@GAME@@QAEII_N@Z
  0x000ff5b8  mov      ecx, dword ptr [ebx + 4]
  0x000ff5bb  mov      edi, eax
  0x000ff5bd  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff5c2  cmp      edi, dword ptr [eax + 8]
  0x000ff5c5  je       0x100ff5e0
  0x000ff5c7  push     0x1052ce84
  0x000ff5cc  lea      ecx, [ebp - 0x54]
  0x000ff5cf  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff5d4  mov      dword ptr [ebp - 4], 3
  0x000ff5db  jmp      0x100ff73f   ; -> ?OnUpdate@ControllerMonsterStatePursue@GAME@@MAEXH@Z+0x3bf
  0x000ff5e0  mov      dword ptr [ebx + 0x14], 0xc8
  0x000ff5e7  mov      ecx, dword ptr [ebx + 4]
  0x000ff5ea  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff5ef  mov      ecx, dword ptr [ebx + 4]
  0x000ff5f2  mov      esi, dword ptr [eax + 8]
  0x000ff5f5  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff5fa  mov      edx, dword ptr [ebx]
  0x000ff5fc  mov      ecx, ebx
  0x000ff5fe  push     esi
  0x000ff5ff  push     dword ptr [eax]
  0x000ff601  mov      eax, dword ptr [edx + 8]
  0x000ff604  call     eax
  0x000ff606  test     al, al
  0x000ff608  jne      0x100ff718
  0x000ff60e  mov      ecx, dword ptr [ebx + 4]
  0x000ff611  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff616  mov      edx, dword ptr [ebx]
  0x000ff618  mov      ecx, dword ptr [eax + 8]
  0x000ff61b  lea      eax, [ebx + 0x20]
  0x000ff61e  push     eax
  0x000ff61f  mov      eax, dword ptr [edx + 0xc]
  0x000ff622  push     ecx
  0x000ff623  mov      ecx, ebx
  0x000ff625  call     eax
  0x000ff627  test     al, al
  0x000ff629  jne      0x100ff718
  0x000ff62f  mov      ecx, ebx
  0x000ff631  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff636  movss    xmm0, dword ptr [eax + 0x3068]
  0x000ff63e  comiss   xmm0, dword ptr [0x105f5708]   ; f32=0 i32=0 f64=0
  0x000ff645  movss    dword ptr [ebp + 8], xmm0
  0x000ff64a  jbe      0x100ff781
  0x000ff650  mov      ecx, ebx
  0x000ff652  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff657  cmp      byte ptr [ebx + 0x1c], 0
  0x000ff65b  mov      eax, dword ptr [eax + 0x950]
  0x000ff661  movups   xmm0, xmmword ptr [eax + 0x14]
  0x000ff665  movups   xmmword ptr [ebp - 0x3c], xmm0
  0x000ff669  je       0x100ff781
  0x000ff66f  mov      ecx, ebx
  0x000ff671  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff676  mov      ecx, eax
  0x000ff678  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x000ff67e  lea      ecx, [ebp - 0x68]
  0x000ff681  movups   xmm0, xmmword ptr [eax]
  0x000ff684  lea      eax, [ebp - 0x3c]
  0x000ff687  push     eax
  0x000ff688  lea      eax, [ebp - 0x1c]
  0x000ff68b  push     eax
  0x000ff68c  movups   xmmword ptr [ebp - 0x68], xmm0
  0x000ff690  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x000ff696  movss    xmm1, dword ptr [eax + 4]
  0x000ff69b  movss    xmm2, dword ptr [eax]
  0x000ff69f  movss    xmm0, dword ptr [eax + 8]
  0x000ff6a4  mulss    xmm2, xmm2
  0x000ff6a8  mulss    xmm1, xmm1
  0x000ff6ac  mulss    xmm0, xmm0
  0x000ff6b0  addss    xmm2, xmm1
  0x000ff6b4  addss    xmm2, xmm0
  0x000ff6b8  xorps    xmm0, xmm0
  0x000ff6bb  ucomiss  xmm2, xmm0
  0x000ff6be  lahf     
  0x000ff6bf  test     ah, 0x44
  0x000ff6c2  jnp      0x100ff6cb
  0x000ff6c4  xorps    xmm0, xmm0
  0x000ff6c7  sqrtss   xmm0, xmm2
  0x000ff6cb  comiss   xmm0, dword ptr [ebp + 8]
  0x000ff6cf  jbe      0x100ff781
  0x000ff6d5  mov      ecx, dword ptr [ebx + 4]
  0x000ff6d8  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff6dd  mov      ecx, dword ptr [ebx + 4]
  0x000ff6e0  mov      esi, dword ptr [eax + 8]
  0x000ff6e3  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff6e8  push     ecx
  0x000ff6e9  mov      ecx, dword ptr [ebx + 4]
  0x000ff6ec  mov      dword ptr [esp], 0x3f800000
  0x000ff6f3  push     5
  0x000ff6f5  push     esi
  0x000ff6f6  push     dword ptr [eax]
  0x000ff6f8  lea      eax, [ebp - 0x3c]
  0x000ff6fb  push     eax
  0x000ff6fc  call     0x100e6cd0   ; -> ?MoveTo@ControllerAI@GAME@@QAEXABVWorldVec3@2@IIW4AnimationSet_Type@2@M@Z
  0x000ff701  pop      edi
  0x000ff702  pop      esi
  0x000ff703  mov      byte ptr [ebx + 0x1c], 0
  0x000ff707  pop      ebx
  0x000ff708  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff70b  mov      dword ptr fs:[0], ecx
  0x000ff712  mov      esp, ebp
  0x000ff714  pop      ebp
  0x000ff715  ret      4
  0x000ff718  mov      ecx, dword ptr [ebx + 4]
  0x000ff71b  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff720  push     0x1052ce7c
  0x000ff725  lea      ecx, [ebp - 0x54]
  0x000ff728  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff72d  mov      dword ptr [ebp - 4], 4
  0x000ff734  mov      ecx, dword ptr [ebx + 4]
  0x000ff737  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff73c  mov      edi, dword ptr [eax + 8]
  0x000ff73f  mov      ecx, dword ptr [ebx + 4]
  0x000ff742  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff747  lea      ecx, [ebp - 0x84]
  0x000ff74d  mov      esi, dword ptr [eax]
  0x000ff74f  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000ff755  mov      ecx, dword ptr [ebx + 4]
  0x000ff758  mov      dword ptr [ebp - 0x74], esi
  0x000ff75b  mov      dword ptr [ebp - 0x70], 0
  0x000ff762  movups   xmm0, xmmword ptr [eax]
  0x000ff765  lea      eax, [ebp - 0x74]
  0x000ff768  mov      dword ptr [ebp - 0x6c], edi
  0x000ff76b  push     eax
  0x000ff76c  lea      eax, [ebp - 0x54]
  0x000ff76f  push     eax
  0x000ff770  movups   xmmword ptr [ebp - 0x68], xmm0
  0x000ff774  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000ff779  lea      ecx, [ebp - 0x54]
  0x000ff77c  call     0x10008cc0   ; -> ??1AuraContainer@GAME@@QAE@XZ
  0x000ff781  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff784  pop      edi
  0x000ff785  pop      esi
  0x000ff786  pop      ebx
  0x000ff787  mov      dword ptr fs:[0], ecx
  0x000ff78e  mov      esp, ebp
  0x000ff790  pop      ebp
  0x000ff791  ret      4
  0x000ff794  int3     
  0x000ff795  int3     
  0x000ff796  int3     
  0x000ff797  int3     
  0x000ff798  int3     
  0x000ff799  int3     
  0x000ff79a  int3     
  0x000ff79b  int3     
  0x000ff79c  int3     
  0x000ff79d  int3     
  0x000ff79e  int3     
  0x000ff79f  int3     
