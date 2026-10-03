#!/usr/bin/env python3
"""
dm.py -- Dharmamitra / DharmaNexus client for the analysis and citation passes.

Public, keyless JSON endpoints on https://dharmamitra.org (documented at /api-search/docs and
/api-db/docs, and sanctioned by Dharmamitra's own Claude Code starter pack). Use them for
personal research at a polite rate; do not build them into a hosted product (their ToS).

COMMANDS
  dm.py identify "<passage>" [--exclude TOH]     find the passage in the canon: groups the hits by
                                                  work, gives Derge/Toh numbers, variant readings
                                                  and the commentaries that quote it   (~1500 chars)
  dm.py search   "<query>" [--lang bo] [--n 15]   raw semantic search, one line per hit
  dm.py segment  <segmentnr> [--context] [--window N]   one canonical segment (+ N segments each side, default 6;
                                                  use --window 10-15 to reach a quotation inside a commentary)
  dm.py parallels <segmentnr> [...]               precomputed parallels of a segment (variants)
  dm.py translate "<tibetan>" [--style ...] [--context ...]   MITRA cat-translate (second opinion)
  dm.py translate --file <units.md> [--style ...]        the same for every `Uxx` line of a page file
  dm.py explore  "<query>"                        the Explore page's Gemini summary (slow, 10-20 s)
  dm.py meta     <filename>                       a work's metadata (titles, Toh, translators)

All commands print compact text meant for a model's context. Add --json for the raw response.
Network required. Timeouts are generous; the cat-translate upstream caps at 100 s.
"""
import argparse, json, re, sys, time, urllib.request, urllib.error, urllib.parse

BASE = "https://dharmamitra.org"
UA = "tibetan-translate-skill/1.0 (personal research)"

def _req(url, body=None, timeout=120, accept="application/json"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Accept": accept, "User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 * (attempt + 1)); continue
            sys.exit(f"dm.py: HTTP {e.code} from {url}: {e.read()[:300].decode('utf8','replace')}")
        except (urllib.error.URLError, OSError) as e:
            if attempt < 2:
                time.sleep(2); continue
            sys.exit(f"dm.py: network error: {e}")

def post(path, body, timeout=120):
    return json.loads(_req(BASE + path, body, timeout))

def get(path, timeout=60):
    return json.loads(_req(BASE + path, None, timeout))

# --------------------------------------------------------------------------- helpers
def toh_of(segmentnr):
    """BO_K12_D0381:158a-16 -> ('Toh 381', 'K'), BO_T02_D1490:... -> ('Toh 1490','T')"""
    m = re.match(r'BO_([KT])\d+_D(\d+)', segmentnr)
    if m:
        return f"Toh {int(m.group(2))}", m.group(1)
    return None, None

_conv = None
WYLIE = True   # Tibetan script costs ~3x the tokens of Wylie; convert output unless --script
def wy(t):
    """Convert Tibetan-script runs in t to Wylie (if pyewts is available and WYLIE is on)."""
    global _conv
    if not WYLIE or not re.search(r'[ༀ-࿿]', t or ''):
        return t or ''
    if _conv is None:
        try:
            import pyewts; _conv = pyewts.pyewts()
        except ImportError:
            _conv = False
    if not _conv:
        return t
    out = re.sub(r'[ༀ-࿿][ༀ-࿿\s]*', lambda m: ' ' + _conv.toWylie(m.group(0)).strip() + ' ', t)
    out = out.replace('_', ' ')
    out = re.sub(r'/\s+/', '//', out)
    return re.sub(r'\s+', ' ', out).strip()

def short_title(t, n=70):
    t = re.sub(r'\s+', ' ', wy(t or '')).strip()
    return t if len(t) <= n else t[:n - 1] + '…'

def clean_text(t):
    return re.sub(r'\s+', ' ', wy((t or '').replace('\n', ' '))).strip()

def search_raw(query, lang="bo", n=30, search_type="semantic", filters=None):
    body = {"search_input": query, "input_encoding": "auto", "search_type": search_type,
            "filter_source_language": lang, "filter_target_language": "all",
            "source_filters": filters or {"include_collections": None, "include_categories": None, "include_files": None},
            "do_ranking": False, "max_depth": n, "expand_parallels": False}
    return post("/api-search/primary/", body).get("results", [])

