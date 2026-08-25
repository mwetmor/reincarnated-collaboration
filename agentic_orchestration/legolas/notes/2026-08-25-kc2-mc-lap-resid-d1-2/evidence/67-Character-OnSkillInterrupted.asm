=== 67-Character-OnSkillInterrupted RVA 0x0005d970 sym=?OnSkillInterrupted@Character@GAME@@UAEXXZ ===
  0x0005d970  push     ebx
  0x0005d971  push     esi
  0x0005d972  mov      esi, ecx
  0x0005d974  push     edi
  0x0005d975  mov      edi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0005d97b  cmp      byte ptr [esi + 0x30cc], 0
  0x0005d982  je       0x1005d9c4
  0x0005d984  lea      ecx, [esi + 0x434]
  0x0005d98a  call     0x102112e0   ; -> ?GetWeaponIdRight@EquipManager@GAME@@QBEIXZ
  0x0005d98f  mov      ebx, eax
  0x0005d991  push     ebx
  0x0005d992  call     edi
  0x0005d994  mov      ecx, eax
  0x0005d996  call     0x10062290   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1a0
  0x0005d99b  test     eax, eax
  0x0005d99d  je       0x1005d9bd
  0x0005d99f  test     ebx, ebx
  0x0005d9a1  je       0x1005d9bd
  0x0005d9a3  push     ebx
  0x0005d9a4  call     edi
  0x0005d9a6  mov      ecx, eax
  0x0005d9a8  call     0x10062290   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1a0
  0x0005d9ad  test     eax, eax
  0x0005d9af  je       0x1005d9bd
  0x0005d9b1  mov      edx, dword ptr [eax]
  0x0005d9b3  mov      ecx, eax
  0x0005d9b5  push     1
  0x0005d9b7  call     dword ptr [edx + 0xfc]
  0x0005d9bd  mov      byte ptr [esi + 0x30cc], 0
  0x0005d9c4  cmp      byte ptr [esi + 0x30cd], 0
  0x0005d9cb  je       0x1005da0d
  0x0005d9cd  lea      ecx, [esi + 0x434]
  0x0005d9d3  call     0x10211360   ; -> ?GetWeaponIdLeft@EquipManager@GAME@@QBEIXZ
  0x0005d9d8  mov      ebx, eax
  0x0005d9da  push     ebx
  0x0005d9db  call     edi
  0x0005d9dd  mov      ecx, eax
  0x0005d9df  call     0x10062290   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1a0
  0x0005d9e4  test     eax, eax
  0x0005d9e6  je       0x1005da06
  0x0005d9e8  test     ebx, ebx
  0x0005d9ea  je       0x1005da06
  0x0005d9ec  push     ebx
  0x0005d9ed  call     edi
  0x0005d9ef  mov      ecx, eax
  0x0005d9f1  call     0x10062290   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1a0
  0x0005d9f6  test     eax, eax
  0x0005d9f8  je       0x1005da06
  0x0005d9fa  mov      edx, dword ptr [eax]
  0x0005d9fc  mov      ecx, eax
  0x0005d9fe  push     1
  0x0005da00  call     dword ptr [edx + 0xfc]
  0x0005da06  mov      byte ptr [esi + 0x30cd], 0
  0x0005da0d  pop      edi
  0x0005da0e  pop      esi
  0x0005da0f  pop      ebx
  0x0005da10  ret      
  0x0005da11  int3     
  0x0005da12  int3     
  0x0005da13  int3     
  0x0005da14  int3     
  0x0005da15  int3     
  0x0005da16  int3     
  0x0005da17  int3     
  0x0005da18  int3     
  0x0005da19  int3     
  0x0005da1a  int3     
  0x0005da1b  int3     
  0x0005da1c  int3     
  0x0005da1d  int3     
  0x0005da1e  int3     
  0x0005da1f  int3     
