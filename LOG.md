
---

## Step 31 — DEC-050, the stop line waived, recorded before the readout runs (2026-08-10)

**DEC-050 — the owner directs that the Phase-C-2 readout be computed in the same
session that produced the records.** The brief for this session put the readout
in the next one, "the same separation as C-1", and Step 30 held that line and
said so. The owner has now waived it. This entry is written **before**
`readout_c2.py` exists, so nothing below it can have been shaped by what the
readout returned.

**What the separation was protecting, and what actually protects it.** Phase C-1
split Step 19 from Step 21 so that the session which watched the episodes land
could not tune the analysis to them. **That protection does not principally come
from the gap between sessions.** It comes from `REGISTRY_C2.md` being frozen at
`82b6463` before the first call, from every clause being a predicate function
enumerated over 15,524 outcomes by `--partition-check`, and from the readout
being forbidden to decide what *confirmed* means — it computes an outcome and
asks the frozen clauses what that outcome is called. All three of those hold
whatever session the readout runs in, and they are checkable by a reader who
trusts neither session.

**What is genuinely lost, stated rather than waved away.** The session has
already seen both arms' marginal claim counts, in Step 28. A readout author who
had seen nothing could not have been influenced by them; this one has. The
guard against that is that **there is nothing left to choose**: the population,
the direction, the statistic, the thresholds and the denominators were all fixed
in a frozen file, and the module's only freedom is in how it *prints*. Phase
C-1's own correction to Step 21 is the precedent for what that freedom can and
cannot do — adding baseline rows to a secondary changed the render hash and
moved **no** verdict, because the clause functions never saw the secondary.

**The rule is not amended.** `REGISTRY_C2.md` is not touched, and its §0 sentence
that the readout is not run in the session that produces the records reads
exactly as frozen. This is a waiver of a process separation on one session by
the owner, recorded as one, and not a precedent.

**Two things this does not license.** The readout still reads **COUNT against
CTRL′ and never against Phase B's CTRL**, and S-C2 is still **counts only, no
test** (DEC-045). Those are registered constraints on the analysis, not process
conveniences, and no waiver of the session boundary reaches them.

**Spend for this step: $0.00.**
