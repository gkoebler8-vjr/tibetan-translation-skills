#!/usr/bin/env python3
"""
tibdict.py -- offline Tibetan dictionary index + word segmentation for the analysis pass.

Builds one SQLite index (default ~/.tibdict/tibdict.sqlite) from:
  * the MITRA Tibetan Lexicon (StarDict, Dharmamitra 2026): senses, English/Sanskrit renderings
    attested in parallel texts, POS profile, verb paradigms with Hackett syntax, and cited
    example passages (read on demand with --examples)
  * the user's GoldenDict folder (StarDict): Hopkins, 84000 glossary, Rangjung Yeshe, Monlam
    2007, Valby, Penatsang, Duff, Das, Verbs (VB), and Steinert-format TSVs (Hackett-Def,
    Mahavyutpatti, Berzin, Dan Martin ...)
  * optionally (--public DIR) the freely redistributable dictionaries of Christian Steinert's open-source
    project (github.com/christiansteinert/tibetan-dictionary), fetched with `fetch-public`: for users
    without a GoldenDict folder

Then annotates a passage: segments it (botok if installed, else dictionary max-match with a
particle penalty), looks every word up (full form, lemma, components), and prints a compact
report sized for a model's context (default --budget 9000 chars; detail is shed step by step to fit, never the
particle rows or the slip flags). annotate also flags known botok slips: a negation swallowed into a word is
re-split (sgo ma | lags -> sgo + ma NEG), and NEG:, COMPOUND?, "after NEG", "or fused" and "or split" lines mark the rest.

USAGE
  tibdict.py build   [--golden DIR] [--mitra DIR] [--public DIR] [--db PATH] [--tib]   # once; ~2-4 min
  tibdict.py fetch-public [--dest DIR]      # download Steinert's open Tibetan-English files (default ~/.tibdict/public)
  tibdict.py annotate "<tibetan or wylie>" | --file F  [--budget 9000] [--brief] [--examples] [--per-line]
  tibdict.py lookup  "<word>" ["<word>" ...] [--full] [--examples]
  tibdict.py verb    "<stem>"
  tibdict.py status

Runs under any Python 3.9+ with pyewts; segmentation uses botok when importable (it is in
~/.venvs/tib on this machine; the script re-executes itself there if botok is missing).

The index is private working data (the source dictionaries are copyrighted). Do not redistribute it.
The public files remain the copyright of their respective authors (see LICENSE-NOTES.md).
"""
import argparse, gzip, html, json, os, re, sqlite3, struct, sys, time, glob

DB_DEFAULT = os.path.expanduser("~/.tibdict/tibdict.sqlite")
GOLDEN_DEFAULT = os.environ.get("TIBDICT_GOLDEN", "")  # a GoldenDict/StarDict folder; optional
MITRA_DEFAULT = os.path.expanduser("~/.tibdict")  # searched recursively for the MITRA lexicon .ifo
VENV_PY = os.path.expanduser("~/.venvs/tib/bin/python")

# --------------------------------------------------------------------------- wylie helpers
_conv = None
def conv():
    global _conv
    if _conv is None:
        import pyewts
        _conv = pyewts.pyewts()
    return _conv

def is_tibetan(s):
    return bool(re.search(r'[\u0F00-\u0FFF]', s))

def to_wylie(s):
    w = conv().toWylie(s)
    return w

def to_unicode(w):
    return conv().toUnicode(w)

def norm_key(k):
    """Normalise a headword (Wylie or Unicode) to a canonical Wylie key."""
    k = k.strip()
    if is_tibetan(k):
        k = re.sub(r'-\d+$', '', k)
        k = k.strip('་།༌ \u0f0b\u0f0c\u0f0d')
        if not k:
            return ""
        try:
            k = to_wylie(k + '་')
        except Exception:
            return ""
    k = k.lower().replace('_', ' ')
    k = re.sub(r'[/\s]+$', '', k)
    k = re.sub(r'\s+', ' ', k).strip()
    return k

# --------------------------------------------------------------------------- stardict reader
def read_stardict(base):
    """Yield (key, body) from a StarDict base path (without extension)."""
    idx = open(base + '.idx', 'rb').read()
    p = base + '.dict'
    data = gzip.open(p + '.dz', 'rb').read() if os.path.exists(p + '.dz') else open(p, 'rb').read()
    ifo = open(base + '.ifo', encoding='utf8', errors='replace').read()
    typed = 'sametypesequence' not in ifo
    i = 0
    while i < len(idx):
        j = idx.index(b'\0', i)
        w = idx[i:j].decode('utf8', 'replace')
        o, s = struct.unpack('>II', idx[j + 1:j + 9])
        i = j + 9
        body = data[o:o + s]
        if typed and body[:1].isalpha():
            body = body[1:]
        yield w, body.decode('utf8', 'replace').rstrip('\0'), o, s

def read_syn(base):
    p = base + '.syn'
    if not os.path.exists(p):
        return
    syn = open(p, 'rb').read()
    i = 0
    while i < len(syn):
        j = syn.index(b'\0', i)
        w = syn[i:j].decode('utf8', 'replace')
        (n,) = struct.unpack('>I', syn[j + 1:j + 5])
        i = j + 5
        yield w, n

