# OUTLINE.md — the new paper, section by section

**Working title (placeholder, owner to decide):** *Where a Coding Agent Decides
It Is Finished.*

**The spine, in one paragraph.** The previous paper found that moving completion
authority from the model to a checker changes outcomes, and it identified the
false claim as the mechanism. That paper could not isolate the mechanism,
because in its design a false claim could happen at any turn and its corpus was
built to measure something else. This paper builds an instrument that isolates
it: a corpus where the correct answer depends on a convention the model is never
told, and a harness that releases the enforcing tests one stage at a time. The
instrument locates the failure at **a single decision state** — the moment every
visible test passes and a stage is still hidden — where 73 of the programme's 74
wrong claims are made. It then eliminates three explanations for what happens
there: the model is not missing the information, it is not responding to the
incentive, and it is not failing to perceive which tasks are risky. One
intervention moves it: doing the arithmetic for the model, in the feedback, at
the moment it decides. The placebo control that would say whether the content or
the mere presence of that line did the work has not been run, and the paper says
so in the abstract.

**Target length: ~7,000 words across nine numbered sections plus abstract**,
against the previous paper's ~6,220. The increase is one extra experiment
section and a longer setup, and it is the maximum; see the open questions.

---

## Section map

Each entry gives the section's job, the material it consumes, the figures and
tables it owns, and its target length. Section numbering follows the previous
paper: the abstract is unnumbered, *Question* is section 1.

### Abstract — 260 words, unnumbered, one paragraph

**Job.** Name the failure, name the instrument, give the four experiments'
answers in order, and state the open control. Effect sizes only, no p-values,
per STRUCTURE.md §3.

**Consumes.** All four write-up summaries; the viz story tab's seven headlines
for the framing order.

**Must contain.** That the model *can* tell which tasks are risky (T4B) — this
is the finding that distinguishes this paper from the previous one and it
belongs in the abstract, not buried in section 6. That the placebo arm has not
been run.

**Owns.** Nothing.

---

### 1. Question — 700 words

**Job.** Start from where the previous paper ended, in the first person, as the
previous paper starts from a practical frustration. The previous paper showed
the gate pays for some models and not others, and that its value tracks the rate
of false claiming. That leaves the question this paper asks: what *is* a false
claim, where does it happen, and what would change it. Then define the failure
concretely and generalise to deployment.

**Consumes.** Previous paper §1 and §6 for the handoff; root `README.md` §"The
question"; the viz "Start here" walkthrough for the framing of one episode.

**Owns.** Nothing. F1 arrives in section 3.

**Note.** The previous paper put its mechanism diagram here. This paper cannot,
because its harness needs the staged-release idea defined first, and that needs
the corpus. See Deviation D1.

---

### 2. What the previous work established, and what it could not — 450 words

**Job.** A short, honest summary of the previous paper as the starting position:
the gate converts false claims into forced repairs, its value is the false-claim
rate times the ability to repair, and the window is a property of the model. Then
the three things that design could not do: the false claim had no located
moment, the corpus could not distinguish "did not know" from "did not check",
and the models were not asked to reason about what they had not been shown.

**Consumes.** Previous paper §6 and §7.

**Owns.** Nothing.

**Note.** This is a section the previous paper does not have — it had no
predecessor to summarise. It replaces a related-work section, which per
STRUCTURE.md §5 this programme does not write.

---

### 3. The instrument — 1,000 words

**Job.** The corpus, the staged release, the harness loop, the claim channel,
and the discipline. This is the previous paper's §2 (Setup), enlarged because
this paper's apparatus is the contribution.

Order: the corpus and why its tasks hide a convention → the ladder and staged
release → the loop and the claim channel (**F1**) → what a claim is scored
against and that the model is never told → the vocabulary, in the rule-2 order
of `LANGUAGE.md` → the arms as a table (**T1**) → the discipline: frozen
corpora, registrations frozen before each run, an append-only deviation log,
holdout untouched.

**Consumes.** Root `README.md` §"The corpus" and §"The question";
`gauntlet/CATALOG.md` for the ambiguity families; `phase_a.md` §"The design";
`declare/arms.py` docstring for the exact arm texts; `DATASHEET.md` for the
dataset and its gates.

**Owns.** **F1** (harness loop, extended). **T1** (the programme at a glance,
11 runs + total).

