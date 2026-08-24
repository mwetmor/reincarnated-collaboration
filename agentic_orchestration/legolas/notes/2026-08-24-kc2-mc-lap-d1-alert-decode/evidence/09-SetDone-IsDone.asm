
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

1005e050 <?SetProcess@CombatAttribute@GAME@@UAEX_N@Z>:
1005e050: 55                           	push	ebp
1005e051: 8b ec                        	mov	ebp, esp
1005e053: 8a 45 08                     	mov	al, byte ptr [ebp + 0x8]
1005e056: 88 41 0c                     	mov	byte ptr [ecx + 0xc], al
1005e059: 5d                           	pop	ebp
1005e05a: c2 04 00                     	ret	0x4

1005e060 <?SupportsNetwork@CharacterActionBase@GAME@@UAE_NXZ>:
1005e060: 8a 41 0c                     	mov	al, byte ptr [ecx + 0xc]
1005e063: c3                           	ret
