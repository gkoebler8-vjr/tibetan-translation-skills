# Tibetan translation skills — overhaul report, 2026-10-03

Done on Fable at max effort, with three Opus/Sonnet research agents and two Opus test agents.

## 1. What changed

| Before (Opus build, 2026-09-02) | After |
|---|---|
| Four skills, each a possible entry point: tibetan-mitra, tibetan-prose, tibetan-verse, tibetan-citations | One entry point, **tibetan-translate**, which detects verse and loads tibetan-verse; tibetan-citations and **tibetan-dharmamitra** are companions. tibetan-prose and tibetan-mitra archived to `~/.claude/skills_archive/` |
| Construal written by the model from memory; no dictionary; MITRA local model never installed | **tibdict.py**: offline index of the MITRA Tibetan Lexicon (237k headwords) plus your GoldenDict folder (Hopkins, 84000, Rangjung Yeshe, Monlam, Valby, Duff, Das, Mahāvyutpatti, Hackett, verb-stem tables); botok segmentation; one call per unit |
| Source identification by hand, 84000 page fetch only | **dm.py**: Dharmamitra's public APIs from the sandbox (search → Toh number and segment id; parallels → variant readings; segment --context → a commentary's gloss; MITRA translate → second opinion) |
| No explicit audience | **Pass 0 brief**: audience (academic / new practitioner / seasoned practitioner / hybrid), purpose, house style; the skill asks once if these are not known; `reference/modes.md` turns the audience into concrete settings |
| One pass, self-checked | Four passes: structured analysis → faithful draft → one style pass → **fidelity check in a fresh subagent** (error spans only, one targeted revision) |
| Verse spec v3.2: band n/n+1 with one outlier; em dashes and contractions banned | **v4**, calibrated on your 135 finished LZ verse blocks: one rhythmic kind per block is the hard rule; band of two counts target, three tolerated, four flagged; bound term over metre; house style decides capitals, contractions, dashes, prose setting |

## 2. What the finished LZ verses actually do (summary; full analysis in `~/.claude/skills/tibetan-verse/reference/lz-practice.md`)

- Only 48 % of your final lines are strict iambic at a single measure; 14 of 135 blocks are fully clean. The finished practice is accentual-iambic with a constant pulse and a line length that flexes inside a band. Lines run 8–12 syllables (median 10), 3–5 beats on the flat read.
- 100 % consistent on rhythmic kind: every block is rising throughout; initial inversions are common and never read as a change.
- Bound terms never give (*primordial awareness* in all ~25 verse occurrences); word order never gives; relation particles always land (`las`, `pas`, `na`, `kyang`, `phyir`), often at line head.
- Line correspondence is the mode, with unpacking of dense padas and one-per-line lists; permutation is used only to bring the predicate or governing noun first (2.1/47, 2.4.4.1/05, 2.4.4.4.1/30).
- Line-initial capitals (R8), 35 em dashes, 21 contractions (R54), no rhyme, end-stopping by default, long padas set as near-prose lines (R53).
- `beats.py` under the v4 rule passes 105 of the 135 blocks cleanly, flags 22 as wide, fails 8 (multi-stanza quotations run together and the R53 prose-set blocks). Checked per stanza it is tighter.

## 3. Dharmamitra: what is possible

