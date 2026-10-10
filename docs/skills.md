# The skills: a guide for translators who know Claude Code

This is the full description of the four skills: the pipeline, the brief, the output and its
notes, the tools from the command line, model and effort, cost, and how it was tested. The front
page of the repository ([README.md](../README.md)) has the quick start and the layout; the
step-by-step guide for people new to Claude Code is [getting-started.md](getting-started.md);
Tiger CAT, the app that runs these skills over a whole text, is described in
[../cat/README.md](../cat/README.md). Paths in this file are written from the repository root.

Four Claude Code skills for translating Classical Tibetan (Wylie or Tibetan script) into English,
prose or verse, any genre. `tibetan-translate` is the entry point; `tibetan-verse` (verse rules v4
and a beat counter), `tibetan-citations` (short titles, sources register, footnote triage) and
`tibetan-dharmamitra` (Dharmamitra API reference and the Claude-versus-MITRA comparison protocol)
are its companions. A translation runs through one pipeline (v2, 4 October 2026): a **brief**
(audience, purpose, house style, notes policy); the model's **own reading and faithful draft** at
maximum effort, with a short construal sketch and the dictionary tool only on demand; a
**grounding pass** that identifies quotations and finds the canon's commentaries on the passage
through Dharmamitra (`dm.py gloss`, `segment`, `parallels`), follows their reading where the
grammar permits, and runs the MITRA cross-check as a flag; one **audience/style pass** with
glossary binding and verse rules; a short in-context **check**; and **two streams of notes**: working
notes for the editing translator and footnotes for the reader in the audience's style. Built and
calibrated on a practitioner edition of a 17th-century Drikung Kagyü guru-yoga treatise (the *Lam
Zab*); the design history is in `docs/Tibetan_Skills_Overhaul_2026-10-03.md`, the measurements that
led to v2 in `docs/Test_Report_2026-10-03.md`.

## What it adds, and what it does not

Measured in October 2026 on 33 pages that have published translations, then against the bare model
on three of them; the full numbers and caveats are in `docs/Test_Report_2026-10-03.md`.

- **Against Dharmamitra's MITRA alone.** MITRA made 2.5–2.9 meaning-changing errors a page and about
  six minor ones; the pipeline on Opus made 0.3 major and 2.6 minor. MITRA stays in the pipeline as
  a second opinion that raises flags (0.2k tokens a unit); it is not the translator.
- **Against bare Opus given the same brief and no skill.** No gain in fidelity, and at max effort
  no gain in English either. On three pages, each output scored by two independent judges, bare Opus
  at max had two major errors and English 3.9; the skill at max five majors and 4.0; the skill at
  xhigh four and 4.05; bare Opus at xhigh one and 3.7 (the judges disagreed by up to two majors on
  the same output, almost all on one tantra passage). So the skill is not more faithful than the bare
  model, and twice its analysis led a run to a worse reading than the bare model chose. What it adds
  is the English at the xhigh setting and on the academic page (where the bare output was bracketed
  study prose), verse that scans, somewhat fewer ambiguities resolved without a note, and
  the working files a bare run does not produce: a construal of every sentence, a glossary that binds
  terms across a long text, source identification with Toh numbers, and the MITRA flags. It costs
  about twice a bare run at max effort and four times one at xhigh, because the bare model at
  those settings spends most of its tokens thinking.
- **Against the published translations.** The judge found about four slips a page in them. The
  pipeline's `Q:` lines are a cheap second reading for a revised edition, not a replacement for the
  translator.
- **Not shown.** That any of this holds beyond three pages or with a judge from another model
  family; that the dictionary pass and the fidelity check catch errors the bare model would make (on
  these pages they did not); and the skill's main design claim, that bound terms and citations stay
  consistent across a long text, which a one-page test cannot measure.

Those measurements are of pipeline v1 (dictionary pass on every unit, 40-line construal, spawned
checker). **Pipeline v2** (4 October 2026) drops what bought nothing and adds what the bare model
cannot do: the model reads and drafts first, at maximum effort; then the grounding pass finds the
commentaries that gloss the passage (Dharmamitra's primary search, read in Tibetan; since 9 October
2026 without Explore's summaries and re-ranking, on Dharmamitra's terms, Explore only on request), follows them where they settle a reading,
and writes the disagreements up for the editor and, per audience, for the reader as footnotes.
Use it when you want a fixed house style, metred verse, a glossary and source references across a
long text, a reading grounded in the commentaries, and notes for editor and reader. For a bare
translation of a page, the model at max effort is as faithful and costs less; v2 has not been
measured against it yet beyond one smoke run.

