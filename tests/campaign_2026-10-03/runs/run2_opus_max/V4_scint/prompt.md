TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/vikra/scint_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run2_opus_max/V4_scint
Work name for the files: scint

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: publication (a reader edition in the manner of Edition Garchen Stiftung's Drikung Kagyü translations).
House style: Sanskrit technical terms anglicized without diacritics where the tradition uses them (dharmakaya, mahamudra, sutra, tantra, mara, samsara, nirvana, bodhisattva); Tibetan names phonetic (Jigten Sumgön, Phagmodrupa, Drikung, Sherab Jungne); no square brackets, Wylie or locators in the body; verse citations rendered by tibetan-verse in citation mode; no contractions; em dashes allowed; doubts as Q: lines for the editor, not in the body. No project glossary exists yet: start one.
Source context: the biography of Jigten Sumgön by Chenga Sherab Jungne (Scintillation of the Precious Vajra, rnam thar). Narrative register with dialogue and honorifics: rje gong ma (the former lord) is Phagmodrupa; rje rin po che and rin po che are Jigten Sumgön; dge ba'i bshes gnyen bkra shis sgang pa is Geshe Tashi Gangpa; the disciples ask whether Jigten Sumgön is a tenth-level bodhisattva or Vajrapani, he answers in the first person, roars the lion's roar in the assembly, and is asked where he will go after nirvana. The page file has the units in Unicode and, below, the same units again in Wylie for reference: translate the 11 Unicode units once.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the units as ONE PAGE: build `scint.construal.md` and `scint.glossary.tsv` incrementally, draft all units, run the style pass, then run the fidelity check per the skill (if the Agent tool is available spawn the checker ONCE for the whole page with file paths; otherwise the in-context check, saying so), apply the one revision round, then the MITRA cross-check as the skill now prescribes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). The skill's MITRA cross-check (`dm.py translate --file`) is run exactly where the skill places it: once, after the fidelity check, never before drafting.
4. Keep `<scratchpad>/runs/run2_opus_max/V4_scint/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run2_opus_max/V4_scint/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
