; entry dtor: proves TWO std::list members (+0x0c scratch, +0x14 live) and sizeof(entry)=0x24
; Game.dll RVA 0x0020c050  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020c050  push     ebp
  0x0020c051  mov      ebp, esp
  0x0020c053  push     esi
  0x0020c054  push     edi
  0x0020c055  mov      edi, ecx
  0x0020c057  lea      ecx, [edi + 0x14]
  0x0020c05a  mov      dword ptr [edi], 0x105cf034
  0x0020c060  call     0x1020c470   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2030
  0x0020c065  mov      ecx, dword ptr [edi + 0x14]
  0x0020c068  mov      edx, 1
  0x0020c06d  push     0x14
  0x0020c06f  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x0020c074  add      esp, 4
  0x0020c077  lea      ecx, [edi + 0xc]
  0x0020c07a  call     0x1020c470   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x2030
  0x0020c07f  mov      ecx, dword ptr [edi + 0xc]
  0x0020c082  mov      edx, 1
  0x0020c087  push     0x14
  0x0020c089  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x0020c08e  add      esp, 4
  0x0020c091  test     byte ptr [ebp + 8], 1
  0x0020c095  je       0x1020c0a2
  0x0020c097  push     0x24
  0x0020c099  push     edi
  0x0020c09a  call     0x104be818   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36b68
  0x0020c09f  add      esp, 8
  0x0020c0a2  mov      eax, edi
  0x0020c0a4  pop      edi
  0x0020c0a5  pop      esi
  0x0020c0a6  pop      ebp
  0x0020c0a7  ret      4
  0x0020c0aa  int3     
  0x0020c0ab  int3     
  0x0020c0ac  int3     
  0x0020c0ad  int3     
  0x0020c0ae  int3     
  0x0020c0af  int3     
  0x0020c0b0  push     ebp
  0x0020c0b1  mov      ebp, esp
  0x0020c0b3  push     esi
