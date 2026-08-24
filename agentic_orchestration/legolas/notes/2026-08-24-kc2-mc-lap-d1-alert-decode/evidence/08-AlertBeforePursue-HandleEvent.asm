
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

101094f0 <?HandleEvent@ControllerMonsterStateAlertBeforePursue@GAME@@MAEXABVName@2@@Z>:
101094f0: 55                           	push	ebp
101094f1: 8b ec                        	mov	ebp, esp
101094f3: 64 a1 00 00 00 00            	mov	eax, dword ptr fs:[0x0]
101094f9: 6a ff                        	push	-0x1
101094fb: 68 5c 8a 4c 10               	push	0x104c8a5c
10109500: 50                           	push	eax
10109501: 64 89 25 00 00 00 00         	mov	dword ptr fs:[0x0], esp
10109508: 64 a1 2c 00 00 00            	mov	eax, dword ptr fs:[0x2c]
1010950e: 8b 15 80 80 80 10            	mov	edx, dword ptr [0x10808080]
10109514: 56                           	push	esi
10109515: 8b f1                        	mov	esi, ecx
10109517: 8b 14 90                     	mov	edx, dword ptr [eax + 4*edx]
1010951a: a1 34 b3 80 10               	mov	eax, dword ptr [0x1080b334]
1010951f: 3b 82 04 00 00 00            	cmp	eax, dword ptr [edx + 0x4]
10109525: 7e 41                        	jle	0x10109568 <?HandleEvent@ControllerMonsterStateAlertBeforePursue@GAME@@MAEXABVName@2@@Z+0x78>
10109527: 68 34 b3 80 10               	push	0x1080b334
1010952c: e8 ae 55 3b 00               	call	0x104beadf <?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36e2f>
10109531: 83 c4 04                     	add	esp, 0x4
10109534: 83 3d 34 b3 80 10 ff         	cmp	dword ptr [0x1080b334], -0x1
1010953b: 75 2b                        	jne	0x10109568 <?HandleEvent@ControllerMonsterStateAlertBeforePursue@GAME@@MAEXABVName@2@@Z+0x78>
1010953d: 68 f4 d3 52 10               	push	0x1052d3f4
10109542: 68 38 b3 80 10               	push	0x1080b338
10109547: c7 45 fc 00 00 00 00         	mov	dword ptr [ebp - 0x4], 0x0
1010954e: ff 15 58 52 4e 10            	call	dword ptr [0x104e5258]
10109554: 68 34 b3 80 10               	push	0x1080b334
10109559: c7 45 fc ff ff ff ff         	mov	dword ptr [ebp - 0x4], 0xffffffff
10109560: e8 3b 55 3b 00               	call	0x104beaa0 <?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36df0>
10109565: 83 c4 0c                     	add	esp, 0xc
10109568: 8b 45 08                     	mov	eax, dword ptr [ebp + 0x8]
1010956b: 8b 00                        	mov	eax, dword ptr [eax]
1010956d: 3b 05 38 b3 80 10            	cmp	eax, dword ptr [0x1080b338]
10109573: 75 0c                        	jne	0x10109581 <?HandleEvent@ControllerMonsterStateAlertBeforePursue@GAME@@MAEXABVName@2@@Z+0x91>
10109575: 8b 06                        	mov	eax, dword ptr [esi]
10109577: 8b ce                        	mov	ecx, esi
10109579: 6a 01                        	push	0x1
1010957b: ff 90 0c 01 00 00            	call	dword ptr [eax + 0x10c]
10109581: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
10109584: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
1010958b: 5e                           	pop	esi
1010958c: 8b e5                        	mov	esp, ebp
1010958e: 5d                           	pop	ebp
1010958f: c2 04 00                     	ret	0x4
