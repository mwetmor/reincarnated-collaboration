=== 80-MoveToAction-Execute RVA 0x0006c600 sym=?Execute@MoveToAction@GAME@@UAEXXZ ===
  0x0006c600  push     ebp
  0x0006c601  mov      ebp, esp
  0x0006c603  sub      esp, 0x38
  0x0006c606  push     ebx
  0x0006c607  push     esi
  0x0006c608  mov      esi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0006c60e  mov      ebx, ecx
  0x0006c610  push     edi
  0x0006c611  push     dword ptr [ebx + 4]
  0x0006c614  call     esi
  0x0006c616  mov      ecx, eax
  0x0006c618  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x0006c61d  mov      edi, eax
  0x0006c61f  test     edi, edi
  0x0006c621  je       0x1006c654
  0x0006c623  mov      eax, dword ptr [edi]
  0x0006c625  mov      ecx, edi
  0x0006c627  mov      eax, dword ptr [eax + 0x22c]
  0x0006c62d  call     eax
  0x0006c62f  test     al, al
  0x0006c631  je       0x1006c654
  0x0006c633  lea      eax, [ebp - 0x38]
  0x0006c636  mov      ecx, edi
  0x0006c638  push     eax
  0x0006c639  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0006c63f  mov      ecx, eax
  0x0006c641  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0006c647  test     eax, eax
  0x0006c649  je       0x1006c654
  0x0006c64b  cmp      byte ptr [edi + 0x1cb7], 0
  0x0006c652  je       0x1006c662
  0x0006c654  mov      eax, dword ptr [ebx]
  0x0006c656  mov      ecx, ebx
  0x0006c658  call     dword ptr [eax + 0xc]
  0x0006c65b  pop      edi
  0x0006c65c  pop      esi
  0x0006c65d  pop      ebx
  0x0006c65e  mov      esp, ebp
  0x0006c660  pop      ebp
  0x0006c661  ret      
  0x0006c662  push     dword ptr [edi + 0x1120]
  0x0006c668  call     esi
  0x0006c66a  mov      ecx, eax
  0x0006c66c  call     0x10062320   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x230
  0x0006c671  test     eax, eax
  0x0006c673  je       0x1006c67f
  0x0006c675  mov      edx, dword ptr [eax]
  0x0006c677  mov      ecx, eax
  0x0006c679  push     dword ptr [ebx + 0x54]
  0x0006c67c  call     dword ptr [edx + 0x30]
  0x0006c67f  lea      esi, [ebx + 0x34]
  0x0006c682  mov      ecx, edi
  0x0006c684  push     esi
  0x0006c685  lea      eax, [ebp - 0x38]
  0x0006c688  push     eax
  0x0006c689  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0006c68f  push     eax
  0x0006c690  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0006c695  mov      ecx, dword ptr [eax]
  0x0006c697  mov      ecx, dword ptr [ecx + 0x28]
  0x0006c69a  call     dword ptr [0x104e5500]   ; f32=1.16563e-38 i32=8318234 f64=2.7526e-306
  0x0006c6a0  fstp     dword ptr [ebp - 4]
  0x0006c6a3  movss    xmm0, dword ptr [ebp - 4]
  0x0006c6a8  comiss   xmm0, dword ptr [0x105f58e8]   ; f32=100 i32=1120403456 f64=1.54811e+15
  0x0006c6af  jbe      0x1006c6b9
  0x0006c6b1  push     esi
  0x0006c6b2  mov      ecx, edi
  0x0006c6b4  call     0x10048d20   ; -> ?SetPathPosition@Character@GAME@@QAEXABVWorldVec3@2@@Z
  0x0006c6b9  lea      ecx, [edi + 0x600]
  0x0006c6bf  call     0x1043ea00   ; -> ?StopCurrentSkill@SkillManager@GAME@@QAEXXZ
  0x0006c6c4  push     dword ptr [ebx + 0x58]
  0x0006c6c7  lea      esi, [ebx + 0x44]
  0x0006c6ca  mov      ecx, edi
  0x0006c6cc  push     esi
  0x0006c6cd  push     dword ptr [ebx + 0x54]
  0x0006c6d0  call     0x10049770   ; -> ?SetCurrentAttackTarget@Character@GAME@@QAEXIABVWorldVec3@2@H@Z
  0x0006c6d5  mov      eax, dword ptr [ebx]
  0x0006c6d7  movss    xmm0, dword ptr [ebx + 0x5c]
  0x0006c6dc  push     ecx
  0x0006c6dd  movss    dword ptr [esp], xmm0
  0x0006c6e2  mov      ecx, ebx
  0x0006c6e4  push     dword ptr [ebx + 0x60]
  0x0006c6e7  mov      eax, dword ptr [eax + 0x34]
  0x0006c6ea  call     eax
  0x0006c6ec  push     ecx
  0x0006c6ed  fstp     dword ptr [esp]
  0x0006c6f0  push     esi
  0x0006c6f1  mov      ecx, edi
  0x0006c6f3  call     0x1004a670   ; -> ?MoveTo@Character@GAME@@QAEXABVWorldVec3@2@MW4AnimationSet_Type@2@M@Z
  0x0006c6f8  push     dword ptr [ebx + 0x58]
  0x0006c6fb  lea      ecx, [edi + 0x600]
  0x0006c701  call     0x1043c8b0   ; -> ?GetSkillIdFromReference@SkillManager@GAME@@QBE?BII@Z
  0x0006c706  push     eax
  0x0006c707  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0006c70d  mov      ecx, eax
  0x0006c70f  call     0x100629c0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x8d0
  0x0006c714  mov      ecx, eax
  0x0006c716  test     ecx, ecx
  0x0006c718  je       0x1006c73c
  0x0006c71a  mov      eax, dword ptr [ecx]
  0x0006c71c  push     dword ptr [edi + 0x60c]
  0x0006c722  mov      eax, dword ptr [eax + 0x358]
  0x0006c728  call     eax
  0x0006c72a  test     al, al
  0x0006c72c  je       0x1006c73c
  0x0006c72e  mov      ecx, edi
  0x0006c730  mov      byte ptr [edi + 0x1cbb], 1
  0x0006c737  call     0x10054470   ; -> ?ForceSpeedUpdate@Character@GAME@@QAEXXZ
  0x0006c73c  mov      eax, dword ptr [edi]
  0x0006c73e  mov      ecx, edi
  0x0006c740  call     dword ptr [eax + 0x228]
  0x0006c746  cmp      eax, 5
  0x0006c749  jne      0x1006c752
  0x0006c74b  mov      ecx, edi
  0x0006c74d  call     0x100482a0   ; -> ?PlayLoopingRunningSound@Character@GAME@@QAEXXZ
  0x0006c752  pop      edi
  0x0006c753  pop      esi
  0x0006c754  pop      ebx
  0x0006c755  mov      esp, ebp
  0x0006c757  pop      ebp
  0x0006c758  ret      
  0x0006c759  int3     
  0x0006c75a  int3     
  0x0006c75b  int3     
  0x0006c75c  int3     
  0x0006c75d  int3     
  0x0006c75e  int3     
  0x0006c75f  int3     
