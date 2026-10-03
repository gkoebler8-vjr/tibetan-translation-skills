import re
draft=open("shastra.draft.md").read()
texts={}
for m in re.finditer(r'^### (U\d\d)\n(.*?)(?=^### U\d\d|\Z)',draft,re.M|re.S):
    texts[m.group(1)]=m.group(2).strip()

H={}
H["U01"]="U01 · prose, 3 Tibetan sentences, commentary gloss (lemma, \"means\", gloss) ending on the lead-in · exposition · academic · source: root-text incipit, source not located (verbatim only in Toh 1183 itself)"
H["U02"]="U02 · verse: citation mode, rising, 3–4 beats; padas 7×4, four lines, order 1-2-3-4, closing frame (ces gsungs pa yin no) as one prose line · definitional root verse · academic · source: root verse (per the brief); source not located (28-syllable verbatim run only in Toh 1183 itself, D 6a)"
H["U03"]="U03 · prose, 1 Tibetan sentence, framing, ends on the lead-in · framing (minimal) · academic · not a citation"
H["U04"]="U04 · verse: citation mode, rising, 3–4 beats; padas 7×2, two lines, order 1-2, followed by the commentator's frame · root incipit + gloss frame · academic · source: Hevajra Tantra, Toh 418 (Kangyur) D 17a, first pada verbatim, second pada a variant; quoted also in Toh 1190, Toh 2255"
H["U05"]="U05 · prose, 5 Tibetan sentences · exposition with a reported objection (debate), prescriptive close · neutral-scholarly · academic · not a citation (a reported saying, source not located)"
H["U06"]="U06 · prose, 3 Tibetan sentences · exposition (grading of disciples; impersonal prescription) · neutral-scholarly · academic · not a citation"
H["U07"]="U07 · prose, 4 Tibetan sentences · exposition (gloss of the prajñājñāna empowerment) · neutral-scholarly · academic · not a citation"
H["U08"]="U08 · prose, 7 Tibetan sentences · commentary gloss on the quoted pada (scaffold kept), then argument and objection · commentary gloss, then exposition/debate · academic · quotes U04 pada 2 and U02 pada 3"
H["U09"]="U09 · prose, 3 Tibetan sentences, objection and reply, ends on the lead-in · debate · neutral-scholarly · academic · not a citation"
H["U10"]="U10 · verse: citation mode, rising, 3–4 beats; padas 7×4, four lines, order 1-2-3-4 · aphoristic verse cited as proof · academic · source not located (28-syllable verbatim run only in Toh 1183 itself, D 7a)"
H["U11"]="U11 · verse: citation mode, rising, 4–5 beats; padas 7×4, four lines, order 1-2-3-4, closing frame (zhes bstan pa yin no) as one prose line · aphoristic verse cited as proof, ends in a rhetorical question · academic · source not located (28-syllable verbatim run only in Toh 1183 itself, D 7a)"
H["U12"]="U12 · prose, 4 Tibetan sentences · debate (objection, reply, rhetorical question), ends on the lead-in · neutral-scholarly · academic · not a citation"

