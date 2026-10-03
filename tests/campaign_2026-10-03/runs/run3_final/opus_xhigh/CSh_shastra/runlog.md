# runlog — shastra (CSh, Toh 1183 Yogaratnamālā 1.1.98–109)
START: 2026-10-03 20:25:38
Model/effort: Claude Opus 5.5 (claude-opus-5-5); effort set by harness (reasoning effort appears below maximum / unverifiable) — proceeding autonomously outside the calibrated setting, as the brief instructs.

## Reference reads
- prompt.md (task file) — before first unit
- material/84000/C_shastra_units.md (page units) — before first unit
- Skill tool tibetan-translate (cached SKILL.md) — before first unit
- ~/.claude/skills/tibetan-translate/SKILL.md (on-disk, authoritative; differs from cached copy: adds the "change on MITRA's word alone is a defect" paragraph) — before first unit
- ~/.claude/skills/tibetan-translate/reference/english.md — before first unit
- ~/.claude/skills/tibetan-translate/reference/analysis.md — before first unit (first construal of session)
- ~/.claude/skills/tibetan-translate/reference/prose.md — before first unit (first prose unit)
- ~/.claude/skills/tibetan-translate/reference/modes.md — before first unit (academic column)
- ~/.claude/skills/tibetan-verse/SKILL.md (on-disk) — before first verse unit U02 (after U01 construal; not invoked via Skill tool)
- ~/.claude/skills/tibetan-translate/reference/check.md — later (about 20:42, after the style pass, before the fidelity check)

## Tool calls (in order; per-call clock times omitted — the minute stamps I first wrote were estimates, not clock readings, and have been removed. Real anchors from file mtimes: draft 20:41, style 20:42, check 20:43, MITRA output 20:45, final 20:48)
- tibdict annotate — U01
- tibdict annotate — U02 (botok slip: fused 'shing dbang' = 'lord of trees'; read as bkrus shing + dbang bskur bas)
- (reference re-read) ~/.claude/skills/tibetan-translate/reference/modes.md — re-read at 20:27 after harness notice that it changed on disk (new paragraph: "Academic mode is documentary in its apparatus, not in its syntax") — before first draft (after U01/U02 annotate)
- dm.py identify — U02 (VERBATIM yes, canonical, but the hit is the citing text itself, Toh 1183 6a; Hevajra Tantra Toh 417 not among candidates)
- tibdict annotate — U03 (slip: de nyid glossed 'suchness'; here 'those very')
- dm.py identify — U04 (VERBATIM yes, canonical: Toh 1190, 2255, 2244 carry both padas; Hevajra Tantra Toh 418 D17a-11 matches pada 1 only, pada 2 reads 'bzhi bde yang de bzhin no')
- dm.py segment BO_K12_D0418:17a-11 --context — U04 (Kangyur reading of the source verse; U02 verse not in this window)
- tibdict annotate --budget 6000 — U05 (slips: 'las kyi phyag rgya' split with las as ABL = karmamudrā; NEG false positive 'skad cig ma'; 'phyir mi ldog pa' split = irreversible; rig par bya glossed 'primordial awareness'; ro = 'taste')
- tibdict annotate --budget 6000 — U06 (slips: 'la yang gsang' fused to 'yang gsang' most secret — read phyogs la yang | gsang bar gnas pa'i; NEG list includes skad cig ma false positive; 'de lta bu' split 'son'; ro = 'taste')
- tibdict annotate --budget 6000 — U07 (slips: snying gi nor bu = 'darling' (MITRA) — here 'the jewel at the heart'; NEG false positives skad cig ma, sgyu ma; yongs su gyur pa read as 'transformed')
- tibdict annotate --budget 6000 — U08 (slips: 'de yang | dag pa'i mtha'' — read de bzhin nyid de | yang dag pa'i mtha'; 'rnams la don' fused to 'la don' grammatical term — read rnams la | don gyi khyad par; 'shing dbang' again; don = 'Don (name)'; NEG list: 4 real (yod pa ma yin, bcad pa ma yin, med par, 'gyur ba ma yin) + dri ma false positive)
- tibdict annotate — U09 (slips: 'ji ltar mi' fused = 'a human being' — read ji ltar | mi 'gyur (NEG); mod = 'moment' — here concessive 'though'; 'de kho na nyid' split)
- dm.py identify — U10+U11 (one quotation, 8 padas; VERBATIM yes, canonical, but only the citing text itself, Toh 1183 D 7a-15, run 38; neighbours = pramāṇa commentaries Toh 4221/4226/4229/4225 with runs ≤5 — not cited; source not located)
- tibdict annotate — U10
- tibdict annotate — U11 (slips: rgyas = 'China' first sense — verb 'grow/spread'; rgyud = 'tantra' — here 'mind stream'. NB the text reads rtog par (conceive) not rtogs par (realize); my U10–U11 identify query had typed 'rtogs par' — mismatch noted, does not change the not-located result)
- tibdict annotate — U12 (slips: ram = seed syllable raṃ — here question particle ram ci; NEG list: real = ma lus pa (lexical), mi 'gyur, mi 'dod, ma mthong, med par; dri ma false positive)
- construal U01–U12 complete in shastra.construal.md; glossary started (shastra.glossary.tsv); drafting begins
- beats.py citation — U02 (band 2–3 OK; WEAK-END l.3; academic free verse, used as hygiene aid only)
- beats.py citation — U04 (band 2–3 OK)
- beats.py citation — U10 (2–4, SAG l.1, l.3; free verse, kept)
- beats.py citation — U11 (band 4–5; UNKNOWN:proliferate — not added to lexicon.py in this measurement run; SAG l.1–2; free verse, kept)
- style pass (Pass 3, academic) done → shastra.style.md
- Agent tool NOT available in this context (no Agent/Task tool exposed) → fidelity check run in-context after a clean break (construal re-read from file); 0 checker spawns
- fidelity check in-context done: VERDICT 0 major, 4 minor; one revision round applied → shastra.revised.md
- dm.py translate --file C_shastra_units.md --style "literal, keep every clause and connective" — whole page U01–U12, once, after the check (1m46s) → shastra.mitra.txt
- MITRA comparison done: differs at U05, U06, U07, U08, U10, U11, U12 (content/referent/relation); all kept on grammatical grounds, Q lines added; no body changes
- final.md assembled (12 units + run summary)

## Notes / problems
- No Agent tool in this context → 0 checker spawns; Check: in-context throughout.
- reference/modes.md changed on disk at 20:26 (after the run started); re-read and followed (new "academic mode is documentary in its apparatus, not in its syntax" paragraph).
- Skill tool's cached SKILL.md differed from the on-disk copy (on-disk adds the "a change made on MITRA's word alone is a defect" paragraph); on-disk followed.
- beats.py reported UNKNOWN:proliferate (U11); the skill says to add the word to tools/lexicon.py — not done, to avoid modifying the skill's tools during a measurement run.
- My own slip: the U10–U11 identify query was typed with "rtogs par" where the text has "rtog par"; the result (not located; verbatim only in Toh 1183) is unaffected.
- Mode conflict handled: tibetan-verse prescribes metred verse; academic mode (modes.md) sets verse free line-for-line — followed the mode; beats.py used only as an aid.
FINISH: 2026-10-03 20:48:39
