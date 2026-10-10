#!/usr/bin/env bash
# install.sh — set up the Tibetan translation skills on this machine.
#
#   ./install.sh                 full setup: skills, venv, MITRA lexicon download, index build
#   ./install.sh --skills-only   just copy skills/ into ~/.claude/skills
#   ./install.sh --golden DIR    also index a GoldenDict/StarDict folder of your own dictionaries
#   ./install.sh --public        also fetch the freely redistributable Tibetan-English dictionaries of
#                                Christian Steinert's open-source project (Hopkins, Rangjung Yeshe, Berzin,
#                                Valby, Ives/Waldo, 84000 glossary ...) and index them (~38 MB download)
#   ./install.sh --cat           also set up Tiger CAT, the local app in cat/: a venv at ~/.venvs/vcat
#                                (python-docx, pyewts) and the double-clickable cat/Tiger CAT.app.
#                                Without this flag the app is not touched. --skills-only --cat gives
#                                skills and app without the dictionary.
#   ./install.sh --help          print this list
#
# New to Claude Code or the terminal? docs/getting-started.md. The skills in full: docs/skills.md.
# The app: cat/README.md.
#
# Idempotent: safe to re-run. Nothing here is uploaded anywhere.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-$(command -v python3.11 || command -v python3)}"
VENV="$HOME/.venvs/tib"
DATA="$HOME/.tibdict"
GOLDEN=""
SKILLS_ONLY=0
PUBLIC=0
CAT=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills-only) SKILLS_ONLY=1; shift ;;
    --golden) GOLDEN="$2"; shift 2 ;;
    --public) PUBLIC=1; shift ;;
    --cat) CAT=1; shift ;;
    -h|--help) awk 'NR>1 && !/^#/ {exit} NR>1 {sub(/^# ?/,""); print}' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

echo "1/4 skills -> ~/.claude/skills"
mkdir -p "$HOME/.claude/skills"
for s in tibetan-translate tibetan-verse tibetan-citations tibetan-dharmamitra; do
  rm -rf "$HOME/.claude/skills/$s"
  cp -R "$HERE/skills/$s" "$HOME/.claude/skills/$s"
done
install_cat() {
  local CVENV="$HOME/.venvs/vcat"
  echo "cat: Tiger CAT venv at $CVENV (python-docx, pyewts)"
  if [[ ! -x "$CVENV/bin/python3" ]]; then "$PY" -m venv "$CVENV"; fi
  "$CVENV/bin/pip" install -q --upgrade pip
  "$CVENV/bin/pip" install -q python-docx pyewts
  echo "cat: building cat/Tiger CAT.app"
  bash "$HERE/cat/tools/make_app.sh"
  echo "cat: done. Double-click \"$HERE/cat/Tiger CAT.app\" or run: $CVENV/bin/python3 cat/tools/serve.py --port 8765"
}
[[ $SKILLS_ONLY -eq 1 ]] && { [[ $CAT -eq 1 ]] && install_cat; echo "done (skills only)"; exit 0; }

echo "2/4 python venv at $VENV (botok, pyewts)"
if [[ ! -x "$VENV/bin/python" ]]; then "$PY" -m venv "$VENV"; fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q botok pyewts

echo "3/4 MITRA Tibetan Lexicon (CC BY-SA 4.0, Dharmamitra) -> $DATA"
mkdir -p "$DATA" "$HERE/resources"
if [[ ! -f "$DATA/mitra-tib-llm-2026/mitra-tib-llm-2026.ifo" ]]; then
  ZIP="$HERE/resources/mitra-stardict-tib-lexicon-2026.zip"
  [[ -f "$ZIP" ]] || curl -L --progress-bar -o "$ZIP" https://dharmamitra.org/pub/dictionaries/mitra-stardict-tib-lexicon-2026.zip
  unzip -q -o "$ZIP" -d "$HERE/resources/"
  rm -rf "$DATA/mitra-tib-llm-2026"
  mv "$HERE/resources/mitra-tib-llm-2026" "$DATA/"
fi

TIBDICT="$HOME/.claude/skills/tibetan-translate/tools/tibdict.py"
if [[ $PUBLIC -eq 1 ]]; then
  echo "3b/4 public Tibetan-English dictionaries (Christian Steinert's open-source project) -> $DATA/public"
  echo "     Freely redistributable dictionary files from github.com/christiansteinert/tibetan-dictionary; per its README, \"THE COPYRIGHT OF THE DICTIONARY DATA IS WITH THE RESPECTIVE AUTHORS\"."
  "$VENV/bin/python" "$TIBDICT" fetch-public --dest "$DATA/public" || echo "     (some files could not be fetched; re-run ./install.sh --public later to complete them)"
fi

echo "4/4 building the dictionary index"
ARGS=(build --mitra "$DATA")
if [[ $PUBLIC -eq 1 && -d "$DATA/public" ]]; then ARGS+=(--public "$DATA/public"); fi
if [[ -n "$GOLDEN" ]]; then ARGS+=(--golden "$GOLDEN"); else ARGS+=(--golden "${TIBDICT_GOLDEN:-/nonexistent}"); fi
"$VENV/bin/python" "$TIBDICT" "${ARGS[@]}"
"$VENV/bin/python" "$TIBDICT" status
[[ $CAT -eq 1 ]] && install_cat
echo "done. Try: python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate \"བླ་མའི་བྱིན་རླབས།\""
