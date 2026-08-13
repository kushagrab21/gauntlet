# `paper/` — the assembled manuscript

The paper, its figures, its tables, and the scripts that regenerate all three
from the committed dataset. Nothing here calls a model and nothing here spends.

## Rebuild everything with one command

```bash
cd paper && ./rebuild.sh
```

That runs, in order: the tables from `declare/data/`, the six figures, the
manuscript assembly, and the verification suite. It ends on `ALL CHECKS PASS`
or exits non-zero.

The individual steps, if you want them separately:

```bash
cd paper/tables  && python3 -B make_tables.py          # T*.csv and T*.md
cd paper/figures && python3 -B make_figures.py         # F1..F6 png
cd paper         && python3 -B build.py                # main.tex, main.html, main.pdf
cd paper         && python3 -B verify.py               # the four checks
```

## Output

| path | what |
|---|---|
| `manuscript/main.tex` | the manuscript in the benchmark paper's LaTeX format. **This is the canonical source.** Compile with `pdflatex main.tex` wherever a TeX distribution exists |
| `manuscript/main.html` | the same manuscript rendered for the browser build |
| `manuscript/main.pdf` | 23 pages, built from `main.html` by headless Chrome |
| `manuscript/overleaf.zip` | the same `main.tex` with the six figures beside it, ready to upload to Overleaf |

## Compiling it on Overleaf

`manuscript/overleaf.zip` is the LaTeX, laid out flat because a hosted project
has no parent directory to reach into. Upload it as a new project, set
`main.tex` as the main document, and compile with pdfLaTeX twice so the figure
and table references resolve. `README.txt` inside the zip repeats this and lists
the packages, all of which are in a full TeX Live.

`build.py` writes the zip and the unpacked `manuscript/overleaf/` on every
build. Only the zip is committed, because the directory is a copy of `main.tex`
and `figures/*.png`. The zip is written with a fixed timestamp, so rebuilding
without changing a source produces the same bytes.

One `main.tex` serves both layouts. Figure paths are bare file names and
`\graphicspath` searches `figures/` and `../figures/`, so the file compiles
unchanged from the repository and from the bundle.

**This machine has no TeX**, so `main.tex` has never been compiled here. Check 5
of `verify.py` stands in for the compile: environments closed in order, braces
balanced, every table row matching its column spec, no unconverted markdown, and
the bundle carrying the same `main.tex` as the manuscript directory. What it
cannot catch is a bad line break or a float landing awkwardly, so read the first
Overleaf build before sending it anywhere.

**Why the PDF is not built from the LaTeX.** This machine has no TeX
distribution, no pandoc and no package manager, so `main.tex` cannot be
compiled here. `build.py` therefore emits two renderings of one set of section
files: the LaTeX for the owner's TeX, and an HTML rendering that Chrome prints.
They come from the same sources and the same manifest, so they cannot drift in
content. What differs is typesetting. Two things the LaTeX will do that the
browser build does not: page numbers, which Chrome's print path cannot place,
and float placement, which LaTeX will optimise and the browser build fixes
where the marker sits.

## Layout of this directory

| path | what |
|---|---|
| `draft/*.md` | the thirteen section files. **These are the prose source.** Everything else is generated |
| `build.py` | merges the sections, numbers the floats, resolves cross-references, writes the manuscript |
| `verify.py` | the five checks, runnable on its own: numbers, floats, terminology, the claims boundary, and the LaTeX source |
| `extract_numbers.py` | the before/after numbers safeguard |
| `tables/make_tables.py` | the ten tables, from `declare/data/`, importing the pinned exact tests from `declare.exact` |
| `tables/check_numbers.py` | 60 checks of `NUMBERS.md` against the dataset |
| `figures/make_figures.py` | the six figures. Every quantity read from a CSV, none written into the script |
| `figures/F*.md` | one specification per figure: what it shows, its data source, what a reader must be able to read off it |
| `STRUCTURE.md` | the benchmark paper recorded as a template contract |
| `OUTLINE.md` | the section map, and the deviations from `STRUCTURE.md` with reasons |
| `STYLE.md` | the register contract, from two readings of the benchmark |
| `LANGUAGE.md` | the writing rules, as amended by the owner rulings D1 and D2 |
| `NUMBERS.md` | every number the paper may assert, with its source |
| `EDIT_LOG.md` | 59 logged edits across five passes, and the five DECISIONS, all of them now ruled |

## The production rules this directory follows

Carried from the benchmark paper.

- **Every figure is drawn by a named committed script.** No figure is hand-made
  and none is edited after rendering. `make_figures.py --check` renders each one
  twice and requires the bytes to match, so a figure cannot drift silently.
- **Every data-driven figure reads a CSV.** No experimental number is written
  into `make_figures.py`. The paired cells that no table prints as a column are
  read through `tables/make_tables.py`, so a figure and the table beside it
  cannot disagree.
- **Every table carries a source line** naming the script and the dataset it
  came from, and regenerates byte-identically.
- **Every number in the prose appears in `NUMBERS.md`** with its provenance, and
  `verify.py` diffs the manuscript against that file.

## Figures

| in the paper | file | drawn by | data |
|---|---|---|---|
| Figure 1 | `figures/F1_harness_loop.png` | `make_figures.py:f1_harness_loop` | diagram |
| Figure 2 | `figures/F2_decision_point.png` | `make_figures.py:f2_decision_point` | diagram |
| Figure 3 | `figures/F6_claim_timing.png` | `make_figures.py:f6_claim_timing` | `tables/T2.csv` |
| Figure 4 | `figures/F5_capability_ladder.png` | `make_figures.py:f5_capability_ladder` | `tables/T3.csv` |
| Figure 5 | `figures/F4_paired_flips.png` | `make_figures.py:f4_paired_flips` | `declare/data/` via `make_tables.py` |
| Figure 6 | `figures/F3_timeline.png` | `make_figures.py:f3_timeline` | `declare/data/`, `T3.csv`, `T6.csv` |

Figure numbers run in order of first reference in the manuscript, which is not
the order of the file names. The file names are stable ids and the numbers are
what a reader counts.

## Tables

Ten, `T1` through `T9` with `T4B` as a lettered supplement to `T4`, printed with
those numbers because the prose was written against them and they already fall
in order of first reference.
