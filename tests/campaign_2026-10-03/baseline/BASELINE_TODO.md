# Baseline test to run: bare Opus, no skill (handover for a new chat)

Purpose: measure what the tibetan-translate skill adds over simply asking the model to translate.
Same pages, same judge, same scoring as the campaign, so the numbers slot into the report.

## Pages (already prepared; Tibetan units, reference English, MITRA output)

Use the three final-matrix pages, so the result compares directly with the skill at every setting:

| Page | Tibetan units | Reference (H) | MITRA (M) | Brief used by the skill runs |
|---|---|---|---|---|
| V1 Rays of Sunlight | `../material/vikra/rays_units.md` | NOT in the repo (Vikra reference; on Gabriel's machine it was in the session scratchpad `material/vikra/rays_reference_H.md`; rebuild from the Vikra alignment sheet `Rays-of-Sunlight_TTN-Commentary.xlsx` rows 42–62 if needed) | `../material/mitra/rays_M.md` | `../runs/run3_final/opus_high/V1_rays/prompt.md` (the BRIEF block) |
| CT Caṇḍamahāroṣaṇa ch. 15 | `../material/84000/C_tantra_units.md` | `../material/84000/C_tantra_reference_H.md` | `../material/mitra/C_tantra_M.md` | `../runs/run3_final/opus_high/CT_tantra/prompt.md` |
| CSh Jewel Garland of Yoga | `../material/84000/C_shastra_units.md` | `../material/84000/C_shastra_reference_H.md` | `../material/mitra/C_shastra_M.md` | `../runs/run3_final/opus_high/CSh_shastra/prompt.md` |

Optionally add the sutra page (`C_sutra_*`) to match the skill's Opus-high and Sonnet-high runs.

## Runs (6, or 8 with the sutra page)

For each page, two bare runs: **Opus at max** and **Opus at xhigh**. The prompt is deliberately
minimal. Give the model ONLY the brief block (audience, purpose, house style, source context — the
same text the skill runs received, so the comparison is fair) and the Tibetan, and ask:

> Translate the following Classical Tibetan into English for the audience and house style described.
> Give one finished rendering per unit, keeping the `Uxx` ids, verse as lines. Add a short note where a
> reading is uncertain. Do not use any tools or files; translate from your own knowledge.

No skill invocation, no tibdict, no dm.py, no checker. Write each result as `final.md` in
`baseline/<setting>/<page>/` in the campaign's block format (`### Uxx` / `TEXT:` / `NOTES:`), so the
judge template works unchanged.

How to control model and effort per run: the Workflow tool (approved by Gabriel for this purpose),
one `agent()` per run with `model: 'opus'` and `effort: 'max' | 'xhigh'`, `agentType:
'general-purpose'`; the Agent tool cannot set effort. Expect ~5–20k tokens per bare run.

## Judging (same as the campaign)

Fill `judge_prompt_template_v1.md` (in this folder; the version without the checker-recall section)
with PAGE / FINAL_C / CONSTRUAL / REF_H / MITRA_M. There is no construal for a bare run: replace the
construal line with "Construal: none (bare run); judge from the Tibetan." Spawn one Opus judge per
run (Agent tool, model opus, fresh context), ~75k tokens each. Collect the Totals lines into
`baseline/results.tsv` with the campaign's columns (`../results.tsv` header).

## What to report

Add a row block to `docs/Test_Report_2026-10-03.md` under "Final matrix": bare Opus max and bare Opus
xhigh beside the skill's figures for the same three pages (skill Opus xhigh: 1 major / 6 minor /
English 4.0 on these pages; skill Opus max on Rays: 0 / 1 / 4.3). Report major and minor errors,
English score, silent doubts (bare runs rarely list alternatives: count how many of the judge's
findings had no note), and tokens. Then one paragraph: what the skill buys for its ~20× cost.

## Also worth one line in the report

MITRA alone was already measured on every page (the M columns in `../results.tsv`): 25 major / 64
minor on the ten Opus-max pages (116 units), 88 / 180 over all 30 pages (354 units).
