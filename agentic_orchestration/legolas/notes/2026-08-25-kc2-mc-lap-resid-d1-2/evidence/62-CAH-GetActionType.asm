=== 62-CAH-GetActionType  RVA 0x00072610  sym=?GetActionType@CharacterActionHandler@GAME@@QAE?AW4CharacterActionType@2@XZ ===
  0x00072610  mov      ecx, dword ptr [ecx + 4]
  0x00072613  test     ecx, ecx
  0x00072615  je       0x1007261c
  0x00072617  mov      eax, dword ptr [ecx]
  0x00072619  jmp      dword ptr [eax + 0x2c]
  0x0007261c  xor      eax, eax
  0x0007261e  ret      
  0x0007261f  int3     
