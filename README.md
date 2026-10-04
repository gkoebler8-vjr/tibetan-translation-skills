# Tibetan Translation Skills

Four Claude Code skills for translating Classical Tibetan (Wylie or Tibetan script) into English,
prose or verse, any genre. `tibetan-translate` is the entry point; `tibetan-verse` (verse rules v4
and a beat counter), `tibetan-citations` (short titles, sources register, footnote triage) and
`tibetan-dharmamitra` (Dharmamitra API reference and the Claude-versus-MITRA comparison protocol)
are its companions. A translation runs through one pipeline: a **brief** (audience, purpose, house
style); an **analysis** pass that segments and looks up every word with `tibdict.py` (a local
dictionary index) and identifies quotations with `dm.py` (Dharmamitra), and writes a structured
construal; a **faithful draft** from the construal; one **audience/style pass**; a **fidelity
check** in a fresh context that returns error spans only; and a **MITRA cross-check** whose
differences are flagged, never voted on. Built and calibrated on a practitioner edition of a
17th-century Drikung Kagyü guru-yoga treatise (the *Lam Zab*); see
`docs/Tibetan_Skills_Overhaul_2026-10-03.md` for the design and the test runs.

Author: Gabriel Kobler. Built with Claude (Opus and Fable), 2026-09 to 2026-10.

## Requirements

- macOS or Linux, Python 3.9+ (3.11 recommended) (`python3.11` via Homebrew on the Mac this was built on), `git`, `curl`.
- Claude Code (CLI or the desktop app's Code tab, local sessions). Personal skills in
  `~/.claude/skills/` are not read by Cowork or cloud sessions.
- Claude Opus or Fable at maximum effort for translation work (see "Model and effort").
- Network for the Dharmamitra endpoints and for the one-time lexicon download (~274 MB).
- About 1 GB of disk (download, extracted lexicon, 178 MB index, venv).
- Optional: a GoldenDict/StarDict folder of your own Tibetan dictionaries (Hopkins, Rangjung Yeshe,
  Monlam, ...); see `docs/own-dictionaries.md`.

## Quick start

```bash
git clone https://github.com/gkoebler8-vjr/tibetan-translation-skills.git
```

```bash
cd tibetan-translation-skills
```

```bash
./install.sh
```

This copies the four skills to `~/.claude/skills/`, creates a venv at `~/.venvs/tib` (botok,
pyewts), downloads the MITRA Tibetan Lexicon (CC BY-SA 4.0), and builds the index at
`~/.tibdict/tibdict.sqlite`. It is idempotent. Flags:

```bash
./install.sh --skills-only
```

Copy the skills only (no venv, download or index).

```bash
./install.sh --golden "/path/to/GoldenDict/TIBETAN"
```

Also index a folder of your own StarDict dictionaries.

```bash
./install.sh --public
```

Also fetch the open Tibetan-English dictionaries of Christian Steinert's project (~38 MB, fetched
onto your machine, not bundled) and index them.

Smoke tests:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "བླ་མའི་བྱིན་རླབས་ཁོ་ན་ལས།"
```

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "rnam rtog ma rig chen po ste / 'khor ba'i rgya mtshor ltung byed yin"
```

The first prints a segmentation with a dictionary row per word; the second a `VERBATIM MATCH` line
and the works containing the passage. A running session picks up new skills without a restart; if
`~/.claude/skills/` did not exist when it started, run `/reload-skills`.

## How to translate

In Claude Code, invoke the skill:

```text
/tibetan-translate
```

or just ask to translate, re-translate or check a Tibetan passage; the skill's description matches
those requests. Paste the Tibetan (Wylie or script).

**Pass 0, the brief.** Before drafting, the skill needs four things: *audience* (academic, new
practitioner, seasoned practitioner, hybrid, other), *purpose* (publication, study aid,
practice/recitation, working crib), *house style* (glossary file, diacritics, Sanskrit kept or
translated, capitalization, verse form, notes policy, contractions and dashes) and *source context*.
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

**Output.** A one-line header (unit id, form, register, audience mode, source: `Toh ...`, `source
not located`, or `not a citation`); one finished rendering (two only for a genuine fork); then one-line
notes only where there is something to say:

