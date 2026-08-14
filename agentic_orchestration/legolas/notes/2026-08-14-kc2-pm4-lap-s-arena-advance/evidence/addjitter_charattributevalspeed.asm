
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

10095400 <?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z>:
10095400: 55                           	push	ebp
10095401: 8b ec                        	mov	ebp, esp
10095403: f3 0f 10 65 08               	movss	xmm4, dword ptr [ebp + 0x8]
10095408: 0f 57 ed                     	xorps	xmm5, xmm5
1009540b: 0f 2f e5                     	comiss	xmm4, xmm5
1009540e: 56                           	push	esi
1009540f: 8b f1                        	mov	esi, ecx
10095411: 0f 86 a7 00 00 00            	jbe	0x100954be <?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z+0xbe>
10095417: 57                           	push	edi
10095418: 8b 7d 0c                     	mov	edi, dword ptr [ebp + 0xc]
1009541b: 85 ff                        	test	edi, edi
1009541d: 0f 84 9a 00 00 00            	je	0x100954bd <?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z+0xbd>
10095423: 8b 4e 08                     	mov	ecx, dword ptr [esi + 0x8]
10095426: 3b 4e 0c                     	cmp	ecx, dword ptr [esi + 0xc]
10095429: 0f 84 8e 00 00 00            	je	0x100954bd <?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z+0xbd>
1009542f: f3 0f 59 25 80 57 5f 10      	mulss	xmm4, dword ptr [0x105f5780]
10095437: c7 45 08 1d f3 01 00         	mov	dword ptr [ebp + 0x8], 0x1f31d
1009543e: f3 0f 10 35 10 5b 5f 10      	movss	xmm6, dword ptr [0x105f5b10]
10095446: f3 0f 10 3d 18 57 5f 10      	movss	xmm7, dword ptr [0x105f5718]
1009544e: 66 90                        	nop
10095450: 8b 07                        	mov	eax, dword ptr [edi]
10095452: 33 d2                        	xor	edx, edx
10095454: f7 75 08                     	div	dword ptr [ebp + 0x8]
10095457: f3 0f 10 19                  	movss	xmm3, dword ptr [ecx]
1009545b: 0f 28 d4                     	movaps	xmm2, xmm4
1009545e: 69 d2 a7 41 00 00            	imul	edx, edx, 0x41a7
10095464: 69 c0 14 0b 00 00            	imul	eax, eax, 0xb14
1009546a: f3 0f 59 d3                  	mulss	xmm2, xmm3
1009546e: 2b d0                        	sub	edx, eax
10095470: 0f 28 ca                     	movaps	xmm1, xmm2
10095473: 0f 57 ce                     	xorps	xmm1, xmm6
10095476: f3 0f 5c d1                  	subss	xmm2, xmm1
1009547a: 8d 82 ff ff ff 7f            	lea	eax, [edx + 0x7fffffff]
10095480: 0f 48 d0                     	cmovs	edx, eax
10095483: 89 17                        	mov	dword ptr [edi], edx
10095485: 66 0f 6e c2                  	movd	xmm0, edx
10095489: f3 0f e6 c0                  	cvtdq2pd	xmm0, xmm0
1009548d: c1 ea 1f                     	shr	edx, 0x1f
10095490: f2 0f 58 04 d5 e0 5a 5f 10   	addsd	xmm0, qword ptr [8*edx + 0x105f5ae0]
10095499: 66 0f 5a c0                  	cvtpd2ps	xmm0, xmm0
1009549d: f3 0f 59 c7                  	mulss	xmm0, xmm7
100954a1: f3 0f 59 c2                  	mulss	xmm0, xmm2
100954a5: f3 0f 58 c1                  	addss	xmm0, xmm1
100954a9: f3 0f 58 c3                  	addss	xmm0, xmm3
100954ad: f3 0f 5f c5                  	maxss	xmm0, xmm5
100954b1: f3 0f 11 01                  	movss	dword ptr [ecx], xmm0
100954b5: 83 c1 04                     	add	ecx, 0x4
100954b8: 3b 4e 0c                     	cmp	ecx, dword ptr [esi + 0xc]
100954bb: 75 93                        	jne	0x10095450 <?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z+0x50>
100954bd: 5f                           	pop	edi
100954be: 5e                           	pop	esi
100954bf: 5d                           	pop	ebp
100954c0: c2 08 00                     	ret	0x8
100954c3: cc                           	int3
100954c4: cc                           	int3
100954c5: cc                           	int3
100954c6: cc                           	int3
100954c7: cc                           	int3
100954c8: cc                           	int3
100954c9: cc                           	int3
100954ca: cc                           	int3
100954cb: cc                           	int3
100954cc: cc                           	int3
100954cd: cc                           	int3
100954ce: cc                           	int3
100954cf: cc                           	int3
