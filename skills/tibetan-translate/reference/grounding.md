# Pass 2 — grounding the reading in the tradition's commentaries

A translation that follows the grammar and the dictionary alone is a reading; one that follows
the commentators who glossed the same words is a reading the tradition recognizes. Dharmamitra's
index holds the Kangyur, the Tengyur, the Nyingma Kama and Terma, the Sakya collections, the ACIP
sungbums, the Tsadra series and more, and its primary search finds the passages that quote or
explain the words you are translating. This pass uses it to do three things: translate according
to the commentaries where they settle a reading, tell the editing translator where they disagree,
and give the reader a footnote where the commentary unlocks the passage.

On Dharmamitra's terms (5 October 2026, tibetan-dharmamitra §1): the semantic search is light, the
Explore summaries and the re-ranking are what drive their compute. So the grounding tool is
`dm.py gloss`, the primary search without re-ranking and without a summary; `dm.py explore --summary`
exists only for a user who asks for Explore's summary by name. Every output names the resource it
used, and the unit header's `grounding:` field repeats it.

## 1. The tools, in the order you reach for them

```bash
DM=~/.claude/skills/tibetan-translate/tools/dm.py
python3 $DM gloss    "<key clause or line, Wylie>" --context 8   # the works that carry these words, labelled GLOSS | QUOTE | NEAR, the gloss read in context
python3 $DM segment  <segmentnr> --context --window 8       # read on where a gloss runs further
python3 $DM parallels <segmentnr>                           # variant readings of a canonical line
python3 $DM identify "<quoted words>" [--exclude <Toh>]     # source of a quotation (tibetan-citations)
```

**`gloss`** posts the query to DharmaMitra's primary search (semantic, Tibetan sources, no
re-ranking, no summary), groups the hits by work and prints one block per work: title, collection,
segment id (`BO_T06_D4025:118b-31` = Tengyur, Toh 4025, folio 118b; `BO_S10_…`, `BO_TSD_…`,
`BO_ACIP-SUNGBUM_…`, `BO_EGS_…` = sungbum and series texts; `BO_K12_D0431` = Kangyur, Toh 431), a
label, and the hit's Tibetan in Wylie. **GLOSS**: the hit or its neighbours take the query's words up
with gloss scaffolding (`zhes pa ni`, `zhes bya ba ni`, `ces pa ni`, `zhes pa'i don`, `… ni … ste`,
`… la bya`), or a commentary on the root work restates them in a paraphrase with the root words
woven into its prose. **QUOTE**: a verbatim run of 12 or more syllables (the whole query when it is
shorter). **NEAR**: a semantic neighbour, not grounding. Order: GLOSS first, then Tengyur, then
sungbum and series, then the rest; twelve works. The first line names the resource; a `root work`
line names the Kangyur/Tengyur text that carries the line verbatim, when there is one.

**`--context 8`** adds one DharmaNexus text-view request (two when the hit sits at the end of its
100-segment page) for each of the five works most likely to gloss the line: GLOSS hits first, then
commentaries whose title names the root work, then other commentary-titled works that quote it. It
scans forward from the quotation for the gloss and prints the hit segment (`>>`), the gloss segment
(`GL`) and eight segments after it, so one call reads the gloss. A commentary that quotes sixteen
padas and then glosses them puts the gloss twenty or more segments after the hit: this is why the
scan looks forward instead of taking a window around the hit. Where nothing is found, the block says
so and names the segment from which `segment --context` reads on. Query with the **words that carry
the doubt**: the clause whose agent, relation or term is in question, 10–25 syllables, in Wylie. A
whole stanza returns the same commentaries less precisely. Two to four calls a page is the budget
(2–3k tokens a call, ~4k with `--context 8`); more than that means you are querying units that are
not in doubt.

