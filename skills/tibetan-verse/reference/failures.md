# Failure taxonomy and worked examples

Named failures with a diagnostic you can apply to a draft line without re-reading the Tibetan, and
a fix. Run this list against any version that feels wrong but you cannot say why. Failures 1–10 are
about structure and content; 11–15 are about English, and in practice they are the ones that keep
recurring.

---

## Structure and content

**1. Scattered head.** A noun and the words that identify it spread across two or more lines, so
the reader builds one referent and then has to rebuild it.
*Diagnostic:* the head noun of the subject arrives after the reader has already parsed a complete
noun phrase. *Fix:* head noun first, modifiers after it, inside one line.

**2. Vanishing predicate.** Two or more padas compressed into a short verb phrase ("comes alone",
"is thus", "abides") that carries none of them.
*Diagnostic:* one English line standing for two Tibetan lines. *Fix:* the lines ≥ padas check.
Restore the content; if it will not fit, unpack, never compress.

**3. Stranded subject.** The subject waits two or more lines for its verb, usually because
appositives are stacked between them. *Fix:* permute so the predicate comes earlier, or move the
modifiers after the verb.

**4. Noun pile.** A stanza with no finite verb, reading as a caption. *Fix:* supply the verb the
Tibetan elides. That is grammar, not invention.

**5. Reversed causation.** An ablative or instrumental rendered as a manner adverb or an adjective,
flipping the direction of the sentence. `kho na las` ("only from") becoming "alone" is the textbook
case. *Diagnostic:* back-construal.

**6. Metrical inversion.** Word order bent to land a beat. See failure 14.

**7. Filler beat.** "truly", "indeed", "all", "so", "O", a doubled adjective, inserted to fill a
measure the content does not reach. *Fix:* drop the measure by one for the whole stanza.

**8. Sag.** Four or more unstressed syllables in a row, or a second run of three; the line loses
its pulse. *Fix:* replace a function-word chain with a content word, or re-break the line.

**9. Term-collision fudge.** A bound technical term quietly swapped for a shorter word because the
line would not otherwise hold. *Fix:* guidelines §8 order of preference; note any surviving swap.

**10. Silent doubt.** A construal that could have gone the other way, made and not recorded.

---

## English

**11. Dead collocation.** Two words that are each correct and that English never puts together.
*veils made clean* — veils are lifted, torn, or removed; obscurations are purified, dispelled,
cleared. *merit heaped*, *blessing inserted*, *wisdom conducted*: same failure.
*Diagnostic:* would a competent English writer, translating nothing, ever write this pair?
*Fix:* find the verb English actually uses with that noun, then re-measure if the beat count moved.

**12. Calqued idiom.** A Tibetan image rendered literally into an English phrase that carries no
meaning here. *the marrow of the heart of the victors of the three times*: accurate, and not
English. Nobody says *marrow of the heart*.
*Fix:* use the English expression with the same force — *the very heart of*, *the lifeblood of*,
*the innermost heart of*, *the quintessence of* — and note the image you let go. Keep a source
image only where English can carry it unexplained.

**13. Opaque line.** Grammatical, accurate, and it communicates nothing: the reader cannot say what
is being claimed. *The heart's own meaning holds no view of words.*
*Diagnostic:* read the line once and state its claim. If you cannot, it fails, no matter how
faithful it is. *Fix:* make the assertion explicit — *For the quintessential meaning there is no
view expressed by words.*

**14. Inversion.** Verb before subject, fronted object, postposed adjective — almost always to land
a beat. *The one from whom spring all the qualities.*
*Fix:* *the one from whom all qualities arise.* Then re-measure. Meter is the thing that gives, not
the syntax.

**15. Coerced stress.** The line reaches its measure only by putting a beat where English does not
put one, or by moving a word's lexical stress. Almost always an object pronoun after an imperative
verb, because that is exactly where an iambic reading wants an ictus.

> *bless me to realize the dharmakāya* read as a pentameter puts the beat on *me* and drags
> *realize* onto its second syllable. English says **BLESS** me to **RE**alize the dharma**KĀ**ya:
> three beats.

*Diagnostic:* the flat read — say the line in a plain non-metrical voice and mark the stresses; and
`beats.py`, which counts only what the language gives. A claimed measure above the tool's low count,
with the difference landing on function words, is coerced.
*Fix:* rewrite the line, or re-measure the stanza to the count the language actually gives. Never
re-scan the line to make it fit. See the worked repair below.

**16. Flattened relation.** A grammatical relation dissolved into a comma, an "and", or a bare
sequence. The Tibetan says *through this, that*; the English says *this happens. That happens.* A
cause becomes a coincidence; a condition becomes a chronology.
*Diagnostic:* walk the relation tags from guidelines §3.3 and check each one is still visible in
the English. `las`, `pas`, and `pa'i` are three different relations and must not converge on the
same English comma. *Fix:* restore the connective, even at the cost of a beat or an extra line.

---

## Coerced stress, worked

A drafted supplication, claimed as iambic pentameter:

```
Grant me your blessing in dharmata's state.
This wholly pure mind, from the first unborn:
bless me to realize the dharmakaya,
the one that lies beyond the thinking mind.
```

Flat-read, the stanza gives 4 / 4 / **3** / 4. The pentameter exists only if *me* takes a beat in
line 3 and *realize* is pulled onto its second syllable. Line 2 is also inverted (*from the first
unborn*), which is failure 14 arriving for the same reason: the measure was leading.

Repaired at the count the language actually gives, band 3–4:

```
Grant me your blessing in the state of dharmata.     4
This mind, unborn, is pure from the beginning.       4
Bless me to realize the dharmakaya,                  3
that lies beyond the thinking mind.                  4
```

