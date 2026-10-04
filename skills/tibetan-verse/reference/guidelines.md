# Versification guidelines v4 — Tibetan verse into English verse

**Scope.** Any Tibetan verse, rendered into English verse from a construal built from the Tibetan
(tibetan-translate, analysis pass). No crib is assumed; where one exists it is a witness, not the
arbiter.

**Lineage.** v2 (strict iambic, five versions) ran the Lam Zab pass B. v3.x replaced feet with
counted beats, added the priority order, idiom and relation rules, line integrity, and the flat
read. **v4 is calibrated against the 135 finished Lam Zab verse blocks** (`lz-practice.md`): it
keeps everything v3 learned, relaxes the band to what the translator's own lines do, makes "one
rhythmic kind per block" the one hard metrical rule, and lets the translator's house choices
(capitals, contractions, dashes, prose setting) be house choices. §10 lists the changes.

---

## 1. The priority order

1. **Natural, clear, idiomatic English.** Reads as current English on first hearing, aloud,
   without backtracking; every phrase one an English writer would write; every line makes a point
   the reader can state back.
2. **Content and its logic.** Everything the Tibetan says is in the English, nothing else is, and
   the grammatical relations survive intact.
3. **One rhythmic kind and a stable measure.** The block is rising or falling throughout; its
   lines sit in a band. **This is the rule that gives** when 1 or 2 need a syllable.
4. **Line correspondence.** One English line per pada, in the Tibetan's order.
5. **Sound.** Alliteration, assonance, rhyme — only if free.

How conflicts resolve: naturalness against metre → metre yields, immediately. Naturalness against
completeness → the form yields: **more lines, never less meaning**. Logic against elegance → logic.
Correspondence against anything above → correspondence yields, declared.

---

## 2. Mode, kind, band

| | Chant mode | Citation mode |
|---|---|---|
| Material | sādhana, liturgy, prayer, anything recited aloud in unison or to a melody | verse quoted inside prose, verse in a treatise or commentary, dohā cited as evidence, verse in a translated book |
| Line length | isometric: every line the same count | a band of two adjacent counts n / n+1; a spread of three (n..n+2) is tolerated when the padas are long, and when one **thin pada** (two or three content words, nothing to add without invention) falls one count under the block's band (§5: a thin pada stays short; `beats.py` accepts 2–4 for 7-syllable padas); a spread of four is flagged; wider fails |
| Kind | one, declared | one, declared |
| Ceiling | 7 beats | 7 beats |

**Kind.** Rising = the first beat falls after one or two unstressed syllables in most lines (iambic
or anapestic base). Falling = most lines open on a beat and close off it (trochaic or dactylic
base). An initial inversion in a rising block ("Bless me…", "Whatever may arise…") is normal
English and not a change of kind. What is forbidden is a block whose lines alternate kinds, so that
the ear resets every line. `beats.py` prints a KIND? advisory when a block looks mixed.

**Why the band is what it is.** The finished Lam Zab verse, flat-read, has lines of 3 to 6 beats
inside one block while reading as one piece, because the pulse is constant and the outliers are
single lines spent on a dense pada or a bound term. A strict single count was tried (pass B) and
abandoned in half the lines by the translator's own hand. The target remains two counts; three
passes; four is a warning; more is a different poem.

**Measure.** Take the densest pada, write it as one natural English line, count its beats on the
flat read. That is the top of the band. 7-syllable padas land at 3–5 beats, 9 at 4–6, 11 at 5–7.
Chant mode takes the count that the densest line needs and holds it; if that pads the thin lines,
unpack the dense line instead and drop the count.

---

## 3. Beats, not feet

