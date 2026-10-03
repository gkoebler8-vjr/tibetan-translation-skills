TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/84000/shastra_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run1_opus_max/Sh_shastra
Work name for the files: shastra

BRIEF (Pass 0 is already answered; do not ask):
Audience: academic. Purpose: publication (a scholarly translation of a Tengyur commentary). IAST with full diacritics for Sanskrit names and terms (Śāriputra, arhat → arhat, tathāgata, prajñāpāramitā); square-bracket interpolations allowed and expected where the Tibetan elides; the Question/Response/Qualm structure of the scholastic exchange marked as the Tibetan marks it; neutral-scholarly register, no elevation; footnote-style notes allowed in the apparatus block; doubts in the notes with alternatives. Start a glossary.
Source context: the Bṛhaṭṭīkā (Toh 3808), the long explanation of the Perfection of Wisdom in 100,000, 25,000 and 18,000 lines, attributed to Daṃṣṭrasena or Vasubandhu; introduction, "presentation of the single vehicle system". The passage is a scholastic debate on why the Buddha addresses Śāriputra alone, whether an arhat whose contaminants are exhausted can be predicted to buddhahood, and the single-vehicle position. Units are 84000 paragraphs and may contain several Tibetan sentences; keep each unit together but split into English sentences freely. Prose throughout.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the units as ONE PAGE: build `shastra.construal.md` and `shastra.glossary.tsv` incrementally, draft all units, run the style pass, then spawn the fidelity checker ONCE for the whole page (Agent tool, per reference/check.md; pass file paths). If the Agent tool is unavailable to you, do the in-context check and say so.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). `dm.py translate` (MITRA) is NOT to be used in this run.
4. Keep `<scratchpad>/runs/run1_opus_max/Sh_shastra/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run1_opus_max/Sh_shastra/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