## How to translate

**Where to run it.** The skills install to `~/.claude/skills/` and call their tools by absolute path,
so they work from any folder in a local Claude Code session (desktop app, Code tab, Local; or the
terminal). For a passage, start a chat anywhere, paste the Tibetan and say "translate this with the
skill". For a long text, open the text's folder each time: the brief in a `CLAUDE.md` there and the
glossary and construal files the skill keeps beside the text are what make terms and titles
consistent from page to page. To get a Word file with real footnotes:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/export_docx.py final.md --notes
```

In Claude Code, invoke the skill:

```text
/tibetan-translate
```

or just ask to translate, re-translate or check a Tibetan passage; the skill's description matches
those requests. Paste the Tibetan (Wylie or script).

**Pass 0, the brief.** Before drafting, the skill needs five things: *audience* (academic, new
practitioner, seasoned practitioner, hybrid, other), *purpose* (publication, study aid,
practice/recitation, working crib), *house style* (glossary file, diacritics, Sanskrit kept or
translated, capitalization, verse form, contractions and dashes), *notes policy* (which footnotes
the reader gets; defaults per audience in `skills/tibetan-translate/reference/notes.md`) and
*source context* (including known commentaries on the text).
If they are not already fixed it asks once, in a single question. "You choose" gives seasoned
practitioner, study aid, and the defaults in `skills/tibetan-translate/reference/modes.md`. In an
autonomous run it takes the defaults and prints them as assumptions at the top.

**Fix them in a project CLAUDE.md** and the skill uses them without asking and says so in one line:

```text
# Brief for this project
Audience: seasoned practitioner. Purpose: publication.
House style: no diacritics; Sanskrit terms kept where the tradition uses them (dharmakaya,
mahamudra); metred verse in chant mode for liturgy; no apparatus in the body; glossary is
glossary.tsv and it binds.
```

**The passes.** The model reads the Tibetan itself and drafts (a construal sketch of 8–15 lines
per unit goes to `<work>.construal.md`; `tibdict.py` is called only for a word it cannot settle).
Then the grounding pass: `dm.py identify` for every quotation, `dm.py gloss` on the clauses that
carry a doubt or a doctrine, which returns the commentaries that gloss those words with their
Tibetan (the primary search, no summary); the skill reads the gloss, follows it where the grammar permits, and records what it did.
MITRA is run once per page as a flag; a change made on MITRA's word alone is treated as a defect.
Then the style pass for the audience, glossary binding, verse per tibetan-verse, and a short
in-context check against the sketch.

**Output.** A one-line header (unit id, form, register, audience mode, source: `Toh ...`, `source
not located`, or `not a citation`; grounding: which commentary was followed, or `none found`); one
finished rendering (two only for a genuine fork); a `FOOTNOTES:` block for the reader where the
audience's notes policy allows one (anchored `FN(word): …`, written from the Tibetan of the
commentary); and a `NOTES:` block for the editing translator, one line each, only where there is
something to say:

- `Q:` a doubt and the alternative construal, and whether a commentary resolved it
- `Alt:` a hard word or line
- `Comm:` what a commentary says where it differs from the body or from another commentary, with its source
- `Var:` a variant reading that changes the sense
- `Source:` the identification
- `MITRA:` where MITRA differs on a content word, referent, agent or relation, kept or changed
- `Prior:` what an existing published translation reads where it differs, and whether it was followed
  or adapted under the brief's prior-translations policy (consult only by default; adaptation only
  where the licence or a permission allows, always cited: `skills/tibetan-translate/reference/existing-translations.md`)
- `Conf:` the unit's confidence grade (high / medium / low / very low) with its reason; the Word export
  shades low units orange and very-low units red so a reviser sees where to look first
- `Issue:` a term swap, an unpacking, an image let go, a register shift
- `Check:` what the in-context check found and changed

The skill keeps two work files beside your text and appends to them: `<work>.construal.md` (the
sketches, grounding and variants) and `<work>.glossary.tsv` (wylie, English, note; every term
decision and every fixed short title; a project glossary binds). Neither is printed unless you
ask. A spawned fresh-context checker runs only if you ask for an independent check.

## The tools from the command line

All four are plain Python and print compact text meant for a model's context.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py lookup "ye shes" --full --examples
```