The line is counted in beats, the stressed syllables; the syllables between them fall as speech
puts them (accentual verse: Heaney's *Beowulf* line). Foot-by-foot metre and natural English with
fixed technical vocabulary are in direct competition, and naturalness wins.

**What counts.** Content words take a beat. A polysyllable takes one on its primary stress, or two
if it is long and the rhythm wants its secondary (*prímordial awáreness*). Function words do not.
Test: say the line across a room; the syllables you hit are the beats.

**Stress is given by the language, never chosen by the line.** *bless me to realize the dharmakāya*
is BLESS me to RE-alize the dharma-KĀ-ya: three beats. Read as a pentameter it puts the beat on
*me* and pulls *realize* onto its second syllable, and English does neither. The line is fixed by
rewriting it, not by scanning it differently. Traps: an object pronoun after a verb never takes the
beat (*bless me*, *show us*); prepositions, articles, auxiliaries and the copula take none mid-line;
lexical stress does not move (*RE-alize*, *PRI-mor-dial*); compounds keep initial stress
(*DHARma-kaya*); the line end promotes nothing.

**The flat read is the diagnostic**, and `beats.py` performs it mechanically: a claimed count above
the tool's low count, with the difference on function words, is coerced.

**Rhythm hygiene.** One or two unstressed syllables between beats is the norm; three is ordinary
once in a line; twice in one line is slack; four in a row is a sag. Two adjacent beats once per line
is useful emphasis. End on a beat or a falling ending, never on a preposition, auxiliary or article.

**Substitutions that are simply English**, and that the finished Lam Zab lines use freely: an
initial inversion; an anapest mid-line ("to be FREE of FAULT"); a feminine ending (every Sanskrit
term: *Vairocana*, *mandala*, *dharmakaya*); a dactylic word whose falling syllables are absorbed by
the next rise ("PriMORdially unCREated, FULly PURE"); one spondee ("GREAT BLISS").

---

## 4. Reading the Tibetan

Done in tibetan-translate's analysis pass (`reference/analysis.md`): segment and count; find the
verb; tag every relation; negation and scope; the items that leak (restrictives, quantifiers,
honorifics, vocatives, mood, tense stems); verse filler and elided case markers; devices held in
position; the construal in plain prose; the doubts. The verse is drafted from that object.

**Supplying an elided verb is not invention.** Adding an adjective, an image, or an intensifier
is.

---

## 5. Prose first, then lines

Draft the natural English sentence before any line. Then break *that* at the measure, adjusting
wording only as far as the breaks require. If the prose will not break at the measure, change the
measure, not the prose.

---

## 6. Line order

Any permutation of the padas inside one sentence is legal when it makes the English natural, and
the finished Lam Zab uses it for one reason almost every time: **to get the predicate or the
governing noun first.** "It is the heart of the victors of the three times" (pada 4) opens the
stanza so the four appositive padas hang off a stated subject; "I offer homage to the precious
master" (pada 4) opens the homage. Declare it (`order 4-1-2-3`). Never across a sentence boundary.
Never where position is content: line-initial anaphora ("Vajrasattva is exactly that. / The six
buddhas are exactly that."), enumeration, temporal or logical sequence, a climactic close. Prefer
the Tibetan order when both read equally well.

---

## 7. Line integrity

A sentence may run over several lines; the *point* may not be split. Stop at every line end: it
must be a unit the ear can hold, and nothing already read may need re-parsing. Never break
determiner/noun, preposition/object, auxiliary/verb, verb/short object, a noun and the phrase that
identifies it, the halves of a fixed expression. Break where a speaker pauses: between clauses,
before a conjunction or subordinator, after a fronted frame, between list items.

Subject and main verb in the same line or adjacent lines with nothing between. One appositive per
sentence, inside a line.

**Never fewer English lines than content-bearing padas.** A tag-pada (`zhes dang`) or an
introducer (`kun mkhyen klong chen pas`) is frame, not content, and folds into the prose. A dense
pada becomes two lines; a list becomes one line per item. Fewer lines than content padas means
something was dropped.

End-stop where the Tibetan end-stops; enjamb only where the Tibetan syntax runs over and the
integrity test still passes.

**Long padas.** Where padas run 11+ syllables and the English would sprawl or need three lines per
pada, a house rule may set the block as long lines that are frankly prose with line breaks; say so
in an `Issue:` line.

---

## 8. Diction

`english.md` governs: collocation, idiom-for-idiom, clarity, no inversion, the bans, strong verbs,
the short concrete word, person. Verse adds:

- **Terms.** Glossary exactly, chosen before drafting with their stress shape. Where a bound term
  will not sit: re-measure the block, then unpack the pada, then place the term at line end, and
  only then render it differently and note the swap. *ye shes* = "primordial awareness" held in
  every Lam Zab verse is the model: the term wins, the metre gives.
- **Names** scan like any other word: line end, unpack, or the established epithet (Vajra-Holder,
  Lotus-Born), noted.
- **Register** matches the source: homage and supplication elevated but current; instruction plain;
  song colloquial. If the Tibetan is plain, add no ornament.
- **Interjections and address** kept: "Oh! Behold!", "Alas", "Beware!", "O you gracious one".
- **House style** decides line-initial capitals, contractions, em dashes. Defaults for a new
  project: capital at sentence start only; contractions allowed in instruction and song, not in
  homage; em dashes allowed sparingly.

---

## 9. Output

1. Mode, kind, measure, pada count, line count, order — one line.
2. One finished version, through every gate.
3. A second version only for a genuine fork.
4. Notes: `Q:` · `Alt:` · `Issue:` — one line each, only where there is something to say.

No gloss, construal, scansion or gate working in the reply unless asked.

---

## 10. What changed in v4, and why

| v3.2 said | v4 says | Because |
|---|---|---|
| band n/n+1, one line one beat outside | band n/n+1 is the target; a spread of three passes, four is flagged, more fails | the translator's finished lines spread over three counts in most blocks and read as one piece; the strict band rejected half of them |
| rising assumed | one rhythmic kind per block, rising or falling, declared; mixing is the one hard metrical failure | the translator's stated hard limit; the corpus is 100 % consistent on it |
| no em dashes, no contractions | house style | the corpus has 35 dashes and 21 contractions by the translator's hand (ruling R54) |
| permutation "a licence" | permutation for one purpose: predicate or governing noun first | that is the only use the corpus makes of it |
| construal rules inside this spec | construal lives in tibetan-translate's analysis pass | one construal feeds prose, verse, citations and the checker |
| strict foot check (v2) | the flat read, `beats.py`, kind advisory | the foot check bought a metronome and paid with the English; 48 % of the finished lines fail it |
| five versions (v2), three (v3), one (v3.2) | one | unchanged: the choosing is the work |
