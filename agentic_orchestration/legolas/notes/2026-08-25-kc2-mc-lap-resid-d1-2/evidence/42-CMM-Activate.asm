=== 42-CMM-Activate  RVA 0x00078100  sym=?Activate@CharacterMovementManager@GAME@@QAEXXZ ===
  0x00078100  cmp      byte ptr [ecx + 0x41], 0
  0x00078104  jne      0x1007812a
  0x00078106  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0007810b  mov      eax, dword ptr [eax]
  0x0007810d  cmp      byte ptr [eax + 0x192], 0
  0x00078114  jne      0x1007812a
  0x00078116  push     dword ptr [ecx]
  0x00078118  mov      byte ptr [ecx + 0x40], 1
  0x0007811c  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x00078122  mov      ecx, eax
  0x00078124  call     dword ptr [0x104e57a4]   ; f32=1.16695e-38 i32=8327610 f64=2.76532e-306
  0x0007812a  ret      
  0x0007812b  int3     
  0x0007812c  int3     
  0x0007812d  int3     
  0x0007812e  int3     
  0x0007812f  int3     
