=== 32-Character-UpdateSelf  RVA 0x0004cad0  sym=?UpdateSelf@Character@GAME@@UAEXH@Z ===
  0x0004cad0  push     ebp
  0x0004cad1  mov      ebp, esp
  0x0004cad3  push     -1
  0x0004cad5  push     0x104c2cbc
  0x0004cada  mov      eax, dword ptr fs:[0]
  0x0004cae0  push     eax
  0x0004cae1  mov      dword ptr fs:[0], esp
  0x0004cae8  sub      esp, 0x58
  0x0004caeb  push     esi
  0x0004caec  mov      esi, dword ptr [ebp + 8]
  0x0004caef  push     edi
  0x0004caf0  mov      edi, ecx
  0x0004caf2  push     esi
  0x0004caf3  mov      dword ptr [ebp - 0x14], edi
  0x0004caf6  call     dword ptr [0x104e5394]   ; f32=1.16497e-38 i32=8313492 f64=2.74613e-306
  0x0004cafc  mov      ecx, dword ptr [edi + 0x3064]
  0x0004cb02  test     ecx, ecx
  0x0004cb04  je       0x1004cb0c
  0x0004cb06  push     esi
  0x0004cb07  call     0x100b2600   ; -> ?CalculateAllocatedMemory@CharFxPak@GAME@@QBEIXZ+0x16a0
  0x0004cb0c  mov      dword ptr [edi + 0x1894], 0
  0x0004cb16  test     esi, esi
  0x0004cb18  jle      0x1004d0eb
  0x0004cb1e  push     1
  0x0004cb20  lea      ecx, [edi + 0x184c]
  0x0004cb26  call     dword ptr [0x104e5598]   ; f32=1.16591e-38 i32=8320210 f64=2.75525e-306
  0x0004cb2c  lea      ecx, [edi + 0x184c]
  0x0004cb32  call     dword ptr [0x104e560c]   ; f32=1.16615e-38 i32=8321912 f64=2.75757e-306
  0x0004cb38  add      dword ptr [edi + 0x30ac], eax
  0x0004cb3e  mov      dword ptr [edi + 0x1894], eax
  0x0004cb44  mov      eax, dword ptr [edi + 0x3008]
  0x0004cb4a  test     eax, eax
  0x0004cb4c  jle      0x1004cb56
  0x0004cb4e  sub      eax, esi
  0x0004cb50  mov      dword ptr [edi + 0x3008], eax
  0x0004cb56  push     esi
  0x0004cb57  lea      ecx, [edi + 0x190c]
  0x0004cb5d  call     0x10317380   ; -> ?ContributeMiscConversionAttributes@PetPlayerScaling@GAME@@UBEXAAVConversionAttributeAccumulator@2@@Z+0xcf0
  0x0004cb62  push     esi
  0x0004cb63  lea      ecx, [edi + 0x1918]
  0x0004cb69  call     0x10317380   ; -> ?ContributeMiscConversionAttributes@PetPlayerScaling@GAME@@UBEXAAVConversionAttributeAccumulator@2@@Z+0xcf0
  0x0004cb6e  push     dword ptr [edi + 0x1894]
  0x0004cb74  lea      ecx, [edi + 0x980]
  0x0004cb7a  call     0x10317a40   ; -> ?Update@PFxManager@GAME@@QAEXH@Z
  0x0004cb7f  mov      eax, dword ptr [edi + 0x3034]
  0x0004cb85  mov      eax, dword ptr [eax]
  0x0004cb87  cmp      eax, dword ptr [edi + 0x3034]
  0x0004cb8d  je       0x1004cc02
  0x0004cb8f  nop      
  0x0004cb90  mov      ecx, dword ptr [edi + 0x1894]
  0x0004cb96  sub      dword ptr [eax + 0x28], ecx
  0x0004cb99  cmp      dword ptr [eax + 0x28], 0
  0x0004cb9d  jg       0x1004cbb3
  0x0004cb9f  push     eax
  0x0004cba0  lea      eax, [ebp - 0x10]
  0x0004cba3  push     eax
  0x0004cba4  lea      ecx, [edi + 0x3034]
  0x0004cbaa  call     0x1005fba0   ; -> ?SelectPrimaryAction@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MAE_N_N_N1ABVWorldVec3@2@AAI1@Z+0x1b00
  0x0004cbaf  mov      eax, dword ptr [eax]
  0x0004cbb1  jmp      0x1004cbf7   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x127
  0x0004cbb3  cmp      byte ptr [eax + 0xd], 0
  0x0004cbb7  jne      0x1004cbf7
  0x0004cbb9  mov      ecx, dword ptr [eax + 8]
  0x0004cbbc  cmp      byte ptr [ecx + 0xd], 0
  0x0004cbc0  jne      0x1004cbdc
  0x0004cbc2  mov      eax, ecx
  0x0004cbc4  mov      ecx, dword ptr [eax]
  0x0004cbc6  cmp      byte ptr [ecx + 0xd], 0
  0x0004cbca  jne      0x1004cbf7
  0x0004cbcc  nop      dword ptr [eax]
  0x0004cbd0  mov      eax, ecx
  0x0004cbd2  mov      ecx, dword ptr [eax]
  0x0004cbd4  cmp      byte ptr [ecx + 0xd], 0
  0x0004cbd8  je       0x1004cbd0
  0x0004cbda  jmp      0x1004cbf7   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x127
  0x0004cbdc  mov      ecx, dword ptr [eax + 4]
  0x0004cbdf  cmp      byte ptr [ecx + 0xd], 0
  0x0004cbe3  jne      0x1004cbf5
  0x0004cbe5  cmp      eax, dword ptr [ecx + 8]
  0x0004cbe8  jne      0x1004cbf5
  0x0004cbea  mov      eax, ecx
  0x0004cbec  mov      ecx, dword ptr [ecx + 4]
  0x0004cbef  cmp      byte ptr [ecx + 0xd], 0
  0x0004cbf3  je       0x1004cbe5
  0x0004cbf5  mov      eax, ecx
  0x0004cbf7  cmp      eax, dword ptr [edi + 0x3034]
  0x0004cbfd  jne      0x1004cb90
  0x0004cbff  mov      esi, dword ptr [ebp + 8]
  0x0004cc02  mov      eax, dword ptr [edi]
  0x0004cc04  mov      ecx, edi
  0x0004cc06  mov      eax, dword ptr [eax + 0x21c]
  0x0004cc0c  call     eax
  0x0004cc0e  cmp      eax, 4
  0x0004cc11  je       0x1004d05e
  0x0004cc17  mov      eax, dword ptr [edi]
  0x0004cc19  mov      ecx, edi
  0x0004cc1b  mov      eax, dword ptr [eax + 0x228]
  0x0004cc21  call     eax
  0x0004cc23  add      eax, -3
  0x0004cc26  cmp      eax, 0x12
  0x0004cc29  ja       0x1004ce09
  0x0004cc2f  movzx    eax, byte ptr [eax + 0x1004d264]
  0x0004cc36  jmp      dword ptr [eax*4 + 0x1004d254]
  0x0004cc3d  mov      ecx, edi
  0x0004cc3f  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x0004cc45  lea      ecx, [ebp - 0x30]
  0x0004cc48  mov      dword ptr [ebp + 8], eax
  0x0004cc4b  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x0004cc51  push     dword ptr [edi + 0x1c9c]
  0x0004cc57  mov      eax, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0004cc5c  call     eax
  0x0004cc5e  mov      ecx, eax
  0x0004cc60  call     0x1000b150   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd90
  0x0004cc65  mov      dword ptr [ebp - 0x10], eax
  0x0004cc68  test     eax, eax
  0x0004cc6a  je       0x1004cc94
  0x0004cc6c  mov      edx, dword ptr [eax]
  0x0004cc6e  mov      ecx, eax
  0x0004cc70  mov      edx, dword ptr [edx + 0x30]
  0x0004cc73  call     edx
  0x0004cc75  test     al, al
  0x0004cc77  je       0x1004cc94
  0x0004cc79  mov      ecx, dword ptr [ebp + 8]
  0x0004cc7c  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004cc82  test     eax, eax
  0x0004cc84  je       0x1004cc94
  0x0004cc86  mov      ecx, dword ptr [ebp - 0x10]
  0x0004cc89  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x0004cc8f  movups   xmm0, xmmword ptr [eax]
  0x0004cc92  jmp      0x1004ccb8   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x1e8
  0x0004cc94  lea      ecx, [edi + 0x1ca0]
  0x0004cc9a  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004cca0  test     eax, eax
  0x0004cca2  je       0x1004ccfb
  0x0004cca4  mov      ecx, dword ptr [ebp + 8]
  0x0004cca7  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004ccad  test     eax, eax
  0x0004ccaf  je       0x1004ccfb
  0x0004ccb1  movups   xmm0, xmmword ptr [edi + 0x1ca0]
  0x0004ccb8  cmp      byte ptr [edi + 0x1cb4], 0
  0x0004ccbf  movups   xmmword ptr [ebp - 0x30], xmm0
  0x0004ccc3  je       0x1004ccfb
  0x0004ccc5  lea      eax, [ebp - 0x30]
  0x0004ccc8  mov      byte ptr [edi + 0x1cb6], 0
  0x0004cccf  push     eax
  0x0004ccd0  push     dword ptr [ebp + 8]
  0x0004ccd3  lea      eax, [ebp - 0x20]
  0x0004ccd6  push     eax
  0x0004ccd7  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004ccdc  mov      ecx, dword ptr [eax]
  0x0004ccde  mov      ecx, dword ptr [ecx + 0x28]
  0x0004cce1  call     dword ptr [0x104e5610]   ; f32=1.16615e-38 i32=8321950 f64=2.75765e-306
  0x0004cce7  push     dword ptr [ebp + 8]
  0x0004ccea  lea      eax, [ebp - 0x20]
  0x0004cced  mov      ecx, edi
  0x0004ccef  push     eax
  0x0004ccf0  push     esi
  0x0004ccf1  call     0x10049290   ; -> ?RotateTowards@Character@GAME@@QAE_NHABVVec3@2@ABVWorldVec3@2@@Z
  0x0004ccf6  jmp      0x1004ce09   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x339
  0x0004ccfb  cmp      byte ptr [edi + 0x1cb6], 0
  0x0004cd02  je       0x1004ce09
  0x0004cd08  lea      ecx, [edi + 0x3020]
  0x0004cd0e  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004cd14  test     eax, eax
  0x0004cd16  je       0x1004ce09
  0x0004cd1c  lea      eax, [edi + 0x3020]
  0x0004cd22  push     eax
  0x0004cd23  push     dword ptr [ebp + 8]
  0x0004cd26  lea      eax, [ebp - 0x20]
  0x0004cd29  push     eax
  0x0004cd2a  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004cd2f  mov      ecx, dword ptr [eax]
  0x0004cd31  mov      ecx, dword ptr [ecx + 0x28]
  0x0004cd34  call     dword ptr [0x104e5610]   ; f32=1.16615e-38 i32=8321950 f64=2.75765e-306
  0x0004cd3a  push     dword ptr [ebp + 8]
  0x0004cd3d  jmp      0x1004cdf2   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x322
  0x0004cd42  push     dword ptr [edi + 0x1120]
  0x0004cd48  mov      eax, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0004cd4d  call     eax
  0x0004cd4f  mov      ecx, eax
  0x0004cd51  call     0x100625d0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x4e0
  0x0004cd56  mov      ecx, edi
  0x0004cd58  mov      esi, eax
  0x0004cd5a  mov      edi, dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x0004cd60  call     edi
  0x0004cd62  mov      edx, dword ptr [esi]
  0x0004cd64  mov      ecx, esi
  0x0004cd66  mov      dword ptr [ebp - 0x10], eax
  0x0004cd69  mov      edx, dword ptr [edx + 0x34]
  0x0004cd6c  call     edx
  0x0004cd6e  push     eax
  0x0004cd6f  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0004cd75  mov      ecx, eax
  0x0004cd77  call     0x10034d50   ; -> ?CalculateAllocatedMemory@AuraManager@GAME@@QBEIXZ+0x370
  0x0004cd7c  mov      ecx, eax
  0x0004cd7e  call     edi
  0x0004cd80  mov      esi, dword ptr [ebp - 0x10]
  0x0004cd83  push     eax
  0x0004cd84  push     esi
  0x0004cd85  lea      eax, [ebp - 0x20]
  0x0004cd88  push     eax
  0x0004cd89  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004cd8e  mov      ecx, dword ptr [eax]
  0x0004cd90  mov      ecx, dword ptr [ecx + 0x28]
  0x0004cd93  call     dword ptr [0x104e5610]   ; f32=1.16615e-38 i32=8321950 f64=2.75765e-306
  0x0004cd99  mov      edi, dword ptr [ebp - 0x14]
  0x0004cd9c  lea      eax, [ebp - 0x20]
  0x0004cd9f  push     esi
  0x0004cda0  mov      esi, dword ptr [ebp + 8]
  0x0004cda3  mov      ecx, edi
  0x0004cda5  push     eax
  0x0004cda6  push     esi
  0x0004cda7  call     0x10049290   ; -> ?RotateTowards@Character@GAME@@QAE_NHABVVec3@2@ABVWorldVec3@2@@Z
  0x0004cdac  jmp      0x1004ce09   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x339
  0x0004cdae  cmp      byte ptr [edi + 0x1cb6], 0
  0x0004cdb5  je       0x1004ce09
  0x0004cdb7  lea      ecx, [edi + 0x3020]
  0x0004cdbd  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x0004cdc3  test     eax, eax
  0x0004cdc5  je       0x1004ce09
  0x0004cdc7  mov      ecx, edi
  0x0004cdc9  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x0004cdcf  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004cdd5  mov      esi, eax
  0x0004cdd7  lea      eax, [edi + 0x3020]
  0x0004cddd  push     eax
  0x0004cdde  push     esi
  0x0004cddf  mov      ecx, dword ptr [ecx]
  0x0004cde1  lea      eax, [ebp - 0x20]
  0x0004cde4  push     eax
  0x0004cde5  mov      ecx, dword ptr [ecx + 0x28]
  0x0004cde8  call     dword ptr [0x104e5610]   ; f32=1.16615e-38 i32=8321950 f64=2.75765e-306
  0x0004cdee  push     esi
  0x0004cdef  mov      esi, dword ptr [ebp + 8]
  0x0004cdf2  lea      eax, [ebp - 0x20]
  0x0004cdf5  mov      ecx, edi
  0x0004cdf7  push     eax
  0x0004cdf8  push     esi
  0x0004cdf9  call     0x10049290   ; -> ?RotateTowards@Character@GAME@@QAE_NHABVVec3@2@ABVWorldVec3@2@@Z
  0x0004cdfe  test     al, al
  0x0004ce00  je       0x1004ce09
  0x0004ce02  mov      byte ptr [edi + 0x1cb6], 0
  0x0004ce09  mov      ecx, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004ce0f  mov      ecx, dword ptr [ecx]
  0x0004ce11  call     dword ptr [0x104e5614]   ; f32=1.16616e-38 i32=8322010 f64=2.75772e-306
  0x0004ce17  lea      eax, [edi + 0xa18]
  0x0004ce1d  push     eax
  0x0004ce1e  push     dword ptr [edi + 0x1894]
  0x0004ce24  lea      ecx, [edi + 0x3dc]
  0x0004ce2a  call     0x100dfc80   ; -> ?Update@CombatManager@GAME@@QAEXHAAVCharacterBio@2@@Z
  0x0004ce2f  push     dword ptr [edi + 0x1894]
  0x0004ce35  lea      ecx, [edi + 0x88c]
  0x0004ce3b  push     edi
  0x0004ce3c  call     0x10034430   ; -> ?Update@AuraManager@GAME@@QAEXAAVActor@2@H@Z
  0x0004ce41  mov      eax, dword ptr [edi]
  0x0004ce43  mov      ecx, edi
  0x0004ce45  mov      eax, dword ptr [eax + 0x22c]
  0x0004ce4b  call     eax
  0x0004ce4d  test     al, al
  0x0004ce4f  je       0x1004ce62
  0x0004ce51  push     dword ptr [edi + 0x1894]
  0x0004ce57  mov      ecx, dword ptr [edi + 0x950]
  0x0004ce5d  call     0x100781a0   ; -> ?Update@CharacterMovementManager@GAME@@QAEXH@Z
  0x0004ce62  call     dword ptr [0x104e5600]   ; f32=1.16611e-38 i32=8321642 f64=2.75724e-306
  0x0004ce68  mov      ecx, eax
  0x0004ce6a  call     dword ptr [0x104e5618]   ; f32=1.16617e-38 i32=8322064 f64=2.75777e-306
  0x0004ce70  test     al, al
  0x0004ce72  je       0x1004ce7b
  0x0004ce74  mov      ecx, edi
  0x0004ce76  call     0x1004d3c0   ; -> ?DebugRenderPathing@Character@GAME@@QAEXXZ
  0x0004ce7b  mov      ecx, dword ptr [edi + 0x1cbc]
  0x0004ce81  test     ecx, ecx
  0x0004ce83  je       0x1004ce90
  0x0004ce85  push     dword ptr [edi + 0x1894]
  0x0004ce8b  call     0x101a2b10   ; -> ?IsRegisteredForForcedUpdates@Character@GAME@@QBE_NXZ+0x160
  0x0004ce90  movss    xmm5, dword ptr [edi + 0x9fc]
  0x0004ce98  movss    xmm4, dword ptr [edi + 0xa00]
  0x0004cea0  comiss   xmm4, xmm5
  0x0004cea3  movd     xmm3, esi
  0x0004cea7  cvtdq2ps xmm3, xmm3
  0x0004ceaa  mulss    xmm3, dword ptr [0x105f575c]   ; f32=0.001 i32=981668463 f64=1.972e-24
  0x0004ceb2  mulss    xmm3, dword ptr [edi + 0xa04]
  0x0004ceba  ja       0x1004cec3
  0x0004cebc  xorps    xmm3, xmmword ptr [0x105f5b10]   ; f32=-0 i32=-2147483648 f64=-1.061e-314
  0x0004cec3  movaps   xmm2, xmm4
  0x0004cec6  movaps   xmm0, xmm3
  0x0004cec9  andps    xmm0, xmmword ptr [0x105f5af0]   ; f32=nan i32=2147483647 f64=nan
  0x0004ced0  subss    xmm2, xmm5
  0x0004ced4  andps    xmm2, xmmword ptr [0x105f5af0]   ; f32=nan i32=2147483647 f64=nan
  0x0004cedb  comiss   xmm0, xmm2
  0x0004cede  jbe      0x1004ceea
  0x0004cee0  movss    dword ptr [edi + 0x9fc], xmm4
  0x0004cee8  jmp      0x1004cef6   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x426
  0x0004ceea  addss    xmm3, xmm5
  0x0004ceee  movss    dword ptr [edi + 0x9fc], xmm3
  0x0004cef6  mov      eax, dword ptr [edi + 0x307c]
  0x0004cefc  xor      ecx, ecx
  0x0004cefe  sub      eax, dword ptr [edi + 0x3078]
  0x0004cf04  sar      eax, 2
  0x0004cf07  mov      dword ptr [ebp + 8], ecx
  0x0004cf0a  test     eax, eax
  0x0004cf0c  je       0x1004cf39
  0x0004cf0e  nop      
  0x0004cf10  mov      eax, dword ptr [edi + 0x3078]
  0x0004cf16  push     esi
  0x0004cf17  mov      ecx, dword ptr [eax + ecx*4]
  0x0004cf1a  mov      eax, dword ptr [ecx]
  0x0004cf1c  call     dword ptr [eax + 0x18]
  0x0004cf1f  mov      eax, dword ptr [edi + 0x307c]
  0x0004cf25  mov      ecx, dword ptr [ebp + 8]
  0x0004cf28  sub      eax, dword ptr [edi + 0x3078]
  0x0004cf2e  inc      ecx
  0x0004cf2f  sar      eax, 2
  0x0004cf32  mov      dword ptr [ebp + 8], ecx
  0x0004cf35  cmp      ecx, eax
  0x0004cf37  jb       0x1004cf10
  0x0004cf39  mov      eax, dword ptr [edi + 0x1cbc]
  0x0004cf3f  test     eax, eax
  0x0004cf41  je       0x1004cf88
  0x0004cf43  mov      ecx, eax
  0x0004cf45  call     0x101a2c00   ; -> ?IsRegisteredForForcedUpdates@Character@GAME@@QBE_NXZ+0x250
  0x0004cf4a  test     al, al
  0x0004cf4c  je       0x1004cf88
  0x0004cf4e  mov      ecx, dword ptr [edi + 0x1cbc]
  0x0004cf54  call     0x101a2c60   ; -> ?IsRegisteredForForcedUpdates@Character@GAME@@QBE_NXZ+0x2b0
  0x0004cf59  mov      eax, dword ptr [edi + 0x1ba4]
  0x0004cf5f  mov      dword ptr [ebp + 8], eax
  0x0004cf62  mov      ecx, dword ptr [eax + 4]
  0x0004cf65  test     ecx, ecx
  0x0004cf67  je       0x1004cf88
  0x0004cf69  mov      eax, dword ptr [ecx]
  0x0004cf6b  call     dword ptr [eax + 0xc]
  0x0004cf6e  mov      eax, dword ptr [ebp + 8]
  0x0004cf71  mov      ecx, dword ptr [eax + 4]
  0x0004cf74  test     ecx, ecx
  0x0004cf76  je       0x1004cf81
  0x0004cf78  mov      eax, dword ptr [ecx]
  0x0004cf7a  push     1
  0x0004cf7c  call     dword ptr [eax]
  0x0004cf7e  mov      eax, dword ptr [ebp + 8]
  0x0004cf81  mov      dword ptr [eax + 4], 0
  0x0004cf88  mov      eax, dword ptr [edi + 0x11e4]
  0x0004cf8e  movd     xmm0, dword ptr [edi + 0x11e8]
  0x0004cf96  add      eax, esi
  0x0004cf98  movss    xmm2, dword ptr [0x105f593c]   ; f32=-0 i32=-2147483648 f64=-5.87891e-39
  0x0004cfa0  cvtdq2ps xmm0, xmm0
  0x0004cfa3  mov      dword ptr [edi + 0x11e4], eax
  0x0004cfa9  movd     xmm1, eax
  0x0004cfad  cvtdq2ps xmm1, xmm1
  0x0004cfb0  movss    xmm3, dword ptr [0x105f5808]   ; f32=1 i32=1065353216 f64=5.26354e-315
  0x0004cfb8  addss    xmm1, xmm0
  0x0004cfbc  movaps   xmm4, xmm1
  0x0004cfbf  movss    dword ptr [ebp + 8], xmm1
  0x0004cfc4  mulss    xmm4, dword ptr [0x105f575c]   ; f32=0.001 i32=981668463 f64=1.972e-24
  0x0004cfcc  movss    xmm1, dword ptr [0x105f5934]   ; f32=8.38861e+06 i32=1258291200 f64=5.88763e+53
  0x0004cfd4  andps    xmm2, xmm4
  0x0004cfd7  movaps   xmm0, xmm4
  0x0004cfda  xorps    xmm0, xmm2
  0x0004cfdd  cmpltss  xmm0, xmm1
  0x0004cfe2  andps    xmm1, xmm0
  0x0004cfe5  movaps   xmm0, xmm4
  0x0004cfe8  orps     xmm1, xmm2
  0x0004cfeb  addss    xmm0, xmm1
  0x0004cfef  subss    xmm0, xmm1
  0x0004cff3  movaps   xmm1, xmm0
  0x0004cff6  subss    xmm1, xmm4
  0x0004cffa  cmpnless xmm1, xmm2
  0x0004cfff  andps    xmm1, xmm3
  0x0004d002  subss    xmm0, xmm1
  0x0004d006  call     0x104bfcf0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x38040
  0x0004d00b  test     eax, eax
  0x0004d00d  je       0x1004d052
  0x0004d00f  add      dword ptr [edi + 0x11ec], eax
  0x0004d015  movss    xmm1, dword ptr [ebp + 8]
  0x0004d01a  movd     xmm0, eax
  0x0004d01e  cvtdq2pd xmm0, xmm0
  0x0004d022  shr      eax, 0x1f
  0x0004d025  mov      dword ptr [edi + 0x11e4], 0
  0x0004d02f  addsd    xmm0, qword ptr [eax*8 + 0x105f5ae0]
  0x0004d038  cvtpd2ps xmm0, xmm0
  0x0004d03c  mulss    xmm0, dword ptr [0x105f5918]   ; f32=1000 i32=1148846080 f64=8.53804e+24
  0x0004d044  subss    xmm1, xmm0
  0x0004d048  cvttss2si eax, xmm1
  0x0004d04c  mov      dword ptr [edi + 0x11e8], eax
  0x0004d052  mov      byte ptr [edi + 0x1350], 1
  0x0004d059  jmp      0x1004d0eb   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x61b
  0x0004d05e  mov      eax, dword ptr [edi + 0x3040]
  0x0004d064  test     eax, eax
  0x0004d066  jle      0x1004d089
  0x0004d068  sub      eax, dword ptr [edi + 0x1894]
  0x0004d06e  mov      dword ptr [edi + 0x3040], eax
  0x0004d074  test     eax, eax
  0x0004d076  jg       0x1004d089
  0x0004d078  mov      ecx, edi
  0x0004d07a  mov      dword ptr [edi + 0x3040], 0
  0x0004d084  call     0x10047810   ; -> ?ClearDamageFxs@Character@GAME@@QAEXXZ
  0x0004d089  mov      eax, dword ptr [edi]
  0x0004d08b  mov      ecx, edi
  0x0004d08d  mov      eax, dword ptr [eax]
  0x0004d08f  call     eax
  0x0004d091  cmp      eax, 0x107ff5a0
  0x0004d096  je       0x1004d0eb
  0x0004d098  mov      ecx, dword ptr [eax + 8]
  0x0004d09b  test     ecx, ecx
  0x0004d09d  je       0x1004d0b5
  0x0004d09f  cmp      ecx, 0x107ff5a0
  0x0004d0a5  je       0x1004d0eb
  0x0004d0a7  push     0x107ff5a0
  0x0004d0ac  call     0x1048a5f0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x2940
  0x0004d0b1  test     al, al
  0x0004d0b3  jne      0x1004d0eb
  0x0004d0b5  mov      eax, dword ptr [edi + 0x3060]
  0x0004d0bb  test     eax, eax
  0x0004d0bd  jle      0x1004d0eb
  0x0004d0bf  sub      eax, esi
  0x0004d0c1  mov      dword ptr [edi + 0x3060], eax
  0x0004d0c7  test     eax, eax
  0x0004d0c9  jg       0x1004d0eb
  0x0004d0cb  cmp      dword ptr [edi + 0x3040], 0
  0x0004d0d2  jle      0x1004d0db
  0x0004d0d4  mov      ecx, edi
  0x0004d0d6  call     0x10047810   ; -> ?ClearDamageFxs@Character@GAME@@QAEXXZ
  0x0004d0db  cmp      byte ptr [edi + 0x1cc0], 0
  0x0004d0e2  je       0x1004d0eb
  0x0004d0e4  mov      ecx, edi
  0x0004d0e6  call     0x100490b0   ; -> ?DestroyMe@Character@GAME@@QAEXXZ
  0x0004d0eb  mov      ecx, dword ptr [edi + 0x3090]
  0x0004d0f1  test     ecx, ecx
  0x0004d0f3  je       0x1004d10c
  0x0004d0f5  cmp      dword ptr [ecx + 0x20], 0
  0x0004d0f9  jne      0x1004d102
  0x0004d0fb  push     0
  0x0004d0fd  call     0x1012fd10   ; -> ?Build@Conversation@GAME@@AAEX_N@Z
  0x0004d102  mov      eax, dword ptr [edi]
  0x0004d104  mov      ecx, edi
  0x0004d106  call     dword ptr [eax + 0x134]
  0x0004d10c  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x0004d111  mov      ecx, dword ptr [eax]
  0x0004d113  mov      ecx, dword ptr [ecx + 0x20]
  0x0004d116  call     dword ptr [0x104e561c]   ; f32=1.16617e-38 i32=8322102 f64=2.75783e-306
  0x0004d11c  test     al, al
  0x0004d11e  sete     al
  0x0004d121  mov      byte ptr [ebp + 0xb], al
  0x0004d124  cmp      al, byte ptr [edi + 0x30b0]
  0x0004d12a  je       0x1004d226
  0x0004d130  cmp      dword ptr [edi + 0x30c8], 0x10
  0x0004d137  lea      eax, [edi + 0x30b4]
  0x0004d13d  jb       0x1004d141
  0x0004d13f  mov      eax, dword ptr [eax]
  0x0004d141  lea      ecx, [edi + 0x600]
  0x0004d147  push     eax
  0x0004d148  call     0x1043bc60   ; -> ?FindSkillId@SkillManager@GAME@@QBE?BIPBD@Z
  0x0004d14d  test     eax, eax
  0x0004d14f  je       0x1004d21d
  0x0004d155  push     eax
  0x0004d156  lea      ecx, [edi + 0x600]
  0x0004d15c  call     0x1043c700   ; -> ?GetSkillReferenceNumber@SkillManager@GAME@@QBE?BII@Z
  0x0004d161  cmp      byte ptr [ebp + 0xb], 0
  0x0004d165  mov      dword ptr [ebp - 0x14], eax
  0x0004d168  je       0x1004d1f4
  0x0004d16e  mov      ecx, dword ptr fs:[0x2c]
  0x0004d175  mov      edx, dword ptr [0x10808080]   ; f32=0 i32=0 f64=0
  0x0004d17b  mov      edx, dword ptr [ecx + edx*4]
  0x0004d17e  mov      ecx, dword ptr [0x1080b1a4]   ; f32=0.0190718 i32=1016872062 f64=9.01345e-16
  0x0004d184  cmp      ecx, dword ptr [edx + 4]
  0x0004d18a  jle      0x1004d1cd
  0x0004d18c  push     0x1080b1a4
  0x0004d191  call     0x104beadf   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36e2f
  0x0004d196  add      esp, 4
  0x0004d199  cmp      dword ptr [0x1080b1a4], -1   ; f32=0.0190718 i32=1016872062 f64=9.01345e-16
  0x0004d1a0  jne      0x1004d1cd
  0x0004d1a2  push     0x104f5408
  0x0004d1a7  push     0x1080b1a8
  0x0004d1ac  mov      dword ptr [ebp - 4], 0
  0x0004d1b3  call     dword ptr [0x104e5258]   ; f32=1.16438e-38 i32=8309306 f64=2.74045e-306
  0x0004d1b9  push     0x1080b1a4
  0x0004d1be  mov      dword ptr [ebp - 4], 0xffffffff
  0x0004d1c5  call     0x104beaa0   ; -> ?GetLeftHandType@WeaponArmor_Offhand@GAME@@UBE?AW4EquipmentHandTypes@2@XZ+0x36df0
  0x0004d1ca  add      esp, 0xc
  0x0004d1cd  lea      eax, [ebp - 0x64]
  0x0004d1d0  mov      ecx, edi
  0x0004d1d2  push     eax
  0x0004d1d3  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x0004d1d9  push     eax
  0x0004d1da  mov      ecx, edi
  0x0004d1dc  call     dword ptr [0x104e5090]   ; f32=1.16349e-38 i32=8302926 f64=2.73178e-306
  0x0004d1e2  push     eax
  0x0004d1e3  push     0x1080b1a8
  0x0004d1e8  push     dword ptr [ebp - 0x14]
  0x0004d1eb  mov      ecx, edi
  0x0004d1ed  call     0x10058580   ; -> ?ActivateSkill@Character@GAME@@QAEXIABVName@2@IABVWorldVec3@2@@Z
  0x0004d1f2  jmp      0x1004d21d   ; -> ?UpdateSelf@Character@GAME@@UAEXH@Z+0x74d
  0x0004d1f4  push     eax
  0x0004d1f5  lea      ecx, [edi + 0x600]
  0x0004d1fb  call     0x1043c8b0   ; -> ?GetSkillIdFromReference@SkillManager@GAME@@QBE?BII@Z
  0x0004d200  push     eax
  0x0004d201  call     dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x0004d207  mov      ecx, eax
  0x0004d209  call     0x100629c0   ; -> ?GetSkillUseTolerance@?$ControllerAIStateT@VControllerNpc2@GAME@@VNpc@2@@GAME@@MBEMI@Z+0x8d0
  0x0004d20e  test     eax, eax
  0x0004d210  je       0x1004d21d
  0x0004d212  mov      edx, dword ptr [eax]
  0x0004d214  mov      ecx, eax
  0x0004d216  push     edi
  0x0004d217  call     dword ptr [edx + 0x24c]
  0x0004d21d  mov      al, byte ptr [ebp + 0xb]
  0x0004d220  mov      byte ptr [edi + 0x30b0], al
  0x0004d226  mov      eax, dword ptr [edi + 0x1df8]
  0x0004d22c  test     eax, eax
  0x0004d22e  jle      0x1004d238
  0x0004d230  sub      eax, esi
  0x0004d232  mov      dword ptr [edi + 0x1df8], eax
  0x0004d238  mov      eax, dword ptr [edi]
  0x0004d23a  mov      ecx, edi
  0x0004d23c  call     dword ptr [eax + 0x1ec]
  0x0004d242  mov      ecx, dword ptr [ebp - 0xc]
  0x0004d245  pop      edi
  0x0004d246  pop      esi
  0x0004d247  mov      dword ptr fs:[0], ecx
  0x0004d24e  mov      esp, ebp
  0x0004d250  pop      ebp
  0x0004d251  ret      4
  0x0004d254  scasb    al, byte ptr es:[edi]
  0x0004d255  int      4
  0x0004d257  adc      byte ptr [0x421004cc], bh
  0x0004d25d  int      4
  0x0004d25f  adc      byte ptr [ecx], cl
  0x0004d261  into     
  0x0004d262  add      al, 0x10
  0x0004d264  add      byte ptr [ebx], al
  0x0004d266  add      eax, dword ptr [ebx]
  0x0004d268  add      dword ptr [ebx], eax
  0x0004d26a  add      eax, dword ptr [ebx]
  0x0004d26c  add      eax, dword ptr [ebx]
  0x0004d26e  add      eax, dword ptr [ebx]
  0x0004d270  add      eax, dword ptr [edx]
  0x0004d272  add      eax, dword ptr [ebx]
  0x0004d274  add      byte ptr [ebx], al
  0x0004d276  add      ah, cl
  0x0004d278  int3     
  0x0004d279  int3     
  0x0004d27a  int3     
  0x0004d27b  int3     
  0x0004d27c  int3     
  0x0004d27d  int3     
  0x0004d27e  int3     
  0x0004d27f  int3     
