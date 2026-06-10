#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ -z "${ANTCHAT_API_KEY:-}" ]]; then
  echo "ANTCHAT_API_KEY is not set. You can either export it or rely on IJBR_API_KEY_FILE." >&2
  echo "Recommended: export ANTCHAT_API_KEY=\"YOUR_REAL_KEY\"" >&2
fi

python3 OMG.py \
  --input data/harmful_behaviors_custom.xlsx \
  --output data/reproduction/offense.real.json \
  --overwrite \
  --limit 1 \
  --max-defenses 1 \
  --model deepseek-v4-flash \
  --request-sleep 70

python3 jailbreak.py \
  --input data/reproduction/offense.real.json \
  --output data/reproduction/jailbreak.real.json \
  --overwrite \
  --limit 1 \
  --model deepseek-v4-flash \
  --request-sleep 70

echo "Done:"
echo "  data/reproduction/offense.real.json"
echo "  data/reproduction/jailbreak.real.json"
