# Prompt: merge Tiger CAT into the skills repository (written 10 October 2026)

Why this way round: `~/Desktop/Tibetan Translation Skills` has the git history (16 commits), the GitHub
remote, the licence, the tests and the installer; `~/Desktop/CAT Tool` has one commit. The skill stays
usable outside the app because Claude Code loads the *installed* copy in `~/.claude/skills/` (written by
`install.sh`), and the skill's own tools are called by absolute path there. Where the source lives on disk
changes nothing for a user who only has the skill. The app already treats the installed copy as the
runtime and the repo as the source of truth; the merge keeps that.

Paste everything below the line into a Claude Code session opened in `~/Desktop/Tibetan Translation Skills`.

---

Merge the Tiger CAT app into this repository and reorder the folder. Work in the order given; verify
after each step; commit once at the end. Do not change the skills' content (`skills/*`) except where a
path or a README sentence must change. Keep the skill usable on its own: `./install.sh --skills-only`
must still produce a working `~/.claude/skills/tibetan-*` without the app.

## 0. Starting state

- Check that no Tiger CAT translation run is going: `curl -s http://127.0.0.1:8765/api/run?p=<slug>` for
  each project under `../CAT Tool/projects/` (or the server is not running). If a run is active, stop here.
- Stop the server (`pkill -f tools/serve.py`) and quit the app if open.
- `git status` must be clean here. Read `HANDOVER.md` (this repo) and `../CAT Tool/HANDOVER.md`.
- If `../CAT Tool` still exists: `mv "../CAT Tool" ./cat`, then `rm -rf cat/.git` (its one commit is
  already described in `cat/HANDOVER.md`; this repo's history is the one to keep) and `git add cat`.

## 1. Target layout

```
.
├── README.md              one README: the skills (as now) + a section "Tiger CAT, the app" that links cat/README.md
├── LICENSE, LICENSE-NOTES.md
├── install.sh             + `--cat`: creates ~/.venvs/vcat (python-docx, pyewts) and builds cat/Tiger CAT.app
├── export.sh
├── HANDOVER.md            one handover with two sections: skills state, app state (merge cat/HANDOVER.md into it, then delete cat/HANDOVER.md)
├── skills/                unchanged: tibetan-translate, tibetan-verse, tibetan-citations, tibetan-dharmamitra
├── cat/                   the app, self-contained
│   ├── README.md          cat/README.md as it is, paths adjusted
│   ├── app/               index.html, style.css, app.js
│   ├── tools/             serve.py, build_data.py, tibseg.py, make_app.sh
│   ├── projects/          rays (sample), try-it-…, lesson-prep (Gabriel's own)
│   ├── Tiger CAT.app/     built by tools/make_app.sh; its launcher finds the repo as the bundle's parent, so it keeps working inside cat/
│   └── docs/              skill-update-prompt.md, this file
├── docs/                  the skills' docs as now
├── tests/                 as now
└── .claude/launch.json    merged: the `cat-demo` URL config (port 8765) kept; `tiger-cat` config's command path becomes cat/tools/serve.py
```

Use `git mv` for every move so history follows. Nothing goes under `skills/` that the installer should
not copy into `~/.claude/skills/`.

## 2. References to fix

- `cat/tools/serve.py`: `SKILL_TOOLS` stays `~/.claude/skills/tibetan-translate/tools` (the runtime copy),
  but fall back to `<repo>/skills/tibetan-translate/tools` when the installed copy is missing, so the
  Word export works from a fresh checkout. The headless run keeps `--add-dir ~/.claude/skills` and the
  prompt line that reads `~/.claude/skills/tibetan-translate/SKILL.md`: the installed copy is what
  headless Claude Code loads. Add a one-line check at server start: if the installed skill is older than
  `skills/tibetan-translate/SKILL.md`, print "skills in ~/.claude/skills are older than the repo; run
  ./install.sh --skills-only".
- `cat/tools/make_app.sh` and the launcher inside the .app: `ROOT` is the bundle's parent (now `cat/`);
  confirm the launcher's `cd "$ROOT"` and `tools/serve.py` path still resolve, rebuild the .app, test a
  double-click start (`open "cat/Tiger CAT.app"`), then quit it.
- `.gitignore`: append the app's rules with the `cat/` prefix (`cat/projects/*/export/`,
  `cat/projects/*/jobs/`, `cat/*.docx`), keep this repo's rules; `cat/.gitignore` is deleted.
- `install.sh --cat`: venv `~/.venvs/vcat` with python-docx and pyewts, then `bash cat/tools/make_app.sh`.
  Its header comment lists the new flag. `./install.sh` without flags does not touch the app.
- `README.md` (top): a short section "Tiger CAT" (what it is, that it runs the skill through the user's
  own Claude Code, `./install.sh --cat`, then double-click `cat/Tiger CAT.app`), linking to `cat/README.md`.
  `cat/README.md`: paths that said `tools/serve.py` from the app folder stay valid when run inside `cat/`;
  say so in its Start section ("from the repository root: `python3 cat/tools/serve.py`").
- `skills/tibetan-translate/SKILL.md` §8.6 and `reference/notes.md` §4 mention "the CAT app": leave the
  sentences, no path there.
- `cat/docs/skill-update-prompt.md`: add one line under §5 that the skills now live in `../../skills/`.
- Two `.claude/` folders: keep this repo's (`.claude/worktrees` is gitignored), move the app's
  `launch.json` configs into `.claude/launch.json` with the server path `cat/tools/serve.py`.
- `tests/campaign_*` runlogs and prompts contain `~/.claude/skills/...` paths: leave them, they are
  records of runs.

## 3. Memory and handover

- Claude Code keeps per-folder memory under `~/.claude/projects/<path-key>/memory/`. The app's notes live
  under the key for `~/Desktop/CAT Tool` (`-Users-gabrielkobler-Desktop-CAT-Tool`). Copy its `*.md` files
  into this folder's memory directory (`-Users-gabrielkobler-Desktop-Tibetan-Translation-Skills`), append
  their index lines to that `MEMORY.md`, and fix the handover pointer to `HANDOVER.md` in this repo. Do not
  delete the old memory directory.
- `HANDOVER.md`: merge the two files into one with the sections "Skills" and "Tiger CAT (cat/)"; update
  every path; note the date of the merge and that the app's git history was not carried over.

## 4. Verify

- `python3 -m py_compile cat/tools/*.py skills/tibetan-translate/tools/*.py`
- `./install.sh --skills-only` then `diff -r skills/tibetan-translate ~/.claude/skills/tibetan-translate` is empty.
- `cat/tools/build_data.py` on `cat/projects/lesson-prep` writes data.json with 4 gloss files.
- Start the server from the repo root (`~/.venvs/vcat/bin/python3 cat/tools/serve.py --port 8765`),
  open http://127.0.0.1:8765/?p=lesson-prep, check the Grounding tab of U02 shows the primary-search hits
  and that an aligned export succeeds; stop the server.
- `open "cat/Tiger CAT.app"` starts the server and the browser; quit it.
- `git status`: no stray files; `git diff --stat --cached` shows renames, not deletes plus adds.

## 5. Commit

One commit: "Merge Tiger CAT into the repository under cat/; install.sh --cat; one README and handover".
Then tell me what changed, what you verified, and anything you left out.
