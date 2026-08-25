=== helper-A  as-Player  RVA 0x0000b260
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
    0x0000b2cf  pop      edi
    0x0000b2d0  mov      eax, esi
    0x0000b2d2  pop      esi
    0x0000b2d3  mov      esp, ebp
    0x0000b2d5  pop      ebp
    0x0000b2d6  ret      4
    0x0000b2d9  call     dword ptr [0x104e505c]   ; f32=1.16341e-38 i32=8302344 f64=2.73099e-306
    0x0000b2df  pop      edi
    0x0000b2e0  xor      eax, eax
    0x0000b2e2  pop      esi
    0x0000b2e3  mov      esp, ebp
    0x0000b2e5  pop      ebp
    0x0000b2e6  ret      4
    0x0000b2e9  int3     
    0x0000b2ea  int3     
    0x0000b2eb  int3     
    0x0000b2ec  int3     
    0x0000b2ed  int3     
    0x0000b2ee  int3     
    0x0000b2ef  int3     
    0x0000b2f0  push     ebp
    0x0000b2f1  mov      ebp, esp
    0x0000b2f3  push     -1
    0x0000b2f5  push     0x104c0248
    0x0000b2fa  mov      eax, dword ptr fs:[0]
    0x0000b300  push     eax
    0x0000b301  mov      dword ptr fs:[0], esp
    0x0000b308  sub      esp, 8
    0x0000b30b  push     ebx
    0x0000b30c  push     esi
    0x0000b30d  mov      esi, ecx
    0x0000b30f  push     edi
    0x0000b310  mov      dword ptr [ebp - 0x14], esi
    0x0000b313  mov      dword ptr [ebp - 0x10], esp
    0x0000b316  mov      dword ptr [esi], 0
    0x0000b31c  mov      dword ptr [esi + 4], 0
    0x0000b323  call     0x1000b4d0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0x1110
    0x0000b328  mov      dword ptr [esi], eax
    0x0000b32a  mov      dword ptr [ebp - 4], 0
    0x0000b331  mov      ecx, esi
    0x0000b333  mov      byte ptr [ebp - 4], 1
    0x0000b337  push     dword ptr [ebp + 8]
    0x0000b33a  push     dword ptr [ebp + 8]
    0x0000b33d  call     0x1000b420   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0x1060
    0x0000b342  mov      ecx, dword ptr [ebp - 0xc]
    0x0000b345  mov      eax, esi
    0x0000b347  pop      edi
    0x0000b348  pop      esi
    0x0000b349  mov      dword ptr fs:[0], ecx
    0x0000b350  pop      ebx

=== helper-B  as-Character  RVA 0x0000b150
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
    0x0000b1bf  pop      edi
    0x0000b1c0  mov      eax, esi
    0x0000b1c2  pop      esi
    0x0000b1c3  mov      esp, ebp
    0x0000b1c5  pop      ebp
    0x0000b1c6  ret      4
    0x0000b1c9  call     dword ptr [0x104e505c]   ; f32=1.16341e-38 i32=8302344 f64=2.73099e-306
    0x0000b1cf  pop      edi
    0x0000b1d0  xor      eax, eax
    0x0000b1d2  pop      esi
    0x0000b1d3  mov      esp, ebp
    0x0000b1d5  pop      ebp
    0x0000b1d6  ret      4
    0x0000b1d9  int3     
    0x0000b1da  int3     
    0x0000b1db  int3     
    0x0000b1dc  int3     
    0x0000b1dd  int3     
    0x0000b1de  int3     
    0x0000b1df  int3     
    0x0000b1e0  push     esi
    0x0000b1e1  mov      esi, ecx
    0x0000b1e3  test     esi, esi
    0x0000b1e5  je       0x1000b213
    0x0000b1e7  mov      eax, dword ptr [esi]
    0x0000b1e9  call     dword ptr [eax]
    0x0000b1eb  cmp      eax, 0x107ff5b8
    0x0000b1f0  je       0x1000b20f
    0x0000b1f2  mov      ecx, dword ptr [eax + 8]
    0x0000b1f5  test     ecx, ecx
    0x0000b1f7  je       0x1000b213
    0x0000b1f9  cmp      ecx, 0x107ff5b8
    0x0000b1ff  je       0x1000b20f
    0x0000b201  push     0x107ff5b8
    0x0000b206  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
    0x0000b20b  test     al, al
    0x0000b20d  je       0x1000b213
    0x0000b20f  mov      eax, esi
    0x0000b211  pop      esi
    0x0000b212  ret      
    0x0000b213  xor      eax, eax
    0x0000b215  pop      esi
    0x0000b216  ret      
    0x0000b217  int3     
    0x0000b218  int3     
    0x0000b219  int3     
    0x0000b21a  int3     
    0x0000b21b  int3     
    0x0000b21c  int3     
    0x0000b21d  int3     

