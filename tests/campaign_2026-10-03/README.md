# Test campaign, 3 October 2026

Data behind `docs/Test_Report_2026-10-03.md`. Layout:

- `material/` — the test pages: `*_units.md` (Tibetan, one unit per line), 84000 reference English
  (`84000/*_reference_H.md`, CC BY-NC-ND 4.0, attributed in `84000/*.md`), MITRA renderings
  (`mitra/*_M.md`). The Vikramashila reference translations are not redistributed.
- `runs/run1_opus_max/`, `runs/run2_opus_max/`, `runs/run3_final/<model>_<effort>/` — one folder per
  judged page: `prompt.md` (the brief and rules), `final.md` (the pipeline's output), the construal and
  glossary files, `runlog.md`, `judge.md` (the fresh-context judge's report), `check_external.md`
  where an external checker ran.
- `results.tsv` — one row per judged page; `tokens_per_run.txt` / `tokens_final.json` — new tokens per
  run from the agent transcripts (`wf_tokens.py`); `fixlist_iter1.md` — the running error → source →
  fix list; the three prompt templates (runner, checker, judge).
