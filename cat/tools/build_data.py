#!/usr/bin/env python3
"""
build_data.py -- parse a tibetan-translate run directory into one JSON file for the CAT demo UI.

  python3 tools/build_data.py <run_dir> --units <units.md> --work <name> -o demo/data.json

Reads the files the skill writes (final.md, <work>.construal.md, <work>.glossary.tsv, <work>.sources.tsv,
dm_*.txt, runlog.md) plus the page's Tibetan units file, and emits data.json. The skill's own files stay
the source of truth; this is a viewer's index of them. Wylie <-> Unicode conversion uses pyewts when
importable (the ~/.venvs/tib interpreter has it); otherwise only the given form is stored.
"""
import argparse, glob, json, os, re, sys

try:
    import pyewts
    _C = pyewts.pyewts()
except ImportError:
    _C = None

TIB = re.compile(r'[\u0F00-\u0FFF]')
UID = r'U\d+[a-z]?'            # a unit id; a long period may be split into sub-units U10a, U10b …

def nat(k):
    """Natural order of unit ids: U09 < U10 < U10a < U10b < U11."""
    m = re.match(r'U(\d+)([a-z]?)', k or '')
    return (int(m.group(1)), m.group(2)) if m else (10**6, k)

def id_range(a, b):
    """U06–U09 -> U06..U09; U10a–U10c -> U10a..U10c; U10–U10c -> U10, U10a..U10c."""
    na, nb = nat(a), nat(b)
    if na[0] == nb[0] and nb[1]:
        letters = [chr(c) for c in range(ord(na[1] or 'a'), ord(nb[1]) + 1)]
        return ([a] if not na[1] else []) + ['U%02d%s' % (na[0], l) for l in letters]
    return ['U%02d' % i for i in range(na[0], nb[0] + 1)]

def to_wylie(t):
    if not t or not _C or not TIB.search(t): return t or ''
    w = _C.toWylie(t).replace('_', ' ')
    w = re.sub(r'/\s*/', '//', w)
    w = re.sub(r'//(?=[^\s/])', '// ', w)
    return re.sub(r'\s+', ' ', w).strip()

def to_script(w):
    if not w or not _C or TIB.search(w): return w or ''
    try:
        return _C.toUnicode(w)
    except Exception:
        return w

# ------------------------------------------------------------------ units (Tibetan)
def parse_units(path):
    units, meta = {}, {}
    for line in open(path, encoding='utf-8'):
        s = line.strip()
        m = re.match(r'^(%s)\s*(\([^)]*\))?\s*(.+)$' % UID, s)
        if m:
            units[m.group(1)] = {'hint': (m.group(2) or '').strip('()'), 'tib': m.group(3).strip()}
        elif s.startswith('# '): meta['title'] = s[2:].strip()
        elif s.startswith('Work:'): meta['work'] = s[5:].strip()
        elif s.startswith('Source:'): meta['source'] = s[7:].strip()
    return units, meta

# ------------------------------------------------------------------ final.md
NOTE_TAGS = ['Q', 'Alt', 'Comm', 'Var', 'Source', 'MITRA', 'Issue', 'Check', 'Conf', 'Grounding', 'Prior']

def parse_final(md):
    units, cur, field, intro = [], None, None, []
    for line in md.splitlines():
        m = re.match(r'^### (%s)\s*$' % UID, line)
        if m:
            cur = {'id': m.group(1), 'header': '', 'text': [], 'footnotes': [], 'notes': []}
            units.append(cur); field = None; continue
        if cur is None:
            if line.startswith('## '): break
            intro.append(line); continue
        if line.startswith('## '):
            cur = None; field = None; continue
        m = re.match(r'^(HEADER|TEXT|FOOTNOTES|NOTES):\s*(.*)$', line)
        if m:
            field = m.group(1)
            if field == 'HEADER': cur['header'] = m.group(2).strip()
            elif m.group(2).strip(): cur[field.lower()].append(m.group(2))
            continue
        if field in ('TEXT', 'FOOTNOTES', 'NOTES'):
            cur[field.lower()].append(line)
    out = []
    for u in units:
        text = [l.rstrip() for l in u['text']]
        while text and not text[-1]: text.pop()
        while text and not text[0]: text.pop(0)
        fns = []
        for l in u['footnotes']:
            m = re.match(r'^\s*FN\((.*?)\):\s*(.*)$', l)
            if m: fns.append({'anchor': '' if m.group(1).strip() in ('', '*') else m.group(1).strip(), 'text': m.group(2).strip()})   # FN() / FN(*): on the whole unit
            elif fns and l.strip() and l.strip().lower() != 'none': fns[-1]['text'] += ' ' + l.strip()
        notes = []
        for l in u['notes']:
            s = l.strip()
            if not s or s.lower() == 'none': continue
            m = re.match(r'^(%s):\s*(.*)$' % '|'.join(NOTE_TAGS), s)
            if m:
                tag, body = m.group(1), m.group(2)
                n = {'tag': tag, 'text': body}
                if tag == 'Q':
                    q = re.match(r'^\((Q\d+)[^)]*\)\s*(.*)$', body)
                    if q: n['qid'] = q.group(1); n['text'] = q.group(2)
                    n['resolved'] = bool(re.search(r'\bresolved\b', body))
                notes.append(n)
            elif notes:
                notes[-1]['text'] += ' ' + s
            else:
                notes.append({'tag': 'Note', 'text': s})
        out.append({'id': u['id'], 'header': u['header'], 'header_fields': parse_header(u['header']),
                    'text': text, 'footnotes': fns, 'notes': notes})
    return out, '\n'.join(intro).strip()

