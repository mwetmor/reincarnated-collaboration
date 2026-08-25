=== ??0JumpAttackAction@GAME@@QAE@ABV01@@Z 0x471ff0
  0x00471ff0  push     ebp
  0x00471ff1  mov      ebp, esp
  0x00471ff3  push     esi
  0x00471ff4  mov      esi, dword ptr [ebp + 8]
  0x00471ff7  push     edi
  0x00471ff8  push     esi
  0x00471ff9  mov      edi, ecx
  0x00471ffb  call     0x10471d50   ; -> ??0CharacterActionBase@GAME@@QAE@ABV01@@Z
  0x00472000  mov      dword ptr [edi], 0x10591f50
  0x00472006  mov      eax, dword ptr [esi + 0x34]
  0x00472009  mov      dword ptr [edi + 0x34], eax
  0x0047200c  movups   xmm0, xmmword ptr [esi + 0x38]
  0x00472010  movups   xmmword ptr [edi + 0x38], xmm0
  0x00472014  mov      eax, dword ptr [esi + 0x48]
  0x00472017  mov      dword ptr [edi + 0x48], eax
  0x0047201a  mov      eax, dword ptr [esi + 0x4c]
  0x0047201d  mov      dword ptr [edi + 0x4c], eax
  0x00472020  movups   xmm0, xmmword ptr [esi + 0x50]
  0x00472024  movups   xmmword ptr [edi + 0x50], xmm0
  0x00472028  mov      eax, dword ptr [esi + 0x60]
  0x0047202b  mov      dword ptr [edi + 0x60], eax
  0x0047202e  movzx    eax, byte ptr [esi + 0x64]
  0x00472032  mov      byte ptr [edi + 0x64], al
  0x00472035  mov      dword ptr [edi], 0x10591f0c
  0x0047203b  movups   xmm0, xmmword ptr [esi + 0x68]
  0x0047203f  movups   xmmword ptr [edi + 0x68], xmm0
  0x00472043  mov      eax, dword ptr [esi + 0x78]
  0x00472046  mov      dword ptr [edi + 0x78], eax
  0x00472049  mov      eax, dword ptr [esi + 0x7c]
  0x0047204c  mov      dword ptr [edi + 0x7c], eax
  0x0047204f  mov      eax, dword ptr [esi + 0x80]
  0x00472055  mov      dword ptr [edi + 0x80], eax
  0x0047205b  movzx    eax, byte ptr [esi + 0x84]
  0x00472062  mov      byte ptr [edi + 0x84], al
  0x00472068  mov      eax, edi
  0x0047206a  pop      edi
  0x0047206b  pop      esi
  0x0047206c  pop      ebp
  0x0047206d  ret      4
=== ??0JumpAttackAction@GAME@@QAE@IABVWorldVec3@1@0IIMW4AnimationSet_Type@1@ABVName@1@I_NABUTargetLeadingData@1@@Z 0x6dcf0
  0x0006dcf0  push     ebp
  0x0006dcf1  mov      ebp, esp
  0x0006dcf3  push     ecx
  0x0006dcf4  push     esi
  0x0006dcf5  push     dword ptr [ebp + 0x30]
  0x0006dcf8  mov      esi, ecx
  0x0006dcfa  push     dword ptr [ebp + 0x28]
  0x0006dcfd  mov      dword ptr [ebp - 4], esi
  0x0006dd00  push     dword ptr [ebp + 0x18]
  0x0006dd03  push     dword ptr [ebp + 0x10]
  0x0006dd06  push     dword ptr [ebp + 0x14]
  0x0006dd09  push     dword ptr [ebp + 8]
  0x0006dd0c  call     0x1006d2f0   ; -> ??0AttackAction@GAME@@QAE@IIABVWorldVec3@1@IIABUTargetLeadingData@1@@Z
  0x0006dd11  mov      eax, dword ptr [ebp + 0xc]
  0x0006dd14  mov      dword ptr [esi], 0x10591f0c
  0x0006dd1a  movups   xmm0, xmmword ptr [eax]
  0x0006dd1d  mov      eax, dword ptr [ebp + 0x20]
  0x0006dd20  mov      dword ptr [esi + 0x7c], eax
  0x0006dd23  mov      eax, dword ptr [ebp + 0x24]
  0x0006dd26  movups   xmmword ptr [esi + 0x68], xmm0
  0x0006dd2a  movss    xmm0, dword ptr [ebp + 0x1c]
  0x0006dd2f  movss    dword ptr [esi + 0x78], xmm0
  0x0006dd34  mov      eax, dword ptr [eax]
  0x0006dd36  mov      dword ptr [esi + 0x80], eax
  0x0006dd3c  mov      al, byte ptr [ebp + 0x2c]
  0x0006dd3f  mov      byte ptr [esi + 0x84], al
  0x0006dd45  mov      eax, esi
  0x0006dd47  pop      esi
  0x0006dd48  mov      esp, ebp
  0x0006dd4a  pop      ebp
  0x0006dd4b  ret      0x2c
  0x0006dd4e  int3     
  0x0006dd4f  int3     
