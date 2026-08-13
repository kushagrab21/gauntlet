# F4 — The paired flips

**Image:** `F4_paired_flips.png`, drawn by `figures/make_figures.py:f4_paired_flips`.
**Sections:** 6, 7 and 8 carry one panel each. The fourth panel, the churn
floor, belongs to 8, where the floor is reported.

## What it shows

One dot per task, for each of the three paired comparisons and for the churn
floor. Every task was played under both sets of rules, so each dot falls into
one of four cells:

| dot | meaning |
|---|---|
| grey, faded | claimed under both sets of rules |
| amber, solid | claimed only under the rules **without** the intervention |
| blue, solid | claimed only under the rules **with** the intervention |
| hollow | claimed under neither |

The registered tests read only the solid dots. The figure draws the faded and
hollow ones anyway, because the fraction of tasks that did not move is the thing
a bar chart of two rates would hide, and it is what makes a 13-against-1 split
look different from a 6-against-6 one.

## Why this form, and its ancestor

This is the previous paper's `dotMatrix` idea carried forward: that paper's
"6 against 6" and "13 against 1" are shapes, not numbers, and a dot grid shows
how few tasks move at all. The previous paper reported paired disagreements as
`b` and `c` columns inside a results table; this paper promotes them to a figure
because in this programme the paired split **is** the result, and there is no
success-rate curve to carry the story instead.

**Deviation to record:** the previous paper's figures 1–4 are all quantitative
charts with continuous axes (success rate, Δ, false-DONE rate). F4 has no axis at
all. The reason is that this paper's outcome is a per-task binary and its effects
live in counts of single digits, where a continuous axis would imply a precision
the data does not have.

## Data source

`../tables/T4.md`, `T5.md`, `T6.md`, parsed by `read_flip()`. The figure reads
the tables rather than the dataset on purpose: a number can only reach a figure
through a table the paper prints, so a figure and its table cannot disagree.
The tables are regenerated from `declare/data/` by `../tables/make_tables.py`.

## What a reader must be able to read off it

1. That most tasks did not change answer in any of the three experiments.
2. That experiment 2's movement is symmetric and experiment 4's is not.
3. That experiment 3's six moving tasks are too few to carry a direction, which
   the panel makes visible without needing the power calculation.

## The one thing this figure must not imply

That the three panels are comparable in size. They are not: experiment 2 has 115
paired tasks and experiments 3 and 4 have 71. The panels are drawn on the same
dot scale so the difference in area is honest, and the count is printed under
each panel.

## Open question for the finished version

Whether to colour the solid dots by whether the claim was right or wrong.
Experiment 4's thirteen suppressed claims split eight benign and five enforcing,
which is a real fact about what the counter removed, and it is currently
invisible. It would add a fifth and sixth colour to a figure whose strength is
that it has four.
