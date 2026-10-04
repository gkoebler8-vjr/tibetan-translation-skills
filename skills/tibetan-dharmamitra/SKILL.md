---
name: tibetan-dharmamitra
description: Use Dharmamitra's public research APIs (DharmaMitra search, DharmaNexus parallels, MITRA translation) from this machine for Tibetan, Sanskrit, Pali and Buddhist Chinese — find where a passage occurs in the canon with its Toh number, pull variant readings and the commentaries that gloss it, fetch a canonical segment with context, and get a MITRA machine translation as a second opinion to compare against a Claude rendering. Use when the user mentions Dharmamitra, MITRA, DharmaNexus, BuddhaNexus, "explore", source identification, parallels, variants, or wants a translation cross-checked; tibetan-translate calls it through tools/dm.py in its analysis pass. Also documents the optional local MITRA model.
---

# Dharmamitra from the command line

## 1. What is available, and on what terms

`https://dharmamitra.org` exposes two documented, keyless JSON backends (`/api-search/docs`,
`/api-db/docs`), and Dharmamitra publishes its own Claude Code starter pack that calls them
(`github.com/dharmamitra/dharmamitra-claude-code-agent`). The client here,
`~/.claude/skills/tibetan-translate/tools/dm.py`, wraps the parts a translator needs and prints
compact text (Tibetan in Wylie: three times cheaper in tokens than script; `--script` keeps script).

Terms: personal research use at a polite rate (one request at a time, cache results). Their ToS
forbids using the APIs to populate third-party applications; this pipeline is a personal research
tool, not a product. The Explore page's AI summary and Deep Research are Gemini-backed; the search,
parallels and MITRA translation are self-hosted. Tested 2026-10-03: Kangyur (1,158 files), Tengyur
(3,855), Nyingma Kama and Terma, Sakya, ACIP sungbums, the Tsadra series (Drikung, Gampopa,
Phagmodrupa, Götsangpa, Mikyö Dorje …), Lotsawa House, Edition Garchen Stiftung are all indexed.

## 2. Commands

```bash
DM=~/.claude/skills/tibetan-translate/tools/dm.py
python3 $DM identify "<quoted lines, Wylie or script>"   # source + Toh, who quotes it   (~0.8k tokens)
python3 $DM parallels <segmentnr>                        # precomputed parallels, variant readings
python3 $DM segment <segmentnr> --context [--window 3]   # the segment with its neighbours (a commentary's gloss)
python3 $DM search "<query>" [--lang bo|sa|zh|pa|all] [--type regular|semantic|semantic_only]
python3 $DM translate "<tibetan>" [--style "..."] [--context "..."]   # MITRA cat-translate
python3 $DM meta <filename>                              # titles, Toh/Peking, translators, BDRC link
python3 $DM explore "<query>"                            # the works that quote or gloss the words, Tibetan + segment id (10–20 s); the grounding tool
```

`explore` is the tool of tibetan-translate's grounding pass (`reference/grounding.md` there): given
10–25 syllables of Wylie it lists the commentaries, treatises and sungbum texts that take up those
words, each with its Tibetan, a machine rendering and a segment id, then a Gemini summary. Read the
Tibetan of the hits; treat the renderings and the summary as a map. Follow a cut-off gloss with
`segment <id> --context --window 8`.

Segment ids are stable keys: `BO_K12_D0381:158a-16` = Kangyur, Derge 381 (Toh 381), folio 158a.
`BO_T02_D1490` = Tengyur, Toh 1490. `BO_TSD_…`, `BO_S10_…`, `BO_LH_…` are sungbum and series texts.
`dm.py` derives the Toh number from the id; confirm it against the title before writing it down.

## 3. The identification procedure (for tibetan-citations)

1. `identify` on the **quoted words**, never on the title. The citing author abbreviates titles
   and quotes from memory.
