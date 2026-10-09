# Existing English translations: when to use them, how to attribute them

Dharmamitra's index holds aligned English translations of many texts (segment ids beginning `EN_`:
84000, Edition Garchen Stiftung, Lotsawa House and others), and `dm.py gloss` returns them beside
the commentaries, labelled. Using them well saves work and improves the result; using them without
regard to their terms is a legal and an ethical problem that attribution alone does not cure. The
brief decides; this file gives the rules and the mechanics.

## 1. What the law and the licences allow (the short version)

| Source | Terms | May consult and compare | May quote with attribution | May adapt into the body |
|---|---|---|---|---|
| 84000 Reading Room | CC BY-NC-ND 4.0 | yes | short passages, attributed, in a non-commercial work | **no**: ND forbids derivatives, attribution does not lift it |
| Lotsawa House | CC BY-NC 3.0/4.0 (check the text's own page) | yes | yes, attributed, non-commercial | yes for a non-commercial work, attributed; no for a commercial edition |
| Edition Garchen Stiftung, Padmakara, Shambhala, Wisdom, Snow Lion, LTWA, academic presses | all rights reserved | yes | short passages under fair use, attributed | **only with the publisher's or translator's permission**, recorded in the brief |
| The project's own earlier translations (the translator's, the group's) | yours | yes | yes | yes, attributed to the earlier edition |
| Public-domain or CC BY / CC BY-SA / CC0 translations | open | yes | yes | yes, attributed (SA: the new work shares alike) |

"Consult and compare" is always allowed: reading a published translation after you have drafted,
to see where it differs, is scholarship. Everything beyond that depends on the terms, and the
brief's **prior-translations policy** records what applies to this project:

```
Prior translations: adapt <sources> (permission/licence: …) · consult only · ignore
```

Default when the brief says nothing: **consult only**. In a measured test run: **ignore** (and
`dm.py gloss --no-en`), so the test stays blind.

## 2. The procedure

1. **Draft first.** Your own reading and draft (Pass 1) come before any existing translation is
   opened. A translation read before drafting shapes the construal; one read after is a witness.
2. **Collect.** The `EN_` hits of `gloss`, or `dm.py segment EN_<file>:<n> --context` for the
   aligned passage. Note which published translation it is: `dm.py cite EN_<file>:<n>` gives the
   translator, title, publisher, year, ISBN and the aligned segment (no page numbers are in the
   index; supply them from the printed edition when you cite).
3. **Compare, clause by clause**, as with MITRA: where the published translation differs on a
   content word, a referent, an agent or a relation, go back to the Tibetan and the grammar. A
   published translator may have read a commentary you have not: check with `gloss` on the
   clause before deciding. Record the outcome as a `Prior:` editor note: what the prior reads,
   whether you followed it, and why.
4. **Adapt only under the policy.** When the brief allows adaptation of this source, you may take
   its wording where it is better than yours, sentence by sentence, and the unit's header says
   `prior: adapted <translator year>`, the editor note lists the sentences taken, and the edition
   carries the attribution line `dm.py cite` prints (in the front matter, the sources register, or
   a footnote, as the house style says). Taking a whole page unchanged is not adaptation; it is
   reprinting, and needs the publisher's agreement in writing.
5. **Under "consult only"**, nothing from the prior translation enters the body except through your
   own re-reading of the Tibetan: if the prior convinced you of a reading, you re-express it. A
   bound term the project already uses is yours; a felicitous phrase of the prior translator's is
   not. The `Prior:` note still records the comparison, and a footnote may say "X reads …" where the
   audience's notes policy allows (academic: always with the full citation).
6. **Under "ignore"** (tests), the hit is neither read nor cited; log the exposure.

## 3. Attribution formats

`dm.py cite` prints them from Dharmamitra's catalogue fields (never from its AI-generated overview,
which `dm.py meta` omits unless `--overview`):

- **Academic:** `Gabriele Staron, trans., *Rays of Sunlight: A Commentary on The Heart of the
  Mahayana Teachings*, by Ayang Thubten Rinpoche, Edition Garchen Stiftung (2015), ISBN …, p. N.`
  (the page from the printed edition; the index gives only the aligned segment).
- **Reader edition:** in the front matter or the sources register: `Passages marked † follow /
  are adapted from Gabriele Staron's translation, *Rays of Sunlight*, Edition Garchen Stiftung
  (2015), with permission.` A footnote only where a single passage is taken.
- **Canonical texts quoted:** `*Title* (wylie), Toh N, Degé Kangyur, section, vol. X, f. Yb` from
  `dm.py cite <segment>`; the segment number is Dharmamitra's position within the folio, not the
  Derge line.

## 4. Editor notes and header values

- Header: `prior: none` · `prior: consulted (<translator year>)` · `prior: adapted (<translator year>)`.
- `Prior:` note: `Prior: Staron 2015 reads "…" for X; differs on the agent; kept mine (ergative on
  Y).` or `Prior: Staron 2015 followed for the enumeration wording (adapted, brief permits).`
- Register row (tibetan-citations) for every adapted source, once per text, with the attribution
  line.
