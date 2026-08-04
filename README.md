# Gauntlet

This repository holds one measurement program in three parts. The question behind all of it: when a coding agent cannot see the whole specification, does it know that it cannot see it, or does it fill the gap from its priors and call the work finished.

The findings in one paragraph. Given a channel to declare a task complete, the frontier model `claude-opus-5` used it on 67 of 68 tasks and was wrong 4 times. All 4 errors fall in the hardest band, where the tests are released one stage at a time. The floor model `claude-haiku-4.5` used the same channel on 37 tasks and was wrong 0 times. In 5 of the 6 false claims across three models, every test failing at the moment of the claim belonged to a stage the model had not been shown. Each model had passed everything it could see and read that as done. Willingness to claim rises with capability, 0.544 then 0.838 then 0.985. Accuracy of the claim falls, 0.000 then 0.035 then 0.060 wrong among the claims made. The registered write up carrying all four predictions and their verdicts is `traverse/writeups/phase_a.md`.

Everything below is a map. Each state of the program has a place on disk, and each claim has a command that recomputes it. Corpus construction, verification and analysis run offline on the Python standard library with nothing installed. Only the live episodes need an API key, and their logs are committed, so every offline claim stays checkable without one.

## What is in here

| directory | what it is | size | frozen as |
|---|---|---|---|
| `gauntlet/` | the corpus. Broken Python functions whose correct behaviour depends on a convention the solver is never told, arranged in a ladder of seven levels | 452 tasks, 2818 files | `gauntlet-v1.0`, freeze hash `2cbe3bb2` |
| `traverse/` | the experiment. Three models, two arms, the same 68 development tasks in the same frozen order, registered before the first episode | 407 episodes, 1106 calls, $16.74 | no tag, pinned at `REGISTRY.md` commit `e62eb0f` |
| `dnc/` | the second corpus, built after the experiment to isolate the failure it found. Mechanical difficulty is pinned flat, so the only variation left is what the task withholds | 159 tasks, 1224 files | `dnc-v0.2`, freeze hash `fd828da6` |

Total live spend across the whole program is $22.78 over 610 episodes.

## Start here

1. Read this file.
2. Read `traverse/writeups/phase_a.md`. It is the result.
3. Read `gauntlet/README.md` for the corpus the experiment ran on, then `gauntlet/CATALOG.md` for the catalog of ambiguities every task draws from.
4. Read `dnc/README.md` and `dnc/LEAK.md` for the follow on corpus and for the measured leak that forced it to be rebuilt.

The three log files `gauntlet/CORPUS_LOG.md`, `traverse/LOG.md` and `dnc/LOG.md` are append only ledgers of every step and every deviation. They are reference material for looking things up, not reading material. When the text cites a decision code such as `D-011` or a surprise code such as `S-033`, the log is where that entry lives.

## The question

A code benchmark that hands a model a task description measures whether the model can work out how. This program measures something earlier: whether the model can work out what, and whether it notices when it cannot.

Every task in `gauntlet/` is a small broken Python function with a test suite. The function is pure, under forty lines, imports nothing, and carries no docstring or comment. Repairing it looks mechanical. The difficulty sits somewhere else. The code has to make a decision that nothing the solver can see states, and a hidden suite enforces one specific answer.

Is a record with no `value` field an error, a null, or a zero. Does a range include its upper bound. When every score in a group is null, is the average `None` or `0`. Do you get back a new list, or the caller's list, mutated.

Each of those questions has several defensible answers, and real systems disagree about which one is right. `gauntlet/CATALOG.md` records 93 such readings with 186 attestations across 41 domains, running from numbered standards such as RFC 4180 and IEEE 754, through product behaviour in Excel, PostgreSQL and Stripe, to business and regulatory practice such as HMRC VAT Notice 700. A task withholds one of these decisions and grades against a reading the corpus guarantees is never the one a Python developer writes unprompted.

If the information is genuinely absent from what the solver was handed, then reasoning cannot recover it. The solver can only guess, and the corpus is built so that guessing loses. What stays measurable is whether the solver notices the gap and interacts until it closes. That is what the ladder is for. At the shallow levels every enforcing test is visible from the first turn. At the deep levels the tests are released one stage at a time, and the only route through is to submit, learn what failed, and submit again.

The experiment in `traverse/` adds one binary channel to that loop. The model may reply with the token `DONE` instead of code.

- **BIND** ignores the claim. The episode ends when the hidden suite passes.
- **ADV** believes the claim and scores it against the hidden suite.

Everything else about the two arms is identical, down to byte identical feedback text. The false claim is the event the two arms were built to count.

## Reproduce it

