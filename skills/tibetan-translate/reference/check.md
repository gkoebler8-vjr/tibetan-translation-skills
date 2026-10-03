# Pass 4 — the fidelity check (fresh context)

The drafter does not grade its own draft: self-preference bias and failed self-correction are the
documented failure (research brief §9). The check runs in a new context, ideally on a different
model, with the construal as the reference. It returns error spans, not a rewrite.

## 0. When to spawn, and what it costs

A spawned checker costs **~50–60k tokens** whatever it checks, because the subagent carries the
harness's own system context; the check itself is 2–5k. So the checker is spawned **once per page**
(5–12 units, all construals and drafts in two files), not per unit. A single unit gets an
in-context check after a clean break (re-read the construal file, then run the protocol), marked
`Check: in-context`, unless the user asks for the independent check.

## 1. What the checker receives

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

## 4. Spawning it

Agent tool, `subagent_type: general-purpose`, model Sonnet for a page of routine units, Opus for a
page with hard construals, fresh context, `run_in_background: false` because the revision depends
on it. The prompt is the four items of §1 (paths + protocol) and nothing else. Expected cost:
~50–60k tokens per spawn, nearly all overhead, which is why it is batched.

If the Agent tool is not available, do the protocol in-context after re-reading the construal
from the file, and say "Check: in-context" in the output.
