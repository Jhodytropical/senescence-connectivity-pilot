#!/usr/bin/env bash
# Check downloaded inputs against the checksums of the files the pilot actually used (fetched 2026-09-28/2026-10-01).
# A mismatch means your inputs differ from the pilot's. Upstream libraries (Enrichr, MSigDB, HAGR) are updated over
# time, so a fresh download may legitimately differ; results computed on different inputs are not a reproduction.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
status=0
(cd "$root/senolytic_repurposing/data" && shasum -a 256 -c "$root/scripts/INPUT_SHA256SUMS") || status=1
if [ -d "$root/test_a_prep/data" ]; then
  (cd "$root/test_a_prep/data" && shasum -a 256 -c "$root/scripts/TESTA_INPUT_SHA256SUMS") || status=1
fi
[ $status -eq 0 ] && echo "All inputs match the pilot's checksums." || echo "Some inputs differ from the pilot's (see above)."
exit $status
