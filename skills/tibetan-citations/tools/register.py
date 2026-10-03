#!/usr/bin/env python3
"""
register.py -- safe maintenance of a sources register and a title glossary.

The register is append-only shared state: one row per quotation, keyed by unit and original
footnote number, compiled at final layout into the back-matter Sources register. Losing or
duplicating a row is silent and expensive, so every write goes through here.

REGISTER FORMAT (tab-separated, '#' comment lines preserved):
    chunk   unit_id   orig_fn   opening_words   work_and_locator
    dedup key: unit_id + orig_fn

GLOSSARY TITLE ROWS:
    TITLE   english_short_title   wylie_title   iast_title   locator
    dedup key: wylie_title

USE
    register.py --check  sources.tsv
    register.py --add    sources.tsv --chunk 05 --unit 1.3/12 --fn 214 \
                         --opening "For one who violates discipline" \
                         --locator "Tōh 373, DK vol. 78, f. 265a"
    register.py --titles glossary.tsv

--check   duplicates, malformed rows, empty or unlocated locators
--add     appends one row unless its key already exists (then it reports and changes nothing)
--titles  lists TITLE rows and flags drift: one Wylie title with two English forms, or one
          English form claimed by two Wylie titles
Exit status is non-zero when --check or --titles finds a problem.
"""
import argparse
import csv
import os
import sys

COLS = ["chunk", "unit_id", "orig_fn", "opening_words", "work_and_locator"]


def read_rows(path):
    if not os.path.exists(path):
        return [], []
    comments, rows = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                comments.append(line.rstrip("\n"))
                continue
            if not line.strip():
                continue
            rows.append(line.rstrip("\n").split("\t"))
    if rows and rows[0][:2] == COLS[:2]:
        rows = rows[1:]
    return comments, rows


def check(path):
    comments, rows = read_rows(path)
    bad = 0
    seen = {}
    for i, r in enumerate(rows, 1):
        if len(r) != len(COLS):
            print("  MALFORMED row %d: %d fields, expected %d -> %s"
                  % (i, len(r), len(COLS), "\t".join(r)[:90]))
            bad += 1
            continue
        key = (r[1], r[2])
        if key in seen:
            print("  DUPLICATE %s (rows %d and %d)" % (key, seen[key], i))
            bad += 1
        seen[key] = i
        loc = r[4].strip().lower()
        if not loc:
            print("  EMPTY LOCATOR  %s  %s" % (r[1], r[3][:60]))
            bad += 1
        elif "not located" in loc or "source not located" in loc:
            print("  UNLOCATED      %s  %s" % (r[1], r[3][:60]))
    print("  %d rows, %d problems" % (len(rows), bad))
    return bad


def add(path, chunk, unit, fn, opening, locator):
    comments, rows = read_rows(path)
    for r in rows:
        if len(r) == len(COLS) and (r[1], r[2]) == (unit, fn):
            print("  exists already: %s / fn %s -> %s" % (unit, fn, r[4][:70]))
            print("  nothing written")
            return 0
    new = [chunk, unit, fn, opening, locator]
    write_header = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if write_header:
            f.write("\t".join(COLS) + "\n")
        f.write("\t".join(new) + "\n")
    print("  appended: %s" % "\t".join(new))
    return 0


def titles(path):
    by_wylie, by_english, bad = {}, {}, 0
    with open(path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if not row or row[0] != "TITLE" or len(row) < 3:
                continue
            eng, wyl = row[1].strip(), row[2].strip()
            by_wylie.setdefault(wyl, set()).add(eng)
            by_english.setdefault(eng, set()).add(wyl)
    for wyl, engs in sorted(by_wylie.items()):
        if len(engs) > 1:
            print("  DRIFT  one Wylie title, %d English forms: %s -> %s"
                  % (len(engs), wyl[:40], " | ".join(sorted(engs))))
            bad += 1
    for eng, wyls in sorted(by_english.items()):
        if len(wyls) > 1:
            print("  DRIFT  one English title, %d Wylie titles: %s -> %s"
                  % (len(wyls), eng[:40], " | ".join(sorted(wyls))))
            bad += 1
    print("  %d TITLE rows, %d distinct works, %d problems"
          % (sum(len(v) for v in by_wylie.values()), len(by_wylie), bad))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("path")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--titles", action="store_true")
    ap.add_argument("--add", action="store_true")
    for o in ("chunk", "unit", "fn", "opening", "locator"):
        ap.add_argument("--" + o, default="")
    a = ap.parse_args()
    if a.titles:
        sys.exit(1 if titles(a.path) else 0)
    if a.add:
        if not (a.unit and a.fn):
            sys.exit("--add needs at least --unit and --fn")
        sys.exit(add(a.path, a.chunk, a.unit, a.fn, a.opening, a.locator))
    sys.exit(1 if check(a.path) else 0)


if __name__ == "__main__":
    main()
