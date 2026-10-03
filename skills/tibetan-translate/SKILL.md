---
name: tibetan-translate
description: Translate Classical Tibetan (Wylie or Tibetan script) into English — prose or verse, any genre: treatises, commentaries, pith instructions, sādhana and liturgy, dohā and songs, biographies, colophons, and the verse citations inside a prose text. Use for every request to translate, re-translate, check, or de-academize a Tibetan passage, and for building a construal or gloss of one. Runs the four-pass pipeline (brief → analysis with the local dictionary and Dharmamitra → faithful draft → audience/style pass → separate fidelity check), detects verse and applies the tibetan-verse skill for it, and asks for the audience and house style when they are not known. The one entry point for Tibetan translation; tibetan-verse, tibetan-citations and tibetan-dharmamitra are its companions.
---

# Tibetan → English: the pipeline

## 0. Gate

Calibrated for **Claude Opus or Claude Fable at maximum reasoning effort**. State the model and
effort in one line at the top of the reply. Not Opus or Fable: stop and ask the user to switch.
Effort unverifiable or below maximum: say so and ask. If the user tells you to proceed, or if you
are running autonomously (a subagent, a scheduled run, a brief that says not to ask), proceed and
say once that it ran outside the calibrated setting.

## 1. What this is

Four passes, each with a defined product. The analysis pass produces **structured data** (a
construal object), never prose reflections; the draft is written for fidelity; the style pass is one
parameterized adaptation to the audience; the fidelity check runs in a **fresh context** against
the construal. This shape is what the evidence on LLM translation supports (`reference/research.md`,
for the curious, not for routine reading): refinement and a separate span-level check are where
quality comes from; chains of role-play agents and free-form "research" steps are not.

Priority order, every conflict: **natural, clear, idiomatic English > content and its logic >
register fidelity > form (metre, line correspondence, sentence correspondence) > sound.**

**What to read, and when.** This file is sufficient for a routine unit. Read `reference/english.md`
(the standard and the gates) once per session before the first draft. Read the others only when
the need arises: `analysis.md` for a hard or unusual passage or your first construal of the
session · `prose.md` before the first prose unit · `modes.md` once per project, the column for the
brief's audience · `check.md` before the fidelity check, spawned or in-context (it holds the protocol). Do not cat every reference file at
the start; that costs more than the translation.

## 2. Pass 0 — the brief (ask once, then hold)

| Field | Values | Default if the user says "you choose" |
|---|---|---|
| **Audience** | academic · new practitioner · seasoned practitioner · hybrid (practitioner text, thin scholarly layer) · other (state it) | seasoned practitioner |
| **Purpose** | publication · study aid · practice/recitation · working crib | study aid |
| **House style** | glossary/terminology file; diacritics (IAST / none); Sanskrit kept or translated; capitalization; verse form (metred / free line-for-line / prose); notes policy; contractions, dashes | per `reference/modes.md` for the audience |
| **Source context** | work, author, genre, where the passage sits, who speaks to whom | inferred from the text, stated as an assumption |

If a project file (CLAUDE.md, a workflow file, a glossary, a memory note) already fixes these, use it
and say so in one line. Otherwise **ask once**, as a single compact question, before starting.
Never guess the audience silently: it changes the apparatus, the Sanskrit, the register ceiling and
the verse form. In an autonomous run take the defaults and print them as assumptions at the top.

A project glossary binds. Keep a running glossary for the piece (`<work>.glossary.tsv`: wylie,
English, note) and append every term decision; later units reuse it.

## 3. Pass 1 — analysis (the construal object)

**Unit:** one stanza, or one Tibetan period of up to ~8 clauses (a list of nominalized items joined
by `dang` is one period). Keep the unit's logic together rather than cutting at an arbitrary
sentence count. For a long text keep `<work>.construal.md` and append; the checker and later
units read the same file.

1. **Segment, count, classify.** Verse or prose (verse: shad-delimited padas of equal syllable
   count, usually 7/9/11; a `zhes/ces … las` frame around it means a *citation*). A quoted
   saying of only two matched lines (a parallel or chiastic dictum, 11/11 or 9/9) is verse only if
   it comes from a known verse work; otherwise set it as a prose dictum inline and record the
   verse setting as a `Q:`. Genre and register (`modes.md` §2).
2. **Dictionary pass — one call per unit:**
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "<unit, Tibetan or Wylie>"
   ```
   Segmentation (botok), every particle labelled with its function, each word's MITRA lexicon sense
   with attested English/Sanskrit renderings plus one classical dictionary, verb stems with Hackett
   syntax. `--examples` adds a cited parallel passage per word (hard terms only); `lookup <word>
   --full --examples` for one word in depth; `verb <stem>` for a paradigm; `--budget 6000` when the
   unit runs over ~40 syllables (it trims the sense lists, never the particle labels). The report
   opens with a `NEG:` count of the negation syllables in the raw text and a `COMPOUND?` line
   listing multi-syllable headwords that botok split (`phyag na rdo rje`, `mdo 'gag`): check that
   every counted negation surfaces as a NEG row, and read the compounds before the token rows.
   Glosses are **options with senses**, never forced equivalents; the project glossary
   outranks them. **Known slips** (read every row critically): botok sometimes absorbs a negation
   into a preceding token (`la ma gus pa` → "la ma" + "gus pa", which flips polarity) or picks a
   loan-word reading; the MITRA first sense can be the wrong sense (`skyes pa` "man" where the
   text means "arisen", `'dul ba` "vinaya" where it means "to tame"); verb-form lines list every
   lemma a form could belong to; the POS tag is botok's guess. The grammar decides.
