=== 94-Monster-CrowdAgentMoved RVA 0x002d5770 sym=?CrowdAgentMoved@Monster@GAME@@UAEXHABUCrowdAgentData@CROWD@@@Z ===
  0x002d5770  push     ebp
  0x002d5771  mov      ebp, esp
  0x002d5773  push     edi
  0x002d5774  push     dword ptr [ebp + 0xc]
  0x002d5777  mov      edi, ecx
  0x002d5779  push     dword ptr [ebp + 8]
  0x002d577c  call     0x10052960   ; -> ?CrowdAgentMoved@Character@GAME@@UAEXHABUCrowdAgentData@CROWD@@@Z
  0x002d5781  cmp      dword ptr [ebp + 8], 0
  0x002d5785  jle      0x102d5790
  0x002d5787  mov      word ptr [edi + 0x3a97], 1
  0x002d5790  pop      edi
  0x002d5791  pop      ebp
  0x002d5792  ret      8
  0x002d5795  int3     
  0x002d5796  int3     
  0x002d5797  int3     
  0x002d5798  int3     
  0x002d5799  int3     
  0x002d579a  int3     
  0x002d579b  int3     
  0x002d579c  int3     
  0x002d579d  int3     
  0x002d579e  int3     
  0x002d579f  int3     
