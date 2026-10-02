#!/bin/bash
H=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad/hunt2
cd $H/eng/src
for a in "$@"; do
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$H/eng/src:$H/tools python3 $H/tools/hunt2.py $a 20 $H/out/$a.json > $H/out/$a.log 2>&1
done
