# F6 — The claim-timing signature

**Image:** `F6_claim_timing.png`, drawn by
`figures/make_figures.py:f6_claim_timing`.
**Section:** 4, The decision point. It sits beside Table 2, which carries the
same numbers per run.

## What it shows

Where in an episode the model said `DONE`, and where those claims were wrong.

The left panel is the whole programme in three horizontal bars, one per moment:
at the decision point with a stage still hidden, once every stage had been
released, and before any test had run. The grey length is the number of claims
and the red segment inside it is the wrong ones, which is the previous paper's
claim-bar convention. The counts are printed at the end of each bar as
`n DONEs · m wrong`, so no reader has to measure a bar against an axis.

The right panel repeats the split for each of the eight runs that could claim,
stacking wrong-at-the-decision-point against wrong-anywhere-else. Experiment 1's
three runs are labelled by model, because all three ran the same arm and the arm
code would not separate them.

## Why this figure carries the paper

Section 4 asserts that the failure has a location. This is the evidence, and it
is a shape rather than a number: one long grey bar with a red bite taken out of
it, one long grey bar with none, and one bar a single claim wide that is
entirely red. The right panel shows the same shape holding run by run, which is
what makes it a signature rather than an aggregate.

## Data source

`../tables/T2.csv`, which `tables/make_tables.py` regenerates from
`declare/data/`. No number is written into the script.

## What a reader must be able to read off it

1. That 344 claims were made after every stage had been released and none of
   them was wrong.
2. That the wrong claims are concentrated in the first bar.
3. That the single blue segment in the right panel is the one exception, the
   claim made before any test had run.

## The one thing this figure must not imply

That the first bar is mostly wrong. It is not: 73 of 263. The red segment is
about a quarter of the bar and should be drawn at exactly that proportion, which
it is, because both numbers come from the same table row.

## Open question for the finished version

Whether the right panel should be ordered by experiment, as it is now, or by
size of the wrong count. Experiment order is more honest and reads worse.
