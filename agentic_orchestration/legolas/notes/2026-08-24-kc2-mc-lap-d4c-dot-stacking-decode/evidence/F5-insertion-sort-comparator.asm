; inlined comparator: comiss on inst+0x00, DESCENDING
; Game.dll RVA 0x0020ef70  (image_base 0x10000000)
; READ-ONLY disassembly, capstone x86-32

  0x0020ef70  push     ebp
  0x0020ef71  mov      ebp, esp
  0x0020ef73  sub      esp, 0x20
  0x0020ef76  push     ebx
  0x0020ef77  push     esi
  0x0020ef78  push     edi
  0x0020ef79  mov      ebx, edx
  0x0020ef7b  mov      edi, ecx
  0x0020ef7d  cmp      edi, ebx
  0x0020ef7f  je       0x1020f00e
  0x0020ef85  lea      edx, [edi + 0x18]
  0x0020ef88  mov      esi, edx
  0x0020ef8a  cmp      esi, ebx
  0x0020ef8c  je       0x1020f00e
  0x0020ef92  movups   xmm1, xmmword ptr [esi]
  0x0020ef95  mov      ecx, esi
  0x0020ef97  movq     xmm2, qword ptr [esi + 0x10]
  0x0020ef9c  comiss   xmm1, dword ptr [edi]
  0x0020ef9f  movups   xmmword ptr [ebp - 0x1c], xmm1
  0x0020efa3  movq     qword ptr [ebp - 0xc], xmm2
  0x0020efa8  jbe      0x1020efd0
  0x0020efaa  mov      eax, esi
  0x0020efac  sub      eax, edi
  0x0020efae  push     eax
  0x0020efaf  push     edi
  0x0020efb0  push     edx
  0x0020efb1  call     dword ptr [0x104e63e4]   ; f32=1.17327e-38 i32=8372762 f64=2.82655e-306
  0x0020efb7  movups   xmm0, xmmword ptr [ebp - 0x1c]
  0x0020efbb  add      esp, 0xc
  0x0020efbe  lea      edx, [edi + 0x18]
  0x0020efc1  movups   xmmword ptr [edi], xmm0
  0x0020efc4  movq     xmm0, qword ptr [ebp - 0xc]
  0x0020efc9  movq     qword ptr [edi + 0x10], xmm0
  0x0020efce  jmp      0x1020f007   ; -> ?CalculateAllocatedMemory@DurationDamageManager@GAME@@QBEIXZ+0x4bc7
  0x0020efd0  comiss   xmm1, dword ptr [esi - 0x18]
  0x0020efd4  lea      eax, [esi - 0x18]
  0x0020efd7  jbe      0x1020efff
  0x0020efd9  nop      dword ptr [eax]
  0x0020efe0  movups   xmm0, xmmword ptr [eax]
  0x0020efe3  movups   xmmword ptr [ecx], xmm0
  0x0020efe6  movq     xmm0, qword ptr [eax + 0x10]
  0x0020efeb  movq     qword ptr [ecx + 0x10], xmm0
  0x0020eff0  mov      ecx, eax
  0x0020eff2  movss    xmm0, dword ptr [eax - 0x18]
  0x0020eff7  sub      eax, 0x18
  0x0020effa  comiss   xmm0, xmm1
  0x0020effd  jb       0x1020efe0
  0x0020efff  movups   xmmword ptr [ecx], xmm1
  0x0020f002  movq     qword ptr [ecx + 0x10], xmm2
  0x0020f007  add      esi, 0x18
  0x0020f00a  cmp      esi, ebx
  0x0020f00c  jne      0x1020ef92
  0x0020f00e  pop      edi
  0x0020f00f  pop      esi
  0x0020f010  pop      ebx