Everything the index has on one word: the pipeline's on-demand call.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "<unit>" --budget 6000
```

Whole-unit report: segmentation, labelled particles, MITRA sense plus one classical dictionary per
word, verb paradigms, a `NEG:` count, a `COMPOUND?` line. Also `--file F`, `--brief`, `--examples`.
No longer run on every unit (it did not reduce errors in testing); useful when a unit will not parse.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py verb "<stem>"
```

The paradigm and case frame. `tibdict.py status` lists what is indexed; `tibdict.py build` rebuilds.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "<quoted lines>"
```

Find a quotation in the canon (Toh number, who quotes it). Read the `VERBATIM MATCH` line first:
`NO` means the hits are only semantic neighbours.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py gloss "<clause, Wylie>" --context 8
```

The grounding call: Dharmamitra's primary search without re-ranking or summary, the works grouped
and labelled GLOSS / QUOTE / NEAR, and the gloss of the commentaries on the root work read in
context. `dm.py explore --summary` runs Dharmamitra's Explore (the heavy operation on their side)
only when you ask for it.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py cite <segmentnr>
```

Citation lines (academic with folio, reader, register; for a published translation the translator,
publisher, year, ISBN and an attribution line) from Dharmamitra's catalogue fields; the AI-generated
overview is never used.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py parallels <segmentnr>
```