Nothing is re-scanned. Line 3 keeps its natural three beats and the band absorbs it, which is what
the one-line tolerance and the citation band are for. The inversion in line 2 is gone because the
line no longer has to reach a fixed five.

---

## Worked example

**Tibetan** (four padas, seven syllables each):

```
སྙིང་པོའི་དོན་ལ་ཚིག་གི་ལྟ་བ་མེད། །      snying po'i don la tshig gi lta ba med
བརྗོད་བྲལ་ལྷན་ཅིག་སྐྱེས་པའི་ཡེ་ཤེས་འདི། །   brjod bral lhan cig skyes pa'i ye shes 'di
ཚོགས་བསགས་སྒྲིབ་པ་དག་པའི་ལག་རྗེས་དང་། །  tshogs bsags sgrib pa dag pa'i lag rjes dang
རྟོགས་ལྡན་བླ་མའི་བྱིན་རླབས་ཁོ་ན་ལས། །     rtogs ldan bla ma'i byin rlabs kho na las
```

**Construal.** Pada 1 is one sentence. Padas 2–4 are a second, with the verb of arising elided
after the final `las`. "For the quintessential meaning there is no view made of words. This
inexpressible coemergent wisdom [arises] only from the imprint of gathering the accumulations and
purifying the obscurations, and from the blessing of a realized guru."

**Relations:** `la` (pada 1) goal or locus, "for / in" · `pa'i` (pada 3) modification, not a second
clause · `dang` list continuation, the two sources are coordinate · `kho na` restrictive, "only" ·
`las` ablative, source. The whole of padas 3–4 stands in a *source* relation to the subject in
pada 2. Losing that relation is the failure that matters most here.

### First attempt, and why every line of it fails

```
The heart's own meaning has no view of words.
This coemergent one, beyond all speech,
primordial awareness, comes alone.
```

- **Vanishing predicate (2).** Padas 3 and 4 — accumulation, purification, the imprint, the
  realized guru, the blessing — gone.
- **Lines < padas.** Four padas, three lines.
- **Scattered head (1)** and **stranded subject (3)**: `ye shes` arrives in line 3, after the
  reader has parsed "This coemergent one" as complete.
- **Reversed causation (5).** `kho na las`, "only from", became "comes alone": a source turned into
  a solitude.
- **Opaque line (13).** "The heart's own meaning has no view of words" does not state a claim.

### Second attempt, still failing

```
The heart's own meaning holds no view of words.
This coemergent wisdom, past all speech,
comes only from the mark of merit gathered,
from veils made clean, from a realized master's blessing.
```

Complete, correctly measured at 4–5 beats, and still not publishable: **veils made clean** is a
dead collocation (11) and line 1 is still opaque (13). Passing the structural gates is not enough.

### The rendering that works

Six English lines for four padas, citation mode, roughly 3–4 beats, order 1-2-3-4.

```
For the quintessential meaning
There is no view expressed by words.
This innate wisdom, inexpressible,
comes only through the gathering of merit,
from purifying obscurations,
and from a realized master's blessings.
```

What it gets right and the earlier attempts did not:

- **Every phrase is English.** *gathering of merit*, *purifying obscurations*, *master's blessings*
  are the collocations English uses.
- **Each line is a unit of sense.** Line 1 is a frame; line 2 the assertion; line 3 the subject;
  lines 4–6 three coordinate sources, one per line. The sentence spans four lines and the point is
  never split.
- **The relations survive.** *For* carries `la`; *comes only through / from / and from* carries the
  restrictive `kho na` and the ablative `las` across all three sources, so the causal structure of
  padas 3–4 is visible rather than flattened into apposition.
- **It unpacks rather than compresses.** Six lines for four padas: the coordinate sources each get
  their own line instead of being crushed into one.
- **The measure gives.** The beat counts are not uniform to the letter, and that is the correct
  trade: idiom first, count second.

`Alt:` `lag rjes` (imprint, handprint, the trace left behind) is carried here by "through the
gathering / from purifying" rather than by a noun. To keep it: *comes only through the imprint left
by gathered merit*. `Q:` pada 1 can also read "words afford no view of the quintessential meaning".

---

## Idiom, worked

```
དུས་གསུམ་རྒྱལ་བའི་ཐུགས་ཀྱི་ཉིང་ཁུ་ཡིན། །   dus gsum rgyal ba'i thugs kyi nying khu yin
```

*This is the heart's own marrow of the victors of three times* — accurate, and not English.
`thugs kyi nying khu` is "the essence of the enlightened mind", and English already has expressions
that do exactly that work:

```
This is the very heart of the victors of the three times.
This is the lifeblood of the buddhas of past, present, and future.
This is the innermost heart of every victor of the three times.
```

`Issue:` the marrow image is let go; English has no *marrow of the heart* idiom, and keeping it
costs the reader the sentence.

---

## Permutation, worked

Constructed for the illustration. Tibetan order is condition then result, with the verb at the end:

```
བླ་མའི་བྱིན་རླབས་སྙིང་ལ་ཞུགས་པའི་ཚེ། །   bla ma'i byin rlabs snying la zhugs pa'i tshe
རང་སེམས་ཆོས་སྐུར་ངོ་ཤེས་འཆར་བར་འགྱུར། །  rang sems chos skur ngo shes 'char bar 'gyur
```

Held in Tibetan order the English strands the subject behind its modifiers. Order 2-1 lets the
predicate lead, where English wants it:

```
Your own mind dawns, and you know it as dharmakaya,
the hour the master's blessing enters your heart.
```

`pa'i tshe` is a temporal condition and *the hour* keeps it as one; rendering it as a bare "and"
would flatten the relation (15). Do not permute when the sequence is itself the content — an
enumeration, a narrative, a chain of reasoning, or a closing aspiration whose force depends on
standing last.