def collection_of(segmentnr):
    m = re.match(r'BO_([A-Z]+)\d*_', segmentnr)
    c = m.group(1) if m else '?'
    return {'K': 'Kangyur', 'T': 'Tengyur', 'S': 'Sungbum/series', 'TSD': 'Tsadra series', 'LH': 'Lotsawa House',
            'NG': 'Nyingma', 'NK': 'Nyingma Kama', 'ACIP': 'ACIP sungbum', 'MONLAM': 'Monlam'}.get(c, c)

# --------------------------------------------------------------------------- commands
def cmd_identify(a):
    hits = search_raw(a.query, lang="bo", n=a.n)
    if getattr(a, 'exclude', None):
        ex = {x.strip().lstrip('Toh').strip() for x in a.exclude.split(',')}
        before = len(hits)
        hits = [h for h in hits if str(toh_of(h['segmentnr'])[0]) not in ex]
        print(f"(excluded {before - len(hits)} hit(s) from Toh {', '.join(sorted(ex))}: the text being translated)")
    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=1)); return
    if not hits:
        print("no hits"); return
    # group by source file
    groups = {}
    for h in hits:
        groups.setdefault(h['source'], []).append(h)
    # order: Kangyur/Tengyur first (canonical sources), then others by number of hits
    def rank(item):
        src, hs = item
        toh, kt = toh_of(hs[0]['segmentnr'])
        return (-max(h.get('_run', 0) for h in hs), 0 if kt == 'K' else 1 if kt == 'T' else 2, -len(hs))
    # exact-match test: longest run of query syllables found verbatim in a hit (in Wylie)
    def syls(t):
        t = wy(t) if re.search(r'[\u0F00-\u0FFF]', t) else t
        return [x for x in re.split(r"[\s/|]+", t.lower().replace('_', ' ')) if x and x not in ('/', '//')]
    q = syls(a.query)
    def run_len(h):
        hs = syls(h.get('text', ''))
        best = 0
        for i in range(len(q)):
            for j in range(len(hs)):
                k = 0
                while i + k < len(q) and j + k < len(hs) and q[i + k] == hs[j + k]:
                    k += 1
                best = max(best, k)
        return best
    for h in hits:
        h['_run'] = run_len(h)
    longest = max((h['_run'] for h in hits), default=0)
    thresh = max(4, len(q) // 2)
    # verbatim verdict is computed separately for canonical (Kangyur BO_K / Tengyur BO_T) and other hits,
    # so a non-canonical copy of the citing text cannot pass for the source
    canon = [h for h in hits if toh_of(h['segmentnr'])[1] in ('K', 'T')]
    noncanon = [h for h in hits if toh_of(h['segmentnr'])[1] not in ('K', 'T')]
    canon_best = max(canon, key=lambda h: h['_run'], default=None)
    canon_run = canon_best['_run'] if canon_best else 0
    canon_exact = [h for h in canon if h['_run'] >= thresh]
    non_exact = [h for h in noncanon if h['_run'] >= thresh]
    non_run = max((h['_run'] for h in noncanon), default=0)
    print(f"query ({len(q)} syllables): {wy(a.query)}")
    print(f"{len(hits)} hits in {len(groups)} works (semantic search, Tibetan sources)")
    if canon_exact:
        toh, kt = toh_of(canon_best['segmentnr'])
        tag = f"{toh} ({'Kangyur' if kt == 'K' else 'Tengyur'})"
        print(f"VERBATIM MATCH: yes, canonical \u2014 {len(canon_exact)} Kangyur/Tengyur hit(s) share {canon_run} consecutive "
              f"syllables; best: {short_title(canon_best['title'])} [{tag}] {canon_best['segmentnr']}\n")
    elif non_exact:
        print(f"VERBATIM MATCH: only in non-canonical works \u2014 {len(non_exact)} hit(s) share {non_run} syllables "
              f"(these may be the citing text itself or later works quoting it); canonical best run is {canon_run} "
              f"syllable(s): SOURCE NOT LOCATED in Kangyur/Tengyur as quoted (a loose quotation, a master's saying, "
              f"or a variant)\n")
    else:
        print(f"VERBATIM MATCH: NO \u2014 longest shared run is {longest} syllable(s). The passage is not in the index as "
              f"quoted (a non-canonical saying, a paraphrase, or a variant wording). The hits below are semantic "
              f"neighbours only; do not cite them as the source.\n")
    # hits with a verbatim run come first inside each group
    for hs in groups.values():
        hs.sort(key=lambda h: -h['_run'])
    print("CANONICAL / SOURCE CANDIDATES")
    shown = 0
    for src, hs in sorted(groups.items(), key=rank):
        h = hs[0]
        toh, kt = toh_of(h['segmentnr'])
        tag = f"{toh} ({'Kangyur' if kt=='K' else 'Tengyur'})" if toh else collection_of(h['segmentnr'])
        if shown >= a.n_works:
            break
        if kt in ('K', 'T'):
            print(f"- {short_title(h['title'])}  [{tag}]  {h['segmentnr']}  ({len(hs)} hit{'s' if len(hs) > 1 else ''}; verbatim run {h['_run']})")
            print(f"    {clean_text(h['text'])[:a.snippet]}")
            shown += 1
    if shown == 0:
        print("  (none in Kangyur/Tengyur)")
    others = [(src, hs) for src, hs in sorted(groups.items(), key=rank) if toh_of(hs[0]['segmentnr'])[1] not in ('K', 'T')]
    print(f"\nQUOTED IN / COMMENTED ON BY ({len(others)} other works; first {min(len(others), a.n_others)}):")
    for src, hs in others[:a.n_others]:
        h = hs[0]
        print(f"- {short_title(h['title'], 55)}  {h['segmentnr']}  [{collection_of(h['segmentnr'])}; run {h['_run']}]")
    print("\nNext: dm.py parallels <segmentnr> for variant readings; dm.py segment <segmentnr> --context "
          "for the surrounding text (e.g. a commentary's gloss of the line).")

def cmd_search(a):
    hits = search_raw(a.query, lang=a.lang, n=a.n, search_type=a.type)
    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=1)); return
    for h in hits:
        toh, kt = toh_of(h['segmentnr'])
        print(f"{h['segmentnr']:<34} {(toh or collection_of(h['segmentnr'])):<14} {short_title(h['title'],50)} | {clean_text(h['text'])[:a.snippet]}")

