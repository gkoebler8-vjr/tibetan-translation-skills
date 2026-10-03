# Protocol: does MITRA catch what Claude misses?

Purpose: decide whether the MITRA second opinion earns its place in the pipeline, with evidence
rather than opinion. Run it on a page the translator has already finished by hand (the reference).

## Setup

1. Pick one page: 8–12 units (prose sentences and at least two verse blocks) with a finished
   human rendering (for the Lam Zab, a merged chunk in `08_Master_Edition/src/`).
2. For each unit, produce:
   - **C** = the tibetan-translate rendering (full pipeline, including the fidelity check, without
     the MITRA step);
   - **M** = `dm.py translate` with `--style "literal, keep every clause and connective"`;
   - **H** = the human rendering.
3. A fresh-context judge (Agent, different model from the drafter) receives the Tibetan, the
   construal, H, C and M, and lists for each unit: meaning errors in C (against H and the
   Tibetan), meaning errors in M, and whether M's output would have revealed each error in C
   (i.e. M is right where C is wrong).

## Scoring

| | count |
|---|---|
| Units | n |
| Major errors in C | |
| Major errors in M | |
| Errors in C that M gets right (MITRA would have caught) | |
| Errors in M that C gets right | |
| Cases where C and M agree and are both wrong | |

MITRA earns a permanent place if "errors in C that M gets right" is not zero over two pages. If
it is zero, keep it as an optional flag (`--mitra`) for hard passages only.

## Record

Append the table and the error list to `reference/compare-log.md` with the date, the model used
for C, and the page. The next run compares against the previous one.
