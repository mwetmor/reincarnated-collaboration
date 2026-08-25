=== 91-Pursue-OnBegin RVA 0x000fee40 sym=?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ ===
  0x000fee40  push     ebp
  0x000fee41  mov      ebp, esp
  0x000fee43  push     -1
  0x000fee45  push     0x104c8480
  0x000fee4a  mov      eax, dword ptr fs:[0]
  0x000fee50  push     eax
  0x000fee51  mov      dword ptr fs:[0], esp
  0x000fee58  sub      esp, 0x9c
  0x000fee5e  push     ebx
  0x000fee5f  mov      ebx, ecx
  0x000fee61  mov      dword ptr [ebp - 0x18], ebx
  0x000fee64  mov      ecx, dword ptr [ebx + 4]
  0x000fee67  mov      eax, dword ptr [ecx]
  0x000fee69  mov      eax, dword ptr [eax + 0xfc]
  0x000fee6f  call     eax
  0x000fee71  test     al, al
  0x000fee73  jne      0x100feefd
  0x000fee79  push     4
  0x000fee7b  push     0x1052cda8
  0x000fee80  lea      ecx, [ebp - 0x5c]
  0x000fee83  mov      dword ptr [ebp - 0x48], 0xf
  0x000fee8a  mov      dword ptr [ebp - 0x4c], 0
  0x000fee91  mov      byte ptr [ebp - 0x5c], al
  0x000fee94  call     0x10008b80   ; -> ?AddTimeToLive@Skill@GAME@@UAEXH@Z+0x6b0
  0x000fee99  mov      dword ptr [ebp - 4], 0
  0x000feea0  lea      ecx, [ebp - 0x78]
  0x000feea3  mov      dword ptr [ebp - 0x84], 0
  0x000feead  mov      dword ptr [ebp - 0x80], 0
  0x000feeb4  mov      dword ptr [ebp - 0x7c], 0
  0x000feebb  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000feec1  mov      ecx, dword ptr [ebx + 4]
  0x000feec4  lea      eax, [ebp - 0x84]
  0x000feeca  push     eax
  0x000feecb  lea      eax, [ebp - 0x5c]
  0x000feece  push     eax
  0x000feecf  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000feed4  mov      edx, dword ptr [ebp - 0x48]
  0x000feed7  cmp      edx, 0x10
  0x000feeda  jb       0x100ff363
  0x000feee0  mov      ecx, dword ptr [ebp - 0x5c]
  0x000feee3  inc      edx
  0x000feee4  push     1
  0x000feee6  call     0x10008d00   ; -> ??1AuraContainer@GAME@@QAE@XZ+0x40
  0x000feeeb  add      esp, 4
  0x000feeee  pop      ebx
  0x000feeef  mov      ecx, dword ptr [ebp - 0xc]
  0x000feef2  mov      dword ptr fs:[0], ecx
  0x000feef9  mov      esp, ebp
  0x000feefb  pop      ebp
  0x000feefc  ret      
  0x000feefd  mov      ecx, dword ptr [ebx + 4]
  0x000fef00  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000fef05  mov      ecx, dword ptr [ebx + 4]
  0x000fef08  push     dword ptr [eax]
  0x000fef0a  call     0x100fb220   ; -> ?IsEnemyValid@ControllerMonster@GAME@@QBE_NI@Z
  0x000fef0f  test     al, al
  0x000fef11  jne      0x100fef2c
  0x000fef13  push     0x1052cdc8
  0x000fef18  lea      ecx, [ebp - 0x5c]
  0x000fef1b  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000fef20  mov      dword ptr [ebp - 4], 1
  0x000fef27  jmp      0x100feea0   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x60
  0x000fef2c  mov      ecx, dword ptr [ebx + 4]
  0x000fef2f  push     esi
  0x000fef30  push     edi
  0x000fef31  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000fef36  mov      edi, dword ptr [0x104e504c]   ; f32=1.16338e-38 i32=8302122 f64=2.73074e-306
  0x000fef3c  push     dword ptr [eax]
  0x000fef3e  call     edi
  0x000fef40  mov      ecx, eax
  0x000fef42  call     0x10034d50   ; -> ?CalculateAllocatedMemory@AuraManager@GAME@@QBEIXZ+0x370
  0x000fef47  mov      ecx, dword ptr [ebx + 4]
  0x000fef4a  mov      dword ptr [ebp - 0x64], eax
  0x000fef4d  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000fef52  mov      ecx, dword ptr [ebx + 4]
  0x000fef55  mov      eax, dword ptr [eax + 8]
  0x000fef58  mov      dword ptr [ebp - 0x68], eax
  0x000fef5b  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000fef60  mov      esi, dword ptr [ebx + 8]
  0x000fef63  mov      eax, dword ptr [eax]
  0x000fef65  mov      dword ptr [ebp - 0x14], eax
  0x000fef68  test     esi, esi
  0x000fef6a  jne      0x100fef80
  0x000fef6c  mov      eax, dword ptr [ebx + 4]
  0x000fef6f  push     dword ptr [eax + 0x24]
  0x000fef72  call     edi
  0x000fef74  mov      ecx, eax
  0x000fef76  call     0x1000b0c0   ; -> ?Reset@AchievementManager@GAME@@QAEXXZ+0xd00
  0x000fef7b  mov      esi, eax
  0x000fef7d  mov      dword ptr [ebx + 8], esi
  0x000fef80  mov      ecx, dword ptr [ebp - 0x64]
  0x000fef83  lea      eax, [ebp - 0x9c]
  0x000fef89  push     eax
  0x000fef8a  call     dword ptr [0x104e5288]   ; f32=1.16448e-38 i32=8310008 f64=2.74142e-306
  0x000fef90  push     eax
  0x000fef91  push     dword ptr [ebp - 0x68]
  0x000fef94  lea      eax, [ebp - 0x28]
  0x000fef97  mov      ecx, esi
  0x000fef99  push     dword ptr [ebp - 0x14]
  0x000fef9c  push     eax
  0x000fef9d  call     0x10049980   ; -> ?GetMoveToPoint@Character@GAME@@QBE?AVWorldVec3@2@IIABV32@@Z
  0x000fefa2  lea      ecx, [ebp - 0x28]
  0x000fefa5  call     dword ptr [0x104e524c]   ; f32=1.16436e-38 i32=8309154 f64=2.74026e-306
  0x000fefab  test     eax, eax
  0x000fefad  jne      0x100fefc8
  0x000fefaf  push     0x1052cdb8
  0x000fefb4  lea      ecx, [ebp - 0x80]
  0x000fefb7  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000fefbc  mov      dword ptr [ebp - 4], 2
  0x000fefc3  jmp      0x100ff317   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x4d7
  0x000fefc8  mov      ecx, dword ptr [ebx + 4]
  0x000fefcb  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000fefd0  push     dword ptr [eax + 8]
  0x000fefd3  call     edi
  0x000fefd5  mov      ecx, eax
  0x000fefd7  call     0x1000d4f0   ; -> ?CreateUISummaryText@AmbientCharacter@GAME@@UBEXW4GameTextClass@2@AAV?$vector@UGameTextLine@GAME@@@mem@@@Z+0x7e0
  0x000fefdc  mov      esi, eax
  0x000fefde  mov      byte ptr [ebp - 0xd], 0
  0x000fefe2  mov      byte ptr [ebp - 0xe], 0
  0x000fefe6  test     esi, esi
  0x000fefe8  je       0x100ff021
  0x000fefea  mov      edx, dword ptr [esi]
  0x000fefec  mov      ecx, esi
  0x000fefee  call     dword ptr [edx + 0x12c]
  0x000feff4  cmp      eax, 3
  0x000feff7  je       0x100ff00c
  0x000feff9  mov      eax, dword ptr [esi]
  0x000feffb  mov      ecx, esi
  0x000feffd  call     dword ptr [eax + 0x12c]
  0x000ff003  mov      byte ptr [ebp - 0xd], 0
  0x000ff007  cmp      eax, 5
  0x000ff00a  jne      0x100ff010
  0x000ff00c  mov      byte ptr [ebp - 0xd], 1
  0x000ff010  mov      eax, dword ptr [esi]
  0x000ff012  mov      ecx, esi
  0x000ff014  call     dword ptr [eax + 0x12c]
  0x000ff01a  cmp      eax, 2
  0x000ff01d  sete     byte ptr [ebp - 0xe]
  0x000ff021  mov      ecx, dword ptr [ebx + 4]
  0x000ff024  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff029  mov      ecx, dword ptr [ebx + 4]
  0x000ff02c  mov      esi, dword ptr [eax + 8]
  0x000ff02f  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff034  mov      edx, dword ptr [ebx]
  0x000ff036  mov      ecx, ebx
  0x000ff038  push     esi
  0x000ff039  push     dword ptr [eax]
  0x000ff03b  mov      eax, dword ptr [edx + 8]
  0x000ff03e  call     eax
  0x000ff040  test     al, al
  0x000ff042  jne      0x100ff2fb
  0x000ff048  cmp      byte ptr [ebp - 0xd], al
  0x000ff04b  jne      0x100ff2fb
  0x000ff051  push     ecx
  0x000ff052  lea      eax, [ebp - 0x28]
  0x000ff055  mov      dword ptr [esp], 0x3ccccccd
  0x000ff05c  push     eax
  0x000ff05d  mov      ecx, ebx
  0x000ff05f  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff064  mov      ecx, eax
  0x000ff066  call     0x10048b20   ; -> ?AlreadyThere@Character@GAME@@QBE_NABVWorldVec3@2@M@Z
  0x000ff06b  test     al, al
  0x000ff06d  je       0x100ff0cf
  0x000ff06f  push     0x1052ce54
  0x000ff074  lea      ecx, [ebp - 0x80]
  0x000ff077  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff07c  lea      ecx, [ebp - 0x60]
  0x000ff07f  mov      dword ptr [ebp - 4], 5
  0x000ff086  call     0x100e8a60   ; -> ??0ControllerAIStateData@GAME@@QAE@XZ
  0x000ff08b  mov      ecx, dword ptr [ebx + 4]
  0x000ff08e  push     eax
  0x000ff08f  lea      eax, [ebp - 0x80]
  0x000ff092  push     eax
  0x000ff093  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000ff098  lea      ecx, [ebp - 0x80]
  0x000ff09b  mov      dword ptr [ebp - 4], 0xffffffff
  0x000ff0a2  call     0x10008cc0   ; -> ??1AuraContainer@GAME@@QAE@XZ
  0x000ff0a7  mov      eax, dword ptr [0x104e5028]   ; f32=1.16329e-38 i32=8301522 f64=2.72987e-306
  0x000ff0ac  push     0x1052ce00
  0x000ff0b1  push     2
  0x000ff0b3  mov      eax, dword ptr [eax]
  0x000ff0b5  push     eax
  0x000ff0b6  mov      ecx, dword ptr [eax]
  0x000ff0b8  call     dword ptr [ecx + 0xc]
  0x000ff0bb  add      esp, 0xc
  0x000ff0be  pop      edi
  0x000ff0bf  pop      esi
  0x000ff0c0  pop      ebx
  0x000ff0c1  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff0c4  mov      dword ptr fs:[0], ecx
  0x000ff0cb  mov      esp, ebp
  0x000ff0cd  pop      ebp
  0x000ff0ce  ret      
  0x000ff0cf  mov      ecx, ebx
  0x000ff0d1  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff0d6  push     0
  0x000ff0d8  push     ecx
  0x000ff0d9  lea      ecx, [ebp - 0x28]
  0x000ff0dc  mov      dword ptr [esp], 0
  0x000ff0e3  mov      edx, dword ptr [eax]
  0x000ff0e5  push     ecx
  0x000ff0e6  mov      ecx, eax
  0x000ff0e8  mov      eax, dword ptr [edx + 0x2a4]
  0x000ff0ee  call     eax
  0x000ff0f0  test     al, al
  0x000ff0f2  jne      0x100ff10d
  0x000ff0f4  push     0x1052cdec
  0x000ff0f9  lea      ecx, [ebp - 0x80]
  0x000ff0fc  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff101  mov      dword ptr [ebp - 4], 6
  0x000ff108  jmp      0x100ff317   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x4d7
  0x000ff10d  mov      ecx, ebx
  0x000ff10f  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff114  movss    xmm0, dword ptr [eax + 0x3068]
  0x000ff11c  comiss   xmm0, dword ptr [0x105f5708]   ; f32=0 i32=0 f64=0
  0x000ff123  movss    dword ptr [ebp - 0x14], xmm0
  0x000ff128  jbe      0x100ff26f
  0x000ff12e  mov      ecx, ebx
  0x000ff130  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff135  mov      ecx, eax
  0x000ff137  call     dword ptr [0x104e55ec]   ; f32=1.16607e-38 i32=8321344 f64=2.75683e-306
  0x000ff13d  lea      ecx, [ebp - 0x38]
  0x000ff140  movups   xmm0, xmmword ptr [eax]
  0x000ff143  lea      eax, [ebp - 0x28]
  0x000ff146  push     eax
  0x000ff147  lea      eax, [ebp - 0xa8]
  0x000ff14d  push     eax
  0x000ff14e  movups   xmmword ptr [ebp - 0x38], xmm0
  0x000ff152  call     dword ptr [0x104e551c]   ; f32=1.16568e-38 i32=8318562 f64=2.75303e-306
  0x000ff158  movss    xmm1, dword ptr [eax + 4]
  0x000ff15d  movss    xmm2, dword ptr [eax]
  0x000ff161  movss    xmm0, dword ptr [eax + 8]
  0x000ff166  mulss    xmm2, xmm2
  0x000ff16a  mulss    xmm1, xmm1
  0x000ff16e  mulss    xmm0, xmm0
  0x000ff172  addss    xmm2, xmm1
  0x000ff176  addss    xmm2, xmm0
  0x000ff17a  xorps    xmm0, xmm0
  0x000ff17d  ucomiss  xmm2, xmm0
  0x000ff180  lahf     
  0x000ff181  test     ah, 0x44
  0x000ff184  jnp      0x100ff18d
  0x000ff186  xorps    xmm0, xmm0
  0x000ff189  sqrtss   xmm0, xmm2
  0x000ff18d  comiss   xmm0, dword ptr [ebp - 0x14]
  0x000ff191  jbe      0x100ff1fc
  0x000ff193  mov      ecx, dword ptr [ebx + 4]
  0x000ff196  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff19b  cmp      byte ptr [ebp - 0xe], 0
  0x000ff19f  mov      ecx, dword ptr [ebx + 4]
  0x000ff1a2  je       0x100ff1bb
  0x000ff1a4  mov      esi, dword ptr [eax + 8]
  0x000ff1a7  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff1ac  push     ecx
  0x000ff1ad  mov      dword ptr [esp], 0x3f800000
  0x000ff1b4  push     7
  0x000ff1b6  push     esi
  0x000ff1b7  push     dword ptr [eax]
  0x000ff1b9  jmp      0x100ff1e7   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x3a7
  0x000ff1bb  mov      edi, dword ptr [eax + 8]
  0x000ff1be  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff1c3  push     0
  0x000ff1c5  mov      ecx, ebx
  0x000ff1c7  mov      esi, dword ptr [eax]
  0x000ff1c9  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff1ce  mov      ecx, eax
  0x000ff1d0  call     0x10054750   ; -> ?GetRunSpeed@Character@GAME@@QAE?BM_N@Z
  0x000ff1d5  push     ecx
  0x000ff1d6  fstp     dword ptr [ebp - 0x14]
  0x000ff1d9  movss    xmm0, dword ptr [ebp - 0x14]
  0x000ff1de  movss    dword ptr [esp], xmm0
  0x000ff1e3  push     5
  0x000ff1e5  push     edi
  0x000ff1e6  push     esi
  0x000ff1e7  mov      ecx, dword ptr [ebx + 4]
  0x000ff1ea  lea      eax, [ebp - 0x28]
  0x000ff1ed  push     eax
  0x000ff1ee  call     0x100e6cd0   ; -> ?MoveTo@ControllerAI@GAME@@QAEXABVWorldVec3@2@IIW4AnimationSet_Type@2@M@Z
  0x000ff1f3  mov      byte ptr [ebx + 0x1c], 0
  0x000ff1f7  jmp      0x100ff2cf   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x48f
  0x000ff1fc  mov      ecx, ebx
  0x000ff1fe  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff203  mov      esi, dword ptr [ebp - 0x18]
  0x000ff206  mov      ecx, esi
  0x000ff208  mov      ebx, dword ptr [eax + 0x306c]
  0x000ff20e  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff213  mov      ecx, dword ptr [esi + 4]
  0x000ff216  movss    xmm0, dword ptr [eax + 0x3070]
  0x000ff21e  movss    dword ptr [ebp - 0x14], xmm0
  0x000ff223  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff228  mov      ecx, dword ptr [esi + 4]
  0x000ff22b  mov      edi, dword ptr [eax + 8]
  0x000ff22e  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff233  mov      ecx, dword ptr [ebp - 0x18]
  0x000ff236  push     0
  0x000ff238  mov      esi, dword ptr [eax]
  0x000ff23a  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff23f  mov      ecx, eax
  0x000ff241  call     0x10054750   ; -> ?GetRunSpeed@Character@GAME@@QAE?BM_N@Z
  0x000ff246  fmul     dword ptr [ebp - 0x14]
  0x000ff249  lea      eax, [ebp - 0x28]
  0x000ff24c  push     ecx
  0x000ff24d  fstp     dword ptr [ebp - 0x14]
  0x000ff250  movss    xmm0, dword ptr [ebp - 0x14]
  0x000ff255  movss    dword ptr [esp], xmm0
  0x000ff25a  push     ebx
  0x000ff25b  mov      ebx, dword ptr [ebp - 0x18]
  0x000ff25e  push     edi
  0x000ff25f  push     esi
  0x000ff260  push     eax
  0x000ff261  mov      ecx, dword ptr [ebx + 4]
  0x000ff264  call     0x100e6cd0   ; -> ?MoveTo@ControllerAI@GAME@@QAEXABVWorldVec3@2@IIW4AnimationSet_Type@2@M@Z
  0x000ff269  mov      byte ptr [ebx + 0x1c], 1
  0x000ff26d  jmp      0x100ff2cf   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x48f
  0x000ff26f  mov      ecx, dword ptr [ebx + 4]
  0x000ff272  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff277  cmp      byte ptr [ebp - 0xe], 0
  0x000ff27b  mov      ecx, dword ptr [ebx + 4]
  0x000ff27e  je       0x100ff297
  0x000ff280  mov      esi, dword ptr [eax + 8]
  0x000ff283  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff288  push     ecx
  0x000ff289  mov      dword ptr [esp], 0x3f800000
  0x000ff290  push     7
  0x000ff292  push     esi
  0x000ff293  push     dword ptr [eax]
  0x000ff295  jmp      0x100ff2c3   ; -> ?OnBegin@ControllerMonsterStatePursue@GAME@@MAEXXZ+0x483
  0x000ff297  mov      edi, dword ptr [eax + 8]
  0x000ff29a  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff29f  push     0
  0x000ff2a1  mov      ecx, ebx
  0x000ff2a3  mov      esi, dword ptr [eax]
  0x000ff2a5  call     0x100d17c0   ; -> ?GetCharacter@?$ControllerAIStateT@VControllerSpirit@GAME@@VMonster@2@@GAME@@IAEAAVMonster@2@XZ
  0x000ff2aa  mov      ecx, eax
  0x000ff2ac  call     0x10054750   ; -> ?GetRunSpeed@Character@GAME@@QAE?BM_N@Z
  0x000ff2b1  push     ecx
  0x000ff2b2  fstp     dword ptr [ebp - 0x14]
  0x000ff2b5  movss    xmm0, dword ptr [ebp - 0x14]
  0x000ff2ba  movss    dword ptr [esp], xmm0
  0x000ff2bf  push     5
  0x000ff2c1  push     edi
  0x000ff2c2  push     esi
  0x000ff2c3  mov      ecx, dword ptr [ebx + 4]
  0x000ff2c6  lea      eax, [ebp - 0x28]
  0x000ff2c9  push     eax
  0x000ff2ca  call     0x100e6cd0   ; -> ?MoveTo@ControllerAI@GAME@@QAEXABVWorldVec3@2@IIW4AnimationSet_Type@2@M@Z
  0x000ff2cf  mov      eax, dword ptr [ebx + 4]
  0x000ff2d2  movups   xmm0, xmmword ptr [ebp - 0x28]
  0x000ff2d6  pop      edi
  0x000ff2d7  pop      esi
  0x000ff2d8  mov      eax, dword ptr [eax + 0x2fc]
  0x000ff2de  mov      dword ptr [ebx + 0x10], eax
  0x000ff2e1  mov      dword ptr [ebx + 0x14], 0xc8
  0x000ff2e8  movups   xmmword ptr [ebx + 0x20], xmm0
  0x000ff2ec  pop      ebx
  0x000ff2ed  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff2f0  mov      dword ptr fs:[0], ecx
  0x000ff2f7  mov      esp, ebp
  0x000ff2f9  pop      ebp
  0x000ff2fa  ret      
  0x000ff2fb  mov      ecx, dword ptr [ebx + 4]
  0x000ff2fe  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff303  push     0x1052cde4
  0x000ff308  lea      ecx, [ebp - 0x80]
  0x000ff30b  call     0x1000c380   ; -> ??0CombatAttributeAccumulator@GAME@@QAE@ABV01@@Z+0x100
  0x000ff310  mov      dword ptr [ebp - 4], 3
  0x000ff317  mov      ecx, dword ptr [ebx + 4]
  0x000ff31a  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff31f  mov      ecx, dword ptr [ebx + 4]
  0x000ff322  mov      edi, dword ptr [eax + 8]
  0x000ff325  call     0x100e84e0   ; -> ?GetCurrentStateData@ControllerAI@GAME@@IBEABVControllerAIStateData@2@XZ
  0x000ff32a  lea      ecx, [ebp - 0x54]
  0x000ff32d  mov      esi, dword ptr [eax]
  0x000ff32f  call     dword ptr [0x104e5388]   ; f32=1.16495e-38 i32=8313394 f64=2.74599e-306
  0x000ff335  mov      ecx, dword ptr [ebx + 4]
  0x000ff338  mov      dword ptr [ebp - 0x44], esi
  0x000ff33b  mov      dword ptr [ebp - 0x40], 0
  0x000ff342  movups   xmm0, xmmword ptr [eax]
  0x000ff345  lea      eax, [ebp - 0x44]
  0x000ff348  mov      dword ptr [ebp - 0x3c], edi
  0x000ff34b  push     eax
  0x000ff34c  lea      eax, [ebp - 0x80]
  0x000ff34f  push     eax
  0x000ff350  movups   xmmword ptr [ebp - 0x38], xmm0
  0x000ff354  call     0x100e6780   ; -> ?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@ABVControllerAIStateData@2@@Z
  0x000ff359  lea      ecx, [ebp - 0x80]
  0x000ff35c  call     0x10008cc0   ; -> ??1AuraContainer@GAME@@QAE@XZ
  0x000ff361  pop      edi
  0x000ff362  pop      esi
  0x000ff363  mov      ecx, dword ptr [ebp - 0xc]
  0x000ff366  pop      ebx
  0x000ff367  mov      dword ptr fs:[0], ecx
  0x000ff36e  mov      esp, ebp
  0x000ff370  pop      ebp
  0x000ff371  ret      
  0x000ff372  int3     
  0x000ff373  int3     
  0x000ff374  int3     
  0x000ff375  int3     
  0x000ff376  int3     
