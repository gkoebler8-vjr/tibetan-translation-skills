# Pass 5 — notes for the editing translator, footnotes for the reader

Two streams with different readers. Editor notes are working material: every doubt, alternative,
commentary and tool flag the revising translator needs, terse, in the `NOTES:` block of each unit.
Footnotes are part of the edition: written for the reader, in the body's voice, only where the
audience's notes policy allows, in the `FOOTNOTES:` block. Nothing from the editor stream leaks
into a footnote unrewritten; nothing a reader needs is left only in the editor stream.

## 1. Editor notes (`NOTES:`), every unit

One line each, only where there is something to say, otherwise `none`:

| Tag | What it carries | Example |
|---|---|---|
| `Q:` | a construal that could go another way, with the alternative, and whether grounding resolved it | `Q: de yang = he too (subject) or him too (object); plain reading taken; Padmāvatī silent.` |
| `Alt:` | a hard word or line with the rendering not taken | `Alt: 'jig rten mkhyen "knows the world" / "knows beings".` |
| `Comm:` | what a commentary says where it differs from the body or from another commentary, with work and locator | `Comm: Toh 4025, 118b: 'jig rten mkhyen = ji snyed pa mkhyen pa; followed. KHEZ009:4568 (rin po che'i sgron me) same.` |
| `Var:` | a variant reading that changes the sense, from `parallels` | `Var: Sahajasiddhi (MW1PD95844:2571) reads min for yin in line 2, flipping the sense; the commentary's yin translated.` |
| `Source:` | the identification result | `Source: Toh 4024, Uttaratantra I.?; verbatim; quoted also in Toh 4025.` · `Source: not located.` |
| `MITRA:` | the flag, kept or changed with the reason | `MITRA: differs at clause 3 (reads rigs par as object); kept, adverbial by position.` |
| `Issue:` | a term swap, an unpack, an image let go, a register shift, a speech-act conversion | `Issue: enumeration rendered as "you" imperatives (instruction register).` |
| `Prior:` | what an existing published translation reads where it differs, whether it was followed or adapted, under which policy (`existing-translations.md`) | `Prior: Staron 2015 reads the sons as the slain; kept mine (plain reading); consult-only brief.` |
| `Conf:` | the unit's confidence grade and its reason (§1b) | `Conf: low — agent of 'dod par byed open after grounding; MITRA differs.` |
| `Check:` | what the in-context check found and changed | `Check: in-context, 1 fixed (pas → because).` |

Editor notes carry Wylie, segment ids and Toh numbers freely. They are never shipped to the reader.

## 1b. Confidence grade, per unit

So the reviser knows where to look first, every unit's header carries `confidence: high | medium |
low | very low` and the `Conf:` note gives the reason. Grade from the facts of the unit, not from
how the English feels:

| Grade | When |
|---|---|
| **high** | no open `Q:` on a content word, agent, relation or referent; grounding found or not needed; MITRA agrees or differs only in phrasing; check found nothing or only register |
| **medium** | one open `Q:` on a term or nuance, or MITRA differs on a content word and the grammar settled it, or a commentary differs and the plain reading was kept |
| **low** | a fork on an agent, relation, head noun or referent is still open after grounding; or the check changed a relation; or a bound term has no attested sense here |
| **very low** | two or more such open forks; or a suspected corruption or a variant that flips the sense; or the unit could not be parsed with confidence and was rendered on the most plausible reading |

The document export shades low units orange and very-low units red and prints the reason in the
header line, so a reviser can go straight to them.

## 2. Footnotes (`FOOTNOTES:`), by audience

The notes policy of the brief overrides this table.

| | Academic | Hybrid | Seasoned practitioner | New practitioner | Working crib / recitation |
|---|---|---|---|---|---|
| **Locators** (Toh, folio, witness) | in the footnote | in an endnote | never in a footnote: the sources register, keyed by opening words | never | none |
| **Commentary readings** | the gloss quoted or paraphrased, with the commentary's title, Toh and folio; disagreements between commentaries stated | the reading followed, with the work named; disagreements in an endnote | the explanation in plain English where it unlocks the passage or matters to practice; the commentary named by its English short title only if the reader would know it; no folios | only when the passage is otherwise unreadable; one sentence, no titles | none |
| **Variants** | stated, with witnesses | endnote | only when the variant changes what the practitioner would do | never | none |
| **Sanskrit / Wylie** | IAST, Wylie of the term glossed | IAST in the note only | none, unless the term itself is the point | none | none |
| **Enumerations, names, images** | footnote | footnote | footnote: the four maras listed, who a name is, one opaque image unpacked | footnote, one sentence | none |
| **Translation choices** | a note where a bound term departs from the common rendering | endnote | never (editor stream) | never | none |
| **Length** | as needed | ≤ 3 sentences | ≤ 3 sentences | 1 sentence | — |
| **Voice** | neutral-scholarly | body voice | body voice: warm, direct; no hedging, no "lit." | body voice | — |

Rules that hold in every mode:

1. A footnote is **anchored to a word or phrase of the rendering**; write it as `FN(<anchor>): …`.
2. A footnote that reports a **commentary's reading or a variant** is written from the Tibetan of
   the hit you read, never from the machine rendering beside it and never from memory. A footnote
   that supplies a **standard enumeration or identification** (the four maras listed, the five
   certainties, who an epithet names) may come from standard reference knowledge when no grounding
   call covers it; mark it `[standard]` in the editor's `Issue:` line so the reviser can check it.
3. It explains **this passage**, not the topic: a footnote on *dharmakaya* in a homage is not a
   lecture on the three bodies.
4. A footnote never carries a doubt the body silently resolved: if the reader would read the
   passage differently with the alternative, the alternative is in the footnote (academic, hybrid,
   seasoned where it matters to practice) or the body keeps the plain reading and the `Q:` goes to
   the editor.
5. Nothing in a footnote that the text you translate does not occasion; nothing in the body that
   belongs in a footnote (no explanatory expansion of the rendering).
6. Numbering is the editor's; the pipeline gives the anchor.

## 3. Triage of an existing apparatus

When the task is to re-edit an academic translation for a reader edition, tibetan-citations §2
applies: source locators go to the register, reader-relevant explanations are rewritten in the body
voice and kept, witness variants and secondary literature are cut and reported in the run log.

## 4. Output shape

Schematic; locators are placeholders, never to be copied:

```
### U0n
HEADER: U0n · verse citation, 7×4, metred 4-beat, block U0n–U0n+2 · homage · seasoned · Toh <root> (<English short title>), quoted in Toh <comm.> · grounding: <commentary> gloss followed
TEXT:
<rendering>
FOOTNOTES:
FN(<anchor phrase>): <one to three sentences in the body voice, from the Tibetan of the gloss you read>
NOTES:
Source: Toh <root>, verbatim (<segment>); quoted also in <work> (<segment>).
Comm: <work> (<segment>) glosses <wylie> as <reading>; followed. <other work> same / differs: <reading>.
Q: <fork>; <branch taken>; resolved by <work> / open.
MITRA: differs at clause <n> (<what>); kept (<grammatical reason>).
Check: in-context, <n> fixed.
```