=== RTTI resolve inner  RVA 0x0000bb10
    0x0000bb10  push     ebp
    0x0000bb11  mov      ebp, esp
    0x0000bb13  push     ebx
    0x0000bb14  push     esi
    0x0000bb15  push     edi
    0x0000bb16  mov      edi, dword ptr [ebp + 0xc]
    0x0000bb19  mov      esi, ecx
    0x0000bb1b  movzx    eax, byte ptr [edi]
    0x0000bb1e  xor      eax, 0x811c9dc5
    0x0000bb23  imul     edx, eax, 0x1000193
    0x0000bb29  movzx    eax, byte ptr [edi + 1]
    0x0000bb2d  xor      edx, eax
    0x0000bb2f  movzx    eax, byte ptr [edi + 2]
    0x0000bb33  imul     edx, edx, 0x1000193
    0x0000bb39  xor      edx, eax
    0x0000bb3b  movzx    eax, byte ptr [edi + 3]
    0x0000bb3f  imul     ecx, edx, 0x1000193
    0x0000bb45  mov      edx, dword ptr [esi + 0xc]
    0x0000bb48  xor      ecx, eax
    0x0000bb4a  imul     eax, ecx, 0x1000193
    0x0000bb50  mov      ecx, dword ptr [esi + 0x18]
    0x0000bb53  mov      esi, dword ptr [esi + 4]
    0x0000bb56  and      ecx, eax
    0x0000bb58  mov      eax, dword ptr [edx + ecx*8]
    0x0000bb5b  add      ecx, ecx
    0x0000bb5d  mov      ebx, dword ptr [edx + ecx*4]
    0x0000bb60  lea      edx, [edx + ecx*4]
    0x0000bb63  cmp      ebx, esi
    0x0000bb65  jne      0x1000bb6b
    0x0000bb67  mov      ecx, esi
    0x0000bb69  jmp      0x1000bb70   ; -> ?GetRTTIClassInfo@Monster@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x70
    0x0000bb6b  mov      ecx, dword ptr [edx + 4]
    0x0000bb6e  mov      ecx, dword ptr [ecx]
    0x0000bb70  cmp      eax, ecx
    0x0000bb72  je       0x1000bb95
    0x0000bb74  mov      ecx, dword ptr [eax + 8]
    0x0000bb77  cmp      ecx, dword ptr [edi]
    0x0000bb79  je       0x1000bb7f
    0x0000bb7b  mov      eax, dword ptr [eax]
    0x0000bb7d  jmp      0x1000bb63   ; -> ?GetRTTIClassInfo@Monster@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x63
    0x0000bb7f  mov      ecx, dword ptr [edi]
    0x0000bb81  cmp      ecx, dword ptr [eax + 8]
    0x0000bb84  mov      ecx, dword ptr [ebp + 8]
    0x0000bb87  cmovne   eax, esi
    0x0000bb8a  pop      edi
    0x0000bb8b  pop      esi
    0x0000bb8c  mov      dword ptr [ecx], eax
    0x0000bb8e  mov      eax, ecx
    0x0000bb90  pop      ebx
    0x0000bb91  pop      ebp
    0x0000bb92  ret      8
    0x0000bb95  mov      eax, dword ptr [ebp + 8]
    0x0000bb98  pop      edi
    0x0000bb99  mov      dword ptr [eax], esi
    0x0000bb9b  pop      esi
    0x0000bb9c  pop      ebx
    0x0000bb9d  pop      ebp
    0x0000bb9e  ret      8
    0x0000bba1  int3     
    0x0000bba2  int3     
    0x0000bba3  int3     
    0x0000bba4  int3     
    0x0000bba5  int3     
    0x0000bba6  int3     
    0x0000bba7  int3     
    0x0000bba8  int3     
    0x0000bba9  int3     
    0x0000bbaa  int3     
    0x0000bbab  int3     
    0x0000bbac  int3     
    0x0000bbad  int3     
    0x0000bbae  int3     
    0x0000bbaf  int3     
    0x0000bbb0  push     ebp
    0x0000bbb1  mov      ebp, esp
    0x0000bbb3  push     ecx
    0x0000bbb4  push     esi
    0x0000bbb5  mov      esi, ecx
    0x0000bbb7  push     edi
    0x0000bbb8  push     0x10589370
    0x0000bbbd  lea      edi, [esi + 0xc]
    0x0000bbc0  mov      ecx, edi
    0x0000bbc2  call     dword ptr [0x104e5060]   ; f32=1.16341e-38 i32=8302382 f64=2.73105e-306
    0x0000bbc8  lea      eax, [ebp + 8]
    0x0000bbcb  push     eax
    0x0000bbcc  lea      eax, [ebp - 4]
    0x0000bbcf  push     eax
    0x0000bbd0  lea      ecx, [esi + 0x18]
    0x0000bbd3  call     0x1000bb10   ; -> ?GetRTTIClassInfo@Monster@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x10
    0x0000bbd8  mov      eax, dword ptr [ebp - 4]

