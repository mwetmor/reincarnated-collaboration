=== ?StopObject@NavManager@GAME@@QAEXPAVEntity@2@@Z @ 0x00127aa0 (?StopObject@NavManager@GAME@@QAEXPAVEntity@2@@Z) ===
  0x00127aa0  push     ebp
  0x00127aa1  mov      ebp, esp
  0x00127aa3  mov      edx, dword ptr [ebp + 8]
  0x00127aa6  lea      eax, [edx + 0x28]
  0x00127aa9  neg      edx
  0x00127aab  sbb      edx, edx
  0x00127aad  and      edx, eax
  0x00127aaf  mov      dword ptr [ebp + 8], edx
  0x00127ab2  mov      ecx, dword ptr [ecx + 8]
  0x00127ab5  mov      ecx, dword ptr [ecx + 4]
  0x00127ab8  pop      ebp
  0x00127ab9  jmp      0x102045c0   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25490
  0x00127abe  int3     
  0x00127abf  int3     

=== ?MoveObject@NavManager@GAME@@QAE_NPAVEntity@2@ABVVec3@2@@Z @ 0x00127a80 (?MoveObject@NavManager@GAME@@QAE_NPAVEntity@2@ABVVec3@2@@Z) ===
  0x00127a80  push     ebp
  0x00127a81  mov      ebp, esp
  0x00127a83  mov      ecx, dword ptr [ecx + 8]
  0x00127a86  mov      edx, dword ptr [ebp + 8]
  0x00127a89  lea      eax, [edx + 0x28]
  0x00127a8c  neg      edx
  0x00127a8e  sbb      edx, edx
  0x00127a90  and      edx, eax
  0x00127a92  mov      dword ptr [ebp + 8], edx
  0x00127a95  mov      ecx, dword ptr [ecx + 4]
  0x00127a98  pop      ebp
  0x00127a99  jmp      0x10204430   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25300
  0x00127a9e  int3     
  0x00127a9f  int3     

=== ?Update@NavManager@GAME@@QAEXH@Z @ 0x00127ac0 (?Update@NavManager@GAME@@QAEXH@Z) ===
  0x00127ac0  push     ebp
  0x00127ac1  mov      ebp, esp
  0x00127ac3  and      esp, 0xfffffff8
  0x00127ac6  push     esi
  0x00127ac7  push     edi
  0x00127ac8  mov      edi, ecx
  0x00127aca  call     0x101a48e0   ; -> ?GetMachineTime@GAME@@YAHXZ
  0x00127acf  mov      ecx, dword ptr [edi + 4]
  0x00127ad2  mov      esi, eax
  0x00127ad4  call     0x100ee630   ; -> ?Create@NavMeshBuilder@GAME@@QAE_NPBVPortal@2@AAPAVNavMesh@2@@Z+0x4640
  0x00127ad9  mov      ecx, dword ptr [edi + 8]
  0x00127adc  push     dword ptr [ebp + 8]
  0x00127adf  mov      ecx, dword ptr [ecx + 4]
  0x00127ae2  call     0x10204650   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25520
  0x00127ae7  call     0x101a48e0   ; -> ?GetMachineTime@GAME@@YAHXZ
  0x00127aec  sub      eax, esi
  0x00127aee  mov      dword ptr [edi + 0x40], eax
  0x00127af1  pop      edi
  0x00127af2  pop      esi
  0x00127af3  mov      esp, ebp
  0x00127af5  pop      ebp
  0x00127af6  ret      4
  0x00127af9  int3     
  0x00127afa  int3     
  0x00127afb  int3     
  0x00127afc  int3     
  0x00127afd  int3     
  0x00127afe  int3     
  0x00127aff  int3     

=== ?RemoveObject@NavManager@GAME@@QAEXPAVEntity@2@@Z @ 0x001279b0 (?RemoveObject@NavManager@GAME@@QAEXPAVEntity@2@@Z) ===
  0x001279b0  push     ebp
  0x001279b1  mov      ebp, esp
  0x001279b3  mov      edx, dword ptr [ebp + 8]
  0x001279b6  lea      eax, [edx + 0x28]
  0x001279b9  neg      edx
  0x001279bb  sbb      edx, edx
  0x001279bd  and      edx, eax
  0x001279bf  mov      dword ptr [ebp + 8], edx
  0x001279c2  mov      ecx, dword ptr [ecx + 8]
  0x001279c5  mov      ecx, dword ptr [ecx + 4]
  0x001279c8  pop      ebp
  0x001279c9  jmp      0x102042a0   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25170
  0x001279ce  int3     
  0x001279cf  int3     

