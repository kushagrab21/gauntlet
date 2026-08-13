"""The five verification checks that must pass before the manuscript compiles.

    python3 -B verify.py

1. Every number in the manuscript appears in NUMBERS.md with its source.
2. Every figure referenced exists, every figure present is referenced, and
   every table regenerates byte-identically from the dataset.
3. Terminology is uniform: one name per concept, no section using a private
   synonym, and no raw spec id in published prose.
4. The claims boundary: the abstract and the conclusion assert nothing that the
   limitations retract, and the placebo confound appears in the Experiment 4
   results section and in the limitations in the same terms.
5. The LaTeX source is structurally sound and the Overleaf bundle matches it.
   This machine has no TeX, so these checks stand in for the compile.

Exits non-zero on the first failing check. Reads only committed files.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT = os.path.join(HERE, "draft")
FIGS = os.path.join(HERE, "figures")
TABS = os.path.join(HERE, "tables")
MS = os.path.join(HERE, "manuscript")

FAIL = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


def flat(path):
    return re.sub(r"\s+", " ", open(path, encoding="utf-8").read())


def drafts():
    return sorted(os.path.join(DRAFT, f) for f in os.listdir(DRAFT)
                  if f.endswith(".md"))


# --- 1. numbers -------------------------------------------------------------

def check_numbers():
    r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "extract_numbers.py"),
                        "--values", "--out", os.path.join(HERE, "numbers_after_values.txt")],
                       capture_output=True, text=True)
    if r.returncode:
        check("numbers extracted", False, r.stderr.strip()[:200])
        return
    a = open(os.path.join(HERE, "numbers_before_values.txt"), encoding="utf-8").read()
    b = open(os.path.join(HERE, "numbers_after_values.txt"), encoding="utf-8").read()
    n = len([x for x in b.split("\n") if x.strip()])
    check("numbers diff empty against the pre-assembly baseline", a == b,
          "%d numbers" % n)

    r = subprocess.run([sys.executable, "-B", os.path.join(TABS, "check_numbers.py")],
                       capture_output=True, text=True, cwd=TABS)
    tail = r.stdout.strip().split("\n")[-1] if r.stdout else ""
    check("NUMBERS.md recomputed from declare/data/", r.returncode == 0, tail)


# --- 2. figures and tables --------------------------------------------------

def check_assets():
    tex = open(os.path.join(MS, "main.tex"), encoding="utf-8").read()
    used = set(re.findall(r"\\includegraphics\[[^]]*\]\{([^{}]+\.png)\}", tex))
    disk = {f for f in os.listdir(FIGS) if f.endswith(".png")}
    check("every figure referenced exists", not (used - disk),
          "missing: " + ", ".join(sorted(used - disk)) if used - disk else
          "%d referenced" % len(used))
    check("every figure present is referenced", not (disk - used),
          "orphans: " + ", ".join(sorted(disk - used)) if disk - used else
          "%d on disk" % len(disk))

    specs = {f[:-3] for f in os.listdir(FIGS) if re.fullmatch(r"F\d+_.*\.md", f)}
    imgs = {f[:-4] for f in disk}
    check("every figure has a spec and every spec has a figure", specs == imgs,
          "specs %d, images %d" % (len(specs), len(imgs)))

    before = {f: open(os.path.join(TABS, f), "rb").read()
              for f in os.listdir(TABS) if re.fullmatch(r"T\d+B?\.csv", f)}
    subprocess.run([sys.executable, "-B", os.path.join(TABS, "make_tables.py")],
                   capture_output=True, cwd=TABS)
    same = all(open(os.path.join(TABS, f), "rb").read() == v
               for f, v in before.items())
    check("every table regenerates byte-identically", same,
          "%d tables" % len(before))

    r = subprocess.run([sys.executable, "-B", os.path.join(FIGS, "make_figures.py"),
                        "--check"], capture_output=True, text=True, cwd=FIGS)
    tail = r.stdout.strip().split("\n")[-1] if r.stdout else ""
    check("every figure renders byte-identically twice", r.returncode == 0, tail)


# --- 3. terminology ---------------------------------------------------------

# one concept -> (the name the paper uses, the synonyms it must not use)
TERMS = [
    ("the decision state", "decision point", [r"\bnode[ -]D\b", r"\bD[ -]node\b"]),
    ("a claim that was wrong", "wrong claim",
     [r"\bfalse claim\w*\b", r"\bfalse[- ]claiming\b"]),
    ("a withheld batch of tests", "stage", [r"\bwithheld modules?\b",
                                            r"\btest modules?\b"]),
]


def check_terminology():
    for concept, canonical, bad in TERMS:
        hits = []
        for p in drafts():
            t = flat(p)
            for pat in bad:
                for m in re.finditer(pat, t, re.I):
                    ctx = t[max(0, m.start() - 40):m.end() + 25]
                    # the one licensed mention: naming the predecessor's term
                    if "named this failure" in ctx:
                        continue
                    hits.append(os.path.basename(p) + ": " + m.group(0))
        check("one name for %s (%r)" % (concept, canonical), not hits,
              "; ".join(hits[:3]) if hits else "clean")

    leaks = []
    for p in drafts() + [os.path.join(TABS, f) for f in os.listdir(TABS)
                         if f.endswith(".md")]:
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            if i == 1 or line.lstrip().startswith("<!--"):
                continue
            for m in re.finditer(r"(?<![\w/])(T\d+B?|F\d+)(?![\w.])", line):
                leaks.append(os.path.basename(p) + ":" + str(i) + " " + m.group(0))
    check("no raw spec id in published prose", not leaks,
          "; ".join(leaks[:4]) if leaks else "clean")


# --- 4. claims boundary -----------------------------------------------------

CONFOUND = ("cannot separate the content of the counter line from the presence "
            "of an extra sentence of feedback")


def check_boundary():
    res = flat(os.path.join(DRAFT, "08_arithmetic.md"))
    lim = flat(os.path.join(DRAFT, "10_limitations.md"))
    check("the placebo confound appears in the Experiment 4 results section",
          CONFOUND in res)
    check("the placebo confound appears in the limitations, in the same terms",
          CONFOUND in lim)

    abstract = flat(os.path.join(DRAFT, "00_abstract.md"))
    concl = flat(os.path.join(DRAFT, "09_together.md"))
    check("the abstract states the control has not been run",
          "has not been run" in abstract)
    check("the conclusion states the control has not been run",
          "has not\nbeen run".replace("\n", " ") in concl
          or "has not been run" in concl)

    # nothing in the abstract or the conclusion may claim the mechanism is shown
    overclaim = re.compile(r"(demonstrat|establishes that the (failure|model)|"
                           r"proves|shows that the mechanism)", re.I)
    for name, text in (("abstract", abstract), ("conclusion", concl)):
        m = overclaim.search(text)
        check("the %s asserts nothing the limitations retract" % name, not m,
              m.group(0) if m else "clean")


# --- 5. the LaTeX source ----------------------------------------------------

# This machine has no TeX distribution, so main.tex cannot be compiled here and
# these checks stand in for the compile: the failures a generated .tex actually
# has are unbalanced environments, a row whose cell count does not match its
# column spec, and markdown that the converter failed to convert and left for
# the typesetter to print as literal asterisks.

ENV = re.compile(r"\\(begin|end)\{(figure|table|tabularx|enumerate|document)\}")
ROW = re.compile(r"^(?!\\)(.*?)\s*\\\\$")


def check_tex():
    path = os.path.join(MS, "main.tex")
    tex = open(path, encoding="utf-8").read()

    stack, bad = [], []
    for m in ENV.finditer(tex):
        kind, name = m.groups()
        if kind == "begin":
            stack.append(name)
        elif not stack or stack.pop() != name:
            bad.append(name)
    check("every LaTeX environment is closed in order", not bad and not stack,
          "unclosed: " + ", ".join(stack + bad) if (stack or bad)
          else "%d environments" % len(ENV.findall(tex)))

    # brace balance, ignoring the escaped braces the converter emits
    naked = re.sub(r"\\[{}]", "", tex)
    check("braces balance", naked.count("{") == naked.count("}"),
          "%d open, %d close" % (naked.count("{"), naked.count("}")))

    # every row of every tabularx has one cell per column
    wrong = []
    for block in re.findall(r"\\begin\{tabularx\}\{\\textwidth\}\{(.+?)\}\n(.*?)"
                            r"\\end\{tabularx\}", tex, re.S):
        spec, body = block
        ncol = len(re.findall(r"[LR]\{[\d.]+\}", spec))
        for line in body.split("\n"):
            m = ROW.match(line.strip())
            if not m or not m.group(1):
                continue
            cells = len(re.split(r"(?<!\\)&", m.group(1)))
            if cells != ncol:
                wrong.append("%d cells against %d columns" % (cells, ncol))
    check("every table row matches its column spec", not wrong,
          "; ".join(wrong[:3]) if wrong else "clean")

    # markdown the converter should have consumed
    left = re.findall(r"\*\*|(?<![\\\w])`", tex)
    check("no unconverted markdown in the LaTeX", not left,
          "%d marker(s) left" % len(left) if left else "clean")

    # the bundle is the same manuscript, laid out flat
    zpath = os.path.join(MS, "overleaf.zip")
    if not os.path.exists(zpath):
        check("the Overleaf bundle exists", False, "run build.py")
        return
    import zipfile
    with zipfile.ZipFile(zpath) as z:
        names = set(z.namelist())
        same = z.read("main.tex").decode("utf-8") == tex
    pngs = {"figures/" + f for f in os.listdir(FIGS) if f.endswith(".png")}
    check("the Overleaf bundle carries the same main.tex", same)
    check("the Overleaf bundle carries every figure", pngs <= names,
          "%d figure(s), %d file(s)" % (len(pngs), len(names)))


def main():
    print("--- 1. numbers ---")
    check_numbers()
    print("\n--- 2. figures and tables ---")
    check_assets()
    print("\n--- 3. terminology ---")
    check_terminology()
    print("\n--- 4. claims boundary ---")
    check_boundary()
    print("\n--- 5. the LaTeX source ---")
    check_tex()
    print()
    if FAIL:
        print("%d CHECK(S) FAILED: %s" % (len(FAIL), "; ".join(FAIL)))
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
