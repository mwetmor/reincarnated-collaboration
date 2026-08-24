; sum of inst+0x04 over the next 10 buckets = the 1-second rate query
; Game.dll RVA 0x0020dbd0  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020dbd0  push     ebp
  0x0020dbd1  mov      ebp, esp
  0x0020dbd3  push     ecx
  0x0020dbd4  push     esi
  0x0020dbd5  mov      esi, dword ptr [ecx + 0x14]
  0x0020dbd8  xorps    xmm1, xmm1
  0x0020dbdb  push     edi
  0x0020dbdc  movss    dword ptr [ebp - 4], xmm1
  0x0020dbe1  mov      edi, 0xa
  0x0020dbe6  mov      ecx, dword ptr [esi]
  0x0020dbe8  cmp      ecx, esi
  0x0020dbea  je       0x1020dc25
  0x0020dbec  nop      dword ptr [eax]
  0x0020dbf0  test     edi, edi
  0x0020dbf2  jle      0x1020dc1c
  0x0020dbf4  mov      eax, dword ptr [ecx + 8]
  0x0020dbf7  mov      edx, dword ptr [ecx + 0xc]
  0x0020dbfa  cmp      eax, edx
  0x0020dbfc  je       0x1020dc11
  0x0020dbfe  nop      
  0x0020dc00  addss    xmm1, dword ptr [eax + 4]
  0x0020dc05  add      eax, 0x18
  0x0020dc08  cmp      eax, edx
  0x0020dc0a  jne      0x1020dc00
  0x0020dc0c  movss    dword ptr [ebp - 4], xmm1
  0x0020dc11  mov      ecx, dword ptr [ecx]
  0x0020dc13  dec      edi
  0x0020dc14  cmp      ecx, esi
  0x0020dc16  jne      0x1020dbf0
  0x0020dc18  test     edi, edi
  0x0020dc1a  jg       0x1020dc25
  0x0020dc1c  fld      dword ptr [ebp - 4]
  0x0020dc1f  pop      edi
  0x0020dc20  pop      esi
  0x0020dc21  mov      esp, ebp
  0x0020dc23  pop      ebp
  0x0020dc24  ret      
  0x0020dc25  fldz     
  0x0020dc27  pop      edi
  0x0020dc28  pop      esi
