
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

10109410 <?OnBegin@ControllerMonsterStateAlertBeforePursue@GAME@@UAEXXZ>:
10109410: 6a 00                        	push	0x0
10109412: 6a 00                        	push	0x0
10109414: 51                           	push	ecx
10109415: 8b 49 04                     	mov	ecx, dword ptr [ecx + 0x4]
10109418: c7 04 24 00 00 80 3f         	mov	dword ptr [esp], 0x3f800000
1010941f: ff 35 b0 52 4e 10            	push	dword ptr [0x104e52b0]
10109425: 6a 21                        	push	0x21
10109427: e8 c4 e3 fd ff               	call	0x100e77f0 <?PlayAnimation@ControllerAI@GAME@@QAEXW4AnimationSet_Type@2@ABVName@2@M_NI@Z>
1010942c: c3                           	ret
