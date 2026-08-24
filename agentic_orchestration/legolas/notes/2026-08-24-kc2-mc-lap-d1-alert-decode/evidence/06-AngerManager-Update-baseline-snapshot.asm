
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

1000f3a0 <?Update@AngerManager@GAME@@QAEXHM_N0@Z>:
1000f460: 00 00                        	add	byte ptr [eax], al
1000f462: 84 c0                        	test	al, al
1000f464: 0f 85 be 01 00 00            	jne	0x1000f628 <?Update@AngerManager@GAME@@QAEXHM_N0@Z+0x288>
1000f46a: f3 0f 10 46 14               	movss	xmm0, dword ptr [esi + 0x14]
1000f46f: 0f 57 e4                     	xorps	xmm4, xmm4
1000f472: 0f 2f e0                     	comiss	xmm4, xmm0
1000f475: 0f 87 ad 01 00 00            	ja	0x1000f628 <?Update@AngerManager@GAME@@QAEXHM_N0@Z+0x288>
1000f47b: 8b 7d f8                     	mov	edi, dword ptr [ebp - 0x8]
1000f47e: f3 0f 10 2d 08 58 5f 10      	movss	xmm5, dword ptr [0x105f5808]
1000f486: f3 0f 11 46 18               	movss	dword ptr [esi + 0x18], xmm0
1000f48b: f3 0f 10 97 68 0c 00 00      	movss	xmm2, dword ptr [edi + 0xc68]
1000f493: f3 0f 10 9f 98 0a 00 00      	movss	xmm3, dword ptr [edi + 0xa98]
1000f49b: f3 0f 58 d5                  	addss	xmm2, xmm5
1000f49f: 0f 2f dc                     	comiss	xmm3, xmm4
