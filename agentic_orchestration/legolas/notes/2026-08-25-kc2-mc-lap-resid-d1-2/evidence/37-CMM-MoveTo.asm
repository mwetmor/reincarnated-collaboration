=== 37-CMM-MoveTo  RVA 0x00077f40  sym=?MoveTo@CharacterMovementManager@GAME@@QAE_NABVWorldVec3@2@@Z ===
  0x00077f40  push     ebp
  0x00077f41  mov      ebp, esp
  0x00077f43  sub      esp, 0x14c
  0x00077f49  push     ebx
  0x00077f4a  mov      ebx, ecx
  0x00077f4c  push     esi
  0x00077f4d  push     edi
  0x00077f4e  lea      ecx, [ebx + 0x28]
  0x00077f51  call     0x1005f070   ; -> ?SelectPrimaryAction@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MAE_N_N_N1ABVWorldVec3@2@AAI1@Z+0xfd0
  0x00077f56  mov      ecx, dword ptr [ebx]
  0x00077f58  lea      eax, [ebp - 0x118]
  0x00077f5e  push     eax
  0x00077f5f  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x00077f65  mov      edi, dword ptr [ebp + 8]
  0x00077f68  mov      ecx, ebx
  0x00077f6a  push     edi
  0x00077f6b  movups   xmm0, xmmword ptr [eax]
  0x00077f6e  lea      eax, [ebp - 0x5c]
  0x00077f71  push     eax
  0x00077f72  movups   xmmword ptr [ebp - 0x5c], xmm0
  0x00077f76  call     0x100775f0   ; -> ?CheckForPortal@CharacterMovementManager@GAME@@ABEPBVPortal@2@ABVWorldVec3@2@0@Z
  0x00077f7b  mov      dword ptr [ebp - 4], eax
  0x00077f7e  test     eax, eax
  0x00077f80  je       0x1007803e
  0x00077f86  mov      edi, dword ptr [0x104e5790]   ; f32=1.1669e-38 i32=8327272 f64=2.76487e-306
  0x00077f8c  lea      ecx, [ebp - 0x118]
  0x00077f92  push     ecx
  0x00077f93  mov      ecx, eax
  0x00077f95  call     edi
  0x00077f97  mov      esi, dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x00077f9d  lea      ecx, [ebp - 0x9c]
  0x00077fa3  call     esi
  0x00077fa5  lea      ecx, [ebp - 0x48]
  0x00077fa8  call     esi
  0x00077faa  lea      ecx, [ebp - 0xe0]
  0x00077fb0  call     esi
  0x00077fb2  movups   xmm0, xmmword ptr [ebp - 0x118]
  0x00077fb9  mov      ecx, dword ptr [ebp - 4]
  0x00077fbc  lea      eax, [ebp - 0x14c]
  0x00077fc2  push     eax
  0x00077fc3  mov      dword ptr [ebp - 0xa0], 0
  0x00077fcd  movups   xmmword ptr [ebp - 0x9c], xmm0
  0x00077fd4  mov      dword ptr [ebp - 0x4c], 1
  0x00077fdb  call     dword ptr [0x104e5798]   ; f32=1.16692e-38 i32=8327440 f64=2.76509e-306
  0x00077fe1  mov      ecx, eax
  0x00077fe3  call     edi
  0x00077fe5  mov      ecx, dword ptr [ebp - 4]
  0x00077fe8  movups   xmm0, xmmword ptr [eax]
  0x00077feb  lea      eax, [ebp - 8]
  0x00077fee  mov      dword ptr [ebp - 8], 0
  0x00077ff5  push     eax
  0x00077ff6  lea      eax, [ebp - 0x38]
  0x00077ff9  push     eax
  0x00077ffa  movups   xmmword ptr [ebp - 0x48], xmm0
  0x00077ffe  call     dword ptr [0x104e579c]   ; f32=1.16693e-38 i32=8327488 f64=2.76519e-306
  0x00078004  mov      eax, dword ptr [ebp + 8]
  0x00078007  lea      ecx, [ebx + 0x28]
  0x0007800a  mov      dword ptr [ebp - 0xe4], 0
  0x00078014  movups   xmm0, xmmword ptr [eax]
  0x00078017  lea      eax, [ebp - 0xa0]
  0x0007801d  push     eax
  0x0007801e  movups   xmmword ptr [ebp - 0xe0], xmm0
  0x00078025  call     0x100786f0   ; -> ?DebugRender@CharacterMovementManager@GAME@@QAEXXZ+0x430
  0x0007802a  lea      eax, [ebp - 0x4c]
  0x0007802d  push     eax
  0x0007802e  lea      ecx, [ebx + 0x28]
  0x00078031  call     0x100786f0   ; -> ?DebugRender@CharacterMovementManager@GAME@@QAEXXZ+0x430
  0x00078036  lea      eax, [ebp - 0xe4]
  0x0007803c  jmp      0x10078061   ; -> ?MoveTo@CharacterMovementManager@GAME@@QAE_NABVWorldVec3@2@@Z+0x121
  0x0007803e  lea      ecx, [ebp - 0x48]
  0x00078041  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x00078047  movups   xmm0, xmmword ptr [edi]
  0x0007804a  lea      ecx, [ebp - 0x48]
  0x0007804d  movups   xmmword ptr [ebp - 0x48], xmm0
  0x00078051  call     dword ptr [0x104e55d0]   ; f32=1.16601e-38 i32=8320960 f64=2.75627e-306
  0x00078057  mov      dword ptr [ebp - 0x4c], 0
  0x0007805e  lea      eax, [ebp - 0x4c]
  0x00078061  push     eax
  0x00078062  lea      ecx, [ebx + 0x28]
  0x00078065  call     0x100786f0   ; -> ?DebugRender@CharacterMovementManager@GAME@@QAEXXZ+0x430
  0x0007806a  mov      ecx, ebx
  0x0007806c  call     0x100771a0   ; -> ?MoveToNextWaypoint@CharacterMovementManager@GAME@@AAE_NXZ
  0x00078071  pop      edi
  0x00078072  pop      esi
  0x00078073  pop      ebx
  0x00078074  mov      esp, ebp
  0x00078076  pop      ebp
  0x00078077  ret      4
  0x0007807a  int3     
  0x0007807b  int3     
  0x0007807c  int3     
  0x0007807d  int3     
  0x0007807e  int3     
  0x0007807f  int3     
