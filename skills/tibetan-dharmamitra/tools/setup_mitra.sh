#!/usr/bin/env bash
# Set up MITRA (Dharmamitra's translation model) locally on Apple Silicon and serve it on
# 127.0.0.1:8080 as an OpenAI-compatible endpoint.
#
# NOTHING HERE HAS BEEN RUN FOR YOU. It downloads ~18-37 GB and writes ~5 GB. Read it, then run it.
#
#   bash ~/.claude/skills/tibetan-mitra/tools/setup_mitra.sh
#
# MODEL, verified 2026-09-02:
#   buddhist-nlp/mitra-qwen35-translate -- Qwen3.5-9B, Apache 2.0, translation-tuned.
#   Sources: Classical Tibetan, Sanskrit, Pali, Classical/Buddhist Chinese.
#   Targets: English, German, Japanese, Modern Chinese, Korean, and others.
#   This is the current model. The earlier Gemma-2 line (gemma-2-mitra-it) is superseded;
#   Dharmamitra moved to Qwen because it is properly open and does not route data to Google.
#   Requires transformers >= 5.13 and enable_thinking=False on the chat template.
#
# On an M4 with 16 GB: 4-bit (~5 GB) is comfortable, 8-bit (~9.5 GB) fits with less headroom.
set -euo pipefail

MODEL_ID="${MODEL_ID:-buddhist-nlp/mitra-qwen35-translate}"
OUT="${HOME}/models/mitra-qwen35-4bit"
BITS="${BITS:-4}"

echo "==> checking python"
PY=""
for c in /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.11 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  echo "    no python >= 3.10 found; installing one"
  brew install python@3.12
  PY="$(brew --prefix)/bin/python3.12"
fi
echo "    using $PY ($($PY -V))"

echo "==> creating a venv at ~/.venvs/mitra"
mkdir -p "${HOME}/.venvs"
$PY -m venv "${HOME}/.venvs/mitra"
source "${HOME}/.venvs/mitra/bin/activate"
pip install --upgrade pip
pip install --upgrade mlx-lm transformers huggingface_hub

echo "==> downloading and quantising ${MODEL_ID} to ${BITS}-bit"
mkdir -p "${HOME}/models"
mlx_lm.convert --hf-path "${MODEL_ID}" -q --q-bits "${BITS}" --mlx-path "${OUT}"

echo "==> smoke test (Tibetan Unicode in, English out)"
mlx_lm.server --model "${OUT}" --port 8080 &
SRV=$!
sleep 25
python3 "$(dirname "$0")/mitra.py" "སྙིང་པོའི་དོན་ལ་ཚིག་གི་ལྟ་བ་མེད།" || true
kill $SRV 2>/dev/null || true

cat <<'EOS'

==> done.

Start the server when you want it (leave it running in its own terminal):

    source ~/.venvs/mitra/bin/activate
    mlx_lm.server --model ~/models/mitra-qwen35-4bit --port 8080

Then Claude calls it with no further setup:

    python3 ~/.claude/skills/tibetan-mitra/tools/mitra.py "སྙིང་པོའི་དོན་ལ་ཚིག་གི་ལྟ་བ་མེད།"
    python3 ~/.claude/skills/tibetan-mitra/tools/mitra.py --file verse.txt --per-line

If MLX gives trouble, the transformers path also works (slower, more RAM):
    pip install torch transformers>=5.13 accelerate
and load with dtype=bfloat16, device_map="auto", enable_thinking=False.
EOS
