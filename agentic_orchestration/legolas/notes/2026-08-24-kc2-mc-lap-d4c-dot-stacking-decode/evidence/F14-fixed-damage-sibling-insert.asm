; CombatAttributeDurFixedDamage insert: same buckets, flat maxss, NO source key / NO sort
; Game.dll RVA 0x0020e060  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020e060  push     ebp
  0x0020e061  mov      ebp, esp
  0x0020e063  mov      eax, dword ptr fs:[0]
  0x0020e069  push     -1
  0x0020e06b  push     0x104cb838
  0x0020e070  push     eax
  0x0020e071  mov      dword ptr fs:[0], esp
  0x0020e078  sub      esp, 0x1c
  0x0020e07b  cmp      dword ptr [ecx + 0x10], 0
  0x0020e07f  push     ebx
  0x0020e080  push     esi
  0x0020e081  mov      esi, dword ptr [ebp + 8]
  0x0020e084  lea      ebx, [ecx + 0xc]
  0x0020e087  push     edi
  0x0020e088  movss    xmm0, dword ptr [esi + 8]
  0x0020e08d  mulss    xmm0, dword ptr [0x105f58a4]   ; f32=10 i32=1092616192 f64=2.09715e+06
  0x0020e095  cvttss2si edi, xmm0
  0x0020e099  jne      0x1020e0ae
  0x0020e09b  lea      eax, [ecx + 0x14]
  0x0020e09e  cmp      ebx, eax
  0x0020e0a0  je       0x1020e0ae
  0x0020e0a2  mov      eax, dword ptr [eax]
  0x0020e0a4  mov      ecx, ebx
  0x0020e0a6  push     eax
  0x0020e0a7  push     dword ptr [eax]
  0x0020e0a9  call     0x1020c6c0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2280
  0x0020e0ae  cmp      dword ptr [ebx + 4], edi
  0x0020e0b1  jae      0x1020e10b
  0x0020e0b3  mov      dword ptr [ebp - 0x1c], 0
  0x0020e0ba  mov      dword ptr [ebp - 0x18], 0
  0x0020e0c1  mov      dword ptr [ebp - 0x14], 0
  0x0020e0c8  lea      eax, [ebp - 0x1c]
  0x0020e0cb  mov      dword ptr [ebp - 4], 0
  0x0020e0d2  push     eax
  0x0020e0d3  push     edi
  0x0020e0d4  mov      ecx, ebx
  0x0020e0d6  call     0x1020e4b0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4070
  0x0020e0db  mov      dword ptr [ebp - 4], 0xffffffff
  0x0020e0e2  mov      ecx, dword ptr [ebp - 0x1c]
  0x0020e0e5  test     ecx, ecx
  0x0020e0e7  je       0x1020e10b
  0x0020e0e9  mov      edx, dword ptr [ebp - 0x14]
  0x0020e0ec  mov      eax, 0x2aaaaaab
  0x0020e0f1  sub      edx, ecx
  0x0020e0f3  imul     edx
  0x0020e0f5  push     0x18
  0x0020e0f7  mov      eax, edx
  0x0020e0f9  sar      eax, 2
  0x0020e0fc  mov      edx, eax
  0x0020e0fe  shr      edx, 0x1f
  0x0020e101  add      edx, eax
  0x0020e103  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x0020e108  add      esp, 4
  0x0020e10b  mov      eax, dword ptr [ebx]
  0x0020e10d  movss    xmm1, dword ptr [esi]
  0x0020e111  movss    dword ptr [ebp - 0x10], xmm1
  0x0020e116  mov      esi, dword ptr [eax]
  0x0020e118  cmp      esi, eax
  0x0020e11a  je       0x1020e188
  0x0020e11c  nop      dword ptr [eax]
  0x0020e120  test     edi, edi
  0x0020e122  jle      0x1020e188
  0x0020e124  mov      eax, dword ptr [esi + 8]
  0x0020e127  mov      ecx, dword ptr [esi + 0xc]
  0x0020e12a  cmp      eax, ecx
  0x0020e12c  je       0x1020e145
  0x0020e12e  nop      
  0x0020e130  movss    xmm0, dword ptr [eax + 4]
  0x0020e135  maxss    xmm0, xmm1
  0x0020e139  movss    dword ptr [eax + 4], xmm0
