---
name: tibetan-translate
description: Translate Classical Tibetan (Wylie or Tibetan script) into English — prose or verse, any genre: treatises, commentaries, pith instructions, sādhana and liturgy, dohā and songs, biographies, colophons, and the verse citations inside a prose text. Use for every request to translate, re-translate, check, or de-academize a Tibetan passage, and for building a construal or gloss of one. Pipeline v2 (4 October 2026): brief → the model's own reading and faithful draft → grounding in the canon's commentaries through Dharmamitra (explore, identify, parallels) → audience/style pass with glossary binding and verse rules → short fidelity check → notes for the editing translator and footnotes for the reader in the audience's style. Detects verse and applies the tibetan-verse skill for it; asks for the audience and house style when they are not known. The one entry point for Tibetan translation; tibetan-verse, tibetan-citations and tibetan-dharmamitra are its companions.
---

# Tibetan → English: the pipeline (v2)

## 0. Gate

Calibrated for **Claude Opus or Claude Fable at maximum reasoning effort**. State the model and
effort in one line at the top of the reply. Not Opus or Fable: stop and ask the user to switch.
Effort unverifiable or below maximum: say so and ask. If the user tells you to proceed, or if you
are running autonomously (a subagent, a scheduled run, a brief that says not to ask), proceed and
say once that it ran outside the calibrated setting.

## 1. What this is, and why it is shaped this way

Measured on 3–4 October 2026 (`docs/Test_Report_2026-10-03.md`): Claude Opus at maximum effort,
given only a brief and the Tibetan, translates a page as faithfully as the same model wrapped in
a dictionary pass, a 40-line construal and a spawned fidelity checker, and reads about as well.
Twice the apparatus led a run to a worse reading than the bare model chose. So this pipeline no
longer front-loads tools between you and the Tibetan. **Your own reading at maximum effort is the
construal.** The pipeline adds what the bare model cannot give a translator:

1. a **brief** held across a whole text (audience, purpose, house style, glossary);
2. **grounding**: the canon's own commentaries on the passage, found through Dharmamitra, read in
   Tibetan, and followed where they settle a reading (`reference/grounding.md`);
3. **sources**: quotations identified with Toh numbers, variants noted (tibetan-citations);
4. **verse as verse**, in the house style's metre or line-for-line form (tibetan-verse);
5. **two streams of notes**: working notes for the editing translator, and footnotes for the
   reader written in the audience's style (`reference/notes.md`).

Priority order, every conflict: **natural, clear, idiomatic English > content and its logic >
register fidelity > form (metre, line correspondence, sentence correspondence) > sound.**

**What to read, and when.** This file is sufficient for a routine unit. Once per session before the
first draft: `reference/english.md` (the standard and the gates). Once per project: `modes.md`, the
column for the brief's audience, and `notes.md` (what becomes a footnote for this audience). Before
the first grounding call: `grounding.md`. Before the first prose unit: `prose.md`. `analysis.md`
only when a construal is contested or you reach for the dictionary tool; `check.md` holds the check
protocol. Do not cat every reference file at the start.

**Resuming after an interruption or a context reset.** The run's state is on disk: the construal
sketch, the glossary, the draft and style-pass files, the runlog, and the saved tool outputs
(`dm_<command>_<unit>.txt`, see §4). Re-read this file, `english.md`, `notes.md` and the brief, then
the state files, and continue from the last line of the runlog; do not repeat a tool call whose
output is saved.

## 1b. Where it runs, and what it needs from the folder

The skills live in `~/.claude/skills/` and every tool is called by its absolute path, so the
pipeline runs from **any folder** in a local Claude Code session (not Cowork, not cloud sessions).
Pasted Tibetan is enough: write it to `<work>.units.md` (one `Uxx` line per unit) in the current
folder, since the MITRA call and the runlog need a file, and keep the work files beside it.

- **A passage, once:** start a chat anywhere, paste the Tibetan, say "translate this with the
  skill". The skill asks the brief, writes its files into the current folder, and the glossary it
  starts binds for this chat only.
- **A long text:** open the text's folder each time. The brief in a `CLAUDE.md` there, the glossary
  `<work>.glossary.tsv` and the construal file persist across chats; that is what keeps terms and
  short titles consistent from page to page.
- **Output as a document:** `tools/export_docx.py final.md` writes a Word file with the footnotes
  as real footnotes (`--notes` appends the editor notes as a final section).

