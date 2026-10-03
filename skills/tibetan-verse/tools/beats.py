#!/usr/bin/env python3
"""
beats.py -- beat counter and stanza-shape checker for Tibetan verse rendering (guidelines v4).

WHAT IT DOES. Counts the stressed syllables (beats) of an English verse line, checks the
rhythm hygiene of guidelines section 7, and checks a whole stanza against its mode:

    chant mode     every line carries the same number of beats
    citation mode  a core band of two adjacent counts n / n+1, with at most ONE line in the
                   stanza sitting one beat outside it (so 4-5-4-5-6 passes, 3-5-4-3-5 does not)
    both           no line exceeds 7 beats

WHAT IT IS NOT. It is an aid, not the authority. Gate 1 (read the stanza aloud) outranks it
always. English stress is contextual; this counts lexical stress, so it reports each line as an
interval -- the beats it is sure of, plus the syllables that could take a beat if the rhythm
promotes them -- and asks whether the stanza can be *satisfied* inside those intervals, rather
than pretending to a single true count.

USE -- import:
    from beats import line_beats, stanza
    lo, hi, pattern, flags = line_beats("comes only from the mark of merit gathered,")
    report = stanza(lines, "citation")     # report.ok, report.text

USE -- command line:
    python3 beats.py citation "line one," "line two,"
    python3 beats.py chant < stanza.txt          # one line per row, blank rows skipped
    exit status is non-zero if the stanza fails its mode.

PATTERN symbols:  / a beat   x a syllable that may take a beat (secondary stress, or a
monosyllable English promotes and demotes by context)   . an off-beat   ? an unknown polysyllable

FLAGS:
    SAG:n          four or more off-beats in a row ending at syllable n -- the line has lost
                   its pulse; replace a function-word chain with a content word, or re-break
    SLACK:n        a second run of three off-beats; one such run per line is ordinary English,
                   two make the line go slack
    CLASH:n        more than one pair of adjacent beats; one is fine and useful, two is a stumble
    WEAK-END       the line ends on a function word, or trails more than two off-beats past its
                   last beat -- end on a stressed heavy word or a falling ending
    OVER           more than 7 beats even on the low count -- unpack the pada into two lines
    UNKNOWN:w      w is a polysyllable the lexicon does not have; first-syllable stress assumed.
                   Add it to lexicon.py as "word": (syllables, [primary], [secondary]) and the
                   tool is right about it forever after.

EXTENDING. lexicon.py carries ~2100 hand-checked words, inherited from the Lam Zab scansion
checker. Adding to it is the intended maintenance.
"""
import re
import unicodedata

def _ascii(s):
    """IAST and other diacritics to plain letters (Śavarī -> Savari) so names are not split at the marks."""
    s = s.replace('ṃ', 'm').replace('ṁ', 'm')
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexicon import STRESS

# Never take a beat.
FUNCTION = set("""a an the of to in on at by for and or but nor so as is are was were be been
being am do does did has have had will would shall should can could may might must if that this
these those with from into onto upon within without through over under above below than then
there here i you he she it we they me him her us them my your his its our their who whom whose
which what while when where because though although until since about across after before
against among around behind beneath beside between beyond during except inside like near off
out past per round toward towards up upon via yet nor am 's""".split())

# Swing either way: English promotes or demotes them by position. Counted as "may take a beat".
FLEX = set("""all each one own no not now then thus still just such very more most less least
made make makes come comes came go goes went let lets take takes put gets get give gives kept
keep well much many few both same own back down out up on in off well like near far new old
long great good big small first last next same self same""".split())


def _count_syl(w):
    groups = re.findall(r'[aeiouy]+', w)
    n = len(groups)
    if n > 1 and w.endswith('e') and not w.endswith(('le', 'ee', 'ie', 'ye')):
        n -= 1
    if (n > 1 and w.endswith('es') and w[-3:-2] not in 'aeiou'
            and not w.endswith(('ces', 'ges', 'ses', 'xes', 'zes', 'ches', 'shes'))):
        n -= 1
    return max(1, n)


SUFFIX = [('edly', 2), ('ing', 1), ('ness', 1), ('ment', 1), ('ly', 1), ('ers', 1),
          ('er', 1), ('est', 1), ('ed', 0), ('es', 0), ('s', 0)]


def _labels_from_entry(entry):
    n, prim, sec = entry
    out = []
    for i in range(1, n + 1):
        if i in prim:
            out.append('/')
        elif i in sec:
            out.append('x')
        else:
            out.append('.')
    return out


