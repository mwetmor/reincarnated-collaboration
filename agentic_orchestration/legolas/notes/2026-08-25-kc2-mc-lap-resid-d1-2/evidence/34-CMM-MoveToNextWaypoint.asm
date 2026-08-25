=== 34-CMM-MoveToNextWaypoint  RVA 0x000771a0  sym=?MoveToNextWaypoint@CharacterMovementManager@GAME@@AAE_NXZ ===
  0x000771a0  push     ebp
  0x000771a1  mov      ebp, esp
  0x000771a3  sub      esp, 0xc4
  0x000771a9  push     ebx
  0x000771aa  mov      ebx, ecx
  0x000771ac  cmp      dword ptr [ebx + 0x38], 0
  0x000771b0  jne      0x100771b9
  0x000771b2  xor      al, al
  0x000771b4  pop      ebx
  0x000771b5  mov      esp, ebp
  0x000771b7  pop      ebp
  0x000771b8  ret      
  0x000771b9  push     esi
  0x000771ba  lea      eax, [ebp - 0x18]
  0x000771bd  push     eax
  0x000771be  lea      ecx, [ebx + 0x28]
  0x000771c1  call     0x1005f1f0   ; -> ?SelectPrimaryAction@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MAE_N_N_N1ABVWorldVec3@2@AAI1@Z+0x1150
  0x000771c6  mov      edx, eax
  0x000771c8  mov      eax, dword ptr [edx]
  0x000771ca  test     eax, eax
  0x000771cc  je       0x100771d0
  0x000771ce  mov      eax, dword ptr [eax]
  0x000771d0  mov      ecx, dword ptr [eax + 8]
  0x000771d3  mov      eax, dword ptr [eax + 4]
  0x000771d6  dec      ecx
  0x000771d7  and      ecx, dword ptr [edx + 8]
  0x000771da  mov      eax, dword ptr [eax + ecx*4]
  0x000771dd  movups   xmm0, xmmword ptr [eax]
  0x000771e0  movups   xmmword ptr [ebp - 0x5c], xmm0
  0x000771e4  movups   xmm0, xmmword ptr [eax + 0x10]
  0x000771e8  movups   xmmword ptr [ebp - 0x4c], xmm0
  0x000771ec  movups   xmm0, xmmword ptr [eax + 0x20]
  0x000771f0  movups   xmmword ptr [ebp - 0x3c], xmm0
  0x000771f4  movups   xmm0, xmmword ptr [eax + 0x30]
  0x000771f8  movups   xmmword ptr [ebp - 0x2c], xmm0
  0x000771fc  mov      eax, dword ptr [eax + 0x40]
  0x000771ff  add      dword ptr [ebx + 0x38], -1
  0x00077203  mov      dword ptr [ebp - 0x1c], eax
  0x00077206  jne      0x10077211
  0x00077208  mov      dword ptr [ebx + 0x34], 0
  0x0007720f  jmp      0x10077214   ; -> ?MoveToNextWaypoint@CharacterMovementManager@GAME@@AAE_NXZ+0x74
  0x00077211  inc      dword ptr [ebx + 0x34]
  0x00077214  mov      eax, dword ptr [ebp - 0x5c]
  0x00077217  cmp      eax, 1
  0x0007721a  jne      0x1007755d
  0x00077220  mov      ecx, dword ptr [ebx]
  0x00077222  lea      eax, [ebp - 0x90]
  0x00077228  push     eax
  0x00077229  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0007722f  movups   xmm0, xmmword ptr [ebp - 0x58]
  0x00077233  movss    xmm5, dword ptr [ebp - 0x7c]
  0x00077238  movss    xmm2, dword ptr [ebp - 0x80]
  0x0007723d  movups   xmmword ptr [ebp - 0x90], xmm0
  0x00077244  movss    xmm0, dword ptr [ebp - 0x3c]
  0x00077249  movaps   xmm6, xmm0
  0x0007724c  movss    xmm4, dword ptr [ebp - 0x78]
  0x00077251  movq     qword ptr [ebp - 8], xmm0
  0x00077256  movss    xmm0, dword ptr [ebp - 0x48]
  0x0007725b  mulss    xmm0, xmm2
  0x0007725f  movss    xmm3, dword ptr [ebp - 0x44]
  0x00077264  mulss    xmm6, xmm5
  0x00077268  movss    xmm1, dword ptr [ebp - 0x40]
  0x0007726d  movss    xmm7, dword ptr [ebp - 0x28]
  0x00077272  addss    xmm6, xmm0
  0x00077276  mulss    xmm3, xmm2
  0x0007727a  movss    xmm0, dword ptr [ebp - 0x30]
  0x0007727f  mulss    xmm0, xmm4
  0x00077283  mulss    xmm1, xmm2
  0x00077287  addss    xmm6, xmm0
  0x0007728b  movss    xmm2, dword ptr [ebp - 0x74]
  0x00077290  movss    xmm0, dword ptr [ebp - 0x38]
  0x00077295  mulss    xmm0, xmm5
  0x00077299  addss    xmm3, xmm0
  0x0007729d  movss    xmm0, dword ptr [ebp - 0x2c]
  0x000772a2  mulss    xmm0, xmm4
  0x000772a6  addss    xmm3, xmm0
  0x000772aa  movss    xmm0, dword ptr [ebp - 0x34]
  0x000772af  mulss    xmm0, xmm5
  0x000772b3  movss    xmm5, dword ptr [ebp - 0x70]
  0x000772b8  addss    xmm1, xmm0
  0x000772bc  unpcklps xmm6, xmm3
  0x000772bf  movss    xmm3, dword ptr [ebp - 0x6c]
  0x000772c4  movaps   xmm0, xmm7
  0x000772c7  mulss    xmm0, xmm4
  0x000772cb  movss    xmm4, dword ptr [ebp - 0x38]
  0x000772d0  movq     qword ptr [ebp - 0x80], xmm6
  0x000772d5  movss    xmm6, dword ptr [ebp - 8]
  0x000772da  addss    xmm1, xmm0
  0x000772de  movss    xmm0, dword ptr [ebp - 0x48]
  0x000772e3  mulss    xmm0, xmm2
  0x000772e7  mulss    xmm6, xmm5
  0x000772eb  mulss    xmm4, xmm5
  0x000772ef  addss    xmm6, xmm0
  0x000772f3  movss    dword ptr [ebp - 0x10], xmm1
  0x000772f8  movss    xmm0, dword ptr [ebp - 0x30]
  0x000772fd  movss    xmm1, dword ptr [ebp - 0x40]
  0x00077302  mulss    xmm0, xmm3
  0x00077306  mov      eax, dword ptr [ebp - 0x10]
  0x00077309  mulss    xmm1, xmm2
  0x0007730d  mov      dword ptr [ebp - 0x78], eax
  0x00077310  addss    xmm6, xmm0
  0x00077314  movss    xmm0, dword ptr [ebp - 0x44]
  0x00077319  mulss    xmm0, xmm2
  0x0007731d  movss    xmm2, dword ptr [ebp - 0x64]
  0x00077322  addss    xmm4, xmm0
  0x00077326  movss    xmm0, dword ptr [ebp - 0x2c]
  0x0007732b  mulss    xmm0, xmm3
  0x0007732f  addss    xmm4, xmm0
  0x00077333  movss    xmm0, dword ptr [ebp - 0x34]
  0x00077338  mulss    xmm0, xmm5
  0x0007733c  movq     xmm5, qword ptr [ebp - 8]
  0x00077341  mulss    xmm5, xmm2
  0x00077345  addss    xmm1, xmm0
  0x00077349  unpcklps xmm6, xmm4
  0x0007734c  movaps   xmm0, xmm7
  0x0007734f  movq     qword ptr [ebp - 0x74], xmm6
  0x00077354  mulss    xmm0, xmm3
  0x00077358  addss    xmm1, xmm0
  0x0007735c  movss    xmm0, dword ptr [ebp - 0x68]
  0x00077361  movss    dword ptr [ebp - 0x10], xmm1
  0x00077366  movss    xmm1, dword ptr [ebp - 0x48]
  0x0007736b  mov      eax, dword ptr [ebp - 0x10]
  0x0007736e  mulss    xmm1, xmm0
  0x00077372  mov      dword ptr [ebp - 0x6c], eax
  0x00077375  addss    xmm5, xmm1
  0x00077379  movss    xmm1, dword ptr [ebp - 0x60]
  0x0007737e  movss    xmm3, dword ptr [ebp - 0x30]
  0x00077383  movss    xmm4, dword ptr [ebp - 0x38]
  0x00077388  mulss    xmm3, xmm1
  0x0007738c  mov      esi, dword ptr [ebx]
  0x0007738e  mulss    xmm4, xmm2
  0x00077392  mulss    xmm7, xmm1
  0x00077396  addss    xmm5, xmm3
  0x0007739a  movss    xmm3, dword ptr [ebp - 0x44]
  0x0007739f  mulss    xmm3, xmm0
  0x000773a3  addss    xmm4, xmm3
  0x000773a7  movss    xmm3, dword ptr [ebp - 0x2c]
  0x000773ac  mulss    xmm3, xmm1
  0x000773b0  addss    xmm4, xmm3
  0x000773b4  movss    xmm3, dword ptr [ebp - 0x40]
  0x000773b9  mulss    xmm3, xmm0
  0x000773bd  movss    xmm0, dword ptr [ebp - 0x34]
  0x000773c2  mulss    xmm0, xmm2
  0x000773c6  unpcklps xmm5, xmm4
  0x000773c9  movq     qword ptr [ebp - 0x68], xmm5
  0x000773ce  addss    xmm3, xmm0
  0x000773d2  addss    xmm3, xmm7
  0x000773d6  movss    dword ptr [ebp - 0x10], xmm3
  0x000773db  mov      eax, dword ptr [ebp - 0x10]
  0x000773de  mov      dword ptr [ebp - 0x60], eax
  0x000773e1  test     esi, esi
  0x000773e3  je       0x10077515
  0x000773e9  mov      eax, dword ptr [esi]
  0x000773eb  mov      ecx, esi
  0x000773ed  call     dword ptr [eax]
  0x000773ef  cmp      eax, 0x107ff5a0
  0x000773f4  je       0x1007741b
  0x000773f6  mov      ecx, dword ptr [eax + 8]
  0x000773f9  test     ecx, ecx
  0x000773fb  je       0x10077515
  0x00077401  cmp      ecx, 0x107ff5a0
  0x00077407  je       0x1007741b
  0x00077409  push     0x107ff5a0
  0x0007740e  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
  0x00077413  test     al, al
  0x00077415  je       0x10077515
  0x0007741b  mov      ecx, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x00077421  call     0x10268ad0   ; -> ?GetMainPlayer@GameEngine@GAME@@QBEPAVPlayer@2@XZ
  0x00077426  cmp      esi, eax
  0x00077428  jne      0x10077515
  0x0007742e  mov      ecx, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x00077434  lea      eax, [ebp - 0xc4]
  0x0007743a  push     eax
  0x0007743b  lea      ecx, [ecx + 0xc84]
  0x00077441  call     dword ptr [0x104e5778]   ; f32=1.16686e-38 i32=8326984 f64=2.76448e-306
  0x00077447  movss    xmm5, dword ptr [ebp - 0x9c]
  0x0007744f  movss    xmm4, dword ptr [ebp - 0x98]
  0x00077457  movss    xmm6, dword ptr [ebp - 0x48]
  0x0007745c  movss    xmm0, dword ptr [ebp - 0x3c]
  0x00077461  movss    xmm2, dword ptr [ebp - 0x94]
  0x00077469  movss    xmm3, dword ptr [ebp - 0x44]
  0x0007746e  mulss    xmm0, xmm4
  0x00077472  mov      ecx, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x00077478  mulss    xmm6, xmm5
  0x0007747c  add      ecx, 0xc84
  0x00077482  push     ecx
  0x00077483  movss    xmm1, dword ptr [ebp - 0x40]
  0x00077488  mulss    xmm3, xmm5
  0x0007748c  addss    xmm6, xmm0
  0x00077490  mulss    xmm1, xmm5
  0x00077494  movss    xmm0, dword ptr [ebp - 0x30]
  0x00077499  mulss    xmm0, xmm2
  0x0007749d  addss    xmm6, xmm0
  0x000774a1  movss    xmm0, dword ptr [ebp - 0x38]
  0x000774a6  mulss    xmm0, xmm4
  0x000774aa  addss    xmm3, xmm0
  0x000774ae  movss    xmm0, dword ptr [ebp - 0x2c]
  0x000774b3  mulss    xmm0, xmm2
  0x000774b7  addss    xmm3, xmm0
  0x000774bb  movss    xmm0, dword ptr [ebp - 0x34]
  0x000774c0  mulss    xmm0, xmm4
  0x000774c4  addss    xmm1, xmm0
  0x000774c8  unpcklps xmm6, xmm3
  0x000774cb  movss    xmm0, dword ptr [ebp - 0x28]
  0x000774d0  mulss    xmm0, xmm2
  0x000774d4  movq     qword ptr [ebp - 0xc], xmm6
  0x000774d9  fld      dword ptr [ebp - 0xc]
  0x000774dc  addss    xmm1, xmm0
  0x000774e0  movq     qword ptr [ebp - 0x9c], xmm6
  0x000774e8  movss    dword ptr [ebp - 4], xmm1
  0x000774ed  fld      dword ptr [ebp - 4]
  0x000774f0  fpatan   
  0x000774f2  mov      eax, dword ptr [ebp - 4]
  0x000774f5  mov      dword ptr [ebp - 0x94], eax
  0x000774fb  mov      eax, dword ptr [ecx]
  0x000774fd  fstp     dword ptr [ebp - 4]
  0x00077500  movss    xmm0, dword ptr [ebp - 4]
  0x00077505  subss    xmm0, dword ptr [0x105f5874]   ; f32=3.14159 i32=1078530011 f64=512
  0x0007750d  movss    dword ptr [esp], xmm0
  0x00077512  call     dword ptr [eax + 8]
  0x00077515  movups   xmm0, xmmword ptr [ebp - 0x58]
  0x00077519  lea      eax, [ebp - 0x90]
  0x0007751f  push     eax
  0x00077520  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x00077525  push     dword ptr [ebx]
  0x00077527  movups   xmmword ptr [ebx + 0x14], xmm0
  0x0007752b  mov      ecx, dword ptr [eax]
  0x0007752d  mov      ecx, dword ptr [ecx + 0x28]
  0x00077530  call     dword ptr [0x104e55d4]   ; f32=1.16602e-38 i32=8320998 f64=2.75636e-306
  0x00077536  cmp      byte ptr [ebx + 0x40], 0
  0x0007753a  je       0x1007754c
  0x0007753c  push     dword ptr [ebx]
  0x0007753e  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x00077544  mov      ecx, eax
  0x00077546  call     dword ptr [0x104e57ac]   ; f32=1.16696e-38 i32=8327712 f64=2.76546e-306
  0x0007754c  mov      ecx, ebx
  0x0007754e  mov      byte ptr [ebx + 0x24], 0
  0x00077552  call     0x100771a0   ; -> ?MoveToNextWaypoint@CharacterMovementManager@GAME@@AAE_NXZ
  0x00077557  pop      esi
  0x00077558  pop      ebx
  0x00077559  mov      esp, ebp
  0x0007755b  pop      ebp
  0x0007755c  ret      
  0x0007755d  test     eax, eax
  0x0007755f  jne      0x100775e5
  0x00077565  mov      esi, dword ptr [0x104e56c4]   ; f32=1.16652e-38 i32=8324584 f64=2.76122e-306
  0x0007756b  lea      eax, [ebp - 0x18]
  0x0007756e  push     eax
  0x0007756f  lea      ecx, [ebp - 0x58]
  0x00077572  call     esi
  0x00077574  push     eax
  0x00077575  push     dword ptr [ebx]
  0x00077577  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x0007757d  mov      ecx, eax
  0x0007757f  call     dword ptr [0x104e577c]   ; f32=1.16687e-38 i32=8327038 f64=2.76456e-306
  0x00077585  test     al, al
  0x00077587  je       0x100775e5
  0x00077589  mov      ecx, dword ptr [ebx]
  0x0007758b  lea      eax, [ebp - 0xc4]
  0x00077591  push     edi
  0x00077592  push     eax
  0x00077593  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x00077599  lea      ecx, [ebp - 0x58]
  0x0007759c  movups   xmm0, xmmword ptr [eax]
  0x0007759f  lea      eax, [ebp - 0x18]
  0x000775a2  push     eax
  0x000775a3  movups   xmmword ptr [ebx + 4], xmm0
  0x000775a7  call     esi
  0x000775a9  lea      ecx, [ebx + 4]
  0x000775ac  movq     xmm0, qword ptr [eax]
  0x000775b0  movq     qword ptr [ebp - 0xc], xmm0
  0x000775b5  mov      eax, dword ptr [eax + 8]
  0x000775b8  mov      dword ptr [ebp - 4], eax
  0x000775bb  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x000775c1  push     eax
  0x000775c2  lea      eax, [ebp - 0xc]
  0x000775c5  push     eax
  0x000775c6  lea      ecx, [ebx + 0x14]
  0x000775c9  call     dword ptr [0x104e56d8]   ; f32=1.16655e-38 i32=8324784 f64=2.76151e-306
  0x000775cf  lea      ecx, [ebx + 0x14]
  0x000775d2  call     dword ptr [0x104e55d0]   ; f32=1.16601e-38 i32=8320960 f64=2.75627e-306
  0x000775d8  pop      edi
  0x000775d9  pop      esi
  0x000775da  mov      byte ptr [ebx + 0x24], 1
  0x000775de  mov      al, 1
  0x000775e0  pop      ebx
  0x000775e1  mov      esp, ebp
  0x000775e3  pop      ebp
  0x000775e4  ret      
  0x000775e5  pop      esi
  0x000775e6  xor      al, al
  0x000775e8  pop      ebx
  0x000775e9  mov      esp, ebp
  0x000775eb  pop      ebp
  0x000775ec  ret      
  0x000775ed  int3     
  0x000775ee  int3     
  0x000775ef  int3     
