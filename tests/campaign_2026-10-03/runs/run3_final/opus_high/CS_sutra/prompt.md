TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/84000/C_sutra_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run3_final/opus_high/CS_sutra
Work name for the files: sutra

BRIEF (Pass 0 is already answered; do not ask):
Audience: new practitioner. Purpose: publication (a reader edition for educated non-specialists, in the manner of the 84000 Reading Room prose: common Buddhist words anglicized without diacritics — sutra, bodhisattva, nirvana, samsara, tathagata, buddha; technical terms translated into English wherever a good English term exists; no square brackets, Wylie or locators in the body).
House style: verse as free verse, line for line, one English line per pada, not metred; no contractions; speaker formulas plain; doubts as Q: lines for the editor. Start a glossary.
Source context: The Great Compassion of the Tathāgata (Toh 147, Tathāgatamahākaruṇānirdeśa), chapter 2; a numbered list of items runs through the prose (the numbers are 84000's, not in the Tibetan; do not add numbers), followed by verse.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first, then read `~/.claude/skills/tibetan-translate/SKILL.md` from disk: the Skill tool may serve a cached older copy, and the on-disk text is authoritative. Follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed whatever the effort setting is (say so once; this run measures that setting).
2. Treat the units as ONE PAGE: build `sutra.construal.md` and `sutra.glossary.tsv` incrementally, draft all units, run the style pass, then run the fidelity check per the skill (if the Agent tool is available spawn the checker ONCE for the whole page with file paths; otherwise the in-context check, saying so), apply the one revision round, then the MITRA cross-check as the skill now prescribes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). The skill's MITRA cross-check (`dm.py translate --file`) is run exactly where the skill places it: once, after the fidelity check, never before drafting.
4. Keep `<scratchpad>/runs/run3_final/opus_high/CS_sutra/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run3_final/opus_high/CS_sutra/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
