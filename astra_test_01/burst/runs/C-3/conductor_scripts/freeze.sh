#!/bin/zsh
# C-3 freeze (C-2 domain R-28/R-30 + export/ per SPEC § 7 T3f): prints rows, sha[:12], path delta, verify.
set -e
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
P=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad/MANIFEST.prev
cp MANIFEST.sha256 $P
DIRS=(lane gates oracle oracles parts compare transcribe review bible fixtures tests); [ -d export ] && DIRS+=(export)
{
  find $DIRS -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -path 'tests/tmp/*' \
     ! -name 't0c_suite_output.txt' ! -name 't0c_summary.json' ! -name '.DS_Store' -print
  ls BURST_RULES.md JUDGE_RUBRIC.md REGISTER_CARD.md SPEC.md receipt.schema.json transcribe.schema.json
} | LC_ALL=C sort | xargs shasum -a 256 > MANIFEST.sha256.new
mv MANIFEST.sha256.new MANIFEST.sha256
echo "rows: $(wc -l < MANIFEST.sha256)  sha256[:12]: $(shasum -a 256 MANIFEST.sha256 | cut -c1-12)"
echo "--- path delta ---"; diff <(awk '{print $2}' $P | LC_ALL=C sort) <(awk '{print $2}' MANIFEST.sha256 | LC_ALL=C sort) || true
echo "--- changed hashes ---"; diff <(sort -k2 $P) <(sort -k2 MANIFEST.sha256) | grep '^>' | awk '{print $3}' | head -40 || true
shasum -c MANIFEST.sha256 | grep -v ': OK$' || echo "verify: all OK"
