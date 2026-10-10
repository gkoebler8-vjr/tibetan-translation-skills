/* Tiger CAT — a local viewer and editor over the files the tibetan-translate skill writes.
   No model is called from this page; Dharmamitra is not called from this page. */
const S = { data: null, state: { units: {} }, active: null, tab: 'notes', reviewOnly: false, query: '', expanded: new Set(), saveTimer: null, slug: '', projects: [], meta: {}, job: { state: 'idle' },
  prefs: { left: 250, right: 420, leftOpen: true, rightOpen: true, script: true, slug: '', tips: true, split: 50 } };
const P = () => '?p=' + encodeURIComponent(S.slug);
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const confClass = c => 'conf-' + String(c || 'medium').toLowerCase().replace(/\s+/g, '-');
const md = s => esc(s).replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>').replace(/\*([^*\n]+)\*/g, '<i>$1</i>');
const FLAGCOL = ['#b3261e', '#1f6f8b', '#7d2f6b', '#2f7d4f', '#c2410c', '#4b4bb3', '#8a6b2a', '#0e7c7b'];
const fcol = i => FLAGCOL[i % FLAGCOL.length];
const K = { script: 's', review: 'n', translate: 't', export: 'e', help: '?', tips: 'i', next: 'j / ↓', prev: 'k / ↑', reviewed: 'r', edit: 'Enter', fn: '⌘⇧F', left: '[', right: ']', tabs: '1–5', glossary: 'g', search: '/' };
const LABELMEAN = { GLOSS: ['Gloss', 'This work takes the words up with gloss scaffolding (zhes pa ni …, … la bya) or a paraphrase: a commentary on these very words. Read the passage around the hit.'], QUOTE: ['Quotation', 'This work quotes the line verbatim (a run of twelve syllables or more, or the whole of a short query); the gloss, if any, follows the quotation.'], NEAR: ['Near', 'Similar wording only, found by the semantic search; not a quotation and not a gloss.'] };
const TAGMEAN = { Q: 'Open question: a reading that could go another way, with the alternative', Alt: 'An alternative wording that was considered', Comm: 'What a commentary says about these words, and whether it was followed', Var: 'A variant reading in another witness of the line', Source: 'Where the quotation comes from (Toh number, folio, who else quotes it)', MITRA: "How Dharmamitra's MITRA translation differs, and what was done about it", Issue: 'A translation choice to be aware of: a term swap, an unpacked phrase, a register shift', Check: 'What the fidelity check changed', Conf: 'The confidence grade and its reason', Prior: 'An existing published translation: whether it was consulted or adapted', Grounding: 'The grounding decision', Note: 'Note' };
const CONFRULE = { high: 'No open question on a content word, agent, relation or referent; grounding found or not needed; MITRA agrees or differs only in phrasing.', medium: 'One open question on a term or nuance, or MITRA differs on a content word and the grammar settled it, or a commentary differs and the plain reading was kept.', low: 'A fork on an agent, relation, head noun or referent is still open after grounding; or the check changed a relation; or a bound term has no attested sense here.', 'very low': 'Two or more such open forks; or a suspected corruption or a variant that flips the sense; or the unit could not be parsed with confidence.' };
const KINDLABEL = { form: 'Form', register: 'Register', citation: 'Citation', 'citation-open': 'Citation, source not located', grounded: 'Grounding', variant: 'Variant reading', prior: 'Prior translation' };

/* ---------------------------------------------------------------- boot */
async function init() {
  try { Object.assign(S.prefs, JSON.parse(localStorage.getItem('vcat.prefs') || '{}')); } catch (e) {}
  bind(); applyLayout();
  await loadProjects();
  const want = new URLSearchParams(location.search).get('p') || S.prefs.slug;
  const first = S.projects.find(x => x.slug === want) ? want : (S.projects[0] && S.projects[0].slug);
  if (first) await openProject(first); else showWelcome();
  setInterval(pollRefresh, 8000);
}
async function loadProjects() { const r = await (await fetch('/api/projects')).json(); S.projects = r.projects || []; S.meta = r; renderProjectSelect(); }
async function openProject(slug) {
  S.slug = slug; S.prefs.slug = slug; savePrefs(); history.replaceState(null, '', '?p=' + encodeURIComponent(slug));
  await loadData();
  try { S.state = await (await fetch('/api/state' + P())).json(); } catch (e) { S.state = { units: {} }; }
  S.state.units = S.state.units || {};
  S.active = S.data.units[0]?.id || null;
  renderProjectSelect(); renderAll();
  try { S.job = await (await fetch('/api/run' + P())).json(); } catch (e) {} renderJob(); refreshClaudeStatus(); renderUsage();
}
async function loadData() { S.data = await (await fetch('data.json' + P() + '&t=' + Date.now())).json(); }
function renderProjectSelect() {
  const sel = $('#proj-select'); sel.innerHTML = S.projects.map(x => `<option value="${esc(x.slug)}" ${x.slug === S.slug ? 'selected' : ''}>${esc(x.title)}${x.pending ? ` (${x.pending} to go)` : ''}</option>`).join('') || '<option>no project yet</option>';
}
function showWelcome() {
  $('#units').innerHTML = `<div class="welcome"><h1>Welcome to Tiger CAT</h1><p class="muted">No project yet. A project is one Tibetan text with its brief, its translation run and your revisions.</p><ol class="steps"><li><b>New project:</b> paste the Tibetan (script or Wylie), give it a title, set the audience, purpose, house style and notes policy, and choose the model and effort.</li><li><b>Check the segments</b> the app made, merging or splitting lines if needed.</li><li><b>Translate</b> a page at a time through your own Claude Code with the tibetan-translate skill. The app waits out usage limits and resumes.</li><li><b>Review</b> each segment beside its Tibetan, with the notes, the commentaries and the second opinion.</li><li><b>Export</b> a Word file with real footnotes, English only or aligned.</li></ol><p><button id="welcome-new" class="primary">New project</button> <button id="welcome-help">How it works</button></p></div>`;
  $('#welcome-new').addEventListener('click', newProjectUI); $('#welcome-help').addEventListener('click', helpUI);
  $('#inspector').innerHTML = ''; $('#outline').innerHTML = '';
}
function renderAll() { renderTop(); renderOutline(); renderUnits(); renderInspector(); }
function savePrefs() { try { localStorage.setItem('vcat.prefs', JSON.stringify(S.prefs)); } catch (e) {} }

