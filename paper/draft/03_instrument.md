# 3. The instrument

**The corpus.** The tasks are generated rather than collected, because the
property this paper needs is one no real repository can guarantee: that the
correct answer is not derivable from what the model was handed. Each
task is a short pure Python function with a defect, and behind the defect sits a
*hidden convention*, which is a decision the code must make that the description
never states and that several competent developers would answer differently.

Three admission rules keep the corpus measuring withheld information rather than
trivia. Every convention family lists at least three plausible readings, so a
guess cannot be a coin flip. Every family and every individual reading carries
attestations from at least two unrelated domains, so each convention is one that
real systems disagree about rather than one the author invented. And where
the withheld decision can be a value drawn from a large space, that is preferred
over a choice between enumerated branches, because the size of the space then
bounds how much a model could recover by guessing. The catalogue behind the
corpus records 93 attested readings with 186 attestations across 41 domains,
running from numbered standards to product behaviour to regulatory practice.
The first corpus holds 452 tasks and the second, built afterwards to pin
mechanical difficulty flat so that the only remaining variation is what the task
withholds, holds 159, of which 119 are the working set the later experiments
play.

**Staged release.** A task ships the tests the model can read plus a chain of
withheld stages. A stage is released only when every test
currently visible passes, and the depth of the chain is certified so that no
stage can be skipped, because at no point does the information for stage `k`
exist inside the stages before it. The consequence is the one the experiment
needs: passing everything visible is the trigger that reveals more work, so it
is the last thing a model should read as evidence that the work is over.

**The loop, and the claim.** Figure 1 draws the harness. The model submits code,
a checker runs the tests it is allowed to run and reports which failed, and the
loop repeats. Two things are added to that ordinary loop. The tests arrive in
stages, as above. And the model may reply with the single word `DONE` instead of
code, which ends the episode. The harness then runs the entire suite including
every unreleased stage, records whether the claim was true, and reports nothing
back. A reply counts as a claim only when the whole reply is the token, so a
message that merely mentions the word is treated as a submission.

<!--FIG:F1-->

**The vocabulary, in the order it is needed.** A *task* is one broken function
and its suite. A *stage* is a batch of tests the model cannot yet see, and a
*release* is the harness showing it one more stage. An *episode* is one model
working one task from the first message to the end, a *turn* is one message from
the model inside an episode, a *submission* is a turn carrying code, and a
*claim* is a turn carrying the token. An *arm* is one set of rules, differing
from another arm in exactly one sentence. A *run* is one model playing every
task in a list once under one arm, and an *experiment* is one comparison between
arms, with its predictions written down and frozen before the first episode.

**The arms.** Table 1 lists every run. Seven sets of rules appear across the
four experiments, and each differs from the arm it is compared against by at
most one sentence. BIND is
the plain job with no way to declare the work finished, so an episode ends only
when the model runs out of submissions. ADV is BIND plus the paragraph that
opens the claim channel, which reads `If you judge that the module as it
currently stands already passes every test - including tests you have not been
shown - reply with the single word DONE and nothing else, instead of a code
block. DONE ends the episode.` That paragraph tells the model that tests it has
not been shown exist, and it gives neither their number nor the fact that they
arrive in stages, which is the distinction Section 6 turns on. CTRL is ADV,
byte-identical, re-run on the second corpus.
WARN is CTRL plus one sentence in the rules: `This task's hidden tests are
released in exactly K stages.` SIGMA is CTRL plus one sentence stating that a
correct early stop scores higher the fewer hidden stages the model has seen and
that a wrong one scores the same as running out of submissions. CTRL′ is CTRL
again, unchanged, run in a later session. COUNT is the only arm whose change is
in the feedback rather than the rules, appending one line at every release:
`Released so far: stage R of K. Stages still withheld: N.`

<!--TAB:T1-->

**The discipline.** Both corpora were frozen by content hash before any episode
ran. Each experiment's predictions, together with the result that would confirm
each and the result that would refute it, were committed to a version-controlled
file before its first live call, and every deviation from plan was recorded in
an append-only log. A holdout split was reserved and never touched. Every number
in this paper is recomputed offline from committed episode logs by one command,
with no model call and no key, and two runs produce identical output.