## 2. Pass 0 — the brief (ask once, then hold)

| Field | Values | Default if the user says "you choose" |
|---|---|---|
| **Audience** | academic · new practitioner · seasoned practitioner · hybrid (practitioner text, thin scholarly layer) · other (state it) | seasoned practitioner |
| **Purpose** | publication · study aid · practice/recitation · working crib | study aid |
| **House style** | glossary/terminology file; diacritics (IAST / none); Sanskrit kept or translated; capitalization; verse form (metred / free line-for-line / prose); contractions, dashes | per `reference/modes.md` for the audience |
| **Notes policy** | footnotes: scholarly · reader · minimal · none; endnotes or footnotes; sources in a register or in notes | per `reference/notes.md` for the audience |
| **Prior translations** | adapt <sources> (permission or licence stated) · consult only · ignore (`reference/existing-translations.md`) | consult only |
| **Source context** | work, author, genre, where the passage sits, who speaks to whom; known commentaries on it | inferred from the text, stated as an assumption |

If a project file (CLAUDE.md, a workflow file, a glossary, a memory note) already fixes these, use it
and say so in one line. Otherwise **ask once**, as a single compact question, before starting.
Never guess the audience silently: it changes the footnotes, the Sanskrit, the register ceiling and
the verse form. In an autonomous run take the defaults and print them as assumptions at the top.

A project glossary binds. Keep a running glossary for the piece (`<work>.glossary.tsv`: wylie,
English, note) and append every term decision; later units reuse it. Fixed English short titles of
quoted works are `TITLE` rows in the same file, in `register.py`'s column order:
`TITLE <tab> english_short_title <tab> wylie_title <tab> iast_title <tab> locator` (tibetan-citations §4).

## 3. Pass 1 — your reading, and the faithful draft

**Unit:** one stanza, or one Tibetan period of up to ~8 clauses (a list of nominalized items joined
by `dang` is one period). Work a **page** (5–12 units) at a time: grounding, the MITRA flag and the
check are per page.

1. **Read the Tibetan yourself**, verb first. Find each finite verb, its agent and object from the
   case frame, every relation particle and what it relates (`las` source · `pas` cause · `pa'i`
   modification · `na` condition · `phyir` purpose · `kyang` concession · `nas/te` sequence · `la`
   goal/locus), every negation with its scope, quantifiers, restrictives, honorifics, speaker and
   addressee. Verse or prose; a `zhes/ces … las` frame marks a citation.
2. **Write a construal sketch** in `<work>.construal.md`, 8–15 lines per unit: `SPINE` (the finite
   verbs and who does what to whom), `RELATIONS` (each particle = its relation), `NEG/QUANT`,
   `TERMS` taken from the glossary, `DOUBTS` as `Q:` lines with the alternative. The full schema in
   `analysis.md` §1 is for a contested unit, not for every unit. The sketch is working material,
   never shipped; the check and the grounding pass read it.
3. **The dictionary tool is on demand, not a pass.** Use `tibdict.py` for a word you cannot settle,
   a rare term, a name or transliteration, or when the user asks:
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py lookup "<word>" --full --examples
   ```
   `annotate "<unit>"` (the whole-unit report) only for a unit whose grammar you cannot parse; if
   you run it, read `analysis.md` §2a first: its segmenter and first senses mislead as often as they
   help. Glosses are options; the grammar and the glossary decide.
4. **Draft** from your reading, not from the Tibetan word order. Prose per `prose.md`: split the
   long period into English sentences **without dropping the connective at the seam**; strong
   finite verbs; "you" where the text instructs; no additions, no apparatus in the body. Verse:
   if the brief sets *free line-for-line*, one English line per pada with tibetan-verse's order and
   line-integrity rules and no metre; otherwise load **tibetan-verse** and follow its loop. A verse
   quotation inside prose is a verse block. Bound terms exactly.
5. **Forks.** A construal that could go another way is a `Q:`, always; a fork on the head noun of
   the period, on who the elided subject is, or on who does what in a loaded passage, is a `Q:`
   even when one branch looks clearly better. Resolve a fork **by the grammar first, then by the
   commentaries in Pass 2, never by the smoother English**. When both branches still stand after
   grounding, take the plainer reading in the body and keep the `Q:`. (Measured failure to avoid:
   `de yang bur skye bar byed` read as the father reborn as the son's son, with the plain "he in
   turn begets sons" recorded only as the alternative.)

## 4. Pass 2 — grounding in the tradition (Dharmamitra)

This is the pass that makes the translation more than grammar and vocabulary. Procedure and
examples: `reference/grounding.md`. The shape, per page:

1. **Quotations.** For every unit that is or contains a citation:
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "<the quoted words, Wylie>" [--exclude <Toh of the text you translate>]
   ```
   Read the **VERBATIM MATCH** line first; a Kangyur/Tengyur hit carrying the words is the source,
   a commentary carrying them is a witness. tibetan-citations fixes the English short title and
   writes the register row. Never state a Toh number you have not seen in a hit.
