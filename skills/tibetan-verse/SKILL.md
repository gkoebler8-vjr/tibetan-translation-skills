---
name: tibetan-verse
description: Render Tibetan verse into English verse — sādhana, liturgy, prayer, aspiration, homage, dohā and song, and verse citations quoted inside prose — and check, fix, or re-metre an existing English rendering of Tibetan verse. Called by tibetan-translate for every verse unit (the analysis pass detects verse); usable alone when the construal is already in hand. Carries versification guidelines v4.1: one finished version taken through six gates; metred English in counted beats with one rhythmic kind per block, an audible pulse in every line (at most one slip per line, checked by beats.py) and a two-count band per block (chant mode isometric; one count aimed for when the padas are equal); natural stress never coerced; natural word order, idiom and collocation first; lines never fewer than content padas; free line order inside a sentence; bound terms held even at metrical cost. Derived from the finished Lam Zab verses. Not for Tibetan prose.
---

# Tibetan verse into English verse (guidelines v4.1)

## 0. Gate

Opus or Fable at maximum effort; otherwise stop and say so (tibetan-translate §0 applies).

## 1. What governs

`reference/guidelines.md` is the full spec and is binding, but this file carries everything a routine
stanza needs: read the guidelines before the first verse of a long job or when a question arises,
not for a single stanza. `reference/lz-practice.md` is where the spec comes from: the 135 finished Lam
Zab verse blocks, measured. `reference/failures.md` has the named failures and the worked examples;
read it when a draft feels wrong and you cannot say why.

The English standard is shared with prose: `~/.claude/skills/tibetan-translate/reference/english.md`.
The construal comes from tibetan-translate's analysis pass (`reference/analysis.md` there). If you
are called without one, build it first; never versify from the Tibetan word order.

**Priority order:** natural, clear, idiomatic English > content and its logic > one rhythmic kind
and a stable measure > line correspondence > sound. **The beat count is the rule that gives.**

## 2. Before drafting: mode, kind, measure

- **Mode.** *Chant* (to be recited: sādhana, liturgy, prayer): every line the same count. *Citation*
  (verse quoted in prose, dohā cited as evidence, verse in a translated book): a band of two
  adjacent counts, n / n+1; aim for one count when the padas are equal; a spread of three only
  with a single outlier line. Ceiling 7.
- **Kind.** Rising (iambic base; the English default, and what the Lam Zab verse is throughout) or
  falling (trochaic base; for incantatory 7-syllable material when it genuinely reads better). **One
  kind per block, never mixed.** An initial inversion, a feminine ending, an anapest mid-line are
  not a change of kind; a block that reads iambic, then trochaic, then iambic is a failure. **The
  pulse must be audible in every line**: one or two off-beats between beats; a clash or a run of
  three-plus off-beats is a slip, one per line at most, or the line is rewritten (`beats.py`
  `PULSE`). A line that reads as cadenced prose is not finished, however natural it is.
