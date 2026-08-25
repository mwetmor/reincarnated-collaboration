=== 90-ControllerAI-SetState RVA 0x000e6780 sym=?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z ===
  0x000e6780  push     ebp
  0x000e6781  mov      ebp, esp
  0x000e6783  push     ebx
  0x000e6784  push     esi
  0x000e6785  mov      ebx, ecx
  0x000e6787  push     edi
  0x000e6788  push     dword ptr [ebp + 8]
  0x000e678b  lea      ecx, [ebx + 0x1dc]
  0x000e6791  call     0x10062ef0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0xe00
  0x000e6796  mov      edi, dword ptr [ebx + 0x1dc]
  0x000e679c  mov      esi, eax
  0x000e679e  cmp      esi, edi
  0x000e67a0  je       0x100e67b2
  0x000e67a2  lea      eax, [esi + 0x10]
  0x000e67a5  push     eax
  0x000e67a6  push     dword ptr [ebp + 8]
  0x000e67a9  call     0x10029fc0   ; -> ?GetReagentText@AscendantAltarFormula@GAME@@QAEXIAAV?$vector@UGameTextLine@GAME@@@mem@@W4GameTextClass@2@@Z+0xbc0
  0x000e67ae  test     al, al
  0x000e67b0  je       0x100e67b4
  0x000e67b2  mov      esi, edi
  0x000e67b4  cmp      esi, edi
  0x000e67b6  jne      0x100e67e2
  0x000e67b8  mov      edx, dword ptr [ebp + 8]
  0x000e67bb  cmp      dword ptr [edx + 0x14], 0x10
  0x000e67bf  jb       0x100e67c3
  0x000e67c1  mov      edx, dword ptr [edx]
  0x000e67c3  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000e67c8  push     edx
  0x000e67c9  push     0x10528e20
  0x000e67ce  push     2
  0x000e67d0  mov      eax, dword ptr [eax]
  0x000e67d2  push     eax
  0x000e67d3  mov      ecx, dword ptr [eax]
  0x000e67d5  call     dword ptr [ecx + 0xc]
  0x000e67d8  add      esp, 0x10
  0x000e67db  pop      edi
  0x000e67dc  pop      esi
  0x000e67dd  pop      ebx
  0x000e67de  pop      ebp
  0x000e67df  ret      8
  0x000e67e2  mov      al, byte ptr [ebx + 0x204]
  0x000e67e8  mov      byte ptr [ebx + 0x204], 0
  0x000e67ef  cmp      dword ptr [ebx + 0x214], 0
  0x000e67f6  mov      byte ptr [ebp + 0xb], al
  0x000e67f9  jne      0x100e6904
  0x000e67ff  mov      ecx, dword ptr [ebx + 0x1e4]
  0x000e6805  mov      edi, dword ptr [ebp + 0xc]
  0x000e6808  test     ecx, ecx
  0x000e680a  je       0x100e68c3
  0x000e6810  mov      eax, dword ptr [ecx]
  0x000e6812  call     dword ptr [eax + 0x114]
  0x000e6818  cmp      byte ptr [ebx + 0x204], 0
  0x000e681f  jne      0x100e6939
  0x000e6825  mov      ecx, ebx
  0x000e6827  mov      byte ptr [ebp + 0xb], 1
  0x000e682b  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000e6830  mov      eax, dword ptr [eax]
  0x000e6832  cmp      eax, dword ptr [edi]
  0x000e6834  je       0x100e68c3
  0x000e683a  mov      ecx, ebx
  0x000e683c  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000e6841  push     dword ptr [eax]
  0x000e6843  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e6849  mov      ecx, eax
  0x000e684b  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6850  mov      dword ptr [ebp + 0xc], eax
  0x000e6853  test     eax, eax
  0x000e6855  je       0x100e687e
  0x000e6857  push     dword ptr [ebx + 0x24]
  0x000e685a  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e6860  mov      ecx, eax
  0x000e6862  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6867  mov      ecx, eax
  0x000e6869  call     dword ptr [0x104e5090]   ; f32=1.16349e-38 i32=8302926 f64=2.73178e-306
  0x000e686f  mov      ecx, dword ptr [ebp + 0xc]
  0x000e6872  push     eax
  0x000e6873  mov      ecx, dword ptr [ecx + 0x1dd0]
  0x000e6879  call     0x1045f6a0   ; -> ?ReleaseSlot@SlotManager@GAME@@QAEXI@Z
  0x000e687e  mov      ecx, ebx
  0x000e6880  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000e6885  push     dword ptr [eax + 4]
  0x000e6888  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e688e  mov      ecx, eax
  0x000e6890  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6895  mov      dword ptr [ebp + 0xc], eax
  0x000e6898  test     eax, eax
  0x000e689a  je       0x100e68c3
  0x000e689c  push     dword ptr [ebx + 0x24]
  0x000e689f  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e68a5  mov      ecx, eax
  0x000e68a7  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e68ac  mov      ecx, eax
  0x000e68ae  call     dword ptr [0x104e5090]   ; f32=1.16349e-38 i32=8302926 f64=2.73178e-306
  0x000e68b4  mov      ecx, dword ptr [ebp + 0xc]
  0x000e68b7  push     eax
  0x000e68b8  mov      ecx, dword ptr [ecx + 0x1dd4]
  0x000e68be  call     0x1045f6a0   ; -> ?ReleaseSlot@SlotManager@GAME@@QAEXI@Z
  0x000e68c3  movups   xmm0, xmmword ptr [edi]
  0x000e68c6  movups   xmmword ptr [ebx + 0x1e8], xmm0
  0x000e68cd  movq     xmm0, qword ptr [edi + 0x10]
  0x000e68d2  movq     qword ptr [ebx + 0x1f8], xmm0
  0x000e68da  mov      eax, dword ptr [edi + 0x18]
  0x000e68dd  mov      dword ptr [ebx + 0x200], eax
  0x000e68e3  mov      ecx, dword ptr [esi + 0x28]
  0x000e68e6  mov      dword ptr [ebx + 0x1e4], ecx
  0x000e68ec  mov      eax, dword ptr [ecx]
  0x000e68ee  call     dword ptr [eax + 0x110]
  0x000e68f4  mov      al, byte ptr [ebp + 0xb]
  0x000e68f7  pop      edi
  0x000e68f8  pop      esi
  0x000e68f9  mov      byte ptr [ebx + 0x204], al
  0x000e68ff  pop      ebx
  0x000e6900  pop      ebp
  0x000e6901  ret      8
  0x000e6904  mov      eax, dword ptr [ebp + 0xc]
  0x000e6907  movups   xmm0, xmmword ptr [eax]
  0x000e690a  movups   xmmword ptr [ebx + 0x1e8], xmm0
  0x000e6911  movq     xmm0, qword ptr [eax + 0x10]
  0x000e6916  movq     qword ptr [ebx + 0x1f8], xmm0
  0x000e691e  mov      eax, dword ptr [eax + 0x18]
  0x000e6921  mov      dword ptr [ebx + 0x200], eax
  0x000e6927  mov      eax, dword ptr [esi + 0x28]
  0x000e692a  mov      dword ptr [ebx + 0x1e4], eax
  0x000e6930  mov      al, byte ptr [ebp + 0xb]
  0x000e6933  mov      byte ptr [ebx + 0x204], al
  0x000e6939  pop      edi
  0x000e693a  pop      esi
  0x000e693b  pop      ebx
  0x000e693c  pop      ebp
  0x000e693d  ret      8