def parse_header(h):
    parts = [p.strip() for p in re.split(r'\s·\s', h)]
    f = {'raw': h}
    rest = []
    for i, p in enumerate(parts):
        low = p.lower()
        if i == 0 and re.match(r'^U\d+$', p): continue
        if low.startswith('grounding:'): f['grounding'] = p.split(':', 1)[1].strip()
        elif low.startswith('confidence:'): f['confidence'] = p.split(':', 1)[1].strip()
        elif low.startswith('prior:'): f['prior'] = p.split(':', 1)[1].strip()
        elif re.search(r'\btoh\b|not a citation|source not located|quoted in', low): f['source'] = p
        elif re.search(r'practitioner|academic|hybrid|working crib', low): f['audience'] = p
        elif 'form' not in f: f['form'] = p
        else: rest.append(p)
    f['register'] = ' · '.join(rest)
    return f

# ------------------------------------------------------------------ construal
def parse_construal(md):
    units, grounding, check, cur = {}, {}, [], None
    section = None
    for line in md.splitlines():
        m = re.match(r'^## (?:block\s+)?(%s)' % UID, line)
        if m:
            cur = m.group(1); units.setdefault(cur, []); section = 'unit'; continue
        if line.startswith('## GROUNDING'): section = 'grounding'; cur = None; continue
        if line.startswith('## CHECK'): section = 'check'; cur = None; continue
        if line.startswith('## '): section = None; cur = None; continue
        if section == 'unit' and line.strip():
            m = re.match(r'^([A-Z/\-]+\d*|Q\d+|Var\d*|Issue)\s*(?:\([^)]*\))?:\s*(.*)$', line.strip())
            if m: units[cur].append({'key': m.group(1), 'text': m.group(2)})
            elif units[cur]: units[cur][-1]['text'] += ' ' + line.strip()
        elif section == 'grounding' and line.strip():
            m = re.match(r'^(%s)(?:[–-](%s))?\s*(.*)$' % (UID, UID), line.strip())
            if m:
                a, b = m.group(1), m.group(2) or m.group(1)
                ids = id_range(a, b)
                for i in ids: grounding.setdefault(i, []).append(line.strip())
                last = ids
            elif grounding and line.startswith(' '):
                for i in last: grounding[i][-1] += '\n' + line.strip()
        elif section == 'check' and line.strip():
            check.append(line.strip())
    return units, grounding, check

# ------------------------------------------------------------------ dm_* outputs
SEG_RE = re.compile(r'\b((?:BO|EN|SA|ZH|PA)_[A-Za-z0-9_\-\(\)\.]+:[0-9a-z\-]+)')

def parse_explore(txt):
    blocks = [b.strip() for b in re.split(r'\n-{3,}\n', txt) if b.strip()]
    hits, summary = [], ''
    for b in blocks:
        lines = b.splitlines()
        heads = [l for l in lines if re.match(r'^\*\*[^*].*\*\*\s*$', l.strip())]
        orig = re.search(r'\*\*Original:\*\*\s*(.*)', b)
        trans = re.search(r'\*\*Translation:\*\*\s*(.*)', b)
        seg = SEG_RE.findall(b)
        if not orig and not seg:
            summary += ('\n\n' if summary else '') + b; continue
        pre = b.split('**Original:**')[0] if orig else b
        intro = re.split(r'\n\*\*', pre, 1)[0].strip() if not pre.lstrip().startswith('**') else ''
        if intro and not summary: summary = intro
        segid = seg[-1] if seg else ''
        worklines = [l for l in lines if ' · ' in l and segid in l]
        work = worklines[0].split(' · ')[0].strip() if worklines else (heads[0].strip('* ') if heads else '')
        o = (orig.group(1).strip() if orig else '')
        hits.append({'work': work, 'heading': heads[0].strip('* ') if heads else '', 'segid': segid,
                     'is_en': segid.startswith('EN_'), 'tib': to_script(o) if not TIB.search(o) and segid.startswith('BO_') else o,
                     'wylie': to_wylie(o) if TIB.search(o) else o,
                     'rendering': trans.group(1).strip() if trans else '',
                     'url': ('https://dharmamitra.org/db/bo/%s/text?active_segment=%s' % (segid.split(':')[0], segid)) if segid else ''})
    summary = re.sub(r'Please note that I am a specialized assistant.*', '', summary, flags=re.S).strip()
    return {'summary': summary, 'hits': hits}

