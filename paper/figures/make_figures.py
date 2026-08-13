"""Every figure in the paper, drawn from committed data by this script.

    python3 -B make_figures.py            # write F1..F6 png into this directory
    python3 -B make_figures.py --hash     # write, then print one sha256 per file
    python3 -B make_figures.py --check    # render twice, require byte-identical

NOTHING IN THIS SCRIPT IS A LITERAL NUMBER FROM THE EXPERIMENTS. Layout,
labels and annotation text are here; every quantity is read either from
`../tables/*.csv` or, for the paired cells that no table prints as a column,
from `declare/data/` through `tables/make_tables.py`. Importing the table
builder rather than recomputing means a figure and the table beside it cannot
disagree, and it is why `paired()` appears in one place in this repository.

DETERMINISM. `savefig` is called with `metadata={"Software": None}` so no
version string or date is written into the PNG, and two runs of `--check`
compare the bytes. A figure that changed because it was redrawn on a different
day would make the byte check useless.

THE VISUAL VOCABULARY is the previous paper's, and `style.py` is copied from it
byte-identical, so the palette and the matplotlib rc are the same objects that
drew its figures. The grammar it establishes:

    grey box            an input, or a party that does not hold the authority
    blue box            an active state or artifact
    dashed grey box     something sealed or withheld from the model
    green box           a terminal that counts as finished
    red-edged box       a terminal that counts as a wrong claim
    solid grey arrow    an action, labelled in grey italic
    amber               the channel this paper measures
    bullet key          the grammar, restated under each diagram

Plot conventions are also the previous paper's: the title sits above the axes,
counts are printed on the bars, the y grid only, and the source of the numbers
is named in the LaTeX caption rather than inside the image.
"""

import argparse
import csv
import hashlib
import os
import shutil
import sys
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

import style  # noqa: E402

style.apply()
C = style

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
TABLES = os.path.join(PAPER, "tables")
OUT = HERE

sys.path.insert(0, TABLES)
import make_tables as MT  # noqa: E402

NODE, NEDGE = "#eef4fc", C.S1_BLUE
GOOD, GEDGE = "#e6f4e6", C.S6_GREEN
BAD, BEDGE = "#fdecec", C.CRITICAL
SEALED, SEDGE = "#f1f1ee", C.MUTED

_written = []


def table(name):
    with open(os.path.join(TABLES, name + ".csv"), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


LAYOUT = False


def save(fig, name):
    path = os.path.join(OUT, name)
    if LAYOUT:
        for i, ax in enumerate(fig.axes):
            layout_report(fig, ax, name + (":%d" % i if len(fig.axes) > 1 else ""))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)
    _written.append(path)
    return path


# ---------------------------------------------------------------------------
# Diagram primitives, shared by F1 and F2
# ---------------------------------------------------------------------------

def box(ax, x, y, w, h, text, fc, ec, tc=C.INK, fs=9.5, weight="normal",
        dashed=False, lw=1.2):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.012,rounding_size=0.015",
                       fc=fc, ec=ec, lw=lw, zorder=3,
                       linestyle="--" if dashed else "-")
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
            zorder=4, linespacing=1.35, fontweight=weight)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0, ly=0, color=None,
          dashed=False, curve=0.0, fs=8.6):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                        color=color or C.MUTED, lw=1.3, zorder=2,
                        shrinkA=3, shrinkB=3,
                        linestyle="--" if dashed else "-",
                        connectionstyle="arc3,rad=" + str(curve))
    ax.add_patch(a)
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=fs,
                color=color or C.INK2, ha="center", va="center", zorder=5,
                style="italic",
                bbox=dict(fc=C.SURFACE, ec="none", pad=1.2))


def key(ax, x, y, lines, fs=8.6, gap=0.42):
    for i, ln in enumerate(lines):
        ax.text(x, y - i * gap, "•  " + ln, fontsize=fs, color=C.INK2,
                ha="left", va="top")


def measure(ax, text, fs, weight="normal", style="normal", linespacing=1.35):
    """The width and height of a string in data units, as it will render.

    Guessing a label's width from its character count is how text ends up
    outside its box: the body face is wide, and one long word in a three-line
    label decides the whole width. This draws the string, asks the renderer for
    its extent, and removes it.
    """
    t = ax.text(0, 0, text, fontsize=fs, fontweight=weight, style=style,
                linespacing=linespacing, ha="center", va="center")
    fig = ax.figure
    fig.canvas.draw()
    bb = t.get_window_extent(fig.canvas.get_renderer())
    t.remove()
    (x0, y0), (x1, y1) = ax.transData.inverted().transform(
        [(bb.x0, bb.y0), (bb.x1, bb.y1)])
    return abs(x1 - x0), abs(y1 - y0)


def fitbox(ax, x, y, text, fc, ec, fs=8.0, weight="normal", dashed=False,
           lw=1.2, padx=0.36, pady=0.30, min_w=0.0, tc=C.INK):
    """A box sized to its own text. Returns its width and height."""
    w, h = measure(ax, text, fs, weight)
    w, h = max(w + 2 * padx, min_w), h + 2 * pady
    box(ax, x, y, w, h, text, fc, ec, tc=tc, fs=fs, weight=weight,
        dashed=dashed, lw=lw)
    return w, h


def panel_size(ax, rows, padx=0.50, pady=0.40, gap=0.18):
    """What `panel` will measure for these rows, before anything is drawn.

    A lane of boxes only reads as a lane if every box in it is the same width,
    and the width is not known until the widest label in the lane has been
    measured. This is the half of `panel` that answers that, so a caller can
    size a whole row and then pass the answer back as min_w.
    """
    m = [measure(ax, r["text"], r.get("fs", 9.0), r.get("weight", "normal"),
                 r.get("style", "normal")) for r in rows]
    return (max(w for w, _ in m) + 2 * padx,
            sum(h for _, h in m) + gap * (len(m) - 1) + 2 * pady)


def panel(ax, x, y, rows, fc, ec, padx=0.50, pady=0.40, lw=1.4, gap=0.18,
          dashed=False, min_w=0.0, min_h=0.0):
    """A box whose lines carry different styles, sized to the widest of them.

    F2 needs one box to hold two viewpoints: what the model can see, and what
    only the harness knows. Drawing that as one string would make both facts
    look equally available to the model, which is the misreading the figure
    exists to prevent, so each row carries its own size, colour and weight, and
    a row may be underlined to mark it as not the model's.

    min_w and min_h widen or deepen the box past its own content, which is how
    F3 gives a lane one width and one depth; the rows stay centred in whatever
    the box ends up being, so the padding a caller asked for is a floor rather
    than an exact margin.

    rows: dicts of text, and optionally fs, color, weight, style, underline.
    """
    spec = []
    for r in rows:
        fs = r.get("fs", 9.0)
        w, h = measure(ax, r["text"], fs, r.get("weight", "normal"),
                       r.get("style", "normal"))
        spec.append((r, fs, w, h))
    fit_h = sum(h for _, _, _, h in spec) + gap * (len(spec) - 1) + 2 * pady
    bw = max(max(w for _, _, w, _ in spec) + 2 * padx, min_w)
    bh = max(fit_h, min_h)
    p = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                       boxstyle="round,pad=0.012,rounding_size=0.015",
                       fc=fc, ec=ec, lw=lw, zorder=3,
                       linestyle="--" if dashed else "-")
    ax.add_patch(p)

    # Measured from the height the rows themselves ask for, not from the height
    # the box ended up at, so the rows stay centred when min_h opens the box up
    # and the arithmetic is untouched — to the last bit — when it does not.
    top = y + fit_h / 2 - pady
    for r, fs, w, h in spec:
        cy = top - h / 2
        ax.text(x, cy, r["text"], ha="center", va="center", fontsize=fs,
                color=r.get("color", C.INK), fontweight=r.get("weight", "normal"),
                style=r.get("style", "normal"), zorder=4, linespacing=1.35)
        if r.get("underline"):
            ax.plot([x - w / 2, x + w / 2], [cy - h / 2 - 0.07] * 2,
                    color=r.get("color", C.MUTED), lw=0.9, zorder=4,
                    linestyle=(0, (2.5, 2.5)))
        top -= h + gap
    return bw, bh


