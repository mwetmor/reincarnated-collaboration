
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100e77f0 <?PlayAnimation@ControllerAI@GAME@@QAEXW4AnimationSet_Type@2@ABVName@2@M_NI@Z>:
100e77f0: 55                           	push	ebp
100e77f1: 8b ec                        	mov	ebp, esp
100e77f3: 6a ff                        	push	-0x1
100e77f5: 68 d8 79 4c 10               	push	0x104c79d8
100e77fa: 64 a1 00 00 00 00            	mov	eax, dword ptr fs:[0x0]
100e7800: 50                           	push	eax
100e7801: 64 89 25 00 00 00 00         	mov	dword ptr fs:[0x0], esp
100e7808: 51                           	push	ecx
100e7809: 53                           	push	ebx
100e780a: 56                           	push	esi
100e780b: 57                           	push	edi
100e780c: 6a 48                        	push	0x48
100e780e: 8b d9                        	mov	ebx, ecx
100e7810: e8 0b 71 3d 00               	call	0x104be920 <?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36c70>
100e7815: 8b f8                        	mov	edi, eax
100e7817: 83 c4 04                     	add	esp, 0x4
100e781a: 89 7d f0                     	mov	dword ptr [ebp - 0x10], edi
100e781d: c7 45 fc 00 00 00 00         	mov	dword ptr [ebp - 0x4], 0x0
100e7824: 8b cf                        	mov	ecx, edi
100e7826: 8b 73 24                     	mov	esi, dword ptr [ebx + 0x24]
100e7829: 56                           	push	esi
100e782a: ff 15 60 57 4e 10            	call	dword ptr [0x104e5760]
100e7830: c6 45 fc 01                  	mov	byte ptr [ebp - 0x4], 0x1
100e7834: 8d 4f 18                     	lea	ecx, [edi + 0x18]
100e7837: c7 07 d4 21 59 10            	mov	dword ptr [edi], 0x105921d4
100e783d: 89 77 04                     	mov	dword ptr [edi + 0x4], esi
100e7840: c7 47 08 00 00 00 00         	mov	dword ptr [edi + 0x8], 0x0
100e7847: 66 c7 47 0c 00 01            	mov	word ptr [edi + 0xc], 0x100
100e784d: c7 47 10 00 00 7a 43         	mov	dword ptr [edi + 0x10], 0x437a0000
100e7854: c6 47 14 00                  	mov	byte ptr [edi + 0x14], 0x0
100e7858: ff 15 88 53 4e 10            	call	dword ptr [0x104e5388]
100e785e: 8b 45 08                     	mov	eax, dword ptr [ebp + 0x8]
100e7861: 8b cb                        	mov	ecx, ebx
100e7863: f3 0f 10 45 10               	movss	xmm0, dword ptr [ebp + 0x10]
100e7868: c7 07 48 1b 59 10            	mov	dword ptr [edi], 0x10591b48
100e786e: c7 47 38 00 00 00 00         	mov	dword ptr [edi + 0x38], 0x0
100e7875: 89 47 34                     	mov	dword ptr [edi + 0x34], eax
100e7878: 8b 45 0c                     	mov	eax, dword ptr [ebp + 0xc]
100e787b: 57                           	push	edi
100e787c: 8b 00                        	mov	eax, dword ptr [eax]
100e787e: 89 47 38                     	mov	dword ptr [edi + 0x38], eax
100e7881: 8a 45 14                     	mov	al, byte ptr [ebp + 0x14]
100e7884: 88 47 40                     	mov	byte ptr [edi + 0x40], al
100e7887: 8b 45 18                     	mov	eax, dword ptr [ebp + 0x18]
100e788a: f3 0f 11 47 3c               	movss	dword ptr [edi + 0x3c], xmm0
100e788f: 89 47 44                     	mov	dword ptr [edi + 0x44], eax
100e7892: c7 47 08 12 00 00 00         	mov	dword ptr [edi + 0x8], 0x12
100e7899: c6 47 0c 01                  	mov	byte ptr [edi + 0xc], 0x1
100e789d: c7 45 fc ff ff ff ff         	mov	dword ptr [ebp - 0x4], 0xffffffff
100e78a4: e8 d7 2b 00 00               	call	0x100ea480 <?HandleAction@ControllerBaseCharacter@GAME@@QAEXPAVCharacterAction@2@@Z>
100e78a9: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
100e78ac: 5f                           	pop	edi
100e78ad: 5e                           	pop	esi
100e78ae: 5b                           	pop	ebx
100e78af: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
100e78b6: 8b e5                        	mov	esp, ebp
100e78b8: 5d                           	pop	ebp
100e78b9: c2 14 00                     	ret	0x14
