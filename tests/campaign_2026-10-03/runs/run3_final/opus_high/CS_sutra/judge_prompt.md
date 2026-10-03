You are judging an English translation of a Classical Tibetan page, unit by unit, in a fresh context. You read Classical Tibetan. Be exact and sparing: findings only, no praise, no rewriting.

FILES
- Tibetan units: <scratchpad>/material/84000/C_sutra_units.md
- C = the pipeline's rendering (Claude, the system under test): <scratchpad>/runs/run3_final/opus_high/CS_sutra/final.md   (read the TEXT blocks and NOTES; ignore the Run summary)
- Construal used by C (its reading of the grammar): <scratchpad>/runs/run3_final/opus_high/CS_sutra/sutra.construal.md
- H = the published human translation of the same units (the reference; it is not infallible): <scratchpad>/material/84000/C_sutra_reference_H.md
- M = MITRA machine translation of the same units (a second opinion): <scratchpad>/material/mitra/C_sutra_M.md

FOR EACH UNIT Uxx, work from the Tibetan first, then compare.
1. Errors in C. A MAJOR error changes meaning: wrong polarity, wrong agent/object/role, a relation particle rendered as another relation or dropped (las/pas/na/phyir/kyang/nas/te/pa'i/la), content omitted, content invented, wrong speaker or addressee, wrong referent, a wrong technical term that changes the doctrine. A MINOR error is nuance: a weaker term, a dropped honorific nuance, a shade of tense/mood, a bound-term inconsistency. Quote the English span and say what the Tibetan has. If H differs from C but C is defensible from the Tibetan, that is NOT an error in C; say "C ≠ H, C defensible" in one clause if worth noting. If H itself is wrong where C is right, note "H error" in one clause.
2. Errors in M, the same way (MAJOR/MINOR, briefly).
3. For each MAJOR or MINOR error in C: would M have revealed it (M is right where C is wrong)? yes/no.
4. English quality of C, 1–5, where 5 = publishable as is for a seasoned-practitioner reader edition (natural, clear, idiomatic, strong verbs, no calques, no translationese, right register); 3 = readable but needs an editor's pass; 1 = unusable. One clause on the main weakness if < 5. For verse units also say whether the lines read as metred English verse (yes / roughly / no).
5. Did C's NOTES record a doubt (Q:) where the construal genuinely forks? If a fork went unrecorded and C silently chose, say "silent doubt".

OUTPUT, exactly this shape, one block per unit:

### Uxx
C errors: <none | list "MAJOR|MINOR <category> | \"<span>\" | <what the Tibetan has> | M reveals: yes/no">
M errors: <none | list>
H notes: <none | "C ≠ H, C defensible: ..." | "H error: ...">
English: <1–5> <clause> | verse: yes/roughly/no (verse units only)
Doubts: <ok | silent doubt: ...>

Then a final section:

## Totals
units: n | C major: n | C minor: n | M major: n | M minor: n | C errors M would reveal: n | both wrong same place: n | H errors: n | mean English: x.x
## Top 5 problems in C, ranked by damage, each with a one-line diagnosis of the likely cause (grammar misread / dictionary sense / term choice / register / verse constraint / construal fork / skill rule misapplied / omission under compression)
## Worst 3 units (ids) and best 3 units (ids)

Write the full report to <scratchpad>/runs/run3_final/opus_high/CS_sutra/judge.md and reply with only the Totals section.