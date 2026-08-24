
/Users/admin/Games/vendor/grim-dawn/Engine.dll:	file format coff-i386

Disassembly of section .text:

10087660 <?LoadANMData@GraphicsAnim@GAME@@QAE_NPBXHH@Z>:
100876a0: 45                           	inc	ebp
100876a1: fc                           	cld
100876a2: 00 00                        	add	byte ptr [eax], al
100876a4: 00 00                        	add	byte ptr [eax], al
100876a6: 8d 79 04                     	lea	edi, [ecx + 0x4]
100876a9: 8b 01                        	mov	eax, dword ptr [ecx]
100876ab: 8d 9e 80 00 00 00            	lea	ebx, [esi + 0x80]
100876b1: 50                           	push	eax
100876b2: 8b cb                        	mov	ecx, ebx
100876b4: 89 45 90                     	mov	dword ptr [ebp - 0x70], eax
100876b7: 89 bd 64 ff ff ff            	mov	dword ptr [ebp - 0x9c], edi
100876bd: e8 fe 2c fa ff               	call	0x1002a3c0 <?SupportsNetwork@ActorConfigCommand@GAME@@QBE?B_NXZ+0x1230>
100876c2: 8b 07                        	mov	eax, dword ptr [edi]
100876c4: 89 86 8c 00 00 00            	mov	dword ptr [esi + 0x8c], eax
100876ca: 8b 47 04                     	mov	eax, dword ptr [edi + 0x4]
100876cd: 83 c7 08                     	add	edi, 0x8
100876d0: 89 86 90 00 00 00            	mov	dword ptr [esi + 0x90], eax
100876d6: 33 f6                        	xor	esi, esi
100876d8: 89 bd 64 ff ff ff            	mov	dword ptr [ebp - 0x9c], edi
100876de: 39 75 90                     	cmp	dword ptr [ebp - 0x70], esi
