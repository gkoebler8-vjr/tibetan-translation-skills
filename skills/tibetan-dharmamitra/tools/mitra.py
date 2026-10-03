#!/usr/bin/env python3
"""
mitra.py -- client for a locally served MITRA model (Dharmamitra's gemma-2-mitra-it).

Gives Claude a literal, source-faithful translation of Tibetan (or Sanskrit, Pali, Buddhist
Chinese) to use as the construal baseline, so the rendering stage is not also carrying the
lexical load. It is a first pass, never the final text, and never the arbiter of meaning.

SERVER. Expects an OpenAI-compatible endpoint at http://127.0.0.1:8080 (mlx_lm.server, llama.cpp
server, or Ollama on 11434). Start it with tools/setup_mitra.sh; if nothing is listening, this
script says so and exits non-zero rather than guessing.

USE
    python3 mitra.py "སྙིང་པོའི་དོན་ལ་ཚིག་གི་ལྟ་བ་མེད།"
    python3 mitra.py --file verse.txt --per-line      # one translation per line (pada by pada)
    python3 mitra.py --lang German "..."              # any target the model supports
    cat lines.txt | python3 mitra.py --per-line

MODEL. buddhist-nlp/mitra-qwen35-translate (Qwen3.5-9B, Apache 2.0). Its prompt template is the
one on the model card, sent as a plain completion; --legacy switches to the older gemma-2-mitra-it
format ("Please translate into <lang>: ... 🔽 Translation::") if you are serving that instead.

OUTPUT. Plain text on stdout: one translation per input unit, tab-separated from the source when
--per-line is used, so it can be pasted straight into a gloss table.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINTS = [
    ("http://127.0.0.1:8080/v1/completions", "openai"),
    ("http://127.0.0.1:8080/completion", "llamacpp"),
    ("http://127.0.0.1:11434/api/generate", "ollama"),
]
SEP = "\U0001F53D"  # 🔽


SYSTEM = (
    "You are an expert translator of classical Asian languages. In your translation, make sure "
    "to use proper IAST diacritics if Sanskrit terms occur, but also translate Sanskrit terms "
    "into English if English is the target language. The translation should be fluid and "
    "accurate. If the input is in English and the target is English, just return the input then."
)


def build_prompt(text, lang="English", legacy=False):
    """Prompt for mitra-qwen35-translate (default) or the older gemma-2-mitra-it (legacy)."""
    if legacy:
        return "Please translate into %s: %s %s Translation::" % (
            lang, text.replace("\n", " %s " % SEP).strip(), SEP)
    return ("%s\n\nHere is a piece of text to translate: %s\nProvide only the translation, "
            "without any explanation or additional information. Provide your translation in "
            "%s:" % (SYSTEM, text.strip(), lang))


def _post(url, payload, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def call(prompt, timeout=180, max_tokens=512):
    last = None
    for url, kind in ENDPOINTS:
        try:
            if kind == "openai":
                d = _post(url, {"prompt": prompt, "max_tokens": max_tokens,
                                "temperature": 0.0, "stop": ["#", "\n\n"]}, timeout)
                return d["choices"][0]["text"].strip()
            if kind == "llamacpp":
                d = _post(url, {"prompt": prompt, "n_predict": max_tokens,
                                "temperature": 0.0, "stop": ["#", "\n\n"]}, timeout)
                return d["content"].strip()
            d = _post(url, {"model": "mitra", "prompt": prompt, "stream": False,
                            "options": {"temperature": 0.0, "stop": ["#"]}}, timeout)
            return d["response"].strip()
        except (urllib.error.URLError, OSError, KeyError) as e:
            last = "%s: %s" % (url, e)
            continue
    sys.stderr.write(
        "no local MITRA server answered.\n"
        "  last error: %s\n"
        "  start one:  source ~/.venvs/mitra/bin/activate && "
        "mlx_lm.server --model ~/models/mitra-9b-4bit --port 8080\n"
        "  install it: bash ~/.claude/skills/tibetan-mitra/tools/setup_mitra.sh\n" % last)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="Literal translation via a local MITRA model.")
    ap.add_argument("text", nargs="*", help="source text; omit to read stdin")
    ap.add_argument("--file", help="read the source from this file")
    ap.add_argument("--lang", default="English", help="target language (default English)")
    ap.add_argument("--per-line", action="store_true",
                    help="translate each line separately (pada by pada) and tab-align the pairs")
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--legacy", action="store_true",
                    help="use the old gemma-2-mitra-it prompt format instead of qwen35")
    a = ap.parse_args()

    if a.file:
        src = open(a.file, encoding="utf-8").read()
    elif a.text:
        src = " ".join(a.text)
    else:
        src = sys.stdin.read()
    src = src.strip()
    if not src:
        sys.exit("no input")

    units = [l.strip() for l in src.splitlines() if l.strip()] if a.per_line else [src]
    for u in units:
        out = call(build_prompt(u, a.lang, legacy=a.legacy), max_tokens=a.max_tokens)
        print("%s\t%s" % (u, out) if a.per_line else out)


if __name__ == "__main__":
    main()