This block replays the program in the order it happened. Offline steps carry their expected output. Paid steps are marked, and the whole live program cost under twenty three US dollars.

The key is never read from inside the repository. It resolves from an explicit `--key-file`, or from a sibling `api_key/` folder that sits outside the working tree. Keep it that way.

```bash
git clone --recursive https://github.com/kushagrab21/gauntlet.git
cd gauntlet

# the three parts are submodules, each one a repository with its own history
# and its own tags. If the clone above missed them:
git submodule update --init

# ---------- part 1: the corpus ----------
cd gauntlet

# every invariant re-measured from disk, and all 1297 recorded rejections replayed
python3 -m generator.validate --tasks
# takes a few minutes, runs every suite of every task several times over,
# and must end on the line TASKS GATE PASS

# the release identity, computed from the git index
python3 -m generator.freeze --rev gauntlet-v1.0
# must print FREEZE_HASH 2cbe3bb2b4637b165ce20dc9c20ed85715f5e4f474db56ba88b9bf72d7f5c51f
#            tasks=452 files=2818 rev=gauntlet-v1.0
# and must match corpus.freeze_hash in MANIFEST.json

# the calibration table, which refuses to print any cell measured on bytes other than the shipped bytes
python3 -m calibration.table_of_record

# the development and test split, rebuilt from its rule and compared
python3 -m calibration.split --check

# rebuild every task from seed families alone, about an hour of CPU, byte identical output
python3 -m generator.coupling --emit

# the calibration probes (paid step, $6.04 as run)
python3 -m calibration.probe --model anthropic/claude-haiku-4.5 --i-have-approval

cd ..

# ---------- part 2: the experiment ----------
cd traverse

# the registered readout: predictions P1 to P4, secondaries S1 to S3, stopping conditions
python3 -B -m analysis.readout

# the same, rendered twice from two independent loads and hashed
python3 -B -m analysis.readout --determinism
# must print 9d60eb9962d22366a5be8d436f7125b5c8de288ec5450488cd122351668f8629 twice

# the eight trajectory metrics over the six Phase A runs
python3 -B -m analysis.trajectory --phase-a

# the exploratory annex, which computes no significance test anywhere
python3 -B -m analysis.ab --determinism
# must print c7169c3d87341607b745ee94ac0b6d2330fb19a1aa4fe9bf939f038561d91993 twice

# which task and model pairs have been spent, derived from the committed files
python3 -B -m traverse.exposures
# must print pairs 407  distinct tasks 68  models 3, and test-split exposures: 0

# the arms, on stubs, offline and free
python3 -B -m traverse.run --stub reference --arm bind
python3 -B -m traverse.run --stub eager-done --arm adv

# a live arm (paid step, $16.74 for all six runs as run)
python3 -B -m traverse.run --model anthropic/claude-opus-5 --arm adv --approved

cd ..

# ---------- part 3: the second corpus ----------
cd dnc

# invariants, the freeze run twice, the stub triple, and the split
PYTHONDONTWRITEBYTECODE=1 python3 -B -m builder.verify_all
# must print 5/5 item(s) PASS

# the six indistinguishability checks behind the q knob
PYTHONDONTWRITEBYTECODE=1 python3 -B -m builder.d006
```

Everything after the two paid lines reads committed files and calls no model.

## The corpus: `gauntlet/`

Seven levels, differing in how much of the withheld information the solver can see and in how many mechanical defects sit on top of it.

| level | mechanical defects | secrets | tests | tasks |
|---|---|---|---|---|
| L0 | 1 | none | all visible | 5 |
| L1 | 2 to 3, independent | none | all visible | 25 |
| L2 | 2, coupled | none | all visible | 11 |
| L3 | 1 | 1 to 2 | all visible | 156 |
| L4 | 2, coupled | 1 to 2 | all visible | 42 |
| L5 | 1 | 2 to 3, chained | staged, depth 2 to 3 | 188 |
| L6 | 1 | 4, chained | staged, depth 4 | 25 |
| | | | | **452** |

A **secret** is a decision the code must make, the description does not state, and a competent developer could reasonably answer three or more ways. Three admission rules keep the corpus measuring withheld information instead of trivia. Every secret bearing family lists at least three plausible readings, so a guess cannot be a coin flip. Every family and every individual reading carries attestations from at least two unrelated domains, judged by field rather than by vendor. Where the secret can be a drawn value out of a large space, that is preferred over an enumerated branch, because the size of that space then bounds the entropy, and an enumerated branch is bounded by whatever options an author could think of.

