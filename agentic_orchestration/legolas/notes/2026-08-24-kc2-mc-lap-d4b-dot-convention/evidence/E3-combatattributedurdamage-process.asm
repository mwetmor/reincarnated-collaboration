; CombatAttributeDurDamage::Process  (percent modifier only)
; Game.dll RVA 0x000d7dd0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x000d7dd0  push     ebp
  0x000d7dd1  mov      ebp, esp
  0x000d7dd3  sub      esp, 0xc
  0x000d7dd6  movss    xmm6, dword ptr [0x105f5af0]   ; f32=nan i32=2147483647 f64=nan
  0x000d7dde  movss    xmm2, dword ptr [0x105f5780]   ; f32=0.01 i32=1008981770 f64=5.37372e-17
  0x000d7de6  push     esi
  0x000d7de7  mov      esi, ecx
  0x000d7de9  cmp      byte ptr [esi + 0xc], 0
  0x000d7ded  movss    xmm3, dword ptr [esi + 0x2c]
  0x000d7df2  movss    xmm0, dword ptr [esi + 0x30]
  0x000d7df7  andps    xmm3, xmm6
  0x000d7dfa  movss    xmm1, dword ptr [esi + 0x1c]
  0x000d7dff  movss    xmm4, dword ptr [esi + 0x28]
  0x000d7e04  andps    xmm1, xmm6
  0x000d7e07  andps    xmm4, xmm6
  0x000d7e0a  mulss    xmm3, xmm0
  0x000d7e0e  mulss    xmm1, xmm0
  0x000d7e12  mulss    xmm4, xmm0
  0x000d7e16  mulss    xmm3, xmm2
  0x000d7e1a  mulss    xmm1, xmm2
  0x000d7e1e  mulss    xmm4, xmm2
  0x000d7e22  movss    dword ptr [ebp - 0xc], xmm3
  0x000d7e27  xorps    xmm3, xmm3
  0x000d7e2a  movss    dword ptr [ebp - 4], xmm1
  0x000d7e2f  movss    dword ptr [ebp - 8], xmm4
  0x000d7e34  je       0x100d7f4f
  0x000d7e3a  movss    xmm0, dword ptr [esi + 0x1c]
  0x000d7e3f  comiss   xmm0, xmm3
  0x000d7e42  push     edi
  0x000d7e43  mov      edi, dword ptr [ebp + 8]
  0x000d7e46  jbe      0x100d7e90
  0x000d7e48  mov      eax, dword ptr [esi + 4]
  0x000d7e4b  cmp      eax, 0xf
  0x000d7e4e  je       0x100d7e55
  0x000d7e50  cmp      eax, 2
  0x000d7e53  jne      0x100d7e90
  0x000d7e55  mov      ecx, dword ptr [edi + 0x544]
  0x000d7e5b  lea      edx, [edi + 0x3dc]
  0x000d7e61  movss    dword ptr [edx + 0x10c], xmm0
  0x000d7e69  test     ecx, ecx
  0x000d7e6b  je       0x100d7e8b
  0x000d7e6d  mov      ecx, dword ptr [ecx]
  0x000d7e6f  test     ecx, ecx
  0x000d7e71  je       0x100d7e88
  0x000d7e73  mov      eax, dword ptr [ecx]
  0x000d7e75  push     edx
  0x000d7e76  mov      eax, dword ptr [eax + 4]
  0x000d7e79  call     eax
  0x000d7e7b  fstp     dword ptr [ebp + 8]
  0x000d7e7e  movss    xmm0, dword ptr [ebp + 8]
  0x000d7e83  xorps    xmm3, xmm3
  0x000d7e86  jmp      0x100d7e8b   ; -> ?Process@CombatAttributeDurDamage@GAME@@UAEXABVCharacter@2@ABUReductionInfo@2@ABUDamageScaleInfo@2@M@Z+0xbb
  0x000d7e88  movaps   xmm0, xmm3
  0x000d7e8b  movss    dword ptr [esi + 0x1c], xmm0
  0x000d7e90  movss    xmm0, dword ptr [esi + 0x28]
  0x000d7e95  comiss   xmm0, xmm3
  0x000d7e98  jbe      0x100d7ee2
  0x000d7e9a  mov      eax, dword ptr [esi + 4]
  0x000d7e9d  cmp      eax, 0xf
  0x000d7ea0  je       0x100d7ea7
  0x000d7ea2  cmp      eax, 2
  0x000d7ea5  jne      0x100d7ee2
  0x000d7ea7  mov      ecx, dword ptr [edi + 0x544]
  0x000d7ead  lea      edx, [edi + 0x3dc]
  0x000d7eb3  movss    dword ptr [edx + 0x10c], xmm0
  0x000d7ebb  test     ecx, ecx
  0x000d7ebd  je       0x100d7edd
  0x000d7ebf  mov      ecx, dword ptr [ecx]
  0x000d7ec1  test     ecx, ecx
  0x000d7ec3  je       0x100d7eda
  0x000d7ec5  mov      eax, dword ptr [ecx]
  0x000d7ec7  push     edx
  0x000d7ec8  mov      eax, dword ptr [eax + 4]
  0x000d7ecb  call     eax
  0x000d7ecd  fstp     dword ptr [ebp + 8]
  0x000d7ed0  movss    xmm0, dword ptr [ebp + 8]
  0x000d7ed5  xorps    xmm3, xmm3
  0x000d7ed8  jmp      0x100d7edd   ; -> ?Process@CombatAttributeDurDamage@GAME@@UAEXABVCharacter@2@ABUReductionInfo@2@ABUDamageScaleInfo@2@M@Z+0x10d
  0x000d7eda  movaps   xmm0, xmm3
  0x000d7edd  movss    dword ptr [esi + 0x28], xmm0
  0x000d7ee2  movss    xmm0, dword ptr [esi + 0x2c]
  0x000d7ee7  comiss   xmm0, xmm3
  0x000d7eea  jbe      0x100d7f34
  0x000d7eec  mov      eax, dword ptr [esi + 4]
  0x000d7eef  cmp      eax, 0xf
  0x000d7ef2  je       0x100d7ef9
  0x000d7ef4  cmp      eax, 2
  0x000d7ef7  jne      0x100d7f34
  0x000d7ef9  mov      ecx, dword ptr [edi + 0x544]
  0x000d7eff  lea      edx, [edi + 0x3dc]
  0x000d7f05  movss    dword ptr [edx + 0x10c], xmm0
  0x000d7f0d  test     ecx, ecx
  0x000d7f0f  je       0x100d7f2f
  0x000d7f11  mov      ecx, dword ptr [ecx]
  0x000d7f13  test     ecx, ecx
  0x000d7f15  je       0x100d7f2c
  0x000d7f17  mov      eax, dword ptr [ecx]
  0x000d7f19  push     edx
  0x000d7f1a  mov      eax, dword ptr [eax + 4]
  0x000d7f1d  call     eax
  0x000d7f1f  fstp     dword ptr [ebp + 8]
  0x000d7f22  movss    xmm0, dword ptr [ebp + 8]
  0x000d7f27  xorps    xmm3, xmm3
  0x000d7f2a  jmp      0x100d7f2f   ; -> ?Process@CombatAttributeDurDamage@GAME@@UAEXABVCharacter@2@ABUReductionInfo@2@ABUDamageScaleInfo@2@M@Z+0x15f
  0x000d7f2c  movaps   xmm0, xmm3
  0x000d7f2f  movss    dword ptr [esi + 0x2c], xmm0
  0x000d7f34  movss    xmm2, dword ptr [0x105f5780]   ; f32=0.01 i32=1008981770 f64=5.37372e-17
  0x000d7f3c  movss    xmm1, dword ptr [ebp - 4]
  0x000d7f41  movss    xmm4, dword ptr [ebp - 8]
  0x000d7f46  movss    xmm6, dword ptr [0x105f5af0]   ; f32=nan i32=2147483647 f64=nan
  0x000d7f4e  pop      edi
  0x000d7f4f  movss    xmm5, dword ptr [esi + 0x2c]
  0x000d7f54  addss    xmm1, dword ptr [esi + 0x1c]
  0x000d7f59  addss    xmm4, dword ptr [esi + 0x28]
  0x000d7f5e  addss    xmm5, dword ptr [ebp - 0xc]
  0x000d7f63  mov      ecx, dword ptr [ebp + 0x10]
  0x000d7f66  movss    dword ptr [esi + 0x1c], xmm1
  0x000d7f6b  movss    dword ptr [esi + 0x28], xmm4
  0x000d7f70  movss    dword ptr [esi + 0x2c], xmm5
  0x000d7f75  movss    xmm0, dword ptr [ecx]
  0x000d7f79  ucomiss  xmm0, xmm3
  0x000d7f7c  lahf     
  0x000d7f7d  test     ah, 0x44
  0x000d7f80  jnp      0x100d7fb1
  0x000d7f82  mulss    xmm0, xmm2
  0x000d7f86  mulss    xmm0, xmm1
  0x000d7f8a  movss    dword ptr [esi + 0x1c], xmm0
  0x000d7f8f  movss    xmm0, dword ptr [ecx]
  0x000d7f93  mulss    xmm0, xmm2
  0x000d7f97  mulss    xmm0, xmm4
