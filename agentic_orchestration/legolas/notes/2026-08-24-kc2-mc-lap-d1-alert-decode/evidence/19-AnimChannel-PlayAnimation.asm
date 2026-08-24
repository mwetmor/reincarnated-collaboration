
/Users/admin/Games/vendor/grim-dawn/Engine.dll:	file format coff-i386

Disassembly of section .text:

10031480 <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z>:
10031480: 55                           	push	ebp
10031481: 8b ec                        	mov	ebp, esp
10031483: 64 a1 00 00 00 00            	mov	eax, dword ptr fs:[0x0]
10031489: 6a ff                        	push	-0x1
1003148b: 68 5f 29 29 10               	push	0x1029295f
10031490: 50                           	push	eax
10031491: 64 89 25 00 00 00 00         	mov	dword ptr fs:[0x0], esp
10031498: 83 ec 30                     	sub	esp, 0x30
1003149b: 56                           	push	esi
1003149c: 8b f1                        	mov	esi, ecx
1003149e: 57                           	push	edi
1003149f: 8b 7d 14                     	mov	edi, dword ptr [ebp + 0x14]
100314a2: 83 7e 08 00                  	cmp	dword ptr [esi + 0x8], 0x0
100314a6: 74 66                        	je	0x1003150e <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0x8e>
100314a8: 0f 10 46 08                  	movups	xmm0, xmmword ptr [esi + 0x8]
100314ac: 53                           	push	ebx
100314ad: 0f 11 45 c4                  	movups	xmmword ptr [ebp - 0x3c], xmm0
100314b1: 0f 10 46 18                  	movups	xmm0, xmmword ptr [esi + 0x18]
100314b5: 0f 11 45 d4                  	movups	xmmword ptr [ebp - 0x2c], xmm0
100314b9: c7 45 fc 00 00 00 00         	mov	dword ptr [ebp - 0x4], 0x0
100314c0: 8b 46 2c                     	mov	eax, dword ptr [esi + 0x2c]
100314c3: 89 7d e4                     	mov	dword ptr [ebp - 0x1c], edi
100314c6: 8b 18                        	mov	ebx, dword ptr [eax]
100314c8: 8d 45 c4                     	lea	eax, [ebp - 0x3c]
100314cb: 50                           	push	eax
100314cc: ff 73 04                     	push	dword ptr [ebx + 0x4]
100314cf: 53                           	push	ebx
100314d0: e8 4b 8e fe ff               	call	0x1001a320 <?Destroy@?$Singleton@VNavManager@GAME@@@GAME@@SAXXZ+0x2440>
100314d5: b9 5c 74 d1 05               	mov	ecx, 0x5d1745c
100314da: 8b d0                        	mov	edx, eax
100314dc: 2b 4e 30                     	sub	ecx, dword ptr [esi + 0x30]
100314df: 83 f9 01                     	cmp	ecx, 0x1
100314e2: 73 0b                        	jae	0x100314ef <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0x6f>
100314e4: 68 4c 4f 2d 10               	push	0x102d4f4c
100314e9: ff 15 b0 22 2a 10            	call	dword ptr [0x102a22b0]
100314ef: ff 46 30                     	inc	dword ptr [esi + 0x30]
100314f2: 89 53 04                     	mov	dword ptr [ebx + 0x4], edx
100314f5: 8b 42 04                     	mov	eax, dword ptr [edx + 0x4]
100314f8: 89 10                        	mov	dword ptr [eax], edx
100314fa: c7 45 fc 01 00 00 00         	mov	dword ptr [ebp - 0x4], 0x1
10031501: 8b 4d c4                     	mov	ecx, dword ptr [ebp - 0x3c]
10031504: 5b                           	pop	ebx
10031505: 85 c9                        	test	ecx, ecx
10031507: 74 05                        	je	0x1003150e <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0x8e>
10031509: e8 02 76 05 00               	call	0x10088b10 <?ReleaseCreateEntities@GraphicsAnim@GAME@@QBEXXZ>
1003150e: 85 ff                        	test	edi, edi
10031510: 75 1c                        	jne	0x1003152e <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0xae>
10031512: 8b 46 2c                     	mov	eax, dword ptr [esi + 0x2c]
10031515: 8b 08                        	mov	ecx, dword ptr [eax]
10031517: 3b c8                        	cmp	ecx, eax
10031519: 74 13                        	je	0x1003152e <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0xae>
1003151b: 0f 1f 44 00 00               	nop	dword ptr [eax + eax]
10031520: c7 41 28 00 00 00 00         	mov	dword ptr [ecx + 0x28], 0x0
10031527: 8b 09                        	mov	ecx, dword ptr [ecx]
10031529: 3b 4e 2c                     	cmp	ecx, dword ptr [esi + 0x2c]
1003152c: 75 f2                        	jne	0x10031520 <?PlayAnimation@AnimChannel@GAME@@QAEXPBVGraphicsAnim@2@_NMH@Z+0xa0>
1003152e: 8b 45 08                     	mov	eax, dword ptr [ebp + 0x8]
10031531: 0f 57 c9                     	xorps	xmm1, xmm1
10031534: f3 0f 10 45 10               	movss	xmm0, dword ptr [ebp + 0x10]
10031539: 8b 4d f4                     	mov	ecx, dword ptr [ebp - 0xc]
1003153c: 89 46 08                     	mov	dword ptr [esi + 0x8], eax
1003153f: 8a 45 0c                     	mov	al, byte ptr [ebp + 0xc]
10031542: 88 46 0c                     	mov	byte ptr [esi + 0xc], al
10031545: c7 45 f0 00 00 00 00         	mov	dword ptr [ebp - 0x10], 0x0
1003154c: 8b 45 f0                     	mov	eax, dword ptr [ebp - 0x10]
1003154f: 0f 14 c9                     	unpcklps	xmm1, xmm1              # xmm1 = xmm1[0,0,1,1]
10031552: 66 0f d6 4e 18               	movq	qword ptr [esi + 0x18], xmm1
10031557: c7 46 10 00 00 00 00         	mov	dword ptr [esi + 0x10], 0x0
1003155e: f3 0f 11 46 14               	movss	dword ptr [esi + 0x14], xmm0
10031563: 89 46 20                     	mov	dword ptr [esi + 0x20], eax
10031566: c7 46 24 00 00 00 00         	mov	dword ptr [esi + 0x24], 0x0
1003156d: c7 46 28 00 00 00 00         	mov	dword ptr [esi + 0x28], 0x0
10031574: 5f                           	pop	edi
10031575: 5e                           	pop	esi
10031576: 64 89 0d 00 00 00 00         	mov	dword ptr fs:[0x0], ecx