- `Q:` a doubt and the alternative construal (the editor's list)
- `Alt:` a hard word or line
- `Issue:` a term swap, an unpacking, an image let go, a register shift
- `Source:` identification and variants that affect the reading
- `Check:` what the fidelity check found and changed
- `MITRA:` where MITRA differs on a content word, referent, agent or relation, and whether you kept or changed

Academic and hybrid modes add an apparatus block. The skill keeps two work files beside your text and appends to them: `<work>.construal.md` (the analysis; the checker and
later units read it) and `<work>.glossary.tsv` (wylie, English, note; every term decision, and a
project glossary binds). The construal is not printed in the reply unless you ask.

The fidelity check runs a page (5-12 units) at a time in one spawned subagent. A single unit is
checked in-context after a clean break (`Check: in-context`) unless you ask for the independent check;
so is a page when the running context has no Agent tool (workflow subagents, some headless runs). The
MITRA cross-check then runs once per page; a change made on MITRA's word alone is treated as a defect.

## The tools from the command line

All four are plain Python and print compact text meant for a model's context.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "<unit>" --budget 6000
```

Per-unit report: segmentation, labelled particles, MITRA sense plus one classical dictionary per
word, verb paradigms, a `NEG:` count, a `COMPOUND?` line. Also `--file F`, `--brief`, `--examples`.

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py lookup "ye shes" --full --examples
```

Everything the index has on one word.

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
python3 ~/.claude/skills/tibetan-translate/tools/dm.py parallels <segmentnr>
```

Variant readings. `dm.py segment <segmentnr> --context` fetches a segment with its neighbours (a
commentary's gloss).

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py translate --file page_units.md --style "literal, keep every clause and connective"
```

MITRA translation of every `Uxx` line of a page file (or pass the Tibetan as an argument for one
unit). Also `dm.py search`, `meta`, `explore`. Dharmamitra: one request at a time, cache results.

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
| Opus, max | ~250–400k | 0.3 | 4.2 |
| Opus, xhigh | ~200–340k | 0.3 | 4.0 |
| Opus, high | ~130–185k | 0.75 | 3.7 |
| Opus, medium | ~90–135k | 0.7 | 3.8 |
| Sonnet, xhigh | ~300–455k | 1.7 | 3.5 |
| Sonnet, high | ~160–280k | 1.75 | 3.45 |
| Sonnet, medium | ~120–140k | 3.0 | 3.6 |

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
| Pipeline, Opus max | 0.3 | 2.6 | 4.2 | 10 |
| Pipeline, Opus xhigh | 0.3 | 2.0 | 4.0 | 3 |
| Pipeline, Opus high / medium | 0.75 / 0.7 | 3.8 / 2.7 | 3.7 / 3.8 | 4 / 3 |
| Pipeline, Sonnet (medium–xhigh) | 1.7–3.0 | 5–7 | 3.5 | 10 |
| MITRA alone (`dm.py translate`, literal style) | 2.5 (Opus-max pages); 2.9 (all 30 pages) | 6.4; 6.0 | not scored | 10; 30 |
| Published human translation | 3.9 errors per page, mostly minor (relay translations and Sanskrit-based editions count against this) | | | 10 |
| Bare Opus, no skill ("translate this" with the same brief) | **not yet measured** | | | |

The bare-model baseline is the missing row; `tests/campaign_2026-10-03/baseline/BASELINE_TODO.md`
describes how to run it on the same pages so the figures are comparable. Caveats: one judge per
page, from the same model family as the drafter; the pipeline's fidelity check ran in-context in
these runs; the figures are error counts against a construal of the Tibetan, not a reader study.

## Layout

```
skills/                 the four skills (source of truth; install.sh copies them to ~/.claude/skills)
  tibetan-translate/    SKILL.md + reference/ (english, analysis, prose, modes, check, research) + tools/ (tibdict.py, dm.py)
  tibetan-verse/        SKILL.md + reference/ (guidelines, lz-practice, failures) + tools/ (beats.py, lexicon.py)
  tibetan-citations/    SKILL.md + tools/register.py
  tibetan-dharmamitra/  SKILL.md + reference/ (compare, compare-log) + tools/ (mitra.py, setup_mitra.sh: optional local model)
docs/                   Test_Report_2026-10-03.md, the overhaul report, own-dictionaries.md, the Lam Zab verse analysis, research/
tests/                  campaign_2026-10-03/ (33 judged page runs: material, outputs, checks, judge reports, token table) and the first two unit tests
resources/              downloaded dictionary data (gitignored)
install.sh  export.sh   setup; copy edited live skills back into the repo
HANDOVER.md  LICENSE  LICENSE-NOTES.md
```

## Editing the skills

Edit this repo, then:

```bash
./install.sh --skills-only
```

Or edit the live copies under `~/.claude/skills/` while working, then copy them back before
committing:

```bash
./export.sh
```

`install.sh` replaces each skill directory wholesale, so do one or the other, not both at once.

## Licences

Code (`skills/*/tools/`, `install.sh`, `export.sh`, `tests/*.py`): MIT. Text (SKILL.md and
reference files, docs, READMEs, test reports): CC BY 4.0, attribution "Tibetan Translation Skills by
Gabriel Kobler, built with Claude (Anthropic)". Third-party data is not bundled. The installer
downloads the MITRA Tibetan Lexicon (Dharmamitra, CC BY-SA 4.0) and, on request, open dictionaries
whose copyright stays with their authors. An index built from your own or the public dictionaries is
private working data; do not redistribute it. Details in `LICENSE` and `LICENSE-NOTES.md`.

## Credits

- **Dharmamitra** (Sebastian Nehrdich and colleagues): the MITRA Tibetan Lexicon, the search and
  parallels endpoints, and MITRA translation, used here at personal-research rate.
- **84000**: translations and the glossary, used for citation lookup and as references.
- **Christian Steinert**: the open tibetan-dictionary project and its dictionary files; copyright
  of the dictionary data is with the respective authors (Hopkins, Rangjung Yeshe, Berzin, Valby,
  Ives Waldo and others).
- **Edition Garchen Stiftung translators**, whose published work was used as references in testing.
- botok and pyewts for segmentation and Wylie conversion.

## More

`docs/`: the overhaul report, `own-dictionaries.md`, `lz_verse_practice_analysis.md`, and
`research/` (AI-assisted briefs on translation practice, dictionaries and NLP, the Dharmamitra
API). New to Claude Code or the command line: `README-beginners.md`.