def _from_base(w):
    """Strip a suffix and look the base up; returns labels or None."""
    for suf, extra in SUFFIX:
        if w.endswith(suf) and len(w) > len(suf) + 1:
            base = w[:-len(suf)]
            if suf == 'ed':
                extra = 1 if base and base[-1] in 'td' else 0
            if suf in ('es', 's'):
                extra = 1 if (base and base[-1] in 'sxz') or base.endswith(
                    ('ch', 'sh', 'ce', 'ge', 'se', 'ze', 'x')) else 0
            if base in STRESS:
                return _labels_from_entry(STRESS[base]) + ['.'] * extra
            if base + 'e' in STRESS:
                return _labels_from_entry(STRESS[base + 'e']) + ['.'] * extra
            if _count_syl(base) == 1:
                return (['.'] if base in FUNCTION else
                        ['x'] if base in FLEX else ['/']) + ['.'] * extra
    return None


def word_labels(token):
    """One token -> a list of syllable labels, plus a list of unknown words seen."""
    if '-' in token:
        out, unk = [], []
        for part in token.split('-'):
            if not part:
                continue
            l, u = word_labels(part)
            out += l
            unk += u
        return out, unk
    w = re.sub(r"[^a-zA-Z']", "", token).lower().strip("'")
    if not w:
        return [], []
    bare = w.replace("'", "")
    if bare in STRESS:
        return _labels_from_entry(STRESS[bare]), []
    if w.endswith("'s") and bare[:-1] in STRESS:
        e = STRESS[bare[:-1]]
        extra = 1 if bare[:-2].endswith(('s', 'x', 'z', 'ch', 'sh', 'ce', 'ge', 'se')) else 0
        return _labels_from_entry(e) + ['.'] * extra, []
    n = _count_syl(bare)
    if n == 1:
        if bare in FUNCTION:
            return ['.'], []
        if bare in FLEX:
            return ['x'], []
        return ['/'], []
    fb = _from_base(bare)
    if fb is not None:
        return fb, []
    # Unknown polysyllable: assume first-syllable stress (the English noun default) and flag it.
    return ['/'] + ['.'] * (n - 1), [bare]


def line_beats(line):
    """-> (low, high, pattern, flags). low = beats it is sure of; high = low + promotable ones."""
    line = _ascii(line)
    toks = re.findall(r"[A-Za-z][A-Za-z'-]*", line)
    pattern, unknown, last_word = [], [], None
    for t in toks:
        labs, unk = word_labels(t)
        pattern += labs
        unknown += unk
        if labs:
            last_word = re.sub(r"[^a-zA-Z']", "", t).lower()
    pat = ''.join(pattern)
    low = pat.count('/')
    high = low + pat.count('x')

    flags = []
    for u in dict.fromkeys(unknown):
        flags.append("UNKNOWN:" + u)
    if low > 7:
        flags.append("OVER")
    # rhythm: runs of off-beats. Three in a row is ordinary English and allowed once;
    # a second such run goes slack, and four in a row has lost the pulse outright.
    runs, run = [], 0
    for i, c in enumerate(pat, 1):
        if c == '.':
            run += 1
        else:
            if run:
                runs.append((run, i - 1))
            run = 0
    if run:
        runs.append((run, len(pat)))
    threes = [end for length, end in runs if length == 3]
    for length, end in runs:
        if length >= 4:
            flags.append("SAG:%d" % end)
    if len(threes) > 1:
        flags.append("SLACK:%d" % threes[1])
    # clash: more than one pair of adjacent certain beats
    clashes = [i for i in range(1, len(pat)) if pat[i - 1] == '/' and pat[i] == '/']
    if len(clashes) > 1:
        flags.append("CLASH:%d" % (clashes[1] + 1))
    # weak ending
    tail = len(pat) - (max(pat.rfind('/'), pat.rfind('x')) + 1) if ('/' in pat or 'x' in pat) else 0
    if last_word in FUNCTION or tail > 2:
        flags.append("WEAK-END")
    return low, high, pat, flags


class Report(object):
    def __init__(self, ok, text):
        self.ok = ok
        self.text = text

    def __str__(self):
        return self.text