N={}
N["U01"]="""Q: "de'i rab tu dbye ba ni dbye ba ste" has the gloss as topic and the lemma as predicate (the reverse of the preceding clause); rendered with the scaffold "'Division' means its subdivision". Alt, literal order: 'Its subdivision is the "division."'
Q: "de yang": de = the division just defined (taken); alt: the whole preceding gloss. "de'i" = of the vow, that is, of empowerment.
Alt: mtshan nyid = "defining characteristics" (lakṣaṇa); "characteristics" would also do.
Source: the lemma sdom pa'i dbye ba la sogs pa is the incipit of a root passage; dm.py identify finds it verbatim only in Toh 1183 itself (D 6a); source not located.
Issue: the English ends on the lead-in (ji skad du); the quotation (U02) follows outside the span.
Check: in-context, no finding on this unit; MITRA agrees in substance."""
N["U02"]="""Source: root verse (the brief says the commentator quotes root padas); dm.py identify: 28-syllable verbatim run only in Toh 1183 itself (D 6a); source not located in the canon.
Issue: "made known" for bsgrags ("proclaimed"), because "proclaimed" leaves a four-syllable sag in the line; "washes and empowers" keeps the dbang bskur play on which U08 depends.
Issue: 'di yis (instrument) rendered as the subject "this", with "one" supplied for the agentless passive; bas and de phyir are both kept ("since ... therefore").
Q: the agent of bsgrags and of gsungs is unnamed; U08 names the Bhagavān as the speaker of the root; left unnamed here, the closing frame rendered "This is what was said."
Q: 'di ("this") has no stated antecedent (the washing/empowerment itself).
Q: bzhi ru = "as fourfold" (four kinds), cf. U03 "those same four".
Check: in-context, minor (bsgrags term, noted); MITRA agrees."""
N["U03"]="""Q: the verb of saying is elided; "[the root text] says" is supplied because the following quotation (U04) is root text. Alt: "[it is said]".
Q: de nyid = "those same four" (anaphoric to U02), not "reality" (de nyid = tattva).
Issue: yang = "also"; 'di ltar ("as follows") is carried by the colon; the English ends on the lead-in.
Check: in-context, no finding; MITRA agrees in substance."""
N["U04"]="""Source: dm.py identify: the first pada is verbatim in several canonical quoters (Toh 1190, D 163a; Toh 2255) and in the Hevajra Tantra, Toh 418 (Kangyur), D 17a, where the pair reads "slob dpon gsang ba shes rab dang / bzhi bde yang de bzhin no"; the commentary's second pada (de ltar de bzhin bzhi pa yang) is a variant of that reading.
Issue: de ltar de bzhin yang is folded into "likewise ... too" in the verse; the commentary reads de, de bzhin and yang separately in U08, where the glosses are keyed with Wylie.
Issue: shes rab = "wisdom" here as the name of the third empowerment; U07 glosses it as prajñā within prajñājñāna.
Q: the subject of 'chad par 'gyur ba is elided: "[the subdivisions]" (cf. U03); alt: "[the four empowerments]".
Q: MITRA reads the padas as the grammatical topic ("the master, the secret, the wisdom and the fourth will be explained"); kept: the padas are the quoted incipit (U08 quotes the same words with zhes bya ba).
Check: in-context, minor (subject bracket aligned with the construal; de ltar folded and noted)."""
N["U05"]="""Issue: S1 is an etymology of ācārya (ā-cāra, "conduct"); the Sanskrit is given here only, not in the text. Register shifts from exposition to debate at "But there is this saying" and to prescription at "Therefore, to begin with".
Q: "de nyid kyi de'i sdom pa yin pas": double genitive; read "this is his very vow" (the conduct is the master's vow). Alt: "because it is the vow of that very [empowerment]".
Q: slob dpon = the person in S1's etymology and the empowerment named after him from S2 on.
Q: scope of the reported saying: taken to begin at "yang bya ba'i rgyud ..." (after yin gyi) and to end at "'gyur ro"; the saying opens its conclusion with de lta bas na ("therefore"), so its premises precede it in the same voice. Alt: it begins at "slob dpon gyis dbang bskur ba'i ngo bo". MITRA reads the premises as the commentator's own and only the conclusion as the saying; kept.
Q: "slob dpon gyis dbang bskur bas dbang bskur ba la ni mi bya'o" rendered "one is not to be empowered by the master's empowerment" (the contrast with S4 requires this sense). Alt: "no [further] empowerment is to be performed, since the master has empowered".
Q: gang read as a relative ("what is called"); alt: part of "gang las kyi phyag rgya" ("whichever karmamudrā").
Q: mi ldog pa'i dbang bskur ba = "irreversible empowerment", taken as the empowerment already received in the lower tantras.
Q: mngon par rtogs pa rendered "abhisamaya": a named text (perhaps a Hevajra abhisamaya) or the genre; left open. "This" in the last sentence = the master's empowerment (taken); alt: empowerment in general.
Q: dgyes pa'i rdo rje = Hevajra (the root of this commentary, Toh 1183 "dgyes pa rdo rje'i dka' 'grel"); alt: "Joyous Vajra" as a title.
Alt: dbang ba = "authority" (adhikāra); "entitlement" also possible.
Check: in-context, no major; MITRA differs on the scope of the saying (kept, recorded above)."""
N["U06"]="""Q: "mos pas nges par bzung nas": agent and object elided; read "[they], having firmly taken hold [of it] through conviction"; alt: the teacher, having firmly taken them [as disciples].
Q: gsang bar gnas pa'i nor bu is taken in apposition to the guru's pith instruction (it fits the explanation of "secret"); alt: a separate locus or means ("in/by the jewel that dwells in secret").
Q: "'dir dbang bskur ba'i dbang po 'bring po rnams": "Here, among the empowered, those of middling faculties"; alt: "those of middling faculties for empowerment".
Alt: spros pa'i phyag rgya = "mudrā of elaboration"; the lexicon has no Sanskrit for it and none is back-formed (MITRA gives prapañcamudrā).
Issue: S3 pairs the samayamudrā with the middling grade as the next grade; it is not stated as the counterpart of the "secret empowerment".
Check: in-context, no finding; MITRA agrees in substance."""
N["U07"]="""Issue: jñāna, prajñā and prajñājñāna are kept in IAST (attested equivalents of ye shes, shes rab and shes rab ye shes in the lexicon) because the commentary glosses the two members of the compound; shes rab = "wisdom" in the root names (U04, U05).
Q: khyad par can gyi ye shes: "the special jñāna" is the jñāna of prajñājñāna, glossed as prajñā; alt: "the awareness that is distinguished/excellent".
Q: de rab tu bsgrub pa'i phyir: purpose ("for accomplishing that"); alt: cause ("because it accomplishes that").
Q: the long noun phrase of S3: gang as relative, nor bur "as a heart-jewel", gzugs can "having form"; bsdus pa'i gzugs can may be a fixed expression ("having a condensed form"). Alt: the guru's instruction is itself the heart-jewel; MITRA reads "within the heart-jewel".
Q: yongs su gyur pa rendered "the transformed", as the text reads; possibly a corruption of yongs su grub pa, "the perfected" (MITRA reads "perfected"); rnam par shes pa gsum is taken in apposition to the three.
Q: dbang bskur ba'i dbang po rab: "the highest faculties among the empowered" (as U06); des = "through that"; alt: "by that empowerment".
Check: in-context, no finding; MITRA differs on nor bur and yongs su gyur pa (kept, recorded)."""
N["U08"]="""Issue: the root words are given in a gloss-keyed literal form ("thus likewise also") with Wylie because the commentary glosses de, de bzhin and yang separately; the verse itself (U04) is rendered as natural English. The quotation in the last sentence is U02's third pada, rendered as there.
Q: "de bzhin du ... yang yin te": ordinary "in the same way"; the commentary then reads the quoted de bzhin as a term (suchness).
Q: "de bzhin nyid de yang dag pa'i mtha' ...": taken as three terms; alt: de = ste.
Q: de'i ngo bo nyid: "its" = suchness; alt: prajñājñāna.
Q: sbyin: the object is elided; "[the fourth empowerment]" supplied. Alt: rjes thogs su "immediately after" (kept, with MITRA: "immediately following").
Q: the long clause of S6: "gang ... byed pa de ni" read as a correlative; the guru's pith instruction is the means of the observing (as in U07 S3); dmigs pa med par dmigs pa = "observing without observing" (alt: "focusing on it without a focal object"); the external mudrā and the perfection of the moment are the objects, as in U07 S3. MITRA reads the external mudrā and the guru's instruction as what does NOT delimit the perfection of the moment (alt reading; kept mine).
Q: "man ngag nye bar bstan par byas pa tsam gyis": "merely because ... has been set out".
Q: bzhed pa: "holds" (honorific); 'dir = "here"; de = the washing away of stains (MITRA: the fourth empowerment).
Check: in-context, no major. MITRA: S5 "immediately after" adopted, reason: the dictionary row for rjes thogs (following immediately), missed in the first construal, not MITRA's word alone; S6 kept (recorded above)."""
N["U09"]="""Issue: objection frame "It may be objected" for gal te ... zhe na; the English ends on the lead-in.
Q: bzhi pa'i bdag nyid can gyi de kho na nyid = "reality, whose nature is the fourth"; alt: "reality, the nature of the fourth [empowerment]".
Q: der ji ltar mi 'gyur: der = "in that case", with "[the fourth empowerment]" supplied; alt (MITRA): "why would it not become that [the fourth]?".
Q: "de ni bden mod": "That is true", a concession answered by 'on kyang.
Alt: thos pas bsgrub par yang mi nus = "through hearing (alone)".
Check: in-context, minor (bracket aligned with the construal); MITRA differs on der (recorded)."""
N["U10"]="""Source: dm.py identify: 28-syllable verbatim run only in Toh 1183 itself (D 7a); semantic neighbours in Pramāṇa works (Toh 4226 and others) share only 4–5 syllables; source not located.
Q: pada 2 is the crux: "ngag las mngon sum thos mthong yin". (b) las as comparison, "more direct than speech: heard and seen" (taken: it fits U09's argument that reality is not reached through speech); (a) las as source, "from speech it is directly heard and seen" (MITRA reads "the direct hearing and seeing of speech"); (c) "apart from speech".
Q: nang na gsal ba de nyid = the clear reality within (de kho na nyid of U09); alt: any inner experience.
Q: thos mthong "heard and seen" as a pair for direct experience; alt: two separate items.
Q: sgra la = "in sound"; alt: "from the sound".
Issue: ba yin (pada 4) is nominaliser plus copula for the count, not emphasis; de nyid ni is topic, not "indeed".
Check: in-context, minor (construal and draft aligned on reading (b)); MITRA differs (reading (a)), kept."""
N["U11"]="""Source: dm.py identify: 28-syllable verbatim run only in Toh 1183 itself (D 7a); source not located.
Q: syntax of padas 1–2: (A) pada 1 a clause, "one's own conceptual thoughts each grow", pada 2 "by meditating on an imagined reality" (taken, after MITRA's flag: each pada self-contained, rgyas a pada-final verb); (B) "a reality imagined at length by each of one's own conceptual thoughts" (the earlier choice, now the alternative). The protasis is cumulative; "and" is supplied.
Q: rtog par is spelled rtog ("conceive") where the sense wants rtogs ("realize"); rendered "realized".
Q: rgyud la = "in the mindstream"; alt: "in the continuum".
Q: de de = "each" (alt: "this and that").
Q: the agent of bstan is unnamed ("This is what was taught").
Check: in-context, minor (rgyas had been dropped, restored; then MITRA flagged the syntax). MITRA: changed to reading A, reason: pada-clause alignment (P1 is a complete clause ending in the verb rgyas, as P3 and P4 are complete clauses; reading B needs rgyas to cross the pada break); the relation and role tests were re-run on the clause and the reason is in the construal; the argument is moderate and reading B stays as the alternative."""
N["U12"]="""Issue: objection frame "It may be objected"; the English ends on the lead-in.
Q: de'i skad cig nyid la = "in that very moment" (the moment of the empowerment); alt: "in the moment of that realization".
Q: S2 nyid is read as emphatic ("is indeed accomplished"); MITRA reads "only"; alt: restrictive.
Q: S3 "gang zhig sus kyang mi 'dod cing ma mthong ba": "something no one wants and no one has seen"; de = the instantaneous attainment; mi 'dod could be "does not accept"; the question is rhetorical.
Alt: brtson 'grus 'bar ba = "ardent diligence" (literally blazing).
Check: in-context, no finding; MITRA differs only on nyid (kept)."""

order=["U%02d"%i for i in range(1,13)]
out=[]
for u in order:
    out.append(f"### {u}\nHEADER: {H[u]}\nTEXT:\n{texts[u]}\nNOTES:\n{N[u]}\n")
open("final_body.md","w").write("\n".join(out))
print(len(out))
