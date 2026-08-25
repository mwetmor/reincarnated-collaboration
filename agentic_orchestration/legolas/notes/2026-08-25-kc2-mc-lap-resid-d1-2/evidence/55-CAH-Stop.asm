=== 55-CAH-Stop  RVA 0x000725a0  sym=?Stop@CharacterActionHandler@GAME@@QAEXXZ ===
  0x000725a0  push     esi
  0x000725a1  mov      esi, ecx
  0x000725a3  mov      ecx, dword ptr [esi + 4]
  0x000725a6  test     ecx, ecx
  0x000725a8  je       0x100725c3
  0x000725aa  mov      eax, dword ptr [ecx]
  0x000725ac  call     dword ptr [eax + 0xc]
  0x000725af  mov      ecx, dword ptr [esi + 4]
  0x000725b2  test     ecx, ecx
  0x000725b4  je       0x100725bc
  0x000725b6  mov      eax, dword ptr [ecx]
  0x000725b8  push     1
  0x000725ba  call     dword ptr [eax]
  0x000725bc  mov      dword ptr [esi + 4], 0
  0x000725c3  pop      esi
  0x000725c4  ret      
  0x000725c5  int3     
  0x000725c6  int3     
  0x000725c7  int3     
  0x000725c8  int3     
  0x000725c9  int3     
  0x000725ca  int3     
  0x000725cb  int3     
  0x000725cc  int3     
  0x000725cd  int3     
  0x000725ce  int3     
  0x000725cf  int3     
