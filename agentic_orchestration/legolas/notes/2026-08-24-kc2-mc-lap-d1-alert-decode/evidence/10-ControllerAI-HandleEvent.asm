
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100e6130 <?HandleEvent@ControllerAI@GAME@@UAEXABVName@2@@Z>:
100e6130: 55                           	push	ebp
100e6131: 8b ec                        	mov	ebp, esp
100e6133: 56                           	push	esi
100e6134: ff 75 08                     	push	dword ptr [ebp + 0x8]
100e6137: 8b f1                        	mov	esi, ecx
100e6139: e8 42 85 00 00               	call	0x100ee680 <?HandleEvent@ControllerCombat@GAME@@UAEXABVName@2@@Z>
100e613e: 83 be 14 02 00 00 00         	cmp	dword ptr [esi + 0x214], 0x0
100e6145: 74 0d                        	je	0x100e6154 <?HandleEvent@ControllerAI@GAME@@UAEXABVName@2@@Z+0x24>
100e6147: 8b 86 10 02 00 00            	mov	eax, dword ptr [esi + 0x210]
100e614d: 8b 00                        	mov	eax, dword ptr [eax]
100e614f: 8b 48 08                     	mov	ecx, dword ptr [eax + 0x8]
100e6152: eb 06                        	jmp	0x100e615a <?HandleEvent@ControllerAI@GAME@@UAEXABVName@2@@Z+0x2a>
100e6154: 8b 8e e4 01 00 00            	mov	ecx, dword ptr [esi + 0x1e4]
100e615a: 8b 01                        	mov	eax, dword ptr [ecx]
100e615c: 5e                           	pop	esi
100e615d: 5d                           	pop	ebp
100e615e: ff 60 34                     	jmp	dword ptr [eax + 0x34]
