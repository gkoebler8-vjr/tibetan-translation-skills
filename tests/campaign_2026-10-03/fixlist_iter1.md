# Iteration 1 — errors found, their sources, and the fixes (running list)

## Measurements (Opus max, workflow subagents, in-context check because the Agent tool is absent inside workflow agents)
- V1 Rays (12 units, prose + 4 verse stanzas): ~320–350k tokens; 12 annotate, 1 identify, 2 segment, 4 beats. Judge: C 0 major / 1 minor; English 4.3; M 3 major / 3 minor; M would reveal 0 of C's errors; H errors 4.
- V2 Stages (12 units, prose + 1 couplet): ~340k tokens; 12 annotate + 1 lookup, 2 identify, 2 segment, 1 beats. Judge: C 0 major / 2 minor; English 4.3; M 0 major / 3 minor; M would reveal 2 of C's errors; H errors 3.
- Both agents' own breakdown: construal reasoning ≈ 45–50 % of tokens; tibdict output 20–45k per page; skill/reference files 25–30k; check 12k.

## Error → source → fix
| # | Error (where) | Source | Fix | Status |
|---|---|---|---|---|
| 1 | botok absorbs negation: `'jug sgo ma lags sam` → "sgo ma" (V2 U03); `ma dag zhing` → "dag zhing" = pure land (V1 U09) | tool (tibdict segmentation) | tibdict: re-split final ma/mi before verb/aux; hint after a NEG particle; NEG count line per unit | agent working (repo copy) |
| 2 | `char` → cha + r; `mdo 'gag`, `phyag na rdo rje`, `a ma na se`, `khong du chud pa` split | tool | tibdict: fused-affix alternative; COMPOUND? line from greedy longest-match over token boundaries | agent working |
| 3 | wrong MITRA first sense (don, thogs med, lam, rgyud, 'byung ba, len pa, rnyed pa, 'dzin pa, 'debs, 'don, ro) | tool/data (lexicon first sense) + already documented in analysis.md §2a | keep the rule "read all senses; grammar decides"; add the new examples to §2a | to do (skill text) |
| 4 | `dm.py identify` said VERBATIM yes for the citing text's own copy (EGS) while the Kangyur run was 8 syllables (V2 U10) | tool (verdict computed over all hits) | dm.py: canonical vs non-canonical verdict; SKILL §3.3 wording | agent working |
| 5 | `segment --context` window 3 too narrow to reach a quoted stanza | tool default | default 6, help text | agent working |
| 6 | beats.py UNKNOWN: entire, tushita, consorts, renunciation, enlightenment, vanquishing | lexicon gap | added to lexicon.py (repo + live) | done |
| 7 | annotate output 12k chars on a long period; `--budget` had no effect; `--brief` larger than default | tool bug | fix --budget; make skill say `--budget 6000` for units over ~40 syllables | agent working |
| 8 | two-line chiastic saying (11/11) treated as verse by the 7/9/11 rule (V2 U11) | skill rule gap | SKILL §3.1 + analysis.md §2.1: a quoted dictum of two matched lines may be set as prose; verse needs ≥3 padas or a known verse source | to do |
| 9 | silent construal fork: `bstan bcos … snying po` apposition vs genitive (V1 U10) | model (doubt discipline) | analysis.md §2.10: forks on the head noun of a period always get a Q | to do |
| 10 | calques: "manifestly taking birth" (mngon par), "the later relies on the earlier", "this text / this treatise / this essence" chain, adverb wedged between verb and object (V1 U05, U07, U12) | model/english.md coverage | english.md §9: add rows for mngon par, nominal calques, demonstrative chains, interposed adverbials | to do |
| 11 | minor role/sequence slips: smin pa subject (V2 U08); "Then comes liberation" invented sequence (V2 U12) | model (construal) — both were Q-flagged forks | none beyond #9; checker did not catch them because the construal itself chose the reading | note as limitation |
| 12 | verse units scored 3–4, "roughly" metred: gerund lists flat, "heart of enlightenment" calque | model + verse mode (citation band 3–4 beats on a long list) | verse skill: for an enumerative stanza-run allow a longer measure (4–5) so each deed gets a verb; failures.md note | to do (light) |
| 13 | Agent tool absent inside workflow subagents → check ran in-context in every run | harness | document in SKILL §6: in-context fallback is the norm for autonomous/ workflow runs; spawn the checker from the orchestrator when running pages in bulk | to do |
| 14 | test material: page header quoted a phrase of H (V1) | test harness | headers cleaned | done |
| 15 | brief error (speaker of U11 given as Phagmodrupa) | test harness / editor | pipeline flagged Q, correct behaviour | none |

