=== 22-ControllerCombat-Update  RVA 0x000eea10  sym=?Update@ControllerCombat@GAME@@UAEXH@Z ===
  0x000eea10  push     ebp
  0x000eea11  mov      ebp, esp
  0x000eea13  push     ecx
  0x000eea14  push     esi
  0x000eea15  push     edi
  0x000eea16  push     dword ptr [ebp + 8]
  0x000eea19  mov      edi, ecx
  0x000eea1b  call     0x100ecf50   ; -> ?Update@ControllerCharacter@GAME@@UAEXH@Z
  0x000eea20  push     dword ptr [edi + 0x24]
  0x000eea23  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000eea29  mov      ecx, eax
  0x000eea2b  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x000eea30  mov      esi, eax
  0x000eea32  test     esi, esi
  0x000eea34  je       0x100eea9a
  0x000eea36  mov      edx, dword ptr [esi]
  0x000eea38  mov      ecx, esi
  0x000eea3a  mov      edx, dword ptr [edx + 0x22c]
  0x000eea40  call     edx
  0x000eea42  test     al, al
  0x000eea44  je       0x100eea9a
  0x000eea46  mov      eax, dword ptr [esi]
  0x000eea48  mov      ecx, esi
  0x000eea4a  mov      eax, dword ptr [eax + 0x418]
  0x000eea50  call     eax
  0x000eea52  test     al, al
  0x000eea54  jne      0x100eea9a
  0x000eea56  movsd    xmm0, qword ptr [esi + 0xa38]
  0x000eea5e  maxsd    xmm0, qword ptr [0x105f5710]   ; f32=0 i32=0 f64=0
  0x000eea66  mov      eax, dword ptr [esi]
  0x000eea68  push     ecx
  0x000eea69  mov      ecx, esi
  0x000eea6b  cvtpd2ps xmm0, xmm0
  0x000eea6f  movss    dword ptr [ebp + 8], xmm0
  0x000eea74  movss    dword ptr [esp], xmm0
  0x000eea79  call     dword ptr [eax + 0x270]
  0x000eea7f  xorps    xmm0, xmm0
  0x000eea82  comiss   xmm0, dword ptr [ebp + 8]
  0x000eea86  jb       0x100eea9a
  0x000eea88  mov      edx, dword ptr [edi]
  0x000eea8a  mov      ecx, edi
  0x000eea8c  movzx    eax, byte ptr [esi + 0x1d8c]
  0x000eea93  push     eax
  0x000eea94  call     dword ptr [edx + 0x88]
  0x000eea9a  pop      edi
  0x000eea9b  pop      esi
  0x000eea9c  pop      ecx
  0x000eea9d  pop      ebp
  0x000eea9e  ret      4
  0x000eeaa1  int3     
  0x000eeaa2  int3     
  0x000eeaa3  int3     
  0x000eeaa4  int3     
  0x000eeaa5  int3     
  0x000eeaa6  int3     
  0x000eeaa7  int3     
  0x000eeaa8  int3     
  0x000eeaa9  int3     
  0x000eeaaa  int3     
  0x000eeaab  int3     
  0x000eeaac  int3     
  0x000eeaad  int3     
  0x000eeaae  int3     
  0x000eeaaf  int3     