def strip_html(s):
    s = re.sub(r'<k>.*?</k>\s*', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' / ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = s.replace('\\n', ' / ').replace('\n', ' / ')
    s = re.sub(r'\s+', ' ', s).strip(' /')
    return s

# --------------------------------------------------------------------------- MITRA parsing
_TIB = r'[\u0F00-\u0FFF\u0f0b]+'
def parse_mitra(body):
    """Compact JSON for a MITRA Tibetan Lexicon entry (evidence excluded)."""
    head, _, _ = body.partition('<div><b>Evidence</b></div>')
    out = {}
    m = re.search(r'<div><b>Verb</b>(.*?)</div>', head, re.S)
    if m:
        v = strip_html(m.group(1))
        v = re.sub(_TIB + r'\s*', '', v)         # drop the Tibetan-script duplicates
        out['verb'] = re.sub(r'\s+', ' ', v).strip()
    m = re.search(r'<b>Used as:</b>\s*([^<]+)', head)
    if m:
        out['pos'] = m.group(1).strip()
    m = re.search(r'<b>Nominalized forms with their own entries:</b>(.*?)</div>', head, re.S)
    if m:
        out['nom'] = [x for x in re.findall(r'bword://([^"]+)"', m.group(1))][:4]
    m = re.search(r'<b>Related forms with their own entries:</b>(.*?)</div>', head, re.S)
    if m:
        out['rel'] = [x for x in re.findall(r'bword://([^"]+)"', m.group(1))][:4]
    senses = []
    for sm in re.finditer(r'<div style="margin-top:\.7em"><b>(\d+)\.\s*(.*?)</b></div>\s*<ul[^>]*>(.*?)</ul>', head, re.S):
        gloss = strip_html(sm.group(2))
        ul = sm.group(3)
        d = {'g': gloss}
        for lang, key in (('English', 'en'), ('Sanskrit', 'sa'), ('Chinese', 'zh'), ('Note', 'note')):
            lm = re.search(r'<li><b>%s:</b>(.*?)</li>' % lang, ul, re.S)
            if lm:
                d[key] = strip_html(lm.group(1))
        senses.append(d)
    out['senses'] = senses
    return out

def mitra_evidence(body, n=2):
    """Up to n cited passages: (wylie, english, source)."""
    _, _, ev = body.partition('<div><b>Evidence</b></div>')
    out = []
    for block in re.findall(r'<div style="margin:\.35em[^"]*">(.*?)</div>\s*(?=<div style="margin:\.35em|$)', ev, re.S):
        wy = re.search(r'\((.*?)\)<br>', block, re.S)
        en = re.search(r'<br>en:\s*(.*?)<br>', block, re.S)
        src = re.search(r'<small[^>]*>(.*?)</small>', block, re.S)
        if wy and en:
            out.append((strip_html(wy.group(1)), strip_html(en.group(1)),
                        strip_html(src.group(1))[:90] if src else ''))
        if len(out) >= n:
            break
    return out

# --------------------------------------------------------------------------- other dict cleaners
def clean_hopkins(body):
    f = strip_html(body).split('\t') if '\t' in body else [strip_html(body)]
    f = [x.strip() for x in body.replace('<k>', '').split('\t')]
    f[0] = re.sub(r'^.*?</k>\s*', '', f[0], flags=re.S)
    skt = f[0].replace('Skt.', '').strip() if f and f[0].startswith('Skt') else ''
    gl = f[1] if len(f) > 1 else ''
    stems = None
    m = re.search(r'f\.pr\.p\.i:\s*([\w\' ]+)', gl)
    if m:
        parts = m.group(1).split()
        if len(parts) == 4:
            stems = dict(zip(('fut', 'pres', 'past', 'imp'), parts))
        gl = gl.replace(m.group(0), '').strip()
    gl = re.sub(r'\s+', ' ', html.unescape(gl))
    extra = html.unescape(f[2]) if len(f) > 2 else ''
    txt = gl
    if skt:
        txt += ' [Skt. ' + re.sub(r'\{[^}]*\}', '', skt).strip() + ']'
    if extra:
        txt += ' {' + re.sub(r'\{[^}]*\}', '', extra).strip() + '}'
    return re.sub(r'\s+', ' ', txt).strip(), stems

def clean_84000(body):
    f = [x.strip() for x in body.split(';')]
    if len(f) < 5:
        return strip_html(body)
    eng, skt, defn = f[0], f[1], f[2]
    toh = next((x for x in f if x.startswith('Toh')), '')
    title = f[f.index(toh) + 1] if toh and f.index(toh) + 1 < len(f) else ''
    s = eng
    if skt:
        s += ' (' + skt + ')'
    if defn:
        s += ' — ' + defn
    if toh:
        s += ' [' + toh + (', ' + title if title else '') + ']'
    return s

def clean_vb(body):
    s = strip_html(body)
    s = re.sub(_TIB, lambda m: to_wylie(m.group(0) + '་').strip(), s)
    return s

def clean_generic(body):
    return strip_html(body)

# --------------------------------------------------------------------------- sources
# (name, relative path or glob, kind, priority, key-script, cleaner)
GOLDEN_SOURCES = [
    ("JH",     "Hopkins (Tib, Cn, Eng)/JH_wy-en/jh_dict_wylie", "stardict", 2,  "w", "hopkins"),
    ("84000",  "84000/Wylie Key/84000_Glossary-03-04-2021-wylie-key", "stardict", 3, "w", "84000"),
    ("RY",     "RYI/RangjungYesheTibetanWylie", "stardict", 4, "w", "generic"),
    ("Hackett","from McNamara/Hackett-Def2015.txt", "tsv", 5, "w", "generic"),
    ("Mvy",    "from McNamara/Mahavyutpatti-Skt.txt", "tsv", 6, "w", "generic"),
    ("ML",     "Lobsang Monlam/ML_Tb-En_2007.xdxf", "stardict", 7, "u", "generic"),
    ("VB",     "Verbs/VB.xdxf", "stardict", 8, "u", "vb"),
    ("Verbinator", "from McNamara/Verbinator.txt", "tsv", 8, "w", "generic"),
    ("Berzin", "from McNamara/Berzin.txt", "tsv", 9, "w", "generic"),
    ("BerzinDef", "from McNamara/Berzin-Def.txt", "tsv", 9, "w", "generic"),
    ("Tsepak", "06TsepakRigdzin/**/*.idx", "stardict-glob", 10, "?", "generic"),
    ("JV",     "Jim Valby/JW", "stardict", 11, "u", "generic"),
    ("EP",     "Erik Penatsang/EP", "stardict", 12, "u", "generic"),
    ("Duff",   "Tony Duff/2td", "stardict", 14, "u", "generic"),
    ("Das",    "Chandra Das/SD", "stardict", 15, "u", "generic"),
    ("Martin", "from McNamara/DanMartin.txt", "tsv", 16, "w", "generic"),
    ("Yogacara", "from McNamara/Yoghacharabhumi-glossary.txt", "tsv", 17, "w", "generic"),
    ("Gateway", "from McNamara/GatewayToKnowledge.txt", "tsv", 18, "w", "generic"),
    ("Sera",   "from McNamara/Sera-Textbook-Definitions.txt", "tsv", 19, "w", "generic"),
    ("Doctor", "from McNamara/ThomasDoctor.txt", "tsv", 20, "w", "generic"),
    # Tibetan-Tibetan, only with --tib
    ("MonlamGrand", "monlamGrandDic/monlamGrand", "stardict", 30, "u", "generic"),
    ("Dunkar", "Dunkar/DK", "stardict", 31, "u", "generic"),
    ("TshigMdzod", "1tsig_mdzod_chen_mo.dictionary/**/*.idx", "stardict-glob", 32, "u", "generic"),
]

# Christian Steinert's open-source dictionary project keeps the freely redistributable dictionaries as
# plain text, one entry per line, `wylie headword|definition` ('#' lines are comments), in
#   https://github.com/christiansteinert/tibetan-dictionary  ->  _input/dictionaries/public/
# The dictionary name is the filename ("NN-Name"). `fetch-public` downloads the Tibetan->English
# files into ~/.tibdict/public; `build --public DIR` indexes them.
#   "THE COPYRIGHT OF THE DICTIONARY DATA IS WITH THE RESPECTIVE AUTHORS" (README of that repository)
PUBLIC_REPO = "christiansteinert/tibetan-dictionary"
PUBLIC_PATH = "_input/dictionaries/public"
PUBLIC_DEFAULT = os.path.expanduser("~/.tibdict/public")
PUBLIC_ATTRIBUTION = ("Dictionary data: Christian Steinert's Tibetan dictionary project, "
                      "https://github.com/%s (%s). Note from its README: \"the dictionary data is not my own "
                      "and thus THE COPYRIGHT OF THE DICTIONARY DATA IS WITH THE RESPECTIVE AUTHORS\"." % (PUBLIC_REPO, PUBLIC_PATH))

# (filename in the repository, label, priority); labels equal to a GOLDEN_SOURCES name mean the same dictionary
# Priorities 21-29 sit after MITRA (1) and after the GoldenDict sources (2-20), below the Tibetan-Tibetan
# band (30+, hidden without --tib). A file whose label is already indexed from the GoldenDict folder is skipped.
PUBLIC_SOURCES = [
    ('01-Hopkins2015', 'JH', 21),
    ('02-RangjungYeshe', 'RY', 22),
    ('43-84000Dict', '84000', 23),
    ('05-Hackett-Def2015', 'Hackett', 24),
    ('21-Mahavyutpatti-Skt', 'Mvy', 24),
    ('07-JimValby', 'Valby', 24),
    ('08-IvesWaldo', 'IvesWaldo', 24),
    ('33-TsepakRigdzin', 'Tsepak', 25),
    ('03-Berzin', 'Berzin', 25),
    ('04-Berzin-Def', 'BerzinDef', 25),
    ('26-Verbinator', 'Verbinator', 25),
    ('35-ThomasDoctor', 'Doctor', 25),
    ('05-Hopkins-Def2015', 'HopkinsDef', 26),
    ('20-Hopkins-othersEnglish2015', 'HopkinsOth', 26),
    ('15-Hopkins-Skt2015', 'HopkinsSkt', 26),
    ('10-RichardBarron', 'Barron', 26),
    ('23-GatewayToKnowledge', 'Gateway', 26),
    ('22-Yogacharabhumi-glossary', 'Yogacara', 26),
    ('40-CommonTerms-Lin', 'LinTerms', 26),
    ('48-TibTermProject', 'TibTerm', 26),
    ('52-ITLR', 'ITLR', 26),
    ('11-Hopkins-Divisions2015', 'HopkinsDiv', 27),
    ('13-Hopkins-Examples', 'HopkinsEx', 27),
    ('36-ComputerTerms', 'ComputerTerm', 27),
    ('38-GaengWetzel', 'GaengWetzel', 27),
    ('44-84000Definitions', '84000Def', 27),
    ('46-84000Skt', '84000Skt', 27),
    ('53-Bialek', 'Bialek', 27),
    ('01-JongbokYi', 'JongbokYi', 27),
    ('09-DanMartin', 'Martin', 28),
    ('06-Hopkins-Comment', 'HopkinsCmt', 28),
    ('16-Hopkins-Synonyms1992', 'HopkinsSyn', 28),
    ('47-Misc', 'Misc', 28),
    ('68-tibetanlanguage-school', 'TLSchool', 28),
    ('59-sgra_bye_brag_tu_rtogs_byed_chen_mo', 'SgraByeBrag', 28),
]

def public_label(fname):
    """(label, priority) for a Steinert-format file; unknown files get a label from the name."""
    for f, label, prio in PUBLIC_SOURCES:
        if f == fname:
            return label, prio
    label = re.sub(r'^\d+-', '', fname)
    label = re.sub(r'[^A-Za-z0-9]+', '', label)[:12] or 'public'
    return label, 28

def clean_public(body):
    """Definition text of a Steinert-format file: literal '\\n' -> ' / ', real HTML tags dropped,
    but the <place>/<term>/<person> type markers of the 84000 files kept as [place] etc."""
    s = re.sub(r'(?:\\n\s*)+', ' / ', body)
    s = re.sub(r'</?(?:b|i|u|em|strong|br|p|div|span|a|small|sup|sub|font|ul|ol|li)\b[^>]*>', ' ', s, flags=re.I)
    s = re.sub(r'<([A-Za-z][^<>]{0,30})>', r'[\1]', s)
    return strip_html(s)

def parse_public(path, maxlen=1500, verbs=None):
    """Read a `headword|definition` file -> ({key: [definitions]}, lines skipped).
    Tolerates a UTF-8 BOM, CRLF, blank and '#' lines, lines without '|'; repeated headwords keep each
    distinct definition (in file order); bracketed asides in the headword are dropped as Steinert does.
    Verbinator-style 'Present: {x}' fields are appended to VERBS as (form, key, tense) when a list is given."""
    entries, skipped = {}, 0
    with open(path, encoding='utf-8-sig', errors='replace') as fh:
        for line in fh:
            line = line.rstrip('\r\n').lstrip('\ufeff')
            if not line.strip() or line.startswith('#') or '|' not in line:
                skipped += 1
                continue
            key, body = line.split('|', 1)
            key = re.sub(r'\([^)]*\)|\[[^\]]*\]|\{[^}]*\}', ' ', key).replace(',', ' ')
            k = norm_key(key)
            txt = clean_public(body)
            if not k or not txt:
                skipped += 1
                continue
            if verbs is not None and 'Present:' in body:
                for tense, tag in (('pres', 'Present'), ('past', 'Past'), ('fut', 'Future'), ('imp', 'Imperative')):
                    m = re.search(tag + r':\s*\{([^}]+)\}', body)
                    if m:
                        verbs.append((m.group(1).strip(), k, tense))
            defs = entries.setdefault(k, [])
            if txt not in defs:
                defs.append(txt)
    out = {}
    for k, defs in entries.items():
        s = ' // '.join(defs)
        out[k] = s if len(s) <= maxlen else s[:maxlen - 1] + '…'
    return out, skipped

def build_public(db, add_dict, folder, t0):
    """Index every file of FOLDER that is in Steinert's headword|definition format."""
    if not os.path.isdir(folder):
        print(f"public: {folder} not found (run: tibdict.py fetch-public)"); return
    have = {r[0] for r in db.execute("SELECT name FROM dicts")}
    files = sorted(f for f in os.listdir(folder)
                   if os.path.isfile(os.path.join(folder, f)) and not f.startswith('.')
                   and not f.lower().endswith(('.md', '.json', '.py', '.sh', '.zip', '.sqlite', '.db')))
    for fname in files:
        label, prio = public_label(fname)
        if label in have:
            print(f"{label}: skipped ({fname}; a source of that name is already indexed)"); continue
        path = os.path.join(folder, fname)
        verbs = []
        entries, skipped = parse_public(path, verbs=verbs)
        if not entries:
            print(f"{label}: no headword|definition lines in {fname}"); continue
        d = add_dict(label, prio, path, 'public')
        db.executemany("INSERT INTO entries(dict,key,body,off,len) VALUES(?,?,?,?,?)",
                       [(d, k, txt, None, None) for k, txt in entries.items()])
        if verbs:
            db.executemany("INSERT INTO verbs VALUES(?,?,?,?)", [(f, k, t, label) for f, k, t in verbs])
        db.commit(); have.add(label)
        print(f"{label}: {len(entries)} entries" + (f" ({skipped} lines skipped)" if skipped else '') + f" ({time.time()-t0:.0f}s)")

# --------------------------------------------------------------------------- fetch-public
def _http_get(url, accept=None, timeout=120):
    """GET url -> bytes. urllib first, curl as a fallback (some Pythons lack CA certificates)."""
    import urllib.request, subprocess
    hdr = {'User-Agent': 'tibdict'}
    if accept:
        hdr['Accept'] = accept
    if 'api.github.com' in url and os.environ.get('GITHUB_TOKEN'):
        hdr['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=timeout) as r:
            return r.read()
    except Exception as e:
        err = e
    cmd = ['curl', '-fsSL', '--max-time', str(timeout)] + sum((['-H', f'{k}: {v}'] for k, v in hdr.items()), []) + [url]
    try:
        r = subprocess.run(cmd, capture_output=True)
    except OSError:
        raise err
    if r.returncode:
        raise RuntimeError(f"{url}: {err}")
    return r.stdout

def _git_sha(data):
    import hashlib
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()

def fetch_public(args):
    """Download the Tibetan->English dictionaries listed in PUBLIC_SOURCES into args.dest (idempotent)."""
    dest = os.path.expanduser(args.dest)
    os.makedirs(dest, exist_ok=True)
    api = f"https://api.github.com/repos/{PUBLIC_REPO}/contents/{PUBLIC_PATH}"
    raw = f"https://raw.githubusercontent.com/{PUBLIC_REPO}/master/{PUBLIC_PATH}/"
    listing = {}
    try:
        for x in json.loads(_http_get(api).decode('utf8')):
            if x.get('type') == 'file':
                listing[x['name']] = x
    except Exception as e:
        print(f"fetch-public: cannot read the GitHub listing ({str(e)[:120]}); using the built-in file list")
    wanted = [f for f, *_ in PUBLIC_SOURCES]
    got = kept = failed = 0
    via_api = False
    for name in wanted:
        info = listing.get(name)
        local = os.path.join(dest, name)
        if listing and not info:
            print(f"  gone upstream: {name}"); continue
        if os.path.exists(local):
            data = open(local, 'rb').read()
            if info is None or _git_sha(data) == info.get('sha'):
                kept += 1; print(f"  up to date   {name:<42} {len(data)/1e6:6.2f} MB"); continue
        data = None
        try:
            if not via_api:
                try:
                    data = _http_get(raw + name)
                except Exception:
                    if not info:
                        raise
                    via_api = True      # raw.githubusercontent.com unreachable: use the contents API (rate-limited) instead
                    print("  (raw.githubusercontent.com unreachable; using the GitHub contents API)")
            if data is None:
                data = _http_get(info['url'], accept='application/vnd.github.raw')
            if info and _git_sha(data) != info.get('sha'):
                raise RuntimeError('checksum mismatch')
        except Exception as e:
            failed += 1; print(f"  FAILED       {name}: {str(e)[:100]}"); continue
        tmp = local + '.part'
        with open(tmp, 'wb') as fh:
            fh.write(data)
        os.replace(tmp, local)
        got += 1; print(f"  fetched      {name:<42} {len(data)/1e6:6.2f} MB")
    print(f"public dictionaries in {dest}: {got} fetched, {kept} already current, {failed} failed")
    print(PUBLIC_ATTRIBUTION)
    print(f"next: tibdict.py build --public {dest} ...")
    if failed:
        sys.exit(1)

# --------------------------------------------------------------------------- build
SCHEMA = """
CREATE TABLE IF NOT EXISTS dicts(id INTEGER PRIMARY KEY, name TEXT UNIQUE, prio INT, path TEXT, kind TEXT);
CREATE TABLE IF NOT EXISTS entries(id INTEGER PRIMARY KEY, dict INT, key TEXT, body TEXT, off INT, len INT);
CREATE INDEX IF NOT EXISTS entries_key ON entries(key);
CREATE INDEX IF NOT EXISTS entries_dict ON entries(dict);
CREATE TABLE IF NOT EXISTS keys(key TEXT, entry INT);
CREATE INDEX IF NOT EXISTS keys_key ON keys(key);
CREATE TABLE IF NOT EXISTS verbs(form TEXT, lemma TEXT, tense TEXT, src TEXT);
CREATE INDEX IF NOT EXISTS verbs_form ON verbs(form);
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
"""

def build(args):
    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    if os.path.exists(args.db):
        os.remove(args.db)
    db = sqlite3.connect(args.db)
    db.executescript(SCHEMA)
    t0 = time.time()
    did = 0

    def add_dict(name, prio, path, kind):
        nonlocal did
        did += 1
        db.execute("INSERT INTO dicts VALUES(?,?,?,?,?)", (did, name, prio, path, kind))
        return did

    # ---- MITRA lexicon
    mbase = None
    for cand in glob.glob(os.path.join(args.mitra, '**/*.ifo'), recursive=True):
        mbase = cand[:-4]
    if mbase:
        d = add_dict("MITRA", 1, mbase, "mitra")
        rows, keys, verbs = [], [], []
        n = 0
        for key, body, off, ln in read_stardict(mbase):
            k = norm_key(key)
            if not k:
                continue
            j = parse_mitra(body)
            n += 1
            rows.append((d, k, json.dumps(j, ensure_ascii=False), off, ln))
            if 'verb' in j:
                for tense in ('present', 'past', 'future', 'imperative'):
                    for m in re.finditer(tense + r'\s+([a-z\' ]+?)(?:[;,·]|$)', j['verb']):
                        for form in m.group(1).split(','):
                            form = form.strip()
                            if form:
                                verbs.append((form, k, tense[:4], 'MITRA'))
            if len(rows) >= 20000:
                db.executemany("INSERT INTO entries(dict,key,body,off,len) VALUES(?,?,?,?,?)", rows); rows = []
        db.executemany("INSERT INTO entries(dict,key,body,off,len) VALUES(?,?,?,?,?)", rows)
        db.executemany("INSERT INTO verbs VALUES(?,?,?,?)", verbs)
        # synonyms: map inflected forms / script forms to the entry (by index order)
        ids = [r[0] for r in db.execute("SELECT id FROM entries WHERE dict=? ORDER BY id", (d,))]
        krows = []
        for w, idx in read_syn(mbase):
            k = norm_key(w)
            if k and idx < len(ids):
                krows.append((k, ids[idx]))
            if len(krows) >= 50000:
                db.executemany("INSERT INTO keys VALUES(?,?)", krows); krows = []
        db.executemany("INSERT INTO keys VALUES(?,?)", krows)
        db.commit()
        print(f"MITRA: {n} entries, {len(verbs)} verb forms  ({time.time()-t0:.0f}s)")
    else:
        print("MITRA lexicon not found under", args.mitra, "(skipping)")

    # ---- GoldenDict sources
    for name, rel, kind, prio, script, cleaner in GOLDEN_SOURCES:
        if prio >= 30 and not args.tib:
            continue
        if kind == 'stardict-glob':
            c = glob.glob(os.path.join(args.golden, rel), recursive=True)
            if not c:
                print(f"{name}: not found"); continue
            path = c[0][:-4]; kind = 'stardict'
        else:
            path = os.path.join(args.golden, rel)
        if kind == 'stardict' and not os.path.exists(path + '.idx') or kind == 'tsv' and not os.path.exists(path):
            print(f"{name}: not found at {path}"); continue
        d = add_dict(name, prio, path, kind)
        rows, verbs, n = [], [], 0
        if kind == 'stardict':
            for key, body, off, ln in read_stardict(path):
                k = norm_key(key)
                if not k:
                    continue
                stems = None
                if cleaner == 'hopkins':
                    txt, stems = clean_hopkins(body)
                elif cleaner == '84000':
                    txt = clean_84000(body)
                elif cleaner == 'vb':
                    txt = clean_vb(body)
                else:
                    txt = clean_generic(body)
                if not txt:
                    continue
                n += 1
                rows.append((d, k, txt[:1500], off, ln))
                if stems:
                    for tense, form in stems.items():
                        verbs.append((form, k, tense, 'JH'))
                if len(rows) >= 20000:
                    db.executemany("INSERT INTO entries(dict,key,body,off,len) VALUES(?,?,?,?,?)", rows); rows = []
        else:
            for line in open(path, encoding='utf8', errors='replace'):
                if line.startswith('#') or '\t' not in line:
                    continue
                key, body = line.rstrip('\n').split('\t', 1)
                k = norm_key(key)
                if not k:
                    continue
                txt = strip_html(body)
                n += 1
                rows.append((d, k, txt[:1500], None, None))
                if name == 'Verbinator':
                    for tense, tag in (('pres', 'Present'), ('past', 'Past'), ('fut', 'Future'), ('imp', 'Imperative')):
                        m = re.search(tag + r':\s*\{([^}]+)\}', body)
                        if m:
                            verbs.append((m.group(1).strip(), k, tense, 'Verbinator'))
        db.executemany("INSERT INTO entries(dict,key,body,off,len) VALUES(?,?,?,?,?)", rows)
        if verbs:
            db.executemany("INSERT INTO verbs VALUES(?,?,?,?)", verbs)
        db.commit()
        print(f"{name}: {n} entries ({time.time()-t0:.0f}s)")
    # ---- public Steinert-format dictionaries (headword|definition files)
    if args.public:
        build_public(db, add_dict, os.path.expanduser(args.public), t0)
    db.execute("INSERT OR REPLACE INTO meta VALUES('built', ?)", (time.strftime('%Y-%m-%d %H:%M'),))
    db.commit()
    db.execute("VACUUM")
    print("done:", args.db, f"{os.path.getsize(args.db)/1e6:.0f} MB")

# --------------------------------------------------------------------------- lookup
PARTICLES = {
    "gi": "GEN (of; 's; marks the preceding phrase as modifier of what follows)", "kyi": "GEN", "gyi": "GEN", "'i": "GEN", "yi": "GEN",
    "gis": "ERG/INSTR (agent; by means of; because)", "kyis": "ERG/INSTR", "gyis": "ERG/INSTR", "'is": "ERG/INSTR", "yis": "ERG/INSTR",
    "la": "LA-DON (to, for, in, at; recipient; locus; after a verb: purpose or connective 'and')",
    "na": "LOC / COND (in, at; if, when)", "tu": "LA-DON (to, in; adverbial -ly)", "du": "LA-DON", "ru": "LA-DON", "su": "LA-DON", "r": "LA-DON (terminative)", "lar": "LA-DON (to; in; for)", "des": "ERG of de (by that; therefore)", "des na": "therefore", "de nas": "then, after that", "de ltar": "thus, in that way", "de bas na": "therefore", "ji ltar": "just as; how", "ji srid": "as long as", "de srid": "so long", "gang": "which; whoever; what", "gang zhig": "someone who", "ci": "what; whatever", "ci yang": "anything (at all)", "sogs pa": "and so on",
    "las": "ABL (from, out of; than; after a title: 'from the …')", "nas": "ABL / SEQ (from; having done, then)",
    "dang": "COMIT / COORD (and; with; after some verbs: from)",
    "ste": "SEMI-FINAL (… and; having …; namely; so that)", "te": "SEMI-FINAL", "de": "SEMI-FINAL (or the demonstrative 'that')",
    "cing": "COORD (and, while)", "zhing": "COORD", "shing": "COORD",
    "kyang": "CONC (although; even; also)", "yang": "CONC / also", "'ang": "CONC / also",
    "ni": "TOPIC (marks the topic; usually untranslated)", "pas": "CAUSE (because, since; or ERG on a nominalised verb)", "bas": "CAUSE",
    "phyir": "PURPOSE / CAUSE (in order to; because)", "pa'i": "GEN on nominalised verb (… which …; of …)", "ba'i": "GEN on nominalised verb",
    "pa": "NOMINALISER", "ba": "NOMINALISER", "po": "NOMINALISER / def.", "mo": "NOMINALISER / fem.",
    "rnams": "PLURAL", "dag": "PLURAL / dual", "tsam": "RESTR (merely, only; as soon as)", "kho na": "RESTR (only)",
    "mi": "NEG (present/future)", "ma": "NEG (past / prohibitive)", "med": "NEG existential (there is no; without)", "min": "NEG copula (is not)",
    "zhes": "QUOT (thus, saying)", "ces": "QUOT", "shes": "QUOT", "zhes bya ba": "QUOT ('called')", "sogs": "etc.", "la sogs pa": "etc.",
    "shog": "OPT (may …)", "cig": "IMP / indef.", "zhig": "IMP / indef. (a, some)", "shig": "IMP", "gyur cig": "OPT (may it become)",
    "'o": "FINAL (statement)", "so": "FINAL", "to": "FINAL", "ngo": "FINAL", "'am": "ALT (or; question)", "sam": "ALT (or)", "tam": "ALT (or)",
    "ltar": "SIMILE / manner (like, as, according to)", "bzhin": "SIMILE / manner (like; while)", "lta bu": "SIMILE (like, such as)",
}

class Dict:
    def __init__(self, path=DB_DEFAULT):
        if not os.path.exists(path):
            sys.exit(f"tibdict: no index at {path}; run: tibdict.py build")
        self.db = sqlite3.connect(path)
        self.dicts = {r[0]: (r[1], r[2], r[3], r[4]) for r in self.db.execute("SELECT id,name,prio,path,kind FROM dicts")}
        self._mitra_cache = {}

    def entries(self, key, tib=False):
        key = norm_key(key)
        if not key:
            return []
        rows = self.db.execute(
            "SELECT e.id,e.dict,e.key,e.body,e.off,e.len FROM entries e WHERE e.key=? "
            "UNION SELECT e.id,e.dict,e.key,e.body,e.off,e.len FROM keys k JOIN entries e ON e.id=k.entry WHERE k.key=?",
            (key, key)).fetchall()
        out = []
        for eid, d, k, body, off, ln in rows:
            name, prio, path, kind = self.dicts[d]
            if prio >= 30 and not tib:
                continue
            out.append((prio, name, k, body, off, ln, path))
        out.sort()
        return out

    def has(self, key):
        key = norm_key(key)
        return bool(self.db.execute("SELECT 1 FROM entries WHERE key=? LIMIT 1", (key,)).fetchone()
                    or self.db.execute("SELECT 1 FROM keys WHERE key=? LIMIT 1", (key,)).fetchone())

    def verb(self, form):
        form = norm_key(form)
        return self.db.execute("SELECT DISTINCT lemma,tense,src FROM verbs WHERE form=?", (form,)).fetchall()

    def mitra_evidence(self, path, off, ln, n=2):
        if path not in self._mitra_cache:
            p = path + '.dict'
            self._mitra_cache[path] = gzip.open(p + '.dz', 'rb').read() if os.path.exists(p + '.dz') else open(p, 'rb').read()
        body = self._mitra_cache[path][off:off + ln].decode('utf8', 'replace')
        return mitra_evidence(body, n)

def fmt_mitra(j, width, en=4, skt=2, senses=3):
    parts = []
    if j.get('pos'):
        parts.append('[' + j['pos'].replace(' · ', ', ') + ']')
    if j.get('verb'):
        parts.append('VERB ' + j['verb'])
    def top(field, n):
        # 'blessings (1816), blessing (892), power (25) · 88% of 3122' -> 'blessings, blessing, power'
        items = re.sub(r'\s*·\s*\d+% of \d+', '', field)
        items = [re.sub(r'\s*\(\d+\)', '', x).strip() for x in items.split(',')]
        return ', '.join([x for x in items if x][:n])
    for i, s in enumerate(j.get('senses', [])[:senses], 1):
        g = s['g'] if len(s['g']) <= 110 else s['g'][:109] + '…'
        seg = f"{i}. {g}"
        if s.get('en') and en:
            seg += ' <en: ' + top(s['en'], en) + '>'
        if s.get('sa') and skt:
            seg += ' <skt: ' + top(s['sa'], skt) + '>'
        parts.append(seg)
    if j.get('nom'):
        parts.append('nominalised: ' + ', '.join(j['nom']))
    s = ' | '.join(parts)
    return s if len(s) <= width else s[:width - 1] + '…'

def fmt_entry(prio, name, key, body, width, **mitra):
    if name == 'MITRA':
        return 'MITRA: ' + fmt_mitra(json.loads(body), width, **mitra)
    b = body if len(body) <= width else body[:width - 1] + '…'
    return f"{name}: {b}"

# --------------------------------------------------------------------------- segmentation
_bt = None
def botok_tokens(text_uni):
    """Return list of (text_wylie, pos, lemma_wylie) via botok, or None if unavailable."""
    global _bt
    try:
        import warnings
        warnings.filterwarnings('ignore')
        from botok import WordTokenizer, Config
    except ImportError:
        return None
    if _bt is None:
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            _bt = WordTokenizer(config=Config(dialect_name="general"))
    out = []
    for tk in _bt.tokenize(text_uni):
        if tk.chunk_type != 'TEXT':
            if tk.chunk_type in ('PUNCT',) and '།' in tk.text:
                out.append(('/', 'SHAD', '/'))
            continue
        w = norm_key(tk.text) or tk.text
        lem = norm_key(tk.lemma) if tk.lemma else w
        # botok splits affixed particles (bla ma + 'i, la + s). Re-join when the joined form is itself
        # a particle (las, lar, nas, des ...) so the relation table can label it.
        if getattr(tk, 'affix', False) and out and out[-1][1] != 'SHAD':
            aff = w[0] if re.fullmatch(r'[srd]a', w) else w      # pyewts renders a bare suffix letter as 'sa'
            joined = out[-1][0] + aff
            if joined in PARTICLES or (len(out[-1][0].split()) == 1 and out[-1][0] in PARTICLES):
                out[-1] = (joined, 'PART', joined)
                continue
            w = aff if aff != w else w
        if w in BAD_MERGES:
            for part in BAD_MERGES[w]:
                out.append((part, 'PART' if part in PARTICLES else '', part))
            continue
        out.append((w, tk.pos or '', lem))
    return out

PART_SET = set(PARTICLES)
# botok merges these into a loan word or a phrase; in classical text they are particle + word.
# ('la ma' is handled by resplit_negation below, with a note.)
BAD_MERGES = {'ma la': ['ma', 'la'], 'ma yin pa la': ['ma yin pa', 'la']}
def lattice_tokens(syls, D, maxn=5):
    """Dictionary max-match over Wylie syllables, penalising matches that swallow a particle."""
    out, i = [], 0
    while i < len(syls):
        best, bestn = None, 1
        for n in range(min(maxn, len(syls) - i), 0, -1):
            cand = ' '.join(syls[i:i + n])
            if D.has(cand):
                inner = syls[i + 1:i + n]
                if n > 1 and (syls[i + n - 1] in PART_SET and cand not in PARTICLES) and n > 2:
                    continue
                best, bestn = cand, n
                break
        w = best or syls[i]
        out.append((w, 'PART' if w in PARTICLES else '', w))
        i += bestn
    return out

def split_affix(w):
    """bla ma'i -> (bla ma, 'i); sems su -> handled as separate syllable; return (stem, affix) or (w, None)."""
    m = re.match(r"^(.*?[a-z])('i|'o|'am|'ang|s|r)$", w)
    if m and m.group(1) not in PARTICLES and not D_has_fast(w):
        return m.group(1), m.group(2)
    return w, None
_D = None
def D_has_fast(w):
    return _D.has(w) if _D else False

def tokenize(text, D):
    """Return list of (surface_wylie, pos, lemma) for one unit of text (any script)."""
    text = text.strip()
    if not text:
        return []
    uni = text if is_tibetan(text) else to_unicode(text)
    toks = botok_tokens(uni)
    if toks is None:
        wy = to_wylie(uni) if is_tibetan(uni) else text
        syls = [s for s in re.split(r"[\s/]+|[།༎]+", wy) if s and s not in ('_',)]
        toks = lattice_tokens(syls, D)
    return toks

# --------------------------------------------------------------------------- segmentation repairs
# botok slips that annotate flags or repairs (see repair_segmentation):
#   1. a negation swallowed at the end of a word (sgo ma | lags -> sgo + ma NEG + lags)
#   2. a compound right after a negation that hides the negation's scope (ma + dag zhing)
#   3. a word split into stem + affix (cha + r, where char "rain" is a word)
#   4. a multi-syllable headword split across tokens (phyag + na + rdo rje)
NEG_SYLS = ('ma', 'mi')
NEG_COUNT_SYLS = ('ma', 'mi', 'med', 'min')
COPULA_VERBS = {"lags", "yin", "min", "'dug", "red", "mchis", "gda'", "yod", "med", "'gyur", "byed", "bya"}
# lexical -ma / -mi words that are never re-split, even before a copula (bla ma yin, dbu ma yin ...)
NEG_PROTECT = {"bla ma", "a ma", "ma ma", "slob ma", "srung ma", "dbu ma", "sgrol ma", "nyi ma", "mkha' 'gro ma",
               "rnal 'byor ma", "dge slong ma", "dge tshul ma", "dge bsnyen ma", "'phags ma", "rig ma", "yum ma",
               "phyi ma", "snga ma", "gong ma", "'og ma", "tha ma", "sngon ma", "gzhon nu ma", "lha mi", "rje ma", "cig ma", "dri ma", "sgyu ma"}
NEG_STRONG_NOUN = 200      # a -ma/-mi word with this many MITRA attestations is a real word: leave it alone
AFFIXES = ("r", "s", "'i", "'am", "'ang", "'o")
# case markers and clause connectives: a dictionary window may not start or end on one of these
EDGE_PARTICLES = {"gi", "kyi", "gyi", "'i", "yi", "gis", "kyis", "gyis", "'is", "yis", "la", "na", "tu", "du", "ru",
                  "su", "r", "lar", "las", "nas", "dang", "ste", "te", "cing", "zhing", "shing", "kyang", "yang",
                  "'ang", "ni", "pas", "bas", "zhes", "ces", "shes", "'o", "so", "to", "ngo", "'am", "sam", "tam",
                  "rnams", "sogs"}
# PARTICLES entries that are just as often words (dag pure, zhing field, de that ...): not 'particles only'
LEXICAL_PARTICLES = {"dag", "zhing", "de", "gang", "ci", "bzhin", "ltar", "phyir", "tsam", "yang"}
COMPOUND_MAXPRIO = 20      # MITRA, JH, RY ... every GoldenDict source; not the public (21+) or Tibetan-Tibetan (30+) ones
COMPOUND_MAX = 8

def headword(D, key, maxprio=COMPOUND_MAXPRIO, syn=True, names=None):
    """Best (prio, name, key, body) for KEY among sources with priority <= maxprio, or None.
    syn=False ignores MITRA's inflected-form synonyms (only real headwords count)."""
    key = norm_key(key)
    if not key:
        return None
    sql = ("SELECT d.prio,d.name,e.key,e.body FROM entries e JOIN dicts d ON d.id=e.dict WHERE e.key=? AND d.prio<=?")
    params = [key, maxprio]
    if syn:
        sql += (" UNION SELECT d.prio,d.name,e.key,e.body FROM keys k JOIN entries e ON e.id=k.entry "
                "JOIN dicts d ON d.id=e.dict WHERE k.key=? AND d.prio<=?")
        params += [key, maxprio]
    rows = [r for r in D.db.execute(sql + " ORDER BY 1", params).fetchall() if not names or r[1] in names]
    return rows[0] if rows else None

def short_gloss(name, body, maxlen=60):
    """First sense of an entry in a few words (MITRA: its top English renderings)."""
    if name == 'MITRA':
        j = json.loads(body)
        s = (j.get('senses') or [{}])[0]
        g = ''
        if s.get('en'):
            items = re.sub(r'\s*·\s*\d+% of \d+', '', s['en'])
            out = []
            for x in (re.sub(r'\s*\(\d+\)', '', x).strip() for x in items.split(',')):
                if x and not re.search(r'[.:;!?]', x) and x.lower().rstrip('s') not in [o.lower().rstrip('s') for o in out]:
                    out.append(x)
            g = ', '.join(out[:3])
        g = g or s.get('g', '').split(';')[0]
    else:
        segs = [re.sub(r'\[[^\]]*\]', ' ', x).replace('*', ' ').strip() for x in re.split(r' // | / ', body)]
        g = next((x for x in segs if x and not re.match(r'(?i)syn\b', x)), segs[0])
        if not re.sub(r'\{[^}]*\}', '', g).strip():           # JH: gloss only in {…}
            m = re.search(r'\{([^}]*)\}', g)
            g = m.group(1) if m else g
        g = re.sub(r'\{[^}]*\}', ' ', g)
        g = re.sub(r'^\s*\d+\)\s*', '', g)
        g = re.sub(r'\s+\d+\)\s*', ' ', g)
        g = '; '.join(x.strip() for x in g.split(';') if x.strip())
    g = re.sub(r'\s+', ' ', g).strip(' ;,')
    return g if len(g) <= maxlen else g[:maxlen - 1].rstrip(' ;,') + '…'

def mitra_attestations(D, key):
    """Total number of parallel-text attestations MITRA gives for KEY (0 if no MITRA entry)."""
    hw = headword(D, key, maxprio=1, syn=False, names=('MITRA',))
    if not hw:
        return 0
    return sum(int(n) for s in json.loads(hw[3]).get('senses', []) for n in re.findall(r'of (\d+)', s.get('en', '')))

def _is_verbal(tok):
    return bool(tok) and tok[1] != 'SHAD' and (tok[0].split()[0] in COPULA_VERBS or tok[1] in ('VERB', 'AUX'))

def resplit_negation(toks, D):
    """Slip 1: a token of 2+ syllables ending in ma/mi is re-split into stem + NEG when the stem is a case
    particle (la ma: always), or when the next token is a verb/auxiliary/copula, the stem is a headword and the
    whole token is not a well-attested word. Returns (tokens, groups, notes): groups[i] is the index of the botok
    token that token i came from; notes maps a token index to extra lines."""
    out, groups, notes = [], [], {}
    for i, (w, pos, lem) in enumerate(toks):
        syls = w.split()
        if pos != 'SHAD' and len(syls) >= 2 and syls[-1] in NEG_SYLS:
            stem, neg = ' '.join(syls[:-1]), syls[-1]
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            split = stem in EDGE_PARTICLES or (
                _is_verbal(nxt) and w not in NEG_PROTECT and headword(D, stem) is not None
                and mitra_attestations(D, w) < NEG_STRONG_NOUN)
            if split:
                out.append((stem, 'PART' if stem in PARTICLES else '', stem)); groups.append(i)
                out.append((neg, 'PART', neg)); groups.append(i)
                notes.setdefault(len(out) - 1, []).append(
                    f'      (tibdict split: botok had "{w}"; read as {stem} + {neg} NEG)')
                continue
            if w in NEG_PROTECT and _is_verbal(nxt) and stem not in EDGE_PARTICLES:
                out.append((w, pos, lem)); groups.append(i)
                notes.setdefault(len(out) - 1, []).append(
                    f'      ⚠ "{w}" before a verb: also read as {stem} + {neg} NEG ("{stem} … not …", e.g. sngon ma byung = never arose before)')
                continue
        out.append((w, pos, lem)); groups.append(i)
    return out, groups, notes

def neg_compound_hints(toks, D, notes):
    """Slip 2: NEG followed by a compound whose first syllable is a verb/adjective (ma + dag zhing): hint that
    the negation may scope over that syllable only. Segmentation is not changed."""
    for i in range(len(toks) - 1):
        neg, (w, pos, lem) = toks[i][0], toks[i + 1]
        syls = w.split()
        if neg not in NEG_SYLS or pos == 'SHAD' or len(syls) < 2:
            continue
        first, rest = syls[0], ' '.join(syls[1:])
        if re.fullmatch(r"(?:pa|ba|po|bo|mo|ma)(?:'i|'o|r|s|'am|'ang)?", rest):   # just verb + nominaliser
            continue
        hw = headword(D, first, maxprio=2, syn=False)
        if not hw:
            continue
        verbal = ('verb' in json.loads(hw[3]).get('pos', '') or 'adjective' in json.loads(hw[3]).get('pos', '')
                  if hw[1] == 'MITRA' else bool(D.verb(first)))
        if not verbal:
            continue
        negd = headword(D, f"{neg} {first}")
        neg_g = short_gloss(negd[1], negd[3], 30) if negd else 'not ' + short_gloss(hw[1], hw[3], 26)
        rhw = headword(D, rest)
        rest_g = short_gloss(rhw[1], rhw[3], 30) if rhw else rest
        notes.setdefault(i + 1, []).append(
            f'      ⚠ after NEG: consider {neg} + {first} | {rest} (= "{neg_g}" + "{rest_g}")'
            f' · {first} = {short_gloss(hw[1], hw[3], 50)} ({hw[1]})')

def fused_affix_notes(toks, D):
    """Slip 3: an affix row (r, s, 'i, 'am, 'ang, 'o) whose fusion with the preceding token is itself a headword
    (cha + r -> char "rain"). Returns {token index: text appended to the affix row}."""
    inline = {}
    for i in range(1, len(toks)):
        w, prev = toks[i][0], toks[i - 1]
        if w not in AFFIXES or prev[1] == 'SHAD':
            continue
        fused = prev[0] + w
        if fused in PARTICLES:
            continue
        # a vowel affix ('i 'o 'am 'ang) never ends a separate word; dictionaries list such fusions as
        # conveniences, so only MITRA/JH count there
        hw = headword(D, fused, syn=False,
                      names=None if w in ('r', 's') and ' ' not in prev[0] else ('MITRA', 'JH'))
        if hw:
            inline[i] = f"  (or fused: {hw[2]} — {short_gloss(hw[1], hw[3], 40)}, {hw[1]})"
            continue
        # botok also glues a syllable to the token before it and leaves the affix alone (la la + s for la + las,
        # dang la + s for dang + las): fuse the last syllable only, unless it is a nominaliser (pa + r is just par)
        syls = prev[0].split()
        if len(syls) > 1 and w in ('r', 's') and not re.fullmatch(r"(?:pa|ba|po|bo|mo|ma)", syls[-1]):
            last = syls[-1] + w
            hw = headword(D, last, syn=False, names=('MITRA', 'JH'))
            if hw:
                part = f"; or {PARTICLES[last].split(' (')[0]} particle" if last in PARTICLES else ''
                inline[i] = (f"  (or fused: {' '.join(syls[:-1])} + {last} — {short_gloss(hw[1], hw[3], 40)}, "
                             f"{hw[1]}{part})")
    return inline

def merged_token_notes(toks, D, inline):
    """A multi-syllable token that MITRA and JH do not list but that splits into two headwords
    (sgra med dri med -> sgra med | dri med; sems las -> sems | las): append (or split: A | B) to its row."""
    for i, (w, pos, lem) in enumerate(toks):
        syls = w.split()
        if pos == 'SHAD' or len(syls) < 2 or w in PARTICLES or i in inline:
            continue
        if headword(D, w, maxprio=2, syn=False):
            continue
        cuts = sorted(range(1, len(syls)), key=lambda c: -min(c, len(syls) - c))   # balanced cuts first
        for c in cuts:
            a, b = ' '.join(syls[:c]), ' '.join(syls[c:])
            if (a in PARTICLES or headword(D, a, syn=False)) and (b in PARTICLES or headword(D, b, syn=False)):
                inline[i] = f"  (or split: {a} | {b})"
                break

# Case-particle allomorphs: gi/gis after final g ng; kyi/kyis after d b s; gyi/gyis after n m r l.
# A gi/kyi/gyi(s) whose form does not fit the syllable before it probably belongs to a word (yo gi + s).
_ALLOMORPH = {'g': ('g', 'ng'), 'ky': ('d', 'b', 's'), 'gy': ('n', 'm', 'r', 'l')}
def allomorph_mismatch(prev_syl, particle):
    m = re.fullmatch(r"(g|ky|gy)is?", particle)
    if not m:
        return False
    tail = re.sub(r"'(?:i|o|am|ang)$", '', prev_syl)
    if re.search(r"[aeiou']$", tail):        # open syllable: 'i / yi / s / yis expected
        return True
    return not tail.endswith(_ALLOMORPH[m.group(1)]) and not (m.group(1) == 'g' and tail.endswith('d'))

def compound_candidates(toks, groups, D):
    """Slip 4: greedy longest match over 2-5 consecutive syllables that cross a botok token boundary; returns
    the COMPOUND? line (or None). Affix rows are merged into their syllable (chud pa + r -> chud par). A window may
    cut into a token only where what it leaves of that token is one particle syllable (de | yang dag par,
    ma dag | zhing); it may not start or end on a standalone case/connective particle. A gi/kyi/gyi(s) of the
    wrong allomorph is tried as the end of a word (yo gis -> yo gi + s)."""
    syl = []          # [text, botok group, token index, text without affix] or None at a shad
    tok_syls = {}
    for i, (w, pos, lem) in enumerate(toks):
        if pos == 'SHAD':
            syl.append(None)
        elif w in AFFIXES and syl and syl[-1] is not None:
            syl[-1][3] = syl[-1][0]; syl[-1][0] += w
        else:
            for s_ in w.split():
                tok_syls.setdefault(i, []).append(len(syl))
                syl.append([s_, groups[i], i, None])

    def leftover_ok(pos_list, keep):
        rest = [syl[p][0] for p in pos_list if p not in keep]
        return not rest or (len(rest) == 1 and rest[0] in PARTICLES)

    cands, seen, i = [], set(), 0
    while i < len(syl):
        took = 1
        for n in range(min(5, len(syl) - i), 1, -1):
            win = syl[i:i + n]
            if any(x is None for x in win) or len({x[1] for x in win}) < 2:
                continue
            if all((x[3] or x[0]) in PARTICLES and (x[3] or x[0]) not in LEXICAL_PARTICLES for x in win):
                continue
            span = set(range(i, i + n))
            if not (leftover_ok(tok_syls[win[0][2]], span) and leftover_ok(tok_syls[win[-1][2]], span)):
                continue
            keys, extra = [], ''
            first_alone = len(tok_syls[win[0][2]]) == 1
            last_alone = len(tok_syls[win[-1][2]]) == 1
            if win[0][0] in EDGE_PARTICLES and first_alone:
                continue
            if win[-1][0] in EDGE_PARTICLES and last_alone:
                if not allomorph_mismatch(win[-2][0], win[-1][0]):
                    continue
                keys.append(' '.join([x[0] for x in win[:-1]] + [win[-1][0].rstrip('s')]))
                extra = '; +s ERG' if win[-1][0].endswith('s') else ''
            else:
                keys.append(' '.join(x[0] for x in win))
                if win[-1][3]:
                    keys.append(' '.join([x[0] for x in win[:-1]] + [win[-1][3]]))
            hw = next((h for h in (headword(D, k) for k in keys) if h), None)
            if hw:
                if hw[2] not in seen:
                    seen.add(hw[2])
                    budget = 80 - len(hw[2]) - len(hw[1]) - len(extra) - 6
                    cands.append((-n, len(cands), f"{hw[2]} = {short_gloss(hw[1], hw[3], max(20, budget))} ({hw[1]}{extra})"))
                took = n
                break
        i += took
    if not cands:
        return None
    return 'COMPOUND? ' + ' · '.join(c for _, _, c in sorted(cands)[:COMPOUND_MAX])

def neg_count_line(unit, D=None):
    """Slip 5: the negation syllables of the raw text with one syllable of context each side, so
    the reader can check that every real negation surfaces as a NEG row. A `ma`/`mi` that is the
    second syllable of a protected noun (bla ma, dbu ma …) or that is followed by a syllable making
    a protected name/noun (ma dros pa = Anavatapta) is listed as `(noun)` rather than counted."""
    wy = to_wylie(unit) if is_tibetan(unit) else unit
    syls = [x for x in re.split(r"[\s/|_]+|[།༎]+", wy.lower()) if x]
    items, n_real = [], 0
    for i, syl in enumerate(syls):
        if syl not in NEG_COUNT_SYLS:
            continue
        prev = syls[i - 1] if i else ''
        nxt = syls[i + 1] if i + 1 < len(syls) else ''
        ctx = f"{prev} {syl} {nxt}".strip()
        pair_before = f"{prev} {syl}".strip()
        pair_after = f"{syl} {nxt}".strip()
        noun = False
        if syl in ('ma', 'mi') and (pair_before in NEG_PROTECT or pair_after in NEG_NAME_HEADS):
            noun = True
        elif syl == 'ma' and prev and headword(D, pair_before) is not None and mitra_attestations(D, pair_before) >= 40:
            noun = True          # dri ma, sgyu ma, skad cig ma, nyi ma …: the -ma noun, not a negation
        elif syl == 'mi' and nxt in ('yi', "'i", 'yis', 'rnams', 'dag', 'lus', 'yul', 'la', 'las', 'dang', 'dbang', 'rje', 'chen', 'rnams'):
            noun = True          # mi = human being
        if noun:
            items.append(f"{ctx} (noun)")
            continue
        n_real += 1
        items.append(ctx)
    return f"NEG: {n_real}" + (' — ' + ' · '.join(items) if items else ' (none)')

# -ma/-mi initial words that are names or nouns, not a negation + verb (checked as `ma <next>`)
NEG_NAME_HEADS = {"ma dros", "ma gcig", "ma skyes", "ma bskyod", "ma ma", "mi pham", "mi 'gyur", "mi la", "ma hA", "ma ha", "mi bskyod",
                  "ma mo", "mi rje", "mi rigs", "mi lus", "mi yul", "mi dbang", "mi chen"}

def repair_segmentation(toks, D):
    """Apply the slip rules above. Returns (tokens, notes, inline, compound_line)."""
    toks, groups, notes = resplit_negation(toks, D)
    neg_compound_hints(toks, D, notes)
    inline = fused_affix_notes(toks, D)
    merged_token_notes(toks, D, inline)
    return toks, notes, inline, compound_candidates(toks, groups, D)

# --------------------------------------------------------------------------- annotate
def annotate_word(D, args, st, w, pos, lem, suffix=''):
    """Head line + dictionary lines for one (non-particle) token, at shrink state ST."""
    width = st['width']
    mitra = dict(en=st['en'], skt=st['skt'], senses=st['senses'])
    cands = [w]
    if lem and lem != w:
        cands.append(lem)
    stem, affix = split_affix(w)
    if affix and stem not in cands:
        cands.append(stem)
    lines = []
    found = None
    for c in cands:
        ents = D.entries(c, tib=args.tib)
        if ents:
            found = c
            byname = {}
            for prio, name, k, body, off, ln, path in ents:
                byname.setdefault(name, (prio, name, k, body, off, ln, path))
            chosen = sorted(byname.values())[:st['max_dicts']]
            for prio, name, k, body, off, ln, path in chosen:
                lines.append('      ' + fmt_entry(prio, name, k, body, width if name == 'MITRA' else max(80, width // 3), **mitra))
                if args.examples and name == 'MITRA':
                    for wy, en, src in D.mitra_evidence(path, off, ln, 1):
                        lines.append(f"      ex: {wy} = {en} [{src}]")
            break
    vb = D.verb(w) or (D.verb(stem) if affix else [])
    vb = sorted(vb, key=lambda r: (0 if r[2] == 'MITRA' else 1 if r[2] == 'JH' else 2))
    head = f"  {w:<14} {pos or '':<6}"
    if found and found != w:
        head += f" -> {found}" + (f" (+{affix})" if affix and found == stem else '')
    if vb:
        n = st['verb_forms']
        if st['verb_src']:
            head += '  VERB-FORM?: ' + '; '.join(f"{l} ({t}, {s})" for l, t, s in vb[:n]) + ('  …' if len(vb) > n else '')
        else:
            head += '  VERB-FORM?: ' + '; '.join(f"{l} ({t})" for l, t, s in vb[:n]) + ('  …' if len(vb) > n else '')
    if not found and not vb:
        # try components
        parts = w.split()
        comp = [p for p in parts if D.has(p)] if len(parts) > 1 else []
        head += '  (no entry' + (f"; components: {', '.join(comp)}" if comp else '') + ')'
        if comp:
            for p in comp[:3]:
                e = D.entries(p)[:1]
                if e:
                    lines.append('      ' + p + ' = ' + fmt_entry(e[0][0], e[0][1], e[0][2], e[0][3], width // 2, **mitra))
    return [head + suffix] + lines

def shrink_states(args):
    """Output settings from fullest to smallest, in the order annotate gives things up to meet --budget:
    (a) MITRA <en:> 4->2->1 and <skt:> 2->1->0, (b) MITRA senses 3->2->1, (c) VERB-FORM? one alternative, no
    source, (d) one dictionary per word, (e) narrower lines. Returns (states, index of state (d))."""
    st = dict(en=4, skt=2, senses=3, verb_forms=3, verb_src=True, max_dicts=args.max_dicts, width=args.width)
    states = [dict(st)]
    for en, skt in ((2, 1), (1, 0)):
        st.update(en=en, skt=skt); states.append(dict(st))
    for n in (2, 1):
        st.update(senses=n); states.append(dict(st))
    st.update(verb_forms=1, verb_src=False); states.append(dict(st))
    st.update(max_dicts=1); states.append(dict(st))
    d = len(states) - 1
    while st['width'] > 60:
        st.update(width=max(60, int(st['width'] * 0.7))); states.append(dict(st))
    return states, d

def render_annotation(D, args, analysed, st):
    seen = {}
    report = []
    for ui, (unit, toks, notes, inline, compounds) in enumerate(analysed, 1):
        surface = ' '.join(t[0] for t in toks if t[1] != 'SHAD')
        report.append(f"## unit {ui}: {surface}")
        report.append(neg_count_line(unit, D))
        if compounds:
            report.append(compounds)
        for ti, (w, pos, lem) in enumerate(toks):
            if pos == 'SHAD':
                continue
            if w in PARTICLES or pos in ('PART', 'ADP', 'NO_POS', 'DET') and w in PARTICLES:
                report.append(f"  {w:<14} PARTICLE {PARTICLES.get(w, '')}" + inline.get(ti, ''))
            elif w in seen:
                report.append(f"  {w:<14} (see above)" + inline.get(ti, ''))
            else:
                seen[w] = 1
                report.extend(annotate_word(D, args, st, w, pos, lem, inline.get(ti, '')))
            report.extend(notes.get(ti, []))
    return '\n'.join(report)

def annotate(args):
    global _D
    D = Dict(args.db); _D = D
    text = open(args.file, encoding='utf8').read() if args.file else ' '.join(args.text)
    units = [u for u in re.split(r'\n+', text) if u.strip()] if (args.per_line or '\n' in text.strip()) else [text]
    analysed = [(unit,) + repair_segmentation(tokenize(unit, D), D) for unit in units]
    states, brief_from = shrink_states(args)
    # --brief starts where the budget loop would have reached one dictionary per word, so it is never larger
    for st in states[brief_from if args.brief else 0:]:
        out = render_annotation(D, args, analysed, st)
        if len(out) <= args.budget:
            break
    print(out)

def lookup(args):
    D = Dict(args.db)
    for w in args.text:
        ents = D.entries(w, tib=args.tib)
        print(f"== {w}" + (f" ({norm_key(w)})" if is_tibetan(w) else ''))
        if not ents:
            print("   no entry")
        for prio, name, k, body, off, ln, path in ents:
            if name == 'MITRA' and args.full:
                j = json.loads(body)
                print('   MITRA:', json.dumps(j, ensure_ascii=False, indent=1))
                if args.examples:
                    for wy, en, src in D.mitra_evidence(path, off, ln, 3):
                        print(f"      ex: {wy}\n          = {en}  [{src}]")
            else:
                print('   ' + fmt_entry(prio, name, k, body, 100000 if args.full else args.width))
        for l, t, s in D.verb(w):
            print(f"   VERB-FORM of {l} ({t}, {s})")

def verb(args):
    D = Dict(args.db)
    for w in args.text:
        rows = D.verb(w)
        print(f"== {w}: " + ('; '.join(f"form of {l} ({t}, {s})" for l, t, s in rows) if rows else 'not a listed stem form'))
        lemmas = {l for l, t, s in rows} | {norm_key(w)}
        for l in lemmas:
            for prio, name, k, body, off, ln, path in D.entries(l):
                if name in ('MITRA', 'JH', 'VB', 'Verbinator', 'Hackett'):
                    print('   ' + fmt_entry(prio, name, k, body, 400))

def status(args):
    D = Dict(args.db)
    for d, (name, prio, path, kind) in sorted(D.dicts.items(), key=lambda x: x[1][1]):
        n = D.db.execute("SELECT count(*) FROM entries WHERE dict=?", (d,)).fetchone()[0]
        print(f"{prio:>3} {name:<12} {n:>8} entries")
    print("verb forms:", D.db.execute("SELECT count(*) FROM verbs").fetchone()[0],
          "| synonym keys:", D.db.execute("SELECT count(*) FROM keys").fetchone()[0],
          "| built:", D.db.execute("SELECT v FROM meta WHERE k='built'").fetchone()[0])
    try:
        import botok; print("segmentation: botok", botok.__version__)
    except ImportError:
        print("segmentation: dictionary max-match (botok not importable)")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--db', default=DB_DEFAULT)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build'); b.add_argument('--golden', default=GOLDEN_DEFAULT); b.add_argument('--mitra', default=MITRA_DEFAULT); b.add_argument('--tib', action='store_true', help='also index Tibetan-Tibetan dictionaries'); b.add_argument('--public', metavar='DIR', help="also index a folder of Christian Steinert's headword|definition files (see fetch-public)")
    a = sub.add_parser('annotate'); a.add_argument('text', nargs='*'); a.add_argument('--file'); a.add_argument('--budget', type=int, default=9000, help='max characters of output (shrinks dictionaries per word to fit)'); a.add_argument('--width', type=int, default=300, help='max chars per dictionary line'); a.add_argument('--max-dicts', type=int, default=2); a.add_argument('--brief', action='store_true', help='one dictionary per word (= --max-dicts 1)'); a.add_argument('--examples', action='store_true'); a.add_argument('--per-line', action='store_true'); a.add_argument('--tib', action='store_true')
    l = sub.add_parser('lookup'); l.add_argument('text', nargs='+'); l.add_argument('--full', action='store_true'); l.add_argument('--examples', action='store_true'); l.add_argument('--width', type=int, default=300); l.add_argument('--tib', action='store_true')
    v = sub.add_parser('verb'); v.add_argument('text', nargs='+')
    f = sub.add_parser('fetch-public', help="download the Tibetan-English dictionaries of Christian Steinert's public folder"); f.add_argument('--dest', default=PUBLIC_DEFAULT)
    sub.add_parser('status')
    args = ap.parse_args()
    # re-exec under the venv that has botok + pyewts if this interpreter lacks them
    try:
        import pyewts  # noqa
        if args.cmd == 'annotate':
            import botok  # noqa
    except ImportError:
        if os.path.exists(VENV_PY) and os.path.realpath(sys.executable) != os.path.realpath(VENV_PY):
            os.execv(VENV_PY, [VENV_PY] + sys.argv)
    {'build': build, 'annotate': annotate, 'lookup': lookup, 'verb': verb, 'status': status, 'fetch-public': fetch_public}[args.cmd](args)

if __name__ == '__main__':
    main()
