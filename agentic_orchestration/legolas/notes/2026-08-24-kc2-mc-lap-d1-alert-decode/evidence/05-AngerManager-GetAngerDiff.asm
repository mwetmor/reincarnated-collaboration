
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

1000f360 <?GetAngerDiff@AngerManager@GAME@@QBEMI@Z>:
1000f360: 55                           	push	ebp
1000f361: 8b ec                        	mov	ebp, esp
1000f363: 51                           	push	ecx
1000f364: 56                           	push	esi
1000f365: 8d 45 08                     	lea	eax, [ebp + 0x8]
1000f368: 50                           	push	eax
1000f369: 8d 71 04                     	lea	esi, [ecx + 0x4]
1000f36c: 8d 45 fc                     	lea	eax, [ebp - 0x4]
1000f36f: 8b ce                        	mov	ecx, esi
1000f371: 50                           	push	eax
1000f372: e8 a9 0e 00 00               	call	0x10010220 <?ShouldRemoveEnemy@AngerManager@GAME@@AAE_NI_N@Z+0x230>
1000f377: 8b 00                        	mov	eax, dword ptr [eax]
1000f379: 3b 06                        	cmp	eax, dword ptr [esi]
1000f37b: 5e                           	pop	esi
1000f37c: 74 0c                        	je	0x1000f38a <?GetAngerDiff@AngerManager@GAME@@QBEMI@Z+0x2a>
1000f37e: d9 40 14                     	fld	dword ptr [eax + 0x14]
1000f381: d8 60 18                     	fsub	dword ptr [eax + 0x18]
1000f384: 8b e5                        	mov	esp, ebp
1000f386: 5d                           	pop	ebp
1000f387: c2 04 00                     	ret	0x4
1000f38a: d9 ee                        	fldz
1000f38c: 8b e5                        	mov	esp, ebp
1000f38e: 5d                           	pop	ebp
1000f38f: c2 04 00                     	ret	0x4
