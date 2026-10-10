# runlog — lesson-prep

2026-10-09 · MODEL: Claude Opus 5.5 (claude-opus-5-5), max reasoning effort as set for this session: the calibrated setting. Autonomous run inside Vikramashila CAT; brief taken from CLAUDE.md, Pass 0 not asked.
- Brief from CLAUDE.md (Pass 0 answered): audience new practitioner · purpose publication · house style per modes.md (new practitioner column) · notes: reader footnotes, sources in lesson-prep.sources.tsv · source context: infer and state · prior translations: consult and cite (dm.py cite) · glossary lesson-prep.glossary.tsv binds.
- Page: U01–U03 of lesson-prep.units.md, treated as one page.
- Read: SKILL.md (on disk, authoritative; identical to the loaded skill), reference/english.md, modes.md (new-practitioner column), notes.md, prose.md.
- Read: tools/export_docx.py header (TEXT: lines = line breaks inside a paragraph, blank line = new paragraph; `## ` ends a unit block); format conventions checked against projects/rays/run (final.md, sources.tsv columns).
- Skill tool: tibetan-verse (loaded; ~/.claude/skills/tibetan-verse/SKILL.md checked on disk) for the one-pada verse citation in U02; guidelines.md not read (a single line, no question arose).
- Pass 1: lesson-prep.construal.md (source context assumed and stated there), lesson-prep.draft1.md written.
- beats.py (citation): "variety" UNKNOWN in lexicon.py → hand-counted va-RI-e-ty (4, [2], []) in memory for this run, tool files untouched; "The world in all its variety comes from karma." PULSE:2 → rejected; "The world's variety comes from karma." 3–4 beats, passes.
- Read: reference/grounding.md (before the first grounding call). Skill tool: tibetan-citations (loaded) for the U02 quotation.
- dm.py identify U02 (as quoted, 7 syl.) → dm_identify_U02.txt: best verbatim run 6/7 (paraphrase); Toh 4089 not among the top candidates.
- dm.py gloss U02 (canonical wording, --context 8) → dm_gloss_U02.txt: root work Toh 4089; Bhāṣya Toh 4090 166a-3–7 (= Toh 4091, 4095) and Tibetan Kośa commentaries: sems can dang snod kyi 'jig rten … las las; resolves the rgyu las las Q.
- dm.py identify U02 (canonical, 14 syl.) → dm_identify_U02-2.txt: verbatim, Toh 4089 10b-43 (verification of the locator).
- dm.py cite BO_T07_D4089:10b-43 → dm_cite_U02.txt (REGISTER line; READER title Treasury of Abhidharma).
- dm.py gloss U03 (the three sufferings, --context 8) → dm_gloss_U03.txt: Toh 3996 165a-18–26 gloss (pain / pleasure / neither; khyab = pervades every feeling); Toh 4421 194a–b; KN-LYN-02 lamrim commentary.
- dm.py gloss U01 (gross/subtle impermanence, --context 8) → dm_gloss_U01.txt: QUOTE (Gyaltsab, Four Hundred comm.) and NEAR only; none found for the formula.
- dm.py gloss U02-2 (the three death contemplations, --context 8) → dm_gloss_U02-2.txt: NEAR (lamrim works: rtsa ba gsum); consistent.
- Gloss calls: 4 (budget 2–4). EN_ (published English) hits: none in any saved output; prior translations: none found (consult policy, nothing to consult; existing-translations.md not needed).
- dm.py translate --file lesson-prep.units.md (MITRA flag) → dm_translate_U01-U03.txt: agrees on content; differs on person in U01 item 1 (one's own vs bdag = I) and turns list items into imperatives.
- Pass 3 (style, new-practitioner mode) → lesson-prep.pass3.md: no change of meaning from draft1; glossary: 36 term rows + TITLE row (Treasury of Abhidharma) appended to lesson-prep.glossary.tsv; register row P01/U02 via register.py --add (--check: 0 problems; --titles: 0 problems).
- Read: reference/check.md. Pass 4 (in-context, after re-reading lesson-prep.construal.md from disk): no finding in the body; the sketch's U02 TERMS entry aligned with the glossary (housekeeping). Check: in-context, 0 fixed.
- Pass 5: editor notes per unit; one reader footnote (U03, the three kinds of suffering, written from Toh 3996 165a and KN-LYN-02); confidence U01 high, U02 high, U03 medium (agent of honorific gsungs open).
- final.md created with a title line; U01–U03 appended. Test export (export_docx.py → /tmp, deleted): 3 units, 1 footnote, no anchor warning. Note for the user: export_docx.py writes TEXT lines as plain runs, so *Treasury of Abhidharma* would show its asterisks in Word (italics not rendered); not changed.
- After the run (tibetan-verse §3.7): 'variety': (4, [2], []) added to ~/.claude/skills/tibetan-verse/tools/lexicon.py; beats.py now passes the U02 line without the hand count.
- DONE U01–U03.