def parse_segment(txt):
    lines = txt.splitlines()
    head = lines[0].split()
    fn = head[0]; url = next((h for h in head if h.startswith('http')), '')
    toh = ' '.join(h for h in head[1:] if not h.startswith('http'))
    rows = []
    for l in lines[1:]:
        m = re.match(r'^(>>)?\s*([0-9a-z\-]+):\s*(.*)$', l)
        if m: rows.append({'id': m.group(2), 'active': bool(m.group(1)), 'wylie': m.group(3).strip(), 'tib': to_script(m.group(3).strip())})
    return {'file': fn, 'toh': toh, 'url': url, 'rows': rows}

def parse_parallels(txt):
    lines = txt.splitlines()
    out = {'head': lines[0] if lines else '', 'rows': []}
    for l in lines[1:]:
        m = re.match(r'^- score (\d+)\s+len (\d+)\s+(\S+)\s+(Toh \d+)?\s*(.*)$', l.strip())
        if m: out['rows'].append({'score': int(m.group(1)), 'len': int(m.group(2)), 'segid': m.group(3), 'toh': m.group(4) or '', 'title': m.group(5).strip()})
        elif out['rows'] and l.startswith('    '): out['rows'][-1]['snippet'] = l.strip()
    return out

def parse_meta(txt):
    try: raw = json.loads(txt, strict=False).get('raw_metadata', '')
    except Exception:
        m = re.search(r'"raw_metadata":\s*"(.*)', txt, re.S)
        raw = (m.group(1) if m else txt).replace('\\n', '\n').replace('\\"', '"')
    head = re.split(r'\n## AI-generated', raw, 1)[0]
    f = {}
    for m in re.finditer(r'\*\*(.+?):\*\*\s*(.*)', head): f[m.group(1).strip()] = m.group(2).strip()
    t = re.match(r'#\s*(.+)', head); f['heading'] = t.group(1).strip() if t else ''
    return f

def parse_mitra(txt):
    out = {}
    for l in txt.splitlines():
        m = re.match(r'^(%s):\s*(.*)$' % UID, l.strip())
        if m: out[m.group(1)] = m.group(2)
    return out

GLOSS_HEAD = re.compile(r'^=== (.*?) · (.*?) · (\S+) · (GLOSS|QUOTE|NEAR)(?:\s*\(([^)]*gloss)\))?(?:\s*\(\+(\d+) more hits?: ([^)]*)\))?\s*$')

def seg_url(segid):
    if not segid or ':' not in segid: return ''
    lang = segid.split('_', 1)[0].lower()
    return 'https://dharmamitra.org/db/%s/%s/text?active_segment=%s' % (lang if lang in ('bo', 'en', 'sa', 'zh', 'pa') else 'bo', segid.split(':')[0], segid)

def title_script(work):
    """Script form of a Wylie work title as the search prints it ('author — title…', with a truncated tail);
    ACIP titles in capitals and anything that is not plain Wylie stay as they are."""
    parts = [re.sub(r'\s*\(.*$|…|/\s*$', '', x).strip() for x in work.split(' — ')]
    if any(TIB.search(x) or re.search(r'[A-Z]{3}|::|\d', x) for x in parts): return ''
    out = []
    for x in parts:
        if not x: continue
        if not re.match(r"^[a-z'\.\+\s/-]+$", x): return ''
        out.append(to_script(x))
    return ' — '.join(out)

def snippet_script(w):
    """A search snippet is cut mid-syllable at both ends: drop a vowel-initial first fragment, which pyewts
    would render with an a-chung carrier, and let the UI mark the cut with ellipses."""
    toks = w.split(' ')
    if toks and re.match(r'^[aeiou]', toks[0]) and len(toks) > 1: toks = toks[1:]
    return to_script(' '.join(toks))

def parse_gloss(txt):
    """dm.py gloss output (primary search, no re-ranking): a header, then one block per work with the hit,
    its label (GLOSS | QUOTE | NEAR) and, with --context, the DharmaNexus window around it."""
    lines = txt.splitlines()
    out = {'summary': '', 'query': '', 'syllables': 0, 'root': '', 'context_note': '', 'notes': [], 'hits': []}
    m = re.search(r'(\d+) hits? in (\d+) works?', lines[0] if lines else '')
    out['summary'] = lines[0].strip() if lines else ''
    out['n_hits'], out['n_works'] = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    cur = None
    for l in lines[1:]:
        if cur is None:
            m = re.match(r'^query \((\d+) syllables?\):\s*(.*)$', l)
            if m: out['syllables'] = int(m.group(1)); out['query'] = m.group(2).strip(); continue
            m = re.match(r'^root work[^:]*:\s*(.*)$', l)
            if m: out['root'] = m.group(1).strip(); continue
            if l.startswith('(context:'): out['context_note'] = l.strip('() '); continue
            if l.startswith('(') and l.strip(): out['notes'].append(l.strip('() ')); continue
        m = GLOSS_HEAD.match(l)
        if m:
            work, coll, segid, label, kind, nmore, more = m.groups()
            toh = re.search(r'Toh \d+', coll or '')
            cur = {'work': work.strip(), 'work_tib': title_script(work),
                   'collection': coll.strip(), 'toh': toh.group(0) if toh else '', 'segid': segid, 'label': label, 'kind': (kind or '').replace(' gloss', ''),
                   'more': [x.strip() for x in (more or '').split(',') if x.strip()], 'is_en': segid.startswith('EN_'), 'wylie': '', 'tib': '', 'ctx': [], 'note': '', 'url': seg_url(segid)}
            out['hits'].append(cur); continue
        if cur is None: continue
        if not l.strip(): continue
        if l.startswith('[EXISTING ENGLISH'): cur['note'] = l.strip('[] '); continue
        m = re.match(r'^(>>|GL|  ) ([0-9a-z\-]+): (.*)$', l)
        if m:
            mark, sid, t = m.groups()
            cur['ctx'].append({'mark': {'>>': 'hit', 'GL': 'gloss'}.get(mark, ''), 'id': sid, 'wylie': t.strip(), 'tib': to_script(t.strip())}); continue
        m = re.match(r'^\s+… \((\d+) segments?\)', l)
        if m: cur['ctx'].append({'mark': 'gap', 'id': '', 'wylie': '… %s segments' % m.group(1), 'tib': ''}); continue
        if re.match(r'^\s+\(no gloss', l) or l.lstrip().startswith('scaffolding in'): cur['note'] = (cur['note'] + ' ' + l.strip('() ')).strip(); continue
        if l.startswith('(') and not cur['wylie']: out['notes'].append(l.strip('() ')); continue
        if not cur['wylie']: cur['wylie'] = l.strip(); cur['tib'] = snippet_script(l.strip())
        elif l.startswith('('): out['notes'].append(l.strip('() '))
    return out

