; DurationDamageManager::EndAttack per-entry: live = scratch, then scratch.clear()
; Game.dll RVA 0x0020d940  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020d940  push     ebp
  0x0020d941  mov      ebp, esp
  0x0020d943  mov      eax, dword ptr fs:[0]
  0x0020d949  push     -1
  0x0020d94b  push     0x104cb838
  0x0020d950  push     eax
  0x0020d951  mov      dword ptr fs:[0], esp
  0x0020d958  sub      esp, 0x10
  0x0020d95b  push     ebx
  0x0020d95c  push     esi
  0x0020d95d  mov      esi, ecx
  0x0020d95f  mov      eax, dword ptr [esi + 0x18]
  0x0020d962  lea      ebx, [esi + 0x14]
  0x0020d965  test     eax, eax
  0x0020d967  jne      0x1020d984
  0x0020d969  lea      ecx, [esi + 0xc]
  0x0020d96c  mov      dword ptr [ebp - 0x10], ecx
  0x0020d96f  cmp      ebx, ecx
  0x0020d971  je       0x1020d9f2
  0x0020d973  mov      eax, dword ptr [ecx]
  0x0020d975  mov      ecx, ebx
  0x0020d977  push     eax
  0x0020d978  push     dword ptr [eax]
  0x0020d97a  call     0x1020c6c0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2280
  0x0020d97f  mov      ecx, dword ptr [ebp - 0x10]
  0x0020d982  jmp      0x1020d9f2   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x35b2
  0x0020d984  mov      ecx, dword ptr [esi + 0x10]
  0x0020d987  cmp      eax, ecx
  0x0020d989  jae      0x1020d9c2
  0x0020d98b  mov      dword ptr [ebp - 0x1c], 0
  0x0020d992  mov      dword ptr [ebp - 0x18], 0
  0x0020d999  mov      dword ptr [ebp - 0x14], 0
  0x0020d9a0  lea      eax, [ebp - 0x1c]
  0x0020d9a3  mov      dword ptr [ebp - 4], 0
  0x0020d9aa  push     eax
  0x0020d9ab  push     ecx
  0x0020d9ac  mov      ecx, ebx
  0x0020d9ae  call     0x1020e4b0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4070
  0x0020d9b3  lea      ecx, [ebp - 0x1c]
  0x0020d9b6  mov      dword ptr [ebp - 4], 0xffffffff
  0x0020d9bd  call     0x1020c520   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x20e0
  0x0020d9c2  mov      eax, dword ptr [esi + 0xc]
  0x0020d9c5  lea      ecx, [esi + 0xc]
  0x0020d9c8  mov      esi, dword ptr [ebx]
  0x0020d9ca  push     edi
  0x0020d9cb  mov      dword ptr [ebp - 0x10], ecx
  0x0020d9ce  mov      edi, dword ptr [eax]
  0x0020d9d0  mov      esi, dword ptr [esi]
  0x0020d9d2  cmp      edi, eax
  0x0020d9d4  je       0x1020d9f1
  0x0020d9d6  cmp      esi, dword ptr [ebx]
  0x0020d9d8  je       0x1020d9f1
  0x0020d9da  lea      eax, [edi + 8]
  0x0020d9dd  push     eax
  0x0020d9de  lea      ecx, [esi + 8]
  0x0020d9e1  call     0x1020e2e0   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x3ea0
  0x0020d9e6  mov      ecx, dword ptr [ebp - 0x10]
  0x0020d9e9  mov      edi, dword ptr [edi]
  0x0020d9eb  mov      esi, dword ptr [esi]
  0x0020d9ed  cmp      edi, dword ptr [ecx]
  0x0020d9ef  jne      0x1020d9d6
  0x0020d9f1  pop      edi
  0x0020d9f2  call     0x1020c470   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2030
  0x0020d9f7  mov      ecx, dword ptr [ebp - 0xc]
  0x0020d9fa  pop      esi
  0x0020d9fb  pop      ebx
  0x0020d9fc  mov      dword ptr fs:[0], ecx
  0x0020da03  mov      esp, ebp
  0x0020da05  pop      ebp
  0x0020da06  ret      
  0x0020da07  int3     
  0x0020da08  int3     
  0x0020da09  int3     
  0x0020da0a  int3     
  0x0020da0b  int3     
