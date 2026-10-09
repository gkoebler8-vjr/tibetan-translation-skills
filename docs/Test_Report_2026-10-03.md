# Tibetan Translation Skills — test report, 3 October 2026

*For translators, especially the Vikramashila group. Short version first; the data and every judged
page are in `tests/campaign_2026-10-03/`.*

*Postscript, 4 October 2026: everything measured below is pipeline **v1**. Its findings (the bare
model at max effort is as faithful as the model with a dictionary pass, a full construal and a
spawned checker) led to pipeline **v2** the same day: the model reads and drafts first; a grounding
pass then finds the canon's commentaries on the passage through Dharmamitra (since 9 October 2026
through the primary search alone, `dm.py gloss`, without Explore's summaries and re-ranking, at
Dharmamitra's request; Explore only when the user asks) and follows them where they settle a reading; notes for the editor and footnotes for the reader are written per audience.
v2 has had one smoke run, not a campaign; see the README's "What it adds, and what it does not".*

## In one paragraph

We ran the `tibetan-translate` pipeline on 33 pages (10–12 sentences or stanzas each) of texts that
already have published English translations: two pages of Drikung commentary (Ayang Thubten's *Rays of
Sunlight*, Jigten Sumgön's *Stages of the Path*), a page of Khenpo Kunpal's *Single Intention*
commentary, a page of the *Scintillation* biography, and pages from 84000's *King of Samādhis*,
*Lotus*, *Great Compassion of the Tathāgata*, *Sampuṭa*, *Hevajra*, *Caṇḍamahāroṣaṇa*, the
*Bṛhaṭṭīkā* and two Hevajra commentaries. A separate judge (Claude Opus in a fresh context, reading the
Tibetan) counted meaning errors in the pipeline's rendering (C), in Dharmamitra's MITRA machine
translation (M) and in the published human translation (H), and scored the English. **On Claude Opus at
maximum effort the pipeline made three major meaning errors in ten pages (116 units), two of them
from readings it changed on MITRA's word before that was forbidden, and about two and a half minor
ones per page, with English rated 4.2 out of 5; the published translations of the same pages carried
about four judge-confirmed errors a page, MITRA two and a half majors and six minors a page.** Weaker
settings degrade quickly: Opus at high effort makes a major error every page or two; Sonnet two to
three a page. A bare-model baseline run afterwards (Opus with the same brief and no skill, three
pages, each output scored by two independent judges, the skill re-run at max on the same pages) made
no more meaning errors than the skill and read about as well: pooled over both judges, bare Opus at
max had two majors and English 3.9, the skill at max five majors and 4.0, the skill at xhigh four and
4.05, bare Opus at xhigh one and 3.7. On these pages the skill's measurable gain over the bare model is
confined to the English at the xhigh setting and to what the bare run does not produce at all (the
construal, glossary, source identification, metred verse and MITRA flags); it does not make the
translation more faithful. The output is a strong draft with its doubts listed, not a finished
translation.

## What was tested

| Set | Pages | Texts | Mode (brief) |
|---|---|---|---|
| Run 1 (Opus max, skill as handed over) | 5 | Rays of Sunlight (homage + Uttaratantra citation); Stages of the Path (argument, citations); King of Samādhis ch. 4 (list + 6 stanzas); Sampuṭa ch. 1 (12 stanzas); Bṛhaṭṭīkā (scholastic prose) | seasoned practitioner · seasoned · new practitioner (84000-like) · seasoned · academic |
| Run 2 (Opus max, after the first fixes) | 5 | Single Intention commentary; Scintillation (narrative, dialogue); Lotus ch. 14; Hevajra II.4; String of Pearls (Hevajra commentary) | seasoned · seasoned · new practitioner · seasoned · academic |
| Final matrix (fixed skill, 20 runs) | Rays of Sunlight, Caṇḍamahāroṣaṇa ch. 15, Jewel Garland of Yoga (Hevajra commentary) × Opus and Sonnet × medium, high, xhigh; Great Compassion ch. 2 × both at high | |

Each page went through the whole pipeline: brief → analysis with the local dictionary (`tibdict.py`)
and Dharmamitra source identification → faithful draft → audience/style pass → fidelity check against
the construal → MITRA cross-check (from run 2). The runs were autonomous (no questions asked) and the
fidelity check ran in-context, because the harness used for the runs gives subagents no way to spawn
a second agent; on the run-2 pages an external checker was spawned separately as well.

## Results

**Opus at maximum effort (runs 1 and 2, the calibrated setting), 10 pages, 116 units**

| Page | Units | C major | C minor | English | M major | M minor | M would reveal of C's | H errors |
|---|---|---|---|---|---|---|---|---|
| Rays of Sunlight | 12 | 0 | 1 | 4.3 | 3 | 3 | 0 | 4 |
| Stages of the Path | 12 | 0 | 2 | 4.3 | 0 | 3 | 2 | 3 |
| King of Samādhis | 12 | 1 | 3 | 4.3 | 3 | 3 | 2 | 3 |
| Sampuṭa | 12 | 0 | 3 | 3.8 | 2 | 7 | 1 | 7 |
| Bṛhaṭṭīkā | 10 | 0 | 1 | 4.2 | 2 | 13 | 0 | 4 |
| Single Intention | 12 | 0 | 2 | 4.2 | 1 | 7 | 2 | 7 |
| Scintillation | 11 | 0 | 3 | 4.4 | 1 | 8 | 2 | 6 |
| Lotus | 11 | 0 | 2 | 3.9 | 3 | 4 | 2 | 2 |
| Hevajra | 12 | 2 | 5 | 4.2 | 7 | 7 | 3 | 0 |
| String of Pearls | 12 | 0 | 4 | 4.0 | 3 | 9 | 2 | 3 |
| **Total** | **116** | **3** | **26** | **4.2** | **25** | **64** | **16** | **39** |

Two of the three majors are on the Hevajra page, and both were readings the run changed on MITRA's
word (`yongs su gcod` "destroys" → "ascertains"; the outcastes' role in the last stanza). The rule
that forbids a change on MITRA's word alone was added after that run.

"H errors" are places where the judge found the published translation wrong against the Tibetan
(a dropped quantifier, a restrictive read the wrong way, an added word, a wrong referent). They are
a by-product, not a verdict on anyone's work: the Scintillation English is a relay translation via
German, and several 84000 texts follow the Sanskrit where the Tibetan differs. They do show that a
construal-based check finds things that editing by eye does not.

**Final matrix, three pages (Rays of Sunlight, Caṇḍamahāroṣaṇa, Jewel Garland of Yoga)**

| Setting | Major errors (3 pages) | Minor | English | New tokens per page | Minutes per page |
|---|---|---|---|---|---|
| Opus xhigh | 1 | 6 | 4.0 | 260k | ~24 |
| Opus high | 2 (+1 on the sutra page) | 9 | 3.7 | 155k | ~12 |
| Opus medium | 2 | 8 | 3.8 | 112k | ~9 |
| Sonnet xhigh | 5 | 19 | 3.5 | 375k | ~35 |
| Sonnet high | 7 (incl. sutra page) | 28 | 3.45 | 213k | ~25 |
| Sonnet medium | 9 | 15 | 3.6 | 129k | ~20 |
| *Opus max (runs 1–2, 10 pages, for scale)* | *0.3 per page* | *2.6 per page* | *4.2* | *390k mean* | *~35* |

Ranking by output quality: Opus max > Opus xhigh > Opus medium ≈ Opus high > Sonnet (any effort).
Ranking by tokens per page: Opus medium < Sonnet medium < Opus high < Sonnet high < Opus xhigh <
Sonnet xhigh ≈ Opus max. **Best value: Opus at xhigh** (a third cheaper than max, one major error in
three pages). Sonnet is not cheaper at high or xhigh effort and makes two to three meaning errors a
page: usable only with a reviser who reads the Tibetan. Opus at medium is the cheapest setting that
still reads well (3.8), but it slips on construal forks. We did not need to test Sonnet at max.

**Baseline: the bare model, no skill (added 4 October 2026)**

Same three pages, same briefs, same judge protocol. The model received only the brief and the
Tibetan and was told to translate from its own knowledge: no skill, dictionary, Dharmamitra, checker
or reference files, one finished rendering per unit and a short note where a reading is uncertain.
Six bare runs (Opus at max and at xhigh), and, for a like-for-like comparison at the calibrated
setting, the skill re-run at Opus max on the same three pages (run 4, same day). Every output in this
table was scored by two independent fresh-context Opus judges, the second with the first's report
withheld. Figures are major / minor / English; the first judge is before the semicolon, the second
after.

| Page | Skill, Opus max | Skill, Opus xhigh | Bare Opus max | Bare Opus xhigh |
|---|---|---|---|---|
| Rays of Sunlight | 0 / 1 / 4.2; 0 / 1 / 4.1 | 0 / 3 / 4.2; 0 / 3 / 4.3 | 0 / 0 / 4.1; 0 / 1 / 4.1 | 0 / 1 / 3.9; 0 / 2 / 3.9 |
| Caṇḍamahāroṣaṇa ch. 15 | 1 / 1 / 4.1; 1 / 4 / 4.1 | 1 / 2 / 3.9; 3 / 1 / 4.0 | 2 / 1 / 4.3; 0 / 1 / 4.3 | 0 / 3 / 4.1; 1 / 1 / 3.9 |
| Jewel Garland of Yoga | 2 / 2 / 3.8; 1 / 2 / 3.6 | 0 / 1 / 4.0; 0 / 3 / 3.9 | 0 / 2 / 3.4; 0 / 1 / 3.4 | 0 / 4 / 2.9; 0 / 2 / 3.4 |
| **Pooled, both judges (72 unit-judgments)** | **5 / 11 / 3.98** | **4 / 13 / 4.05** | **2 / 6 / 3.93** | **1 / 13 / 3.68** |
| Silent doubts (forks resolved without a note, both judges) | 4 | 4 | 6 | 8 |
| New tokens per page | ~410k (310–540k) | 260k | 210k (146–290k) | 69k (48–104k) |
| Minutes per page | ~35 | ~24 | 13–19 | 3–5 |

(The skill's run-1 Opus-max result on Rays of Sunlight, 0 / 1 / 4.3 with one judge, is consistent
with the run-4 figures above; the run-4 skill runs were interrupted once by a usage limit and resumed
from their saved construal files, which added some re-done dictionary calls to their token count.)

What the skill buys, on this evidence. On meaning errors, nothing: the bare model is at least as
faithful at either setting, and at max the pooled count runs the other way (two majors bare, five
with the skill). The second judging round was run to test whether the first round's tie was judge
noise, and it held. English scores were stable between judges (within 0.1 on most outputs); error
counts on the same output moved by up to two majors, almost all on the tantra page's units 6 and 7
(who kills whom, who desires whom), which every run read the same way and which the judges scored
anywhere from "defensible, silent doubt" to two majors. Two of the skill's majors are instructive:
on the tantra page both judges faulted the skill at max for `de yang bur skye bar byed`, where it
recorded the fork and then took the weaker branch (the father reborn as the son's son) while both
bare runs took the plain one (he in turn begets sons); and on the same page the skill's dictionary
tool offered a compound `mthar thug pa sangs rgyas` "ultimate buddhahood" that the first draft
followed and only the MITRA cross-check caught. The analysis apparatus can mislead as well as help.
The bare runs also wrote more notes than expected (13–24 `Q:` lines a page), so the "silent doubt"
gap is small (6–8 against 4 over two judges). On English the skill at max (3.98) is level with bare
max (3.93); the one clear gain is at xhigh (4.05 against 3.68), and on the academic page at either
setting (3.7–3.95 against 3.15–3.4), where the bare output was bracket-laden study-translation
prose with Sanskrit in parentheses after every term; the bare runs' verse was unmetred, and the
homage period came out as one 150-word sentence. What the skill leaves that the bare run cannot: a
construal file that records how each sentence was read, a glossary, source identification with Toh
numbers (it found the Uttaratantra citation and, on the Jewel Garland page, the Sahajasiddhi source
of a quotation with a meaning-flipping variant), and the MITRA flag. The cost is not the twentyfold we
expected: at max and xhigh the bare model spends most of its tokens thinking (one bare max run spent
126k output tokens on a page), so the skill costs about twice a bare run at max and four times one at
xhigh. The honest summary: on single pages the bare model at max effort already translates as
faithfully and reads as well; the skill's measurable value is the house-style English at lower
effort, the verse, and the audit trail. Its main design claim, consistency of bound terms and
citations across a long text, is not something a one-page test can measure and remains untested.

## What went well

- **Fidelity at the calibrated setting.** Three major errors in 116 units, one of them the pipeline's
  own (a `nas` sequence made a relative clause), two induced by MITRA before the rule against it. Relations (`las`, `pas`,
  `na`, `kyang`, `phyir`) survive; negations and quantifiers land; honorific speech acts are kept.
- **Doubts are visible.** Every page comes with `Q:` lines naming the construal that could go the
  other way; most of the judge's minor findings were already flagged as alternatives.
- **Source identification.** `dm.py identify` found the Uttaratantra citation (Toh 4024) with its
  folio, told apart a loose quotation of the Avadānaśataka from the citing text's own copy, and
  recorded "not located" honestly for a master's saying.
- **English.** Prose pages for practitioners scored 4.2–4.4 ("publishable after an editor's pass").
  A sample, Jigten Sumgön on the doors of Dharma (Stages of the Path, unit 12):

  > Therefore, for people whose minds have different ways in, putting different approaches to Dharma
  > into practice becomes the antidote to afflictions and conceptual thoughts. Then comes liberation,
  > and in the great ocean of liberation all phenomena become one taste. This is the crux of all the
  > scriptures of the Buddha, the Blessed One. … It delights the learned and makes the heads of the
  > deluded spin; it is the domain of those whose realization is profound and vast. Understand this,
  > and this alone, through and through.

  (The judge's one minor here: "Then comes liberation" makes a sequence of what is one locative
  frame. The alternative was in the `Q:` list.)
- **The MITRA cross-check earns its place, with a leash.** Over the Opus-max pages MITRA would have
  revealed 16 of the pipeline's 29 errors (relations and roles more than terms), at 0.2k tokens per
  unit; across all 30 judged pages, 67 of 147. It also talked one run into two wrong readings. It is
  now a standing step, as a flag, never a vote: a change needs a stated grammatical reason.
- **The published translations as a mirror.** Judge-confirmed slips in H ran three to seven per page
  in the Drikung books; the pipeline's `Q:` lists are a cheap second reading for a revised edition.

## Mistakes, and where they came from

| Source | What happened | Fix made |
|---|---|---|
| Segmenter (botok) | Negations absorbed into words (`'jug sgo ma lags sam` → "gatekeeper"; `ma dag zhing` → "pure land"), names split (`phyag na rdo rje`, `a ma na se`), affixes fused away (`char` → `cha` + r; `las` karma → `la` + s), feminine `-ma` read as a negation | `annotate` now prints a `NEG:` line with context, a `COMPOUND?` line, re-splits a final `ma` before a verb, notes fused and split alternatives; protected nouns and names listed |
| Lexicon first sense | `skyes pa` "man", `thogs med` "unobstructed" (Asaṅga), `'debs` "plant", `las` as ablative, `zhing` as connective, `shes` as quotative | documented in `analysis.md` §2a; the rule stays "all senses, grammar decides" |
| Source identification | "VERBATIM yes" when the long match was the citing text's own copy | verdict split into canonical / only non-canonical / NO; `--exclude <Toh>` for canonical citing texts; commentary hits are witnesses, not sources |
| Construal forks | the recorded alternative was sometimes the right one (a `nas` sequence made a relative clause; `rigs par` adverbial made an object; the head noun's apposition vs genitive) | `analysis.md` §2.10: head-noun forks always get a `Q:`; grammar decides between close branches, with the specific patterns named |
| MITRA | one correct reading (`skye bar byed` = begets) was changed on MITRA's word | a MITRA-prompted change must be justified in the construal's case-frame fields and re-pass the relation/role tests; otherwise it stays a `Q:` |
| Register | academic mode drifted into calques ("the very own-nature", bracket-heavy clauses): 3.3/5 on a Hevajra commentary | `modes.md`: documentary in apparatus, not in syntax; english.md gained rows for adverb calques (`mngon par` "manifestly"), nominal calques, demonstrative chains, interposed adverbials |
| Verse | enumerative stanzas under a 3–4 beat band came out as flat gerund lists (3.8) | wider measure for enumerative runs; a quoted two-line dictum may be set as prose; free-verse house styles handled without the metre loop |
| Tools, small | `--budget` did nothing; `segment --window` needed `--context`; MITRA's 10-per-minute limit; `beats.py` split IAST names and lacked ~60 words | all fixed |
| Harness | subagents in a workflow have no Agent tool, so the check ran in-context; the Skill tool serves the SKILL.md it loaded at session start | documented; `/reload-skills` after editing |

## Limitations (what the tool will not do for you)

- **It is a drafter with a conscience, not a translator.** Three major errors in ten pages is low,
  but not zero, and the minors (a dropped `yongs su`, a term that clashes with a bound one, a slightly
  over-specified word) are two a page. Read the `Q:` lines; they are where the risk is.
- **Verse is the weak flank.** Verse-heavy pages scored 3.8–3.9 even on Opus max: metrically clean,
  but stiff where the Tibetan is dense, and the judge called several stanzas "roughly" metred.
- **The fidelity check catches relation and role errors, not term choices.** On the run-2 pages the
  external checker caught none of the judge's minors and raised one or two false findings a page.
  The MITRA flag covers part of that gap; your own reading covers the rest.
- **The dictionary is only as good as its segmenter.** The new hint lines surface the known slips;
  they do not remove them. Sanskrit transliterations and rare names still need the reader's eye.
- **It is not more faithful than the bare model.** On the three baseline pages, scored by two
  judges each, bare Opus made fewer meaning errors than the skill at either effort and read as well
  at max. The dictionary pass, construal and fidelity check are an audit trail, not a safety net;
  twice they led a run toward a worse reading than the bare model chose.
- **Cost.** 250–400k tokens for a page on Opus max is roughly a tenth of a Max-5x five-hour window
  (and about half of a Pro window). The method is for careful work, not bulk.
- **Dharmamitra is a public research service.** One request at a time; it can be slow or down; the
  pipeline then skips identification and MITRA and says so.

## How to use it well

1. Opus at max effort for anything you intend to publish; xhigh if you must economize; Sonnet only
   with a Tibetan-reading reviser.
2. Give the brief once (audience, purpose, house style) in a `CLAUDE.md`; a project glossary binds.
3. Feed it a page at a time (5–12 units): the check and the MITRA call are per page.
4. Treat the `Q:` lines as the editor's list; treat `MITRA:` lines as "look again", not as a
   correction.
5. Keep the construal file: it is the record of how each sentence was read.

## Method notes

Reference material: the Vikramashila sentence alignments of four Edition Garchen Stiftung
translations (Rays of Sunlight, Stages of the Path, Single Intention, Scintillation; the last a relay
translation via German; the translators are credited in the published books) and 84000's
translations (CC BY-NC-ND 4.0; Toh 127, 113, 147, 381, 417, 431, 3808, 1189, 1183; Tibetan and
English pulled from 84000's own alignment data). The pipeline never saw the reference English. Judges
were Claude Opus agents in a fresh context with the Tibetan, the construal, C, H and M, using the
protocol in `tests/campaign_2026-10-03/judge_prompt_template_v2.md`; their reports are beside each
run. Token figures are new tokens per run computed from the agent transcripts (`wf_tokens.py`). The
bare-model baseline (4 October) used the judge template without the checker-recall section, with the
construal line replaced by "none (bare run); judge from the Tibetan"; its prompts, outputs and judge
reports are in `tests/campaign_2026-10-03/baseline/`. The second judging round (`judge2.md` beside
each `judge.md`) used the same template with the first report withheld; the skill's Opus-max re-run
on the three pages is `runs/run4_opus_max/` with two judges each. With two judges per output the
judge-to-judge spread on one page was up to two major errors, which is the resolution of every
per-page figure in this report.
Caveats: one judge per page (no inter-judge agreement measured); the judge and the drafter are the
same model family; briefs for the 84000 pages were written quickly and were wrong in small ways
(pada counts) that the runs noticed and flagged; the final matrix ran on the skill as of the run-2
fixes, with two small text edits landing while it ran. The Vikra reference translations are not
redistributed in the repository.

Orchestrated by Claude Fable 5.1 with Opus and Sonnet subagents, 3 October 2026, for Gabriel Kobler.
