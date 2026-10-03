#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
gate() { f=$(df -k /System/Volumes/Data | tail -1 | awk '{print int($4/1048576)}'); echo "df_gib $f"; [ $f -ge 21 ]; }
gate || { echo "HALT disk"; exit 3; }
python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh work/chain_final_cs.sh > work/chain_final_cs.log 2>&1
echo "cs done"; du -sk . ../join1_pack/en-coilseer
gate || { echo "HALT disk"; exit 3; }
python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh work/chain_final_gw.sh > work/chain_final_gw.log 2>&1
echo "gw done"; du -sk . ../join1_pack/en-gloamwing; gate
