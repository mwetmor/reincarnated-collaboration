; DurationDamageManager::ExecuteDamage -> CombatManager::ApplyDamage
; Game.dll RVA 0x00208370  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x00208370  push     ebp
  0x00208371  mov      ebp, esp
  0x00208373  push     -1
  0x00208375  push     0x104cb5ee
  0x0020837a  mov      eax, dword ptr fs:[0]
  0x00208380  push     eax
  0x00208381  mov      dword ptr fs:[0], esp
  0x00208388  sub      esp, 0xc0
  0x0020838e  xor      al, al
  0x00208390  xorps    xmm0, xmm0
  0x00208393  mov      dword ptr [ebp - 0x2c], eax
  0x00208396  mov      eax, dword ptr [ebp + 8]
  0x00208399  push     esi
  0x0020839a  push     edi
  0x0020839b  mov      edi, ecx
  0x0020839d  movss    dword ptr [ebp - 0x34], xmm0
  0x002083a2  mov      dword ptr [ebp - 0x14], edi
  0x002083a5  movss    dword ptr [ebp - 0x38], xmm0
  0x002083aa  mov      dword ptr [eax], 0
  0x002083b0  call     0x10209fc0   ; -> ?UpdateFxAndInfluence@DurationDamageManager@GAME@@IAEXXZ
  0x002083b5  mov      esi, dword ptr [edi + 0x2c]
  0x002083b8  mov      dword ptr [ebp - 0x30], esi
  0x002083bb  cmp      esi, dword ptr [edi + 0x30]
  0x002083be  je       0x1020873c
  0x002083c4  push     ebx
  0x002083c5  mov      bl, byte ptr [ebp + 0xb]
  0x002083c8  nop      dword ptr [eax + eax]
  0x002083d0  mov      dword ptr [ebp - 0x28], 0
  0x002083d7  mov      dword ptr [ebp - 0x24], 0
  0x002083de  mov      dword ptr [ebp - 0x20], 0
  0x002083e5  mov      dword ptr [ebp - 4], 0
  0x002083ec  lea      ecx, [ebp - 0x40]
  0x002083ef  mov      eax, dword ptr [esi]
  0x002083f1  push     ecx
  0x002083f2  lea      ecx, [ebp - 0x28]
  0x002083f5  mov      dword ptr [ebp - 0x40], 0
  0x002083fc  push     ecx
  0x002083fd  mov      eax, dword ptr [eax + 8]
  0x00208400  mov      ecx, esi
  0x00208402  call     eax
  0x00208404  mov      edx, dword ptr [ebp - 0x24]
  0x00208407  lea      eax, [ebp - 0x18]
  0x0020840a  mov      ecx, dword ptr [ebp - 0x28]
  0x0020840d  push     eax
  0x0020840e  mov      eax, edx
  0x00208410  mov      byte ptr [ebp - 0x18], bl
  0x00208413  sub      eax, ecx
  0x00208415  sar      eax, 2
  0x00208418  push     eax
  0x00208419  fstp     dword ptr [ebp - 0x1c]
  0x0020841c  call     0x1020b630   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x11f0
  0x00208421  mov      ecx, dword ptr [ebp - 0x24]
  0x00208424  add      esp, 8
  0x00208427  mov      edi, dword ptr [ebp - 0x28]
  0x0020842a  mov      eax, ecx
  0x0020842c  mov      dword ptr [ebp - 0x3c], eax
  0x0020842f  cmp      edi, ecx
  0x00208431  je       0x10208451
  0x00208433  mov      edx, edi
  0x00208435  add      edi, 4
  0x00208438  cmp      edi, ecx
  0x0020843a  je       0x10208451
  0x0020843c  nop      dword ptr [eax]
  0x00208440  mov      ecx, dword ptr [edx]
  0x00208442  cmp      ecx, dword ptr [edi]
  0x00208444  mov      ecx, eax
  0x00208446  je       0x10208463
  0x00208448  mov      edx, edi
  0x0020844a  add      edi, 4
  0x0020844d  cmp      edi, ecx
  0x0020844f  jne      0x10208440
  0x00208451  mov      edi, ecx
  0x00208453  mov      edx, dword ptr [ebp - 0x28]
  0x00208456  cmp      edi, edx
  0x00208458  jne      0x102084b5
  0x0020845a  cmp      eax, ecx
  0x0020845c  jne      0x102084b5
  0x0020845e  mov      dword ptr [ebp - 0x24], edx
  0x00208461  jmp      0x102084d2   ; -> ?ExecuteDamage@DurationDamageManager@GAME@@IAEMAAM@Z+0x162
  0x00208463  add      edi, 4
  0x00208466  mov      dword ptr [ebp - 0x10], 0
  0x0020846d  mov      esi, ecx
  0x0020846f  mov      dword ptr [ebp - 0x44], 0
  0x00208476  sub      esi, edi
  0x00208478  add      esi, 3
  0x0020847b  shr      esi, 2
  0x0020847e  cmp      edi, ecx
  0x00208480  cmova    esi, dword ptr [ebp - 0x10]
  0x00208484  mov      dword ptr [ebp - 0x10], esi
  0x00208487  test     esi, esi
  0x00208489  mov      esi, dword ptr [ebp - 0x30]
  0x0020848c  je       0x102084b0
  0x0020848e  mov      ecx, dword ptr [ebp - 0x44]
  0x00208491  mov      esi, dword ptr [ebp - 0x10]
  0x00208494  mov      eax, dword ptr [edi]
  0x00208496  cmp      dword ptr [edx], eax
  0x00208498  je       0x1020849f
  0x0020849a  add      edx, 4
  0x0020849d  mov      dword ptr [edx], eax
  0x0020849f  inc      ecx
  0x002084a0  add      edi, 4
  0x002084a3  cmp      ecx, esi
  0x002084a5  jne      0x10208494
  0x002084a7  mov      eax, dword ptr [ebp - 0x3c]
  0x002084aa  mov      esi, dword ptr [ebp - 0x30]
  0x002084ad  mov      ecx, dword ptr [ebp - 0x24]
  0x002084b0  lea      edi, [edx + 4]
  0x002084b3  jmp      0x10208453   ; -> ?ExecuteDamage@DurationDamageManager@GAME@@IAEMAAM@Z+0xe3
  0x002084b5  cmp      edi, eax
  0x002084b7  je       0x102084d2
  0x002084b9  sub      ecx, eax
  0x002084bb  push     ecx
  0x002084bc  push     eax
  0x002084bd  push     edi
  0x002084be  mov      dword ptr [ebp - 0x10], ecx
  0x002084c1  call     dword ptr [0x104e63e4]   ; f32=1.17327e-38 i32=8372762 f64=2.82655e-306
  0x002084c7  mov      eax, dword ptr [ebp - 0x10]
  0x002084ca  add      esp, 0xc
  0x002084cd  add      eax, edi
  0x002084cf  mov      dword ptr [ebp - 0x24], eax
  0x002084d2  mov      eax, dword ptr [ebp + 8]
  0x002084d5  movss    xmm0, dword ptr [eax]
  0x002084d9  maxss    xmm0, dword ptr [ebp - 0x40]
  0x002084de  movss    dword ptr [eax], xmm0
  0x002084e2  mov      eax, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x002084e7  mov      edi, dword ptr [esi + 4]
  0x002084ea  mov      ecx, dword ptr [eax + 0x27f0]
  0x002084f0  mov      eax, dword ptr [ecx]
  0x002084f2  call     dword ptr [eax + 0xc]
  0x002084f5  movss    xmm1, dword ptr [ebp - 0x1c]
  0x002084fa  cmp      edi, dword ptr [eax + 8]
  0x002084fd  jne      0x1020850c
  0x002084ff  movaps   xmm0, xmm1
  0x00208502  addss    xmm0, dword ptr [ebp - 0x38]
  0x00208507  movss    dword ptr [ebp - 0x38], xmm0
  0x0020850c  comiss   xmm1, dword ptr [0x105f5708]   ; f32=0 i32=0 f64=0
  0x00208513  movaps   xmm0, xmm1
  0x00208516  addss    xmm0, dword ptr [ebp - 0x34]
  0x0020851b  movss    dword ptr [ebp - 0x34], xmm0
  0x00208520  jbe      0x10208614
  0x00208526  mov      ecx, dword ptr [ebp - 0x14]
  0x00208529  mov      edx, dword ptr [esi + 4]
  0x0020852c  mov      edi, dword ptr [esi + 8]
  0x0020852f  push     edx
  0x00208530  mov      ecx, dword ptr [ecx + 4]
  0x00208533  mov      dword ptr [ebp - 0x10], edx
  0x00208536  mov      eax, dword ptr [ecx]
  0x00208538  call     dword ptr [eax + 0x360]
  0x0020853e  cmp      edi, 0x14
  0x00208541  jne      0x10208757
  0x00208547  mov      ecx, dword ptr [ebp - 0x14]
  0x0020854a  xorps    xmm1, xmm1
  0x0020854d  mov      edi, dword ptr [ebp - 0x10]
  0x00208550  mov      dword ptr [ebp - 0x4c], 1
  0x00208557  mov      dword ptr [ebp - 0x48], 0x14
  0x0020855e  mov      eax, dword ptr [ecx + 4]
  0x00208561  movsd    xmm0, qword ptr [eax + 0xa38]
  0x00208569  mov      eax, dword ptr [ecx + 8]
  0x0020856c  maxsd    xmm0, xmm1
  0x00208570  mov      dword ptr [eax + 0xf4], edi
  0x00208576  lea      eax, [ebp - 0x28]
  0x00208579  cvtpd2ps xmm0, xmm0
  0x0020857d  push     eax
  0x0020857e  push     0x14
  0x00208580  lea      eax, [ebp - 0x4c]
  0x00208583  push     eax
  0x00208584  push     ecx
  0x00208585  mov      ecx, dword ptr [ecx + 8]
  0x00208588  movss    dword ptr [ebp - 0x3c], xmm0
  0x0020858d  movss    xmm0, dword ptr [ebp - 0x1c]
  0x00208592  movss    dword ptr [esp], xmm0
  0x00208597  call     0x100e0a40   ; -> ?ApplyDamage@CombatManager@GAME@@QAE_NMABUPlayStatsDamageType@2@W4CombatAttributeType@2@ABV?$vector@I@mem@@@Z
  0x0020859c  test     al, al
  0x0020859e  je       0x10208614
  0x002085a0  lea      ecx, [ebp - 0xcc]
  0x002085a6  call     0x10035c10   ; -> ?IsUsed@ConversationStep@GAME@@QBE_NXZ+0x10
  0x002085ab  movss    xmm0, dword ptr [ebp - 0x1c]
  0x002085b0  mov      byte ptr [ebp - 4], 1
  0x002085b4  movss    xmm1, dword ptr [ebp - 0x3c]
  0x002085b9  comiss   xmm1, xmm0
  0x002085bc  jbe      0x102085c8
  0x002085be  movss    dword ptr [ebp - 0xc8], xmm0
  0x002085c6  jmp      0x102085d0   ; -> ?ExecuteDamage@DurationDamageManager@GAME@@IAEMAAM@Z+0x260
  0x002085c8  movss    dword ptr [ebp - 0xc8], xmm1
  0x002085d0  push     edi
  0x002085d1  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x002085d7  mov      ecx, eax
  0x002085d9  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x002085de  test     eax, eax
  0x002085e0  je       0x102085f7
  0x002085e2  mov      edx, dword ptr [eax]
  0x002085e4  lea      ecx, [ebp - 0xcc]
  0x002085ea  push     0
  0x002085ec  push     0
  0x002085ee  push     ecx
  0x002085ef  mov      ecx, eax
  0x002085f1  call     dword ptr [edx + 0x32c]
  0x002085f7  mov      edx, dword ptr [ebp - 0x78]
  0x002085fa  mov      byte ptr [ebp - 0x2c], 1
  0x002085fe  cmp      edx, 0x10
  0x00208601  jb       0x10208614
  0x00208603  mov      ecx, dword ptr [ebp - 0x8c]
  0x00208609  inc      edx
  0x0020860a  push     1
  0x0020860c  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x00208611  add      esp, 4
  0x00208614  mov      edi, dword ptr [ebp - 0x14]
  0x00208617  add      esi, 0x24
  0x0020861a  mov      dword ptr [ebp - 4], 0xffffffff
  0x00208621  mov      ecx, dword ptr [ebp - 0x28]
  0x00208624  mov      dword ptr [ebp - 0x30], esi
  0x00208627  test     ecx, ecx
  0x00208629  je       0x10208690
  0x0020862b  mov      eax, dword ptr [ebp - 0x20]
  0x0020862e  sub      eax, ecx
  0x00208630  sar      eax, 2
  0x00208633  cmp      eax, 0x3fffffff
  0x00208638  ja       0x10208876
  0x0020863e  shl      eax, 2
  0x00208641  cmp      eax, 0x1000
  0x00208646  jb       0x10208672
  0x00208648  test     cl, 0x1f
  0x0020864b  jne      0x10208876
  0x00208651  mov      eax, dword ptr [ecx - 4]
  0x00208654  cmp      eax, ecx
  0x00208656  jae      0x10208876
  0x0020865c  sub      ecx, eax
  0x0020865e  cmp      ecx, 4
  0x00208661  jb       0x10208876
  0x00208667  cmp      ecx, 0x23
  0x0020866a  ja       0x10208876
  0x00208670  mov      ecx, eax
  0x00208672  push     ecx
  0x00208673  call     0x104be91b   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c6b
  0x00208678  add      esp, 4
  0x0020867b  mov      dword ptr [ebp - 0x28], 0
  0x00208682  mov      dword ptr [ebp - 0x24], 0
  0x00208689  mov      dword ptr [ebp - 0x20], 0
  0x00208690  cmp      esi, dword ptr [edi + 0x30]
  0x00208693  jne      0x102083d0
  0x00208699  mov      eax, dword ptr [ebp - 0x2c]
  0x0020869c  pop      ebx
  0x0020869d  test     al, al
  0x0020869f  je       0x1020873c
  0x002086a5  mov      esi, dword ptr [edi + 4]
  0x002086a8  xorps    xmm1, xmm1
  0x002086ab  movaps   xmm0, xmmword ptr [0x105f5a20]   ; f32=0 i32=0 f64=0.0078125
  0x002086b2  movups   xmmword ptr [ebp - 0x6c], xmm0
  0x002086b6  mov      dword ptr [ebp - 0x70], 0
  0x002086bd  movsd    xmm0, qword ptr [esi + 0xa38]
  0x002086c5  maxsd    xmm0, xmm1
  0x002086c9  mov      dword ptr [ebp - 0x5c], 0
  0x002086d0  cvtpd2ps xmm0, xmm0
  0x002086d4  comiss   xmm1, xmm0
  0x002086d7  jae      0x1020873c
  0x002086d9  cmp      dword ptr [esi + 0x1b9c], 9
  0x002086e0  je       0x1020873c
  0x002086e2  movups   xmm0, xmmword ptr [ebp - 0x70]
  0x002086e6  lea      eax, [esi + 0x1db0]
  0x002086ec  movups   xmmword ptr [esi + 0x1de0], xmm0
  0x002086f3  movq     xmm0, qword ptr [ebp - 0x60]
  0x002086f8  movq     qword ptr [esi + 0x1df0], xmm0
  0x00208700  mov      dword ptr [esi + 0x1df8], 0
  0x0020870a  cmp      dword ptr [eax + 0x10], 0
  0x0020870e  je       0x10208723
  0x00208710  push     eax
  0x00208711  call     dword ptr [0x104e5704]   ; f32=1.16663e-38 i32=8325376 f64=2.7624e-306
  0x00208717  add      esp, 4
  0x0020871a  mov      dword ptr [esi + 0x1de0], eax
  0x00208720  xorps    xmm1, xmm1
