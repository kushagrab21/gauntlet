#!/bin/sh
# One command that rebuilds the paper from the committed dataset and verifies it.
# Calls no model and spends nothing.
set -e
cd "$(dirname "$0")"
echo "== tables ==";   (cd tables  && python3 -B make_tables.py)
echo "== figures ==";  (cd figures && python3 -B make_figures.py)
echo "== manuscript =="; python3 -B build.py
echo "== verify ==";   python3 -B verify.py