**Staged release** is the mechanism the experiment turns on. At L5 and L6 a task ships `tests_visible.py` plus a chain of withheld modules, and stage `k` unlocks only once every test of the stages before it passes. The declared depth is certified by an oracle ladder, so no stage can be skipped, because at no point does the information for stage `k` exist in the stages before it. At those levels `buggy.py` carries none of the answers.

| state | where | pinned or checked by |
|---|---|---|
| the ambiguity catalog, 6 seats and 20 families and 93 attested readings | `CATALOG.md` | `python3 -m generator.validate --coverage` |
| the 452 tasks, never edited after the freeze | `corpus/L0/` through `corpus/L6/` | `python3 -m generator.freeze --rev gauntlet-v1.0` |
| the generator that mints them from seed families alone | `generator/` | `python3 -m generator.coupling --emit` reproduces every byte |
| everything the generator built and threw away, 1297 records | `REJECTIONS.json` | replayed by the task gate, each must still reject |
| the development and test split, 68 and 384 | `calibration/split.json` | `python3 -m calibration.split --check` |
| the calibration results, eleven files | `calibration/probe_*.json` | hashed individually in `MANIFEST.json` |
| the release identity, hashes and regeneration commands | `MANIFEST.json` | the freeze command above |
| contents, validation and the limitations | `DATASHEET.md` | |
| immutability, versioning and the issues logged against a v2 | `RELEASES.md` | |

Emission has no randomness, no clock, no filesystem read and no timestamp. Parameter draws come from a sha256 chain instead of `random`, whose stream is a documented and unstable implementation detail across Python versions. A clean checkout was emitted at three different absolute paths hours apart and compared file by file against the committed tree: 2873 files, zero differing, zero on one side only, three ways. The emitter's own stdout matched too, which is the stronger statement. Two runs that agree on the log agreed at every decision point along the way, and agreement on the final tree alone would leave the path between the decisions unchecked.

## The experiment: `traverse/`

Every model ran both arms over the same 68 development task ids in the same fixed stratified order, so every comparison is within task.

| state or action | where or command |
|---|---|
| the preregistration, frozen before the first live episode | `REGISTRY.md`, commit `e62eb0f` |
| the loop and the two arms | `traverse/episode.py` and `traverse/run.py` |
| the corpus pin the runs recorded | `CORPUS_PIN.json` |
| the saved record, one file per model and arm | `results/` |
| the registered readout | `python3 -B -m analysis.readout` |
| the exact tests behind it | `analysis/exact.py` |
| the trajectory metrics | `python3 -B -m analysis.trajectory --phase-a` |
| the registered write up | `writeups/phase_a.md` |
| the exploratory annex, carrying no significance test | `writeups/phase_a_ab_annex.md` |
| the descriptive baseline that spent nothing | `writeups/trajectories.md` |

The registration fixed the four predictions, the denominators, the tests and the disconfirmation conditions before any money was spent. One prediction was confirmed. One failed its significance test without meeting either registered disconfirmation condition. Two were disconfirmed, one of them in the opposite direction to the one predicted. All four are reported at the same volume, because a preregistration that reports only its wins is not a preregistration.

| | prediction | verdict |
|---|---|---|
| P1 | frontier models produce more than zero false claims at L5 and L6 | **CONFIRMED**, four, all in that band |
| P2 | the BIND minus ADV gap is hump shaped in capability at L0 to L4 | **NOT CONFIRMED**, the ordering holds and McNemar gives p = 1.0000 |
| P3 | the ADV to BIND rescue shrinks at L5 and L6 | **DISCONFIRMED**, it grew, 0.073 against 0.009 |
| P4 | the gap moves together with the false claim count | **DISCONFIRMED** on its ordering clause |

### The result in numbers

False claims by model and band, under ADV:

| model | rung | L0 to L4 | L5 and L6 | claimed | false | false rate among claims |
|---|---|---|---|---|---|---|
| `claude-haiku-4.5` | floor | 0 | 0 | 37 of 68 | 0 | 0.000 |
| `claude-sonnet-5` | interior | 1 | 1 | 57 of 68 | 2 | 0.035 |
| `claude-opus-5` | frontier | 0 | 4 | 67 of 68 | 4 | 0.060 |

The floor model's zero is not a failure of the instrument to fire. The `eager-done` stub declares completion at turn 1 unconditionally and is scored false on every task whose handed over file fails, which proves the counter counts.

P3 is the finding the registration did not expect. Seven tasks at L5 and L6 were solved under BIND that the same model failed under ADV, against one such task across the whole of L0 to L4. A completion gate supplies no information. It denies the model the option of declaring victory, and at the levels where information is withheld that alone is worth roughly eight times more than it is worth on the easy band.

## The second corpus: `dnc/`

