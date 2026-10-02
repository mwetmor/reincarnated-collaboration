#!/bin/bash
H="${H:?set H to a scratch dir holding rerun114/ rerun115/ copies of the committed instruments}"
T=$H/rerun114/oracle_trace_v3p11.py; R=$H/rerun114/raw
run() { "$@" >> $H/runall.log 2>&1; echo "rc=$? :: $*" >> $H/runall.rc; }
n=0
for a in M0 M-POL-2 M-POL-2-NULL W1 W1-NULL; do
  for cmd in "hooked $a $R/hooked_$a.json" "bare $a $R/bare_$a.json" "single $a 0 $R/single_${a}_s0.json" "single $a 1 $R/single_${a}_s1.json" "single $a 2 $R/single_${a}_s2.json" "single $a 3 $R/single_${a}_s3.json" "single $a 4 $R/single_${a}_s4.json"; do
    run python3 $T $cmd &
    n=$((n+1)); if (( n % 6 == 0 )); then wait; fi
  done
  run python3 $H/rerun115/audit_v1p15.py $a $H/rerun115/raw/audit_$a.json &
  n=$((n+1)); if (( n % 6 == 0 )); then wait; fi
done
run python3 $T single M0 2 $R/repeat_M0_s2.json &
wait
echo ALLDONE >> $H/runall.rc
