TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/84000/sutra_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run1_opus_max/S_sutra
Work name for the files: sutra

BRIEF (Pass 0 is already answered; do not ask):
Audience: new practitioner. Purpose: publication (a reader edition for educated non-specialists, in the manner of the 84000 Reading Room prose: common Buddhist words anglicized without diacritics — sutra, samadhi, bodhisattva, nirvana, samsara, tathagata; technical terms translated into English wherever a good English term exists; no square brackets, Wylie or locators in the body).
House style: verse as free verse, line for line, one English line per pada, not metred; no contractions; speaker formulas plain ("the Blessed One said"); doubts as Q: lines for the editor. Start a glossary.
Source context: the King of Samādhis Sūtra (Toh 127, Samādhirājasūtra), chapter 4. The Buddha answers the youth Candraprabha by defining the samādhi as a list of qualities (U01–U05 are the continuation of one long enumeration; U06 is the transition sentence introducing the verses); U07–U12 are six stanzas (7-syllable padas, four per stanza) in the Buddha's voice summarizing the same. The list items are nominal phrases joined by dang: render them as a list of "It is …" sentences or as a running list, per the English standard; do not number them.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the units as ONE PAGE: build `sutra.construal.md` and `sutra.glossary.tsv` incrementally, draft all units, run the style pass, then spawn the fidelity checker ONCE for the whole page (Agent tool, per reference/check.md; pass file paths). If the Agent tool is unavailable to you, do the in-context check and say so.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). `dm.py translate` (MITRA) is NOT to be used in this run.
4. Keep `<scratchpad>/runs/run1_opus_max/S_sutra/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run1_opus_max/S_sutra/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
