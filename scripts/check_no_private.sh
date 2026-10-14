#!/usr/bin/env bash
# Refuse to commit or push private material. Run by the git hooks that scripts/install_hooks.sh installs.
#   - blocks private/third-party paths (PRIVATE_*, OUTREACH_PLAN*, data folders, publisher full text)
#   - blocks content matching patterns listed in .private_patterns (one extended regex per line; that file is
#     gitignored and local-only, so the patterns themselves are never published), in file contents, in commit
#     messages, and in the message and tagger lines of annotated tags
# Usage:
#   check_no_private.sh [--staged]        the files staged for commit (default)
#   check_no_private.sh --commit <rev>    what that one commit adds or changes, plus its message
#   check_no_private.sh --range <a..b>    EVERY commit in the range, one by one. A net diff would hide something
#                                         added in one commit and removed in the next, although both are published.
#   check_no_private.sh --tag <rev>       the message and tagger lines of an annotated tag (and any tag it points at)
# Exit status: 0 = clean, 1 = private material found, 2 = the check itself could not run (git error, invalid
# pattern, bad argument). A tooling error is never treated as a pass.
set -uo pipefail
die() { echo "check_no_private: $*" >&2; exit 2; }
root="$(git rev-parse --show-toplevel)" || die "not inside a git repository"
cd "$root" || die "cannot enter $root"
mode="${1:---staged}"
path_re='(^|/)(PRIVATE_[^/]*|OUTREACH_PLAN[^/]*)$|(^|/)data/|^dataset_search/paper_[^/]*\.xml$|^\.private_patterns$'
empty_tree=$(git hash-object -t tree /dev/null) || die "cannot compute the empty tree"
patfile="${PRIVATE_PATTERNS_FILE:-.private_patterns}"
pats=()
if [ -f "$patfile" ]; then
  n=0
  while IFS= read -r pat; do
    n=$((n+1)); [[ -z "$pat" || "$pat" == \#* ]] && continue
    printf '' | grep -q -i -E -- "$pat"; rc=$?
    [ "$rc" -ge 2 ] && die "invalid regular expression at line $n of $patfile"
    pats+=("$pat")
  done < "$patfile"
else
  echo "warning: $patfile not found; only path rules applied" >&2
fi
bad=0

has_match() {   # $1 pattern, $2 text; returns 0 on a match, 1 on none, and aborts the whole check on a grep error
  local rc
  printf '%s' "$2" | grep -q -i -E -- "$1"; rc=${PIPESTATUS[1]}
  [ "$rc" -ge 2 ] && die "grep failed (exit $rc) while scanning"
  [ "$rc" -eq 0 ]
}

scan() {   # $1 label, $2 rev ("" = the index), $3 newline-separated file list, $4 message text (may be empty)
  local label="$1" rev="$2" files="$3" msg="$4" f pat content
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [[ "$f" =~ $path_re ]]; then echo "BLOCKED path in $label: $f"; bad=1; fi
  done <<< "$files"
  for pat in "${pats[@]:-}"; do
    [ -z "$pat" ] && continue
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if [ -n "$rev" ]; then content=$(git show "$rev:$f") || die "cannot read $f at $rev"
      else content=$(git show ":$f") || die "cannot read staged $f"; fi
      if has_match "$pat" "$content"; then echo "BLOCKED content in $label: $f (matches a .private_patterns entry)"; bad=1; fi
    done <<< "$files"
    if [ -n "$msg" ] && has_match "$pat" "$msg"; then echo "BLOCKED message of $label (matches a .private_patterns entry)"; bad=1; fi
  done
}

check_commit() {   # first parent only for merges; a root commit is compared with the empty tree
  local c="$1" parents parent files msg
  parents=$(git rev-list --parents -n 1 "$c") || die "cannot read commit $c"
  parent=$(printf '%s\n' "$parents" | awk '{print $2}')
  [ -z "$parent" ] && parent="$empty_tree"
  files=$(git diff --name-only --diff-filter=ACMR "$parent" "$c") || die "git diff failed for $c"
  msg=$(git log -1 --format=%B "$c") || die "git log failed for $c"
  scan "commit ${c:0:7}" "$c" "$files" "$msg"
}

check_tag() {   # the tag's own text (headers, tagger, message), following tags that point at tags
  local obj="$1" type text
  type=$(git cat-file -t "$obj") || die "cannot read object $obj"
  while [ "$type" = "tag" ]; do
    text=$(git cat-file tag "$obj") || die "cannot read tag $obj"
    scan "tag ${obj:0:7}" "" "" "$text"
    obj=$(printf '%s\n' "$text" | sed -n 's/^object //p' | head -1)
    [ -n "$obj" ] || die "tag object without a target"
    type=$(git cat-file -t "$obj") || die "cannot read object $obj"
  done
}

case "$mode" in
  --staged)
    files=$(git diff --cached --name-only --diff-filter=ACMR) || die "git diff --cached failed"
    scan "staged files" "" "$files" "" ;;
  --commit)
    [ -n "${2:-}" ] || die "--commit needs a revision"
    c=$(git rev-parse --verify "$2^{commit}") || die "unknown revision: $2"
    check_commit "$c" ;;
  --range)
    [ -n "${2:-}" ] || die "--range needs a rev range, for example base..tip"
    list=$(git rev-list --reverse "$2") || die "invalid range: $2"
    for c in $list; do check_commit "$c"; done ;;
  --tag)
    [ -n "${2:-}" ] || die "--tag needs a revision"
    obj=$(git rev-parse --verify "$2") || die "unknown revision: $2"
    check_tag "$obj" ;;
  *) die "usage: check_no_private.sh [--staged | --commit <rev> | --range <a..b> | --tag <rev>]" ;;
esac
[ $bad -eq 0 ] || { echo "Private-content check failed. Nothing was committed/pushed."; exit 1; }
