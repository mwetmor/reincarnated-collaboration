; DamageAttributeStore::AddDamageToAccumulator — the Global roll + XOR roulette
; Game.dll RVA 0x00156bf0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x00156bf0  push     ebp
  0x00156bf1  mov      ebp, esp
  0x00156bf3  sub      esp, 0xc
  0x00156bf6  push     ebx
  0x00156bf7  mov      ebx, ecx
  0x00156bf9  push     esi
  0x00156bfa  push     edi
  0x00156bfb  mov      dword ptr [ebp - 8], ebx
  0x00156bfe  mov      esi, dword ptr [ebx + 0x1c]
  0x00156c01  cmp      esi, dword ptr [ebx + 0x20]
  0x00156c04  je       0x10156c50
  0x00156c06  nop      word ptr [eax + eax]
  0x00156c10  mov      ecx, dword ptr [ebp + 0xc]
  0x00156c13  sub      esp, 8
  0x00156c16  movss    xmm0, dword ptr [ebp + 0x18]
  0x00156c1b  mov      edi, dword ptr [esi]
  0x00156c1d  mov      eax, dword ptr [ecx]
  0x00156c1f  movss    dword ptr [esp + 4], xmm0
  0x00156c25  movss    xmm0, dword ptr [ebp + 0x14]
  0x00156c2a  mov      ebx, dword ptr [edi]
  0x00156c2c  movss    dword ptr [esp], xmm0
  0x00156c31  push     0
  0x00156c33  call     dword ptr [eax + 4]
  0x00156c36  push     eax
  0x00156c37  push     dword ptr [ebp + 0x10]
  0x00156c3a  mov      ecx, edi
  0x00156c3c  push     dword ptr [ebp + 0xc]
  0x00156c3f  push     dword ptr [ebp + 8]
  0x00156c42  call     dword ptr [ebx + 0x28]
  0x00156c45  mov      ebx, dword ptr [ebp - 8]
  0x00156c48  add      esi, 4
  0x00156c4b  cmp      esi, dword ptr [ebx + 0x20]
  0x00156c4e  jne      0x10156c10
  0x00156c50  mov      edx, dword ptr [ebp + 0x10]
  0x00156c53  xorps    xmm1, xmm1
  0x00156c56  movaps   xmm0, xmm1
  0x00156c59  movss    dword ptr [ebp - 4], xmm0
  0x00156c5e  test     edx, edx
  0x00156c60  je       0x10156c8e
  0x00156c62  mov      eax, dword ptr [ebx + 0x30]
  0x00156c65  sub      eax, dword ptr [ebx + 0x2c]
  0x00156c68  sar      eax, 2
  0x00156c6b  test     eax, eax
  0x00156c6d  je       0x10156c8e
  0x00156c6f  mov      ecx, dword ptr [ebx + 0x30]
  0x00156c72  lea      eax, [edx - 1]
  0x00156c75  sub      ecx, dword ptr [ebx + 0x2c]
  0x00156c78  sar      ecx, 2
  0x00156c7b  dec      ecx
  0x00156c7c  cmp      eax, ecx
  0x00156c7e  cmovbe   ecx, eax
  0x00156c81  mov      eax, dword ptr [ebx + 0x2c]
  0x00156c84  movss    xmm0, dword ptr [eax + ecx*4]
  0x00156c89  movss    dword ptr [ebp - 4], xmm0
  0x00156c8e  cmp      edx, 1
  0x00156c91  jne      0x10156cc9
  0x00156c93  movss    xmm2, dword ptr [ebx + 0x38]
  0x00156c98  comiss   xmm2, xmm1
  0x00156c9b  jbe      0x10156ca5
  0x00156c9d  movaps   xmm0, xmm2
  0x00156ca0  movss    dword ptr [ebp - 4], xmm0
  0x00156ca5  movss    xmm2, dword ptr [ebx + 0x3c]
  0x00156caa  comiss   xmm2, xmm1
  0x00156cad  jbe      0x10156cb7
  0x00156caf  movaps   xmm0, xmm2
  0x00156cb2  movss    dword ptr [ebp - 4], xmm0
  0x00156cb7  movss    xmm2, dword ptr [ebx + 0x40]
  0x00156cbc  comiss   xmm2, xmm1
  0x00156cbf  jbe      0x10156cc9
  0x00156cc1  movaps   xmm0, xmm2
  0x00156cc4  movss    dword ptr [ebp - 4], xmm0
  0x00156cc9  comiss   xmm0, xmm1
  0x00156ccc  jbe      0x10156ea6
  0x00156cd2  mov      edi, dword ptr [ebp + 0xc]
  0x00156cd5  mov      ecx, edi
  0x00156cd7  mov      eax, dword ptr [edi]
  0x00156cd9  call     dword ptr [eax + 4]
  0x00156cdc  mov      esi, eax
  0x00156cde  movss    xmm1, dword ptr [ebp - 4]
  0x00156ce3  xor      edx, edx
  0x00156ce5  mov      ecx, 0x1f31d
  0x00156cea  mov      eax, dword ptr [esi]
  0x00156cec  div      ecx
  0x00156cee  imul     edx, edx, 0x41a7
  0x00156cf4  imul     ecx, eax, 0xb14
  0x00156cfa  sub      edx, ecx
  0x00156cfc  lea      eax, [edx + 0x7fffffff]
  0x00156d02  cmovs    edx, eax
  0x00156d05  mov      dword ptr [esi], edx
  0x00156d07  movd     xmm0, edx
  0x00156d0b  cvtdq2pd xmm0, xmm0
  0x00156d0f  shr      edx, 0x1f
  0x00156d12  addsd    xmm0, qword ptr [edx*8 + 0x105f5ae0]
  0x00156d1b  cvtpd2ps xmm0, xmm0
  0x00156d1f  mulss    xmm0, dword ptr [0x105f5718]   ; f32=4.65661e-10 i32=805306368 f64=4.52784e-72
  0x00156d27  mulss    xmm0, dword ptr [0x105f58e8]   ; f32=100 i32=1120403456 f64=1.54811e+15
  0x00156d2f  comiss   xmm1, xmm0
  0x00156d32  jb       0x10156ea6
  0x00156d38  mov      eax, dword ptr [edi]
  0x00156d3a  mov      ecx, edi
  0x00156d3c  mov      eax, dword ptr [eax + 0x10]
  0x00156d3f  call     eax
  0x00156d41  test     al, al
  0x00156d43  je       0x10156ea6
  0x00156d49  mov      eax, dword ptr [edi]
  0x00156d4b  movss    xmm0, dword ptr [ebp - 4]
  0x00156d50  push     ecx
  0x00156d51  mov      ecx, edi
  0x00156d53  movss    dword ptr [esp], xmm0
  0x00156d58  call     dword ptr [eax + 0x14]
  0x00156d5b  mov      esi, dword ptr [ebx + 0x10]
  0x00156d5e  cmp      esi, dword ptr [ebx + 0x14]
  0x00156d61  je       0x10156da6
  0x00156d63  mov      ecx, dword ptr [ebp + 0xc]
  0x00156d66  sub      esp, 8
  0x00156d69  movss    xmm0, dword ptr [ebp + 0x18]
  0x00156d6e  mov      edi, dword ptr [esi]
  0x00156d70  mov      eax, dword ptr [ecx]
  0x00156d72  movss    dword ptr [esp + 4], xmm0
  0x00156d78  movss    xmm0, dword ptr [ebp + 0x14]
  0x00156d7d  mov      ebx, dword ptr [edi]
  0x00156d7f  movss    dword ptr [esp], xmm0
  0x00156d84  push     1
  0x00156d86  call     dword ptr [eax + 4]
  0x00156d89  push     eax
  0x00156d8a  push     dword ptr [ebp + 0x10]
  0x00156d8d  mov      ecx, edi
  0x00156d8f  push     dword ptr [ebp + 0xc]
  0x00156d92  push     dword ptr [ebp + 8]
  0x00156d95  call     dword ptr [ebx + 0x28]
  0x00156d98  mov      ebx, dword ptr [ebp - 8]
  0x00156d9b  add      esi, 4
  0x00156d9e  cmp      esi, dword ptr [ebx + 0x14]
  0x00156da1  jne      0x10156d63
  0x00156da3  mov      edi, dword ptr [ebp + 0xc]
  0x00156da6  mov      eax, dword ptr [edi]
  0x00156da8  push     ecx
  0x00156da9  mov      ecx, edi
  0x00156dab  mov      dword ptr [esp], 0
  0x00156db2  call     dword ptr [eax + 0x14]
  0x00156db5  mov      eax, dword ptr [ebx + 8]
  0x00156db8  sub      eax, dword ptr [ebx + 4]
  0x00156dbb  sar      eax, 2
  0x00156dbe  test     eax, eax
  0x00156dc0  je       0x10156ea6
  0x00156dc6  mov      esi, dword ptr [ebx + 4]
  0x00156dc9  xorps    xmm0, xmm0
  0x00156dcc  movss    dword ptr [ebp - 8], xmm0
  0x00156dd1  movss    dword ptr [ebp - 4], xmm0
  0x00156dd6  cmp      esi, dword ptr [ebx + 8]
  0x00156dd9  je       0x10156e0c
  0x00156ddb  fld      dword ptr [ebp - 4]
  0x00156dde  mov      edi, dword ptr [ebp + 0x10]
  0x00156de1  fstp     dword ptr [ebp - 8]
  0x00156de4  mov      ecx, dword ptr [esi]
  0x00156de6  push     edi
  0x00156de7  mov      eax, dword ptr [ecx]
  0x00156de9  mov      eax, dword ptr [eax + 4]
  0x00156dec  call     eax
  0x00156dee  fadd     dword ptr [ebp - 8]
  0x00156df1  add      esi, 4
  0x00156df4  fst      dword ptr [ebp - 8]
  0x00156df7  fstp     dword ptr [ebp - 4]
  0x00156dfa  cmp      esi, dword ptr [ebx + 8]
  0x00156dfd  jne      0x10156de4
  0x00156dff  movss    xmm0, dword ptr [ebp - 4]
  0x00156e04  mov      edi, dword ptr [ebp + 0xc]
  0x00156e07  movss    dword ptr [ebp - 8], xmm0
  0x00156e0c  mov      eax, dword ptr [edi]
  0x00156e0e  mov      ecx, edi
  0x00156e10  call     dword ptr [eax + 4]
  0x00156e13  movss    xmm2, dword ptr [ebp - 8]
  0x00156e18  xorps    xmm1, xmm1
  0x00156e1b  mov      ecx, eax
  0x00156e1d  call     0x1048c100   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x4450
