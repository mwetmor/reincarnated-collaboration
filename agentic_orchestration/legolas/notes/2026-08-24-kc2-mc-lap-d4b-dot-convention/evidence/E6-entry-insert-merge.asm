; entry vtable slot1 @0x20d6b0 — THE DECISIVE SITE: nTicks=dur*10.0, perTick=dmg*0.1
; Game.dll RVA 0x0020d6b0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020d6b0  push     ebp
  0x0020d6b1  mov      ebp, esp
  0x0020d6b3  push     -1
  0x0020d6b5  push     0x104cb820
  0x0020d6ba  mov      eax, dword ptr fs:[0]
  0x0020d6c0  push     eax
  0x0020d6c1  mov      dword ptr fs:[0], esp
  0x0020d6c8  sub      esp, 0x54
  0x0020d6cb  mov      eax, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x0020d6d0  push     ebx
  0x0020d6d1  push     esi
  0x0020d6d2  push     edi
  0x0020d6d3  add      eax, 0x292d4
  0x0020d6d8  mov      esi, ecx
  0x0020d6da  push     eax
  0x0020d6db  lea      ecx, [ebp - 0x48]
  0x0020d6de  call     0x1000c220   ; -> ?IsUsedForDisplay@CombatAttributeAccumulator@GAME@@UAE_NXZ+0x80
  0x0020d6e3  mov      dword ptr [ebp - 4], 0
  0x0020d6ea  mov      ecx, dword ptr [ebp + 8]
  0x0020d6ed  cmp      dword ptr [ecx + 0x10], 0
  0x0020d6f1  movss    xmm0, dword ptr [ecx + 8]
  0x0020d6f6  mulss    xmm0, dword ptr [0x105f58a4]   ; f32=10 i32=1092616192 f64=2.09715e+06
  0x0020d6fe  cvttss2si eax, xmm0
  0x0020d702  mov      dword ptr [ebp - 0x14], eax
  0x0020d705  je       0x1020d715
  0x0020d707  mov      eax, dword ptr [ecx + 0x10]
  0x0020d70a  mov      dword ptr [ebp - 0x28], eax
  0x0020d70d  mov      eax, dword ptr [ecx + 0x14]
  0x0020d710  mov      dword ptr [ebp - 0x24], eax
  0x0020d713  jmp      0x1020d722   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x32e2
  0x0020d715  mov      eax, dword ptr [ecx + 0x18]
  0x0020d718  mov      dword ptr [ebp - 0x28], eax
  0x0020d71b  mov      dword ptr [ebp - 0x24], 0
  0x0020d722  cmp      dword ptr [esi + 0x10], 0
  0x0020d726  lea      eax, [ebp - 0x28]
  0x0020d729  mov      ecx, dword ptr [eax]
  0x0020d72b  lea      ebx, [esi + 0xc]
  0x0020d72e  mov      eax, dword ptr [eax + 4]
  0x0020d731  mov      dword ptr [ebp - 0x18], ecx
  0x0020d734  mov      dword ptr [ebp - 0x1c], eax
  0x0020d737  mov      dword ptr [ebp - 0x20], ebx
  0x0020d73a  jne      0x1020d74f
  0x0020d73c  lea      eax, [esi + 0x14]
  0x0020d73f  cmp      ebx, eax
  0x0020d741  je       0x1020d74f
  0x0020d743  mov      eax, dword ptr [eax]
  0x0020d745  mov      ecx, ebx
  0x0020d747  push     eax
  0x0020d748  push     dword ptr [eax]
  0x0020d74a  call     0x1020c6c0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2280
  0x0020d74f  mov      ecx, dword ptr [ebp - 0x14]
  0x0020d752  cmp      dword ptr [ebx + 4], ecx
  0x0020d755  jae      0x1020d7ac
  0x0020d757  mov      dword ptr [ebp - 0x3c], 0
  0x0020d75e  mov      dword ptr [ebp - 0x38], 0
  0x0020d765  mov      dword ptr [ebp - 0x34], 0
  0x0020d76c  lea      eax, [ebp - 0x3c]
  0x0020d76f  mov      byte ptr [ebp - 4], 1
  0x0020d773  push     eax
  0x0020d774  push     ecx
  0x0020d775  mov      ecx, ebx
  0x0020d777  call     0x1020e4b0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4070
  0x0020d77c  mov      byte ptr [ebp - 4], 0
  0x0020d780  mov      ecx, dword ptr [ebp - 0x3c]
  0x0020d783  test     ecx, ecx
  0x0020d785  je       0x1020d7a9
  0x0020d787  mov      edx, dword ptr [ebp - 0x34]
  0x0020d78a  mov      eax, 0x2aaaaaab
  0x0020d78f  sub      edx, ecx
  0x0020d791  imul     edx
  0x0020d793  push     0x18
  0x0020d795  mov      eax, edx
  0x0020d797  sar      eax, 2
  0x0020d79a  mov      edx, eax
  0x0020d79c  shr      edx, 0x1f
  0x0020d79f  add      edx, eax
  0x0020d7a1  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x0020d7a6  add      esp, 4
  0x0020d7a9  mov      ecx, dword ptr [ebp - 0x14]
  0x0020d7ac  mov      edx, dword ptr [ebp + 8]
  0x0020d7af  mov      eax, dword ptr [ebx]
  0x0020d7b1  movss    xmm1, dword ptr [edx]
  0x0020d7b5  mulss    xmm1, dword ptr [0x105f57ac]   ; f32=0.1 i32=1036831949 f64=4.65661e-10
  0x0020d7bd  mov      edi, dword ptr [eax]
  0x0020d7bf  movss    dword ptr [ebp - 0x24], xmm1
  0x0020d7c4  cmp      edi, eax
  0x0020d7c6  je       0x1020d904
  0x0020d7cc  mov      bl, byte ptr [ebp + 0xb]
  0x0020d7cf  nop      
  0x0020d7d0  test     ecx, ecx
  0x0020d7d2  jle      0x1020d904
  0x0020d7d8  mov      eax, dword ptr [edi + 8]
  0x0020d7db  lea      esi, [edi + 8]
  0x0020d7de  xor      bh, bh
  0x0020d7e0  cmp      eax, dword ptr [edi + 0xc]
  0x0020d7e3  je       0x1020d840
  0x0020d7e5  lea      esi, [eax + 0xc]
  0x0020d7e8  cmp      dword ptr [esi], 0
  0x0020d7eb  je       0x1020d7fd
  0x0020d7ed  mov      edx, dword ptr [esi]
  0x0020d7ef  mov      dword ptr [ebp - 0x30], edx
  0x0020d7f2  mov      edx, dword ptr [esi + 4]
  0x0020d7f5  mov      dword ptr [ebp - 0x2c], edx
  0x0020d7f8  lea      edx, [ebp - 0x30]
  0x0020d7fb  jmp      0x1020d80d   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x33cd
  0x0020d7fd  mov      edx, dword ptr [esi + 8]
  0x0020d800  mov      dword ptr [ebp - 0x38], edx
  0x0020d803  lea      edx, [ebp - 0x38]
  0x0020d806  mov      dword ptr [ebp - 0x34], 0
  0x0020d80d  mov      ecx, dword ptr [ebp - 0x18]
  0x0020d810  cmp      dword ptr [edx], ecx
  0x0020d812  mov      ecx, dword ptr [edi + 0xc]
  0x0020d815  jne      0x1020d830
  0x0020d817  mov      ecx, dword ptr [ebp - 0x1c]
  0x0020d81a  cmp      dword ptr [edx + 4], ecx
  0x0020d81d  mov      ecx, dword ptr [edi + 0xc]
  0x0020d820  jne      0x1020d830
  0x0020d822  movss    xmm0, dword ptr [eax]
  0x0020d826  mov      bh, 1
  0x0020d828  maxss    xmm0, xmm1
  0x0020d82c  movss    dword ptr [eax], xmm0
  0x0020d830  add      eax, 0x18
  0x0020d833  add      esi, 0x18
  0x0020d836  cmp      eax, ecx
  0x0020d838  jne      0x1020d7e8
  0x0020d83a  mov      edx, dword ptr [ebp + 8]
  0x0020d83d  lea      esi, [edi + 8]
  0x0020d840  test     bh, bh
  0x0020d842  jne      0x1020d875
  0x0020d844  mov      eax, dword ptr [edx + 0x10]
  0x0020d847  mov      ecx, esi
  0x0020d849  movss    xmm0, dword ptr [edx + 0xc]
  0x0020d84e  mov      dword ptr [ebp - 0x54], eax
  0x0020d851  mov      eax, dword ptr [edx + 0x14]
  0x0020d854  mov      dword ptr [ebp - 0x50], eax
  0x0020d857  mov      eax, dword ptr [edx + 0x18]
  0x0020d85a  mov      dword ptr [ebp - 0x4c], eax
  0x0020d85d  lea      eax, [ebp - 0x60]
  0x0020d860  push     eax
  0x0020d861  movss    dword ptr [ebp - 0x60], xmm1
  0x0020d866  movss    dword ptr [ebp - 0x5c], xmm1
  0x0020d86b  movss    dword ptr [ebp - 0x58], xmm0
  0x0020d870  call     0x1020e420   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x3fe0
  0x0020d875  mov      edx, dword ptr [edi + 0xc]
  0x0020d878  lea      eax, [ebp - 0x10]
  0x0020d87b  mov      ecx, dword ptr [edi + 8]
  0x0020d87e  sub      edx, ecx
  0x0020d880  push     eax
  0x0020d881  mov      eax, 0x2aaaaaab
  0x0020d886  mov      byte ptr [ebp - 0x10], bl
  0x0020d889  imul     edx
  0x0020d88b  sar      edx, 2
  0x0020d88e  mov      eax, edx
  0x0020d890  shr      eax, 0x1f
  0x0020d893  add      eax, edx
  0x0020d895  mov      edx, dword ptr [edi + 0xc]
  0x0020d898  push     eax
  0x0020d899  call     0x1020ea70   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4630
  0x0020d89e  mov      eax, dword ptr [edi + 8]
  0x0020d8a1  add      esp, 8
  0x0020d8a4  xor      esi, esi
  0x0020d8a6  cmp      eax, dword ptr [edi + 0xc]
  0x0020d8a9  je       0x1020d8e8
  0x0020d8ab  mov      edx, dword ptr [ebp - 0x44]
  0x0020d8ae  sub      edx, dword ptr [ebp - 0x48]
  0x0020d8b1  movss    xmm1, dword ptr [0x105f5780]   ; f32=0.01 i32=1008981770 f64=5.37372e-17
  0x0020d8b9  sar      edx, 2
  0x0020d8bc  lea      ecx, [edx - 1]
  0x0020d8bf  nop      
  0x0020d8c0  cmp      esi, edx
  0x0020d8c2  cmovb    ecx, esi
  0x0020d8c5  mov      esi, dword ptr [ebp - 0x48]
  0x0020d8c8  movss    xmm0, dword ptr [esi + ecx*4]
  0x0020d8cd  lea      esi, [ecx + 1]
  0x0020d8d0  mulss    xmm0, xmm1
  0x0020d8d4  lea      ecx, [edx - 1]
  0x0020d8d7  mulss    xmm0, dword ptr [eax]
  0x0020d8db  movss    dword ptr [eax + 4], xmm0
  0x0020d8e0  add      eax, 0x18
  0x0020d8e3  cmp      eax, dword ptr [edi + 0xc]
  0x0020d8e6  jne      0x1020d8c0
  0x0020d8e8  mov      eax, dword ptr [ebp - 0x20]
  0x0020d8eb  mov      ecx, dword ptr [ebp - 0x14]
  0x0020d8ee  mov      edi, dword ptr [edi]
  0x0020d8f0  dec      ecx
  0x0020d8f1  movss    xmm1, dword ptr [ebp - 0x24]
  0x0020d8f6  mov      edx, dword ptr [ebp + 8]
  0x0020d8f9  mov      dword ptr [ebp - 0x14], ecx
  0x0020d8fc  cmp      edi, dword ptr [eax]
  0x0020d8fe  jne      0x1020d7d0
  0x0020d904  mov      eax, dword ptr [ebp - 0x48]
  0x0020d907  pop      edi
  0x0020d908  pop      esi
  0x0020d909  pop      ebx
  0x0020d90a  test     eax, eax
  0x0020d90c  je       0x1020d922
  0x0020d90e  mov      edx, dword ptr [ebp - 0x40]
  0x0020d911  mov      ecx, eax
  0x0020d913  sub      edx, eax
  0x0020d915  push     4
