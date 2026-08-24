; MSVC std::sort(first,last,ideal,pred) over 24-byte instances
; Game.dll RVA 0x0020ea70  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020ea70  push     ebp
  0x0020ea71  mov      ebp, esp
  0x0020ea73  and      esp, 0xfffffff8
  0x0020ea76  sub      esp, 0xc
  0x0020ea79  mov      eax, 0x2aaaaaab
  0x0020ea7e  push     ebx
  0x0020ea7f  push     esi
  0x0020ea80  push     edi
  0x0020ea81  mov      edi, edx
  0x0020ea83  mov      ebx, ecx
  0x0020ea85  mov      esi, edi
  0x0020ea87  sub      esi, ebx
  0x0020ea89  imul     esi
  0x0020ea8b  sar      edx, 2
  0x0020ea8e  mov      ecx, edx
  0x0020ea90  shr      ecx, 0x1f
  0x0020ea93  add      ecx, edx
  0x0020ea95  cmp      ecx, 0x20
  0x0020ea98  jle      0x1020eb48
  0x0020ea9e  mov      esi, dword ptr [ebp + 8]
  0x0020eaa1  test     esi, esi
  0x0020eaa3  jle      0x1020eb61
  0x0020eaa9  push     ecx
  0x0020eaaa  push     edi
  0x0020eaab  mov      edx, ebx
  0x0020eaad  lea      ecx, [esp + 0x18]
  0x0020eab1  call     0x1020eb90   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4750
  0x0020eab6  mov      eax, esi
  0x0020eab8  add      esp, 8
  0x0020eabb  cdq      
  0x0020eabc  sub      eax, edx
  0x0020eabe  mov      ecx, eax
  0x0020eac0  sar      ecx, 1
  0x0020eac2  mov      eax, ecx
  0x0020eac4  cdq      
  0x0020eac5  sub      eax, edx
  0x0020eac7  sar      eax, 1
  0x0020eac9  add      ecx, eax
  0x0020eacb  mov      eax, 0x2aaaaaab
  0x0020ead0  mov      dword ptr [ebp + 8], ecx
  0x0020ead3  mov      ecx, edi
  0x0020ead5  sub      ecx, dword ptr [esp + 0x14]
  0x0020ead9  imul     ecx
  0x0020eadb  mov      ecx, dword ptr [esp + 0x10]
  0x0020eadf  mov      eax, 0x2aaaaaab
  0x0020eae4  push     dword ptr [ebp + 0xc]
  0x0020eae7  sar      edx, 2
  0x0020eaea  sub      ecx, ebx
  0x0020eaec  mov      esi, edx
  0x0020eaee  shr      esi, 0x1f
  0x0020eaf1  add      esi, edx
  0x0020eaf3  imul     ecx
  0x0020eaf5  sar      edx, 2
  0x0020eaf8  mov      eax, edx
  0x0020eafa  shr      eax, 0x1f
  0x0020eafd  add      eax, edx
  0x0020eaff  cmp      eax, esi
  0x0020eb01  mov      esi, dword ptr [ebp + 8]
  0x0020eb04  push     esi
  0x0020eb05  jge      0x1020eb18
  0x0020eb07  mov      edx, dword ptr [esp + 0x18]
  0x0020eb0b  mov      ecx, ebx
  0x0020eb0d  call     0x1020ea70   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4630
  0x0020eb12  mov      ebx, dword ptr [esp + 0x1c]
  0x0020eb16  jmp      0x1020eb27   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x46e7
  0x0020eb18  mov      ecx, dword ptr [esp + 0x1c]
  0x0020eb1c  mov      edx, edi
  0x0020eb1e  call     0x1020ea70   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4630
  0x0020eb23  mov      edi, dword ptr [esp + 0x18]
  0x0020eb27  mov      ecx, edi
  0x0020eb29  mov      eax, 0x2aaaaaab
  0x0020eb2e  sub      ecx, ebx
  0x0020eb30  add      esp, 8
  0x0020eb33  imul     ecx
  0x0020eb35  sar      edx, 2
  0x0020eb38  mov      ecx, edx
  0x0020eb3a  shr      ecx, 0x1f
  0x0020eb3d  add      ecx, edx
  0x0020eb3f  cmp      ecx, 0x20
  0x0020eb42  jg       0x1020eaa1
  0x0020eb48  cmp      ecx, 2
  0x0020eb4b  jl       0x1020eb5a
  0x0020eb4d  push     ecx
  0x0020eb4e  mov      edx, edi
  0x0020eb50  mov      ecx, ebx
  0x0020eb52  call     0x1020ef70   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4b30
  0x0020eb57  add      esp, 4
  0x0020eb5a  pop      edi
  0x0020eb5b  pop      esi
  0x0020eb5c  pop      ebx
  0x0020eb5d  mov      esp, ebp
  0x0020eb5f  pop      ebp
  0x0020eb60  ret      
  0x0020eb61  cmp      ecx, 0x20
  0x0020eb64  jle      0x1020eb48
