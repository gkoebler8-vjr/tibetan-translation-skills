# What the finished Lam Zab verses actually do

An analysis of the 135 finished verse blocks (782 lines) in `08_Master_Edition/src/LZ_src_01..13.md`,
read against their Tibetan and the academic crib in `04_Working_Drafts/LZ_chunk_*.docx`. The purpose
is to derive the ruleset a verse skill should enforce, from practice rather than from theory.

## 1. The numbers

| Measure | Finding |
|---|---|
| Lines fully clean as strict iambic at one measure per block (`scan.py`) | 362 / 761 = 48 % |
| Blocks where every line is strict-clean at one measure | 14 / 135 |
| Best single measure per block | tetrameter 42, pentameter 53, trimeter 28, hexameter 8, 7-beat 4 |
| Syllables per line | median 10, mean 10.4, inner band 8–12 (85 % of lines) |
| Flat-read beats (`beats.py` low count) | 3 beats 39 %, 4 beats 28 %, 2 beats 19 %, 5+ 13 % |
| Within-block variation of line length | the norm is a spread of 1–2 beats; only 18 blocks are isometric |
| Line-initial capital | 741 / 743 (house rule R8) |
| Line-end punctuation | comma 39 %, full stop 32 %, none 19 %, em dash 4 % |
| Em dashes in verse | 35 lines (the v2/v3 "no em dash" ban is not what the translator does) |
| Contractions (it's, won't, aren't) | 21 lines (ruling R54: ordinary contractions are admitted) |
| Rhyme | none sought |
| English lines vs Tibetan padas | one-to-one is the mode; roughly a third of blocks unpack (+1 to +5 lines); a third compress by one line, almost always where an introducer or a half-pada was folded |

The headline: **the finished verse is accentual-iambic in feel, not strict iambic in fact.** Strict
foot-by-foot metre was the pass-B spec, and the translator's own final choices abandon it in half the
lines. What survives is a rising pulse, a line length that stays inside a two-beat band for the
block, and a strong preference for natural word order and the bound terminology over metrical
cleanliness.

## 2. What is held constant inside a block

1. **One rhythmic kind per block.** Every block is rising (iambic/anapestic) throughout. There is no
   block that starts iambic and turns trochaic. Initial inversions ("Bless me in the state of
   dharmata", "Whatever harm there is within these worlds") are common and never read as a change of
   metre. This is the single rule the translator calls a hard limit, and the corpus bears it out.
2. **A beat band of two adjacent counts**, with occasional outliers. "To calm afflictions, to be free
   of fault and harm" (5–6) sits next to "Achieve both aims spontaneously" (3–4) inside one block; the
   block still reads as one piece because the pulse is the same and the outliers are single lines.
3. **Line-initial capital, sentence punctuation at line ends, end-stopping by default.** Enjambment
   is used, but the line end nearly always coincides with a phrase boundary: "The buddhas through all
   eons, every single one, / Arose by their reliance on their gurus."
4. **Plain diction, second person, contractions allowed.** "What's the point of so much studying",
   "That's conceptual thought", "Then aren't they deceiving others and themselves". The register is a
   teacher talking, not a hymnal.

## 3. What flexes

1. **Line length flexes to the content.** A dense 9-syllable pada becomes a 6-beat line rather than
   two 3-beat lines when the sentence would otherwise break badly: "Let conceptual patterns of
   scriptural phrases fade." A thin pada stays short: "The way things truly are."
2. **Feet flex.** Anapests mid-line ("to be FREE of FAULT and HARM"), feminine endings on every
   Sanskrit term ("Vairocana", "mandala", "dharmakaya"), occasional spondees ("great bliss"). Dactylic
   words are not avoided ("Primordially uncreated, fully pure"); they are placed where the falling
   syllables are absorbed by the next rising foot.
3. **Lines-to-padas flexes.** Unpack when the pada is dense (2.1/44: five padas → eight lines) or
   when a list wants one item per line (1.1/40). Compress when an introducer or a tag-pada
   (`zhes dang`) carries nothing. Never drop content: the compression is of frame, not of meaning.
4. **Order flexes, sparingly, and almost always for one reason**: to get the predicate or the
   governing noun first. 2.1/47 moves the final pada ("it is the heart of the victors of the three
   times") to the front so the four appositive padas hang off a stated subject. 2.4.4.1/05 moves the
   homage ("I offer homage to the precious master") from pada 4 to line 1 for the same reason.
   2.4.4.4.1/30 swaps padas 1 and 2 so the conditional clause leads. Enumerations, anaphora
   ("Vajrasattva is exactly that. / The six buddhas are exactly that. / ...") and climactic closes
   are never permuted.
5. **Prose setting flexes in.** Where the padas are long (11+ syllables) and the English would sprawl,
   the block is set as long lines that are frankly prose with line breaks (2.4.4.4.2.2.1.3/48,
   2.4.4.4.2.2.2/41). Ruling R53 licenses this.

## 4. What never gives

1. **The bound term.** `ye shes` is "primordial awareness" in every one of its ~25 verse occurrences,
   even where it costs the metre ("You come to touch that same primordial awareness"). `dge ba'i bshes
   gnyen` is "friend of virtue" (with "spiritual friend" in prose). `rnam rtog` is "conceptual
   thought(s)". `byin rlabs` "blessings". Sanskrit stays anglicized without diacritics and lowercase
   for common nouns (dharmakaya, mahamudra, samsara, bhumi, kaya), capitalized for names.
2. **Natural word order.** No "the mind supreme", no "him I praise". The two or three inversions that
   survive are the ordinary English kind ("Beyond the stains of thoughts and concepts, / That
   suchness... / Is the non-abiding nirvana": fronted adverbial, not verb-subject inversion).
3. **The relation particles.** `las` "from/out of", `pas` "because/since/by", `na` "if/when", `kyang`
   "although/even", `phyir` "to/in order to/because". These are in the English every time, often at
   the line head, where they also set the rhythm: "If you follow...", "Although I saw...", "Because
   the faults are adventitious...", "Until the stake of grasping is removed".
4. **Completeness.** Quantifiers ("every single one", "without exception", "all"), restrictives
   ("merely", "only", "just"), interjections ("Oh! Behold!", "Alas", "Beware!"), honorific address ("O
   you gracious one") all land.
5. **The speech act.** Homage stays homage ("To you I offer reverence"), aspiration stays optative,
   instruction stays imperative ("Give up your hopes and wishes for clairvoyance"), rhetorical
   question stays a question ("Am I, Milarepa, not a great meditator?").

## 5. Three failure types the translator himself corrected

Reading the academic crib against the finals shows what he changes:

- **Crib inversions and hymnal syntax**: "I offer reverence to this precious Master" → "I offer
  homage to the precious master"; "Thus, in the teaching of the Buddha" → "Thus in the Buddha's word
  it says".
- **Scattered heads**: the crib's "The master, the Svābhāvikakāya of the true nature of mind, / Is
  effortlessly accomplished..." becomes homage-first with the appositives after the governing noun.
- **Opaque calques**: "jewel of suchness will be lost amidst the thicket of phenomena" is kept
  (English can carry it); "lotus feet", "marrow of the heart" types are let go.

And one failure he leaves standing and marks: lines he cannot settle stay red with a `{{V:...}}` or
`{{Q:...}}` marker and a query to the Vikramashila reviewers. A doubt is recorded, never smoothed.

## 6. The ruleset this implies (what the skill should enforce)

**Hard rules (a line that breaks one is rewritten):**
- R1 One rhythmic kind per block: rising (iambic base) or falling (trochaic base), declared, never
  mixed. Initial inversion and feminine ending do not count as a change.
- R2 A beat band of two adjacent counts for the block (n, n+1); at most two lines may sit one beat
  outside it, never more than one beat outside. Ceiling 7 beats.
- R3 Stress is given by the language (the flat read). A line that needs a function word promoted or
  a lexical stress moved to reach its count has not reached its count.
- R4 Natural word order; no inversion, no postposed adjective, no archaism, no filler.
- R5 Bound terms exactly, even at metrical cost; place them at line end or step the measure up; swap
  only with a note.
- R6 Every grammatical relation carried (las/pas/na/kyang/phyir/pa'i/la); every quantifier,
  negation, restrictive, honorific, vocative, mood lands.
- R7 Line integrity: each line a unit the ear can hold; never break determiner/noun, preposition/
  object, auxiliary/verb, verb/short object.
- R8 No fewer English lines than content-bearing padas (tag-padas and introducers excepted); unpack
  rather than compress.

**Soft rules (preferences, departures declared):**
- S1 One English line per pada in Tibetan order; permute only inside one sentence and only to
  bring the predicate or governing noun forward; never across anaphora, enumeration, sequence, or a
  climactic close.
- S2 End-stop where the Tibetan end-stops; enjamb only where the Tibetan syntax runs over.
- S3 Prefer the measure the densest pada gives; 7-syllable padas ~3–4 beats, 9 ~4–5, 11 ~5–6.
- S4 Anapests, feminine endings, one spondee, dactylic words absorbed by the following rise are all
  ordinary; a run of four unstressed syllables is a sag, two runs of three in one line is slack.
- S5 Where the padas are 11+ syllables and the English sprawls, set as long lines (frank prose with
  line breaks) rather than unpacking into three lines per pada; say so.
- S6 Contractions and em dashes follow the project's house style (LZ: both allowed); default for a
  new project: contractions allowed in instruction register, not in homage; em dashes allowed.
- S7 Capital at every line start if the house style says so (LZ: yes); otherwise sentence-initial
  only.

**Output discipline:**
- One finished version, not a menu. A second only for a genuine fork.
- Mode and measure declared in one line; order declared when permuted.
- Notes only where there is something to say (`Q:` doubt, `Alt:` hard word, `Issue:` term swap /
  unpack / image let go).

## 7. Calibration check

`beats.py citation` (v4 rule) over all 135 finished blocks: 65 sit inside a band of two counts, 40
inside three, 22 are flagged WIDE (four counts), 8 fail. The failures are the long-pada blocks the
translator set as near-prose lines under ruling R53 and a few blocks that mix a one-word line with
a seven-beat line. Four blocks draw a KIND? advisory, all of them imperative-opening homage or
instruction stanzas where the initial inversions pile up; none actually changes kind. The rule
therefore passes the translator's own practice and flags only what he would himself look at twice.