- **Measure.** Write the densest pada as one natural English line and count its beats on the flat
  read; that is the top of the band. 7-syllable padas usually land at 3–5 beats, 9 at 4–6, 11 at
  5–7. If an 11-syllable pada will not sit under 7, unpack it, or (house rule) set the block as long
  lines. An **enumerative run** (one deed or item per pada, as in the Uttaratantra's twelve deeds)
  wants the wider measure of its range so that each item keeps a finite verb or a full phrase; a
  3–4 beat band turns it into a flat list of gerunds.
- **Terms**, with their stress shapes, chosen now. *primordial awareness* (../..) will not sit in a
  short line; give it the line end or a longer measure. Repairing a line by swapping a bound term is
  a defect, not a fix.

Say mode, kind and measure in one line of the output.

## 3. The loop, per block

1. Construal in hand: spine (how many sentences, where each finite verb sits), relations tagged,
   speech act and controlling mood, devices to keep in position (anaphora, enumeration, simile,
   climactic close), filler particles marked.
2. **Prose first.** Write the natural English sentence(s). Then break into lines at the measure,
   adjusting wording only as far as the breaks require. Pada-first drafting produces stacked
   fragments and verbs that never arrive.
3. **Set the order.** Tibetan order by default. Permute inside one sentence only, and only to bring
   the predicate or the governing noun forward (2-1-3-4, 4-1-2-3); declare it (`order 4-1-2-3`).
   Never across a sentence boundary; never where position is content: anaphora, enumeration,
   narrative or logical sequence, a closing line that lands the point.
4. **Lines ≥ content padas.** Unpack a dense pada into two lines; give a list one line per item;
   fold only a frame-pada (`zhes dang`, an introducer) into the surrounding prose. Never compress.
5. **Line integrity.** Stop at every line end: a clause, a complete phrase, a frame, a list item,
   and nothing already read needs re-parsing when the next line arrives. Never break
   determiner/noun, preposition/object, auxiliary/verb, verb/short object. Subject and main verb in
   the same or adjacent lines. One appositive per sentence, inside a line.
6. **Run the gates** (§4). Revise until they pass. Never print with an apology attached.
7. **`beats.py`** on the finished block, in its mode:
   ```bash
   python3 ~/.claude/skills/tibetan-verse/tools/beats.py citation "line one," "line two,"
   ```
   It performs the flat read and reports each line's beat interval, PULSE/SAG/SLACK/CLASH/WEAK-END/OVER,
   the band verdict and a KIND? advisory. `PULSE` and WIDE fail the block: rewrite before printing.
   Gate 1 outranks the count, never the pulse: a line that cannot keep the pulse in natural English
   is re-worded until it does, and only when no natural wording exists does the count give. `UNKNOWN:<word>` →
   count the word by hand for this run and note it; add it to `tools/lexicon.py` as
   `"word": (syllables, [primary], [secondary])` afterwards, never during a measured run (the tool
   under test must not change mid-run).

## 4. The gates

1. **Read aloud** at speaking pace: no backtracking, no second pass.
2. **Idiom and collocation**: would an English writer write this pair, this image?
3. **Clarity**: say what each line claims.
4. **Logic**: every tagged relation still visible (`las` from, `pas` because, `na` if, `kyang`
   although, `phyir` to/because). None became a comma or "and".
5. **Completeness**: walk the construal; lines ≥ content padas; back-construe.
6. **Measure**: the **flat read** first (say each line in a plain voice; where the stress fell is
   the count; *BLESS me*, never *bless ME*; *RE-alize*, never *re-a-LIZE*; prepositions, articles,
   auxiliaries and object pronouns carry no beat; the line end promotes nothing); then the mode's
   band, one kind, the ceiling, and the **pulse**: tap the kind's rhythm while reading; every beat
   lands on a tap; at most one slip (a clash, or three-plus off-beats between beats) per line.
   Two slips: rewrite the line, keeping the words that carry the sense and moving the rest. A
   run of four unstressed syllables is a sag; one spondee per line is fine.

**No inversion, ever.** If the count then breaks, the count is what changes.

## 5. What flexes and what does not (from the finished Lam Zab verses)

Flexes: line length inside the band (a dense pada takes a 6-beat line rather than two 3-beat
lines when the sentence would otherwise break badly; a thin pada stays short); feet (anapests,
feminine endings on every Sanskrit term, dactylic words absorbed by the next rising foot); lines
per pada; order, sparingly; prose setting for 11-syllable padas under a house rule.

Does not give: the bound term (*ye shes* = primordial awareness in all ~25 Lam Zab verse
occurrences, even where it costs the metre); natural word order; the relation particles; the
quantifiers, restrictives, interjections, honorific address; the speech act (homage stays homage,
instruction stays imperative, a rhetorical question stays a question).

House style settles: line-initial capitals (Lam Zab: yes), contractions (Lam Zab: ordinary ones
allowed in instruction and song, not in homage), em dashes (Lam Zab: allowed), rhyme (never sought).

## 6. Output

1. One line, merged into tibetan-translate's header when called from it: `Citation mode, rising,
   4–5 beats. Padas 9 × 4, five English lines, order 1-2-3-4.`
2. **One finished version.** A second only for a genuine fork (two defensible construals; term vs
   idiom; chant vs citation setting), both finished, one line on the choice.
3. Notes, one line each, only where needed: `Q:` · `Alt:` · `Issue:` (term swap, unpack, image let
   go, prose setting).

Never print scansion, stress marks or gate working in the verse or the reply unless asked.
Long pieces: one mode, kind and measure across the piece; stanza by stanza; whole piece unless
chunking is requested.

## 7. Project bindings

A glossary, terminology list or house style binds and overrides the defaults here. For the Lam
Zab practitioner edition the pass-B files (`02_Prompts/prompt_verse.md`, `LZ_Workflow_B_verse.md`)
still describe that pipeline's docx handling and five-version stack; its *metrical* practice is
what this spec now codifies, so a Lam Zab verse checked against v4 should pass.
