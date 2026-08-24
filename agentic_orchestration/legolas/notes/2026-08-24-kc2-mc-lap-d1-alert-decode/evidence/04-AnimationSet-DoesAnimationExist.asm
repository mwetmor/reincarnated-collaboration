
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

10015d60 <?DoesAnimationExist@AnimationSet@GAME@@QAE_NW4AnimationSet_Type@2@@Z>:
10015d60: 55                           	push	ebp
10015d61: 8b ec                        	mov	ebp, esp
10015d63: 8b 45 08                     	mov	eax, dword ptr [ebp + 0x8]
10015d66: 83 f8 33                     	cmp	eax, 0x33
10015d69: 77 14                        	ja	0x10015d7f <?DoesAnimationExist@AnimationSet@GAME@@QAE_NW4AnimationSet_Type@2@@Z+0x1f>
10015d6b: 8b 4c 81 0c                  	mov	ecx, dword ptr [ecx + 4*eax + 0xc]
10015d6f: 8b 01                        	mov	eax, dword ptr [ecx]
10015d71: 8b 40 3c                     	mov	eax, dword ptr [eax + 0x3c]
10015d74: ff d0                        	call	eax
10015d76: 84 c0                        	test	al, al
10015d78: 0f 94 c0                     	sete	al
10015d7b: 5d                           	pop	ebp
10015d7c: c2 04 00                     	ret	0x4
10015d7f: 8b 49 0c                     	mov	ecx, dword ptr [ecx + 0xc]
10015d82: 8b 01                        	mov	eax, dword ptr [ecx]
10015d84: 8b 40 3c                     	mov	eax, dword ptr [eax + 0x3c]
10015d87: ff d0                        	call	eax
10015d89: 84 c0                        	test	al, al
10015d8b: 0f 94 c0                     	sete	al
10015d8e: 5d                           	pop	ebp
10015d8f: c2 04 00                     	ret	0x4
