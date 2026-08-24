
/Users/admin/Games/vendor/grim-dawn/Engine.dll:	file format coff-i386

Disassembly of section .text:

100889a0 <?GetLength@GraphicsAnim@GAME@@QBEIXZ>:
100889a0: 56                           	push	esi
100889a1: 8b f1                        	mov	esi, ecx
100889a3: e8 08 9d 0d 00               	call	0x101626b0 <?EnsureAvailable@Resource@GAME@@QBEXXZ>
100889a8: 8b 86 8c 00 00 00            	mov	eax, dword ptr [esi + 0x8c]
100889ae: 5e                           	pop	esi
100889af: c3                           	ret

100889b0 <?GetNumHitBoxes@GraphicsMesh@GAME@@QBEIXZ>:
100889b0: 56                           	push	esi
100889b1: 8b f1                        	mov	esi, ecx
100889b3: e8 f8 9c 0d 00               	call	0x101626b0 <?EnsureAvailable@Resource@GAME@@QBEXXZ>
100889b8: 8b 86 90 00 00 00            	mov	eax, dword ptr [esi + 0x90]
100889be: 5e                           	pop	esi
100889bf: c3                           	ret
