# F3 — The argument tree

**Image:** `F3_timeline.png`, drawn by `figures/make_figures.py:f3_timeline`.
**Section:** 9, What the four experiments say together. It prints as Figure 6.
It is the map the reader navigates by, placed as a summary rather than a
roadmap; see OUTLINE.md deviation D3.

The file name and the builder's name are unchanged because the paper numbers
its figures by file, and renaming would move every other figure. What the
image holds is no longer a timeline, and the caption in `build.py` still
describes the old one.

## What it shows

Three lanes, read downwards, on one canvas.

**Lane 1, the spine.** A root node for the previous paper, then the four
experiments left to right in the order they ran, joined by arrows. Each node
carries its date, its size, and both of its arms with the arm code glossed in
brackets where it appears, so a reader who has never seen `ADV` or `CTRL′`
does not have to go looking. Each arrow carries, in italic above the shaft,
the question the next experiment inherited from the one before it. That is the
content the old dated line could not hold: the programme did not accumulate
four results, it passed one question forward four times.

**Lane 2, the registered predictions.** Under each experiment, one pill per
prediction registered before that experiment ran, with its label, a one-line
gloss and its verdict as a glyph and a fill: green ✓ confirmed, red ✗
disconfirmed, grey ◦ neither. Fourteen pills, eight green, five red, one grey.

**Lane 3, the explanation ledger.** Five boxes, each tied by an arrow to the
experiment that produced it. Four are red and eliminated. The fifth is amber
rather than green, and prints `placebo control unrun` inside the box rather
than in a footnote, because the mechanism is proposed and its control has not
been run.

| ledger entry | from | what did it |
|---|---|---|
| one weak model's quirk | 1 | claiming rises with capability, 0.5441 → 0.8382 → 0.9853 |
| missing information | 2 | 6 tasks moved each way of 115 |
| blind to the risk | 2 | claims at 97 of 117 safe visits, 23 of 121 risky ones |
| the incentive | 3 | no large increase; powered only for 0.155 |
| integration at the decision point | 4 | moved 13 tasks against 1; wrong claims fell 12 to 6 |

## Where the numbers come from

Dates are read from `runs.csv` through `make_tables.RUN_BY_ID`, not hard-coded
as they were in the previous version of this figure. Verdicts and prediction
labels are read from `tables/T8.csv`; the one-line glosses beside them are
captions written in the script, and the script raises if the set of labels in
`F3_SHORT` ever stops matching the set in T8, so a prediction added to the
registration cannot silently go undrawn. Counts come from `T3`, `T4B` and `T6`
and from `paired()` in the table builder.

One number is written in the script rather than read: `0.155`, the shift
Experiment 3 was registered as powered for. It is a design parameter and not a
measurement, and no table prints it as a column, so it is guarded instead — the
figure raises if `tables/T5.md`, which also prints it, stops agreeing.

## Why it earns its place

The paper's spine is elimination: three explanations are removed and one
intervention survives with its control unrun. A reader who cannot hold four
experiments in mind at once will lose that spine in the prose. This is the only
place where the whole argument is visible at once, and the only place where the
registered predictions and their verdicts sit beside the experiments that
tested them rather than in a table eight pages away.

**Deviation to record:** F3 is new against the previous paper, which had no
such figure because three experiments in one narrative line did not need one.

## What a reader must be able to read off it

1. The design of every arm, without reading Section 4 first.
2. That two experiments returned null results, and that these are load-bearing
   rather than filler.
3. That the fifth ledger entry is not green, and why.
4. That experiments 3 and 4 ran on the same day, which is the fact that makes
   the churn floor in T6 interpretable.

## Layout, and why it is computed rather than placed

Nothing in this figure is nudged by hand. Every distance is in data units, the
canvas is sized from measured content at a fixed ten units to the inch, and the
column pitch is the largest of three demands: half a box width, the edge label
that has to fit between two columns, and the room the five-box ledger lane needs
under a four-column spine. Crowding is resolved with space and never with a
smaller font, which is why the image is 26 by 13 inches.

Two checks run on every render and raise rather than warn: no arrow may be
shorter than five head-lengths plus its end clearance, which is what stops an
arrow rendering as a head with no shaft; and no label may cross a box edge,
overlap another label, or sit within 10px of the border of the box it is in.

## Open question for the finished version

Whether the unrun placebo arm should appear as a fifth, hollow position on the
spine as well as inside the ledger box. It would state the paper's largest open
question in the same figure that states its findings. The risk is that a reader
takes an unrun arm for a run one.
