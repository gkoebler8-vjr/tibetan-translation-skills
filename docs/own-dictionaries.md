# Using your own dictionaries

The analysis pass looks every word up in a local index (`~/.tibdict/tibdict.sqlite`) built by
`tibdict.py`. What goes into that index is up to you, and nothing in it ever leaves your machine.

## What you get out of the box

`./install.sh` downloads the **MITRA Tibetan Lexicon** (Dharmamitra, CC BY-SA 4.0; 237,000
headwords with attested English and Sanskrit renderings, part-of-speech profiles and verb
paradigms) and builds the index from it. That alone is enough to run the pipeline.

`./install.sh --public` adds the 35 Tibetan–English dictionaries that Christian Steinert's
open-source dictionary project keeps in its `public` folder (Hopkins 2015, Rangjung Yeshe, Jim Valby,
Ives Waldo, Dan Martin, Berzin, the 84000 glossary, Mahāvyutmatti Sanskrit index, Verbinator verb
tables, Tsepak Rigdzin, Yogācārabhūmi glossary and others; about 38 MB). They are fetched onto your
machine, not bundled here; their copyright stays with their authors (see LICENSE-NOTES.md).

## Adding a GoldenDict or StarDict folder

If you already use GoldenDict with a folder of Tibetan dictionaries (`.ifo/.dict/.idx` sets), index
it alongside the lexicon:

```bash
./install.sh --golden "/path/to/your/GoldenDict/TIBETAN"
```

or, later, without reinstalling:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py build --mitra ~/.tibdict --golden "/path/to/folder"
```

The build takes about twenty seconds for 400,000 entries. `tibdict.py status` lists what is
indexed and in which priority. Known dictionaries get a short label and a fixed priority (the table
`GOLDEN_SOURCES` near the top of `tibdict.py`); an unknown StarDict set is indexed under its own
name at low priority. To change which dictionary `annotate` shows first, edit that table and
rebuild. Tibetan–Tibetan dictionaries are indexed only with `--tib`.

## Adding a plain text dictionary

Any file of lines `headword|definition` (Wylie headword) can be dropped into a folder and indexed
with `build --public <folder>`. Steinert's format is exactly this, so a dictionary you have typed up
yourself goes in the same way. Comment lines start with `#`.

## What the tools do with it

- `tibdict.py annotate "<unit>"` — the per-unit report the skill reads: segmentation, particle
  labels, the MITRA sense and one classical dictionary per word, verb paradigms, a `NEG:` count, a
  `COMPOUND?` line for multi-syllable headwords the segmenter split. `--budget 6000` for a long unit.
- `tibdict.py lookup "<word>" --full --examples` — everything the index has on one word.
- `tibdict.py verb <stem>` — the paradigm and the case frame.

## Do not publish the index

An index built from your GoldenDict folder or from the public set contains other people's work under
mixed licences (some non-commercial, some no-derivatives). Use it, do not redistribute it. The
lexicon-only index could in principle be shared under CC BY-SA, but it is quicker for everyone to
build their own.
