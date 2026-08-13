# STRUCTURE.md — the previous paper, recorded as a template contract

**Subject.** *Who Decides When the Task Is Done? Measuring the Effect of Moving
Completion Authority from LLMs to Checkers*, Kushagra Bhatnagar, July 2026,
DOI 10.5281/zenodo.21698264. Source at
`~/Desktop/Experiment_binding_agent/binding-feedback-experiment/paper/`.

**Status of this document.** It records what the previous paper does, factually,
without judging it. It is the template contract for the new paper: **every
choice in the new paper either follows this document or records why it
deviates.** Deviations are collected in `OUTLINE.md` under "Deviations from
STRUCTURE.md", and each one names the section it applies to.

**Physical form.** 19 pages, `article` class at 11pt, `newpxtext`/`newpxmath`,
text block 5.6in × 8.6in, `booktabs` rules, one accent colour
(`bindingblue` `#1668A1`) used for links and nothing else. Ten section files
under `sections/`, one per section, assembled by `main.tex`. Section numbering
starts at 1 for *Question*, because the abstract is unnumbered and starred.

---

## 1. Section order, and the job each section does

| # | section | words | job |
|---|---|---|---|
| — | Abstract | 258 | One paragraph, no headings. States the distinction, names the failure, gives the scale, and gives all three headline numbers with their direction. |
| 1 | Question | 592 | Where the question came from, in the first person, starting from a practical frustration. Then the design in prose. Then the failure mode named and explained mechanistically. Ends by generalising to deployment. |
| 2 | Setup | 573 | The corpus and why it is synthetic. The checker. What the two harnesses share and the exact list of what they do not. The presentation discovery, dated and logged. The anti-fitting discipline. |
| 3 | Experiment 1: the interaction | 841 | The 2×2. Introduces the statistical machinery the paper reuses. Breaks the effect down by bug class, then by rescue kind, then costs it. |
| 4 | Experiment 2: the capability ladder | 1,998 | The largest section. Bridge, preconditions, the independent capability axis, five registered predictions, results, the curve, the test, prediction scoring, exit classification, three number series, the floor, the window interior, replication, cost, deviations, inference. |
| 5 | Experiment 3: the composition window | 1,813 | Same skeleton as section 4, one factor changed. Ends on the disconfirmation that is the paper's headline. |
| 6 | The mechanism, unified | 399 | One quantity explains all three experiments. Evidence stacked in one paragraph. The mechanism in one sentence. What follows for practice. |
| 7 | Limitations | 389 | Nine numbered items, drawn from the experiment ledger. |
| 8 | What this means for agent design, and reproducibility | 357 | Design advice as a decision rule. Scale and cost. Reproducibility. Provenance of AI assistance. |
| 9 | References | 108 | Four entries, `thebibliography`. |

**Total prose: ~6,220 words across nine numbered sections plus abstract.**

### The repeated experiment-section skeleton

Sections 3, 4 and 5 share one skeleton, and it is the most transferable thing in
the paper. In order, as bold run-in `\paragraph` headings:

1. **Bridge from the previous experiment** — what the last section established,
   what it left open, and *the design follows directly*: the phrase recurs.
   Present in 4 and 5, absent in 3.
2. **Preconditions** — every factor held fixed, named, with the count of
   episodes derived as an arithmetic sentence (`7 models × 2 modes × 87 tasks =
   1,218 episodes`). Closes with "because everything except X is held fixed, any
   change is attributable to X alone."
3. **Predictions** — numbered, stated as they were registered, with confirmatory
   and exploratory separated explicitly.
4. **Results** — one sentence naming what the table's rows and columns are,
   then the table.
5. **Reading the table / the curve** — what the shape is, in words, before any
   test.
6. **Statistical test** — three italic sub-blocks in fixed order:
   *Definition* (what the test is and why it applies, in plain language),
   *Calculation* (the arithmetic), *Inference* (what it licenses).
7. **Scoring the predictions** — each registered prediction marked confirmed or
   disconfirmed, failures first.
8. **Patterns in the table** — a fixed three-part rhythm repeated per number
   series: *The X series is a, b, c. The pattern is a NAME. The inference is …*
9. **Sub-findings** — the floor, the window interior, rescue quality, replication.
10. **Cost** — dollars, every time.
11. **Deviations** — operational scars, named and logged.
12. **Inference** — what died, what survived, and the question the next
    experiment exists to answer.

---

## 2. How the experimental procedure is presented

**Where the diagrams sit.** Two diagrams, both early, both before any result.

- **Figure 7 (`fig7_modes.png`) sits in section 1 (Question)**, immediately
  after the paragraph that defines the two designs and before the paragraph that
  names the failure. It is the first figure in the paper. It shows *the
  mechanism under test*, not the workflow.
