=== 81-MoveToAction-Finish RVA 0x0006c850 sym=?Finish@MoveToAction@GAME@@UAEXXZ ===
  0x0006c850  push     ebp
  0x0006c851  mov      ebp, esp
  0x0006c853  sub      esp, 0x10
  0x0006c856  push     ebx
  0x0006c857  mov      ebx, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0006c85d  push     esi
  0x0006c85e  push     edi
  0x0006c85f  mov      edi, ecx
  0x0006c861  push     dword ptr [edi + 4]
  0x0006c864  call     ebx
  0x0006c866  mov      ecx, eax
  0x0006c868  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x0006c86d  mov      esi, eax
  0x0006c86f  test     esi, esi
  0x0006c871  je       0x1006c946
  0x0006c877  mov      eax, dword ptr [edi + 0x54]
  0x0006c87a  lea      ecx, [esi + 0x600]
  0x0006c880  push     dword ptr [edi + 0x58]
  0x0006c883  mov      dword ptr [ebp - 4], eax
  0x0006c886  call     0x1043c8b0   ; -> ?GetSkillIdFromReference@SkillManager@GAME@@QBE?BII@Z
  0x0006c88b  push     eax
  0x0006c88c  call     ebx
  0x0006c88e  mov      ecx, eax
  0x0006c890  call     0x100629c0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x8d0
  0x0006c895  test     eax, eax
  0x0006c897  je       0x1006c8ac
  0x0006c899  push     dword ptr [ebp - 4]
  0x0006c89c  mov      edx, dword ptr [eax]
  0x0006c89e  mov      ecx, eax
  0x0006c8a0  push     dword ptr [esi + 0x60c]
  0x0006c8a6  call     dword ptr [edx + 0x35c]
  0x0006c8ac  cmp      byte ptr [esi + 0x1cbb], 0
  0x0006c8b3  je       0x1006c8c3
  0x0006c8b5  mov      ecx, esi
  0x0006c8b7  mov      byte ptr [esi + 0x1cbb], 0
  0x0006c8be  call     0x10054470   ; -> ?ForceSpeedUpdate@Character@GAME@@QAEXXZ
  0x0006c8c3  mov      ebx, dword ptr [esi + 0x1a00]
  0x0006c8c9  test     ebx, ebx
  0x0006c8cb  jne      0x1006c8d7
  0x0006c8cd  mov      ebx, dword ptr [esi + 0x1980]
  0x0006c8d3  test     ebx, ebx
  0x0006c8d5  je       0x1006c8f3
  0x0006c8d7  mov      ecx, ebx
  0x0006c8d9  call     dword ptr [0x104e54fc]   ; f32=1.16563e-38 i32=8318198 f64=2.75252e-306
  0x0006c8df  test     al, al
  0x0006c8e1  je       0x1006c8f3
  0x0006c8e3  push     0
  0x0006c8e5  push     dword ptr [esi + 0x1a5c]
  0x0006c8eb  mov      ecx, ebx
  0x0006c8ed  call     dword ptr [0x104e550c]   ; f32=1.16565e-38 i32=8318388 f64=2.7528e-306
  0x0006c8f3  mov      ebx, dword ptr [esi + 0x950]
  0x0006c8f9  cmp      byte ptr [ebx + 0x40], 0
  0x0006c8fd  je       0x1006c90f
  0x0006c8ff  push     dword ptr [ebx]
  0x0006c901  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x0006c907  mov      ecx, eax
  0x0006c909  call     dword ptr [0x104e57a0]   ; f32=1.16694e-38 i32=8327560 f64=2.76525e-306
  0x0006c90f  mov      byte ptr [ebx + 0x24], 0
  0x0006c913  lea      ecx, [esi + 0x600]
  0x0006c919  push     dword ptr [edi + 0x58]
  0x0006c91c  call     0x1043c8b0   ; -> ?GetSkillIdFromReference@SkillManager@GAME@@QBE?BII@Z
  0x0006c921  test     eax, eax
  0x0006c923  je       0x1006c946
  0x0006c925  lea      eax, [ebp - 0x10]
  0x0006c928  mov      dword ptr [ebp - 0x10], 0
  0x0006c92f  push     eax
  0x0006c930  mov      ecx, esi
  0x0006c932  mov      dword ptr [ebp - 0xc], 0
  0x0006c939  mov      dword ptr [ebp - 8], 0
  0x0006c940  call     dword ptr [0x104e5680]   ; f32=1.16639e-38 i32=8323648 f64=2.75993e-306
  0x0006c946  mov      byte ptr [edi + 0xd], 0
  0x0006c94a  pop      edi
  0x0006c94b  pop      esi
  0x0006c94c  pop      ebx
  0x0006c94d  mov      esp, ebp
  0x0006c94f  pop      ebp
  0x0006c950  ret      
  0x0006c951  int3     
  0x0006c952  int3     
  0x0006c953  int3     
  0x0006c954  int3     
  0x0006c955  int3     
  0x0006c956  int3     
  0x0006c957  int3     
  0x0006c958  int3     
  0x0006c959  int3     
  0x0006c95a  int3     
  0x0006c95b  int3     
  0x0006c95c  int3     
  0x0006c95d  int3     
  0x0006c95e  int3     
  0x0006c95f  int3     
