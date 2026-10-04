# The construal: sketch by default, full object when contested

Pipeline v2 (SKILL.md §3) asks for a **construal sketch** of 8–15 lines per unit: `SPINE`,
`RELATIONS`, `NEG/QUANT`, `TERMS`, `DOUBTS`, plus `GROUNDING` and `VAR` after Pass 2. The full
object below is for a **contested unit**: a head-noun fork, an elided agent in a loaded passage, a
period whose syntax you cannot settle, or a unit the user asks you to construe in full. It is
working material in `<work>.construal.md`, read by the check and the grounding pass, never shipped.
Measured 2026-10-03/04: a 40-line construal for every unit did not make the translation more
faithful than the model's own reading; the sketch records the same decisions at a tenth of the
length.

## 1. Schema (full object; the sketch uses the starred fields)

```
UNIT      * <id>                e.g. 1.3/12, or "stanza 4", or a file + line range
FORM        verse | prose | mixed      verse: padas × syllables (7×4, 9×4 …); citation? (zhes/ces … las frame)
GENRE       pith instruction | exposition | debate | liturgy | song/dohā | narrative | colophon | framing
REGISTER    <one line>          who speaks to whom, at what temperature (modes.md §2)
SOURCE      <padas or sentences, Wylie, numbered>
WORDS       <from tibdict annotate: the senses you are taking; only the non-obvious ones>
SPINE     * <who does what to whom, finite verb by finite verb; what is elided and filled from where>
CLAUSES     <n>  verb=<stem> class=<tr/intr, vol/invol> frame=<ERG agent / ABS object / LA-DON role>
            tense/mood=<…> hon=<plain/hon>  elided=<what, filled from where>
RELATIONS * <n>  <particle> = <relation>     las=source · pas=cause · pa'i=modification · gis=agent/means
                                             na=condition · phyir=purpose/cause · kyang=concession
                                             nas/te=sequence · dang=coordination · la=goal/locus/purpose
NEG/QUANT * <negations with scope; restrictives (only, merely); quantifiers (all, without exception)>
VERSE-NOTES <filler particles (ni, yang, dag, rnams, extra pa/ba for the count); elided case markers;
             devices to keep in position (anaphora, enumeration, simile, climactic close)>
CONSTRUAL   <plain English prose, relations spelled out in full, no elevation, no compression>
TERMS     * <wylie> = <bound English>     from the glossary; decided here, with stress shape if verse
CITATION    <quoted work, opening words; dm.py identify result: Toh, segmentnr, src_link>
GROUNDING * <commentary glosses found by dm.py explore / segment: work, Toh or segment id, what it says, followed or not; or "none found">
VAR       * <readings from dm.py parallels that change the sense>
DOUBTS    * Q: <one line per construal that could go another way, with the alternative; resolved by grammar / by <commentary> / open>
```

## 2. Procedure

1. **Segment and count.** Shad `།` ends a pada; double shad a stanza; in many editions the shad
   after a syllable ending in `ག` is dropped, so count syllables, not marks. 7/9/11/15 are the
   normal verse measures; an unequal count is prose or a dohā-type free line.
2. **The dictionary tool is on demand** (`tibdict.py lookup <word> --full --examples` for a word you
   cannot settle; `annotate` on the whole unit only when you cannot parse it). If you use it, read
   §2a first and correct the segmenter by eye; the dictionary is an aid, the grammar decides.
3. **Find the verb first.** Tibetan is verb-final; one sentence often runs across two, three or four
   padas with the finite verb only at the end. Read the padas of a stanza backwards the first time:
   final verb, then its agent, object, modifiers. Common finite endings: `yin/red` (is), `yod/med`,
   `'gyur` (becomes), `'byung` (arises), `mdzad` (hon. does), `so/do/ngo/bo` (closing particles),
   `shog / gyur cig` (may it be). Padas 1–3 may have no verb at all.
4. **Assign the case frame** from the verb's class (`tibdict verb <stem>` gives Hackett's frame):
   ergative `gis/kyis` = agent of a transitive verb, or means, or cause; absolutive = object or
   intransitive subject; `la don` (`la na tu du ru su r`) = recipient, locus, goal, or purpose.
   Tournadre's warning: the same particle is transcategorial (case marker and clause connector), so
   decide its function from the clause, not from the form.
5. **Tag every relation** (table above). This is where meaning leaks: a cause rendered as a
   sequence turns an argument into a coincidence.
6. **Negation and scope.** `mi` (present/future), `ma` (past, prohibitive), `med` (there is no,
   without), `min` (is not), `bral` (free of). Double negation is often affirmative rhetoric and
   usually stays double. Note what the negation scopes over inside a nominalized clause.
7. **The items that leak** — check each: restrictives (`kho na`, `'ba' zhig`, `tsam`); quantifiers
   (`kun`, `thams cad`, `ma lus`, `so so`, `rnams/dag`, numbered enumerations `sku gsum`); emphatics
   (`nyid`); topic `ni` (tells you the subject, is not translated); honorifics; mood (`shog`,
   `gyur cig`, `cig/shig/zhig`, `mdzod`, `gsol`); vocatives (`kye`, a name in address); tense stems
   (`byed/byas/bya/byos`).
