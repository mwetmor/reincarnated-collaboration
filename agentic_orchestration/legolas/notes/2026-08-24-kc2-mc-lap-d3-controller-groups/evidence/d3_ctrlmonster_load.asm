
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

100f6da0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z>:
100f6da0: 55                           	push	ebp
100f6da1: 8b ec                        	mov	ebp, esp
100f6da3: 6a ff                        	push	-0x1
100f6da5: 68 a8 7f 4c 10               	push	0x104c7fa8
100f6daa: 64 a1 00 00 00 00            	mov	eax, dword ptr fs:[0x0]
100f6db0: 50                           	push	eax
100f6db1: 64 89 25 00 00 00 00         	mov	dword ptr fs:[0x0], esp
100f6db8: 83 ec 3c                     	sub	esp, 0x3c
100f6dbb: 53                           	push	ebx
100f6dbc: 56                           	push	esi
100f6dbd: 8b 75 08                     	mov	esi, dword ptr [ebp + 0x8]
100f6dc0: 57                           	push	edi
100f6dc1: 51                           	push	ecx
100f6dc2: 8b f9                        	mov	edi, ecx
100f6dc4: c7 04 24 00 00 70 41         	mov	dword ptr [esp], 0x41700000
100f6dcb: 8b 06                        	mov	eax, dword ptr [esi]
100f6dcd: 8b ce                        	mov	ecx, esi
100f6dcf: 68 08 8e 52 10               	push	0x10528e08
100f6dd4: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f6dd7: ff d0                        	call	eax
100f6dd9: d9 9f 1c 02 00 00            	fstp	dword ptr [edi + 0x21c]
100f6ddf: 8b 06                        	mov	eax, dword ptr [esi]
100f6de1: 51                           	push	ecx
100f6de2: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f6de9: 8b ce                        	mov	ecx, esi
100f6deb: 68 50 8e 52 10               	push	0x10528e50
100f6df0: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f6df3: ff d0                        	call	eax
100f6df5: d9 9f 20 02 00 00            	fstp	dword ptr [edi + 0x220]
100f6dfb: c7 45 e4 0f 00 00 00         	mov	dword ptr [ebp - 0x1c], 0xf
100f6e02: c7 45 e0 00 00 00 00         	mov	dword ptr [ebp - 0x20], 0x0
100f6e09: c6 45 d0 00                  	mov	byte ptr [ebp - 0x30], 0x0
100f6e0d: c7 45 fc 00 00 00 00         	mov	dword ptr [ebp - 0x4], 0x0
100f6e14: 8b 06                        	mov	eax, dword ptr [esi]
100f6e16: 51                           	push	ecx
100f6e17: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f6e1e: 8b ce                        	mov	ecx, esi
100f6e20: 68 90 b9 52 10               	push	0x1052b990
100f6e25: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f6e28: ff d0                        	call	eax
100f6e2a: d8 0d 18 59 5f 10            	fmul	dword ptr [0x105f5918]
100f6e30: 51                           	push	ecx
100f6e31: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f6e38: 8b ce                        	mov	ecx, esi
100f6e3a: 68 80 b9 52 10               	push	0x1052b980
100f6e3f: d9 5d 08                     	fstp	dword ptr [ebp + 0x8]
100f6e42: f3 0f 2c 45 08               	cvttss2si	eax, dword ptr [ebp + 0x8]
100f6e47: 89 87 f0 02 00 00            	mov	dword ptr [edi + 0x2f0], eax
100f6e4d: 8b 06                        	mov	eax, dword ptr [esi]
100f6e4f: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f6e52: ff d0                        	call	eax
100f6e54: d8 0d 18 59 5f 10            	fmul	dword ptr [0x105f5918]
100f6e5a: d9 5d 08                     	fstp	dword ptr [ebp + 0x8]
100f6e5d: f3 0f 2c 55 08               	cvttss2si	edx, dword ptr [ebp + 0x8]
100f6e62: 89 97 f4 02 00 00            	mov	dword ptr [edi + 0x2f4], edx
100f6e68: 8b 0d a4 80 80 10            	mov	ecx, dword ptr [0x108080a4]
100f6e6e: 52                           	push	edx
100f6e6f: ff b7 f0 02 00 00            	push	dword ptr [edi + 0x2f0]
100f6e75: 8d 89 04 0c 00 00            	lea	ecx, [ecx + 0xc04]
100f6e7b: ff 15 44 55 4e 10            	call	dword ptr [0x104e5544]
100f6e81: 89 87 f8 02 00 00            	mov	dword ptr [edi + 0x2f8], eax
100f6e87: 8b ce                        	mov	ecx, esi
100f6e89: 8b 06                        	mov	eax, dword ptr [esi]
100f6e8b: 68 b8 0b 00 00               	push	0xbb8
100f6e90: 68 b0 b9 52 10               	push	0x1052b9b0
100f6e95: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f6e98: 89 87 10 03 00 00            	mov	dword ptr [edi + 0x310], eax
100f6e9e: 8b ce                        	mov	ecx, esi
100f6ea0: 8b 06                        	mov	eax, dword ptr [esi]
100f6ea2: 6a 02                        	push	0x2
100f6ea4: 68 a0 b9 52 10               	push	0x1052b9a0
100f6ea9: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f6eac: 89 87 0c 03 00 00            	mov	dword ptr [edi + 0x30c], eax
100f6eb2: 8b 06                        	mov	eax, dword ptr [esi]
100f6eb4: 51                           	push	ecx
100f6eb5: c7 04 24 00 00 a0 40         	mov	dword ptr [esp], 0x40a00000
100f6ebc: 8b ce                        	mov	ecx, esi
100f6ebe: 68 d4 b9 52 10               	push	0x1052b9d4
100f6ec3: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f6ec6: ff d0                        	call	eax
100f6ec8: d9 9f 18 03 00 00            	fstp	dword ptr [edi + 0x318]
100f6ece: 8b 06                        	mov	eax, dword ptr [esi]
100f6ed0: 8b ce                        	mov	ecx, esi
100f6ed2: 6a 00                        	push	0x0
100f6ed4: 68 bc b9 52 10               	push	0x1052b9bc
100f6ed9: 8b 40 2c                     	mov	eax, dword ptr [eax + 0x2c]
100f6edc: ff d0                        	call	eax
100f6ede: 88 87 1c 03 00 00            	mov	byte ptr [edi + 0x31c], al
100f6ee4: 8b 06                        	mov	eax, dword ptr [esi]
100f6ee6: 8b ce                        	mov	ecx, esi
100f6ee8: 6a 00                        	push	0x0
100f6eea: 68 f0 b9 52 10               	push	0x1052b9f0
100f6eef: 8b 40 2c                     	mov	eax, dword ptr [eax + 0x2c]
100f6ef2: ff d0                        	call	eax
100f6ef4: 88 87 a4 03 00 00            	mov	byte ptr [edi + 0x3a4], al
100f6efa: 8b ce                        	mov	ecx, esi
100f6efc: 8b 06                        	mov	eax, dword ptr [esi]
100f6efe: 68 e4 b9 52 10               	push	0x1052b9e4
100f6f03: 68 14 ba 52 10               	push	0x1052ba14
100f6f08: ff 50 14                     	call	dword ptr [eax + 0x14]
100f6f0b: 8b d0                        	mov	edx, eax
100f6f0d: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f6f10: 75 04                        	jne	0x100f6f16 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x176>
100f6f12: 33 c9                        	xor	ecx, ecx
100f6f14: eb 13                        	jmp	0x100f6f29 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x189>
100f6f16: 8b ca                        	mov	ecx, edx
100f6f18: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f6f1b: 0f 1f 44 00 00               	nop	dword ptr [eax + eax]
100f6f20: 8a 01                        	mov	al, byte ptr [ecx]
100f6f22: 41                           	inc	ecx
100f6f23: 84 c0                        	test	al, al
100f6f25: 75 f9                        	jne	0x100f6f20 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x180>
100f6f27: 2b cb                        	sub	ecx, ebx
100f6f29: 51                           	push	ecx
100f6f2a: 52                           	push	edx
100f6f2b: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6f2e: e8 4d 1c f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f6f33: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f6f37: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6f3a: 8b 5d e0                     	mov	ebx, dword ptr [ebp - 0x20]
100f6f3d: b8 09 00 00 00               	mov	eax, 0x9
100f6f42: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f6f46: ba 08 ba 52 10               	mov	edx, 0x1052ba08
100f6f4b: 3b d8                        	cmp	ebx, eax
100f6f4d: 0f 42 c3                     	cmovb	eax, ebx
100f6f50: 50                           	push	eax
100f6f51: e8 ea 4d f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f6f56: 83 c4 04                     	add	esp, 0x4
100f6f59: 85 c0                        	test	eax, eax
100f6f5b: 75 0f                        	jne	0x100f6f6c <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x1cc>
100f6f5d: 83 fb 09                     	cmp	ebx, 0x9
100f6f60: 72 0a                        	jb	0x100f6f6c <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x1cc>
100f6f62: 77 08                        	ja	0x100f6f6c <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x1cc>
100f6f64: 89 87 04 03 00 00            	mov	dword ptr [edi + 0x304], eax
100f6f6a: eb 55                        	jmp	0x100f6fc1 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x221>
100f6f6c: ba 34 ba 52 10               	mov	edx, 0x1052ba34
100f6f71: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6f74: e8 27 4e f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f6f79: 84 c0                        	test	al, al
100f6f7b: 74 0c                        	je	0x100f6f89 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x1e9>
100f6f7d: c7 87 04 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x304], 0x1
100f6f87: eb 38                        	jmp	0x100f6fc1 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x221>
100f6f89: ba 24 ba 52 10               	mov	edx, 0x1052ba24
100f6f8e: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6f91: e8 0a 4e f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f6f96: 84 c0                        	test	al, al
100f6f98: 74 0c                        	je	0x100f6fa6 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x206>
100f6f9a: c7 87 04 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x304], 0x2
100f6fa4: eb 1b                        	jmp	0x100f6fc1 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x221>
100f6fa6: ba 54 ba 52 10               	mov	edx, 0x1052ba54
100f6fab: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6fae: e8 ed 4d f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f6fb3: 84 c0                        	test	al, al
100f6fb5: 74 0a                        	je	0x100f6fc1 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x221>
100f6fb7: c7 87 04 03 00 00 03 00 00 00	mov	dword ptr [edi + 0x304], 0x3
100f6fc1: 8b 06                        	mov	eax, dword ptr [esi]
100f6fc3: 8b ce                        	mov	ecx, esi
100f6fc5: 68 44 ba 52 10               	push	0x1052ba44
100f6fca: 68 78 ba 52 10               	push	0x1052ba78
100f6fcf: ff 50 14                     	call	dword ptr [eax + 0x14]
100f6fd2: 8b d0                        	mov	edx, eax
100f6fd4: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f6fd7: 75 04                        	jne	0x100f6fdd <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x23d>
100f6fd9: 33 c9                        	xor	ecx, ecx
100f6fdb: eb 0e                        	jmp	0x100f6feb <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x24b>
100f6fdd: 8b ca                        	mov	ecx, edx
100f6fdf: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f6fe2: 8a 01                        	mov	al, byte ptr [ecx]
100f6fe4: 41                           	inc	ecx
100f6fe5: 84 c0                        	test	al, al
100f6fe7: 75 f9                        	jne	0x100f6fe2 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x242>
100f6fe9: 2b cb                        	sub	ecx, ebx
100f6feb: 51                           	push	ecx
100f6fec: 52                           	push	edx
100f6fed: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6ff0: e8 8b 1b f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f6ff5: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f6ff9: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f6ffc: bb 0d 00 00 00               	mov	ebx, 0xd
100f7001: ba 68 ba 52 10               	mov	edx, 0x1052ba68
100f7006: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f700a: 8b c3                        	mov	eax, ebx
100f700c: 39 45 e0                     	cmp	dword ptr [ebp - 0x20], eax
100f700f: 0f 42 45 e0                  	cmovb	eax, dword ptr [ebp - 0x20]
100f7013: 50                           	push	eax
100f7014: e8 27 4d f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f7019: 83 c4 04                     	add	esp, 0x4
100f701c: 85 c0                        	test	eax, eax
100f701e: 75 15                        	jne	0x100f7035 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x295>
100f7020: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f7023: 3b c3                        	cmp	eax, ebx
100f7025: 72 0e                        	jb	0x100f7035 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x295>
100f7027: 77 0c                        	ja	0x100f7035 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x295>
100f7029: c7 87 08 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x308], 0x0
100f7033: eb 38                        	jmp	0x100f706d <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x2cd>
100f7035: ba 90 ba 52 10               	mov	edx, 0x1052ba90
100f703a: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f703d: e8 5e 4d f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f7042: 84 c0                        	test	al, al
100f7044: 74 0c                        	je	0x100f7052 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x2b2>
100f7046: c7 87 08 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x308], 0x1
100f7050: eb 1b                        	jmp	0x100f706d <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x2cd>
100f7052: ba 84 ba 52 10               	mov	edx, 0x1052ba84
100f7057: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f705a: e8 41 4d f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f705f: 84 c0                        	test	al, al
100f7061: 74 0a                        	je	0x100f706d <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x2cd>
100f7063: c7 87 08 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x308], 0x2
100f706d: 8b 06                        	mov	eax, dword ptr [esi]
100f706f: 8b ce                        	mov	ecx, esi
100f7071: 6a 03                        	push	0x3
100f7073: 68 ac ba 52 10               	push	0x1052baac
100f7078: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f707b: 89 87 0c 03 00 00            	mov	dword ptr [edi + 0x30c], eax
100f7081: 8b ce                        	mov	ecx, esi
100f7083: 8b 06                        	mov	eax, dword ptr [esi]
100f7085: 68 d0 07 00 00               	push	0x7d0
100f708a: 68 a0 ba 52 10               	push	0x1052baa0
100f708f: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7092: 89 87 14 03 00 00            	mov	dword ptr [edi + 0x314], eax
100f7098: 8b ce                        	mov	ecx, esi
100f709a: 8b 06                        	mov	eax, dword ptr [esi]
100f709c: 6a 64                        	push	0x64
100f709e: 68 d0 ba 52 10               	push	0x1052bad0
100f70a3: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f70a6: 89 87 d8 02 00 00            	mov	dword ptr [edi + 0x2d8], eax
100f70ac: 8b 06                        	mov	eax, dword ptr [esi]
100f70ae: 51                           	push	ecx
100f70af: c7 04 24 00 00 a0 40         	mov	dword ptr [esp], 0x40a00000
100f70b6: 8b ce                        	mov	ecx, esi
100f70b8: 68 bc ba 52 10               	push	0x1052babc
100f70bd: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f70c0: ff d0                        	call	eax
100f70c2: d9 9f 88 03 00 00            	fstp	dword ptr [edi + 0x388]
100f70c8: 8b 06                        	mov	eax, dword ptr [esi]
100f70ca: 51                           	push	ecx
100f70cb: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f70d2: 8b ce                        	mov	ecx, esi
100f70d4: 68 e8 ba 52 10               	push	0x1052bae8
100f70d9: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f70dc: ff d0                        	call	eax
100f70de: d9 9f 8c 03 00 00            	fstp	dword ptr [edi + 0x38c]
100f70e4: 8b 06                        	mov	eax, dword ptr [esi]
100f70e6: 8b ce                        	mov	ecx, esi
100f70e8: 68 10 27 00 00               	push	0x2710
100f70ed: 68 dc ba 52 10               	push	0x1052badc
100f70f2: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f70f5: 3d e8 03 00 00               	cmp	eax, 0x3e8
100f70fa: b9 40 1f 00 00               	mov	ecx, 0x1f40
100f70ff: 51                           	push	ecx
100f7100: 0f 4c c1                     	cmovl	eax, ecx
100f7103: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f710a: 89 87 fc 02 00 00            	mov	dword ptr [edi + 0x2fc], eax
100f7110: 8b ce                        	mov	ecx, esi
100f7112: 8b 06                        	mov	eax, dword ptr [esi]
100f7114: 68 08 bb 52 10               	push	0x1052bb08
100f7119: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f711c: ff d0                        	call	eax
100f711e: d9 9f 00 03 00 00            	fstp	dword ptr [edi + 0x300]
100f7124: 8b 06                        	mov	eax, dword ptr [esi]
100f7126: 8b ce                        	mov	ecx, esi
100f7128: 68 fc ba 52 10               	push	0x1052bafc
100f712d: 68 28 bb 52 10               	push	0x1052bb28
100f7132: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7135: 8b d0                        	mov	edx, eax
100f7137: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f713a: 75 04                        	jne	0x100f7140 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3a0>
100f713c: 33 c9                        	xor	ecx, ecx
100f713e: eb 12                        	jmp	0x100f7152 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3b2>
100f7140: 8b ca                        	mov	ecx, edx
100f7142: 8d 41 01                     	lea	eax, [ecx + 0x1]
100f7145: 89 45 08                     	mov	dword ptr [ebp + 0x8], eax
100f7148: 8a 01                        	mov	al, byte ptr [ecx]
100f714a: 41                           	inc	ecx
100f714b: 84 c0                        	test	al, al
100f714d: 75 f9                        	jne	0x100f7148 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3a8>
100f714f: 2b 4d 08                     	sub	ecx, dword ptr [ebp + 0x8]
100f7152: 51                           	push	ecx
100f7153: 52                           	push	edx
100f7154: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7157: e8 24 1a f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f715c: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f7160: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7163: b8 09 00 00 00               	mov	eax, 0x9
100f7168: ba 1c bb 52 10               	mov	edx, 0x1052bb1c
100f716d: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f7171: 39 45 e0                     	cmp	dword ptr [ebp - 0x20], eax
100f7174: 0f 42 45 e0                  	cmovb	eax, dword ptr [ebp - 0x20]
100f7178: 50                           	push	eax
100f7179: e8 c2 4b f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f717e: 83 c4 04                     	add	esp, 0x4
100f7181: 85 c0                        	test	eax, eax
100f7183: 75 16                        	jne	0x100f719b <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3fb>
100f7185: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f7188: 83 f8 09                     	cmp	eax, 0x9
100f718b: 72 0e                        	jb	0x100f719b <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3fb>
100f718d: 77 0c                        	ja	0x100f719b <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x3fb>
100f718f: c7 87 20 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x320], 0x0
100f7199: eb 1b                        	jmp	0x100f71b6 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x416>
100f719b: ba 48 bb 52 10               	mov	edx, 0x1052bb48
100f71a0: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f71a3: e8 f8 4b f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f71a8: 84 c0                        	test	al, al
100f71aa: 74 0a                        	je	0x100f71b6 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x416>
100f71ac: c7 87 20 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x320], 0x1
100f71b6: 8b 06                        	mov	eax, dword ptr [esi]
100f71b8: 51                           	push	ecx
100f71b9: c7 04 24 00 00 00 40         	mov	dword ptr [esp], 0x40000000
100f71c0: 8b ce                        	mov	ecx, esi
100f71c2: 68 38 bb 52 10               	push	0x1052bb38
100f71c7: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f71ca: ff d0                        	call	eax
100f71cc: d9 9f 9c 03 00 00            	fstp	dword ptr [edi + 0x39c]
100f71d2: 8b 06                        	mov	eax, dword ptr [esi]
100f71d4: 51                           	push	ecx
100f71d5: c7 04 24 00 00 20 41         	mov	dword ptr [esp], 0x41200000
100f71dc: 8b ce                        	mov	ecx, esi
100f71de: 68 64 bb 52 10               	push	0x1052bb64
100f71e3: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f71e6: ff d0                        	call	eax
100f71e8: d9 9f 74 03 00 00            	fstp	dword ptr [edi + 0x374]
100f71ee: 8b 06                        	mov	eax, dword ptr [esi]
100f71f0: 8b ce                        	mov	ecx, esi
100f71f2: 68 b8 0b 00 00               	push	0xbb8
100f71f7: 68 50 bb 52 10               	push	0x1052bb50
100f71fc: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f71ff: 89 87 94 03 00 00            	mov	dword ptr [edi + 0x394], eax
100f7205: 8b ce                        	mov	ecx, esi
100f7207: 8b 06                        	mov	eax, dword ptr [esi]
100f7209: 68 10 27 00 00               	push	0x2710
100f720e: 68 88 bb 52 10               	push	0x1052bb88
100f7213: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7216: 89 87 98 03 00 00            	mov	dword ptr [edi + 0x398], eax
100f721c: 8b 06                        	mov	eax, dword ptr [esi]
100f721e: 51                           	push	ecx
100f721f: c7 04 24 00 00 00 40         	mov	dword ptr [esp], 0x40000000
100f7226: 8b ce                        	mov	ecx, esi
100f7228: 68 74 bb 52 10               	push	0x1052bb74
100f722d: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7230: ff d0                        	call	eax
100f7232: d9 9f a0 03 00 00            	fstp	dword ptr [edi + 0x3a0]
100f7238: 8b 06                        	mov	eax, dword ptr [esi]
100f723a: 51                           	push	ecx
100f723b: c7 04 24 00 00 a0 40         	mov	dword ptr [esp], 0x40a00000
100f7242: 8b ce                        	mov	ecx, esi
100f7244: 68 b8 bb 52 10               	push	0x1052bbb8
100f7249: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f724c: ff d0                        	call	eax
100f724e: d9 9f 70 03 00 00            	fstp	dword ptr [edi + 0x370]
100f7254: 8b 06                        	mov	eax, dword ptr [esi]
100f7256: 51                           	push	ecx
100f7257: c7 04 24 00 00 a0 41         	mov	dword ptr [esp], 0x41a00000
100f725e: 8b ce                        	mov	ecx, esi
100f7260: 68 9c bb 52 10               	push	0x1052bb9c
100f7265: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7268: ff d0                        	call	eax
100f726a: d9 9f 78 03 00 00            	fstp	dword ptr [edi + 0x378]
100f7270: 8b 06                        	mov	eax, dword ptr [esi]
100f7272: 8b ce                        	mov	ecx, esi
100f7274: 68 dc bb 52 10               	push	0x1052bbdc
100f7279: 68 c8 bb 52 10               	push	0x1052bbc8
100f727e: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7281: 8b d0                        	mov	edx, eax
100f7283: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7286: 75 04                        	jne	0x100f728c <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x4ec>
100f7288: 33 c9                        	xor	ecx, ecx
100f728a: eb 12                        	jmp	0x100f729e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x4fe>
100f728c: 8b ca                        	mov	ecx, edx
100f728e: 8d 41 01                     	lea	eax, [ecx + 0x1]
100f7291: 89 45 08                     	mov	dword ptr [ebp + 0x8], eax
100f7294: 8a 01                        	mov	al, byte ptr [ecx]
100f7296: 41                           	inc	ecx
100f7297: 84 c0                        	test	al, al
100f7299: 75 f9                        	jne	0x100f7294 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x4f4>
100f729b: 2b 4d 08                     	sub	ecx, dword ptr [ebp + 0x8]
100f729e: 51                           	push	ecx
100f729f: 52                           	push	edx
100f72a0: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f72a3: e8 d8 18 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f72a8: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f72ac: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f72af: 8b c3                        	mov	eax, ebx
100f72b1: ba f8 bb 52 10               	mov	edx, 0x1052bbf8
100f72b6: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f72ba: 39 45 e0                     	cmp	dword ptr [ebp - 0x20], eax
100f72bd: 0f 42 45 e0                  	cmovb	eax, dword ptr [ebp - 0x20]
100f72c1: 50                           	push	eax
100f72c2: e8 79 4a f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f72c7: 83 c4 04                     	add	esp, 0x4
100f72ca: 85 c0                        	test	eax, eax
100f72cc: 75 16                        	jne	0x100f72e4 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x544>
100f72ce: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f72d1: 83 f8 0d                     	cmp	eax, 0xd
100f72d4: 72 0e                        	jb	0x100f72e4 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x544>
100f72d6: 77 0c                        	ja	0x100f72e4 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x544>
100f72d8: c7 87 24 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x324], 0x0
100f72e2: eb 55                        	jmp	0x100f7339 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x599>
100f72e4: ba ec bb 52 10               	mov	edx, 0x1052bbec
100f72e9: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f72ec: e8 af 4a f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f72f1: 84 c0                        	test	al, al
100f72f3: 74 0c                        	je	0x100f7301 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x561>
100f72f5: c7 87 24 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x324], 0x1
100f72ff: eb 38                        	jmp	0x100f7339 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x599>
100f7301: ba 1c bc 52 10               	mov	edx, 0x1052bc1c
100f7306: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7309: e8 92 4a f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f730e: 84 c0                        	test	al, al
100f7310: 74 0c                        	je	0x100f731e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x57e>
100f7312: c7 87 24 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x324], 0x2
100f731c: eb 1b                        	jmp	0x100f7339 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x599>
100f731e: ba 08 bc 52 10               	mov	edx, 0x1052bc08
100f7323: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7326: e8 75 4a f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f732b: 84 c0                        	test	al, al
100f732d: 74 0a                        	je	0x100f7339 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x599>
100f732f: c7 87 24 03 00 00 03 00 00 00	mov	dword ptr [edi + 0x324], 0x3
100f7339: 8b 06                        	mov	eax, dword ptr [esi]
100f733b: 8b ce                        	mov	ecx, esi
100f733d: 68 40 bc 52 10               	push	0x1052bc40
100f7342: 68 2c bc 52 10               	push	0x1052bc2c
100f7347: ff 50 14                     	call	dword ptr [eax + 0x14]
100f734a: 8b d0                        	mov	edx, eax
100f734c: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f734f: 75 04                        	jne	0x100f7355 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x5b5>
100f7351: 33 c9                        	xor	ecx, ecx
100f7353: eb 15                        	jmp	0x100f736a <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x5ca>
100f7355: 8b ca                        	mov	ecx, edx
100f7357: 8d 41 01                     	lea	eax, [ecx + 0x1]
100f735a: 89 45 08                     	mov	dword ptr [ebp + 0x8], eax
100f735d: 0f 1f 00                     	nop	dword ptr [eax]
100f7360: 8a 01                        	mov	al, byte ptr [ecx]
100f7362: 41                           	inc	ecx
100f7363: 84 c0                        	test	al, al
100f7365: 75 f9                        	jne	0x100f7360 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x5c0>
100f7367: 2b 4d 08                     	sub	ecx, dword ptr [ebp + 0x8]
100f736a: 51                           	push	ecx
100f736b: 52                           	push	edx
100f736c: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f736f: e8 0c 18 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7374: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f7378: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f737b: 8b c3                        	mov	eax, ebx
100f737d: ba 5c bc 52 10               	mov	edx, 0x1052bc5c
100f7382: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f7386: 39 45 e0                     	cmp	dword ptr [ebp - 0x20], eax
100f7389: 0f 42 45 e0                  	cmovb	eax, dword ptr [ebp - 0x20]
100f738d: 50                           	push	eax
100f738e: e8 ad 49 f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f7393: 83 c4 04                     	add	esp, 0x4
100f7396: 85 c0                        	test	eax, eax
100f7398: 75 16                        	jne	0x100f73b0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x610>
100f739a: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f739d: 83 f8 0d                     	cmp	eax, 0xd
100f73a0: 72 0e                        	jb	0x100f73b0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x610>
100f73a2: 77 0c                        	ja	0x100f73b0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x610>
100f73a4: c7 87 28 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x328], 0x0
100f73ae: eb 55                        	jmp	0x100f7405 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x665>
100f73b0: ba 50 bc 52 10               	mov	edx, 0x1052bc50
100f73b5: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f73b8: e8 e3 49 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f73bd: 84 c0                        	test	al, al
100f73bf: 74 0c                        	je	0x100f73cd <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x62d>
100f73c1: c7 87 28 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x328], 0x1
100f73cb: eb 38                        	jmp	0x100f7405 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x665>
100f73cd: ba 80 bc 52 10               	mov	edx, 0x1052bc80
100f73d2: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f73d5: e8 c6 49 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f73da: 84 c0                        	test	al, al
100f73dc: 74 0c                        	je	0x100f73ea <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x64a>
100f73de: c7 87 28 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x328], 0x2
100f73e8: eb 1b                        	jmp	0x100f7405 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x665>
100f73ea: ba 6c bc 52 10               	mov	edx, 0x1052bc6c
100f73ef: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f73f2: e8 a9 49 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f73f7: 84 c0                        	test	al, al
100f73f9: 74 0a                        	je	0x100f7405 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x665>
100f73fb: c7 87 28 03 00 00 03 00 00 00	mov	dword ptr [edi + 0x328], 0x3
100f7405: 8b 06                        	mov	eax, dword ptr [esi]
100f7407: 8b ce                        	mov	ecx, esi
100f7409: 68 a4 bc 52 10               	push	0x1052bca4
100f740e: 68 90 bc 52 10               	push	0x1052bc90
100f7413: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7416: 8b d0                        	mov	edx, eax
100f7418: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f741b: 75 04                        	jne	0x100f7421 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x681>
100f741d: 33 c9                        	xor	ecx, ecx
100f741f: eb 19                        	jmp	0x100f743a <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x69a>
100f7421: 8b ca                        	mov	ecx, edx
100f7423: 8d 41 01                     	lea	eax, [ecx + 0x1]
100f7426: 89 45 08                     	mov	dword ptr [ebp + 0x8], eax
100f7429: 0f 1f 80 00 00 00 00         	nop	dword ptr [eax]
100f7430: 8a 01                        	mov	al, byte ptr [ecx]
100f7432: 41                           	inc	ecx
100f7433: 84 c0                        	test	al, al
100f7435: 75 f9                        	jne	0x100f7430 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x690>
100f7437: 2b 4d 08                     	sub	ecx, dword ptr [ebp + 0x8]
100f743a: 51                           	push	ecx
100f743b: 52                           	push	edx
100f743c: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f743f: e8 3c 17 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7444: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f7448: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f744b: b8 0b 00 00 00               	mov	eax, 0xb
100f7450: ba c0 bc 52 10               	mov	edx, 0x1052bcc0
100f7455: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f7459: 39 45 e0                     	cmp	dword ptr [ebp - 0x20], eax
100f745c: 0f 42 45 e0                  	cmovb	eax, dword ptr [ebp - 0x20]
100f7460: 50                           	push	eax
100f7461: e8 da 48 f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f7466: 83 c4 04                     	add	esp, 0x4
100f7469: 85 c0                        	test	eax, eax
100f746b: 75 16                        	jne	0x100f7483 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x6e3>
100f746d: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f7470: 83 f8 0b                     	cmp	eax, 0xb
100f7473: 72 0e                        	jb	0x100f7483 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x6e3>
100f7475: 77 0c                        	ja	0x100f7483 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x6e3>
100f7477: c7 87 2c 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x32c], 0x0
100f7481: eb 38                        	jmp	0x100f74bb <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x71b>
100f7483: ba b0 bc 52 10               	mov	edx, 0x1052bcb0
100f7488: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f748b: e8 10 49 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f7490: 84 c0                        	test	al, al
100f7492: 74 0c                        	je	0x100f74a0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x700>
100f7494: c7 87 2c 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x32c], 0x1
100f749e: eb 1b                        	jmp	0x100f74bb <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x71b>
100f74a0: ba dc bc 52 10               	mov	edx, 0x1052bcdc
100f74a5: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f74a8: e8 f3 48 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f74ad: 84 c0                        	test	al, al
100f74af: 74 0a                        	je	0x100f74bb <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x71b>
100f74b1: c7 87 2c 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x32c], 0x2
100f74bb: 8b 06                        	mov	eax, dword ptr [esi]
100f74bd: 8b ce                        	mov	ecx, esi
100f74bf: 68 cc bc 52 10               	push	0x1052bccc
100f74c4: 68 f8 bc 52 10               	push	0x1052bcf8
100f74c9: ff 50 14                     	call	dword ptr [eax + 0x14]
100f74cc: 8b d0                        	mov	edx, eax
100f74ce: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f74d1: 75 04                        	jne	0x100f74d7 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x737>
100f74d3: 33 c9                        	xor	ecx, ecx
100f74d5: eb 13                        	jmp	0x100f74ea <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x74a>
100f74d7: 8b ca                        	mov	ecx, edx
100f74d9: 8d 41 01                     	lea	eax, [ecx + 0x1]
100f74dc: 89 45 08                     	mov	dword ptr [ebp + 0x8], eax
100f74df: 90                           	nop
100f74e0: 8a 01                        	mov	al, byte ptr [ecx]
100f74e2: 41                           	inc	ecx
100f74e3: 84 c0                        	test	al, al
100f74e5: 75 f9                        	jne	0x100f74e0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x740>
100f74e7: 2b 4d 08                     	sub	ecx, dword ptr [ebp + 0x8]
100f74ea: 51                           	push	ecx
100f74eb: 52                           	push	edx
100f74ec: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f74ef: e8 8c 16 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f74f4: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f74f8: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f74fb: ba e8 bc 52 10               	mov	edx, 0x1052bce8
100f7500: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f7504: 39 5d e0                     	cmp	dword ptr [ebp - 0x20], ebx
100f7507: 0f 42 5d e0                  	cmovb	ebx, dword ptr [ebp - 0x20]
100f750b: 53                           	push	ebx
100f750c: e8 2f 48 f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f7511: 83 c4 04                     	add	esp, 0x4
100f7514: 85 c0                        	test	eax, eax
100f7516: 75 16                        	jne	0x100f752e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x78e>
100f7518: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
100f751b: 83 f8 0d                     	cmp	eax, 0xd
100f751e: 72 0e                        	jb	0x100f752e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x78e>
100f7520: 77 0c                        	ja	0x100f752e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x78e>
100f7522: c7 87 30 03 00 00 00 00 00 00	mov	dword ptr [edi + 0x330], 0x0
100f752c: eb 38                        	jmp	0x100f7566 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x7c6>
100f752e: ba 1c bd 52 10               	mov	edx, 0x1052bd1c
100f7533: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7536: e8 65 48 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f753b: 84 c0                        	test	al, al
100f753d: 74 0c                        	je	0x100f754b <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x7ab>
100f753f: c7 87 30 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x330], 0x1
100f7549: eb 1b                        	jmp	0x100f7566 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x7c6>
100f754b: ba 0c bd 52 10               	mov	edx, 0x1052bd0c
100f7550: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f7553: e8 48 48 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f7558: 84 c0                        	test	al, al
100f755a: 74 0a                        	je	0x100f7566 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x7c6>
100f755c: c7 87 30 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x330], 0x2
100f7566: 8b 06                        	mov	eax, dword ptr [esi]
100f7568: 8b ce                        	mov	ecx, esi
100f756a: 6a 64                        	push	0x64
100f756c: 68 28 bd 52 10               	push	0x1052bd28
100f7571: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7574: 89 87 38 03 00 00            	mov	dword ptr [edi + 0x338], eax
100f757a: 8b ce                        	mov	ecx, esi
100f757c: 8b 06                        	mov	eax, dword ptr [esi]
100f757e: 68 c3 0b 4f 10               	push	0x104f0bc3
100f7583: 68 58 bd 52 10               	push	0x1052bd58
100f7588: ff 50 14                     	call	dword ptr [eax + 0x14]
100f758b: 8b d0                        	mov	edx, eax
100f758d: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7590: 75 04                        	jne	0x100f7596 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x7f6>
100f7592: 33 c9                        	xor	ecx, ecx
100f7594: eb 13                        	jmp	0x100f75a9 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x809>
100f7596: 8b ca                        	mov	ecx, edx
100f7598: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f759b: 0f 1f 44 00 00               	nop	dword ptr [eax + eax]
100f75a0: 8a 01                        	mov	al, byte ptr [ecx]
100f75a2: 41                           	inc	ecx
100f75a3: 84 c0                        	test	al, al
100f75a5: 75 f9                        	jne	0x100f75a0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x800>
100f75a7: 2b cb                        	sub	ecx, ebx
100f75a9: 51                           	push	ecx
100f75aa: 52                           	push	edx
100f75ab: 8d 8f 3c 03 00 00            	lea	ecx, [edi + 0x33c]
100f75b1: e8 ca 15 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f75b6: 8b 06                        	mov	eax, dword ptr [esi]
100f75b8: 8b ce                        	mov	ecx, esi
100f75ba: 68 48 bd 52 10               	push	0x1052bd48
100f75bf: 68 84 bd 52 10               	push	0x1052bd84
100f75c4: ff 50 14                     	call	dword ptr [eax + 0x14]
100f75c7: 8b d0                        	mov	edx, eax
100f75c9: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f75cc: 75 04                        	jne	0x100f75d2 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x832>
100f75ce: 33 c9                        	xor	ecx, ecx
100f75d0: eb 0e                        	jmp	0x100f75e0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x840>
100f75d2: 8b ca                        	mov	ecx, edx
100f75d4: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f75d7: 8a 01                        	mov	al, byte ptr [ecx]
100f75d9: 41                           	inc	ecx
100f75da: 84 c0                        	test	al, al
100f75dc: 75 f9                        	jne	0x100f75d7 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x837>
100f75de: 2b cb                        	sub	ecx, ebx
100f75e0: 51                           	push	ecx
100f75e1: 52                           	push	edx
100f75e2: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f75e5: e8 96 15 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f75ea: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f75ee: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f75f1: 8b 5d e0                     	mov	ebx, dword ptr [ebp - 0x20]
100f75f4: b8 12 00 00 00               	mov	eax, 0x12
100f75f9: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f75fd: ba 70 bd 52 10               	mov	edx, 0x1052bd70
100f7602: 3b d8                        	cmp	ebx, eax
100f7604: 0f 42 c3                     	cmovb	eax, ebx
100f7607: 50                           	push	eax
100f7608: e8 33 47 f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f760d: 83 c4 04                     	add	esp, 0x4
100f7610: 85 c0                        	test	eax, eax
100f7612: 75 0f                        	jne	0x100f7623 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x883>
100f7614: 83 fb 12                     	cmp	ebx, 0x12
100f7617: 72 0a                        	jb	0x100f7623 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x883>
100f7619: 77 08                        	ja	0x100f7623 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x883>
100f761b: 89 87 54 03 00 00            	mov	dword ptr [edi + 0x354], eax
100f7621: eb 1d                        	jmp	0x100f7640 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x8a0>
100f7623: ba ac bd 52 10               	mov	edx, 0x1052bdac
100f7628: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f762b: e8 70 47 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f7630: 0f b6 c0                     	movzx	eax, al
100f7633: f7 d8                        	neg	eax
100f7635: 1b c0                        	sbb	eax, eax
100f7637: 83 c0 02                     	add	eax, 0x2
100f763a: 89 87 54 03 00 00            	mov	dword ptr [edi + 0x354], eax
100f7640: 8b 06                        	mov	eax, dword ptr [esi]
100f7642: 8b ce                        	mov	ecx, esi
100f7644: 68 a0 bd 52 10               	push	0x1052bda0
100f7649: 68 cc bd 52 10               	push	0x1052bdcc
100f764e: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7651: 8b d0                        	mov	edx, eax
100f7653: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7656: 75 04                        	jne	0x100f765c <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x8bc>
100f7658: 33 c9                        	xor	ecx, ecx
100f765a: eb 0e                        	jmp	0x100f766a <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x8ca>
100f765c: 8b ca                        	mov	ecx, edx
100f765e: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f7661: 8a 01                        	mov	al, byte ptr [ecx]
100f7663: 41                           	inc	ecx
100f7664: 84 c0                        	test	al, al
100f7666: 75 f9                        	jne	0x100f7661 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x8c1>
100f7668: 2b cb                        	sub	ecx, ebx
100f766a: 51                           	push	ecx
100f766b: 52                           	push	edx
100f766c: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f766f: e8 0c 15 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7674: 83 7d e4 10                  	cmp	dword ptr [ebp - 0x1c], 0x10
100f7678: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f767b: 8b 5d e0                     	mov	ebx, dword ptr [ebp - 0x20]
100f767e: b8 09 00 00 00               	mov	eax, 0x9
100f7683: 0f 43 4d d0                  	cmovae	ecx, dword ptr [ebp - 0x30]
100f7687: ba c0 bd 52 10               	mov	edx, 0x1052bdc0
100f768c: 83 fb 09                     	cmp	ebx, 0x9
100f768f: 0f 42 c3                     	cmovb	eax, ebx
100f7692: 50                           	push	eax
100f7693: e8 a8 46 f1 ff               	call	0x1000bd40 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x20>
100f7698: 83 c4 04                     	add	esp, 0x4
100f769b: 85 c0                        	test	eax, eax
100f769d: 75 0f                        	jne	0x100f76ae <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x90e>
100f769f: 83 fb 09                     	cmp	ebx, 0x9
100f76a2: 72 0a                        	jb	0x100f76ae <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x90e>
100f76a4: 77 08                        	ja	0x100f76ae <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x90e>
100f76a6: 89 87 60 03 00 00            	mov	dword ptr [edi + 0x360], eax
100f76ac: eb 55                        	jmp	0x100f7703 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x963>
100f76ae: ba f0 bd 52 10               	mov	edx, 0x1052bdf0
100f76b3: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f76b6: e8 e5 46 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f76bb: 84 c0                        	test	al, al
100f76bd: 74 0c                        	je	0x100f76cb <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x92b>
100f76bf: c7 87 60 03 00 00 01 00 00 00	mov	dword ptr [edi + 0x360], 0x1
100f76c9: eb 38                        	jmp	0x100f7703 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x963>
100f76cb: ba dc bd 52 10               	mov	edx, 0x1052bddc
100f76d0: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f76d3: e8 c8 46 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f76d8: 84 c0                        	test	al, al
100f76da: 74 0c                        	je	0x100f76e8 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x948>
100f76dc: c7 87 60 03 00 00 02 00 00 00	mov	dword ptr [edi + 0x360], 0x2
100f76e6: eb 1b                        	jmp	0x100f7703 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x963>
100f76e8: ba 10 be 52 10               	mov	edx, 0x1052be10
100f76ed: 8d 4d d0                     	lea	ecx, [ebp - 0x30]
100f76f0: e8 ab 46 f1 ff               	call	0x1000bda0 <??0ScriptableConditionCollection@GAME@@QAE@XZ+0x80>
100f76f5: 84 c0                        	test	al, al
100f76f7: 74 0a                        	je	0x100f7703 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0x963>
100f76f9: c7 87 60 03 00 00 03 00 00 00	mov	dword ptr [edi + 0x360], 0x3
100f7703: 8b 06                        	mov	eax, dword ptr [esi]
100f7705: 51                           	push	ecx
100f7706: c7 04 24 00 00 a0 40         	mov	dword ptr [esp], 0x40a00000
100f770d: 8b ce                        	mov	ecx, esi
100f770f: 68 00 be 52 10               	push	0x1052be00
100f7714: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7717: ff d0                        	call	eax
100f7719: d9 9f 64 03 00 00            	fstp	dword ptr [edi + 0x364]
100f771f: 8b 06                        	mov	eax, dword ptr [esi]
100f7721: 8b ce                        	mov	ecx, esi
100f7723: 6a 04                        	push	0x4
100f7725: 68 3c be 52 10               	push	0x1052be3c
100f772a: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f772d: 89 87 68 03 00 00            	mov	dword ptr [edi + 0x368], eax
100f7733: 8b ce                        	mov	ecx, esi
100f7735: 8b 06                        	mov	eax, dword ptr [esi]
100f7737: 6a 00                        	push	0x0
100f7739: 68 20 be 52 10               	push	0x1052be20
100f773e: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7741: 89 87 58 03 00 00            	mov	dword ptr [edi + 0x358], eax
100f7747: 8b ce                        	mov	ecx, esi
100f7749: 8b 06                        	mov	eax, dword ptr [esi]
100f774b: 6a 00                        	push	0x0
100f774d: 68 64 be 52 10               	push	0x1052be64
100f7752: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7755: 89 87 5c 03 00 00            	mov	dword ptr [edi + 0x35c], eax
100f775b: 8b ce                        	mov	ecx, esi
100f775d: 8b 06                        	mov	eax, dword ptr [esi]
100f775f: 6a 14                        	push	0x14
100f7761: 68 4c be 52 10               	push	0x1052be4c
100f7766: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7769: 89 87 7c 03 00 00            	mov	dword ptr [edi + 0x37c], eax
100f776f: 8b ce                        	mov	ecx, esi
100f7771: 8b 06                        	mov	eax, dword ptr [esi]
100f7773: 68 d0 07 00 00               	push	0x7d0
100f7778: 68 94 be 52 10               	push	0x1052be94
100f777d: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7780: 89 87 80 03 00 00            	mov	dword ptr [edi + 0x380], eax
100f7786: 8b ce                        	mov	ecx, esi
100f7788: 8b 06                        	mov	eax, dword ptr [esi]
100f778a: 68 88 13 00 00               	push	0x1388
100f778f: 68 80 be 52 10               	push	0x1052be80
100f7794: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7797: 89 87 84 03 00 00            	mov	dword ptr [edi + 0x384], eax
100f779d: 8b 06                        	mov	eax, dword ptr [esi]
100f779f: 51                           	push	ecx
100f77a0: c7 04 24 00 00 20 41         	mov	dword ptr [esp], 0x41200000
100f77a7: 8b ce                        	mov	ecx, esi
100f77a9: 68 b8 be 52 10               	push	0x1052beb8
100f77ae: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f77b1: ff d0                        	call	eax
100f77b3: d9 9f 94 02 00 00            	fstp	dword ptr [edi + 0x294]
100f77b9: 8b 06                        	mov	eax, dword ptr [esi]
100f77bb: 51                           	push	ecx
100f77bc: c7 04 24 00 00 c8 42         	mov	dword ptr [esp], 0x42c80000
100f77c3: 8b ce                        	mov	ecx, esi
100f77c5: 68 a8 be 52 10               	push	0x1052bea8
100f77ca: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f77cd: ff d0                        	call	eax
100f77cf: d9 9f 98 02 00 00            	fstp	dword ptr [edi + 0x298]
100f77d5: 8b 06                        	mov	eax, dword ptr [esi]
100f77d7: 51                           	push	ecx
100f77d8: c7 04 24 00 00 80 3f         	mov	dword ptr [esp], 0x3f800000
100f77df: 8b ce                        	mov	ecx, esi
100f77e1: 68 d8 be 52 10               	push	0x1052bed8
100f77e6: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f77e9: ff d0                        	call	eax
100f77eb: d9 9f 9c 02 00 00            	fstp	dword ptr [edi + 0x29c]
100f77f1: 8b 06                        	mov	eax, dword ptr [esi]
100f77f3: 51                           	push	ecx
100f77f4: c7 04 24 00 00 a0 41         	mov	dword ptr [esp], 0x41a00000
100f77fb: 8b ce                        	mov	ecx, esi
100f77fd: 68 c8 be 52 10               	push	0x1052bec8
100f7802: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7805: ff d0                        	call	eax
100f7807: 51                           	push	ecx
100f7808: d9 9f a0 02 00 00            	fstp	dword ptr [edi + 0x2a0]
100f780e: 8b 06                        	mov	eax, dword ptr [esi]
100f7810: 8b ce                        	mov	ecx, esi
100f7812: c7 04 24 00 00 a0 41         	mov	dword ptr [esp], 0x41a00000
100f7819: 68 fc be 52 10               	push	0x1052befc
100f781e: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7821: ff d0                        	call	eax
100f7823: d9 9f a8 02 00 00            	fstp	dword ptr [edi + 0x2a8]
100f7829: 8b 06                        	mov	eax, dword ptr [esi]
100f782b: 51                           	push	ecx
100f782c: c7 04 24 00 00 a0 41         	mov	dword ptr [esp], 0x41a00000
100f7833: 8b ce                        	mov	ecx, esi
100f7835: 68 ec be 52 10               	push	0x1052beec
100f783a: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f783d: ff d0                        	call	eax
100f783f: d9 9f ac 02 00 00            	fstp	dword ptr [edi + 0x2ac]
100f7845: 8b 06                        	mov	eax, dword ptr [esi]
100f7847: 51                           	push	ecx
100f7848: c7 04 24 00 00 48 42         	mov	dword ptr [esp], 0x42480000
100f784f: 8b ce                        	mov	ecx, esi
100f7851: 68 20 bf 52 10               	push	0x1052bf20
100f7856: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7859: ff d0                        	call	eax
100f785b: d9 9f a4 02 00 00            	fstp	dword ptr [edi + 0x2a4]
100f7861: 8b 06                        	mov	eax, dword ptr [esi]
100f7863: 51                           	push	ecx
100f7864: c7 04 24 00 00 a0 40         	mov	dword ptr [esp], 0x40a00000
100f786b: 8b ce                        	mov	ecx, esi
100f786d: 68 10 bf 52 10               	push	0x1052bf10
100f7872: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7875: ff d0                        	call	eax
100f7877: d9 9f b4 02 00 00            	fstp	dword ptr [edi + 0x2b4]
100f787d: 8b 06                        	mov	eax, dword ptr [esi]
100f787f: 8b ce                        	mov	ecx, esi
100f7881: 6a 00                        	push	0x0
100f7883: 68 48 bf 52 10               	push	0x1052bf48
100f7888: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f788b: 89 87 90 03 00 00            	mov	dword ptr [edi + 0x390], eax
100f7891: 8b ce                        	mov	ecx, esi
100f7893: 8b 06                        	mov	eax, dword ptr [esi]
100f7895: 68 b8 0b 00 00               	push	0xbb8
100f789a: 68 2c bf 52 10               	push	0x1052bf2c
100f789f: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f78a2: 89 87 04 05 00 00            	mov	dword ptr [edi + 0x504], eax
100f78a8: 8b ce                        	mov	ecx, esi
100f78aa: 8b 06                        	mov	eax, dword ptr [esi]
100f78ac: 68 88 13 00 00               	push	0x1388
100f78b1: 68 6c bf 52 10               	push	0x1052bf6c
100f78b6: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f78b9: 89 87 10 05 00 00            	mov	dword ptr [edi + 0x510], eax
100f78bf: 8b 06                        	mov	eax, dword ptr [esi]
100f78c1: 51                           	push	ecx
100f78c2: c7 04 24 00 00 80 40         	mov	dword ptr [esp], 0x40800000
100f78c9: 8b ce                        	mov	ecx, esi
100f78cb: 68 5c bf 52 10               	push	0x1052bf5c
100f78d0: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f78d3: ff d0                        	call	eax
100f78d5: d9 9f a8 03 00 00            	fstp	dword ptr [edi + 0x3a8]
100f78db: 8b 06                        	mov	eax, dword ptr [esi]
100f78dd: 8b ce                        	mov	ecx, esi
100f78df: 6a 00                        	push	0x0
100f78e1: 68 8c bf 52 10               	push	0x1052bf8c
100f78e6: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f78e9: 89 87 dc 02 00 00            	mov	dword ptr [edi + 0x2dc], eax
100f78ef: 8b 06                        	mov	eax, dword ptr [esi]
100f78f1: 51                           	push	ecx
100f78f2: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
100f78f9: 8b ce                        	mov	ecx, esi
100f78fb: 68 78 bf 52 10               	push	0x1052bf78
100f7900: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
100f7903: ff d0                        	call	eax
100f7905: d9 9f ac 03 00 00            	fstp	dword ptr [edi + 0x3ac]
100f790b: 8b 06                        	mov	eax, dword ptr [esi]
100f790d: 8b ce                        	mov	ecx, esi
100f790f: 6a 00                        	push	0x0
100f7911: 68 b0 bf 52 10               	push	0x1052bfb0
100f7916: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7919: 89 87 b0 03 00 00            	mov	dword ptr [edi + 0x3b0], eax
100f791f: 8b ce                        	mov	ecx, esi
100f7921: 8b 06                        	mov	eax, dword ptr [esi]
100f7923: 6a 00                        	push	0x0
100f7925: 68 98 bf 52 10               	push	0x1052bf98
100f792a: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f792d: 89 87 e0 02 00 00            	mov	dword ptr [edi + 0x2e0], eax
100f7933: c7 45 e8 00 00 00 00         	mov	dword ptr [ebp - 0x18], 0x0
100f793a: c7 45 ec 00 00 00 00         	mov	dword ptr [ebp - 0x14], 0x0
100f7941: c7 45 f0 00 00 00 00         	mov	dword ptr [ebp - 0x10], 0x0
100f7948: c6 45 fc 01                  	mov	byte ptr [ebp - 0x4], 0x1
100f794c: 8d 4d e8                     	lea	ecx, [ebp - 0x18]
100f794f: 8b 06                        	mov	eax, dword ptr [esi]
100f7951: 51                           	push	ecx
100f7952: 68 dc bf 52 10               	push	0x1052bfdc
100f7957: 8b ce                        	mov	ecx, esi
100f7959: ff 50 34                     	call	dword ptr [eax + 0x34]
100f795c: 8b 55 e8                     	mov	edx, dword ptr [ebp - 0x18]
100f795f: 8b 4d ec                     	mov	ecx, dword ptr [ebp - 0x14]
100f7962: 3b d1                        	cmp	edx, ecx
100f7964: f3 0f 10 0d 80 57 5f 10      	movss	xmm1, dword ptr [0x105f5780]
100f796c: 0f 94 c0                     	sete	al
100f796f: 84 c0                        	test	al, al
100f7971: 75 60                        	jne	0x100f79d3 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xc33>
100f7973: 66 0f 6e 02                  	movd	xmm0, dword ptr [edx]
100f7977: 2b ca                        	sub	ecx, edx
100f7979: 0f 5b c0                     	cvtdq2ps	xmm0, xmm0
100f797c: c1 f9 02                     	sar	ecx, 0x2
100f797f: f3 0f 59 c1                  	mulss	xmm0, xmm1
100f7983: f3 0f 11 87 e4 02 00 00      	movss	dword ptr [edi + 0x2e4], xmm0
100f798b: 83 f9 01                     	cmp	ecx, 0x1
100f798e: 76 2f                        	jbe	0x100f79bf <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xc1f>
100f7990: 66 0f 6e 42 04               	movd	xmm0, dword ptr [edx + 0x4]
100f7995: 0f 5b c0                     	cvtdq2ps	xmm0, xmm0
100f7998: f3 0f 59 c1                  	mulss	xmm0, xmm1
100f799c: f3 0f 11 87 e8 02 00 00      	movss	dword ptr [edi + 0x2e8], xmm0
100f79a4: 83 f9 02                     	cmp	ecx, 0x2
100f79a7: 76 0c                        	jbe	0x100f79b5 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xc15>
100f79a9: 66 0f 6e 42 08               	movd	xmm0, dword ptr [edx + 0x8]
100f79ae: 0f 5b c0                     	cvtdq2ps	xmm0, xmm0
100f79b1: f3 0f 59 c1                  	mulss	xmm0, xmm1
100f79b5: f3 0f 11 87 ec 02 00 00      	movss	dword ptr [edi + 0x2ec], xmm0
100f79bd: eb 14                        	jmp	0x100f79d3 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xc33>
100f79bf: 8b 87 e4 02 00 00            	mov	eax, dword ptr [edi + 0x2e4]
100f79c5: f3 0f 11 87 e8 02 00 00      	movss	dword ptr [edi + 0x2e8], xmm0
100f79cd: 89 87 ec 02 00 00            	mov	dword ptr [edi + 0x2ec], eax
100f79d3: 8b 06                        	mov	eax, dword ptr [esi]
100f79d5: 8b ce                        	mov	ecx, esi
100f79d7: 6a 00                        	push	0x0
100f79d9: 68 c4 bf 52 10               	push	0x1052bfc4
100f79de: 8b 40 2c                     	mov	eax, dword ptr [eax + 0x2c]
100f79e1: ff d0                        	call	eax
100f79e3: 88 87 d9 04 00 00            	mov	byte ptr [edi + 0x4d9], al
100f79e9: 8b ce                        	mov	ecx, esi
100f79eb: 8b 06                        	mov	eax, dword ptr [esi]
100f79ed: 6a 64                        	push	0x64
100f79ef: 68 fc bf 52 10               	push	0x1052bffc
100f79f4: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f79f7: 89 87 14 05 00 00            	mov	dword ptr [edi + 0x514], eax
100f79fd: 8b ce                        	mov	ecx, esi
100f79ff: 8b 06                        	mov	eax, dword ptr [esi]
100f7a01: 68 88 13 00 00               	push	0x1388
100f7a06: 68 e8 bf 52 10               	push	0x1052bfe8
100f7a0b: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a0e: 89 87 18 05 00 00            	mov	dword ptr [edi + 0x518], eax
100f7a14: 8b ce                        	mov	ecx, esi
100f7a16: 8b 06                        	mov	eax, dword ptr [esi]
100f7a18: 68 10 27 00 00               	push	0x2710
100f7a1d: 68 24 c0 52 10               	push	0x1052c024
100f7a22: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a25: 89 87 1c 05 00 00            	mov	dword ptr [edi + 0x51c], eax
100f7a2b: 8b ce                        	mov	ecx, esi
100f7a2d: 8b 06                        	mov	eax, dword ptr [esi]
100f7a2f: 6a 00                        	push	0x0
100f7a31: 68 10 c0 52 10               	push	0x1052c010
100f7a36: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a39: 89 87 6c 05 00 00            	mov	dword ptr [edi + 0x56c], eax
100f7a3f: 8b ce                        	mov	ecx, esi
100f7a41: 8b 06                        	mov	eax, dword ptr [esi]
100f7a43: 68 88 13 00 00               	push	0x1388
100f7a48: 68 50 c0 52 10               	push	0x1052c050
100f7a4d: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a50: 89 87 70 05 00 00            	mov	dword ptr [edi + 0x570], eax
100f7a56: 8b ce                        	mov	ecx, esi
100f7a58: 8b 06                        	mov	eax, dword ptr [esi]
100f7a5a: 6a 00                        	push	0x0
100f7a5c: 68 38 c0 52 10               	push	0x1052c038
100f7a61: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a64: 68 e8 03 00 00               	push	0x3e8
100f7a69: 68 7c c0 52 10               	push	0x1052c07c
100f7a6e: 8b ce                        	mov	ecx, esi
100f7a70: 66 0f 6e c0                  	movd	xmm0, eax
100f7a74: 0f 5b c0                     	cvtdq2ps	xmm0, xmm0
100f7a77: f3 0f 59 05 80 57 5f 10      	mulss	xmm0, dword ptr [0x105f5780]
100f7a7f: f3 0f 11 87 7c 05 00 00      	movss	dword ptr [edi + 0x57c], xmm0
100f7a87: 8b 06                        	mov	eax, dword ptr [esi]
100f7a89: ff 50 1c                     	call	dword ptr [eax + 0x1c]
100f7a8c: 89 87 80 05 00 00            	mov	dword ptr [edi + 0x580], eax
100f7a92: 8b ce                        	mov	ecx, esi
100f7a94: 8b 06                        	mov	eax, dword ptr [esi]
100f7a96: 6a 00                        	push	0x0
100f7a98: 68 64 c0 52 10               	push	0x1052c064
100f7a9d: 8b 40 2c                     	mov	eax, dword ptr [eax + 0x2c]
100f7aa0: ff d0                        	call	eax
100f7aa2: 88 87 84 05 00 00            	mov	byte ptr [edi + 0x584], al
100f7aa8: 8b ce                        	mov	ecx, esi
100f7aaa: 8b 06                        	mov	eax, dword ptr [esi]
100f7aac: 6a 00                        	push	0x0
100f7aae: 68 90 c0 52 10               	push	0x1052c090
100f7ab3: 8b 40 2c                     	mov	eax, dword ptr [eax + 0x2c]
100f7ab6: ff d0                        	call	eax
100f7ab8: 88 87 85 05 00 00            	mov	byte ptr [edi + 0x585], al
100f7abe: 8b ce                        	mov	ecx, esi
100f7ac0: 8b 06                        	mov	eax, dword ptr [esi]
100f7ac2: 68 d5 0b 4f 10               	push	0x104f0bd5
100f7ac7: 68 a8 c0 52 10               	push	0x1052c0a8
100f7acc: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7acf: 8b d0                        	mov	edx, eax
100f7ad1: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7ad4: 75 04                        	jne	0x100f7ada <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd3a>
100f7ad6: 33 c9                        	xor	ecx, ecx
100f7ad8: eb 0f                        	jmp	0x100f7ae9 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd49>
100f7ada: 8b ca                        	mov	ecx, edx
100f7adc: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f7adf: 90                           	nop
100f7ae0: 8a 01                        	mov	al, byte ptr [ecx]
100f7ae2: 41                           	inc	ecx
100f7ae3: 84 c0                        	test	al, al
100f7ae5: 75 f9                        	jne	0x100f7ae0 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd40>
100f7ae7: 2b cb                        	sub	ecx, ebx
100f7ae9: 51                           	push	ecx
100f7aea: 52                           	push	edx
100f7aeb: 8d 8f 4c 06 00 00            	lea	ecx, [edi + 0x64c]
100f7af1: e8 8a 10 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7af6: 8b 06                        	mov	eax, dword ptr [esi]
100f7af8: 8b ce                        	mov	ecx, esi
100f7afa: 68 d6 0b 4f 10               	push	0x104f0bd6
100f7aff: 68 c0 c0 52 10               	push	0x1052c0c0
100f7b04: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7b07: 8b d0                        	mov	edx, eax
100f7b09: c7 45 cc 0f 00 00 00         	mov	dword ptr [ebp - 0x34], 0xf
100f7b10: c7 45 c8 00 00 00 00         	mov	dword ptr [ebp - 0x38], 0x0
100f7b17: c6 45 b8 00                  	mov	byte ptr [ebp - 0x48], 0x0
100f7b1b: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7b1e: 75 04                        	jne	0x100f7b24 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd84>
100f7b20: 33 c9                        	xor	ecx, ecx
100f7b22: eb 15                        	jmp	0x100f7b39 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd99>
100f7b24: 8b ca                        	mov	ecx, edx
100f7b26: 8d 59 01                     	lea	ebx, [ecx + 0x1]
100f7b29: 0f 1f 80 00 00 00 00         	nop	dword ptr [eax]
100f7b30: 8a 01                        	mov	al, byte ptr [ecx]
100f7b32: 41                           	inc	ecx
100f7b33: 84 c0                        	test	al, al
100f7b35: 75 f9                        	jne	0x100f7b30 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xd90>
100f7b37: 2b cb                        	sub	ecx, ebx
100f7b39: 51                           	push	ecx
100f7b3a: 52                           	push	edx
100f7b3b: 8d 4d b8                     	lea	ecx, [ebp - 0x48]
100f7b3e: e8 3d 10 f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7b43: c6 45 fc 02                  	mov	byte ptr [ebp - 0x4], 0x2
100f7b47: 83 7d c8 00                  	cmp	dword ptr [ebp - 0x38], 0x0
100f7b4b: 74 21                        	je	0x100f7b6e <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xdce>
100f7b4d: 83 7d cc 10                  	cmp	dword ptr [ebp - 0x34], 0x10
100f7b51: 8d 45 b8                     	lea	eax, [ebp - 0x48]
100f7b54: 0f 43 45 b8                  	cmovae	eax, dword ptr [ebp - 0x48]
100f7b58: 50                           	push	eax
100f7b59: 8d 45 08                     	lea	eax, [ebp + 0x8]
100f7b5c: 50                           	push	eax
100f7b5d: ff 15 58 52 4e 10            	call	dword ptr [0x104e5258]
100f7b63: 83 c4 08                     	add	esp, 0x8
100f7b66: 8b 00                        	mov	eax, dword ptr [eax]
100f7b68: 89 87 48 06 00 00            	mov	dword ptr [edi + 0x648], eax
100f7b6e: 8b 06                        	mov	eax, dword ptr [esi]
100f7b70: 8b ce                        	mov	ecx, esi
100f7b72: 68 d7 0b 4f 10               	push	0x104f0bd7
100f7b77: 68 e4 c0 52 10               	push	0x1052c0e4
100f7b7c: ff 50 14                     	call	dword ptr [eax + 0x14]
100f7b7f: 8b d0                        	mov	edx, eax
100f7b81: 80 3a 00                     	cmp	byte ptr [edx], 0x0
100f7b84: 75 04                        	jne	0x100f7b8a <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xdea>
100f7b86: 33 c9                        	xor	ecx, ecx
100f7b88: eb 0f                        	jmp	0x100f7b99 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xdf9>
100f7b8a: 8b ca                        	mov	ecx, edx
100f7b8c: 8d 71 01                     	lea	esi, [ecx + 0x1]
100f7b8f: 90                           	nop
100f7b90: 8a 01                        	mov	al, byte ptr [ecx]
100f7b92: 41                           	inc	ecx
100f7b93: 84 c0                        	test	al, al
100f7b95: 75 f9                        	jne	0x100f7b90 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xdf0>
100f7b97: 2b ce                        	sub	ecx, esi
100f7b99: 51                           	push	ecx
100f7b9a: 52                           	push	edx
100f7b9b: 8d 8f 64 06 00 00            	lea	ecx, [edi + 0x664]
100f7ba1: e8 da 0f f1 ff               	call	0x10008b80 <?_DrawEditorArrow@SkillLocation@GAME@@IBEXABVWorldVec3@2@@Z+0x6b0>
100f7ba6: 8b 55 cc                     	mov	edx, dword ptr [ebp - 0x34]
100f7ba9: 5f                           	pop	edi
100f7baa: 5e                           	pop	esi
100f7bab: 5b                           	pop	ebx
100f7bac: 83 fa 10                     	cmp	edx, 0x10
100f7baf: 72 0e                        	jb	0x100f7bbf <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xe1f>
100f7bb1: 8b 4d b8                     	mov	ecx, dword ptr [ebp - 0x48]
100f7bb4: 42                           	inc	edx
100f7bb5: 6a 01                        	push	0x1
100f7bb7: e8 44 11 f1 ff               	call	0x10008d00 <??1AuraContainer@GAME@@QAE@XZ+0x40>
100f7bbc: 83 c4 04                     	add	esp, 0x4
100f7bbf: 8b 4d e8                     	mov	ecx, dword ptr [ebp - 0x18]
100f7bc2: c7 45 cc 0f 00 00 00         	mov	dword ptr [ebp - 0x34], 0xf
100f7bc9: c7 45 c8 00 00 00 00         	mov	dword ptr [ebp - 0x38], 0x0
100f7bd0: c6 45 b8 00                  	mov	byte ptr [ebp - 0x48], 0x0
100f7bd4: 85 c9                        	test	ecx, ecx
100f7bd6: 74 27                        	je	0x100f7bff <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xe5f>
100f7bd8: 8b 55 f0                     	mov	edx, dword ptr [ebp - 0x10]
100f7bdb: 2b d1                        	sub	edx, ecx
100f7bdd: 6a 04                        	push	0x4
100f7bdf: c1 fa 02                     	sar	edx, 0x2
100f7be2: e8 19 11 f1 ff               	call	0x10008d00 <??1AuraContainer@GAME@@QAE@XZ+0x40>
100f7be7: 83 c4 04                     	add	esp, 0x4
100f7bea: c7 45 e8 00 00 00 00         	mov	dword ptr [ebp - 0x18], 0x0
100f7bf1: c7 45 ec 00 00 00 00         	mov	dword ptr [ebp - 0x14], 0x0
100f7bf8: c7 45 f0 00 00 00 00         	mov	dword ptr [ebp - 0x10], 0x0
100f7bff: 8b 55 e4                     	mov	edx, dword ptr [ebp - 0x1c]
100f7c02: 83 fa 10                     	cmp	edx, 0x10
100f7c05: 72 0e                        	jb	0x100f7c15 <?Load@ControllerMonster@GAME@@UAEXABVLoadTable@2@@Z+0xe75>
100f7c07: 8b 4d d0                     	mov	ecx, dword ptr [ebp - 0x30]
100f7c0a: 42                           	inc	edx
100f7c0b: 6a 01                        	push	0x1
100f7c0d: e8 ee 10 f1 ff               	call	0x10008d00 <??1AuraContainer@GAME@@QAE@XZ+0x40>
100f7c12: 83 c4 04                     	add	esp, 0x4
100f7c15: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
100f7c18: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
100f7c1f: 8b e5                        	mov	esp, ebp
100f7c21: 5d                           	pop	ebp
100f7c22: c2 04 00                     	ret	0x4
100f7c25: cc                           	int3
100f7c26: cc                           	int3
100f7c27: cc                           	int3
100f7c28: cc                           	int3
100f7c29: cc                           	int3
100f7c2a: cc                           	int3
100f7c2b: cc                           	int3
100f7c2c: cc                           	int3
100f7c2d: cc                           	int3
100f7c2e: cc                           	int3
100f7c2f: cc                           	int3
