# 4. The decision point

**The state.** Figure 2 draws the moment this paper is about. The model's last
submission passed every test it could see, that pass released a fresh stage, and
at least one stage is still hidden. Nothing on the model's screen is failing.
The work may be finished or it may not, and the model has no way to check. This
is the decision point.

<!--FIG:F2-->

Two moves are available from that state and the harness treats them
differently. The model can say `DONE`, which ends the episode on a guess about
evidence it has never seen. Or it can submit again, which costs it nothing, and
which releases the next stage and returns it to the same kind of state with
strictly more information. On this harness a claim is never the cheaper move, so
a claim is never forced by a budget and is always a choice to stop early.

**Where the wrong claims are.** Table 2 sorts every `DONE` in the programme by
what the model could see when it said it. Of the 74 wrong claims, 73 were made
at the decision point. Of the 344 claims made once every stage had been
released, when nothing was hidden and the model had watched the whole suite
pass, not one was wrong. Figure 3 draws the same split, for the programme and
run by run. One further claim was made before any test had run, by
the middle model in Experiment 1, which replied `DONE` on its first turn having
made zero submissions, and it was wrong.

<!--TAB:T2-->

<!--FIG:F6-->

**The branch nobody took.** The harness allows a model to reply `DONE` from any
state, and that includes the state where a test it can see is failing. Across
the eleven live runs there were 115 turns in which the previous submission had
left a visible test failing, and the number of claims made from those turns is
zero. That zero rules out a simpler reading of the result, because a model
claiming to escape a hard task would claim from a red board and none ever did.
No claim in the programme was made after a submission that left a visible test
failing.

**What this section licenses.** It licenses one thing: the error has a location,
and the location is a state defined entirely by what the model has and has not
been shown. It licenses nothing about the cause, because a state where an error
concentrates is a place to intervene rather than an explanation. The next three
sections are the attempts to explain it.