/* ---------------------------------------------------------------- data helpers */
function U(id) { return S.data.units.find(u => u.id === id); }
function st(id) { return S.state.units[id] = S.state.units[id] || {}; }
function textOf(u) { const e = S.state.units[u.id]; return (e && e.text) ? e.text : u.text; }
function fnsOf(u) { const e = S.state.units[u.id]; return (e && e.footnotes) ? e.footnotes : u.footnotes; }
function reviewed(u) { return !!(S.state.units[u.id] && S.state.units[u.id].reviewed); }
function isEdited(u) { const e = S.state.units[u.id]; if (!e) return false; return (e.text && JSON.stringify(e.text) !== JSON.stringify(u.text)) || (e.footnotes && JSON.stringify(e.footnotes) !== JSON.stringify(u.footnotes)); }
function revertUnit(u) { const e = S.state.units[u.id]; if (!e) return; delete e.text; delete e.footnotes; save(); renderUnits(); renderInspector(); toast(`${u.id}: back to the skill's text and footnotes.`); }
const enKey = s => String(s || '').toLowerCase().replace(/[*"“”‘’']/g, '').replace(/\s+/g, ' ').trim().replace(/^(the|a|an) /, '').replace(/[ .,;:]+$/, '');
function termInText(t, text) { const k = enKey(t); if (!k || /…|\.\.\.|(^| )x( |$)/i.test(k)) return true; const h = enKey(text); if (h.includes(k)) return true; const stem = k.replace(/(ies|es|s|ed|ing)$/, ''); return stem.length >= 4 && h.includes(stem); }
function matches(u) {
  const q = S.query.trim().toLowerCase(); if (!q) return true;
  const hay = [u.id, u.tib, u.wylie, textOf(u).join(' '), u.header, ...u.notes.map(n => n.text), ...fnsOf(u).map(f => f.text)].join('\n').toLowerCase();
  return hay.includes(q);
}
function needsReview(u) { return !reviewed(u); }
function tibHtml(script, wylie, cls = '') { return S.prefs.script ? `<div class="tibt ${cls}">${esc(script)}</div>` : `<div class="wyl ${cls}">${esc(wylie || script)}</div>`; }
function save() {
  clearTimeout(S.saveTimer);
  S.saveTimer = setTimeout(async () => {
    try { await fetch('/api/state' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(S.state) }); }
    catch (e) { toast('Could not save: is tools/serve.py running?'); }
  }, 600);
}
function toast(html, ms = 4500) { const t = $('#toast'); t.innerHTML = html; t.classList.remove('hidden'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.add('hidden'), ms); }
const tip = (title, body) => ` data-tip-title="${esc(title)}" data-tip="${esc(body)}"`;

/* ---------------------------------------------------------------- layout: resizable, collapsible panes */
function applyLayout() {
  const p = S.prefs; const b = document.body;
  b.style.setProperty('--lw', p.left + 'px'); b.style.setProperty('--rw', p.right + 'px');
  b.classList.toggle('left-closed', !p.leftOpen); b.classList.toggle('right-closed', !p.rightOpen);
  if (p.leftOpen && p.rightOpen) b.style.gridTemplateColumns = `${p.left}px 6px minmax(0,1fr) 6px ${p.right}px`; else b.style.gridTemplateColumns = '';
  $('#expand-left').classList.toggle('hidden', p.leftOpen); $('#expand-right').classList.toggle('hidden', p.rightOpen);
  $('#btn-script').textContent = p.script ? 'Script' : 'Wylie'; $('#btn-script').classList.toggle('on', p.script);
  $('#btn-tips').classList.toggle('on', p.tips !== false);
}
function bindResizers() {
  const start = (which) => (e) => {
    e.preventDefault(); const rz = e.currentTarget; rz.classList.add('active'); document.body.classList.add('dragging');
    const move = (ev) => {
      if (which === 'left') S.prefs.left = Math.max(170, Math.min(520, ev.clientX));
      else S.prefs.right = Math.max(280, Math.min(760, window.innerWidth - ev.clientX));
      applyLayout();
    };
    const up = () => { document.removeEventListener('mousemove', move); document.removeEventListener('mouseup', up); rz.classList.remove('active'); document.body.classList.remove('dragging'); savePrefs(); };
    document.addEventListener('mousemove', move); document.addEventListener('mouseup', up);
  };
  $('#rz-left').addEventListener('mousedown', start('left')); $('#rz-right').addEventListener('mousedown', start('right'));
  $('#collapse-left').addEventListener('click', () => { S.prefs.leftOpen = false; applyLayout(); savePrefs(); });
  $('#collapse-right').addEventListener('click', () => { S.prefs.rightOpen = false; applyLayout(); savePrefs(); });
  $('#expand-left').addEventListener('click', () => { S.prefs.leftOpen = true; applyLayout(); savePrefs(); });
  $('#expand-right').addEventListener('click', () => { S.prefs.rightOpen = true; applyLayout(); savePrefs(); });
}

/* ---------------------------------------------------------------- tooltips */
function bindTips() {
  const t = $('#tip');
  document.addEventListener('mouseover', e => {
    if (!S.prefs.tips) return;
    const el = e.target.closest('[data-tip]'); if (!el) return;
    $('.tip-title', t).textContent = el.dataset.tipTitle || ''; $('.tip-body', t).innerHTML = esc(el.dataset.tip).replace(/\n/g, '<br>');
    t.classList.remove('hidden'); place(e);
  });
  document.addEventListener('mousemove', e => { if (!t.classList.contains('hidden')) place(e); });
  document.addEventListener('mouseout', e => { const el = e.target.closest('[data-tip]'); if (el && !el.contains(e.relatedTarget)) t.classList.add('hidden'); });
  function place(e) { const w = t.offsetWidth, h = t.offsetHeight; let x = e.clientX + 14, y = e.clientY + 16; if (x + w > window.innerWidth - 8) x = e.clientX - w - 10; if (y + h > window.innerHeight - 8) y = e.clientY - h - 10; t.style.left = x + 'px'; t.style.top = y + 'px'; }
}

/* ---------------------------------------------------------------- top bar */
function renderTop() {
  const brief = (S.data.brief || '').split(' · ').filter(Boolean);
  const briefTips = ['Audience: decides the register ceiling, the Sanskrit treatment, the verse form and what gets a footnote', 'Purpose of the translation', 'House style and glossary policy'];
  $('#proj-brief').innerHTML = brief.map((c, i) => `<span${tip('Brief', (briefTips[i] ? briefTips[i] + '\n' : '') + c)}>${esc(c)}</span>`).join('');
  const n = S.data.units.length, r = S.data.units.filter(reviewed).length;
  $('#progress-fill').style.width = (100 * r / n) + '%'; $('#progress-text').textContent = `${r}/${n} reviewed`;
  const grades = {}; S.data.units.forEach(u => { if (!u.pending) grades[u.confidence] = (grades[u.confidence] || 0) + 1; });
  $('#grades').innerHTML = ['high', 'medium', 'low', 'very low'].filter(g => grades[g]).map(g => `<span class="conf ${confClass(g)}"${tip('Confidence: ' + g + ' · ' + grades[g] + ' segment' + (grades[g] > 1 ? 's' : ''), CONFRULE[g])}>${grades[g]}</span>`).join('') + (S.data.pending ? `<span class="muted"${tip('Not translated yet', S.data.pending + ' segment(s) wait for a run')}>${S.data.pending} to go</span>` : '');
  $('#c-glossary').textContent = S.data.glossary.length + (S.data.titles.length ? ` + ${S.data.titles.length} titles` : '');
  $('#c-sources').textContent = S.data.sources.length; $('#c-works').textContent = S.data.works.length;
  $('#btn-review').classList.toggle('on', S.reviewOnly);
}

/* ---------------------------------------------------------------- outline */
function renderOutline() {
  const o = $('#outline'); o.innerHTML = '';
  S.data.outline.forEach(sec => {
    const d = document.createElement('div'); d.className = 'sec';
    const single = sec.items.length === 1;
    d.innerHTML = `<div class="lbl" data-first="${sec.units[0]}" data-units="${single ? sec.units.join(',') : ''}"><span>${md(sec.label)}</span><span class="range">${rangeOf(sec.units)}</span></div>` +
      (single ? (sec.items[0].source ? `<span class="src">${esc(sec.items[0].source)}</span>` : '') :
        sec.items.map(it => `<div class="item" data-first="${it.units[0]}" data-units="${it.units.join(',')}"><span>${esc(itemLabel(it, sec))}</span><span class="range">${rangeOf(it.units)}</span></div>` + (it.source ? `<span class="src">${esc(it.source)}</span>` : '')).join(''));
    o.appendChild(d);
  });
  o.querySelectorAll('[data-first]').forEach(el => el.addEventListener('click', () => setActive(el.dataset.first, true)));
}
const rangeOf = us => us.length > 1 ? `${us[0]}–${us[us.length - 1]}` : us[0];
function itemLabel(it, sec) { let l = it.label; if (l.toLowerCase().startsWith(sec.label.toLowerCase())) l = l.slice(sec.label.length).trim(); l = l.replace(/^\((.*)\)$/, '$1'); return l ? l[0].toUpperCase() + l.slice(1) : it.label; }

/* ---------------------------------------------------------------- the English with inline footnote marks and flagged phrases */
function enHtml(u) {
  const lines = textOf(u).slice(); const fns = fnsOf(u); const flags = u.flags || [];
  const placed = new Set();
  const out = lines.map(line => {
    let raw = line;
    fns.forEach((f, i) => { if (placed.has(i)) return; const a = (f.anchor || '').trim(); if (!a) return; const k = raw.indexOf(a); if (k >= 0) { raw = raw.slice(0, k + a.length) + `\u0001F${i}\u0002` + raw.slice(k + a.length); placed.add(i); } });
    return raw;
  });
  fns.forEach((f, i) => { if (placed.has(i)) return; let li = out.length - 1; while (li > 0 && !out[li].trim()) li--; out[li] += `\u0001F${i}\u0002`; placed.add(i); });
  const isL = ch => /[A-Za-zÀ-ɏ]/.test(ch || '');
  return out.map(raw => {
    const toks = [];
    flags.forEach((f, i) => {
      if (!f.phrase) return; let k = -1, from = 0;
      while ((k = raw.indexOf(f.phrase, from)) >= 0) { if (!isL(raw[k - 1]) && !isL(raw[k + f.phrase.length])) break; from = k + 1; }
      if (k < 0) return; const tok = `\u0001Q${i}\u0002`; raw = raw.slice(0, k) + tok + raw.slice(k + f.phrase.length); toks.push([tok, f]);
    });
    let h = md(raw);
    toks.forEach(([tok, f]) => { const note = u.notes[f.note]; const fi = flags.indexOf(f); h = h.replace(tok, `<mark class="flag" data-f="${fi}" style="--fc:${fcol(fi)}" contenteditable="false"${tip((note ? note.tag + ' · ' : '') + (TAGMEAN[f.tag] || '').split(':')[0] + ' · click to open the note', (f.tib ? f.tib + '  ↔  ' : '') + (note ? note.text : ''))}>${esc(f.phrase)}</mark>`); });
    h = h.replace(/\u0001F(\d+)\u0002/g, (m, i) => `<sup class="fnref" contenteditable="false" data-i="${i}"${tip('Footnote ' + (+i + 1), fns[i].text || '(empty)')}>${+i + 1}</sup>`);
    return h;
  }).join('\n');
}
function readEn(el) { const c = el.cloneNode(true); c.querySelectorAll('.fnref').forEach(x => x.remove()); c.querySelectorAll('i').forEach(x => x.replaceWith('*' + x.textContent + '*')); c.querySelectorAll('b').forEach(x => x.replaceWith('**' + x.textContent + '**')); return c.innerText.replace(/\u00a0/g, ' ').replace(/\n{3,}/g, '\n\n').split('\n'); }
function tibHtmlUnit(u) {
  if (!S.prefs.script) return esc(u.wylie);
  let raw = u.tib; const toks = [];
  (u.flags || []).forEach((f, i) => { if (!f.tib) return; const k = raw.indexOf(f.tib); if (k < 0) return; const tok = `\u0001T${i}\u0002`; raw = raw.slice(0, k) + tok + raw.slice(k + f.tib.length); toks.push([tok, f, i]); });
  let h = esc(raw);
  toks.forEach(([tok, f, i]) => { h = h.replace(tok, `<mark class="flag tibmark" data-f="${i}" style="--fc:${fcol(i)}"${tip('Rendered as', '“' + f.phrase + '”')}>${esc(f.tib)}</mark>`); });
  return h;
}

/* ---------------------------------------------------------------- units with sa bcad headings */
function headingsByUnit() {
  const map = {};
  S.data.outline.forEach(sec => sec.items.forEach((it, i) => {
    const first = it.units[0];
    map[first] = { label: sec.items.length === 1 ? sec.label : `${sec.label} · ${itemLabel(it, sec)}`, range: rangeOf(it.units), source: it.source || '' };
  }));
  return map;
}
function renderUnits() {
  const m = $('#units'); m.innerHTML = '';
  const heads = headingsByUnit();
  document.body.style.setProperty('--split', (S.prefs.split || 50) + '%');
  let hidden = [];
  const flushGap = () => {
    if (!hidden.length) return;
    const g = document.createElement('div'); g.className = 'gap';
    const first = hidden[0], last = hidden[hidden.length - 1];
    g.innerHTML = `<span class="muted">${hidden.length === 1 ? first : first + '–' + last} already reviewed</span><span class="spacer"></span>` +
      (hidden.length > 1 ? `<button data-show="${first}">▾ show ${first}</button><button data-show="${last}">show ${last} ▴</button>` : '') + `<button data-show="${hidden.join(',')}">show ${hidden.length === 1 ? 'it' : 'all ' + hidden.length}</button>`;
    g.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { b.dataset.show.split(',').forEach(id => S.expanded.add(id)); renderUnits(); }));
    m.appendChild(g); hidden = [];
  };
  let shown = 0;
  S.data.units.forEach(u => {
    if (!matches(u)) return;
    shown++;
    if (S.reviewOnly && !needsReview(u) && !S.expanded.has(u.id)) { hidden.push(u.id); return; }
    flushGap();
    if (heads[u.id]) { const h = document.createElement('h2'); h.className = 'sabche'; const hd = heads[u.id]; h.innerHTML = `<span>${md(hd.label)}</span><span class="sub">${hd.range}${hd.source ? ' · ' + md(hd.source) : ''}</span>`; m.appendChild(h); }
    const card = document.createElement('article');
    card.className = 'unit' + (u.id === S.active ? ' on' : '') + (reviewed(u) ? ' reviewed' : '') + (u.pending ? ' pending' : ''); card.dataset.id = u.id;
    const chips = (u.tags || []).filter(t => t.kind !== 'register' || !/^(prose|verse)$/i.test(t.label)).map(t => `<span class="chip k-${t.kind}"${tip(KINDLABEL[t.kind] || t.kind, t.detail)}>${esc(t.label)}</span>`).join('');
    const grade = String(u.confidence).toLowerCase();
    const counts = {}; u.notes.forEach(n => counts[n.tag] = (counts[n.tag] || 0) + 1);
    const noteTip = Object.entries(counts).map(([k, v]) => `${v} × ${k}: ${(TAGMEAN[k] || '').split(':')[0].split(',')[0]}`).join('\n') || 'no notes';
    card.innerHTML = `
      <div class="head">
        <span class="id">${u.id}</span>
        ${u.pending ? '' : `<span class="conf ${confClass(u.confidence)}${u.confidence_provisional ? ' prov' : ''}"${tip('Confidence: ' + u.confidence + (u.confidence_provisional ? ' (derived)' : ''), (CONFRULE[grade] || '') + (u.confidence_reason ? '\n\nReason: ' + u.confidence_reason : ''))}>${esc(u.confidence)}</span>`}
        ${chips}
        <span class="spacer"></span>
        <span class="badge"${tip('Editor notes', noteTip)}>${u.notes.length} notes${u.open_q ? ` · ${u.open_q} open` : ''}</span>
        ${isEdited(u) ? `<span class="chip edited"${tip('Edited by you', 'The text or the footnotes differ from what the skill wrote. Revert restores the skill\'s version; final.md in the run folder is never changed by your edits.')}>edited</span><button class="revert"${tip('Revert', 'Back to the skill\'s text and footnotes for this segment')}>revert</button>` : ''}
        <label${tip('Reviewed', 'Tick when you have gone through this segment. Every machine translation needs this, whatever its grade.\nShortcut: ' + K.reviewed)}><input type="checkbox" class="rev" ${reviewed(u) ? 'checked' : ''}> reviewed</label>
      </div>
      <div class="body">
        <div class="tib ${S.prefs.script ? '' : 'wylie'}">${tibHtmlUnit(u)}</div>
        <div class="divider" data-tip="Drag to move the divider between Tibetan and translation for all segments"></div>
        <div class="en" contenteditable="true" spellcheck="false" data-ph="Not translated yet. Run Translate, or type a translation here.">${enHtml(u)}</div>
        <div class="fns">${fnsHtml(u)}</div>
      </div>`;
    card.addEventListener('mousedown', () => { if (S.active !== u.id) setActive(u.id, false); });
    const en = $('.en', card);
    en.addEventListener('input', () => { st(u.id).text = readEn(en); save(); });
    en.addEventListener('blur', () => { en.innerHTML = enHtml(u); bindMarks(card, u); if (isEdited(u) !== !!$('.chip.edited', card)) renderUnits(); });
    en.addEventListener('keydown', e => { if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key.toLowerCase() === 'f') { e.preventDefault(); footnoteAtCaret(card, u); } });
    bindMarks(card, u);
    $('.divider', card).addEventListener('mousedown', e => {
      e.preventDefault(); const body = $('.body', card); document.body.classList.add('dragging');
      const move = ev => { const r = body.getBoundingClientRect(); S.prefs.split = Math.max(25, Math.min(75, Math.round(100 * (ev.clientX - r.left) / r.width))); document.body.style.setProperty('--split', S.prefs.split + '%'); };
      const up = () => { document.removeEventListener('mousemove', move); document.removeEventListener('mouseup', up); document.body.classList.remove('dragging'); savePrefs(); };
      document.addEventListener('mousemove', move); document.addEventListener('mouseup', up);
    });
    $('.rev', card).addEventListener('change', e => { st(u.id).reviewed = e.target.checked; card.classList.toggle('reviewed', e.target.checked); renderTop(); save(); });
    const rv = $('.revert', card); if (rv) rv.addEventListener('click', e => { e.stopPropagation(); if (confirm(`${u.id}: discard your edits and go back to the skill's text and footnotes?`)) revertUnit(u); });
    bindFns(card, u);
    m.appendChild(card);
  });
  flushGap();
  $('#search-count').textContent = S.query.trim() ? `${shown} of ${S.data.units.length}` : '';
  if (!m.querySelector('.unit')) m.innerHTML = S.query.trim() ? `<div class="empty">No segment contains “${esc(S.query.trim())}”.</div>` : '<div class="empty">Every segment is marked reviewed. Switch "Needs review" off to see them all.</div>';
}
function fnsHtml(u) {
  const fns = fnsOf(u);
  const rows = fns.map((f, i) => `<div class="fn" data-i="${i}"><span class="n">${i + 1}</span><div class="txt" contenteditable="true" data-ph="Type the footnote…">${md(f.text)}</div><span class="where"${tip('Where the mark sits', f.anchor ? 'After “' + f.anchor + '”' : 'At the end of the segment')}>${f.anchor ? 'after “' + esc(f.anchor.length > 24 ? f.anchor.slice(0, 22) + '…' : f.anchor) + '”' : 'end of segment'}</span><button class="del" data-tip="Remove this footnote">×</button></div>`).join('');
  return rows + `<button class="add"${tip('Add a footnote', 'Adds a footnote marked at the end of the segment. Select a phrase first to attach it there, or, while typing in the translation, press ' + K.fn + ' to put one right at the cursor.')}>+ footnote <span class="kbd">${K.fn} at the cursor</span></button>`;
}
function bindFns(card, u) {
  const box = $('.fns', card);
  const commit = () => { st(u.id).footnotes = [...box.querySelectorAll('.fn')].map(r => ({ anchor: fnsOf(u)[+r.dataset.i]?.anchor || '', text: readEn($('.txt', r)).join(' ').trim() })); save(); };
  box.querySelectorAll('.fn .txt').forEach(el => { el.addEventListener('input', commit); el.addEventListener('blur', () => { $('.en', card).innerHTML = enHtml(u); }); });
  box.querySelectorAll('.fn .del').forEach(b => b.addEventListener('click', () => { const i = +b.closest('.fn').dataset.i; const fns = fnsOf(u).slice(); fns.splice(i, 1); st(u.id).footnotes = fns; save(); box.innerHTML = fnsHtml(u); bindFns(card, u); $('.en', card).innerHTML = enHtml(u); }));
  $('.add', box).addEventListener('click', () => {
    const sel = window.getSelection(); let anchor = '';
    if (sel && sel.rangeCount && !sel.isCollapsed && $('.en', card).contains(sel.anchorNode)) anchor = sel.toString().trim();
    const fns = fnsOf(u).slice(); fns.push({ anchor, text: '' }); st(u.id).footnotes = fns; save();
    box.innerHTML = fnsHtml(u); bindFns(card, u); $('.en', card).innerHTML = enHtml(u);
    const last = box.querySelectorAll('.fn .txt'); if (last.length) last[last.length - 1].focus();
  });
}
function bindMarks(card, u) {
  card.querySelectorAll('mark.flag').forEach(mk => {
    mk.addEventListener('mouseenter', () => card.querySelectorAll(`mark.flag[data-f="${mk.dataset.f}"]`).forEach(x => x.classList.add('pair-on')));
    mk.addEventListener('mouseleave', () => card.querySelectorAll('mark.flag.pair-on').forEach(x => x.classList.remove('pair-on')));
    mk.addEventListener('click', e => {
      e.preventDefault(); const f = (u.flags || [])[+mk.dataset.f]; if (!f) return;
      if (S.active !== u.id) setActive(u.id, false);
      S.tab = 'notes'; $('#tabs').querySelectorAll('button[data-tab]').forEach(x => x.classList.toggle('on', x.dataset.tab === 'notes')); renderInspector();
      let n = $(`#inspector [data-note="${f.note}"]`);
      if (!n) { const d = $('#inspector details.rest'); if (d) { d.open = true; n = $(`#inspector [data-note="${f.note}"]`); } }
      if (n) { n.scrollIntoView({ block: 'center' }); n.classList.add('flash'); setTimeout(() => n.classList.remove('flash'), 1600); }
    });
  });
}
function footnoteAtCaret(card, u) {
  const en = $('.en', card); const sel = window.getSelection(); let anchor = '';
  if (sel && sel.rangeCount && en.contains(sel.anchorNode)) {
    if (!sel.isCollapsed) anchor = sel.toString().trim();
    else {
      const r = document.createRange(); r.setStart(en, 0); r.setEnd(sel.anchorNode, sel.anchorOffset);
      const d = document.createElement('div'); d.appendChild(r.cloneContents()); d.querySelectorAll('.fnref').forEach(x => x.remove());
      const before = d.innerText.replace(/\u00a0/g, ' ');
      const m = before.match(/(\S+(?:\s+\S+){0,2})\s*$/); anchor = m ? m[1].replace(/[\s,.;:]+$/, '') : '';
    }
  }
  const fns = fnsOf(u).slice(); fns.push({ anchor, text: '' }); st(u.id).footnotes = fns; save();
  const box = $('.fns', card); box.innerHTML = fnsHtml(u); bindFns(card, u); en.innerHTML = enHtml(u); bindMarks(card, u);
  const last = box.querySelectorAll('.fn .txt'); if (last.length) last[last.length - 1].focus();
}
function setActive(id, scroll) {
  S.active = id;
  document.querySelectorAll('.unit').forEach(c => c.classList.toggle('on', c.dataset.id === id));
  document.querySelectorAll('#outline [data-units]').forEach(el => el.classList.toggle('on', (el.dataset.units || '').split(',').includes(id)));
  if (scroll) { const c = document.querySelector(`.unit[data-id="${id}"]`); if (c) { const h = c.previousElementSibling; (h && h.classList.contains('sabche') ? h : c).scrollIntoView({ block: 'start' }); } }
  renderInspector();
}

