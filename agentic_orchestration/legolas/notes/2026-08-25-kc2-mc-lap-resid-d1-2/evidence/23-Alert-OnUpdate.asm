=== 23-Alert-OnUpdate  RVA 0x00109430  sym=?OnUpdate@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXH@Z ===
  0x00109430  push     ebp
  0x00109431  mov      ebp, esp
  0x00109433  and      esp, 0xfffffff0
  0x00109436  sub      esp, 0x68
  0x00109439  push     esi
  0x0010943a  mov      esi, ecx
  0x0010943c  push     edi
  0x0010943d  mov      ecx, dword ptr [esi + 4]
  0x00109440  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x00109445  push     dword ptr [eax]
  0x00109447  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0010944d  mov      ecx, eax
  0x0010944f  call     0x10034d50   ; -> ?CalculateAllocatedMemory@AuraManager@GAME@@QBEIXZ+0x370
  0x00109454  mov      dword ptr [esp + 0x10], eax
  0x00109458  test     eax, eax
  0x0010945a  je       0x101094d9
  0x0010945c  mov      edx, dword ptr [eax]
  0x0010945e  mov      ecx, eax
  0x00109460  mov      edx, dword ptr [edx + 0x30]
  0x00109463  call     edx
  0x00109465  test     al, al
  0x00109467  je       0x101094d9
  0x00109469  mov      edi, dword ptr [esi + 8]
  0x0010946c  test     edi, edi
  0x0010946e  jne      0x10109488
  0x00109470  mov      eax, dword ptr [esi + 4]
  0x00109473  push     dword ptr [eax + 0x24]
  0x00109476  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0010947c  mov      ecx, eax
  0x0010947e  call     0x1000b0c0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd00
  0x00109483  mov      edi, eax
  0x00109485  mov      dword ptr [esi + 8], edi
  0x00109488  mov      esi, dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0010948e  lea      eax, [esp + 0x3c]
  0x00109492  push     eax
  0x00109493  mov      ecx, edi
  0x00109495  call     esi
  0x00109497  mov      ecx, dword ptr [esp + 0x10]
  0x0010949b  movups   xmm0, xmmword ptr [eax]
  0x0010949e  lea      eax, [esp + 0x3c]
  0x001094a2  push     eax
  0x001094a3  movups   xmmword ptr [esp + 0x24], xmm0
  0x001094a8  call     esi
  0x001094aa  push     eax
  0x001094ab  lea      eax, [esp + 0x24]
  0x001094af  push     eax
  0x001094b0  lea      eax, [esp + 0x1c]
  0x001094b4  push     eax
  0x001094b5  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x001094ba  mov      ecx, dword ptr [eax]
  0x001094bc  mov      ecx, dword ptr [ecx + 0x28]
  0x001094bf  call     dword ptr [0x104e5610]   ; f32=1.16615e-38 i32=8321950 f64=2.75765e-306
  0x001094c5  lea      eax, [esp + 0x20]
  0x001094c9  mov      ecx, edi
  0x001094cb  push     eax
  0x001094cc  lea      eax, [esp + 0x18]
  0x001094d0  push     eax
  0x001094d1  push     dword ptr [ebp + 8]
  0x001094d4  call     0x10049290   ; -> ?RotateTowards@Character@GAME@@QAE_NHABVVec3@2@ABVWorldVec3@2@@Z
  0x001094d9  pop      edi
  0x001094da  pop      esi
  0x001094db  mov      esp, ebp
  0x001094dd  pop      ebp
  0x001094de  ret      4
  0x001094e1  int3     
  0x001094e2  int3     
  0x001094e3  int3     
  0x001094e4  int3     
  0x001094e5  int3     
  0x001094e6  int3     
  0x001094e7  int3     
  0x001094e8  int3     
  0x001094e9  int3     
  0x001094ea  int3     
  0x001094eb  int3     
  0x001094ec  int3     
  0x001094ed  int3     
  0x001094ee  int3     
  0x001094ef  int3     
