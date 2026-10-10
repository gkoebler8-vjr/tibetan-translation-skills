TASK: translate one test page with the tibetan-translate skill (pipeline v2), end to end, exactly as the skill prescribes, and leave a measurable trail. This is the first run of v2: note anything in the skill text that is unclear, contradictory or impossible to follow.

Page file (Tibetan units, one per `Uxx` line; the parenthesis after the id is a hint, not part of the text): <repo>/tests/campaign_2026-10-03/material/vikra/rays_units.md
Run directory (create it; all work files go here): <repo>/tests/campaign_2026-10-03/runs/run5_v2_smoke/V1_rays
Work name for the files: rays

BRIEF (Pass 0 is already answered; do not ask):
Audience: seasoned practitioner. Purpose: publication (a reader edition in the manner of Edition Garchen Stiftung's Drikung Kagyü translations).
House style: Sanskrit technical terms anglicized without diacritics where the tradition uses them (dharmakaya, sambhogakaya, nirmanakaya, sutra, tantra, mara, samsara, nirvana, bodhisattva); Tibetan names phonetic (Jigten Sumgön, Phagmodrupa, Drikung); no square brackets, Wylie or locators in the body; verse citations rendered by tibetan-verse in citation mode; no contractions; em dashes allowed; doubts as Q: lines for the editor, not in the body. No project glossary exists yet: start one.
Source context: Ayang Thubten Rinpoche (1899–1966), nyi ma'i 'od zer, a commentary on Zhedang Dorje's theg chen bstan pa'i snying po (a Drikung lam rim root text). This page is the commentary's own opening: the expression of worship (one long homage period addressed to Shakyamuni, U01–U05 are one Tibetan sentence), a verse citation from the rgyud bla ma (Uttaratantra; U06–U09 are one sentence running across four stanzas of 7-syllable padas, the Tibetan as given lacks one canonical pada), and the commitment to explain (U10–U12). The commentator speaks; register: homage, then exposition.
Notes policy: reader footnotes per the seasoned-practitioner column of notes.md (no locators in footnotes; sources to the register); editor notes in full.

RULES FOR THIS RUN
1. Invoke the skill with the Skill tool (`tibetan-translate`) first, then read `~/.claude/skills/tibetan-translate/SKILL.md` from disk: the on-disk text is authoritative. Follow it, including the references it tells you to read and when. You are running autonomously: take the brief above as given, state the model/effort line as the skill asks, and proceed.
2. Treat the 12 units as ONE PAGE: your own reading and draft of all units with the construal sketch in `rays.construal.md` and the glossary in `rays.glossary.tsv`; then the grounding pass (identify for the citation, explore on the clauses in doubt or doctrinally loaded, segment/parallels as needed, MITRA once with --file); then the style pass; then the in-context check; then the notes and footnotes.
3. Never open, search for, or guess at any existing human translation of this passage (no files named reference_H, no web lookups of the English, no 84000 pages).
4. Keep `<repo>/tests/campaign_2026-10-03/runs/run5_v2_smoke/V1_rays/runlog.md` as you go: one line per reference file you read (path, when), one line per tool call (tibdict / dm.py / beats.py) with the unit id and what it returned in five words, and the time you started and finished.
5. Final deliverable: `<repo>/tests/campaign_2026-10-03/runs/run5_v2_smoke/V1_rays/final.md` containing, for each unit in order, exactly the block the skill's §8 and notes.md §4 specify:

   ### Uxx
   HEADER: <one line>
   TEXT:
   <the finished English; verse lines one per line>
   FOOTNOTES:
   <FN(anchor): … lines, or "none">
   NOTES:
   <the editor notes, or "none">

   then a closing section `## Run summary` with: units done, grounding calls made and what each found, check line, references read, your estimate of where the tokens went, and a list of problems in the skill text (unclear, contradictory, or impossible steps) with the file and section.
6. Your reply to me is only: the path of final.md, the check line, the grounding summary in two lines, and the problems list. Do not paste the translation into the reply.
