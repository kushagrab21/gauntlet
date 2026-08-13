# NUMBERS.md — every number the paper may assert

**The rule for the writing session: a number that is not in this file may not
appear in the paper.** If the draft needs one that is missing, add it here first,
with its source, and re-run the checker.

**Two kinds of entry.**

- `computed` — recomputed from `declare/data/` by `tables/check_numbers.py`.
  62 of these are checked on every run, and the checker exits non-zero if any
  drifts. Run it before the writing session and after any edit to a table.
- `written` — a reading rather than a computation: a registered verdict, a power
  figure fixed before the run, a corpus property recorded at freeze time, a
  provider bill. These carry a write-up section instead of a command, and they
  are transcription. Check them by eye against the cited section.

```bash
cd paper/tables
python3 -B check_numbers.py     # 62 checks, must end "0 failed"
python3 -B make_tables.py --check
```

Conventions used below, and to be used in the paper: a count is written `n/N`
with the denominator visible; a rate is given to four decimals; a p-value is
given to four decimals, or in scientific notation when smaller than 0.0001;
money is given to the cent.

---

## 1. The programme as a whole

| value | what it is | kind | source |
|---|---|---|---|
| 11 | runs that called a real model | computed | `check_numbers.py` |
| 6 | further runs against offline stubs, excluded from every table | written | `DATASHEET.md` §"The seventeen sources" |
| 856 | episodes that came back, across the eleven runs | computed | `check_numbers.py` |
| 2,485 | turns the models took in those episodes | computed | `turns.csv`, rows whose `run_id` is one of the eleven |
| 860 | visits to the decision point | computed | `check_numbers.py` |
| 608 | times a model replied DONE | computed | `check_numbers.py` |
| 74 | times DONE was wrong | computed | `check_numbers.py` |
| $55.21 | booked spend over the eleven runs | computed | `check_numbers.py` |
| $61.25 | live spend across the whole programme, including calibration probing that produced no episode | written | root `README.md` §"What is in here" |
| $6.04 | the calibration probing inside that total | written | root `README.md` reproduce block |
| 9,194 | rows in the flattened dataset, five tables | written | `DATASHEET.md` header |
| 5,082 / 1,673 / 846 | turns, decision-point visits and DONEs across all seventeen files including the stubs | written | `DATASHEET.md` table |

**Do not mix the two populations.** Every figure the paper prints is over the
eleven live runs. The seventeen-file figures exist only to explain why the live
numbers are smaller, and if one appears it must be named as such in the same
sentence.

## 2. The corpus

| value | what it is | kind | source |
|---|---|---|---|
| 452 | tasks in the first corpus, seven levels | written | root `README.md` §"The corpus" |
| 159 | tasks in the second corpus, built to pin mechanical difficulty flat | written | root `README.md` §"What is in here" |
| 119 | working tasks of the second corpus, the set experiments 2 to 4 play | written | `phase_b.md` §"How to regenerate" |
| 72 | the frozen prefix experiments 3 and 4 play | written | `phase_c1.md` §"How to regenerate" |
| 93 / 186 / 41 | attested readings, attestations and domains in the ambiguity catalogue | written | root `README.md` §"The question" |
| 0.5185 vs 0.5259 | a classifier's accuracy against the base rate for reading the task class off the bytes the model sees on turn 1, a lift of −0.0074 | written | `phase_b.md` §S1 |

## 3. Experiment 1 — the failure exists, and capability makes it worse

| value | what it is | kind | source |
|---|---|---|---|
| 68 | tasks, played by three models under both sets of rules | written | `phase_a.md` §"The design" |
| 407 | episodes | computed | `check_numbers.py` |
| $16.74 | spend | computed | `check_numbers.py` |
| 37/68 = 0.5441 | weakest model, tasks where it said DONE | computed | `check_numbers.py`, T3 |
| 57/68 = 0.8382 | middle model, tasks where it said DONE | computed | `check_numbers.py`, T3 |
| 67/68 = 0.9853 | strongest model, tasks where it said DONE | computed | `check_numbers.py`, T3 |
| 0 / 2 / 4 | wrong DONEs, weakest to strongest | computed | `check_numbers.py`, T3 |
| 0.0000 / 0.0351 / 0.0597 | share of each model's DONEs that were wrong | computed | T3 |
| 4 | wrong DONEs by the strongest model, all in the hardest band, none in the easy band | written | `phase_a.md` §P1 |
| 5 of 6 | wrong claims where every failing test belonged to a stage that had not been released | written | `phase_a.md` §"The common structure" |
| 1 | wrong claim made before any test had run, by the middle model on `L3-109`, with zero submissions | computed | `check_numbers.py`; described in `phase_a.md` §"The sixth false claim" |
| 1/107 = 0.009 vs 7/96 = 0.073 | tasks rescued by removing the channel, easy band against hard band, pooled | written | `phase_a.md` §P3 |

