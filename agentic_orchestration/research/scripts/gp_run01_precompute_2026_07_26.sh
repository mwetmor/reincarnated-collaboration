#!/bin/bash
# GP run 01 precompute — the expensive part of the M6 ingest, isolated so a rebuild
# does not have to repeat it.
#
# Reads 13.2 GB over SMB at ~3.5 MB/s. Budget ~70 minutes.
# Outputs are COMMITTED under research/curated/gp-run01-manifest/ and are the durable
# record; fixtures_m6_gp_run01_ingest_2026_07_26.py reads them, not the share.
#
# Requires: /Volumes/reincarnated mounted (//mwetmor@reincarnated-pi.local/reincarnated).
set -eu

SRC="/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1"
OUT="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/gp-run01-manifest"
mkdir -p "$OUT"
cd "$SRC"

# numeric sort on the "Screenshot (NN).png" ordinal, NUL-delimited (paths contain spaces)
SORTED=$(mktemp)
ls screenshots/*.png | sort -t'(' -k2 -n > "$SORTED"

# 1. sha256 of every still (~1.2 GB)
tr '\n' '\0' < "$SORTED" | xargs -0 shasum -a 256 > "$OUT/sha256-png.txt"

# 2. sha256 of both videos (~13.2 GB — this is the long pole)
shasum -a 256 recorded_videos/play_test_2026-07-26.mp4 \
              recorded_videos/smoke_test_2026-07-26.mp4 > "$OUT/sha256-mp4.txt"

# 3. mtime (fractional epoch) + size. mtime is CAPTURE time here, not transfer time:
#    it aligns to the video timeline at four independent points. Birthtime (%FB) is the
#    share-copy time and is deliberately NOT used.
tr '\n' '\0' < "$SORTED" | xargs -0 stat -f "%N|%Fm|%z" > "$OUT/stat-png.txt"
stat -f "%N|%Fm|%z" recorded_videos/*.mp4 >> "$OUT/stat-png.txt"

# 4. pixel dimensions straight from the PNG IHDR (33-byte read, not a decode)
python3 - <<'EOF' > "$OUT/dim-png.txt"
import glob, re, struct
for f in sorted(glob.glob('screenshots/*.png'),
                key=lambda p: int(re.search(r'\((\d+)\)', p).group(1))):
    with open(f, 'rb') as fh:
        h = fh.read(33)
    w, ht = struct.unpack('>II', h[16:24])
    print("%s|%d|%d" % (f.split('/')[-1], w, ht))
EOF

rm -f "$SORTED"
echo "precompute complete:"
wc -l "$OUT"/*.txt