def parse_cite(txt):
    out = {}
    for l in txt.splitlines():
        m = re.match(r'^(ACADEMIC|READER|REGISTER|CREDITS|NOTE):\s*(.*)$', l.strip())
        if m: out[m.group(1).lower()] = m.group(2).strip()
    return out

def unit_of_file(name):
    m = re.search(r'_(%s)(?:-\d+)?\.txt$' % UID, name)
    return m.group(1) if m else '?'

def file_key(name):
    """dm_segment_KK07_3669 -> 'KK-07'; dm_segment_PARCHIN094_7603 -> 'PARCHIN-094'; dm_segment_4024_64b-23 -> '4024'"""
    base = re.sub(r'^dm_(segment|parallels|meta)_', '', name).rsplit('.', 1)[0]
    stem = base.split('_')[0]
    m = re.match(r'^([A-Za-z]+)(\d+)$', stem)
    return '%s-%s' % (m.group(1), m.group(2)) if m else stem

# ------------------------------------------------------------------ glossary, sources
def parse_tsv(path):
    rows = []
    for i, line in enumerate(open(path, encoding='utf-8')):
        if not line.strip(): continue
        cols = line.rstrip('\n').split('\t')
        if i == 0 and cols[0].lower() in ('wylie', 'chunk'): continue
        rows.append(cols)
    return rows

def confidence_from_notes(u, grounding_field):
    """Provisional grade for runs made before the skill carried a confidence field (notes.md §1b)."""
    open_q = [n for n in u['notes'] if n['tag'] == 'Q' and not n.get('resolved')]
    heavy = [n for n in open_q if re.search(r'head noun|agent|subject of|referent|who (does|kills|desires)|scope', n['text'], re.I)
             and not re.search(r'pronoun choice|surface|same referent|leaves it open', n['text'], re.I)]
    var_flip = any(n['tag'] == 'Var' and re.search(r'flip|changes the sense', n['text'], re.I) for n in u['notes'])
    check_rel = any(n['tag'] == 'Check' and re.search(r'relation|agent|polarity', n['text'], re.I) for n in u['notes'])
    mitra_diff = any(n['tag'] == 'MITRA' and not re.search(r'^agrees', n['text'], re.I) for n in u['notes'])
    if var_flip or len(heavy) >= 2: return 'very low', 'provisional: two or more open forks on agent/relation/head noun, or a sense-flipping variant'
    if heavy or check_rel: return 'low', 'provisional: an open fork on an agent, relation, head noun or referent after grounding'
    if open_q or mitra_diff: return 'medium', 'provisional: an open Q: on a term or nuance, or MITRA differs on a content word with the grammar settling it'
    return 'high', 'provisional: no open Q: on content; grounding found or not needed; MITRA agrees'

WYLIE_RUN = re.compile(r"(?<![A-Za-z])((?:[a-zA-Z'\.\+]+(?:\s|$)){1,8})\s*(?==)")

def tib_norm(t): return re.sub(r'[\s་]+', '', t)

WYLIE_LEAD = re.compile(r"^((?:[a-zA-Z'\.\+]+\s){0,7}[a-zA-Z'\.\+]+)\s*(?::|\(|=|,|;)")
WYLIE_PAREN = re.compile(r"\(((?:[a-zA-Z'\.\+]+\s){0,7}[a-zA-Z'\.\+]+)\)")

def clean_wylie(w):
    w = re.sub(r"\(.*?\)", ' ', w or '')                      # (heading), (resolved) …
    w = re.sub(r"\b(X|…|\.\.\.)\b", ' ', w)
    return re.sub(r'\s+', ' ', w).strip(" /:;,")

def en_key(e):
    e = re.sub(r"[*\"“”‘’']", '', (e or '').lower())
    return re.sub(r'^(the|a|an)\s+', '', re.sub(r'\s+', ' ', e).strip(' .,;:'))

