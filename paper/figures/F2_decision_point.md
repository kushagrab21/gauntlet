# F2 — The decision point

**Image:** `F2_decision_point.png`, drawn by `figures/make_figures.py:f2_decision_point`.
**Section:** 4, The decision point. It is the paper's central diagram.

## What it shows

One moment, magnified. The model's last submission has passed every test it can
see, that pass released a fresh stage, and at least one stage is still hidden.
Nothing on the model's screen is failing. The work may or may not be finished
and the model cannot check.

From that state the harness allows two moves, and the figure draws both:

- **Say DONE.** The episode ends. The harness scores the claim against the full
  suite and tells the model nothing. Two endings, right and wrong, and the model
  never learns which it reached.
- **Submit again.** Free, and it releases the next stage, which returns the
  model to the same state one rung further up with strictly more information.

The asymmetry is the whole point and the figure has to make it visible: one
branch costs nothing and buys information, the other ends the episode on a
guess. The return arrow from *the next stage is released* back into the decision
box carries that.

Below the decision box, in a dashed box, sits what the model cannot see: the
hidden stage may enforce a convention it guessed wrong. The dashed border is the
same mark F1 uses for a withheld stage.

## Why this figure exists

The previous paper had no equivalent, because in that design the failure had no
single location — a false-DONE could happen at any turn. This paper's
contribution is that the failure **has** a location, and this is the figure that
asserts it. T2 is the evidence: 73 of the programme's 74 wrong claims were made
in exactly this state.

**Deviation to record:** this figure has no ancestor in the previous paper. Its
grammar is inherited but its subject is new.

## Data source

None directly. The figure is a diagram of one harness state. Its claim to
importance is T2, which the caption should cite by number rather than restate.

## What a reader must be able to read off it

1. The two moves available, and that one of them is free.
2. That the model cannot distinguish "finished" from "not yet caught".
3. That the outcome of a claim is never fed back.

## Caption sketch

> The decision point. The model has passed every test it can see, one more stage
> of tests was released because of that, and at least one stage is still hidden.
> It may end the episode by replying `DONE`, which is scored against the tests it
> has not seen and never reported back to it, or it may submit again, which costs
> nothing and releases the next stage. Drawn by `figures/make_figures.py`.

## Open questions for the finished version

- Whether to overlay the traffic: 860 visits to this state across the programme,
  263 of which took the DONE branch. It would make the figure carry data as well
  as structure, at some cost in cleanliness.
- Whether the dashed "what it cannot see" box should name a concrete convention
  from `gauntlet/CATALOG.md` rather than describe one in the abstract.