- **Figure 6 (`fig6_workflow.png`) sits in section 2 (Setup)**, after the
  corpus and checker paragraphs and before the discipline paragraph. It shows
  *the process discipline*: what was frozen, what was hidden, what order things
  happened in.

The ordering is deliberate and worth carrying: **mechanism first, discipline
second, results third.** A reader meets the thing being measured before the
apparatus that protects the measurement.

**What the loop diagram shows.** `fig7_modes` is two side-by-side panels, one
per mode, sharing a caption. Each panel carries: the LLM box, the checker box, a
two-arrow cycle between them labelled `writes code` and `returns a verdict (pass
or fail)`, a terminal `episode ends` box, and a one-line grey caption under the
panel stating the consequence in plain words. The party holding the authority is
drawn with a thick coloured border and a bold coloured label reading `holds the
authority to end the loop`; the party that does not is drawn in grey. In the
binding panel the ignored channel is drawn as a **grey dashed arrow struck
through with a red ×** and labelled `saying DONE is ignored`.

**Visual vocabulary, from `writeup_figures/style.py` and the diagram scripts.**

| mark | meaning |
|---|---|
| grey box | an input, or a party without authority |
| blue box (`#eef4fc` on `S1_BLUE`) | an active state or artifact |
| dashed grey box | sealed or hidden material |
| green box (`#e6f4e6` on `S6_GREEN`) | a terminal that is a success |
| red box (`#fdecec` on `CRITICAL`) | a terminal that is a failure |
| pale grey box | `continue ↺`, a loop-back |
| solid grey arrow, italic grey label | an action |
| dashed arrow + red × | a channel that exists and is ignored |
| amber `ADVISORY` `#c2801f` | the baseline condition |
| deep blue `BINDING` `#1668a1` | the intervention |
| bullet list under the diagram | the grammar, restated in two lines |

Two conventions travel with these: **every diagram restates its own grammar** in
a bullet key beneath it ("boxes show states and arrows show actions"), and
**every figure caption names the script that drew it**.

**Decision trees.** `fig5_exit_trees` draws each mode's exit classification as a
binary tree with yes/no edge labels, leaves coloured green or red, and leaves
placed on a uniform grid so the two modes' trees are visually comparable. A
starred leaf carries a footnote inside the axes.

---

## 3. How results are presented

**Table format.** `booktabs` throughout: `\toprule`, `\midrule`, `\bottomrule`,
no vertical rules, no colour, no shading. `\small` and reduced `\tabcolsep` only
when a table would otherwise overrun the text block. Multi-block headers use
`\multicolumn` with `\cmidrule(lr){…}` under each group.

**What rows and columns carry.** Rows are the experimental unit that varies —
models in the ladder, model × tier in the composition matrix — ordered by the
locked capability ranking, strongest first, never by effect size. Columns are, in
order: identity, then raw counts, then the derived difference, then the test
statistics. Counts are printed as `79/87`, numerator over denominator, **never as
a bare percentage**; the percentage follows in parentheses when it appears at
all. Δ is in percentage points with an explicit sign, always. The paired
disagreement counts `b` and `c` are their own columns beside the p-value.

