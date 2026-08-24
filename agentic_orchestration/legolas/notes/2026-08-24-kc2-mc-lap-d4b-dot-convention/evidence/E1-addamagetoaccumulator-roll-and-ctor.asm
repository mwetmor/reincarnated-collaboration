; DamageAttributeDur::AddDamageToAccumulator (.dbr roll -> CombatAttributeDurDamage ctor, inlined)
; Game.dll RVA 0x001425b0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x001425b0  push     ebp
  0x001425b1  mov      ebp, esp
  0x001425b3  push     -1
  0x001425b5  push     0x104c9f6f
  0x001425ba  mov      eax, dword ptr fs:[0]
  0x001425c0  push     eax
  0x001425c1  mov      dword ptr fs:[0], esp
  0x001425c8  sub      esp, 0x10
  0x001425cb  push     ebx
  0x001425cc  mov      ebx, ecx
  0x001425ce  push     esi
  0x001425cf  mov      esi, dword ptr [ebp + 0x10]
  0x001425d2  push     esi
  0x001425d3  mov      eax, dword ptr [ebx]
  0x001425d5  mov      dword ptr [ebp - 0x1c], ebx
  0x001425d8  mov      eax, dword ptr [eax + 4]
  0x001425db  call     eax
  0x001425dd  cmp      byte ptr [ebp + 0x18], 0
  0x001425e1  fstp     dword ptr [ebp - 0x10]
  0x001425e4  jne      0x10142603
  0x001425e6  mov      ecx, dword ptr [ebp + 0xc]
  0x001425e9  movss    xmm0, dword ptr [ebp - 0x10]
  0x001425ee  push     ecx
  0x001425ef  movss    dword ptr [esp], xmm0
  0x001425f4  mov      eax, dword ptr [ecx]
  0x001425f6  mov      eax, dword ptr [eax + 8]
  0x001425f9  call     eax
  0x001425fb  test     al, al
  0x001425fd  je       0x10142849
  0x00142603  mov      eax, dword ptr [ebx]
  0x00142605  mov      ecx, ebx
  0x00142607  push     edi
  0x00142608  push     0
  0x0014260a  push     esi
  0x0014260b  mov      eax, dword ptr [eax + 0xb4]
  0x00142611  call     eax
  0x00142613  mov      eax, dword ptr [ebx]
  0x00142615  mov      ecx, ebx
  0x00142617  push     0
  0x00142619  fstp     dword ptr [ebp - 0x18]
  0x0014261c  push     esi
  0x0014261d  mov      eax, dword ptr [eax + 0xb8]
  0x00142623  call     eax
  0x00142625  mov      edi, dword ptr [ebp + 0x14]
  0x00142628  xor      edx, edx
  0x0014262a  mov      ecx, 0x1f31d
  0x0014262f  movss    xmm0, dword ptr [ebp + 0x1c]
  0x00142634  addss    xmm0, dword ptr [ebp + 0x20]
  0x00142639  fstp     dword ptr [ebp - 0x14]
  0x0014263c  mov      eax, dword ptr [edi]
  0x0014263e  div      ecx
  0x00142640  mov      ecx, dword ptr [ebp + 0xc]
  0x00142643  imul     eax, eax, 0xb14
  0x00142649  imul     esi, edx, 0x41a7
  0x0014264f  movss    dword ptr [ebp + 0x18], xmm0
  0x00142654  movss    xmm0, dword ptr [ebp - 0x10]
  0x00142659  push     ecx
  0x0014265a  movss    dword ptr [esp], xmm0
  0x0014265f  sub      esi, eax
  0x00142661  lea      eax, [esi + 0x7fffffff]
  0x00142667  cmovs    esi, eax
  0x0014266a  mov      dword ptr [edi], esi
  0x0014266c  mov      eax, dword ptr [ecx]
  0x0014266e  mov      eax, dword ptr [eax + 0xc]
  0x00142671  call     eax
  0x00142673  movss    xmm2, dword ptr [ebp - 0x14]
  0x00142678  mov      ecx, ebx
  0x0014267a  subss    xmm2, dword ptr [ebp - 0x18]
  0x0014267f  movd     xmm0, esi
  0x00142683  cvtdq2pd xmm0, xmm0
  0x00142687  shr      esi, 0x1f
  0x0014268a  mov      eax, dword ptr [ebx]
  0x0014268c  push     0
  0x0014268e  mov      eax, dword ptr [eax + 0xbc]
  0x00142694  addsd    xmm0, qword ptr [esi*8 + 0x105f5ae0]
  0x0014269d  mov      esi, dword ptr [ebp + 0x10]
  0x001426a0  push     esi
  0x001426a1  cvtpd2ps xmm0, xmm0
  0x001426a5  mulss    xmm2, xmm0
  0x001426a9  mulss    xmm2, dword ptr [0x105f5718]   ; f32=4.65661e-10 i32=805306368 f64=4.52784e-72
  0x001426b1  addss    xmm2, dword ptr [ebp - 0x18]
  0x001426b6  movss    dword ptr [ebp + 0x14], xmm2
  0x001426bb  fmul     dword ptr [ebp + 0x14]
  0x001426be  fmul     dword ptr [ebp + 0x18]
  0x001426c1  fstp     dword ptr [ebp + 0x20]
  0x001426c4  call     eax
  0x001426c6  mov      eax, dword ptr [ebx]
  0x001426c8  mov      ecx, ebx
  0x001426ca  push     0
  0x001426cc  fstp     dword ptr [ebp + 0x1c]
  0x001426cf  push     esi
  0x001426d0  mov      eax, dword ptr [eax + 0xc0]
  0x001426d6  call     eax
  0x001426d8  mov      eax, dword ptr [edi]
  0x001426da  xor      edx, edx
  0x001426dc  mov      ecx, 0x1f31d
  0x001426e1  div      ecx
  0x001426e3  fstp     dword ptr [ebp + 0x14]
  0x001426e6  movss    xmm2, dword ptr [ebp + 0x14]
  0x001426eb  subss    xmm2, dword ptr [ebp + 0x1c]
  0x001426f0  imul     eax, eax, 0xb14
  0x001426f6  imul     ecx, edx, 0x41a7
  0x001426fc  sub      ecx, eax
  0x001426fe  lea      eax, [ecx + 0x7fffffff]
  0x00142704  cmovs    ecx, eax
  0x00142707  mov      dword ptr [edi], ecx
  0x00142709  movd     xmm0, ecx
  0x0014270d  cvtdq2pd xmm0, xmm0
  0x00142711  shr      ecx, 0x1f
  0x00142714  addsd    xmm0, qword ptr [ecx*8 + 0x105f5ae0]
  0x0014271d  mov      eax, dword ptr [ebx]
  0x0014271f  mov      ecx, ebx
  0x00142721  cvtpd2ps xmm0, xmm0
  0x00142725  push     0
  0x00142727  push     esi
  0x00142728  mov      eax, dword ptr [eax + 0xb4]
  0x0014272e  mulss    xmm2, xmm0
  0x00142732  mulss    xmm2, dword ptr [0x105f5718]   ; f32=4.65661e-10 i32=805306368 f64=4.52784e-72
  0x0014273a  addss    xmm2, dword ptr [ebp + 0x1c]
  0x0014273f  movss    dword ptr [ebp + 0x1c], xmm2
  0x00142744  call     eax
  0x00142746  mov      esi, dword ptr [ebp + 0xc]
  0x00142749  movss    xmm0, dword ptr [ebp - 0x10]
  0x0014274e  push     ecx
  0x0014274f  fstp     dword ptr [ebp + 0x14]
  0x00142752  mov      eax, dword ptr [esi]
  0x00142754  mov      ecx, esi
  0x00142756  movss    dword ptr [esp], xmm0
  0x0014275b  mov      eax, dword ptr [eax + 0xc]
  0x0014275e  call     eax
  0x00142760  fmul     dword ptr [ebp + 0x14]
  0x00142763  mov      ecx, ebx
  0x00142765  mov      eax, dword ptr [ebx]
  0x00142767  push     0
  0x00142769  push     dword ptr [ebp + 0x10]
  0x0014276c  fmul     dword ptr [ebp + 0x18]
  0x0014276f  mov      eax, dword ptr [eax + 0xb8]
  0x00142775  fstp     dword ptr [ebp + 0x14]
  0x00142778  call     eax
  0x0014277a  mov      eax, dword ptr [esi]
  0x0014277c  movss    xmm0, dword ptr [ebp - 0x10]
  0x00142781  push     ecx
  0x00142782  fstp     dword ptr [ebp + 0x10]
  0x00142785  mov      eax, dword ptr [eax + 0xc]
  0x00142788  mov      ecx, esi
  0x0014278a  movss    dword ptr [esp], xmm0
  0x0014278f  call     eax
  0x00142791  fmul     dword ptr [ebp + 0x10]
  0x00142794  push     0x3c
  0x00142796  fmul     dword ptr [ebp + 0x18]
  0x00142799  fstp     dword ptr [ebp + 0x18]
  0x0014279c  call     0x104be920   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70
  0x001427a1  mov      ebx, eax
  0x001427a3  add      esp, 4
  0x001427a6  mov      dword ptr [ebp + 0x10], ebx
  0x001427a9  mov      ecx, dword ptr [ebp - 0x1c]
  0x001427ac  mov      esi, dword ptr [ebp + 8]
  0x001427af  mov      dword ptr [ebp - 4], 0
  0x001427b6  mov      edx, dword ptr [ecx]
  0x001427b8  mov      edi, dword ptr [ecx + 0x54]
  0x001427bb  call     dword ptr [edx + 0x14]
  0x001427be  movss    xmm0, dword ptr [ebp + 0x20]
  0x001427c3  mov      ecx, dword ptr [ebp + 0xc]
  0x001427c6  mov      dword ptr [ebx + 4], eax
  0x001427c9  add      ecx, 4
  0x001427cc  mov      dword ptr [ebx + 8], 0
  0x001427d3  lea      eax, [ebp + 0x18]
  0x001427d6  mov      dword ptr [ebx + 0x10], 0
  0x001427dd  mov      dword ptr [ebx + 0x14], 0
  0x001427e4  movss    dword ptr [ebx + 0x1c], xmm0
  0x001427e9  movss    xmm0, dword ptr [ebp + 0x14]
  0x001427ee  movss    dword ptr [ebx + 0x28], xmm0
  0x001427f3  movss    xmm0, dword ptr [ebp + 0x18]
  0x001427f8  movss    dword ptr [ebx + 0x2c], xmm0
  0x001427fd  movss    xmm0, dword ptr [ebp + 0x1c]
  0x00142802  mov      dword ptr [ebp - 4], 0xffffffff
  0x00142809  push     eax
  0x0014280a  mov      dword ptr [ebx + 0x18], 0
  0x00142811  mov      dword ptr [ebx], 0x105b9940
  0x00142817  movss    dword ptr [ebx + 0x20], xmm0
  0x0014281c  movss    dword ptr [ebx + 0x24], xmm0
  0x00142821  mov      dword ptr [ebx + 0x10], esi
  0x00142824  mov      dword ptr [ebx + 0x14], edi
  0x00142827  mov      dword ptr [ebx + 0x30], 0
  0x0014282e  mov      dword ptr [ebx + 0x34], 0
  0x00142835  mov      dword ptr [ebx + 0x38], 0
  0x0014283c  mov      byte ptr [ebx + 0xc], 1
  0x00142840  mov      dword ptr [ebp + 0x18], ebx
  0x00142843  call     0x1000a3e0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0x20
  0x00142848  pop      edi
  0x00142849  mov      ecx, dword ptr [ebp - 0xc]
  0x0014284c  pop      esi
  0x0014284d  pop      ebx
  0x0014284e  mov      dword ptr fs:[0], ecx
  0x00142855  mov      esp, ebp
  0x00142857  pop      ebp
  0x00142858  ret      0x1c
  0x0014285b  int3     
  0x0014285c  int3     
  0x0014285d  int3     
  0x0014285e  int3     
  0x0014285f  int3     
  0x00142860  push     ebp
  0x00142861  mov      ebp, esp
  0x00142863  push     ecx