8. **Verse-specific.** Particles are dropped *metri causa*: a missing genitive or agentive is often
   still operative; reconstruct it and note it if load-bearing. Short forms (`yi`, `'i`, `ru`, `su`)
   are for the count. Filler (`ni`, `yang`, `dag`, extra `pa`) is not emphasis. Anaphora across
   padas, enumeration, and a climactic final pada are positional content.
9. **Citations.** A `zhes/ces/shes … las`, `… las kyang`, `… gsungs pa ltar` frame names or implies
   a work; `X na re` a person; the citing author often abbreviates the title (`gur`, `sdud pa`,
   `spyod 'jug`). Run `dm.py identify` on the quoted words, not on the title. Record the Toh and
   segmentnr. Where the parallels show a different reading (`gti mug` for `ma rig`, `'gyur` for
   `mngon`), record it in VARIANTS and decide which reading the citing text has.
10. **Construe in plain prose**, then **ledger the doubts**. A stated doubt is usable by the
    translator; a smoothed-over one is a defect that reaches print. A fork on the **head noun of
    the period** (apposition vs genitive: `bstan bcos … gsum du bstan pa'i snying po`, "the
    treatise, the essence" vs "the essence of the treatise"; which noun a long relative clause
    modifies; who the elided subject of a nominalized verb is) is always a `Q:`, even when one
    reading looks clearly better. When the two branches of a recorded fork are close, the
    grammar decides, not the smoother English: a `nas` sequence stays a sequence ("having seen
    fit vessels, you bring them into bodhicitta", not "who have entered bodhicitta"); an `X par`
    / `X du` phrase before a verb is adverbial by default (`rigs par rnal 'byor du byed pa` =
    practise yoga properly, not "apply oneself to what is proper"); an agent named twice in one
    clause (`yo gis … blo dang ldan pas`) is one person restated, not two. A term is rendered at
    the level of specificity the Tibetan has (`kha zas rgyu 'thun` = the outflow of food, not
    "what it turns into"; `shes par mi rung` = untenable, not "cannot be understood"). A verbal
    noun + `bar byed` is causative (`skye bar byed` = begets, brings about birth; `'dod par byed`
    = makes desire / desires, with the object in the absolutive): read the case frame, not the
    nearest English auxiliary.

## 2a. Tool slips seen in testing (read every tibdict row critically; this is why the tool is on demand)

- botok absorbs a negation into a preceding token: `la ma gus pa` → "la ma" (lāmā) + "gus pa",
  which flips the polarity. The tool now splits `la ma`; watch for the same with `ma`/`mi` after
  other particles.
- The MITRA first sense can be the wrong sense for the context: `skyes pa` "man" where the text has
  "arisen"; `'dul ba` "vinaya" where it means "to tame"; `don` "Don (name)" where it means
  "meaning/purpose"; `thogs med` "unobstructed" where it is Asaṅga; `'debs` "plant" in `skur ba
  'debs` (disparage); `'don` "recite" in `bogs 'don` (enhance); `len pa`/`rnyed pa`/`'dzin pa` in
  their idioms (`nyams su len`, `mig rnyed`, `yongs su 'dzin`); `las` tagged as the ablative where
  it is karma; `zhing` tagged as a connective where it is "field"; the final particle `ro` glossed
  as "taste". Read all listed senses and the Hopkins/RY line; look the idiom up as a whole.
- botok splits multi-syllable names and terms (`phyag na rdo rje` → phyag + na + rdo rje; `mdo
  'gag` → sutra + cease; `a ma na se` → mother + Sera; `khong du chud pa` around `du`; `yang dag
  par` after `de`) and fuses an affix away from a word (`char` rain → `cha` + `r`; `las` karma →
  `la` + `s`), or merges two words (`sgra med dri med`, `sems las`). The `COMPOUND?` line, the
  `(or fused: …)` and `(or split: …)` notes now flag these; a Sanskrit transliteration (`a ma na
  se` = amanasi) has no entry and must be recognized by eye.
- `VERB-FORM?` lists every lemma a form could belong to (`thob` is also a form of `stob`); the
  paradigm in the MITRA line is the reliable one.
- The POS tag is botok's guess (`dka' ba`, `stong pa` tagged VERB; `mdzod` tagged NOUN); the
  dictionary line usually corrects it.
- A final `s`/`r` is shown as a separate particle row (`bkra ba` + `s` = `bkra bas`, cause); read
  it as the affix on the preceding word.

## 3. The construal is not the translation

It exists to be rendered, and the draft is written from it, not from the Tibetan word order. The
relation and negation fields are what the check tests; fill them from the Tibetan, never from a
machine translation (MITRA output is a cross-check that flattens relations), and let a commentary
gloss (Pass 2) settle a fork only through the grammar it implies.

## 4. Sizing

A sketch is 8–15 lines; a full object for a contested unit 25–40. If a sketch runs longer, you are
writing an essay; if it has no `DOUBTS` line on a loaded passage, you have smoothed a fork over. The
dictionary report, when there is one, is not copied in: only the senses you took and why.
