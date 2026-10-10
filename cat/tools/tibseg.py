#!/usr/bin/env python3
"""
tibseg.py -- first-pass segmentation of a Tibetan text into translation units for Tiger CAT.

  python3 tools/tibseg.py <text.txt> [--max 45]   -> one "Uxx (hint) text" line per unit

The source's own structure comes first: a line is a unit, a blank line closes a section, a short line that
ends with a shad is a heading (hint "heading"), a numbered line keeps its number. A long line is split at
sentence ends (shad) into pieces of at most --max syllables, never below a sentence end; a line that does
not end at a shad continues into the next. Verse is a run of three or more shad-delimited lines with the
same syllable count (7, 9, 11, 13, 15) and is grouped into stanzas of four. Tiny fragments (a closing frame
such as "ces gsungs so") join the unit before them. Heuristic: the translator corrects the split in Settings.
"""
import argparse, re, sys

VERSE_COUNTS = (7, 9, 11, 13, 15)
NUM = re.compile(r'^\s*(?:[༠-༩]+[\.\)༔]?|\d+[\.\)]|[a-zA-Z][\.\)])\s*')

def syllables(s):
    s = re.sub(r'[།༑༔\s]+', ' ', s).strip()
    s = NUM.sub('', s)
    return len([x for x in re.split(r'[་ ]+', s) if x])

def pieces_of(text):
    """Split one line at every shad, keeping the shad(s) with the clause."""
    text = re.sub(r'\s+', ' ', text).strip()
    out = []
    for m in re.finditer(r'[^།༑༔]+(?:[།༑༔]\s*)*', text):
        p = m.group(0).strip()
        if not p or not re.search(r'[ༀ-࿿]', p): continue
        body = re.sub(r'[།༑༔\s]+$', '', p)
        out.append({'text': p, 'syl': syllables(body), 'ends': bool(re.search(r'[།༑༔]\s*$', p))})
    return out

def verse_groups(ps):
    """Return a list of ('verse', count, [pieces]) / ('prose', None, [pieces]) runs."""
    runs, i, n = [], 0, len(ps)
    while i < n:
        c = ps[i]['syl']; j = i
        while j < n and ps[j]['syl'] == c: j += 1
        if c in VERSE_COUNTS and j - i >= 3: runs.append(('verse', c, ps[i:j])); i = j; continue
        if runs and runs[-1][0] == 'prose': runs[-1][2].append(ps[i])
        else: runs.append(('prose', None, [ps[i]]))
        i += 1
    return runs

def chunk_prose(ps, max_syl):
    """Pieces of one prose line -> units of at most max_syl syllables, split only at sentence ends."""
    units, buf, syl = [], [], 0
    for p in ps:
        if buf and syl + p['syl'] > max_syl and syl >= 8:
            units.append(buf); buf, syl = [], 0
        buf.append(p); syl += p['syl']
    if buf: units.append(buf)
    return units

def segment(text, max_syl=45):
    lines = [l.rstrip() for l in text.replace('\r', '').split('\n')]
    units, carry = [], ''
    for idx, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            if units: units[-1]['section_end'] = True
            continue
        if not re.search(r'[ༀ-࿿]', line): continue
        if carry: line = carry + ' ' + line; carry = ''
        if not re.search(r'[།༑༔]\s*$', line) and idx + 1 < len(lines) and lines[idx + 1].strip():
            carry = line; continue                       # the sentence continues on the next line
        ps = pieces_of(line)
        if not ps: continue
        numbered = bool(NUM.match(line))
        nxt = next((l for l in lines[idx + 1:] if l.strip()), '')
        if len(ps) == 1 and syllables(line) <= 12 and nxt and not numbered:
            units.append({'hint': 'heading', 'text': line}); continue
        for kind, cnt, run in verse_groups(ps):
            if kind == 'verse':
                k = 0
                while k < len(run):
                    take = 4 if len(run) - k >= 4 else len(run) - k
                    units.append({'hint': 'verse %d×%d' % (cnt, take), 'text': ' '.join(x['text'] for x in run[k:k + take])}); k += take
            else:
                for ci, chunk in enumerate(chunk_prose(run, max_syl)):
                    units.append({'hint': 'numbered' if numbered and ci == 0 else 'prose', 'text': ' '.join(x['text'] for x in chunk)})
    if carry: units.append({'hint': 'prose', 'text': carry})
    FRAME_END = re.compile(r'^((?:[^།༑༔]*(?:གསུངས|ཞེས|ཅེས|ཤེས)[^།༑༔]*)[།༑༔\s]+)')
    FRAME_OPEN = re.compile(r'(?:ལས|ནས|ན་རེ|ཞེས|ཅེས|ཏེ|སྟེ)[།༑༔\s]*$')
    merged = []
    for u in units:
        prev = merged[-1] if merged else None
        # a closing frame ("ces gsungs so") at the start of a prose unit after verse joins the verse
        if prev and prev['hint'].startswith(('verse', 'frame')) and u['hint'] in ('prose', 'numbered'):
            m = FRAME_END.match(u['text'])
            if m and syllables(m.group(1)) <= 5:
                prev['text'] += ' ' + m.group(1).strip(); rest = u['text'][m.end():].strip()
                if not rest: continue
                u = dict(u, text=rest)
        # a short opening frame ("de yang rgyud bla ma las/") before verse joins the verse
        if prev and prev['hint'] in ('prose', 'numbered') and u['hint'].startswith('verse') and syllables(prev['text']) <= 12 and FRAME_OPEN.search(prev['text']):
            merged.pop(); u = dict(u, text=prev['text'] + ' ' + u['text'], hint='frame + ' + u['hint'])
        # tiny fragments join the unit before
        if merged and u['hint'] in ('prose', 'numbered') and syllables(u['text']) <= 4 and not merged[-1].get('section_end'):
            merged[-1]['text'] += ' ' + u['text']; continue
        merged.append(u)
    return merged

def to_lines(units):
    return ['U%02d (%s) %s' % (i + 1, u['hint'], u['text']) for i, u in enumerate(units)]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file'); ap.add_argument('--max', type=int, default=45)
    a = ap.parse_args()
    for l in to_lines(segment(open(a.file, encoding='utf-8').read(), a.max)): print(l)

if __name__ == '__main__':
    main()
