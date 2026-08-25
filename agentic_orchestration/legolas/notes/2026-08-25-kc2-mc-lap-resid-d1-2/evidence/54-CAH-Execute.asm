=== 54-CAH-Execute  RVA 0x000724f0  sym=?Execute@CharacterActionHandler@GAME@@QAEXPAVCharacterAction@2@AAH@Z ===
  0x000724f0  push     ebp
  0x000724f1  mov      ebp, esp
  0x000724f3  push     esi
  0x000724f4  push     edi
  0x000724f5  mov      edi, dword ptr [ebp + 8]
  0x000724f8  mov      esi, ecx
  0x000724fa  test     edi, edi
  0x000724fc  je       0x10072592
  0x00072502  push     ebx
  0x00072503  mov      ebx, dword ptr [ebp + 0xc]
  0x00072506  mov      eax, dword ptr [ebx]
  0x00072508  test     eax, eax
  0x0007250a  jle      0x10072589
  0x0007250c  dec      eax
  0x0007250d  mov      dword ptr [ebx], eax
  0x0007250f  cmp      byte ptr [esi + 0xc], 0
  0x00072513  jne      0x10072576
  0x00072515  cmp      dword ptr [esi + 4], 0
  0x00072519  mov      byte ptr [esi + 0xc], 1
  0x0007251d  je       0x10072526
  0x0007251f  mov      ecx, esi
  0x00072521  call     0x100725a0   ; -> ?Stop@CharacterActionHandler@GAME@@QAEXXZ
  0x00072526  mov      dword ptr [esi + 4], edi
  0x00072529  mov      ecx, edi
  0x0007252b  mov      eax, dword ptr [edi]
  0x0007252d  call     dword ptr [eax + 4]
  0x00072530  mov      byte ptr [esi + 0xc], 0
  0x00072534  cmp      dword ptr [esi + 0x14], 0
  0x00072538  je       0x10072591
  0x0007253a  mov      eax, dword ptr [esi + 0x10]
  0x0007253d  push     0xc
  0x0007253f  mov      eax, dword ptr [eax]
  0x00072541  mov      edi, dword ptr [eax + 8]
  0x00072544  mov      eax, dword ptr [esi + 0x10]
  0x00072547  mov      ecx, dword ptr [eax]
  0x00072549  mov      edx, dword ptr [ecx + 4]
  0x0007254c  mov      eax, dword ptr [ecx]
  0x0007254e  mov      dword ptr [edx], eax
  0x00072550  mov      edx, dword ptr [ecx]
  0x00072552  mov      eax, dword ptr [ecx + 4]
  0x00072555  mov      dword ptr [edx + 4], eax
  0x00072558  mov      edx, 1
  0x0007255d  dec      dword ptr [esi + 0x14]
  0x00072560  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x00072565  add      esp, 4
  0x00072568  mov      dword ptr [ebp + 8], edi
  0x0007256b  test     edi, edi
  0x0007256d  jne      0x10072506
  0x0007256f  pop      ebx
  0x00072570  pop      edi
  0x00072571  pop      esi
  0x00072572  pop      ebp
  0x00072573  ret      8
  0x00072576  lea      eax, [ebp + 8]
  0x00072579  push     eax
  0x0007257a  lea      ecx, [esi + 0x10]
  0x0007257d  call     0x100727a0   ; -> ?QueryActionPermission@CharacterActionHandler@GAME@@QBE?AW4CharacterActionPermission@2@PAVCharacterAction@2@0@Z+0x20
  0x00072582  pop      ebx
  0x00072583  pop      edi
  0x00072584  pop      esi
  0x00072585  pop      ebp
  0x00072586  ret      8
  0x00072589  lea      ecx, [esi + 0x10]
  0x0007258c  call     0x1005ed30   ; -> ?SelectPrimaryAction@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MAE_N_N_N1ABVWorldVec3@2@AAI1@Z+0xc90
  0x00072591  pop      ebx
  0x00072592  pop      edi
  0x00072593  pop      esi
  0x00072594  pop      ebp
  0x00072595  ret      8
  0x00072598  int3     
  0x00072599  int3     
  0x0007259a  int3     
  0x0007259b  int3     
  0x0007259c  int3     
  0x0007259d  int3     
  0x0007259e  int3     
  0x0007259f  int3     
