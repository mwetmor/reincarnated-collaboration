; per-entry retire: pop_front x ticksDue on the live list
; Game.dll RVA 0x0020dc80  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

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
  0x0020dc9b  push     edi
  0x0020dc9c  nop      dword ptr [eax]
  0x0020dca0  test     ebx, ebx
  0x0020dca2  jle      0x1020dd3b
  0x0020dca8  mov      eax, dword ptr [esi + 4]
  0x0020dcab  mov      edi, dword ptr [esi]
  0x0020dcad  mov      dword ptr [eax], edi
  0x0020dcaf  mov      ecx, dword ptr [esi]
  0x0020dcb1  mov      eax, dword ptr [esi + 4]
  0x0020dcb4  mov      dword ptr [ecx + 4], eax
  0x0020dcb7  dec      dword ptr [edx + 0x18]
  0x0020dcba  mov      ecx, dword ptr [esi + 8]
  0x0020dcbd  test     ecx, ecx
  0x0020dcbf  je       0x1020dd23
  0x0020dcc1  mov      edx, dword ptr [esi + 0x10]
  0x0020dcc4  mov      eax, 0x2aaaaaab
  0x0020dcc9  sub      edx, ecx
  0x0020dccb  imul     edx
  0x0020dccd  sar      edx, 2
  0x0020dcd0  mov      eax, edx
  0x0020dcd2  shr      eax, 0x1f
  0x0020dcd5  add      eax, edx
  0x0020dcd7  cmp      eax, 0xaaaaaaa
  0x0020dcdc  ja       0x1020dd42
  0x0020dcde  lea      eax, [eax + eax*2]
  0x0020dce1  shl      eax, 3
  0x0020dce4  cmp      eax, 0x1000
  0x0020dce9  jb       0x1020dd05
  0x0020dceb  test     cl, 0x1f
  0x0020dcee  jne      0x1020dd42
  0x0020dcf0  mov      eax, dword ptr [ecx - 4]
  0x0020dcf3  cmp      eax, ecx
  0x0020dcf5  jae      0x1020dd42
  0x0020dcf7  sub      ecx, eax
  0x0020dcf9  cmp      ecx, 4
  0x0020dcfc  jb       0x1020dd42
  0x0020dcfe  cmp      ecx, 0x23
  0x0020dd01  ja       0x1020dd42
  0x0020dd03  mov      ecx, eax
  0x0020dd05  push     ecx
  0x0020dd06  call     0x104be91b   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c6b
  0x0020dd0b  mov      dword ptr [esi + 8], 0
  0x0020dd12  add      esp, 4
