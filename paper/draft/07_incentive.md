# 7. It is not the incentive

**Bridge from Experiment 2.** If the model can tell which tasks are risky and
claims on some of them anyway, the next candidate is the criterion it applies.
Under any signal-detection reading of the decision point, where the model is
weighing an uncertain cue against the cost of being wrong, the criterion moves
with the ratio of the payoffs. So one way to test whether the model is applying
a criterion of that kind is to state a different payoff and see whether its
behaviour moves.

**Preconditions.** One model played the first 72 ids of the same frozen order
under SIGMA, which is CTRL plus one sentence appended to the rules: a `DONE`
that turns out to be correct scores higher the fewer hidden stages the model has
seen, and a `DONE` that turns out to be wrong scores the same as running out of
submissions. Two clauses rather than one, because a reward with no stated cost
is an instruction to claim rather than a payoff. The second clause is true of
this harness, since a wrong claim and an exhausted submission bound are both
terminal and both unsolved. 72 episodes at $6.17, compared against the CTRL
record on the same ids.

**The standing caveat.** The payoff is stated and never delivered. Nothing in
the harness pays a bonus and no score is ever shown to the model, so an effect
here would be evidence that behaviour is sensitive to a described payoff
structure rather than evidence about a real one. This caveat travels with every
result in this section.

**The power statement, quoted before the result.** The registration recorded
this design as having 0.80 power at a shift of 0.155, 0.50 at 0.10 and 0.18 at
0.05. A ten-point shift was a coin flip here and a five-point shift was
invisible, and the registration said in advance that both would land in the
disconfirmed cell.

**Predictions.** C1: the stated payoff makes the model claim on more tasks. C2:
the extra claims come from tasks where it had been right to withhold, so
accuracy among claims collapses. C5: the working phase has not drifted between
the two days on which the arms ran.

**Results.** Table 5 gives the two arms, and the second panel of Figure 5 draws
the tasks.

<!--TAB:T5-->

**Reading the table.** 71 tasks were played under both. On 41 the model claimed
under both and on 24 under neither. Six tasks changed answer, and five of them
changed against the prediction.

**Statistical test.**

*Definition.* This is the same paired test as Experiment 2, reading only the
tasks whose answer differs between the two arms, and it is one-sided in the
registered direction, which here is an increase in claiming under the payoff.

*Calculation.* The split is 5 against 1 on 6 discordant pairs, and the one-sided
exact value in the registered direction is p = 0.9844.

*Inference.* C1 is disconfirmed. The p-value is as far on the wrong side of 0.5
as six observations can put it, and claiming fell rather than rose.

**What the fall does not mean.** The reverse-direction test on the same six
pairs returns p = 0.1094. That figure was not registered and is quoted only so
it cannot later be told as though it had been, and it is quoted at all because
it is the number that stops the decrease being over-read. Six discordant pairs
cannot establish a direction either way. What this experiment licenses is a
bound in one direction: a large increase in claiming is ruled out for the
strongest payoff statement this harness can make while keeping the statement
true, on this model, this corpus and this prefix, and nothing else is
established.

**Headroom existed and was not taken.** 25 of the 71 tasks were not claimed at
the decision point under the control, and the registration recorded that count
in advance as the room an increase had to grow into. Under the payoff the model
claimed on exactly one of them.

**Scoring the predictions.** C1 disconfirmed. C2 disconfirmed, since accuracy
among claims did not collapse. C5 confirmed on both metrics, the second by one
guess.

**Inference.** Two descriptions of the payoff structure have now been given to
this model, the stage count in Experiment 2 and the reward here, and neither
moved the claim rate by an amount either design could see. Both put the
information or the incentive in the rules, at the start of the episode, and
asked the model to carry it to the decision point. Experiment 4 stops asking it
to carry anything.