2. **Commentaries on the passage.** What gets queried: (a) every citation and every root-text line
   (the tradition glosses these); (b) in the author's own prose, a technical term, formula or
   enumeration the tradition glosses (`nges pa lnga`, `bdud bzhi`, `rtag chad kyi mtha'`): query the
   **term or formula**, not the sentence; (c) a unit whose reading forks on a doctrinal point. Plain
   prose of the author's own is **not queried**: nothing in the canon glosses it, and the header says
   `grounding: not queried`.
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/dm.py explore "<the key clause, line or formula, Wylie>"
   ```
   It returns the works that quote or gloss those words (commentaries, treatises, sungbum) with the
   Tibetan of each passage, a machine rendering, and a segment id. **Read the Tibetan of the gloss,
   not the machine English.** Where a gloss is cut short, `dm.py segment <id> --context --window 8`;
   for a canonical line, `dm.py parallels <id>` gives the variant readings. Budget: two to four
   `explore` calls a page (10–20 s and ~3–5k tokens each). **Ignore any hit that is an English
   translation** (segment ids beginning `EN_`, or a hit in the text you are translating with its
   published English beside it): do not read it, do not cite it, log the exposure in the runlog.
   Save every `dm.py` output to the run directory as `dm_<command>_<unit>.txt` so a resumed run
   need not repeat the call.
3. **Decide, and record.** Where a commentary glosses the very words you are translating
   (`… zhes pa ni …`, `… zhes bya ba ni …`), **translate according to the commentary's reading** when
   the grammar permits it, and say so in the sketch's `GROUNDING` line (work, Toh or segment id, what
   it says, what you did). Where commentaries differ from each other, or from your grammatical
   reading, keep the grammatical reading in the body unless the commentary resolves a recorded
   fork; write a `Comm:` note for the editor with the alternative and its source, and a footnote
   for the reader where `notes.md` says this audience gets one. Where nothing is found, write
   `GROUNDING: none found` once for the unit and move on. The explore summary is machine-made:
   use it as a map; cite only what you have read in Tibetan in a hit.
4. **Existing English translations.** `explore` labels any published translation among its hits
   (`EN_` ids). Handle them by the brief's prior-translations policy (`existing-translations.md`):
   never before drafting; under *consult only* compare after drafting and record a `Prior:` note;
   under *adapt* take wording where the licence or permission allows, say so in the header and cite
   it with `dm.py cite EN_<file>:<n>`; under *ignore* (tests) do not read them (`explore --no-en`).
   A published translator's reading that differs from yours is a flag like MITRA's, with a name:
   go back to the grammar and the commentaries before deciding.
5. **MITRA flag**, once per page, after drafting:
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/dm.py translate --file <page_units.md> --style "literal, keep every clause and connective"
   ```
   Where MITRA differs on a content word, a referent, an agent or a relation, go back to the
   Tibetan; keep your reading if the grammar holds and record a `Q:`; change only when the grammar
   says MITRA is right, and write the grammatical reason into the sketch first. **A change made on
   MITRA's word alone is a defect.** MITRA has no register, no glossary, and flattens relations.
   A `MITRA:` line in the notes of each unit where it differs on content, kept or changed with the
   reason; nothing where it merely rephrases.

## 5. Pass 3 — audience, style, glossary

Apply `modes.md` for the brief's audience: Sanskrit treatment, apparatus in the body (academic
only), epithets, register ceiling, verse form. Bind every term to the glossary and append new
decisions. This pass changes **surface, never meaning**: it may not add, drop or reorder a relation,
a negation, a quantifier or a speech act. Read the result aloud (`english.md` Gate 1); fix what
stumbles. A verse unit has been through tibetan-verse's loop already; apply only the mode's Sanskrit
and notes settings.

