# Prompt for the tibetan-translate skill session (9 October 2026)

Paste the block below into the session that maintains the skills.

---

Update the Tibetan translation skills in `~/Desktop/Tibetan Translation Skills` (repo copy = source of truth; sync with `./install.sh --skills-only`). Four changes, in this order. Keep the honesty rules: never print a Toh number, folio or attribution that did not come from a hit; examples in the skill text must come from real tool output.

## 1. Grounding without Explore's summaries and re-ranking (Dharmamitra's terms)

Sebastian Nehrdich (Dharmamitra) replied on 5 October 2026: plain semantic search on the primary path is light; what drives their compute is "the text-based replies of explore and the re-ordering of the results". He asked that the explore summaries be avoided and that it stay transparent which Dharmamitra resource is used at which stage. Today `dm.py explore` posts to `/bff/api/search/explore` with `do_ranking: True` and reads the Gemini event stream, so every hit it prints is part of the summary: there is no flag to switch the summary off. Replace it:

- Add `dm.py gloss "<10–25 syllables, Wylie>" [--n 50] [--context N] [--exclude-file PREFIX] [--no-en]`. It calls `/api-search/primary/` exactly as `search_raw` does (semantic, `filter_source_language: bo`, `do_ranking: False`, `expand_parallels: False`, `max_depth` = n). Group the hits by work as `identify` does. For each work print one block:
  ```
  === <work title, Wylie> · <collection> · <segmentnr> · GLOSS | QUOTE | NEAR
  <the hit's Tibetan in Wylie>
  ```
  `GLOSS` when the hit or its neighbours carry gloss scaffolding (`zhes pa ni`, `zhes bya ba ni`, `ces pa ni`, `zhes pa'i don`, `… ni … ste`, `… la bya`), `QUOTE` when the hit shares a verbatim run of ≥ 12 syllables with the query, `NEAR` otherwise. Order: GLOSS first, then Tengyur commentaries, then sungbum and series, then the rest; at most 12 works; drop `EN_` hits under `--no-en`, label them otherwise as `explore` does now. With `--context N`, fetch ±N segments for the top three GLOSS hits through the segment endpoint `cmd_segment` already uses, printed under the block with their ids, so one call reads the gloss. No machine rendering: the model reads the Tibetan. First output line: `DharmaMitra primary search · semantic · no re-ranking · <n> hits in <k> works`.
- Keep `explore` but rename its use: it stays available as `dm.py explore --summary` for a user who asks for it explicitly, with a note in its help text that the summary and re-ranking are the heavy operations on Dharmamitra's side.
- Skill text: `tibetan-translate/SKILL.md` §4.2 and §9, `reference/grounding.md` §1–§3, `tibetan-dharmamitra/SKILL.md` §1, §2, §3b: `gloss` replaces `explore` as the grounding tool; the save-file name becomes `dm_gloss_<unit>.txt`; the token budget line becomes 2–3k per call; add a short "Terms" paragraph in `tibetan-dharmamitra/SKILL.md` §1 quoting the two sentences above and the request for stage-by-stage transparency, and say that the header's `grounding:` field names the resource used. Fix the test report's and READMEs' mentions of explore in one sentence each (v2 now grounds through primary search; Explore only on request).
- Smoke test on the Uttaratantra line `thugs rje chen pos 'jig rten mkhyen/ 'jig rten kun la gzigs nas ni/`: `gloss --context 8` must surface Kongtrul's `rgyud bla ma'i 'grel pa phyir mi ldog pa seng ge'i nga ro` and Jamyang Lodrö's `nges don rab gsal snang ba` as GLOSS hits with the `zhes pa ni` gloss readable in the context. Paste that real output into `grounding.md` §3 as the example.

## 2. Long periods are split into sub-units

A Tibetan period with one finite verb can run to 100+ syllables (Rays of Sunlight U10 has 11 clauses). SKILL.md §3 defines a unit as "one Tibetan period of up to ~8 clauses" and so keeps such a period whole; in the CAT editor and in an aligned export a unit that long cannot be lined up with its English. Add to SKILL.md §1b (writing `<work>.units.md` from pasted text) and §3 (the unit): a period longer than about 70 syllables or 8 clauses is split at a major clause boundary (after `dang /`, `ste/`, `nas/`, `te/`, `zhing/`, `cing/`, `la/`, `na/`, `phyir/`; never inside a `zhes … las` citation frame, never between a verb and its arguments) into sub-units `U10a`, `U10b` …; the construal sketch and the `Q:` lines live under the first sub-unit with a `block U10a–U10c` header, as verse blocks do now; the English of the whole period is drafted once and then distributed so that each sub-unit's TEXT carries the English that renders its own Tibetan. Put the rule in `reference/analysis.md` §2.1 as well. `export_docx.py` needs no change. State in the test material note that Rays U10 came pre-segmented from the Vikramashila alignment sheet.

## 3. Footnotes at the end of a unit

`FN(): text` (empty anchor) or `FN(*): text` means "this footnote belongs to the whole unit": `export_docx.py` places its mark after the last character of the unit's last paragraph (after the final punctuation), with no "anchor not found" warning. Document it in `reference/notes.md` §4 and SKILL.md §8.6. The CAT app writes its edited `final.md` in this format.

## 4. Check, then sync

Run `python3 -m py_compile` on every changed tool, re-run `tests/` as the README says, `./install.sh --skills-only`, and `/reload-skills`. Commit with a message that names the four changes. Do not change the confidence-grade work from this morning.

## 5. German as a target language (added 9 October 2026, afternoon)

Since 10 October 2026 the skills live in this repository, in `../../skills/` relative to this file (edit there,
then `./install.sh --skills-only`); the app's runs still load the installed copy in `~/.claude/skills/`.

Tiger CAT now has a per-project target language (English or German) and writes it into the brief in
CLAUDE.md as "Target language: German" with this instruction: render the TEXT, the footnotes and the fixed
English short titles in German; keep the editor notes (Q/Alt/Comm/Var/Source/MITRA/Issue/Check/Conf) in
English; bind the glossary in German. The skill is English-only in its references, so add:

- `reference/german.md`, the German counterpart of `english.md` and `modes.md`: the standard and gates for
  natural German (verb position and clause length, Nominalstil avoided, the register ceiling per
  audience), the Sanskrit treatment per audience (Duden spellings such as Nirwana/Karma for the common
  words, IAST for academic, anglicized-style German forms for practitioners: Dharmakaya, Bodhisattva,
  Mahamudra), capitalisation of Dharma terms, Du/Sie and the imperative in instructions (seasoned
  practitioner texts of this tradition use the Du of Edition Garchen Stiftung's German editions; state
  the default and let the brief override), quotation marks („…“), the fixed German short titles of the
  canonical works where Edition Garchen Stiftung or 84000's German partners have one, and how a verse
  citation is set in German (free line-for-line is the default; metred German only when the brief asks,
  since beats.py is English-only).
- SKILL.md §2: a `Target language` row in the brief table (default English); §5 and §7: the style pass and
  the footnotes follow german.md when the target is German; the construal sketch and all editor notes
  stay in English so the trail is one language.
- tibetan-citations §4: TITLE rows carry the German short title when the target is German, in the same
  column; the register's locators do not change.
- tibetan-verse: declare that metre checking is English-only; for German the skill uses line-for-line
  verse unless the house style supplies a German metre rule.
- export_docx.py needs nothing; the app's exporter handles the text as given.

Run one smoke page in German (the Rays homage) and paste a real unit block into german.md as the example.
