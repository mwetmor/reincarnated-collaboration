  0x0006b590  push     ebp
  0x0006b591  mov      ebp, esp
  0x0006b593  push     -1
  0x0006b595  push     0x104c3b28
  0x0006b59a  mov      eax, dword ptr fs:[0]
  0x0006b5a0  push     eax
  0x0006b5a1  mov      dword ptr fs:[0], esp
  0x0006b5a8  sub      esp, 0x1c
  0x0006b5ab  push     esi
  0x0006b5ac  mov      esi, ecx
  0x0006b5ae  mov      dword ptr [ebp - 0x14], esi
  0x0006b5b1  cmp      byte ptr [esi + 0x14], 0
  0x0006b5b5  je       0x1006b6aa
  0x0006b5bb  push     edi
  0x0006b5bc  push     dword ptr [esi + 4]
  0x0006b5bf  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0006b5c5  mov      ecx, eax
  0x0006b5c7  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x0006b5cc  mov      edi, eax
  0x0006b5ce  test     edi, edi
  0x0006b5d0  je       0x1006b698
  0x0006b5d6  push     ebx
  0x0006b5d7  push     0x64
  0x0006b5d9  call     0x104be920   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70
  0x0006b5de  add      esp, 4
  0x0006b5e1  mov      dword ptr [ebp - 0x10], eax
  0x0006b5e4  mov      ecx, edi
  0x0006b5e6  mov      dword ptr [ebp - 4], 0
  0x0006b5ed  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x0006b5f3  mov      ebx, dword ptr [esi + 0x2c]
  0x0006b5f6  mov      edi, dword ptr [esi + 0x28]
  0x0006b5f9  mov      ecx, dword ptr [ebp - 0x10]
  0x0006b5fc  movups   xmm0, xmmword ptr [eax]
  0x0006b5ff  movups   xmmword ptr [ebp - 0x28], xmm0
  0x0006b603  movss    xmm0, dword ptr [esi + 0x30]
  0x0006b608  mov      esi, dword ptr [esi + 4]
  0x0006b60b  push     esi
  0x0006b60c  movss    dword ptr [ebp - 0x18], xmm0
  0x0006b611  call     dword ptr [0x104e5760]   ; f32=1.16681e-38 i32=8326670 f64=2.76403e-306
  0x0006b617  mov      byte ptr [ebp - 4], 1
  0x0006b61b  mov      eax, dword ptr [ebp - 0x10]
  0x0006b61e  mov      dword ptr [eax + 4], esi
  0x0006b621  mov      esi, eax
  0x0006b623  mov      dword ptr [eax], 0x105921d4
  0x0006b629  lea      ecx, [esi + 0x18]
  0x0006b62c  mov      dword ptr [esi + 8], 0
  0x0006b633  mov      word ptr [esi + 0xc], 0x100
  0x0006b639  mov      dword ptr [esi + 0x10], 0x437a0000
  0x0006b640  mov      byte ptr [esi + 0x14], 0
  0x0006b644  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x0006b64a  movups   xmm0, xmmword ptr [ebp - 0x28]
  0x0006b64e  mov      eax, dword ptr [ebp - 0x14]
  0x0006b651  mov      dword ptr [esi], 0x10592098
  0x0006b657  movups   xmmword ptr [esi + 0x34], xmm0
  0x0006b65b  movups   xmm0, xmmword ptr [eax + 0x18]
  0x0006b65f  mov      dword ptr [esi + 0x58], ebx
  0x0006b662  mov      eax, esi
  0x0006b664  pop      ebx
  0x0006b665  movups   xmmword ptr [esi + 0x44], xmm0
  0x0006b669  mov      dword ptr [esi + 0x54], edi
  0x0006b66c  movss    xmm0, dword ptr [ebp - 0x18]
  0x0006b671  pop      edi
  0x0006b672  movss    dword ptr [esi + 0x5c], xmm0
  0x0006b677  mov      dword ptr [esi + 0x60], 5
  0x0006b67e  mov      dword ptr [esi + 8], 4
  0x0006b685  mov      byte ptr [esi + 0xc], 1
  0x0006b689  pop      esi
  0x0006b68a  mov      ecx, dword ptr [ebp - 0xc]
  0x0006b68d  mov      dword ptr fs:[0], ecx
  0x0006b694  mov      esp, ebp
  0x0006b696  pop      ebp
  0x0006b697  ret      
  0x0006b698  pop      edi
  0x0006b699  xor      eax, eax
  0x0006b69b  pop      esi
  0x0006b69c  mov      ecx, dword ptr [ebp - 0xc]
  0x0006b69f  mov      dword ptr fs:[0], ecx
  0x0006b6a6  mov      esp, ebp
  0x0006b6a8  pop      ebp
  0x0006b6a9  ret      
  0x0006b6aa  mov      ecx, dword ptr [ebp - 0xc]
  0x0006b6ad  xor      eax, eax
  0x0006b6af  pop      esi
  0x0006b6b0  mov      dword ptr fs:[0], ecx
  0x0006b6b7  mov      esp, ebp
  0x0006b6b9  pop      ebp
  0x0006b6ba  ret      
  0x0006b6bb  int3     
  0x0006b6bc  int3     
  0x0006b6bd  int3     
  0x0006b6be  int3     
  0x0006b6bf  int3     