def flagged_phrases(u, tib='', term_pairs=()):
    """Quoted English phrases in Q:/Alt:/Issue: notes that occur in the unit's text -> highlight spans,
    each paired with the Tibetan it renders when that can be found: from a Wylie phrase in the note itself
    (before '=' or ':', or in parentheses), else from a glossary row or a construal TERMS pair whose English
    matches the phrase. The longest Wylie whose script form occurs in the unit wins."""
    text = ' '.join(u['text'])
    flags = []
    norm_tib = tib_norm(tib)
    def locate(w):
        sc = to_script(clean_wylie(w)).strip()
        if not sc or not TIB.search(sc) or tib_norm(sc) not in norm_tib: return ''
        for cand in (sc, sc.rstrip('་'), sc.rstrip('། ').rstrip('་')):
            if cand and tib.find(cand) >= 0: return cand
        return ''
    for i, n in enumerate(u['notes']):
        if n['tag'] not in ('Q', 'Alt', 'Issue', 'Check', 'Var', 'Comm'): continue
        wy_cands = {m.group(1).strip() for m in WYLIE_RUN.finditer(n['text']) if len(m.group(1).strip()) >= 4}
        m = WYLIE_LEAD.match(n['text'])
        if m and len(m.group(1)) >= 4: wy_cands.add(m.group(1))
        wy_cands |= {m.group(1) for m in WYLIE_PAREN.finditer(n['text']) if len(m.group(1)) >= 4}
        for ph in re.findall(r'"([^"]{3,80})"', n['text']):
            ph2 = ph.strip(' ,.;:')
            if not ph2 or ph2 not in text or any(f['phrase'] == ph2 for f in flags): continue
            f = {'phrase': ph2, 'note': i, 'tag': n['tag'], 'tib': ''}
            cands = sorted(wy_cands, key=len, reverse=True)
            key = en_key(ph2)
            if key:
                for wy, en in term_pairs:                   # glossary rows and TERMS pairs whose English matches the phrase
                    ek = en_key(en)
                    if ek and len(ek) >= 3 and (ek == key or (len(ek) >= 5 and ek in key) or (len(key) >= 5 and key in ek)): cands.append(wy)
            best = ''
            for w in cands:
                sc = locate(w)
                if sc and len(sc) > len(best): best = sc
            f['tib'] = best
            flags.append(f)
    return flags

PARTICLES = {'las', 'la', 'nas', 'gi', 'kyi', 'gyi', "'i", 'yi', 'gis', 'kyis', 'gyis', 'yis', 'dang', 'ni', 'de', 'du', 'tu', 'ru', 'su', 'na',
             'ste', 'te', 'pa', 'ba', 'pas', 'bas', 'ma', 'mi', 'yang', 'kyang', "'ang", 'par', 'bar', 'zhing', 'cing', 'shing', 'zhes', 'ces', 'zhe', 'ce', 'ltar', 'bzhin', 'phyir', 'rnams', 'dag', 'gang', 'ci', 'ji'}

def term_in_unit(wylie, unit_wylie):
    """Does the glossary term occur in the unit? Whole syllables only, the first of alternative forms ('a / b'),
    annotations like '(heading)' removed; a pattern term (… or X) never binds, and a one-syllable term that is
    also a grammatical particle (las, la, nas …) is left out since it cannot be told from the particle."""
    w = re.sub(r"\s*\(.*?\)\s*", ' ', wylie or '').split(' / ')[0].strip(" /")
    if not w or '…' in w or re.search(r'(^|\s)X(\s|$)', w) or '...' in w: return False
    if ' ' not in w and w in PARTICLES: return False
    return re.search(r"(?<![a-zA-Z'\.\+])" + re.escape(w) + r"(?![a-zA-Z'\.\+])", unit_wylie or '') is not None

CLUTTER = re.compile(r'^(house style|anglicized|lowercase|no diacritics|capitalized|per modes\.md|decision; house style to confirm)[^;]*$', re.I)

def term_alternatives(note):
    """Alternatives recorded in a glossary note: Alt: …, Pass 1 '…', not '…', "…" / "…"."""
    alts = []
    for m in re.finditer(r"(?:Alt:|alt\.|Pass 1|not|rather than)\s*[\"'‘“]([^\"'’”]{2,60})[\"'’”]", note): alts.append(m.group(1).strip())
    for m in re.finditer(r"Alt:\s*([^;\"']{2,60})", note):
        a = m.group(1).strip(' .')
        if a and a not in alts and not a.startswith(("'", '"')): alts.append(a)
    for m in re.finditer(r"(?<![\w'])\"([^\"]{2,50})\"\s*/\s*\"([^\"]{2,50})\"", note): alts += [m.group(1), m.group(2)]
    return [a for a in dict.fromkeys(alts) if a]

