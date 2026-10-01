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
while read -r lref lsha rref rsha; do
  [ "$lsha" = "$z" ] && continue
  if [ "$rsha" = "$z" ]; then range="$(git rev-list --max-parents=0 "$lsha" | tail -1)..$lsha"; else range="$rsha..$lsha"; fi
  "$(git rev-parse --show-toplevel)/scripts/check_no_private.sh" --range "$range" || exit 1
done
H
chmod +x "$hooks/pre-commit" "$hooks/pre-push"
echo "Installed pre-commit and pre-push hooks."
