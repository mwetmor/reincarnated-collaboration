
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

10015b50 <?PlayAnimationIfAvailable@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z>:
10015b50: 55                           	push	ebp
10015b51: 8b ec                        	mov	ebp, esp
10015b53: 56                           	push	esi
10015b54: 8b f1                        	mov	esi, ecx
10015b56: 57                           	push	edi
10015b57: 8b 7d 0c                     	mov	edi, dword ptr [ebp + 0xc]
10015b5a: 89 7e 08                     	mov	dword ptr [esi + 0x8], edi
10015b5d: 83 ff 33                     	cmp	edi, 0x33
10015b60: 77 06                        	ja	0x10015b68 <?PlayAnimationIfAvailable@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z+0x18>
10015b62: 8b 4c be 0c                  	mov	ecx, dword ptr [esi + 4*edi + 0xc]
10015b66: eb 03                        	jmp	0x10015b6b <?PlayAnimationIfAvailable@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z+0x1b>
10015b68: 8b 4e 0c                     	mov	ecx, dword ptr [esi + 0xc]
10015b6b: ff 75 1c                     	push	dword ptr [ebp + 0x1c]
10015b6e: f3 0f 10 45 14               	movss	xmm0, dword ptr [ebp + 0x14]
10015b73: ff 75 18                     	push	dword ptr [ebp + 0x18]
10015b76: 8b 01                        	mov	eax, dword ptr [ecx]
10015b78: 51                           	push	ecx
10015b79: f3 0f 11 04 24               	movss	dword ptr [esp], xmm0
10015b7e: ff 75 10                     	push	dword ptr [ebp + 0x10]
10015b81: 8b 40 04                     	mov	eax, dword ptr [eax + 0x4]
10015b84: ff 75 08                     	push	dword ptr [ebp + 0x8]
10015b87: ff d0                        	call	eax
10015b89: 84 c0                        	test	al, al
10015b8b: 74 12                        	je	0x10015b9f <?PlayAnimationIfAvailable@AnimationSet@GAME@@QAE?B_NAAVActor@2@W4AnimationSet_Type@2@ABVName@2@M_NI@Z+0x4f>
10015b8d: 89 7e 04                     	mov	dword ptr [esi + 0x4], edi
10015b90: b0 01                        	mov	al, 0x1
10015b92: 5f                           	pop	edi
10015b93: c7 46 08 00 00 00 00         	mov	dword ptr [esi + 0x8], 0x0
10015b9a: 5e                           	pop	esi
10015b9b: 5d                           	pop	ebp
10015b9c: c2 18 00                     	ret	0x18
10015b9f: 5f                           	pop	edi
10015ba0: 32 c0                        	xor	al, al
10015ba2: 5e                           	pop	esi
10015ba3: 5d                           	pop	ebp
10015ba4: c2 18 00                     	ret	0x18
