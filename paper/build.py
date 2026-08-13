"""Assemble the manuscript from the edited sections, and build the PDF.

    python3 -B build.py            # write manuscript/main.tex, main.html, main.pdf
    python3 -B build.py --no-pdf   # source only, skip the browser step

It also writes manuscript/overleaf/ and manuscript/overleaf.zip, which are the
same main.tex laid out flat with the figures beside it, for upload to a hosted
TeX service. See write_overleaf.

WHY TWO OUTPUT FORMATS. The benchmark paper is LaTeX and that is the format
this manuscript is written in, so `manuscript/main.tex` is the canonical
source and it compiles with `pdflatex` wherever a TeX distribution exists.
This machine has no TeX and no pandoc, so the PDF here is produced from a
second rendering of the same sections into HTML, printed by headless Chrome.
Both renderings come from one set of section files and one manifest, so they
cannot drift; what differs between them is typesetting, not content.

THE SECTION FILES ARE THE SOURCE. `draft/*.md` carries the prose that the
editorial pass in EDIT_LOG.md worked on. This script adds no prose. It supplies
the numbering, the floats, the captions and the front matter, and it fails
loudly rather than guessing when a float has no home.

FLOAT PLACEMENT is by marker. A section says `<!--FIG:F5-->` or `<!--TAB:T4B-->`
on its own line, at the point the float should appear, and this script replaces
the marker with the float. Figures are numbered by first appearance in reading
order, which is why the display numbers below are not the spec ids: the spec
ids are stable filenames and the display numbers are what a reader counts.
"""

import argparse
import csv
import html as htmllib
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(HERE, "draft")
FIGDIR = os.path.join(HERE, "figures")
TABDIR = os.path.join(HERE, "tables")
OUT = os.path.join(HERE, "manuscript")
os.makedirs(OUT, exist_ok=True)

TITLE = "Where a Coding Agent Decides It Is Finished"
SUBTITLE = ("Locating the Wrong Claim, and Three Explanations It Is Not")
AUTHOR = "Kushagra Bhatnagar"
DATE = "August 2026"

SECTIONS = [
    ("00_abstract.md",      None, "Abstract"),
    ("01_question.md",      1, "Question"),
    ("02_previous.md",      2, "What the previous work established, and what it could not"),
    ("03_instrument.md",    3, "The instrument"),
    ("04_decision_point.md", 4, "The decision point"),
    ("05_capability.md",    5, "Capability makes it worse"),
    ("06_information.md",   6, "It is not missing information"),
    ("07_incentive.md",     7, "It is not the incentive"),
    ("08_arithmetic.md",    8, "The arithmetic, at the decision point"),
    ("09_together.md",      9, "What the four experiments say together"),
    ("10_limitations.md",  10, "Limitations"),
    ("11_design.md",       11, "What this means for building agents, and reproducibility"),
    ("12_references.md",   12, "References"),
]

SCRIPT = "figures/make\\_figures.py"

