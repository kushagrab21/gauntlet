# T4B — Experiment 2: the model can tell which tasks are safe to claim

| what the model was told it could do | kind of task | visits to the decision point | of those, it said DONE | share where it said DONE |
|---|---|---|---|---|
| may say DONE (control) (CTRL) | hides nothing | 58 | 50 | 0.8621 |
| may say DONE (control) (CTRL) | hides a convention | 62 | 11 | 0.1774 |
| told how many stages are hidden (WARN) | hides nothing | 59 | 47 | 0.7966 |
| told how many stages are hidden (WARN) | hides a convention | 59 | 12 | 0.2034 |
| both sets of rules pooled | hides nothing | 117 | 97 | 0.8291 |
| both sets of rules pooled | hides a convention | 121 | 23 | 0.1901 |

**Caption.** A task **hides a convention** when the code has to make a choice the task never states, several answers look reasonable, and the hidden tests accept exactly one; on such a task, passing everything visible does not mean the work is finished. A task that **hides nothing** is one where passing everything visible really does mean it is finished. Which kind a task is cannot be read from the bytes the model sees on its first turn: a leave-one-out classifier over those bytes scores 0.5185 against a base rate of 0.5259, a lift of -0.0074. A **visit to the decision point** is one moment where the model had passed everything visible with stages still hidden; a task can supply more than one. The 24-task annex is excluded because it carries no reliability label. The pooled difference is +0.6390, two-sided Fisher exact p = 2.75e-24. **The model claims far more often on tasks where claiming is correct, so it can tell at the decision point whether stopping is safe, and the failure is the threshold it applies to what it can tell rather than an inability to tell.**
