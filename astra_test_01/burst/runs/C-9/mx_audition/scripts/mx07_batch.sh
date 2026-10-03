#!/bin/zsh
# MX audition (R-C9-149): several SHORT Godot renders under ONE heavy-lock acquisition (each render is ~5-40 s; the lock wait was
# ~9 min per acquisition with barrow_v2 + KC2 contending, so one acquisition per batch is the lighter footprint).
#   python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh scripts/mx07_batch.sh "<mode> <tag> <cfg> [out]" ...
cd "$(dirname "$0")/.."; export MX_NOLOCK=1
F=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); [ $F -lt 21 ] && { echo "DISK HALT: $F GiB < 21"; exit 3; }
for job in "$@"; do set -- ${=job}; t0=$(date +%s)
  case $2 in revenant_em) export GLB_TAG=revenant;; golem_em) export GLB_TAG=golem;; *) unset GLB_TAG;; esac
  bash scripts/mx04_godot.sh $1 $2 $3 $4 | grep -E "film|ERROR|SCRIPT" | cut -c1-140; echo "job $job: $(( $(date +%s) - t0 )) s"
done
