; DurationDamageManager::AddDamage (damage stored verbatim)
; Game.dll RVA 0x00208a30  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x00208a30  push     ebp
  0x00208a31  mov      ebp, esp
  0x00208a33  mov      eax, dword ptr fs:[0]
  0x00208a39  push     -1
  0x00208a3b  push     0x104cb608
  0x00208a40  push     eax
  0x00208a41  mov      dword ptr fs:[0], esp
  0x00208a48  sub      esp, 0x68
  0x00208a4b  push     ebx
  0x00208a4c  mov      ebx, ecx
  0x00208a4e  mov      ecx, dword ptr [ebx + 4]
  0x00208a51  mov      eax, dword ptr [ecx]
  0x00208a53  mov      eax, dword ptr [eax + 0x418]
  0x00208a59  call     eax
  0x00208a5b  test     al, al
  0x00208a5d  jne      0x10208c1e
  0x00208a63  mov      ecx, dword ptr [ebx + 4]
  0x00208a66  mov      eax, dword ptr [ecx]
  0x00208a68  call     dword ptr [eax + 0x228]
  0x00208a6e  cmp      eax, 0x15
  0x00208a71  je       0x10208c1e
  0x00208a77  movss    xmm0, dword ptr [ebp + 0xc]
  0x00208a7c  xorps    xmm1, xmm1
  0x00208a7f  comiss   xmm0, xmm1
  0x00208a82  jbe      0x10208c1e
  0x00208a88  movss    xmm0, dword ptr [ebp + 0x10]
  0x00208a8d  comiss   xmm0, xmm1
  0x00208a90  jbe      0x10208c1e
  0x00208a96  push     esi
  0x00208a97  mov      esi, dword ptr [ebp + 8]
  0x00208a9a  mov      ecx, ebx
  0x00208a9c  push     edi
  0x00208a9d  push     esi
  0x00208a9e  call     0x1020a3e0   ; -> ?AddDamageEffect@DurationDamageManager@GAME@@IAEXW4CombatAttributeType@2@@Z
  0x00208aa3  xor      al, al
  0x00208aa5  xor      ecx, ecx
  0x00208aa7  mov      byte ptr [ebp - 0xd], al
  0x00208aaa  mov      eax, 0x38e38e39
  0x00208aaf  mov      dword ptr [ebp - 0x14], ecx
  0x00208ab2  mov      ecx, dword ptr [ebx + 0x30]
  0x00208ab5  sub      ecx, dword ptr [ebx + 0x2c]
  0x00208ab8  imul     ecx
  0x00208aba  sar      edx, 3
  0x00208abd  mov      eax, edx
  0x00208abf  shr      eax, 0x1f
  0x00208ac2  add      eax, edx
  0x00208ac4  je       0x10208b78
  0x00208aca  xor      esi, esi
  0x00208acc  nop      dword ptr [eax]
  0x00208ad0  mov      eax, dword ptr [ebx + 0x2c]
  0x00208ad3  mov      ecx, dword ptr [ebp + 8]
  0x00208ad6  cmp      dword ptr [eax + esi + 8], ecx
  0x00208ada  jne      0x10208b44
  0x00208adc  mov      eax, dword ptr [eax + esi + 4]
  0x00208ae0  cmp      eax, dword ptr [ebx + 0x18]
  0x00208ae3  jne      0x10208b44
  0x00208ae5  movss    xmm0, dword ptr [ebp + 0x10]
  0x00208aea  push     ecx
  0x00208aeb  movss    dword ptr [esp], xmm0
  0x00208af0  push     ecx
  0x00208af1  mov      ecx, ebx
  0x00208af3  call     0x10209db0   ; -> ?ModifyDuration@DurationDamageManager@GAME@@IAEMW4CombatAttributeType@2@M@Z
  0x00208af8  mov      ecx, dword ptr [ebp + 0x14]
  0x00208afb  lea      edx, [ebp - 0x34]
  0x00208afe  movss    xmm0, dword ptr [ebp + 0xc]
  0x00208b03  movss    dword ptr [ebp - 0x34], xmm0
  0x00208b08  movss    dword ptr [ebp - 0x30], xmm0
  0x00208b0d  mov      eax, dword ptr [ecx]
  0x00208b0f  mov      dword ptr [ebp - 0x24], eax
  0x00208b12  mov      eax, dword ptr [ecx + 4]
  0x00208b15  mov      ecx, dword ptr [ebx + 0x2c]
  0x00208b18  fstp     dword ptr [ebp - 0x18]
  0x00208b1b  movss    xmm0, dword ptr [ebp - 0x18]
  0x00208b20  add      ecx, esi
  0x00208b22  movss    dword ptr [ebp - 0x2c], xmm0
  0x00208b27  movss    xmm0, dword ptr [ebp + 0x1c]
  0x00208b2c  mov      dword ptr [ebp - 0x20], eax
  0x00208b2f  mov      eax, dword ptr [ebp + 0x18]
  0x00208b32  movss    dword ptr [ebp - 0x28], xmm0
  0x00208b37  mov      dword ptr [ebp - 0x1c], eax
  0x00208b3a  mov      eax, dword ptr [ecx]
  0x00208b3c  push     edx
  0x00208b3d  call     dword ptr [eax + 4]
  0x00208b40  mov      byte ptr [ebp - 0xd], 1
  0x00208b44  mov      ecx, dword ptr [ebx + 0x30]
  0x00208b47  mov      eax, 0x38e38e39
  0x00208b4c  sub      ecx, dword ptr [ebx + 0x2c]
  0x00208b4f  add      esi, 0x24
  0x00208b52  inc      dword ptr [ebp - 0x14]
  0x00208b55  imul     ecx
  0x00208b57  sar      edx, 3
  0x00208b5a  mov      eax, edx
  0x00208b5c  shr      eax, 0x1f
  0x00208b5f  add      eax, edx
  0x00208b61  cmp      dword ptr [ebp - 0x14], eax
  0x00208b64  jb       0x10208ad0
  0x00208b6a  mov      al, byte ptr [ebp - 0xd]
  0x00208b6d  test     al, al
  0x00208b6f  jne      0x10208c1c
  0x00208b75  mov      esi, dword ptr [ebp + 8]
  0x00208b78  push     dword ptr [ebx + 0x18]
  0x00208b7b  lea      ecx, [ebp - 0x74]
  0x00208b7e  push     esi
  0x00208b7f  call     0x1020d000   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2bc0
  0x00208b84  push     eax
  0x00208b85  lea      ecx, [ebx + 0x2c]
  0x00208b88  mov      dword ptr [ebp - 4], 0
  0x00208b8f  call     0x1020a760   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x320
  0x00208b94  lea      ecx, [ebp - 0x74]
  0x00208b97  mov      dword ptr [ebp - 4], 0xffffffff
  0x00208b9e  call     0x1020d0a0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2c60
  0x00208ba3  movss    xmm0, dword ptr [ebp + 0x10]
  0x00208ba8  push     ecx
  0x00208ba9  movss    dword ptr [esp], xmm0
  0x00208bae  mov      ecx, ebx
  0x00208bb0  push     esi
  0x00208bb1  call     0x10209db0   ; -> ?ModifyDuration@DurationDamageManager@GAME@@IAEMW4CombatAttributeType@2@M@Z
  0x00208bb6  mov      edx, dword ptr [ebp + 0x14]
  0x00208bb9  mov      eax, dword ptr [ebp + 0x18]
  0x00208bbc  movss    xmm0, dword ptr [ebp + 0xc]
  0x00208bc1  mov      dword ptr [ebp - 0x38], eax
  0x00208bc4  mov      eax, 0x38e38e39
  0x00208bc9  mov      ecx, dword ptr [edx]
  0x00208bcb  mov      dword ptr [ebp - 0x40], ecx
  0x00208bce  mov      ecx, dword ptr [edx + 4]
  0x00208bd1  mov      dword ptr [ebp - 0x3c], ecx
  0x00208bd4  mov      ecx, dword ptr [ebx + 0x30]
  0x00208bd7  sub      ecx, dword ptr [ebx + 0x2c]
  0x00208bda  imul     ecx
  0x00208bdc  movss    dword ptr [ebp - 0x50], xmm0
  0x00208be1  movss    dword ptr [ebp - 0x4c], xmm0
  0x00208be6  fstp     dword ptr [ebp + 8]
  0x00208be9  movss    xmm0, dword ptr [ebp + 8]
  0x00208bee  movss    dword ptr [ebp - 0x48], xmm0
  0x00208bf3  movss    xmm0, dword ptr [ebp + 0x1c]
  0x00208bf8  sar      edx, 3
  0x00208bfb  mov      eax, edx
  0x00208bfd  movss    dword ptr [ebp - 0x44], xmm0
  0x00208c02  shr      eax, 0x1f
  0x00208c05  add      eax, edx
  0x00208c07  lea      edx, [ebp - 0x50]
  0x00208c0a  push     edx
  0x00208c0b  lea      ecx, [eax + eax*8]
  0x00208c0e  mov      eax, dword ptr [ebx + 0x2c]
  0x00208c11  lea      ecx, [ecx - 9]
  0x00208c14  lea      ecx, [eax + ecx*4]
  0x00208c17  mov      eax, dword ptr [ecx]
  0x00208c19  call     dword ptr [eax + 4]
  0x00208c1c  pop      edi
  0x00208c1d  pop      esi
  0x00208c1e  mov      ecx, dword ptr [ebp - 0xc]
  0x00208c21  pop      ebx
  0x00208c22  mov      dword ptr fs:[0], ecx
  0x00208c29  mov      esp, ebp
  0x00208c2b  pop      ebp
  0x00208c2c  ret      0x18
  0x00208c2f  int3     
  0x00208c30  push     ebx
  0x00208c31  push     esi
  0x00208c32  mov      esi, ecx
  0x00208c34  mov      eax, 0x38e38e39
  0x00208c39  xor      ebx, ebx
  0x00208c3b  push     edi
  0x00208c3c  mov      edx, dword ptr [esi + 0x30]
  0x00208c3f  sub      edx, dword ptr [esi + 0x2c]
  0x00208c42  imul     edx
  0x00208c44  sar      edx, 3
  0x00208c47  mov      eax, edx
  0x00208c49  shr      eax, 0x1f
  0x00208c4c  add      eax, edx
  0x00208c4e  je       0x10208c7b
  0x00208c50  xor      edi, edi
  0x00208c52  mov      ecx, dword ptr [esi + 0x2c]
  0x00208c55  add      ecx, edi
  0x00208c57  call     0x1020d940   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x3500
  0x00208c5c  mov      ecx, dword ptr [esi + 0x30]
  0x00208c5f  mov      eax, 0x38e38e39
  0x00208c64  sub      ecx, dword ptr [esi + 0x2c]
  0x00208c67  inc      ebx
  0x00208c68  imul     ecx
  0x00208c6a  add      edi, 0x24
  0x00208c6d  sar      edx, 3
  0x00208c70  mov      eax, edx
  0x00208c72  shr      eax, 0x1f
  0x00208c75  add      eax, edx
  0x00208c77  cmp      ebx, eax
  0x00208c79  jb       0x10208c52
  0x00208c7b  mov      ecx, dword ptr [esi + 0x3c]
  0x00208c7e  mov      eax, 0x38e38e39
  0x00208c83  sub      ecx, dword ptr [esi + 0x38]
  0x00208c86  xor      ebx, ebx
  0x00208c88  imul     ecx
  0x00208c8a  sar      edx, 3
  0x00208c8d  mov      eax, edx
  0x00208c8f  shr      eax, 0x1f
  0x00208c92  add      eax, edx
  0x00208c94  je       0x10208cc9
  0x00208c96  xor      edi, edi
  0x00208c98  nop      dword ptr [eax + eax]
  0x00208ca0  mov      ecx, dword ptr [esi + 0x38]
  0x00208ca3  add      ecx, edi
  0x00208ca5  call     0x1020d940   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x3500
  0x00208caa  mov      ecx, dword ptr [esi + 0x3c]
  0x00208cad  mov      eax, 0x38e38e39
  0x00208cb2  sub      ecx, dword ptr [esi + 0x38]
  0x00208cb5  inc      ebx
  0x00208cb6  imul     ecx
  0x00208cb8  add      edi, 0x24
  0x00208cbb  sar      edx, 3
  0x00208cbe  mov      eax, edx
