#!/usr/bin/env bash
# Install pre-commit and pre-push hooks that run scripts/check_no_private.sh. Hooks are local to each clone.
set -euo pipefail
root="$(git rev-parse --show-toplevel)"; hooks="$root/.git/hooks"
cat > "$hooks/pre-commit" <<'H'
#!/usr/bin/env bash
exec "$(git rev-parse --show-toplevel)/scripts/check_no_private.sh" --staged
H
cat > "$hooks/pre-push" <<'H'
#!/usr/bin/env bash
z=0000000000000000000000000000000000000000
empty_tree=$(git hash-object -t tree /dev/null)
while read -r lref lsha rref rsha; do
  [ "$lsha" = "$z" ] && continue
  commit=$(git rev-parse "$lsha^{commit}" 2>/dev/null) || { echo "pre-push: cannot resolve $lref"; exit 1; }
  # A tag is skipped only if its commit is already on a remote-tracking branch (so it was checked when that
  # branch was pushed). A tag on any other commit is checked like a branch push.
  case "$lref" in refs/tags/*)
    if git branch -r --contains "$commit" 2>/dev/null | grep -q .; then continue; fi;;
  esac
  if [ "$rsha" = "$z" ]; then base=$(git merge-base "$commit" origin/main 2>/dev/null || echo "$empty_tree"); else base="$rsha"; fi
  "$(git rev-parse --show-toplevel)/scripts/check_no_private.sh" --range "$base..$commit" || exit 1
done
H
chmod +x "$hooks/pre-commit" "$hooks/pre-push"
echo "Installed pre-commit and pre-push hooks."