**Must contain.** The three admission rules for a hidden convention, in one
sentence each — they are what make the corpus an instrument rather than a set of
trick questions. The exact treatment sentence of each arm, quoted.

---

### 4. The decision point — 800 words

**Job.** The paper's pivot, and the section with no counterpart in the previous
paper. Define the state. Show that the harness makes it a genuine choice, with
one branch free. Then show that the failure lives there and almost nowhere else.

**Consumes.** `phase_c2.md` §S-C6 (the timing signature, replicated four times);
`phase_a.md` §"The common structure"; the viz state machine, which is total over
all 2,485 turns with no fallthrough.

**Owns.** **F2** (the decision point) and **F6** (the claim-timing signature).
**T2** (when the model said DONE, and whether it was right, 9 rows).

**Must contain.** That claiming from a board with a visibly failing test is
allowed by the harness and was taken zero times in 2,485 turns. That is a
finding about where the failure is not, and it is the cleanest evidence that the
model is responding to the visible board rather than being careless.

**The inference this section licenses, and the one it does not.** It licenses:
the error has one location. It does not license: the error is caused by anything
about that location. The three eliminations come next.

---

### 5. Capability makes it worse — 700 words

**Job.** Experiment 1. Three models, the same 68 tasks, with and without the
channel. Willingness to claim rises with capability and accuracy of the claim
falls.

**Skeleton.** Preconditions → predictions (P1–P4) → results (**T3**) → reading
the table → statistical test (*Definition / Calculation / Inference*) → scoring
the predictions, failures first → cost → inference.

**Consumes.** `phase_a.md` in full, especially §P1, §P3, §P4 and §"The
false-DONE floor".

**Owns.** **F5** (the capability ladder). **T3** (the capability ladder, 3 rows).

**Must contain.** That three of four registered predictions did not confirm, and
that the one confirmed prediction (P1) is evidence about *existence*, not about
a rate — `phase_a.md` says so explicitly and the paper must not quietly upgrade
it. That the strongest model made zero wrong claims in the easy band.

---

### 6. It is not missing information — 900 words

**Job.** Experiment 2. The first elimination, and the section that also carries
the paper's most surprising positive result.

**Skeleton.** Bridge (the obvious explanation of section 5: nothing tells the
model how many stages exist) → preconditions → predictions (B1–B4) → results
(**T4**, **F4** panel 1) → reading → test → scoring → **the discrimination
split (T4B)** → inference.

**Consumes.** `phase_b.md` in full, especially §B1, §B2 and §S1.

**Owns.** **T4** (paired flips, 2 rows). **T4B** (discrimination split, 6 rows).
Panel 1 of **F4**.

**Must contain.** The pooling trap from `NUMBERS.md` §4: the published S1 and B3
figures are over the eight files that existed at publication, and the paper must
quote those and name the population. The reason the discrimination is not a
corpus leak — the model is reading the stage it was just handed, which is the
job — stated in the two sentences `phase_b.md` uses.

**Why the discrimination split lives here and not in the mechanism section.** It
is the result that reframes the whole paper: the model is not blind, so every
later experiment is about a threshold rather than about perception. Holding it
back to section 9 would make sections 7 and 8 read as searches for something the
paper already knows is absent.

---

### 7. It is not the incentive — 600 words

**Job.** Experiment 3. The second elimination, and the weakest section in the
programme. Its honest content is a bound in one direction.

**Skeleton.** Bridge → preconditions → predictions (C1, C2, C5) → results
(**T5**, **F4** panel 2) → reading → test → scoring → **the power statement,
quoted from the registration** → inference.

**Consumes.** `phase_c1.md` §C1 and §C2.

**Owns.** **T5** (paired flips, 2 rows). Panel 2 of **F4**.

**Must contain.** The registered power figures *before* the result, so the
reader can see the design was known to be blind to a shift this size before the
number is shown. The reverse-direction p = 0.1094, labelled as descriptive and
never registered. That the reward was stated and never delivered.

**Length discipline.** This section is short on purpose. A null that the design
could not have seen deserves accurate reporting, not volume.

---

### 8. The arithmetic, at the decision point — 900 words

**Job.** Experiment 4. The one intervention that moved the behaviour, and the
churn floor that makes every discordance count in the paper interpretable.

