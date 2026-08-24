; CombatAttribute::SetSkillSource -> this[0x18] (the fallback key)
; Game.dll RVA 0x000d70e0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x000d70e0  push     ebp
  0x000d70e1  mov      ebp, esp
  0x000d70e3  mov      eax, dword ptr [ebp + 8]
  0x000d70e6  mov      dword ptr [ecx + 0x18], eax
  0x000d70e9  pop      ebp
  0x000d70ea  ret      4