FILTERS = {"par_length": 30, "score": 0, "languages": ["all"], "include_files": [], "exclude_files": [],
           "include_categories": [], "exclude_categories": [], "include_collections": [], "exclude_collections": []}

def cmd_segment(a):
    """Print a segment with its neighbours from the reading-room text view (api-db)."""
    fn = a.segmentnr.split(':')[0]
    r = post("/api-db/text-view/text-parallels/", {"filename": fn, "folio": "", "active_segment": a.segmentnr,
                                                   "include_matches": False, "page": 0, "page_size": 100, "filters": FILTERS})
    items = r.get('items', [])
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return
    idx = next((i for i, it in enumerate(items) if it.get('segnr') == a.segmentnr), None)
    if idx is None:
        print(f"segment {a.segmentnr} not found in {fn} (page {r.get('page')} of {r.get('total_pages')})"); return
    w = a.window if (a.context or a.window_given) else 0
    lo, hi = max(0, idx - w), min(len(items), idx + w + 1)
    print(f"{fn}  {toh_of(a.segmentnr)[0] or ''}  https://dharmamitra.org/db/bo/{fn}/text?active_segment={a.segmentnr}")
    for it in items[lo:hi]:
        mark = '>>' if it['segnr'] == a.segmentnr else '  '
        print(f"{mark} {it['segnr'].split(':')[1]}: {clean_text(' '.join(s.get('text', '') for s in it.get('segtext', [])))}")

def cmd_parallels(a):
    r = post("/api-db/matches/", {"segment_nrs": a.segmentnrs})
    ms = r.get('matches', [])
    if a.json:
        print(json.dumps(ms, ensure_ascii=False, indent=1)); return
    print(f"{len(ms)} precomputed parallels for {', '.join(a.segmentnrs)}")
    ms.sort(key=lambda m: -m.get('score', 0))
    for m in ms[:a.n]:
        par = m['par_segnr'][0] if isinstance(m.get('par_segnr'), list) and m['par_segnr'] else m.get('par_segnr')
        toh, kt = toh_of(par or '')
        name = (m.get('par_full_names') or {}).get('display_name') or (m.get('par_full_names') or {}).get('text_name') or ''
        print(f"- score {m.get('score',0):.0f}  len {m.get('par_length')}  {par}  {toh or ''}  {short_title(name, 55)}")
        pt = clean_text(m.get('par_text', ''))
        if pt and not re.match(r'^[a-zA-Z+ /]+$', pt[:40]):
            print(f"    {pt[:a.snippet]}")

def _translate_one(text, a):
    body = {"input_tibetan": text, "input_chinese": "", "input_pali": "", "input_sanskrit": "",
            "context": a.context or "", "focus": "tibetan", "target_language": a.lang,
            "style_instruction": a.style}
    r = post("/api-search/cat-translate/v1/translate", body, timeout=150)
    return r.get('translation', json.dumps(r))