/* ---------------------------------------------------------------- inspector */
function renderInspector() {
  const u = U(S.active); const box = $('#inspector');
  if (!u) { box.innerHTML = '<div class="empty">Select a segment.</div>'; return; }
  if (u.pending) { box.innerHTML = `<div class="muted" style="margin-bottom:6px">${u.id}${u.hint ? ' · ' + esc(u.hint) : ''}</div><div class="empty">Not translated yet. Notes, grounding and the second opinion appear here once the skill has run on this page.</div>`; return; }
  const h = { notes: tabNotes, grounding: tabGrounding, mitra: tabMitra, reading: tabReading, terms: tabTerms }[S.tab];
  box.innerHTML = `<div class="muted" style="margin-bottom:6px">${u.id}${u.hint ? ' · ' + esc(u.hint) : ''}</div>` + h(u);
}
const NOTEHEAD = { Q: 'Open question', Var: 'Variant reading', Comm: 'Commentary', Alt: 'Alternative wording', Issue: 'Translation choice', Check: 'Changed in the check', Source: 'Source', MITRA: 'MITRA differs', Prior: 'Prior translation', Grounding: 'Grounding', Note: 'Note' };
function splitQ(text) {
  const m = text.match(/^(.*?)(?:[;,]\s*|\s)(?:alt\.|alternative:|alt:)\s*(.*)$/i);
  return m ? { main: m[1].trim(), alt: m[2].trim() } : { main: text, alt: '' };
}
const noteCard = (n, i, cls = '') => {
  const q = n.tag === 'Q' ? splitQ(n.text) : null;
  return `<div class="note ${cls}" data-note="${i}"><div class="nh"><span class="tag t-${n.tag}"${tip(n.tag, TAGMEAN[n.tag] || '')}>${n.tag}</span><b>${NOTEHEAD[n.tag] || n.tag}</b>${n.tag === 'Q' && n.resolved ? '<span class="st">settled</span>' : ''}</div>` +
    (q ? `<div>${md(q.main)}</div>${q.alt ? `<div class="alt"><span class="k">or</span> ${md(q.alt)}</div>` : ''}` : `<div>${md(n.text)}</div>`) + `</div>`;
};
function isPrimary(n) {
  if (n.tag === 'Q') return !n.resolved;
  if (n.tag === 'Var') return true;
  if (n.tag === 'Comm') return /\b(kept|rejected|not followed|differs|plain reading)\b/i.test(n.text);
  if (n.tag === 'Check') return /relation|agent|polarity|referent/i.test(n.text);
  if (n.tag === 'MITRA') return !/^agrees/i.test(n.text) && /agent|referent|relation|subject|object|negation|rejected on/i.test(n.text);
  return false;
}
function tabNotes(u) {
  const idx = u.notes.map((n, i) => [n, i]).filter(([n]) => n.tag !== 'Conf' && !(n.tag === 'MITRA' && /^agrees/i.test(n.text)));
  const primary = idx.filter(([n]) => isPrimary(n)), rest = idx.filter(([n]) => !isPrimary(n));
  if (!primary.length && !rest.length) return '<div class="empty">Nothing to look at: no open question, no variant, no disagreement.</div>';
  let out = primary.length ? primary.map(([n, i]) => noteCard(n, i)).join('') : '<div class="empty">No open question, no variant, no disagreement. The rest is for the record.</div>';
  if (rest.length) out += `<details class="rest"><summary>For the record · ${rest.length}</summary>${rest.map(([n, i]) => noteCard(n, i, 'small')).join('')}</details>`;
  return out;
}
function verdictOf(u) {
  const g = (u.fields.grounding || '').trim(); const lower = g.toLowerCase();
  if (!g) return { cls: 'none', head: 'No grounding recorded', body: '' };
  if (lower.startsWith('not queried')) return { cls: 'none', head: 'Not checked against commentaries', body: (g.replace(/^not queried[:;,]?\s*/i, '') || 'The author\'s own prose, which nothing in the canon glosses. Grounding calls are spent on citations, root-text lines and technical terms.') };
  if (lower.startsWith('none found')) return { cls: 'none', head: 'No commentary found for these words', body: g.replace(/^none found[:;,]?\s*/i, '') };
  if (lower.includes('service unavailable')) return { cls: 'warn', head: 'Dharmamitra was unavailable', body: 'Translated from the grammar alone; re-run the grounding later.' };
  return { cls: 'ok', head: 'Grounded in the tradition', body: g };
}
function commCard(n) {
  const followed = /\bfollowed\b/i.test(n.text) && !/not followed/i.test(n.text); const kept = /\b(kept|rejected|not followed|plain reading)\b/i.test(n.text);
  let t = n.text.replace(/;?\s*(followed|not followed|kept|plain reading kept)\.?\s*$/i, '').trim();
  const k = t.indexOf(': '); let who = '', what = t;
  if (k > 0 && k < 160) { who = t.slice(0, k); what = t.slice(k + 2); }
  const items = what.split(/;\s+/).map(x => x.trim()).filter(Boolean);
  const item = x => { const m = x.match(/^(.{2,60}?)\s=\s(.*)$/); return m ? `<li><span class="w">${esc(m[1])}</span> <span class="muted">→</span> ${md(m[2])}</li>` : `<li>${md(x)}</li>`; };
  return `<div class="card comm"><div class="kicker"><span>${who ? md(who) : 'Commentary'}</span>${followed ? '<span class="pill ok">followed</span>' : kept ? '<span class="pill kept">plain reading kept</span>' : ''}</div>${items.length > 1 ? `<ul class="gl">${items.map(item).join('')}</ul>` : md(what)}</div>`;
}
function tabGrounding(u) {
  const v = verdictOf(u);
  let out = `<div class="verdict ${v.cls}"><b>${esc(v.head)}</b>${v.body ? `<div>${esc(v.body)}</div>` : ''}</div>`;
  const src = u.notes.filter(n => n.tag === 'Source'), comm = u.notes.filter(n => n.tag === 'Comm'), vars = u.notes.filter(n => n.tag === 'Var');
  if (u.fields.source && !/not a citation/i.test(u.fields.source)) out += `<div class="card"><div class="kicker"><span>Quotation</span>${u.identify_summary ? `<span class="pill ${/yes/i.test(u.identify_summary) ? 'ok' : ''}"${tip('Source identification', u.identify_summary)}>${/yes, canonical/i.test(u.identify_summary) ? 'verbatim in the canon' : /yes/i.test(u.identify_summary) ? 'verbatim match' : 'no verbatim match'}</span>` : ''}</div><b>${esc(u.fields.source)}</b>${(u.cite || []).map(c => `<div class="cite"${tip('Citation forms', 'From dm.py cite: the reader form, the academic form and the register row, built from Dharmamitra\'s catalogue data.')}>${c.reader ? `<div><span class="k">reader</span> ${md(c.reader)}</div>` : ''}${c.academic ? `<div><span class="k">academic</span> ${md(c.academic)}</div>` : ''}${c.credits ? `<div class="muted small">${esc(c.credits)}</div>` : ''}</div>`).join('')}${src.map(n => `<div class="muted" style="margin-top:4px">${esc(n.text)}</div>`).join('')}</div>`;
  if (comm.length) out += `<h4>What the commentaries say</h4>` + comm.map(commCard).join('');
  if (vars.length) out += `<h4>Variant readings</h4>` + vars.map(n => `<div class="card"><div class="kicker"><span>Variant</span></div>${esc(n.text)}</div>`).join('');
  (u.gloss || []).forEach(g => {
    out += `<h4>Primary search <span class="badge"${tip('DharmaMitra primary search', 'Semantic search on dharmamitra.org without re-ranking and without an AI summary (the light operation, per Dharmamitra\'s terms). Hits are grouped by work and labelled GLOSS, QUOTE or NEAR; each links to the segment on dharmamitra.org.')}>${g.n_hits} hits in ${g.n_works} works</span></h4>` + glossCall(g);
  });
  if (u.explore.length) {
    u.explore.forEach(ex => {
      const hits = ex.hits.filter(h => !h.is_en), en = ex.hits.filter(h => h.is_en);
      out += `<h4>Passages that quote or gloss these words <span class="badge"${tip('Dharmamitra', 'Found with DharmaMitra search; each hit links to the segment on dharmamitra.org')}>${hits.length}</span></h4>`;
      out += hits.map(h => `<div class="hit"><div class="work ${/[ༀ-࿿]/.test(h.work) ? 'tibt' : ''}">${esc(h.work)}</div><div class="seg"><a href="${esc(h.url)}" target="_blank" rel="noopener">${esc(h.segid)}</a></div>${tibHtml(h.tib, h.wylie)}${h.rendering ? `<details><summary>machine rendering</summary><div class="rend">${esc(h.rendering)}</div></details>` : ''}</div>`).join('');
      if (en.length) out += `<div class="warn">${en.length} hit${en.length > 1 ? 's are' : ' is'} an existing English translation of this passage (${en.map(h => esc(h.segid)).join(', ')}): shown for reference only, per the brief's prior-translation policy.</div>`;
    });
  }
  if (u.segments.length) {
    out += `<h4>Commentary passages read <span class="badge"${tip('Dharmamitra', 'Segments fetched with their context so the gloss could be read in full')}>${u.segments.length}</span></h4>`;
    out += u.segments.map((s, i) => `<div class="segwin" data-i="${i}"><div class="sw-head"><span>${s.title ? `<b>${esc(s.title)}</b> ` : ''}${s.author ? `<span class="muted">${esc(s.author)}</span> ` : ''}<span class="muted">${esc(s.toh || s.file.replace(/^dm_segment_|\.txt$/g, ''))}</span></span><a class="ghostlink" href="${esc(s.url)}" target="_blank" rel="noopener">open</a></div><div class="rows">${segRows(s, false)}</div><button class="more" data-all="0">show the whole window (${s.rows.length} segments)</button></div>`).join('');
  }
  if (u.parallels.length) out += `<h4>Other witnesses of the line</h4>` + u.parallels.map(p => `<div class="muted" style="margin-bottom:4px">${esc(p.head)}</div><table class="t"><tr><th>match</th><th>segment</th><th>work</th></tr>${p.rows.slice(0, 8).map(r => `<tr><td>${r.score}</td><td style="font-family:ui-monospace,Menlo,monospace;font-size:11px">${esc(r.segid)}</td><td>${esc(r.toh)} ${esc(r.title)}</td></tr>`).join('')}</table>`).join('');
  const tech = [];
  if (u.identify) tech.push(`<h4>Source identification output</h4><pre class="mono">${esc(u.identify)}</pre>`);
  u.explore.forEach(ex => { if (ex.summary) tech.push(`<h4>Explore's AI summary</h4><div class="sum">${esc(ex.summary)}</div>`); });
  if (u.grounding.length) tech.push(`<h4>Grounding lines from the construal file</h4>` + u.grounding.map(g => `<div class="note" style="white-space:pre-wrap">${esc(g)}</div>`).join(''));
  if (tech.length) out += `<details style="margin-top:14px"><summary>Technical trail (for the skill's developer)</summary>${tech.join('')}</details>`;
  return out;
}
function glossHit(h) {
  const lm = LABELMEAN[h.label] || [h.label, ''];
  const rows = h.ctx.map(r => r.mark === 'gap' ? `<div class="row"><span class="rid"></span><span class="muted">${esc(r.wylie)}</span></div>` : `<div class="row ${r.mark}"><span class="rid">${esc(r.id)}</span>${S.prefs.script ? `<span class="tibt">${esc(r.tib)}</span>` : `<span>${esc(r.wylie)}</span>`}</div>`).join('');
  const n = h.ctx.filter(r => r.id).length, gl = h.ctx.some(r => r.mark === 'gloss');
  return `<div class="hit g-${h.label}"><div class="kicker"><span><span class="pill lbl ${h.label}"${tip(lm[0] + (h.kind ? ' · ' + h.kind : ''), lm[1])}>${h.label}${h.kind ? ' · ' + esc(h.kind) : ''}</span> ${esc(h.collection)}</span><a class="ghostlink" href="${esc(h.url)}" target="_blank" rel="noopener"${tip('Open on dharmamitra.org', h.segid)}>${esc(h.segid.split(':')[1] || h.segid)}</a></div>` +
    `<div class="work ${h.work_tib && S.prefs.script ? 'tibt' : ''}">${esc(S.prefs.script && h.work_tib ? h.work_tib : h.work)}</div>` +
    (h.note && h.is_en ? `<div class="warn">${esc(h.note)}</div>` : '') +
    tibHtml('…' + h.tib + '…', '…' + h.wylie + '…') +
    (n ? `<details${gl ? ' open' : ''}><summary>${gl ? 'the gloss, read in context' : 'the passage around the hit'} · ${n} segments</summary><div class="rows">${rows}</div></details>` : '') +
    (h.more.length ? `<div class="muted small">also at ${h.more.map(esc).join(', ')}</div>` : '') + (h.note && !h.is_en ? `<div class="muted small">${esc(h.note)}</div>` : '') + `</div>`;
}
function glossCall(g) {
  const main = g.hits.filter(h => h.label !== 'NEAR'), near = g.hits.filter(h => h.label === 'NEAR');
  return `<div class="gcall"><div class="muted small gq">Query (${g.syllables} syllables): <i>${esc(g.query)}</i>${g.root ? `<br>Root work with the verbatim line: ${esc(g.root)}` : ''}${g.context_note ? `<br>${esc(g.context_note)}` : ''}${g.notes.map(x => `<br>${esc(x)}`).join('')}</div>` +
    (main.length ? main.map(glossHit).join('') : '<div class="empty">No work among the hits quotes or glosses these words.</div>') +
    (near.length ? `<details class="near"><summary>${near.length} work${near.length > 1 ? 's' : ''} near in sense only (NEAR)</summary>${near.map(glossHit).join('')}</details>` : '') + `</div>`;
}
function segRows(s, all) { const ai = s.rows.findIndex(r => r.active); const lo = Math.max(0, ai - 4), hi = Math.min(s.rows.length, ai + 6); return s.rows.slice(all ? 0 : lo, all ? s.rows.length : hi).map(r => `<div class="row ${r.active ? 'active' : ''}"><span class="rid">${esc(r.id)}</span>${S.prefs.script ? `<span class="tibt">${esc(r.tib)}</span>` : `<span>${esc(r.wylie)}</span>`}</div>`).join(''); }
function tabMitra(u) {
  const note = u.notes.find(n => n.tag === 'MITRA');
  return `<div class="mitra-cmp"><div class="box"><small>Dharmamitra MITRA, literal setting</small>${u.mitra ? md(u.mitra) : '<span class="muted">no MITRA output saved for this segment</span>'}</div></div>` +
    (note ? `<h4>What was done with the difference</h4>${noteCard(note)}` : '') +
    `<p class="muted">MITRA reads content words well and relations unreliably. A disagreement is a question to settle from the grammar, never a vote; the skill does not change a reading on MITRA's word alone.</p>`;
}
const READLABEL = { SPINE: 'Who does what', RELATIONS: 'How the clauses connect', 'NEG/QUANT': 'Negations and quantities', TERMS: 'Terms', CONSTRUAL: 'Plain construal', VERSE: 'Verse notes', 'VERSE-NOTES': 'Verse notes', CITATION: 'Citation', GROUNDING: 'Grounding', VAR: 'Variants', DOUBTS: 'Could also be read as' };
function tabReading(u) {
  if (!u.construal.length) return '<div class="empty">No reading sketch was saved for this segment.</div>';
  const main = u.construal.filter(c => !/^Q\d+|^Var|^Issue/.test(c.key) && !['WORDS', 'FORM', 'GENRE', 'REGISTER', 'SOURCE', 'CLAUSES', 'UNIT'].includes(c.key));
  const qs = u.construal.filter(c => /^Q\d+/.test(c.key)); const other = u.construal.filter(c => /^Var|^Issue/.test(c.key));
  const list = (txt, sep) => { const parts = txt.split(sep).map(x => x.trim()).filter(Boolean); return parts.length > 1 ? `<ul>${parts.map(x => `<li>${esc(x)}</li>`).join('')}</ul>` : esc(txt); };
  const pairs = (txt, sep) => { let parts = txt.split(sep).map(x => x.trim()).filter(Boolean); if (parts.length < 2 && /;\s/.test(txt)) parts = txt.split(/;\s+/).map(x => x.trim()).filter(Boolean); const rows = parts.map(x => { const m = x.match(/^(.{1,70}?)\s=\s(.*)$/); return m ? [m[1], m[2]] : ['', x]; }); return `<table class="t pairs">${rows.map(([l, r]) => `<tr><td class="w">${esc(l)}</td><td>${md(r)}</td></tr>`).join('')}</table>`; };
  let out = '';
  main.forEach(c => {
    const body = c.key === 'RELATIONS' ? pairs(c.text, ' | ') : c.key === 'TERMS' ? pairs(c.text, ' · ') : c.key === 'SPINE' ? `<div class="spine">${md(c.text)}</div>` : md(c.text);
    out += `<h4>${esc(READLABEL[c.key] || c.key)}</h4>${body}`;
  });
  if (qs.length) out += `<h4>Could also be read as</h4>${qs.map(c => { const q = splitQ(c.text); return `<div class="note"><div>${md(q.main)}</div>${q.alt ? `<div class="alt"><span class="k">or</span> ${md(q.alt)}</div>` : ''}</div>`; }).join('')}`;
  if (other.length) out += `<h4>Also noted</h4>` + other.map(c => `<div class="note">${esc(c.text)}</div>`).join('');
  if (S.data.check.length) out += `<details style="margin-top:14px"><summary>Fidelity check of the whole page</summary>${S.data.check.map(c => `<div class="muted" style="margin:3px 0">${esc(c)}</div>`).join('')}</details>`;
  return out;
}
function tabTerms(u) {
  if (!u.terms.length) return '<div class="empty">No glossary term is bound in this segment.</div>';
  const alts = u.notes.filter(n => n.tag === 'Alt');
  const text = textOf(u).join(' ');
  const state = t => termInText(t.english, text) ? '' : (t.alts || []).some(a => termInText(a, text)) ? `<span class="pill kept"${tip('Alternative used', 'An alternative recorded for this term is in the text, not the bound rendering.')}>alternative used</span>` : `<span class="pill warn"${tip('Not in this translation', 'The glossary binds this rendering, but the current text of this segment does not contain it. Either the term is rendered differently here (check), or the Tibetan word occurs in another sense.')}>not in the text</span>`;
  return `<table class="t"><tr><th>Tibetan</th><th>bound rendering</th><th>also possible here</th></tr>${u.terms.map(t => `<tr><td class="w">${esc(t.wylie)}</td><td><b>${esc(t.english)}</b> ${state(t)}${t.clutter || !t.note ? '' : `<div class="muted small">${md(t.note)}</div>`}</td><td>${(t.alts || []).length ? t.alts.map(x => `<span class="syn">${esc(x)}</span>`).join(' ') : '<span class="muted">—</span>'}</td></tr>`).join('')}</table>` +
    (alts.length ? `<h4>Alternative wordings noted for this segment</h4>${alts.map(n => `<div class="note small">${md(n.text)}</div>`).join('')}` : '') +
    `<p class="muted">A term decided once is reused in every later segment. “Also possible” lists the alternatives recorded when the term was decided; add your own in Glossary → Import.</p>`;
}