## 4. Experiment 2 — it is not missing information

| value | what it is | kind | source |
|---|---|---|---|
| 118 / 116 | episodes that came back, control and warned | computed | T1 |
| $19.79 | spend | computed | `check_numbers.py` |
| 115 | tasks played under both | computed | `check_numbers.py`, T4 |
| 63 / 6 / 6 / 40 | both, control only, warned only, neither | computed | `check_numbers.py`, T4 |
| 12 | tasks that changed answer | computed | T4 |
| p = 0.6128 | one-sided exact McNemar in the registered direction | computed | `check_numbers.py` |
| 154 / 71 / 21 | control visits to the decision point, DONEs there, wrong ones | computed | `check_numbers.py`, T4 |
| 152 / 69 / 19 | the same three under the warning | computed | `check_numbers.py`, T4 |
| 0.6017 / 0.5948 | share of tasks with at least one DONE at the decision point | computed | T4 |
| 0.4610 / 0.4539 | the same per visit rather than per task | written | `phase_b.md` §B1 |
| 97/117 = 0.8291 | DONEs at the decision point on tasks that hide nothing | computed | `check_numbers.py`, T4B |
| 23/121 = 0.1901 | DONEs at the decision point on tasks that hide a convention | computed | `check_numbers.py`, T4B |
| +0.6390 | the difference between those two | computed | `check_numbers.py`, T4B |
| p = 2.75e-24 | two-sided Fisher exact on that difference | computed | T4B |
| 0.4324 vs 0.0482 | share of DONEs that were wrong, in the batch where a green board is rarely trustworthy against the batch where it usually is | written | `phase_b.md` §B3; T7 gives the same split per run |
| 1.0261 both, delta +0.0000 | submissions to the first all-visible-pass, control against warned | written | `phase_b.md` §B4 |
| 0.6613 vs 0.6129, delta −0.0484, band ±0.05 | reach for the majority reading at stage 1, inside its band by 0.0016 | written | `phase_b.md` §B4 |

**A pooling trap, recorded because it has already produced two wrong numbers
once.** `phase_b.md`'s pooled cells were computed over the eight files that
existed when it was published. Recomputed over every file that exists now, B3's
first cell reads 19F/27T rather than 16F/21T and S1's pooled difference reads
+0.6656 rather than +0.6390. No verdict moves and every per-arm row is
unchanged. **The paper must quote the published figures and say which
population they are over.** T4B and T7 are computed over the experiment-2 runs
only, which is why they reproduce the published values. This is `SUR-008` in
`declare/LOG.md`.

## 5. Experiment 3 — it is not the incentive

| value | what it is | kind | source |
|---|---|---|---|
| 72 | episodes | computed | T1 |
| $6.17 | spend | computed | `check_numbers.py` |
| 71 | tasks played under both | computed | `check_numbers.py`, T5 |
| 41 / 5 / 1 / 24 | both, control only, rewarded only, neither | computed | `check_numbers.py`, T5 |
| 6 | tasks that changed answer, five of them against the prediction | computed | T5 |
| p = 0.9844 | one-sided exact McNemar in the registered direction | computed | `check_numbers.py` |
| p = 0.1094 | the same test run the other way, descriptive and never registered | written | `phase_c1.md` §C1 |
| 46 / 13 and 42 / 10 | DONEs at the decision point and wrong ones, control against rewarded, on the same 72 tasks | computed | T9 |
| 0.6479 / 0.5833 | share of tasks with a DONE at the decision point | computed | T9 |
| −0.0646 | the realised shift | written | `phase_c1.md` §C1 |
| 0.80 at 0.155, 0.50 at 0.10, 0.18 at 0.05 | the power this design was registered as having, before the run | written | `phase_c1.md` §C1 |
| 25 | tasks that did not claim under the control, recorded in advance as the room an increase had to grow into; one of them moved | written | `phase_c1.md` §C1 |