=== 0x2045c0 @ 0x002045c0 (?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25490) ===
  0x002045c0  push     ecx
  0x002045c1  mov      eax, dword ptr [esp + 8]
  0x002045c5  push     esi
  0x002045c6  mov      dword ptr [esp + 0xc], eax
  0x002045ca  mov      esi, ecx
  0x002045cc  lea      eax, [esp + 0xc]
  0x002045d0  push     eax
  0x002045d1  lea      eax, [esp + 8]
  0x002045d5  push     eax
  0x002045d6  lea      ecx, [esi + 0x1c]
  0x002045d9  call     0x10204b70   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25a40
  0x002045de  mov      eax, dword ptr [esp + 4]
  0x002045e2  cmp      eax, dword ptr [esi + 0x20]
  0x002045e5  pop      esi
  0x002045e6  je       0x10204611
  0x002045e8  mov      ecx, dword ptr [eax + 0xc]
  0x002045eb  test     ecx, ecx
  0x002045ed  je       0x10204611
  0x002045ef  movq     xmm0, qword ptr [ecx + 0x40]
  0x002045f4  mov      eax, dword ptr [ecx + 0x48]
  0x002045f7  movq     qword ptr [ecx + 0x70], xmm0
  0x002045fc  mov      dword ptr [ecx + 0x68], 3
  0x00204603  mov      dword ptr [ecx + 0x78], eax
  0x00204606  mov      dword ptr [ecx + 0x64], 0
  0x0020460d  pop      ecx
  0x0020460e  ret      4
  0x00204611  cmp      byte ptr [0x103688c5], 0
  0x00204618  jne      0x10204640
  0x0020461a  push     0x103688c5
  0x0020461f  push     0x137
  0x00204624  push     0x102df5b8
  0x00204629  mov      edx, 0x102df5d0
  0x0020462e  mov      ecx, 0x102df624
  0x00204633  call     0x10218c70   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x39b40
  0x00204638  add      esp, 0xc
  0x0020463b  test     al, al
  0x0020463d  je       0x10204640
  0x0020463f  int3     
  0x00204640  pop      ecx
  0x00204641  ret      4
  0x00204644  int3     
  0x00204645  int3     
  0x00204646  int3     
  0x00204647  int3     
  0x00204648  int3     
  0x00204649  int3     
  0x0020464a  int3     
  0x0020464b  int3     
  0x0020464c  int3     
  0x0020464d  int3     
  0x0020464e  int3     
  0x0020464f  int3     
  0x00204650  push     ecx
  0x00204651  push     ebx
  0x00204652  push     esi
  0x00204653  mov      esi, ecx
  0x00204655  push     edi
  0x00204656  xor      edi, edi
  0x00204658  mov      eax, dword ptr [esi + 0x14]
  0x0020465b  sub      eax, dword ptr [esi + 0x10]
  0x0020465e  sar      eax, 2
  0x00204661  test     eax, eax
  0x00204663  je       0x1020468a
  0x00204665  mov      ebx, dword ptr [esp + 0x14]
  0x00204669  nop      dword ptr [eax]
  0x00204670  mov      ecx, dword ptr [esi + 0x10]
  0x00204673  push     ebx
  0x00204674  mov      ecx, dword ptr [ecx + edi*4]
  0x00204677  call     0x10205a50   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x26920
  0x0020467c  mov      eax, dword ptr [esi + 0x14]
