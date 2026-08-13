# F1 — The loop, the release rule, and the claim channel

**Image:** `F1_harness_loop.png`, drawn by `figures/make_figures.py:f1_harness_loop`.
**Section:** 3, The instrument. It is the first figure a reader meets.

## What it shows

One turn of the harness, the rule that releases a hidden stage, and the channel
the model may use to end the episode. Three things are drawn, and each of them
is a property of the code rather than a result.

**The turn.** The model sends a rewritten module, the checker runs the tests now
visible and reports how many passed and which failed, and the loop repeats.

**The suite, and what of it is visible.** The tests are a stack: the ones the
model can see, the next hidden stage, and the stages after that. `K` stages in
all. A stage becomes visible only when every visible test passes, so passing
everything visible is what buys the next stage rather than what ends the work.

**The claim, and its two outcomes.** At any turn the model may reply `DONE`
instead of code. The whole suite is then run against the module as it stands,
visible tests and hidden ones alike. If all pass the claim was right; if any
fails the claim was wrong. The model is told neither outcome.

## The conditions that used to be implicit, and are now on the figure

An earlier version of this figure drew the same boxes and left the model's
information state to the prose, which made the diagram ambiguous about the one
thing the paper is about. What the model knows at the moment it decides is now
written beside the object that decides it.

| condition | where it is drawn |
|---|---|
| unseen tests exist, and the rules say so | annotation beside the stack |
| the rules do not say how many there are | same annotation |
| passing everything visible is what releases the next stage | same annotation |
| a claim may be made at any turn, not only at the end | label on the claim arrow |
| the claim is scored against the hidden tests | the fork after the scoring box |
| the model learns neither outcome | line under the fork |

So the figure now says what the paper needs it to say: the model knows hidden
tests are there and cannot read them, and a claim is a judgement about them.

## Relationship to the previous paper's Figure 7

The previous paper drew two panels, advisory and binding, to contrast who holds
the authority to end the loop. This paper does not repeat that contrast, because
it is settled: every arm here except BIND grants the model the channel, and the
question has moved from *who holds the authority* to *what the model does with
it*. F1 therefore draws one loop rather than two panels.

**Deviation to record in the paper:** the previous paper's fig7 is a two-panel
comparison; F1 is a single annotated loop. It should appear in one sentence of
the Setup section.

## Data source

None. F1 is a diagram of the harness and asserts no measured quantity, so it
adds nothing to `NUMBERS.md`. Every label is a property of the code: the staged
release and the release condition are `traverse/traverse/episode.py` in
`run_episode`, the claim clause is `CONTRACT_ADV` in the same file, and the
silent grading of every submission against the full suite is the `run_suite_
modules(source, modules)` call whose result the model is never shown.

## What a reader must be able to read off it

1. The model never learns whether its claim was right.
2. Submitting again is available and always releases more information.
3. There exist tests the model has not seen at the moment it may claim, and it
   has been told so.
4. A claim has two outcomes, and which one occurred is what the paper counts.

## Visual vocabulary

Inherited from `style.py`, copied byte-identical from the previous paper.

| mark | meaning |
|---|---|
| blue box | an active state or artifact |
| dashed grey box | something withheld from the model |
| green box | an outcome that counts as a correct claim |
| red-edged box | an outcome that counts as a wrong claim |
| amber box and arrow | the channel this paper measures |
| grey arrow, italic label | an action |
| grey italic text beside an object | a condition that holds of that object |

## Production rules this figure follows

- **Drawn at page width.** The manuscript sets every figure to `\textwidth`, so
  a figure drawn 13in wide has its type scaled to 42 per cent and lands under
  5pt on the page. This one is drawn 6.03in wide with the axes filling the
  figure, so one data unit is exactly `figsize / xlim` and a 10pt label prints
  at 8.6pt, just under the 8.9pt caption beside it.
- **Boxes are sized to their text**, by `fitbox`, which measures the rendered
  string rather than guessing from its character count.
- **No collisions.** `make_figures.py --layout` reports every overlapping box,
  overlapping label, and label crossing a box edge. This figure reports clean.
- **Few words per box.** Page width is fixed, so what a box does not spend on
  text becomes the gap beside it, and the gaps are what make the connections
  legible.

## Resolved questions

- **Three stages or `K`.** Both. The stack draws the visible tests, the next
  hidden stage and the stages after that, and the annotation says `K` stages in
  all, which is honest about the depth without drawing a number the corpus does
  not fix.
- **Whether to print 608 claims and zero outcomes learned.** No. F1 asserts no
  measured quantity, and adding one would put it in `NUMBERS.md` and in the
  numbers check for no gain the fork does not already make visually.
- **Whether the outcome terminals belong here or only in F2.** Here. The claim
  is the object of the paper, and a channel drawn without its two outcomes
  leaves the reader to infer what is being counted.
