=== 24-Alert-OnBegin  RVA 0x00109410  sym=?OnBegin@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXXZ ===
  0x00109410  push     0
  0x00109412  push     0
  0x00109414  push     ecx
  0x00109415  mov      ecx, dword ptr [ecx + 4]
  0x00109418  mov      dword ptr [esp], 0x3f800000
  0x0010941f  push     dword ptr [0x104e52b0]   ; f32=1.16458e-38 i32=8310708 f64=2.74234e-306
  0x00109425  push     0x21
  0x00109427  call     0x100e77f0   ; -> ?PlayAnimation@ControllerAI@GAME@@QAEXW4AnimationSet_Type@2@ABVName@2@M_NI@Z
  0x0010942c  ret      
  0x0010942d  int3     
  0x0010942e  int3     
  0x0010942f  int3     
