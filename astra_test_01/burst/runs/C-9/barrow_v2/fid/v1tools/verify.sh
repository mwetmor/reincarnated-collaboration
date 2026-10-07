#!/bin/bash
# BV2F frozen v1 toolchain check (lane PT, 0.3; R-C9-163 B-1). Every BV2F lane script calls this FIRST.
#   bash barrow_v2/fid/v1tools/verify.sh
# Exit 0 = all checks pass. Exit 1 = any failure (charter § 6: frozen-tool sha mismatch -> HALT the lane).
#  1. every shipped file matches its SHA256SUMS shipped sha; no unlisted file in tierA/ tierB/
#  2. the v1 column is re-read from git at the pinned commit (git show <pin>:<path>), never from the copies
#  3. Tier A: shipped sha == v1 sha (byte-identical)
#  4. Tier B: patch(v1 @ pin, patches/<file>.diff) reproduces the shipped file byte for byte
#  5. Tier B: every v1 line a patch removes is listed in ALLOWLIST.md's `allow <file>` block
#  6. the driver's command lines call only fid/v1tools/ copies: no $C/, no conductor_scripts/ or
#     barrow_full/tools/ path outside v1tools, every python3/zsh/bash call goes through $A or $V
V="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$V" rev-parse --show-toplevel)"
C9REL="astra_test_01/burst/runs/C-9"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/v1verify.XXXXXX")"
fail=0; n=0
bad() { echo "[v1tools] FAIL: $*"; fail=1; }

# 1-4
while read -r shipped v1 pin path; do
  case "$shipped" in \#*|"") continue;; esac
  n=$((n+1)); f="$V/${path#./}"
  [ -f "$f" ] || { bad "missing $path"; continue; }
  s=$(shasum -a 256 "$f" | cut -d' ' -f1)
  [ "$s" = "$shipped" ] || bad "shipped sha $path: ${s:0:12} != ${shipped:0:12}"
  [ "$v1" = "-" ] && continue
  rel="${path#./tier?/}"
  git -C "$REPO" show "$pin:$C9REL/$rel" > "$TMP/v1" 2>/dev/null || { bad "cannot read $pin:$C9REL/$rel from git"; continue; }
  g=$(shasum -a 256 "$TMP/v1" | cut -d' ' -f1)
  [ "$g" = "$v1" ] || bad "v1 sha $rel @ $pin: git ${g:0:12} != recorded ${v1:0:12}"
  case "$path" in
    ./tierA/*) [ "$shipped" = "$v1" ] || bad "Tier A not byte-identical: $path" ;;
    ./tierB/*)
      d="$V/patches/$(basename "$rel").diff"
      [ -f "$d" ] || { bad "no patch for $path"; continue; }
      patch -s -o "$TMP/patched" "$TMP/v1" < "$d" > /dev/null 2>&1 || { bad "patch does not apply: $d"; continue; }
      cmp -s "$TMP/patched" "$f" || bad "patch(v1) != shipped: $path"
      awk -v F="$(basename "$rel")" '
        FNR==NR { if ($0 ~ "^```allow "F"$") {on=1; next} if (on && $0 ~ /^```/) {on=0} if (on) A[$0]=1; next }
        /^---/ { next } /^-/ { l=substr($0,2); if (!(l in A)) { print "unlisted removed line: " l; bad=1 } }
        END { exit bad }' "$V/ALLOWLIST.md" "$d" || bad "patch $d removes a v1 line not in ALLOWLIST.md"
      # W-1 (Gate-2): every non-blank ADDED line carries BV2F or sits inside a BV2F-BEGIN ... BV2F-END block
      awk '/^\+\+\+/ { next } /^\+/ { l=substr($0,2); if (l ~ /BV2F-BEGIN/) blk=1; if (l !~ /^[[:space:]]*$/ && !(l ~ /BV2F/) && !blk) { print "unmarked added line: " l; bad=1 } if (l ~ /BV2F-END/) blk=0 }
        END { exit bad }' "$d" || bad "patch $d adds a line without a BV2F marker (W-1)"
      ;;
  esac
done < "$V/SHA256SUMS"
listed=$(awk '!/^#/ && NF {print $4}' "$V/SHA256SUMS" | grep -E '^\./tier[AB]/' | sort)
present=$(cd "$V" && find ./tierA ./tierB -type f | sort)
[ "$listed" = "$present" ] || { bad "files in tierA/tierB != files listed"; diff <(echo "$listed") <(echo "$present"); }

# 6
DRV="$V/tierB/conductor_scripts/t10bf_drive.sh"
code=$(grep -v '^[[:space:]]*#' "$DRV" | sed 's/[[:space:]]#.*$//')
code_nov=$(echo "$code" | sed -E 's#\$(V|A)/[^[:space:]]*#<v1tools>#g')   # frozen-copy paths are allowed; look for originals in the rest
echo "$code" | grep -nE '\$C/|\$\{C\}/' && bad "driver references \$C/ (v1 conductor_scripts)"
echo "$code_nov" | grep -nE '(runs/C-9/conductor_scripts|conductor_scripts/[a-z_]+\.(py|sh)|barrow_full/(godot/)?tools/)' && bad "driver names a v1-original tool path"
calls=$(echo "$code" | grep -oE '(python3|zsh|bash)[[:space:]]+[^[:space:]-][^[:space:]]*' | grep -E '/' )
while read -r c; do
  [ -z "$c" ] && continue
  echo "$c" | grep -qE '^(python3|zsh|bash)[[:space:]]+\$(A|V)/' || bad "driver call outside v1tools: $c"
done <<< "$calls"

# W-2(b): lane/run_burst.py is shared lane infrastructure (not a v1 tool): its sha at the pin is recorded in
# PROVENANCE; a drift is a WARNING (not a failure) so another seam's edit cannot halt BV2F silently -- or loudly.
RB="$REPO/astra_test_01/burst/lane/run_burst.py"; RBPIN=$(awk '/^run_burst_pin_sha256/ {print $2}' "$V/PROVENANCE.md")
rb=$(shasum -a 256 "$RB" | cut -d' ' -f1)
[ -n "$RBPIN" ] && [ "$rb" != "$RBPIN" ] && echo "[v1tools] WARN: lane/run_burst.py ${rb:0:12} != pin ${RBPIN:0:12} (shared infra changed since the freeze)"

rm -f "$TMP/v1" "$TMP/patched"; rmdir "$TMP" 2>/dev/null
[ $fail -eq 0 ] && echo "[v1tools] OK: $n files; Tier A byte-identical to v1 @ $(cat "$V/PIN_COMMIT"); Tier B = v1 + allowlisted patches; driver calls only v1tools"
exit $fail