=== ??0MoveAttackAction@GAME@@QAE@ABV01@@Z 0x4720e0
  0x004720e0  push     ebp
  0x004720e1  mov      ebp, esp
  0x004720e3  push     esi
  0x004720e4  mov      esi, dword ptr [ebp + 8]
  0x004720e7  push     edi
  0x004720e8  push     esi
  0x004720e9  mov      edi, ecx
  0x004720eb  call     0x10471d50   ; -> ??0CharacterActionBase@GAME@@QAE@ABV01@@Z
  0x004720f0  mov      dword ptr [edi], 0x10591f50
  0x004720f6  mov      eax, dword ptr [esi + 0x34]
  0x004720f9  mov      dword ptr [edi + 0x34], eax
  0x004720fc  movups   xmm0, xmmword ptr [esi + 0x38]
  0x00472100  movups   xmmword ptr [edi + 0x38], xmm0
  0x00472104  mov      eax, dword ptr [esi + 0x48]
  0x00472107  mov      dword ptr [edi + 0x48], eax
  0x0047210a  mov      eax, dword ptr [esi + 0x4c]
  0x0047210d  mov      dword ptr [edi + 0x4c], eax
  0x00472110  movups   xmm0, xmmword ptr [esi + 0x50]
  0x00472114  movups   xmmword ptr [edi + 0x50], xmm0
  0x00472118  mov      eax, dword ptr [esi + 0x60]
  0x0047211b  mov      dword ptr [edi + 0x60], eax
  0x0047211e  mov      al, byte ptr [esi + 0x64]
  0x00472121  mov      byte ptr [edi + 0x64], al
  0x00472124  mov      eax, edi
  0x00472126  mov      dword ptr [edi], 0x10591e84
  0x0047212c  movups   xmm0, xmmword ptr [esi + 0x68]
  0x00472130  movups   xmmword ptr [edi + 0x68], xmm0
  0x00472134  pop      edi
  0x00472135  pop      esi
  0x00472136  pop      ebp
  0x00472137  ret      4
  0x0047213a  int3     
  0x0047213b  int3     
  0x0047213c  int3     
  0x0047213d  int3     
  0x0047213e  int3     
  0x0047213f  int3     
=== ??0MoveAttackAction@GAME@@QAE@IIABVWorldVec3@1@0IIABUTargetLeadingData@1@@Z 0x6ea60
  0x0006ea60  push     ebp
  0x0006ea61  mov      ebp, esp
  0x0006ea63  push     ecx
  0x0006ea64  push     esi
  0x0006ea65  push     dword ptr [ebp + 0x20]
  0x0006ea68  mov      esi, ecx
  0x0006ea6a  push     dword ptr [ebp + 0x1c]
  0x0006ea6d  mov      dword ptr [ebp - 4], esi
  0x0006ea70  push     dword ptr [ebp + 0x18]
  0x0006ea73  push     dword ptr [ebp + 0x14]
  0x0006ea76  push     dword ptr [ebp + 0xc]
  0x0006ea79  push     dword ptr [ebp + 8]
  0x0006ea7c  call     0x1006d2f0   ; -> ??0AttackAction@GAME@@QAE@IIABVWorldVec3@1@IIABUTargetLeadingData@1@@Z
  0x0006ea81  mov      eax, dword ptr [ebp + 0x10]
  0x0006ea84  mov      dword ptr [esi], 0x10591e84
  0x0006ea8a  movups   xmm0, xmmword ptr [eax]
  0x0006ea8d  mov      eax, esi
  0x0006ea8f  movups   xmmword ptr [esi + 0x68], xmm0
  0x0006ea93  pop      esi
  0x0006ea94  mov      esp, ebp
  0x0006ea96  pop      ebp
  0x0006ea97  ret      0x1c
  0x0006ea9a  int3     
  0x0006ea9b  int3     
  0x0006ea9c  int3     
  0x0006ea9d  int3     
  0x0006ea9e  int3     
  0x0006ea9f  int3     