# spec id -> (display number, file, caption). Display numbers run in order of
# first appearance in the assembled document, which is not the order of the
# spec ids; see the module docstring.
FIGURES = {
    "F1": ("1", "F1_harness_loop.png",
           "One turn of the harness, the rule that releases a hidden stage, "
           "and the channel the model may use to end the episode. The checker "
           "runs only the tests now visible and reports which of them failed. "
           "It also grades every submission against the hidden tests, and "
           "withholds that grade. A stage becomes visible only when every "
           "visible test passes, so passing everything visible is what buys "
           "the next stage rather than what ends the work. Replying DONE "
           "instead of code ends the episode, the whole suite is then run "
           "against the module as it stands, and the model is told neither "
           "whether the claim was right nor that it was scored at all. Drawn "
           "by \\texttt{" + SCRIPT + ":f1\\_harness\\_loop}."),
    "F2": ("2", "F2_decision_point.png",
           "The decision point. Every test the model can see is passing, that "
           "pass released a fresh stage, and at least one stage is still "
           "hidden. Saying DONE ends the episode on a guess. Submitting again "
           "costs nothing and releases the next stage. Drawn by "
           "\\texttt{" + SCRIPT + ":f2\\_decision\\_point}."),
    "F6": ("3", "F6_claim_timing.png",
           "Where in an episode the model said DONE, and where it was wrong. "
           "The left panel is the whole programme, with the wrong claims drawn "
           "in red inside each bar. The right panel repeats the split for each "
           "run that could claim. Drawn by \\texttt{" + SCRIPT +
           ":f6\\_claim\\_timing} from \\texttt{tables/T2.csv}."),
    "F5": ("4", "F5_capability_ladder.png",
           "Experiment 1 by capability rung, ordered strongest to weakest. The "
           "left panel counts tasks on which the model said DONE and the right "
           "panel counts the claims that were wrong, so the two denominators "
           "differ and each bar prints its own. Drawn by \\texttt{" + SCRIPT +
           ":f5\\_capability\\_ladder} from \\texttt{tables/T3.csv}."),
    "F4": ("5", "F4_paired_flips.png",
           "One dot per task, for the three paired comparisons and for the "
           "churn floor. The registered test reads only the solid dots, which "
           "are the tasks that changed answer. The fourth panel is the same "
           "control contract played twice and carries no registered test. "
           "Drawn by \\texttt{" + SCRIPT + ":f4\\_paired\\_flips} from "
           "\\texttt{declare/data/} through \\texttt{tables/make\\_tables.py}."),
    "F3": ("6", "F3_timeline.png",
           "\\textbf{The programme as an argument tree.} The spine is what was "
           "run: the four experiments in the order they ran, each with its date, "
           "its size and both of its arms, and each arrow carrying the question "
           "the next experiment inherited. Beneath each experiment are the "
           "predictions registered before it ran, one pill each, marked "
           "confirmed, disconfirmed or neither. Along the bottom is the ledger "
           "of candidate explanations: four struck out, and one left standing in "
           "amber rather than green because the placebo control that would show "
           "whether the content of the counter line or merely its presence did "
           "the work has not been run. Drawn by \\texttt{" + SCRIPT +
           ":f3\\_timeline} from \\texttt{declare/data/} and "
           "\\texttt{tables/T3.csv}, \\texttt{T4B.csv}, \\texttt{T6.csv}, "
           "\\texttt{T8.csv}."),
}

# Tables keep their spec ids as display numbers, because the prose was written
# against them and they already run in order of first appearance. T4B is a
# lettered supplement to T4 and is printed as such.
TABLES = ["T1", "T2", "T3", "T4", "T4B", "T5", "T6", "T7", "T8", "T9"]
TABLE_NUM = {t: t[1:] for t in TABLES}
TABLE_SOURCE = ("Regenerated from \\texttt{declare/data/} by "
                "\\texttt{tables/make\\_tables.py}.")

# Set smaller, for the tables that would otherwise overrun.
NARROW = {"T1", "T2", "T7", "T8", "T9"}

# Tables whose columns cannot all fit at their set size, filled in during the
# build and reported at the end. Empty is the passing state.
TIGHT = []


# ---------------------------------------------------------------------------
# Inline conversion
# ---------------------------------------------------------------------------

TEX_CHARS = [("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"),
             ("$", "\\$"), ("#", "\\#"), ("_", "\\_"),
             ("{", "\\{"), ("}", "\\}"), ("~", "\\textasciitilde{}"),
             ("^", "\\textasciicircum{}")]
TEX_UNI = [("\u00d7", "$\\times$"), ("\u2032", "$'$"), ("\u2212", "$-$"),
           ("\u00b7", "$\\cdot$"), ("\u2192", "$\\rightarrow$"),
           ("\u2014", "---"), ("\u2013", "--"), ("\u2018", "`"),
           ("\u2019", "'"), ("\u201c", "``"), ("\u201d", "''")]


