#!/usr/bin/env bash
# Refuse to commit or push private material. Run by the git hooks that scripts/install_hooks.sh installs.
#   - blocks private/third-party paths (PRIVATE_*, OUTREACH_PLAN*, data folders, publisher full text)
#   - blocks content matching patterns listed in .private_patterns (one extended regex per line; that file is
#     gitignored and local-only, so the patterns themselves are never published)
# Usage: check_no_private.sh [--staged | --range <rev-range>]   (default --staged)
set -uo pipefail
root="$(git rev-parse --show-toplevel)"; cd "$root"
mode="${1:---staged}"
if [ "$mode" = "--range" ]; then
  files=$(git diff --name-only --diff-filter=ACMR "$2")
  show() { git show "${2##*..}:$1" 2>/dev/null; }
else
  files=$(git diff --cached --name-only --diff-filter=ACMR)
  show() { git show ":$1" 2>/dev/null; }
fi
bad=0
path_re='(^|/)(PRIVATE_[^/]*|OUTREACH_PLAN[^/]*)$|(^|/)data/|^dataset_search/paper_[^/]*\.xml$|^\.private_patterns$'
for f in $files; do
  if [[ "$f" =~ $path_re ]]; then echo "BLOCKED path: $f"; bad=1; fi
done
if [ -f .private_patterns ]; then
  while IFS= read -r pat; do
    [[ -z "$pat" || "$pat" == \#* ]] && continue
    for f in $files; do
      if show "$f" | grep -q -i -E -- "$pat"; then echo "BLOCKED content in $f (matches a .private_patterns entry)"; bad=1; fi
    done
  done < .private_patterns
else
  echo "warning: .private_patterns not found; only path rules applied" >&2
fi
[ $bad -eq 0 ] || { echo "Private-content check failed. Nothing was committed/pushed."; exit 1; }
