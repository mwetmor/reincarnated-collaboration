; CombatAttributeDurDamage::ctor  [+0x1c]=damage [+0x20]=[+0x24]=duration
; Game.dll RVA 0x000d7c80  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x000d7c80  push     ebp
  0x000d7c81  mov      ebp, esp
  0x000d7c83  mov      eax, dword ptr [ebp + 8]
  0x000d7c86  mov      edx, ecx
  0x000d7c88  movss    xmm0, dword ptr [ebp + 0xc]
  0x000d7c8d  mov      ecx, dword ptr [ebp + 0x14]
  0x000d7c90  mov      dword ptr [edx + 4], eax
  0x000d7c93  mov      byte ptr [edx + 0xc], 1
  0x000d7c97  mov      dword ptr [edx + 8], 0
  0x000d7c9e  mov      dword ptr [edx + 0x10], 0
  0x000d7ca5  mov      dword ptr [edx + 0x14], 0
  0x000d7cac  movss    dword ptr [edx + 0x1c], xmm0
  0x000d7cb1  movss    xmm0, dword ptr [ebp + 0x18]
  0x000d7cb6  movss    dword ptr [edx + 0x28], xmm0
  0x000d7cbb  movss    xmm0, dword ptr [ebp + 0x1c]
  0x000d7cc0  movss    dword ptr [edx + 0x2c], xmm0
  0x000d7cc5  movss    xmm0, dword ptr [ebp + 0x10]
  0x000d7cca  mov      dword ptr [edx + 0x18], 0
  0x000d7cd1  mov      dword ptr [edx], 0x105b9940
  0x000d7cd7  movss    dword ptr [edx + 0x20], xmm0
  0x000d7cdc  movss    dword ptr [edx + 0x24], xmm0
  0x000d7ce1  mov      eax, dword ptr [ecx]
  0x000d7ce3  mov      dword ptr [edx + 0x10], eax
  0x000d7ce6  mov      eax, dword ptr [ecx + 4]
  0x000d7ce9  mov      dword ptr [edx + 0x14], eax
  0x000d7cec  mov      al, byte ptr [ebp + 0x20]
  0x000d7cef  mov      byte ptr [edx + 0xc], al
  0x000d7cf2  mov      eax, edx
  0x000d7cf4  mov      dword ptr [edx + 0x30], 0
  0x000d7cfb  mov      dword ptr [edx + 0x34], 0
  0x000d7d02  mov      dword ptr [edx + 0x38], 0
  0x000d7d09  pop      ebp
  0x000d7d0a  ret      0x1c
  0x000d7d0d  int3     
  0x000d7d0e  int3     