def tex_escape(s):
    for a, b in TEX_CHARS:
        s = s.replace(a, b)
    for a, b in TEX_UNI:
        s = s.replace(a, b)
    return s


def inline(s, fmt):
    """Convert `code`, **bold** and *italic*, escaping everything else.

    Runs on the fragments between markup so an escape can never eat a control
    sequence this function just wrote.
    """
    out, i = [], 0
    pattern = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\*([^*]+)\*", re.S)
    for m in pattern.finditer(s):
        out.append(_plain(s[i:m.start()], fmt))
        code, bold, ital = m.group(1), m.group(2), m.group(3)
        if code is not None:
            out.append("\\texttt{%s}" % tex_escape(code) if fmt == "tex"
                       else "<code>%s</code>" % htmllib.escape(code))
        elif bold is not None:
            out.append("\\textbf{%s}" % _plain(bold, fmt) if fmt == "tex"
                       else "<strong>%s</strong>" % _plain(bold, fmt))
        else:
            out.append("\\emph{%s}" % _plain(ital, fmt) if fmt == "tex"
                       else "<em>%s</em>" % _plain(ital, fmt))
        i = m.end()
    out.append(_plain(s[i:], fmt))
    return "".join(out)


def _plain(s, fmt):
    return tex_escape(s) if fmt == "tex" else htmllib.escape(s)


# ---------------------------------------------------------------------------
# Floats
# ---------------------------------------------------------------------------

def figure_block(fid, fmt):
    num, fname, caption = FIGURES[fid]
    if fmt == "tex":
        return ("\\begin{figure}[t]\n\\centering\n"
                "\\includegraphics[width=\\textwidth]{%s}\n"
                "\\caption{%s}\n\\label{fig:%s}\n\\end{figure}" % (fname, caption, fid))
    cap = re.sub(r"\\texttt\{(.+?)\}", r"<code>\1</code>", caption)
    cap = cap.replace("\\_", "_")
    return ('<figure id="fig-%s">\n<img src="../figures/%s" alt="Figure %s">\n'
            '<figcaption><span class="lab">Figure %s.</span> %s</figcaption>\n'
            '</figure>' % (fid, fname, num, num, cap))


