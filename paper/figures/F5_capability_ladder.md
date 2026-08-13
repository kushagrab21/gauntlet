# F5 — The capability ladder

**Image:** `F5_capability_ladder.png`, drawn by
`figures/make_figures.py:f5_capability_ladder`.
**Section:** 5, Capability makes it worse.

## What it shows

Two panels over the same three models, ordered strongest to weakest by the
capability rung that was fixed before the run.

The left panel counts the tasks on which the model said `DONE`, out of the 68 it
played. A dashed reference line marks all 68, so the reader can see how close
the strongest model comes to claiming on everything. Each bar carries its share
above it and its `n/N` inside it in white, which is the previous paper's bar
convention.

The right panel counts, of those claims, how many were wrong. It is a separate
panel rather than a red segment inside the left bars because the wrong counts
are 4, 2 and 0 against claim counts of 67, 57 and 37, and a segment that small
would be invisible at any honest scale.

## Why two panels rather than one

The two panels have different denominators, and the paper's table rule is that a
denominator is always visible. Tasks played is the denominator on the left and
claims made is the denominator on the right, so each bar prints its own. Putting
both series on one axis would invite the reader to compare 67 against 4 as
though they were the same kind of quantity.

## Data source

`../tables/T3.csv`, which `tables/make_tables.py` regenerates from
`declare/data/`. No number is written into the script.

## What a reader must be able to read off it

1. That claiming rises with capability and is nearly total at the top.
2. That the wrong claims rise in the same order.
3. That the weakest model made no wrong claims at all, which is the fact that
   stops the reader concluding that weaker models are simply worse at
   everything.

## The one thing this figure must not imply

That the right panel is a rate. It is a count. The share of each model's claims
that were wrong is in T3 and in the prose, and it moves 0.0000, 0.0351, 0.0597,
which is a much smaller spread than the bar heights suggest.

## Open question for the finished version

Whether to add the third model series, tasks solved without ever claiming, which
would show that the weakest model's reticence costs it solved tasks. It is in
T3, it is relevant, and it would make a two-panel figure into a three-panel one.
