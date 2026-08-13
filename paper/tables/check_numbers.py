"""Recompute every dataset-derived number in `../NUMBERS.md` and compare.

    python3 -B check_numbers.py

Exit 0 only when every checked value matches the value recorded in NUMBERS.md.
Reads only `declare/data/` and the pinned exact tests. Calls no model.

WHAT THIS DOES NOT CHECK. Numbers that are readings rather than computations —
a registered verdict, a power figure fixed before the run, a corpus property
recorded at freeze time — are marked `written` in NUMBERS.md and carry a
write-up section instead of a command. Those are transcription, and the paper's
own check against the write-ups is what catches an error in them.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import make_tables as M  # noqa: E402

T = "true"


def ep(run):
    return [e for e in M.EPS if e["run_id"] == run]


def dn(run):
    return [d for d in M.DN if d["run_id"] == run]


def claims_at_d(run):
    return [d for d in dn(run) if d["claimed"] == T]


CHECKS = []


def check(name, got, want):
    CHECKS.append((name, got, want))


# --- programme scale -------------------------------------------------------
check("live runs", len(M.LIVE), 11)
check("live episodes that came back", len(M.EPS), 856)
check("live visits to the decision point", len(M.DN), 860)
check("DONEs, programme-wide", len([e for e in M.EPS if e["declared_done"] == T]), 608)
check("wrong DONEs, programme-wide",
      len([e for e in M.EPS if e["terminal_status"] == "declared_done_false"]), 74)
check("total booked spend over the eleven runs, USD",
      round(sum(float(M.RUN_BY_ID[r]["booked_usd"]) for r in M.RUN_ORDER), 2), 55.21)

# --- experiment 1 ----------------------------------------------------------
for model, short, want_cl, want_false in (
        ("claude-haiku-4.5_adv", "weakest model", 37, 0),
        ("claude-sonnet-5_adv", "middle model", 57, 2),
        ("claude-opus-5_adv", "strongest model", 67, 4)):
    e = ep(model)
    check("experiment 1, " + short + ", DONEs",
          len([x for x in e if x["declared_done"] == T]), want_cl)
    check("experiment 1, " + short + ", wrong DONEs",
          len([x for x in e if x["terminal_status"] == "declared_done_false"]),
          want_false)
check("experiment 1, episodes", sum(len(ep(r)) for r in M.RUN_ORDER[:6]), 407)
check("experiment 1, spend USD",
      round(sum(float(M.RUN_BY_ID[r]["booked_usd"]) for r in M.RUN_ORDER[:6]), 2),
      16.74)

# --- experiment 2 ----------------------------------------------------------
b1 = M.paired("claude-opus-5_ctrl", "claude-opus-5_warn")
check("experiment 2, tasks played both ways", b1["n_paired"], 115)
check("experiment 2, claimed under both", b1["both"], 63)
check("experiment 2, claimed only without the warning", b1["left_only"], 6)
check("experiment 2, claimed only with the warning", b1["right_only"], 6)
check("experiment 2, claimed under neither", b1["neither"], 40)
check("experiment 2, one-sided exact McNemar p",
      round(M.exact_mcnemar_one_sided(b1["right_only"], b1["left_only"])["p_value"], 4),
      0.6128)
check("experiment 2, control visits to the decision point",
      len(dn("claude-opus-5_ctrl")), 154)
check("experiment 2, control DONEs there", len(claims_at_d("claude-opus-5_ctrl")), 71)
check("experiment 2, control wrong DONEs there",
      len([d for d in claims_at_d("claude-opus-5_ctrl") if d["claim_true"] != T]), 21)
check("experiment 2, warned visits to the decision point",
      len(dn("claude-opus-5_warn")), 152)
check("experiment 2, warned DONEs there", len(claims_at_d("claude-opus-5_warn")), 69)
check("experiment 2, warned wrong DONEs there",
      len([d for d in claims_at_d("claude-opus-5_warn") if d["claim_true"] != T]), 19)
check("experiment 2, spend USD",
      round(float(M.RUN_BY_ID["claude-opus-5_ctrl"]["booked_usd"])
            + float(M.RUN_BY_ID["claude-opus-5_warn"]["booked_usd"]), 2), 19.79)

# the discrimination split
cells = {}
for gt in ("benign", "enforcing"):
    num = den = 0
    for rid in ("claude-opus-5_ctrl", "claude-opus-5_warn"):
        v = [d for d in dn(rid) if d["ground_truth"] == gt and M.core(d)]
        den += len(v)
        num += len([d for d in v if d["claimed"] == T])
    cells[gt] = (num, den)
check("experiment 2, DONEs on tasks that hide nothing", cells["benign"], (97, 117))
check("experiment 2, DONEs on tasks that hide a convention",
      cells["enforcing"], (23, 121))
check("experiment 2, difference between the two",
      round(cells["benign"][0] / cells["benign"][1]
            - cells["enforcing"][0] / cells["enforcing"][1], 4), 0.639)

# --- experiment 3 ----------------------------------------------------------
c1 = M.paired("claude-opus-5_ctrl", "claude-opus-5_sigma")
check("experiment 3, tasks played both ways", c1["n_paired"], 71)
check("experiment 3, claimed under both", c1["both"], 41)
check("experiment 3, claimed only without the reward", c1["left_only"], 5)
check("experiment 3, claimed only with the reward", c1["right_only"], 1)
check("experiment 3, claimed under neither", c1["neither"], 24)
check("experiment 3, one-sided exact McNemar p",
      round(M.exact_mcnemar_one_sided(c1["left_only"], c1["right_only"])["p_value"], 4),
      0.9844)
check("experiment 3, rewarded DONEs at the decision point",
      len(claims_at_d("claude-opus-5_sigma")), 42)
check("experiment 3, rewarded wrong DONEs there",
      len([d for d in claims_at_d("claude-opus-5_sigma") if d["claim_true"] != T]), 10)
check("experiment 3, spend USD",
      round(float(M.RUN_BY_ID["claude-opus-5_sigma"]["booked_usd"]), 2), 6.17)

# --- experiment 4 ----------------------------------------------------------
c4 = M.paired("claude-opus-5_ctrlprime", "claude-opus-5_count")
check("experiment 4, tasks played both ways", c4["n_paired"], 71)
check("experiment 4, claimed under both", c4["both"], 30)
check("experiment 4, claimed only without the count", c4["left_only"], 13)
check("experiment 4, claimed only with the count", c4["right_only"], 1)
check("experiment 4, claimed under neither", c4["neither"], 27)
check("experiment 4, one-sided exact McNemar p",
      round(M.exact_mcnemar_one_sided(c4["right_only"], c4["left_only"])["p_value"], 4),
      0.0009)
check("experiment 4, control DONEs at the decision point",
      len(claims_at_d("claude-opus-5_ctrlprime")), 44)
check("experiment 4, control wrong DONEs there",
      len([d for d in claims_at_d("claude-opus-5_ctrlprime") if d["claim_true"] != T]),
      12)
check("experiment 4, counted DONEs at the decision point",
      len(claims_at_d("claude-opus-5_count")), 31)
check("experiment 4, counted wrong DONEs there",
      len([d for d in claims_at_d("claude-opus-5_count") if d["claim_true"] != T]), 6)
check("experiment 4, spend USD",
      round(float(M.RUN_BY_ID["claude-opus-5_ctrlprime"]["booked_usd"])
            + float(M.RUN_BY_ID["claude-opus-5_count"]["booked_usd"]), 2), 12.51)

churn = M.paired("claude-opus-5_ctrl", "claude-opus-5_ctrlprime")
check("the churn floor, tasks that disagreed",
      churn["left_only"] + churn["right_only"], 2)
check("the churn floor, tasks played both ways", churn["n_paired"], 71)

L = {e["task_id"]: e for e in ep("claude-opus-5_ctrlprime")}
R = {e["task_id"]: e for e in ep("claude-opus-5_count")}
sup = [k for k in sorted(set(L) & set(R))
       if L[k]["claimed_at_D"] == T and R[k]["claimed_at_D"] != T]
check("experiment 4, suppressed claims that hid nothing",
      len([k for k in sup if L[k]["ground_truth"] == "benign"]), 8)
check("experiment 4, suppressed claims that hid a convention",
      len([k for k in sup if L[k]["ground_truth"] == "enforcing"]), 5)
check("experiment 4, correct DONEs before and after",
      (len([e for e in ep("claude-opus-5_ctrlprime")
            if e["terminal_status"] == "declared_done_true"]),
       len([e for e in ep("claude-opus-5_count")
            if e["terminal_status"] == "declared_done_true"])), (60, 63))

# --- where the wrong claims are -------------------------------------------
ep_by = {(e["run_id"], e["task_id"]): e for e in M.EPS}
buckets = {}
for c in M.CL:
    b = M.claim_bucket(c, ep_by)
    n_, f_ = buckets.get(b, (0, 0))
    buckets[b] = (n_ + 1, f_ + (1 if c["claim_true"] != T else 0))
check("DONEs at the decision point, and wrong ones", buckets["node_D"], (263, 73))

# --- the green-cue split that T7 asserts in its caption ----------------------
pooled = {}
for rid in ("claude-opus-5_ctrl", "claude-opus-5_warn", "claude-opus-5_sigma",
            "claude-opus-5_ctrlprime", "claude-opus-5_count"):
    for q in ("q0.25", "q0.75"):
        v = [d for d in claims_at_d(rid)
             if M.core(d) and M.EP_BY[(rid, d["task_id"])]["q_batch"] == q]
        num, den = pooled.get(q, (0, 0))
        pooled[q] = (num + len([d for d in v if d["claim_true"] != T]), den + len(v))
check("wrong DONEs where a green board is rarely worth it", pooled["q0.25"], (25, 65))
check("wrong DONEs where a green board is usually worth it", pooled["q0.75"], (6, 155))

# --- the branch nobody took ------------------------------------------------
# A turn sits in the visible-red state when the previous submission failed at
# least one test the model was allowed to see. The harness permits a DONE from
# there. Counted because a branch nobody takes is a finding, not an absence.
turns = [t for t in M.read("turns") if t["run_id"] in M.LIVE]
by = {}
for t in turns:
    by.setdefault((t["run_id"], t["task_id"]), []).append(t)
red = red_claims = 0
for rows in by.values():
    rows.sort(key=lambda r: int(r["turn"]))
    for i, t in enumerate(rows):
        if i == 0 or t["is_d_node"] == T:
            continue
        failing = rows[i - 1]["n_released_failing"]
        if failing and int(failing) > 0:
            red += 1
            red_claims += 1 if t["action"] == "DONE" else 0
check("turns with a visible test failing", red, 115)
check("DONEs said from a visible test failing", red_claims, 0)
check("DONEs once every stage was released, and wrong ones",
      buckets["ladder_unfolded"], (344, 0))
check("DONEs before any test had run, and wrong ones",
      buckets["before_any_test"], (1, 1))


def main():
    bad = 0
    for name, got, want in CHECKS:
        ok = got == want
        bad += 0 if ok else 1
        print(("PASS  " if ok else "FAIL  ") + name.ljust(58)
              + "got " + str(got).rjust(12) + "   want " + str(want))
    print()
    print(str(len(CHECKS)) + " check(s), " + str(bad) + " failed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
