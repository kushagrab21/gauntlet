# Abstract

A coding agent given a channel to declare its own work finished will sometimes
use it on work that is not finished. The previous paper in this programme showed
that moving the authority to end a task from the model to a checker changes
outcomes, and that the size of the change tracks how often the model wrongly
claims completion. That design could not isolate the wrong claim itself,
because a claim could happen at any turn and the corpus was built to measure
something else. This paper builds an instrument for it. Every task hides a
convention that the code must choose and the description never states, and the
tests that enforce that convention are released one stage at a time, so what the
model knows changes while the episode runs. Across eleven runs of three models,
856 episodes at $55.21 of booked compute, the instrument locates the failure at
a single state, the moment every
visible test passes and a stage is still hidden: 73 of the programme's 74 wrong
claims are made there, and not one is made after a submission that left a
visible test failing. Three explanations are then eliminated. Telling the model exactly how
many stages are hidden does not reduce claiming, with 6 tasks moving each way of
115. Telling it that stopping early is rewarded does not raise claiming. And the
model is not blind to the risk, because it claims at 97 of 117 visits where
claiming is safe and at 23 of 121 where it is not. One intervention moves
the behaviour: printing the count of what is still hidden into the feedback, at
the moment of the decision, moves 13 tasks against 1 and halves the wrong
claims. The control that would show whether the content of that line or merely
its presence did the work has not been run.
