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
remote="${1:-origin}"
z=0000000000000000000000000000000000000000
while read -r lref lsha rref rsha; do
  [ "$lsha" = "$z" ] && continue
  commit=$(git rev-parse "$lsha^{commit}" 2>/dev/null) || { echo "pre-push: cannot resolve $lref"; exit 1; }
  # Every commit that is new on THIS remote is checked one by one. Commits already on this remote's tracking
  # branches expose nothing new, which also covers a tag on a published commit. If there are no tracking refs
  # for this remote (for example a push to a bare URL), all history is checked, so the hook fails closed.
  for c in $(git rev-list --reverse "$commit" --not --remotes="$remote"); do
    "$(git rev-parse --show-toplevel)/scripts/check_no_private.sh" --commit "$c" || exit 1
  done
done
H
chmod +x "$hooks/pre-commit" "$hooks/pre-push"
echo "Installed pre-commit and pre-push hooks."
