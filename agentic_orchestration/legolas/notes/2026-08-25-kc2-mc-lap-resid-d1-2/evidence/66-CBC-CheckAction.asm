=== 66-CBC-CheckAction RVA 0x000ea260 sym=?CheckAction@ControllerBaseCharacter@GAME@@MBE?AW4CharacterActionPermission@2@PAVCharacterAction@2@@Z ===
  0x000ea260  push     ebp
  0x000ea261  mov      ebp, esp
  0x000ea263  push     ecx
  0x000ea264  push     ebx
  0x000ea265  mov      ebx, dword ptr [ebp + 8]
  0x000ea268  push     esi
  0x000ea269  mov      esi, ecx
  0x000ea26b  mov      ecx, ebx
  0x000ea26d  push     edi
  0x000ea26e  mov      eax, dword ptr [ebx]
  0x000ea270  mov      dword ptr [ebp - 4], esi
  0x000ea273  call     dword ptr [eax + 0x2c]
  0x000ea276  push     dword ptr [esi + 0x24]
  0x000ea279  mov      edi, eax
  0x000ea27b  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ea281  mov      ecx, eax
  0x000ea283  call     0x1000b260   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xea0
  0x000ea288  mov      esi, eax
  0x000ea28a  test     esi, esi
  0x000ea28c  je       0x100ea347
  0x000ea292  mov      ecx, dword ptr [esi + 0x1ba4]
  0x000ea298  mov      ecx, dword ptr [ecx + 4]
  0x000ea29b  test     ecx, ecx
  0x000ea29d  je       0x100ea2aa
  0x000ea29f  mov      eax, dword ptr [ecx]
  0x000ea2a1  mov      eax, dword ptr [eax + 0x18]
  0x000ea2a4  call     eax
  0x000ea2a6  test     al, al
  0x000ea2a8  jne      0x100ea2c1
  0x000ea2aa  mov      eax, dword ptr [ebx]
  0x000ea2ac  mov      ecx, ebx
  0x000ea2ae  call     dword ptr [eax + 0x2c]
  0x000ea2b1  cmp      eax, 8
  0x000ea2b4  je       0x100ea2c1
  0x000ea2b6  pop      edi
  0x000ea2b7  pop      esi
  0x000ea2b8  xor      eax, eax
  0x000ea2ba  pop      ebx
  0x000ea2bb  mov      esp, ebp
  0x000ea2bd  pop      ebp
  0x000ea2be  ret      4
  0x000ea2c1  mov      eax, dword ptr [esi + 0x1ba4]
  0x000ea2c7  mov      ecx, dword ptr [eax + 4]
  0x000ea2ca  test     ecx, ecx
  0x000ea2cc  je       0x100ea2dc
  0x000ea2ce  mov      eax, dword ptr [ecx]
  0x000ea2d0  call     dword ptr [eax + 0x2c]
  0x000ea2d3  mov      ebx, eax
  0x000ea2d5  cmp      ebx, 8
  0x000ea2d8  je       0x100ea306
  0x000ea2da  jmp      0x100ea2de   ; -> ?CheckAction@ControllerBaseCharacter@GAME@@MBE?AW4CharacterActionPermission@2@PAVCharacterAction@2@@Z+0x7e
  0x000ea2dc  xor      ebx, ebx
  0x000ea2de  push     dword ptr [esi + 0x760]
  0x000ea2e4  mov      eax, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ea2e9  call     eax
  0x000ea2eb  mov      ecx, eax
  0x000ea2ed  call     0x1000d4f0   ; -> ?CreateUISummaryText@AmbientCharacter@GAME@@UBEXW4GameTextClass@2@AAV?$vector@UGameTextLine@GAME@@@mem@@@Z+0x7e0
  0x000ea2f2  mov      ecx, eax
  0x000ea2f4  test     ecx, ecx
  0x000ea2f6  je       0x100ea306
  0x000ea2f8  mov      eax, dword ptr [ecx]
  0x000ea2fa  mov      eax, dword ptr [eax + 0x2d4]
  0x000ea300  call     eax
  0x000ea302  test     al, al
  0x000ea304  jne      0x100ea2b6
  0x000ea306  mov      eax, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x000ea30b  imul     ecx, edi, 0x1a
  0x000ea30e  add      ecx, ebx
  0x000ea310  mov      eax, dword ptr [eax + ecx*4 + 0x2802c]
  0x000ea317  cmp      eax, 3
  0x000ea31a  jne      0x100ea3a2
  0x000ea320  mov      eax, dword ptr [esi + 0x1ba4]
  0x000ea326  mov      ecx, dword ptr [eax + 4]
  0x000ea329  test     ecx, ecx
  0x000ea32b  je       0x100ea2b6
  0x000ea32d  mov      edx, dword ptr [ebp - 4]
  0x000ea330  mov      eax, dword ptr [ecx]
  0x000ea332  push     dword ptr [edx + 0x88]
  0x000ea338  push     dword ptr [ebp + 8]
  0x000ea33b  call     dword ptr [eax + 0x40]
  0x000ea33e  pop      edi
  0x000ea33f  pop      esi
  0x000ea340  pop      ebx
  0x000ea341  mov      esp, ebp
  0x000ea343  pop      ebp
  0x000ea344  ret      4
  0x000ea347  mov      edx, dword ptr [ebp - 4]
  0x000ea34a  mov      eax, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000ea34f  push     dword ptr [edx + 0x24]
  0x000ea352  call     eax
  0x000ea354  mov      ecx, eax
  0x000ea356  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000ea35b  mov      esi, eax
  0x000ea35d  test     esi, esi
  0x000ea35f  je       0x100ea39d
  0x000ea361  mov      edx, dword ptr [esi]
  0x000ea363  mov      ecx, esi
  0x000ea365  call     dword ptr [edx + 0x21c]
  0x000ea36b  cmp      eax, 4
  0x000ea36e  jne      0x100ea3ab
  0x000ea370  cmp      edi, 0x14
  0x000ea373  jne      0x100ea39d
  0x000ea375  cmp      edi, 0xf
  0x000ea378  jne      0x100ea2b6
  0x000ea37e  mov      eax, dword ptr [esi + 0x1ba4]
  0x000ea384  mov      ecx, dword ptr [eax + 4]
  0x000ea387  test     ecx, ecx
  0x000ea389  je       0x100ea2b6
  0x000ea38f  mov      eax, dword ptr [ecx]
  0x000ea391  call     dword ptr [eax + 0x2c]
  0x000ea394  cmp      eax, 0xf
  0x000ea397  jne      0x100ea2b6
  0x000ea39d  mov      eax, 2
  0x000ea3a2  pop      edi
  0x000ea3a3  pop      esi
  0x000ea3a4  pop      ebx
  0x000ea3a5  mov      esp, ebp
  0x000ea3a7  pop      ebp
  0x000ea3a8  ret      4
  0x000ea3ab  cmp      eax, 3
  0x000ea3ae  jne      0x100ea375
  0x000ea3b0  cmp      edi, 0xf
  0x000ea3b3  je       0x100ea37e
  0x000ea3b5  pop      edi
  0x000ea3b6  pop      esi
  0x000ea3b7  mov      eax, 2
  0x000ea3bc  pop      ebx
  0x000ea3bd  mov      esp, ebp
  0x000ea3bf  pop      ebp
  0x000ea3c0  ret      4
  0x000ea3c3  int3     
  0x000ea3c4  int3     
  0x000ea3c5  int3     
  0x000ea3c6  int3     
  0x000ea3c7  int3     
  0x000ea3c8  int3     
  0x000ea3c9  int3     
  0x000ea3ca  int3     
  0x000ea3cb  int3     
  0x000ea3cc  int3     
  0x000ea3cd  int3     
  0x000ea3ce  int3     
  0x000ea3cf  int3     
