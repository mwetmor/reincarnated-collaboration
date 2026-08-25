=== 95-Character-CrowdAgentReachedGoal RVA 0x00052bc0 sym=?CrowdAgentReachedGoal@Character@GAME@@UAEXABUCrowdAgentData@CROWD@@@Z ===
  0x00052bc0  push     esi
  0x00052bc1  push     edi
  0x00052bc2  mov      edi, ecx
  0x00052bc4  mov      eax, dword ptr [edi - 0x28]
  0x00052bc7  lea      ecx, [edi - 0x28]
  0x00052bca  call     dword ptr [eax + 0x228]
  0x00052bd0  cmp      eax, 5
  0x00052bd3  je       0x10052c08
  0x00052bd5  mov      eax, dword ptr [edi - 0x28]
  0x00052bd8  lea      ecx, [edi - 0x28]
  0x00052bdb  call     dword ptr [eax + 0x228]
  0x00052be1  cmp      eax, 6
  0x00052be4  je       0x10052c08
  0x00052be6  mov      eax, dword ptr [edi - 0x28]
  0x00052be9  lea      ecx, [edi - 0x28]
  0x00052bec  call     dword ptr [eax + 0x228]
  0x00052bf2  cmp      eax, 0x13
  0x00052bf5  je       0x10052c08
  0x00052bf7  mov      eax, dword ptr [edi - 0x28]
  0x00052bfa  lea      ecx, [edi - 0x28]
  0x00052bfd  call     dword ptr [eax + 0x228]
  0x00052c03  cmp      eax, 0x15
  0x00052c06  jne      0x10052c36
  0x00052c08  mov      eax, dword ptr [edi - 0x28]
  0x00052c0b  lea      ecx, [edi - 0x28]
  0x00052c0e  call     dword ptr [eax + 0x228]
  0x00052c14  cmp      eax, 0x13
  0x00052c17  je       0x10052c36
  0x00052c19  mov      eax, dword ptr [edi - 0x28]
  0x00052c1c  lea      ecx, [edi - 0x28]
  0x00052c1f  call     dword ptr [eax + 0x228]
  0x00052c25  cmp      eax, 0x15
  0x00052c28  je       0x10052c36
  0x00052c2a  mov      eax, dword ptr [edi - 0x28]
  0x00052c2d  lea      ecx, [edi - 0x28]
  0x00052c30  call     dword ptr [eax + 0x414]
  0x00052c36  mov      eax, dword ptr [edi + 0x928]
  0x00052c3c  mov      byte ptr [eax + 0x24], 0
  0x00052c40  push     dword ptr [edi + 0x10f8]
  0x00052c46  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x00052c4c  mov      ecx, eax
  0x00052c4e  call     0x10062320   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x230
  0x00052c53  test     eax, eax
  0x00052c55  je       0x10052c5e
  0x00052c57  mov      edx, dword ptr [eax]
  0x00052c59  mov      ecx, eax
  0x00052c5b  call     dword ptr [edx + 0x40]
  0x00052c5e  push     9
  0x00052c60  lea      ecx, [edi + 0x301c]
  0x00052c66  call     dword ptr [0x104e56dc]   ; f32=1.16656e-38 i32=8324854 f64=2.76157e-306
  0x00052c6c  pop      edi
  0x00052c6d  pop      esi
  0x00052c6e  ret      4
  0x00052c71  int3     
  0x00052c72  int3     
  0x00052c73  int3     
  0x00052c74  int3     
  0x00052c75  int3     
  0x00052c76  int3     
  0x00052c77  int3     
  0x00052c78  int3     
  0x00052c79  int3     
  0x00052c7a  int3     
  0x00052c7b  int3     
  0x00052c7c  int3     
  0x00052c7d  int3     
  0x00052c7e  int3     
  0x00052c7f  int3     