/* ---------------------------------------------------------------- project panels */
function openModal(title, html) { $('#modal-title').textContent = title; $('#modal-body').innerHTML = html; $('#modal').classList.remove('hidden'); }
function closeModal() { $('#modal').classList.add('hidden'); }
function panel(name) {
  const d = S.data;
  if (name === 'glossary') {
    openModal(`Glossary · ${d.glossary.length} terms, ${d.titles.length} titles`,
      `<div class="toolbar"><button id="gl-import" class="primary">Import glossary…</button><span class="muted">Rows go into the run's glossary file, which the skill reads on its next page, so your house terms bind from then on.</span></div>` + consistencyHtml() +
      (d.titles.length ? `<h4>Fixed English short titles</h4><table class="t"><tr><th>English</th><th>Tibetan</th><th>Sanskrit</th><th>locator</th></tr>${d.titles.map(t => `<tr><td><i>${esc(t.english)}</i></td><td class="w">${esc(t.wylie)}</td><td>${esc(t.iast)}</td><td class="muted">${esc(t.locator)}</td></tr>`).join('')}</table>` : '') +
      `<h4>Terms</h4><table class="t"><tr><th>Tibetan</th><th>English</th><th>note</th></tr>${d.glossary.map(g => `<tr><td class="w">${esc(g.wylie)}</td><td><b>${esc(g.english)}</b></td><td class="muted">${esc(g.note)}</td></tr>`).join('')}</table>`);
    $('#gl-import').addEventListener('click', importGlossaryUI);
    $('#modal-body').querySelectorAll('a.goto').forEach(a => a.addEventListener('click', e => { e.preventDefault(); closeModal(); S.tab = 'terms'; $('#tabs').querySelectorAll('button[data-tab]').forEach(x => x.classList.toggle('on', x.dataset.tab === 'terms')); setActive(a.dataset.id, true); }));
  }
  if (name === 'sources') openModal('Sources register', d.sources.length ? `<p class="muted">Back matter, keyed by each quotation's opening words. Locators live here, not in footnotes, so they never disturb the reader.</p><table class="t"><tr><th>segment</th><th>opening words</th><th>work and locator</th></tr>${d.sources.map(s => `<tr><td>${esc(s.unit_id)}</td><td>“${esc(s.opening_words)}”</td><td>${esc(s.work_and_locator)}</td></tr>`).join('')}</table>` : '<div class="empty">No register rows yet.</div>');
  if (name === 'works') openModal('Works and people met in this run',
    `<h4>Commentaries read</h4>` + (d.works.length ? d.works.map(w => `<div class="hit"><div class="work ${/[ༀ-࿿]/.test(w.title) ? 'tibt' : ''}">${esc(w.title)}</div><div class="muted">${esc(w.title_wylie)}</div><div>${w.from_search ? `<span class="muted">met through the primary search:</span> ${Object.entries(w.labels || {}).map(([l, n]) => `<span class="pill lbl ${l}">${l} × ${n}</span>`).join(' ')} <span class="muted">in ${(w.units || []).join(', ')}</span>` : `<b>${esc(w.author || 'author not in the catalogue')}</b>`}${w.collection ? ' · ' + esc(w.collection) : ''}${w.genre ? ' · ' + esc(w.genre) : ''}</div><div class="seg">${w.url ? `<a href="${esc(w.url)}" target="_blank" rel="noopener">Dharmamitra text</a>` : ''}${w.source ? ` · <a href="${esc(w.source)}" target="_blank" rel="noopener">source PDF</a>` : ''}${w.bdrc ? ` · BDRC ${esc(w.bdrc)}` : ''}</div></div>`).join('') : '<div class="empty">none</div>') +
    `<h4>From the brief</h4><div class="note">${esc(d.work)}</div>` +
    `<p class="muted">Planned: Treasury of Lives and BDRC entries for each author and person named, shown as a two-line summary with the link. Only catalogue data is shown until then; no biography is generated.</p>`);
  if (name === 'activity') openModal('Run log', `<p class="muted">What the skill read and called, with times. Useful when a run was interrupted and resumed.</p><pre class="mono" style="max-height:70vh">${esc(d.runlog || 'no runlog')}</pre>`);
  if (name === 'about') openModal('About Tiger CAT',
    `<p>A local editor for translations made with the <b>tibetan-translate</b> Claude Code skill. The skill writes plain files; this app reads them, lets you revise the English and the footnotes segment by segment, and exports a Word file with real footnotes through the skill's own exporter.</p>
     <p><b>No model is called from this app.</b> The translation run happens in your own Claude Code, on your own account. The app only reads and writes files in the project folder, and reloads when the skill writes a new page.</p>
     <p><b>Dharmamitra resources used by the runs shown here:</b> DharmaMitra primary semantic search without re-ranking or AI summary (source identification and grounding, the light operation on Dharmamitra's side), the DharmaNexus text view and parallels (reading a gloss in context, variant readings), the MITRA translation model as a second opinion, and the catalogue data behind the citation forms, all from <a href="https://dharmamitra.org" target="_blank" rel="noopener">dharmamitra.org</a>; the MITRA Tibetan Lexicon (CC BY-SA 4.0). Explore's summaries are used only on explicit request. Each resource is named at the stage where it was used.</p>
     <p class="muted">Project folder: <code>${esc(d.run_dir)}</code></p>
     <p class="muted">Free and open source, for the Vikramashila translation group and anyone who finds it useful. If it helps your work, consider supporting <a href="https://dharmamitra.org" target="_blank" rel="noopener">Dharmamitra</a>, whose research service makes the grounding possible.</p>`);
}
function consistencyHtml() {
  const rows = [];
  d_units().forEach(u => { if (u.pending) return; const text = textOf(u).join(' '); u.terms.forEach(t => { if (!termInText(t.english, text)) rows.push({ t, u, alt: (t.alts || []).find(a => termInText(a, text)) }); }); });
  if (!rows.length) return `<h4>Consistency</h4><div class="muted">Every bound rendering occurs where its Tibetan term does. (Checked on the current text, your edits included.)</div>`;
  const by = {}; rows.forEach(r => (by[r.t.wylie] = by[r.t.wylie] || { t: r.t, us: [] }).us.push(r));
  return `<h4>Consistency <span class="badge">${rows.length}</span></h4><p class="muted">Segments whose current text lacks the glossary's bound rendering of a term that occurs in their Tibetan. A rendering can differ for a reason (another sense, a heading form); this is a check, not a verdict.</p><table class="t"><tr><th>Tibetan</th><th>bound rendering</th><th>missing in</th></tr>${Object.values(by).map(({ t, us }) => `<tr><td class="w">${esc(t.wylie)}</td><td><b>${esc(t.english)}</b></td><td>${us.map(r => `<a href="#" class="goto" data-id="${r.u.id}">${r.u.id}</a>${r.alt ? ` <span class="muted small">(“${esc(r.alt)}”)</span>` : ''}`).join(', ')}</td></tr>`).join('')}</table>`;
}
function d_units() { return (S.data && S.data.units) || []; }
function importGlossaryUI() {
  openModal('Import a glossary',
    `<p class="muted">One term per line: <b>Tibetan</b> (script or Wylie), tab or comma, <b>English</b>, optionally a note. A header row is skipped. Rows already present (same Wylie) are skipped.</p>
     <div class="toolbar"><input type="file" id="gl-file" accept=".tsv,.csv,.txt"> <span class="muted">or paste below</span></div>
     <textarea id="gl-text" placeholder="byang chub sems&#9;bodhicitta&#9;house style: anglicized&#10;ཐུགས་རྗེ་ཆེན་པོ&#9;great compassion"></textarea>
     <div class="toolbar"><button id="gl-go" class="primary">Import</button><span id="gl-status" class="muted"></span></div>`);
  $('#gl-file').addEventListener('change', e => { const f = e.target.files[0]; if (f) f.text().then(t => $('#gl-text').value = t); });
  $('#gl-go').addEventListener('click', async () => {
    const text = $('#gl-text').value; if (!text.trim()) return;
    $('#gl-status').textContent = 'Importing…';
    try {
      const r = await (await fetch('/api/glossary/import' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }) })).json();
      if (!r.ok) { $('#gl-status').textContent = 'Failed: ' + (r.error || r.log || 'unknown'); return; }
      await loadData(); renderAll(); closeModal(); toast(`Glossary: ${r.added} added, ${r.skipped} already present. Written to the run's glossary file.`);
    } catch (e) { $('#gl-status').textContent = 'Import needs the local server.'; }
  });
}

