
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100454b0 <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z>:
10045cb0: e8 db 04 fd ff               	call	0x10016190 <?CalculateAllocatedMemory@AnimationSet@GAME@@QBEIXZ+0x310>
10045cb5: 84 c0                        	test	al, al
10045cb7: 0f 85 a6 05 00 00            	jne	0x10046263 <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z+0xdb3>
10045cbd: 8b 06                        	mov	eax, dword ptr [esi]
10045cbf: 3b 05 08 b1 80 10            	cmp	eax, dword ptr [0x1080b108]
10045cc5: 75 22                        	jne	0x10045ce9 <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z+0x839>
10045cc7: 8b 07                        	mov	eax, dword ptr [edi]
10045cc9: 8b cf                        	mov	ecx, edi
10045ccb: ff 10                        	call	dword ptr [eax]
10045ccd: 8b 87 a4 1b 00 00            	mov	eax, dword ptr [edi + 0x1ba4]
10045cd3: 8b 48 04                     	mov	ecx, dword ptr [eax + 0x4]
10045cd6: 85 c9                        	test	ecx, ecx
10045cd8: 0f 84 85 05 00 00            	je	0x10046263 <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z+0xdb3>
10045cde: 8b 01                        	mov	eax, dword ptr [ecx]
10045ce0: 56                           	push	esi
10045ce1: ff 50 08                     	call	dword ptr [eax + 0x8]
10045ce4: e9 7a 05 00 00               	jmp	0x10046263 <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z+0xdb3>
10045ce9: 3b 05 10 b1 80 10            	cmp	eax, dword ptr [0x1080b110]
10045cef: 0f 84 38 01 00 00            	je	0x10045e2d <?AnimationCallback@Character@GAME@@UAE_NABVName@2@@Z+0x97d>