def collisions(fig, ax, pad_px=0.0):
    """Every collision in a finished figure, in pixels of the written PNG.

    Three kinds are found: two boxes overlapping, two labels overlapping, and a
    label that lies partly inside a box, which is the case that reads as a word
    cutting across a line. With pad_px set, a label that sits inside a box must
    also clear its border by that many pixels, which is the check that catches
    text touching the edge it is nominally inside of.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    # zorder below 2 is a grouping frame, which contains other boxes by design
    boxes = [p.get_window_extent(r) for p in ax.patches
             if isinstance(p, FancyBboxPatch) and p.get_zorder() >= 2]
    texts = [(t.get_text().replace("\n", " ")[:34], t.get_window_extent(r))
             for t in ax.texts if t.get_text().strip()]

    def hit(a, b, slack=0.5):
        return (a.x0 < b.x1 - slack and b.x0 < a.x1 - slack
                and a.y0 < b.y1 - slack and b.y0 < a.y1 - slack)

    out = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if hit(a, b):
                out.append("box overlaps box")
    for i, (na, a) in enumerate(texts):
        for nb, b in texts[i + 1:]:
            if hit(a, b):
                out.append("label %r overlaps label %r" % (na, nb))
    for na, a in texts:
        for b in boxes:
            inside = (a.x0 >= b.x0 - 1 and a.x1 <= b.x1 + 1
                      and a.y0 >= b.y0 - 1 and a.y1 <= b.y1 + 1)
            if hit(a, b) and not inside:
                out.append("label %r crosses a box edge" % na)
            if inside and pad_px:
                m = min(a.x0 - b.x0, b.x1 - a.x1, a.y0 - b.y0, b.y1 - a.y1)
                if m < pad_px:
                    out.append("label %r sits %.1fpx from its border, under %g"
                               % (na, m, pad_px))
    return out


def layout_report(fig, ax, name):
    """Print what `collisions` found. Development aid, not a gate."""
    out = collisions(fig, ax)
    print(name + ": " + ("clean" if not out else "%d collision(s)" % len(out)))
    for line in sorted(set(out)):
        print("    " + line)
    return out


def elbow(ax, pts, color=None, lw=1.3, dashed=False):
    """A right-angled path through pts, with the arrowhead on the last leg.

    A curved arrow that has to travel round the outside of a diagram either
    cuts through a label or forces the label off the figure. An elbow keeps to
    the margin, which leaves the space beside it usable.
    """
    col = color or C.MUTED
    ls = "--" if dashed else "-"
    for (x1, y1), (x2, y2) in zip(pts[:-2], pts[1:-1]):
        ax.plot([x1, x2], [y1, y2], color=col, lw=lw, ls=ls, zorder=2,
                solid_capstyle="round")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color=col, lw=lw, zorder=2,
                                 shrinkA=0, shrinkB=3, linestyle=ls))


# ---------------------------------------------------------------------------
# F1 - the harness loop, extended
# ---------------------------------------------------------------------------

def f1_harness_loop():
    """The loop, the release rule, and what the model knows when it claims.

    Drawn at page width rather than at twice it. The manuscript sets every
    figure to \\textwidth, so a figure drawn 13 inches wide has its type scaled
    to 42 per cent and lands under 5pt on the page. Here 14.6 data units span
    6.0 inches, the saved file is 6.5 inches with the pad, and a 9.5pt label
    prints at about 8pt, which is the size of the caption beside it.

    Every condition of the loop is written on the figure, because the ones that
    were left implicit are the ones a reader needs: that the model is told
    hidden tests exist, that it is not told how many, that passing everything
    visible is what releases the next stage, and that the claim is the one move
    whose result it never sees.
    """
    # The axes fills the figure, so one data unit is exactly figsize/xlim and
    # the size a label prints at is decided here rather than by a subplot
    # margin. 14.6 units over 6.03in, saved 6.5in wide with the pad, scaled to
    # a 5.6in text block: a 10pt label lands at 8.6pt, just under the caption.
    fig = plt.figure(figsize=(6.03, 4.65))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 14.6); ax.set_ylim(-0.65, 10.60); ax.axis("off")
    ax.text(7.30, 10.22, "The loop, the release rule, and the claim channel",
            fontsize=11.5, fontweight="bold", color=C.INK, ha="center",
            va="center")

    # Every box carries as few words as the mechanism allows, because the page
    # width is fixed: what a box does not spend on text becomes the gap beside
    # it, and the gaps are what make the connections legible. Conditions are
    # written beside the thing they constrain, not listed at the foot.
    PB = dict(padx=0.52, pady=0.42)

    # --- one turn ----------------------------------------------------------
    fitbox(ax, 1.90, 8.35, "the model", NODE, NEDGE, fs=10.0, weight="bold", **PB)
    fitbox(ax, 6.75, 8.35, "the checker", NODE, NEDGE, fs=10.0, weight="bold",
           **PB)
    arrow(ax, 3.60, 8.72, 4.90, 8.72, "the rewritten module", ly=0.80,
          curve=-0.26, fs=8.8)
    arrow(ax, 4.90, 7.98, 3.60, 7.98,
          "how many visible tests passed,\nand which of them failed",
          lx=1.20, ly=-1.08, curve=-0.26, fs=8.8)

    # --- the suite, and which part of it the checker may run ---------------
    stack_w = 4.05
    fitbox(ax, 12.18, 9.15, "tests it can see", NODE, NEDGE, fs=9.0,
           pady=0.28, min_w=stack_w)
    fitbox(ax, 12.18, 8.05, "next hidden stage", SEALED, SEDGE, fs=9.0,
           pady=0.28, dashed=True, min_w=stack_w)
    fitbox(ax, 12.18, 6.95, "stages after that", SEALED, SEDGE, fs=9.0,
           pady=0.28, dashed=True, min_w=stack_w)
    arrow(ax, 8.60, 8.60, 10.00, 9.00, fs=8.8)
    ax.text(11.30, 5.50,
            "the rules say unseen tests exist,\n"
            "and not how many. A stage becomes\n"
            "visible only when all visible pass",
            fontsize=8.4, color=C.INK2, ha="center", va="center",
            style="italic", linespacing=1.6)

    # --- the claim channel -------------------------------------------------
    arrow(ax, 1.30, 7.67, 1.30, 4.20, "at any turn", lx=1.40, ly=-0.35,
          color=C.ADVISORY, fs=8.8)
    wl, _ = fitbox(ax, 3.30, 3.25, "the model replies DONE\ninstead of code",
                   "#fdf3e3", C.ADVISORY, fs=9.0, **PB)
    wr, _ = fitbox(ax, 9.70, 3.25, "every test is run,\nvisible and hidden",
                   "#fdf3e3", C.ADVISORY, fs=9.0, **PB)
    arrow(ax, 3.30 + wl / 2 + 0.12, 3.25, 9.70 - wr / 2 - 0.12, 3.25,
          color=C.ADVISORY, fs=8.8)

    # The claim is a prediction about the hidden tests, so it has two outcomes
    # and the model is shown neither. Which of the two happened is the quantity
    # every experiment in the paper counts.
    arrow(ax, 9.10, 2.36, 7.60, 1.78, fs=8.8)
    arrow(ax, 10.30, 2.36, 11.90, 1.78, fs=8.8)
    fitbox(ax, 6.90, 0.98, "all pass:\nthe claim was right", GOOD, GEDGE,
           fs=9.0, padx=0.40, pady=0.30)
    fitbox(ax, 12.10, 0.98, "any fails:\nthe claim was wrong", BAD, BEDGE,
           fs=9.0, padx=0.40, pady=0.30)
    ax.text(9.50, -0.32, "the model is never told which of the two happened",
            fontsize=8.4, color=C.ADVISORY, ha="center", va="center",
            style="italic")
    return save(fig, "F1_harness_loop.png")


# ---------------------------------------------------------------------------
# F2 - the decision point
# ---------------------------------------------------------------------------

def f2_decision_point(traffic=False):
    """The decision point, formalised: the state, the options, the outcomes.

    With traffic=True the claim branch also carries how many claims the
    programme actually made from this state, read from `tables/T2.csv` rather
    than written here. That variant is a trial for the owner and is not what
    `render_all` writes.

    Section 4 says the state is "defined entirely by what the model has and has
    not been shown", so the figure draws that partition as its structure rather
    than describing it. Six facts hold at the state. Three are on the model's
    screen and three are the harness's, and which side a fact falls on is the
    whole content of the section.

    Everything is a node. An earlier version wrote the state into one box of
    prose, which made the most important object in the paper the least legible
    thing in the figure.
    """
    # The lower half is taller than the state panel needs, and deliberately: a
    # connector drawn across a 0.27-unit gap is 8pt long, of which 13pt is
    # arrowhead, so it reads as a stray triangle rather than as a link between
    # two things. Each connector below gets a clear run of CONNECT, and the
    # figure is sized to hold it. The data units per inch are unchanged from the
    # earlier layout (13.20 over 5.45in against 12.25 over 5.06in), so every
    # label still prints at the size it did.
    fig = plt.figure(figsize=(6.03, 5.45))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 14.6); ax.set_ylim(-2.10, 11.10); ax.axis("off")
    ax.text(7.30, 10.75, "The decision point: what the model can see, and what "
                         "it cannot", fontsize=11.0, fontweight="bold",
            color=C.INK, ha="center", va="center")

    # One visual job per style. A fact is an unfilled box, an action is a filled
    # one with a heavier edge, an outcome is a coloured terminal. Blue is the
    # model's side of the loop and amber is the claim channel, as in F1.
    FACT = dict(fs=8.0, padx=0.40, pady=0.30, lw=1.0)
    ACT_A = dict(fs=9.0, padx=0.46, pady=0.30, lw=1.6)
    ACT_B = dict(fs=9.0, padx=0.46, pady=0.30, lw=1.6)
    ACT_BLUE, ACT_BLUE_EDGE = "#e7f0f9", C.BINDING

    # --- the state, as six facts in two registers ---------------------------
    # The registers are the content of the section: the model holds the rules'
    # statement that unseen tests MAY exist, and the harness holds whether one
    # actually remains. Erasing that difference would erase the paper's claim,
    # so the two sit in the same column, one above the other.
    # The panel stops short of the right edge so the return path has a lane of
    # its own. Given to the panel instead, that width buys nothing: the fact
    # boxes are already wider than the text in them, and the arrow that closes
    # the loop is left with a run too short to read as an arrow.
    FL, FR, FTOP, FBOT = 0.25, 13.55, 10.35, 5.00
    ax.add_patch(FancyBboxPatch((FL, FBOT), FR - FL, FTOP - FBOT,
                                boxstyle="round,pad=0.012,rounding_size=0.05",
                                fc=C.SURFACE, ec=C.BASELINE, lw=1.0, zorder=1))
    ax.text(0.60, 10.00, "the decision point holds six facts", fontsize=8.6,
            fontweight="bold", color=C.INK, ha="left", va="center")

    # Three columns of one width, evenly spaced inside the panel: the widest of
    # the six labels measures 3.68, so 3.95 holds every one of them.
    CW = (3.95, 3.95, 3.95)
    CGAP = 0.42
    CM = ((FR - FL) - (sum(CW) + 2 * CGAP)) / 2          # margin inside the panel
    CX = (FL + CM + CW[0] / 2,
          FL + CM + CW[0] + CGAP + CW[1] / 2,
          FL + CM + CW[0] + CGAP + CW[1] + CGAP + CW[2] / 2)
    ax.text(0.60, 9.55, "the model can see", fontsize=7.8, fontweight="bold",
            color=C.INK2, ha="left", va="center")
    fitbox(ax, CX[0], 8.50, "every test it\ncan see passes", C.SURFACE, NEDGE,
           min_w=CW[0], **FACT)
    fitbox(ax, CX[1], 8.50, "new tests appeared\nafter each pass", C.SURFACE,
           NEDGE, min_w=CW[1], **FACT)
    fitbox(ax, CX[2], 8.50, "the rules say unseen\ntests may exist", C.SURFACE,
           NEDGE, min_w=CW[2], **FACT)

    ax.text(0.60, 7.45, "only the harness can see", fontsize=7.8,
            fontweight="bold", color=C.MUTED, ha="left", va="center")
    fitbox(ax, CX[0], 6.45, "whether the hidden\ntests pass", SEALED, SEDGE,
           dashed=True, min_w=CW[0], **FACT)
    fitbox(ax, CX[1], 6.45, "how many stages\nthere are in total", SEALED,
           SEDGE, dashed=True, min_w=CW[1], **FACT)
    fitbox(ax, CX[2], 6.45, "at least one stage\nis still hidden", SEALED,
           SEDGE, dashed=True, min_w=CW[2], **FACT)
    ax.text((FL + FR) / 2, 5.45, "and the hidden tests enforce a convention the "
                                 "code had to guess", fontsize=7.8,
            color=C.MUTED, ha="center", va="center", style="italic")

    # --- the option set -----------------------------------------------------
    # Both moves drop vertically out of the state's own edge, in the same
    # geometry, because neither is the default and the asymmetry between them is
    # cost, which the annotations carry.
    # The cheap move drops out of the column that states the fact it acts on,
    # which also keeps its chain clear of the right margin the loop-back uses.
    # The claim, which has no one fact to sit under, takes the space between the
    # first two columns, and its outcome row opens out around that axis.
    AX_, BX_ = (CX[0] + CX[1]) / 2, CX[2]
    # Every row is placed from the measured height of the row above it, so the
    # gap a connector spans is the same number wherever it appears and cannot
    # drift when a label is reworded into another line.
    CONNECT = 0.90
    ACT_H = max(measure(ax, "reply DONE", ACT_A["fs"])[1],
                measure(ax, "submit again", ACT_B["fs"])[1]) + 2 * ACT_A["pady"]
    RES = dict(fs=8.4, padx=0.44, pady=0.30, lw=1.6)
    A_RES = "the whole suite is run against\nthe module as it stands"
    B_RES = "the next stage\nbecomes visible"
    RES_H = max(measure(ax, A_RES, RES["fs"])[1],
                measure(ax, B_RES, RES["fs"])[1]) + 2 * RES["pady"]

    AY_ = FBOT - CONNECT - ACT_H / 2
    RY_ = AY_ - ACT_H / 2 - CONNECT - RES_H / 2

    fitbox(ax, AX_, AY_, "reply DONE", "#fdf3e3", C.ADVISORY, **ACT_A)
    fitbox(ax, BX_, AY_, "submit again", ACT_BLUE, ACT_BLUE_EDGE, **ACT_B)
    arrow(ax, AX_, FBOT, AX_, AY_ + ACT_H / 2, color=C.ADVISORY, fs=8.0)
    arrow(ax, BX_, FBOT, BX_, AY_ + ACT_H / 2, color=C.BINDING, fs=8.0)
    ax.text((AX_ + BX_) / 2, AY_, "a claim is never\nthe cheaper move", fontsize=8.0,
            color=C.INK2, ha="center", va="center", style="italic",
            linespacing=1.55)

    # --- what each option resolves to --------------------------------------
    _, ah = fitbox(ax, AX_, RY_, A_RES, "#fdf3e3", C.ADVISORY, **RES)
    bw, bh = fitbox(ax, BX_, RY_, B_RES, ACT_BLUE, ACT_BLUE_EDGE, **RES)
    arrow(ax, AX_, AY_ - ACT_H / 2, AX_, RY_ + ah / 2, color=C.ADVISORY, fs=8.0)
    arrow(ax, BX_, AY_ - ACT_H / 2, BX_, RY_ + bh / 2, color=C.BINDING, fs=8.0)

    # The terminals hang the same clear run below the suite box, and are measured
    # the way panel() will measure them, so the fork can be placed before the
    # thing it points at exists.
    PAN = dict(padx=0.40, pady=0.24, lw=1.2, gap=0.10)
    GOOD_ROWS = [
        {"text": "all pass", "fs": 7.8, "weight": "bold", "color": C.S6_GREEN},
        {"text": "the claim was right", "fs": 8.2},
        {"text": "a few turns saved", "fs": 7.4, "color": C.INK2,
         "style": "italic"},
    ]
    BAD_ROWS = [
        {"text": "any fails", "fs": 7.8, "weight": "bold", "color": C.CRITICAL},
        {"text": "the claim was wrong", "fs": 8.2},
        {"text": "the task ends unsolved", "fs": 7.4, "color": C.INK2,
         "style": "italic"},
    ]

    def term_size(rows):
        m = [measure(ax, r["text"], r["fs"], r.get("weight", "normal"),
                     r.get("style", "normal")) for r in rows]
        return (max(w for w, _ in m) + 2 * PAN["padx"],
                sum(h for _, h in m) + PAN["gap"] * (len(m) - 1)
                + 2 * PAN["pady"])

    TERM_W = max(term_size(GOOD_ROWS)[0], term_size(BAD_ROWS)[0])
    TERM_H = max(term_size(GOOD_ROWS)[1], term_size(BAD_ROWS)[1])
    OY = RY_ - RES_H / 2 - CONNECT - TERM_H / 2
    # The two outcomes open out until the left one is flush with the panel above
    # it. Held any closer in, the row huddles under the middle of the figure and
    # leaves the corner beneath the loop-back branch empty.
    TSPREAD = AX_ - (FL + TERM_W / 2)
    gw, gh = panel(ax, AX_ - TSPREAD, OY, GOOD_ROWS, GOOD, GEDGE, **PAN)
    panel(ax, AX_ + TSPREAD, OY, BAD_ROWS, BAD, BEDGE, **PAN)
    # The fork reaches the terminals it names, from the measured edges of both.
    arrow(ax, AX_ - 0.90, RY_ - ah / 2, AX_ - TSPREAD + 0.70, OY + gh / 2,
          color=C.ADVISORY, fs=8.0)
    arrow(ax, AX_ + 0.90, RY_ - ah / 2, AX_ + TSPREAD - 0.70, OY + gh / 2,
          color=C.ADVISORY, fs=8.0)
    ax.text(AX_, OY - gh / 2 - 0.45, "the model is told neither, and the "
                                     "episode is over", fontsize=8.2,
            color=C.MUTED, ha="center", va="center", style="italic")

    # Every italic note sits directly beneath what it qualifies, this one under
    # the move it prices. Held down at the outcome row instead, where it would
    # fill more of the corner, it reads as a caption to nothing: the branch it
    # belongs to ended two rows above it.
    _, nh = measure(ax, "costs nothing, and\nnever ends the episode", 8.0,
                    linespacing=1.55)
    ax.text(BX_, RY_ - RES_H / 2 - 0.45 - nh / 2,
            "costs nothing, and\nnever ends the episode",
            fontsize=8.0, color=C.BINDING, ha="center", va="center",
            style="italic", linespacing=1.55)

    # The cheap move returns to a state of the same kind. It re-enters at the
    # visible register, because it shows the model one more stage and never the
    # harness's verdict. The last leg stops on the panel's edge rather than
    # reaching over it: the loop returns to the state, and the fact it lands
    # beside is which of the six the return changes.
    LANE = 14.45
    elbow(ax, [(BX_ + bw / 2, RY_), (LANE, RY_), (LANE, 8.50), (FR, 8.50)],
          color=C.BINDING)

    if traffic:
        # Every quantity read from the table, none written here.
        tot = [r for r in table("T2") if r["experiment"].startswith("all")][0]
        claims = int(tot["said DONE at the decision point"])
        wrong = int(tot["wrong at the decision point"])
        ax.text(AX_ - 1.15, FBOT - CONNECT / 2, "%d claims" % claims, fontsize=8.0,
                color=C.ADVISORY, ha="right", va="center", style="italic")
        ax.text(AX_ - TSPREAD - gw / 2 - 0.30, OY + gh / 2 + 0.30,
                "%d" % (claims - wrong),
                fontsize=8.6, color=C.S6_GREEN, fontweight="bold", ha="center",
                va="center")
        ax.text(AX_ + TSPREAD + gw / 2 + 0.30, OY + gh / 2 + 0.30, "%d" % wrong,
                fontsize=8.6, color=C.CRITICAL, fontweight="bold", ha="center",
                va="center")
    return save(fig, "F2_decision_point.png")


# ---------------------------------------------------------------------------
# Paired cells, read through the table builder so figures and tables agree
# ---------------------------------------------------------------------------

PAIRS = {
    "B":     ("claude-opus-5_ctrl", "claude-opus-5_warn"),
    "C1":    ("claude-opus-5_ctrl", "claude-opus-5_sigma"),
    "C2":    ("claude-opus-5_ctrlprime", "claude-opus-5_count"),
    "churn": ("claude-opus-5_ctrl", "claude-opus-5_ctrlprime"),
}


def cells(key_):
    left, right = PAIRS[key_]
    return MT.paired(left, right)


def mcnemar_p(key_, predicted_lower):
    left, right = PAIRS[key_]
    p = cells(key_)
    b = p["right_only"] if predicted_lower == right else p["left_only"]
    c = p["left_only"] if predicted_lower == right else p["right_only"]
    return MT.exact_mcnemar_one_sided(b, c)["p_value"]


# ---------------------------------------------------------------------------
# F3 - the argument tree
# ---------------------------------------------------------------------------
#
# Three lanes, read downwards. The spine is what was run and when; the pills
# under each experiment are what was registered before it ran and how each
# prediction came out; the ledger along the bottom is what the programme is
# entitled to say afterwards. A reader who has read none of the paper has to
# be able to reconstruct the whole design from this one image, which is why
# every arm code is glossed where it appears and the subtitle states the game.
#
# GEOMETRY. Every distance below is in data units, and the canvas is computed
# from the content rather than the content fitted to a canvas: the lane widths
# come out of `measure`, the column pitch comes out of the widest thing that
# has to sit in a column, and the figure is finally sized so that one data
# unit is exactly F3_K to the inch. That makes a constraint stated in pixels a
# constant here — at savefig.dpi 200 one unit is 0.1in, which is 20px — and it
# is why nothing in this figure is nudged by hand.

F3_K = 10.0                       # data units per inch
F3_PX = 20.0                      # px per data unit, at savefig.dpi 200
F3_SCALE = 14.0                   # arrow mutation_scale
F3_HEAD = 0.4 * F3_SCALE / 72.0 * F3_K       # arrowhead length, data units
F3_SHRINK = 3.6                   # points: 10px of clear air at each end
F3_CLEAR = 2 * F3_SHRINK / 72.0 * F3_K       # both ends, data units
# An arrow shorter than this renders as a head with no shaft, which reads as a
# stray triangle rather than as a link. Boxes move apart; arrows do not shrink.
F3_MIN_ARROW = 5 * F3_HEAD + F3_CLEAR
F3_TEXT_PAD = 10.0                # px of clear air inside every box

# The registered design parameter Experiment 3 was powered against. It is not
# a measurement and no table prints it as a column, so it is written here and
# guarded against the caption that also prints it: if the registration is ever
# restated, the two cannot drift apart in silence.
F3_MDE = "0.155"

NUMWORD = ("zero", "one", "two", "three", "four", "five", "six", "seven",
           "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
           "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")

# The verdict vocabulary of T8, and nothing else. A verdict outside this map
# raises rather than drawing an uncoloured pill.
F3_VERDICT = {
    "CONFIRMED":     ("✓", GOOD, GEDGE, C.S6_GREEN),
    "DISCONFIRMED":  ("✗", BAD, BEDGE, C.CRITICAL),
    "NOT CONFIRMED": ("◦", SEALED, SEDGE, C.MUTED),
}

# One line per registered prediction, keyed by its T8 label. These are captions
# for the verdicts beside them and carry no quantities; the verdict itself, and
# the set of labels, are read from T8 and checked against these keys, so a
# prediction added to the registration cannot go unnoticed here.
F3_SHORT = {
    "P1": "claims work it cannot verify",
    "P2": "the gate helps the middle model most",
    "P3": "the gate helps less where staged",
    "P4": "gate benefit tracks wrong claims",
    "B1": "the stage count reduces claiming",
    "B2": "wrong claims survive the count",
    "B3": "accuracy tracks a green board's worth",
    "B4": "the warning changes only the ending",
    "C1": "a stated reward raises claiming",
    "C2": "extra claims come from safe withholds",
    "C5": "the working phase did not drift",
    "C4": "doing the arithmetic cuts claiming",
    "C6": "two identical runs barely disagree",
    "C8": "the counter changes only the ending",
}

F3_TITLE = ("How the programme unravelled: %s experiments, %s predictions, "
            "%s surviving explanation")
F3_SUB = ("each task: repair a broken function whose tests are partly hidden "
          "and released in stages; the model may end the episode by replying "
          "DONE, which is scored against the tests it has not seen")

# The question each experiment inherited from the one before it. The first is
# inherited from the previous paper, which is the root of the tree.
F3_EDGES = [
    "what is a wrong claim,\nand where does it happen?",
    "does the model claim because\nit does not know how much\nis hidden?",
    "does the model claim because\nstopping early looks cheap?",
    "does the model fail to combine\nwhat it already knows at\nthe moment it decides?",
]


def _f3_scratch():
    """An axes with F3's data-units-per-inch, for measuring before sizing.

    `measure` needs a transform, and the transform needs a figure size, and the
    figure size is what the measurements are for. Fixing units per inch instead
    of figure size breaks the circle: an axes that fills its figure and spans
    figw * F3_K in x has the same transform whatever figw is, so a string
    measured here is the size it will be in the figure this measurement sizes.
    """
    fig = plt.figure(figsize=(20.0, 12.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 20.0 * F3_K)
    ax.set_ylim(0, 12.0 * F3_K)
    ax.axis("off")
    return fig, ax


def _f3_arrow(ax, x1, y1, x2, y2, color, reg, lw=1.4):
    reg.append(((x1, y1), (x2, y2)))
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=F3_SCALE, color=color, lw=lw,
                                 zorder=2, shrinkA=F3_SHRINK, shrinkB=F3_SHRINK))


def _f3_content(ax):
    """Every string F3 draws, and every number in them, read from the data.

    Split out from the drawing because the layout has to be computed from the
    measured size of these strings before anything can be placed.
    """
    t1, t3, t4b, t6, t8 = (table("T1"), table("T3"), table("T4B"), table("T6"),
                           table("T8"))
    b, c1, c2 = cells("B"), cells("C1"), cells("C2")
    day = lambda rid: MT.RUN_BY_ID[rid]["started_at"][:10]

    def models(exp):
        return len({r["model"] for r in t1
                    if r["experiment"] == exp and r["model"]})

    # Experiment 1 played the same corpus under both arms at every rung, and
    # the node says so in one number; if that ever stops being true the figure
    # must say something else rather than pick a row.
    played = {r["tasks played"] for r in t3}
    if len(played) != 1:
        raise AssertionError("T3 rungs no longer share a task count: %r" % played)
    n_tasks = played.pop()

    rungs = {r["capability rung"]: r for r in t3}
    ladder = [rungs["weakest"], rungs["middle"], rungs["strongest"]]
    shares = [r["share of tasks where it said DONE"] for r in ladder]
    if [float(s) for s in shares] != sorted(float(s) for s in shares):
        raise AssertionError("claiming no longer rises with capability: %r"
                             % (shares,))

    pooled = {r["kind of task"]: r for r in t4b
              if r["what the model was told it could do"]
              == "both sets of rules pooled"}
    safe, risky = pooled["hides nothing"], pooled["hides a convention"]

    prime, count = t6[0], t6[1]
    fell_from = prime["of those, how many were wrong"]
    fell_to = count["of those, how many were wrong"]

    moved_b = ("%d tasks moved each way of %d" % (b["left_only"], b["n_paired"])
               if b["left_only"] == b["right_only"] else
               "%d tasks moved against %d, of %d"
               % (b["left_only"], b["right_only"], b["n_paired"]))

    nodes = [
        ["Experiment 1 · " + day("claude-opus-5_adv"),
         "%d models, %s tasks each" % (models("experiment 1"), n_tasks),
         "BIND (no way to say DONE)   vs",
         "ADV (may say DONE; told only\nthat unseen tests exist)"],
        ["Experiment 2 · " + day("claude-opus-5_ctrl"),
         "%d model, %d paired tasks" % (models("experiment 2"), b["n_paired"]),
         "CTRL (the ADV rules, unchanged,\non the new corpus)   vs",
         "WARN (CTRL + one rules sentence:\nthe exact number of hidden stages)"],
        ["Experiment 3 · " + day("claude-opus-5_sigma"),
         "%d model, %d paired tasks" % (models("experiment 3"), c1["n_paired"]),
         "SIGMA (CTRL + one rules sentence:\na correct early stop scores higher)   vs",
         "the CTRL record on the same tasks"],
        ["Experiment 4 · " + day("claude-opus-5_count"),
         "%d model, %d paired tasks" % (models("experiment 4"), c2["n_paired"]),
         "CTRL′ (CTRL run again, unchanged,\nsame day)   vs",
         "COUNT (CTRL′ + one feedback line at\nevery release: the count still hidden)"],
    ]

    root = ["the previous paper",
            "wrong claims exist, and the",
            "value of a gate tracks them"]

    # The pills, in registration order, grouped by the experiment that ran
    # them. Labels and verdicts are T8's; only the one-line gloss is written
    # here, and every label must have one.
    if set(F3_SHORT) != {r["label"] for r in t8}:
        raise AssertionError("F3_SHORT and T8 disagree about the labels: %r"
                             % (set(F3_SHORT) ^ {r["label"] for r in t8},))
    pills = []
    for i in range(len(nodes)):
        rows = [r for r in t8 if r["experiment"] == "experiment %d" % (i + 1)]
        for r in rows:
            if r["verdict"] not in F3_VERDICT:
                raise AssertionError("T8 verdict %r is not in the key"
                                     % r["verdict"])
        pills.append([(r["label"], F3_SHORT[r["label"]], r["verdict"])
                      for r in rows])

    # The ledger. Each entry names the explanation, what the programme did to
    # it, and the evidence that did it, and is tied to the experiment that
    # produced it by index into `nodes`.
    ledger = [
        (0, "one weak model's quirk", "ELIMINATED",
         ["claiming rises with capability", " → ".join(shares)], False),
        (1, "missing information", "ELIMINATED", [moved_b], False),
        (1, "blind to the risk", "ELIMINATED",
         ["claims at %s of %s safe visits,"
          % (safe["of those, it said DONE"], safe["visits to the decision point"]),
          "%s of %s risky ones"
          % (risky["of those, it said DONE"],
             risky["visits to the decision point"])], False),
        (2, "the incentive", "BOUNDED",
         ["no large increase; the design",
          "was powered only for " + F3_MDE], False),
        (3, "integration at the decision point", "SURVIVES",
         ["moved %d tasks against %d;" % (c2["left_only"], c2["right_only"]),
          "wrong claims fell %s to %s" % (fell_from, fell_to)], True),
    ]

    n_exp = len({r["experiment"] for r in t8})
    n_survive = sum(1 for e in ledger if e[4])
    title = F3_TITLE % (NUMWORD[n_exp], NUMWORD[len(t8)], NUMWORD[n_survive])
    return nodes, root, pills, ledger, title


def f3_timeline():
    """The argument tree: what was run, what was registered, what survives.

    Named f3_timeline, and writing F3_timeline.png, because the paper numbers
    its figures by file and this is the sixth. What it draws is no longer a
    line: the programme did not accumulate four results, it eliminated three
    explanations and was left holding one, and an elimination has a shape that
    a dated line cannot show.
    """
    # The one number here that no table prints as a column, checked against the
    # caption that does print it.
    with open(os.path.join(TABLES, "T5.md"), encoding="utf-8") as f:
        if F3_MDE not in f.read():
            raise AssertionError("T5's caption no longer states the registered "
                                 "shift %s that F3 prints" % F3_MDE)

    fig, ax = _f3_scratch()
    nodes, root, pills, ledger, title = _f3_content(ax)

    # --- styles -------------------------------------------------------------
    NODE_PAD = dict(padx=3.4, pady=2.6, gap=1.5)
    PILL_PADX, PILL_PADY, PILL_GAP = 2.4, 1.9, 2.2
    LEDG_PAD = dict(padx=2.8, pady=2.4, gap=1.3)
    FS_TITLE, FS_SUB, FS_EDGE = 17.0, 11.5, 8.8
    FS_PILL, FS_GLYPH = 8.4, 9.6

    def node_rows(lines, muted=False):
        head = dict(text=lines[0], fs=11.0, weight="bold",
                    color=C.MUTED if muted else C.INK)
        rest = [dict(text=t, fs=9.5 if i == 0 else 9.0,
                     color=C.INK2 if i == 0 else C.INK)
                for i, t in enumerate(lines[1:])]
        return [head] + rest

    def ledger_rows(name, verdict, evidence, survives):
        col = C.ADVISORY if survives else C.CRITICAL
        mark = verdict if survives else "✗  " + verdict
        rows = [dict(text=name, fs=9.2, weight="bold"),
                dict(text=mark, fs=9.2, weight="bold", color=col)]
        rows += [dict(text=t, fs=8.2, color=C.INK2) for t in evidence]
        if survives:
            rows.append(dict(text="placebo control unrun", fs=8.4, color=col,
                             weight="bold", style="italic"))
        return rows

    # --- widths, measured, then the pitch that holds the widest of them -----
    node_specs = [node_rows(n) for n in nodes]
    root_rows = node_rows(root, muted=True)
    node_w = max(panel_size(ax, s, NODE_PAD["padx"], NODE_PAD["pady"],
                            NODE_PAD["gap"])[0] for s in node_specs)
    node_h = max(panel_size(ax, s, NODE_PAD["padx"], NODE_PAD["pady"],
                            NODE_PAD["gap"])[1] for s in node_specs)
    root_w, root_h = panel_size(ax, root_rows, NODE_PAD["padx"],
                                NODE_PAD["pady"], NODE_PAD["gap"])

    lab_w = max(measure(ax, p[0], FS_PILL, "bold")[0] for st in pills for p in st)
    txt_w = max(measure(ax, p[1], FS_PILL)[0] for st in pills for p in st)
    gly_w = max(measure(ax, F3_VERDICT[v][0], FS_GLYPH)[0]
                for _, _, v in (p for st in pills for p in st))
    pill_h = measure(ax, "Xy", FS_PILL)[1] + 2 * PILL_PADY
    pill_w = 2 * PILL_PADX + lab_w + 2.0 + txt_w + 2.0 + gly_w
    stack_h = len(max(pills, key=len)) * pill_h + (len(max(pills, key=len)) - 1) * PILL_GAP

    ledger_specs = [ledger_rows(*e[1:]) for e in ledger]
    ledger_sz = [panel_size(ax, s, LEDG_PAD["padx"], LEDG_PAD["pady"],
                            LEDG_PAD["gap"]) for s in ledger_specs]
    ledger_w, ledger_h = max(w for w, _ in ledger_sz), max(h for _, h in ledger_sz)

    edge_w = max(measure(ax, e, FS_EDGE, style="italic")[0] for e in F3_EDGES)
    edge_h = max(measure(ax, e, FS_EDGE, style="italic")[1] for e in F3_EDGES)

    # A column is as wide as the widest thing that has to sit in it, and the
    # gap between two columns is the largest of three demands: half a box
    # width, the edge label that has to fit between them, and the room the
    # five-box ledger lane needs to keep its own half-box gaps under a
    # four-column spine. Nothing is resolved by making anything smaller.
    colw = max(node_w, pill_w)
    colgap = max(0.5 * colw, edge_w + 4.0, (7 * ledger_w - 4 * colw) / 3.0)
    spine_w = 4 * colw + 3 * colgap
    rootgap = max(0.5 * min(root_w, colw), edge_w + 4.0)

    # --- the horizontal positions, which the ledger lane's depth needs ------
    MARGIN = 3.0
    x_root = MARGIN + root_w / 2
    x_col = [MARGIN + root_w + rootgap + colw / 2 + i * (colw + colgap)
             for i in range(4)]
    # Five ledger boxes evenly across the four-column spine, each with a clear
    # half of its own width beside it. They cannot sit under their own
    # experiment, because two of them came out of Experiment 2.
    lgap = (spine_w - 5 * ledger_w) / 4.0
    x_led = [x_col[0] - colw / 2 + ledger_w / 2 + i * (ledger_w + lgap)
             for i in range(5)]
    tie = {}
    for i, e in enumerate(ledger):
        tie.setdefault(e[0], []).append(i)
    # Two entries sharing a parent reach it from either side of its column
    # rather than converging on one point, which would pile two heads together.
    ties = []
    for parent, idxs in tie.items():
        span = 0.0 if len(idxs) == 1 else 4.0
        for k, i in enumerate(idxs):
            off = -span + k * (2 * span / max(len(idxs) - 1, 1))
            ties.append((x_led[i], x_col[parent] + off))

    # --- the vertical stack, top down ---------------------------------------
    GAP_TITLE, GAP_SUB = 2.4, 7.0
    # Lane to lane, never less than one pill height, and never less than the
    # run an arrow needs to show a shaft.
    GAP_NODE_PILL = max(pill_h, F3_MIN_ARROW + 2.0)
    # The ledger arrows are the only diagonals here. The lane is as deep as the
    # longest sideways reach in it, so even the arrow that travels furthest
    # stays nearer vertical than horizontal and points at one column only.
    GAP_PILL_LEDGER = max(pill_h, F3_MIN_ARROW,
                          0.9 * max(abs(a - b) for a, b in ties))
    GAP_LEDGER_KEY = 6.5

    h_title = measure(ax, title, FS_TITLE, "bold")[1]
    h_sub = measure(ax, F3_SUB, FS_SUB, style="italic")[1]
    key_h = pill_h

    H = (MARGIN + h_title + GAP_TITLE + h_sub + GAP_SUB + node_h
         + GAP_NODE_PILL + stack_h + GAP_PILL_LEDGER + ledger_h
         + GAP_LEDGER_KEY + key_h + MARGIN)
    W = MARGIN + root_w + rootgap + spine_w + MARGIN
    plt.close(fig)

    # --- the figure itself, at exactly F3_K units to the inch ---------------
    fig = plt.figure(figsize=(W / F3_K, H / F3_K))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    arrows = []

    y = H - MARGIN - h_title / 2
    ax.text(W / 2, y, title, fontsize=FS_TITLE, fontweight="bold", color=C.INK,
            ha="center", va="center")
    y -= h_title / 2 + GAP_TITLE + h_sub / 2
    ax.text(W / 2, y, F3_SUB, fontsize=FS_SUB, color=C.INK2, ha="center",
            va="center", style="italic")

    y_node = y - h_sub / 2 - GAP_SUB - node_h / 2
    y_stack = y_node - node_h / 2 - GAP_NODE_PILL          # top of the pills
    y_ledger = y_stack - stack_h - GAP_PILL_LEDGER - ledger_h / 2

    # --- lane 1, the spine --------------------------------------------------
    panel(ax, x_root, y_node, root_rows, SEALED, SEDGE, dashed=True,
          min_w=root_w, min_h=root_h, lw=1.2, **NODE_PAD)

    # The gutter under the root node is the one part of the canvas the tree
    # does not reach, and a reader coming to this figure first needs to be
    # told what kind of thing each lane holds. It costs no width to say so
    # there, and every other placement would take room from a lane.
    for cy, head, gloss in [
            (y_stack - stack_h / 2, "the registered predictions",
             "written down, with the result that\nwould refute each, before the run"),
            (y_ledger, "the explanation ledger",
             "what each experiment removed,\nand the one thing left standing")]:
        gh = measure(ax, gloss, 8.6, style="italic")[1]
        ax.text(x_root, cy + gh / 2 + 1.2, head, fontsize=9.8, color=C.INK2,
                fontweight="bold", ha="center", va="center")
        ax.text(x_root, cy - 1.2, gloss, fontsize=8.6, color=C.MUTED,
                ha="center", va="center", style="italic", linespacing=1.35)
    for i, spec in enumerate(node_specs):
        panel(ax, x_col[i], y_node, spec, NODE, NEDGE, min_w=colw,
              min_h=node_h, lw=1.6, **NODE_PAD)

    edges = [(x_root + root_w / 2, x_col[0] - colw / 2)] + \
            [(x_col[i] + colw / 2, x_col[i + 1] - colw / 2) for i in range(3)]
    for (x1, x2), text in zip(edges, F3_EDGES):
        _f3_arrow(ax, x1, y_node, x2, y_node, C.MUTED, arrows)
        ax.text((x1 + x2) / 2, y_node + 1.6 + edge_h / 2, text, fontsize=FS_EDGE,
                color=C.INK2, ha="center", va="center", style="italic",
                linespacing=1.35)

    # --- lane 2, the registered predictions ---------------------------------
    for i, stack in enumerate(pills):
        _f3_arrow(ax, x_col[i], y_node - node_h / 2, x_col[i], y_stack,
                  C.MUTED, arrows, lw=1.2)
        for j, (label, short, verdict) in enumerate(stack):
            glyph, fc, ec, gc = F3_VERDICT[verdict]
            cy = y_stack - pill_h / 2 - j * (pill_h + PILL_GAP)
            ax.add_patch(FancyBboxPatch(
                (x_col[i] - colw / 2, cy - pill_h / 2), colw, pill_h,
                boxstyle="round,pad=0.012,rounding_size=0.015",
                fc=fc, ec=ec, lw=1.1, zorder=3))
            left = x_col[i] - colw / 2 + PILL_PADX
            ax.text(left, cy, label, fontsize=FS_PILL, fontweight="bold",
                    color=gc, ha="left", va="center", zorder=4)
            ax.text(left + lab_w + 2.0, cy, short, fontsize=FS_PILL,
                    color=C.INK, ha="left", va="center", zorder=4)
            ax.text(x_col[i] + colw / 2 - PILL_PADX, cy, glyph, fontsize=FS_GLYPH,
                    color=gc, ha="right", va="center", zorder=4)

    # --- lane 3, the ledger -------------------------------------------------
    # The arrow says which entry came out of which experiment, and points at
    # the foot of that experiment's own stack of predictions.
    for x1, x2 in ties:
        _f3_arrow(ax, x1, y_ledger + ledger_h / 2, x2, y_stack - stack_h,
                  C.MUTED, arrows, lw=1.2)
    for i, spec in enumerate(ledger_specs):
        survives = ledger[i][4]
        fc, ec = (("#fdf3e3", C.ADVISORY) if survives else (BAD, BEDGE))
        panel(ax, x_led[i], y_ledger, spec, fc, ec, min_w=ledger_w,
              min_h=ledger_h, lw=2.0, **LEDG_PAD)

    # --- the key ------------------------------------------------------------
    y_key = y_ledger - ledger_h / 2 - GAP_LEDGER_KEY - key_h / 2
    entries = [("✓", GOOD, GEDGE, C.S6_GREEN, "confirmed"),
               ("✗", BAD, BEDGE, C.CRITICAL, "disconfirmed / eliminated"),
               ("◦", SEALED, SEDGE, C.MUTED, "neither"),
               ("", "#fdf3e3", C.ADVISORY, C.ADVISORY,
                "survives, its control unrun")]
    sw = key_h
    widths = [sw + 1.6 + measure(ax, t, FS_PILL)[0] for _, _, _, _, t in entries]
    kx = x_col[3] + colw / 2 - (sum(widths) + 4.0 * (len(entries) - 1))
    for (glyph, fc, ec, gc, text), wdt in zip(entries, widths):
        ax.add_patch(FancyBboxPatch((kx, y_key - sw / 2), sw, sw,
                                    boxstyle="round,pad=0.012,rounding_size=0.015",
                                    fc=fc, ec=ec, lw=1.1, zorder=3))
        if glyph:
            ax.text(kx + sw / 2, y_key, glyph, fontsize=FS_GLYPH, color=gc,
                    ha="center", va="center", zorder=4)
        ax.text(kx + sw + 1.6, y_key, text, fontsize=FS_PILL, color=C.INK2,
                ha="left", va="center")
        kx += wdt + 4.0

    # --- the layout, checked rather than eyeballed --------------------------
    short = [a for a in arrows
             if ((a[1][0] - a[0][0]) ** 2 + (a[1][1] - a[0][1]) ** 2) ** 0.5
             < F3_MIN_ARROW]
    if short:
        raise AssertionError("%d arrow(s) shorter than %.2f units, which is a "
                             "head with no shaft: %r"
                             % (len(short), F3_MIN_ARROW, short[0]))
    bad = collisions(fig, ax, pad_px=F3_TEXT_PAD)
    if bad:
        raise AssertionError("F3 layout: " + "; ".join(sorted(set(bad))))
    return save(fig, "F3_timeline.png")


# ---------------------------------------------------------------------------
# F4 - the paired flips, with the churn floor as a fourth panel
# ---------------------------------------------------------------------------

PANELS = [
    ("B", "Experiment 2\ntold how many stages are hidden",
     "claimed only\nwithout the warning", "claimed only\nwith the warning",
     "claude-opus-5_warn"),
    ("C1", "Experiment 3\ntold that stopping early is rewarded",
     "claimed only\nwithout the reward", "claimed only\nwith the reward",
     "claude-opus-5_ctrl"),
    ("C2", "Experiment 4\nshown the count at the decision point",
     "claimed only\nwithout the count", "claimed only\nwith the count",
     "claude-opus-5_count"),
    ("churn", "The churn floor\nthe same control, played twice",
     "claimed only\nthe first time", "claimed only\nthe second time", None),
]


def f4_paired_flips():
    fig, axes = plt.subplots(1, 4, figsize=(16.4, 5.6))
    fig.suptitle("Every task played both ways, one dot per task",
                 fontsize=13, fontweight="bold", y=0.99)
    for ax, (kind, title, lname, rname, lower) in zip(axes, PANELS):
        d = cells(kind)
        ax.set_xlim(-0.7, 11.0); ax.set_ylim(-4.8, 11.6); ax.axis("off")
        ax.set_title(title, fontsize=10.5, pad=6)
        order = [("both", d["both"], C.MUTED),
                 ("left", d["left_only"], C.ADVISORY),
                 ("right", d["right_only"], C.BINDING),
                 ("neither", d["neither"], None)]
        i, per = 0, 11
        for k, count, col in order:
            for _ in range(count):
                cx, cy = i % per, 10.6 - (i // per) * 0.95
                if k == "neither":
                    ax.plot([cx], [cy], marker="o", ms=7.6, mfc="none",
                            mec=C.BASELINE, mew=1.3)
                else:
                    ax.plot([cx], [cy], marker="o", ms=7.6, color=col,
                            alpha=0.42 if k == "both" else 1.0)
                i += 1
        legend = [("claimed under both", d["both"], C.MUTED, 0.42, True),
                  (lname.replace("\n", " "), d["left_only"], C.ADVISORY, 1.0, True),
                  (rname.replace("\n", " "), d["right_only"], C.BINDING, 1.0, True),
                  ("claimed under neither", d["neither"], C.BASELINE, 1.0, False)]
        for j, (lab, cnt, col, alpha, filled) in enumerate(legend):
            y = -0.55 - j * 0.66
            if filled:
                ax.plot([0], [y], marker="o", ms=7.6, color=col, alpha=alpha)
            else:
                ax.plot([0], [y], marker="o", ms=7.6, mfc="none", mec=col, mew=1.3)
            ax.text(0.7, y, str(cnt) + "  " + lab, fontsize=8.4, color=C.INK2,
                    va="center")
        moved = d["left_only"] + d["right_only"]
        tail = ("{} tasks played both ways\n{} changed answer  ·  p = {:.4f}"
                .format(d["n_paired"], moved, mcnemar_p(kind, lower))
                if lower else
                "{} tasks played both ways\n{} changed answer  ·  no test"
                .format(d["n_paired"], moved))
        ax.text(0, -3.85, tail, fontsize=8.8, color=C.INK, va="center",
                ha="left", fontweight="bold", linespacing=1.5)
    fig.text(0.5, 0.015,
             "The registered test reads only the tasks that changed answer. The "
             "grey and hollow dots are the tasks that did not. The fourth panel "
             "is the same control contract played twice, which is how much this "
             "setup moves on its own, and it carries no registered test.",
             fontsize=8.8, color=C.INK2, ha="center")
    fig.subplots_adjust(bottom=0.16, top=0.83)
    return save(fig, "F4_paired_flips.png")


# ---------------------------------------------------------------------------
# F5 - the capability ladder
# ---------------------------------------------------------------------------

def f5_capability_ladder():
    rows = table("T3")
    labels = [r["model"] for r in rows]
    rungs = [r["capability rung"] for r in rows]
    played = [int(r["tasks played"]) for r in rows]
    claimed = [int(r["times it said DONE"]) for r in rows]
    wrong = [int(r["times DONE was wrong"]) for r in rows]
    share = [float(r["share of tasks where it said DONE"]) for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0))
    fig.suptitle("Experiment 1: the stronger the model, the more it claims, "
                 "and the more of those claims are wrong",
                 fontsize=12.5, fontweight="bold", y=0.99)
    x = np.arange(len(rows))

    ax = axes[0]
    bars = ax.bar(x, claimed, 0.52, color=C.ADVISORY, zorder=3)
    ax.set_ylim(0, max(played) * 1.32)
    ax.set_xticks(x)
    ax.set_xticklabels([m + "\n" + r for m, r in zip(labels, rungs)], fontsize=9)
    ax.set_ylabel("tasks where it said DONE")
    ax.set_title("how often it claimed", fontsize=11, pad=10)
    ax.grid(axis="x", visible=False)
    ax.axhline(played[0], color=C.BASELINE, lw=1.1, ls="--", zorder=2)
    ax.annotate("all {} tasks".format(played[0]), (len(rows) - 1.35, played[0]),
                ha="left", va="bottom", fontsize=8.6, color=C.MUTED,
                xytext=(0, 4), textcoords="offset points")
    for rect, cl, pl, sh in zip(bars, claimed, played, share):
        cx = rect.get_x() + rect.get_width() / 2
        ax.annotate("{:.4f}".format(sh), (cx, rect.get_height()), ha="center",
                    va="bottom", fontsize=10, color=C.INK,
                    xytext=(0, 3), textcoords="offset points")
        ax.annotate("{} / {}".format(cl, pl), (cx, rect.get_height()),
                    ha="center", va="top", fontsize=9.5, color="#ffffff",
                    xytext=(0, -6), textcoords="offset points")

    ax = axes[1]
    bars = ax.bar(x, wrong, 0.52, color=C.CRITICAL, zorder=3)
    ax.set_ylim(0, max(max(wrong), 1) * 1.55)
    ax.set_xticks(x)
    ax.set_xticklabels([m + "\n" + r for m, r in zip(labels, rungs)], fontsize=9)
    ax.set_ylabel("claims that were wrong")
    ax.set_title("how many of those claims were wrong", fontsize=11, pad=10)
    ax.grid(axis="x", visible=False)
    for rect, w, cl in zip(bars, wrong, claimed):
        cx = rect.get_x() + rect.get_width() / 2
        ax.annotate("{} of {} claims".format(w, cl), (cx, rect.get_height()),
                    ha="center", va="bottom", fontsize=9.5, color=C.INK,
                    xytext=(0, 4), textcoords="offset points")
    fig.text(0.5, 0.015,
             "Both panels are ordered strongest to weakest by the capability "
             "rung fixed before the run. The left panel counts tasks, the right "
             "panel counts claims, so the two denominators differ and are "
             "printed on each bar.",
             fontsize=8.8, color=C.INK2, ha="center")
    fig.subplots_adjust(bottom=0.20, top=0.80, wspace=0.24)
    return save(fig, "F5_capability_ladder.png")


# ---------------------------------------------------------------------------
# F6 - the claim-timing signature
# ---------------------------------------------------------------------------

def f6_claim_timing():
    rows = table("T2")
    total = next(r for r in rows if r["experiment"] == "all eleven runs")
    per_run = [r for r in rows if r["experiment"] != "all eleven runs"]

    moments = [
        ("at the decision point,\nwith a stage still hidden",
         int(total["said DONE at the decision point"]),
         int(total["wrong at the decision point"])),
        ("once every stage\nhad been released",
         int(total["said DONE once every stage was released"]),
         int(total["wrong once every stage was released"])),
        ("before any test\nhad run",
         int(total["said DONE before any test had run"]),
         int(total["wrong before any test had run"])),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13.6, 4.9),
                             gridspec_kw={"width_ratios": [1.35, 1]})
    fig.suptitle("Where in an episode the model said DONE, and where it was wrong",
                 fontsize=12.5, fontweight="bold", y=0.99)

    ax = axes[0]
    y = np.arange(len(moments))[::-1]
    for yy, (lab, n, bad) in zip(y, moments):
        ax.barh(yy, n, 0.5, color=C.MUTED, alpha=0.35, zorder=3)
        if bad:
            ax.barh(yy, bad, 0.5, color=C.CRITICAL, zorder=4)
        ax.annotate("{} {} · {} wrong".format(n, "DONE" if n == 1 else "DONEs",
                                              bad), (n, yy),
                    va="center", ha="left", fontsize=10, color=C.INK,
                    xytext=(7, 0), textcoords="offset points")
    ax.set_yticks(y)
    ax.set_yticklabels([m[0] for m in moments], fontsize=9.4)
    ax.set_xlim(0, max(m[1] for m in moments) * 1.42)
    ax.set_xlabel("claims across the eleven runs")
    ax.set_title("the whole programme", fontsize=11, pad=10)
    ax.grid(axis="y", visible=False)

    ax = axes[1]
    names, at_d, elsewhere = [], [], []
    for r in per_run:
        arm = r["what the model was told it could do"].split(" (")[-1].rstrip(")")
        # Experiment 1 ran three models under one arm, so the arm code does not
        # separate its three bars and the model name does.
        second = (r["model"].replace("claude-", "").split("-")[0]
                  if r["experiment"] == "experiment 1" else arm)
        names.append(r["experiment"].replace("experiment ", "exp ") + "\n" + second)
        at_d.append(int(r["wrong at the decision point"]))
        elsewhere.append(int(r["wrong once every stage was released"])
                         + int(r["wrong before any test had run"]))
    x = np.arange(len(names))
    ax.bar(x, at_d, 0.56, color=C.CRITICAL, zorder=3,
           label="wrong at the decision point")
    ax.bar(x, elsewhere, 0.56, bottom=at_d, color=C.S1_BLUE, zorder=3,
           label="wrong anywhere else")
    ax.set_ylim(0, max(a + e for a, e in zip(at_d, elsewhere)) * 1.75)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=7.6)
    ax.set_ylabel("wrong claims")
    ax.set_title("by run", fontsize=11, pad=10)
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=8.6, loc="upper left")
    for xx, a, e in zip(x, at_d, elsewhere):
        if a + e:
            ax.annotate(str(a + e), (xx, a + e), ha="center", va="bottom",
                        fontsize=9, color=C.INK, xytext=(0, 3),
                        textcoords="offset points")
    fig.text(0.5, 0.015,
             "Every wrong claim in the programme but one was made at the "
             "decision point. The exception is a claim made before any test had "
             "run, which is drawn in blue on the second panel.",
             fontsize=8.8, color=C.INK2, ha="center")
    fig.subplots_adjust(bottom=0.23, top=0.82, wspace=0.30)
    return save(fig, "F6_claim_timing.png")


BUILDERS = [f1_harness_loop, f2_decision_point, f3_timeline, f4_paired_flips,
            f5_capability_ladder, f6_claim_timing]


def render_all():
    del _written[:]
    for b in BUILDERS:
        b()
    return list(_written)


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--layout", action="store_true",
                    help="report overlapping boxes and labels in each figure")
    args = ap.parse_args(argv)

    global LAYOUT
    LAYOUT = args.layout
    paths = render_all()

    if args.check:
        first = {p: digest(p) for p in paths}
        tmp = tempfile.mkdtemp()
        try:
            for p in paths:
                shutil.copy2(p, os.path.join(tmp, os.path.basename(p)))
            render_all()
            bad = 0
            for p in paths:
                same = digest(p) == first[p]
                bad += 0 if same else 1
                print(("PASS  " if same else "FAIL  ")
                      + os.path.basename(p).ljust(30)
                      + ("byte-identical" if same else "BYTES CHANGED"))
            print()
            print(str(len(paths)) + " figure(s), " + str(bad) + " not reproducible")
            return 1 if bad else 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    for p in paths:
        if args.hash:
            print(os.path.basename(p).ljust(30) + digest(p))
        else:
            print("wrote " + p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
