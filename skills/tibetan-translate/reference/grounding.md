# Pass 2 — grounding the reading in the tradition's commentaries

A translation that follows the grammar and the dictionary alone is a reading; one that follows
the commentators who glossed the same words is a reading the tradition recognizes. Dharmamitra's
index holds the Kangyur, the Tengyur, the Nyingma Kama and Terma, the Sakya collections, the ACIP
sungbums, the Tsadra series and more, and its Explore endpoint finds the passages that quote or
explain the words you are translating. This pass uses it to do three things: translate according
to the commentaries where they settle a reading, tell the editing translator where they disagree,
and give the reader a footnote where the commentary unlocks the passage.

## 1. The tools, in the order you reach for them

```bash
DM=~/.claude/skills/tibetan-translate/tools/dm.py
python3 $DM explore  "<key clause or line, Wylie>"          # the works that quote or gloss these words, with the Tibetan of each
python3 $DM segment  <segmentnr> --context --window 8       # read on where a gloss is cut short
python3 $DM parallels <segmentnr>                           # variant readings of a canonical line
python3 $DM identify "<quoted words>" [--exclude <Toh>]     # source of a quotation (tibetan-citations)
```

**`explore`** takes 10–20 seconds and returns, for each work it finds, the Tibetan of the passage,
a machine rendering, the work's title and a segment id (`BO_T06_D4025:118b-31` = Tengyur, Toh 4025,
folio 118b; `BO_S10_…`, `BO_TSD_…`, `BO_ACIP-SUNGBUM_…`, `BO_EGS_…` = sungbum and series texts;
`BO_K12_D0431` = Kangyur, Toh 431). Query it with the **words that carry the doubt**: the clause
whose agent, relation or term is in question, 10–25 syllables, in Wylie. A whole stanza returns the
same commentaries less precisely. Two to four calls a page is the budget; more than that means you
are querying units that are not in doubt.

**Read the Tibetan of the hit, not its machine English.** The rendering beside each hit is MITRA or
Gemini output: good enough to tell you which hit matters, not good enough to translate from. The
closing summary is Gemini's and may blur works together; the hits are data, the summary is a map.

**`segment --context`** when the hit stops before the gloss finishes (the window default is 6
segments each side; 8–15 reaches the end of a long gloss). **`parallels`** on a canonical segment
lists the other witnesses of the line with their wording; a variant that changes the sense (`gti
mug` for `ma rig`, `min` for `yin`) goes into the sketch's `VAR` line and, in academic mode, into a
footnote.

`dm.py search` (raw semantic search) is noisier than `explore` and is not needed in this pass.

**Existing English translations among the hits** (`EN_` segment ids; `explore` labels them). They
are not grounding (a translation is not a gloss), and they are handled by the brief's
prior-translations policy and `reference/existing-translations.md`: consulted after drafting as a
witness, adapted only where the licence or a permission allows, always cited (`dm.py cite
EN_<file>:<n>`), never read before Pass 1. In a blind test run use `explore --no-en`. The text you
are translating can also appear among the hits (`--exclude-file <its prefix>` hides it;
`identify --exclude` takes a Toh number or a segment prefix).

**What is queried, and what is not.** Citations and root-text lines, always. In the author's own
prose, a technical term, formula or enumeration (`nges pa lnga`, `bdud bzhi`, `rtag chad kyi
mtha'`): query the term, not the sentence. The author's plain prose is **not queried**; its header
says `grounding: not queried`. Save each output as `dm_<command>_<unit>.txt` in the run directory.

## 2. What counts as a gloss, and what you do with it

A **gloss** is a passage in another work that takes up the words you are translating and explains
them: the scaffold `… zhes pa ni … ste`, `… zhes bya ba ni …`, `… ni … la bya`, a paraphrase that
restates the line with the elided arguments filled in, or an enumeration that spells out a term
(`sku gsum ni …`). A **quotation** is a work citing the line without explaining it; it is a witness
for the wording (variants), not for the meaning. A **semantic neighbour** shares a topic, not the
words; it is not grounding and is not cited.

| What you find | What you do in the body | What you write |
|---|---|---|
| One gloss, consistent with the grammar | translate according to it (the elided subject it names, the sense it gives a term, the relation it makes explicit) | `GROUNDING: <work>, <Toh/segment>: reads X as Y; followed.` and a `Source:`-style mention in the header |
| A gloss that resolves a recorded `Q:` | take its branch | keep the `Q:` shortened to "resolved by <work>"; a footnote where the audience gets one |
| A gloss that contradicts the grammar you read | keep the grammatical reading unless you can see how the commentator read the syntax; then follow the commentator and say so | `Comm:` note giving the commentary's reading and source; footnote in academic and seasoned modes |
| Two glosses that disagree | the plainer or the lineage's own reading in the body (the brief's source context says which lineage) | `Comm:` note with both readings and sources; footnote in academic mode, and in seasoned mode when the difference matters to practice |
| Only quotations, no gloss | nothing changes in the body | `VAR:` if the wording differs in a way that matters |
| Nothing | nothing | `GROUNDING: none found` once for the unit |

A commentary written in the tradition the text belongs to (the brief's source context) outranks
one from another school when they disagree; the root text's own commentary (a `rnam bshad` or
`'grel pa` of that very work) outranks a commentary that merely quotes it. Say which you followed.

Never let a gloss add content to the body that the Tibetan you translate does not carry: the
gloss settles **which** reading of these words, it does not license an explanatory expansion. The
explanation goes into the footnote.

## 3. Patterns (schematic; the test pages are deliberately not used as examples)

- **A root-text citation in a commentary.** `identify` on the quoted words gives the root (Kangyur
  or Tengyur, with Toh) and the works that quote it. `explore` on the padas in doubt usually returns
  quotations only; the gloss is in the root's own commentaries, which appear among the quoting works:
  `segment <id> --context --window 8–12` on one of them reaches the `… zhes pa ni …` passage. Where
  an epithet-like phrase (`'jig rten mkhyen`) is glossed as a technical knowledge or activity, the
  body follows the gloss and a seasoned-practitioner footnote says so in one sentence; an academic
  footnote adds the commentary and folio.
- **A tantra's prose with an elided agent.** `explore` on the clause returns the root and later
  quotations; the tantra's Tengyur commentary, if indexed, is the gloss to read with `segment
  --context`. If it names the agent, follow it; if it does not, the plain grammatical reading stands
  and the fork stays a `Q:`.
- **A commentary that is itself the text.** `identify --exclude <its Toh>` on its quotations finds
  their sources; `explore` on its own glosses finds the parallel commentaries on the same root
  words, which is where a disputed sense of a term is settled or shown to be disputed. Its own
  copy, and any aligned English, will appear among the hits: skip them.
- **The author's own prose.** A formula or enumeration in it (`bdud bzhi`, `nges pa lnga`) is
  queried as a term; the sentence itself is not. `grounding: not queried`.

## 4. Honesty rules

- A Toh number, folio or attribution appears in a note only if you have seen it in a hit and read
  the title. `source not located` and `GROUNDING: none found` are honest; an inferred locator is not.
- The explore summary's attributions are checked against the hit list before use.
- An English translation among the hits (`EN_…`) is used only as the prior-translations policy
  allows, and always cited; in a blind test it is neither read nor cited and the exposure is logged.
- Dharmamitra is a public research service used one request at a time; when it is slow or down,
  skip the pass, say `GROUNDING: service unavailable`, and translate from the grammar.
