=== 52-CBC-HandleAction  RVA 0x000ea480  sym=?HandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z ===
  0x000ea480  push     ebp
  0x000ea481  mov      ebp, esp
  0x000ea483  push     edi
  0x000ea484  mov      edi, ecx
  0x000ea486  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000ea48c  mov      ecx, dword ptr [ecx]
  0x000ea48e  call     dword ptr [0x104e5514]   ; f32=1.16567e-38 i32=8318480 f64=2.75291e-306
  0x000ea494  test     al, al
  0x000ea496  je       0x100ea4cd
  0x000ea498  push     esi
  0x000ea499  mov      esi, dword ptr [ebp + 8]
  0x000ea49c  mov      ecx, esi
  0x000ea49e  mov      eax, dword ptr [esi]
  0x000ea4a0  mov      eax, dword ptr [eax + 0x28]
  0x000ea4a3  call     eax
  0x000ea4a5  test     al, al
  0x000ea4a7  je       0x100ea4bf
  0x000ea4a9  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000ea4af  mov      ecx, dword ptr [ecx]
  0x000ea4b1  call     dword ptr [0x104e55f4]   ; f32=1.16608e-38 i32=8321456 f64=2.75697e-306
  0x000ea4b7  push     esi
  0x000ea4b8  mov      ecx, eax
  0x000ea4ba  mov      edx, dword ptr [eax]
  0x000ea4bc  call     dword ptr [edx + 4]
  0x000ea4bf  push     esi
  0x000ea4c0  mov      ecx, edi
  0x000ea4c2  call     0x100ea4e0   ; -> ?LocalHandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z
  0x000ea4c7  pop      esi
  0x000ea4c8  pop      edi
  0x000ea4c9  pop      ebp
  0x000ea4ca  ret      4
  0x000ea4cd  push     dword ptr [ebp + 8]
  0x000ea4d0  mov      ecx, edi
  0x000ea4d2  call     0x100ea4e0   ; -> ?LocalHandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z
  0x000ea4d7  pop      edi
  0x000ea4d8  pop      ebp
  0x000ea4d9  ret      4
  0x000ea4dc  int3     
  0x000ea4dd  int3     
  0x000ea4de  int3     
  0x000ea4df  int3     