**Skeleton.** Bridge (both previous arms put the information or the incentive in
the contract and asked the model to carry it) → preconditions → predictions (C4,
C6, C8) → results (**T6**, **F4** panel 3) → reading → test → scoring → **the
churn floor and what it does to sections 6 and 7** → where the suppressed claims
went → the limitation, stated here and not deferred → inference.

**Consumes.** `phase_c2.md` in full.

**Owns.** **T6** (paired flips plus churn floor row, 3 rows). Panels 3 and 4 of
**F4**, the second of which is the churn floor itself.

**Must contain.** That the counter supplies no information the warned model
lacked. That the thirteen suppressed claims were eight benign and five
enforcing, so the intervention bought conservatism rather than accuracy, and
that this cost nothing only because submitting again is free on this harness.
That the confound with sentence length is unresolved.

---

### 9. What the four experiments say together — 700 words

**Job.** The previous paper's §6, in the same role: one place where the whole
argument is visible. Three explanations eliminated, one intervention found, one
mechanism proposed and not established.

**Owns.** **F3** (the timeline). **T7** (wrong-claim rate against how much a
green board is worth, 12 rows). **T8** (every registered prediction and its
verdict, 14 rows). **T9** (the five sets of rules as rows, 5 rows).

**Consumes.** All four write-ups' verdict tables; `phase_c2.md` §S-C8.

**The proposed mechanism, stated as a proposal.** The model reads the green
board as evidence of completion, weights it by a reliability it cannot observe
(T7), and applies a threshold that is too low. Information about the hidden
stages does not move the threshold when it is in the contract (section 6). A
payoff does not move it (section 7). The same information moves it when it
arrives already computed, in the channel the model is reading, at the moment of
the decision (section 8). **The paper's claim is that the failure is one of
integration at the decision point, and its own evidence for that is one
experiment with an unrun control.**

**Note on F3's placement.** STRUCTURE.md §2 records the previous paper's
mechanism-first ordering, which would put the timeline in section 3. It is here
instead; see Deviation D3.

---

### 10. Limitations — 500 words

**Job.** A numbered list, as the previous paper's §7, drawn from the programme's
own logs and registrations. Draft list, in order:

1. **The placebo arm has not been run.** Experiment 4 cannot separate the
   content of the counter line from the presence of an extra sentence.
2. **One model carries three of the four experiments.** Experiments 2 to 4 are
   all `claude-opus-5`. The capability result is three models, and every
   elimination is one.
3. **One provider, and a snapshot.** No replication across providers.
4. **The strongest experiment is 71 paired tasks.** Effects live in counts of
   single digits, which is why every test here is exact and why no confidence
   interval appears.
5. **Two experiments ran on different days from their controls.** The churn
   floor calibrates this once; it says what a third identical run would probably
   do, not what a different day would.
6. **The corpus is synthetic and its conventions are drawn from a catalogue.**
   Whether the same failure appears on organic under-specification is untested.
7. **Experiment 1's registrations did not partition the outcome space**, which
   is why one prediction is recorded as neither confirmed nor disconfirmed.
8. **Absent episodes.** Four in experiment 2, and one each elsewhere; they are
   dropped from paired statistics rather than counted as failures.
9. **Operational scars**, including the waived publish gate and the pooling
   behaviour recorded as `SUR-008`.

**Consumes.** `phase_c2.md` §"Scope and limits"; `phase_c1.md` §C1;
`phase_b.md` §"Paired denominator"; `declare/LOG.md` deviation codes.

---

### 11. What this means for building agents, and reproducibility — 450 words

**Job.** The previous paper's §8, same three parts. The design advice this
programme licenses is narrower than the previous paper's and must be stated as
such: **if an agent must decide for itself when a task is finished, put the
state it needs in front of it at the moment it decides, already computed.**
Putting it in the system prompt did not work. Paying for it did not work.

Then scale and cost: 856 episodes, $55.21, offline reproduction of every number.
Then reproducibility: the five-table dataset, the gates, the registration
commits. Then the provenance paragraph on AI assistance, matching the previous
paper's.

---

### 12. References — 120 words

Four to six entries. The two exact tests carry over (McNemar 1947, and Fisher).
No related-work section, per STRUCTURE.md §5.

---

