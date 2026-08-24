
/Users/admin/Games/vendor/grim-dawn/Engine.dll:	file format coff-i386

Disassembly of section .text:

1002e8b0 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ>:
10030577: 8b 33                        	mov	esi, dword ptr [ebx]
10030579: 8b ce                        	mov	ecx, esi
1003057b: e8 30 21 13 00               	call	0x101626b0 <?EnsureAvailable@Resource@GAME@@QBEXXZ>
10030580: 8b 86 8c 00 00 00            	mov	eax, dword ptr [esi + 0x8c]
10030586: f3 0f 10 4d 20               	movss	xmm1, dword ptr [ebp + 0x20]
1003058b: f3 0f 10 55 08               	movss	xmm2, dword ptr [ebp + 0x8]
10030590: 8d 48 ff                     	lea	ecx, [eax - 0x1]
10030593: 8a 43 04                     	mov	al, byte ptr [ebx + 0x4]
10030596: 84 c0                        	test	al, al
10030598: 74 0c                        	je	0x100305a6 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1cf6>
1003059a: 0f 2f d1                     	comiss	xmm2, xmm1
1003059d: 76 07                        	jbe	0x100305a6 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1cf6>
1003059f: ba 01 00 00 00               	mov	edx, 0x1
100305a4: eb 02                        	jmp	0x100305a8 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1cf8>
100305a6: 33 d2                        	xor	edx, edx
100305a8: 84 c0                        	test	al, al
100305aa: 75 18                        	jne	0x100305c4 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1d14>
100305ac: 66 0f 6e c1                  	movd	xmm0, ecx
100305b0: 0f 5b c0                     	cvtdq2ps	xmm0, xmm0
100305b3: 0f 2f c2                     	comiss	xmm0, xmm2
100305b6: 76 0c                        	jbe	0x100305c4 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1d14>
100305b8: 0f 2f c8                     	comiss	xmm1, xmm0
100305bb: 72 07                        	jb	0x100305c4 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1d14>
100305bd: b8 01 00 00 00               	mov	eax, 0x1
100305c2: eb 02                        	jmp	0x100305c6 <?Destroy@?$Singleton@VJukebox@GAME@@@GAME@@SAXXZ+0x1d16>
100305c4: 33 c0                        	xor	eax, eax
100305c6: 8b 3d 94 21 2a 10            	mov	edi, dword ptr [0x102a2194]
100305cc: 0a d0                        	or	dl, al
100305ce: 8b 1d 98 21 2a 10            	mov	ebx, dword ptr [0x102a2198]
100305d4: 89 55 e0                     	mov	dword ptr [ebp - 0x20], edx