def unit_tags(hf, notes, titles):
    """Positive tags only: what the unit HAS (a citation, grounding, a variant, a prior translation), never what it lacks."""
    tags = []
    form = (hf.get('form') or '').strip()
    if form:
        kind = 'Verse' if re.search(r'verse', form, re.I) and not re.match(r'prose', form, re.I) else 'Prose'
        tags.append({'kind': 'form', 'label': kind, 'detail': form})
    reg = (hf.get('register') or '').strip()
    if reg:
        lab = re.sub(r'^framing;\s*', '', reg); lab = re.sub(r'\s*\(.*$', '', lab).strip()
        tags.append({'kind': 'register', 'label': lab[0].upper() + lab[1:], 'detail': reg})
    src = (hf.get('source') or '').strip()
    if src and not re.search(r'not a citation|source not located', src, re.I):
        title = next((t['english'] for t in titles if t['english'] and t['english'] in src), '')
        toh = re.search(r'Toh\s*\d+', src)
        lab = 'Citation' + (': ' + title if title else '') + ((' (' + toh.group(0) + ')') if toh and not title else '')
        tags.append({'kind': 'citation', 'label': lab, 'detail': src})
    elif src and re.search(r'source not located', src, re.I):
        tags.append({'kind': 'citation-open', 'label': 'Citation: source not located', 'detail': src})
    gr = (hf.get('grounding') or '').strip()
    if gr and re.search(r'followed|gloss', gr, re.I) and not re.search(r'^(none|not queried)', gr, re.I):
        names = re.findall(r"([A-Z][\w\u00C0-\u024F]+(?: [A-Z][\w\u00C0-\u024F]+)*)'s\b", gr)
        tags.append({'kind': 'grounded', 'label': 'Grounded' + (': ' + ', '.join(names) if names else ''), 'detail': gr})
    if any(n['tag'] == 'Var' for n in notes):
        tags.append({'kind': 'variant', 'label': 'Variant reading', 'detail': ' '.join(n['text'] for n in notes if n['tag'] == 'Var')})
    pr = (hf.get('prior') or '').strip()
    if pr and not re.match(r'none', pr, re.I):
        tags.append({'kind': 'prior', 'label': 'Prior translation ' + pr.split('(')[0].strip(), 'detail': pr})
    return tags

