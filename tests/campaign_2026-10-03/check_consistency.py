#!/usr/bin/env python3
"""
check_consistency.py -- does the shared glossary hold across consecutive pages?

  python3 check_consistency.py runs/run6_consistency/shared/gc.glossary.tsv \
          material/consistency/GC1_units.md:runs/run6_consistency/GC1/final.md \
          material/consistency/GC2_units.md:runs/run6_consistency/GC2/final.md ...

For every glossary row (wylie <tab> English [<tab> note]) it finds the pages whose Tibetan contains
the wylie term (units converted to Wylie with pyewts, falling back to the ~/.venvs/tib interpreter if
pyewts is not importable), then checks whether that page's TEXT uses the bound English (stem match on
each content word of the English, case-insensitive). It reports, per page: terms expected / found /
missing, and lists the missing ones with the alternatives actually used when one of the other
glossary Englishes for the same wylie appears. It also lists wylie keys that carry two different
Englishes in the glossary (drift inside the file). Also runs `register.py --titles` on the glossary.
"""
import sys, re, os, subprocess
def to_wylie(text):
    try:
        import pyewts
        return pyewts.pyewts().toWylie(text)
    except ImportError:
        py = os.path.expanduser("~/.venvs/tib/bin/python")
        r = subprocess.run([py, "-c", "import sys,pyewts;print(pyewts.pyewts().toWylie(sys.stdin.read()))"], input=text, capture_output=True, text=True)
        return r.stdout
def stems(english):
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", english.lower()) if w not in STOP]
    return [w[:5] if len(w) > 5 else w for w in words]
STOP = set("the a an of to in and or for with by on at from as is are be that this it its".split())
def main():
    gl = sys.argv[1]; pages = [x.split(":") for x in sys.argv[2:]]
    rows = []
    for l in open(gl, encoding="utf-8"):
        if not l.strip() or l.startswith("#") or l.startswith("TITLE"): continue
        f = l.rstrip("\n").split("\t")
        if len(f) >= 2 and f[0].strip() and f[1].strip(): rows.append((f[0].strip(), f[1].strip()))
    by = {}
    for w, e in rows: by.setdefault(w, []).append(e)
    drift = {w: es for w, es in by.items() if len(set(x.lower() for x in es)) > 1}
    print(f"glossary: {len(rows)} rows, {len(by)} wylie keys, {len(drift)} keys with more than one English:")
    for w, es in drift.items(): print(f"  {w}: {' | '.join(dict.fromkeys(es))}")
    total_exp = total_found = 0
    for upath, fpath in pages:
        tib = "\n".join(l.split(" ", 2)[-1] for l in open(upath, encoding="utf-8") if re.match(r"^U\d\d ", l))
        wy = to_wylie(tib).lower()
        wy = re.sub(r"[/|_\n]+", " ", wy); wy = re.sub(r"\s+", " ", wy)
        text = []
        for block in re.split(r"^### ", open(fpath, encoding="utf-8").read(), flags=re.M)[1:]:
            m = re.search(r"TEXT:\n(.*?)\n(?:FOOTNOTES|NOTES):", block, re.S)
            if m: text.append(m.group(1))
        text = "\n".join(text).lower()
        expected = [(w, by[w][0]) for w in by if f" {w} " in f" {wy} "]
        found, missing = [], []
        for w, e in expected:
            st = stems(e)
            if st and all(s in text for s in st): found.append((w, e))
            else:
                alt = [x for x in by[w][1:] if stems(x) and all(s in text for s in stems(x))]
                missing.append((w, e, alt))
        total_exp += len(expected); total_found += len(found)
        print(f"\n{os.path.basename(fpath)}: {len(expected)} bound terms occur in the Tibetan; {len(found)} rendered as bound; {len(missing)} not found as bound")
        for w, e, alt in missing: print(f"  MISSING {w} = {e}" + (f"  (page uses: {' | '.join(alt)})" if alt else ""))
    if total_exp: print(f"\nTOTAL: {total_found}/{total_exp} bound-term occurrences rendered as bound ({100*total_found//total_exp}%)")
    reg = os.path.expanduser("~/.claude/skills/tibetan-citations/tools/register.py")
    if os.path.exists(reg):
        print("\nregister.py --titles:"); subprocess.run([sys.executable, reg, "--titles", gl])
if __name__ == "__main__": main()
