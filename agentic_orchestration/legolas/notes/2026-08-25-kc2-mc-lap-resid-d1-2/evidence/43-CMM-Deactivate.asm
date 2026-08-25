=== 43-CMM-Deactivate  RVA 0x00078130  sym=?Deactivate@CharacterMovementManager@GAME@@QAEXXZ ===
  0x00078130  push     esi
  0x00078131  mov      esi, ecx
  0x00078133  cmp      byte ptr [esi + 0x41], 0
  0x00078137  jne      0x1007814d
  0x00078139  push     dword ptr [esi]
  0x0007813b  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x00078141  mov      ecx, eax
  0x00078143  call     dword ptr [0x104e57a8]   ; f32=1.16695e-38 i32=8327660 f64=2.76539e-306
  0x00078149  mov      byte ptr [esi + 0x40], 0
  0x0007814d  pop      esi
  0x0007814e  ret      
  0x0007814f  int3     
