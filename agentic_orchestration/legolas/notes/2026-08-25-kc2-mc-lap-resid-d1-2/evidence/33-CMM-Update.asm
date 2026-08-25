=== 33-CMM-Update  RVA 0x000781a0  sym=?Update@CharacterMovementManager@GAME@@QAEXH@Z ===
  0x000781a0  push     ebp
  0x000781a1  mov      ebp, esp
  0x000781a3  sub      esp, 0x34
  0x000781a6  push     esi
  0x000781a7  push     edi
  0x000781a8  mov      edi, ecx
  0x000781aa  mov      esi, dword ptr [edi]
  0x000781ac  mov      ecx, esi
  0x000781ae  mov      eax, dword ptr [esi]
  0x000781b0  call     dword ptr [eax + 0x228]
  0x000781b6  cmp      eax, 5
  0x000781b9  je       0x100781fb
  0x000781bb  mov      eax, dword ptr [esi]
  0x000781bd  mov      ecx, esi
  0x000781bf  call     dword ptr [eax + 0x228]
  0x000781c5  cmp      eax, 6
  0x000781c8  je       0x100781fb
  0x000781ca  mov      eax, dword ptr [esi]
  0x000781cc  mov      ecx, esi
  0x000781ce  call     dword ptr [eax + 0x228]
  0x000781d4  cmp      eax, 0x13
  0x000781d7  je       0x100781fb
  0x000781d9  mov      eax, dword ptr [esi]
  0x000781db  mov      ecx, esi
  0x000781dd  call     dword ptr [eax + 0x228]
  0x000781e3  cmp      eax, 0x15
  0x000781e6  je       0x100781fb
  0x000781e8  mov      ecx, dword ptr [edi]
  0x000781ea  mov      eax, dword ptr [ecx]
  0x000781ec  call     dword ptr [eax + 0x228]
  0x000781f2  cmp      eax, 0x14
  0x000781f5  jne      0x10078292
  0x000781fb  mov      eax, dword ptr [0x108080a4]   ; [?gGameEngine@GAME@@3PAVGameEngine@1@A] f32=0 i32=0 f64=0
  0x00078200  mov      ecx, dword ptr [eax + 0x27f4]
  0x00078206  mov      eax, dword ptr [ecx]
  0x00078208  call     dword ptr [eax + 0xc]
  0x0007820b  test     eax, eax
  0x0007820d  je       0x10078216
  0x0007820f  mov      ecx, dword ptr [edi]
  0x00078211  call     0x10048dc0   ; -> ?UpdatePath@Character@GAME@@QAEXXZ
  0x00078216  mov      eax, dword ptr [ebp + 8]
  0x00078219  sub      dword ptr [edi + 0x3c], eax
  0x0007821c  cmp      dword ptr [edi + 0x3c], 0
  0x00078220  jg       0x10078292
  0x00078222  mov      ecx, dword ptr [edi]
  0x00078224  xor      esi, esi
  0x00078226  mov      eax, dword ptr [ecx]
  0x00078228  call     dword ptr [eax]
  0x0007822a  cmp      eax, 0x107ff5a0
  0x0007822f  je       0x1007824e
  0x00078231  mov      ecx, dword ptr [eax + 8]
  0x00078234  test     ecx, ecx
  0x00078236  je       0x10078253
  0x00078238  cmp      ecx, 0x107ff5a0
  0x0007823e  je       0x1007824e
  0x00078240  push     0x107ff5a0
  0x00078245  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
  0x0007824a  test     al, al
  0x0007824c  je       0x10078253
  0x0007824e  mov      esi, 1
  0x00078253  mov      ecx, dword ptr [edi]
  0x00078255  push     esi
  0x00078256  push     1
  0x00078258  push     ecx
  0x00078259  mov      eax, dword ptr [ecx]
  0x0007825b  mov      dword ptr [esp], 0x40400000
  0x00078262  mov      eax, dword ptr [eax + 0xe0]
  0x00078268  call     eax
  0x0007826a  push     ecx
  0x0007826b  mov      ecx, dword ptr [edi]
  0x0007826d  lea      eax, [ebp - 0x34]
  0x00078270  fstp     dword ptr [esp]
  0x00078273  push     eax
  0x00078274  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0007827a  push     eax
  0x0007827b  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x00078280  mov      ecx, dword ptr [eax]
  0x00078282  mov      ecx, dword ptr [ecx + 0x28]
  0x00078285  call     dword ptr [0x104e5654]   ; f32=1.16629e-38 i32=8322920 f64=2.75899e-306
  0x0007828b  mov      dword ptr [edi + 0x3c], 1
  0x00078292  pop      edi
  0x00078293  pop      esi
  0x00078294  mov      esp, ebp
  0x00078296  pop      ebp
  0x00078297  ret      4
  0x0007829a  int3     
  0x0007829b  int3     
  0x0007829c  int3     
  0x0007829d  int3     
  0x0007829e  int3     
  0x0007829f  int3     
