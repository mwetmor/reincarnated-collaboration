; vector<Instance>::operator= — EndAttack transfer is OVERWRITE, not append
; Game.dll RVA 0x0020e2e0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020e2e0  push     ebp
  0x0020e2e1  mov      ebp, esp
  0x0020e2e3  push     ecx
  0x0020e2e4  push     ebx
  0x0020e2e5  mov      ebx, dword ptr [ebp + 8]
  0x0020e2e8  push     esi
  0x0020e2e9  push     edi
  0x0020e2ea  mov      edi, ecx
  0x0020e2ec  cmp      edi, ebx
  0x0020e2ee  je       0x1020e411
  0x0020e2f4  mov      esi, dword ptr [ebx]
  0x0020e2f6  mov      eax, dword ptr [ebx + 4]
  0x0020e2f9  cmp      esi, eax
  0x0020e2fb  jne      0x1020e30d
  0x0020e2fd  mov      eax, dword ptr [edi]
  0x0020e2ff  mov      dword ptr [edi + 4], eax
  0x0020e302  mov      eax, edi
  0x0020e304  pop      edi
  0x0020e305  pop      esi
  0x0020e306  pop      ebx
  0x0020e307  mov      esp, ebp
  0x0020e309  pop      ebp
  0x0020e30a  ret      4
  0x0020e30d  mov      ecx, eax
  0x0020e30f  mov      eax, 0x2aaaaaab
  0x0020e314  sub      ecx, esi
  0x0020e316  imul     ecx
  0x0020e318  mov      ecx, dword ptr [edi + 4]
  0x0020e31b  sub      ecx, dword ptr [edi]
  0x0020e31d  sar      edx, 2
  0x0020e320  mov      eax, edx
  0x0020e322  shr      eax, 0x1f
  0x0020e325  add      eax, edx
  0x0020e327  mov      dword ptr [ebp + 8], eax
  0x0020e32a  mov      eax, 0x2aaaaaab
  0x0020e32f  imul     ecx
  0x0020e331  sar      edx, 2
  0x0020e334  mov      eax, edx
  0x0020e336  shr      eax, 0x1f
  0x0020e339  add      eax, edx
  0x0020e33b  mov      dword ptr [ebp - 4], eax
  0x0020e33e  cmp      dword ptr [ebp + 8], eax
  0x0020e341  ja       0x1020e382
  0x0020e343  mov      ecx, dword ptr [ebx + 4]
  0x0020e346  mov      edx, dword ptr [edi]
  0x0020e348  sub      ecx, esi
  0x0020e34a  push     ecx
  0x0020e34b  push     esi
  0x0020e34c  push     edx
  0x0020e34d  call     dword ptr [0x104e63e4]   ; f32=1.17327e-38 i32=8372762 f64=2.82655e-306
  0x0020e353  mov      ecx, dword ptr [ebx + 4]
  0x0020e356  mov      eax, 0x2aaaaaab
  0x0020e35b  sub      ecx, dword ptr [ebx]
  0x0020e35d  add      esp, 0xc
  0x0020e360  imul     ecx
  0x0020e362  sar      edx, 2
  0x0020e365  mov      eax, edx
  0x0020e367  shr      eax, 0x1f
  0x0020e36a  add      eax, edx
  0x0020e36c  lea      ecx, [eax + eax*2]
  0x0020e36f  mov      eax, dword ptr [edi]
  0x0020e371  lea      eax, [eax + ecx*8]
  0x0020e374  mov      dword ptr [edi + 4], eax
  0x0020e377  mov      eax, edi
  0x0020e379  pop      edi
  0x0020e37a  pop      esi
  0x0020e37b  pop      ebx
  0x0020e37c  mov      esp, ebp
  0x0020e37e  pop      ebp
  0x0020e37f  ret      4
  0x0020e382  mov      ecx, dword ptr [edi + 8]
  0x0020e385  mov      eax, 0x2aaaaaab
  0x0020e38a  sub      ecx, dword ptr [edi]
  0x0020e38c  imul     ecx
  0x0020e38e  sar      edx, 2
  0x0020e391  mov      ecx, edx
  0x0020e393  shr      ecx, 0x1f
  0x0020e396  add      ecx, edx
  0x0020e398  cmp      dword ptr [ebp + 8], ecx
  0x0020e39b  ja       0x1020e3c4
  0x0020e39d  mov      eax, dword ptr [ebp - 4]
  0x0020e3a0  mov      ecx, dword ptr [ebx]
  0x0020e3a2  lea      eax, [eax + eax*2]
  0x0020e3a5  lea      esi, [esi + eax*8]
  0x0020e3a8  mov      eax, esi
  0x0020e3aa  sub      eax, ecx
  0x0020e3ac  push     eax
  0x0020e3ad  push     ecx
  0x0020e3ae  push     dword ptr [edi]
  0x0020e3b0  call     dword ptr [0x104e63e4]   ; f32=1.17327e-38 i32=8372762 f64=2.82655e-306
  0x0020e3b6  add      esp, 8
  0x0020e3b9  push     dword ptr [ebp + 8]
  0x0020e3bc  push     ecx
  0x0020e3bd  push     dword ptr [edi + 4]
  0x0020e3c0  mov      ecx, esi
  0x0020e3c2  jmp      0x1020e403   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x3fc3
  0x0020e3c4  mov      eax, dword ptr [edi]
  0x0020e3c6  test     eax, eax
  0x0020e3c8  je       0x1020e3d8
  0x0020e3ca  mov      edx, ecx
  0x0020e3cc  mov      ecx, eax
  0x0020e3ce  push     0x18
  0x0020e3d0  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x0020e3d5  add      esp, 4
  0x0020e3d8  mov      ecx, dword ptr [ebx + 4]
  0x0020e3db  mov      eax, 0x2aaaaaab
  0x0020e3e0  sub      ecx, dword ptr [ebx]
  0x0020e3e2  imul     ecx
  0x0020e3e4  mov      ecx, edi
  0x0020e3e6  sar      edx, 2
  0x0020e3e9  mov      eax, edx
  0x0020e3eb  shr      eax, 0x1f
  0x0020e3ee  add      eax, edx
  0x0020e3f0  push     eax
  0x0020e3f1  call     0x1000e0f0   ; -> ??0Controller@GAME@@QAE@ABV01@@Z+0x110
  0x0020e3f6  test     al, al
  0x0020e3f8  je       0x1020e411
  0x0020e3fa  push     ecx
  0x0020e3fb  push     dword ptr [ebp + 8]
  0x0020e3fe  push     ecx
