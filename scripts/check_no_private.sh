#!/usr/bin/env bash
# Refuse to commit or push private material. Run by the git hooks that scripts/install_hooks.sh installs.
#   - blocks private/third-party paths (PRIVATE_*, OUTREACH_PLAN*, data folders, publisher full text)
#   - blocks content matching patterns listed in .private_patterns (one extended regex per line; that file is
#     gitignored and local-only, so the patterns themselves are never published), in file contents AND in
#     commit messages
# Usage:
#   check_no_private.sh [--staged]        the files staged for commit (default)
#   check_no_private.sh --commit <rev>    what that one commit adds or changes, plus its message
#   check_no_private.sh --range <a..b>    EVERY commit in the range, one by one. A net diff would hide something
#                                         added in one commit and removed in the next, although both are published.
set -uo pipefail
root="$(git rev-parse --show-toplevel)"; cd "$root"
mode="${1:---staged}"
path_re='(^|/)(PRIVATE_[^/]*|OUTREACH_PLAN[^/]*)$|(^|/)data/|^dataset_search/paper_[^/]*\.xml$|^\.private_patterns$'
empty_tree=$(git hash-object -t tree /dev/null)
pats=()
if [ -f .private_patterns ]; then
  while IFS= read -r pat; do [[ -z "$pat" || "$pat" == \#* ]] && continue; pats+=("$pat"); done < .private_patterns
else
  echo "warning: .private_patterns not found; only path rules applied" >&2
fi
bad=0

scan() {   # $1 label, $2 rev ("" = the index), $3 newline-separated file list, $4 commit message (may be empty)
  local label="$1" rev="$2" files="$3" msg="$4" f pat content
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [[ "$f" =~ $path_re ]]; then echo "BLOCKED path in $label: $f"; bad=1; fi
  done <<< "$files"
  for pat in "${pats[@]:-}"; do
    [ -z "$pat" ] && continue
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if [ -n "$rev" ]; then content=$(git show "$rev:$f" 2>/dev/null); else content=$(git show ":$f" 2>/dev/null); fi
      if printf '%s' "$content" | grep -q -i -E -- "$pat"; then echo "BLOCKED content in $label: $f (matches a .private_patterns entry)"; bad=1; fi
    done <<< "$files"
    if [ -n "$msg" ] && printf '%s' "$msg" | grep -q -i -E -- "$pat"; then echo "BLOCKED message of $label (matches a .private_patterns entry)"; bad=1; fi
  done
}

check_commit() {   # first parent only for merges; a root commit is compared with the empty tree
  local c="$1" parent files msg
  parent=$(git rev-parse -q --verify "$c^" 2>/dev/null || echo "$empty_tree")
  files=$(git diff --name-only --diff-filter=ACMR "$parent" "$c")
  msg=$(git log -1 --format=%B "$c")
  scan "commit ${c:0:7}" "$c" "$files" "$msg"
}

case "$mode" in
  --staged) scan "staged files" "" "$(git diff --cached --name-only --diff-filter=ACMR)" "" ;;
  --commit) check_commit "$(git rev-parse "${2:?--commit needs a revision}^{commit}")" ;;
  --range)  for c in $(git rev-list --reverse "${2:?--range needs a rev range, for example base..tip}"); do check_commit "$c"; done ;;
  *) echo "usage: check_no_private.sh [--staged | --commit <rev> | --range <a..b>]" >&2; exit 2 ;;
esac
[ $bad -eq 0 ] || { echo "Private-content check failed. Nothing was committed/pushed."; exit 1; }
