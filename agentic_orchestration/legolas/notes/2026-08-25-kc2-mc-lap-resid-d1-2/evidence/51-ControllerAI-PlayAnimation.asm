=== 51-ControllerAI-PlayAnimation  RVA 0x000e77f0  sym=?PlayAnimation@ControllerAI@GAME@@QAEXW4AnimationSet_Type@2@ABVName@2@M_NI@Z ===
  0x000e77f0  push     ebp
  0x000e77f1  mov      ebp, esp
  0x000e77f3  push     -1
  0x000e77f5  push     0x104c79d8
  0x000e77fa  mov      eax, dword ptr fs:[0]
  0x000e7800  push     eax
  0x000e7801  mov      dword ptr fs:[0], esp
  0x000e7808  push     ecx
  0x000e7809  push     ebx
  0x000e780a  push     esi
  0x000e780b  push     edi
  0x000e780c  push     0x48
  0x000e780e  mov      ebx, ecx
  0x000e7810  call     0x104be920   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70
  0x000e7815  mov      edi, eax
  0x000e7817  add      esp, 4
  0x000e781a  mov      dword ptr [ebp - 0x10], edi
  0x000e781d  mov      dword ptr [ebp - 4], 0
  0x000e7824  mov      ecx, edi
  0x000e7826  mov      esi, dword ptr [ebx + 0x24]
  0x000e7829  push     esi
  0x000e782a  call     dword ptr [0x104e5760]   ; f32=1.16681e-38 i32=8326670 f64=2.76403e-306
  0x000e7830  mov      byte ptr [ebp - 4], 1
  0x000e7834  lea      ecx, [edi + 0x18]
  0x000e7837  mov      dword ptr [edi], 0x105921d4
  0x000e783d  mov      dword ptr [edi + 4], esi
  0x000e7840  mov      dword ptr [edi + 8], 0
  0x000e7847  mov      word ptr [edi + 0xc], 0x100
  0x000e784d  mov      dword ptr [edi + 0x10], 0x437a0000
  0x000e7854  mov      byte ptr [edi + 0x14], 0
  0x000e7858  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000e785e  mov      eax, dword ptr [ebp + 8]
  0x000e7861  mov      ecx, ebx
  0x000e7863  movss    xmm0, dword ptr [ebp + 0x10]
  0x000e7868  mov      dword ptr [edi], 0x10591b48
  0x000e786e  mov      dword ptr [edi + 0x38], 0
  0x000e7875  mov      dword ptr [edi + 0x34], eax
  0x000e7878  mov      eax, dword ptr [ebp + 0xc]
  0x000e787b  push     edi
  0x000e787c  mov      eax, dword ptr [eax]
  0x000e787e  mov      dword ptr [edi + 0x38], eax
  0x000e7881  mov      al, byte ptr [ebp + 0x14]
  0x000e7884  mov      byte ptr [edi + 0x40], al
  0x000e7887  mov      eax, dword ptr [ebp + 0x18]
  0x000e788a  movss    dword ptr [edi + 0x3c], xmm0
  0x000e788f  mov      dword ptr [edi + 0x44], eax
  0x000e7892  mov      dword ptr [edi + 8], 0x12
  0x000e7899  mov      byte ptr [edi + 0xc], 1
  0x000e789d  mov      dword ptr [ebp - 4], 0xffffffff
  0x000e78a4  call     0x100ea480   ; -> ?HandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z
  0x000e78a9  mov      ecx, dword ptr [ebp - 0xc]
  0x000e78ac  pop      edi
  0x000e78ad  pop      esi
  0x000e78ae  pop      ebx
  0x000e78af  mov      dword ptr fs:[0], ecx
  0x000e78b6  mov      esp, ebp
  0x000e78b8  pop      ebp
  0x000e78b9  ret      0x14
  0x000e78bc  int3     
  0x000e78bd  int3     
  0x000e78be  int3     
  0x000e78bf  int3     