The experiment located a reproducible failure at a single decision node. All visible tests pass, stages of hidden tests remain, and the model may either claim completion or submit again to release the next stage for free. `dnc/` is built to put a solver at that node as often and as cleanly as possible. Difficulty ladders are deliberately absent: mechanical difficulty is pinned trivial everywhere and every variation is epistemic.

| state | where | what it is |
|---|---|---|
| the plan of record, committed before the build | `PLAN.md` | with its sha256 recorded |
| the core, 135 tasks | `corpus/L5/` | q in {0.25, 0.75} by k in {2, 3} by arm in {high, low} |
| the annex, 24 tasks | `corpus/L6/` | k = 4, enforcing only, no q label, excluded from q analyses |
| the batch table and the ground truth flags | `BATCHES.json` | |
| the builder that minted the corpus | `builder/` | reproduces it exactly |
| the holdout, 40 of 159, never touched | `SPLIT.json` | `dnc-split-v1` |
| the leak that demoted the first version | `LEAK.md` | measured, with the command that reproduces it |

The corpus mixes tasks that withhold a convention, called **enforcing**, with tasks that withhold nothing, called **benign**. A recorded fraction `q` of each batch is benign, which makes visible green genuinely mean done for that fraction. The knob is only a knob when a solver cannot tell which half a task is in from the bytes it sees at turn 1.

**The first version failed that test, and the failure is documented instead of buried.** A leave one out classifier over turn 1 tokens read the benign or enforcing flag at 0.9097 against a base rate of 0.5000, a lift of +0.4097 past a threshold of 0.15 that was fixed in code before the run. Two channels caused it. The conservation block appeared in 59 of 72 enforcing tasks and 0 of 72 benign ones, and visible test volume differed because the benign builder had to fund its visible layer out of the same pool as its hidden stages. `dnc-v0.1` ships with the knob demoted and `LEAK.md` says exactly what it leaks.

**The fix is the shadow twin.** A benign task is rebuilt as an enforcing build with only its hidden side swapped, so `buggy.py` and `tests_visible.py` come off the identical code path, conservation block included, and both channels close by construction. On `dnc-v0.2` the same unchanged checker reads the flag at 0.5185 against a base rate of 0.5259, a lift of −0.0074. The classifier ends up below its own base rate, which means nothing is left in the bytes to read.

`dnc-v0.1` is kept rather than superseded. It fills two cells of the design table that `dnc-v0.2` cannot, because one host offers 31 byte distinct visible layers against a pair demand of 36, so the version that closes the leak is 159 tasks against the ruled 144 plus 24. Both trees are in the history and both are tagged.

## Limitations

The three documents carry the full lists. `gauntlet/DATASHEET.md` section 5 covers the corpus, `traverse/writeups/phase_a.md` covers the experiment, and `dnc/LEAK.md` covers what the first corpus version does not support. The short version follows.

**Four false claims are four events.** They establish existence against a baseline of zero. They do not establish a rate, and the per band rates should be read as descriptive accompaniment to a count.

**Three models on one provider, single runs.** Both arms of a model ran minutes apart on one day, which licenses the paired statistics used throughout and licenses no comparison against runs made elsewhere or later. Three points on the capability axis is the minimum that makes a question about shape askable and is not enough to answer one with confidence.

**The easy band is close to saturated.** Across three models and 107 paired tasks at L0 to L4 there are three discordant pairs in total, which is why P2 could be tested and could not be resolved.

**The solver cannot ask questions.** The only channels are a code submission and a single completion token. Nothing here speaks to how models behave when they can ask.

**The corpus tasks are synthetic single function repairs.** The effect exists in the regime where the specification is stripped from the presented code.

**The test split has never been shown to a model.** 384 of the 452 tasks remain unexposed, `traverse.exposures` reports zero test split exposures, and that number is derived from the committed files instead of book kept. A contaminated holdout is the one asset here that no command can regenerate, and nothing downstream can detect the contamination, because a result file on a leaked task looks exactly like a result file on a clean one.

## Provenance

This program follows the binding feedback experiment, which asked the same question on simpler tasks and found that moving completion authority from the model to a checker lifts a weak model by 9.2 points and leaves a strong one unchanged. That work identified the false claim as the mechanism. GAUNTLET was built because testing the mechanism properly needed tasks where the withheld information is real, catalogued and enforced, instead of merely stripped. `gauntlet/REUSE.md` records every item carried across, per item, with blob hashes.

The corpus generators, the harness and the analysis code were built with AI assistance under execution verified acceptance gates. Every phase advanced only on raw command output audited by the author, every rejection is recorded by machine instead of hand repaired, and all deviations live in the three logs. The research questions, the registered predictions and the interpretations are the author's.
