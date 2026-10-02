#!/bin/bash
# bm_mx stage 2: Mixamo FBX (Matt's packs, reincarnated-godot/animations/mixamo, R-C9-131) -> renamed GLBs via e40a, one heavy-lock batch.
# Output names: pack prefix (ss_ / ax_) + the file name lower-cased, spaces/parentheses/dots -> '_'. Raw FBX never copied.
cd "$(dirname "$0")/.."
while IFS= read -r f; do
  b=$(basename "$f" .fbx); case "$f" in *"Sword and Shield"*) p=ss;; *Axe*) p=ax;; esac
  n=${p}_$(echo "$b" | tr 'A-Z' 'a-z' | sed -E 's/[ ().]+/_/g; s/_+$//')
  [ -f mixamo2/glb/$n.glb ] && continue
  blender -b -noaudio --python scripts/e40a_mixamo_fbx.py -- "$f" mixamo2/glb/$n.glb --json mixamo2/glb/$n.json 2>&1 | grep -q '^MIXAMO' && echo "OK $n" || echo "FAIL $n"
done < work/s2_fbx_list.txt