Variant readings. `dm.py segment <segmentnr> --context --window 8` fetches a segment with its
neighbours (the rest of a commentary's gloss).

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py translate --file page_units.md --style "literal, keep every clause and connective"
```

MITRA translation of every `Uxx` line of a page file (or pass the Tibetan as an argument for one
unit). Also `dm.py search`, `meta`. Dharmamitra: one request at a time, cache results, no Explore
summaries unless asked (their terms, 5 October 2026: `skills/tibetan-dharmamitra/SKILL.md` §1).

```bash
python3 ~/.claude/skills/tibetan-verse/tools/beats.py citation "line one," "line two,"
```

Beat count and stanza-shape check for an English verse block; `chant` mode for isometric lines. An
aid, not the authority: reading aloud outranks it.

```bash
python3 ~/.claude/skills/tibetan-citations/tools/register.py --check sources.tsv
```

Checks a sources register; `--add` appends a row, `--titles glossary.tsv` checks title consistency.

## Model and effort

The skills are calibrated on Claude Opus or Fable at `max` effort. Each skill opens with a gate:

- Not Opus or Fable: the skill stops and asks you to switch.
- Effort unverifiable or below max: it says so and asks.
- You tell it to proceed, or it runs autonomously (a subagent, a scheduled run, a brief that says not
  to ask): it proceeds and says once that it ran outside the calibrated setting.

```text
/model opus
```

```text
/effort max
```

Per the Claude Code docs, `max` applies to the current session unless set through
`CLAUDE_CODE_EFFORT_LEVEL` (https://code.claude.com/docs/en/model-config). If you must economize,
Opus at `xhigh` is the next setting down that the tests support; see "Cost". After editing a skill,
run `/reload-skills`: the Skill tool otherwise serves the copy it loaded at session start.

## Cost and what the settings buy

Measured 2026-10-03 on 30 full-page runs (10–12 units each; sutra, tantra, Tengyur commentary and a
Drikung commentary; a fresh-context Opus judge counted the errors against the Tibetan and a published
translation). Tokens are new tokens per page (input written plus output; cache reads excluded).

| Setting | Tokens per page | Major errors per page | English quality (1–5) |
|---|---|---|---|
| Opus, max | ~250–400k | 0.3 (0.8 on the 3 baseline pages, two judges) | 4.2 (4.0) |
| Opus, xhigh | ~200–340k | 0.3 (0.7 with a second judge) | 4.0 |
| Opus, high | ~130–185k | 0.75 | 3.7 |
| Opus, medium | ~90–135k | 0.7 | 3.8 |
| Sonnet, xhigh | ~300–455k | 1.7 | 3.5 |
| Sonnet, high | ~160–280k | 1.75 | 3.45 |
| Sonnet, medium | ~120–140k | 3.0 | 3.6 |
| *Bare Opus, max, no skill (3 pages, two judges)* | *~150–290k* | *0.3* | *3.9* |
| *Bare Opus, xhigh, no skill (3 pages, two judges)* | *~50–105k* | *0.2* | *3.7* |

Opus at max is the calibrated setting (3 major errors in 10 pages, 2 of them readings changed on
MITRA's word before that was forbidden). Opus at xhigh costs a third less for one major error in
three pages. Sonnet is not
cheaper per page at high or xhigh effort and makes two to three meaning errors a page, so it needs a
reviser who reads Tibetan. The in-page fixed costs: a spawned fidelity checker ≈ 55–85k whatever it
checks (so it is batched per page); MITRA ≈ 0.2k per unit; the first unit of a session carries ≈ 10k
of skill text. The full test report: `docs/Test_Report_2026-10-03.md`.

## How it was tested, and how it compares

Method (3 October 2026): 33 pages of 10–12 units were run through the pipeline autonomously (brief
given, no questions), on texts with a published English translation: two Drikung commentary pages
(*Rays of Sunlight*, *Stages of the Path*), the *Single Intention* commentary, the *Scintillation*
biography, and 84000 pages from *King of Samādhis*, *Lotus*, *Great Compassion of the Tathāgata*,
*Sampuṭa*, *Hevajra*, *Caṇḍamahāroṣaṇa*, the *Bṛhaṭṭīkā* and two Hevajra commentaries. The pipeline
never saw the English. For every page a separate judge (Claude Opus in a fresh context, reading the
Tibetan) listed the meaning errors in the pipeline's rendering, in MITRA's rendering of the same
units, and in the published translation, classed MAJOR (polarity, agent, relation, omission,
invention, referent) or MINOR (nuance, term), and scored the English 1–5. Tokens were read from the
agent transcripts. Protocols, briefs, outputs and judge reports: `tests/campaign_2026-10-03/`; report:
`docs/Test_Report_2026-10-03.md`.

Error rates per page of ~12 units, same pages, same judge:

| Translator | Major errors per page | Minor errors per page | English (1–5) | Pages |
|---|---|---|---|---|
| Pipeline, Opus max | 0.3 (0.8 on the 3 baseline pages, two judges) | 2.6 (1.8) | 4.2 (4.0) | 10 (+3) |
| Pipeline, Opus xhigh | 0.3 (0.7 pooled over two judges) | 2.0 (2.2) | 4.0 (4.05) | 3 |
| Pipeline, Opus high / medium | 0.75 / 0.7 | 3.8 / 2.7 | 3.7 / 3.8 | 4 / 3 |
| Pipeline, Sonnet (medium–xhigh) | 1.7–3.0 | 5–7 | 3.5 | 10 |
| MITRA alone (`dm.py translate`, literal style) | 2.5 (Opus-max pages); 2.9 (all 30 pages) | 6.4; 6.0 | not scored | 10; 30 |
| Published human translation | 3.9 errors per page, mostly minor (relay translations and Sanskrit-based editions count against this) | | | 10 |
| Bare Opus, no skill ("translate this" with the same brief; max / xhigh; two judges) | 0.3 / 0.2 | 1.0 / 2.2 | 3.9 / 3.7 | 3 / 3 |

The bare-model rows (4 October 2026, `tests/campaign_2026-10-03/baseline/`) show that on three pages
the skill does not lower the meaning-error count: with two judges per output the skill had five majors
at max and four at xhigh on these pages, bare Opus two and one. What it adds is the English at xhigh
(4.05 against 3.7) and on the academic page, metred verse, fewer silently resolved forks, and the
construal, glossary and source identification, for about four times the tokens of a bare xhigh run
(260k against 69k) and twice a bare max run (410k against 210k, the latter mostly thinking). Caveats: one judge per
page, from the same model family as the drafter; the pipeline's fidelity check ran in-context in
these runs; the figures are error counts against a construal of the Tibetan, not a reader study.

## Editing the skills

Edit this repo, then `./install.sh --skills-only`; or edit the live copies under `~/.claude/skills/`
while working, then `./export.sh` to copy them back before committing. `install.sh` replaces each
skill directory wholesale, so do one or the other, not both at once. After editing, `/reload-skills`
in a running session: the Skill tool otherwise serves the copy it loaded at session start.

## More

`docs/`: the test report (`Test_Report_2026-10-03.md`), the overhaul report
(`Tibetan_Skills_Overhaul_2026-10-03.md`, design and rationale), `own-dictionaries.md`, and
`research/research_dharmamitra_api.md` (an AI-assisted brief on the Dharmamitra endpoints and their
terms). The analysis of finished verse practice that the verse rules were derived from is
`skills/tibetan-verse/reference/lz-practice.md`. Licences and credits: the front page.