- The sandbox **has network** (the handover note was stale). Everything below runs from Claude's shell.
- Keyless, documented endpoints: `/api-search/primary/` (the engine under Explore's "Database Results"), `/api-db/matches/` (parallels), `/api-db/text-view/text-parallels/` (segment in context), `/api-search/cat-translate/v1/translate` (the hosted MITRA Qwen3.5). The Explore AI summary is a Gemini-backed BFF endpoint; it also works keyless but is slow and secondary. Grammar-explain and the per-segment "Explanation" need an API key they do not publish.
- Coverage: Kangyur, Tengyur, Nyingma Kama/Terma, Sakya, ACIP sungbums, the Tsadra series (Drikung Gongchig, Jigten Sumgön, Gampopa, Phagmodrupa, Götsangpa, Mikyö Dorje), Lotsawa House, Edition Garchen Stiftung.
- On the sample verse (`rnam rtog ma rig chen po ste …`) `dm.py identify` returns the Sampuṭa (Toh 381, D 158a), the Vajrahṛdayālaṃkāra (Toh 451) and the Māyājāla (Toh 466) as canonical sources, the Bodhipathapradīpa and five Tengyur commentaries, and 82 later works that quote it; `parallels` gives the variants (`gti mug` / `ma rig` / `rmongs pa`; `'gyur` / `mngon` / `snang` / `gsal`); `segment --context` on a commentary hit gives its attribution and gloss. ~2.5k characters for the whole identification.
- Terms: personal research use; not to be built into a hosted product. Dharmamitra's own Claude Code starter pack does exactly this kind of use. Worth a courtesy email to dharmamitra.project@gmail.com if the pipeline becomes routine.
- The local MITRA install is now optional: the hosted `translate` endpoint is the same Qwen3.5 model.

## 4. Research findings that shaped the design (full brief: `~/.claude/skills/tibetan-translate/reference/research.md`)

- Multi-pass helps when the analysis pass produces checkable structure (Briakou et al. 2024); free-form decomposition does not (Wu, Aycock & Monz 2025); parallel examples and glossary options beat grammar prose in the prompt (Aycock et al. 2025); a separate GEMBA-style span check is the best error detector in the Buddhist domain (MITRA-zh-eval 2025; Metzger 2026), and a model should not grade its own draft (Panickssery 2024; Huang 2024).
- Translation practice: skopos/audience decides the contract (84000 vs Hopkins vs Padmakara vs LoTC); the imperial decree allows free syntax inside a stanza while keeping the stanza; no major English house imitates Tibetan syllabics; 84000's style rules are the clearest written standard for a reader edition; 84000's AI policy bars AI first drafts of canonical texts.

## 5. How to use it

```
/tibetan-translate   (or just ask to translate a Tibetan passage)
```
Give the audience and house style once, or let it ask. For a project, put them in CLAUDE.md or a
workflow file and the skill will use that. Tools can be run directly:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "<tibetan or wylie>"
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py lookup "ye shes" --full --examples
python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "<quoted lines>"
python3 ~/.claude/skills/tibetan-translate/tools/dm.py translate "<tibetan>" --style "literal, keep every clause"
python3 ~/.claude/skills/tibetan-verse/tools/beats.py citation "line one," "line two,"
```

The dictionary index is at `~/.tibdict/tibdict.sqlite` (rebuild: `tibdict.py build`, 20 s). botok
and pyewts live in `~/.venvs/tib`.

## 6. Test runs (two Opus subagents, default effort, each with a Sonnet checker)

**Verse, 2.4.4.4.1/30** (`sems nyid kyi nam mkha' yangs pa la …`), brief: seasoned practitioner, LZ house style.

> In the vast sky of mind itself, / Unless the massed clouds of conceptual thought have cleared, /
> The stars and planets of the two knowings don't shine, / So persevere in this non-conceptual mind.

Your final: *If the clouds of thoughts do not disperse and clear / Within the vast and open sky of
mind itself, / The stars of the two knowings will not shine: / Therefore, persevere in
non-conceptuality.* Same construal, same relations (`na` condition, `bas` cause, `mdzod`
imperative), bound terms held, order 1-2-3-4; line 2 heavier than yours. `dm.py identify`
correctly found no verbatim source (a master's saying). Checker: 0 major, 4 minor.

**Prose, 1.3/05–1.3/11** (the five ways of relying on the guru), same brief.

> Rely on the guru without growing weary of hardship and suffering. And since relying on him for
> just a short while is not enough, rely on him until you attain awakening. Through the arising in
> your mindstream of bodhicitta, in which emptiness and compassion are inseparable, you should come
> to realize the guru's intent. The guru's words are the very heart of all the Dharma, so practice
> exactly in accord with the instructions he has given. In this degenerate age, even though the
> guru is in essence a buddha, he cannot tame his disciples' minds unless he acts, through the
> conduct of skillful means, in whatever way will tame them. So give up any disrespect for anything
> the guru does, and cultivate the perception that he is a buddha. Thus the sutra teaches five
> ways of relying on the guru.

Close to your merged final; every connective survives. One genuine divergence worth your eye:
`snyigs ma'i dus 'dir ngo bo sangs rgyas yin yang` — your final reads the elided subject as
"every being"; the pipeline (and MITRA independently) reads it as the guru ("even though the guru
is in essence a buddha, unless he acts with skillful means …"), which is also what the following
`gdul bya … 'dul ba de ltar ma mdzad na` wants. Q for the Vikramashila list. Checker: 0 major, 3
minor (one real: a mixed means/temporal reading of `skyes pas`, fixed).

**Cost.** ~88k tokens for the main agent and ~52–57k for the checker in each test, i.e. ~140k per
unit. The logs showed where it went: ~50k characters of reference files read up front, and the
checker's cost is almost all harness overhead (its system context), not the check. Fixes applied:
references read on need, not up front; the fidelity check batched per page (one spawn for 5–12
units) with an in-context check for a single unit; the unit may be one whole Tibetan period;
`tibdict --brief`; the gate and header now have autonomous-run and "source not located" slots;
`dm.py identify` prints a VERBATIM MATCH line so semantic neighbours are not mistaken for a
source; `la ma gus pa` mis-segmentation fixed; 46 words added to the stress lexicon. Expected now:
~40–60k for a first unit, 15–25k per further unit, plus one ~55k check per page.

**MITRA second opinion on the same two units** (`dm.py translate`): both correct, both agree with
the pipeline against your "every being" reading; no error in the pipeline's output that MITRA
would have caught. Two units is not evidence either way; the protocol in
`~/.claude/skills/tibetan-dharmamitra/reference/compare.md` is the real test.

## 7. To do

1. **Claude vs MITRA comparison** on a finished page, per `~/.claude/skills/tibetan-dharmamitra/reference/compare.md`: decide whether the MITRA second opinion earns a permanent place.
2. Glossary title drift (from the previous handover): `dpal phreng gi mdo`, `sgyu 'phrul dra ba'i rgyud`, `yang dag par sbyor ba` have multiple English forms; `register.py --titles 03_Terminology/LZ_Running_Glossary.tsv`.
3. Optional: wire the construal stage into the LZ passes (Pass A could read `<work>.construal.md`).
4. Optional: a `--mitra` flag in tibetan-translate to run the second opinion automatically for hard units once the comparison says it is worth it.
5. Optional: email Dharmamitra about routine use of the APIs.
