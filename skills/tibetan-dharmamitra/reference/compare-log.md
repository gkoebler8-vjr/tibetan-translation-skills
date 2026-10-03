# Claude vs MITRA — comparison log

Protocol: `compare.md`. C = tibetan-translate (full pipeline, in-context check), M = `dm.py translate
--style "literal, keep every clause and connective"`, H = the published human translation. Judge: a
fresh-context Opus agent working from the Tibetan.

## 2026-10-03 — run 1, Opus at max effort, five pages, 58 units

| Page | Units | C major | C minor | M major | M minor | C errors M gets right | both wrong, same place | H errors |
|---|---|---|---|---|---|---|---|---|
| Rays of Sunlight, opening homage (Vikra; prose + Uttaratantra citation) | 12 | 0 | 1 | 3 | 3 | 0 | 1 | 4 |
| Jigten Sumgön, Stages of the Path (Vikra; argumentative prose) | 12 | 0 | 2 | 0 | 3 | 2 | 0 | 3 |
| King of Samādhis, ch. 4 (Toh 127; prose list + 6 stanzas) | 12 | 1 | 3 | 3 | 3 | 2 | 2 | 3 |
| Emergence from Sampuṭa, ch. 1 (Toh 381; 12 stanzas) | 12 | 0 | 3 | 2 | 7 | 1 | 1 | 7 |
| Bṛhaṭṭīkā, introduction (Toh 3808; scholastic prose) | 10 | 0 | 1 | 2 | 13 | 0 | 1 | 4 |
| **Total** | **58** | **1** | **10** | **10** | **29** | **5** | **5** | **21** |

Errors in C that M got right (the cases that justify the step): Stages U08 (subject of `smin pa`),
Stages U12 (an invented "then comes" sequence inside one locative frame), Sūtra U01 (`rigs par`
adverbial, read as an object), Sūtra U11 (a `nas` sequence turned into a relative clause), Sampuṭa
U09 (`bskor ba` voice). Four of the five are relation or role slips, which is what MITRA reads well
enough to flag; none is a term choice.

Where M fails: roles in long periods (dangling participles make the speaker the agent of the
deeds, Rays U05), omissions in verse lists (Rays U08), wrong subject in the last pada of a run
(Rays U09), a flattened scholastic exchange (13 minors in the Bṛhaṭṭīkā page), and the citing
text's own structure.

**Decision:** MITRA earns a standing place as a *flag-raiser* after the fidelity check (SKILL.md
§6), one `dm.py translate --file <page>` call per page (~0.2k tokens per unit). Disagreements on a
content word, referent, agent or relation are resolved from the grammar and recorded as `Q:`;
they are never a vote. The H column is a by-product worth noting: the fresh-context judge found 21
defensible errors in the five published translations, which says more about the usefulness of a
construal-based check than about any translator.

## 2026-10-03 — run 2 (Opus max, five more pages) and the final matrix

| Page | Units | C major | C minor | M major | M minor | C errors M gets right | H errors |
|---|---|---|---|---|---|---|---|
| Single Intention commentary (Vikra) | 12 | 0 | 2 | 1 | 7 | 2 | 7 |
| Scintillation biography (Vikra, relay H) | 11 | 0 | 3 | 1 | 8 | 2 | 6 |
| Lotus ch. 14 (Toh 113) | 11 | 0 | 2 | 3 | 4 | 2 | 2 |
| Hevajra II.4 (Toh 417) | 12 | 2 | 5 | 7 | 7 | 3 | 0 |
| String of Pearls (Toh 1189) | 12 | 0 | 4 | 3 | 9 | 2 | 3 |

Opus max over all ten pages: C 3 major / 26 minor; M 25 / 64; M reveals 16 of C's 29; H 39.
All 30 judged pages (both models, all efforts): C 30 / 117; M 88 / 180; M reveals 67 of 147.

The Hevajra page is the warning: both of its majors were readings the run *changed* after the MITRA
step. The step stays, with the rule added to SKILL.md §6 that a change needs a grammatical reason
written into the construal, and otherwise becomes a `Q:`.
