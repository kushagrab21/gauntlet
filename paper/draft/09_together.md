# 9. What the four experiments say together

**The programme in one line each.** Figure 6 draws the whole programme as the
tree it was: each experiment, the question it inherited from the one before it,
the predictions registered before it ran, and what its result did to the list of
candidate explanations. Experiment 1 asked whether a model given the channel
claims work it cannot verify, and it does, more often as it gets stronger.
Experiment 2 asked whether the cause is missing information, and it is not.
Experiment 3 asked whether the cause is the incentive, and within what that
design could see it is not. Experiment 4 asked whether doing the arithmetic at
the moment of the decision changes the behaviour, and it does. Four explanations
are struck out along the bottom of that figure and one is left standing, in
amber rather than green, because its control has not been run.

<!--FIG:F3-->

**One state carries the failure.** Across 856 episodes and 608 claims, the
programme produced 74 wrong claims, of which 73 were made at the decision point.
Claims made once every stage had been released were never wrong, 344 times out
of 344. No claim was made after a submission that left a visible test
failing, across 115 opportunities. The error is concentrated at the one state where the
visible evidence is complete and the hidden evidence is not.

**The cue, and its reliability.** Table 7 splits the wrong claims by how much a
green board is worth. The corpus was built in two batches, one in which a
quarter of tasks hide nothing and one in which three quarters do, and the model
is never told which batch a task came from. Claims are wrong far more often in
the batch where a green board is less often trustworthy, so the model is
weighting a real cue by a reliability it has no way to observe, and nothing
available to it inside an episode would let it calibrate that weight.

<!--TAB:T7-->

**What was eliminated, and what survived.** Table 8 lists all 14 registered
predictions with their verdicts, 8 confirmed, 5 refuted and 1 returning neither.
The refutations are what carry the argument. Missing information was eliminated
because supplying the exact stage count moved nothing. Incentive was eliminated
within the bound that design could see. Perception was eliminated because the
model already discriminates the two kinds of task by a margin of +0.6390. What
survives is integration, meaning the step in which a model combines what its
rules told it with what its own transcript shows, at the moment it decides.

<!--TAB:T8-->

**The mechanism, proposed and not established.** The model reads a green board
as evidence of completion and applies a threshold to it. The threshold is too
low for the tasks that hide something, and it is not moved by putting
information about the hidden stages in the rules, nor by attaching a payoff to
stopping. The same information moves it when it arrives already computed, in the
channel the model is reading, at the moment of the decision. The claim this
paper makes is that the failure is one of integration at the decision point, and
the evidence for that claim is one experiment whose placebo control has not
been run.

**Table 9, and what it is not.** The five sets of rules that played the same 72
tasks are listed as rows for reference. Three of them ran on one day and two on
another, and a difference between rows from different days cannot be told apart
from a difference between the days, so no comparison is drawn from that table.
Every comparison in this paper is one of the task-by-task ones in Tables 4, 5
and 6, each reading only tasks played under both of the arms it compares.


<!--TAB:T9-->