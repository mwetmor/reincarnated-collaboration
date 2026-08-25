    0x00046e80  push     ebp
    0x00046e81  mov      ebp, esp
    0x00046e83  push     ecx
    0x00046e84  mov      eax, dword ptr [ecx + 0x1b98]
    0x00046e8a  mov      dword ptr [ebp - 4], 0
    0x00046e91  push     esi
    0x00046e92  cmp      eax, 5
    0x00046e95  ja       0x10046f2c
    0x00046e9b  jmp      dword ptr [eax*4 + 0x10046f58]
    0x00046ea2  mov      ecx, dword ptr [ebp + 8]
    0x00046ea5  push     0x104f4fb4
    0x00046eaa  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046eaf  mov      eax, dword ptr [ebp + 8]
    0x00046eb2  pop      esi
    0x00046eb3  mov      esp, ebp
    0x00046eb5  pop      ebp
    0x00046eb6  ret      4
    0x00046eb9  mov      ecx, dword ptr [ebp + 8]
    0x00046ebc  push     0x104f4fc4
    0x00046ec1  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046ec6  mov      eax, dword ptr [ebp + 8]
    0x00046ec9  pop      esi
    0x00046eca  mov      esp, ebp
    0x00046ecc  pop      ebp
    0x00046ecd  ret      4
    0x00046ed0  mov      ecx, dword ptr [ebp + 8]
    0x00046ed3  push     0x104f4fd8
    0x00046ed8  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046edd  mov      eax, dword ptr [ebp + 8]
    0x00046ee0  pop      esi
    0x00046ee1  mov      esp, ebp
    0x00046ee3  pop      ebp
    0x00046ee4  ret      4
    0x00046ee7  mov      ecx, dword ptr [ebp + 8]
    0x00046eea  push     0x104f4fe4
    0x00046eef  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046ef4  mov      eax, dword ptr [ebp + 8]
    0x00046ef7  pop      esi
    0x00046ef8  mov      esp, ebp
    0x00046efa  pop      ebp
    0x00046efb  ret      4
    0x00046efe  mov      ecx, dword ptr [ebp + 8]
    0x00046f01  push     0x104f4ff0
    0x00046f06  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046f0b  mov      eax, dword ptr [ebp + 8]
    0x00046f0e  pop      esi
    0x00046f0f  mov      esp, ebp
    0x00046f11  pop      ebp
    0x00046f12  ret      4
    0x00046f15  mov      ecx, dword ptr [ebp + 8]
    0x00046f18  push     0x104f4ffc
    0x00046f1d  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
    0x00046f22  mov      eax, dword ptr [ebp + 8]
    0x00046f25  pop      esi
    0x00046f26  mov      esp, ebp
    0x00046f28  pop      ebp
    0x00046f29  ret      4
    0x00046f2c  mov      esi, dword ptr [ebp + 8]
    0x00046f2f  mov      ecx, esi
    0x00046f31  push     0xd
    0x00046f33  push     0x104f5010
    0x00046f38  mov      dword ptr [esi + 0x14], 0xf
    0x00046f3f  mov      dword ptr [esi + 0x10], 0
    0x00046f46  mov      byte ptr [esi], 0
    0x00046f49  call     0x10008b80   ; -> ?AddTimeToLive@Skill@GAME@@UAEXH@Z+0x6b0
    0x00046f4e  mov      eax, esi
    0x00046f50  pop      esi
    0x00046f51  mov      esp, ebp
    0x00046f53  pop      ebp
    0x00046f54  ret      4
    0x00046f57  nop      
    0x00046f58  mov      byte ptr [0xb910046e], al
    0x00046f5d  outsb    dx, byte ptr [esi]
    0x00046f5e  add      al, 0x10
    0x00046f60  shr      byte ptr [esi + 4], 1
    0x00046f63  adc      bh, ah
    0x00046f65  outsb    dx, byte ptr [esi]
    0x00046f66  add      al, 0x10

--- literal string operands referenced in the body ---
  0x00046ea5  0x104f4fb4 -> "Life: Unknown"
  0x00046ebc  0x104f4fc4 -> "Life: Initializing"
  0x00046ed3  0x104f4fd8 -> "Life: Alive"
  0x00046eea  0x104f4fe4 -> "Life: Dying"
  0x00046f01  0x104f4ff0 -> "Life: Dead"
  0x00046f18  0x104f4ffc -> "Life: Respawning"
  0x00046f33  0x104f5010 -> "Life: Illegal"
