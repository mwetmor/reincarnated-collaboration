
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

1010a360 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z>:
1010a744: 8b 43 08                     	mov	eax, dword ptr [ebx + 0x8]
1010a747: 85 c0                        	test	eax, eax
1010a749: 75 12                        	jne	0x1010a75d <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3fd>
1010a74b: 8b 43 04                     	mov	eax, dword ptr [ebx + 0x4]
1010a74e: ff 70 24                     	push	dword ptr [eax + 0x24]
1010a751: ff d7                        	call	edi
1010a753: 8b c8                        	mov	ecx, eax
1010a755: e8 66 09 f0 ff               	call	0x1000b0c0 <?Reset@AchievementManager@GAME@@QAEXXZ+0xd00>
1010a75a: 89 43 08                     	mov	dword ptr [ebx + 0x8], eax
1010a75d: 8b b0 40 32 00 00            	mov	esi, dword ptr [eax + 0x3240]
1010a763: ff 15 0c 65 4e 10            	call	dword ptr [0x104e650c]
1010a769: 99                           	cdq
1010a76a: b9 64 00 00 00               	mov	ecx, 0x64
1010a76f: f7 f9                        	idiv	ecx
1010a771: 3b d6                        	cmp	edx, esi
1010a773: 73 2e                        	jae	0x1010a7a3 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x443>
1010a775: 8b 43 04                     	mov	eax, dword ptr [ebx + 0x4]
1010a778: 80 b8 8c 02 00 00 00         	cmp	byte ptr [eax + 0x28c], 0x0
1010a77f: 74 22                        	je	0x1010a7a3 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x443>
1010a781: c6 80 8c 02 00 00 00         	mov	byte ptr [eax + 0x28c], 0x0
1010a788: 8b cb                        	mov	ecx, ebx
1010a78a: e8 31 70 fc ff               	call	0x100d17c0 <?GetCharacter@?$ControllerAIStateT@VControllerTyphonChained@GAME@@VMonster@2@@GAME@@IBEABVMonster@2@XZ>
1010a78f: 8b cb                        	mov	ecx, ebx
1010a791: ff b0 3c 32 00 00            	push	dword ptr [eax + 0x323c]
1010a797: e8 24 70 fc ff               	call	0x100d17c0 <?GetCharacter@?$ControllerAIStateT@VControllerTyphonChained@GAME@@VMonster@2@@GAME@@IBEABVMonster@2@XZ>
1010a79c: 8b c8                        	mov	ecx, eax
1010a79e: e8 7d dd f3 ff               	call	0x10048520 <?PlayNetSound@Character@GAME@@QAEXPAVSoundPak@2@@Z>
1010a7a3: 8b 43 04                     	mov	eax, dword ptr [ebx + 0x4]
1010a7a6: 5f                           	pop	edi
1010a7a7: 5e                           	pop	esi
1010a7a8: 83 b8 60 03 00 00 02         	cmp	dword ptr [eax + 0x360], 0x2
1010a7af: 75 07                        	jne	0x1010a7b8 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x458>
1010a7b1: 8b cb                        	mov	ecx, ebx
1010a7b3: e8 78 0e 00 00               	call	0x1010b630 <?CallForFollowers@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXXZ>
1010a7b8: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
1010a7bb: 5b                           	pop	ebx
1010a7bc: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
1010a7c3: 8b e5                        	mov	esp, ebp
1010a7c5: 5d                           	pop	ebp
1010a7c6: c2 04 00                     	ret	0x4

1010a7d0 <?DefaultClosestEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXIM@Z>:
1010a7d0: 55                           	push	ebp
1010a7d1: 8b ec                        	mov	ebp, esp
1010a7d3: 64 a1 00 00 00 00            	mov	eax, dword ptr fs:[0x0]
1010a7d9: 6a ff                        	push	-0x1
1010a7db: 68 c8 34 4c 10               	push	0x104c34c8
1010a7e0: 50                           	push	eax
1010a7e1: 64 89 25 00 00 00 00         	mov	dword ptr fs:[0x0], esp
1010a7e8: 83 ec 44                     	sub	esp, 0x44
1010a7eb: 56                           	push	esi
1010a7ec: 57                           	push	edi
1010a7ed: 8b f9                        	mov	edi, ecx
1010a7ef: 8b 77 04                     	mov	esi, dword ptr [edi + 0x4]
1010a7f2: 83 be 04 03 00 00 03         	cmp	dword ptr [esi + 0x304], 0x3
1010a7f9: 0f 85 8b 00 00 00            	jne	0x1010a88a <?DefaultClosestEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXIM@Z+0xba>
1010a7ff: 8b 86 28 05 00 00            	mov	eax, dword ptr [esi + 0x528]
1010a805: 3b 86 0c 03 00 00            	cmp	eax, dword ptr [esi + 0x30c]
1010a80b: 73 7d                        	jae	0x1010a88a <?DefaultClosestEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXIM@Z+0xba>
1010a80d: 83 be 2c 05 00 00 00         	cmp	dword ptr [esi + 0x52c], 0x0
1010a814: 7f 74                        	jg	0x1010a88a <?DefaultClosestEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXIM@Z+0xba>
1010a816: ff 15 0c 65 4e 10            	call	dword ptr [0x104e650c]
1010a81c: 99                           	cdq
1010a81d: b9 64 00 00 00               	mov	ecx, 0x64
1010a822: f7 f9                        	idiv	ecx
1010a824: 3b 96 d8 02 00 00            	cmp	edx, dword ptr [esi + 0x2d8]
