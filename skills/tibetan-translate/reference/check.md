# Pass 4 — the fidelity check

The check tests the page against the construal sketch, clause by clause, and returns error spans,
not a rewrite. In pipeline v2 it runs **in-context after a clean break**: re-read the sketch from
the file, then apply the protocol of §2 to each unit, fix what fails, one round, and write
`Check: in-context, <n> fixed`.

A **spawned fresh-context checker** is no longer the default. Measured 2026-10-03/04: on the pages
where one ran it caught none of the errors the independent judges later found, raised one or two
false findings a page, and cost 55–85k tokens whatever it checked; the in-context check found the
same minors. Spawn one only when the user asks for an independent check, with the inputs of §1 and
the protocol of §2, one call per page.

## 1. What a spawned checker receives (when asked for)

1. The construal file (its SOURCE field holds the Tibetan; the Tibetan need not be repeated).
2. The draft file (after the style pass), one block per unit, ids matching the construal.
3. The project glossary file or excerpt.
4. The protocol below, verbatim.

Pass **file paths**, not pasted text: it keeps the main context small, and the checker reads only
what it needs. Nothing else: not the transcript, not the dictionary report, not earlier drafts.

## 2. The protocol (paste into the checker's prompt)

```
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
```

## 3. What the drafter does with it

- Apply one targeted revision for every MAJOR and for the MINORs that are cheap.
- A `CONSTRUAL?:` line is a doubt: resolve it from the Tibetan, update the construal file, and
  record a `Q:` if it remains open.
- Rerun the gates of `english.md` on the revised sentences only.
- One round. A second round only if a MAJOR touched a relation and the revision reshaped the
  sentence.
- In the output, one `Check:` line: what was found and what changed ("Check: 1 major (pas rendered
  as 'and', restored as 'because'); 2 minor").

## 4. Spawning it (only when the user asks)

Agent tool, `subagent_type: general-purpose`, model Opus, fresh context, `run_in_background: false`
because the revision depends on it. The prompt is the four items of §1 (paths + protocol) and
nothing else. One call per page; expected cost ~50–60k tokens, nearly all harness overhead.
