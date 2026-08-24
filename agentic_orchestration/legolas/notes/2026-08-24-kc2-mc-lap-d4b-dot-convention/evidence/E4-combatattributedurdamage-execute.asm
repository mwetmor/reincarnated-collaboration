; CombatAttributeDurDamage::Execute -> DurationDamageManager::AddDamage
; Game.dll RVA 0x000d80c0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x000d80c0  push     ebp
  0x000d80c1  mov      ebp, esp
  0x000d80c3  push     esi
  0x000d80c4  mov      esi, ecx
  0x000d80c6  mov      ecx, dword ptr [ebp + 8]
  0x000d80c9  add      ecx, 0x3e4
  0x000d80cf  push     ecx
  0x000d80d0  movss    xmm0, dword ptr [esi + 0x38]
  0x000d80d5  lea      eax, [esi + 0x10]
  0x000d80d8  mov      edx, dword ptr [ecx]
  0x000d80da  movss    dword ptr [esp], xmm0
  0x000d80df  push     dword ptr [esi + 0x18]
  0x000d80e2  movss    xmm0, dword ptr [esi + 0x20]
  0x000d80e7  push     eax
  0x000d80e8  sub      esp, 8
  0x000d80eb  movss    dword ptr [esp + 4], xmm0
  0x000d80f1  movss    xmm0, dword ptr [esi + 0x1c]
  0x000d80f6  movss    dword ptr [esp], xmm0
  0x000d80fb  push     dword ptr [esi + 4]
  0x000d80fe  call     dword ptr [edx + 0x10]
  0x000d8101  pop      esi
  0x000d8102  pop      ebp
  0x000d8103  ret      4
  0x000d8106  int3     
  0x000d8107  int3     