def outline(units, tib_units=None):
    """Two levels. When the page file marks headings (hint 'heading'), the headings are the sections;
    otherwise a section is the register's head word and its items the full register labels."""
    tib_units = tib_units or {}
    if any((tib_units.get(u['id'], {}).get('hint') or '').startswith('heading') for u in units):
        secs = []
        for u in units:
            h = tib_units.get(u['id'], {})
            if (h.get('hint') or '').startswith('heading'):
                label = ' '.join(u['text']).strip() or h.get('tib', '')[:40]
                label = re.sub(r'\*+', '', label)
                secs.append({'label': label, 'heading': True, 'items': [{'label': label, 'units': [u['id']]}], 'units': [u['id']]})
            elif secs: secs[-1]['items'][0]['units'].append(u['id']); secs[-1]['units'].append(u['id'])
            else: secs.append({'label': 'Opening', 'items': [{'label': 'Opening', 'units': [u['id']]}], 'units': [u['id']]})
        return secs
    secs = []
    for u in units:
        if u.get('pending'):
            if secs and secs[-1]['label'] == 'Not yet translated': secs[-1]['items'][0]['units'].append(u['id'])
            else: secs.append({'label': 'Not yet translated', 'items': [{'label': 'Not yet translated', 'units': [u['id']]}]})
            continue
        reg = u['header_fields'].get('register') or u['header_fields'].get('form') or ''
        label = re.sub(r'^framing;\s*', '', reg).strip() or 'untitled'
        label = re.sub(r'^(verse|prose)\b.*?·\s*', '', label)
        head = label.split('(')[0].strip().rstrip(';').strip()
        head = head[0].upper() + head[1:] if head else 'Untitled'
        item = label[0].upper() + label[1:]
        if secs and secs[-1]['label'] == head: sec = secs[-1]
        else: sec = {'label': head, 'items': []}; secs.append(sec)
        if sec['items'] and sec['items'][-1]['label'] == item: sec['items'][-1]['units'].append(u['id'])
        else: sec['items'].append({'label': item, 'units': [u['id']]})
    byid = {u['id']: u for u in units}
    for sec in secs:
        for it in sec['items']:
            for i in it['units']:
                src = byid[i]['header_fields'].get('source', '')
                if src and 'not a citation' not in src: it['source'] = src; break
        sec['units'] = [i for it in sec['items'] for i in it['units']]
    return secs

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('run_dir'); ap.add_argument('--units', required=True); ap.add_argument('--work', required=True)
    ap.add_argument('-o', '--out', default='demo/data.json'); ap.add_argument('--title', default='')
    ap.add_argument('--brief', default='', help='a short brief line shown in the top bar')
    a = ap.parse_args()
    rd = a.run_dir
    tib_units, page_meta = parse_units(a.units)
    fpath = os.path.join(rd, 'final.md')
    final_units, intro = parse_final(open(fpath, encoding='utf-8').read()) if os.path.exists(fpath) else ([], '')
    cpath = os.path.join(rd, a.work + '.construal.md')
    construal, grounding, check = parse_construal(open(cpath, encoding='utf-8').read()) if os.path.exists(cpath) else ({}, {}, [])
    gpath = os.path.join(rd, a.work + '.glossary.tsv')
    glossary, titles = [], []
    if os.path.exists(gpath):
        for cols in parse_tsv(gpath):
            if cols[0] == 'TITLE': titles.append({'english': cols[1] if len(cols) > 1 else '', 'wylie': cols[2] if len(cols) > 2 else '', 'iast': cols[3] if len(cols) > 3 else '', 'locator': cols[4] if len(cols) > 4 else ''})
            else: glossary.append({'wylie': cols[0], 'english': cols[1] if len(cols) > 1 else '', 'note': cols[2] if len(cols) > 2 else ''})
    spath = os.path.join(rd, a.work + '.sources.tsv')
    sources = [dict(zip(['chunk', 'unit_id', 'orig_fn', 'opening_words', 'work_and_locator'], c)) for c in parse_tsv(spath)] if os.path.exists(spath) else []
    mitra = {}
    for p in glob.glob(os.path.join(rd, 'dm_mitra*.txt')) + glob.glob(os.path.join(rd, 'dm_translate*.txt')):
        mitra.update(parse_mitra(open(p, encoding='utf-8').read()))
    explores, segments, parallels, metas, identifies, glosses, cites = {}, [], [], {}, {}, {}, {}
    for p in sorted(glob.glob(os.path.join(rd, 'dm_*.txt'))):
        name = os.path.basename(p); txt = open(p, encoding='utf-8').read()
        if name.startswith('dm_explore'):
            explores.setdefault(unit_of_file(name), []).append(dict(parse_explore(txt), file=name))
        elif name.startswith('dm_gloss'):
            glosses.setdefault(unit_of_file(name), []).append(dict(parse_gloss(txt), file=name))
        elif name.startswith('dm_cite'):
            cites.setdefault(unit_of_file(name), []).append(dict(parse_cite(txt), file=name))
        elif name.startswith('dm_identify'):
            identifies.setdefault(unit_of_file(name), []).append('— %s —\n%s' % (name, txt.strip()))
        elif name.startswith('dm_segment'):
            segments.append(dict(parse_segment(txt), key=file_key(name), file=name))
        elif name.startswith('dm_parallels'):
            parallels.append(dict(parse_parallels(txt), key=file_key(name), file=name))
        elif name.startswith('dm_meta'):
            metas[file_key(name)] = dict(parse_meta(txt), file=name)
    # attach segments / parallels / metas to units by key mentions in their notes, header or grounding lines
    def mentions(u, key):
        hay = u['header'] + ' ' + ' '.join(n['text'] for n in u['notes'])
        k2 = key.replace('-', '')
        return key in hay or k2 in hay.replace('-', '') or (key.isdigit() and ('Toh ' + key) in hay)
    for s in segments:
        meta = next((m for k, m in metas.items() if s['file'].replace('dm_segment_', '').startswith(k.replace('-', ''))), None)
        if meta: s['title'] = meta.get('heading', ''); s['author'] = meta.get('Author (catalog)') or meta.get('Author (colophon)', ''); s['collection'] = meta.get('Collection', '')
    units = []
    done_ids = {u['id'] for u in final_units}
    for uid in sorted(tib_units, key=nat):
        if uid not in done_ids:
            final_units.append({'id': uid, 'header': '', 'header_fields': {'raw': ''}, 'text': [], 'footnotes': [], 'notes': [], 'pending': True})
    final_units.sort(key=lambda u: nat(u['id']))
    for u in final_units:
        t = tib_units.get(u['id'], {})
        tib = t.get('tib', '')
        hf = u['header_fields']
        conf = hf.get('confidence')
        conf_note = next((n['text'] for n in u['notes'] if n['tag'] == 'Conf'), '')
        provisional = False
        if not conf:
            conf, conf_note = confidence_from_notes(u, hf.get('grounding', '')); provisional = True
        wy = to_wylie(tib) if TIB.search(tib) else tib
        terms = [dict(g, alts=term_alternatives(g.get('note', '')), clutter=bool(CLUTTER.match((g.get('note') or '').strip())))
                 for g in glossary if term_in_unit(g['wylie'], wy)]
        if u.get('pending'):
            t = tib_units.get(u['id'], {}); tib = t.get('tib', ''); wy = to_wylie(tib) if TIB.search(tib) else tib
            units.append({'id': u['id'], 'hint': t.get('hint', ''), 'tib': to_script(tib) if not TIB.search(tib) else tib, 'wylie': wy, 'pending': True,
                          'tags': [], 'open_q': 0, 'header': '', 'fields': {}, 'confidence': '', 'confidence_reason': '', 'confidence_provisional': False,
                          'text': [], 'footnotes': [], 'notes': [], 'flags': [], 'construal': [], 'grounding': [], 'mitra': mitra.get(u['id'], ''),
                          'explore': [], 'gloss': [], 'cite': [], 'identify': '', 'identify_summary': '', 'segments': [], 'parallels': [], 'terms': []})
            continue
        tags = unit_tags(hf, u['notes'], titles)
        open_q = sum(1 for n in u['notes'] if n['tag'] == 'Q' and not n.get('resolved'))
        term_pairs = [(g['wylie'], g['english']) for g in glossary if g['wylie'] and g['english']]
        for c in construal.get(u['id'], []):
            if c['key'] == 'TERMS':
                for part in re.split(r';\s+|\s·\s', c['text']):
                    mm = re.match(r'^(.{2,60}?)\s=\s(.{2,80}?)\s*$', part.strip())
                    if mm: term_pairs.append((mm.group(1), mm.group(2)))
        idents = identifies.get(u['id'], [])
        ident_summary = next((l.strip() for t in idents for l in t.splitlines() if l.startswith('VERBATIM MATCH')), '')
        units.append({
            'id': u['id'], 'hint': t.get('hint', ''), 'tib': to_script(tib) if not TIB.search(tib) else tib, 'wylie': wy,
            'tags': tags, 'open_q': open_q,
            'header': u['header'], 'fields': hf, 'confidence': conf, 'confidence_reason': conf_note, 'confidence_provisional': provisional,
            'text': u['text'], 'footnotes': u['footnotes'], 'notes': u['notes'], 'flags': flagged_phrases(u, to_script(tib) if not TIB.search(tib) else tib, term_pairs),
            'construal': construal.get(u['id'], []), 'grounding': grounding.get(u['id'], []),
            'mitra': mitra.get(u['id'], ''), 'explore': explores.get(u['id'], []), 'gloss': glosses.get(u['id'], []), 'cite': cites.get(u['id'], []),
            'identify': '\n\n'.join(idents), 'identify_summary': ident_summary,
            'segments': [s for s in segments if mentions(u, s['key'])],
            'parallels': [p for p in parallels if mentions(u, p['key'])],
            'terms': terms,
        })
    works = []
    for k, m in metas.items():
        works.append({'key': k, 'title': m.get('heading', ''), 'title_wylie': m.get('Title (Wylie, catalog)') or m.get('Title (Wylie)', ''),
                      'author': m.get('Author (catalog)') or m.get('Author (colophon)', ''), 'collection': m.get('Collection', ''),
                      'genre': m.get('Genre', ''), 'source': m.get('Source', ''), 'bdrc': m.get('BDRC', ''), 'file': m.get('file', ''),
                      'url': 'https://dharmamitra.org/db/bo/%s/text' % (m.get('ID') or '')})
    # works met through the primary search: one row per work, with where it was hit and how it was labelled
    seen = {}
    for uid, calls in glosses.items():
        for call in calls:
            for h in call['hits']:
                if h['is_en']: continue
                w = seen.setdefault(h['work'], {'key': h['segid'].split(':')[0], 'title': h['work_tib'] or h['work'], 'title_wylie': h['work'] if h['work_tib'] else '',
                                                 'author': '', 'collection': h['collection'], 'genre': '', 'source': '', 'bdrc': '', 'file': '', 'url': seg_url(h['segid']).split('?')[0],
                                                 'from_search': True, 'labels': {}, 'units': []})
                w['labels'][h['label']] = w['labels'].get(h['label'], 0) + 1 + len(h['more'])
                if uid not in w['units']: w['units'].append(uid)
    known = {w['title'] for w in works} | {w['title_wylie'] for w in works}
    for t, w in seen.items():
        if t not in known: works.append(w)
    works.sort(key=lambda w: (0 if not w.get('from_search') else 1, -(w.get('labels', {}).get('GLOSS', 0)), -(w.get('labels', {}).get('QUOTE', 0)), w['title']))
    runlog = open(os.path.join(rd, 'runlog.md'), encoding='utf-8').read() if os.path.exists(os.path.join(rd, 'runlog.md')) else ''
    data = {
        'title': a.title or page_meta.get('title', a.work), 'work': page_meta.get('work', ''), 'work_name': a.work, 'brief': a.brief, 'intro': intro,
        'build': {'python': sys.executable, 'run_dir': os.path.abspath(rd), 'units': os.path.abspath(a.units), 'work': a.work,
                  'title': a.title, 'brief': a.brief, 'out': os.path.abspath(a.out), 'final_mtime': os.path.getmtime(fpath) if os.path.exists(fpath) else 0},
        'page_source': page_meta.get('source', ''), 'run_dir': os.path.abspath(rd), 'units_file': os.path.abspath(a.units),
        'units': units, 'outline': outline(final_units, tib_units), 'glossary': glossary, 'titles': titles, 'sources': sources,
        'works': works, 'check': check, 'runlog': runlog,
        'pending': sum(1 for u in units if u.get('pending')),
        'counts': {'units': len(units), 'glossary': len(glossary), 'sources': len(sources), 'explore_calls': sum(len(v) for v in explores.values()),
                   'gloss_calls': sum(len(v) for v in glosses.values()),
                   'segments': len(segments), 'footnotes': sum(len(u['footnotes']) for u in units), 'notes': sum(len(u['notes']) for u in units)},
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(data, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote %s: %d units, %d glossary rows, %d sources, %d gloss files, %d explore files, %d segment files, pyewts=%s' % (
        a.out, len(units), len(glossary), len(sources), data['counts']['gloss_calls'], data['counts']['explore_calls'], len(segments), bool(_C)))

if __name__ == '__main__':
    main()
