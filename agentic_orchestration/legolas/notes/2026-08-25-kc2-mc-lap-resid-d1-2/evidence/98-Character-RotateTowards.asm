  0x00049290  push     ebp
  0x00049291  mov      ebp, esp
  0x00049293  and      esp, 0xfffffff0
  0x00049296  sub      esp, 0x11c
  0x0004929c  push     esi
  0x0004929d  lea      eax, [esp + 0x4c]
  0x000492a1  mov      esi, ecx
  0x000492a3  push     eax
  0x000492a4  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x000492aa  mov      ecx, dword ptr [ebp + 0xc]
  0x000492ad  xorps    xmm3, xmm3
  0x000492b0  movq     qword ptr [esp + 0x28], xmm3
  0x000492b6  movss    xmm1, dword ptr [ecx + 4]
  0x000492bb  movss    xmm2, dword ptr [ecx]
  0x000492bf  movss    xmm0, dword ptr [ecx + 8]
  0x000492c4  mulss    xmm2, xmm2
  0x000492c8  mulss    xmm1, xmm1
  0x000492cc  mulss    xmm0, xmm0
  0x000492d0  addss    xmm2, xmm1
  0x000492d4  addss    xmm2, xmm0
  0x000492d8  ucomiss  xmm2, xmm3
  0x000492db  lahf     
  0x000492dc  test     ah, 0x44
  0x000492df  jnp      0x100496cf
  0x000492e5  xorps    xmm1, xmm1
  0x000492e8  movss    xmm0, dword ptr [0x105f57b4]   ; f32=0.2 i32=1045220557 f64=1.19209e-07
  0x000492f0  sqrtss   xmm1, xmm2
  0x000492f4  comiss   xmm0, xmm1
  0x000492f7  ja       0x100496cf
  0x000492fd  cmp      byte ptr [esi + 0x1cb8], 0
  0x00049304  movq     xmm0, qword ptr [ecx]
  0x00049308  mov      eax, dword ptr [ecx + 8]
  0x0004930b  movq     qword ptr [esp + 0x1c], xmm0
  0x00049311  movss    xmm2, dword ptr [esp + 0x1c]
  0x00049317  mov      dword ptr [esp + 0x24], eax
  0x0004931b  movaps   xmm0, xmm2
  0x0004931e  movss    xmm4, dword ptr [esp + 0x24]
  0x00049324  movaps   xmm1, xmm4
  0x00049327  mulss    xmm0, xmm2
  0x0004932b  mulss    xmm1, xmm4
  0x0004932f  movss    xmm6, dword ptr [0x105f5808]   ; f32=1 i32=1065353216 f64=5.26354e-315
  0x00049337  movd     xmm7, dword ptr [ebp + 8]
  0x0004933c  addss    xmm1, xmm0
  0x00049340  xorps    xmm0, xmm0
  0x00049343  cvtdq2ps xmm7, xmm7
  0x00049346  sqrtss   xmm0, xmm1
  0x0004934a  movaps   xmm1, xmm6
  0x0004934d  divss    xmm1, xmm0
  0x00049351  movaps   xmm5, xmm1
  0x00049354  mulss    xmm2, xmm1
  0x00049358  mulss    xmm5, xmm3
  0x0004935c  mulss    xmm4, xmm1
  0x00049360  movss    dword ptr [esp + 0x44], xmm2
  0x00049366  movss    dword ptr [esp + 0x10], xmm2
  0x0004936c  movss    dword ptr [esp + 0x40], xmm5
  0x00049372  movss    dword ptr [esp + 0x14], xmm5
  0x00049378  movss    dword ptr [esp + 0x48], xmm4
  0x0004937e  movss    dword ptr [esp + 0x18], xmm4
  0x00049384  jne      0x100496a5
  0x0004938a  movaps   xmm0, xmm2
  0x0004938d  movaps   xmm1, xmm5
  0x00049390  mulss    xmm0, xmm2
  0x00049394  mulss    xmm1, xmm5
  0x00049398  addss    xmm1, xmm0
  0x0004939c  movaps   xmm0, xmm4
  0x0004939f  mulss    xmm0, xmm4
  0x000493a3  addss    xmm1, xmm0
  0x000493a7  ucomiss  xmm1, xmm3
  0x000493aa  lahf     
  0x000493ab  test     ah, 0x44
  0x000493ae  jnp      0x100496a5
  0x000493b4  xorps    xmm0, xmm0
  0x000493b7  sqrtss   xmm0, xmm1
  0x000493bb  ucomiss  xmm0, xmm3
  0x000493be  lahf     
  0x000493bf  test     ah, 0x44
  0x000493c2  jnp      0x100496a5
  0x000493c8  movss    xmm3, dword ptr [esp + 0x74]
  0x000493ce  movss    xmm0, dword ptr [esp + 0x78]
  0x000493d4  mulss    xmm3, xmm2
  0x000493d8  mulss    xmm0, xmm5
  0x000493dc  movss    xmm2, dword ptr [esi + 0x3014]
  0x000493e4  addss    xmm3, xmm0
  0x000493e8  movss    xmm0, dword ptr [esp + 0x7c]
  0x000493ee  mulss    xmm0, xmm4
  0x000493f2  movss    xmm4, dword ptr [esi + 0x3010]
  0x000493fa  addss    xmm3, xmm0
  0x000493fe  movss    xmm0, dword ptr [esi + 0x3018]
  0x00049406  mulss    xmm4, xmm0
  0x0004940a  mulss    xmm2, xmm0
  0x0004940e  maxss    xmm3, dword ptr [0x105f594c]   ; f32=-1 i32=-1082130432 f64=-2
  0x00049416  subss    xmm4, xmm2
  0x0004941a  minss    xmm3, xmm6
  0x0004941e  movaps   xmm1, xmm3
  0x00049421  movaps   xmm0, xmm3
  0x00049424  addss    xmm1, xmm6
  0x00049428  mulss    xmm1, dword ptr [0x105f57dc]   ; f32=0.5 i32=1056964608 f64=3.05225e-05
  0x00049430  mulss    xmm4, xmm1
  0x00049434  addss    xmm4, xmm2
  0x00049438  mulss    xmm4, xmm7
  0x0004943c  mulss    xmm4, dword ptr [0x105f575c]   ; f32=0.001 i32=981668463 f64=1.972e-24
  0x00049444  movss    dword ptr [esp + 0x3c], xmm4
  0x0004944a  call     0x104c006e   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x383be
  0x0004944f  movss    xmm2, dword ptr [esp + 0x3c]
  0x00049455  comiss   xmm2, xmm0
  0x00049458  jbe      0x10049548
  0x0004945e  lea      eax, [esp + 0x1c]
  0x00049462  mov      dword ptr [esp + 0x1c], 0
  0x0004946a  push     eax
  0x0004946b  lea      eax, [esp + 0x14]
  0x0004946f  mov      dword ptr [esp + 0x24], 0x3f800000
  0x00049477  push     eax
  0x00049478  lea      edx, [esp + 0x30]
  0x0004947c  mov      dword ptr [esp + 0x2c], 0
  0x00049484  lea      ecx, [esp + 0x88]
  0x0004948b  mov      dword ptr [esp + 0x30], 0
  0x00049493  mov      dword ptr [esp + 0x34], 0
  0x0004949b  mov      dword ptr [esp + 0x38], 0
  0x000494a3  call     0x1048ad40   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x3090
  0x000494a8  add      esp, 8
