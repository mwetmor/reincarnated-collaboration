=== 38-Character-MoveTo  RVA 0x0004a670  sym=?MoveTo@Character@GAME@@QAEXABVWorldVec3@2@MW4AnimationSet_Type@2@M@Z ===
  0x0004a670  push     ebp
  0x0004a671  mov      ebp, esp
  0x0004a673  sub      esp, 0x40
  0x0004a676  push     ebx
  0x0004a677  mov      ebx, dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004a67d  push     esi
  0x0004a67e  push     edi
  0x0004a67f  mov      edi, dword ptr [ebp + 8]
  0x0004a682  mov      esi, ecx
  0x0004a684  mov      ecx, edi
  0x0004a686  call     ebx
  0x0004a688  test     eax, eax
  0x0004a68a  je       0x1004a846
  0x0004a690  mov      eax, dword ptr [esi]
  0x0004a692  mov      ecx, esi
  0x0004a694  mov      eax, dword ptr [eax + 0x22c]
  0x0004a69a  call     eax
  0x0004a69c  test     al, al
  0x0004a69e  je       0x1004a846
  0x0004a6a4  mov      ecx, dword ptr [esi + 0x950]
  0x0004a6aa  lea      eax, [ebp - 0x40]
  0x0004a6ad  push     eax
  0x0004a6ae  mov      ecx, dword ptr [ecx]
  0x0004a6b0  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0004a6b6  push     eax
  0x0004a6b7  lea      eax, [ebp - 0xc]
  0x0004a6ba  mov      ecx, edi
  0x0004a6bc  push     eax
  0x0004a6bd  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x0004a6c3  movss    xmm0, dword ptr [ebp - 8]
  0x0004a6c8  movss    xmm1, dword ptr [ebp - 0xc]
  0x0004a6cd  mulss    xmm0, xmm0
  0x0004a6d1  mulss    xmm1, xmm1
  0x0004a6d5  addss    xmm1, xmm0
  0x0004a6d9  movss    xmm0, dword ptr [ebp - 4]
  0x0004a6de  mulss    xmm0, xmm0
  0x0004a6e2  addss    xmm1, xmm0
  0x0004a6e6  movss    xmm0, dword ptr [0x105f5758]   ; f32=0.000625 i32=975427339 f64=7.70312e-27
  0x0004a6ee  comiss   xmm0, xmm1
  0x0004a6f1  jb       0x1004a73e
  0x0004a6f3  mov      edi, dword ptr [esi + 0x950]
  0x0004a6f9  cmp      byte ptr [edi + 0x40], 0
  0x0004a6fd  je       0x1004a70f
  0x0004a6ff  push     dword ptr [edi]
  0x0004a701  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x0004a707  mov      ecx, eax
  0x0004a709  call     dword ptr [0x104e57a0]   ; f32=1.16694e-38 i32=8327560 f64=2.76525e-306
  0x0004a70f  mov      byte ptr [edi + 0x24], 0
  0x0004a713  push     dword ptr [esi + 0x1120]
  0x0004a719  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0004a71f  mov      ecx, eax
  0x0004a721  call     0x10062320   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x230
  0x0004a726  test     eax, eax
  0x0004a728  je       0x1004a866
  0x0004a72e  mov      edx, dword ptr [eax]
  0x0004a730  mov      ecx, eax
  0x0004a732  call     dword ptr [edx + 0x40]
  0x0004a735  pop      edi
  0x0004a736  pop      esi
  0x0004a737  pop      ebx
  0x0004a738  mov      esp, ebp
  0x0004a73a  pop      ebp
  0x0004a73b  ret      0x10
  0x0004a73e  mov      ecx, dword ptr [esi + 0x950]
  0x0004a744  push     edi
  0x0004a745  call     0x10077f40   ; -> ?MoveTo@CharacterMovementManager@GAME@@QAE_NABVWorldVec3@2@@Z
  0x0004a74a  test     al, al
  0x0004a74c  jne      0x1004a7b5
  0x0004a74e  mov      ecx, dword ptr [esi + 0x950]
  0x0004a754  add      ecx, 0x14
  0x0004a757  call     ebx
  0x0004a759  test     eax, eax
  0x0004a75b  je       0x1004a7a1
  0x0004a75d  mov      eax, dword ptr [esi + 0x950]
  0x0004a763  push     ecx
  0x0004a764  add      eax, 0x14
  0x0004a767  mov      dword ptr [esp], 0x3ccccccd
  0x0004a76e  push     eax
  0x0004a76f  mov      ecx, esi
  0x0004a771  call     0x10048b20   ; -> ?AlreadyThere@Character@GAME@@QBE_NABVWorldVec3@2@M@Z
  0x0004a776  test     al, al
  0x0004a778  je       0x1004a7a1
  0x0004a77a  mov      ecx, esi
  0x0004a77c  call     0x10047290   ; -> ?IsMoving@Character@GAME@@QBE_NXZ
  0x0004a781  test     al, al
  0x0004a783  je       0x1004a713
  0x0004a785  mov      ecx, dword ptr [esi + 0x1ba4]
  0x0004a78b  call     0x100725a0   ; -> ?Stop@CharacterActionHandler@GAME@@QAEXXZ
  0x0004a790  mov      eax, dword ptr [esi]
  0x0004a792  mov      ecx, esi
  0x0004a794  push     1
  0x0004a796  call     dword ptr [eax + 0x224]
  0x0004a79c  jmp      0x1004a713   ; -> ?MoveTo@Character@GAME@@QAEXABVWorldVec3@2@MW4AnimationSet_Type@2@M@Z+0xa3
  0x0004a7a1  push     1
  0x0004a7a3  push     1
  0x0004a7a5  mov      ecx, esi
  0x0004a7a7  call     0x1004a9f0   ; -> ?StopMoving@Character@GAME@@QAEX_N0@Z
  0x0004a7ac  pop      edi
  0x0004a7ad  pop      esi
  0x0004a7ae  pop      ebx
  0x0004a7af  mov      esp, ebp
  0x0004a7b1  pop      ebp
  0x0004a7b2  ret      0x10
  0x0004a7b5  mov      ecx, esi
  0x0004a7b7  call     0x10046780   ; -> ?GetAnimationSet@Character@GAME@@QBEPAVAnimationSet@2@XZ
  0x0004a7bc  push     0
  0x0004a7be  mov      ecx, esi
  0x0004a7c0  mov      ebx, dword ptr [eax + 4]
  0x0004a7c3  call     dword ptr [0x104e55f0]   ; f32=1.16608e-38 i32=8321404 f64=2.7569e-306
  0x0004a7c9  mov      eax, dword ptr [esi]
  0x0004a7cb  mov      ecx, esi
  0x0004a7cd  fstp     dword ptr [ebp + 8]
  0x0004a7d0  call     dword ptr [eax + 0x228]
  0x0004a7d6  mov      edi, dword ptr [ebp + 0x10]
  0x0004a7d9  cmp      eax, 5
  0x0004a7dc  jne      0x1004a7f1
  0x0004a7de  cmp      ebx, edi
  0x0004a7e0  jne      0x1004a7f1
  0x0004a7e2  movss    xmm0, dword ptr [ebp + 8]
  0x0004a7e7  ucomiss  xmm0, dword ptr [ebp + 0x14]
  0x0004a7eb  lahf     
  0x0004a7ec  test     ah, 0x44
  0x0004a7ef  jnp      0x1004a866
  0x0004a7f1  mov      eax, dword ptr [esi]
  0x0004a7f3  mov      ecx, esi
  0x0004a7f5  push     5
  0x0004a7f7  call     dword ptr [eax + 0x224]
  0x0004a7fd  movss    xmm0, dword ptr [ebp + 0x14]
  0x0004a802  push     0
  0x0004a804  push     1
  0x0004a806  push     ecx
  0x0004a807  movss    dword ptr [esp], xmm0
  0x0004a80c  mov      ecx, esi
  0x0004a80e  push     dword ptr [0x104e52b0]   ; f32=1.16458e-38 i32=8310708 f64=2.74234e-306
  0x0004a814  push     edi
  0x0004a815  push     esi
  0x0004a816  call     0x10046780   ; -> ?GetAnimationSet@Character@GAME@@QBEPAVAnimationSet@2@XZ
  0x0004a81b  mov      ecx, eax
  0x0004a81d  call     0x10015b50   ; -> ?PlayAnimation@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z
  0x0004a822  test     al, al
  0x0004a824  jne      0x1004a866
  0x0004a826  mov      ecx, dword ptr [esi + 0x950]
  0x0004a82c  call     0x100780e0   ; -> ?Stop@CharacterMovementManager@GAME@@QAEXXZ
  0x0004a831  mov      eax, dword ptr [esi]
  0x0004a833  mov      ecx, esi
  0x0004a835  push     1
  0x0004a837  call     dword ptr [eax + 0x224]
  0x0004a83d  pop      edi
  0x0004a83e  pop      esi
  0x0004a83f  pop      ebx
  0x0004a840  mov      esp, ebp
  0x0004a842  pop      ebp
  0x0004a843  ret      0x10
  0x0004a846  mov      esi, dword ptr [esi + 0x950]
  0x0004a84c  cmp      byte ptr [esi + 0x40], 0
  0x0004a850  je       0x1004a862
  0x0004a852  push     dword ptr [esi]
  0x0004a854  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x0004a85a  mov      ecx, eax
  0x0004a85c  call     dword ptr [0x104e57a0]   ; f32=1.16694e-38 i32=8327560 f64=2.76525e-306
  0x0004a862  mov      byte ptr [esi + 0x24], 0
  0x0004a866  pop      edi
  0x0004a867  pop      esi
  0x0004a868  pop      ebx
  0x0004a869  mov      esp, ebp
  0x0004a86b  pop      ebp
  0x0004a86c  ret      0x10
  0x0004a86f  int3     
