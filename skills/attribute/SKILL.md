---
name: attribute
description: Determine the likely author of a text by comparing against a corpus of known authors. Use when the user wants authorship attribution or stylometric comparison.
---

# Authorship Attribution

Determine the likely author of a text by comparing against a corpus of known authors.

## Arguments

$ARGUMENTS should be: `<file> --corpus <corpus-dir>`

Both paths can be absolute or relative to the current working directory.

## Corpus Structure

The corpus directory should have one folder per author:
```
<corpus-dir>/
├── author1/
│   ├── text1.txt
│   └── text2.txt
├── author2/
│   └── text1.txt
└── author3/
    └── text1.txt
```

A default location for corpora is `~/.local/share/stilwerk/corpus/`.

## Process

1. **Validate inputs**
   - Query file must exist
   - Corpus directory must exist and contain author subdirectories

2. **Run attribution**
   ```bash
   stilwerk attribute <file> \
     --corpus <corpus-dir> \
     --n-features 100 --json
   ```

3. **Display results**
   - Most likely author
   - Distance score (lower = more similar)
   - Nearest neighbors ranked

## Example

```
/stilwerk:attribute mystery.txt --corpus ~/corpora/authors

Analyzing: mystery.txt
Comparing against: ~/corpora/authors/ (3 authors, 25 texts)

Attribution result:
  Most likely author: hamilton
  Distance: 0.423

Nearest neighbors:
  1. hamilton/fed51.txt: 0.423
  2. hamilton/fed72.txt: 0.445
  3. madison/fed10.txt: 0.512

Confidence: HIGH
```
