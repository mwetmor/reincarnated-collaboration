=== 56-PlayAnimationAction-ctor  RVA 0x00070400  sym=??0PlayAnimationAction@GAME@@QAE@IW4AnimationSet_Type@1@ABVName@1@M_NI@Z ===
  0x00070400  push     ebp
  0x00070401  mov      ebp, esp
  0x00070403  push     -1
  0x00070405  push     0x104c3af9
  0x0007040a  mov      eax, dword ptr fs:[0]
  0x00070410  push     eax
  0x00070411  mov      dword ptr fs:[0], esp
  0x00070418  push     ecx
  0x00070419  push     esi
  0x0007041a  mov      esi, dword ptr [ebp + 8]
  0x0007041d  push     edi
  0x0007041e  mov      edi, ecx
  0x00070420  push     esi
  0x00070421  mov      dword ptr [ebp - 0x10], edi
  0x00070424  call     dword ptr [0x104e5760]   ; f32=1.16681e-38 i32=8326670 f64=2.76403e-306
  0x0007042a  mov      dword ptr [ebp - 4], 0
  0x00070431  lea      ecx, [edi + 0x18]
  0x00070434  mov      dword ptr [edi], 0x105921d4
  0x0007043a  mov      dword ptr [edi + 4], esi
  0x0007043d  mov      dword ptr [edi + 8], 0
  0x00070444  mov      word ptr [edi + 0xc], 0x100
  0x0007044a  mov      dword ptr [edi + 0x10], 0x437a0000
  0x00070451  mov      byte ptr [edi + 0x14], 0
  0x00070455  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x0007045b  mov      eax, dword ptr [ebp + 0xc]
  0x0007045e  movss    xmm0, dword ptr [ebp + 0x14]
  0x00070463  mov      ecx, dword ptr [ebp - 0xc]
  0x00070466  mov      dword ptr [edi], 0x10591b48
  0x0007046c  mov      dword ptr [edi + 0x38], 0
  0x00070473  mov      dword ptr [edi + 0x34], eax
  0x00070476  mov      eax, dword ptr [ebp + 0x10]
  0x00070479  mov      eax, dword ptr [eax]
  0x0007047b  mov      dword ptr [edi + 0x38], eax
  0x0007047e  mov      al, byte ptr [ebp + 0x18]
  0x00070481  mov      byte ptr [edi + 0x40], al
  0x00070484  mov      eax, dword ptr [ebp + 0x1c]
  0x00070487  mov      dword ptr [edi + 0x44], eax
  0x0007048a  mov      eax, edi
  0x0007048c  movss    dword ptr [edi + 0x3c], xmm0
  0x00070491  mov      dword ptr [edi + 8], 0x12
  0x00070498  mov      byte ptr [edi + 0xc], 1
  0x0007049c  pop      edi
  0x0007049d  pop      esi
  0x0007049e  mov      dword ptr fs:[0], ecx
  0x000704a5  mov      esp, ebp
  0x000704a7  pop      ebp
  0x000704a8  ret      0x18
  0x000704ab  int3     
  0x000704ac  int3     
  0x000704ad  int3     
  0x000704ae  int3     
  0x000704af  int3     
