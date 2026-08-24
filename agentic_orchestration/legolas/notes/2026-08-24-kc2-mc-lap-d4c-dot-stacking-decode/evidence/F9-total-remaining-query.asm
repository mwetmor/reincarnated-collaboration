; sum of inst+0x04 over ALL live buckets = total remaining DoT
; Game.dll RVA 0x0020dc40  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020dc40  push     ebp
  0x0020dc41  mov      ebp, esp
  0x0020dc43  push     ecx
  0x0020dc44  push     esi
  0x0020dc45  mov      esi, dword ptr [ecx + 0x14]
  0x0020dc48  xorps    xmm1, xmm1
  0x0020dc4b  movss    dword ptr [ebp - 4], xmm1
  0x0020dc50  mov      ecx, dword ptr [esi]
  0x0020dc52  cmp      ecx, esi
  0x0020dc54  je       0x1020dc77
  0x0020dc56  mov      eax, dword ptr [ecx + 8]
  0x0020dc59  mov      edx, dword ptr [ecx + 0xc]
  0x0020dc5c  cmp      eax, edx
  0x0020dc5e  je       0x1020dc71
  0x0020dc60  addss    xmm1, dword ptr [eax + 4]
  0x0020dc65  add      eax, 0x18
  0x0020dc68  cmp      eax, edx
  0x0020dc6a  jne      0x1020dc60
  0x0020dc6c  movss    dword ptr [ebp - 4], xmm1
  0x0020dc71  mov      ecx, dword ptr [ecx]
  0x0020dc73  cmp      ecx, esi
  0x0020dc75  jne      0x1020dc56
  0x0020dc77  fld      dword ptr [ebp - 4]
  0x0020dc7a  pop      esi
  0x0020dc7b  mov      esp, ebp
  0x0020dc7d  pop      ebp
  0x0020dc7e  ret      
  0x0020dc7f  int3     
  0x0020dc80  push     ebp
  0x0020dc81  mov      ebp, esp
  0x0020dc83  push     ecx
  0x0020dc84  mov      edx, ecx
  0x0020dc86  push     ebx
  0x0020dc87  push     esi
  0x0020dc88  mov      dword ptr [ebp - 4], edx
  0x0020dc8b  mov      eax, dword ptr [edx + 0x14]
  0x0020dc8e  mov      ebx, dword ptr [edx + 0x20]
  0x0020dc91  mov      esi, dword ptr [eax]
  0x0020dc93  cmp      esi, eax
  0x0020dc95  je       0x1020dd3c
