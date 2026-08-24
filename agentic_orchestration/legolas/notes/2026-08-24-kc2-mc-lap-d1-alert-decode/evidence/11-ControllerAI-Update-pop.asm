
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100e5b80 <?Update@ControllerAI@GAME@@UAEXH@Z>:
100e5b80: 55                           	push	ebp
100e5b81: 8b ec                        	mov	ebp, esp
100e5b83: 83 ec 38                     	sub	esp, 0x38
100e5b86: 53                           	push	ebx
100e5b87: 56                           	push	esi
100e5b88: 8b 75 08                     	mov	esi, dword ptr [ebp + 0x8]
100e5b8b: 57                           	push	edi
100e5b8c: 8b f9                        	mov	edi, ecx
100e5b8e: 56                           	push	esi
100e5b8f: 89 7d dc                     	mov	dword ptr [ebp - 0x24], edi
100e5b92: e8 79 8e 00 00               	call	0x100eea10 <?Update@ControllerCombat@GAME@@UAEXH@Z>
100e5b97: 8b cf                        	mov	ecx, edi
100e5b99: e8 82 29 00 00               	call	0x100e8520 <?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ>
100e5b9e: 8b c8                        	mov	ecx, eax
100e5ba0: 8b 10                        	mov	edx, dword ptr [eax]
100e5ba2: 8b 82 08 01 00 00            	mov	eax, dword ptr [edx + 0x108]
100e5ba8: ff d0                        	call	eax
100e5baa: 84 c0                        	test	al, al
100e5bac: 74 78                        	je	0x100e5c26 <?Update@ControllerAI@GAME@@UAEXH@Z+0xa6>
100e5bae: 66 90                        	nop
100e5bb0: 8b 87 10 02 00 00            	mov	eax, dword ptr [edi + 0x210]
100e5bb6: 8b 00                        	mov	eax, dword ptr [eax]
100e5bb8: 8b 48 08                     	mov	ecx, dword ptr [eax + 0x8]
100e5bbb: 8b 01                        	mov	eax, dword ptr [ecx]
100e5bbd: ff 90 14 01 00 00            	call	dword ptr [eax + 0x114]
100e5bc3: 8b 87 10 02 00 00            	mov	eax, dword ptr [edi + 0x210]
100e5bc9: 6a 00                        	push	0x0
100e5bcb: 8b 00                        	mov	eax, dword ptr [eax]
100e5bcd: 8b 48 08                     	mov	ecx, dword ptr [eax + 0x8]
100e5bd0: 8b 01                        	mov	eax, dword ptr [ecx]
100e5bd2: ff 90 0c 01 00 00            	call	dword ptr [eax + 0x10c]
100e5bd8: 8b 87 10 02 00 00            	mov	eax, dword ptr [edi + 0x210]
100e5bde: 8b 10                        	mov	edx, dword ptr [eax]
100e5be0: 52                           	push	edx
100e5be1: 8b 4a 04                     	mov	ecx, dword ptr [edx + 0x4]
100e5be4: 8b 02                        	mov	eax, dword ptr [edx]
100e5be6: 89 01                        	mov	dword ptr [ecx], eax
100e5be8: 8b 0a                        	mov	ecx, dword ptr [edx]
100e5bea: 8b 42 04                     	mov	eax, dword ptr [edx + 0x4]
100e5bed: 89 41 04                     	mov	dword ptr [ecx + 0x4], eax
100e5bf0: ff 8f 14 02 00 00            	dec	dword ptr [edi + 0x214]
100e5bf6: e8 20 8d 3d 00               	call	0x104be91b <?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c6b>
100e5bfb: 83 c4 04                     	add	esp, 0x4
100e5bfe: 8b cf                        	mov	ecx, edi
100e5c00: e8 1b 29 00 00               	call	0x100e8520 <?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ>
100e5c05: 8b c8                        	mov	ecx, eax
100e5c07: 8b 10                        	mov	edx, dword ptr [eax]
100e5c09: ff 92 10 01 00 00            	call	dword ptr [edx + 0x110]
100e5c0f: 8b cf                        	mov	ecx, edi
100e5c11: e8 0a 29 00 00               	call	0x100e8520 <?GetExecutingState@ControllerAI@GAME@@IBEPAVControllerAIState@2@XZ>
100e5c16: 8b c8                        	mov	ecx, eax
100e5c18: 8b 10                        	mov	edx, dword ptr [eax]
100e5c1a: 8b 82 08 01 00 00            	mov	eax, dword ptr [edx + 0x108]
100e5c20: ff d0                        	call	eax
100e5c22: 84 c0                        	test	al, al
100e5c24: 75 8a                        	jne	0x100e5bb0 <?Update@ControllerAI@GAME@@UAEXH@Z+0x30>
100e5c26: 83 bf 14 02 00 00 00         	cmp	dword ptr [edi + 0x214], 0x0
100e5c2d: 74 0d                        	je	0x100e5c3c <?Update@ControllerAI@GAME@@UAEXH@Z+0xbc>
100e5c2f: 8b 87 10 02 00 00            	mov	eax, dword ptr [edi + 0x210]
100e5c35: 8b 00                        	mov	eax, dword ptr [eax]
100e5c37: 8b 48 08                     	mov	ecx, dword ptr [eax + 0x8]
100e5c3a: eb 06                        	jmp	0x100e5c42 <?Update@ControllerAI@GAME@@UAEXH@Z+0xc2>
100e5c3c: 8b 8f e4 01 00 00            	mov	ecx, dword ptr [edi + 0x1e4]
100e5c42: 8b 01                        	mov	eax, dword ptr [ecx]
100e5c44: 56                           	push	esi
100e5c45: ff 90 18 01 00 00            	call	dword ptr [eax + 0x118]
100e5c4b: 8b 87 d8 01 00 00            	mov	eax, dword ptr [edi + 0x1d8]
