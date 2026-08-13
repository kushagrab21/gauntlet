# 2. What the previous work established, and what it could not

**What it established.** The previous experiment compared two agent designs on a
repair corpus. In the first the model could declare the task finished and the
declaration was believed. In the second the declaration was ignored and the
episode ended only when the checker passed. Everything else was held identical,
down to byte-identical feedback text, so the only varying factor was who held
the authority to end the episode. That paper named this failure the
false-DONE. This paper calls the same event a wrong claim and uses that name
throughout.

Three results carried forward into this one. The gate helps by converting wrong
claims into forced repairs, so its value is the rate of wrong claiming times the
model's ability to repair once refused. That value is zero at both ends of the
capability range for opposite reasons: a model at the ceiling never claims
wrongly and has nothing to convert, and a model below the floor cannot complete
the repair it is forced into. And the window is a property of the model rather
than of the model and task together, because raising task difficulty deepened
the window for models already inside it and never dragged a stronger model in.

**What it could not do.** That design had three limits, and this paper addresses
them.

The wrong claim had no located moment. A model could declare completion at any
turn, from any state, and the design recorded that it happened without
recording what the model was looking at when it happened. That leaves a rate and
no state, and a rate can be lowered by many different mechanisms, so a rate on
its own does not say which mechanism to intervene on.

The corpus could not separate a model that did not know from one that did not
check. Its tasks were bugs with a determinate correct fix, hidden only by
stripping the description, so a model that failed had either missed something
present in the code or guessed wrong about something absent from it, and nothing
in the record said which. The corpus here is built the other way round, because
the answer is absent from what the model is handed by construction, and the
question is only whether the model notices.

And the models were never asked to reason about what they had not seen. Nothing
in that harness told a model that anything was withheld, so a claim made on a
green board was not obviously irrational, and the available explanation for the
whole effect was that the model did not know there was more. That explanation is
the first thing this paper tests, and Section 6 removes it.
