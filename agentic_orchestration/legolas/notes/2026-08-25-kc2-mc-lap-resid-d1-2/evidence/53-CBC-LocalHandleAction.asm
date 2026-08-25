  0x000ea4e0  push     ebp
  0x000ea4e1  mov      ebp, esp
  0x000ea4e3  push     ecx
  0x000ea4e4  push     ebx
  0x000ea4e5  push     esi
  0x000ea4e6  mov      esi, ecx
  0x000ea4e8  push     dword ptr [esi + 0x24]
  0x000ea4eb  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ea4f1  mov      ecx, eax
  0x000ea4f3  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000ea4f8  mov      ebx, eax
  0x000ea4fa  test     ebx, ebx
  0x000ea4fc  jne      0x100ea52e
  0x000ea4fe  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000ea503  push     0x105295d8
  0x000ea508  push     1
  0x000ea50a  mov      eax, dword ptr [eax]
  0x000ea50c  push     eax
  0x000ea50d  mov      ecx, dword ptr [eax]
  0x000ea50f  call     dword ptr [ecx + 0xc]
  0x000ea512  mov      ecx, dword ptr [ebp + 8]
  0x000ea515  add      esp, 0xc
  0x000ea518  test     ecx, ecx
  0x000ea51a  je       0x100ea636
  0x000ea520  mov      eax, dword ptr [ecx]
  0x000ea522  push     1
  0x000ea524  call     dword ptr [eax]
  0x000ea526  pop      esi
  0x000ea527  pop      ebx
  0x000ea528  mov      esp, ebp
  0x000ea52a  pop      ebp
  0x000ea52b  ret      4
  0x000ea52e  mov      eax, dword ptr [esi]
  0x000ea530  mov      ecx, esi
  0x000ea532  push     edi
  0x000ea533  mov      edi, dword ptr [ebp + 8]
  0x000ea536  push     edi
  0x000ea537  call     dword ptr [eax + 0x68]
  0x000ea53a  cmp      eax, 4
  0x000ea53d  jne      0x100ea54b
  0x000ea53f  mov      eax, dword ptr [ebx]
  0x000ea541  mov      ecx, ebx
  0x000ea543  call     dword ptr [eax + 0x450]
  0x000ea549  jmp      0x100ea553   ; -> ?LocalHandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z+0x73
  0x000ea54b  test     eax, eax
  0x000ea54d  jne      0x100ea600
  0x000ea553  mov      ecx, dword ptr [esi + 0x84]
  0x000ea559  mov      dword ptr [esi + 0x84], 0
  0x000ea563  test     ecx, ecx
  0x000ea565  je       0x100ea56c
  0x000ea567  mov      eax, dword ptr [ecx]
  0x000ea569  call     dword ptr [eax + 0x10]
  0x000ea56c  mov      ecx, dword ptr [esi + 0x84]
  0x000ea572  test     ecx, ecx
  0x000ea574  je       0x100ea57c
  0x000ea576  mov      eax, dword ptr [ecx]
  0x000ea578  push     1
  0x000ea57a  call     dword ptr [eax]
  0x000ea57c  mov      ecx, dword ptr [esi + 0x88]
  0x000ea582  mov      dword ptr [esi + 0x84], 0
  0x000ea58c  test     ecx, ecx
  0x000ea58e  je       0x100ea596
  0x000ea590  mov      eax, dword ptr [ecx]
  0x000ea592  push     1
  0x000ea594  call     dword ptr [eax]
  0x000ea596  mov      dword ptr [esi + 0x88], 0
  0x000ea5a0  mov      ecx, edi
  0x000ea5a2  mov      eax, dword ptr [edi]
  0x000ea5a4  mov      dword ptr [ebp + 8], 0x64
  0x000ea5ab  call     dword ptr [eax + 0x30]
  0x000ea5ae  mov      dword ptr [ebp - 4], eax
  0x000ea5b1  test     eax, eax
  0x000ea5b3  je       0x100ea5e7
  0x000ea5b5  mov      ecx, dword ptr [esi + 0x84]
  0x000ea5bb  test     ecx, ecx
  0x000ea5bd  je       0x100ea5c8
  0x000ea5bf  mov      edx, dword ptr [ecx]
  0x000ea5c1  push     1
  0x000ea5c3  call     dword ptr [edx]
  0x000ea5c5  mov      eax, dword ptr [ebp - 4]
  0x000ea5c8  lea      ecx, [ebp + 8]
  0x000ea5cb  mov      dword ptr [esi + 0x84], edi
  0x000ea5d1  push     ecx
  0x000ea5d2  mov      ecx, dword ptr [ebx + 0x1ba4]
  0x000ea5d8  push     eax
  0x000ea5d9  call     0x100724f0   ; -> ?Execute@CharacterActionHandler@GAME@@QAEXPAVCharacterAction@2@AAH@Z
  0x000ea5de  pop      edi
  0x000ea5df  pop      esi
  0x000ea5e0  pop      ebx
  0x000ea5e1  mov      esp, ebp
  0x000ea5e3  pop      ebp
  0x000ea5e4  ret      4
  0x000ea5e7  mov      ecx, dword ptr [ebx + 0x1ba4]
  0x000ea5ed  lea      eax, [ebp + 8]
  0x000ea5f0  push     eax
  0x000ea5f1  push     edi
  0x000ea5f2  call     0x100724f0   ; -> ?Execute@CharacterActionHandler@GAME@@QAEXPAVCharacterAction@2@AAH@Z
  0x000ea5f7  pop      edi
  0x000ea5f8  pop      esi
  0x000ea5f9  pop      ebx
  0x000ea5fa  mov      esp, ebp
  0x000ea5fc  pop      ebp
  0x000ea5fd  ret      4
  0x000ea600  cmp      eax, 1
  0x000ea603  jne      0x100ea624
  0x000ea605  mov      ecx, dword ptr [esi + 0x88]
  0x000ea60b  test     ecx, ecx
  0x000ea60d  je       0x100ea615
  0x000ea60f  mov      eax, dword ptr [ecx]
  0x000ea611  push     1
  0x000ea613  call     dword ptr [eax]
  0x000ea615  mov      dword ptr [esi + 0x88], edi
  0x000ea61b  pop      edi
  0x000ea61c  pop      esi
  0x000ea61d  pop      ebx
  0x000ea61e  mov      esp, ebp
  0x000ea620  pop      ebp
  0x000ea621  ret      4
  0x000ea624  cmp      eax, 2
  0x000ea627  jne      0x100ea635
  0x000ea629  test     edi, edi
  0x000ea62b  je       0x100ea635
  0x000ea62d  mov      eax, dword ptr [edi]
  0x000ea62f  mov      ecx, edi
  0x000ea631  push     1
  0x000ea633  call     dword ptr [eax]
  0x000ea635  pop      edi
  0x000ea636  pop      esi
  0x000ea637  pop      ebx
  0x000ea638  mov      esp, ebp
  0x000ea63a  pop      ebp
  0x000ea63b  ret      4
  0x000ea63e  int3     
  0x000ea63f  int3     
