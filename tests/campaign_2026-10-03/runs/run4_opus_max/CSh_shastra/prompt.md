TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <repo>/tests/campaign_2026-10-03/material/84000/C_shastra_units.md
Run directory (create it; all work files go here): <repo>/tests/campaign_2026-10-03/runs/run4_opus_max/CSh_shastra
Work name for the files: shastra

BRIEF (Pass 0 is already answered; do not ask):
Audience: academic. Purpose: publication (a scholarly translation of a Tengyur commentary). IAST with full diacritics for Sanskrit names and terms; square-bracket interpolations allowed where the Tibetan elides; the commentary's scaffold kept (the root words quoted, "means", the gloss); root verses quoted inside the commentary are set as verse blocks; neutral-scholarly register; notes allowed in the apparatus block; doubts in the notes with alternatives. Start a glossary.
Source context: Kāṇha's Jewel Garland of Yoga (Toh 1183, Yogaratnamālā), a Hevajra commentary, part I chapter 1, early in the text; the commentator quotes root padas and glosses them; several units end on a lead-in formula ('as is said') whose quotation follows outside the span: end the English on the lead-in too.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first, then read `~/.claude/skills/tibetan-translate/SKILL.md` from disk: the Skill tool may serve a cached older copy, and the on-disk text is authoritative. Follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the 12 units as ONE PAGE: build `shastra.construal.md` and `shastra.glossary.tsv` incrementally, draft all units, run the style pass, then run the fidelity check per the skill (if the Agent tool is available spawn the checker ONCE for the whole page with file paths; otherwise the in-context check, saying so), apply the one revision round, then the MITRA cross-check as the skill now prescribes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). The skill's MITRA cross-check (`dm.py translate --file`) is run exactly where the skill places it: once, after the fidelity check, never before drafting.
4. Keep `<repo>/tests/campaign_2026-10-03/runs/run4_opus_max/CSh_shastra/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<repo>/tests/campaign_2026-10-03/runs/run4_opus_max/CSh_shastra/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
