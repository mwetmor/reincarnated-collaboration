
/Users/admin/Games/vendor/grim-dawn/Game.dll:	file format coff-i386

Disassembly of section .text:

102d3010 <?Load@Monster@GAME@@UAEXABVLoadTable@2@@Z>:
102d3511: 30 d4                        	xor	ah, dl
102d3513: ff 8d 4d cc 89 87            	dec	dword ptr [ebp - 0x787633b3]
102d3519: a0 32 00 00 c6               	mov	al, byte ptr [0xc6000032]
102d351e: 45                           	inc	ebp
102d351f: fc                           	cld
102d3520: 00 e8                        	add	al, ch
102d3522: 9a 57 d3 ff 8b 03 51         	lcall	0x5103, 0x8bffd357
102d3529: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
102d3530: 8b cb                        	mov	ecx, ebx
102d3532: 68 a0 0e 56 10               	push	0x10560ea0
102d3537: 8b 40 24                     	mov	eax, dword ptr [eax + 0x24]
102d353a: ff d0                        	call	eax
102d353c: d9 7d ee                     	fnstcw	word ptr [ebp - 0x12]
102d353f: 0f b7 45 ee                  	movzx	eax, word ptr [ebp - 0x12]
102d3543: 8b cb                        	mov	ecx, ebx
102d3545: 0d 00 0c 00 00               	or	eax, 0xc00
102d354a: 89 45 e8                     	mov	dword ptr [ebp - 0x18], eax
102d354d: 6a 00                        	push	0x0
102d354f: 68 70 0e 56 10               	push	0x10560e70
102d3554: d9 6d e8                     	fldcw	word ptr [ebp - 0x18]
102d3557: df 7d e4                     	fistp	qword ptr [ebp - 0x1c]
102d355a: 8b 45 e4                     	mov	eax, dword ptr [ebp - 0x1c]
102d355d: 89 87 40 32 00 00            	mov	dword ptr [edi + 0x3240], eax
102d3563: 8b 03                        	mov	eax, dword ptr [ebx]
102d3565: d9 6d ee                     	fldcw	word ptr [ebp - 0x12]
102d3568: ff 50 1c                     	call	dword ptr [eax + 0x1c]
102d356b: 89 87 44 32 00 00            	mov	dword ptr [edi + 0x3244], eax
102d3571: 8b 03                        	mov	eax, dword ptr [ebx]
102d3573: 51                           	push	ecx
102d3574: c7 04 24 00 00 00 00         	mov	dword ptr [esp], 0x0
102d357b: 8b cb                        	mov	ecx, ebx
102d357d: 68 80 0e 56 10               	push	0x10560e80
