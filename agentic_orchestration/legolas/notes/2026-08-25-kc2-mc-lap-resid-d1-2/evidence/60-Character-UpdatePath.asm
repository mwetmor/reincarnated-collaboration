=== 60-Character-UpdatePath  RVA 0x00048dc0  sym=?UpdatePath@Character@GAME@@QAEXXZ ===
  0x00048dc0  push     ebp
  0x00048dc1  mov      ebp, esp
  0x00048dc3  push     -1
  0x00048dc5  push     0x104c2bff
  0x00048dca  mov      eax, dword ptr fs:[0]
  0x00048dd0  push     eax
  0x00048dd1  mov      dword ptr fs:[0], esp
  0x00048dd8  sub      esp, 0x30
  0x00048ddb  push     edi
  0x00048ddc  mov      edi, ecx
  0x00048dde  mov      dword ptr [ebp - 0x14], edi
  0x00048de1  mov      eax, dword ptr [edi + 0x1c9c]
  0x00048de7  test     eax, eax
  0x00048de9  je       0x10048fcc
  0x00048def  push     ebx
  0x00048df0  push     esi
  0x00048df1  mov      esi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x00048df7  push     eax
  0x00048df8  call     esi
  0x00048dfa  mov      ecx, eax
  0x00048dfc  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x00048e01  mov      ebx, eax
  0x00048e03  mov      dword ptr [ebp - 0x18], ebx
  0x00048e06  test     ebx, ebx
  0x00048e08  je       0x10048fca
  0x00048e0e  mov      edx, dword ptr [ebx]
  0x00048e10  mov      ecx, ebx
  0x00048e12  mov      edx, dword ptr [edx + 0x30]
  0x00048e15  call     edx
  0x00048e17  test     al, al
  0x00048e19  je       0x10048fca
  0x00048e1f  mov      ecx, ebx
  0x00048e21  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x00048e27  mov      ecx, edi
  0x00048e29  movups   xmm0, xmmword ptr [eax]
  0x00048e2c  lea      eax, [ebp - 0x2c]
  0x00048e2f  push     eax
  0x00048e30  push     dword ptr [edi + 0x1cb0]
  0x00048e36  lea      eax, [ebp - 0x3c]
  0x00048e39  push     dword ptr [edi + 0x1c9c]
  0x00048e3f  movups   xmmword ptr [ebp - 0x2c], xmm0
  0x00048e43  push     eax
  0x00048e44  call     0x10049980   ; -> ?GetMoveToPoint@Character@GAME@@QBE?AVWorldVec3@2@IIABV32@@Z
  0x00048e49  push     dword ptr [edi + 0x1120]
  0x00048e4f  call     esi
  0x00048e51  mov      ecx, eax
  0x00048e53  call     0x10062320   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x230
  0x00048e58  lea      ecx, [ebp - 0x3c]
  0x00048e5b  mov      dword ptr [ebp - 0x10], eax
  0x00048e5e  push     ecx
  0x00048e5f  lea      ecx, [ebp - 0x2c]
  0x00048e62  mov      edx, dword ptr [eax]
  0x00048e64  push     ecx
  0x00048e65  mov      ecx, eax
  0x00048e67  call     dword ptr [edx + 0x60]
  0x00048e6a  lea      ecx, [ebp - 0x3c]
  0x00048e6d  movups   xmm0, xmmword ptr [eax]
  0x00048e70  movups   xmmword ptr [ebp - 0x3c], xmm0
  0x00048e74  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x00048e7a  test     eax, eax
  0x00048e7c  je       0x10048fca
  0x00048e82  mov      ecx, dword ptr [edi + 0x950]
  0x00048e88  lea      eax, [ebp - 0x3c]
  0x00048e8b  push     eax
  0x00048e8c  lea      eax, [ebp - 0x28]
  0x00048e8f  add      ecx, 0x14
  0x00048e92  push     eax
  0x00048e93  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x00048e99  movss    xmm1, dword ptr [eax + 4]
  0x00048e9e  movss    xmm2, dword ptr [eax]
  0x00048ea2  movss    xmm0, dword ptr [eax + 8]
  0x00048ea7  mulss    xmm2, xmm2
  0x00048eab  mulss    xmm1, xmm1
  0x00048eaf  mulss    xmm0, xmm0
  0x00048eb3  addss    xmm2, xmm1
  0x00048eb7  addss    xmm2, xmm0
  0x00048ebb  ucomiss  xmm2, dword ptr [0x105f5708]   ; f32=0 i32=0 f64=0
  0x00048ec2  lahf     
  0x00048ec3  test     ah, 0x44
  0x00048ec6  jnp      0x10048fca
  0x00048ecc  xorps    xmm0, xmm0
  0x00048ecf  sqrtss   xmm0, xmm2
  0x00048ed3  comiss   xmm0, dword ptr [0x105f5808]   ; f32=1 i32=1065353216 f64=5.26354e-315
  0x00048eda  jbe      0x10048fca
  0x00048ee0  push     ecx
  0x00048ee1  lea      eax, [ebp - 0x3c]
  0x00048ee4  mov      dword ptr [esp], 0x3ccccccd
  0x00048eeb  push     eax
  0x00048eec  mov      ecx, edi
  0x00048eee  call     0x10048b20   ; -> ?AlreadyThere@Character@GAME@@QBE_NABVWorldVec3@2@M@Z
  0x00048ef3  test     al, al
  0x00048ef5  jne      0x10048fca
  0x00048efb  mov      ecx, dword ptr [edi + 0x950]
  0x00048f01  lea      eax, [ebp - 0x3c]
  0x00048f04  push     eax
  0x00048f05  call     0x10077f40   ; -> ?MoveTo@CharacterMovementManager@GAME@@QAE_NABVWorldVec3@2@@Z
  0x00048f0a  test     al, al
  0x00048f0c  jne      0x10048f19
  0x00048f0e  push     1
  0x00048f10  push     1
  0x00048f12  mov      ecx, edi
  0x00048f14  call     0x1004a9f0   ; -> ?StopMoving@Character@GAME@@QAEX_N0@Z
  0x00048f19  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x00048f1f  mov      ecx, dword ptr [ecx]
  0x00048f21  call     dword ptr [0x104e5514]   ; f32=1.16567e-38 i32=8318480 f64=2.75291e-306
  0x00048f27  test     al, al
  0x00048f29  je       0x10048fca
  0x00048f2f  push     0x64
  0x00048f31  call     0x104be920   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70
  0x00048f36  mov      ebx, eax
  0x00048f38  add      esp, 4
  0x00048f3b  mov      dword ptr [ebp - 0x1c], ebx
  0x00048f3e  mov      ecx, edi
  0x00048f40  mov      dword ptr [ebp - 4], 0
  0x00048f47  call     0x10046780   ; -> ?GetAnimationSet@Character@GAME@@QBEPAVAnimationSet@2@XZ
  0x00048f4c  mov      ecx, edi
  0x00048f4e  mov      esi, dword ptr [eax + 4]
  0x00048f51  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x00048f57  mov      edi, dword ptr [ebp - 0x10]
  0x00048f5a  push     esi
  0x00048f5b  mov      esi, dword ptr [ebp - 0x14]
  0x00048f5e  mov      ecx, esi
  0x00048f60  movups   xmm0, xmmword ptr [eax]
  0x00048f63  mov      edi, dword ptr [edi + 0x24]
  0x00048f66  push     0
  0x00048f68  movups   xmmword ptr [ebp - 0x2c], xmm0
  0x00048f6c  call     dword ptr [0x104e55f0]   ; f32=1.16608e-38 i32=8321404 f64=2.7569e-306
  0x00048f72  push     ecx
  0x00048f73  mov      ecx, dword ptr [ebp - 0x18]
  0x00048f76  fstp     dword ptr [esp]
  0x00048f79  push     dword ptr [esi + 0x1cb0]
  0x00048f7f  call     dword ptr [0x104e5090]   ; f32=1.16349e-38 i32=8302926 f64=2.73178e-306
  0x00048f85  push     eax
  0x00048f86  lea      eax, [ebp - 0x3c]
  0x00048f89  mov      ecx, ebx
  0x00048f8b  push     eax
  0x00048f8c  lea      eax, [ebp - 0x2c]
  0x00048f8f  push     eax
  0x00048f90  push     edi
  0x00048f91  call     0x1006c550   ; -> ??0MoveToAction@GAME@@QAE@IABVWorldVec3@1@0IIMW4AnimationSet_Type@1@@Z
  0x00048f96  mov      esi, eax
  0x00048f98  mov      dword ptr [ebp - 4], 0xffffffff
  0x00048f9f  mov      ecx, esi
  0x00048fa1  mov      edx, dword ptr [esi]
  0x00048fa3  mov      edx, dword ptr [edx + 0x28]
  0x00048fa6  call     edx
  0x00048fa8  test     al, al
  0x00048faa  je       0x10048fc2
  0x00048fac  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x00048fb2  mov      ecx, dword ptr [ecx]
  0x00048fb4  call     dword ptr [0x104e55f4]   ; f32=1.16608e-38 i32=8321456 f64=2.75697e-306
  0x00048fba  push     esi
  0x00048fbb  mov      ecx, eax
  0x00048fbd  mov      edx, dword ptr [eax]
  0x00048fbf  call     dword ptr [edx + 4]
  0x00048fc2  mov      eax, dword ptr [esi]
  0x00048fc4  mov      ecx, esi
  0x00048fc6  push     1
  0x00048fc8  call     dword ptr [eax]
  0x00048fca  pop      esi
  0x00048fcb  pop      ebx
  0x00048fcc  mov      ecx, dword ptr [ebp - 0xc]
  0x00048fcf  pop      edi
  0x00048fd0  mov      dword ptr fs:[0], ecx
  0x00048fd7  mov      esp, ebp
  0x00048fd9  pop      ebp
  0x00048fda  ret      
  0x00048fdb  int3     
  0x00048fdc  int3     
  0x00048fdd  int3     
  0x00048fde  int3     
  0x00048fdf  int3     
