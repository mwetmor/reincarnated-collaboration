#!/bin/zsh
# One verify entry point for the burst lane (adoption 3, R-C7-15): verify.sh {suite|freeze|sync|fence|reds|all}
# Wraps what exists — no new behaviour. Heavy work runs under the shared advisory lock (8 GB host, C-6 concurrency law).
set -e
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-7/conductor_scripts; L=$HOME/astra-burst/logs/C-7; mkdir -p $L
cd $B
case "${1:-all}" in
  suite)  python3 $C/heavy_lock.py C-7 -- python3 -B tests/run_t0c.py | tail -1 || true
          echo "--- reds (tests/t0c_suite_output.txt) ---"; grep -E "^(FAIL|ERROR): " tests/t0c_suite_output.txt | sed -E 's/^(FAIL|ERROR): //' | cut -c1-140 | sort; tail -3 tests/t0c_suite_output.txt ;;
  reds)   grep -E "^(FAIL|ERROR): " tests/t0c_suite_output.txt | sed -E 's/^(FAIL|ERROR): //' | cut -c1-140 | sort; tail -3 tests/t0c_suite_output.txt ;;
  fence)  python3 $C/heavy_lock.py C-7 -- python3 -B -m unittest tests.test_godot_import.BL2VBConfigResourceTests -v 2>&1 | tail -6 ;;
  sync)   python3 lane/check_sync.py | grep -c "OK " | sed 's/$/ \/ 10 OK/' ;;
  freeze) zsh $C/freeze.sh; python3 $C/restamp.py | tail -3
          echo "REMINDER: append the row to runs/FREEZE_NOTICES.md and ledger the freeze (cl.py rulings), then commit --only the named paths" ;;
  all)    zsh $0 suite; zsh $0 fence; zsh $0 sync ;;
  *) echo "usage: verify.sh {suite|freeze|sync|fence|reds|all}"; exit 2 ;;
esac
