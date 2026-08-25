=== 21-ControllerAI-Update  RVA 0x000e5b80  sym=?Update@ControllerAI@GAME@@UAEXH@Z ===
  0x000e5b80  push     ebp
  0x000e5b81  mov      ebp, esp
  0x000e5b83  sub      esp, 0x38
  0x000e5b86  push     ebx
  0x000e5b87  push     esi
  0x000e5b88  mov      esi, dword ptr [ebp + 8]
  0x000e5b8b  push     edi
  0x000e5b8c  mov      edi, ecx
  0x000e5b8e  push     esi
  0x000e5b8f  mov      dword ptr [ebp - 0x24], edi
  0x000e5b92  call     0x100eea10   ; -> ?Update@ControllerCombat@GAME@@UAEXH@Z
  0x000e5b97  mov      ecx, edi
  0x000e5b99  call     0x100e8520   ; -> ?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ
  0x000e5b9e  mov      ecx, eax
  0x000e5ba0  mov      edx, dword ptr [eax]
  0x000e5ba2  mov      eax, dword ptr [edx + 0x108]
  0x000e5ba8  call     eax
  0x000e5baa  test     al, al
  0x000e5bac  je       0x100e5c26
  0x000e5bae  nop      
  0x000e5bb0  mov      eax, dword ptr [edi + 0x210]
  0x000e5bb6  mov      eax, dword ptr [eax]
  0x000e5bb8  mov      ecx, dword ptr [eax + 8]
  0x000e5bbb  mov      eax, dword ptr [ecx]
  0x000e5bbd  call     dword ptr [eax + 0x114]
  0x000e5bc3  mov      eax, dword ptr [edi + 0x210]
  0x000e5bc9  push     0
  0x000e5bcb  mov      eax, dword ptr [eax]
  0x000e5bcd  mov      ecx, dword ptr [eax + 8]
  0x000e5bd0  mov      eax, dword ptr [ecx]
  0x000e5bd2  call     dword ptr [eax + 0x10c]
  0x000e5bd8  mov      eax, dword ptr [edi + 0x210]
  0x000e5bde  mov      edx, dword ptr [eax]
  0x000e5be0  push     edx
  0x000e5be1  mov      ecx, dword ptr [edx + 4]
  0x000e5be4  mov      eax, dword ptr [edx]
  0x000e5be6  mov      dword ptr [ecx], eax
  0x000e5be8  mov      ecx, dword ptr [edx]
  0x000e5bea  mov      eax, dword ptr [edx + 4]
  0x000e5bed  mov      dword ptr [ecx + 4], eax
  0x000e5bf0  dec      dword ptr [edi + 0x214]
  0x000e5bf6  call     0x104be91b   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c6b
  0x000e5bfb  add      esp, 4
  0x000e5bfe  mov      ecx, edi
  0x000e5c00  call     0x100e8520   ; -> ?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ
  0x000e5c05  mov      ecx, eax
  0x000e5c07  mov      edx, dword ptr [eax]
  0x000e5c09  call     dword ptr [edx + 0x110]
  0x000e5c0f  mov      ecx, edi
  0x000e5c11  call     0x100e8520   ; -> ?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ
  0x000e5c16  mov      ecx, eax
  0x000e5c18  mov      edx, dword ptr [eax]
  0x000e5c1a  mov      eax, dword ptr [edx + 0x108]
  0x000e5c20  call     eax
  0x000e5c22  test     al, al
  0x000e5c24  jne      0x100e5bb0
  0x000e5c26  cmp      dword ptr [edi + 0x214], 0
  0x000e5c2d  je       0x100e5c3c
  0x000e5c2f  mov      eax, dword ptr [edi + 0x210]
  0x000e5c35  mov      eax, dword ptr [eax]
  0x000e5c37  mov      ecx, dword ptr [eax + 8]
  0x000e5c3a  jmp      0x100e5c42   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0xc2
  0x000e5c3c  mov      ecx, dword ptr [edi + 0x1e4]
  0x000e5c42  mov      eax, dword ptr [ecx]
  0x000e5c44  push     esi
  0x000e5c45  call     dword ptr [eax + 0x118]
  0x000e5c4b  mov      eax, dword ptr [edi + 0x1d8]
  0x000e5c51  test     eax, eax
  0x000e5c53  jle      0x100e5c5d
  0x000e5c55  sub      eax, esi
  0x000e5c57  mov      dword ptr [edi + 0x1d8], eax
  0x000e5c5d  mov      esi, dword ptr [edi + 0x1cc]
  0x000e5c63  xor      ebx, ebx
  0x000e5c65  mov      ecx, dword ptr [edi + 0x1d0]
  0x000e5c6b  mov      eax, esi
  0x000e5c6d  mov      dword ptr [ebp - 0xc], ebx
  0x000e5c70  mov      dword ptr [ebp - 0x14], ebx
  0x000e5c73  mov      dword ptr [ebp - 0x1c], ebx
  0x000e5c76  mov      dword ptr [ebp - 4], ebx
  0x000e5c79  mov      dword ptr [ebp - 8], ebx
  0x000e5c7c  mov      dword ptr [ebp + 8], esi
  0x000e5c7f  cmp      eax, ecx
  0x000e5c81  je       0x100e5cbc
  0x000e5c83  xor      edi, edi
  0x000e5c85  xor      esi, esi
  0x000e5c87  mov      edx, dword ptr [eax]
  0x000e5c89  cmp      edx, 4
  0x000e5c8c  ja       0x100e5ca6
  0x000e5c8e  jmp      dword ptr [edx*4 + 0x100e5e80]
  0x000e5c95  inc      ebx
  0x000e5c96  jmp      0x100e5ca6   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x126
  0x000e5c98  inc      edi
  0x000e5c99  jmp      0x100e5ca6   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x126
  0x000e5c9b  inc      esi
  0x000e5c9c  jmp      0x100e5ca6   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x126
  0x000e5c9e  inc      dword ptr [ebp - 4]
  0x000e5ca1  jmp      0x100e5ca6   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x126
  0x000e5ca3  inc      dword ptr [ebp - 8]
  0x000e5ca6  add      eax, 0x40
  0x000e5ca9  cmp      eax, ecx
  0x000e5cab  jne      0x100e5c87
  0x000e5cad  mov      dword ptr [ebp - 0x1c], esi
  0x000e5cb0  mov      esi, dword ptr [ebp + 8]
  0x000e5cb3  mov      dword ptr [ebp - 0x14], edi
  0x000e5cb6  mov      edi, dword ptr [ebp - 0x24]
  0x000e5cb9  mov      dword ptr [ebp - 0xc], ebx
  0x000e5cbc  xor      edx, edx
  0x000e5cbe  mov      dword ptr [ebp + 8], edx
  0x000e5cc1  mov      dword ptr [ebp - 0x10], edx
  0x000e5cc4  mov      dword ptr [ebp - 0x18], edx
  0x000e5cc7  mov      dword ptr [ebp - 0x20], edx
  0x000e5cca  mov      dword ptr [ebp - 0x24], edx
  0x000e5ccd  cmp      esi, ecx
  0x000e5ccf  je       0x100e5d9e
  0x000e5cd5  lea      ebx, [esi + 0x40]
  0x000e5cd8  nop      dword ptr [eax + eax]
  0x000e5ce0  mov      eax, dword ptr [esi]
  0x000e5ce2  cmp      eax, 4
  0x000e5ce5  ja       0x100e5d92
  0x000e5ceb  jmp      dword ptr [eax*4 + 0x100e5e94]
  0x000e5cf2  inc      edx
  0x000e5cf3  mov      dword ptr [ebp + 8], edx
  0x000e5cf6  cmp      edx, dword ptr [ebp - 0xc]
  0x000e5cf9  jge      0x100e5d8c
  0x000e5cff  mov      byte ptr [ebp - 0x28], 0
  0x000e5d03  push     dword ptr [ebp - 0x28]
  0x000e5d06  jmp      0x100e5d5a   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x1da
  0x000e5d08  mov      eax, dword ptr [ebp - 0x10]
  0x000e5d0b  inc      eax
  0x000e5d0c  mov      dword ptr [ebp - 0x10], eax
  0x000e5d0f  cmp      eax, dword ptr [ebp - 0x14]
  0x000e5d12  jge      0x100e5d8c
  0x000e5d14  mov      byte ptr [ebp - 0x2c], 0
  0x000e5d18  push     dword ptr [ebp - 0x2c]
  0x000e5d1b  jmp      0x100e5d5a   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x1da
  0x000e5d1d  mov      eax, dword ptr [ebp - 0x18]
  0x000e5d20  inc      eax
  0x000e5d21  mov      dword ptr [ebp - 0x18], eax
  0x000e5d24  cmp      eax, dword ptr [ebp - 0x1c]
  0x000e5d27  jge      0x100e5d8c
  0x000e5d29  mov      byte ptr [ebp - 0x30], 0
  0x000e5d2d  push     dword ptr [ebp - 0x30]
  0x000e5d30  jmp      0x100e5d5a   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x1da
  0x000e5d32  mov      eax, dword ptr [ebp - 0x20]
  0x000e5d35  inc      eax
  0x000e5d36  mov      dword ptr [ebp - 0x20], eax
  0x000e5d39  cmp      eax, dword ptr [ebp - 4]
  0x000e5d3c  jge      0x100e5d8c
  0x000e5d3e  mov      byte ptr [ebp - 0x34], 0
  0x000e5d42  push     dword ptr [ebp - 0x34]
  0x000e5d45  jmp      0x100e5d5a   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x1da
  0x000e5d47  mov      eax, dword ptr [ebp - 0x24]
  0x000e5d4a  inc      eax
  0x000e5d4b  mov      dword ptr [ebp - 0x24], eax
  0x000e5d4e  cmp      eax, dword ptr [ebp - 8]
  0x000e5d51  jge      0x100e5d8c
  0x000e5d53  mov      byte ptr [ebp - 0x38], 0
  0x000e5d57  push     dword ptr [ebp - 0x38]
  0x000e5d5a  mov      edx, dword ptr [edi + 0x1d0]
  0x000e5d60  mov      ecx, ebx
  0x000e5d62  push     esi
  0x000e5d63  call     0x100e8870   ; -> ?IsInState@ControllerAI@GAME@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z+0x210
  0x000e5d68  mov      edx, dword ptr [edi + 0x1d0]
  0x000e5d6e  add      esp, 8
  0x000e5d71  push     dword ptr [ebp + 8]
  0x000e5d74  push     ecx
  0x000e5d75  lea      ecx, [edx - 0x40]
  0x000e5d78  call     0x10063da0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1cb0
  0x000e5d7d  mov      edx, dword ptr [ebp + 8]
  0x000e5d80  add      esp, 8
  0x000e5d83  add      dword ptr [edi + 0x1d0], -0x40
  0x000e5d8a  jmp      0x100e5d92   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x212
  0x000e5d8c  add      esi, 0x40
  0x000e5d8f  add      ebx, 0x40
  0x000e5d92  cmp      esi, dword ptr [edi + 0x1d0]
  0x000e5d98  jne      0x100e5ce0
  0x000e5d9e  mov      esi, dword ptr [edi + 0x1cc]
  0x000e5da4  cmp      esi, dword ptr [edi + 0x1d0]
  0x000e5daa  je       0x100e5e52
  0x000e5db0  lea      ebx, [esi + 0x28]
  0x000e5db3  mov      eax, dword ptr [esi]
  0x000e5db5  cmp      eax, 4
  0x000e5db8  ja       0x100e5e40
  0x000e5dbe  jmp      dword ptr [eax*4 + 0x100e5ea8]
  0x000e5dc5  movzx    eax, byte ptr [ebx - 0x10]
  0x000e5dc9  mov      ecx, edi
  0x000e5dcb  mov      edx, dword ptr [edi]
  0x000e5dcd  push     eax
  0x000e5dce  lea      eax, [ebx - 0x20]
  0x000e5dd1  push     eax
  0x000e5dd2  push     dword ptr [ebx - 0x24]
  0x000e5dd5  push     ebx
  0x000e5dd6  call     dword ptr [edx + 0xe4]
  0x000e5ddc  jmp      0x100e5e40   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x2c0
  0x000e5dde  movzx    eax, byte ptr [ebx - 0x10]
  0x000e5de2  mov      ecx, edi
  0x000e5de4  mov      edx, dword ptr [edi]
  0x000e5de6  push     eax
  0x000e5de7  lea      eax, [ebx - 0x20]
  0x000e5dea  push     eax
  0x000e5deb  push     dword ptr [ebx - 0x24]
  0x000e5dee  call     dword ptr [edx + 0xe8]
  0x000e5df4  jmp      0x100e5e40   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x2c0
  0x000e5df6  movzx    eax, byte ptr [ebx - 0x10]
  0x000e5dfa  mov      ecx, edi
  0x000e5dfc  mov      edx, dword ptr [edi]
  0x000e5dfe  push     eax
  0x000e5dff  movzx    eax, byte ptr [ebx - 0xf]
  0x000e5e03  push     eax
  0x000e5e04  push     dword ptr [ebx - 0xc]
  0x000e5e07  push     ebx
  0x000e5e08  call     dword ptr [edx + 0xec]
  0x000e5e0e  jmp      0x100e5e40   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x2c0
  0x000e5e10  movzx    eax, byte ptr [ebx - 0x10]
  0x000e5e14  mov      ecx, edi
  0x000e5e16  mov      edx, dword ptr [edi]
  0x000e5e18  push     eax
  0x000e5e19  push     dword ptr [ebx - 4]
  0x000e5e1c  push     dword ptr [ebx - 0x24]
  0x000e5e1f  push     dword ptr [ebx - 8]
  0x000e5e22  call     dword ptr [edx + 0xf0]
  0x000e5e28  jmp      0x100e5e40   ; -> ?Update@ControllerAI@GAME@@UAEXH@Z+0x2c0
  0x000e5e2a  movzx    eax, byte ptr [ebx - 0x10]
  0x000e5e2e  mov      ecx, edi
  0x000e5e30  mov      edx, dword ptr [edi]
  0x000e5e32  push     eax
  0x000e5e33  lea      eax, [ebx - 0x20]
  0x000e5e36  push     eax
  0x000e5e37  push     dword ptr [ebx - 0x24]
  0x000e5e3a  call     dword ptr [edx + 0xf4]
  0x000e5e40  add      esi, 0x40
  0x000e5e43  add      ebx, 0x40
  0x000e5e46  cmp      esi, dword ptr [edi + 0x1d0]
  0x000e5e4c  jne      0x100e5db3
  0x000e5e52  push     dword ptr [ebp + 8]
  0x000e5e55  mov      edx, dword ptr [edi + 0x1d0]
  0x000e5e5b  push     ecx
  0x000e5e5c  mov      ecx, dword ptr [edi + 0x1cc]
  0x000e5e62  call     0x10063da0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x1cb0
  0x000e5e67  mov      eax, dword ptr [edi + 0x1cc]
  0x000e5e6d  add      esp, 8
  0x000e5e70  mov      dword ptr [edi + 0x1d0], eax
  0x000e5e76  pop      edi
  0x000e5e77  pop      esi
  0x000e5e78  pop      ebx
  0x000e5e79  mov      esp, ebp
  0x000e5e7b  pop      ebp
  0x000e5e7c  ret      4
  0x000e5e7f  nop      
  0x000e5e80  xchg     ebp, eax
  0x000e5e81  pop      esp
  0x000e5e82  push     cs
  0x000e5e83  adc      byte ptr [eax - 0x64eff1a4], bl
  0x000e5e89  pop      esp
  0x000e5e8a  push     cs
  0x000e5e8b  adc      byte ptr [ebx - 0x61eff1a4], ah
  0x000e5e91  pop      esp
  0x000e5e92  push     cs
  0x000e5e93  adc      dl, dh
  0x000e5e95  pop      esp
  0x000e5e96  push     cs
  0x000e5e97  adc      byte ptr [eax], cl
  0x000e5e99  pop      ebp
  0x000e5e9a  push     cs
  0x000e5e9b  adc      byte ptr [0x47100e5d], bl
  0x000e5ea1  pop      ebp
  0x000e5ea2  push     cs
  0x000e5ea3  adc      byte ptr [edx], dh
  0x000e5ea5  pop      ebp
  0x000e5ea6  push     cs
  0x000e5ea7  adc      ch, al
  0x000e5ea9  pop      ebp
  0x000e5eaa  push     cs
  0x000e5eab  adc      dh, bl
  0x000e5ead  pop      ebp
  0x000e5eae  push     cs
  0x000e5eaf  adc      dh, dh
  0x000e5eb1  pop      ebp
  0x000e5eb2  push     cs
  0x000e5eb3  adc      byte ptr [eax], dl
  0x000e5eb5  pop      esi
  0x000e5eb6  push     cs
  0x000e5eb7  adc      byte ptr [edx], ch
  0x000e5eb9  pop      esi
  0x000e5eba  push     cs
  0x000e5ebb  adc      ah, cl
  0x000e5ebd  int3     
  0x000e5ebe  int3     
  0x000e5ebf  int3     
