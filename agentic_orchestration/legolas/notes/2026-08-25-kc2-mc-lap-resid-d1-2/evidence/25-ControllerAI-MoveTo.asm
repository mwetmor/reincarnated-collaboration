=== 25-ControllerAI-MoveTo  RVA 0x000e6cd0  sym=?MoveTo@ControllerAI@GAME@@QAEXABVWorldVec3@2@IIW4AnimationSet_Type@2@M@Z ===
  0x000e6cd0  push     ebp
  0x000e6cd1  mov      ebp, esp
  0x000e6cd3  push     -1
  0x000e6cd5  push     0x104c78b8
  0x000e6cda  mov      eax, dword ptr fs:[0]
  0x000e6ce0  push     eax
  0x000e6ce1  mov      dword ptr fs:[0], esp
  0x000e6ce8  sub      esp, 0x1c
  0x000e6ceb  push     ebx
  0x000e6cec  push     esi
  0x000e6ced  push     edi
  0x000e6cee  mov      esi, ecx
  0x000e6cf0  push     0x64
  0x000e6cf2  mov      dword ptr [ebp - 0x10], esi
  0x000e6cf5  call     0x104be920   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70
  0x000e6cfa  mov      ebx, eax
  0x000e6cfc  add      esp, 4
  0x000e6cff  mov      dword ptr [ebp - 0x14], ebx
  0x000e6d02  mov      dword ptr [ebp - 4], 0
  0x000e6d09  push     dword ptr [esi + 0x24]
  0x000e6d0c  mov      esi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000e6d12  call     esi
  0x000e6d14  mov      ecx, eax
  0x000e6d16  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6d1b  push     dword ptr [ebp + 0x10]
  0x000e6d1e  lea      ecx, [eax + 0x600]
  0x000e6d24  call     0x1043c700   ; -> ?GetSkillReferenceNumber@SkillManager@GAME@@QBE?BII@Z
  0x000e6d29  mov      edi, eax
  0x000e6d2b  mov      eax, dword ptr [ebp - 0x10]
  0x000e6d2e  push     dword ptr [eax + 0x24]
  0x000e6d31  call     esi
  0x000e6d33  mov      ecx, eax
  0x000e6d35  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000e6d3a  mov      ecx, eax
  0x000e6d3c  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x000e6d42  mov      ecx, ebx
  0x000e6d44  movups   xmm0, xmmword ptr [eax]
  0x000e6d47  mov      eax, dword ptr [ebp - 0x10]
  0x000e6d4a  movups   xmmword ptr [ebp - 0x28], xmm0
  0x000e6d4e  mov      esi, dword ptr [eax + 0x24]
  0x000e6d51  push     esi
  0x000e6d52  call     dword ptr [0x104e5760]   ; f32=1.16681e-38 i32=8326670 f64=2.76403e-306
  0x000e6d58  mov      byte ptr [ebp - 4], 1
  0x000e6d5c  lea      ecx, [ebx + 0x18]
  0x000e6d5f  mov      dword ptr [ebx], 0x105921d4
  0x000e6d65  mov      dword ptr [ebx + 4], esi
  0x000e6d68  mov      dword ptr [ebx + 8], 0
  0x000e6d6f  mov      word ptr [ebx + 0xc], 0x100
  0x000e6d75  mov      dword ptr [ebx + 0x10], 0x437a0000
  0x000e6d7c  mov      byte ptr [ebx + 0x14], 0
  0x000e6d80  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000e6d86  movups   xmm0, xmmword ptr [ebp - 0x28]
  0x000e6d8a  mov      eax, dword ptr [ebp + 8]
  0x000e6d8d  mov      ecx, dword ptr [ebp - 0x10]
  0x000e6d90  movups   xmmword ptr [ebx + 0x34], xmm0
  0x000e6d94  mov      dword ptr [ebx], 0x10592098
  0x000e6d9a  movups   xmm0, xmmword ptr [eax]
  0x000e6d9d  mov      eax, dword ptr [ebp + 0xc]
  0x000e6da0  mov      dword ptr [ebx + 0x54], eax
  0x000e6da3  mov      eax, dword ptr [ebp + 0x14]
  0x000e6da6  movups   xmmword ptr [ebx + 0x44], xmm0
  0x000e6daa  push     ebx
  0x000e6dab  movss    xmm0, dword ptr [ebp + 0x18]
  0x000e6db0  mov      dword ptr [ebx + 0x58], edi
  0x000e6db3  movss    dword ptr [ebx + 0x5c], xmm0
  0x000e6db8  mov      dword ptr [ebx + 0x60], eax
  0x000e6dbb  mov      dword ptr [ebx + 8], 4
  0x000e6dc2  mov      byte ptr [ebx + 0xc], 1
  0x000e6dc6  mov      dword ptr [ebp - 4], 0xffffffff
  0x000e6dcd  call     0x100ea480   ; -> ?HandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z
  0x000e6dd2  mov      ecx, dword ptr [ebp - 0xc]
  0x000e6dd5  pop      edi
  0x000e6dd6  pop      esi
  0x000e6dd7  mov      dword ptr fs:[0], ecx
  0x000e6dde  pop      ebx
  0x000e6ddf  mov      esp, ebp
  0x000e6de1  pop      ebp
  0x000e6de2  ret      0x14
  0x000e6de5  int3     
  0x000e6de6  int3     
  0x000e6de7  int3     
  0x000e6de8  int3     
  0x000e6de9  int3     
  0x000e6dea  int3     
  0x000e6deb  int3     
  0x000e6dec  int3     
  0x000e6ded  int3     
  0x000e6dee  int3     
  0x000e6def  int3     
