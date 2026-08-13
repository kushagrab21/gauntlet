# 5. Capability makes it worse

**Bridge from the decision point.** Section 4 located the failure without saying
whose failure it is. A state where wrong claims concentrate could be a property
of one weak model, in which case the finding is about that model, or a property
of the channel, in which case it is about any agent given one. Experiment 1
separates those by holding the tasks and the rules fixed and varying only the
model. If wrong claims are a weakness, the strongest model should make the
fewest.

**Preconditions.** Experiment 1 ran three models of different strength over the
same 68 tasks in the same frozen order, under two arms: BIND, with no way to
declare the work finished, and ADV, with the claim channel open. The models are
ranked by the programme's own capability labels, fixed before the run and not
derived from these results. Everything except the model and the arm is held
fixed, so the scale follows from the design: 3 models × 2 arms × 68 tasks, which
returned 407 completed episodes once one transport failure is excluded, at
$16.74.

**Predictions.** Four were registered. P1: the strongest model produces more
than zero wrong claims in the hardest band, where tests are staged. P2: the
benefit of removing the channel is largest for the middle model. P3: that
benefit shrinks in the hardest band, because forcing persistence cannot supply
information that was withheld. P4: the benefit tracks the count of wrong claims
across models.

**Results.** Table 3 has one row per model, ordered strongest to weakest, with
the tasks it claimed and the claims that were wrong.

<!--TAB:T3-->

**Reading the table.** Figure 4 draws both columns. They move in opposite
directions. Claiming rises
steeply with capability, from 37 of 68 to 57 of 68 to 67 of 68. Accuracy of the
claim falls, from 0 wrong to 2 wrong to 4 wrong, which as a share of each
model's own claims is 0.0000, then 0.0351, then 0.0597. The strongest model is
better at the work and more willing to certify it, and the certification is
where the new error lives.

<!--FIG:F5-->

**Statistical test.**

*Definition.* P1 asks whether an event occurs at all, against a baseline that
recorded zero such events at every difficulty, so the registered form is a
threshold on a count rather than a comparison of rates. It is confirmed if at
least one frontier model shows one or more wrong claims in the hardest band.

*Calculation.* The strongest model produced 4 wrong claims, all of them in the
hardest band, and 0 in the easy band where every enforcing test is visible from
the first turn.

*Inference.* P1 is confirmed. The confirmation is evidence about existence and
not about a rate, because a count of 4 cannot support a magnitude, and the
registration said so in advance. No claim about how often this happens is made
here and none should be made downstream of these counts.

**Scoring the predictions.** Three of the four did not confirm. P2 is recorded
as neither confirmed nor disconfirmed, because its two registered clauses did
not cover the whole range of outcomes and the run landed in the gap between
them: the predicted ordering held, but the middle model's test rested on a
single task that changed answer. P3 is disconfirmed in the opposite direction to
the one predicted, since the rescue rate in the hardest band was 7 of 96 against
1 of 107 in the easy band, roughly eight times higher rather than lower. P4 is
disconfirmed on its ordering clause, because the model with the largest benefit
and the model with the most wrong claims are different models. Reporting these
as failures rather than adjusting them afterwards is what the registration was
for.

**What P3's reversal means.** The prediction assumed that a gate cannot supply
withheld information, which is true, and concluded that the gate would therefore
help less where information is withheld, which turned out to be false. The
mechanism is visible in P1. In the hardest band the model under ADV ends
episodes early by claiming, and BIND has no way to end early except by actually
passing, so the gate is not supplying the missing bits, it is denying the model
the option of declaring victory without them.

**Cost.** $16.74 across 407 episodes.

**Inference.** Wrong claims exist, they are specific to the band where
information is withheld, and they get more common as the model gets stronger.
That leaves the obvious explanation standing: nothing in these rules tells the
model that anything is hidden at all, so a claim on a green board is not
obviously irrational. Experiment 2 closes that gap.