/* ---------------------------------------------------------------- export and refresh */
async function doExport(mode) {
  const notes = $('#exp-notes').checked, headers = $('#exp-headers').checked; toast('Exporting…', 20000);
  try {
    const r = await (await fetch('/api/export' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode, notes, headers }) })).json();
    if (r.ok) toast(`Wrote <a href="${esc(r.file)}" download>${esc(r.name)}</a>${r.log ? ' · ' + esc(r.log) : ''}`, 12000); else toast('Export failed: ' + esc(r.error || 'unknown'), 10000);
  } catch (e) { toast('Export needs the local server (tools/serve.py).'); }
}
async function pollRefresh() {
  if (!S.slug) return;
  try {
    const r = await (await fetch('/api/refresh' + P())).json();
    if (r.job) { S.job = r.job; renderJob(); }
    renderUsage();
    if (r.rebuilt) { const act = S.active; await loadData(); if (!U(act)) S.active = S.data.units[0]?.id; renderAll(); toast('The run has new output; reloaded.'); }
  } catch (e) {}
}

/* ---------------------------------------------------------------- translation runs */
function renderJob() {
  const j = S.job || { state: 'idle' }; const el = $('#jobbar');
  if (!S.slug || j.state === 'idle') { el.classList.add('hidden'); document.body.classList.remove('has-job'); return; }
  el.classList.remove('hidden'); el.className = j.state + (j.needs_login ? ' needs-login' : ''); document.body.classList.add('has-job');
  const icon = j.state === 'running' ? '●' : j.state === 'waiting' ? '◔' : j.state === 'error' ? '✕' : '✓';
  const text = j.needs_login ? 'Claude Code is not signed in yet. Click here to sign in (one time), then start the run again.' : (j.message || j.state) + (j.last && j.state === 'running' ? '  ·  ' + j.last.replace(/^tool: /, '') : '');
  $('#job-text').textContent = icon + '  ' + text;
  $('#job-text').onclick = j.needs_login ? signIn : null;
  const prog = $('#job-progress');
  if (j.state === 'running' && j.stages) {
    const st = j.stage || 0; const mm = s => s == null ? '' : Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
    const label = j.stages[st] + (st === 3 && j.grounding_calls ? ` (${j.grounding_calls} call${j.grounding_calls > 1 ? 's' : ''})` : '');
    prog.classList.remove('hidden');
    prog.innerHTML = `<div class="steps-bar"${tip('Stage of this page', 'Read off the skill\'s own tool calls as they happen: no extra tokens. Each page goes through these stages in order; the model\'s reasoning between them is the part nobody can time in advance.')}>${j.stages.slice(1).map((s, i) => `<span class="${i + 1 < st ? 'done' : i + 1 === st ? 'now' : ''}" title="${esc(s)}"></span>`).join('')}</div><span class="stage">${esc(label)}</span><span class="muted">${mm(j.elapsed_s)}${j.typical_s ? ' · usually ≈ ' + Math.round(j.typical_s / 60) + ' min a page' : ''}</span>`;
  } else { prog.classList.add('hidden'); prog.innerHTML = ''; }
  $('#job-stop').classList.toggle('hidden', !['running', 'waiting', 'starting'].includes(j.state));
}
async function renderUsage() {
  const box = $('#usage-body'); if (!box) return;
  let u; try { const r = await fetch('/api/usage'); if (!r.ok) throw 0; u = await r.json(); } catch (e) { box.textContent = 'Usage figures appear after the next start of the server.'; return; }
  const fmt = n => n >= 1e6 ? (n / 1e6).toFixed(2) + 'M' : n >= 1e3 ? Math.round(n / 1e3) + 'k' : String(n);
  const meter = (label, right, used, cap, tipTitle, tipBody) => {
    const pct = cap ? Math.min(100, Math.round(100 * used / cap)) : 0; const cls = pct >= 100 ? 'full' : pct >= 75 ? 'warn' : '';
    return `<div class="meter"${tip(tipTitle, tipBody)}><div class="lbl"><span>${label}</span><span>${right}</span></div><div class="bar ${cap ? '' : 'unknown'}"><div class="${cls}" style="width:${cap ? pct : 35}%"></div></div></div>`;
  };
  const sess = u.session, week = u.week;
  const sessRight = sess.exhausted ? `limit hit · resets ${sess.reset}` : (sess.ceiling ? `${fmt(sess.tokens)} of ≈${fmt(sess.ceiling)}` : fmt(sess.tokens) + ' tokens');
  const sessTip = (sess.reset ? `Window resets at ${sess.reset}. ` : 'Rolling five-hour window. ') + (sess.ceiling ? `The ceiling (≈${fmt(sess.ceiling)} tokens) is what this app had used when a session limit was last hit, so it is an estimate from experience, not a published figure.` : 'No session limit has been hit from this app yet, so the ceiling is unknown; the bar fills once one is observed.') + ' Tokens counted: output, fresh input and cache writes.';
  const weekRight = week.ceiling ? `${fmt(week.tokens)} of ≈${fmt(week.ceiling)}` : `${fmt(week.tokens)} tokens · ${week.pages} page${week.pages === 1 ? '' : 's'}`;
  box.innerHTML = meter('Session window', sessRight, sess.exhausted ? 1 : sess.tokens, sess.exhausted ? 1 : sess.ceiling, 'Session window (five hours)', sessTip) +
    meter('This week', weekRight, week.tokens, week.ceiling, 'Last seven days', (week.ceiling ? 'The ceiling is what this app had used when a weekly limit was last hit.' : 'No weekly limit has been hit from this app yet, so the ceiling is unknown.') + ` ≈ $${week.cost.toFixed(2)} at API list prices, for scale.`) +
    `<p class="muted" style="margin:4px 0 0">Only what this app ran. Other Claude sessions share the same limits; exact figures: <code>/usage</code> in Claude Code.</p>`;
}
async function refreshClaudeStatus() {
  try {
    const c = await (await fetch('/api/claude/status' + (S.slug ? P() : ''))).json(); S.claude = c;
    $('#claude-status').innerHTML = c.logged_in ? '<span class="status-ok">✓ Claude Code is signed in</span>' : `<span class="status-bad">✕ ${esc(c.message)}</span>`;
    $('#btn-login').classList.toggle('hidden', !!c.logged_in);
  } catch (e) {}
}
async function signIn() {
  const r = await (await fetch('/api/claude/login' + (S.slug ? P() : ''), { method: 'POST', body: '{}' })).json();
  if (!r.ok) { toast('Could not start the sign-in: ' + esc(r.error || '')); return; }
  openModal('Sign in to Claude Code', `<ol class="steps"><li>A Terminal window has opened and is running the sign-in.</li><li>Your browser opens the Claude sign-in page; sign in with the account you use for Claude Code.</li><li>Come back here. This box closes by itself once the sign-in is done.</li></ol><p class="muted" id="si-status">Waiting for the sign-in…</p>`);
  const poll = async () => {
    const c = await (await fetch('/api/claude/status' + (S.slug ? P() : ''))).json();
    if (c.logged_in) { closeModal(); toast('Claude Code is signed in. You can start a translation now.', 8000); refreshClaudeStatus(); if (S.job && S.job.needs_login) { S.job = { state: 'idle' }; renderJob(); } return; }
    if ($('#si-status')) setTimeout(poll, 3000);
  };
  setTimeout(poll, 3000);
}
async function runAction(what) {
  if (what === 'login') { signIn(); return; }
  if (!S.slug) return;
  if (what === 'stop') { await fetch('/api/run/stop' + P(), { method: 'POST', body: '{}' }); toast('Stopping after the current step.'); return; }
  if (what === 'log') { const r = await (await fetch('/api/run/log' + P())).json(); openModal('Run log', `<p class="muted">${esc(r.file || '')}</p><pre class="mono" style="max-height:70vh">${esc(r.log || 'no run yet')}</pre>`); return; }
  if (what === 'prompt') { copyPrompt(); return; }
  const pend = S.data.pending || 0; if (!pend) { toast('Every segment is translated already.'); return; }
  const r = await (await fetch('/api/run' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scope: what }) })).json();
  if (!r.ok) { toast('Could not start: ' + esc(r.error || '')); return; }
  toast(what === 'all' ? `Translating ${pend} segments in pages of ${S.data.page_size || ''}…` : 'Translating the next page…'); pollJob();
}
async function pollJob() { try { S.job = await (await fetch('/api/run' + P())).json(); renderJob(); renderUsage(); if (['running', 'waiting', 'starting'].includes(S.job.state)) setTimeout(pollJob, 4000); else { await loadProjects(); } } catch (e) {} }
async function copyPrompt() {
  const r = await (await fetch('/api/project' + P())).json(); const pj = r.project; const b = pj.brief || {};
  const pend = S.data.units.filter(u => u.pending).map(u => u.id); const page = pend.slice(0, pj.page_size || 10);
  if (!page.length) { toast('Nothing left to translate.'); return; }
  const text = `Open Claude Code in this folder: ${r.run_dir}\n\nThen paste:\n\nTranslate units ${page[0]}–${page[page.length - 1]} of ${S.slug}.units.md with the tibetan-translate skill (pipeline v2), end to end. The brief is in CLAUDE.md here (Pass 0 answered; do not ask). Work name: ${S.slug}. Append the finished unit blocks to final.md, keep the glossary, register and runlog in this folder, save every dm.py output as dm_<command>_<unit>.txt. Model ${pj.model} at ${pj.effort} effort. Reply with only the check line and the grounding summary.`;
  try { await navigator.clipboard.writeText(text); toast('Prompt copied. Open Claude Code in the run folder and paste it; the app reloads when final.md changes.', 9000); }
  catch (e) { openModal('Prompt for Claude Code', `<textarea class="mono" style="width:100%;min-height:200px">${esc(text)}</textarea>`); }
}