def cmd_translate(a):
    """One unit, or a whole page: --file <units.md> translates every line that starts with an id
    like `U07` (an optional parenthesis after the id is skipped) and prints `U07: <translation>`,
    one request at a time, so the cross-check of a page is one call (~0.2k tokens per unit)."""
    if a.file:
        import time
        for line in open(a.file, encoding='utf8'):
            m = re.match(r'^(U\d{2,3})\s+(?:\([^)]*\)\s*)?(.+)$', line.strip())
            if not m:
                continue
            uid, tib = m.group(1), m.group(2).strip()
            out = None
            for attempt in range(3):
                try:
                    out = _translate_one(tib, a).replace('\n', ' ')
                    break
                except Exception as e:  # the endpoint allows ~10 calls a minute: wait and retry on 429
                    if '429' in str(e) and attempt < 2:
                        time.sleep(65)
                        continue
                    out = f'(error: {e})'
            print(f'{uid}: {out}', flush=True)
            time.sleep(6.5)   # stay under the 10-per-minute limit
        return
    print(_translate_one(a.text, a))

def cmd_explore(a):
    body = {"search_input": a.query, "input_encoding": "auto", "target_lang": "english", "search_type": "semantic",
            "filter_source_language": "bo", "filter_target_language": "auto",
            "source_filters": {"include_collections": None, "include_categories": None, "include_files": None},
            "do_ranking": True, "max_depth": 50, "expand_parallels": False,
            "messages": [{"parts": [{"type": "text", "text": a.query}], "id": "q1", "role": "user"}]}
    raw = _req(BASE + "/bff/api/search/explore", body, timeout=180, accept="text/event-stream").decode('utf8', 'replace')
    text = []
    for line in raw.splitlines():
        if line.startswith('data: '):
            try:
                j = json.loads(line[6:])
            except ValueError:
                continue
            if j.get('type') == 'text-delta':
                text.append(j.get('delta', ''))
    out = ''.join(text)
    out = re.sub(r'\[View segment\]\([^)]*\)', '', out)
    print(out.strip())

def cmd_meta(a):
    r = get(f"/api-db/utils/raw-metadata/?filename={urllib.parse.quote(a.filename)}")
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return
    s = json.dumps(r, ensure_ascii=False)
    print(s[:3000])

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--script', action='store_true', help='keep Tibetan script in output (default: Wylie, 3x cheaper in tokens)')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('identify'); p.add_argument('query'); p.add_argument('--n', type=int, default=30); p.add_argument('--n-works', type=int, default=5); p.add_argument('--n-others', type=int, default=8); p.add_argument('--snippet', type=int, default=140); p.add_argument('--exclude', default='', help='Toh number(s) of the text you are translating, e.g. 1189, so its own copy of a quotation is not reported as the source')
    p = sub.add_parser('search'); p.add_argument('query'); p.add_argument('--lang', default='bo'); p.add_argument('--n', type=int, default=15); p.add_argument('--type', default='semantic', choices=['semantic', 'regular', 'semantic_only']); p.add_argument('--snippet', type=int, default=90)
    p = sub.add_parser('segment'); p.add_argument('segmentnr'); p.add_argument('--context', action='store_true'); p.add_argument('--window', type=int, default=None, help='segments of context each side with --context (default 6); use --window 10-15 to reach a quotation inside a commentary passage')
    p = sub.add_parser('parallels'); p.add_argument('segmentnrs', nargs='+'); p.add_argument('--n', type=int, default=15); p.add_argument('--snippet', type=int, default=200)
    p = sub.add_parser('translate'); p.add_argument('text', nargs='?', default=''); p.add_argument('--file', default='', help='a page file: translate every line starting with Uxx'); p.add_argument('--style', default='balanced'); p.add_argument('--context', default=''); p.add_argument('--lang', default='english')
    p = sub.add_parser('explore'); p.add_argument('query')
    p = sub.add_parser('meta'); p.add_argument('filename')
    a = ap.parse_args()
    global WYLIE
    WYLIE = not a.script
    if getattr(a, 'cmd', None) == 'segment':
        a.window_given = a.window is not None
        if a.window is None:
            a.window = 6
    {'identify': cmd_identify, 'search': cmd_search, 'segment': cmd_segment, 'parallels': cmd_parallels,
     'translate': cmd_translate, 'explore': cmd_explore, 'meta': cmd_meta}[a.cmd](a)

if __name__ == '__main__':
    main()