=== 0x204650 @ 0x00204650 (?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x25520) ===
  0x00204650  push     ecx
  0x00204651  push     ebx
  0x00204652  push     esi
  0x00204653  mov      esi, ecx
  0x00204655  push     edi
  0x00204656  xor      edi, edi
  0x00204658  mov      eax, dword ptr [esi + 0x14]
  0x0020465b  sub      eax, dword ptr [esi + 0x10]
  0x0020465e  sar      eax, 2
  0x00204661  test     eax, eax
  0x00204663  je       0x1020468a
  0x00204665  mov      ebx, dword ptr [esp + 0x14]
  0x00204669  nop      dword ptr [eax]
  0x00204670  mov      ecx, dword ptr [esi + 0x10]
  0x00204673  push     ebx
  0x00204674  mov      ecx, dword ptr [ecx + edi*4]
  0x00204677  call     0x10205a50   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x26920
  0x0020467c  mov      eax, dword ptr [esi + 0x14]
  0x0020467f  inc      edi
  0x00204680  sub      eax, dword ptr [esi + 0x10]
  0x00204683  sar      eax, 2
  0x00204686  cmp      edi, eax
  0x00204688  jb       0x10204670
  0x0020468a  mov      eax, dword ptr [esi + 0x68]
  0x0020468d  cmp      eax, dword ptr [esi + 0x6c]
  0x00204690  je       0x102046e5
  0x00204692  push     dword ptr [esi + 0x58]
  0x00204695  call     dword ptr [0x102a2194]
  0x0020469b  mov      eax, dword ptr [esi + 0x68]
  0x0020469e  cmp      eax, dword ptr [esi + 0x6c]
  0x002046a1  je       0x102046dc
  0x002046a3  mov      eax, dword ptr [esi + 0x6c]
  0x002046a6  mov      edi, dword ptr [eax - 4]
  0x002046a9  cmp      dword ptr [edi + 0xc0], 0
  0x002046b0  je       0x102046bb
  0x002046b2  cmp      byte ptr [edi + 0xf4], 0
  0x002046b9  je       0x102046dc
  0x002046bb  mov      ecx, edi
  0x002046bd  call     0x10204080   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x24f50
  0x002046c2  push     0xfc
  0x002046c7  push     edi
  0x002046c8  call     0x1027f0f2   ; -> LZ4_decompress_fast_usingDict+0x5f872
  0x002046cd  add      dword ptr [esi + 0x6c], -4
  0x002046d1  add      esp, 8
  0x002046d4  mov      eax, dword ptr [esi + 0x68]
  0x002046d7  cmp      eax, dword ptr [esi + 0x6c]
  0x002046da  jne      0x102046a3
  0x002046dc  push     dword ptr [esi + 0x58]
  0x002046df  call     dword ptr [0x102a2198]
  0x002046e5  pop      edi
  0x002046e6  pop      esi
  0x002046e7  pop      ebx
  0x002046e8  pop      ecx
  0x002046e9  ret      4
  0x002046ec  int3     
  0x002046ed  int3     
  0x002046ee  int3     
  0x002046ef  int3     
  0x002046f0  push     ebp
  0x002046f1  push     edi
  0x002046f2  mov      edi, dword ptr [esp + 0xc]
  0x002046f6  mov      ebp, ecx
  0x002046f8  mov      eax, dword ptr [edi + 8]
  0x002046fb  sub      eax, dword ptr [edi]
  0x002046fd  mov      edx, dword ptr [ebp + 0x24]
  0x00204700  sar      eax, 2
  0x00204703  cmp      eax, edx
  0x00204705  jae      0x10204722
  0x00204707  cmp      edx, 0x3fffffff
  0x0020470d  jbe      0x1020471a
  0x0020470f  push     0x102d4f24
  0x00204714  call     dword ptr [0x102a22b0]
  0x0020471a  push     edx
  0x0020471b  mov      ecx, edi
  0x0020471d  call     0x101e1f80   ; -> ?UpdateBoundingBox@GridBase@GAME@@UAEXXZ+0x2e50
  0x00204722  mov      eax, dword ptr [ebp + 0x20]
  0x00204725  push     esi
  0x00204726  mov      esi, dword ptr [eax]
  0x00204728  cmp      esi, eax
  0x0020472a  je       0x10204784
  0x0020472c  push     ebx
  0x0020472d  nop      dword ptr [eax]
  0x00204730  mov      eax, dword ptr [edi + 4]
  0x00204733  lea      ebx, [esi + 0xc]
  0x00204736  cmp      ebx, eax
  0x00204738  jae      0x10204760
  0x0020473a  mov      ecx, dword ptr [edi]
  0x0020473c  cmp      ecx, ebx
  0x0020473e  ja       0x10204760
  0x00204740  sub      ebx, ecx