/* ---------------------------------------------------------------- project wizard, settings, help */
function briefFields(b = {}, pj = {}) {
  const opt = (list, v) => list.map(x => `<option ${x === v ? 'selected' : ''}>${x}</option>`).join('');
  return `<label>Target language</label><select name="language"><option value="en" ${(b.language || 'en') === 'en' ? 'selected' : ''}>English</option><option value="de" ${b.language === 'de' ? 'selected' : ''}>German (Deutsch)</option></select>
    <div class="hint">The translation, footnotes and short titles come out in this language; the editor's notes stay in English. German needs the skill's German reference, see docs/skill-update-prompt.md.</div>
    <label>Audience</label><select name="audience">${opt(S.meta.audiences || [], b.audience || 'seasoned practitioner')}</select>
    <div class="hint">Decides the register ceiling, the Sanskrit treatment, the verse form and what gets a footnote.</div>
    <label>Purpose</label><select name="purpose">${opt(S.meta.purposes || [], b.purpose || 'study aid')}</select>
    <label>House style</label><textarea name="style" placeholder="e.g. Sanskrit technical terms anglicized without diacritics; Tibetan names phonetic; no brackets or Wylie in the body; verse in citation mode; no contractions">${esc(b.style || '')}</textarea>
    <label>Footnotes</label><select name="notes">${opt(S.meta.notes || [], b.notes || 'reader')}</select>
    <div class="hint">scholarly: locators and variants · reader: what unlocks the passage · minimal · none. Sources always go to the register.</div>
    <label>Source context</label><textarea name="context" placeholder="work, author, genre, where the passage sits, who speaks to whom, known commentaries">${esc(b.context || '')}</textarea>
    <label>Existing translations</label><select name="prior"><option value="consult" ${b.prior === 'consult' ? 'selected' : ''}>consult where found and cite</option><option value="ignore" ${b.prior === 'ignore' ? 'selected' : ''}>ignore (do not read)</option><option value="adapt" ${b.prior === 'adapt' ? 'selected' : ''}>may adapt (permission recorded)</option></select>
    <label>Model</label><div class="row"><select name="model"><option value="opus" ${(pj.model || 'opus') === 'opus' ? 'selected' : ''}>Claude Opus</option><option value="fable" ${pj.model === 'fable' ? 'selected' : ''}>Claude Fable</option></select>
      <select name="effort"><option value="max" ${pj.effort === 'max' ? 'selected' : ''}>max effort (calibrated; ~300–400k tokens a page)</option><option value="xhigh" ${(pj.effort || 'xhigh') === 'xhigh' ? 'selected' : ''}>xhigh effort (~260k a page; measured as faithful)</option><option value="high" ${pj.effort === 'high' ? 'selected' : ''}>high (cheaper; one major error every page or two)</option></select>
      <select name="page_size">${[6, 8, 10, 12].map(n => `<option ${n === (pj.page_size || 10) ? 'selected' : ''}>${n}</option>`).join('')}</select><span class="muted">segments per page</span></div>
    <label>Segment length</label><div class="row"><select name="max_syl">${[30, 45, 60, 70, 90].map(n => `<option ${n === (pj.max_syl || 45) ? 'selected' : ''}>${n}</option>`).join('')}</select><span class="muted">syllables per prose segment at most; a line is split only at a sentence end (shad). Stanzas and headings are kept whole.</span></div>
    <div class="hint">The run uses your own Claude Code login on this Mac. Each page is one headless session; the app waits out usage limits and resumes from the saved files.</div>`;
}
function readForm(root) { const o = {}; root.querySelectorAll('[name]').forEach(el => o[el.name] = el.value); return o; }
function newProjectUI() {
  openModal('New project', `<div class="form" id="np">
    <label>Title</label><input type="text" name="title" placeholder="e.g. Rays of Sunlight, chapter 1">
    <label>Tibetan text</label><textarea name="text" class="tib" placeholder="Paste the Tibetan here, in script or in Wylie…"></textarea>
    <div class="hint"><input type="file" id="np-file" accept=".txt,.md"> or choose a .txt file · The text is split into segments (stanzas and sentence periods); you can correct the split in Settings afterwards.</div>
    ${briefFields({}, {})}
    <label>Glossary (optional)</label><textarea name="glossary" class="mono" placeholder="tibetan&#9;english&#9;note (one per line; script or Wylie)"></textarea>
    <label></label><div class="row"><button id="np-go" class="primary">Create project</button><span id="np-status" class="muted"></span></div></div>`);
  $('#np-file').addEventListener('change', e => { const f = e.target.files[0]; if (f) f.text().then(t => $('#np [name=text]').value = t); });
  $('#np-go').addEventListener('click', async () => {
    const f = readForm($('#np')); if (!f.text.trim()) { $('#np-status').textContent = 'Paste a text first.'; return; }
    $('#np-status').textContent = 'Segmenting…';
    const body = { title: f.title, text: f.text, glossary: f.glossary, model: f.model, effort: f.effort, page_size: f.page_size, max_syl: f.max_syl, brief: { language: f.language, audience: f.audience, purpose: f.purpose, style: f.style, notes: f.notes, context: f.context, prior: f.prior } };
    const r = await (await fetch('/api/projects', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })).json();
    if (!r.ok) { $('#np-status').textContent = 'Failed: ' + (r.error || r.log || ''); return; }
    closeModal(); await loadProjects(); await openProject(r.slug); toast(`Project created: ${r.units} segments. Check them in Settings, then Translate.`, 8000);
  });
}
async function settingsUI() {
  if (!S.slug) return;
  const r = await (await fetch('/api/project' + P())).json(); const pj = r.project;
  openModal('Project settings', `<div class="form" id="ps">
    <label>Title</label><input type="text" name="title" value="${esc(pj.title)}">
    ${briefFields(pj.brief || {}, pj)}
    <label>Segments</label><textarea name="units" class="mono" style="min-height:220px">${esc(r.units_text)}</textarea>
    <div class="hint">One segment per line: id, a hint in parentheses, the Tibetan. Merge or split lines as you like; keep the ids in order (a long period may be split into sub-units U10a, U10b … as the skill does). Segments already translated keep their translation only if the id and text stay the same. <button id="ps-reseg" class="ghost" style="padding:1px 6px">Re-segment from the source text</button> with the segment length chosen above (one segment per source line or sentence group, headings on their own; translations of changed ids drop out of view)</div>
    <label>Claude Code</label><div class="row"><span id="ps-check-out" class="muted">checking…</span><button id="ps-login">Sign in to Claude Code</button></div>
    <div class="hint">Runs use Claude Code on this Mac with your own account. Sign in once; the app remembers it.</div>
    <label>Run folder</label><div class="muted">${esc(r.run_dir)}</div>
    <label></label><div class="row"><button id="ps-save" class="primary">Save</button><button id="ps-delete">Delete project…</button><span id="ps-status" class="muted"></span></div></div>`);
  (async () => { const c = await (await fetch('/api/claude/status' + P())).json(); $('#ps-check-out').innerHTML = `<span class="${c.logged_in ? 'status-ok' : 'status-bad'}">${esc(c.message)}</span>`; $('#ps-login').classList.toggle('hidden', !!c.logged_in); })();
  $('#ps-login').addEventListener('click', signIn);
  $('#ps-reseg').addEventListener('click', async () => {
    if (!confirm('Re-segment from the stored source text? Segment ids change; translations already made stay in final.md but only show where the ids still match.')) return;
    const x = await (await fetch('/api/project/resegment' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ max_syl: $('#ps [name=max_syl]').value }) })).json();
    if (!x.ok) { toast('Could not re-segment: ' + esc(x.error || '')); return; }
    closeModal(); await loadProjects(); await openProject(S.slug); toast(`Re-segmented: ${x.units} segments.`);
  });
  $('#ps-save').addEventListener('click', async () => {
    const f = readForm($('#ps')); $('#ps-status').textContent = 'Saving…';
    const body = { title: f.title, model: f.model, effort: f.effort, page_size: f.page_size, max_syl: f.max_syl, units: f.units, brief: { language: f.language, audience: f.audience, purpose: f.purpose, style: f.style, notes: f.notes, context: f.context, prior: f.prior } };
    const x = await (await fetch('/api/project' + P(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })).json();
    if (!x.ok) { $('#ps-status').textContent = 'Failed: ' + (x.error || x.log || ''); return; }
    closeModal(); await loadProjects(); await openProject(S.slug); toast('Settings saved.');
  });
  $('#ps-delete').addEventListener('click', async () => {
    if (!confirm('Delete this project and all its files? This cannot be undone.')) return;
    await fetch('/api/project/delete' + P(), { method: 'POST', body: '{}' }); S.slug = ''; await loadProjects();
    if (S.projects.length) await openProject(S.projects[0].slug); else showWelcome();
  });
}
function helpUI() {
  openModal('How to use Tiger CAT', `<ol class="steps">
    <li><b>Create a project</b> (＋ in the top bar): paste the Tibetan in script or Wylie, set the brief the skill needs (audience, purpose, house style, footnote policy, source context), choose the model and the effort, and optionally paste a glossary of house terms. The app splits the text into segments.</li>
    <li><b>Check the segments</b> in ⚙ Settings: one line each; merge or split as you like. Long periods are better split at a clause boundary.</li>
    <li><b>Translate</b>: "next page" runs one page of segments through your own Claude Code with the tibetan-translate skill, headless, in the project's run folder; "all remaining pages" runs page after page and waits out usage limits. The status chip in the top bar shows what is happening; the run log has the detail. The first time, choose "Sign in to Claude Code" in the same menu: a Terminal window and your browser open, you sign in with your Claude account, done. Prefer to run it yourself? "Copy the prompt" gives you a prompt to paste into Claude Code opened in the run folder; the app reloads when the skill writes.</li>
    <li><b>Review</b>: each segment shows its Tibetan beside the English. Edit the English directly; add footnotes; tick "reviewed". Notes, Grounding, MITRA, Reading and Terms on the right explain the choices; Grounding shows what the primary search found, labelled GLOSS, QUOTE or NEAR, with the commentary passage readable in context. "Needs review" hides what you have ticked; the search box finds a word in the Tibetan, the Wylie, the English or the notes. A segment you have changed shows "edited" and a revert button. Terms marks a bound rendering missing from the text; Glossary has the same check for the whole project.</li>
    <li><b>Export</b>: English only or aligned Tibetan–English Word files with real footnotes, optionally with the editor's notes as an appendix.</li></ol>
    <h4>Keyboard</h4><p class="muted"><code>j</code>/<code>k</code> or arrows: next / previous segment · <code>Enter</code>: edit the active translation · <code>Esc</code>: leave the editor · <code>r</code>: toggle reviewed · <code>⌘⇧F</code> while typing: footnote at the cursor · <code>1</code>–<code>5</code>: Notes, Grounding, MITRA, Reading, Terms · <code>n</code>: needs review · <code>s</code>: script / Wylie · <code>t</code>: translate the next page · <code>e</code>: export menu · <code>g</code>: glossary · <code>/</code>: search · <code>[</code> <code>]</code>: hide or show the panes · <code>i</code>: tips on/off · <code>?</code>: this help.</p>
    <h4>Where things live</h4><p class="muted">Each project is a folder under <code>projects/</code>: the run folder with the skill's own files (units, glossary, sources register, final.md, saved Dharmamitra outputs), your edits in state.json, exports in export/. You can open the run folder in Claude Code at any time and work there by hand; the app follows.</p>
    <h4>Cost</h4><p class="muted">A page of 10–12 segments costs about 260k tokens at xhigh effort and 300–400k at max, mostly the model's own reasoning. On a Pro plan expect about a page per five-hour window; Max plans or usage credits go further. The run waits for the reset and continues.</p>`);
}

