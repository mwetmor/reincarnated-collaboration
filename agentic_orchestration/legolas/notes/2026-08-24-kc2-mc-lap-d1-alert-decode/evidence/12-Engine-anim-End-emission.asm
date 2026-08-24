
/Users/admin/Games/vendor/grim-dawn/Engine.dll:	file format coff-i386

Disassembly of section .text:

1002e8b0 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ>:
10031133: 8b 5d f0                     	mov	ebx, dword ptr [ebp - 0x10]
10031136: 8b 75 0c                     	mov	esi, dword ptr [ebp + 0xc]
10031139: 8b 45 e0                     	mov	eax, dword ptr [ebp - 0x20]
1003113c: f3 0f 10 43 08               	movss	xmm0, dword ptr [ebx + 0x8]
10031141: f3 0f 58 45 ec               	addss	xmm0, dword ptr [ebp - 0x14]
10031146: f3 0f 11 43 08               	movss	dword ptr [ebx + 0x8], xmm0
1003114b: 84 c0                        	test	al, al
1003114d: 74 6b                        	je	0x100311ba <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x290a>
1003114f: 64 a1 2c 00 00 00            	mov	eax, dword ptr fs:[0x2c]
10031155: 8b 0d 88 71 36 10            	mov	ecx, dword ptr [0x10367188]
1003115b: 8b 0c 88                     	mov	ecx, dword ptr [eax + 4*ecx]
1003115e: a1 18 89 36 10               	mov	eax, dword ptr [0x10368918]
10031163: 3b 81 04 00 00 00            	cmp	eax, dword ptr [ecx + 0x4]
10031169: 7e 40                        	jle	0x100311ab <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x28fb>
1003116b: 68 18 89 36 10               	push	0x10368918
10031170: e8 b6 e5 24 00               	call	0x1027f72b <LZ4_decompress_fast_usingDict+0x5feab>
10031175: 83 c4 04                     	add	esp, 0x4
10031178: 83 3d 18 89 36 10 ff         	cmp	dword ptr [0x10368918], -0x1
1003117f: 75 2a                        	jne	0x100311ab <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x28fb>
10031181: 68 34 58 2a 10               	push	0x102a5834
10031186: 68 1c 89 36 10               	push	0x1036891c
1003118b: c7 45 fc 00 00 00 00         	mov	dword ptr [ebp - 0x4], 0x0
10031192: e8 39 5b 0f 00               	call	0x10126cd0 <?Create@Name@GAME@@SA?AV12@PBD@Z>
10031197: 68 18 89 36 10               	push	0x10368918
1003119c: c7 45 fc ff ff ff ff         	mov	dword ptr [ebp - 0x4], 0xffffffff
100311a3: e8 44 e5 24 00               	call	0x1027f6ec <LZ4_decompress_fast_usingDict+0x5fe6c>
100311a8: 83 c4 0c                     	add	esp, 0xc
100311ab: 8b 06                        	mov	eax, dword ptr [esi]
100311ad: 8b ce                        	mov	ecx, esi
100311af: 68 1c 89 36 10               	push	0x1036891c
100311b4: ff 90 f8 00 00 00            	call	dword ptr [eax + 0xf8]
100311ba: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
100311bd: 5f                           	pop	edi
100311be: 5e                           	pop	esi
100311bf: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
100311c6: 5b                           	pop	ebx
100311c7: 8b e5                        	mov	esp, ebp
