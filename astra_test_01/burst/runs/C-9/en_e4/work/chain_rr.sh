#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
python3 scripts/j_runtime_resample.py export/coilseer/coilseer.glb --clips idle,walk,run,attack_claw,cast_bolt,cast_nova,attack_taillash,hit,death --out work/runtime_resample_en-coilseer.json --index ../join1_pack/en-coilseer/matrix_index.json 2>&1 | grep -i "worst\|error\|trace" | tail -12
python3 scripts/j_runtime_resample.py export/gloamwing/gloamwing.glb --clips idle,walk,run,attack_claw,attack_peck,cast_breath,cast_roar,emerge,hit,death --out work/runtime_resample_en-gloamwing.json --index ../join1_pack/en-gloamwing/matrix_index.json 2>&1 | grep -i "worst\|error\|trace" | tail -12
echo RR_DONE
