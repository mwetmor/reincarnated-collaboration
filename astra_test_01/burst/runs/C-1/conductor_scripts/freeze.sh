#!/bin/zsh
# C-2 freeze (R-28 + R-30): domain = source + data; oracle/ added; volatile test outputs, pycache, tests/tmp excluded.
set -e
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
cp MANIFEST.sha256 /tmp/MANIFEST.prev.$$ 
{
  find lane gates oracle oracles parts compare transcribe review bible fixtures tests -type f \
     ! -path '*/__pycache__/*' ! -name '*.pyc' ! -path 'tests/tmp/*' \
     ! -name 't0c_suite_output.txt' ! -name 't0c_summary.json' ! -name '.DS_Store' -print
  ls BURST_RULES.md JUDGE_RUBRIC.md REGISTER_CARD.md SPEC.md receipt.schema.json transcribe.schema.json
} | LC_ALL=C sort | xargs shasum -a 256 > MANIFEST.sha256.new
mv MANIFEST.sha256.new MANIFEST.sha256
echo "rows: $(wc -l < MANIFEST.sha256)  sha256[:12]: $(shasum -a 256 MANIFEST.sha256 | cut -c1-12)"
echo "--- path delta vs previous manifest ---"
diff <(awk '{print $2}' /tmp/MANIFEST.prev.$$ | LC_ALL=C sort) <(awk '{print $2}' MANIFEST.sha256 | LC_ALL=C sort) || true
shasum -c MANIFEST.sha256 | grep -v ': OK$' || echo "verify: all OK"