def read_table(tid):
    with open(os.path.join(TABDIR, tid + ".csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    md = open(os.path.join(TABDIR, tid + ".md"), encoding="utf-8").read()
    title = md.split("\n")[0].split(" — ", 1)[1].strip()
    cap = md.split("**Caption.**", 1)[1].strip()
    cap = re.sub(r"\s+", " ", cap)
    return rows[0], rows[1:], title, cap


# The text block is 5.6in wide, and a character of the body face is about half
# its point size. These are estimates and they only have to be conservative,
# because they are used to reserve space rather than to typeset.
TEXTWIDTH_PT = 5.6 * 72.27
CHAR_PT = {"\\scriptsize": 4.1, "\\small": 5.1}
TABCOLSEP_PT = 3.4


def longest_token(s):
    return max([len(t) for t in s.split() if t] or [1])


def column_weights(header, body, size):
    """Relative widths for the tabularx columns, from the content.

    Two different things decide a column's width. The floor is what must fit on
    one line: a cell of digits cannot be hyphenated and cannot be allowed to
    stick out into the gutter, so its longest cell reserves that much space,
    while a heading is prose that TeX will hyphenate and so reserves only a
    fraction of its longest word. The share above the floor is then divided in
    proportion to how much text each column carries, capped so that one long
    label column cannot take the whole row.

    Returns the weights, which sum to the column count and so make the table
    exactly \\textwidth wide, and whether the floors alone overran the row.
    """
    ncol = len(header)
    cw = CHAR_PT[size]
    avail = TEXTWIDTH_PT - 2 * TABCOLSEP_PT * ncol

    mins, wants = [], []
    for i, h in enumerate(header):
        cells = [r[i] for r in body if i < len(r)]
        cell_tok = max([longest_token(c) for c in cells] or [1])
        head_tok = longest_token(h)
        mins.append(max(cell_tok, head_tok * 0.6, 3.0) * cw * 1.05)
        wants.append(float(max(head_tok, min(max([len(c) for c in cells] or [1]),
                                             30), 4)))

    # water-fill: hand every column its proportional share, then pin the ones
    # that came in under their floor and redivide what is left among the rest
    pinned, w = set(), [0.0] * ncol
    while True:
        rest = [i for i in range(ncol) if i not in pinned]
        room = avail - sum(mins[i] for i in pinned)
        pool = sum(wants[i] for i in rest) or 1.0
        share = {i: room * wants[i] / pool for i in rest}
        short = [i for i in rest if share[i] < mins[i]]
        if not short or not rest:
            for i in rest:
                w[i] = share[i]
            for i in pinned:
                w[i] = mins[i]
            break
        pinned.update(short)

    tight = sum(w) > avail + 0.5
    if tight:                                  # floors do not fit; shrink all
        w = [v * avail / sum(w) for v in w]

    weights = [round(v * ncol / avail, 3) for v in w]
    widest = weights.index(max(weights))
    weights[widest] = round(weights[widest] + (ncol - sum(weights)), 3)
    return weights, tight


def table_block(tid, fmt):
    header, body, title, cap = read_table(tid)
    num = TABLE_NUM[tid]
    size = "\\scriptsize" if tid in NARROW else "\\small"
    if fmt == "tex":
        # Columns 1 and 2 carry the labels and are set ragged right; the rest
        # are quantities and are set ragged left. X columns rather than l and r
        # because a heading here is a phrase, and a phrase must be allowed to
        # wrap inside the column instead of overrunning the text block.
        ncol = len(header)
        weights, tight = column_weights(header, body, size)
        if tight:
            TIGHT.append(tid)
        kinds = ["L", "L"] + ["R"] * (ncol - 2) if ncol > 2 else ["L"] * ncol
        align = "".join("%s{%s}" % (k, w) for k, w in zip(kinds[:ncol], weights))
        lines = ["\\begin{table}[t]", "\\centering", size,
                 "\\setlength{\\tabcolsep}{3.4pt}",
                 "\\begin{tabularx}{\\textwidth}{%s}" % align, "\\toprule",
                 " & ".join("\\textbf{%s}" % tex_escape(h) for h in header) + " \\\\",
                 "\\midrule"]
        for r in body:
            lines.append(" & ".join(tex_escape(c) for c in r) + " \\\\")
        lines += ["\\bottomrule", "\\end{tabularx}",
                  "\\caption{\\textbf{%s.} %s %s}" %
                  (inline(title, "tex"), inline(cap, "tex"), TABLE_SOURCE),
                  "\\label{tab:%s}" % tid, "\\end{table}"]
        return "\n".join(lines)
    cells = ["<tr>" + "".join("<th>%s</th>" % htmllib.escape(h) for h in header) + "</tr>"]
    for r in body:
        cells.append("<tr>" + "".join("<td>%s</td>" % htmllib.escape(c) for c in r) + "</tr>")
    caph = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", cap)
    caph = re.sub(r"`(.+?)`", r"<code>\1</code>", caph)
    src = TABLE_SOURCE.replace("\\texttt{", "<code>").replace("}", "</code>") \
                      .replace("\\_", "_")
    return ('<div class="tablewrap" id="tab-%s">\n'
            '<table class="%s">%s</table>\n'
            '<div class="tabcap"><span class="lab">Table %s.</span> '
            '<strong>%s.</strong> %s %s</div>\n</div>'
            % (tid, "narrow" if tid in NARROW else "", "".join(cells),
               num, htmllib.escape(title), caph, src))


# ---------------------------------------------------------------------------
# Section conversion
# ---------------------------------------------------------------------------

MARKER = re.compile(r"^<!--(FIG|TAB):([A-Z0-9]+)-->$")
LISTITEM = re.compile(r"^(\d+)\.\s+(.*)$", re.S)


def convert_section(path, number, title, fmt, refs):
    raw = open(path, encoding="utf-8").read()
    paras = [p.strip() for p in raw.split("\n\n") if p.strip()]
    out = []
    if number is None:
        out.append("\\section*{\\centering Abstract}" if fmt == "tex"
                   else '<h2 class="abstract-head">Abstract</h2>')
    else:
        out.append("\\section{%s}" % tex_escape(title) if fmt == "tex"
                   else '<h2><span class="num">%d</span> %s</h2>'
                        % (number, htmllib.escape(title)))
    listbuf = []

    def flush_list():
        if not listbuf:
            return
        if fmt == "tex":
            out.append("\\begin{enumerate}\\setlength{\\itemsep}{4pt}")
            out.extend("\\item %s" % it for it in listbuf)
            out.append("\\end{enumerate}")
        else:
            out.append("<ol>" + "".join("<li>%s</li>" % it for it in listbuf) + "</ol>")
        del listbuf[:]

    for para in paras:
        if para.startswith("# "):
            continue
        m = MARKER.match(para.strip())
        if m:
            flush_list()
            kind, ident = m.groups()
            if kind == "FIG":
                if ident not in FIGURES:
                    sys.exit("unknown figure marker: " + ident)
                refs["fig"].add(ident)
                out.append(figure_block(ident, fmt))
            else:
                if ident not in TABLE_NUM:
                    sys.exit("unknown table marker: " + ident)
                refs["tab"].add(ident)
                out.append(table_block(ident, fmt))
            continue
        li = LISTITEM.match(para)
        if li:
            listbuf.append(inline(" ".join(li.group(2).split()), fmt))
            continue
        flush_list()
        text = " ".join(para.split())
        body = inline(text, fmt)
        # a paragraph opening with a bold run-in label becomes a run-in heading
        lab = re.match(r"^(\\textbf|<strong)", body)
        if fmt == "tex":
            out.append(body)
        else:
            cls = ' class="runin"' if lab else ""
            out.append("<p%s>%s</p>" % (cls, body))
    flush_list()
    return "\n\n".join(out)


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{newpxtext,newpxmath}
\usepackage[textwidth=5.6in,textheight=8.6in]{geometry}
\usepackage{microtype}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{graphicx}
\usepackage{float}
\usepackage{parskip}
\usepackage{xcolor}

% Weighted tabularx columns. The argument is the column's share of the row, and
% the shares of one table sum to its column count, so a table is exactly as
% wide as the text block whatever its headings say.
\newcolumntype{L}[1]{>{\hsize=#1\hsize\raggedright\arraybackslash}X}
\newcolumntype{R}[1]{>{\hsize=#1\hsize\raggedleft\arraybackslash}X}

% Both layouts of the sources are searched, so this file compiles unchanged
% from manuscript/ beside ../figures/ and from the flat Overleaf bundle.
\graphicspath{{figures/}{../figures/}{./}}
\definecolor{bindingblue}{HTML}{1668A1}
\usepackage[colorlinks=true,allcolors=bindingblue]{hyperref}

\makeatletter
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
  {1.25ex \@plus .5ex \@minus .2ex}%
  {-0.5em}%
  {\normalfont\normalsize\bfseries}}
\makeatother
\thickmuskip=3mu plus 2mu
\medmuskip=3mu plus 1mu minus 2mu
\frenchspacing
\makeatletter
\renewcommand\@seccntformat[1]{\csname the#1\endcsname\hspace{0.6em}}
\makeatother

\title{\LARGE TITLE\\[3pt]\large SUBTITLE}
\author{AUTHOR}
\date{DATE}

\begin{document}
\maketitle
"""

CSS = """
:root{--ink:#0b0b0b;--dim:#3d3c39;--rule:#c9c8bf;--accent:#1668A1;--surface:#ffffff}
@page{size:A4;margin:19mm 20mm 20mm 20mm}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);
 font:10.6pt/1.52 "Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;
 text-align:justify;hyphens:auto}
h1.title{font-size:20pt;line-height:1.22;text-align:center;margin:0 0 2pt;font-weight:700}
p.subtitle{font-size:12.4pt;text-align:center;color:var(--ink);margin:0 0 10pt;font-weight:600}
p.byline{text-align:center;color:var(--dim);margin:0 0 3pt;font-size:10.6pt}
p.dateline{text-align:center;color:var(--dim);margin:0 0 20pt;font-size:9.6pt}
h2{font-size:12.2pt;margin:19pt 0 6pt;font-weight:700;text-align:left;
 page-break-after:avoid;break-after:avoid}
h2 .num{color:var(--accent);margin-right:.55em}
h2.abstract-head{text-align:center;margin-top:0}
p{margin:0 0 7.5pt;orphans:3;widows:3}
p.runin strong:first-child{font-weight:700}
code{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.88em}
ol{margin:0 0 8pt 0;padding-left:1.35em}
li{margin:0 0 5.5pt;orphans:3;widows:3}
figure{margin:12pt 0 13pt;page-break-inside:avoid;break-inside:avoid}
figure img{width:100%;height:auto;display:block}
figcaption,.tabcap{font-size:8.9pt;line-height:1.42;color:var(--dim);
 margin-top:5pt;text-align:left}
.lab{font-weight:700;color:var(--ink)}
.tablewrap{margin:12pt 0 13pt;page-break-inside:avoid;break-inside:avoid}
.tabcap{margin:5pt 0 0}
table{border-collapse:collapse;width:100%;font-size:8.6pt;
 font-variant-numeric:tabular-nums}
table.narrow{font-size:7.5pt}
th,td{padding:2.6pt 4pt;text-align:right;vertical-align:top;
 hyphens:none;overflow-wrap:normal}
th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}
thead,tr:first-child{font-weight:700}
table tr:first-child th,table tr:first-child td{border-top:1.1pt solid var(--ink);
 border-bottom:.6pt solid var(--ink)}
table tr:last-child td{border-bottom:1.1pt solid var(--ink)}
.refs p{text-indent:-1.4em;padding-left:1.4em;margin-bottom:5pt}
"""


def tex_hanging(body):
    """Set every paragraph after the heading flush with a hanging indent."""
    parts = body.split("\n\n")
    return "\n\n".join([parts[0]] + ["\\hangindent=1.4em\\hangafter=1\\noindent "
                                     + p for p in parts[1:]])


OVERLEAF_README = """\
main.tex is the manuscript. It is generated by paper/build.py from the section
files in paper/draft/, the tables in paper/tables/ and the figures in
paper/figures/, and it is not edited by hand. Edit the sources and rebuild.

To compile it on a hosted TeX service:

  1. Upload this zip as a new project. It unpacks to main.tex, README.txt and
     figures/ with six PNGs.
  2. Set main.tex as the main document.
  3. Compile with pdfLaTeX. Two passes, because the cross-references to the
     figures and the tables resolve on the second.

Packages used, all of them in a full TeX Live: newpxtext, newpxmath, geometry,
microtype, booktabs, array, tabularx, graphicx, float, parskip, xcolor,
hyperref. Nothing is loaded from a local tree, so the project compiles as
uploaded.

The figure paths are bare file names and \\graphicspath searches figures/ and
../figures/, so the same main.tex compiles both here and in place inside the
repository.
"""


def write_overleaf(tex_text):
    """A flat bundle and a deterministic zip of it, for upload to Overleaf.

    Flat because a hosted project has no parent directory to reach into: the
    figures sit in figures/ beside main.tex. The zip is written with a fixed
    timestamp so that rebuilding produces the same bytes, which is the rule the
    rest of this directory follows.
    """
    dest = os.path.join(OUT, "overleaf")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.join(dest, "figures"))
    pngs = sorted(f for f in os.listdir(FIGDIR) if f.endswith(".png"))
    for f in pngs:
        shutil.copyfile(os.path.join(FIGDIR, f),
                        os.path.join(dest, "figures", f))
    with open(os.path.join(dest, "main.tex"), "w", encoding="utf-8") as f:
        f.write(tex_text)
    with open(os.path.join(dest, "README.txt"), "w", encoding="utf-8") as f:
        f.write(OVERLEAF_README)

    names = ["main.tex", "README.txt"] + ["figures/" + f for f in pngs]
    zpath = os.path.join(OUT, "overleaf.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(dest, n), "rb") as fh:
                z.writestr(info, fh.read())
    return dest, zpath, len(names)


def build_tex(bodies):
    pre = (PREAMBLE.replace("TITLE", TITLE).replace("SUBTITLE", SUBTITLE)
           .replace("AUTHOR", AUTHOR).replace("DATE", DATE))
    return pre + "\n\n" + "\n\n".join(bodies) + "\n\n\\end{document}\n"


def build_html(bodies):
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>%s</title><style>%s</style></head><body>' % (TITLE, CSS))
    front = ('<h1 class="title">%s</h1><p class="subtitle">%s</p>'
             '<p class="byline">%s</p><p class="dateline">%s</p>'
             % (TITLE, SUBTITLE, AUTHOR, DATE))
    return head + front + "\n".join(bodies) + "</body></html>"


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args(argv)

    refs = {"fig": set(), "tab": set()}
    tex, htm = [], []
    for fn, num, title in SECTIONS:
        path = os.path.join(DRAFT, fn)
        tex.append(convert_section(path, num, title, "tex", refs))
        htm.append(convert_section(path, num, title, "html",
                                   {"fig": set(), "tab": set()}))
    # the references section is set flush-and-hang in both renderings
    htm[-1] = htm[-1].replace("<h2>", '<div class="refs"><h2>', 1) + "</div>"
    tex[-1] = tex_hanging(tex[-1])

    missing_f = set(FIGURES) - refs["fig"]
    missing_t = set(TABLE_NUM) - refs["tab"]
    if missing_f or missing_t:
        sys.exit("floats defined but never placed: "
                 + ", ".join(sorted(missing_f | missing_t)))

    tex_text = build_tex(tex)
    with open(os.path.join(OUT, "main.tex"), "w", encoding="utf-8") as f:
        f.write(tex_text)
    with open(os.path.join(OUT, "main.html"), "w", encoding="utf-8") as f:
        f.write(build_html(htm))
    print("wrote manuscript/main.tex")
    print("wrote manuscript/main.html")
    print("placed %d figures and %d tables" % (len(refs["fig"]), len(refs["tab"])))
    if TIGHT:
        print("WARNING: columns do not fit at the set size in " +
              ", ".join(sorted(set(TIGHT))))

    _, zpath, nfiles = write_overleaf(tex_text)
    print("wrote manuscript/overleaf/ and %s (%d files)"
          % (os.path.relpath(zpath, HERE), nfiles))

    if args.no_pdf:
        return 0
    if not os.path.exists(CHROME):
        print("Chrome not found, skipping PDF; compile main.tex with pdflatex")
        return 0
    pdf = os.path.join(OUT, "main.pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    "--print-to-pdf=" + pdf,
                    "file://" + os.path.join(OUT, "main.html")],
                   check=True, capture_output=True)
    print("wrote manuscript/main.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
