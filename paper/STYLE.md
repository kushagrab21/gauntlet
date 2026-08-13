# STYLE.md — the register of the benchmark paper, as an editing contract

Derived from two readings of *Who Decides When the Task Is Done?* (Bhatnagar,
July 2026), 6,688 words across ten section files. The counts below are measured
over those files with tables and figures stripped, so they are checkable rather
than impressionistic.

**This document governs wording.** Where it conflicts with `LANGUAGE.md`, see
§9, which records the conflict rather than resolving it.

---

## 1. The sentence

The author writes **long sentences, not short ones**. Mean length runs 21 to 31
words by section; the longest is 50. A typical sentence carries a claim and the
reason for it in one breath, joined by `so` or `because`.

The joins are done with a small, fixed set of words. Across the whole paper:
`so` 31, `which` 28, `rather than` 21, `but` 19, `because` 17. And across the
whole paper: **`however` 0, `moreover` 0, `furthermore` 0, `crucially` 0,
`notably` 0, `importantly` 0, `remarkably` 0, `arguably` 0, `obviously` 0.**
There are no stock discourse markers anywhere. Causation is carried by `so` and
`because`, contrast by `but` and `rather than`, and nothing is carried by a
signpost adverb.

**Anchor.**

> The p-value of 0.0078 rejects the null hypothesis for the weak model, so the
> mode difference is statistically real and not a chance pattern across 8 tasks.

Thirty words. The test, the verdict, and the boundary of the verdict, joined by
one `so`. No adverb tells the reader it matters.

## 2. Punctuation, and what it says about asides

**Zero em-dashes in 6,688 words. Zero semicolons. Five parentheses.** The only
`--` in the paper is the en dash inside the compound `model--task pair`.

This is the single most distinctive fact about the register, and it is not a
typographic preference. It means the author does not have asides. A qualifier
either earns a clause joined by `so`, `because` or `which`, or it earns its own
sentence, or it is cut. There is no third option and no punctuation available
for one.

Colons are the exception and are used heavily, 138 times, almost always as
*claim, colon, the evidence for it*. That is the author's one device for
attaching an explanation without a new sentence.

## 3. Paragraphs are labelled by their job

Forty-four run-in bold labels across the paper. The label names the paragraph's
**function**, not its topic: `Bridge from Experiment 1:`, `Preconditions:`,
`Predictions:`, `Results:`, `Reading the table:`, `Statistical test:`,
`Scoring the predictions:`, `Patterns in the table:`, `The floor:`,
`Replication:`, `Cost:`, `Deviations:`, `Inference:`.

A reader can navigate the paper by labels alone and know what each block is for
before reading it. When editing, if a paragraph's label does not describe what
the paragraph does, the paragraph is wrong, not the label.

## 4. How a statistic is introduced

Three italic blocks, always in this order, never merged.

- **Definition** — what the test is and why it applies here, in plain words,
  with the null stated as a sentence about the world rather than as notation.
  The author will spend sixty words explaining what a discordant pair is.
- **Calculation** — the arithmetic, shown. `p = 2 × (1/2)^8 = 0.0078`.
- **Inference** — what the number licenses, and immediately what it does not.

The Inference block routinely contains a second fact the p-value does not carry:
`b = 0` is read as "binding never lost a single task that advisory had solved",
which is a separate observation from the significance.

## 5. Number series get a fixed rhythm

When a column of the results table is the finding, the author states the series,
names its shape, then draws the inference, in three sentences:

> The false-DONE series is 0, 8, 8, 15, 16, 4, 1. The pattern is a hump: false
> claiming is absent at the top, frequent in the middle, and nearly absent again
> at the bottom.

This rhythm appears six times. It is worth preserving exactly, because it is
what lets a reader check the author's reading against the numbers in one glance.

## 6. Failed predictions

Reported first, at the same length as successes, and named as failures without
cushioning. The registration is invoked as the reason this is possible, not as
an excuse.

**Anchor.**

> Three of four confirmatory predictions failed, and reporting them as failures
> rather than adjusting them afterwards is what the preregistration was for.

Note what is absent: no "surprisingly", no "while disappointing", no paragraph
explaining that null results are valuable. The fact is stated once.

## 7. Limitations

A numbered list. Each item is a bolded noun phrase naming the weakness, then two
or three sentences that concede it and bound it. The section opens by saying
where the list comes from and why it is there.

**Anchor.**

> Every limitation below is drawn from the experiment ledger, and stating them
> here is cheaper than having a reviewer state them for us.

The bounding move is the important one and it recurs: a limitation is admitted,
then its blast radius is stated. "This inflates absolute success rates but not
the advisory-versus-binding difference, which is what every conclusion rests
on." The concession never floats free.

## 8. When a number is impressive

The number is stated and the sentence ends. "Binding lifts a weak model by 9.2
points while leaving a strong one unchanged." "A difficulty at which Qwen
false-claims 40% of the time did not extract a single false claim from the
strongest model."

There is no intensifier, no restatement in a second sentence, and no
observation that the result is notable. Where the author does add a sentence
after a big number, it is to *reduce* the reader's confidence, not to raise it:
"The gap is one task in each direction and should not be over-read."

## 9. The conflict with LANGUAGE.md, recorded and not resolved

`LANGUAGE.md` carries the visualisation's round-4 rules. Two of them contradict
the benchmark register directly, and this instruction to match the benchmark
does not by itself repeal them.

| | `LANGUAGE.md` | the benchmark |
|---|---|---|
| sentence length | "short declarative sentences, one clause one fact" | mean 21–31 words, clauses joined by `so` and `because` |
| inversions | "no rhetorical inversions, not `not X but Y`" | uses them, sparingly and load-bearing |

On inversions the two are closer than they look, and the distinction is the
editorial judgment this pass turns on. The author's inversion is grounded in the
same sentence:

> This is neither laziness nor defiance of feedback, because the mistake happens
> earlier than the feedback.

The inversion is doing work: it rules out two readings a reader would otherwise
reach for, and the `because` clause pays for it immediately. The failure mode to
strike is the *ungrounded* inversion, which restates the previous sentence in a
more quotable shape and offers no reason. The test is whether the sentence
survives deleting the negated half. If it does, the negated half was ornament.

The sentence-length conflict is real and unresolved. See `EDIT_LOG.md`
DECISIONS D1.

## 10. The checklist this pass applies

Strike or rewrite:

1. Any em-dash aside. The register has none; there is no budget for one.
2. Any semicolon. Same.
3. Any stock transition: however, moreover, furthermore, crucially, notably,
   importantly, remarkably, strikingly, in essence, it is worth noting.
4. Any epigram that restates the previous sentence in quotable form.
5. Any ungrounded `not X but Y`, by the deletion test in §9.
6. Any rule-of-three flourish where the third item carries no new content.
7. Any drama adverb, and any intensifier attached to a number.
8. Any hedge attached to a claim that has an exact number behind it.
9. Any anthropomorphic metaphor for the model beyond the paper's own defined
   vocabulary of claiming, seeing, guessing and telling.
10. Any sentence a reader can take two ways.
11. Any paragraph whose job label does not match what it does.

Preserve:

12. Long sentences joined by `so`, `because`, `which`, `rather than`.
13. The Definition / Calculation / Inference order.
14. The series / pattern / inference rhythm.
15. `n/N` with the denominator visible, and signed effects.
16. `I` for the author's own design decisions, confined to the narrative
    sections. `we` for what the paper does.
17. The bounding sentence after every concession.