**No machine rendering is printed.** You read the Tibetan of the hit and of the gloss; the labels
are a sorting aid computed from the wording (a run of the query's syllables before a scaffold, or
the query's content words in order inside a longer stretch), and they can be wrong in both
directions: a NEAR hit can be a gloss that uses other words, a GLOSS hit a formula shared with
another passage. Read before you cite.

**`segment --context`** when the gloss runs past the printed segments (the window default is 6
segments each side; 8–15 reaches the end of a long gloss). **`parallels`** on a canonical segment
lists the other witnesses of the line with their wording; a variant that changes the sense (`gti
mug` for `ma rig`, `min` for `yin`) goes into the sketch's `VAR` line and, in academic mode, into a
footnote.

`dm.py search` is the same primary search printed one hit per line, ungrouped; `gloss` replaces it
in this pass. `dm.py explore --summary` (Explore's re-ranked hits and Gemini summary) is not part of
the pipeline: only when the user asks for Explore's summary by name, and then the header says
`grounding: DM Explore summary`.

**Existing English translations among the hits** (`EN_` segment ids; `gloss` labels them). They
are not grounding (a translation is not a gloss), and they are handled by the brief's
prior-translations policy and `reference/existing-translations.md`: consulted after drafting as a
witness, adapted only where the licence or a permission allows, always cited (`dm.py cite
EN_<file>:<n>`), never read before Pass 1. In a blind test run use `gloss --no-en`. The text you
are translating can also appear among the hits (`--exclude-file <its prefix>` hides it;
`identify --exclude` takes a Toh number or a segment prefix).

**What is queried, and what is not.** Citations and root-text lines, always. In the author's own
prose, a technical term, formula or enumeration (`nges pa lnga`, `bdud bzhi`, `rtag chad kyi
mtha'`): query the term, not the sentence. The author's plain prose is **not queried**; its header
says `grounding: not queried`. Save each output as `dm_gloss_<unit>.txt` (`dm_<command>_<unit>.txt`
for the others) in the run directory.

## 2. What counts as a gloss, and what you do with it

A **gloss** is a passage in another work that takes up the words you are translating and explains
them: the scaffold `… zhes pa ni … ste`, `… zhes bya ba ni …`, `… ni … la bya`, a paraphrase that
restates the line with the elided arguments filled in (the root words woven into the commentary's
prose: `'jig rten gyi khams ji snyed pa mkhyen pa'i ye shes kyis … 'jig rten ma lus pa kun la legs
par gzigs nas ni …`, the common form in a `rnam bshad` of a root text), or an enumeration that
spells out a term (`sku gsum ni …`). A **quotation** is a work citing the line without explaining it; it is a witness
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

## 3. Patterns, and one real call

- **A root-text citation in a commentary.** `identify` on the quoted words gives the root (Kangyur
  or Tengyur, with Toh) and the works that quote it. `gloss --context 8` on the padas in doubt
  returns the quoting works as QUOTE and the root's own commentaries as GLOSS with their gloss
  printed; where the gloss runs on, `segment <id> --context --window 8–12`. Where an epithet-like
  phrase (`'jig rten mkhyen`) is glossed as a technical knowledge or activity, the body follows the
  gloss and a seasoned-practitioner footnote says so in one sentence; an academic footnote adds the
  commentary and folio.
- **A tantra's prose with an elided agent.** `gloss` on the clause returns the root and later
  quotations; the tantra's Tengyur commentary, if indexed, is the gloss to read (`--context`, or
  `segment --context`). If it names the agent, follow it; if it does not, the plain grammatical
  reading stands and the fork stays a `Q:`.
- **A commentary that is itself the text.** `identify --exclude <its Toh>` on its quotations finds
  their sources; `gloss --exclude-file <its prefix>` on its own glosses finds the parallel
  commentaries on the same root words, which is where a disputed sense of a term is settled or
  shown to be disputed. Its own copy, and any aligned English, will appear among the hits: skip them.
- **The author's own prose.** A formula or enumeration in it (`bdud bzhi`, `nges pa lnga`) is
  queried as a term; the sentence itself is not. `grounding: not queried`.

**The call, as run on 9 October 2026** (Uttaratantra II, the first two padas of the nirmāṇakāya
stanza, quoted in *Rays of Sunlight* U06; four GLOSS blocks came back, two shown, then the root):

```
python3 $DM gloss "thugs rje chen pos 'jig rten mkhyen/ 'jig rten kun la gzigs nas ni/" --context 8
```

```
DharmaMitra primary search · semantic · no re-ranking · 184 hits in 125 works
query (14 syllables): thugs rje chen pos 'jig rten mkhyen/ 'jig rten kun la gzigs nas ni/
root work (Kangyur/Tengyur hit with the verbatim line): theg pa chen po rgyud bla ma'i bstan bcos/ (mahāyānottaratantraśāstra) [Toh 4024]
(context: DharmaNexus text view, 10 request(s) for 5 work(s): theg pa chen po'i rgyud bla ma'i bstan …, theg pa chen po rgyud bla ma'i bstan bc…, rgyad bla ma'i rnam bshad phyir mi ldog…, theg pa chen po rgyud bla ma'i bstan bc…, rgyud bla ma'i 'grel pa phyir mi ldog p…; gloss found in 4)

=== rgyud bla ma'i 'grel pa phyir mi ldog pa seng ge'i nga ro/ · Tsadra series · BO_TSD_BO_DC_RDI-KK-07:3669 · GLOSS (paraphrase gloss)
la gnyis/ mchog gi sprul skus mdzad pa bcu gnyis ston tshul/ de'i byed las gdul bya rim gyis 'dren tshul lo/ dang po (mchog gi sprul skus mdzad pa bcu gnyis ston tshul )ni/ thugs rje chen pos 'jig rten mkhyen/ 'jig rten kun la gzigs nas ni/ chos kyi sku las ma g.yos par/ sprul pa'i rang bzhin sna tshogs kyis/
   3668: don de bzhin du gdul bya'i 'gro ba rnams kyi khams dang bsam pa dang mos pa la sogs pa'i rkyen sna tshogs pas thugs rje chen pos skye dgu la khyab pa'i bdag nyid rdzogs pa'i sangs rgyas rnams kyang sna tshogs pa de'i dngos po min yang kha dog dang tshad la sogs pa'i rnam par 'phrul bar snang ngo*/_
>> 3669: gsum pa sprul sku'i rnam gzhag la gnyis/_
   3670: mchog gi sprul skus mdzad pa bcu gnyis ston tshul/_
   … (21 segments)
   3692: mtha' yas pa'i sems can thams cad la bsam gyis mi khyab pa'i thugs rje chen pos rjes su bzung bar bzhed pa'i rgyu las so/_
   3693: tshul ji ltar ston na/_
GL 3694: 'jig rten gyi khams ji snyed pa mkhyen pa'i ye shes kyis gdul byar gyur pa'i 'jig rten ma lus pa kun la legs par gzigs nas ni ji lta ba mkhyen pa'i ye shes chos kyi sku 'gyur ba med pa'i ngang du mnyam par bzhag pa las nam yang ma g.yos par ro/_
   3695: don gang dag ston na/_
   3696: sprul pa'i rang bzhin rnam pa sna tshogs pa rnams kyis rmad du byung ba'i mdzad pa bcu gnyis yang dag par ston pa ste/_
   3697: de yang shAkya'i rgyal po lta bu la nye bar mtshon na bdag nyid chen po des mdzad pa'i gzhi thog mar dga' ldan pa'i lha'i skye ba dam pa tog dkar zhes bya bar mngon par skye ba'i tshul bstan nas lha'i tshogs rab tu mang po smin grol la bkod pa dang*/_
   3698: de nas mdzad pa bcu gnyis kyi dang po dga' ldan gyi gnas nas 'dzam bu'i gling du 'pho ba dang*/_
   3699: yum gyi lhums su 'jug pa dang*/_
   3700: lhums nas bltams pa dang*/_
   3701: bzo yi gnas la mkhas pa dang*/_
   3702: btsun mo'i 'khor gyi nang na dgyes par rol pa dang*/_

=== theg pa chen po rgyud bla ma'i bstan bcos kyi rnam par bshad pa nges … · Sungbum/series · BO_S03_PARCHIN-094:7547 · GLOSS (paraphrase gloss)
ul pa'i sku la/ mchog gi sprul skus mdzad pa bcu gnyis ston tshul dang*/ de yi byed las gdul bya rim gyis 'dren tshul lo/ de la mdzad pa bcu gnyis ston tshul ni/ thugs rje chen pos 'jig rten mkhyen/ 'jig rten kun la gzigs nas ni/ chos kyi sku las ma g.yos par/ sprul pa'i rang bzhin sna tshogs kyis/ skye ba mngon par skye ba dang*/
   7546: zhes pas so/
>> 7547: sprul
   7548: pa'i sku la/
   … (21 segments)
   7570: de yang rgyu gang las ston na/
   7571: mtha' yas pa'i sems can thams cad bsam gyis mi khyab pa'i thugs rje chen pos rjes su bzung bar bzhed pa'i rgyu las so/
GL 7572: tshul ji ltar na 'jig rten gyi khams ji snyed pa mkhyen pa'i ye shes kyis gdul byar gyur pa'i 'jig rten ma lus pa kun la legs par gzigs nas ni ji lta ba mkhyen pa'i ye shes chos kyi sku 'gyur ba med pa'i ngang du mnyam par bzhag pa las nam yang ma g.yos par ro/
   7573: don gang dag ston na sprul pa'i rang bzhin rnam pa sna tshogs pa rnams kyis rmad du byung ba'i mdzad pa bcu gnyis yang dag par ston pa ste/
   7574: de yang shAkya'i rgyal po lta bu la nye bar mtshon na/
   7575: bdag nyid chen po des dga' ldan pa'i lha'i skye ba dam pa tog dkar
   7576: zhes bya bar mngon par skye ba'i tshul bstan nas lha'i tshogs rab tu mang po smin grol la bkod pa dang*/
   7577: 'dzam bu gling pa rnams gdul ba'i dus la bab pa na lha'i rol mo'i sgra las/
   7578: skyes mchog khyod kyi bsod nams dpal gyis ni/
   7579: dga' ldan pho brang shin tu mdzes mod kyi/
   7580: 'on kyang thugs rje'i thugs dang ldan pas na/

[… two further GLOSS blocks with the same gloss (BO_TSD_BO_DC_RDI-SS-32, a second copy of the
seng ge'i nga ro; BO_S10_KHEZ010, a second copy of the nges don rab gsal snang ba), then
BO_T06_D4025 (the vyākhyā, QUOTE: no paraphrase of these words in the 60 segments after its hit) …]

=== theg pa chen po rgyud bla ma'i bstan bcos/ (mahāyānottaratantraśāstra) · Tengyur, Toh 4024 · BO_T06_D4024:64b-12 · QUOTE
de dngos min snang ltar// de bzhin 'gro rkyen sna tshogs pas// khyab bdag de dngos min par snang // thugs rje chen pos 'jig rten mkhyen// 'jig rten kun la gzigs nas ni// chos kyi sku las ma g.yos par// sprul pa'i rang bzhin sna tshogs kyis// skye ba mngon par skye ba dang // dga' ldan gnas nas 'pho ba dang //

[… 6 further QUOTE blocks: the works that cite the stanza with `rgyud bla ma las`; 113 works not shown …]
```

What the call gives, read in Tibetan: both commentaries quote the stanza under the heading `mchog
gi sprul skus mdzad pa bcu gnyis ston tshul` (how the supreme nirmāṇakāya displays the twelve
deeds) and gloss it by paraphrase after `zhes gsungs te` / `zhes pa ste`: the cause (`rgyu`) of the
display is `thugs rje chen pos rjes su bzung bar bzhed pa`; `'jig rten mkhyen` is `'jig rten gyi
khams ji snyed pa mkhyen pa'i ye shes`, the wisdom that knows the world in its extent; `'jig rten
kun la gzigs nas ni` is that wisdom looking on the whole world of those to be tamed, while `chos kyi
sku las ma g.yos par` is the wisdom that knows things as they are resting unmoved in the
dharmakāya. The `GROUNDING` line then reads: `RDI-KK-07:3694 and PARCHIN-094:7572 (same gloss):
'jig rten mkhyen = ji snyed pa mkhyen pa'i ye shes, the cause = great compassion; followed`, and the
seasoned-practitioner footnote says it in one sentence without the locators.

## 4. Honesty rules

- A Toh number, folio or attribution appears in a note only if you have seen it in a hit and read
  the title. `source not located` and `GROUNDING: none found` are honest; an inferred locator is not.
- The GLOSS / QUOTE / NEAR labels and the `root work` line are computed from the wording; a label
  is not a reading. What goes into a `GROUNDING` line or a footnote is the Tibetan you read in the
  hit or its printed context, with that segment id.
- The pass uses the DharmaMitra primary search and the DharmaNexus text view, nothing else; the
  Explore summary runs only on the user's explicit request and is then named in the header.
- An English translation among the hits (`EN_…`) is used only as the prior-translations policy
  allows, and always cited; in a blind test it is neither read nor cited and the exposure is logged.
- Dharmamitra is a public research service used one request at a time; when it is slow or down,
  skip the pass, say `GROUNDING: service unavailable`, and translate from the grammar.