## Run-1 judge totals (all five pages, Opus max, in-context check)
| Page | Units | C major | C minor | English (1–5) | M major | M minor | C errors M reveals | H errors |
|---|---|---|---|---|---|---|---|---|
| V1 Rays (Vikra, prose+verse) | 12 | 0 | 1 | 4.3 | 3 | 3 | 0 | 4 |
| V2 Stages (Vikra, prose) | 12 | 0 | 2 | 4.3 | 0 | 3 | 2 | 3 |
| S Sutra (Toh 127, prose+verse, new-practitioner mode) | 12 | 1 | 3 | 4.3 | 3 | 3 | 2 | 3 |
| T Tantra (Toh 381, all verse, seasoned mode) | 12 | 0 | 3 | 3.8 | 2 | 7 | 1 | 7 |
| Sh Shastra (Toh 3808, prose, academic mode) | 10 | 0 | 1 | 4.2 | 2 | 13 | 0 | 4 |
| **Total** | **58** | **1** | **10** | **4.2** | **10** | **29** | **5** | **21** |
Tokens: 699k for V1+V2, 942k for S+T+Sh ⇒ ~330k per 12-unit page (no checker spawn). Judges ~70k each (Opus).

## Decisions after run 1
- MITRA cross-check: 5 of C's 11 errors were visible in M ⇒ becomes a standing, cheap step after the fidelity check (`dm.py translate --file <page>`; disagreements become Q: lines, never votes). Added to SKILL §6.
- More model-level error types to address in the skill text: a recorded fork resolved toward the weaker branch (S U11 nas-sequence → relative clause; V1 U07); adverbial `-r/-par` phrase read as object (S U01 rigs par); over-specified term (kha zas rgyu 'thun → "what it turns into"; bag chags sad pa → "awakened tendencies"; shes par mi rung → "cannot be understood"); one agent restated read as two persons (T U12). ⇒ analysis.md: a fork where MITRA or the commentary disagrees is resolved by the grammar and left as Q; english/analysis: `X par` before a verb is adverbial by default; a restated agent is the same person.
- Verse quality lowest (tantra 3.8): under a 3–4 beat band the lines go stiff/clunky; the wider measure rule added; still a model limitation to report.
- In-context check caught 2–9 minors per page but none of the judge's errors except by accident; test the external checker in run 2 (spawned from the orchestrator) and record its recall against the judge.

## Iteration 2 (Gongchig + Scintillation, Opus max, revised skill) — first observations
- Tokens: 643k for 2 pages (~320k/page): no saving from the skill-text changes (expected: they add steps — MITRA, hints).
- Skill tool serves a cached SKILL.md from session start; the runners followed the on-disk text. Runner prompts now say to read SKILL.md from disk. (For users: `/reload-skills` after editing a skill.)
- New tool slips: botok split `ma dros pa` (Anavatapta) into NEG `ma` + `dros pa` (the inverse of the absorbed-negation case: a name); `NEG:` count is naive (counts the `ma` of `bla ma`); `dm.py segment --window N` without `--context` prints only the segment (should imply --context); beats.py UNKNOWN: descent, agree, conflict; `de nyid` "suchness" sense, `'khor los` split as "year", `de kho na nyid` split, `skyes pa` "man" again.
- In-context check: 6 minors (Gongchig), 4 minors (Scint). External Sonnet checker spawned from the orchestrator for comparison; judge v2 reports checker recall.

## Run-2 Vikra judge totals (revised skill; external Sonnet checker spawned by the orchestrator)
| Page | Units | C major | C minor | English | M major | M minor | C errors M reveals | H errors | ext. checker recall |
|---|---|---|---|---|---|---|---|---|---|
| V3 Gongchig (Kunpal commentary; prose + 1 verse) | 12 | 0 | 2 | 4.2 | 1 | 7 | 2 | 7 | 0 of 2 (1 false finding) |
| V4 Scintillation (biography; dialogue) | 11 | 0 | 3 | 4.4 | 1 | 8 | 2 | 6 | 0 of 3 (2 false findings) |
Remaining C errors are term-level minors (a dropped yongs su; "means" for sgo nas clashing with thabs; a doubled predicate; mngon par dropped; a static "embodies" for sbyor ba'i bdag nyid): below the fidelity checker's remit (polarity/role/relation/omission of content). MITRA flagged 4 of the 5. Fixes after run 2: NEG line now shows context and marks protected nouns/names (bla ma, ma dros pa); `dm.py segment --window N` implies --context; lexicon words added.

## Final-matrix observations (first Opus-high judgments)
- Opus high, CT tantra: 1 major / 3 minor, English 3.8 — one major was a correct reading **switched after MITRA** (`skye bar byed` begets → "is born"): the "flag, never a vote" rule was not enough. Fix: a MITRA-induced change must be justified in the construal's case-frame fields and re-pass the relation/role tests; otherwise Q. (SKILL §6, analysis.md §2.10.)
- Opus high, CS sutra: 1 major / 6 minor, English 3.7 — forks resolved toward the weaker branch, dictionary senses (shin tu sbyangs pa = pliancy), bound-term drift (yang dag). More errors than max on the same kind of page.
- Opus high costs ~140–185k new tokens per page vs ~250–350k at max (12 min vs 35 min per page).
