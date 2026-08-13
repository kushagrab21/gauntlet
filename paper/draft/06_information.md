# 6. It is not missing information

**Bridge from Experiment 1.** Experiment 1 left one explanation standing, and it
is the obvious one: the model claims because it does not know how much is still
hidden. The claim clause quoted in Section 3 tells it that tests it has not been
shown exist, and that is the whole of what it is told. The rules never say that
those tests are released in stages, never give their number, and never
distinguish a task that hides something from one that does not, so a model
reasoning correctly from what it was told could treat a green board as the best
evidence it will be given and stop there. If that is the mechanism, then
supplying the count should reduce claiming, and the fix for the whole failure is
one sentence of prompt.

**Preconditions.** One model played the same 119 working tasks in the same
frozen order under two arms. CTRL is Experiment 1's ADV contract, imported and
asserted byte-identical, so this experiment's control is the arm that produced
the earlier wrong claims. WARN is CTRL plus one sentence appended to the rules
and nowhere else: `This task's hidden tests are released in exactly K stages.`
K is the task's real stage count. The sentence lives in the rules rather than in
the feedback, so the model is told the total once and must track releases
itself, and the feedback text was verified identical across the two arms in
every message except the first. 118 episodes came back under CTRL and 116 under
WARN, at $19.79.

**Predictions.** B1: the warned model claims at the decision point on fewer
tasks. B2: wrong claims survive an explicit stage count. B3: accuracy tracks how
much a green board is worth. B4: the warning changes the ending rather than the
working, tested on the window before the first decision point, which no claim
can truncate.

**Results.** Table 4 gives the two arms and the tasks that changed answer, and
the first panel of Figure 5 draws every task as a dot.

<!--TAB:T4-->

<!--FIG:F4-->

**Reading the table.** 115 tasks were played under both arms. On 63 the model
claimed at the decision point under both and on 40 under neither, so 103 tasks
carry no information about a difference. Of the 12 that changed answer, 6 went
each way.

**Statistical test.**

*Definition.* Both arms played the same tasks, so each task has a pair of
outcomes and only the tasks that disagree carry information about the arm. The
null is that the warning has no effect, in which case each disagreement is
equally likely to fall either way, and the probability of a split at least as
extreme as the one observed comes from the exact binomial. This is McNemar's
test, one-sided in the registered direction.

*Calculation.* The split is 6 and 6 on 12 discordant pairs, and the one-sided
exact value in the registered direction is p = 0.6128.

*Inference.* B1 is disconfirmed. The design had more than twice the discordant
pairs it needed to fire, so this is not a test that failed for want of data. It
is the absence of an effect.

**Scoring the predictions.** B1 disconfirmed. B2 confirmed, since the warned
model claimed 69 times at the decision point and was wrong 19 of them, where the
registered clause needed one. B3 confirmed. B4 confirmed on both metrics, the
first identical to four decimal places at 1.0261 submissions to the first green
board under each arm, and the second inside its band by 0.0016, which is one or
two guesses out of sixty and is reported as a near miss rather than a
comfortable pass.

**What B1 rules out.** The information deficit was real, it was closed, and the
behaviour did not move. A model that is told a task has K stages, that has seen
fewer than K, and that could submit again for free, still says `DONE`. Whatever
the failure is, it is not ignorance of how much is hidden.

**The model can tell which tasks are risky.** This was registered as a
secondary in the expectation of no difference, and it returned the largest
effect in the programme. Table 4B splits every visit to the decision point by
whether the task hides a convention. On tasks that hide nothing the model
claimed at 97 of 117 visits. On tasks that hide a convention it claimed at 23 of
121. The difference is +0.6390 with a two-sided Fisher exact p = 2.75e-24, and
it replicates in both arms separately.

<!--TAB:T4B-->

**Why this is not a corpus leak.** The corpus guarantees that the two kinds of
task are indistinguishable in the bytes a solver sees on its first turn, and a
leave-one-out classifier over those bytes confirms it, scoring 0.5185 against a
base rate of 0.5259, which is a lift of −0.0074. But a visit to the decision
point happens later than turn 1. By then a stage has been released and the model
has read that stage's tests, and on a task that hides a convention those tests
encode the drawn convention while on a task that hides nothing they are quiet
tests any visible-green solution already satisfies. The model is not seeing
through the corpus. It is reading the tests it was just handed and judging
whether its current code satisfies them, which is the job.

**Inference.** Two facts now sit together. The model can tell, at the decision
point, whether claiming is safe, and it withholds the claim on roughly four
fifths of the tasks that withhold something. On the remaining fifth it claims
anyway. So the failure is in the threshold the model applies to a cue it reads
correctly, rather than in the reading, and adding information to the rules did
not move that threshold. Experiment 3 tries to move it with a payoff instead.