## 6. Pass 4 — the check (short, in-context)

After a clean break, re-read the construal sketch from the file and test the page against it,
clause by clause, with the protocol in `check.md`: polarity, role, relation, omission, invention,
speaker, term, doubt. Fix what fails; one round. Say `Check: in-context, <n> fixed`. A spawned
fresh-context checker is **not** part of the default pipeline (measured 2026-10-03: it caught none
of the errors the judges later found and cost 55–85k tokens a page); spawn one only when the user
asks for an independent check.

## 7. Pass 5 — notes for the editor, footnotes for the reader

Two streams, never mixed, rules in `reference/notes.md`.

- **Editor notes** (`NOTES:` block, every unit, for the translator who revises): `Q:` doubt and
  alternative · `Alt:` a hard word or line · `Comm:` what a commentary says where it differs from
  the body, with its source · `Var:` a variant reading that changes the sense · `Source:` the
  identification · `MITRA:` the flag · `Issue:` term swap, unpack, image let go, register shift ·
  `Check:` what the check changed. One line each, only where there is something to say; `none`
  otherwise.
- **Footnotes** (`FOOTNOTES:` block, only where the audience's notes policy allows): written for
  the reader in the body's voice, from the Tibetan of the commentary or source, anchored to a word
  of the rendering. Academic: locators, variants, the commentary's reading with Toh and folio,
  Sanskrit. Seasoned practitioner: what the commentary explains where it unlocks the passage, an
  enumeration, a name, one opaque image; no locators (they go to the register). New practitioner:
  rarely, one plain sentence. Working crib and recitation: none.

## 8. Output

1. **Header**, one line: unit id · form (prose / verse: mode, kind, measure, padas, lines) ·
   register · audience mode · source (`Toh 381, Sampuṭa, D 158a; quoted in …` · `source not
   located` · `not a citation`) · grounding (`<work> gloss followed` · `none found` · `not queried`
   · `service unavailable`) · prior (`none` · `consulted (<translator year>)` · `adapted
   (<translator year>)`) · confidence (`high` · `medium` · `low` · `very low`, graded per
   `notes.md` §1b, reason in the `Conf:` note). When one verse sentence runs across several units, the first unit's
   header carries the block's mode, kind, measure and line order and names the span (`block
   U06–U09`); the later units say `verse: cont. of block U06–U09`; each unit's footnotes and notes
   stay with the unit whose words they concern.
2. **One finished rendering.** A second version only for a genuine fork (two defensible
   construals; term vs idiom; chant vs citation), each finished, one line on the choice.
3. **FOOTNOTES:** per §7, or `none`.
4. **NOTES:** per §7, or `none`.
5. The glossary file updated; a register row for every identified quotation (tibetan-citations).
6. When the user wants a document: `python3 ~/.claude/skills/tibetan-translate/tools/export_docx.py
   <final.md> [--notes]`, a .docx with the body text, verse lines kept, and every `FN(anchor):` as a
   Word footnote anchored after its phrase.

Never print the construal sketch, dictionary rows, scansion or gate working unless asked.

## 9. Token discipline

Quality outranks cost; waste is not quality. The bare model at max effort spends 150–290k new
tokens on a 12-unit page, nearly all of it thinking; that is the floor. This pipeline should land
within about 300k at max: two to four `explore` calls (3–5k each), `identify` per quotation (~1k),
`tibdict lookup` for a few words (~1k each), one MITRA call (0.2k a unit), the sketch and the notes.
Measured on the v1 pipeline, which this replaces: a whole-unit dictionary report (2–12k a unit) and
a spawned checker (55–85k a page) bought no measurable fidelity. Opus at max is the calibrated
setting; xhigh is the cheapest setting that read as well; Sonnet at any effort needs a reviser who
reads Tibetan.

## 10. Companions

- **tibetan-verse** — verse rendering rules and `beats.py`; called for every verse unit.
- **tibetan-citations** — short titles, the sources register, footnote triage, `register.py`.
- **tibetan-dharmamitra** — the API reference for `dm.py` (identify, explore, segment, parallels,
  translate, meta, cite), the grounding procedure's tool notes, the optional local model.

Project bindings override defaults. For the Lam Zab practitioner edition the pipeline files in
`02_Prompts/` and `08_Master_Edition/` still govern that workflow; this skill is the general
successor for everything else.
