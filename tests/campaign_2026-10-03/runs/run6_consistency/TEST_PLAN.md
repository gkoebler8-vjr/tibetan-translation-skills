# Run 6: consistency across pages, and v2 measured on two blind pages — READY, NOT RUN

Everything below is prepared; nothing has been launched. `<repo>` = the absolute path of this repository (the prompt files on disk carry the real paths; they are gitignored until scrubbed). Launch after the usage window resets.
Expected cost: 5 skill runs × ~330k + 7 judges × ~80k ≈ 2.2M tokens; the three GC runs are
sequential (about 35 min each), the two v2 runs can go in parallel with them.

## A. Consistency: three consecutive pages of the Great Compassion sutra (Toh 147, 2.464–2.496)

Pages: `material/consistency/GC{1,2,3}_units.md` (11 prose units each), reference
`GC{n}_reference_H.md`, MITRA `material/mitra/GC{n}_M.md`. One SHARED glossary
`runs/run6_consistency/shared/gc.glossary.tsv` (empty now); each run reads and appends it.
Prompts: `runs/run6_consistency/GC{n}/prompt.md`. Runs must be SEQUENTIAL (GC1, then GC2, then GC3).

Workflow script (model opus, effort max, agentType general-purpose):

```js
export const meta = { name: 'run6-consistency', description: 'v2 on three consecutive sutra pages with a shared glossary, sequential', phases: [{ title: 'Translate' }] }
const B = '<repo>/tests/campaign_2026-10-03/runs/run6_consistency'
const out = []
for (const p of ['GC1', 'GC2', 'GC3']) {
  const r = await agent(`Read the file ${B}/${p}/prompt.md and carry out the task in it exactly: a full run of the tibetan-translate skill (pipeline v2) on one page of a text whose earlier pages have been translated already; the shared glossary it names binds. Reply only with what rule 6 of the prompt asks for.`,
    { label: `translate:v2/${p}`, phase: 'Translate', model: 'opus', effort: 'max', agentType: 'general-purpose' })
  out.push({ page: p, reply: r })
}
return out
```

Then one judge per page (Agent tool, model opus, general-purpose, background):
"Read `<B>/GC{n}/judge_prompt.md` and carry out the judging task it describes exactly, reading only
the files it names. Write the full report where it says and reply with only the Totals line."

Then the consistency measurement:

```bash
cd "<repo>/tests/campaign_2026-10-03"
python3 check_consistency.py runs/run6_consistency/shared/gc.glossary.tsv \
  material/consistency/GC1_units.md:runs/run6_consistency/GC1/final.md \
  material/consistency/GC2_units.md:runs/run6_consistency/GC2/final.md \
  material/consistency/GC3_units.md:runs/run6_consistency/GC3/final.md
```

Report: bound-term occurrences rendered as bound per page (the number that matters), keys with two
Englishes in the glossary, title drift; plus the judges' major/minor/English per page (one judge:
read ±2 majors as noise).

## B. v2 measured on the two blind baseline pages (Caṇḍamahāroṣaṇa ch. 15, Jewel Garland of Yoga)

Prompts: `runs/run6_consistency/v2_CT_tantra/prompt.md`, `runs/run6_consistency/v2_CSh_shastra/prompt.md`
(own glossary each). Can run in parallel with A:

```js
export const meta = { name: 'run6-v2-blind', description: 'v2 at Opus max on the two blind baseline pages', phases: [{ title: 'Translate' }] }
const B = '<repo>/tests/campaign_2026-10-03/runs/run6_consistency'
const res = await parallel(['v2_CT_tantra', 'v2_CSh_shastra'].map(p => () =>
  agent(`Read the file ${B}/${p}/prompt.md and carry out the task in it exactly: a full run of the tibetan-translate skill (pipeline v2) on one test page. Reply only with what rule 6 of the prompt asks for.`,
    { label: `translate:${p}`, phase: 'Translate', model: 'opus', effort: 'max', agentType: 'general-purpose' }).then(r => ({ page: p, reply: r }))))
return res.filter(Boolean)
```

Then two judges per page: `judge_prompt.md` → `judge.md`, `judge2_prompt.md` → `judge2.md`.
Compare with the pooled two-judge figures in the report's baseline block (skill v1 max 5/11/3.98,
bare max 2/6/3.93 on three pages; here two pages: v1 max on CT+CSh = 5 maj, bare max = 2 maj).

## C. Afterwards

- Tokens: `CLAUDE_SESSION_DIR=<session dir> python3 wf_tokens.py` (new session's dir).
- Scrub personal paths from the run folders before committing (sed as in the earlier runs).
- Add the rows to `results.tsv` (run6-…), a "v2" row block to the report's baseline section, the
  consistency figure to the README's "What it adds" section (it is the untested claim named there).
- If the GC runs re-use the Rays examples anywhere: they do not; GC pages are blind.
