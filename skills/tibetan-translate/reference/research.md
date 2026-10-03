# Research brief: translating Classical Tibetan Buddhist texts into English, and running LLM-assisted translation pipelines

Prepared 2026-10-03, for redesigning the Tibetan translation skills (analysis → rendering → style adaptation).

**How to read this brief.** Bullets marked **[S]** are sourced claims: what the cited source says, checked against the source text or abstract where I could get it. Bullets marked **[I]** are my own inferences or practitioner generalizations. Several key sources (Jackson 1996, Beyer 1992, Hackett 2003, Wilson 1992, Preston, Sørensen 1990) are print books that I could not read online. Claims about them are limited to what their publishers, reviewers or indexes state, and are marked as such. **Coverage gap:** I found no peer-reviewed study of LLM *translation* errors in Classical Tibetan. The closest work is DharmaBench (classification only) and a series of Pāli→English audits. Item 10 is therefore mostly inference.

---

## PART A: Translating Tibetan Buddhist texts

### 1. Translation-theory frameworks and how Buddhist translators use them

- **[S]** Nida's formal vs. dynamic ("functional") equivalence came out of Bible translation (Nida 1964, *Toward a Science of Translating*; Nida & Taber 1969). Venuti's domestication/foreignization concerns "how much a translation assimilates a foreign text to the translating language and culture, and how much it rather signals the differences of that text" (Venuti 1998, *The Scandals of Translation*, as quoted at https://en.wikipedia.org/wiki/Domestication_and_foreignization).
- **[S]** Skopos theory (Reiss & Vermeer 1984; Nord 1997, *Translating as a Purposeful Activity*) holds that a translation's purpose and audience decide its strategy. Nord distinguishes "documentary" translation, which documents the source for the reader, from "instrumental" translation, which works as a text in its own right. (Standard reference; not fetched.)
- **[S]** Appiah's "thick translation" is "academic translation that seeks with its annotations and its accompanying glosses to locate the text in a rich cultural and linguistic context" (Appiah 1993, *Callaloo* 16(4); https://philpapers.org/rec/APPTT).
- **[S]** The oldest Tibetan precedent is the imperial decree in the *sgra sbyor bam po gnyis pa* (783/814 CE). Namgyal Tsetan translates its governing principle as: "translate in easy-to-read Tibetan without violating the meaning." Other rules in the decree:
  - Prose word order may be changed "in accordance with its meaning … as fluently as possible."
  - Within a stanza "the syntax can be changed as appropriate," and a stanza may run to four or six lines.
  - Polysemous names such as *Gautama* or *Kauśika* should not be forced into one Tibetan equivalent.
  - Speech verbs follow an honorific ladder: Buddhas get high honorifics, others get medium or plain verbs.
  - Sakya Paṇḍita later defended shortening the 21-syllable Sragdharā line to 19 Tibetan syllables "to make it intelligible and easy to read," at the cost of the Indian meter.
  (Namgyal Tsetan 2024, "Tibetan Translation Key: Imperial Decrees of the Two Volume Lexicon," *Journal of Tibetan Literature* 3(1): 71ff, https://journaloftibetanliterature.org/index.php/jtl/article/download/42/210/830; see also Scherrer-Schaub 2002, *JIABS* 25, https://journals.ub.uni-heidelberg.de/index.php/jiabs/article/download/8927/2820/8721)
- **[S]** Thupten Jinpa's 2014 plenary at Tsadra's Translation & Transmission conference used these imperial rules as a modern charter. His slide lists: Tibetan sensibilities take priority in word order "unless resulting in error"; "integrity of verse must be preserved"; polysemous words "should not be reduced to one" rendering; grammatical particles; synonyms. It also lists classic failure types: "excessive literal approach," "mistakes in word divisions, and blind guesswork," ignorance of mythology, and "reverse reading of etymology." He frames the translator's tension as faithfulness (rigor, literalness) against accessibility (flexibility, creative appropriation), with allegiances to the reader, to the text's cultural context, and to the translator (Jinpa 2014, https://conference.tsadra.org/wp-content/uploads/2016/04/Thupten-Jinpa-Plenary-Session-1-Translation.pdf).
- **[S]** Tsadra's 2017 conference (CU Boulder, about 250 translators, keynote by Susan Bassnett) held sessions on "Fidelity vs. Innovation" and "The Translator's Intention," asking "What constitutes an authentic translation?" and how to balance "fidelity to the past with allegiance to the present" (https://conference.tsadra.org/session/translation-fidelity-vs-innovation/; https://www.colorado.edu/tibethimalayainitiative/2017/06/23/tsadra-conference-brought-250-translators-buddhist-texts-cu-boulder-may-31-june-3).
- **[S]** Eben Yonnetti (AAR regional paper, 2015) applies Venuti to liturgy. He argues that foreignizing translations with "visible" translators are *beneficial* for Tibetan practice texts, against the default of transparent domestication (https://www.academia.edu/11624601/).
- **[S]** 84000 rejects the idea that "accuracy and readability are at opposite ends" and calibrates accuracy "in terms of how well the meaning is conveyed rather than … word-for-word correspondence" (84000 *Guidelines for Translators*, https://docs.google.com/document/d/1MMr8x-kACoMB_O6ySU0IagoyFm6gTEGIJqgYi2Dx0rI/). Tom Tillemans adds that the translation should "stand on its own," and that "an approximative understanding of Sanskrit or Tibetan syntax usually yields a vague or wrong translation" (https://84000.co/post/the-art-of-translation-inside-84000s-editorial-process-with-john-canti-and-tom-tillemans).
- **[I]** In practice the field maps onto skopos theory more than onto any single equivalence theory:
  - academic editions are documentary and "thick": Hopkins-school bracketed glosses, endnotes, Wylie;
  - reader editions for 84000, the Library of Tibetan Classics (LoTC) and Padmakara are instrumental, but with consistent terminology;
  - liturgy is instrumental and must be chantable (Nalanda, Padmakara).
  The four target audiences map naturally onto this: academic = documentary/thick; new practitioner = instrumental/domesticating; seasoned practitioner = instrumental with stable technical vocabulary (mild foreignization); hybrid = instrumental main text plus a thin documentary layer.

### 2. Published style and translation guidelines

- **[S] 84000 Guidelines for Translators.**
  - *Values:* "accuracy of meaning, clarity, consensuality, consistency, and flexibility."
  - *Readership:* "nonspecialist but educated readers."
  - *Square brackets:* avoid them. If an addition is justified, the bracket is unnecessary.
  - *Sanskrit:* full IAST diacritics. Dictionary words such as *karma*, *nirvāṇa* and *mantra* are not italicized; rare Sanskrit is italicized at first use.
  - *Names:* Indian people and places in Sanskrit, Tibetan ones phonetically. Do not invent Sanskrit back-forms; translate the name instead.
  - *Repetition:* stock passages are reproduced in full. Narrative connectives like *de nas* may become paragraph breaks.
  - *Honorifics:* render simply ("The Buddha said," not "proclaimed the following words"). In long epithet strings, capitalize only the last epithet.
  - *Language:* gender-neutral, plurals preferred.
  - *Glossary:* a trilingual glossary is required (terms, persons, places, texts; ≤150 words per entry).
  (https://docs.google.com/document/d/1MMr8x-kACoMB_O6ySU0IagoyFm6gTEGIJqgYi2Dx0rI/; hub: https://scholar.84000.co/translator-guidelines)
- **[S] 84000 AI policy (October 2025).** AI may be used to compare editions, draft summaries and glossary definitions, and detect translation errors. It is **prohibited from producing first-draft translations** of canonical texts. The policy warns of "convincing falsities" and says the "superficial plausibility of AI outputs can create a false sense of security." Prompts, model and date must be documented (https://docs.google.com/document/d/1QbImo5kY8Id1DrBvTJcu2qavSLLC24Qa/).
- **[S] Library of Tibetan Classics (Thupten Jinpa, general editor).** The main text is "largely free of scholarly apparatus so that the actual text flows naturally," with an introduction, annotation and glossary (https://tibetanclassics.org/index.php/library-of-tibetan-classics-lotc/; https://www.tsadra.org/translators/institute-of-tibetan-classics/).
- **[S] Alexander Berzin.** Advocates consistent terminology across a corpus; avoiding "translationese"; consulting Sanskrit to settle tense, case and relations "that Tibetan grammar often obscures"; dropping Christian-loaded terms such as "sin"; and treating translations as revisable (https://studybuddhism.com/en/advanced-studies/history-culture/transmission-of-buddhism/methodology-for-translating-buddhist-texts).
- **[S] Rigpa Wiki editorial guidelines.** Full diacritics in scholarly work, phonetic Sanskrit for general-audience books, Wylie for Tibetan transliteration (https://www.rigpawiki.org/index.php?title=Editorial_Guidelines). The Wisdom Publications style guide covers the same ground (https://wisdomexperience.org/wp-content/uploads/2019/06/Wisdom-Style-Guide.pdf; could not be fetched).
- **[S] Hopkins/UMA.** The UMA Tibetan-Sanskrit-English dictionary grew out of "the process of translation" over five decades of group work (https://uma-tibet.org/document/the-uma-institute-for-tibetan-studies-tibetan-sanskrit-english-dictionary/). Hopkins has been "criticized for creating an idiosyncratic lexicon" (https://en.wikipedia.org/wiki/Jeffrey_Hopkins).
- **[I]** Hopkins-school translations use fixed one-to-one term equivalents and bracketed interpolations from commentaries. That suits the academic audience and is exactly what 84000 forbids in reader editions. The skills should treat bracket-glossing as an *academic-mode-only* device.
- **[I]** Points of consensus across these guidelines:
  1. Use one stable glossary per project, but allow context-sensitive renderings for polysemous terms (an imperial rule that Jinpa restates).
  2. Sanskrit takes IAST in academic mode; reader modes either drop or naturalize it.
  3. Honorifics are conveyed through English register and verb choice, not stacked adjectives.
  4. Connectives such as *de nas* or *des na* are structural signals. They may become formatting, but must not be silently deleted when they carry logic.

### 3. Register and genre

- **[S]** Jackson's genre survey distinguishes *glu* (song), *mgur* (songs of experience) and *snyan ngag* (kāvya-style ornate poetry). In his account, *mgur* range from "rhythmically simple personal reports (most often in seven- or nine-syllable lines, mixing trochees and dactyls)" to "highly ornamented verses (of up to twenty-one syllables)" (Jackson 1996, "'Poetry' in Tibet: Glu, mGur, sNyan ngag and 'Songs of Experience'," in Cabezón & Jackson eds., *Tibetan Literature: Studies in Genre*, Snow Lion, 368–392; https://texts.mandala.library.virginia.edu/book_pubreader/15870, quoted via search excerpt).
- **[S]** Lama Jabb (Oxford) treats translation from Tibetan as an "act of bardo," a liminal passage in which both languages are partly dismantled. He stresses Tibetan richness "not only at the level of meaning but also musicality and form," and the "arresting rhythm, haunting lyricism and … repetition of unique Tibetan words and sounds that escape translation" (Jabb, keynote at the Lotsawa Translation Workshop 2018, https://conference.tsadra.org/past-event/2018-lotsawa-translation-workshop/; Huatse Gyal 2024, *Yeshe* special issue, https://yeshe.org/wp-content/uploads/pdf/2024/special_issue/vol_4_1/spl1_v4_1_introduction_translating_across_theBardo.pdf; Jabb 2015, *Oral and Literary Continuities in Modern Tibetan Literature*, Lexington).
- **[S]** Tsadra ran a dedicated session on sādhana and ritual translation. Larry Mermelstein (Nalanda Translation Committee) discussed the demand for "chantability" and choices that "elicit somatic experience" during practice (https://conference.tsadra.org/session/translating-sadhanas-and-rituals/; https://nalandatranslation.org/articles/the-daily-chants-then-and-now/).
- **[S]** DharmaBench builds tasks around genre and discourse markers. Tibetan similes are marked by *'dra ba, dang 'dra, bzhin, ji ltar, de ltar, lta bu*. Quotations are marked by formulaic attribution phrases, especially "in scholastic or polemical writing." The root-text/commentary relation is treated as a structural property models must detect (Golan Hashiloni et al. 2025, IJCNLP, https://aclanthology.org/2025.ijcnlp-long.114.pdf).
- **[I]** Register map for English rendering. This is practitioner consensus I could not tie to one source:

| Genre | English register |
|---|---|
| *man ngag* (pith instruction) | second-person imperative, short clauses, concrete verbs |
| *'grel pa* (commentary) | expository; keep the citation-gloss-conclusion scaffolding (*zhes pa ni … ste … go*) |
| *mtshan nyid* / debate | exact logical connectives (*phyir*, "because"; *thal*, "it follows"); no stylistic variation of technical terms |
| *sādhana* / liturgy | chantable, first person plural or singular, stable line length |
| *mgur* / *dohā* | lyric, colloquial idiom allowed, refrains kept |
| *rnam thar* | narrative past tense; honorific verbs carried by register, not adjectives |
| colophons | formulaic; keep the dating and lineage formulas |

  The shared failure across genres is register flattening into one uniform "dharma English."

### 4. Verse

**Tibetan prosody**

- **[S]** The Tibetan stanza (*tshigs su bcad pa*) normally has four lines (*rkang pa*), mirroring the Sanskrit śloka. Seven- and nine-syllable lines dominate religious verse. Scholarship on *mgur* (Jackson 1996, above; the survey literature on Zhang Tshal pa's songs, https://www.academia.edu/26038348/) describes a falling (trochaic/dactylic) rhythm and a shift toward trochaic patterns in the later-diffusion yogic songs.
- **[S]** Milarepa-style *mgur* often use unequal line lengths and aperiodic form (search excerpt summarizing the Godrakpa *mgur* study, McGill; https://escholarship.mcgill.ca/downloads/n009w5461).
- **[S]** Sørensen's study of the Sixth Dalai Lama's songs analyses the folk *glu* meter. His manuscript work divides stanzas of two 12-syllable lines into four 6-syllable lines (Sørensen 1990, *Divinity Secularized*, WSTB 25, Vienna).
- **[S]** Particle omission is "extremely frequent … especially in poetry where each line … has to be composed in a specific number of syllables" (Rigpa Wiki grammar notes, https://www.rigpawiki.org/index.php?title=Tibetan_Grammar_-_Syntactic_particles). The imperial rules likewise allowed free syntax within a stanza.
- **[I]** For analysis this is the key point. In verse, missing case particles (ergative, *la don*) and inserted filler particles (*ni, yang, dag, rnams*, extra *pa/ba*) are often metrical, not semantic. A grammar pass must mark them as such before the rendering pass reads emphasis or plurality into them.

**English strategies and published choices**

- **[S]** Holmes's taxonomy of verse-translation forms names four:
  - *mimetic*: imitate the source form;
  - *analogical*: use the target culture's functionally equivalent form;
  - *organic* (content-derivative): let the content generate its own form;
  - *extraneous*: impose an unrelated form.
  Holmes also coined "metapoem" for the translated poem (Holmes 1970/1988, "Forms of Verse Translation and the Translation of Verse Form," https://www.degruyterbrill.com/document/doi/10.1515/9783110871098.89/html).
- **[S]** Lefevere compares seven strategies for Catullus 64: phonemic, literal, metrical, verse-to-prose, rhymed, blank/free verse, and interpretation. He finds that each over-privileges one dimension of the original at others' expense (Lefevere 1975, *Translating Poetry: Seven Strategies and a Blueprint*, https://search.worldcat.org/title/1734142).
- **[S] Padmakara, *The Way of the Bodhisattva*.** Renders Śāntideva "in iambic lines," keeping "the traditional Tibetan structure of four-line stanzas," to recover "poetic immediacy." John Pettit's review in *Tricycle* (1997) judges that Padmakara's freer syllable use "has often been successful in evoking the lyricism," at some cost in technical precision. He contrasts it with the Wallaces' literal, footnoted, non-stanzaic version (https://tricycle.org/magazine/guide-bodhisattva-way-life/).
- **[S] 84000 verse rule.** Verse is set "line by line according to Western convention," kept "distinct from prose," and numbered. No meter is mandated (84000 Guidelines, above).
- **[S] Imperial precedent.** Tibetan translators themselves gave up Sanskrit meter for Tibetan readability (Sakya Paṇḍita on the Sragdharā Tārā praise), while preserving the stanza as the unit (Namgyal Tsetan 2024).
- **[S] Other published translators.** Brunnhölzl's *Straight from the Heart* (2007) aims at "a balance of precision and clarity" for verse pith instructions (https://www.shambhala.com/straight-from-the-heart-3273.html). Jinpa & Elsner's *Songs of Spiritual Experience* (2000) is a lyric anthology with an introduction on Tibetan verse; I could not access their stated metrical policy. Jackson's *Tantric Treasures* (OUP 2004) prints romanized Apabhraṃśa and Tibetan beside the English.
- **[I] Synthesis.** Published practice falls into three groups:
  - reader and liturgical editions use line-for-line *analogical* form (Padmakara's iambic, Nalanda's chantable lines);
  - scholarly editions use line-for-line free verse that preserves stanza and line breaks (84000, Jackson, Brunnhölzl);
  - prose is rare outside academic glossing.
  No major house attempts syllable-mimetic seven-syllable trochaics in English.
- **[I] The real trade-off** is between *line integrity* (each Tibetan line's content stays in its English line, which matters when commentaries cite lines) and *English naturalness*. Allowing free movement within the stanza while keeping stanza boundaries is the position the imperial decree itself took.

### 5. Grammar-level analysis as a stage

- **[S]** Wilson's *Translating Buddhism from Tibetan* (Snow Lion 1992) is built on "a system developed by Jeffrey Hopkins at the University of Virginia." It moves from word formation through phrase, clause and sentence patterns (https://www.shambhala.com/translating-buddhism-from-tibetan-2427.html).
- **[S]** Preston's *How to Read Classical Tibetan* (Snow Lion) diagrams "every sentence" of a 15th-century text so readers "see how the words and particles are arranged." Its appendices treat verb classes and the transitive/intransitive distinction (https://www.penguinrandomhouse.com/books/224432/).
- **[S]** Hackett's *A Tibetan Verb Lexicon: Verbs, Classes, and Syntactic Frames* (Snow Lion 2003) covers about 700 verbs and over 1,700 forms, each with syntactic frame, Sanskrit equivalents and corpus sentences. It was compiled statistically from 1,200 years of literature (https://www.shambhala.com/authors/g-n/paul-g-hackett/a-tibetan-verb-lexicon.html).
- **[S]** Tournadre argues that Classical Tibetan case markers are "transcategorial": the same particle works as a case marker, a clause connector and so on. Ergative, genitive and instrumental share surface forms, and the native *la don* group (dative, locative, terminative) has overlapping functions (Tournadre 2010, *Himalayan Linguistics*, https://www.researchgate.net/publication/288028712; Vollmann 2008, https://static.uni-graz.at/fileadmin/_Persoenliche_Webseite/vollmann_ralf/Publikationen/TE50_vollmann_2008_descr_tib_erg.pdf).
- **[S] Dictionaries in current use.**
  - Steinert's Tibetan-English-Sanskrit aggregator, integrated into Dharmamitra on 2025-10-31 (https://dharmamitra.github.io/dharmamitra-guides/news/).
  - Rangjung Yeshe and the RY Wiki (https://rywiki.tsadra.org).
  - Hopkins/UMA (https://uma-tibet.org/tibetan-language-material-dictionaries-and-glossaries/).
  - The Mahāvyutpatti and Madhyavyutpatti, the imperial Sanskrit-Tibetan glossaries (https://en.wikipedia.org/wiki/Madhyavyutpatti).
  - Also standard: Negi's *Tibetan-Sanskrit Dictionary* (CIHTS), the *Bod rgya tshig mdzod chen mo*, the Monlam dictionary, Duff's *Illuminator*.
- **[S]** 84000 translators "consult as many … source texts as possible … and note any differences" (Canti, https://84000.co/post/the-art-of-translation-inside-84000s-editorial-process-with-john-canti-and-tom-tillemans). BuddhaNexus/DharmaNexus locate citations, borrowings and parallels across Tibetan, Sanskrit and Chinese, and DharmaNexus offers sentence-level Sanskrit–Tibetan–Chinese alignment (Almogi & Nehrdich, https://www.kc-tbts.uni-hamburg.de/events/2021-02-10-almogi-nehrdich.html; Nehrdich 2025 announcement, https://list.indology.info/pipermail/indology/2025-July/060877.html; SansTib corpus, Nehrdich 2022, https://aclanthology.org/2022.lrec-1.724/).
- **[I]** The pedagogical procedure shared by the Hopkins/Wilson/Preston line, with Hackett as reference, runs as follows:
  1. Segment the words.
  2. Find the clause-final verb and its class.
  3. Use the class's case frame to assign the agent (ergative), the object (absolutive), and *la don* recipient, locative or purpose.
  4. Resolve the clause connectives (*-pas, -nas, -te/ste/de, -cing, -na, -la*) as cause, sequence, condition and so on.
  5. Read the noun phrases.
  6. Check with a commentary or the Sanskrit.
  This is my reconstruction of common teaching, not a quoted procedure.

---

## PART B: LLM/AI-assisted translation (2023–2026)

### 6. Multi-pass and agentic workflows

- **[S] Andrew Ng's translation-agent (2024)** runs translate → reflect (suggest improvements) → improve. It supports glossary injection and style steering (https://github.com/andrewyng/translation-agent).
- **[S] MAPS (He et al., TACL 2024)** mines keywords, topics and self-generated demonstrations, generates several candidates, then selects one by quality estimation (https://aclanthology.org/2024.tacl-1.13/).
- **[S] Briakou, Luo, Cherry & Freitag (WMT 2024)** use four stages: research, draft "prioritizing faithfulness," refine for fluency "such that the text works on its own," and proofread in a *fresh* conversation. In their ablation:
  - **refinement** gave the biggest gains;
  - research and refinement were complementary;
  - proofreading added only "modest average improvements," and only one language clearly benefited.
  They also criticize TransAgents' human evaluation, which gave annotators neither the source nor the reference (https://aclanthology.org/2024.wmt-1.123/).
- **[S] Wu, Aycock & Monz (EMNLP 2025, "Please Translate Again")** find "no clear evidence that performance gains stem from explicitly decomposing the translation process via CoT." Simply asking the model to "translate again" and self-refine matched or beat the four-step method. "Imposing human biases may lead to suboptimal outcomes." Tested on GPT-4o-mini and Gemini 2.0 Flash, WMT24++, into 8 high-resource languages (https://arxiv.org/abs/2506.04521).
- **[S] TransAgents (Wu et al., 2024)** uses editor, translator, localizer and proofreader agents. Readers preferred its output over references for literary text despite lower d-BLEU (https://aclanthology.org/2024.emnlp-demo.14/; caveat above).
- **[S] TEaR (Feng et al., NAACL Findings 2025)**: translate → estimate (MQM-style errors) → refine. Feeding explicit error information back improves translations (https://aclanthology.org/2025.findings-naacl.218/). Ki & Carpuat (NAACL Findings 2024) show that post-editing guided by MQM error annotations helps (https://aclanthology.org/2024.findings-naacl.265/).
- **[S]** Without external feedback, LLMs often fail to self-correct reasoning and can get worse (Huang et al., ICLR 2024, https://arxiv.org/abs/2310.01798).
- **[S] Reasoning models (2025).** Large reasoning models do better "in semantically complex domains, especially in long-text and high-difficulty" translation (https://arxiv.org/abs/2505.19987). DRT-o1 targets metaphor and simile with a translator–advisor–evaluator loop (https://aclanthology.org/2025.findings-acl.351.pdf).
- **[S] Translationese.** Supervised fine-tuning biases LLMs toward "overly literal" translationese. Polishing the references reduces it (Li et al., ACL 2025, https://arxiv.org/abs/2503.04369).
- **[I]** For a low-resource classical source, the Wu et al. null result for decomposition is the most important caveat. It was measured on *high-resource, out-of-English* pairs, where the model already parses the source well. For Classical Tibetan the bottleneck is parsing, so an explicit analysis pass is more likely to pay off there. But it should produce *checkable structure*, not free-form "research notes," because errors in the decomposition carry forward into later passes.

### 7. Dictionary- and terminology-augmented translation

- **[S] DiPMT (Ghazvininejad et al., 2023)** adds dictionary options for selected source words. Gains averaged about 1 BLEU on 10 low-resource languages and about 9.4 BLEU out of domain (https://arxiv.org/abs/2302.07856).
- **[S] Chain-of-Dictionary (Lu et al., EMNLP 2024)** chains multilingual dictionary entries into the prompt. It gave large gains for low-resource FLORES directions, up to 13× chrF++ for one pair (https://aclanthology.org/2024.emnlp-main.55.pdf).
- **[S] Moslem et al. (EAMT 2023):** supplying translation-memory fuzzy matches in context adapts output to approved terminology and style, and beats random or zero-shot context (https://aclanthology.org/2023.eamt-1.22/).
- **[S] Aycock et al. (ICLR 2025):** for Kalamang, "almost all improvements stem from the book's *parallel examples*." There is "no evidence that long-context LLMs can make effective use of grammatical explanations" (https://arxiv.org/abs/2409.19151).
- **[S] MITRA-zh-eval (Nehrdich et al., NLP4DH 2025):** retrieval-augmented generation improved Buddhist-Chinese→English quality for the top commercial models (https://aclanthology.org/2025.nlp4dh-1.12/).
- **[I] Implications:**
  - Inject *glossary entries and parallel passages* (aligned Tibetan–English or Tibetan–Sanskrit sentences, prior approved renderings).
  - Do not inject long prose grammar explanations. Grammar knowledge should drive a structured parse the model fills in, not sit in the prompt as reading material.
  - Give dictionary hints as *options with senses*, not single forced glosses. Forced one-to-one glosses reproduce the Hopkins-style idiosyncrasy and break the imperial polysemy rule.

### 8. Low-resource and classical-language MT for Buddhist texts

- **[S] MITRA (Nehrdich & Keutzer, arXiv Jan 2026).** 1.74M parallel Sanskrit/Chinese/Tibetan sentence pairs. Gemma 2 MITRA-MT reaches state of the art among open models for translation into English, and a companion embedding model (MITRA-E) does semantic retrieval (https://arxiv.org/abs/2601.06400; corpus: https://github.com/dharmamitra/mitra-parallel).
- **[S]** On 2026-08-23 Dharmamitra switched to a self-trained, self-hosted **Mitra Qwen3.5** translation model, said to "outperform much larger" systems (https://dharmamitra.github.io/dharmamitra-guides/news/). There is also a Qwen3.5-9B-based tagger for Tibetan segmentation and POS tagging (https://github.com/dharmamitra/mitra-bo-zh-tagger).
- **[S]** Earlier open work: Nehrdich et al. 2023, NLP4DH (https://aclanthology.org/2023.nlp4dh-1.29.pdf); MLotsawa, a T5-based Tibetan→English model with UVA THL (https://github.com/billingsmoore/MLotsawa).
- **[S] DharmaBench (Golan Hashiloni et al., IJCNLP 2025), Hamburg/Reichman.** 13 classification and detection tasks: similes, quotations, root-text↔commentary matching, verse/prose, meter. Gemini 2.5 Pro scored best (about 76 F1 on Tibetan). Models fail on root-text/commentary matching when context is truncated. "No single model performs well across all tasks." There are **no generative or translation tasks** (https://aclanthology.org/2025.ijcnlp-long.114.pdf).
- **[S]** A survey of Tibetan NLP notes that the lack of word boundaries, frequent honorifics and case markers complicate processing. It focuses mostly on modern Tibetan (Huang et al. 2025, https://arxiv.org/abs/2510.19144).
- **[S] Pāli as a sister case.** On PaliBench (1,700 passages, three reference translations), most models converge toward one translator's renderings, "potentially flattening legitimate interpretive diversity" (Metzger & Phophichit 2026, https://arxiv.org/abs/2605.16881).

### 9. Quality evaluation

- **[S] GEMBA-MQM (Kocmi & Federmann, WMT 2023):** GPT-4 marks MQM error spans without references (https://aclanthology.org/2023.wmt-1.64/).
- **[S] Buddhist domain:** GEMBA "shows the strongest correlation with human judgment," well ahead of BLEU and chrF (MITRA-zh-eval 2025, above).
- **[S] Classical-text triage (Metzger, arXiv Sept 2026).** Over 15,493 Pāli passages:
  - reviewing the top 10% by GEMBA risk caught **81.6%** of major errors (AUC 0.970);
  - back-translation chrF caught 67.1% (AUC 0.824);
  - source novelty and peer disagreement were weaker;
  - "evaluator strength matters."
  Major errors are those that "materially change the meaning, omit essential content, reverse polarity, assign agency or roles incorrectly" (https://arxiv.org/abs/2609.14963).
- **[S] Drift and severity.** In a multi-reference Pāli audit of GPT-5.5, Claude Sonnet 4.6, Gemini 3.1 Pro and Grok 4.3, drift from the reference envelope predicts *severity*: major errors rose from 7.9% to 51.6% across drift bands (Metzger et al. 2026, https://arxiv.org/abs/2606.01136).
- **[S] Judge bias.** LLM judges favor their own generations (Panickssery, Bowman & Feng, NeurIPS 2024, https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf).
- **[S] Persistent errors.** Document-level LLM literary translation still shows "critical errors … including occasional content omissions" (Karpinska & Iyyer, WMT 2023, https://aclanthology.org/2023.wmt-1.41/). Hallucinations concentrate in low-resource directions (Guerreiro et al., TACL 2023, https://aclanthology.org/2023.tacl-1.85/).
- **[I]** The meaning-error categories Metzger uses (polarity reversal, wrong agency or roles, omission) are exactly the classes that Tibetan ergative/absolutive and negation morphology make risky. A checker pass should check these explicitly, clause by clause, against the parse, rather than give a holistic score.

### 10. Known LLM failure modes on Classical Tibetan

**[S] What is documented:**
- Tokenization and segmentation are weak for Tibetan, which is why DharmaBench capped inputs at 2,000 characters (DharmaBench §3.3).
- Commentary/root alignment is fragile under truncation (DharmaBench).
- Models converge on a dominant translation tradition (PaliBench).
- 84000 warns of "convincing falsities."
- Jinpa's 2014 list of *human* failure modes (word-division errors, "blind guesswork," reverse etymologizing, harmonizing old and new terms) is a ready-made checklist that applies equally to models.

**[I] Not yet documented in the literature**, but predicted from the grammar plus the general MT findings:
- *ergative/genitive confusion* (shared forms) → agent and possessor swapped;
- *la don* collapse → recipient, location and purpose all flattened to "to/in";
- *connective smoothing* → *-pas* (cause), *-nas* (sequence) and *-te* (loose continuation) all become "and," or invented "therefore"s appear;
- *negation scope* (*mi/ma/med/min* inside nominalized clauses) dropped or misplaced;
- *verse filler read as content* (*ni* as "indeed," *rnams* as an emphatic plural);
- *elided arguments* filled in with the wrong referent;
- *honorific collapse* (*gsungs* vs. *smras*) erasing who is speaking to whom;
- *hallucinated Sanskrit* back-forms (which 84000 explicitly forbids);
- *ambiguity smoothing*, where a deliberately polysemous line (common in *mgur*) gets one reading without a flag.

All of these should be logged and tested, not assumed.

---

## Design implications for the multi-pass pipeline

**Evidence-based shape.** Briakou et al. found refinement to be the high-value stage and drafting for faithfulness then refining for fluency to work. Wu et al. found free-form decomposition adds little for high-resource pairs. Aycock et al. found parallel examples beat grammar prose. GEMBA-style span checking was the best error detector in both Buddhist-domain and classical-text studies. Together these support a short pipeline with a *structured* analysis pass, a faithful draft, a fluency/style pass, and a separate span-level fidelity check. A long chain of role-play agents is not supported by the evidence.

**Pass 1: Analysis (construal).** Output is structured data, not prose.
- Segmentation, with a tagger (Mitra) cross-check where available.
- For each clause:
  - the final verb and its Hackett-style class;
  - argument roles from the case particles (agent, patient, *la don* function);
  - the connective type (cause, sequence, condition, concession);
  - negation and its scope;
  - honorific level of the verbs;
  - flags for elided arguments.
- In verse: mark which particles are metrical filler and which case markers are elided.
- Glossary hits with *sense options*.
- 1–3 retrieved parallel passages or prior approved renderings (DharmaNexus/MITRA-style).
- Citation identification.
- Explicit **ambiguity flags**, with alternative construals kept, never silently resolved.
- The MITRA literal output serves as a cross-check, not an arbiter.

**Pass 2: Faithful rendering.** Draft from Tibetan plus the construal object, prioritizing fidelity (Briakou's "draft" stage).
- Preserve every connective relation and negation.
- Keep stanza and line integrity for verse.
- Use glossary terms consistently, while allowing context-sensitive senses for polysemous terms (the imperial rule, Jinpa).
- No brackets except in academic mode.

**Pass 3: Audience and style adaptation (skopos).** One parameterized pass, not four separate pipelines:

| Mode | Treatment |
|---|---|
| Academic | documentary/thick: IAST, Wylie in notes, bracket interpolations allowed, commentary-sourced glosses |
| New practitioner | instrumental: 84000-style plain English, Sanskrit naturalized, epithet strings simplified, no apparatus |
| Seasoned practitioner | instrumental, but technical terms kept stable and lightly foreignized |
| Hybrid | instrumental text plus endnotes |

- Verse: analogical form (counted lines with a stable length for liturgy, free-verse line-for-line for citations), with freedom to rearrange inside the stanza (imperial rule, Padmakara).
- Register calibrated per genre using the map in §3.

**Pass 4: Fidelity check (separate context, ideally a different model).**
- MQM/GEMBA-style error spans against the *construal object*, clause by clause, checking polarity, agency/roles, omission, connective type, honorific direction and terminology.
- Optionally a back-translation of flagged clauses as a secondary signal (weaker than GEMBA, but independent).
- Errors go back as *specific* feedback for a single targeted revision (TEaR, Ki & Carpuat). Do not iterate open-endedly.

**What the evidence says NOT to do:**
1. **Do not let the model first-draft and grade itself in one context.** Self-preference bias (Panickssery) and failed intrinsic self-correction (Huang) argue against it. Use a fresh context or a different model for checking, as Briakou did for proofreading.
2. **Do not load long grammar explanations into the prompt** and expect them to be used (Aycock). Turn grammar into fields the analysis pass must fill.
3. **Do not run unstructured "research" decomposition** that later passes treat as fact. Decomposition errors propagate (Wu et al.).
4. **Do not stack many agent roles.** There is no evidence they beat draft → refine → check, and their evaluations have been methodologically weak (Briakou's critique of TransAgents).
5. **Do not force one-to-one glossary equivalents** across senses (sgra sbyor; Jinpa). Do not invent Sanskrit back-forms (84000).
6. **Do not resolve ambiguity silently** or converge on one canonical translator's reading (PaliBench). Flag it.
7. **Do not use MT output, MITRA included, as the arbiter of meaning.** 84000 bars AI first drafts of canonical texts and warns of "convincing falsities." Keep humans in the loop and record the model, prompt and date, as 84000's policy requires.
8. **Do not rely on BLEU/chrF** for quality. GEMBA-style judgment correlates far better in the Buddhist domain (MITRA-zh-eval).
9. **Do not treat verse particles at face value** or coerce English stress to hit a syllable count. Tibetan translators themselves traded meter for intelligibility (Sakya Paṇḍita), and no major English house mimics Tibetan syllabics.