**The bound, stated exactly.** Experiment 3 rules out a large increase in
claiming from a stated reward, on this model, this corpus and this prefix. It
does not establish that the reward reduced claiming. Both halves must travel
together wherever the experiment is described.

## 6. Experiment 4 — the arithmetic, at the decision point

| value | what it is | kind | source |
|---|---|---|---|
| 72 / 71 | episodes, control re-run and counted | computed | T1 |
| $12.51 | spend | computed | `check_numbers.py` |
| 71 | tasks played under both | computed | `check_numbers.py`, T6 |
| 30 / 13 / 1 / 27 | both, control only, counted only, neither | computed | `check_numbers.py`, T6 |
| 14 | tasks that changed answer, thirteen against one | computed | T6 |
| p = 0.0009 | one-sided exact McNemar in the registered direction | computed | `check_numbers.py` |
| 44 / 12 and 31 / 6 | DONEs at the decision point and wrong ones, control against counted | computed | `check_numbers.py`, T6 |
| 0.6111 / 0.4366 | share of tasks with a DONE at the decision point | computed | T6 |
| 0.1745 | the realised shift, against a design powered for 0.155 | written | `phase_c2.md` §C4 |
| 0.2727 → 0.1935 | share of DONEs at the decision point that were wrong | written | `phase_c2.md` §C4 |
| 8 benign, 5 enforcing | what the thirteen suppressed claims were | computed | `check_numbers.py` |
| `L5-099` | the one task that moved the other way; it is benign, the claim was right, and it is also one of the two churn-floor tasks | written | `phase_c2.md` §C4 |
| 60 → 63 | correct DONEs, control against counted | computed | `check_numbers.py` |
| 60 → 64 | tasks solved by the bound | computed | `episodes.csv`, `solved` column |
| 2 of 71 = 0.0282 | the churn floor: two identical runs disagreeing with each other | computed | `check_numbers.py`, T6 |
| 0.10435 | the threshold the churn floor was registered against | written | `phase_c2.md` §C6 |
| 141 | DONE terminals in this experiment, every wrong one at the decision point and none off it | written | `phase_c2.md` §S-C6 |

## 7. Where the wrong claims are — the paper's central table

| value | what it is | kind | source |
|---|---|---|---|
| 263 DONEs, 73 wrong | at the decision point | computed | `check_numbers.py`, T2 |
| 344 DONEs, 0 wrong | once every stage had been released | computed | `check_numbers.py`, T2 |
| 1 DONE, 1 wrong | before any test had run | computed | `check_numbers.py`, T2 |
| 25 of 65 against 6 of 155 | wrong DONEs at the decision point, in the batch where a green board is rarely worth it against the batch where it usually is, pooled over all four experiments | computed | `check_numbers.py`, T7 |
| p = 2.22e-10 | two-sided Fisher exact on that split | computed | T7, from `declare.exact` |
| 115 turns, 0 DONEs | turns where a test the model could see was failing, and the DONEs said from that state | computed | `check_numbers.py` |
| 14 predictions: 8 confirmed, 5 refuted, 1 neither | the registered predictions across the four experiments | written | T8 caption, transcribed from the four write-ups |

**73 of 74 wrong claims are at one state.** The remaining one is the turn-1
claim in experiment 1. The count of *correct* claims made after full release
(344) is what makes the concentration meaningful: the model says DONE often and
safely once nothing is hidden, and the error is specific to the state where
something is.

## 8. Numbers the paper must not assert

Recorded so the writing session does not reach for them.

- **Any comparison of raw rates across days.** The five runs in T9 span two
  days. Only the paired comparisons in T4, T5 and T6 are licensed.
- **A causal claim from the co-movement of claiming and capability in
  experiment 1.** Three models is rank agreement, not mediation. `phase_a.md`
  §P4 registered this restraint and honours it.
- **That the count in experiment 4 worked because of its content.** The design
  cannot separate content from the presence of an extra sentence. The placebo
  arm has not been run.
- **Turn counts compared across the two sets of rules in experiment 1.** The
  arms end on different conditions by construction, which `phase_a.md` §"The
  design" registers as forbidding the comparison.
- **Any figure over the six offline stub runs**, unless the sentence says it is
  an instrument check.
