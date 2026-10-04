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

## 3. Examples

- *Rays of Sunlight*, the Uttaratantra citation `thugs rje chen pos 'jig rten mkhyen / 'jig rten kun
  la gzigs nas ni / chos kyi sku las ma g.yos par`. `explore` on `'jig rten mkhyen pa thugs rje chen
  po dang ldan pas 'jig rten kun la gzigs nas` returns the root (Toh 4024), Asaṅga's commentary (Toh
  4025) and later Tibetan commentaries (the *Lamp of Precious Definitive Meaning*, the *Lion's Roar of
  the Irreversible*, as the hits title them) whose glosses read
  `'jig rten mkhyen` as the knowledge of the world in its extent (*ji snyed pa mkhyen pa*) and
  `chos kyi sku las ma g.yos par` as unwavering equipoise in the dharmakaya (*ji lta ba mkhyen pa*).
  So "knows the world" is not a loose epithet: it is the extent-knowledge, paired with the
  nature-knowledge of the next line. A seasoned-practitioner footnote says so in one sentence; an
  academic one adds the commentaries and folios.
- *Caṇḍamahāroṣaṇa* ch. 15, `de yang bur skye bar byed` and `bu mo rnams kyang … 'dod par byed`.
  `explore` on the clause returns the root (Toh 431) and quotations in later works; the tantra's Tengyur
  commentary (the Padmāvatī), when it appears among the hits, is the gloss to read with `segment
  --context`. If it names the
  agent, follow it; if it does not, the plain grammatical reading stands and both forks stay `Q:`.
- A commentary text itself (the Jewel Garland of Yoga, Toh 1183): `identify --exclude 1183` on its
  quotations finds their sources; `explore` on its own glosses finds the parallel commentaries on
  the same Hevajra root words, which is where a disputed sense of `rab tu bsgrub pa`
  is settled or shown to be disputed.

## 4. Honesty rules

- A Toh number, folio or attribution appears in a note only if you have seen it in a hit and read
  the title. `source not located` and `GROUNDING: none found` are honest; an inferred locator is not.
- The explore summary's attributions are checked against the hit list before use.
- Dharmamitra is a public research service used one request at a time; when it is slow or down,
  skip the pass, say `GROUNDING: service unavailable`, and translate from the grammar.
