=== 58-ControllerAI-AddTemporaryState  RVA 0x000e6990  sym=?AddTemporaryState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z ===
  0x000e6990  push     ebp
  0x000e6991  mov      ebp, esp
  0x000e6993  sub      esp, 0x2c
  0x000e6996  push     ebx
  0x000e6997  mov      ebx, dword ptr [ebp + 8]
  0x000e699a  push     esi
  0x000e699b  push     edi
  0x000e699c  lea      edi, [ecx + 0x208]
  0x000e69a2  mov      dword ptr [ebp - 8], ecx
  0x000e69a5  push     ebx
  0x000e69a6  mov      ecx, edi
  0x000e69a8  mov      dword ptr [ebp - 4], edi
  0x000e69ab  call     0x10062ef0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0xe00
  0x000e69b0  mov      edi, dword ptr [edi]
  0x000e69b2  mov      esi, eax
  0x000e69b4  cmp      esi, edi
  0x000e69b6  je       0x100e69c6
  0x000e69b8  lea      eax, [esi + 0x10]
  0x000e69bb  push     eax
  0x000e69bc  push     ebx
  0x000e69bd  call     0x10029fc0   ; -> ?GetReagentText@AscendantAltarFormula@GAME@@QAEXIAAV?$vector@UGameTextLine@GAME@@@mem@@W4GameTextClass@2@@Z+0xbc0
  0x000e69c2  test     al, al
  0x000e69c4  je       0x100e69c8
  0x000e69c6  mov      esi, edi
  0x000e69c8  mov      eax, dword ptr [ebp - 4]
  0x000e69cb  cmp      esi, dword ptr [eax]
  0x000e69cd  jne      0x100e69f8
  0x000e69cf  cmp      dword ptr [ebx + 0x14], 0x10
  0x000e69d3  jb       0x100e69d7
  0x000e69d5  mov      ebx, dword ptr [ebx]
  0x000e69d7  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000e69dc  push     ebx
  0x000e69dd  push     0x10528e6c
  0x000e69e2  push     0
  0x000e69e4  mov      eax, dword ptr [eax]
  0x000e69e6  push     eax
  0x000e69e7  mov      ecx, dword ptr [eax]
  0x000e69e9  call     dword ptr [ecx + 0xc]
  0x000e69ec  add      esp, 0x10
  0x000e69ef  pop      edi
  0x000e69f0  pop      esi
  0x000e69f1  pop      ebx
  0x000e69f2  mov      esp, ebp
  0x000e69f4  pop      ebp
  0x000e69f5  ret      8
  0x000e69f8  mov      ebx, dword ptr [ebp - 8]
  0x000e69fb  cmp      dword ptr [ebx + 0x214], 0
  0x000e6a02  jne      0x100e6ac8
  0x000e6a08  mov      ecx, dword ptr [ebx + 0x1e4]
  0x000e6a0e  mov      eax, dword ptr [ecx]
  0x000e6a10  call     dword ptr [eax + 0x114]
  0x000e6a16  mov      ecx, ebx
  0x000e6a18  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000e6a1d  mov      edi, dword ptr [ebp + 0xc]
  0x000e6a20  mov      eax, dword ptr [eax]
  0x000e6a22  cmp      eax, dword ptr [edi]
  0x000e6a24  je       0x100e6a6a
  0x000e6a26  mov      ecx, ebx
  0x000e6a28  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000e6a2d  push     dword ptr [eax]
  0x000e6a2f  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e6a35  mov      ecx, eax
  0x000e6a37  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6a3c  mov      dword ptr [ebp + 0xc], eax
  0x000e6a3f  test     eax, eax
  0x000e6a41  je       0x100e6a6a
  0x000e6a43  push     dword ptr [ebx + 0x24]
  0x000e6a46  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e6a4c  mov      ecx, eax
  0x000e6a4e  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6a53  mov      ecx, eax
  0x000e6a55  call     dword ptr [0x104e5090]   ; f32=1.16349e-38 i32=8302926 f64=2.73178e-306
  0x000e6a5b  mov      ecx, dword ptr [ebp + 0xc]
  0x000e6a5e  push     eax
  0x000e6a5f  mov      ecx, dword ptr [ecx + 0x1dd0]
  0x000e6a65  call     0x1045f6a0   ; -> ?ReleaseSlot@SlotManager@GAME@@QAEXI@Z
  0x000e6a6a  lea      ecx, [ebp - 0x18]
  0x000e6a6d  mov      dword ptr [ebp - 0x24], 0
  0x000e6a74  mov      dword ptr [ebp - 0x20], 0
  0x000e6a7b  mov      dword ptr [ebp - 0x1c], 0
  0x000e6a82  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000e6a88  mov      eax, dword ptr [esi + 0x28]
  0x000e6a8b  lea      ecx, [ebx + 0x210]
  0x000e6a91  movups   xmm0, xmmword ptr [edi]
  0x000e6a94  mov      dword ptr [ebp - 0x28], eax
  0x000e6a97  mov      eax, dword ptr [edi + 0x18]
  0x000e6a9a  mov      dword ptr [ebp - 0xc], eax
  0x000e6a9d  lea      eax, [ebp - 0x28]
  0x000e6aa0  movups   xmmword ptr [ebp - 0x24], xmm0
  0x000e6aa4  push     eax
  0x000e6aa5  movq     xmm0, qword ptr [edi + 0x10]
  0x000e6aaa  movq     qword ptr [ebp - 0x14], xmm0
  0x000e6aaf  call     0x100e86e0   ; -> ?IsInState@ControllerAI@GAME@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z+0x80
  0x000e6ab4  mov      ecx, dword ptr [esi + 0x28]
  0x000e6ab7  mov      eax, dword ptr [ecx]
  0x000e6ab9  call     dword ptr [eax + 0x110]
  0x000e6abf  pop      edi
  0x000e6ac0  pop      esi
  0x000e6ac1  pop      ebx
  0x000e6ac2  mov      esp, ebp
  0x000e6ac4  pop      ebp
  0x000e6ac5  ret      8
  0x000e6ac8  lea      ecx, [ebp - 0x18]
  0x000e6acb  mov      dword ptr [ebp - 0x24], 0
  0x000e6ad2  mov      dword ptr [ebp - 0x20], 0
  0x000e6ad9  mov      dword ptr [ebp - 0x1c], 0
  0x000e6ae0  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000e6ae6  mov      eax, dword ptr [esi + 0x28]
  0x000e6ae9  lea      ecx, [ebx + 0x210]
  0x000e6aef  mov      dword ptr [ebp - 0x28], eax
  0x000e6af2  mov      eax, dword ptr [ebp + 0xc]
  0x000e6af5  movups   xmm0, xmmword ptr [eax]
  0x000e6af8  movups   xmmword ptr [ebp - 0x24], xmm0
  0x000e6afc  movq     xmm0, qword ptr [eax + 0x10]
  0x000e6b01  mov      eax, dword ptr [eax + 0x18]
  0x000e6b04  mov      dword ptr [ebp - 0xc], eax
  0x000e6b07  lea      eax, [ebp - 0x28]
  0x000e6b0a  push     eax
  0x000e6b0b  movq     qword ptr [ebp - 0x14], xmm0
  0x000e6b10  call     0x100e86e0   ; -> ?IsInState@ControllerAI@GAME@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z+0x80
  0x000e6b15  pop      edi
  0x000e6b16  pop      esi
  0x000e6b17  pop      ebx
  0x000e6b18  mov      esp, ebp
  0x000e6b1a  pop      ebp
  0x000e6b1b  ret      8
  0x000e6b1e  int3     
  0x000e6b1f  int3     