**Captions.** One or two sentences. The pattern is: *what the table is*, then
`Source: \texttt{path/to/results.md}`, then how it was produced ("regenerated
deterministically from the committed logs"). Exit-classification captions add
the invariant that makes the table checkable: "every episode falls into exactly
one column, and each mode's columns sum to 87 per model." **Captions do not
state inferences.** The inference lives in the `\paragraph{Reading the table:}`
block that follows.

**Where statistics appear, and in what notation.**

- Never in the abstract. The abstract carries effect sizes only.
- Inside the experiment section, in the `Statistical test` block, split
  *Definition* / *Calculation* / *Inference*.
- p-values are written `p = 0.0078`, four decimals, or in scientific notation
  when small (`3.8e-06`, `$3.8 \times 10^{-6}$` in prose). Never `p < 0.05`
  alone.
- Every test is exact: exact binomial McNemar for paired binary outcomes, exact
  Spearman by enumeration over all 5,040 orderings. No asymptotic tests and no
  confidence intervals anywhere.
- `b = 0` is read as its own fact ("binding never lost a task advisory had
  solved"), not merely as an input to the p-value.
- Cost appears in every experiment section, in dollars to three decimals.

**How a null is reported.** At the same volume as a positive result, in its own
`Scoring the predictions` paragraph, failures first. The sentence "Three of four
confirmatory predictions failed, and reporting them as failures rather than
adjusting them afterwards is what the preregistration was for" is the paper's
model for this and should be matched in tone.

---

## 4. How limitations and claims boundaries are handled

**Limitations are a numbered list of nine, each a bolded phrase followed by two
or three sentences.** The section opens by stating where they come from and why
they are there: *"Every limitation below is drawn from the experiment ledger,
and stating them here is cheaper than having a reviewer state them for us."*

The nine cover, in order: corpus artificiality; the boundary condition the
effect requires; training contamination; a design decision made after seeing
pilots; small denominators, with the fragile claims separated from the robust
ones; the single-model ceiling; imported rather than measured covariates; the
narrowness of the difficulty axis; and operational scars.

**Claims boundaries are also enforced in three places outside the limitations
section**, and this is the more important pattern:

1. **Inline, at the moment of the claim.** "This is a real finding, not a null."
   "Mediation is not causal here, and no causal language is used." "With n = 2
   it may be coincidence."
2. **In the registration itself.** A prediction's disconfirmation condition is
   quoted before the result, so the reader can check the verdict against the
   clause rather than trust it.
3. **By separating exploratory from confirmatory,** explicitly and in advance:
   "the first four are confirmatory and the fifth is explicitly exploratory."

**Two named honesty devices worth carrying.** The paper discloses that a
prediction was registered *against* a dev-set glimpse that contradicted it, and
calls that "a risky prediction rather than a restatement of what the dev data
already showed". And it reports a stochastic component in an effect rather than
rounding it away: "the +9.2 pp therefore carries a small stochastic component,
and it is reported rather than rounded away."

---

## 5. Citation and figure-caption conventions

**Citations.** Four references, `thebibliography`, numeric keys
(`\cite{mcnemar1947}`). Citations appear only where a method or an external
measurement is used, never as background literature. There is no related-work
section and no positioning against prior art. Every citation is load-bearing:
two are the statistical tests, two are the external benchmarks that fix the
capability axis.

**Figure captions.** One or two sentences, then attribution. The attribution
names the script and, for data figures, the CSV: *"Drawn by
`writeup_figures/plot_all.py` from `writeup_figures/data/exp2_ladder.csv`."*
Diagram figures name only the script. Captions state what to look at, not what
to conclude: "the three regimes as shaded bands, filled dots for
McNemar-significant rungs."

**Figure placement.** `[t]` by default, `[H]` where the figure must not float
away from the table it accompanies. Widths are `\textwidth` for wide charts and
diagrams, `0.85` or `0.8\textwidth` for single-panel charts.

**Cross-references.** `\label`/`\ref` on every table and figure, but the prose
rarely says "see Figure 2" — the figure is placed where it is needed instead.

---

## 6. The verification apparatus around the paper

Recorded because the new paper should carry the same, and because it constrains
the schedule.

- `paper/source.txt` holds the approved prose. `check_verbatim.py` extracts a
  named section from it, strips LaTeX from the converted `.tex`, normalises both
  to word sequences and diffs them. **Exit 0 only on exact match**, apart from
  approved substitutions listed one per line in `paper/exceptions/<name>.txt` as
  `OLD>>>NEW`.
- `check_tables.py` parses the `tabular` rows of a named table out of the `.tex`
  and verifies **every printed cell** against the figure-pipeline CSVs.
- `writeup_figures/verify_data.py` recomputes every value in those CSVs from the
  committed analysis outputs and diffs them. Last recorded run: 307 values
  checked, 0 discrepancies.

The chain is: committed logs → `results.json` → `writeup_figures/data/*.csv` →
tables and figures → the typeset paper, with an automatic check at each arrow.

---

## 7. What the new paper inherits, at a glance

Carried without change:

- Mechanism diagram first, discipline diagram second, results third.
- The experiment-section skeleton, especially bridge → preconditions →
  predictions → results → reading → test → scoring → patterns → cost →
  deviations → inference.
- *Definition / Calculation / Inference* for every statistical test.
- Counts as `n/N`, never bare percentages. Signed effects. Exact tests only.
- Nulls at the same volume as positives, failures first.
- Limitations as a numbered list from the ledger, plus inline boundary sentences
  at the moment of each claim.
- Citations only where load-bearing; no related-work section.
- Every figure caption names the script that drew it.
- A cell-level table checker between the data and the typeset paper.

Known tensions, resolved in `OUTLINE.md`:

- The previous paper's captions state no inference; this paper's table design
  rule requires one inference per caption. **The new rule wins**, for the reason
  given in `OUTLINE.md`.
- The previous paper is a three-experiment cumulative narrative; this one is a
  four-experiment eliminative one, and the section skeleton has to carry a null
  as a *result* three times rather than once.
