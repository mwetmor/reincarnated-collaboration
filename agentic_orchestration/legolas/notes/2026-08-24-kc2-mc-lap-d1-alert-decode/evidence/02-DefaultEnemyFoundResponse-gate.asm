
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

1010a360 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z>:
1010a585: 6a 06                        	push	0x6
1010a587: 68 dc d5 52 10               	push	0x1052d5dc
1010a58c: 8d 4d b4                     	lea	ecx, [ebp - 0x4c]
1010a58f: c7 45 c8 0f 00 00 00         	mov	dword ptr [ebp - 0x38], 0xf
1010a596: c7 45 c4 00 00 00 00         	mov	dword ptr [ebp - 0x3c], 0x0
1010a59d: c6 45 b4 00                  	mov	byte ptr [ebp - 0x4c], 0x0
1010a5a1: e8 da e5 ef ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
1010a5a6: 8b 4b 04                     	mov	ecx, dword ptr [ebx + 0x4]
1010a5a9: 8d 45 b4                     	lea	eax, [ebp - 0x4c]
1010a5ac: 50                           	push	eax
1010a5ad: e8 ae e0 fd ff               	call	0x100e8660 <?IsInState@ControllerAI@GAME@@QAE_NABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@@Z>
1010a5b2: 8b 55 c8                     	mov	edx, dword ptr [ebp - 0x38]
1010a5b5: 88 45 f3                     	mov	byte ptr [ebp - 0xd], al
1010a5b8: 83 fa 10                     	cmp	edx, 0x10
1010a5bb: 72 11                        	jb	0x1010a5ce <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x26e>
1010a5bd: 8b 4d b4                     	mov	ecx, dword ptr [ebp - 0x4c]
1010a5c0: 42                           	inc	edx
1010a5c1: 6a 01                        	push	0x1
1010a5c3: e8 38 e7 ef ff               	call	0x10008d00 <??1AuraContainer@GAME@@QAE@XZ+0x40>
1010a5c8: 8a 45 f3                     	mov	al, byte ptr [ebp - 0xd]
1010a5cb: 83 c4 04                     	add	esp, 0x4
1010a5ce: 84 c0                        	test	al, al
1010a5d0: 0f 84 cd 01 00 00            	je	0x1010a7a3 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x443>
1010a5d6: 8b 43 08                     	mov	eax, dword ptr [ebx + 0x8]
1010a5d9: 85 c0                        	test	eax, eax
1010a5db: 75 12                        	jne	0x1010a5ef <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x28f>
1010a5dd: 8b 43 04                     	mov	eax, dword ptr [ebx + 0x4]
1010a5e0: ff 70 24                     	push	dword ptr [eax + 0x24]
1010a5e3: ff d7                        	call	edi
1010a5e5: 8b c8                        	mov	ecx, eax
1010a5e7: e8 d4 0a f0 ff               	call	0x1000b0c0 <?Reset@AchievementManager@GAME@@QAEXXZ+0xd00>
1010a5ec: 89 43 08                     	mov	dword ptr [ebx + 0x8], eax
1010a5ef: 8b b0 44 32 00 00            	mov	esi, dword ptr [eax + 0x3244]
1010a5f5: ff 15 0c 65 4e 10            	call	dword ptr [0x104e650c]
1010a5fb: 99                           	cdq
1010a5fc: b9 64 00 00 00               	mov	ecx, 0x64
1010a601: f7 f9                        	idiv	ecx
1010a603: 3b d6                        	cmp	edx, esi
1010a605: 0f 83 39 01 00 00            	jae	0x1010a744 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3e4>
1010a60b: 8b 43 08                     	mov	eax, dword ptr [ebx + 0x8]
1010a60e: 85 c0                        	test	eax, eax
1010a610: 75 12                        	jne	0x1010a624 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x2c4>
1010a612: 8b 43 04                     	mov	eax, dword ptr [ebx + 0x4]
1010a615: ff 70 24                     	push	dword ptr [eax + 0x24]
1010a618: ff d7                        	call	edi
1010a61a: 8b c8                        	mov	ecx, eax
1010a61c: e8 9f 0a f0 ff               	call	0x1000b0c0 <?Reset@AchievementManager@GAME@@QAEXXZ+0xd00>
1010a621: 89 43 08                     	mov	dword ptr [ebx + 0x8], eax
1010a624: 8b c8                        	mov	ecx, eax
1010a626: e8 55 c1 f3 ff               	call	0x10046780 <?GetAnimationSet@Character@GAME@@QBEPAVAnimationSet@2@XZ>
1010a62b: 8b 88 90 00 00 00            	mov	ecx, dword ptr [eax + 0x90]
1010a631: 8b 01                        	mov	eax, dword ptr [ecx]
1010a633: 8b 40 3c                     	mov	eax, dword ptr [eax + 0x3c]
1010a636: ff d0                        	call	eax
1010a638: 84 c0                        	test	al, al
1010a63a: 0f 85 04 01 00 00            	jne	0x1010a744 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3e4>
1010a640: ff 75 08                     	push	dword ptr [ebp + 0x8]
1010a643: ff d7                        	call	edi
1010a645: 8b c8                        	mov	ecx, eax
1010a647: e8 04 a7 f2 ff               	call	0x10034d50 <?CalculateAllocatedMemory@AuraManager@GAME@@QBEIXZ+0x370>
1010a64c: 89 45 ec                     	mov	dword ptr [ebp - 0x14], eax
1010a64f: 85 c0                        	test	eax, eax
1010a651: 0f 84 ed 00 00 00            	je	0x1010a744 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3e4>
1010a657: 8d 45 98                     	lea	eax, [ebp - 0x68]
1010a65a: 8b cb                        	mov	ecx, ebx
1010a65c: 50                           	push	eax
1010a65d: e8 5e 71 fc ff               	call	0x100d17c0 <?GetCharacter@?$ControllerAIStateT@VControllerTyphonChained@GAME@@VMonster@2@@GAME@@IBEABVMonster@2@XZ>
1010a662: 8b 35 88 52 4e 10            	mov	esi, dword ptr [0x104e5288]
1010a668: 8b c8                        	mov	ecx, eax
1010a66a: ff d6                        	call	esi
1010a66c: 8b 4d ec                     	mov	ecx, dword ptr [ebp - 0x14]
1010a66f: 50                           	push	eax
1010a670: 8d 45 8c                     	lea	eax, [ebp - 0x74]
1010a673: 50                           	push	eax
1010a674: 8d 85 44 ff ff ff            	lea	eax, [ebp - 0xbc]
1010a67a: 50                           	push	eax
1010a67b: ff d6                        	call	esi
1010a67d: 8b c8                        	mov	ecx, eax
1010a67f: ff 15 1c 55 4e 10            	call	dword ptr [0x104e551c]
1010a685: f3 0f 10 48 04               	movss	xmm1, dword ptr [eax + 0x4]
1010a68a: f3 0f 10 10                  	movss	xmm2, dword ptr [eax]
1010a68e: f3 0f 10 40 08               	movss	xmm0, dword ptr [eax + 0x8]
1010a693: f3 0f 59 d2                  	mulss	xmm2, xmm2
1010a697: f3 0f 59 c9                  	mulss	xmm1, xmm1
1010a69b: f3 0f 59 c0                  	mulss	xmm0, xmm0
1010a69f: f3 0f 58 d1                  	addss	xmm2, xmm1
1010a6a3: f3 0f 58 d0                  	addss	xmm2, xmm0
1010a6a7: 0f 57 c0                     	xorps	xmm0, xmm0
1010a6aa: 0f 2e d0                     	ucomiss	xmm2, xmm0
1010a6ad: 9f                           	lahf
1010a6ae: f6 c4 44                     	test	ah, 0x44
1010a6b1: 7b 07                        	jnp	0x1010a6ba <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x35a>
1010a6b3: 0f 57 c0                     	xorps	xmm0, xmm0
1010a6b6: f3 0f 51 c2                  	sqrtss	xmm0, xmm2
1010a6ba: a1 a4 80 80 10               	mov	eax, dword ptr [0x108080a4]
1010a6bf: 0f 2f 80 80 0c 00 00         	comiss	xmm0, dword ptr [eax + 0xc80]
1010a6c6: 76 7c                        	jbe	0x1010a744 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3e4>
1010a6c8: 8b 4b 04                     	mov	ecx, dword ptr [ebx + 0x4]
1010a6cb: 8b 75 08                     	mov	esi, dword ptr [ebp + 0x8]
1010a6ce: 81 c1 b8 02 00 00            	add	ecx, 0x2b8
1010a6d4: 56                           	push	esi
1010a6d5: e8 86 4c f0 ff               	call	0x1000f360 <?GetAngerDiff@AngerManager@GAME@@QBEMI@Z>
1010a6da: f3 0f 10 05 ac 58 5f 10      	movss	xmm0, dword ptr [0x105f58ac]
1010a6e2: d9 5d 08                     	fstp	dword ptr [ebp + 0x8]
1010a6e5: 0f 2f 45 08                  	comiss	xmm0, dword ptr [ebp + 0x8]
1010a6e9: 76 59                        	jbe	0x1010a744 <?DefaultEnemyFoundResponse@?$ControllerMonsterState@VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z+0x3e4>
1010a6eb: 68 fc d5 52 10               	push	0x1052d5fc
1010a6f0: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
1010a6f3: e8 88 1c f0 ff               	call	0x1000c380 <??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100>
1010a6f8: 8d 8d 78 ff ff ff            	lea	ecx, [ebp - 0x88]
1010a6fe: c7 45 fc 03 00 00 00         	mov	dword ptr [ebp - 0x4], 0x3
1010a705: ff 15 88 53 4e 10            	call	dword ptr [0x104e5388]
1010a70b: 8b 4b 04                     	mov	ecx, dword ptr [ebx + 0x4]
1010a70e: 89 75 b0                     	mov	dword ptr [ebp - 0x50], esi
1010a711: c7 45 b4 00 00 00 00         	mov	dword ptr [ebp - 0x4c], 0x0
1010a718: 0f 10 00                     	movups	xmm0, xmmword ptr [eax]
1010a71b: 8d 45 b0                     	lea	eax, [ebp - 0x50]
1010a71e: c7 45 b8 00 00 00 00         	mov	dword ptr [ebp - 0x48], 0x0
1010a725: 50                           	push	eax
1010a726: 8d 45 d0                     	lea	eax, [ebp - 0x30]
1010a729: 50                           	push	eax
