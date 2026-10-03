TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/vikra/stages_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run1_opus_max/V2_stages
Work name for the files: stages

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: publication (a reader edition in the manner of Edition Garchen Stiftung's Drikung Kagyü translations).
House style: Sanskrit technical terms anglicized without diacritics where the tradition uses them (dharmakaya, sambhogakaya, nirmanakaya, sutra, tantra, mara, samsara, nirvana, bodhisattva); Tibetan names phonetic (Jigten Sumgön, Phagmodrupa, Drikung); no square brackets, Wylie or locators in the body; verse citations rendered by tibetan-verse in citation mode; no contractions; em dashes allowed; doubts as Q: lines for the editor, not in the body. No project glossary exists yet: start one.
Source context: Jigten Sumgön (1143–1217), a lam rim teaching from his collected works (recorded by Ön Sherab Jungne; published as "On the Dharma of the Stages of the Path"). The passage argues that the three higher trainings have no fixed order and that every Dharma door leads inside; it rebukes sectarian dismissal of other traditions. Register: exposition/debate with rhetorical questions, shifting to instruction at the end; U10 is a prose citation attributed to the Avadānaśataka (rtogs pa brjod pa brgya pa), U11 a saying of Phagmodrupa (the "precious guru, protector of the three worlds"). The text uses the honorific interrogative lags sam.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the 12 units as ONE PAGE: build `stages.construal.md` and `stages.glossary.tsv` incrementally, draft all units, run the style pass, then spawn the fidelity checker ONCE for the whole page (Agent tool, per reference/check.md; pass file paths). If the Agent tool is unavailable to you, do the in-context check and say so.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). `dm.py translate` (MITRA) is NOT to be used in this run.
4. Keep `<scratchpad>/runs/run1_opus_max/V2_stages/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run1_opus_max/V2_stages/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
