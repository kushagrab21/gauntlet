# 1. Question

The previous experiment in this programme ended with a practical rule and an
unanswered question. The rule was that completion gating pays inside a window of
capability: a model strong enough never to claim wrongly gains nothing from the
gate, a model too weak to repair on feedback is hurt by it, and the models in
between are rescued in proportion to how often they claim wrongly in the first
place. The unanswered question was what the wrong claim is. I had
measured its rate across seven models and three difficulties, and I had shown
that the gate's value moves with that rate, but I had never caught the event in
a state where I could say what the model knew at the moment it decided.

The gap has a practical consequence. If a wrong claim is a slip, a checker is
the fix. If it is a reasoning failure about unseen evidence, a checker only
masks it, and every agent that runs without one keeps making it. Telling those
apart requires a task where I control what the model has been shown, what has
been withheld, and when the withheld part arrives.

**The design follows directly.** Each task is a short broken Python function
with a test suite. The function is pure, under forty lines, and carries no
docstring or comment, so repairing it looks mechanical. The difficulty sits
somewhere else. The code has to make a decision that nothing the model can see
states, and a hidden suite enforces one particular answer to it. Is a record
with no value field an error, a null, or a zero? Does a range include its upper
bound? When every score in a group is null, is the average `None` or zero? Each
of those has several defensible answers and real systems disagree about which
one is right, so a model cannot recover the answer by reasoning. It can only
guess, and the corpus is built so that guessing loses.

What stays measurable is whether the model notices that it is guessing. That is
what the staged release is for. The tests that enforce the withheld convention
do not all arrive at once. A task ships with the tests the model can read, plus
a chain of withheld stages, and one more stage is released only when
everything currently visible passes. The model therefore moves through a
sequence of information states inside a single episode, and I know which one it
was in at every turn.

Onto that loop the experiment adds one binary channel. The model may reply with
the single word `DONE` instead of code, which asserts that the work is finished
including the parts it has not been shown. The harness scores that assertion
against the full suite, ends the episode, and tells the model nothing. A claim
is therefore a bet placed on evidence the model does not have, and the record of
the bet is complete: I know the board it was looking at, how many stages were
still hidden, and whether it was right.

**Why this matters outside the laboratory.** No specification is ever complete.
Every user leaves out edge cases and conventions they assume are obvious, so an
agent working in a real repository is always partly grading itself against an
answer key it reconstructed. Whether that agent's own "done" should carry
authority is a design decision every agent system makes, and most make it
without noticing they have. This paper is about what happens when a model makes
that call in the one situation where a careful engineer would not: everything
visible passes, and there is more that has not been shown.