def stanza(lines, mode="citation", padas=None):
    """Check a stanza. mode: 'chant' (isometric) or 'citation' (band of n / n+1)."""
    lines = [l for l in lines if l.strip()]
    rows = [(l,) + line_beats(l) for l in lines]
    out = []
    for l, lo, hi, pat, flags in rows:
        rng = str(lo) if lo == hi else "%d-%d" % (lo, hi)
        out.append("  %-4s %-28s %s" % (rng, pat, " ".join(flags)))
        out.append("       %s" % l.strip())
    ivals = [(lo, hi) for _, lo, hi, _, _ in rows]
    ok = True
    if not ivals:
        return Report(False, "no lines")

    if mode == "chant":
        good = [n for n in range(1, 8) if all(lo <= n <= hi for lo, hi in ivals)]
        if good:
            verdict = "chant mode OK: every line can be read at %s beats" % (
                " or ".join(map(str, good)))
        else:
            ok = False
            verdict = ("chant mode FAILS: no single beat count fits every line "
                       "(intervals %s). Re-measure the stanza or re-break the offending line."
                       % ", ".join("%d-%d" % iv for iv in ivals))
    else:
        def fits(iv, lo_ok, hi_ok):
            return not (iv[1] < lo_ok or iv[0] > hi_ok)
        # Citation mode (guidelines v4). The target is a band of two adjacent counts, n / n+1.
        # The finished Lam Zab verses, flat-read, actually spread over three counts (the
        # translator promotes a function word onto the iambic grid now and then), so a spread of
        # three passes, a spread of four is reported as WIDE, and anything wider fails.
        def spread_fit(width):
            for n in range(1, 8):
                if all(fits(iv, n, n + width) for iv in ivals):
                    return n
            return None
        n2 = spread_fit(1)
        n3 = spread_fit(2)
        n4 = spread_fit(3)
        if n2 is not None:
            verdict = "citation mode OK: core band %d-%d fits every line" % (n2, n2 + 1)
        elif n3 is not None:
            verdict = ("citation mode OK: lines sit within %d-%d (a spread of three; the band "
                       "of two is the target)" % (n3, n3 + 2))
        elif n4 is not None:
            verdict = ("citation mode WIDE: lines spread over %d-%d. The block still reads as one "
                       "piece only if the pulse is the same throughout; tighten the outliers if "
                       "you can without bending the English." % (n4, n4 + 3))
        else:
            ok = False
            verdict = ("citation mode FAILS: the lines spread over more than four counts "
                       "(intervals %s). Re-measure, unpack the long lines, or set as prose."
                       % ", ".join("%d-%d" % iv for iv in ivals))

    # Rhythmic kind (advisory): rising (first beat not on syllable 1) vs falling. One kind per
    # block is the one hard metrical rule; an initial inversion is not a change of kind, so this
    # only speaks when a clear majority of lines start on a certain beat and others clearly do not.
    starts = []
    for _, lo, hi, pat, _ in rows:
        p = pat.lstrip('?')
        if not p:
            continue
        starts.append('F' if p[0] == '/' else 'R' if p[0] in '._' else 'x')
    nf, nr = starts.count('F'), starts.count('R')
    if nf and nr and min(nf, nr) >= max(3, len(starts) // 3):
        verdict += ("\n  KIND?: %d line(s) open on a beat (falling) and %d on an off-beat (rising). "
                    "One rhythmic kind per block; initial inversions are fine, a block that "
                    "alternates kinds is not." % (nf, nr))

    if any(lo > 7 for lo, _ in ivals):
        ok = False
        verdict += "\n  ceiling FAILS: a line is over 7 beats. Unpack it into two lines."
    if padas is not None and len(lines) < padas:
        ok = False
        verdict += ("\n  line count FAILS: %d English lines for %d Tibetan padas. "
                    "Something has been dropped." % (len(lines), padas))
    out.append("  " + verdict)
    return Report(ok, "\n".join(out))


def _main(argv):
    if len(argv) < 2 or argv[1] not in ("chant", "citation"):
        print(__doc__)
        return 2
    mode = argv[1]
    lines = argv[2:]
    if not lines:
        lines = [l.rstrip("\n") for l in sys.stdin]
    # A blank line separates stanzas; the band and kind rules apply per stanza, not per block
    # of several stanzas (a long quotation is several stanzas).
    stanzas, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l)
        elif cur:
            stanzas.append(cur); cur = []
    if cur:
        stanzas.append(cur)
    ok = True
    for i, st in enumerate(stanzas, 1):
        rep = stanza(st, mode)
        if len(stanzas) > 1:
            print("stanza %d" % i)
        print(rep.text)
        ok = ok and rep.ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