3. **Identify citations — only when the unit is or contains a quotation**, or the user asks:
   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "<the quoted lines, Wylie>"
   ```
   If the text you are translating is itself canonical (a Tengyur commentary, say), add `--exclude
   <its Toh>` so its own copy is not reported as the source. Read the **VERBATIM MATCH** line first.
   *yes, canonical*: the Kangyur/Tengyur hit it names is the source (Toh number in the tag) and the
   rest are works that quote it; but a Tengyur hit that is a *commentary* quoting the same root verse
   is a fellow witness, not the source of a root citation: record `root not located; quoted also in
   Toh …` unless a Kangyur hit carries the words. *only in non-canonical
   works*: the long run is the citing text itself or a later work quoting it (a text you are
   translating may be in the index), and the canon has the words only loosely; record the best
   canonical candidate as `quoted loosely` with its Toh if the sense matches, otherwise `source not
   located`. *NO*: the passage is not in the index as quoted (a master's saying, a paraphrase, a
   variant); record `source not located` and do not cite the semantic neighbours. When a reading matters: `dm.py parallels
   <segmentnr>` for variants, `dm.py segment <segmentnr> --context` for a commentary's gloss. Do
   not call `dm.py explore` unless a verbatim hit is ambiguous between works; it is slow and
   secondary.
4. **Fill the construal object** (`analysis.md` §1 has the schema). The fields that matter most:
   - each clause's **finite verb**, class, **case frame** (ergative agent, absolutive object, *la
     don* role), tense/mood, honorific level, elided arguments;
   - every **relation particle** with its relation (`las` source · `pas` cause · `pa'i` modification
     · `na` condition · `phyir` purpose · `kyang` concession · `nas/te` sequence · `dang` coordination);
   - **negation and its scope**; restrictives, quantifiers, honorifics, vocatives, mood;
   - in verse, **metrical filler** and **elided case markers**;
   - **doubts**: every construal that could go another way, as `Q:` with the alternative.
5. **Construe in plain prose**, relations spelled out. This is the meaning target for every later
   pass.

Do not print the construal in the reply. Keep it in the work file (one compact block for a single
short passage). Keep reasoning about it short: the object is the product of this pass.

## 4. Pass 2 — faithful draft

Draft from the construal, not from the Tibetan word order.

- **Prose** (`reference/prose.md`): register per genre, decided before drafting and held; split the
  long period into English sentences **without dropping the connective at the seam**; median
  sentence 16–20 words, ceiling ~35; strong finite verbs; "you" where the text instructs; process
  language for devotion/blessing/realization; no additions; no apparatus unless the mode allows.
  Where a commentary enumerates practices as nominalized items (`bsten pa dang / … bya ba dang`),
  the instruction register may render them as "you" imperatives or "rely on …" items; ordinals
  ("first, second") are added only if the Tibetan counts them; a closing "these five" may be
  rendered as the Tibetan gives it.
- **Verse**: if the brief or the mode sets verse as *free line-for-line* (academic default; 84000-like
  briefs), render one English line per pada with tibetan-verse's construal, order and line-integrity
  rules but no metre, and use `beats.py` only as a readability aid. Otherwise load the
  **tibetan-verse** skill now and follow its loop (mode, kind, measure, lines ≥
  padas, relations carried, `beats.py`). A verse quotation inside prose is rendered by that skill
  and set as a verse block; never paraphrased into prose unless the house style's prose-setting
  rule applies.
- Bound terms exactly; context-sensitive senses for polysemous terms allowed and noted.
- Every item of the construal lands somewhere. Supplying an elided verb or subject is grammar;
  adding an adjective, image or intensifier is invention.

## 5. Pass 3 — audience and style (one pass, parameterized)

Apply `modes.md` for the brief's audience: Sanskrit treatment, apparatus, epithets, register
ceiling, verse form. This pass changes **surface, never meaning**: it may not add, drop or reorder
a relation. Read the result aloud (`english.md` Gate 1); fix what stumbles. For a verse unit the
verse loop has already done this; apply only the mode's Sanskrit and notes settings.

## 6. Pass 4 — fidelity check, in a fresh context

Do not grade your own draft in the same context. `reference/check.md` has the protocol.

- **Batch it.** A spawned checker costs ~50–60k tokens in harness overhead whatever it checks, so
  check **a page at a time** (5–12 units) in one Agent call, not per unit. For a single short
  unit the user wants now, run the protocol in-context after a clean break (re-read the construal
  from the file, then check clause by clause) and say `Check: in-context`; spawn a subagent for a
  single unit only if the user asks for the independent check.
