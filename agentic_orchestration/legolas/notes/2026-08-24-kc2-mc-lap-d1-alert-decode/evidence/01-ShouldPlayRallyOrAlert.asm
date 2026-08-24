
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100f9ce0 <?ShouldPlayRallyOrAlert@ControllerMonster@GAME@@QAE_NXZ>:
100f9ce0: 80 b9 8c 02 00 00 00         	cmp	byte ptr [ecx + 0x28c], 0x0
100f9ce7: 74 0a                        	je	0x100f9cf3 <?ShouldPlayRallyOrAlert@ControllerMonster@GAME@@QAE_NXZ+0x13>
100f9ce9: c6 81 8c 02 00 00 00         	mov	byte ptr [ecx + 0x28c], 0x0
100f9cf0: b0 01                        	mov	al, 0x1
100f9cf2: c3                           	ret
100f9cf3: 32 c0                        	xor	al, al
100f9cf5: c3                           	ret
