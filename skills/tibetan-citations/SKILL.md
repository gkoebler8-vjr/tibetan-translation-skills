---
name: tibetan-citations
description: Handle the citation apparatus of a Tibetan text — identify the quoted work, fix its English short title, look up Toh and 84000 references, decide what becomes a footnote and what becomes a sources-register entry, and keep the register and title glossary consistent. Use when a translation contains quotations that need identifying or referencing, when triaging the footnotes of an academic translation for a reader edition, when a title needs its fixed English short form, or when building or checking a sources register. Pairs with tibetan-translate and tibetan-verse, which render the quotations themselves, and uses the tibetan-dharmamitra tools (dm.py identify) for the lookup.
---

# Citations, sources, and the register

## 0. Gate

Calibrated for **Opus or Fable at maximum reasoning effort**; identification work is where a weaker
setting invents plausible Toh numbers. State the model and effort. If it is not Opus or Fable,
stop and say so. **Never state a Toh number, folio, or attribution you have not verified** — an
unverified locator is worse than none, because it looks checked.

## 1. The principle

**A locator must not disturb the reader.** Source references leave the footnote stream and go to a
back-matter register keyed by page and by the quotation's opening words, with no in-text marker.
Footnotes are kept only for what a reader actually needs: an enumeration behind a term, an
identification that unlocks the passage, a practical clarification, one genuinely opaque image.

## 2. Footnote triage

Every note in an academic source falls into one of three classes.

- **Keep as a footnote** — explanatory and reader-relevant: the four maras enumerated, who a name
  refers to, a mantra translated, an image that will not survive unglossed. Rewrite it in the body
  voice, three sentences at most, dropping Wylie and IAST unless the term itself is the point, with
  no secondary-literature citations.
- **Move to the register** — source locators: Toh and Derge numbers, Kangyur/Tengyur volume and
  folio, BDRC references, identification of the quoted work. These never appear as body footnotes.
- **Cut** — witness variants, Wylie transcriptions of the quoted passage, secondary literature,
  methodology, translation-choice musings, catalogue notes, cross-references to a thesis. Report
  the dropped originals in the run log, never in the edition.

A mixed note is routed by its dominant function; if the split matters, leave a one-line issue note.
A "source not located" note is dropped, its marker removed, and the fact reported. What a *new*
footnote may contain for each audience, and how it is written, is in tibetan-translate's
`reference/notes.md`.

## 3. Identifying a quotation

1. **Read the introducer.** `zhes … las` / `las kyang` / `gsungs pa ltar` names or implies a work;
   `X na re` names a person. The Tibetan often gives an abbreviated title (`gur` for the Vajra
   Tent, `sdud pa` for the Condensed Perfection of Wisdom, `spyod 'jug`, `mdo sde rgyan`).
2. **Search the quoted words**, not the title. The same verse travels between texts under
   different attributions, and the citing author is often quoting from memory:

   ```bash
   python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "<the quoted lines, Wylie>"
   ```

   This queries Dharmamitra's canon index (Kangyur, Tengyur, sungbums, the Tsadra series,
   Lotsawa House) and prints the Kangyur/Tengyur hits with their Toh numbers and segment ids,
   then the works that quote the passage. Several canonical hits mean the verse travels; say
   which the citing text names and which the corpus supports. `dm.py parallels <segmentnr>`
   gives the variant readings; `dm.py segment <segmentnr> --context` a commentary's gloss.
   Details: the tibetan-dharmamitra skill.
3. **Verify before you write it down.** A Toh number comes from a hit whose words match the
   quotation, and whose title you have read. For a cross-check, the 84000 Reading Room resolves by
   number (`https://84000.co/translation/toh<N>`); a number that does not resolve, or resolves to
   something else, is not confirmed.
4. **Record what you could not confirm.** `source not located` is a legitimate, and honest, register
   entry. An invented locator is not.

## 4. English short titles

- Every work gets **one fixed English short title**, decided on first use and binding thereafter.
- It is recorded as a `TITLE` row in the project glossary, in `register.py`'s column order:
  `TITLE <tab> english_short_title <tab> wylie_title <tab> iast_title <tab> locator` (the Sanskrit
  title where there is one; the locator as verified). The English form is the second column; a
  Wylie title in that column is read by `--titles` as the English title.
- In the body: **English short title only, in italics.** Never a Sanskrit or Wylie title, never a
  Toh number.
- Collections and genres stay roman: Vinaya, Kangyur, Tengyur, Tripitaka, sutra, tantra,
  Anuttarayoga Tantra.
- A title coined for this edition (no established English form) is marked as coined in the notes,
  once.

## 5. The register

One row per quotation. Columns, tab-separated:

```
chunk   unit_id   orig_fn   opening_words   work_and_locator
```

`opening_words` is the quotation's first few words in the final English, which is what keys the
back-matter entry to the page. Append only, dedup on `unit_id + orig_fn`, never rewrite an
existing row. `tools/register.py` does this safely:

```bash
python3 ~/.claude/skills/tibetan-citations/tools/register.py --check   sources.tsv
python3 ~/.claude/skills/tibetan-citations/tools/register.py --add     sources.tsv \
        --chunk 05 --unit 1.3/12 --fn 214 \
        --opening "For one who violates discipline" \
        --locator "Śrīmahāsaṃvarodayatantra; Tōh 373, DK vol. 78, f. 265a"
python3 ~/.claude/skills/tibetan-citations/tools/register.py --titles  glossary.tsv
```

`--check` reports duplicates, malformed rows, and rows whose locator is empty or says "not
located". `--titles` lists the `TITLE` rows and flags any two English short titles pointing at the
same Wylie title, or one Wylie title with two English forms — the drift that makes an edition
inconsistent.

## 6. Italics are verified, not remembered

Every English short title in the body is italic. This is checked mechanically at merge, not by
eye — in the Lam Zab edition by `08_Master_Edition/check_italics.py`, which flags a glossary title
in roman as a defect, a title-shaped phrase in roman as a candidate for a ruling, and italics on a
non-title as a stray. Any project doing this work should have the equivalent check; a title in
roman is a defect that survives every read-through.

## 7. Working with the other skills

Order of operations for a passage that contains a quotation:

1. `tibetan-translate`'s grounding pass (Pass 2) runs `dm.py identify` on the quoted words and
   records the result in the construal sketch's `CITATION` and `VAR` lines (quoted work, opening
   words, Toh, segment id, variants).
2. **This skill** identifies and verifies the source, fixes or reuses the English short title, and
   writes the register row.
3. `tibetan-translate` renders the framing sentence with the citation formula of its prose rules
   (`reference/prose.md` §3), using that fixed title.
4. `tibetan-verse` renders the quotation if it is verse.

The title is fixed **before** the framing sentence is drafted. Retrofitting a title into finished
prose is how two forms of one title end up in one edition.
