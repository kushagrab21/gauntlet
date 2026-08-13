# 8. The arithmetic, at the decision point

**Bridge from Experiment 3.** The two failed interventions share a shape. Each
put a fact in the rules at the start of the episode and required the model to
retrieve it, hold it, and apply it many turns later at the moment it mattered.
Neither tested whether the model performs that retrieval. Experiment 4 removes
the requirement by putting the fact where the decision is made.

**Preconditions.** Two arms played the first 72 ids of the same frozen order in
the same session. CTRL′ is the CTRL contract run again, changing nothing, which
makes it a same-day control rather than a cross-day one. COUNT is CTRL′ plus one
line appended to the feedback at every release, at a fixed registered position:
`Released so far: stage R of K. Stages still withheld: N.` R is the release
index, K the task's stage count, and N the difference. This is the first arm in
the programme whose treatment lives in the feedback channel rather than the
rules. 72 episodes came back under CTRL′ and 71 under COUNT, at $12.51.

**What the line does and does not supply.** It carries no information the warned
model of Experiment 2 lacked, because K was in that arm's rules and R is in the
model's own transcript. What it adds is the subtraction, already performed, in
the channel the model is reading, at the moment the release creates the
decision.

**Predictions.** C4: the model claims on fewer tasks under the counter. C6: the
churn floor, meaning that two identical runs disagree on no more than the twelve
of 115 that Experiment 2 recorded. C8: the counter changes the ending rather
than the working.

**Results.** Table 6 gives the two arms with the churn floor as a third row. The
third panel of Figure 5 draws the tasks, and its fourth panel draws the churn
floor on the same scale.

<!--TAB:T6-->

**Reading the table.** 71 tasks were played under both. On 30 the model claimed
under both and on 27 under neither. Fourteen tasks changed answer, thirteen of
them by ceasing to claim under the counter.

**Statistical test.**

*Definition.* The same paired form again, one-sided in the registered direction,
which here is a decrease.

*Calculation.* The split is 13 against 1 on 14 discordant pairs, and the
one-sided exact value in the registered direction is p = 0.0009.

*Inference.* C4 is confirmed. The realised shift in per-task claiming is 0.1745
against a design registered as powered for 0.155, so this is the first effect in
the programme that its design was powered to see. Wrong claims at the decision
point fell from 12 to 6.

**The churn floor, and what it does to Sections 6 and 7.** C6 bought the number
the programme had been missing. The control contract was run a second time on
the same ids, changing nothing at all, and the two identical runs disagreed with
each other on 2 tasks of 71. That is how much this setup moves on its own.
Against it, Experiment 2's twelve of 115 and Experiment 3's six of 71 are three
to four times the noise, and this experiment's fourteen is seven times it. The
floor does not rescue the two nulls, since a movement above the noise floor that
splits evenly is still an even split. What it does is establish that those
counts were large enough to have shown a direction had one existed.

**Where the claims went.** Of the thirteen tasks the counter stopped the model
claiming on, 8 were tasks that hide nothing, where the claim would have been
true, and 5 were tasks that hide a convention, where it would have been false.
The single task that moved the other way hides nothing and its claim was true,
and it is also one of the two tasks on which the two identical control runs
disagreed, so the control is the odd run out on it rather than the counter. That
is two events and no test, and it is recorded because a thirteen-against-one
split reads differently if its one counter-example is a coin flip.

**The counter bought conservatism rather than accuracy.** It did not make the
model better at guessing the withheld convention. It made it stop more often,
and stopping more often is disproportionately rewarded on this harness because
submitting again is free. The model solved more tasks rather than fewer: correct
claims went from 60 to 63 and tasks solved by the bound from 60 to 64, on one
fewer episode.
Giving up eight correct early stops cost nothing in the task's own terms, and
that is a property of this harness rather than a general result, since a harness
that charged for submissions would price the trade differently.

**The limitation, stated here rather than deferred.** This design cannot
separate the content of the counter line from the presence of an extra sentence
of feedback. Both would produce this result. The mechanism this experiment
is meant to license is that the failure is one of integration rather than of
threshold, and that mechanism follows only if the content of the line is doing
the work. A placebo arm carrying a line of the same shape with its numbers
removed is the missing control. It was not bought.

**Inference.** The same information, moved from the rules to the feedback and
from the start of the episode to the moment of the decision, changed the
behaviour that two earlier arms could not move. Read alongside Experiment 2,
where the model already discriminated the risky tasks from the safe ones, the
result suggests the model has the parts it needs and does not combine them at
the moment it decides unless the combination is supplied. That reading rests on
one experiment whose control has not been run.
