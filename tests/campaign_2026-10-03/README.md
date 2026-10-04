# Test campaign, 3 October 2026

Data behind `docs/Test_Report_2026-10-03.md`. Layout:

- `material/` — the test pages: `*_units.md` (Tibetan, one unit per line), 84000 reference English
  (`84000/*_reference_H.md`, CC BY-NC-ND 4.0, attributed in `84000/*.md`), MITRA renderings
  (`mitra/*_M.md`). The Vikramashila reference translations are not redistributed.
- `runs/run5_v2_smoke/` — the one smoke run of pipeline v2 (Rays of Sunlight, Opus max, 4 October
  2026): final.md with FOOTNOTES and NOTES blocks, the construal sketch, the saved dm.py outputs, the
  runlog with the list of skill-text problems the run reported (fixed the same day). Not judged.
- `runs/run4_opus_max/` — the skill at Opus max on the three baseline pages (4 October 2026), two
  judges each (`judge.md`, `judge2.md`), `tokens_run4.txt`; these runs were interrupted once and
  resumed from their saved construal files (see the runlogs).
- `runs/run1_opus_max/`, `runs/run2_opus_max/`, `runs/run3_final/<model>_<effort>/` — one folder per
  judged page: `prompt.md` (the brief and rules), `final.md` (the pipeline's output), the construal and
  glossary files, `runlog.md`, `judge.md` (the fresh-context judge's report), `check_external.md`
  where an external checker ran.
- `baseline/` — the bare-model baseline (4 October 2026): Opus at max and xhigh on the three
  final-matrix pages with the same brief and no skill or tools; per run `prompt.md`, `final.md`,
  `judge_prompt.md`, `judge.md`, and `judge2.md` from an independent second judge (also beside the
  skill's `runs/run3_final/opus_xhigh/*/judge.md`); `results.tsv` (with silent-doubt and token columns;
  the `*-judge2` rows are the second round),
  `tokens_baseline.txt`; `BASELINE_TODO.md` is the original instruction.
- `results.tsv` — one row per judged page; `tokens_per_run.txt` / `tokens_final.json` — new tokens per
  run from the agent transcripts (`wf_tokens.py`); `fixlist_iter1.md` — the running error → source →
  fix list; the three prompt templates (runner, checker, judge).