2. Read the CANONICAL candidates: the Kangyur/Tengyur hits with the same words are the source;
   several Kangyur hits mean the verse travels (the sample verse appears in the Sampuṭa, the
   Vajrahṛdayālaṃkāra and the Māyājāla, and is attributed by commentators to the
   Vairocanābhisaṃbodhi as well). Say which the citing text names, and which the corpus supports.
3. `parallels` on the best segment for the variant readings (`gti mug` / `ma rig` / `rmongs pa`;
   `'gyur` / `mngon` / `snang`). A variant that changes the sense goes into the construal's VARIANTS
   field and, in academic mode, into a note.
4. `segment --context` on a commentary hit when the line is obscure: the commentary's gloss
   (`zhes pa ni …`) is the traditional reading of the line.
5. Record: work, Toh, segmentnr, src_link. **Never state a Toh number you have not seen in a hit.**
   `source not located` is an honest register entry; an invented locator is not.

## 3b. Grounding a reading in the commentaries (for tibetan-translate Pass 2)

1. `explore` on the clause that carries the doubt (agent, relation, term), not on the whole stanza.
2. Sort the hits: a **gloss** (`… zhes pa ni … ste`, a paraphrase filling the elided arguments, an
   enumeration of a term) is grounding; a bare **quotation** is a witness for the wording; a
   semantic neighbour is neither.
3. Read the gloss in Tibetan (`segment --context` if it is cut short). Follow it where the grammar
   permits; where glosses disagree, the text's own tradition and its own commentary outrank others.
4. Record work, Toh or segment id, what it says and what you did in the construal's `GROUNDING`
   line; the editor gets a `Comm:` note, the reader a footnote per the audience (`notes.md`).
5. Nothing found: `GROUNDING: none found`. Service down: say so and translate from the grammar.

## 4. Second opinion: Claude vs MITRA

MITRA (`translate`) is a translation-tuned Qwen3.5 model trained on 1.7M aligned Buddhist sentence
pairs. It reads content words well and relations unreliably, has no register and no glossary. Use
it as a **cross-check after the fidelity check**, not as a draft:

1. `python3 $DM translate "<unit>" --style "literal, keep every clause and connective"`.
2. Compare against the construal, clause by clause: where MITRA and the construal disagree on a
   content word, a referent, or a reading, that is a `Q:` to resolve from the grammar and the
   dictionary, not a vote. Where they agree against the draft, the draft is probably wrong.
3. Report the disagreements only (`Check: MITRA differs at clause 3: reads skyes pa as "man"`).

Cost: ~0.2k tokens per unit. A standing comparison protocol for evaluating whether MITRA catches
errors Claude makes is in `reference/compare.md`.

## 5. The local model (optional)

The hosted `translate` endpoint is the same MITRA Qwen3.5 model the local install would run, so
the local model is only needed offline. Setup script and client are in `tools/` (`setup_mitra.sh`,
`mitra.py`, which expects an OpenAI-compatible server on port 8080; `mlx_lm.convert` of
`buddhist-nlp/mitra-qwen35-translate`, ~24 GB disk, 4-bit). Check that mlx-lm implements the
Qwen3.5 architecture before converting.

## 6. Other Dharmamitra resources used by the pipeline

- **MITRA Tibetan Lexicon** (StarDict, 237k headwords, English/Sanskrit renderings attested in
  parallel texts, POS profiles, verb paradigms with Hackett syntax, cited examples) — indexed by
  `tibdict.py` at `~/.tibdict/`. Download: `https://dharmamitra.org/pub/dictionaries/mitra-stardict-tib-lexicon-2026.zip`.
- **mitra-bo-zh-tagger** (9B Qwen3.5; word segmentation + POS for classical Tibetan, F1 ≈ 0.95)
  needs 24–32 GB unified memory; not run here (16 GB machine). `tibdict.py` uses botok instead.
- **mitra-parallel** (1.7M aligned Skt–Tib–Chi records, CC BY) on GitHub, for offline retrieval if
  ever needed.
