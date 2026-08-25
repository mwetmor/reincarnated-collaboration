=== 35-CMM-Stop  RVA 0x000780e0  sym=?Stop@CharacterMovementManager@GAME@@QAEXXZ ===
  0x000780e0  push     esi
  0x000780e1  mov      esi, ecx
  0x000780e3  cmp      byte ptr [esi + 0x40], 0
  0x000780e7  je       0x100780f9
  0x000780e9  push     dword ptr [esi]
  0x000780eb  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x000780f1  mov      ecx, eax
  0x000780f3  call     dword ptr [0x104e57a0]   ; f32=1.16694e-38 i32=8327560 f64=2.76525e-306
  0x000780f9  mov      byte ptr [esi + 0x24], 0
  0x000780fd  pop      esi
  0x000780fe  ret      
  0x000780ff  int3     
