=== helper-A used by CBC::CheckAction main path  RVA 0x0000b260
    0x0000b260  push     ebp
    0x0000b261  mov      ebp, esp
    0x0000b263  push     ecx
    0x0000b264  mov      eax, dword ptr [ebp + 8]
    0x0000b267  push     esi
    0x0000b268  mov      esi, ecx
    0x0000b26a  mov      dword ptr [ebp + 8], eax
    0x0000b26d  push     edi
    0x0000b26e  push     0x10589370
    0x0000b273  lea      edi, [esi + 0xc]
    0x0000b276  mov      ecx, edi
    0x0000b278  call     dword ptr [0x104e5060]   ; f32=1.16341e-38 i32=8302382 f64=2.73105e-306
    0x0000b27e  lea      eax, [ebp + 8]
    0x0000b281  push     eax
    0x0000b282  lea      eax, [ebp - 4]
    0x0000b285  push     eax
    0x0000b286  lea      ecx, [esi + 0x18]
    0x0000b289  call     0x1000bb10   ; -> ?GetRTTIClassInfo@Monster@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x10
    0x0000b28e  mov      eax, dword ptr [ebp - 4]
    0x0000b291  mov      ecx, edi
    0x0000b293  cmp      eax, dword ptr [esi + 0x1c]
    0x0000b296  je       0x1000b2d9
    0x0000b298  mov      esi, dword ptr [eax + 0xc]
    0x0000b29b  call     dword ptr [0x104e505c]   ; f32=1.16341e-38 i32=8302344 f64=2.73099e-306
    0x0000b2a1  test     esi, esi
    0x0000b2a3  je       0x1000b2df
    0x0000b2a5  mov      eax, dword ptr [esi]
    0x0000b2a7  mov      ecx, esi
    0x0000b2a9  call     dword ptr [eax]
    0x0000b2ab  cmp      eax, 0x107ff5a0
    0x0000b2b0  je       0x1000b2cf
    0x0000b2b2  mov      ecx, dword ptr [eax + 8]
    0x0000b2b5  test     ecx, ecx
    0x0000b2b7  je       0x1000b2df
    0x0000b2b9  cmp      ecx, 0x107ff5a0
    0x0000b2bf  je       0x1000b2cf
    0x0000b2c1  push     0x107ff5a0
    0x0000b2c6  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
    0x0000b2cb  test     al, al
    0x0000b2cd  je       0x1000b2df

=== helper-B used by CBC::CheckAction fallback + ControllerPlayer + ControllerAI::MoveTo  RVA 0x0000b150
    0x0000b150  push     ebp
    0x0000b151  mov      ebp, esp
    0x0000b153  push     ecx
    0x0000b154  mov      eax, dword ptr [ebp + 8]
    0x0000b157  push     esi
    0x0000b158  mov      esi, ecx
    0x0000b15a  mov      dword ptr [ebp + 8], eax
    0x0000b15d  push     edi
    0x0000b15e  push     0x10589370
    0x0000b163  lea      edi, [esi + 0xc]
    0x0000b166  mov      ecx, edi
    0x0000b168  call     dword ptr [0x104e5060]   ; f32=1.16341e-38 i32=8302382 f64=2.73105e-306
    0x0000b16e  lea      eax, [ebp + 8]
    0x0000b171  push     eax
    0x0000b172  lea      eax, [ebp - 4]
    0x0000b175  push     eax
    0x0000b176  lea      ecx, [esi + 0x18]
    0x0000b179  call     0x1000bb10   ; -> ?GetRTTIClassInfo@Monster@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x10
    0x0000b17e  mov      eax, dword ptr [ebp - 4]
    0x0000b181  mov      ecx, edi
    0x0000b183  cmp      eax, dword ptr [esi + 0x1c]
    0x0000b186  je       0x1000b1c9
    0x0000b188  mov      esi, dword ptr [eax + 0xc]
    0x0000b18b  call     dword ptr [0x104e505c]   ; f32=1.16341e-38 i32=8302344 f64=2.73099e-306
    0x0000b191  test     esi, esi
    0x0000b193  je       0x1000b1cf
    0x0000b195  mov      eax, dword ptr [esi]
    0x0000b197  mov      ecx, esi
    0x0000b199  call     dword ptr [eax]
    0x0000b19b  cmp      eax, 0x107ff618
    0x0000b1a0  je       0x1000b1bf
    0x0000b1a2  mov      ecx, dword ptr [eax + 8]
    0x0000b1a5  test     ecx, ecx
    0x0000b1a7  je       0x1000b1cf
    0x0000b1a9  cmp      ecx, 0x107ff618
    0x0000b1af  je       0x1000b1bf
    0x0000b1b1  push     0x107ff618
    0x0000b1b6  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
    0x0000b1bb  test     al, al
    0x0000b1bd  je       0x1000b1cf