- The checker receives file paths (construal file, draft file, glossary) plus the protocol; it
  returns **error spans only**: polarity, agent/role, omission, relation type, honorific/addressee,
  terminology, invention, silently resolved doubts (a doubt recorded as a `Q:` counts as noted).
- Apply **one** targeted revision for the confirmed spans. A second round only if a revision
  touched a relation.
- **No Agent tool in your context** (a workflow subagent, some headless runs): do the in-context
  check after the clean break and say `Check: in-context`. An orchestrator running several pages
  should spawn the checker itself, one per page, with the file paths.
- **MITRA cross-check, after the check** (standing step; measured 2026-10-03: MITRA showed 5 of the
  11 errors the pipeline made on 58 units, while making 39 of its own). One call per page:
  ```bash
  python3 ~/.claude/skills/tibetan-translate/tools/dm.py translate --file <page_units.md> --style "literal, keep every clause and connective"
  ```
  Compare each unit clause by clause with your rendering. Where MITRA differs on a **content word,
  a referent, an agent, or a relation**, go back to the Tibetan and the construal and decide from
  the grammar; keep your reading if it holds and record the disagreement as a `Q:`; change it only
  when the grammar says MITRA is right. Where MITRA merely phrases differently, ignore it. MITRA
  is a flag, never a vote: it has no register, no glossary, and flattens relations. **A change made
  on MITRA's word alone is a defect** (measured: MITRA talked a run out of the correct `skye bar
  byed` = "begets"): before changing the body, write the grammatical reason into the construal's
  CLAUSES/RELATIONS fields (case frame, verb class, particle) and re-run the relation and role tests
  of the check protocol on that clause; if you cannot state the reason, keep your reading and
  record a `Q:`. One line in the output: `MITRA: differs at U03 (reads rigs par as an object),
  U11 (sequence); kept / changed U07 (reason: …)`.

## 7. Output

1. **Header**, one line, merging the verse mode line when the unit is verse: unit id · form
   (prose / verse: mode, kind, measure, padas, lines, order) · register · audience mode · source
   (`Toh 381, Sampuṭa, D 158a; quoted in …` · `source not located` · `not a citation`).
2. **One finished rendering.** A second version only for a genuine fork (two defensible
   construals; term vs idiom; chant vs citation), each finished, one line on the choice.
3. **Notes**, one line each, only where there is something to say: `Q:` doubt and alternative ·
   `Alt:` a hard word or line · `Issue:` term swap, unpack, image let go, register shift, speech-act
   conversion · `Source:` identification and variants that affect the reading · `Check:` what the
   check found and changed.
4. For **academic / hybrid** modes, the apparatus the mode specifies, in a separate block.

Never print the gloss, the construal, scansion or gate working unless asked.

## 8. Token discipline

Quality outranks cost; waste is not quality. Measured 2026-10-03 on 30 full-page runs (10–12 units
each, prose and verse, in-context fidelity check, MITRA cross-check), new tokens per page
(input written + output; cache reads excluded):

| Setting | Tokens per page | Tool calls | Judge: major errors per page | English (1–5) |
|---|---|---|---|---|
| Opus, max effort | ~250–400k (mean 390k; 35–40 min) | ~45 | 0.3 | 4.2 |
| Opus, xhigh | ~200–340k (mean 260k) | ~36 | 0.3 | 4.0 |
| Opus, high | ~130–185k (mean 155k) | ~31 | 0.75 | 3.7 |
| Opus, medium | ~90–135k (mean 112k) | ~20 | 0.7 | 3.8 |
| Sonnet, xhigh | ~300–455k (mean 375k) | ~51 | 1.7 | 3.5 |
| Sonnet, high | ~160–280k (mean 213k) | ~28 | 1.75 | 3.45 |
| Sonnet, medium | ~120–140k (mean 129k) | ~19 | 3.0 | 3.6 |

Fixed costs inside a page: skill + `english.md` + one reference, first unit ≈ 10k; `tibdict annotate`
≈ 2–12k per unit (use `--budget 6000` on long periods); `dm.py identify` ≈ 0.8k; MITRA ≈ 0.2k per
unit; a spawned checker ≈ 55–85k whatever it checks (harness overhead), so batch it per page.

So: one `annotate` per unit; `identify` only for quotations; `explore` almost never; construal in a
file, not re-printed; references read on need, not up front; the checker batched per page; the
MITRA call once per page with `--file`. Opus at max is the calibrated setting (3 majors in 10 pages, 2 of them MITRA-induced before the
rule in §6); xhigh is the cheapest setting that stayed at or under one major error per three pages; Sonnet at any effort needs a
reviser who reads Tibetan.

## 9. Companions

- **tibetan-verse** — verse rendering rules and `beats.py`; called for every verse unit.
- **tibetan-citations** — short titles, the sources register, footnote triage, `register.py`.
- **tibetan-dharmamitra** — the API reference for `dm.py`, the Claude-vs-MITRA comparison
  protocol, the optional local model.

Project bindings override defaults. For the Lam Zab practitioner edition the pipeline files in
`02_Prompts/` and `08_Master_Edition/` still govern that workflow; this skill is the general
successor for everything else, and its construal stage can feed it.
