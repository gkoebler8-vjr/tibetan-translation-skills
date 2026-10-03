TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/84000/tantra_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run1_opus_max/T_tantra
Work name for the files: tantra

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: study aid (a working translation for practitioners who know the tantric vocabulary). Technical terms kept where the tradition uses them, anglicized without diacritics (vajra, mandala, dharmakaya, samsara); no square brackets or Wylie in the body; verse metred per tibetan-verse in citation mode (a band of two adjacent counts, one rhythmic kind per stanza), one English line per pada where the sense allows; no contractions; doubts as Q: lines. Start a glossary.
Source context: Emergence from Sampuṭa (Toh 381, Sampuṭodbhava Tantra), chapter 1. A dialogue: Vajragarbha questions the Blessed One about the emptiness of the sense faculties and their consciousnesses, the Blessed One answers; the stanzas then describe the nondual secret of all buddhas and the investigation of rebirth destinies. Two stanzas carry a prose speaker introduction (rdo rje snying pos gsol ba / bcom ldan 'das kyis bka' stsal pa); set those as a plain prose line before the stanza. All 12 units are 7-syllable verse, four padas each.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the units as ONE PAGE: build `tantra.construal.md` and `tantra.glossary.tsv` incrementally, draft all units, run the style pass, then spawn the fidelity checker ONCE for the whole page (Agent tool, per reference/check.md; pass file paths). If the Agent tool is unavailable to you, do the in-context check and say so.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). `dm.py translate` (MITRA) is NOT to be used in this run.
4. Keep `<scratchpad>/runs/run1_opus_max/T_tantra/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run1_opus_max/T_tantra/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
