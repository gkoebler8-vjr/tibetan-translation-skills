# Jewel Garland of Yoga (Toh 1183), part I ch. 1 — units U01–U12

Model/effort: Claude Opus 5.5 (claude-opus-5-5), reasoning effort max (the calibrated setting); run autonomously as a workflow subagent, brief taken as given; interrupted during the analysis pass and resumed (see runlog.md).
Brief: academic · publication · IAST · square brackets for supplied words · commentary scaffold kept · root verses as verse blocks, free line-for-line · neutral-scholarly · doubts in the notes.

### U01
HEADER: U01 · prose · commentary gloss (lemma, "means", gloss), ending on a citation lead-in · academic · lemma from the root tantra, not run through identify (three words)
TEXT:
As for “the divisions of the vow” and so on: “vow” means consecration; “division” means its classification, whose defining characteristics will be explained. And this is as it is said:
NOTES:
Q: “division”: the gloss stands first in the Tibetan (de'i rab tu dbye ba ni dbye ba, “its classification is the division”); same sense.
Alt: sdom pa “vow” renders saṃvara (also “binding”, the tantra's own title word); the commentator equates it with consecration.
Q: 'chad par 'gyur ba “will be explained”: later in the tantra (cf. U04) or later in this commentary; alt “to be explained”.
Check: in-context; no finding. MITRA: same reading.

### U02
HEADER: U02 · verse: free line-for-line (academic default, no metre), padas 7×4, 4 lines, order 1-2-3-4; closing frame in prose · citation · academic · root verse not located verbatim (identify's only verbatim hit is this commentary, Toh 1183, D 6a); by content the Hevajra Tantra's etymology of consecration (pt. II), unconfirmed
TEXT:
For the benefit of beings,
consecration has been proclaimed as fourfold.
Since one is washed and consecrated by it,
it is therefore called “consecration.”

So it is taught.
NOTES:
Issue: the etymology works in Sanskrit (seka “consecration” from sic “to sprinkle”); the Tibetan repeats dbang bskur (“consecrated”) in line 3 and the English follows it, so the wordplay does not carry.
Q: line 3, the patient is elided: “one [the disciple] is washed and consecrated by it”; alt “by this [the master] washes and consecrates [the disciple]”.
Q: 'di yis “by it”: the consecration itself, or the water of the rite.
Q: bzhi ru bsgrags “proclaimed as fourfold”; alt “proclaimed in four [kinds]”.
Source: dm.py identify (--exclude 1183): the only verbatim hit is Toh 1183 itself (the exclusion removed nothing); other hits share five syllables or fewer and are not cited.
Check: in-context; no finding. MITRA: same reading.

### U03
HEADER: U03 · prose · framing (lead-in to the root words in U04) · academic · not a citation
TEXT:
To state the classification of these same four consecrations, [the tantra] also says the following:
NOTES:
Q: phyir read as purpose (“to state”); alt cause (“because [the tantra] states the classification …”).
Q: yang “also”; alt “again” (the tantra returns to the topic).
Q: the elided agent of brjod pa is the tantra; alt the commentator (“to state …, [I cite] the following”).
Issue: the main verb of the Tibetan period ('chad par 'gyur, “will be explained”) lands in U04; “says the following” is supplied so that the unit ends on the lead-in.
Check: in-context; no finding.

### U04
HEADER: U04 · mixed: root lemma as verse (free line-for-line, padas 7×2, 2 lines, order 1-2) + prose tail · commentary framing · academic · Hevajra Tantra pt. II (Toh 418), D 17a; line 2 there in another reading; the commentary's reading shared by Toh 1190 and Toh 2255
TEXT:
Master, secret, wisdom,
and likewise the fourth as well.

With these words and those that follow, [the classification] will be explained.
NOTES:
Q: de ltar de bzhin … yang rendered as a whole, “likewise … as well”; U08 glosses its words one by one (de “that”, de bzhin “thus”, yang “too”), so the Wylie is given there.
Q: the elided subject of 'chad par 'gyur is the classification (U03); alt the four consecrations themselves (so MITRA).
Q: 'chad par 'gyur taken as impersonal (“will be explained”); alt with the passage as agent (“with these words … [the tantra] will explain [it]”).
Source: Hevajra Tantra pt. II (Toh 418), D 17a-12/13: line 1 verbatim; line 2 there reads bzhi bde yang de bzhin no. The commentary's reading (de ltar de bzhin bzhi pa yang), which U08 glosses, is translated.
Check: in-context; no finding.

### U05
HEADER: U05 · prose · exposition (S1–S3), debate (S4), prescription (S5–S6) · academic · S4 quotes a claim: source not located
TEXT:
In this yoginī tantra, one is a “master” because one engages in conduct far removed from evil, non-virtuous states; for that very [conduct] is one's vow. In essence, consecration by the master is what is called “bringing about the four joys in their own nature from the action seal, through the four moments.” [The term] is not applied, however, to consecration by a master who has received the irreversible consecration common to the kriyā tantras and the rest. Therefore the statement that “one also becomes qualified to teach all the yoga tantras, the yoginī tantras and the rest, to hear them, and so on” counts for nothing. Accordingly, first of all, to authorize [the disciple] to hear the yoginī tantras such as the *Hevajra*, to meditate on them and so on, he must be consecrated with precisely the master consecration. It should further be understood that, in accordance with the *abhisamaya*, this [consecration] is indicated by the defining characteristics of the master, secret, wisdom and fourth [consecrations].
NOTES:
Q: S1 ring du gyur pa kun du spyod pa “engages in conduct far removed from”; alt “being far removed from …, one engages in conduct” (so MITRA).
Q: S1 de nyid kyi de'i sdom pa yin pas so “for that very [conduct] is one's vow”; alt “because it is the vow belonging to that very [master consecration]” (back to U01: vow = consecration).
Q: S2 slob dpon gyis (ergative) “consecration by the master”, i.e. the master consecration (S5 has the genitive slob dpon gyi); alt “consecrating done by a master”.
Q: S2 las kyi phyag rgya las “from the action seal” (ablative, source); MITRA “by means of the action seal”.
Q: S3 thob pas … slob dpon gyis read as one agent (“a master who has received …”); alt the disciple has received the irreversible consecration and is then consecrated by a master (so MITRA).
Q: S3 phyir mi ldog pa'i read as the compound “irreversible”; alt phyir = “because”: “because it is common to the kriyā tantras and the rest, the non-returning consecration …” (so MITRA).
Q: S3 la ni mi bya'o “[the term] is not applied to”; alt “[the master consecration] is not to be performed by [such] a consecration”.
Q: S4 ci yang ma yin “counts for nothing”; alt “is meaningless”.
Q: S6 “this [consecration]” = the four together (cf. U03); alt the master consecration of S5, each consecration marked by the four.
Q: S6 mngon par rtogs pa ji lta ba bzhin du “in accordance with the abhisamaya” (the ritual manual); alt “according to [the disciple's] realization”.
Source: S4's quoted claim: identify's only verbatim hit is this text itself (Toh 1183, D 6a; --exclude removed nothing); source not located (a view the commentator rejects).
Issue: S5 “Accordingly” renders the second de lta bas na (“therefore”), to avoid two “Therefore” in a row.
Check: in-context; no finding.

### U06
HEADER: U06 · prose · exposition, prescriptive · academic · not a citation
TEXT:
Those of dull faculties who have received such a master consecration are to be made firm through conviction and then taught the meditation on the action seal and on the seal of elaboration. Likewise, as regards the completion stage, too: through the guru's instruction itself, one experiences the four joys, whose nature is the four moments, in the jewel that abides in the secret [place]. That experience is called the secret consecration, because it is not to be taught to yogins who apply themselves to meditation with elaboration. Here, to those of middling faculties who have been consecrated, the meditation on the pledge seal is to be taught and explained.
NOTES:
Q: S1 mos pas nges par bzung nas “made firm through conviction” (the master acting on the disciples); alt “having determined [them] by [their] inclination”; alt “once they have firmly grasped [it] through conviction”; MITRA “having firmly grasped it through devotion” (the teacher grasping “it”).
Q: S1 spros pa'i phyag rgya “the seal of elaboration” (spros pa = prapañca; cf. “meditation with elaboration” in S2); its identity is not stated in the unit; alt “the elaborate seal”.
Q: S2 gsang bar gnas pa'i nor bu read with an elided locative, “in the jewel …” (as in U07 snying gi nor bur); alt in apposition, “the guru's instruction itself, the jewel that abides in secret” (so MITRA); alt a compound, “the guru's instruction on the jewel that abides in the secret [place]”.
Q: S2 gsang bar “in the secret [place]”; alt “in secret, hidden”.
Q: S2 skad cig ma bzhi'i rang bzhin dga' ba bzhi po “the four joys, whose nature is the four moments”; alt “the four joys, the nature of the four moments”.
Q: S2 phyir gives the reason for the name (“secret” because it is not to be taught to these yogins); alt the reason for the whole statement.
Q: S3 'dir “here” = with this (the secret) consecration; alt “in this tantra”.
Issue: S2 split: the nominalized experience (nyams su myong ba de ni) becomes a clause, resumed by “That experience”.
Check: in-context; 2 minor: “and on the seal of elaboration” (one meditation on both seals; “on” added); the glossary note for spros pa bsgom pa aligned with the body.

### U07
HEADER: U07 · prose · commentary gloss (S1–S2), exposition (S3), prescription (S4) · academic · not a citation
TEXT:
Likewise, “wisdom” means a superior gnosis: the knowledge that all phenomena are nothing but mind. The consecration for bringing this about is the consecration of the gnosis of wisdom. Further, it should be understood that the gnosis of wisdom is what, through the guru's instruction itself, rightly indicates the external seal and the moments in the jewel of the heart. That jewel embodies the combined essence of the three consciousnesses: the dependent, the imagined and the transformed. To those of the highest faculties who have been consecrated with that consecration, the Dharma seal is to be taught and explained by means of the illusion-like *samādhi*.
NOTES:
Q: S1 the gloss stands first in the Tibetan (khyad par can gyi ye shes ni shes rab); same sense.
Q: S1 khyad par can “superior” (prajñā read as pra- + jñāna); alt “special”, “distinctive”.
Q: S3 yongs su gyur pa “the transformed”; the usual third of the three natures is yongs su grub pa, “the perfected” (MITRA gives “the perfected”); the text as given is translated, not emended.
Q: S3 gang … yang dag par mtshon pa active, the gnosis “rightly indicates”; alt “in which … the external seal and the moments are rightly indicated (or perceived)”.
Q: S3 ngo bo bsdus pa'i gzugs can “embodies the combined essence of”; alt “whose form condenses the nature of”.
Q: S3 yang de ni: de = the gnosis of wisdom; alt the consecration of the gnosis of wisdom.
Q: S4 sgyu ma lta bu'i ting nge 'dzin gyis “by means of” the illusion-like samādhi (the means of teaching); alt the Dharma seal [practised] with that samādhi.
Issue: S3 the relative clause on the jewel is set as its own sentence after the definition (“That jewel embodies …”).
Check: in-context; 1 minor (the split above), no change.

### U08
HEADER: U08 · prose · commentary gloss (S1–S4), debate (S5–S6) · academic · root lemmas: U04 line 2 (Hevajra Tantra, Toh 418) and U02 line 3 (root not located verbatim)
TEXT:
Likewise, there is the fourth as well. As for the words *de ltar de bzhin … yang*, “likewise … as well”: *de*, “that,” refers to the gnosis of wisdom. *De bzhin*, “thus,” means thusness, which does not differ in meaning from what are called the limit of reality and the *dharmadhātu*. The consecration through which one sees or brings about its very nature is what the word *de bzhin*, “thus,” denotes. The word *yang*, “too,” means that [the fourth] is also to be given immediately after the consecration of the gnosis of wisdom. Further, as to this, there is the external seal, and there is that which, through the guru's instruction itself, focuses on the perfection of the moment by the yoga of objectless focus, a moment characterized by not being definitely delimited into separate objects. These do not become the fourth consecration merely through the teaching of the instruction on what is to be called “the fourth consecration.” Otherwise: if, with the words “one is washed and consecrated by it” and so on, the Blessed One holds that consecration here is the washing away of stains, how could it come about through merely teaching an instruction?
NOTES:
Issue: the gloss works on the root's Tibetan words (which render Sanskrit tat, tathā, punar), so they are given in Wylie with an English word-gloss; U04's “likewise … as well” renders the pada as a whole.
Q: S1 de bzhin du bzhi pa yang yin te: the commentator's paraphrase of the root pada; alt “likewise, it is also the fourth”.
Q: S2 rnams la: thusness compared with the other two; alt the limit of reality and the dharmadhātu only.
Q: S3 de'i ngo bo nyid “its very nature”: of thusness; alt of “that” (the gnosis of wisdom).
Q: S5 the topic (“the external seal, and that which … focuses”) taken as the subject of 'gyur ba ma yin (“these do not become the fourth consecration merely through …”); alt with bya ba'i read as a sentence break: “[this] is what is to be called the fourth consecration; merely teaching the instruction does not make it the fourth consecration”.
Q: S5 gang … dmigs par byed pa “that which focuses” (the gnosis); alt “the one who focuses” (the yogin). MITRA makes the external seal and the guru's instruction what (does not) delimit the moment, ignoring gang; kept: gang opens the relative clause, as in U07.
Q: S5 mtshan nyid can qualifies the moment (perhaps the fourth moment, “devoid of characteristics”) or the perfection of the moment.
Q: S6 gzhan du na “Otherwise” = if mere teaching made it the fourth consecration; the yin na clause rendered with the literal “if” (a factual premise); alt “given that”.
Source: lemma 1 = U04 line 2 (Hevajra Tantra, Toh 418); lemma 2 = U02 line 3, cited here with dbang bskur ba for dbang bskur bas (no change of sense); identify not re-run.
Check: in-context; 3 minor: S5 subject of “do not become” (construal updated to the topic-as-subject parse), S6 “if” against the construal's “given that”, S2 semi-final de rendered “which”; no change to the text.

### U09
HEADER: U09 · prose · debate (objection and reply), ending on a citation lead-in · academic · not a citation (lead-in to U10–U11)
TEXT:
Suppose it is said: “If the reality that has the nature of the fourth is taught, how could it not become that [fourth consecration]?” That is true. However, since reality is not within the domain of speech, it cannot be expressed; nor can it be brought about through hearing. And this is said in these words:
NOTES:
Q: S1 der “become that” = become the fourth consecration; alt “how would it not arise there [in the disciple]”.
Q: S1 bzhi pa'i bdag nyid can gyi de kho na nyid “the reality that has the nature of the fourth”; alt “the reality that is the essence of the fourth”. MITRA reads bzhi pa as “the tetralemma”; kept “the fourth” (an ordinal; the topic of U08).
Q: S1 de ni bden mod: a concession (“That is true. However …”); alt “That would be so, but …”.
Q: S2 the cause (not the domain of speech) read over “cannot be expressed” only; alt over both clauses.
Q: S2 bsgrub pa “brought about”; alt “established”.
Check: in-context; no finding.

### U10
HEADER: U10 · verse: free line-for-line (no metre), padas 7×4, 4 lines, order 1-2-3-4 · citation · academic · Sahajasiddhi (lhan cig skyes pa grub pa), Tengyur, Toh not given by the tool (dm.py BO_T17_MW1PD95844_2571:8–10), with variants
TEXT:
The reality that is clear within
is heard and seen directly from speech;
yet what arises in sound
is a reflection of conceptual thought.
NOTES:
Source: U10–U11 are two verses of the Sahajasiddhi (title line of the witness: rgya gar skad du sa ha dza sid ti / bod skad du lhan cig skyes pa grub pa), found as the 16-syllable run in dm.py identify; the 43-syllable verbatim hit is this commentary itself (Toh 1183, D 7a; --exclude removed nothing).
Q: line 2: the commentary reads yin, “is heard and seen directly from speech”, a concession answered by “yet” (the shape of U09's “That is true. However …”); the Sahajasiddhi witness reads min, “is not heard and seen directly from speech”; translated as the commentary has it.
Q: line 3 sgra la “in sound”; the witness has sgra las, “from sound”.
Q: line 1 de nyid “reality” (as in U09 and U11); MITRA “that which [is luminous within]”, a demonstrative, and makes it the source of the reflection in lines 3–4, which the Tibetan does not mark.
Alt: gsal ba “clear”; alt “luminous”, “manifest”.
Check: in-context; no finding.

### U11
HEADER: U11 · verse: free line-for-line (no metre), padas 7×4, 4 lines, order 2-1-3-4; closing frame in prose · citation · academic · Sahajasiddhi, as U10 (BO_T17_MW1PD95844_2571:10–12), with variants
TEXT:
If, by meditating on a reality
elaborately imagined, this way and that, by one's own conceptual thoughts,
conceptual thought becomes turbulent in the mind-stream,
how could reality be understood?

So it has been shown.
NOTES:
Q: line 2 (pada 1) de de rgyas read as adverbial on “imagined” (“elaborately … this way and that”); alt pada 1 a clause of its own, “as one's own conceptual thoughts proliferate” (so MITRA).
Q: brtags pa'i de nyid “a reality … imagined” (relative); alt genitive, “the reality of what is imagined” (so MITRA).
Q: line 4 rtog par (as given) “conceive, discern”; the witness reads rtogs par, “realize”; rendered “understood”.
Q: line 3 'khrug “turbulent”; the witness has 'khrul, “confused”.
Source: as U10; further variants in the witness: rgyus for rgyas; rtags … sgom for brtags … bsgoms.
Issue: the frame zhes bstan pa yin no (not honorific) is “So it has been shown.”; U02's honorific gsungs is “So it is taught.”
Check: in-context; no finding.

### U12
HEADER: U12 · prose · debate (objection and reply), ending on a citation lead-in · academic · not a citation (the quotation lies outside the page)
TEXT:
Suppose it is said: “If through the consecration one comes to realize reality directly, and the stains are purified without remainder, why then is the accomplishment of the great seal not attained at that very moment?” It is indeed attained by those of sharp faculties and blazing diligence. Does something become non-existent because no one accepts it and no one has seen it? And this is as it is said:
NOTES:
Q: S1 dbang bskur bas “through the consecration” (means); alt cause.
Q: S1 zhing joins two conditions; alt the second as the result of the first (“and thereby the stains are purified”).
Q: S2 nyid emphatic on the predicate (“indeed attained”); alt restrictive on the agent, “attained only by …” (so MITRA); not taken: nyid follows the verb.
Q: S3 'dod “accepts”; alt “wants, desires” (so MITRA).
Q: S3 gang zhig/de left general (“something”), as in the Tibetan; the referent is the accomplishment of the great seal.
Check: in-context; no finding.

## Run summary

- Units done: 12 of 12. U01–U05 were analysed before the interruption (construal and glossary taken as done); after the restart (13:56) U06–U12 were analysed, and all twelve units were drafted, styled, checked, revised and cross-checked with MITRA.
- Checker spawns: 0. The Agent tool is not available in this workflow subagent, so the check.md protocol was run in-context after a clean break (construal, styled draft and glossary re-read from disk).
- Checker verdict line: VERDICT: 0 major, 6 minor. (in-context; shastra.check.md). One revision round: U06 S1 “and on the seal of elaboration”; construal and glossary notes updated; no revision touched a relation, so no second round.
- MITRA: differs at U04 (the four consecrations as what is explained), U05 (S1 state reading; S2 las as means; S3 who obtained the irreversible consecration, phyir as cause), U06 (S1 object of nges par bzung, “devotion”; S2 the jewel in apposition to the guru's instruction), U07 (yongs su gyur pa as “perfected”), U08 (S5 the seal and the instruction as delimiters, gang ignored), U09 (bzhi pa as “tetralemma”), U10 (de nyid as a demonstrative; an added source for the reflection), U11 (pada 1 as a clause; brtags pa'i as genitive), U12 (nyid as “only”; 'dod as “desired”); kept all, changed none (the grammar for each decision is written in shastra.construal.md, MITRA CROSS-CHECK).
- References read (whole run; detail in runlog.md): before the interruption: tibetan-translate SKILL.md (Skill tool + disk), the page file, english.md, analysis.md, prose.md, modes.md, dm.py lines 53–135 (to diagnose --exclude), tibetan-verse SKILL.md. After the restart, re-read in the fresh context: prompt.md, runlog.md, shastra.construal.md, shastra.glossary.tsv, SKILL.md (Skill tool + disk), the page file, analysis.md, prose.md, english.md, modes.md, tibetan-verse SKILL.md (before U10), and check.md (first read, before the check). Not read: research.md, the tibetan-verse guidelines and failures files.
- Tool calls: tibdict annotate ×12 (U01–U05 before; U06 re-run after the restart because its output was lost, then U07–U12), tibdict lookup ×1 (U06); dm.py identify ×4 (U02, U04, U05, U10–U11 together); dm.py segment ×4 (U04 before; U10–U11 ×3 after: the Sahajasiddhi witness and its title); dm.py translate --file ×1; beats.py 0 (verse is free line-for-line in this brief); Agent 0.
- Token estimate (mine, not measured): the resumed part ≈ 200k new tokens: about 30k re-reading the skill, the references and the run files in the fresh context (the cost of the restart); about 30k of dictionary reports (U06–U12, with --budget 6000 on the long units) plus 6k for identify, segment and MITRA; about 25k writing the construal blocks and glossary; about 20k re-reading construal and draft for the in-context check; about 15k for the draft, style, check and final files; the rest, the largest share, reasoning over the hard construals (U05–U06, U08, U10–U11) and the English. The pre-interruption part (U01–U05 analysis) is not visible from this context; by the runlog's calls it was perhaps 80–120k, so the page in total is roughly 300k.
