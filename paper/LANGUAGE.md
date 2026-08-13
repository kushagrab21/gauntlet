# LANGUAGE.md — the writing rules, carried from the visualisation's round 4

These are the rules the explainer page at `declare/viz/trajectories.html` was
rewritten under, carried over verbatim in force. They bind every word of the
paper, including captions, table headings, figure labels and the abstract.

---

## The rules

1. **Sentences carry a claim and its reason together.** *Amended by owner
   ruling, decision D1 in `EDIT_LOG.md`.* The original round-4 rule read "short
   declarative sentences, one clause carrying one fact", and it is withdrawn for
   this paper. The benchmark's register is the target, and its characteristic
   sentence runs 21 to 31 words, joining a claim to the reason for it with `so`
   or `because`. That length is a precision device rather than a lapse: it keeps
   a verdict and the boundary of that verdict in one sentence, so neither can be
   quoted without the other. Join clauses with `so`, `because`, `which` and
   `rather than`. Do not join them with a dash, a semicolon or a parenthesis,
   which rule 3 still forbids and which the benchmark uses zero times in 6,688
   words.

2. **Define before use.** No term appears before the sentence that defines it.
   This applies across the whole paper in reading order, not per section: a term
   defined in section 5 may not be used in section 3. The glossary ordering rule
   from the visualisation is the model — no entry uses a term defined below it.

3. **No em-dash asides.** An aside worth making is worth its own sentence. An
   aside not worth its own sentence is worth deleting.

4. **No aphorisms and no rhetorical inversions.** Not "the model does not know
   when it does not know". Not "it is not X, it is Y". Not "the question is not
   whether, but which". State the finding.

5. **Plain words.** Prefer the short word. `hidden` over `withheld` where both
   fit; `wrong` over `erroneous`; `showed` over `demonstrated`; `about` over
   `regarding`. Technical terms are allowed once defined, and only where a plain
   word would lose the meaning.

6. **Active voice.** "The harness released the next stage", not "the next stage
   was released". Passive is allowed where the actor is genuinely unknown or
   genuinely irrelevant, which is rare.

7. **Denominators before rates.** Never a bare percentage. Write `71 of 118`
   before, or instead of, `0.6017`. Where both appear, the count comes first in
   the sentence and in the table.

---

## What these rules mean for this paper in particular

**Rule 4 is narrowed to a test, not a ban.** *Decision D2 in `EDIT_LOG.md`.*
The previous paper's abstract ends "the model does not know when it does not
know", and that sentence is an inversion. The benchmark uses the device
sparingly and grounds it in the same sentence, as in "this is neither laziness
nor defiance of feedback, because the mistake happens earlier than the
feedback". The test to apply: delete the negated half. If the sentence still
says what it needs to, the negated half was ornament and goes. If deleting it
lets a reader reach a reading the sentence existed to rule out, it stays. An
inversion with no `because` behind it does not survive this test. Aphorisms that
restate the previous sentence in a more quotable shape are still banned outright,
and so is every other item in rule 4.

**Rule 2 is the expensive one.** This paper's vocabulary is deep: task, stage,
release, episode, turn, submission, claim, the decision point, arm, run,
experiment, benign, enforcing, churn floor. The order that satisfies rule 2 is
the order the visualisation's glossary already found, and section 3 should
introduce them in it:

> task → hidden convention → stage → release → episode → turn → submission →
> claim → the decision point → arm → run → experiment → paired comparison →
> task that changed answer → benign → enforcing → churn floor

**Rule 7 is already enforced mechanically** in the tables:
`tables/make_tables.py:check_language()` fails the build if a column heading
carries a project code, and every table prints counts beside their denominators.
No such check exists for the prose, so it is on the writer.

**Naming the arms.** The paper should not print `ctrl`, `warn`, `sigma`,
`ctrlprime` or `count` as bare tokens in prose. Use the plain descriptions the
tables use — "the control", "the warned rules", "the rules that stated a
reward", "the control played a second time", "the counted rules" — and give the
short code once, in parentheses, in section 3 where the arms are defined.

**One thing rule 1 must not cost.** Registered clauses are quoted, and they are
long. Quoting a registration verbatim is exempt from rules 1, 3 and 5, because a
paraphrased clause is no longer the clause that was frozen. Mark quotations as
quotations and keep them exact.

---

## A short list of phrases to avoid, drawn from the source material

The write-ups this paper is built from carry a house style that these rules
forbid. When lifting a sentence from them, rewrite it.

| in the write-ups | in the paper |
|---|---|
| "the failure is not that it cannot tell, it is the threshold it applies" | "the model can tell which tasks are safe. It claims anyway." |
| "a pre-registration that only reports its wins is not a pre-registration" | delete, or state the practice plainly |
| "that defence is now spent" | "experiment 2 removed that explanation" |
| "the line drawn from experiment 1 is dead" | "experiment 2 did not find the effect experiment 1 suggested" |
| "it knows and claims anyway" | "the model had the information and claimed anyway" |
| "the arithmetic, done for it" | "the subtraction, printed where the model decides" |

---

## Checking

There is no automatic checker for prose. Before the draft is considered done,
read it once for each rule separately. The two that fail most often in this
material are rule 3 (the source write-ups are full of em-dash asides) and rule 4
(the source write-ups end most sections on an inversion).
