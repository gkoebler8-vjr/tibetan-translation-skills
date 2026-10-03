TASK: translate one test page with the tibetan-translate skill, end to end, exactly as the skill prescribes, and leave a measurable trail.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <scratchpad>/material/vikra/rays_units.md
Run directory (create it; all work files go here): <scratchpad>/runs/run3_final/opus_high/V1_rays
Work name for the files: rays

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: publication (a reader edition in the manner of Edition Garchen Stiftung's Drikung Kagyü translations).
House style: Sanskrit technical terms anglicized without diacritics where the tradition uses them (dharmakaya, sambhogakaya, nirmanakaya, sutra, tantra, mara, samsara, nirvana, bodhisattva); Tibetan names phonetic (Jigten Sumgön, Phagmodrupa, Drikung); no square brackets, Wylie or locators in the body; verse citations rendered by tibetan-verse in citation mode; no contractions; em dashes allowed; doubts as Q: lines for the editor, not in the body. No project glossary exists yet: start one.
Source context: Ayang Thubten Rinpoche (1899–1966), nyi ma'i 'od zer, a commentary on Zhedang Dorje's theg chen bstan pa'i snying po (a Drikung lam rim root text). This page is the commentary's own opening: the expression of worship (one long homage period addressed to Shakyamuni, U01–U05 are one Tibetan sentence), a verse citation from the rgyud bla ma (Uttaratantra; U06–U09 are one sentence running across four stanzas of 7-syllable padas, the Tibetan as given lacks one canonical pada), and the commitment to explain (U10–U12). The commentator speaks; register: homage, then exposition.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first, then read `~/.claude/skills/tibetan-translate/SKILL.md` from disk: the Skill tool may serve a cached older copy, and the on-disk text is authoritative. Follow it. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed whatever the effort setting is (say so once; this run measures that setting).
2. Treat the units as ONE PAGE: build `rays.construal.md` and `rays.glossary.tsv` incrementally, draft all units, run the style pass, then run the fidelity check per the skill (if the Agent tool is available spawn the checker ONCE for the whole page with file paths; otherwise the in-context check, saying so), apply the one revision round, then the MITRA cross-check as the skill now prescribes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages). Dharmamitra `dm.py identify` is allowed where the skill calls for it (quotations only). The skill's MITRA cross-check (`dm.py translate --file`) is run exactly where the skill places it: once, after the fidelity check, never before drafting.
4. Keep `<scratchpad>/runs/run3_final/opus_high/V1_rays/runlog.md` as you go: one line per reference file you read (path, when: before first unit / later), one line per tool call (tibdict / dm.py / beats.py / Agent) with the unit id, and the time you started and finished. Be honest; this log is the measurement.
5. Final deliverable: `<scratchpad>/runs/run3_final/opus_high/V1_rays/final.md` containing, for each unit in order, exactly this block:

   ### Uxx
   HEADER: <the skill's one-line header>
   TEXT:
   <the finished English; verse lines one per line>
   NOTES:
   <the skill's Q:/Alt:/Issue:/Source:/Check: lines, or "none">

   then a closing section `## Run summary` with: units done, number of checker spawns, checker verdict line, references read, and your own estimate of where the tokens went.
6. Your reply to me is only: the path of final.md, the checker verdict line, and any problem you hit (a tool error, a slip in the skill text, a missing file). Do not paste the translation into the reply.
