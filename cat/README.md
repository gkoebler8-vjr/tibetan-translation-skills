# Tiger CAT

A local app for translating Classical Tibetan with the `tibetan-translate` Claude Code skill: paste a text,
set the brief, run the skill page by page through your own Claude Code, review each segment beside its
Tibetan with the notes, the commentaries and the second opinion, and export a Word file with real footnotes.

**Nothing in the app calls a model or Dharmamitra.** Translation runs are headless sessions of your own
Claude Code, in the project's run folder, with the skill, under your own login. That is the design
Anthropic's terms allow (a third-party app may not route requests through a user's subscription; anything
you run in your own Claude Code is fine), and it keeps the skill as the single source of truth.

## Start

Tiger CAT lives in `cat/` of the Tibetan Translation Skills repository and needs the skills installed
(`./install.sh --skills-only` from the repository root, or the full `./install.sh`); `./install.sh --cat`
also creates `~/.venvs/vcat` (python-docx, pyewts) and builds the .app.

Double-click **Tiger CAT.app** in this folder (built by `tools/make_app.sh`; it starts the server and
opens the app in your browser), or from a terminal, from the repository root:

```bash
python3 cat/tools/serve.py --port 8765
```

The paths in this file are relative to `cat/`; from inside it the command is `python3 tools/serve.py --port 8765`.
Then open http://127.0.0.1:8765 . The first start of the .app creates `~/.venvs/vcat` if `install.sh --cat`
has not. At start the server says if the installed skill is older than the repository's `skills/`.

**One-time sign-in.** Runs use the Claude Code binary that ships with the desktop app (or the `claude`
command if installed) with your own account. The first time, choose *Sign in to Claude Code* in the
Translate menu: a Terminal window and your browser open, you sign in, and the app notices. Until then,
*Copy the prompt for Claude Code* lets you run a page by hand in a Claude Code session opened in the run
folder; the app reloads when the skill writes.

## Use

1. **＋ New project**: paste the Tibetan (script or Wylie) or choose a .txt file; set audience, purpose,
   house style, footnote policy, source context and the policy on existing translations; choose the model
   (Opus or Fable) and the effort (max is the calibrated setting, xhigh measured as faithful and cheaper);
   set the segment length (prose periods are split only at a sentence end; 45 syllables by default);
   optionally paste a glossary of house terms. The text is split into segments: headings, stanzas, and
   prose periods.
2. **⚙ Settings**: correct the segments (one per line), change the brief, model, effort, page size or
   segment length (then *Re-segment*).
3. **Translate ▾**: *next page* or *all remaining pages*. Each page is one headless Claude Code session
   with the skill; the status chip shows progress; a usage limit is waited out and the page resumed from
   the saved files. *Stop* ends after the current step. The run log has every event.
4. **Review**: edit the English in place, add footnotes (at the end of the segment, or at a selected
   phrase), tick *reviewed*. Hover any tag for its meaning. A segment you have changed shows *edited* and a *revert* button (final.md is never touched by
   your edits). *Needs review* hides what you have ticked; the search box (`/`) finds a word in the Tibetan,
   Wylie, English, footnotes or notes; the grade chips in the top bar count the segments per confidence.
   Right pane: Notes; Grounding (the quotation with its citation forms, what the commentaries say, and
   every primary-search call with its hits labelled GLOSS, QUOTE or NEAR and the commentary passage
   readable in context); MITRA; Reading; Terms (a bound rendering missing from the text is marked). Left
   pane: outline (sa bcad), glossary with import and a project-wide consistency check, sources register,
   works and people (including every work met through the search), run log. Panes resize and collapse (`[`, `]`).
5. **Export ▾**: English only or aligned Tibetan–English `.docx` with real footnotes, optionally with the
   editor's notes as an appendix, or `final.md` in the skill's own format.

## Where things live

```
projects/<slug>/project.json   title, brief, model, effort, page size
projects/<slug>/run/           the skill's working folder: <slug>.units.md, CLAUDE.md (the brief), final.md,
                               <slug>.glossary.tsv, <slug>.sources.tsv, dm_*.txt, runlog.md, <slug>.construal.md
projects/<slug>/data.json      built from run/ by tools/build_data.py; rebuilt whenever run/ changes
projects/<slug>/state.json     your edits          projects/<slug>/export/   exports      projects/<slug>/jobs/   run logs
```

You can open a run folder in Claude Code at any time and translate there by hand with the skill; the app
follows. `projects/rays` is a finished sample page (the pipeline-v2 smoke run); the "Try it" project is an
untranslated page to test a run on.

## Cost and plans

A page of 10–12 segments costs about 260k tokens at xhigh effort and 300–400k at max, mostly the model's
own reasoning. No token figure per plan is published; on Pro expect about a page per five-hour window.
The run waits for the reset and continues. Fable on Pro runs on usage credits.

## Known limits

- The segmenter follows the source's lines: a line is a segment, a short line ending in a shad is a heading,
  long lines split at sentence ends (about 45 syllables). Check the split; `Re-segment` in Settings redoes it.
- The outline is derived from the units' register labels (or from the headings the segmenter marks); a
  sa bcad pass belongs in the skill. Sub-units (`U10a`, `U10b` …) and end-of-unit footnotes (`FN(*)`)
  are read as the skill writes them.
- The term checks (Terms tab, Glossary → Consistency) match whole Wylie syllables and skip one-syllable
  terms that are also particles (*las*, *la*, *nas* …) and pattern entries (`… la X`); they are a prompt
  to look, not a verdict.
- Works and people show catalogue data only; Treasury of Lives and BDRC lookups are planned.
- Runs made before the skill's confidence field get a grade derived from their notes (dashed ring).
- The .app is a launcher around a local web app; the UI runs in your default browser.

## Files

- `app/` — the UI (plain HTML, CSS, JavaScript; no build step)
- `tools/serve.py` — the server: projects, runs, exports, glossary import, refresh
- `tools/build_data.py` — run folder → data.json · `tools/tibseg.py` — segmenter · `tools/make_app.sh` — builds the .app
- `docs/skill-update-prompt.md` — changes the skill still needs · `docs/merge-prompt.md` — how the app was merged into the repository
- the skill itself: `../skills/tibetan-translate/` (source), `~/.claude/skills/tibetan-translate/` (the copy the runs load)

Dharmamitra resources used by the runs: DharmaMitra search, DharmaNexus segments and parallels, Explore,
and the MITRA translation model, from https://dharmamitra.org; the MITRA Tibetan Lexicon (CC BY-SA 4.0).
Each is named at the stage where it was used, as Dharmamitra asked.
