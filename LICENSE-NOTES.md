# What may be shared, and on what terms (as of 2026-10-03)

This is a working note, not legal advice. Check each item before publishing.

## Shareable as-is (your own work)

- The four skills (SKILL.md and reference files), `tibdict.py`, `dm.py`, `beats.py`,
  `lexicon.py`, `register.py`, `install.sh`, the docs. Pick a licence: MIT or Apache-2.0 for the
  code, CC BY 4.0 for the prose. The `lexicon.py` stress table was hand-built over the Lam Zab
  edition and is yours.
- `docs/lz_verse_practice_analysis.md` quotes your own translations: yours to publish.
- The research briefs in `docs/research/` cite public sources; fine to publish with the note that
  they were AI-assisted.

## Shareable with attribution and share-alike

- **MITRA Tibetan Lexicon** (Dharmamitra, CC BY-SA 4.0). `install.sh` downloads it from
  dharmamitra.org rather than bundling it; the README of
  `github.com/dharmamitra/dharmamitra-stardict-dictionaries` gives the attribution. An index built
  from it alone could be shared under CC BY-SA, but it is simpler to let each user build it.

- **Christian Steinert's `public` dictionary folder** (`github.com/christiansteinert/tibetan-dictionary`,
  `_input/dictionaries/public/`): Tibetan-keyed dictionaries as plain `headword|definition` text, the
  freely redistributable half of his dictionary app (the repo's README says its private build holds
  further data that he "cannot distribute publically"). The repo states: "the dictionary data is not
  my own and thus *THE COPYRIGHT OF THE DICTIONARY DATA IS WITH THE RESPECTIVE AUTHORS*"; his own code
  is GPL v2/v3, and there is no licence file for the data. Per-dictionary credits (Hopkins/UMA,
  Berzin Archives, Rangjung Yeshe, Valby, Ives Waldo, Barron, Hackett, Tsepak Rigdzin, 84000, Verbinator
  by N. Hill ...) are in the `about` texts of `webapp/src/config/dictlist.ts` there. Treat it as
  "available to read and use, attribution to the respective authors, no licence to repackage".
  `tibdict.py fetch-public` (`install.sh --public`) therefore downloads the Tibetan-English files from
  GitHub onto each user's own machine, prints that attribution line, and `build --public` indexes them
  locally; nothing is bundled in this repo. The resulting index is private working data like any other:
  some of these dictionaries carry stricter licences of their own (Rangjung Yeshe CC BY-NC-SA, 84000
  glossary CC BY-NC-ND), so do not publish an index built from them.

## Not shareable: do not put these in the repo

- The built index `~/.tibdict/tibdict.sqlite` when it includes your GoldenDict folder, and the
  GoldenDict folder itself. Its sources are each someone else's: Hopkins/UMA (copyright, "with
  permission"), Rangjung Yeshe (CC BY-NC-SA), 84000 glossary (CC BY-NC-ND 3.0: the ND clause bars a
  derived index), Monlam (headwords Apache-2.0, dictionary bodies unclear), Tony Duff's Illuminator
  (commercial), Chandra Das e-edition (the 1902 text is public domain, the e-edition may not be),
  Verbinator / Hill's verb lexicon (no licence stated), Hackett (commercial), Christian Steinert's
  bundle ("copyright of the dictionary data is with the respective authors"). The skill therefore
  ships the *tool* and indexes whatever the user legally has; `install.sh --golden <dir>`.
- The Lam Zab calibration corpus (`tests/lz_verses.json`): your translations plus the Tibetan of
  the 2004 Delhi edition; your call, but it is gitignored by default.
- The test work files under `tests/` contain only your own text and tool output; fine.

## Dharmamitra API use

- The endpoints are public and keyless; Dharmamitra publishes its own Claude Code starter pack for
  them, and Sebastian Nehrdich confirmed in a talk (to your question) that MITRA may be used with AI
  agents. Their terms bar using the API "to populate third-party applications"; a skill that each
  translator runs on their own machine for their own research is not that. Before publicizing,
  send one courtesy email to dharmamitra.project@gmail.com describing the use and asking whether
  they want attribution wording or a rate limit respected; keep the reply in the repo.

## Donations

A donation button on a site that hosts the skills does not make the skills commercial. It would
become a problem only if a bundled NC-licensed dictionary were part of what is offered, which is
why none is bundled.
