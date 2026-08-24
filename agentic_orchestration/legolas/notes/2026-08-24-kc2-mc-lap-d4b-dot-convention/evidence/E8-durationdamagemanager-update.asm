; DurationDamageManager::Update — 100 ms (0x64) DoT tick accumulator
; Game.dll RVA 0x00207f40  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x00207f40  push     ebp
  0x00207f41  mov      ebp, esp
  0x00207f43  push     -1
  0x00207f45  push     0x104cb5c4
  0x00207f4a  mov      eax, dword ptr fs:[0]
  0x00207f50  push     eax
  0x00207f51  mov      dword ptr fs:[0], esp
  0x00207f58  sub      esp, 0x90
  0x00207f5e  push     ebx
  0x00207f5f  mov      ebx, ecx
  0x00207f61  push     esi
  0x00207f62  push     edi
  0x00207f63  mov      dword ptr [ebp - 0x18], ebx
  0x00207f66  mov      esi, dword ptr [ebx + 0x2c]
  0x00207f69  cmp      esi, dword ptr [ebx + 0x30]
  0x00207f6c  je       0x10207fab
  0x00207f6e  mov      eax, dword ptr [ebp + 8]
  0x00207f71  mov      edi, dword ptr [esi + 0x1c]
  0x00207f74  add      edi, eax
  0x00207f76  cmp      edi, 0x64
  0x00207f79  jle      0x10207f99
  0x00207f7b  mov      eax, 0x51eb851f
  0x00207f80  imul     edi
  0x00207f82  sar      edx, 5
  0x00207f85  mov      ecx, edx
  0x00207f87  shr      ecx, 0x1f
  0x00207f8a  add      ecx, edx
  0x00207f8c  imul     eax, ecx, 0x64
  0x00207f8f  mov      dword ptr [esi + 0x20], ecx
  0x00207f92  sub      edi, eax
  0x00207f94  mov      eax, dword ptr [ebp + 8]
  0x00207f97  jmp      0x10207fa0   ; -> ?Update@DurationDamageManager@GAME@@UAEXH@Z+0x60
  0x00207f99  mov      dword ptr [esi + 0x20], 0
  0x00207fa0  mov      dword ptr [esi + 0x1c], edi
  0x00207fa3  add      esi, 0x24
  0x00207fa6  cmp      esi, dword ptr [ebx + 0x30]
  0x00207fa9  jne      0x10207f71
  0x00207fab  mov      ecx, dword ptr [ebx + 0x38]
  0x00207fae  cmp      ecx, dword ptr [ebx + 0x3c]
  0x00207fb1  je       0x10207ff0
  0x00207fb3  mov      eax, dword ptr [ebp + 8]
  0x00207fb6  mov      edi, dword ptr [ecx + 0x1c]
  0x00207fb9  add      edi, eax
  0x00207fbb  cmp      edi, 0x64
  0x00207fbe  jle      0x10207fde
  0x00207fc0  mov      eax, 0x51eb851f
  0x00207fc5  imul     edi
  0x00207fc7  sar      edx, 5
  0x00207fca  mov      esi, edx
  0x00207fcc  shr      esi, 0x1f
  0x00207fcf  add      esi, edx
  0x00207fd1  imul     eax, esi, 0x64
  0x00207fd4  mov      dword ptr [ecx + 0x20], esi
  0x00207fd7  sub      edi, eax
  0x00207fd9  mov      eax, dword ptr [ebp + 8]
  0x00207fdc  jmp      0x10207fe5   ; -> ?Update@DurationDamageManager@GAME@@UAEXH@Z+0xa5
  0x00207fde  mov      dword ptr [ecx + 0x20], 0
  0x00207fe5  mov      dword ptr [ecx + 0x1c], edi
  0x00207fe8  add      ecx, 0x24
  0x00207feb  cmp      ecx, dword ptr [ebx + 0x3c]
  0x00207fee  jne      0x10207fb6
  0x00207ff0  mov      eax, dword ptr [ebx]
  0x00207ff2  mov      ecx, ebx
  0x00207ff4  push     0x11
  0x00207ff6  mov      word ptr [ebx + 0x14], 0
  0x00207ffc  mov      eax, dword ptr [eax + 8]
  0x00207fff  call     eax
  0x00208001  mov      eax, dword ptr [ebx]
  0x00208003  mov      ecx, ebx
  0x00208005  fstp     dword ptr [ebp - 0x14]
  0x00208008  push     0x13
  0x0020800a  mov      eax, dword ptr [eax + 8]
  0x0020800d  call     eax
  0x0020800f  movss    xmm0, dword ptr [ebp - 0x14]
  0x00208014  ucomiss  xmm0, dword ptr [ebx + 0xc]
  0x00208018  fstp     dword ptr [ebp - 0x10]
  0x0020801b  lahf     
  0x0020801c  test     ah, 0x44
  0x0020801f  jnp      0x1020802a
  0x00208021  movss    dword ptr [ebx + 0xc], xmm0
