; GameEngine::LoadFromDatabase reads "damageMagnitude" into gGameEngine+0x292d4
; Game.dll RVA 0x002579e4  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x002579e4  push     eax
  0x002579e5  lea      ecx, [edi + 0x2926c]
  0x002579eb  call     0x10009d50   ; -> ?GetRTTIClassInfo@PetPlayerScaling@GAME@@UBEABVRTTI_ClassInfo@2@XZ+0x8c0
  0x002579f0  mov      edx, dword ptr [ebx]
  0x002579f2  lea      eax, [edi + 0x292d4]
  0x002579f8  push     eax
  0x002579f9  push     0x105529ec
  0x002579fe  mov      ecx, ebx
  0x00257a00  mov      eax, dword ptr [edx + 0x44]
  0x00257a03  call     eax
  0x00257a05  cmp      dword ptr [edi + 0xa74], 0
  0x00257a0c  jne      0x10257a63
  0x00257a0e  mov      eax, dword ptr [ebx]
  0x00257a10  mov      ecx, ebx
  0x00257a12  push     0x104f3d17
  0x00257a17  push     0x10552a20
  0x00257a1c  mov      eax, dword ptr [eax + 0x14]
  0x00257a1f  call     eax
  0x00257a21  push     eax
  0x00257a22  lea      ecx, [ebp - 0x8c8]
