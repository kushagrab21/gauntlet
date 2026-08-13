# 11. What this means for building agents, and reproducibility

**Design advice.** The advice this programme licenses is narrower than the
previous paper's, and it should be stated as such. If an agent must judge for
itself when a task is finished, put the state it needs in front of it at the
moment it decides, already computed. Putting the same fact in the system prompt
did not work, across 115 paired tasks. Attaching a payoff to stopping early did
not work, within a bound that rules out a large increase. Printing one line of
arithmetic into the feedback at the moment of the decision moved 13 tasks
against 1 and halved the wrong claims.

Two qualifications travel with that. The first is that the placebo arm has not
run, so a designer following this advice is following a result whose mechanism
is not established. The second is that the intervention bought conservatism
rather than accuracy, and it was free here only because submitting again costs
nothing on this harness. A system that charges for a retry, whether in latency,
tokens or a user's patience, will price that trade differently and should
measure it before adopting the line.

**What to instrument.** The failure has a location and the location is cheap to
detect, because it is the state where every check the agent can run passes and
the agent knows more checks exist. A harness that logs nothing else can log that
state and count what its model does there, and that count is the quantity
everything in this paper turns on.

**Scale and cost.** The four experiments comprise 856 episodes over three
models, and the eleven runs cost $55.21. The whole programme including
calibration probing that produced no episode cost $61.25. An experiment that
locates a reliability failure and then tries three interventions against it fits
inside a rounding error on a compute budget, which is worth knowing before
choosing to ship a harness on intuition instead.

**Reproducibility.** Every number in this paper is recomputed from committed
episode logs by one command, reading only frozen result files, task metadata and
the checker, with no model call and no key. The whole programme is also
published as a flattened dataset of five tables and 9,194 rows, extracted once
and deterministically from the seventeen committed result files, so a reader can
ask a question with a `GROUP BY` rather than by rerunning anything. Both corpora
are pinned by content hash, each experiment's predictions are frozen at a commit
that provably precedes its first live call, and every deviation is recorded in an
append-only log.

**Provenance.** The harness, scaffolding and analysis code were built with AI
assistance under execution-verified acceptance gates, with every phase advancing
only on raw command output audited by the author and all deviations logged. The
research questions, the registered predictions, the verification discipline and
the interpretations are the author's.