/* ---------------------------------------------------------------- events */
function bind() {
  bindResizers(); bindTips();
  $('#btn-script').addEventListener('click', () => { S.prefs.script = !S.prefs.script; savePrefs(); applyLayout(); renderUnits(); renderInspector(); });
  $('#btn-review').addEventListener('click', () => { S.reviewOnly = !S.reviewOnly; S.expanded = new Set(); renderTop(); renderUnits(); });
  let qt; $('#search').addEventListener('input', e => { clearTimeout(qt); qt = setTimeout(() => { S.query = e.target.value; renderUnits(); }, 150); });
  $('#search').addEventListener('keydown', e => { if (e.key === 'Escape') { e.target.value = ''; S.query = ''; renderUnits(); e.target.blur(); } if (e.key === 'Enter') { const c = document.querySelector('#units .unit'); if (c) setActive(c.dataset.id, true); e.target.blur(); } });
  $('#btn-export').addEventListener('click', e => { e.stopPropagation(); $('#export-menu').classList.toggle('open'); $('#translate-menu').classList.remove('open'); });
  document.addEventListener('click', e => { if (!e.target.closest('.menu')) { $('#export-menu').classList.remove('open'); $('#translate-menu').classList.remove('open'); } });
  $('#export-menu').querySelectorAll('button').forEach(b => b.addEventListener('click', () => { $('#export-menu').classList.remove('open'); doExport(b.dataset.mode); }));
  $('#btn-about').addEventListener('click', () => panel('about'));
  $('#btn-help').addEventListener('click', helpUI);
  $('#btn-tips').addEventListener('click', () => { S.prefs.tips = !S.prefs.tips; savePrefs(); applyLayout(); $('#tip').classList.add('hidden'); toast(S.prefs.tips ? 'Hover explanations on.' : 'Hover explanations off.'); });
  $('#btn-translate').addEventListener('mouseenter', refreshClaudeStatus);
  $('#job-stop').addEventListener('click', () => runAction('stop'));
  $('#job-log').addEventListener('click', () => runAction('log'));
  $('#btn-new').addEventListener('click', newProjectUI);
  $('#btn-settings').addEventListener('click', settingsUI);
  $('#proj-select').addEventListener('change', e => { if (e.target.value && e.target.value !== S.slug) openProject(e.target.value); });
  $('#btn-translate').addEventListener('click', e => { e.stopPropagation(); $('#translate-menu').classList.toggle('open'); $('#export-menu').classList.remove('open'); });
  $('#translate-menu').querySelectorAll('button').forEach(b => b.addEventListener('click', () => { $('#translate-menu').classList.remove('open'); runAction(b.dataset.run); }));
  document.querySelectorAll('button.rail').forEach(b => b.addEventListener('click', () => panel(b.dataset.panel)));
  $('#modal-close').addEventListener('click', closeModal);
  $('#modal').addEventListener('click', e => { if (e.target.id === 'modal') closeModal(); });
  $('#tabs').querySelectorAll('button[data-tab]').forEach(b => b.addEventListener('click', () => { S.tab = b.dataset.tab; $('#tabs').querySelectorAll('button[data-tab]').forEach(x => x.classList.toggle('on', x === b)); renderInspector(); }));
  $('#inspector').addEventListener('click', e => {
    const m = e.target.closest('button.more'); if (!m) return;
    const u = U(S.active); const sw = m.closest('.segwin'); const s = u.segments[+sw.dataset.i]; const all = m.dataset.all !== '1'; m.dataset.all = all ? '1' : '0';
    $('.rows', sw).innerHTML = segRows(s, all); m.textContent = all ? 'show fewer' : `show the whole window (${s.rows.length} segments)`;
  });
  document.addEventListener('keydown', e => {
    if (e.target.isContentEditable || /INPUT|TEXTAREA/.test(e.target.tagName)) { if (e.key === 'Escape') e.target.blur(); return; }
    if (e.key === 'Escape') { closeModal(); return; }
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const ids = S.data.units.map(u => u.id); const i = ids.indexOf(S.active);
    if (e.key === 'ArrowDown' || e.key === 'j') { if (i < ids.length - 1) setActive(ids[i + 1], true); e.preventDefault(); }
    if (e.key === 'ArrowUp' || e.key === 'k') { if (i > 0) setActive(ids[i - 1], true); e.preventDefault(); }
    if (e.key === 'r' && S.active) { const u = U(S.active); st(u.id).reviewed = !reviewed(u); renderUnits(); renderTop(); save(); }
    if (e.key === 's') $('#btn-script').click();
    if (e.key === 'n') $('#btn-review').click();
    if (e.key === 'e') $('#btn-export').click();
    if (e.key === 't') runAction('next');
    if (e.key === 'g') panel('glossary');
    if (e.key === '/') { $('#search').focus(); e.preventDefault(); }
    if (e.key === 'i') $('#btn-tips').click();
    if (e.key === '?') helpUI();
    if (e.key === 'Enter' && S.active) { const c = document.querySelector(`.unit[data-id="${S.active}"] .en`); if (c) { c.focus(); e.preventDefault(); } }
    if (e.key === '[') { S.prefs.leftOpen = !S.prefs.leftOpen; applyLayout(); savePrefs(); }
    if (e.key === ']') { S.prefs.rightOpen = !S.prefs.rightOpen; applyLayout(); savePrefs(); }
    if (['1', '2', '3', '4', '5'].includes(e.key)) { const b = $('#tabs').querySelectorAll('button[data-tab]')[+e.key - 1]; if (b) b.click(); }
  });
}
init();
