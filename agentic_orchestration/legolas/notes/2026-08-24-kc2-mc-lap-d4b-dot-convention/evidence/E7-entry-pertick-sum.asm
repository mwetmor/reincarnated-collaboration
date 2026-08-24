; entry vtable slot2 @0x20da10 — per-tick sum over 24-byte instances
; Game.dll RVA 0x0020da10  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020da10  push     ebp
  0x0020da11  mov      ebp, esp
  0x0020da13  sub      esp, 0x1c
  0x0020da16  mov      eax, ecx
  0x0020da18  xorps    xmm1, xmm1
  0x0020da1b  mov      dword ptr [ebp - 0x10], eax
  0x0020da1e  push     edi
  0x0020da1f  movss    dword ptr [ebp - 0x18], xmm1
  0x0020da24  mov      ecx, dword ptr [eax + 0x20]
  0x0020da27  mov      eax, dword ptr [eax + 0x14]
  0x0020da2a  mov      dword ptr [ebp - 0x14], ecx
  0x0020da2d  mov      edi, dword ptr [eax]
  0x0020da2f  cmp      edi, eax
  0x0020da31  je       0x1020dbb6
  0x0020da37  mov      eax, dword ptr [ebp - 0x10]
  0x0020da3a  push     ebx
  0x0020da3b  push     esi
  0x0020da3c  nop      dword ptr [eax]
  0x0020da40  test     ecx, ecx
  0x0020da42  jle      0x1020dbb4
  0x0020da48  mov      esi, dword ptr [edi + 8]
  0x0020da4b  cmp      esi, dword ptr [edi + 0xc]
  0x0020da4e  je       0x1020dba5
  0x0020da54  mov      ecx, dword ptr [ebp + 8]
  0x0020da57  nop      word ptr [eax + eax]
  0x0020da60  addss    xmm1, dword ptr [esi + 4]
  0x0020da65  mov      ebx, dword ptr [ecx + 4]
  0x0020da68  xor      eax, eax
  0x0020da6a  cmp      dword ptr [esi + 0x14], eax
  0x0020da6d  setne    al
  0x0020da70  movss    dword ptr [ebp - 0xc], xmm1
  0x0020da75  movss    dword ptr [ebp - 0x18], xmm1
  0x0020da7a  lea      edx, [eax*8 + 0xc]
  0x0020da81  add      edx, esi
  0x0020da83  mov      dword ptr [ebp - 8], edx
  0x0020da86  cmp      edx, ebx
  0x0020da88  jae      0x1020db0f
  0x0020da8e  mov      eax, dword ptr [ecx]
  0x0020da90  cmp      eax, edx
  0x0020da92  ja       0x1020db0f
  0x0020da94  sub      edx, eax
  0x0020da96  mov      eax, dword ptr [ecx + 8]
  0x0020da99  sar      edx, 2
  0x0020da9c  mov      dword ptr [ebp - 8], edx
  0x0020da9f  mov      dword ptr [ebp - 4], eax
  0x0020daa2  cmp      ebx, eax
  0x0020daa4  jne      0x1020db01
  0x0020daa6  sub      eax, ebx
  0x0020daa8  sar      eax, 2
  0x0020daab  cmp      eax, 1
  0x0020daae  jae      0x1020db01
  0x0020dab0  mov      ecx, dword ptr [ecx]
  0x0020dab2  mov      eax, 0x3fffffff
  0x0020dab7  sub      ebx, ecx
  0x0020dab9  sar      ebx, 2
  0x0020dabc  sub      eax, ebx
  0x0020dabe  cmp      eax, 1
  0x0020dac1  jb       0x1020dbc0
  0x0020dac7  mov      edx, dword ptr [ebp - 4]
  0x0020daca  inc      ebx
  0x0020dacb  sub      edx, ecx
  0x0020dacd  mov      ecx, 0x3fffffff
  0x0020dad2  sar      edx, 2
  0x0020dad5  mov      eax, edx
  0x0020dad7  mov      dword ptr [ebp - 4], edx
  0x0020dada  shr      eax, 1
  0x0020dadc  sub      ecx, eax
  0x0020dade  add      eax, edx
  0x0020dae0  xor      edx, edx
  0x0020dae2  cmp      ecx, dword ptr [ebp - 4]
  0x0020dae5  mov      ecx, dword ptr [ebp + 8]
  0x0020dae8  cmovae   edx, eax
  0x0020daeb  cmp      edx, ebx
  0x0020daed  cmovae   ebx, edx
  0x0020daf0  push     ebx
  0x0020daf1  call     0x1000a8d0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0x510
  0x0020daf6  movss    xmm1, dword ptr [ebp - 0xc]
  0x0020dafb  mov      ecx, dword ptr [ebp + 8]
  0x0020dafe  mov      edx, dword ptr [ebp - 8]
  0x0020db01  mov      ebx, dword ptr [ecx + 4]
  0x0020db04  test     ebx, ebx
  0x0020db06  je       0x1020db7f
  0x0020db08  mov      eax, dword ptr [ecx]
  0x0020db0a  mov      eax, dword ptr [eax + edx*4]
  0x0020db0d  jmp      0x1020db7d   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x373d
  0x0020db0f  mov      eax, dword ptr [ecx + 8]
  0x0020db12  mov      dword ptr [ebp - 4], eax
  0x0020db15  cmp      ebx, eax
  0x0020db17  jne      0x1020db74
  0x0020db19  sub      eax, ebx
  0x0020db1b  sar      eax, 2
  0x0020db1e  cmp      eax, 1
  0x0020db21  jae      0x1020db74
  0x0020db23  mov      ecx, dword ptr [ecx]
  0x0020db25  mov      eax, 0x3fffffff
  0x0020db2a  sub      ebx, ecx
  0x0020db2c  sar      ebx, 2
  0x0020db2f  sub      eax, ebx
  0x0020db31  cmp      eax, 1
  0x0020db34  jb       0x1020dbc0
  0x0020db3a  mov      edx, dword ptr [ebp - 4]
  0x0020db3d  inc      ebx
  0x0020db3e  sub      edx, ecx
  0x0020db40  mov      ecx, 0x3fffffff
  0x0020db45  sar      edx, 2
  0x0020db48  mov      eax, edx
  0x0020db4a  mov      dword ptr [ebp - 4], edx
  0x0020db4d  shr      eax, 1
  0x0020db4f  sub      ecx, eax
  0x0020db51  add      eax, edx
  0x0020db53  xor      edx, edx
  0x0020db55  cmp      ecx, dword ptr [ebp - 4]
  0x0020db58  mov      ecx, dword ptr [ebp + 8]
  0x0020db5b  cmovae   edx, eax
  0x0020db5e  cmp      edx, ebx
  0x0020db60  cmovae   ebx, edx
  0x0020db63  push     ebx
  0x0020db64  call     0x1000a8d0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0x510
  0x0020db69  movss    xmm1, dword ptr [ebp - 0xc]
  0x0020db6e  mov      ecx, dword ptr [ebp + 8]
  0x0020db71  mov      edx, dword ptr [ebp - 8]
  0x0020db74  mov      ebx, dword ptr [ecx + 4]
  0x0020db77  test     ebx, ebx
  0x0020db79  je       0x1020db7f
  0x0020db7b  mov      eax, dword ptr [edx]
  0x0020db7d  mov      dword ptr [ebx], eax
  0x0020db7f  mov      eax, dword ptr [ebp + 0xc]
  0x0020db82  movss    xmm0, dword ptr [esi + 8]
  0x0020db87  add      esi, 0x18
  0x0020db8a  add      dword ptr [ecx + 4], 4
  0x0020db8e  maxss    xmm0, dword ptr [eax]
  0x0020db92  movss    dword ptr [eax], xmm0
  0x0020db96  cmp      esi, dword ptr [edi + 0xc]
  0x0020db99  jne      0x1020da60
  0x0020db9f  mov      ecx, dword ptr [ebp - 0x14]
  0x0020dba2  mov      eax, dword ptr [ebp - 0x10]
  0x0020dba5  mov      edi, dword ptr [edi]
  0x0020dba7  dec      ecx
  0x0020dba8  mov      dword ptr [ebp - 0x14], ecx
  0x0020dbab  cmp      edi, dword ptr [eax + 0x14]
