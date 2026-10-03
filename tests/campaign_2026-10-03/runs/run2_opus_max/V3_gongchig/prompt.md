TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/vikra/gongchig_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run2_opus_max/V3_gongchig
Work name for the files: gongchig

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: publication (a reader edition in the manner of Edition Garchen Stiftung's Drikung Kagyü translations).
House style: Sanskrit technical terms anglicized without diacritics where the tradition uses them (dharmakaya, mahamudra, sutra, tantra, mara, samsara, nirvana, bodhisattva); Tibetan names phonetic (Jigten Sumgön, Phagmodrupa, Drikung, Sherab Jungne); no square brackets, Wylie or locators in the body; verse citations rendered by tibetan-verse in citation mode; no contractions; em dashes allowed; doubts as Q: lines for the editor, not in the body. No project glossary exists yet: start one.
Source context: Khenpo Kunpal's (Kunzang Palden's) commentary on the Single Intention (dgongs gcig) of Jigten Sumgön, introductory section explaining the term. The commentator quotes the Great Overview (khog dbub chen mo, by Sherab Jungne, prose), a four-line verse of Shamar Chökyi Drakpa (9-syllable padas), and the Sutra Requested by Anavatapta (prose). U01 is colloquial in tone (yod tshod mi 'dug). Register: commentary exposition with quotations; the framing sentences name the source. In U02 'bri gung gling pa is Sherab Jungne.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first and follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed even if the effort is not maximum (say so once).
2. Treat the units as ONE PAGE: build `gongchig.construal.md` and `gongchig.glossary.tsv` incrementally, draft all units, run the style pass, then run the fidelity check per the skill (if the Agent tool is available spawn the checker ONCE for the whole page with file paths; otherwise the in-context check, saying so), apply the one revision round, then the MITRA cross-check as the skill now prescribes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). The skill's MITRA cross-check (`dm.py translate --file`) is run exactly where the skill places it: once, after the fidelity check, never before drafting.
4. Keep `<scratchpad>/runs/run2_opus_max/V3_gongchig/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run2_opus_max/V3_gongchig/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
