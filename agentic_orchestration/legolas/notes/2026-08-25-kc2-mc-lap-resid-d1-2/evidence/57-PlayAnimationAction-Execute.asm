=== 57-PlayAnimationAction-Execute  RVA 0x000704b0  sym=?Execute@PlayAnimationAction@GAME@@UAEXXZ ===
  0x000704b0  push     ebp
  0x000704b1  mov      ebp, esp
  0x000704b3  sub      esp, 0xc
  0x000704b6  push     esi
  0x000704b7  mov      esi, ecx
  0x000704b9  push     edi
  0x000704ba  push     dword ptr [esi + 4]
  0x000704bd  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000704c3  mov      ecx, eax
  0x000704c5  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000704ca  mov      edi, eax
  0x000704cc  test     edi, edi
  0x000704ce  jne      0x100704dd
  0x000704d0  mov      eax, dword ptr [esi]
  0x000704d2  mov      ecx, esi
  0x000704d4  call     dword ptr [eax + 0xc]
  0x000704d7  pop      edi
  0x000704d8  pop      esi
  0x000704d9  mov      esp, ebp
  0x000704db  pop      ebp
  0x000704dc  ret      
  0x000704dd  xor      eax, eax
  0x000704df  lea      ecx, [edi + 0x1c50]
  0x000704e5  push     ebx
  0x000704e6  cmp      dword ptr [ecx], 0
  0x000704e9  jne      0x100704fc
  0x000704eb  inc      eax
  0x000704ec  add      ecx, 4
  0x000704ef  cmp      eax, 2
  0x000704f2  jb       0x100704e6
  0x000704f4  mov      ebx, dword ptr [edi + 0x1c0c]
  0x000704fa  jmp      0x10070503   ; -> ?Execute@PlayAnimationAction@GAME@@UAEXXZ+0x53
  0x000704fc  mov      ebx, dword ptr [edi + eax*4 + 0x1c50]
  0x00070503  mov      eax, dword ptr [esi + 0x44]
  0x00070506  movss    xmm0, dword ptr [esi + 0x3c]
  0x0007050b  mov      dword ptr [ebp - 4], eax
  0x0007050e  mov      al, byte ptr [esi + 0x40]
  0x00070511  mov      byte ptr [ebp - 8], al
  0x00070514  mov      eax, dword ptr [esi + 0x34]
  0x00070517  mov      dword ptr [ebp - 0xc], eax
  0x0007051a  mov      dword ptr [ebx + 8], eax
  0x0007051d  cmp      eax, 0x33
  0x00070520  ja       0x10070528
  0x00070522  mov      ecx, dword ptr [ebx + eax*4 + 0xc]
  0x00070526  jmp      0x1007052b   ; -> ?Execute@PlayAnimationAction@GAME@@UAEXXZ+0x7b
  0x00070528  mov      ecx, dword ptr [ebx + 0xc]
  0x0007052b  push     dword ptr [ebp - 4]
  0x0007052e  mov      edx, dword ptr [ecx]
  0x00070530  lea      eax, [esi + 0x38]
  0x00070533  push     dword ptr [ebp - 8]
  0x00070536  push     ecx
  0x00070537  movss    dword ptr [esp], xmm0
  0x0007053c  push     eax
  0x0007053d  mov      eax, dword ptr [edx + 4]
  0x00070540  push     edi
  0x00070541  call     eax
  0x00070543  test     al, al
  0x00070545  je       0x10070556
  0x00070547  mov      eax, dword ptr [ebp - 0xc]
  0x0007054a  mov      dword ptr [ebx + 4], eax
  0x0007054d  mov      dword ptr [ebx + 8], 0
  0x00070554  jmp      0x1007055d   ; -> ?Execute@PlayAnimationAction@GAME@@UAEXXZ+0xad
  0x00070556  mov      eax, dword ptr [esi]
  0x00070558  mov      ecx, esi
  0x0007055a  call     dword ptr [eax + 0xc]
  0x0007055d  mov      eax, dword ptr [edi]
  0x0007055f  mov      ecx, edi
  0x00070561  push     2
  0x00070563  call     dword ptr [eax + 0x224]
  0x00070569  mov      cl, byte ptr [esi + 0x40]
  0x0007056c  mov      eax, dword ptr [esi + 0x34]
  0x0007056f  pop      ebx
  0x00070570  mov      dword ptr [edi + 0x193c], eax
  0x00070576  mov      byte ptr [edi + 0x1940], cl
  0x0007057c  pop      edi
  0x0007057d  pop      esi
  0x0007057e  mov      esp, ebp
  0x00070580  pop      ebp
  0x00070581  ret      
  0x00070582  int3     
  0x00070583  int3     
  0x00070584  int3     
  0x00070585  int3     
  0x00070586  int3     
  0x00070587  int3     
  0x00070588  int3     
  0x00070589  int3     
  0x0007058a  int3     
  0x0007058b  int3     
  0x0007058c  int3     
  0x0007058d  int3     
  0x0007058e  int3     
  0x0007058f  int3     
