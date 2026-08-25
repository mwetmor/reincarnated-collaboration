=== 93-Character-CrowdAgentMoved RVA 0x00052960 sym=?CrowdAgentMoved@Character@GAME@@UAEXHABUCrowdAgentData@CROWD@@@Z ===
  0x00052960  push     ebp
  0x00052961  mov      ebp, esp
  0x00052963  and      esp, 0xfffffff8
  0x00052966  sub      esp, 0x48
  0x00052969  cmp      dword ptr [ebp + 8], 0
  0x0005296d  push     esi
  0x0005296e  push     edi
  0x0005296f  mov      edi, ecx
  0x00052971  mov      dword ptr [esp + 8], edi
  0x00052975  je       0x100529a3
  0x00052977  lea      ecx, [edi - 0x28]
  0x0005297a  call     dword ptr [0x104e56cc]   ; f32=1.16653e-38 i32=8324668 f64=2.76132e-306
  0x00052980  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x00052986  mov      esi, eax
  0x00052988  mov      ecx, dword ptr [ecx]
  0x0005298a  call     dword ptr [0x104e56d0]   ; f32=1.16654e-38 i32=8324712 f64=2.76137e-306
  0x00052990  dec      eax
  0x00052991  cmp      esi, eax
  0x00052993  jae      0x100529a3
  0x00052995  call     dword ptr [0x104e56d4]   ; f32=1.16655e-38 i32=8324750 f64=2.76142e-306
  0x0005299b  test     al, al
  0x0005299d  je       0x10052bb0
  0x000529a3  lea      ecx, [esp + 0x40]
  0x000529a7  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000529ad  add      edi, -0x28
  0x000529b0  mov      ecx, edi
  0x000529b2  call     dword ptr [0x104e5294]   ; f32=1.1645e-38 i32=8310154 f64=2.74161e-306
  0x000529b8  mov      esi, dword ptr [ebp + 0xc]
  0x000529bb  lea      ecx, [esp + 0x40]
  0x000529bf  push     eax
  0x000529c0  push     esi
  0x000529c1  call     dword ptr [0x104e56d8]   ; f32=1.16655e-38 i32=8324784 f64=2.76151e-306
  0x000529c7  test     al, al
  0x000529c9  je       0x10052bb0
  0x000529cf  lea      ecx, [esp + 0x40]
  0x000529d3  call     dword ptr [0x104e55d0]   ; f32=1.16601e-38 i32=8320960 f64=2.75627e-306
  0x000529d9  test     al, al
  0x000529db  je       0x10052bb0
  0x000529e1  mov      eax, dword ptr [esi + 0x20]
  0x000529e4  mov      ecx, edi
  0x000529e6  movq     xmm0, qword ptr [esi + 0x18]
  0x000529eb  mov      dword ptr [esp + 0x24], eax
  0x000529ef  mov      eax, dword ptr [edi]
  0x000529f1  movq     qword ptr [esp + 0x1c], xmm0
  0x000529f7  mov      eax, dword ptr [eax + 0x228]
  0x000529fd  call     eax
  0x000529ff  cmp      eax, 0x13
  0x00052a02  je       0x10052a19
  0x00052a04  mov      eax, dword ptr [edi]
  0x00052a06  mov      ecx, edi
  0x00052a08  mov      eax, dword ptr [eax + 0x228]
  0x00052a0e  call     eax
  0x00052a10  cmp      eax, 0x15
  0x00052a13  jne      0x10052b8d
  0x00052a19  mov      eax, dword ptr [esp + 8]
  0x00052a1d  lea      ecx, [eax + 0x938]
  0x00052a23  add      eax, 0x948
  0x00052a28  push     ecx
  0x00052a29  mov      dword ptr [esp + 0x18], ecx
  0x00052a2d  lea      ecx, [esp + 0x2c]
  0x00052a31  push     ecx
  0x00052a32  mov      ecx, eax
  0x00052a34  mov      dword ptr [esp + 0x14], eax
  0x00052a38  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x00052a3e  movss    xmm0, dword ptr [eax + 8]
  0x00052a43  movss    xmm1, dword ptr [eax]
  0x00052a47  mulss    xmm0, xmm0
  0x00052a4b  mulss    xmm1, xmm1
  0x00052a4f  addss    xmm1, xmm0
  0x00052a53  xorps    xmm0, xmm0
  0x00052a56  ucomiss  xmm1, xmm0
  0x00052a59  lahf     
  0x00052a5a  test     ah, 0x44
  0x00052a5d  jnp      0x10052a66
  0x00052a5f  xorps    xmm0, xmm0
  0x00052a62  sqrtss   xmm0, xmm1
  0x00052a66  mov      ecx, dword ptr [esp + 0xc]
  0x00052a6a  lea      eax, [esp + 0x40]
  0x00052a6e  push     eax
  0x00052a6f  lea      eax, [esp + 0x2c]
  0x00052a73  movss    dword ptr [esp + 0x14], xmm0
  0x00052a79  push     eax
  0x00052a7a  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x00052a80  movss    xmm0, dword ptr [eax + 8]
  0x00052a85  movss    xmm1, dword ptr [eax]
  0x00052a89  mulss    xmm0, xmm0
  0x00052a8d  mulss    xmm1, xmm1
  0x00052a91  addss    xmm1, xmm0
  0x00052a95  xorps    xmm0, xmm0
  0x00052a98  ucomiss  xmm1, xmm0
  0x00052a9b  lahf     
  0x00052a9c  test     ah, 0x44
  0x00052a9f  jnp      0x10052b49
  0x00052aa5  xorps    xmm0, xmm0
  0x00052aa8  sqrtss   xmm0, xmm1
  0x00052aac  comiss   xmm0, dword ptr [0x105f5870]   ; f32=3 i32=1077936128 f64=50.1239
  0x00052ab3  movss    dword ptr [esp + 0x18], xmm0
  0x00052ab9  jbe      0x10052b49
  0x00052abf  mov      ecx, dword ptr [esp + 0x14]
  0x00052ac3  lea      eax, [esp + 0x28]
  0x00052ac7  mov      esi, dword ptr [0x104e56c4]   ; f32=1.16652e-38 i32=8324584 f64=2.76122e-306
  0x00052acd  push     eax
  0x00052ace  call     esi
  0x00052ad0  mov      ecx, dword ptr [esp + 0xc]
  0x00052ad4  movss    xmm0, dword ptr [eax + 4]
  0x00052ad9  lea      eax, [esp + 0x34]
  0x00052add  push     eax
  0x00052ade  movss    dword ptr [esp + 0x18], xmm0
  0x00052ae4  call     esi
  0x00052ae6  movss    xmm2, dword ptr [esp + 0x18]
  0x00052aec  mov      ecx, edi
  0x00052aee  divss    xmm2, dword ptr [esp + 0x10]
  0x00052af4  mov      esi, dword ptr [ebp + 0xc]
  0x00052af7  movss    xmm1, dword ptr [eax + 4]
  0x00052afc  movss    xmm0, dword ptr [esi]
  0x00052b00  subss    xmm1, dword ptr [esp + 0x14]
  0x00052b06  movss    dword ptr [esp + 0x28], xmm0
  0x00052b0c  movss    xmm0, dword ptr [0x105f5808]   ; f32=1 i32=1065353216 f64=5.26354e-315
  0x00052b14  subss    xmm0, xmm2
  0x00052b18  mulss    xmm0, xmm1
  0x00052b1c  addss    xmm0, dword ptr [esp + 0x14]
  0x00052b22  movss    dword ptr [esp + 0x2c], xmm0
  0x00052b28  movss    xmm0, dword ptr [esi + 8]
  0x00052b2d  movss    dword ptr [esp + 0x30], xmm0
  0x00052b33  call     dword ptr [0x104e5294]   ; f32=1.1645e-38 i32=8310154 f64=2.74161e-306
  0x00052b39  push     eax
  0x00052b3a  lea      eax, [esp + 0x2c]
  0x00052b3e  push     eax
  0x00052b3f  lea      ecx, [esp + 0x48]
  0x00052b43  call     dword ptr [0x104e56d8]   ; f32=1.16655e-38 i32=8324784 f64=2.76151e-306
  0x00052b49  mov      eax, dword ptr [esp + 8]
  0x00052b4d  cmp      byte ptr [eax + 0x934], 0
  0x00052b54  je       0x10052b8d
  0x00052b56  movss    xmm1, dword ptr [0x105f5b10]   ; f32=-0 i32=-2147483648 f64=-1.061e-314
  0x00052b5e  movss    xmm3, dword ptr [esi + 0x18]
  0x00052b63  movss    xmm2, dword ptr [esi + 0x1c]
  0x00052b68  xorps    xmm3, xmm1
  0x00052b6b  movss    xmm0, dword ptr [esi + 0x20]
  0x00052b70  xorps    xmm2, xmm1
  0x00052b73  xorps    xmm0, xmm1
  0x00052b76  unpcklps xmm3, xmm2
  0x00052b79  movss    dword ptr [esp + 0x30], xmm0
  0x00052b7f  mov      eax, dword ptr [esp + 0x30]
  0x00052b83  movq     qword ptr [esp + 0x1c], xmm3
  0x00052b89  mov      dword ptr [esp + 0x24], eax
  0x00052b8d  lea      eax, [esp + 0x40]
  0x00052b91  mov      ecx, edi
  0x00052b93  push     eax
  0x00052b94  lea      eax, [esp + 0x20]
  0x00052b98  push     eax
  0x00052b99  push     dword ptr [ebp + 8]
  0x00052b9c  call     0x10049290   ; -> ?RotateTowards@Character@GAME@@QAE_NHABVVec3@2@ABVWorldVec3@2@@Z
  0x00052ba1  mov      ecx, dword ptr [esp + 8]
  0x00052ba5  lea      ecx, [ecx + 0x5d8]
  0x00052bab  call     0x1043d9a0   ; -> ?Moved@SkillManager@GAME@@QAEXXZ
  0x00052bb0  pop      edi
  0x00052bb1  pop      esi
  0x00052bb2  mov      esp, ebp
  0x00052bb4  pop      ebp
  0x00052bb5  ret      8
  0x00052bb8  int3     
  0x00052bb9  int3     
  0x00052bba  int3     
  0x00052bbb  int3     
  0x00052bbc  int3     
  0x00052bbd  int3     
  0x00052bbe  int3     
  0x00052bbf  int3     
