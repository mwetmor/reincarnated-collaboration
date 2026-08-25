    0x0011b430  push     ebp
    0x0011b431  mov      ebp, esp
    0x0011b433  push     ecx
    0x0011b434  push     ebx
    0x0011b435  push     edi
    0x0011b436  mov      edi, dword ptr [ebp + 8]
    0x0011b439  mov      ebx, ecx
    0x0011b43b  mov      ecx, edi
    0x0011b43d  mov      dword ptr [ebp - 4], ebx
    0x0011b440  mov      eax, dword ptr [edi]
    0x0011b442  call     dword ptr [eax + 0x2c]
    0x0011b445  push     dword ptr [ebx + 0x24]
    0x0011b448  mov      dword ptr [ebp + 8], eax
    0x0011b44b  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
    0x0011b451  mov      ecx, eax
    0x0011b453  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
    0x0011b458  mov      ebx, eax
    0x0011b45a  mov      ecx, dword ptr [ebx + 0x1ba4]
    0x0011b460  mov      ecx, dword ptr [ecx + 4]
    0x0011b463  test     ecx, ecx
    0x0011b465  je       0x1011b472
    0x0011b467  mov      edx, dword ptr [ecx]
    0x0011b469  mov      edx, dword ptr [edx + 0x18]
    0x0011b46c  call     edx
    0x0011b46e  test     al, al
    0x0011b470  jne      0x1011b488
    0x0011b472  mov      eax, dword ptr [edi]
    0x0011b474  mov      ecx, edi
    0x0011b476  call     dword ptr [eax + 0x2c]
    0x0011b479  cmp      eax, 8
    0x0011b47c  je       0x1011b488
    0x0011b47e  pop      edi
    0x0011b47f  xor      eax, eax
    0x0011b481  pop      ebx
    0x0011b482  mov      esp, ebp
    0x0011b484  pop      ebp
    0x0011b485  ret      4
    0x0011b488  mov      eax, dword ptr [ebx + 0x1ba4]
    0x0011b48e  push     esi
    0x0011b48f  mov      ecx, dword ptr [eax + 4]
    0x0011b492  test     ecx, ecx
    0x0011b494  je       0x1011b4a4
    0x0011b496  mov      eax, dword ptr [ecx]
    0x0011b498  call     dword ptr [eax + 0x2c]
    0x0011b49b  mov      esi, eax
    0x0011b49d  cmp      esi, 8
    0x0011b4a0  je       0x1011b4cd
    0x0011b4a2  jmp      0x1011b4a6   ; -> ?CheckAction@ControllerPlayer@GAME@@UBE?AW4CharacterActionPermission@2@PAVCharacterAction@2@@Z+0x76
    0x0011b4a4  xor      esi, esi
    0x0011b4a6  push     dword ptr [ebx + 0x760]
    0x0011b4ac  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
    0x0011b4b2  mov      ecx, eax
    0x0011b4b4  call     0x1000d4f0   ; -> ?CreateUISummaryText@AmbientCharacter@GAME@@UBEXW4GameTextClass@2@AAV?$vector@UGameTextLine@GAME@@@mem@@@Z+0x7e0
    0x0011b4b9  mov      ecx, eax
    0x0011b4bb  test     ecx, ecx
    0x0011b4bd  je       0x1011b4cd
    0x0011b4bf  mov      eax, dword ptr [ecx]
    0x0011b4c1  mov      eax, dword ptr [eax + 0x2d4]
    0x0011b4c7  call     eax
    0x0011b4c9  test     al, al
    0x0011b4cb  jne      0x1011b509
    0x0011b4cd  imul     ecx, dword ptr [ebp + 8], 0x1a
    0x0011b4d1  mov      eax, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
    0x0011b4d6  add      ecx, esi
    0x0011b4d8  mov      eax, dword ptr [eax + ecx*4 + 0x2802c]
    0x0011b4df  cmp      eax, 3
    0x0011b4e2  jne      0x1011b50b
    0x0011b4e4  mov      eax, dword ptr [ebx + 0x1ba4]
    0x0011b4ea  mov      ecx, dword ptr [eax + 4]
    0x0011b4ed  test     ecx, ecx
    0x0011b4ef  je       0x1011b509
    0x0011b4f1  mov      edx, dword ptr [ebp - 4]
    0x0011b4f4  mov      eax, dword ptr [ecx]
    0x0011b4f6  push     dword ptr [edx + 0x88]
    0x0011b4fc  push     edi
    0x0011b4fd  call     dword ptr [eax + 0x40]
    0x0011b500  pop      esi
    0x0011b501  pop      edi
    0x0011b502  pop      ebx
    0x0011b503  mov      esp, ebp
    0x0011b505  pop      ebp
    0x0011b506  ret      4
    0x0011b509  xor      eax, eax
    0x0011b50b  pop      esi
    0x0011b50c  pop      edi
    0x0011b50d  pop      ebx
    0x0011b50e  mov      esp, ebp
    0x0011b510  pop      ebp
    0x0011b511  ret      4
    0x0011b514  int3     
    0x0011b515  int3     
    0x0011b516  int3     
    0x0011b517  int3     
    0x0011b518  int3     
    0x0011b519  int3     
    0x0011b51a  int3     
    0x0011b51b  int3     
    0x0011b51c  int3     
    0x0011b51d  int3     
    0x0011b51e  int3     
    0x0011b51f  int3     
