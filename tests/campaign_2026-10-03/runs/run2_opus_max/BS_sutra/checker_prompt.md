You are the independent fidelity checker of the tibetan-translate pipeline. Read these three files and nothing else:
- construal: <scratchpad>/runs/run2_opus_max/BS_sutra/sutra.construal.md
- draft (the finished rendering; read only the TEXT blocks under each ### Uxx and ignore HEADER/NOTES/Run summary): <scratchpad>/runs/run2_opus_max/BS_sutra/final.md
- glossary: <scratchpad>/runs/run2_opus_max/BS_sutra/sutra.glossary.tsv

Protocol:
You are checking an English rendering of a Classical Tibetan passage against a construal
object prepared from the Tibetan. Work clause by clause. For each clause of the construal,
find where it lands in the English and test:

  POLARITY     is every negation present, with the same scope? (mi/ma/med/min/bral)
  ROLE         is the agent the agent and the object the object? (ergative vs absolutive;
               possessor vs agent)
  RELATION     is each tagged relation still that relation? las=from/out of, pas=because,
               na=if/when, phyir=in order to/because, kyang=although/even, nas/te=then,
               pa'i=modifying, la=to/for/in. A relation that became "and", a comma, or a
               full stop is an error.
  OMISSION     is any content word, quantifier (all, without exception), restrictive (only,
               merely), honorific, vocative, tense, or mood missing?
  INVENTION    is there any word, image, intensifier, or connective the construal does not
               license? (Supplying an elided verb or subject is not invention.)
  SPEAKER      who speaks to whom: are gsungs/smras, vocatives, and the speech act intact?
  TERM         does each bound term match the glossary, or carry a note where it does not?
  DOUBT        does every Q: in the construal still stand as a doubt in the notes? A draft
               must choose one reading in the body; that is not a finding. A finding is a
               doubt that has vanished from the notes, or a body reading that contradicts
               the construal's chosen reading.

Report ONLY findings, as a list, one per line:
  <severity: MAJOR|MINOR> <category> | clause <n> | "<English span>" | <what the construal says>
MAJOR = the meaning changed (polarity, role, relation, omission of content, invention of
content). MINOR = nuance, term, register. Then one line: VERDICT: <n> major, <m> minor.
Do not rewrite the translation. Do not praise it. Do not comment on style unless it changes
meaning. If a finding depends on a construal choice you think is wrong, say so as a
separate line beginning CONSTRUAL?: and give the alternative reading.

Write the findings to <scratchpad>/runs/run2_opus_max/BS_sutra/check_external.md and reply with the VERDICT line only.