## Figures and tables, consolidated

| id | what | owner section | rows | source |
|---|---|---|---|---|
| F1 | the harness loop, extended | 3 | — | diagram |
| F2 | the decision point | 4 | — | diagram |
| F3 | the programme timeline | 9 | — | `runs.csv` dates, T3, T6, paired cells |
| F4 | paired flips, four panels including the churn floor | 6, 7, 8 | — | paired cells from `declare/data/` |
| F5 | the capability ladder | 5 | — | T3 |
| F6 | the claim-timing signature | 4 | — | T2 |
| T1 | the programme at a glance | 3 | 12 | computed |
| T2 | when the model said DONE | 4 | 9 | computed |
| T3 | the capability ladder | 5 | 3 | computed |
| T4 | experiment 2 paired flips | 6 | 2 | computed |
| T4B | the discrimination split | 6 | 6 | computed |
| T5 | experiment 3 paired flips | 7 | 2 | computed |
| T6 | experiment 4 paired flips, with the churn floor | 8 | 3 | computed |
| T7 | wrong-claim rate against green-board reliability | 9 | 12 | computed |
| T8 | every registered prediction and its verdict | 9 | 14 | transcribed |
| T9 | the five sets of rules as rows | 9 | 5 | computed |

Regenerate: `cd paper/tables && python3 -B make_tables.py --hash`, then
`cd paper/figures && python3 -B make_figures.py --check`.
Verify: `python3 -B make_tables.py --check` and `python3 -B check_numbers.py`.

---

## Deviations from STRUCTURE.md

Each names the rule it departs from and why.

**D1 — the mechanism diagram moves from section 1 to section 3.**
STRUCTURE.md §2 records mechanism-first, discipline-second. F1 cannot be
understood before staged release is defined, and staged release needs the
corpus. The compensating move: section 1 still opens on the mechanism in prose,
and F1 sits at the head of section 3 rather than the end.

**D2 — captions state an inference; the previous paper's do not.**
STRUCTURE.md §3 records that the previous paper's captions carry *what the table
is* and its source, with the inference held back to a `Reading the table`
paragraph. This paper's table design rule requires one inference per caption, in
the caption's last sentence. The rule wins because this paper has fourteen
tables to the previous paper's five, and several will be read out of order or in
isolation by a reader following a link. Consequence to accept: the `Reading the
table` paragraphs must not repeat the caption's sentence.

**D3 — the timeline figure sits at the end, not the start.** A timeline of four
experiments given before the reader knows what the decision point is would be a
list of unfamiliar names. F3 is placed in section 9 as a summary. If a reviewer
asks for a roadmap, the fallback is to place F3 in section 2 and cut its outcome
boxes to one line each.

**D4 — an extra section (2) summarising the previous work.** The previous paper
had no predecessor. It is short and it replaces the related-work section this
programme does not write.

**D5 — a new section (4) with no counterpart, and it is the pivot.** The
previous paper had no located failure state to define.

**D6 — three of the four experiment sections report a null or an elimination as
their main result.** STRUCTURE.md §3 records the previous paper's rule that
nulls are reported at the same volume as positives, and this paper inherits it,
but the ratio is different: the previous paper had one disconfirmed section out
of three, and this one has two eliminations plus a partly-null first experiment.
The consequence is that the *bridge* paragraphs carry more weight than they did,
because each elimination has to hand the reader a reason to keep reading. This
is a writing risk, and it is the main thing to watch in the first draft.

**D7 — no capability axis.** The previous paper's signature figure plots an
effect against an externally-fixed capability ranking. This paper has three
models in one experiment and one model in three, so no such axis exists. F4
replaces it as the signature figure. If the owner wants a capability figure, it
requires running experiments 2 to 4 on more models, which is new spend.

---

## What the writing session must not do

- Use a number that is not in `NUMBERS.md`.
- Compare rates across days. Only the paired comparisons are licensed.
- Present the counter's effect as an effect of its content. The placebo arm has
  not been run, and the abstract says so.
- Describe experiment 3 as evidence that a reward reduces claiming.
- Print an arm code as a bare token in prose. See `LANGUAGE.md`.
- Edit anything under `traverse/`, `declare/writeups/`, `declare/data/` or the
  corpora. The registered write-ups are the record; this directory is the paper.
